---
id: puzzler
name: Puzzler (implicit clues)
year: 2024
tier: C
status: conditional
class: obfuscation
access: black-box
---

# Puzzler

Never state the malicious intent. Feed implicit clues, let the model infer the target query, then answer the inferred query.

## Mechanism

A clue-generation step produces hints that together imply the request without containing it. The model reconstructs the intent itself, and therefore never sees an explicit harmful instruction to refuse. Evades jailbreak detectors better than explicit baselines.

## Preconditions

- Single turn.
- A clue-generation step.

## Evidence

| Metric | Value | Target | Note |
|---|---|---|---|
| query_success_rate | 0.966 | closed-source LLMs | author-reported |

Source: "Play Guessing Game with LLM: Indirect Jailbreak Attack with Implicit Clues", 2024.

> Citation check: the URL recorded for this entry is a secondary aggregator. Prefer the venue version when citing.

## Defenses

- **Effective:** semantic intent classification over the clue set. Clue sets repeat, so the classifier generalises.
- **Partial:** refusing "guess the word" framing.

## Reliability note

Tier C. Same profile as PUZZLED: high isolated ASR, small fixed prompt family, therefore defensible. Author-reported only, which is a second reason not to promote it.
