# Contributing

## What belongs here

Published techniques with a named evaluator and a sample size. Aggregated blog lists without methodology do not qualify.

## Required for a new entry

1. **Citation.** Paper, vendor advisory, or reproducible public write-up with a URL.
2. **Metric label.** One of the `reported[].metric` values in `data/schema.json`. Do not invent new ones without changing the schema.
3. **Sample size** (`n`) where it exists. Omit rather than guess.
4. **Precondition.** If it only works with prefill, grammar control, or a conversation, say so in `requires`.
5. **Defense note.** What actually reduces it, or explicitly "none found".
6. **Tier justification.** Apply `docs/reliability.md`. Default to C when uncertain.

## Automatic disqualifiers for Tier A or B

- Keyword-match ASR is the only evidence.
- Single model tested and no transfer evidence.
- Fixed prompt set with no diversity analysis.
- No defense evaluation.

These are not rejections — they are Tier C/D placements. A discarded technique with a good write-up is more valuable than a promoted one with bad methodology.

## Files to touch

Adding a technique means all of:

```
data/techniques.json     append the record
techniques/<id>.md       write the doc, frontmatter mirrors the record
README.md                add the row to the table
llms.txt                 add the line
docs/defenses.md         add the per-technique section
```

`id` is a slug and is permanent once merged. Pick it carefully.

## Validation

```bash
python3 -c "import json;json.load(open('data/techniques.json'))"
python3 scripts/query.py --id <new-id>
```

## Corrections

If a number in the catalog is wrong, fix it and note the correction in the commit message. Do not silently rewrite history; the credibility of the tier marks depends on being able to see what changed and why.
