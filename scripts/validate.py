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
T = {t["id"]: t for t in techs}
if len(ids) != len(set(ids)):
    err(f"duplicate ids: {sorted({i for i in ids if ids.count(i) > 1})}")

for t in techs:
    tid = t["id"]
    if not re.fullmatch(r"[a-z0-9-]+", tid):
        err(f"{tid}: id is not a slug")
    if not t.get("works_best_on"):
        err(f"{tid}: works_best_on missing or empty")
    if not (ROOT / t.get("doc", "")).is_file():
        err(f"{tid}: doc missing: {t.get('doc')}")
    doc = ROOT / t.get("doc", "")
    if doc.is_file():
        body = doc.read_text()
        exs = t.get("examples") or []
        if "## Examples" not in body:
            err(f"{tid}: doc has no ## Examples section")
        elif len(exs) != 3:
            err(f"{tid}: catalog needs exactly 3 examples, has {len(exs)}")
        elif exs[0]["body"].split("\n")[0] not in body:
            err(f"{tid}: doc Examples section does not match catalog[0]")
        for i, e in enumerate(exs, 1):
            if f"### {i}. {e['title']}" not in body:
                err(f"{tid}: doc missing '### {i}. {e['title']}'")
    # Tier discipline: A/B must be recommended, D must be discarded.
    if t["tier"] in "AB" and t["status"] != "recommended":
        err(f"{tid}: Tier {t['tier']} must be recommended, is {t['status']}")
    if t["tier"] == "D" and t["status"] != "discarded":
        err(f"{tid}: Tier D must be discarded, is {t['status']}")
    for r in t.get("reported", []):
        if not r.get("evaluator"):
            err(f"{tid}: reported entry without evaluator ({r.get('metric')})")
        if "n" not in r:
            warnings.append(f"{tid}: reported row without n ({r.get('metric')})")
        if t["tier"] in "AB" and r.get("evaluator") in ("keyword-match", "unspecified"):
            err(f"{tid}: Tier {t['tier']} rests on {r['evaluator']} evidence")
    for ev in t.get("evidence", []):
        if not ev.get("verified_at"):
            err(f"{tid}: evidence without verified_at: {ev.get('title')}")

def best_cell(t):
    b = t["works_best_on"]
    s = ", ".join(b[:2])
    return s + (f" +{len(b) - 2}" if len(b) > 2 else "")

# 3. Cross-file drift: README table and llms.txt must mirror the JSON.
readme = (ROOT / "README.md").read_text().replace("*", "")

# 3b. The short-list table must be parseable by GFM: header, separator and every
# row need the same cell count, otherwise GitHub renders the pipes as text.
lines = readme.split("\n")
try:
    h = next(i for i, l in enumerate(lines) if l.startswith("| ID | Technique |"))
except StopIteration:
    err("README: short-list header missing")
else:
    ncol = lines[h].count("|") - 1
    if lines[h + 1].count("|") - 1 != ncol:
        err(f"README: separator has {lines[h + 1].count('|') - 1} cells, header has {ncol}")
    body = []
    for l in lines[h + 2:]:
        if not l.startswith("|"):
            break
        body.append(l)
        if l.count("|") - 1 != ncol:
            err(f"README: row has {l.count('|') - 1} cells, header has {ncol}: {l[:40]}")
    if len(body) != len(techs):
        err(f"README: short-list has {len(body)} rows, catalog has {len(techs)}")

stamp = f"Last assessed: {data['updated']}"
if stamp not in readme:
    err(f"README: missing assessment stamp {stamp}")
if f"catalog v{data['version']}" not in readme:
    err(f"README: assessment stamp does not cite catalog v{data['version']}")
for t in techs:
    tid = t["id"]
    if f"](#{tid})" not in readme:
        err(f"README: no anchor link to #{tid} from the table")
    if f'<a id="{tid}"></a>' not in readme:
        err(f"README: index anchor for {tid} missing")
    if f"(techniques/{tid}.md)" not in readme:
        err(f"README: index entry for {tid} does not link its doc")

for t in techs:
    row = re.search(rf"^\|\s*`{re.escape(t['id'])}`\s*\|.*\|\s*{t['tier']}\s*\|\s*{t['status']}\s*\|",
                    readme, re.M)
    if not row:
        err(f"README: no row matching tier/status for {t['id']}")
    else:
        want = best_cell(t)
        if f"| {want} |" not in row.group(0):
            err(f"README: Best-on cell for {t['id']} is not '{want}'")
counts = {k: sum(t["tier"] == k for t in techs) for k in "ABCD"}
m = re.search(r"(\d+) entries \((\d+) reliable, (\d+) conditional, (\d+) historical, (\d+) discarded\)", readme)
if not m:
    err("README: entry-count line missing")
elif [int(x) for x in m.groups()] != [len(techs), counts["A"], counts["B"], counts["C"], counts["D"]]:
    err(f"README: counts {m.groups()} != JSON {len(techs), counts['A'], counts['B'], counts['C'], counts['D']}")

stamp = data.get("sources_last_checked", "")
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
    err(f"data: sources_last_checked missing or not YYYY-MM-DD: {stamp!r}")
elif f"sources checked {stamp}" not in (ROOT / "README.md").read_text():
    err(f"README: stamp line does not carry 'sources checked {stamp}'")

llms = (ROOT / "llms.txt").read_text()
for tid in ids:
    line = re.search(rf"^- {re.escape(tid)}:.*$", llms, re.M)
    if not line:
        err(f"llms.txt: no line for {tid}")
    elif f"Best on: {best_cell(T[tid])}." not in line.group(0):
        err(f"llms.txt: missing or stale Best on for {tid}")

# ---- docs/defenses.md must cover every technique and invent none
defenses = (ROOT / "docs/defenses.md")
if not defenses.is_file():
    err("docs/defenses.md missing")
else:
    body = defenses.read_text()
    covered = set()
    for line in body.splitlines():
        if line.startswith("### "):
            covered.update(re.findall(r"`([a-z0-9-]+)`", line))
    missing = sorted(set(ids) - covered)
    stale = sorted(covered - set(ids))
    if missing:
        err(f"defenses.md: no section for {missing}")
    if stale:
        err(f"defenses.md: sections for unknown techniques {stale}")

# ---- docs/taxonomy.md must define every schema class
taxonomy = ROOT / "docs/taxonomy.md"
if not taxonomy.is_file():
    err("docs/taxonomy.md missing")
else:
    body = taxonomy.read_text()
    for cls in sorted(schema["properties"]["techniques"]["items"]["properties"]["class"]["enum"]):
        if f"`{cls}`" not in body:
            err(f"taxonomy.md: class `{cls}` has no definition")

# ---- docs/reliability.md must define every evaluator used and every tier letter
reliability = ROOT / "docs/reliability.md"
if not reliability.is_file():
    err("docs/reliability.md missing")
else:
    body = reliability.read_text()
    used = sorted({r["evaluator"] for t in techs for r in t.get("reported", [])})
    for ev in used:
        if f"`{ev}`" not in body:
            err(f"reliability.md: evaluator `{ev}` undocumented")
    for tier in "ABCD":
        if f"Tier {tier}" not in body:
            err(f"reliability.md: Tier {tier} never mentioned")

for w in warnings:
    print(f"warn: {w}", file=sys.stderr)
if errors:
    print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)
print(f"OK: {len(techs)} techniques, tiers {counts}, docs+README+llms.txt consistent")
