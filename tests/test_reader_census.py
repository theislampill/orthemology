#!/usr/bin/env python3
"""Synthetic Git-object tests; no research result or semantic-reading credit."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reader_census.py"

class ReaderCensusTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "reader census implementation is missing")
        spec = importlib.util.spec_from_file_location("reader_census", SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.temp = tempfile.TemporaryDirectory(prefix="reader-census-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Census fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.write("paper.md", "# Actual fixture body\n")
        self.write("elsewhere/copy.md", "# Actual fixture body\n")
        self.write("unusual.payload", "No extension-based exclusion.\n")
        self.write("owners.json", '{"sources": ["https://example.invalid/not-fetched"]}\n')
        self.commit = self.seal()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, stderr=subprocess.STDOUT).decode().strip()

    def write(self, name, text):
        p = self.repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
        return p

    def seal(self):
        self.git("add", "--all")
        self.git("commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def census(self, ref=None, owners=()):
        return self.module.census(self.repo, ref or self.commit, owners=owners, include_entries=True)

    def test_every_tracked_entry_and_exact_tree(self):
        c = self.census(owners=["owners.json"])
        self.assertEqual(c["baseline"]["tree"], self.git("rev-parse", self.commit + "^{tree}"))
        self.assertEqual(c["population"]["tracked_entries"], 4)
        self.assertEqual(len(c["entries"]), 4)
        self.assertEqual(c["owners"][0]["path"], "owners.json")
        self.assertEqual(c["reading_status"], "NOT_SEMANTICALLY_READ")

    def test_dirty_and_untracked_files_do_not_change_pinned_population(self):
        before = self.census()
        self.write("paper.md", "Dirty replacement\n")
        self.write("never-tracked.md", "Untracked fixture\n")
        self.assertEqual(before, self.census())

    def test_new_committed_file_outside_paper_roots_is_not_silently_omitted(self):
        before = self.census()
        self.write("unexpected/deep/positive-epistemology", "Fixture, not a real claim.\n")
        new = self.seal()
        after = self.census(new)
        self.assertEqual(after["population"]["tracked_entries"], 5)
        self.assertNotEqual(before["entries_sha256"], after["entries_sha256"])
        self.assertIn("unexpected/deep/positive-epistemology", {r["path"] for r in after["entries"]})
        self.assertEqual(before, self.census(self.commit))

    def test_duplicate_bytes_do_not_become_independent_work_counts(self):
        c = self.census()
        self.assertEqual(c["population"]["blob_paths"], 4)
        self.assertEqual(c["population"]["distinct_blob_objects"], 3)
        self.assertNotIn("work_count", c["population"])
        rows = {r["path"]: r for r in c["entries"]}
        self.assertEqual(rows["paper.md"]["git_oid"], rows["elsewhere/copy.md"]["git_oid"])

    def test_spaces_tabs_newlines_and_unicode_paths_survive(self):
        names = ["odd name.md", "tab\tname.txt", "line\nbreak.note", "cognition-عقل.md"]
        for name in names:
            self.write(name, "synthetic\n")
        c = self.census(self.seal())
        self.assertTrue(set(names) <= {r["path"] for r in c["entries"]})
        self.assertEqual(c["population"]["tracked_entries"], 8)

    def test_symlinks_record_identity_without_reading_the_target(self):
        os.symlink("../outside-not-present", self.repo / "link")
        c = self.census(self.seal())
        row = next(r for r in c["entries"] if r["path"] == "link")
        self.assertEqual(row["mode"], "120000")
        self.assertEqual(row["kind"], "blob")
        with self.assertRaises(ValueError):
            self.census(c["baseline"]["commit"], owners=["link"])

    def test_executable_mode_and_gitlinks_are_preserved(self):
        self.write("runner.sh", "#!/bin/sh\nexit 0\n").chmod(0o755)
        self.git("add", "--all")
        self.git("update-index", "--add", "--cacheinfo", "160000," + self.commit + ",dependency")
        self.git("commit", "-qm", "modes")
        c = self.census(self.git("rev-parse", "HEAD"))
        rows = {r["path"]: r for r in c["entries"]}
        self.assertEqual(rows["runner.sh"]["mode"], "100755")
        self.assertEqual(rows["dependency"]["kind"], "commit")
        self.assertIsNone(rows["dependency"]["bytes"])
        self.assertEqual(c["population"]["gitlinks"], 1)

    def test_invalid_or_unpinned_reference_fails_without_head_fallback(self):
        for ref in ("HEAD", "main", "0" * 40, "--all"):
            with self.subTest(ref=ref), self.assertRaises(ValueError):
                self.census(ref)

    def test_missing_duplicate_or_escaping_owner_fails(self):
        for owners in (["missing"], ["owners.json", "owners.json"], ["../owners.json"]):
            with self.subTest(owners=owners), self.assertRaises(ValueError):
                self.census(owners=owners)

    def test_repeated_output_and_owner_order_are_deterministic(self):
        a = self.census(owners=["paper.md", "owners.json"])
        b = self.census(owners=["owners.json", "paper.md"])
        self.assertEqual(a, b)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(self.census(owners=["paper.md", "owners.json"]), sort_keys=True))
        self.assertNotIn("timestamp", a)

if __name__ == "__main__":
    unittest.main()
