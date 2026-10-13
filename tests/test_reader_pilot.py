#!/usr/bin/env python3
"""Mechanical reader-pilot controls; not a classifier of philosophical truth."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "check_reader_pilot.py"


class ReaderPilotTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.exists(), "reader pilot checker has not been implemented")
        spec = importlib.util.spec_from_file_location("reader_pilot_under_test", MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.files = {
            "theory/core.md": "# Core\nA scoped definition.\n",
            "theory/multi.md": "# Multi\nAn additional component.\n",
            "theory/note.md": "# Note\nA substantive work without a PDF.\n",
            "theory/related.tex": r"\title{Related, differently titled source}",
            "theory/edition.pdf": "synthetic preserved edition, not a real PDF",
            "theory/lineage.md": "# Lineage\nExact build provenance is unverified.\n",
            "research/new/README.md": "# Later collection\nIts own scope.\n",
            "docs/profile.yaml": (
                "artifacts:\n"
                "- artifact_id: core\n  sources: [theory/core.md, theory/multi.md]\n"
                "  profile_kind: technical-paper\n"
                "- artifact_id: gallery\n  sources: [docs/gallery.md]\n"
                "  profile_kind: diagnostic-reference\n"
            ),
            "docs/gallery.md": "# Gallery\nReference only.\n",
            "publication/latex/core/main.tex": "synthetic generated text",
            "artifacts/core.pdf": "synthetic composite rendering",
            "artifacts/gallery.pdf": "synthetic reference rendering",
        }
        for p, body in self.files.items():
            out = self.repo / p
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(body)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture baseline")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.owners = {
            "schema": "orthemology-reader-owner-map-v1",
            "baseline": {"commit": self.base},
            "external_body_admissions": [],
            "collections": [
                {"key": "theory", "include": ["theory/"], "exclude": [],
                 "owners": ["theory/lineage.md"]},
                {"key": "later", "include": ["research/new/"], "exclude": [],
                 "owners": ["research/new/README.md"]},
                {"key": "docs", "include": ["docs/"], "exclude": [],
                 "owners": ["docs/profile.yaml"]},
                {"key": "publication", "include": ["publication/", "artifacts/"],
                 "exclude": [], "owners": ["docs/profile.yaml"]},
            ],
            "required_work_sources": ["theory/core.md", "theory/note.md"],
            "publication_profile": "docs/profile.yaml",
            "edition_constraints": [{
                "source": "theory/related.tex", "rendering": "theory/edition.pdf",
                "permitted_relation": "related-source",
                "basis": "theory/lineage.md",
            }],
        }
        def src(path):
            return {"path": path, "sha256": hashlib.sha256((self.repo/path).read_bytes()).hexdigest(),
                    "read_scope": "fixture only"}
        self.cross = {
            "schema": "orthemology-reader-crosswalk-v1",
            "coverage_stage": "representative-pilot",
            "sources": {p: src(p) for p in self.files},
            "works": [
                {"key": "core", "title": "Composite core", "role": "composite-reference",
                 "source_keys": ["theory/core.md", "theory/multi.md"], "artifact_id": "core"},
                {"key": "note", "title": "Substantive note", "role": "research-note",
                 "source_keys": ["theory/note.md"]},
                {"key": "related", "title": "Related source", "role": "research-note",
                 "source_keys": ["theory/related.tex"]},
                {"key": "edition", "title": "Preserved edition", "role": "preserved-edition",
                 "source_keys": ["theory/edition.pdf"]},
                {"key": "gallery", "title": "Reference gallery", "role": "supporting-reference",
                 "source_keys": ["docs/gallery.md"], "artifact_id": "gallery"},
            ],
            "relations": [{
                "from": "theory/related.tex", "to": "theory/edition.pdf",
                "kind": "related-source", "basis": "theory/lineage.md",
            }],
            "probes": [
                {"key": "recognition-correction", "works": ["note"],
                 "sources": ["theory/note.md"]},
                {"key": "tensor-geometry", "works": ["core"],
                 "sources": ["theory/core.md"]},
                {"key": "cross-avenue", "works": ["note", "core"],
                 "sources": ["theory/note.md", "theory/core.md"]},
            ],
        }

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, stderr=subprocess.DEVNULL).decode()

    def check(self, owners=None, cross=None):
        return self.mod.check(self.repo, owners or self.owners, cross or self.cross)

    def reject(self, errors, code):
        self.assertTrue(any(e.startswith(code + ":") for e in errors), errors)

    def test_valid_composite_and_distinct_related_edition(self):
        self.assertEqual(self.check(), [])

    def test_missing_non_pdf_work(self):
        altered = deepcopy(self.cross)
        altered["works"] = [w for w in altered["works"] if w["key"] != "note"]
        self.assertNotEqual(altered, self.cross)
        self.reject(self.check(cross=altered), "missing-work")

    def test_missing_collection(self):
        altered = deepcopy(self.owners)
        altered["collections"] = [c for c in altered["collections"] if c["key"] != "later"]
        self.reject(self.check(owners=altered), "unassigned-source")

    def test_unfamiliar_new_root_is_not_silently_excluded(self):
        p = self.repo / "unexpected" / "new-work.unbuilt"
        p.parent.mkdir()
        p.write_text("A substantive fixture")
        self.git("add", ".")
        self.git("commit", "-qm", "new candidate")
        altered = deepcopy(self.owners)
        altered["baseline"]["commit"] = self.git("rev-parse", "HEAD").strip()
        self.reject(self.check(owners=altered), "unassigned-source")

    def test_overlapping_owner_groups(self):
        altered = deepcopy(self.owners)
        altered["collections"].append({"key": "duplicate", "include": ["theory/"],
                                      "exclude": [], "owners": ["theory/core.md"]})
        self.reject(self.check(owners=altered), "overlapping-source")

    def test_missing_bound_owner(self):
        altered = deepcopy(self.owners)
        altered["collections"][0]["owners"] = ["absent.md"]
        self.reject(self.check(owners=altered), "owner")

    def test_moving_ref_rejected(self):
        altered = deepcopy(self.owners)
        altered["baseline"]["commit"] = "HEAD"
        self.reject(self.check(owners=altered), "baseline")

    def test_external_body_admission_not_in_this_boundary(self):
        altered = deepcopy(self.owners)
        altered["external_body_admissions"] = ["https://example.invalid/new-literature"]
        self.reject(self.check(owners=altered), "external")

    def test_source_drift_requires_synopsis_review(self):
        p = self.repo / "theory/note.md"
        before = p.read_bytes()
        p.write_bytes(before + b"Changed premise.\n")
        self.assertNotEqual(p.read_bytes(), before)
        self.reject(self.check(), "source-drift")

    def test_symlink_source_is_not_followed(self):
        p = self.repo / "theory/note.md"
        p.unlink()
        p.symlink_to(self.repo / "theory/core.md")
        self.reject(self.check(), "unsafe-source")

    def test_parent_symlink_is_not_followed(self):
        p = self.repo / "elsewhere"
        p.symlink_to(self.repo / "theory", target_is_directory=True)
        altered = deepcopy(self.cross)
        altered["sources"]["theory/note.md"]["path"] = "elsewhere/note.md"
        self.reject(self.check(cross=altered), "unsafe-source")

    def test_path_traversal_rejected(self):
        altered = deepcopy(self.cross)
        altered["sources"]["theory/note.md"]["path"] = "../outside.md"
        self.reject(self.check(cross=altered), "unsafe-source")

    def test_missing_composite_component(self):
        altered = deepcopy(self.cross)
        altered["works"][0]["source_keys"].remove("theory/multi.md")
        self.reject(self.check(cross=altered), "composite")

    def test_generated_tex_is_not_another_authored_work(self):
        altered = deepcopy(self.cross)
        altered["works"].append({"key": "fake-third-work", "title": "Not another paper",
                                "role": "research-note",
                                "source_keys": ["publication/latex/core/main.tex"]})
        self.reject(self.check(cross=altered), "generated-work")

    def test_missing_governed_artifact(self):
        altered = deepcopy(self.cross)
        altered["works"] = [w for w in altered["works"] if w.get("artifact_id") != "gallery"]
        self.reject(self.check(cross=altered), "artifact")

    def test_reference_gallery_cannot_become_article(self):
        altered = deepcopy(self.cross)
        altered["works"][-1]["role"] = "research-note"
        self.reject(self.check(cross=altered), "reference-role")

    def test_false_exact_build_relation(self):
        altered = deepcopy(self.cross)
        altered["relations"][0]["kind"] = "verified-build-input"
        self.reject(self.check(cross=altered), "edition")

    def test_duplicate_work_identity(self):
        altered = deepcopy(self.cross)
        altered["works"].append(deepcopy(altered["works"][0]))
        self.reject(self.check(cross=altered), "duplicate-work")

    def test_bound_path_with_wrong_source_bytes(self):
        altered = deepcopy(self.cross)
        altered["sources"]["theory/note.md"]["path"] = "theory/core.md"
        self.reject(self.check(cross=altered), "source-drift")

    def test_all_three_intellectual_routes_required(self):
        for key in ("recognition-correction", "tensor-geometry", "cross-avenue"):
            with self.subTest(probe=key):
                altered = deepcopy(self.cross)
                altered["probes"] = [p for p in altered["probes"] if p["key"] != key]
                self.reject(self.check(cross=altered), "probe")

    def test_decorative_cross_avenue_route_rejected(self):
        altered = deepcopy(self.cross)
        altered["probes"][-1]["works"] = []
        self.reject(self.check(cross=altered), "probe")

    def test_unrelated_worktree_change_does_not_rewrite_every_synopsis(self):
        p = self.repo / "unrelated-scratch.txt"
        p.write_text("Not a bound source or part of the pinned baseline.")
        self.assertEqual(self.check(), [])

    def test_pilot_cannot_declare_whole_corpus_completion(self):
        altered = deepcopy(self.cross)
        altered["coverage_stage"] = "complete"
        self.reject(self.check(cross=altered), "stage")

    def test_check_is_read_only(self):
        before = {p.relative_to(self.repo): p.read_bytes()
                  for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        self.assertEqual(self.check(), [])
        after = {p.relative_to(self.repo): p.read_bytes()
                 for p in self.repo.rglob("*") if p.is_file() and ".git" not in p.parts}
        self.assertEqual(before, after)


    def test_rehashed_scientific_source_cannot_rebind_baseline(self):
        p = self.repo / "theory/note.md"
        before = p.read_bytes()
        p.write_bytes(before + b"A different scientific conclusion.\n")
        altered = deepcopy(self.cross)
        altered["sources"]["theory/note.md"]["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertNotEqual(p.read_bytes(), before)
        self.reject(self.check(cross=altered), "baseline-source")

    def test_source_executable_mode_is_preserved(self):
        p = self.repo / "theory/note.md"
        p.chmod(0o755)
        self.assertTrue(p.stat().st_mode & 0o111)
        self.reject(self.check(), "source-mode")

    def test_unknown_reading_form_source_is_rejected(self):
        altered = deepcopy(self.cross)
        altered["works"][0]["reading_forms"] = [{"source": "ghost", "relationship": "governed-rendering"}]
        self.reject(self.check(cross=altered), "reading-form")

    def test_governed_reading_form_cannot_point_to_other_pdf(self):
        altered = deepcopy(self.cross)
        altered["works"][0]["reading_forms"] = [{"source": "artifacts/gallery.pdf", "relationship": "governed-rendering"}]
        self.reject(self.check(cross=altered), "rendering-target")

    def test_correct_governed_reading_form_is_accepted(self):
        altered = deepcopy(self.cross)
        altered["works"][0]["reading_forms"] = [{"source": "artifacts/core.pdf", "relationship": "governed-rendering"}]
        self.assertEqual(self.check(cross=altered), [])

    def test_discovery_owner_drift_is_detected_from_pinned_git(self):
        p = self.repo / "research/new/README.md"
        before = p.read_bytes()
        p.write_bytes(before + b"Altered collection scope.\n")
        self.assertNotEqual(p.read_bytes(), before)
        self.reject(self.check(), "owner")

    def test_duplicate_json_field_is_not_silently_replaced(self):
        with self.assertRaises(ValueError):
            json.loads('{"scope":"pilot","scope":"complete"}',
                       object_pairs_hook=self.mod.unique_object)



    def test_wrong_recorded_baseline_tree_is_rejected(self):
        altered = deepcopy(self.owners)
        altered["baseline"]["tree"] = "0" * 40
        self.reject(self.check(owners=altered), "baseline")

    def test_wrong_recorded_group_count_is_rejected(self):
        altered = deepcopy(self.owners)
        altered["collections"][0]["candidate_paths"] = 999
        self.reject(self.check(owners=altered), "owner-count")



class ReaderPageRouteTests(unittest.TestCase):
    """Real Markdown link parsing; semantic truth deliberately remains outside it."""
    def setUp(self):
        spec = importlib.util.spec_from_file_location("reader_routes_under_test", MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.assertTrue(hasattr(self.mod, "check_reader_pages"), "reader-page route check not implemented")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        (self.repo / "theory").mkdir()
        (self.repo / "theory/source.md").write_text("# Source\n## Assumptions\nA scoped fixture.\n")
        (self.repo / "theory/other.md").write_text("# Different source\nA different fixture.\n")
        self.pages = ["RESEARCH-ATLAS.md", "PAPER-CATALOGUE.md", "RESULT-INDEX.md",
                      "CURRENT-FRONTIERS.md", "APPLICATIONS.md", "VERIFICATION-GUIDE.md"]
        for name in self.pages:
            path = self.repo / "docs/reader" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Reader\n\n## Overview\nA conditional construction.\n[Read][source]\n\n"
                            "[source]: ../../theory/source.md#assumptions\n")
        self.cross = {
            "sources": {"source": {"path": "theory/source.md"}},
            "reader_journeys": [
                {"id": "J%02d" % i,
                 "entry": "docs/reader/" + self.pages[(i - 1) % len(self.pages)] + "#overview",
                 "source_keys": ["source"]}
                for i in range(1, 8)
            ],
        }

    def check(self, cross=None):
        return self.mod.check_reader_pages(self.repo, cross or self.cross)

    def page(self, name="RESEARCH-ATLAS.md"):
        return self.repo / "docs/reader" / name

    def mutate(self, old, new):
        p = self.page()
        before = p.read_text()
        self.assertIn(old, before, "negative control must actually mutate its target")
        p.write_text(before.replace(old, new))
        self.assertNotEqual(p.read_text(), before)

    def reject(self, code):
        errors = self.check()
        self.assertTrue(any(e.startswith(code + ":") for e in errors), errors)

    def test_valid_reference_style_links_and_source_fragments(self):
        self.assertEqual(self.check(), [])

    def test_missing_reader_page(self):
        self.page().unlink()
        self.reject("reader-page")

    def test_nonexistent_heading_fragment(self):
        self.mutate("#assumptions", "#not-a-real-heading")
        self.reject("reader-fragment")

    def test_correct_http_like_success_is_not_correct_source(self):
        self.mutate("../../theory/source.md#assumptions", "../../theory/other.md")
        self.reject("journey-target")

    def test_wrong_valid_source_fragment_is_not_the_requested_section(self):
        p = self.repo / "theory/source.md"
        p.write_text(p.read_text() + "## Other result\nDifferent scope.\n")
        self.cross["reader_journeys"][0]["source_fragments"] = {"source": "assumptions"}
        self.mutate("#assumptions", "#other-result")
        self.reject("journey-target")

    def test_missing_journey_cannot_pass(self):
        self.cross["reader_journeys"].pop()
        self.reject("journey-map")

    def test_duplicate_journey_cannot_pass(self):
        self.cross["reader_journeys"].append(deepcopy(self.cross["reader_journeys"][0]))
        self.reject("journey-map")

    def test_wrong_entry_fragment_cannot_pass(self):
        self.cross["reader_journeys"][0]["entry"] = "docs/reader/RESEARCH-ATLAS.md#absent"
        self.reject("journey-entry")

    def test_link_elsewhere_is_not_the_promised_section_route(self):
        self.mutate("[Read][source]", "No source here.\n\n## Other section\n[Read][source]")
        self.reject("journey-target")

    def test_fenced_link_is_not_navigation(self):
        self.mutate("[Read][source]", "```text\n[Read](../../theory/source.md#assumptions)\n```")
        self.reject("journey-target")

    def test_absolute_machine_link_is_rejected(self):
        self.mutate("../../theory/source.md#assumptions", "file:///private/example.md")
        with self.assertRaises(ValueError):
            self.mod.resolve_reader_link(self.repo, "docs/reader/RESEARCH-ATLAS.md", "file:///private/example.md")
        # CommonMark suppresses this forbidden link; the promised source
        # route therefore disappears instead of becoming an active URL.
        self.reject("journey-target")

    def test_symlink_reading_target_is_rejected(self):
        p = self.repo / "theory/source.md"
        p.unlink()
        p.symlink_to(self.repo / "theory/other.md")
        self.reject("reader-link")

    def test_semantic_false_friend_is_not_mechanically_certified(self):
        # Deliberately show the limit of the mechanical check. A separate
        # source-bound reviewer must reject this altered prose under T17.
        self.mutate("A conditional construction.", "This proves all real human cognition is correct.")
        self.assertEqual(self.check(), [])

    def test_page_check_does_not_modify_files(self):
        before = {p.relative_to(self.repo): p.read_bytes() for p in self.repo.rglob("*") if p.is_file()}
        self.assertEqual(self.check(), [])
        after = {p.relative_to(self.repo): p.read_bytes() for p in self.repo.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
