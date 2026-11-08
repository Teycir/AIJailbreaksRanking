#!/usr/bin/env python3
"""Negative controls for scripts/validate.py.

Each test copies the catalog to a temp dir, breaks exactly one invariant, and
asserts the validator exits 1. The clean copy must exit 0, so a test can only
fail because the corresponding check stopped working.
ponytail: stdlib only, no fixtures dir, no pytest.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
NEEDED = ["data", "techniques", "docs", "scripts", "README.md", "llms.txt", "CITATION.cff"]


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        for name in NEEDED:
            src, dst = ROOT / name, self.tmp / name
            shutil.copytree(src, dst) if src.is_dir() else shutil.copy2(src, dst)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def edit(self, rel, old, new, count=1):
        p = self.tmp / rel
        text = p.read_text()
        self.assertIn(old, text, f"test setup: {old!r} not in {rel}")
        p.write_text(text.replace(old, new, count))

    def run_validate(self):
        r = subprocess.run(
            [sys.executable, str(self.tmp / "scripts/validate.py")],
            capture_output=True, text=True,
        )
        return r.returncode, r.stdout + r.stderr


class TestClean(Base):
    def test_clean_tree_passes(self):
        code, out = self.run_validate()
        self.assertEqual(code, 0, out)


class TestDrift(Base):
    def test_table_separator_cell_count(self):
        self.edit("README.md", "|---|---|---|---|---|---|---|", "|---|---|---|---|---|---|")
        code, out = self.run_validate()
        self.assertIn("separator", out)
        self.assertEqual(code, 1)

    def test_missing_index_anchor(self):
        self.edit("README.md", '<a id="crescendo"></a>', "")
        code, out = self.run_validate()
        self.assertEqual(code, 1)

    def test_stale_catalog_version_citation(self):
        cur = json.loads((ROOT / "data/techniques.json").read_text())["version"]
        self.edit("README.md", f"catalog v{cur}", "catalog v0.0.0")
        code, out = self.run_validate()
        self.assertIn("does not cite catalog", out)
        self.assertEqual(code, 1)

    def test_cff_version_drift(self):
        cur = json.loads((ROOT / "data/techniques.json").read_text())["version"]
        self.edit("CITATION.cff", f"version: {cur}", "version: 0.0.0")
        code, out = self.run_validate()
        self.assertIn("CITATION.cff: version does not cite", out)
        self.assertEqual(code, 1)

    def test_defenses_missing_section(self):
        self.edit("docs/defenses.md", "### `crescendo` (A)", "### `crescendo` (A)")
        text = (self.tmp / "docs/defenses.md").read_text()
        (self.tmp / "docs/defenses.md").write_text(
            text.replace("### `crescendo` (A)", "### (A)")
        )
        code, out = self.run_validate()
        self.assertIn("no section for", out)
        self.assertEqual(code, 1)

    def test_doc_example_drift(self):
        p = self.tmp / "techniques/tap.md"
        p.write_text(p.read_text().replace("## Examples", "## Worked examples", 1))
        code, out = self.run_validate()
        self.assertIn("no ## Examples", out)
        self.assertEqual(code, 1)

    def test_unknown_technique_in_defenses(self):
        p = self.tmp / "docs/defenses.md"
        p.write_text(p.read_text() + "\n### `ghost-technique` (A)\n")
        code, out = self.run_validate()
        self.assertIn("unknown techniques", out)
        self.assertEqual(code, 1)


    def test_taxonomy_missing_class(self):
        self.edit("docs/taxonomy.md", "`framing`", "`framing-frame`", -1)
        code, out = self.run_validate()
        self.assertEqual(code, 1)
        self.assertIn("class `framing`", out)

    def test_reliability_missing_evaluator(self):
        self.edit("docs/reliability.md", "`qualitative`", "`qual`")
        code, out = self.run_validate()
        self.assertEqual(code, 1)
        self.assertIn("evaluator `qualitative`", out)

    def test_missing_n_warns_only(self):
        p = self.tmp / "data/techniques.json"
        data = json.loads(p.read_text())
        for tech in data["techniques"]:
            for row in tech.get("reported", []):
                row.pop("n", None)
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        code, out = self.run_validate()
        self.assertEqual(code, 0)
        self.assertIn("without n", out)

    def test_csv_summary_drift(self):
        p = self.tmp / "data/techniques-summary.csv"
        lines = p.read_text().splitlines()
        p.write_text("\n".join(lines[:-1]) + "\n")  # remove last technique
        code, out = self.run_validate()
        self.assertEqual(code, 1)
        self.assertIn("techniques-summary.csv mismatch", out)


if __name__ == "__main__":
    unittest.main()
