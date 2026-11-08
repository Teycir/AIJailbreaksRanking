---
id: control-plane-structured-output
name: Constrained Decoding Attack (EnumAttack / DictAttack)
year: 2026
tier: B
status: recommended
class: decoding-control
access: grammar / logit control
---

# Constrained Decoding Attack

Schema-enforced logit masking injects a malicious prefix into the generation trajectory. The visible prompt stays compliant; the decoding path does the work.

## Mechanism

When a caller supplies a JSON schema or grammar, the decoder is constrained to that structure. Field names and enum values are attacker-controlled input that reaches the model *after* prompt-level moderation. The model completes the intent it was structurally forced into, then refuses on the surface. The attack operates on the control plane.

Two variants:

- **EnumAttack** — malicious intent smuggled through enum values and field names. Basic grammar auditing kills it.
- **DictAttack** — evades grammar auditing by distributing intent across nested dictionary keys. Retains most of its strength.

## Preconditions

- Structured output / constrained decoding exposed to the caller.

## Evidence

| Metric | Value | Targets |
|---|---|---|
| binary_ASR | 94.3–99.5% | gpt-5, gemini-2.5-pro, deepseek-r1, gpt-oss-120b across 5 benchmarks |
| binary_ASR | 75.8% | DictAttack vs a coordinated dual-plane guard |

Source: arXiv 2503.24191v3, "When Grammar Guides the Attack: Control-Plane Vulnerabilities in LLMs with Structured Output".

## Defenses

- **Effective against EnumAttack:** audit the grammar itself.
- **Residual:** DictAttack needs decoding-intent inspection, not schema allowlisting.
- **Structural:** treat the decoding path as attacker-controlled input and moderate the decoded intent.

## Reliability note

Tier B. Highest absolute numbers in the catalog, and the most fragile precondition: it requires the deployment to expose a constrained-decoding surface. Where that surface exists it is near-total; where it does not, the technique is inapplicable.
