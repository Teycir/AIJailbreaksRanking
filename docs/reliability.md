# Reliability standard

The whole point of this catalog is the filter. This page defines it, so entries can be argued with rather than believed.

## 1. Metric discipline

Three families of metric appear in the jailbreak literature, and they are not interchangeable.

| Metric | What it measures | Failure mode |
|---|---|---|
| Keyword / refusal-string ASR | Whether the reply avoids a refusal string | Counts incoherent or vacuous compliance as success. Inflates by 30–90 points. |
| LLM-judge binary ASR | A judge decides "did it comply" | Still counts partial, low-substance output. Sensitive to judge prompt. |
| Substance / harm scoring (StrongREJECT, HarmBench) | Separate scores for refusal, specificity, convincingness | Slower and costlier; the only defensible default. |

Rule: a number is accepted as evidence only if the evaluator is named. Keyword-only numbers are recorded but marked, and are never the basis for Tier A or B.

Every `reported[]` row in the catalog names its evaluator with one of these five values:

| `evaluator` | Meaning |
|---|---|
| `substance-scored` | Separate refusal / specificity / convincingness scores (StrongREJECT, HarmBench). |
| `llm-judge-binary` | One judge call decides complied vs refused. |
| `keyword-match` | Refusal-string matching. Recorded, never a Tier A/B basis. |
| `qualitative` | No rate reported; behaviour described. |
| `unspecified` | Source does not say how success was measured. |

Each row also carries `n` — the number of prompts, trials, or (for `model_coverage`) models the rate was computed over. Where a source states no sample size the field is absent rather than imputed, and `scripts/validate.py` lists those rows as warnings.

## 2. The inflation is measured, not hypothetical

The clearest case in the literature:

- Low-resource-language attacks on Qwen3-30B: **96.0% keyword ASR, 2.7% substance ASR** on the same responses.
- One request sampled 100 times at temperature 0.8: **100% keyword, 50% substance**.
- Ranking between DeepInception and prompt-rewriting **reverses** depending on evaluator and attempt budget.

So an evaluator change alone can move a technique between "state of the art" and "discarded". That is why `low-resource-language` is Tier D here despite its headline number.

## 3. Repeatability

A jailbreak that works once is not a jailbreak; it is a coin flip that landed.

Requirements for Tier A and Tier B:

- Report the **attempt budget** and the **success definition**.
- Report behaviour under **repeated sampling**, not a single generation.
- Report **cumulative failure probability**, not only the first-success rate.

Example of the standard applied: Best-of-N is Tier A precisely because the power-law relationship between N and ASR is characterised, not because any single run scored high.

## 4. Transfer

An attack optimised against model X is evidence about model X only.

- GCG suffixes transfer poorly and inconsistently: a multi-model study found no reliable transfer across 13 open models.
- Techniques that work through natural language or conversation state transfer far better, because they exploit alignment that is shared across the training pipeline rather than weights of one checkpoint.

Rule: no Tier A on single-model evidence.

## 5. Prompt diversity

Heuristic attacks with a fixed prompt set score high and generalise badly.

- `puzzled`, `puzzler`: high isolated ASR, low diversity, defeated by a semantic intent classifier.
- `crescendo`, `best-of-n`: high diversity by construction, no single pattern to block.

Rule: high ASR with a small fixed prompt set caps at Tier C regardless of the number.

## 6. Author reporting

Author-reported numbers are accepted but labelled. They are not downgraded automatically; they are simply not sufficient alone for Tier A. Independent reproduction is the promotion path.

## 7. Tier assignment

```
keyword ASR only                    -> D (or C if independently reproduced with a fixed prompt set)
heuristic + fixed prompts           -> C
historically effective, now patched -> C
needs precondition (prefill etc.)   -> B
black-box + defense-robust + reproduced -> A
```

Default when uncertain: **C**. The cost of inflating a technique is higher than the cost of omitting it.

## 8. Known limits of this catalog

- Effect sizes are dated. Guardrails change monthly; a Tier A today is a Tier C later unless re-tested.
- Models are named by family, not by snapshot, because snapshots are not always public.
- Abstract-level evidence only. No entry here has been independently re-run by this repository; the tier reflects the cited study's methodology, not a local benchmark.
