---
id: best-of-n
name: Best-of-N (BoN) Jailbreaking
year: 2024
tier: A
status: recommended
class: sampling
access: black-box
---

# Best-of-N (BoN) Jailbreaking

Apply random surface augmentations to the same request and sample until one succeeds.

## Mechanism

The request is semantically identical every time; only presentation changes — token shuffling, capitalisation, character spacing, typography, image padding, audio pitch. Some fraction of variants slips past the guardrail. ASR follows a power law in the number of samples N, so reliability is bought with query volume rather than cleverness.

This is why BoN is the cleanest Tier A entry: it has no template to patch, no optimisation to detect, and no precondition beyond budget.

## Preconditions

- Query volume (N in the hundreds to tens of thousands).
- A grader to stop at first success.

## Evidence

| Metric | Value | Target | N |
|---|---|---|---|
| binary_ASR | 0.89 | GPT-4o, HarmBench | 10 000 |
| binary_ASR | 0.78 | Claude 3.5 Sonnet, HarmBench | 10 000 |
| binary_ASR | 0.41 | Claude 3.5 Sonnet, HarmBench | 100 |
| binary_ASR | 0.37 | o1, HarmBench | 5 000 |

Source: NeurIPS 2025 / arXiv 2412.03556, "Best-of-N Jailbreaking". Extends to vision (GPT-4o 56%) and audio (GPT-4o Realtime 72%). Composes with prefix attacks for a further ~35% gain.

## Defenses

- **Effective:** none at equal sample budget. This is the finding, not a gap in the literature.
- **Practical control:** per-objective sampling budgets, not per-request rate limits. At N=10 000, per-request checks see ten thousand benign-looking requests.
- **Ineffective:** circuit breakers, Cygnet, input filters.

## Reliability note

Tier A by construction. The honest framing is cost-based: "89% on GPT-4o at ten thousand samples" is the number, and the paper characterises the whole curve. Do not quote the top of the curve without N.
