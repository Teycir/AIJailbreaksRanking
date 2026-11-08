---
id: many-shot
name: Many-shot Jailbreaking
year: 2024
tier: C
status: conditional
class: in-context
access: black-box
---

# Many-shot Jailbreaking

Pack tens to hundreds of fabricated Q&A turns in a single prompt showing the assistant complying, then append the target query.

## Mechanism

In-context learning is used against alignment. A long sequence of fabricated compliant exchanges establishes a pattern the model continues. Effectiveness scales with the number of shots and with context length, which is why it appeared as context windows grew (up to 256 shots in the reported work).

## Preconditions

- Very long context window.
- Token budget.

## Evidence

| Metric | Value | Target | Note |
|---|---|---|---|
| binary_ASR | 0.61 | Claude 2.0 | mitigated to 2% by prompt classification |

Source: Anthropic, "Many-shot jailbreaking", 2024-04-02.

## Defenses

- **Effective:** input prompt classification. 61% → 2%.
- **Contextual:** only a concern for long-context deployments; the attack costs tokens proportional to shots.

## Reliability note

Tier C, conditional. It was strong in 2024 and is largely neutralised by a control that is now standard. Retained because legacy and self-hosted long-context deployments may not run it.
