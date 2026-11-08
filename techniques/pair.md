---
id: pair
name: Prompt Automatic Iterative Refinement (PAIR)
year: 2023
tier: B
status: recommended
class: automated-iterative
access: black-box
---

# PAIR

Cheapest automated loop that still works. An attacker LLM proposes a prompt, the target answers, the attacker refines using that answer as feedback.

## Mechanism

Social-engineering feedback loop rather than token optimisation. The attacker model is told the objective and writes a candidate; the target's reply is fed back as "here is what happened, improve". Convergence in under twenty target queries is typical.

## Preconditions

- An attacker LLM.
- Query access to the target.

## Evidence

| Metric | Value | Note |
|---|---|---|
| queries_to_success | ~20 | order of magnitude cheaper than optimisation attacks |
| binary_ASR | ~0.60 | GPT-4, AdvBench subset, paper-era figure |

Source: IEEE SaTML 2025, "Jailbreaking Black Box Large Language Models in Twenty Queries" (Chao et al.).

## Defenses

- **Partial:** output filters raise the number of iterations.
- **Ineffective:** perplexity and gibberish filters, since the prompts are fluent.

## Reliability note

Tier B. Superseded by TAP on both ASR and cost, so treat PAIR as the cheap baseline component rather than the recommended primary. Its value is interpretability: every attempt is a readable sentence.
