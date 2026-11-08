---
id: breakfun
name: BreakFun (simulated code execution)
year: 2026
tier: B
status: recommended
class: framing
access: black-box
---

# BreakFun

Give a benign-looking Python class with adversarial field names, then ask what the code would print. Harmful content emerges as a side-effect of simulated instantiation.

## Mechanism

The "Trojan Schema" is a plain class definition. Its class name and field names carry the request. The model is asked to mentally execute it and report output. Safety reasoning is focused on the code, not the field contents, so the harmful text is produced as a computed value.

Single turn. No optimisation, no conversation state.

## Preconditions

- None beyond ordinary chat access.

## Evidence

| Metric | Value | Target |
|---|---|---|
| binary_ASR | 0.89 | 13 models averaged, JailbreakBench |
| binary_ASR | ~0.98 | open-weight tier |
| binary_ASR | ~0.78 | API tier |

Ablation: removing or altering the Trojan Schema is the largest single drop in the study, which localises the effect to the schema fields. The abstract confirms the schema is the primary causal factor but publishes no single ablation number.

Source: arXiv 2510.17904, "BreakFun: Jailbreaking LLMs via Object Instantiation under Simulated Code Execution".

## Defenses

- **Effective:** APD — transcribe all readable text in the input before judging it, so schema field names are evaluated as content.
- **Ineffective:** refusing code-execution requests wholesale; legitimate use is common.

## Reliability note

Tier B, near A. Black-box, single-turn, and the highest single-turn ASR in the catalog. Kept at B only because the evidence is recent and less independently reproduced than Crescendo.
