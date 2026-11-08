#!/usr/bin/env python3
"""Export catalog to flat CSV summary (data/techniques-summary.csv).

Stdlib only.
"""
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "techniques.json"
CSV_OUT = ROOT / "data" / "techniques-summary.csv"
HTML_VIEWER = ROOT / "docs" / "index.html"
README = ROOT / "README.md"


def get_reported_effects():
    effects = {}
    if not README.is_file():
        return effects
    lines = README.read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line.startswith("| `"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 7:
                tid = parts[0].strip("`")
                m = re.search(r"\[(.*?)\]\(.*?\)", parts[6])
                effects[tid] = m.group(1) if m else parts[6]
    return effects


def export():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    techs = data["techniques"]
    effects = get_reported_effects()

    with CSV_OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id",
            "name",
            "tier",
            "status",
            "class",
            "access",
            "best_on",
            "reported_effect",
            "mechanism",
            "verified_at",
        ])
        for t in techs:
            tid = t["id"]
            best = ", ".join(t.get("works_best_on", []))
            eff = effects.get(tid, "")
            writer.writerow([
                t["id"],
                t["name"],
                t["tier"],
                t["status"],
                t["class"],
                t["access"],
                best,
                eff,
                t["mechanism"],
                t.get("verified_at", ""),
            ])
    print(f"Exported {len(techs)} techniques to {CSV_OUT.relative_to(ROOT)}")

    if HTML_VIEWER.is_file():
        html = HTML_VIEWER.read_text(encoding="utf-8")
        m = re.search(r"let techniquesData = .*?;", html)
        if m:
            new_data = "let techniquesData = " + json.dumps(techs, ensure_ascii=False) + ";"
            HTML_VIEWER.write_text(html[:m.start()] + new_data + html[m.end():], encoding="utf-8")
            print(f"Updated offline data in {HTML_VIEWER.relative_to(ROOT)}")


if __name__ == "__main__":
    export()
