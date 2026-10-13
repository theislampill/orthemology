#!/usr/bin/env python3
"""Mechanical reader-pilot controls; not a classifier of philosophical truth.

Fixture-only scientific and profile paths use explicit fixture roots. They are
created in temporary repositories, not citations to missing project documents.
The real reader and generated-publication paths still exercise their actual
production contracts; the repository reference gate is unchanged.
"""
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
            "fixture-theory/core.md": "# Core\nA scoped definition.\n",
            "fixture-theory/multi.md": "# Multi\nAn additional component.\n",
            "fixture-theory/note.md": "# Note\nA substantive work without a PDF.\n",
            "fixture-theory/related.tex": r"\title{Related, differently titled source}",
            "fixture-theory/edition.pdf": "synthetic preserved edition, not a real PDF",
            "fixture-theory/lineage.md": "# Lineage\nExact build provenance is unverified.\n",
            "research/new/README.md": "# Later collection\nIts own scope.\n",
            "fixture-docs/profile.yaml": (
                "artifacts:\n"
                "- artifact_id: core\n  sources: [fixture-theory/core.md, fixture-theory/multi.md]\n"
                "  profile_kind: technical-paper\n"
                "- artifact_id: gallery\n  sources: [fixture-docs/gallery.md]\n"
                "  profile_kind: diagnostic-reference\n"
            ),
            "fixture-docs/gallery.md": "# Gallery\nReference only.\n",
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
                {"key": "fixture-theory", "include": ["fixture-theory/"], "exclude": [],
                 "owners": ["fixture-theory/lineage.md"]},
                {"key": "later", "include": ["research/new/"], "exclude": [],
                 "owners": ["research/new/README.md"]},
                {"key": "fixture-docs", "include": ["fixture-docs/"], "exclude": [],
                 "owners": ["fixture-docs/profile.yaml"]},
                {"key": "publication", "include": ["publication/", "artifacts/"],
                 "exclude": [], "owners": ["fixture-docs/profile.yaml"]},
            ],
            "required_work_sources": ["fixture-theory/core.md", "fixture-theory/note.md"],
            "publication_profile": "fixture-docs/profile.yaml",
            "edition_constraints": [{
                "source": "fixture-theory/related.tex", "rendering": "fixture-theory/edition.pdf",
                "permitted_relation": "related-source",
                "basis": "fixture-theory/lineage.md",
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
                 "source_keys": ["fixture-theory/core.md", "fixture-theory/multi.md"], "artifact_id": "core"},
                {"key": "note", "title": "Substantive note", "role": "research-note",
                 "source_keys": ["fixture-theory/note.md"]},
                {"key": "related", "title": "Related source", "role": "research-note",
                 "source_keys": ["fixture-theory/related.tex"]},
                {"key": "edition", "title": "Preserved edition", "role": "preserved-edition",
                 "source_keys": ["fixture-theory/edition.pdf"]},
                {"key": "gallery", "title": "Reference gallery", "role": "supporting-reference",
                 "source_keys": ["fixture-docs/gallery.md"], "artifact_id": "gallery"},
            ],
            "relations": [{
                "from": "fixture-theory/related.tex", "to": "fixture-theory/edition.pdf",
                "kind": "related-source", "basis": "fixture-theory/lineage.md",
            }],
            "probes": [
                {"key": "recognition-correction", "works": ["note"],
                 "sources": ["fixture-theory/note.md"]},
                {"key": "tensor-geometry", "works": ["core"],
                 "sources": ["fixture-theory/core.md"]},
                {"key": "cross-avenue", "works": ["note", "core"],
                 "sources": ["fixture-theory/note.md", "fixture-theory/core.md"]},
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
        altered["collections"].append({"key": "duplicate", "include": ["fixture-theory/"],
                                      "exclude": [], "owners": ["fixture-theory/core.md"]})
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
        p = self.repo / "fixture-theory/note.md"
        before = p.read_bytes()
        p.write_bytes(before + b"Changed premise.\n")
        self.assertNotEqual(p.read_bytes(), before)
        self.reject(self.check(), "source-drift")

    def test_symlink_source_is_not_followed(self):
        p = self.repo / "fixture-theory/note.md"
        p.unlink()
        p.symlink_to(self.repo / "fixture-theory/core.md")
        self.reject(self.check(), "unsafe-source")

    def test_parent_symlink_is_not_followed(self):
        p = self.repo / "elsewhere"
        p.symlink_to(self.repo / "fixture-theory", target_is_directory=True)
        altered = deepcopy(self.cross)
        altered["sources"]["fixture-theory/note.md"]["path"] = "elsewhere/note.md"
        self.reject(self.check(cross=altered), "unsafe-source")

    def test_path_traversal_rejected(self):
        altered = deepcopy(self.cross)
        altered["sources"]["fixture-theory/note.md"]["path"] = "../outside.md"
        self.reject(self.check(cross=altered), "unsafe-source")

    def test_missing_composite_component(self):
        altered = deepcopy(self.cross)
        altered["works"][0]["source_keys"].remove("fixture-theory/multi.md")
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
        altered["sources"]["fixture-theory/note.md"]["path"] = "fixture-theory/core.md"
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
        p = self.repo / "fixture-theory/note.md"
        before = p.read_bytes()
        p.write_bytes(before + b"A different scientific conclusion.\n")
        altered = deepcopy(self.cross)
        altered["sources"]["fixture-theory/note.md"]["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertNotEqual(p.read_bytes(), before)
        self.reject(self.check(cross=altered), "baseline-source")

    def test_source_executable_mode_is_preserved(self):
        p = self.repo / "fixture-theory/note.md"
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

    def second_edition_fixture(self):
        profile = self.repo / "fixture-docs/profile.yaml"
        profile.write_text(profile.read_text() +
                          "- artifact_id: core-second\n  sources: [fixture-theory/core.md, fixture-theory/multi.md]\n"
                          "  profile_kind: technical-paper\n")
        edition = self.repo / "artifacts/core-second.pdf"
        edition.write_text("synthetic second governed edition")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture second edition")
        owners, cross = deepcopy(self.owners), deepcopy(self.cross)
        owners["baseline"]["commit"] = self.git("rev-parse", "HEAD").strip()
        cross["sources"]["fixture-docs/profile.yaml"]["sha256"] = hashlib.sha256(profile.read_bytes()).hexdigest()
        cross["sources"]["artifacts/core-second.pdf"] = {
            "path": "artifacts/core-second.pdf",
            "sha256": hashlib.sha256(edition.read_bytes()).hexdigest(),
            "read_scope": "fixture only",
        }
        return owners, cross

    def test_second_governed_edition_does_not_duplicate_the_work(self):
        owners, cross = self.second_edition_fixture()
        count = len(cross["works"])
        cross["works"][0]["reading_forms"] = [
            {"source": "artifacts/core.pdf", "relationship": "governed-rendering"},
            {"source": "artifacts/core-second.pdf", "artifact_id": "core-second",
             "relationship": "governed-rendering"},
        ]
        self.assertEqual(self.check(owners=owners, cross=cross), [])
        self.assertEqual(len(cross["works"]), count)

    def test_new_governed_edition_cannot_disappear(self):
        owners, cross = self.second_edition_fixture()
        self.reject(self.check(owners=owners, cross=cross), "artifact")

    def test_second_edition_must_target_its_own_governed_pdf(self):
        owners, cross = self.second_edition_fixture()
        cross["works"][0]["reading_forms"] = [
            {"source": "artifacts/gallery.pdf", "artifact_id": "core-second",
             "relationship": "governed-rendering"},
        ]
        self.reject(self.check(owners=owners, cross=cross), "rendering-target")

    def ci_owner_fixture(self):
        path = self.repo / ".github/workflows/validate.yml"
        path.parent.mkdir(parents=True)
        before = ("name: validate\npermissions:\n  contents: read\njobs:\n"
                  "  validate:\n    steps:\n"
                  "      - name: Repository hygiene + honesty checks\n"
                  "        run: python scripts/validate_repo.py\n"
                  "      - name: T20 v6 independent public projection and source boundaries\n"
                  "        run: python -B scripts/validate_t20_v6_projection.py\n")
        step = ("      - name: Reader pilot source, edition and navigation controls (not semantic acceptance)\n"
                "        run: |\n"
                "          python -B tests/test_reader_census.py\n"
                "          python -B -O tests/test_reader_census.py\n"
                "          python -B tests/test_reader_pilot.py\n"
                "          python -B -O tests/test_reader_pilot.py\n"
                "          python -B scripts/check_reader_pilot.py\n")
        path.write_text(before)
        self.git("add", ".github/workflows/validate.yml")
        self.git("commit", "-qm", "fixture operational CI owner")
        owners = deepcopy(self.owners)
        owners["baseline"]["commit"] = self.git("rev-parse", "HEAD").strip()
        owners["collections"].append({
            "key": "ci", "include": [".github/"], "exclude": [],
            "owners": [".github/workflows/validate.yml"],
        })
        anchor = "      - name: T20 v6 independent public projection and source boundaries\n"
        candidate = before.replace(anchor, step + anchor)
        path.write_text(candidate)
        return path, owners, before, candidate, step

    def test_exact_reader_ci_addition_retains_pinned_operational_owner(self):
        path, owners, before, candidate, step = self.ci_owner_fixture()
        self.assertNotEqual(candidate, before)
        self.assertEqual(self.check(owners=owners), [])

    def test_ci_owner_extension_cannot_remove_an_existing_gate(self):
        path, owners, before, candidate, step = self.ci_owner_fixture()
        path.write_text(candidate.replace("        run: python scripts/validate_repo.py\n", "        run: true\n"))
        self.reject(self.check(owners=owners), "owner")

    def test_ci_owner_extension_cannot_expand_token_permissions(self):
        path, owners, before, candidate, step = self.ci_owner_fixture()
        path.write_text(candidate.replace("contents: read", "contents: write"))
        self.reject(self.check(owners=owners), "owner")

    def test_ci_owner_extension_cannot_duplicate_the_reader_step(self):
        path, owners, before, candidate, step = self.ci_owner_fixture()
        path.write_text(candidate.replace(step, step + step))
        self.reject(self.check(owners=owners), "owner")

    def test_ci_owner_extension_cannot_relax_the_reader_command(self):
        path, owners, before, candidate, step = self.ci_owner_fixture()
        path.write_text(candidate.replace("python -B scripts/check_reader_pilot.py", "python -B scripts/check_reader_pilot.py || true"))
        self.reject(self.check(owners=owners), "owner")

    def test_ci_owner_extension_keeps_the_original_file_mode(self):
        path, owners, before, candidate, step = self.ci_owner_fixture()
        path.chmod(0o755)
        self.reject(self.check(owners=owners), "owner")

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
        (self.repo / "fixture-theory").mkdir()
        (self.repo / "fixture-theory/source.md").write_text("# Source\n## Assumptions\nA scoped fixture.\n")
        (self.repo / "fixture-theory/other.md").write_text("# Different source\nA different fixture.\n")
        self.pages = ["RESEARCH-ATLAS.md", "PAPER-CATALOGUE.md", "RESULT-INDEX.md",
                      "CURRENT-FRONTIERS.md", "APPLICATIONS.md", "VERIFICATION-GUIDE.md"]
        for name in self.pages:
            path = self.repo / "docs/reader" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Reader\n\n## Overview\nA conditional construction.\n[Read][source]\n\n"
                            "[source]: ../../fixture-theory/source.md#assumptions\n")
        self.cross = {
            "sources": {"source": {"path": "fixture-theory/source.md"}},
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
        self.mutate("../../fixture-theory/source.md#assumptions", "../../fixture-theory/other.md")
        self.reject("journey-target")

    def test_wrong_valid_source_fragment_is_not_the_requested_section(self):
        p = self.repo / "fixture-theory/source.md"
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
        self.mutate("[Read][source]", "```text\n[Read](../../fixture-theory/source.md#assumptions)\n```")
        self.reject("journey-target")

    def test_absolute_machine_link_is_rejected(self):
        self.mutate("../../fixture-theory/source.md#assumptions", "file:///private/example.md")
        with self.assertRaises(ValueError):
            self.mod.resolve_reader_link(self.repo, "docs/reader/RESEARCH-ATLAS.md", "file:///private/example.md")
        # CommonMark suppresses this forbidden link; the promised source
        # route therefore disappears instead of becoming an active URL.
        self.reject("journey-target")

    def test_symlink_reading_target_is_rejected(self):
        p = self.repo / "fixture-theory/source.md"
        p.unlink()
        p.symlink_to(self.repo / "fixture-theory/other.md")
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


class ReaderFixtureReferenceTests(unittest.TestCase):
    def test_temporary_fixture_names_are_not_ghost_repository_citations(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_internal_references as refs
        owner = "tests/test_reader_pilot.py"
        text = (ROOT / owner).read_text(encoding="utf-8")
        missing = sorted({path for path, _ in refs._citation_occurrences(
            owner, text, root=str(ROOT), successor_sources={})
            if not refs._resolves(owner, path)})
        self.assertEqual(missing, [], "Synthetic fixture paths must not claim live repository sources")



class HistoricalMetadataPinTests(unittest.TestCase):
    """Historical source custody survives an authorised current-index addition."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("reader_metadata_pin", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        owner_path = ROOT / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json"
        baseline = json.loads(owner_path.read_text())["baseline"]["commit"]
        cls.manifest_path = "research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json"
        oid = subprocess.check_output(["git", "rev-parse", baseline + ":" + cls.manifest_path], cwd=ROOT).decode().strip()
        cls.row = {"path": cls.manifest_path, "git_oid": oid}
        cls.original = json.loads(subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT))
        cls.identity = "94fb4c0a0fbe7406570711b222ac0e5dbc7493867cd28cb6f0ef08c6fea99074"

    def candidate(self):
        value = deepcopy(self.original)
        row = next(r for r in value["objects"] if r["source_sha256"] == self.identity)
        row.update(repository_revision="7efc6217c090b92d65f2c4cb8b011c18eb96bf7c",
                   git_blob="d4ec27e7da404b830f1a6fe687809c1cf2011413")
        return value, row

    def permitted(self, value):
        gate = getattr(self.mod, "permitted_historical_status_pin", None)
        return bool(gate and gate(ROOT, self.row, json.dumps(value).encode()))

    def test_exact_historical_status_pin_preserves_source_identity(self):
        value, row = self.candidate()
        self.assertTrue(self.permitted(value), "the exact historical metadata pin is not admitted")
        self.assertEqual(row["public_sha256"], self.identity)
        self.assertEqual(row["source_bytes"], 5312)

    def test_historical_pin_cannot_replace_the_scientific_source_hash(self):
        value, row = self.candidate()
        row["public_sha256"] = "0" * 64
        self.assertFalse(self.permitted(value))

    def test_historical_pin_cannot_use_a_moving_revision(self):
        value, row = self.candidate()
        row["repository_revision"] = "HEAD"
        self.assertFalse(self.permitted(value))

    def test_historical_pin_cannot_change_an_unrelated_row(self):
        value, row = self.candidate()
        value["objects"][0]["role"] = "reclassified"
        self.assertFalse(self.permitted(value))

    def test_historical_pin_cannot_claim_another_git_blob(self):
        value, row = self.candidate()
        row["git_blob"] = "0" * 40
        self.assertFalse(self.permitted(value))



class TwelfthCollectionCoverageTests(unittest.TestCase):
    """Bounded semantic-catalogue coverage, not a new theorem registry."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("reader_twelfth", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        prefix = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.owners = json.loads((prefix / "OWNER-MAP.json").read_text())
        cls.cross = json.loads((prefix / "CROSSWALK.json").read_text())
        identity_path = (
            "experiments/orthemology-v5-successors/source-store/"
            "ec29806cb3087a8a707341d352bbbf8c818a536ce0083a8e6cf75a6b75d3e7bb/"
            "CHECKPOINT_IDENTITY.json"
        )
        raw = subprocess.check_output(
            ["git", "show", cls.owners["baseline"]["commit"] + ":" + identity_path], cwd=ROOT)
        cls.members = json.loads(raw)["payloads"]

    def test_all_nine_declared_twelfth_texts_have_work_and_reading_routes(self):
        # The denominator is the original checkpoint owner, not a list copied
        # from whichever catalogue entries happen to survive a change.
        self.assertEqual(len(self.members), 9)
        sources = self.cross["sources"]
        catalogue = ROOT / "docs/reader/PAPER-CATALOGUE.md"
        headings = self.mod.markdown_index(catalogue.read_text())["anchors"]
        for member in self.members:
            with self.subTest(source=member["path"]):
                keys = {k for k, v in sources.items() if v["sha256"] == member["sha256"]}
                self.assertTrue(keys, "Declared Twelfth source is absent from the crosswalk")
                represented = [w for w in self.cross["works"] if keys.intersection(w["source_keys"])]
                self.assertTrue(represented, "A collection link is not a work-level disposition")
                for key in keys:
                    path = sources[key]["path"]
                    self.assertIn(path, self.owners["required_work_sources"])
                    body = (ROOT / path).read_bytes()
                    self.assertEqual(len(body), member["bytes"])
                    self.assertEqual(hashlib.sha256(body).hexdigest(), member["sha256"])
                for work in represented:
                    entry = work.get("catalogue_entry", "")
                    self.assertTrue(entry.startswith("docs/reader/PAPER-CATALOGUE.md#"))
                    fragment = entry.partition("#")[2]
                    self.assertIn(fragment, headings)
                    page = self.mod.markdown_index(catalogue.read_text())
                    selected = [h for h in page["headings"] if h[0] == fragment]
                    self.assertEqual(len(selected), 1)
                    _, level, start = selected[0]
                    end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
                    linked = set()
                    for line, href in page["links"]:
                        if start <= line < end:
                            target = self.mod.resolve_reader_link(ROOT, "docs/reader/PAPER-CATALOGUE.md", href)
                            if target is not None:
                                linked.add(target[0])
                    self.assertTrue(any(sources[key]["path"] in linked for key in keys),
                                    "The named work section must directly reach its source")

    def test_source_review_does_not_become_another_independent_theorem(self):
        works = [w for w in self.cross["works"] if w["key"] == "t12-concentration-review"]
        self.assertEqual(len(works), 1, "The substantive review needs an explicit role")
        self.assertEqual(works[0]["role"], "review")
        self.assertIn("t12-concentration-review", self.cross["sources"])

    def test_each_new_twelfth_work_omission_is_detected(self):
        self.assertEqual(self.mod.check(ROOT, self.owners, self.cross), [])
        for member in self.members:
            keys = {k for k, v in self.cross["sources"].items() if v["sha256"] == member["sha256"]}
            altered = deepcopy(self.cross)
            before = len(altered["works"])
            altered["works"] = [w for w in altered["works"] if not keys.intersection(w["source_keys"])]
            with self.subTest(source=member["path"]):
                self.assertLess(len(altered["works"]), before, "The omission must change the catalogue")
                errors = self.mod.check(ROOT, self.owners, altered)
                self.assertTrue(any(e.startswith("missing-work:") for e in errors), errors)




class ApplicationCollectionCoverageTests(unittest.TestCase):
    """A fifty-file source population is not fifty papers or deployed services."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("reader_applications", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        record = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.owners = json.loads((record / "OWNER-MAP.json").read_text())
        cls.cross = json.loads((record / "CROSSWALK.json").read_text())
        cls.population = {r["path"] for r in cls.mod.entries_at(ROOT, cls.owners["baseline"]["commit"])
                          if r["path"].startswith("applications/")}
        # Independently selected substantive sources, not an output-derived count.
        cls.primary = {
            "applications/daee-epistemics/NOETIC-ORTHING-APPLICATION.md",
            "applications/daee-epistemics/EPISTEMOLOGICAL-AND-METAPHYSICAL-BOUNDARY.md",
            "applications/daee-epistemics/MULTI-TARGET-NOETIC-ORTHING.md",
            "applications/daee-epistemics/META-NOETIC-MEMETICS-AND-DYNAMIC-ORTHING.md",
            "applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md",
            "applications/daee-epistemics/SEMANTIC-OPERATOR-CONTRACT.yaml",
            "applications/latent-state-orthing/DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md",
            "applications/agentic-runtime/SOMNUS-CANDIDATE-INVENTORY.yaml",
            "applications/agentic-runtime/HERMES-WRITEBACK-ADOPTION-PROFILE.yaml",
            "applications/agentic-runtime/COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml",
        }

    def disposition_errors(self, cross):
        sources, works = cross["sources"], {w["key"]: w for w in cross["works"]}
        permitted = {"work-source", "collection-guide", "source-boundary", "crosswalk",
                     "notation-owner", "contract", "schema", "example", "fixture"}
        seen, errors = [], []
        for row in cross.get("application_dispositions", []):
            source, work = sources.get(row.get("source")), works.get(row.get("work"))
            if not source or not work or row.get("role") not in permitted:
                errors.append("unbound-disposition")
                continue
            path = source["path"]
            seen.append(path)
            if path not in self.population:
                errors.append("outside-population")
            if row["role"] == "work-source" and row["source"] not in work["source_keys"]:
                errors.append("wrong-work-source")
            if path.endswith(".schema.json") and row["role"] != "schema":
                errors.append("schema-is-not-a-paper")
        if set(seen) != self.population or len(seen) != len(set(seen)):
            errors.append("population-coverage")
        bound_primary = {sources[k]["path"] for w in works.values()
                         for k in w["source_keys"] if k in sources}
        if not self.primary <= bound_primary:
            errors.append("missing-substantive-work")
        return errors

    def test_every_baseline_application_file_has_one_explained_disposition(self):
        self.assertEqual(len(self.population), 50)
        self.assertEqual(self.disposition_errors(self.cross), [])

    def test_application_work_sections_reach_their_exact_sources(self):
        page = self.mod.markdown_index((ROOT / "docs/reader/PAPER-CATALOGUE.md").read_text())
        sources = self.cross["sources"]
        for path in sorted(self.primary):
            keys = {k for k,v in sources.items() if v["path"] == path}
            works = [w for w in self.cross["works"] if keys.intersection(w["source_keys"])]
            with self.subTest(source=path):
                self.assertTrue(works, "The application has no work-level reader disposition")
                self.assertIn(path, self.owners["required_work_sources"])
                for work in works:
                    entry = work.get("catalogue_entry", "")
                    self.assertTrue(entry.startswith("docs/reader/PAPER-CATALOGUE.md#"))
                    selected = [h for h in page["headings"] if h[0] == entry.partition("#")[2]]
                    self.assertEqual(len(selected), 1)
                    _, level, start = selected[0]
                    end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
                    targets = [self.mod.resolve_reader_link(ROOT, "docs/reader/PAPER-CATALOGUE.md", href)
                               for line,href in page["links"] if start <= line < end]
                    self.assertTrue(any(t and t[0] == path for t in targets),
                                    "A package README alone is not the promised work route")

    def test_each_application_disposition_omission_is_detected(self):
        self.assertEqual(self.disposition_errors(self.cross), [])
        for i, row in enumerate(self.cross["application_dispositions"]):
            with self.subTest(source=row["source"]):
                changed = deepcopy(self.cross)
                del changed["application_dispositions"][i]
                self.assertIn("population-coverage", self.disposition_errors(changed))

    def test_schema_cannot_be_promoted_to_an_independent_paper(self):
        self.assertEqual(self.disposition_errors(self.cross), [])
        changed = deepcopy(self.cross)
        row = next(r for r in changed["application_dispositions"]
                   if changed["sources"][r["source"]]["path"].endswith(".schema.json"))
        row["role"] = "work-source"
        self.assertIn("schema-is-not-a-paper", self.disposition_errors(changed))

    def test_runtime_outlines_keep_their_source_declared_nonexecution(self):
        import yaml
        sources = self.cross["sources"]
        for path in sorted(p for p in self.primary if p.startswith("applications/agentic-runtime/")):
            with self.subTest(source=path):
                original = yaml.safe_load((ROOT / path).read_text())
                self.assertEqual(original["status"], "outline-only")
                keys = {k for k,v in sources.items() if v["path"] == path}
                represented = [w for w in self.cross["works"] if keys.intersection(w["source_keys"])]
                self.assertEqual(len(represented), 1)
                self.assertEqual(represented[0]["role"], "application-proposal")


class ApplicationReaderRouteTests(unittest.TestCase):
    """Require source-bearing use routes, not just a list of application titles."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("reader_application_routes", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.page_path = "docs/reader/APPLICATIONS.md"
        cls.text = (ROOT / cls.page_path).read_text()
        cls.routes = {
            "a-corrective-step-that-legitimately-ends-in-hold": {
                "applications/daee-epistemics/CORRECTIVE-TRANSITION.example.json",
                "applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md",
                "applications/daee-epistemics/SEMANTIC-OPERATOR-CONTRACT.yaml",
            },
            "learning-without-silently-changing-the-analysis": {
                "applications/latent-state-orthing/DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md",
                "applications/latent-state-orthing/UPDATE-COUPLING.yaml",
            },
            "agentic-coordination-and-writeback-outlines": {
                "applications/agentic-runtime/SOMNUS-CANDIDATE-INVENTORY.yaml",
                "applications/agentic-runtime/HERMES-WRITEBACK-ADOPTION-PROFILE.yaml",
                "applications/agentic-runtime/COLLECTIVE-SOMNUS-TRANSCLUSION-PROFILE.yaml",
            },
        }

    def targets(self, text, heading):
        page = self.mod.markdown_index(text)
        selected = [h for h in page["headings"] if h[0] == heading]
        if len(selected) != 1:
            return set()
        _, level, start = selected[0]
        end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
        found = set()
        for line, href in page["links"]:
            if start <= line < end:
                try:
                    target = self.mod.resolve_reader_link(ROOT, self.page_path, href)
                except ValueError:
                    continue
                if target is not None:
                    found.add(target[0])
        return found

    def test_worked_application_routes_reach_their_controlling_sources(self):
        for heading, expected in self.routes.items():
            with self.subTest(heading=heading):
                self.assertTrue(expected <= self.targets(self.text, heading),
                                "A worked application route is missing its actual source or contract")

    def test_each_worked_route_loses_coverage_when_its_source_link_is_removed(self):
        for heading, expected in self.routes.items():
            for path in expected:
                with self.subTest(heading=heading, source=path):
                    href = "../../" + path
                    self.assertIn(href, self.text, "Control must change an existing source link")
                    mutated = self.text.replace(href, "#removed-source-control")
                    self.assertNotEqual(mutated, self.text)
                    self.assertFalse(expected <= self.targets(mutated, heading))


class IdentityLineageCoverageTests(unittest.TestCase):
    """Read the original group owners, not a self-selected catalogue denominator."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("reader_identity_lineage", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        prefix = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.owners = json.loads((prefix / "OWNER-MAP.json").read_text())
        cls.cross = json.loads((prefix / "CROSSWALK.json").read_text())
        cls.catalogue = "docs/reader/PAPER-CATALOGUE.md"
        cls.text = (ROOT / cls.catalogue).read_text()
        cls.baseline = cls.owners["baseline"]["commit"]
        cls.members = set()
        for group in ("t13-identity", "t14-identity"):
            path = "experiments/orthemology-v5-successors/groups/" + group + "/README.md"
            raw = subprocess.check_output(["git", "show", cls.baseline + ":" + path], cwd=ROOT).decode()
            for _, href in cls.mod.markdown_index(raw)["links"]:
                if "source-store/" in href and href.endswith((".md", ".lean")):
                    target = cls.mod.resolve_reader_link(ROOT, path, href)
                    cls.members.add(target[0])
        cls.results = json.loads(subprocess.check_output([
            "git", "show", cls.baseline + ":docs/provenance/v5-successors/RESULT_STATUS.json"], cwd=ROOT))

    def routes(self, text, cross):
        page = self.mod.markdown_index(text)
        errors = []
        for member in sorted(self.members):
            keys = {k for k, v in cross["sources"].items() if v["path"] == member}
            works = [w for w in cross["works"] if keys.intersection(w["source_keys"])]
            if not keys or not works:
                errors.append("missing-work: " + member)
                continue
            reachable = False
            for work in works:
                entry = work.get("catalogue_entry", "")
                if not entry.startswith(self.catalogue + "#"):
                    continue
                fragment = entry.partition("#")[2]
                selected = [h for h in page["headings"] if h[0] == fragment]
                if len(selected) != 1:
                    continue
                _, level, start = selected[0]
                end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
                for line, href in page["links"]:
                    if start <= line < end:
                        target = self.mod.resolve_reader_link(ROOT, self.catalogue, href)
                        if target is not None and target[0] == member:
                            reachable = True
            if not reachable:
                errors.append("missing-route: " + member)
        return errors

    def test_all_seven_source_bodies_have_work_and_section_routes(self):
        self.assertEqual(len(self.members), 7)
        self.assertEqual(self.routes(self.text, self.cross), [])
        self.assertTrue(self.members <= set(self.owners["required_work_sources"]))

    def test_each_identity_work_omission_is_detected(self):
        self.assertEqual(self.routes(self.text, self.cross), [])
        for member in sorted(self.members):
            keys = {k for k, v in self.cross["sources"].items() if v["path"] == member}
            altered = deepcopy(self.cross)
            altered["works"] = [w for w in altered["works"] if not keys.intersection(w["source_keys"])]
            with self.subTest(source=member):
                self.assertLess(len(altered["works"]), len(self.cross["works"]))
                self.assertTrue(self.routes(self.text, altered))
                errors = self.mod.check(ROOT, self.owners, altered)
                self.assertTrue(any(e.startswith("missing-work:") for e in errors), errors)

    def test_each_real_source_route_cannot_be_retargeted_to_another_file(self):
        self.assertEqual(self.routes(self.text, self.cross), [])
        for member in sorted(self.members):
            # Alter every use of this source target, not its visible link label.
            href = "../../" + member
            altered = self.text.replace(href, "../../README.md")
            with self.subTest(source=member):
                self.assertNotEqual(altered, self.text)
                self.assertIn("missing-route: " + member, self.routes(altered, self.cross))

    def test_historical_open_note_has_one_work_and_statement_specific_resolution(self):
        sources = self.cross["sources"]
        keys = {k for k, v in sources.items() if v["path"].endswith("/RESIDUAL_IDENTITY_COMPLETENESS_FEASIBILITY_v1.md")}
        works = [w for w in self.cross["works"] if keys.intersection(w["source_keys"])]
        self.assertEqual(len(works), 1, "Two result scopes do not make two historical notes")
        relations = [r for r in self.cross["relations"] if r.get("from") in keys
                     and r.get("kind") == "resolves-specific-open-obligation"]
        self.assertEqual(len(relations), 1)
        target = sources[relations[0]["to"]]["path"]
        self.assertTrue(target.endswith("/Intensional_Identity_Separation_and_Closed_Identity_Conversion.md"))
        self.assertEqual(relations[0]["basis"], relations[0]["to"])

    def test_written_identity_and_formal_component_share_work_but_repair_is_distinct(self):
        def work_for(suffix):
            keys = {k for k, v in self.cross["sources"].items() if v["path"].endswith(suffix)}
            return {w["key"] for w in self.cross["works"] if keys.intersection(w["source_keys"])}
        written = work_for("/Intensional_Identity_Separation_and_Closed_Identity_Conversion.md")
        formal = work_for("/IntensionalIdentityTheorems.lean")
        repair = work_for("/ExtensionalRepairTheorems.lean")
        self.assertEqual(len(written), 1)
        self.assertEqual(formal, written, "A formal component is not another copy of the paper")
        self.assertEqual(len(repair), 1)
        self.assertFalse(written.intersection(repair), "HasE is a separately named development")

    def test_declared_identity_result_scopes_remain_findable(self):
        expected = {r["id"] for r in self.results["results"]
                    if r["id"].startswith(("T13-", "T14-")) and r.get("calculus") != "NONE"}
        self.assertEqual(len(expected), 12)
        index = (ROOT / "docs/reader/RESULT-INDEX.md").read_text()
        for identity in sorted(expected):
            with self.subTest(result=identity):
                self.assertIn("`" + identity + "`", index)
        # This is discoverability, not automated adjudication of the prose.



class FifteenthCompendiumCoverageTests(unittest.TestCase):
    """Constituent papers come from the original volume, not the new catalogue."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("reader_fifteenth", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        prefix = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.owners = json.loads((prefix / "OWNER-MAP.json").read_text())
        cls.cross = json.loads((prefix / "CROSSWALK.json").read_text())
        cls.baseline = cls.owners["baseline"]["commit"]
        cls.catalogue = "docs/reader/PAPER-CATALOGUE.md"
        cls.text = (ROOT / cls.catalogue).read_text()
        group = "experiments/orthemology-v5-successors/groups/t15-identity/README.md"
        raw = subprocess.check_output(["git", "show", cls.baseline + ":" + group], cwd=ROOT).decode()
        matches = {cls.mod.resolve_reader_link(ROOT, group, href)[0]
                   for _, href in cls.mod.markdown_index(raw)["links"]
                   if href.endswith("/Orthemology_Fifteenth_Mathematical_Compendium_v1_20261005.md")}
        if len(matches) != 1:
            raise ValueError("The original guide must identify one compendium body")
        cls.volume = matches.pop()
        text = subprocess.check_output(["git", "show", cls.baseline + ":" + cls.volume], cwd=ROOT).decode()
        lines = text.splitlines()
        cls.chapters = {anchor: lines[line][3:] for anchor, level, line
                        in cls.mod.markdown_index(text)["headings"]
                        if level == 2 and lines[line] != "## Relation to established methods"}
        cls.results = json.loads(subprocess.check_output([
            "git", "show", cls.baseline + ":docs/provenance/v5-successors/RESULT_STATUS.json"], cwd=ROOT))

    def bindings(self, cross):
        keys = {key for key, value in cross["sources"].items() if value["path"] == self.volume}
        result = {anchor: [] for anchor in self.chapters}
        for work in cross["works"]:
            for section in work.get("reading_forms", []):
                if section.get("source") in keys and section.get("fragment") in result:
                    if section["source"] in work["source_keys"]:
                        result[section["fragment"]].append(work)
        return result

    def routes(self, text, cross):
        page = self.mod.markdown_index(text)
        errors = []
        for chapter, works in self.bindings(cross).items():
            if len(works) != 1:
                errors.append("constituent-work: " + chapter)
                continue
            entry = works[0].get("catalogue_entry", "")
            if not entry.startswith(self.catalogue + "#"):
                errors.append("constituent-route: " + chapter)
                continue
            selected = [h for h in page["headings"] if h[0] == entry.partition("#")[2]]
            if len(selected) != 1:
                errors.append("constituent-route: " + chapter)
                continue
            _, level, start = selected[0]
            end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
            found = {self.mod.resolve_reader_link(ROOT, self.catalogue, href)
                     for line, href in page["links"] if start <= line < end}
            if (self.volume, chapter) not in found:
                errors.append("constituent-route: " + chapter)
        return errors

    def test_all_six_source_named_papers_have_exact_section_routes(self):
        self.assertEqual(len(self.chapters), 6)
        self.assertEqual(self.routes(self.text, self.cross), [])
        self.assertIn(self.volume, self.owners["required_work_sources"])
        for chapter, works in self.bindings(self.cross).items():
            self.assertEqual(works[0]["title"], self.chapters[chapter])

    def test_each_constituent_omission_fails_even_when_volume_remains_linked(self):
        self.assertEqual(self.routes(self.text, self.cross), [])
        for chapter, works in self.bindings(self.cross).items():
            altered = deepcopy(self.cross)
            altered["works"] = [w for w in altered["works"] if w["key"] != works[0]["key"]]
            with self.subTest(chapter=chapter):
                self.assertEqual(len(altered["works"]), len(self.cross["works"]) - 1)
                self.assertIn("constituent-work: " + chapter, self.routes(self.text, altered))

    def test_valid_volume_link_or_other_chapter_is_not_the_required_paper(self):
        self.assertEqual(self.routes(self.text, self.cross), [])
        for chapter in self.chapters:
            href = "../../" + self.volume + "#" + chapter
            other = next(c for c in self.chapters if c != chapter)
            for replacement in ("../../" + self.volume, "../../" + self.volume + "#" + other):
                with self.subTest(chapter=chapter, replacement=replacement):
                    self.assertIn(href, self.text)
                    changed = self.text.replace(href, replacement)
                    self.assertNotEqual(changed, self.text)
                    self.assertIn("constituent-route: " + chapter, self.routes(changed, self.cross))

    def test_duplicate_edition_entry_does_not_become_a_second_constituent(self):
        self.assertEqual(self.routes(self.text, self.cross), [])
        chapter, works = next(iter(self.bindings(self.cross).items()))
        altered = deepcopy(self.cross)
        duplicate = deepcopy(works[0])
        duplicate["key"] += "-synthetic-duplicate-edition"
        altered["works"].append(duplicate)
        self.assertIn("constituent-work: " + chapter, self.routes(self.text, altered))

    def test_lean_checker_and_json_reference_support_the_same_restricted_paper(self):
        chapter = next(c for c, title in self.chapters.items() if title.startswith("Restricted Semantic"))
        works = self.bindings(self.cross)[chapter]
        self.assertEqual(len(works), 1)
        support = {self.cross["sources"][key]["path"] for key in works[0].get("supporting_source_keys", [])}
        for name in ("IdentityChecker.lean", "RestrictedCompiler.lean", "certificate_checker.py"):
            with self.subTest(component=name):
                self.assertTrue(any(path.endswith("/" + name) for path in support))
        # The formal procedure and wire-format reference remain different interfaces.
        self.assertTrue(any(path.endswith("/DECLARATION_CLAIM_MAP.md") for path in support))

    def test_source_owned_identity_and_collective_result_scopes_remain_findable(self):
        selected = {r["id"] for r in self.results["results"]
                    if (r["id"].startswith("T15-") and r.get("calculus") != "NONE")
                    or (r["id"].startswith("D18-T15-") and
                        "T15-COMPENDIUM-DERIVED-MARKDOWN" in r.get("source_ids", []))}
        self.assertGreaterEqual(len(selected), 20)
        index = (ROOT / "docs/reader/RESULT-INDEX.md").read_text()
        missing = {key for key in selected if "`" + key + "`" not in index}
        self.assertEqual(missing, set(), "Names alone do not establish the fidelity of the accompanying summaries")


if __name__ == "__main__":
    unittest.main()
