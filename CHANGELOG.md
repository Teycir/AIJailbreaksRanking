# Changelog

Every entry in this catalog can be traced to a tag. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html) — a Minor bump means
the schema or a grade can change, a Patch means wording only.

## [Unreleased]

### Added

- Flat CSV export: `data/techniques-summary.csv` and generator `scripts/export_summary.py`.
- `--csv` format support in `scripts/query.py`.
- Interactive web catalog viewer: `docs/index.html` with real-time text search, tier filtering, and offline fallback data.
- "Why this exists" callout box in `README.md` explaining the 96.0% → 2.7% evaluator illusion in plain language.
- "Quick start for defenders" section in `README.md` summarizing the 5 highest-impact architectural mitigations.
- Structured GitHub Issue Forms (`.github/ISSUE_TEMPLATE/new_technique.yml`, `.github/ISSUE_TEMPLATE/data_correction.yml`) and PR template (`.github/PULL_REQUEST_TEMPLATE.md`).
- Active Tier A candidates and promotion gates tracker: `docs/candidates.md`.
- v1.0 Launch announcement drafts for X, LinkedIn, and Reddit: `docs/announcement_v1.md`.
- Citation snippet and metadata synchronization between `CITATION.cff`, `data/techniques.json`, and `README.md`.
- Validation checks for `data/techniques-summary.csv`, `verified_at`, and `CITATION.cff` version alignment.

### Changed

- Added `verified_at` date tracking per technique in `data/schema.json` and `data/techniques.json`.
- Expanded README badges to highlight substance scoring standard, graded count, and citable metadata.

## [1.6.0] - 2026-11-08

Three worked examples per technique, and a link check that leaves a trace.

### Added

- `scripts/check_links.py` with a weekly `links` workflow: every
  `evidence[].url` is fetched and a dead source fails the run. Bot walls
  (403/429) warn.
- `tests/test_validate.py`: ten negative controls, each breaking one invariant
  against a temp copy of the catalog, wired into CI.
- Validator guards: `docs/defenses.md` coverage, `docs/taxonomy.md` class
  definitions, `docs/reliability.md` evaluator and tier vocabulary, the
  three-example shape, and the freshness stamp.
- README: badge header, `## Contents` index, and an ETH support block.

### Changed

- `example` → `examples`: every technique carries three worked examples — the
  paper's run, a second run, and the case where the technique stops working.
  Docs render them under `## Examples`.
- 11 `reported[]` rows gained `n`, the sample size stated by the source. Rows
  whose source states no sample size stay empty and are reported as validator
  warnings rather than imputed.
- Green link checks stamp `sources_last_checked` into the catalog; CI commits
  the stamp and the README shows the date.

## [1.5.0] - 2026-11-08

Worked examples.

### Added

- `## Example` in every technique write-up: the paper's target, a harmless
  stand-in, a short transcript, and one line on why the mechanism lands.
- `example` in the catalog (required by the schema), so agents querying JSON
  get the same worked example the docs show.
- Validator: every doc must carry an `## Example` section matching its catalog
  entry.

## [1.4.0] - 2026-11-08

Readability pass on the short list.

### Added

- `Last assessed` line above the tier table, sourced from `updated` in the
  catalog.
- `Technique index` after the short list: one plain-language paragraph per
  technique, anchored so the table's name cell links straight to it.

### Changed

- Short-list technique names are links to their index anchor.

## [1.3.0] - 2026-11-08

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

## [1.2.0] - 2026-11-08

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

## [1.1.0] - 2026-11-08

Correctness pass over every numeric claim, plus machine-checked consistency.

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

### Fixed

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

### Notes

- `lrm-agent-persuasion`'s 5/900 mitigation figure was re-checked and is correct:
  five of 900 adversarial prompts reached maximum harm score with the immutable
  safety suffix.

## [1.0.0] - 2026-11-08

Initial public catalog: 17 techniques, tiers A-D, JSON Schema, query CLI, agent
files (`AGENTS.md`, `llms.txt`), per-technique docs and defense notes.

[Unreleased]: https://github.com/Teycir/AIJailbreaksRanking/compare/v1.6.0...HEAD
[1.6.0]: https://github.com/Teycir/AIJailbreaksRanking/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/Teycir/AIJailbreaksRanking/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/Teycir/AIJailbreaksRanking/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/Teycir/AIJailbreaksRanking/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/Teycir/AIJailbreaksRanking/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Teycir/AIJailbreaksRanking/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Teycir/AIJailbreaksRanking/releases/tag/v1.0.0
