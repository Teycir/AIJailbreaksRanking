---
id: low-resource-language
name: Low-resource language translation
year: 2023
tier: D
status: discarded
class: obfuscation
access: black-box
---

# Low-resource language translation

Translate the request into a language the model is less safety-trained on.

## Mechanism

Safety training is concentrated in high-resource languages. A request in Scots Gaelic, Zulu, or Hmong was reported to bypass refusal in 2023 and became a standard "high ASR" entry in jailbreak surveys.

## Preconditions

- Translation.

## Evidence — the collapse

| Metric | Value | Note |
|---|---|---|
| binary_ASR (keyword) | 0.96 | same responses, keyword evaluator |
| substance_ASR | 0.027 | same responses, StrongREJECT-style evaluator |

Source: arXiv 2610.26595, "Concerns in Benchmarking Jailbreaks: An Empirical Study of Attack Success Rates", 2026.

## Why it is discarded

The 96% figure is an evaluator artifact. Under substance scoring the outputs are incoherent or vacuous — the model produced *something* that avoided a refusal string, and the keyword judge counted it. A 93-point collapse is the largest recorded in the benchmarking literature.

## Defenses

- **Effective:** decode-then-classify. Nothing special is required.
- **Diagnostic value:** if a scanner reports this as high risk, the scanner is using keyword ASR in 2026.

## Reliability note

Tier D. This is the canonical example of why the catalog exists. Any number that survives only keyword matching is not evidence of capability.
