---
id: lrm-agent-persuasion
name: Autonomous LRM persuasion agent
year: 2026
tier: A
status: recommended
class: multi-turn
access: black-box
---

# Autonomous LRM persuasion agent

A large reasoning model is given a harmful target and a system prompt, then plans and executes a multi-turn persuasion campaign against another model.

## Mechanism

The attacker model does not need jailbreak templates. It reasons about the target's refusals and composes tactics on the fly: rapport building, educational framing, hypotheticals, jargon flooding, gradual escalation, and reframing after each refusal. Because the tactics are generated rather than fixed, there is no surface pattern to block.

Reported as the first fully autonomous jailbreak agent architecture: attacker and target are both LLMs, no human in the loop.

## Preconditions

- An unaligned or weakly-aligned attacker model (an abliterated or minimally-RLHF'd open-weight model works).
- Multi-turn access to the target.

## Evidence

| Metric | Value | Target | Evaluator |
|---|---|---|---|
| binary_ASR | 0.9714 | 9 target models combined | human-validated harm score |

Source: Nature Communications 2026, "Large reasoning models are autonomous jailbreak agents" (s41467-026-69010-1).

## Defenses

- **Effective:** append an immutable safety suffix to every incoming message and evaluate the request together with that suffix. Reported drop to 5/900 adversarial prompts.
- **Cost:** measurable helpfulness reduction. This is the documented trade-off.
- **Ineffective:** style-based "detect persuasion" classifiers. The attacker adapts to them.

## Reliability note

Tier A: black-box, reproduced against nine targets, and it is the technique with the strongest published defense test. Quote the mitigation alongside the 97% figure, because without the suffix the attack is near-total and with it the attack is nearly eliminated. That is the most useful fact on this page.
