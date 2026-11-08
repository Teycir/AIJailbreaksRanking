#!/usr/bin/env python3
"""Validate the catalog: schema, tier discipline, and cross-file drift.

Exit 0 = consistent. Exit 1 = errors printed to stderr.
ponytail: stdlib only; jsonschema used when present, otherwise the checks below
are the ones that actually caught drift, so CI needs no install.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors, warnings = [], []


def load(rel):
    return json.loads((ROOT / rel).read_text())


def err(msg):
    errors.append(msg)


data = load("data/techniques.json")
schema = load("data/schema.json")
techs = data["techniques"]

# 1. Schema, when the validator is installed.
try:
    import jsonschema

    for e in jsonschema.Draft202012Validator(schema).iter_errors(data):
        err(f"schema: {e.json_path}: {e.message}")
except ImportError:
    warnings.append("jsonschema not installed; structural checks only")

# 2. Structural invariants.
ids = [t["id"] for t in techs]
if len(ids) != len(set(ids)):
    err(f"duplicate ids: {sorted({i for i in ids if ids.count(i) > 1})}")

for t in techs:
    tid = t["id"]
    if not re.fullmatch(r"[a-z0-9-]+", tid):
        err(f"{tid}: id is not a slug")
    if not (ROOT / t.get("doc", "")).is_file():
        err(f"{tid}: doc missing: {t.get('doc')}")
    # Tier discipline: A/B must be recommended, D must be discarded.
    if t["tier"] in "AB" and t["status"] != "recommended":
        err(f"{tid}: Tier {t['tier']} must be recommended, is {t['status']}")
    if t["tier"] == "D" and t["status"] != "discarded":
        err(f"{tid}: Tier D must be discarded, is {t['status']}")
    for r in t.get("reported", []):
        if not r.get("evaluator"):
            err(f"{tid}: reported entry without evaluator ({r.get('metric')})")
        if t["tier"] in "AB" and r.get("evaluator") in ("keyword-match", "unspecified"):
            err(f"{tid}: Tier {t['tier']} rests on {r['evaluator']} evidence")
    for ev in t.get("evidence", []):
        if not ev.get("verified_at"):
            err(f"{tid}: evidence without verified_at: {ev.get('title')}")

# 3. Cross-file drift: README table and llms.txt must mirror the JSON.
readme = (ROOT / "README.md").read_text().replace("*", "")
for t in techs:
    row = re.search(rf"^\|\s*`{re.escape(t['id'])}`\s*\|.*\|\s*{t['tier']}\s*\|\s*{t['status']}\s*\|",
                    readme, re.M)
    if not row:
        err(f"README: no row matching tier/status for {t['id']}")
counts = {k: sum(t["tier"] == k for t in techs) for k in "ABCD"}
m = re.search(r"(\d+) entries \((\d+) reliable, (\d+) conditional, (\d+) historical, (\d+) discarded\)", readme)
if not m:
    err("README: entry-count line missing")
elif [int(x) for x in m.groups()] != [len(techs), counts["A"], counts["B"], counts["C"], counts["D"]]:
    err(f"README: counts {m.groups()} != JSON {len(techs), counts['A'], counts['B'], counts['C'], counts['D']}")

llms = (ROOT / "llms.txt").read_text()
for tid in ids:
    if not re.search(rf"^- {re.escape(tid)}:", llms, re.M):
        err(f"llms.txt: no line for {tid}")

for w in warnings:
    print(f"warn: {w}", file=sys.stderr)
if errors:
    print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)
print(f"OK: {len(techs)} techniques, tiers {counts}, docs+README+llms.txt consistent")
