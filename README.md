# AIJailbreaksRanking

![20-second promo: wordmark, tier distribution, and the 96.0% -> 2.7% evaluator drop](video/hero.gif)

*20 seconds, no narration. [1080p mp4](video/out/ranking.mp4) · [source and render notes](video/)*

A maintained, evidence-graded catalog of LLM jailbreak techniques — currently **17 entries** (3 reliable, 6 conditional, 5 historical, 3 discarded). Only techniques that hold up under substance-aware evaluation are marked reliable. Everything else is either marked conditional or explicitly discarded, with the reason on record.

Built for humans and for agents: every technique is a stable slug with structured metadata in [`data/techniques.json`](data/techniques.json).

[![schema](https://img.shields.io/badge/catalog-schema--validated-blue)](data/schema.json)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## What this is

- A **research index**, not a payload dump. Each entry documents mechanism, preconditions, reported effect size, evaluator type, and what actually defends against it.
- **Reliability-graded.** A technique moves to Tier A only if it survives substance scoring (StrongREJECT / HarmBench-class judges) and is reproduced by parties other than its authors.
- **Discard discipline.** Techniques whose headline numbers came from keyword-match ASR, or which do not transfer, are listed in Tier D with the failure evidence. The low-resource-language entry dropped from 96.0% to 2.7% under substance scoring — that is the single best example of why this repo exists.

## Tiers

Tiers are scoped to model generations, not to calendar time. A technique is graded against the models it was measured on, so read the **Best on** column before trusting a grade: it names the families where the result held, and per-model breakouts stay in `reported`. When a model generation changes, the entry needs re-testing, not a new date.

| Tier | Meaning | Count |
|------|---------|-------|
| **A** | Reliable on the named model families. Black-box, defense-robust, independently reproduced. | 3 |
| **B** | Reliable under a stated precondition (multi-turn, prefill, grammar control, long context). | 6 |
| **C** | Historical or heuristic. Degraded on current model families. | 5 |
| **D** | Discarded. Benchmark artifact, non-transferable, or fails substance scoring. | 3 |

## The short list

If you only read one table, read this one. Full metadata and sources are in the catalog.

| ID | Technique | Best on | Tier | Status | Access | Reported effect |
|----|-----------|---------|------|------|--------|-----------|-----------------|
| `crescendo` | Crescendo / Crescendomation | GPT-4, Gemini-Pro | **A** | recommended | black-box | 98% binary on GPT-4; 54.2% still succeeds vs circuit breakers |
| `lrm-agent-persuasion` | Autonomous LRM persuasion agent | frontier targets (9, aggregate) | **A** | recommended | black-box | 97.14% across 9 targets |
| `best-of-n` | Best-of-N augmentation sampling | GPT-4o, Claude 3.5 Sonnet | **A** | recommended | black-box | 89% GPT-4o @ N=10k; power law in N |
| `tap` | Tree of Attacks with Pruning | GPT-4, GPT-4-Turbo +2 | B | recommended | black-box | >80% GPT-4/Turbo/PaLM-2/Gemini, <30 queries avg |
| `pair` | PAIR iterative refinement | GPT-3.5, GPT-4 | B | recommended | black-box | < 20 queries to a working prompt |
| `deceptive-delight` | Deceptive Delight | 8-model average | B | recommended | black-box | 64.6% avg over 8 models, 3 turns |
| `sockpuppetting` | Output-prefix injection | Qwen3-8B, Llama-3.1-8B | B | recommended | prefill | 99% Qwen3-8B (3-variant prefill ensemble) |
| `control-plane-structured-output` | EnumAttack / DictAttack | gpt-5, gemini-2.5-pro +2 | B | recommended | grammar | 94.3–99.5% on gpt-5 / gemini-2.5-pro / deepseek-r1 |
| `breakfun` | Simulated code execution | open-weight models | B | recommended | black-box | 89% over 13 models |
| `many-shot` | Many-shot jailbreaking | Claude 2.0 | C | conditional | black-box | 61% Claude 2.0, cut to 2% by input classification |
| `puzzled` | Word-puzzle encoding | GPT-4.1, Claude 3.7 Sonnet | C | conditional | black-box | 88.8% avg, 96.5% GPT-4.1, heuristic class |
| `puzzler` | Implicit-clue guessing game | closed-source LLMs | C | conditional | black-box | 96.6% author-reported |
| `skeleton-key` | Skeleton Key | GPT-4o, Claude 3 Opus +5 | C | conditional | black-box | 7/7 models in 2024, since patched |
| `dan-persona` | DAN persona override | GPT-3.5 / GPT-4 (2023) | C | **discarded** | black-box | regression test only |
| `low-resource-language` | Translation attack | GPT-3.5 / GPT-4 (keyword-match only) | **D** | **discarded** | black-box | 96.0% keyword → **2.7%** substance |
| `encoding-cipher` | Base64 / cipher | small/old models (occasional) | **D** | **discarded** | black-box | model decodes, then refuses |
| `gcg-suffix` | GCG adversarial suffix | Llama-2 (white-box) | **D** | **discarded** | white-box | poor, inconsistent transfer across 13 models |

## Why some techniques get discarded

The catalog's value is the filter, not the list.

- **Keyword ASR is not a result.** A response that says "Sure, here's how" and then emits vague filler scores as a win under refusal-detection judges and as zero under substance judges. StrongREJECT exists precisely because this inflated most published numbers.
- **Single-generation success is not reliability.** At temperature 0.8, one request sampled 100 times went from 100% ASR (keyword) to 50% (substance) — and a single refusal masks residual unsafe behaviour. Reliability means *repeatable*.
- **High ASR + low prompt diversity = low practicality.** Heuristic attacks score high in isolation and near-zero behind a prompt classifier. This is why `puzzled` and `puzzler` sit at Tier C despite headline numbers.
- **Optimisation attacks do not transfer.** Triggers optimised on one model routinely fail on its sibling. High-perplexity suffixes are trivially filtered.

## Validation

```bash
python3 scripts/validate.py   # schema, tier discipline, README/llms.txt drift
python3 scripts/query.py --tier A
```

CI runs both on every push. Corrections are recorded in [CHANGELOG.md](CHANGELOG.md).

## Agent usage

Three retrieval paths, pick whichever fits:

**1. Structured catalog (preferred).**

```bash
jq '.techniques[] | select(.tier=="A") | {id, name, mechanism, reported}' data/techniques.json
```

**2. Helper CLI.**

```bash
python3 scripts/query.py --tier A                 # reliable techniques
python3 scripts/query.py --status discarded       # what failed and why
python3 scripts/query.py --id crescendo --json    # one record
python3 scripts/query.py --class multi-turn --md  # markdown rows
```

**3. Plain-text index.** [`llms.txt`](llms.txt) is a compact, ordered summary sized for direct context ingestion. [`AGENTS.md`](AGENTS.md) states the operating rules for agent use.

### Stable identifiers

Every technique has an `id` that will not change. Docs live at `techniques/<id>.md`. Frontmatter on each doc mirrors the JSON record, so either surface is safe to index.

## Repository layout

```
data/techniques.json    machine-readable catalog (validated against data/schema.json)
data/schema.json        JSON Schema 2020-12
techniques/<id>.md      one doc per technique, YAML frontmatter
docs/taxonomy.md        how techniques are classified
docs/reliability.md     the evaluation standard and why it matters
docs/defenses.md        what actually works, mapped per technique
scripts/query.py        catalog query helper (stdlib only)
llms.txt                flat index for LLM retrieval
AGENTS.md               agent operating rules
```

## Scope and use

This repo documents published research. It contains no working harmful payloads, no target lists, and no automation for producing harmful output. It is intended for red teams, safety evaluators, and defenders building detection and refusal systems.

If you operate a model or an agent, the useful reading order is `docs/defenses.md` first, then the Tier A entries to understand what your guardrails are actually being tested against.

## Contributing

Additions need a citation, a stated evaluator, and a sample size. Author-reported numbers are accepted but labelled. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT. See [`LICENSE`](LICENSE).
