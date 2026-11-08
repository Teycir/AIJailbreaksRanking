# Taxonomy

Every technique is classified on three axes: **interaction shape**, **access requirement**, and **observable mechanism**. The `class` field in the catalog holds the interaction shape.

## Interaction shapes

| Class | What it means | Typical cost |
|---|---|---|
| `multi-turn` | Exploits conversation state; each turn uses prior output. | 2–10 turns |
| `sampling` | Same request, many variants; stop at first success. | 100–10 000 queries |
| `automated-iterative` | An attacker model proposes and refines. | 10–50 queries |
| `decoding-control` | Manipulates the generation path (prefix, grammar, logits) rather than the visible prompt. | 1 call |
| `framing` | Reframes the request as a persona, game, or code task. | 1 turn |
| `in-context` | Floods context with fabricated compliant examples. | 1 large prompt |
| `obfuscation` | Encodes or hides the request; model must reconstruct it. | 1 turn |
| `optimisation` | Gradient or search over tokens to maximise an affirmative prefix. | GPU hours |

## Access axis

| `access` | Meaning |
|---|---|
| `black-box` | Ordinary chat completions only. |
| `prefill` | Requires setting the assistant turn prefix. |
| `grammar` / `logit control` | Requires the caller to supply a schema or decoding constraint. |
| `white-box` | Requires weights or gradients. |

A technique that needs more than black-box access is not comparable to one that does not. `best-of-n` at N=10 000 and `gcg-suffix` are both expensive, but only the first is deployable against a closed API.

## Why this matters for reliability

The three axes predict failure modes:

- **Obfuscation** techniques fail when the model can decode, because policy is applied to the decoded form. High raw ASR, low durability.
- **Framing** techniques fail when the model has a trained refusal prior for the frame. They are the first thing patched.
- **Multi-turn** techniques fail only when per-turn evaluation is done, which most deployments do not do.
- **Sampling** techniques have no known mitigation at equal budget, so they stay reliable by construction.
- **Decoding-control** techniques fail when the deployment audits the decoding path. When it does not, they are near-total.

## Mapping to tiers

| Class | Usual tier | Reason |
|---|---|---|
| `sampling` | A | Power law; no equal-budget defense found. |
| `multi-turn` | A/B | Robust because defence is per-message, not per-conversation. |
| `automated-iterative` | B | Reliable but costs an attacker model. |
| `decoding-control` | B | Total when the surface exists, zero when it does not. |
| `framing` | C | Patched fastest. |
| `in-context` | C | Patched by input classification. |
| `obfuscation` | C/D | Decode-then-refuse, or evaluator artifact. |
| `optimisation` | D | Transfer failure. |
