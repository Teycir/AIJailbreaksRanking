#!/usr/bin/env python3
"""Render docs/techniques/<id>.html from techniques/<id>.md.

Shared styling comes from docs/assets/style.css, so a technique page looks like
the catalog viewer. Run after editing a technique doc, then commit docs/.

    python3 scripts/build_site.py
"""

import html
import json
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("missing dependency: pip install markdown")

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TECHNIQUES = ROOT / "techniques"
OUT = DOCS / "techniques"

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} — Tier {tier} · AIJailbreaksRanking</title>
  <meta name="description" content="{desc}">
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <div class="container">
    <div class="page-head">
      <a class="back" href="../index.html">← All techniques</a>
      <a class="back" href="https://github.com/Teycir/AIJailbreaksRanking/blob/master/techniques/{id}.md">Markdown source ↗</a>
    </div>
    <div class="meta-row">
      <span class="badge badge-tier-{tier}">Tier {tier}</span>
      <span class="chip">{status}</span>
      <span class="chip">{cls}</span>
      <span class="chip">{access}</span>
      <span class="chip">{year}</span>
      <span class="chip"><code>{id}</code></span>
    </div>
    <article class="prose">
{body}
    </article>
    <footer>
      <p>Part of <a href="../index.html">AIJailbreaksRanking</a> — an evidence-graded catalog of LLM jailbreak techniques.</p>
      <p>Source: <a href="https://github.com/Teycir/AIJailbreaksRanking/blob/master/techniques/{id}.md">techniques/{id}.md</a></p>
    </footer>
  </div>
</body>
</html>
"""

FRONTMATTER = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.S)


def render(record):
    tid = record["id"]
    src = TECHNIQUES / f"{tid}.md"
    if not src.exists():
        sys.exit(f"missing source doc: {src}")
    body = FRONTMATTER.sub("", src.read_text(encoding="utf-8"), count=1)
    body = markdown.markdown(
        body, extensions=["fenced_code", "tables", "sane_lists"]
    )
    # Pygments is not a dependency: keep code blocks plain but readable.
    page = PAGE.format(
        id=tid,
        name=html.escape(record["name"]),
        desc=html.escape(record.get("mechanism", "")),
        tier=record["tier"],
        status=html.escape(record.get("status", "")),
        cls=html.escape(record.get("class", "")),
        access=html.escape(record.get("access", "")),
        year=html.escape(str(record.get("year", ""))),
        body=body,
    )
    return OUT / f"{tid}.html", page


def main():
    data = json.loads((ROOT / "data" / "techniques.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for record in data["techniques"]:
        path, page = render(record)
        path.write_text(page, encoding="utf-8")
        written.append(path.name)
    stale = {p.name for p in OUT.glob("*.html")} - set(written)
    for name in sorted(stale):
        (OUT / name).unlink()
    print(f"built {len(written)} technique pages -> docs/techniques/")
    if stale:
        print(f"removed stale: {', '.join(sorted(stale))}")


if __name__ == "__main__":
    main()
