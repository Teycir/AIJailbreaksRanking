#!/usr/bin/env python3
"""Check every source URL in the catalog still resolves.

Exit 0 = all reachable. Exit 1 = at least one dead link.
ponytail: stdlib only, sequential, no retries - 20 URLs do not need a pool.
Bot walls (403/429) warn instead of failing unless --strict is passed.
"""
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (compatible; AIJailbreaksRanking link check)"
OK, BOTWALL = range(200, 400), (403, 429)


def fetch(url, method):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    if method == "GET":
        req.add_header("Range", "bytes=0-0")
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status


def status(url):
    try:
        return fetch(url, "HEAD")
    except urllib.error.HTTPError as e:
        if e.code in (405, 501):
            return fetch(url, "GET")
        raise
    except Exception:
        return fetch(url, "GET")


def main():
    strict = "--strict" in sys.argv
    data = json.loads((ROOT / "data/techniques.json").read_text())
    dead, walled, checked = [], [], 0
    for t in data["techniques"]:
        for ev in t.get("evidence", []):
            url = ev["url"]
            checked += 1
            try:
                code = status(url)
            except Exception as e:
                dead.append((t["id"], url, repr(e)))
                print(f"DEAD  {t['id']}: {url} ({e})")
                continue
            if code in BOTWALL:
                walled.append((t["id"], url, code))
                print(f"WALL  {t['id']}: {url} (HTTP {code})")
            elif code not in OK:
                dead.append((t["id"], url, code))
                print(f"DEAD  {t['id']}: {url} (HTTP {code})")
    print(f"\n{checked} URLs, {len(dead)} dead, {len(walled)} bot-walled")
    if dead or (strict and walled):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
