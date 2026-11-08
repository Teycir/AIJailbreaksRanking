---
id: tap
name: Tree of Attacks with Pruning (TAP)
year: 2023
tier: B
status: recommended
class: automated-iterative
access: black-box
---

# Tree of Attacks with Pruning (TAP)

Black-box automated jailbreak. An attacker LLM branches candidate prompts; an evaluator LLM prunes branches before they reach the target; surviving branches seed the next round.

## Mechanism

Two models, two roles. The attacker generates variants of the request. The evaluator scores each on likelihood of success. Only the top branches are sent to the target, which keeps the target-query budget low. Pruning happens *before* expensive calls, which is why TAP beats earlier automated methods on both ASR and cost.

## Preconditions

- An attacker LLM (any capable model).
- An evaluator LLM.
- Under 50 target queries.

## Evidence

| Metric | Value | Target | Note |
|---|---|---|---|
| binary_ASR | 0.94 | GPT-4o | 60% fewer queries than prior SOTA |
| binary_ASR | >0.80 | GPT-4-Turbo and GPT-4o | — |

Source: arXiv 2312.02119, "Tree of Attacks: Jailbreaking Black-Box LLMs Automatically" (Mehrotra et al.).

## Defenses

- **Partial:** LlamaGuard-class output filters. TAP still succeeds under 50 queries in the reported setting.
- **Better:** session-level anomaly detection — many semantically similar requests in one session.
- **Ineffective:** perplexity filters. The prompts are natural language.

## Reliability note

Tier B because the precondition is real: an attacker model plus budget. The natural-language surface is what makes it survive filters that kill suffix attacks. Quote 94% with "GPT-4o, attacker+evaluator LLM, <50 target queries".
