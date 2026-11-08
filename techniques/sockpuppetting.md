---
id: sockpuppetting
name: Sockpuppetting (output-prefix injection)
year: 2026
tier: B
status: recommended
class: decoding-control
access: prefill-capable API or open weights
---

# Sockpuppetting

Pre-seed the assistant turn with an acceptance string. The model then completes a trajectory it has already committed to.

## Mechanism

The visible user prompt is benign. The attack lives in the assistant prefix (`"Sure, here is how to..."`) or, on open weights, inside the assistant block. Because the first tokens are supplied rather than sampled, the model's continuation is conditioned on having already accepted. No optimisation loop is required.

Reported as a cheap alternative to GCG, and stronger than it on open-weight models.

## Preconditions

- Ability to set the assistant turn prefix (prefill-capable API, or open weights).
- Not available on hardened chat APIs, which refuse assistant-role prefixes.

## Evidence

| Metric | Value | Target | Note |
|---|---|---|---|
| binary_ASR | 0.99 | Qwen3-8B | 3-variant prefill ensemble; Llama-3.1-8B 90%, Gemma-7B 22% |
| relative_ASR_gain | +82 pp | GCG baseline (reproduced) | prefill ensemble vs GCG |
| relative_ASR_gain | +64 pp | Llama-3.1-8B | RollingSockpuppetGCG, prompt-agnostic vs universal GCG |

Source: arXiv 2601.13359, "Sockpuppetting: Jailbreaking LLMs by Combining Prefilling with Optimization", 2026. Citation verified 2026-11-08.

## Defenses

- **Effective:** reject caller-supplied assistant prefixes; re-score the continued output against the original user request rather than against the prefix.
- **Only applies** where prefill is exposed. If it is not, the technique does not apply.

## Reliability note

Tier B, and conditionally so. Where the surface exists it is close to total for the price of one call; where it does not, it is zero. That binary nature is why it cannot be Tier A.
