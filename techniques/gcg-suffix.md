---
id: gcg-suffix
name: GCG adversarial suffix
year: 2023
tier: D
status: discarded
class: optimisation
access: white-box to optimise, black-box to apply
---

# GCG adversarial suffix

Gradient-search a token suffix that maximises the probability of an affirmative prefix.

## Mechanism

Greedy Coordinate Gradient replaces tokens one at a time using gradients from a white-box surrogate, maximising the likelihood of a target prefix such as `"Sure, here is"`. The resulting suffix is appended to the request. MAGIC and similar variants improve convergence.

## Preconditions

- White-box access to a surrogate model.
- GPU hours.

## Evidence

| Metric | Value | Target | Note |
|---|---|---|---|
| binary_ASR | 0.74 | Llama-2 | white-box, MAGIC variant |
| binary_ASR | 0.54 | GPT-3.5 | transfer, MAGIC |

Source: COLING 2025, "Exploiting the Index Gradients for Optimization-Based Jailbreaking"; TACL 2025, "Investigating Adversarial Trigger Transfer in Large Language Models".

## Why it is discarded

Three independent failures:

1. **High perplexity.** Suffixes are gibberish. A perplexity filter catches them, and the filter is cheap.
2. **Poor, inconsistent transfer.** A multi-model study across 13 open models found no reliable transfer pattern. The 54% GPT-3.5 figure did not reproduce broadly.
3. **Alignment beats direct optimisation.** RLHF/APO-aligned models resist triggers optimised *directly* against them, not just transferred ones.

## Defenses

- **Effective:** perplexity filtering plus alignment.
- **Do not rely on:** input keyword filters, which are why this technique was overrated for two years.

## Reliability note

Tier D as a black-box technique. It remains important as history: it is why the field learned that optimisation on a surrogate is not a transferable attack. That lesson is the transfer of value here, not the suffix.
