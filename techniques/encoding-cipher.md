---
id: encoding-cipher
name: Base64 / cipher obfuscation
year: 2023
tier: D
status: discarded
class: obfuscation
access: black-box
---

# Base64 / cipher obfuscation

Encode the request (Base64, ROT13, hex, leetspeak) and ask the model to decode and answer.

## Mechanism

The theory: the guardrail only recognises the request in plain text, so encoding hides it. The failure: models are trained to decode, and they apply policy to the decoded form. The result on modern models is decode-then-refuse.

## Preconditions

- Single turn.

## Evidence

| Metric | Value | Note |
|---|---|---|
| qualitative | — | modern models decode then refuse; occasional success only on small or old models |

Source: "JailbreakRadar", ACL 2025.

## Defenses

- **Effective:** nothing special — this is default behaviour now.
- **Negative control:** keep it in the catalog as the cheapest demonstration that obfuscation is not a bypass.

## Reliability note

Tier D. Retained as a negative control. Its continued citation in security writeups is a useful signal that the writer has not tested on a current model.
