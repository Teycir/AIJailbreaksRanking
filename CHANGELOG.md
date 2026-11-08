# Changelog

## 1.3.0 — 2026-11-08

Reliability is now stated per model family instead of per date. Jailbreaks
deprecate when a model generation changes, not when the calendar does.

### Added

- `works_best_on` (required) and `works_poorly_on` (optional) on every
  technique, populated only from the recorded evidence.
- `Best on` column replaces `Year` in the README table; `llms.txt` lines carry
  the same field.
- `scripts/query.py --model <substring>` filters across both lists.
- Validator enforces the field and its cross-file drift.

### Changed

- Tier wording is model-scoped: "Reliable on the named model families" rather
  than "reliable now". Tier C degrades "on current model families".
- Schema requires `works_best_on`.

## 1.2.0 — 2026-11-08

Renamed to **AIJailbreaksRanking** (old URLs redirect) and added a 20-second
promo animation.

### Added

- `video/` — Remotion composition `RankingPromo` (1920x1080, 30 fps, 4 scenes),
  rendered to `video/out/ranking.mp4`. Poster frame in `video/poster.jpg`.
- `# Video` section in the README.

### Changed

- Repository name and all internal references: `LatestAIJailbreaks` →
  `AIJailbreaksRanking`. Schema `$id`, `CITATION.cff`, `llms.txt`, query CLI
  docstring, badge and clone links updated.

## 1.1.0 — 2026-11-08

Correctness pass over every numeric claim, plus machine-checked consistency.

### Corrected

- `tap`: the 94% figure was misattributed to GPT-4o. TAP predates GPT-4o; the paper
  reports >80% on GPT-4, GPT-4-Turbo, PaLM-2 and Gemini-Pro with <30 target queries
  on average (Table 1 gives 70-90% per model). Removed the false 60%-fewer-queries
  claim, which came from a different method.
- `puzzled`: average is 88.8%, not 88.5%. Added the per-model split the abstract
  states (96.5% GPT-4.1, 92.3% Claude 3.7 Sonnet).
- `breakfun`: the "94% to 35%" ablation was not in the source. Replaced with what
  the paper actually says — the Trojan Schema is the primary causal factor, no
  single ablation number published.
- `pair`: `queries_to_success: 20` now states it is an upper bound ("fewer than
  twenty queries" in the abstract), not a measured average.

### Added

- `reported[].evaluator` on every entry, with an enum
  (`keyword-match`, `llm-judge-binary`, `substance-scored`, `human`, `qualitative`,
  `unspecified`). Schema now requires it, so the "every entry states its evaluator"
  claim is enforced rather than aspirational.
- `evidence[].verified_at` per source, plus `updated` on the catalog.
- `scripts/validate.py` — schema, tier/status coherence, Tier A/B cannot rest on
  `keyword-match` or `unspecified`, doc existence, and README/llms.txt drift.
- GitHub Actions workflow running the validator and query smoke tests.
- `CITATION.cff`.

### Notes

- `lrm-agent-persuasion`'s 5/900 mitigation figure was re-checked and is correct:
  five of 900 adversarial prompts reached maximum harm score with the immutable
  safety suffix.

## 1.0.0 — 2026-11-08

Initial public catalog: 17 techniques, tiers A-D, JSON Schema, query CLI, agent
files (`AGENTS.md`, `llms.txt`), per-technique docs and defense notes.
