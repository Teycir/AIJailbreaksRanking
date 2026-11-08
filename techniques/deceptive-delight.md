---
id: deceptive-delight
name: Deceptive Delight
year: 2024
tier: B
status: recommended
class: multi-turn
access: black-box
---

# Deceptive Delight

Three-turn camouflage. A benign topic and an unsafe topic are linked in a story, then both are expanded, then only the unsafe one is expanded.

## Mechanism

- Turn 1: ask for a short story that *combines* one unsafe topic with two benign ones.
- Turn 2: ask to expand each of the three topics in more detail.
- Turn 3: ask specifically to expand the unsafe one.

The unsafe content is a minority of the semantic mass in turns 1–2, so per-message classifiers see a mostly benign request. The model has already committed to the topic set by turn 3.

## Preconditions

- 2–3 turns with retained conversation state.

## Evidence

| Metric | Value | Setup |
|---|---|---|
| binary_ASR | 0.646 | 8 models averaged, 40 unsafe topics × 5 cases × 5 repeats (≈8 000 cases) |
| binary_ASR | 0.058 | baseline, direct request on the same set |

Source: Palo Alto Unit 42, "Deceptive Delight: Jailbreak LLMs Through Camouflage and Distraction", 2024-10-23.

## Defenses

- **Effective:** conversation-level intent tracking. The unsafe mass becomes visible across turns 1–2.
- **Ineffective:** per-message moderation, which sees only benign topics in the early turns.

## Reliability note

Tier B. ASR is highest at turn 3 and drops at turn 4 as the expanding unsafe content trips filters, so the technique has an expiry point built into it. That makes it reliable but not unbounded.
