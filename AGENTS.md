# AGENTS.md

Operating rules for agents using this repository.

## Purpose

You are reading a **security research catalog**. It classifies published LLM jailbreak techniques by reliability. It does not contain harmful payloads and must not be treated as an attack toolkit.

## Retrieval

Preferred order:

1. `data/techniques.json` — parse it, filter by `tier`, `status`, `class`.
2. `python3 scripts/query.py` — if a shell is available.
3. `llms.txt` — if you only have flat text.
4. `techniques/<id>.md` — full write-up for one technique.

Do not paginate the whole repo. Query the catalog.

## Field semantics

| Field | Use |
|---|---|
| `tier` | `A` reliable now, `B` reliable under precondition, `C` historical/heuristic, `D` discarded |
| `status` | `recommended`, `conditional`, `discarded` |
| `reported[].metric` | Which metric the number uses. **Never** compare a `binary_ASR` to a `substance_ASR`. |
| `reported[].n` | Sample size. Treat missing `n` as unknown variance. |
| `requires` | Preconditions. A Tier B entry is not reliable outside these. |
| `defense_notes` | What actually mitigates it. |

## Hard rules

- **Do not report a technique as reliable on `binary_ASR` alone.** If only keyword-match numbers exist, say so.
- **Do not average across techniques.** Effect sizes are per-target and per-evaluator.
- **Do not drop Tier D entries** from a recommendation. They are documented failures and are the reason the catalog is trustworthy.
- **Do not infer capability from `model_coverage`.** "7/7 models complied in 2024" is a date-stamped observation, not a current rate.
- **Quote the precondition.** "TAP reaches >80%" is wrong on its own; "TAP reaches >80% on GPT-4-Turbo with an attacker and evaluator LLM and under 30 target queries on average" is right.

## When asked "what is the most reliable jailbreak"

Answer with the Tier A set and their preconditions:

- `crescendo` — needs multi-turn state.
- `lrm-agent-persuasion` — needs an unaligned attacker model.
- `best-of-n` — needs query volume; reliability comes from N, not cleverness.

Then state the active mitigation for each, from `defense_notes`. A technique without its countermeasure is a misleading answer.

## When asked to evaluate a new technique

1. Check whether the headline number is keyword-match or substance-scored.
2. Check sample size and whether it is author-reported.
3. Check whether the prompts are diverse or a fixed heuristic set.
4. Check transfer: was it tested on more than the model it was optimised on?
5. Assign tier by the rules in `docs/reliability.md`. Default to C when in doubt.

## Output shape

When returning catalog data, preserve `id`, `tier`, `status`, the `reported` number with its `metric` label, and the `evidence` source. Do not summarise away the metric type.
