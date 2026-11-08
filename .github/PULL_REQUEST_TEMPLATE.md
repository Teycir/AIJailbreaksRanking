## Summary of changes

<!-- Briefly describe the new technique, update, or bug fix -->

### Checklist for technique additions or updates

- [ ] Technique adheres to the schema (`data/schema.json`)
- [ ] Added to `data/techniques.json` with required fields (including `examples` and `verified_at`)
- [ ] Added write-up in `techniques/<id>.md` (with 3 harmless examples matching `techniques.json`)
- [ ] Added row to `README.md` table and index
- [ ] Added line to `llms.txt`
- [ ] Added defense entry in `docs/defenses.md`
- [ ] Ran `python3 scripts/export_summary.py` to sync `data/techniques-summary.csv`
- [ ] Verified local validation passes:
  ```bash
  python3 scripts/validate.py
  pytest
  ```
