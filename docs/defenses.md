# Defenses

Mapped to the catalog. The short version: **per-message input filtering is not a defense** against anything in Tier A.

## Summary

| Control layer | Stops | Does not stop |
|---|---|---|
| Input classification / prompt modification | many-shot (61%→2%), heuristic obfuscation | multi-turn, sampling |
| Output harm classifier | low-substance compliance | high-substance compliance |
| Per-turn safety judge (whole transcript) | crescendo partially (→54.2%) | best-of-n at scale, LRM agents |
| Immutable safety suffix | LRM agent (5/900 succeed) | best-of-n, TAP |
| Circuit breakers (representation-level) | single-turn attacks (→3.8%) | crescendo (54.2% persists), sampling |
| Grammar / decoding-path audit | EnumAttack | DictAttack (75.8% residual) |
| Refuse assistant-prefill | sockpuppetting | everything else |
| Rate limiting + budget accounting | nothing, but makes best-of-n visible | best-of-n if budget is generous |

## Per-technique

### `crescendo` (A)
- **Works:** score the whole conversation against the objective, not each message. Red-teaming literature shows a conversation-level judge is the only control that materially reduces it.
- **Partially works:** circuit breakers cut it from ~98% to 54.2%. That is a real reduction but not a fix.
- **Fails:** keyword filters, single-message moderation. Each individual turn is benign by design.

### `lrm-agent-persuasion` (A)
- **Works:** an immutable safety suffix appended to every incoming message, evaluated with the request. Reported reduction to 5/900.
- **Cost:** measurable helpfulness loss. This is the cleanest documented trade-off in the corpus.
- **Fails:** detecting "persuasion" as a style. The attacker adapts.

### `best-of-n` (A)
- **Works:** nothing at equal budget. Sampling defeats circuit breakers and Cygnet.
- **Practical control:** account for total sampling per objective, not per request. At N=10 000 the attack is invisible to per-request checks.
- **Fails:** input filtering, because each variant is individually benign-looking.

### `tap` / `pair` (B)
- **Works:** LlamaGuard-class output filters raise cost (TAP still succeeds under 50 queries in the reported setting).
- **Works better:** anomaly detection on query *patterns* — a single session issuing many semantically similar requests is the signal.
- **Fails:** perplexity filters. These attacks are natural language.

### `deceptive-delight` (B)
- **Works:** conversation-level intent tracking; the unsafe mass becomes visible at turn 2–3.
- **Fails:** per-message classifiers, which see only benign topics.

### `sockpuppetting` (B)
- **Works:** do not accept an assistant-role prefix from the caller. Re-score the continued output against the user request.
- **Only relevant** where prefill is exposed. If it is not exposed, the technique does not apply.

### `control-plane-structured-output` (B)
- **Works:** audit the grammar itself. Basic grammar auditing eliminates EnumAttack.
- **Residual:** DictAttack keeps 75.8% against a coordinated dual-plane guard, so decoding-intent inspection is required, not schema allowlisting alone.

### `breakfun` (B)
- **Works:** APD — transcribe all readable text in the input before judging it, so the Trojan Schema fields are evaluated as content.
- **Evidence:** removing the schema drops ASR 94%→35%; that is the size of the effect you are defending against.

### `many-shot` (C)
- **Works:** input prompt classification. 61%→2%.
- **Note:** cost scales with context length, so it is only a concern for long-context deployments.

### `puzzled` / `puzzler` (C)
- **Works:** solve the puzzle, then classify the solved form. Semantic intent classifiers generalise over the fixed clue sets.
- **Fails:** refusing "puzzle" requests wholesale — legitimate use is common.

### `skeleton-key` / `dan-persona` (C)
- **Works:** current models handle both. Keep them as regression tests: a deployment that answers either has no guardrail.
- **Value:** cheap, high-signal smoke test, not a threat.

### `low-resource-language`, `encoding-cipher`, `gcg-suffix` (D)
- **Works:** nothing special. Decode-then-classify handles the first two; perplexity filters plus alignment handle the third.
- **Why they are here:** they are the negative controls. If a scanner flags them as high risk, the scanner is using keyword ASR.

## The structural point

Guardrails are applied per message. Three of the three Tier A techniques operate *between* messages or *across* samples. That mismatch — not any single missing filter — is why the Tier A set stays reliable.

Fix the aggregation layer first:

1. Judge the conversation, not the turn.
2. Budget the sampling, not the request.
3. Treat the decoding path as attacker-controlled input.
