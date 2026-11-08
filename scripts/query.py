#!/usr/bin/env python3
"""Query the AIJailbreaksRanking catalog. Stdlib only.

ponytail: no argparse subcommands, no dataclasses, no rich output. One filter
object + three renderers is all this needs.
"""
import argparse
import csv
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "techniques.json"


def load():
    with CATALOG.open(encoding="utf-8") as fh:
        return json.load(fh)


def match(t, a):
    if a.tier and t["tier"] not in a.tier:
        return False
    if a.status and t["status"] != a.status:
        return False
    if a.klass and t["class"] != a.klass:
        return False
    if a.id and t["id"] != a.id:
        return False
    if a.model:
        hay = " ".join(t.get("works_best_on", []) + t.get("works_poorly_on", [])).lower()
        if a.model.lower() not in hay:
            return False
    if a.search:
        hay = " ".join(
            [t["id"], t["name"], *t.get("aliases", []), t["mechanism"]]
        ).lower()
        if a.search.lower() not in hay:
            return False
    return True


def fmt_report(r):
    v = r.get("value")
    if v is None:
        v = "-"
    elif isinstance(v, float) and r["metric"] != "model_coverage":
        v = f"{v:.1%}" if v <= 1 else f"{v:g}"
    bits = [f"{r['metric']}={v}"]
    for k in ("target", "set", "n", "note"):
        if r.get(k):
            bits.append(f"{k}={r[k]}")
    return "; ".join(bits)


def render_text(rows):
    out = []
    for t in rows:
        out.append(f"\n[{t['tier']}] {t['id']} — {t['name']} ({t['year']})")
        out.append(f"  status: {t['status']} | class: {t['class']} | access: {t['access']}")
        out.append(f"  {t['mechanism']}")
        for r in t.get("reported", []):
            out.append(f"  · {fmt_report(r)}")
        if t.get("defense_notes"):
            out.append(f"  defense: {t['defense_notes']}")
        if t.get("evidence"):
            e = t["evidence"][0]
            out.append(f"  src: {e['publisher']} ({e['year']}) {e.get('url','')}")
    return "\n".join(out)


def render_csv(rows):
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["id", "name", "tier", "status", "class", "access", "best_on", "reported", "mechanism", "verified_at"])
    for t in rows:
        rep = "; ".join(fmt_report(r) for r in t.get("reported", []))
        best = ", ".join(t.get("works_best_on", []))
        writer.writerow([
            t["id"],
            t["name"],
            t["tier"],
            t["status"],
            t["class"],
            t["access"],
            best,
            rep,
            t["mechanism"],
            t.get("verified_at", "")
        ])
    return out.getvalue().strip()


def render_md(rows):
    out = ["| ID | Tier | Status | Technique | Year | Class | Reported |"]
    out.append("|----|------|--------|-----------|------|-------|----------|")
    for t in rows:
        rep = ", ".join(fmt_report(r) for r in t.get("reported", [])) or "-"
        out.append(
            f"| `{t['id']}` | {t['tier']} | {t['status']} | {t['name']} "
            f"| {t['year']} | {t['class']} | {rep} |"
        )
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Query the jailbreak catalog.")
    p.add_argument("--tier", help="filter tier(s), e.g. A or AB")
    p.add_argument("--status", choices=["recommended", "conditional", "discarded"])
    p.add_argument("--class", dest="klass", help="interaction class, e.g. multi-turn")
    p.add_argument("--id", help="exact technique id")
    p.add_argument("--model", help="substring match over works_best_on / works_poorly_on")
    p.add_argument("--search", help="substring search over id/name/aliases/mechanism")
    p.add_argument("--json", action="store_true", help="emit JSON records")
    p.add_argument("--md", action="store_true", help="emit a markdown table")
    p.add_argument("--csv", action="store_true", help="emit CSV format")
    a = p.parse_args()

    data = load()
    rows = [t for t in data["techniques"] if match(t, a)]
    if not rows:
        print("no matches", file=sys.stderr)
        return 1

    if a.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif a.md:
        print(render_md(rows))
    elif a.csv:
        print(render_csv(rows))
    else:
        print(render_text(rows))
        print(f"\n{len(rows)} of {len(data['techniques'])} techniques")
    return 0


if __name__ == "__main__":
    sys.exit(main())
