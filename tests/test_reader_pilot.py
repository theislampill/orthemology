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

    def test_a_research_software_work_has_a_distinct_honest_role(self):
        altered = deepcopy(self.cross)
        altered["works"][1]["role"] = "research-software"
        self.assertEqual(self.check(cross=altered), [])

    def test_valid_composite_and_distinct_related_edition(self):
        self.assertEqual(self.check(), [])


    def test_new_tracked_work_cannot_hide_behind_the_frozen_census(self):
        path = self.repo / "new-lab-area" / "substantive-note.unbuilt"
        path.parent.mkdir(parents=True)
        path.write_text("A synthetic new research work; no PDF is required.")
        self.git("add", "new-lab-area/substantive-note.unbuilt")
        self.reject(self.check(), "corpus-currentness")

    def test_new_committed_checkpoint_requires_disposition_even_with_old_sources_unchanged(self):
        path = self.repo / "research" / "later-checkpoint" / "new-result.md"
        path.parent.mkdir(parents=True)
        path.write_text("A fixture-only new item, not an original scientific claim.")
        self.git("add", "research/later-checkpoint/new-result.md")
        self.git("commit", "-qm", "fixture new checkpoint")
        self.reject(self.check(), "corpus-currentness")

    def test_unbound_baseline_source_change_is_not_invisible(self):
        path = self.repo / "fixture-theory" / "related.tex"
        altered = deepcopy(self.cross)
        altered["sources"].pop("fixture-theory/related.tex")
        altered["works"] = [w for w in altered["works"] if w["key"] != "related"]
        altered["relations"] = []
        owners = deepcopy(self.owners)
        owners["edition_constraints"] = []
        self.assertEqual(self.check(owners=owners, cross=altered), [])
        path.write_text(path.read_text()+"\nChanged the source outside the pilot slice.")
        self.reject(self.check(owners=owners, cross=altered), "corpus-currentness")

    def test_disposable_scratch_does_not_expand_the_tracked_corpus(self):
        path = self.repo / "untracked-research-scratch.md"
        path.write_text("Not admitted or committed to the public corpus.")
        self.assertEqual(self.check(), [])

    def test_admitted_reader_edit_does_not_require_a_scientific_rebaseline(self):
        path = self.repo / "docs" / "reader" / "PAPER-CATALOGUE.md"
        path.parent.mkdir(parents=True)
        path.write_text("# Synthetic reader surface\nNot new original research.")
        self.git("add", "docs/reader/PAPER-CATALOGUE.md")
        self.assertEqual(self.check(), [])

    def test_unknown_file_inside_reader_directory_is_not_a_blanket_exemption(self):
        path = self.repo / "docs" / "reader" / "unregistered-paper.tex"
        path.parent.mkdir(parents=True)
        path.write_text("A hypothetical unregistered source.")
        self.git("add", "docs/reader/unregistered-paper.tex")
        self.reject(self.check(), "corpus-currentness")

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


class ReportReanalysisCoverageTests(unittest.TestCase):
    """Bounded report/software coverage from original owners, not a new registry."""
    @classmethod
    def setUpClass(cls):
        import re
        spec = importlib.util.spec_from_file_location("report_reader_check", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.prefix = "docs/project-closure/reader-refactor-issue-35/"
        cls.cross = json.loads((ROOT / (cls.prefix + "CROSSWALK.json")).read_text())
        cls.owners = json.loads((ROOT / (cls.prefix + "OWNER-MAP.json")).read_text())
        cls.base = cls.owners["baseline"]["commit"]
        cls.catalogue = "docs/reader/PAPER-CATALOGUE.md"
        cls.text = (ROOT / cls.catalogue).read_text()
        def original(path):
            return subprocess.check_output(["git", "show", cls.base + ":" + path], cwd=ROOT).decode()
        def linked(guide, label):
            match = re.search(r"\[" + re.escape(label) + r"\]\(([^)]+)\)", original(guide))
            if match is None:
                raise AssertionError("Original owner no longer declares " + label)
            return cls.mod.resolve_reader_link(ROOT, guide, match.group(1))[0]
        cls.group = "experiments/orthemology-v5-successors/groups/t15-reanalysis/README.md"
        attribution = "experiments/orthemology-v5-successors/groups/t15-attribution/README.md"
        cls.report = linked(attribution, "Fifteenth main report")
        cls.readme = linked(cls.group, "Original portable-package instructions")
        checksums = linked(cls.group, "Original package checksums")
        cls.members = {checksums}
        cls.member_hashes = {}
        for line in original(checksums).splitlines():
            digest, name = line.split(None, 1)
            path = "experiments/orthemology-v5-successors/source-store/" + digest + "/" + Path(name).name
            body = subprocess.check_output(["git", "show", cls.base + ":" + path], cwd=ROOT)
            if hashlib.sha256(body).hexdigest() != digest:
                raise AssertionError("Original package-member identity mismatch")
            cls.members.add(path)
            cls.member_hashes[path] = digest
        cls.integration = {
            linked(cls.group, label) for label in (
                "fresh aggregate", "numerical validation", "execution summary", "environment identities")
        }
        cls.input_path = linked(cls.group, "Exact official input identities and parsing scope")
        cls.input_names = {v["name"] for v in json.loads(original(cls.input_path))["required_inputs"].values()}
        cls.fragments = {
            "finite-construction-and-renewed-function", "a-causal-totality-argument",
            "a-proposal-for-natural-standards", "occurrence-sensitive-language-and-the-present-stopping-point",
        }
        if not cls.fragments <= cls.mod.markdown_index(original(cls.report))["anchors"]:
            raise AssertionError("Expected report sections absent from the original baseline")

    def work(self, cross, path):
        keys = {k for k, v in cross["sources"].items() if v["path"] == path}
        matches = [w for w in cross["works"] if keys.intersection(w.get("source_keys", []))]
        return matches[0] if len(matches) == 1 else None

    def endpoints(self, text, owner, anchor):
        page = self.mod.markdown_index(text)
        chosen = [h for h in page["headings"] if h[0] == anchor]
        if len(chosen) != 1:
            return set()
        _, level, start = chosen[0]
        end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
        return {self.mod.resolve_reader_link(ROOT, owner, href)
                for line, href in page["links"] if start <= line < end}

    def errors(self, cross, text):
        errors = []
        for path in (self.report, self.readme):
            work = self.work(cross, path)
            if work is None:
                errors.append("missing-distinct-work:" + path)
                continue
            entry = work.get("catalogue_entry", "")
            if not entry.startswith(self.catalogue + "#") or (path, "") not in self.endpoints(text, self.catalogue, entry.partition("#")[2]):
                errors.append("missing-work-route:" + path)
        work = self.work(cross, self.readme)
        if work is not None:
            keys = work.get("source_keys", []) + work.get("supporting_source_keys", [])
            bound = {cross["sources"][k]["path"] for k in keys if k in cross["sources"]}
            for path in sorted((self.members | self.integration | {self.group}) - bound):
                errors.append("missing-package-component:" + path)
            if work["role"] != "research-software":
                errors.append("wrong-software-role")
        return errors

    def test_report_and_software_have_distinct_work_routes(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        report, software = self.work(self.cross, self.report), self.work(self.cross, self.readme)
        self.assertNotEqual(report["key"], software["key"])
        self.assertEqual(report["role"], "synthesis")
        self.assertIn(self.report, self.owners["required_work_sources"])
        self.assertIn(self.readme, self.owners["required_work_sources"])

    def test_all_original_package_members_and_replay_records_are_bound(self):
        self.assertEqual(len(self.members), 12)
        self.assertEqual(len(self.integration), 4)
        self.assertEqual(self.errors(self.cross, self.text), [])
        paths = {s["path"]: s for s in self.cross["sources"].values()}
        for path, digest in self.member_hashes.items():
            self.assertEqual(paths[path]["sha256"], digest)

    def test_each_omitted_component_or_work_is_detected(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for path in sorted(self.members | self.integration):
            altered = deepcopy(self.cross)
            altered["sources"] = {k:v for k,v in altered["sources"].items() if v["path"] != path}
            with self.subTest(omitted=path):
                self.assertTrue(self.errors(altered, self.text))
        for path in (self.report, self.readme):
            altered = deepcopy(self.cross)
            key = self.work(altered, path)["key"]
            altered["works"] = [w for w in altered["works"] if w["key"] != key]
            self.assertIn("missing-distinct-work:" + path, self.errors(altered, self.text))

    def test_source_assessments_have_actual_section_routes(self):
        owner = "docs/reader/RESULT-INDEX.md"
        text = (ROOT / owner).read_text()
        targets = self.endpoints(text, owner, "dated-report-assessments")
        for fragment in self.fragments:
            self.assertIn((self.report, fragment), targets)
            href = "../../" + self.report + "#" + fragment
            changed = text.replace(href, "../../" + self.report)
            self.assertNotEqual(changed, text)
            self.assertNotIn((self.report, fragment), self.endpoints(changed, owner, "dated-report-assessments"))
        for result_id in ("D18-T15-EMPIRICAL", "D15-T15-KOONS-TOTALITY", "D15-T15-LOCAL-NATURAL-STANDARDS"):
            self.assertIn("`" + result_id + "`", text)

    def test_software_is_not_duplicated_by_each_aggregate_or_fit_file(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        work = self.work(self.cross, self.readme)
        for other in self.cross["works"]:
            if other["key"] != work["key"]:
                principal = {self.cross["sources"][k]["path"] for k in other["source_keys"]}
                self.assertFalse(principal.intersection(self.members))
        bound_names = {Path(v["path"]).name for v in self.cross["sources"].values()}
        self.assertFalse(bound_names.intersection(self.input_names), "External participant inputs are not public reader bodies")


class PrimaryWorkCurationTests(unittest.TestCase):
    """Primary works need source-chapter routes, not another publication count."""
    @classmethod
    def setUpClass(cls):
        import yaml
        spec = importlib.util.spec_from_file_location("primary_reader_check", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        prefix = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.cross = json.loads((prefix / "CROSSWALK.json").read_text())
        cls.base = json.loads((prefix / "OWNER-MAP.json").read_text())["baseline"]["commit"]
        cls.catalogue = "docs/reader/PAPER-CATALOGUE.md"
        cls.text = (ROOT / cls.catalogue).read_text()
        profile = yaml.safe_load(subprocess.check_output([
            "git", "show", cls.base + ":docs/publication-profile.yaml"], cwd=ROOT))
        cls.artifacts = {a["artifact_id"]: set(a["sources"]) for a in profile["artifacts"]}
        # Exact source chapters selected by this bounded reading task. Their
        # existence is checked against the original corpus, not rendered output.
        cls.required = {
            "main-exposition": {"main": {
                "13-the-thesis-stated-as-an-integration-discipline",
                "85-worked-example-the-stopped-clock-validator", "13-empirical-program"}},
            "formal-reference": {"core": {"22a-endpoint-plus-bounded-trace",
                "52-distributed-episodes-graph-and-composition"},
                "multi": {"3-formal-residue-assessed-against-the-existing-core"}},
            "ground-of-intelligibility": {"ground": {"42-the-chain-with-each-step-labeled",
                "53-adjudication", "8-a-ground-capable-of-disclosure",
                "later-v11-authority-qualification"}},
            "athari-companion": {"athari": {"21-seven-speech-bearers",
                "32-perfection-genus-and-particulars-the-precise-taymiyyan-distinctions",
                "5-the-reciters-act-and-the-carried-word", "8-reason-and-revelation-the-final-accounting"}},
            "dynamic-orthability": {"dynamic": {"81-eight-modalities-that-must-not-collapse",
                "9-metaphysical-argument-map"}},
        }
        for requirements in cls.required.values():
            for key, fragments in requirements.items():
                path = cls.cross["sources"][key]["path"]
                body = subprocess.check_output(["git", "show", cls.base + ":" + path], cwd=ROOT).decode()
                if not fragments <= cls.mod.markdown_index(body)["anchors"]:
                    raise AssertionError("Expected original source chapters are missing: " + path)

    def targets(self, text, entry):
        if not entry.startswith(self.catalogue + "#"):
            return set()
        page = self.mod.markdown_index(text)
        chosen = [h for h in page["headings"] if h[0] == entry.partition("#")[2]]
        if len(chosen) != 1:
            return set()
        _, level, start = chosen[0]
        end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
        return {self.mod.resolve_reader_link(ROOT, self.catalogue, href)
                for line, href in page["links"] if start <= line < end}

    def errors(self, text, cross):
        errors = []
        for key, requirements in self.required.items():
            works = [w for w in cross["works"] if w["key"] == key]
            if len(works) != 1:
                errors.append("primary-work:" + key)
                continue
            targets = self.targets(text, works[0].get("catalogue_entry", ""))
            for source, fragments in requirements.items():
                for fragment in fragments:
                    if (cross["sources"][source]["path"], fragment) not in targets:
                        errors.append("primary-chapter:" + key + ":" + fragment)
        return errors

    def test_existing_primary_works_reach_their_load_bearing_source_chapters(self):
        self.assertEqual(self.errors(self.text, self.cross), [])

    def test_generic_source_or_other_valid_chapter_does_not_replace_argument(self):
        self.assertEqual(self.errors(self.text, self.cross), [])
        for key, requirements in self.required.items():
            for source, fragments in requirements.items():
                path = self.cross["sources"][source]["path"]
                for fragment in fragments:
                    href = "../../" + path + "#" + fragment
                    with self.subTest(work=key, chapter=fragment):
                        self.assertIn(href, self.text)
                        changed = self.text.replace(href, "../../" + path)
                        self.assertNotEqual(changed, self.text)
                        self.assertIn("primary-chapter:" + key + ":" + fragment, self.errors(changed, self.cross))

    def test_historical_positive_route_keeps_its_explicit_later_qualification(self):
        self.assertEqual(self.errors(self.text, self.cross), [])
        key = "ground-of-intelligibility"
        fragment = "later-v11-authority-qualification"
        href = "../../" + self.cross["sources"]["ground"]["path"] + "#" + fragment
        changed = self.text.replace(href, "../../" + self.cross["sources"]["ground"]["path"] + "#42-the-chain-with-each-step-labeled")
        self.assertNotEqual(changed, self.text)
        self.assertIn("primary-chapter:" + key + ":" + fragment, self.errors(changed, self.cross))

    def test_primary_curation_keeps_profile_owned_components_and_six_renderings(self):
        self.assertEqual(self.errors(self.text, self.cross), [])
        rendered = [w for w in self.cross["works"] if w.get("artifact_id") in self.artifacts]
        self.assertEqual(len(rendered), 6)
        for work in rendered:
            self.assertEqual({self.cross["sources"][k]["path"] for k in work["source_keys"]},
                             self.artifacts[work["artifact_id"]])
        self.assertEqual(next(w for w in rendered if w["artifact_id"] == "notation-gallery")["role"], "supporting-reference")

    def test_primary_argument_maps_are_support_not_new_papers(self):
        self.assertEqual(self.errors(self.text, self.cross), [])
        required = {
            "ground-of-intelligibility": "companion/ARGUMENT-MAP-ORTHABILITY.md",
            "dynamic-orthability": "companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml",
        }
        for key, path in required.items():
            work = next(w for w in self.cross["works"] if w["key"] == key)
            support = {self.cross["sources"][k]["path"] for k in work.get("supporting_source_keys", [])}
            self.assertIn(path, support)
            for other in self.cross["works"]:
                self.assertNotIn(path, {self.cross["sources"][k]["path"] for k in other["source_keys"]})

    def test_work_omission_cannot_be_hidden_by_leaving_pdf_links(self):
        self.assertEqual(self.errors(self.text, self.cross), [])
        for key in self.required:
            altered = deepcopy(self.cross)
            altered["works"] = [w for w in altered["works"] if w["key"] != key]
            self.assertIn("primary-work:" + key, self.errors(self.text, altered))



class InformationRevisionCurationTests(unittest.TestCase):
    """Source-located TeX statements, without inventing exact PDF provenance."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("information_revision_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        folder = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.cross = json.loads((folder / "CROSSWALK.json").read_text())
        cls.base = json.loads((folder / "OWNER-MAP.json").read_text())["baseline"]["commit"]
        cls.catalogue = "docs/reader/PAPER-CATALOGUE.md"
        cls.text = (ROOT / cls.catalogue).read_text()
        # Line ranges derive from the protected baseline, not the reader output.
        cls.blocks = {
            "information-composition": ("information", (
                (r"\begin{theorem}[Relational strengthening]", r"\paragraph{The information criterion.}"),
                (r"\begin{proposition}[Output determination on the feasible support]", None),
                (r"\begin{theorem}[Sure finite decision]", None))),
            "reflexive-revision": ("reflexive", (
                (r"\section{Minimum evidence cost}", None),
                (r"\section{Evidence reuse and reflexive revision}", None),
                (r"\section{Behavioural parity leaves delivery undecided}", None))),
        }
        cls.expected = {}
        for key, (source, blocks) in cls.blocks.items():
            path = cls.cross["sources"][source]["path"]
            body = subprocess.check_output(["git", "show", cls.base + ":" + path], cwd=ROOT).decode()
            lines = body.splitlines()
            urls = []
            for marker, _ in blocks:
                starts = [i + 1 for i, line in enumerate(lines) if line.startswith(marker)]
                if len(starts) != 1:
                    raise AssertionError("Original TeX statement marker not unique: " + marker)
                first = starts[0]
                urls.append("https://github.com/theislampill/orthemology/blob/" + cls.base + "/" + path + "#L" + str(first))
            cls.expected[key] = set(urls)

    def links(self, text, entry):
        if not entry.startswith(self.catalogue + "#"):
            return set()
        page = self.mod.markdown_index(text)
        chosen = [h for h in page["headings"] if h[0] == entry.partition("#")[2]]
        if len(chosen) != 1:
            return set()
        _, level, start = chosen[0]
        end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
        return {href for line, href in page["links"] if start <= line < end}

    def errors(self, text, cross):
        errors = []
        for key, urls in self.expected.items():
            works = [w for w in cross["works"] if w["key"] == key]
            if len(works) != 1:
                errors.append("work:" + key)
                continue
            actual = self.links(text, works[0].get("catalogue_entry", ""))
            errors.extend("statement:" + url for url in sorted(urls - actual))
        return errors

    def test_existing_manuscripts_reach_their_original_statements(self):
        self.assertEqual(self.errors(self.text, self.cross), [])

    def test_generic_or_wrong_tex_line_does_not_replace_the_statement(self):
        self.assertEqual(self.errors(self.text, self.cross), [])
        for urls in self.expected.values():
            for href in urls:
                for replacement in (href.partition("#")[0], href.partition("#")[0] + "#L1"):
                    with self.subTest(target=href, replacement=replacement):
                        changed = self.text.replace(href, replacement)
                        self.assertNotEqual(changed, self.text)
                        self.assertIn("statement:" + href, self.errors(changed, self.cross))

    def test_preserved_pdf_and_related_tex_keep_distinct_work_roles(self):
        self.assertEqual(self.errors(self.text, self.cross), [])
        for key in self.expected:
            altered = deepcopy(self.cross)
            altered["works"] = [w for w in altered["works"] if w["key"] != key]
            self.assertIn("work:" + key, self.errors(self.text, altered))
        works = {w["key"]: w for w in self.cross["works"]}
        self.assertEqual(works["decisive-revision"]["source_keys"], ["decisive-pdf"])
        self.assertEqual(works["decisive-revision"]["role"], "preserved-edition")
        self.assertEqual(works["reflexive-revision"]["source_keys"], ["reflexive"])
        relations = [r for r in self.cross["relations"] if r.get("from") == "reflexive" and r.get("to") == "decisive-pdf"]
        self.assertTrue(relations)
        self.assertTrue(all(r["kind"] == "related-source" and r["basis"] == "lineage" for r in relations))



class CollectionDispositionTests(unittest.TestCase):
    """All paths in a completed collection need roles, not one paper per path."""
    def setUp(self):
        spec = importlib.util.spec_from_file_location("collection_dispositions_under_test", MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.directory = ROOT / "docs/project-closure/reader-refactor-issue-35"
        self.owners = json.loads((self.directory / "OWNER-MAP.json").read_text())
        self.cross = json.loads((self.directory / "CROSSWALK.json").read_text())
        self.rows = self.mod.entries_at(ROOT, self.owners["baseline"]["commit"])

    def validate(self, cross):
        checker = getattr(self.mod, "check_collection_dispositions", None)
        self.assertTrue(callable(checker), "Whole-collection disposition contract is not implemented")
        return checker(self.rows, self.owners, cross)

    def test_original_consolidation_has_all_paths_and_distinct_work_roles(self):
        self.assertIn("v5-consolidation", self.cross.get("collection_dispositions", {}),
                      "The original consolidation has no substantive work/support disposition")
        self.assertEqual(self.validate(self.cross), [])
        group = self.cross["collection_dispositions"]["v5-consolidation"]
        expected = {r["path"] for r in self.rows
                    if r["path"].startswith(("experiments/orthemology-v5/", "docs/provenance/v5-consolidation/"))}
        self.assertEqual({d["path"] for d in group["items"]}, expected)
        self.assertLess(len({d["work"] for d in group["items"]}), len(expected))

    def test_required_collection_cannot_disappear(self):
        altered = deepcopy(self.cross)
        altered.setdefault("collection_dispositions", {}).pop("v5-consolidation", None)
        errors = self.validate(altered)
        self.assertTrue(any(e.startswith("collection-missing:") for e in errors), errors)

    def test_omitted_component_cannot_hide_behind_remaining_valid_links(self):
        self.assertIn("v5-consolidation", self.cross.get("collection_dispositions", {}))
        altered = deepcopy(self.cross)
        before = len(altered["collection_dispositions"]["v5-consolidation"]["items"])
        altered["collection_dispositions"]["v5-consolidation"]["items"].pop()
        self.assertEqual(len(altered["collection_dispositions"]["v5-consolidation"]["items"]), before - 1)
        self.assertTrue(any(e.startswith("collection-coverage:") for e in self.validate(altered)))

    def test_disposition_cannot_point_to_an_absent_work(self):
        self.assertIn("v5-consolidation", self.cross.get("collection_dispositions", {}))
        altered = deepcopy(self.cross)
        altered["collection_dispositions"]["v5-consolidation"]["items"][0]["work"] = "absent-fixture-work"
        self.assertTrue(any(e.startswith("collection-work:") for e in self.validate(altered)))

    def test_duplicate_component_and_unexplained_role_are_rejected(self):
        self.assertIn("v5-consolidation", self.cross.get("collection_dispositions", {}))
        altered = deepcopy(self.cross)
        items = altered["collection_dispositions"]["v5-consolidation"]["items"]
        items.append(deepcopy(items[0])); items[0]["role"] = "miscellaneous"
        errors = self.validate(altered)
        self.assertTrue(any(e.startswith("collection-duplicate:") for e in errors), errors)
        self.assertTrue(any(e.startswith("collection-role:") for e in errors), errors)

    def test_convergence_extensions_use_the_existing_proof_owners(self):
        owner = json.loads((ROOT / "experiments/orthemology-v5/THEOREM_CATALOGUE.json").read_text())
        for family in owner["convergence_families"]:
            path = "experiments/orthemology-v5/" + family["proof"]
            source_keys = {k for k,v in self.cross["sources"].items() if v["path"] == path}
            works = [w for w in self.cross["works"] if source_keys.intersection(w["source_keys"])]
            self.assertEqual(len(works), 1, family["id"] + " must reach its original proof as one work")
            entry = works[0].get("catalogue_entry", "")
            self.assertTrue(entry.startswith("docs/reader/PAPER-CATALOGUE.md#"))
            self.assertIn(family["id"], (ROOT / "docs/reader/RESULT-INDEX.md").read_text())


class ContinuationGeometryRoutesTests(unittest.TestCase):
    """Source-owned note population, not a keyword test of philosophical truth."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("continuation_geometry_routes", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.directory = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.cross = json.loads((cls.directory / "CROSSWALK.json").read_text())
        owners = json.loads((cls.directory / "OWNER-MAP.json").read_text())
        raw = subprocess.check_output(["git", "show", owners["baseline"]["commit"] +
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"], cwd=ROOT)
        source_rows = json.loads(raw)["sources"]
        members = (
            "source-bridges/ANCHORED_FAMILY_COMMON_REPAIR.md",
            "source-bridges/DEPENDENCY_BLOCK_SMOOTH_CLASSIFICATION.md",
            "source-bridges/LOCAL_REPAIR_RIGIDITY.md",
            "source-bridges/LOCAL_SMOOTH_APPROXIMATE_IFF.md",
            "source-bridges/SMOOTH_SCORE_RIGIDITY.md",
            "source-bridges/CONTEXT_IDENTITY_CONTROL.md",
            "source-bridges/NUDGE_COMPARISON.md",
            "source-bridges/SOURCE_BRIDGE_SYNTHESIS.md",
            "root-research/DEPENDENCY_BLOCK_NORM_RIGIDITY.md",
            "root-research/REPRESENTATION_TRANSPORT_BOUNDARY.md",
            "root-research/FIRST_ORDER_REPAIR_REGRET.md",
            "root-research/STATISTICAL_REPAIR_BRIDGE.md",
            "root-research/COMMON_OBSERVATION_BOUNDARY.md",
            "root-research/CONTINUUM_RESTORATION_OBSTRUCTION.md",
            "root-research/INTEGRATED_BINARY_EXPERIMENT.md",
            "necessity-bridge-review/sources/CONTROLLED_INFORMATION_RESTORATION.md",
        )
        cls.expected = {}
        for member in members:
            paths = {v["path"] for v in source_rows
                     if v["origin"].startswith("d6f6fa5be51464c0") and v["member"] == member and v["path"]}
            if len(paths) != 1:
                raise AssertionError("Independent source owner not unique: " + member)
            cls.expected[member] = paths.pop()
        cls.text = (ROOT / "docs/reader/PAPER-CATALOGUE.md").read_text()

    def errors(self, cross, text):
        errors = []
        page = self.mod.markdown_index(text)
        for member, path in self.expected.items():
            keys = {k for k,v in cross["sources"].items() if v["path"] == path}
            works = [w for w in cross["works"] if keys.intersection(w["source_keys"])]
            if len(works) != 1:
                errors.append("work:" + member)
                continue
            entry = works[0].get("catalogue_entry", "")
            heading = [h for h in page["headings"] if h[0] == entry.partition("#")[2]]
            if not entry.startswith("docs/reader/PAPER-CATALOGUE.md#") or len(heading) != 1:
                errors.append("entry:" + member)
                continue
            _, level, start = heading[0]
            end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level),page["line_count"])
            targets = {href.split("#", 1)[0] for line,href in page["links"] if start <= line < end}
            if "../../" + path not in targets:
                errors.append("source:" + member)
        return errors

    def test_source_owned_geometry_and_restoration_notes_have_distinct_reading_routes(self):
        self.assertEqual(self.errors(self.cross, self.text), [])

    def test_missing_note_is_not_hidden_by_the_parent_collection_link(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for member,path in self.expected.items():
            altered = deepcopy(self.cross)
            keys = {k for k,v in altered["sources"].items() if v["path"] == path}
            altered["works"] = [w for w in altered["works"] if not keys.intersection(w["source_keys"])]
            self.assertIn("work:" + member,self.errors(altered,self.text))

    def test_another_existing_note_is_not_an_equivalent_source_route(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for member,path in self.expected.items():
            replacement = next(v for v in self.expected.values() if v != path)
            changed = self.text.replace("../../"+path, "../../"+replacement)
            self.assertNotEqual(changed,self.text)
            self.assertIn("source:" + member,self.errors(self.cross,changed))


class ContinuationAuditCostRoutesTests(ContinuationGeometryRoutesTests):
    """Reuse actual-route controls for the next independently named source family."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owners = json.loads((cls.directory / "OWNER-MAP.json").read_text())
        raw = subprocess.check_output(["git", "show", owners["baseline"]["commit"] +
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"], cwd=ROOT)
        source_rows = json.loads(raw)["sources"]
        required = [('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/geometry-delta-audit/author-freeze/SECOND_ORDER_REPAIR_LP.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/geometry-delta-audit/author-freeze/CRITICAL_SECOND_ORDER_CONTROL.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/geometry-delta-audit/author-freeze/MIXED_RANK_COUNTEREXAMPLE.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/root-research/FULL_JET_REPAIR_BOUNDARY.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/challenge/RANK_ONE_SOURCE_AND_PROOF_REVIEW.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/root-research/README.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/challenge/AUDIT_CONFIDENCE_PROOF.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/root-research/CONTINUUM_REPAIR_AND_ERROR_COST.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/root-research/EXPECTED_SCORE_VERSUS_REPORT_CORRECTNESS.md'), ('db6ccdc793a0a1a96b736cee6c55c47145b86b8f5f91d2dbb1cf80e7036b614e', 'tranche3/root-research/FINITE_ISSUANCE_BOUNDARY.md'), ('d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91', 'research/continuum/freeze-fresh-continuum-v1/FRESH_CONTINUUM_PROOF.md'), ('d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91', 'research/beta-budget/BETA_PRIOR_BUDGET_BOUNDARY.md'), ('d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91', 'research/beta-rates/FINITE_HORIZON_BETA_RATES.md'), ('d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91', 'research/beta-rates/DETERMINISTIC_REPORT_CLOCK_COROLLARY.md'), ('d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91', 'research/endpoint-density-rates/ENDPOINT_DENSITY_ROBUSTNESS.md')]
        cls.expected = {}
        for origin, member in required:
            paths = {v["path"] for v in source_rows
                     if v["origin"] == origin and v["member"] == member and v["path"]}
            if len(paths) != 1:
                raise AssertionError("Independent source owner not unique: " + member)
            cls.expected[member] = paths.pop()


class ContinuationControllerRoutesTests(ContinuationGeometryRoutesTests):
    """The original source map supplies controller/work identity, not page names."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owners = json.loads((cls.directory / "OWNER-MAP.json").read_text())
        rows = json.loads(subprocess.check_output(["git", "show", owners["baseline"]["commit"] +
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"], cwd=ROOT))["sources"]
        cls.expected = {}
        for origin,member in [('d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91', 'research/independent-review/markov-support/source/SUPPORT_CHANGING_MARKOV_THEOREM.md'), ('769dc45d15ba6d2ee4cdce41bd719b415591dc1667ab6e6bc834fa53477dc3b0', 'candidate-v1/THEOREM_CONTRACT.md'), ('f9b7614a84f0d21492f63f281165e7fa9bb1bcb4630218c70a9bf01024f7ff73', 'REPORT.md'), ('c86174f55f8474787ce124b2d1f8601e8b13ef0667242d6109ddaaaa8f0578b3', 'author-snapshot/PD_EXPTIME_HARDNESS_CANDIDATE.md'), ('4bd668ffbcfaa1a3f79dfc41d7078bc5a799d9c74b2063da04f21eeffbfe2904', 'THEOREM_AND_PROOF.md'), ('70677d135cd8957f5b527d555001eb8e53b0cc19652297709eb110e94f2a39be', 'prior-art/controller-comparison/CONTROLLER_PRIOR_ART_SYNTHESIS.md'), ('b5be7775f6d0b1d5628f8d100f4d0db3c3d44827472e3965c7bbd4cb04423b34', 'EXACT_RUNTIME_CONTRACT.md'), ('b5be7775f6d0b1d5628f8d100f4d0db3c3d44827472e3965c7bbd4cb04423b34', 'EXACT_RATIONAL_CONTRACT.md'), ('b5be7775f6d0b1d5628f8d100f4d0db3c3d44827472e3965c7bbd4cb04423b34', 'PHASE_SOURCE_CONTRACT.md')]:
            paths = {v["path"] for v in rows if v["origin"] == origin and v["member"] == member and v["path"]}
            if len(paths) != 1:
                raise AssertionError("Pinned controller source owner is not unique: " + member)
            cls.expected[origin[:12] + ":" + member] = paths.pop()

    def test_later_formal_cost_and_source_composition_are_attached_not_lost(self):
        expected = {
            "continuation-generated-cost": ("S6F-19", "S6F-20", "S6F-21"),
            "continuation-full-phase-runtime": ("S6F-22",),
            "continuation-rational-law": ("S6F-23",),
        }
        works = {w["key"]: w for w in self.cross["works"]}
        text = (ROOT / "docs/reader/RESULT-INDEX.md").read_text()
        for key, result_ids in expected.items():
            self.assertIn(key, works)
            self.assertTrue(works[key].get("supporting_source_keys"))
            for result in result_ids:
                self.assertIn(result, text)
        self.assertEqual(len(works), len(self.cross["works"]))

    def test_controller_runtime_reading_route_retains_environment_and_law_owners(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        works = {w["key"]:w for w in self.cross["works"]}
        work = works["continuation-full-phase-runtime"]
        all_keys = work["source_keys"] + work.get("supporting_source_keys", [])
        paths = {self.cross["sources"][k]["path"] for k in all_keys}
        owner = json.loads((self.directory / "OWNER-MAP.json").read_text())
        rows = json.loads(subprocess.check_output(["git","show",owner["baseline"]["commit"]+
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"],cwd=ROOT))["sources"]
        actual_module = {v["path"] for v in rows if v["member"].endswith("/FullControllerCanonicalLaw.lean") and v.get("path")}
        self.assertEqual(len(actual_module), 1)
        self.assertTrue(actual_module <= paths)


class ContinuationPriorRoutesTests(ContinuationGeometryRoutesTests):
    """Read paths are derived from retained source owners, not file-extension counts."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owners = json.loads((cls.directory / "OWNER-MAP.json").read_text())
        rows = json.loads(subprocess.check_output(["git", "show", owners["baseline"]["commit"] +
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"], cwd=ROOT))["sources"]
        cls.expected = {}
        for origin, member in [('323c03dcfc21b1cf6be7b0854926c52f7f2adf72049ee6e0aa076ae825e73318', 'README.md'), ('60d1cd83d5d27d1160402a1478d2ea20024101805d06a442cc757e7e798199a8', 'README.md'), ('a5ea2c5119482abdb1c0b0f59c24a573782707f3d9cae2662ef7af879f39693c', 'README.md'), ('ddbad6ca12d0392615684aca98fa45ebdeb32c0cde4c18cf052aa465e756e473', 'README.md'), ('c95f5175af02c4ac6405cd75200bf5298f7bd4f4b33e17183e61c6c9c9d227f5', 'README.md'), ('10954d525a8c5eb433805ecb86df0435ca8b2871514c0df749aaac1c61612e1e', 'REPORT.md'), ('e41706b14ab77d8c6e00a333ccb18f0d4d841bd36224b5134ec962b8ace7c2c5', 'inputs/CLUSTER_SMOOTHING_THEOREM.md'), ('e41706b14ab77d8c6e00a333ccb18f0d4d841bd36224b5134ec962b8ace7c2c5', 'inputs/WIDTH_BOUNDARY_FINAL.md'), ('e41706b14ab77d8c6e00a333ccb18f0d4d841bd36224b5134ec962b8ace7c2c5', 'inputs/CRITICAL_UNIFORM_THEOREM_FINAL.md'), ('e41706b14ab77d8c6e00a333ccb18f0d4d841bd36224b5134ec962b8ace7c2c5', 'inputs/CONTAMINATION_CROSSOVER.md'), ('e41706b14ab77d8c6e00a333ccb18f0d4d841bd36224b5134ec962b8ace7c2c5', 'inputs/NON_ENDPOINT_CONTAMINATION_FINAL.md'), ('15e2b6abb662c4df77254634da03cea567ec6e896d90c3fb9426d93a872a3feb', 'NONCONVEXITY_THEOREM.md'), ('c9f8099a9d4768f8d37c3d5a94b9828c63939635765c876f8a31bb3e57534e1c', 'ALMOST_SURE_ADDENDUM.md'), ('a64783ac9ab414e894d715a865828dce1695bb3b8842bcb10df46c799085ec8e', 'candidate/EFFECTIVE_WITNESS_THEOREM.md'), ('7871eae3c71aec59d246b81f6dccc67d1c6bedb40f6b8e8a460f1e998fff7815', 'PREDICTION_LOSS_COMPARISON.md')]:
            paths = {v["path"] for v in rows if v["origin"] == origin and v["member"] == member and v.get("path")}
            if len(paths) != 1:
                raise AssertionError("Prior source is not uniquely owned: " + member)
            cls.expected[origin[:12] + ":" + member] = paths.pop()

    def test_rational_runtime_and_loss_obstruction_keep_distinct_source_components(self):
        works = {w["key"]:w for w in self.cross["works"]}
        for key, suffix, role in (
            ("continuation-rational-prior", "/rational-v3/reference.py", "research-software"),
            ("continuation-observed-loss", "/1d294f8542feba53501eedeae981a65d1aabc9f6fa185cf429775607d42ff8f0.lean", "research-note"),
        ):
            self.assertIn(key, works)
            work = works[key]
            self.assertEqual(work["role"], role)
            paths = {self.cross["sources"][k]["path"] for k in
                     work["source_keys"] + work.get("supporting_source_keys", [])}
            self.assertTrue(any(path.endswith(suffix) for path in paths), paths)
        self.assertEqual(works["continuation-two-coin-review"]["role"], "review")
        self.assertEqual(len(works), len(self.cross["works"]))



class ContinuationFoundationalRoutesTests(ContinuationGeometryRoutesTests):
    """Positive source arguments and exact selection contracts keep their owners."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owner = json.loads((cls.directory / "OWNER-MAP.json").read_text())
        rows = json.loads(subprocess.check_output(["git", "show", owner["baseline"]["commit"] +
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"], cwd=ROOT))["sources"]
        required = (
            ("83f1a917b40a", "POSITIVE_GROUND_AND_KNOWLEDGE.md"),
            ("83f1a917b40a", "COMPLETE_SELF_KNOWLEDGE_AND_EFFECTS.md"),
            ("83f1a917b40a", "EXACT_MODAL_RESULT.md"),
            ("eff5fada59f4", "UPSTREAM_SOURCE_ARGUMENT.md"),
            ("0a74eb642cc6", "ARITHMETIC_CERTIFICATE.md"),
            ("549ba6a7f094", "projections/zero-error-formal/ACTION_SUFFICIENT_DISCLOSURE.md"),
        )
        cls.expected = {}
        for prefix, member in required:
            paths = {r["path"] for r in rows if r["origin"].startswith(prefix)
                     and r["member"] == member and r.get("path")}
            if len(paths) != 1:
                raise AssertionError("Unresolved original source: " + member)
            cls.expected[prefix + ":" + member] = paths.pop()

    def test_complete_act_argument_retains_noninferential_clarification(self):
        works = {w["key"]: w for w in self.cross["works"]}
        self.assertIn("continuation-creative-knowledge", works)
        w = works["continuation-creative-knowledge"]
        sources = self.cross["sources"]
        support = [sources[k]["path"] for k in w.get("supporting_source_keys", [])]
        self.assertTrue(any(p.endswith("bc92ae5f37ea73f1196696314646006b5fdfb693c0293c1c92c6d16ec8845308.md") for p in support), support)
        self.assertTrue(any(p.endswith("c6378e90f5347069abaaa3e7d165a6029d6643cd1b551bdd31678906adea9cb1.lean") for p in support))
        self.assertEqual(len(works), len(self.cross["works"]))

    def test_arithmetic_evaluator_keeps_its_implementation_and_type_correction(self):
        works = {w["key"]: w for w in self.cross["works"]}
        self.assertIn("continuation-exact-confidence-budget", works)
        w = works["continuation-exact-confidence-budget"]
        self.assertEqual(w["role"], "research-software")
        paths = {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}
        self.assertIn("experiments/orthemology-v5-continuations/reference/integer-v3/src/exact_budget.py", paths)
        self.assertTrue(any(p.endswith("df3c0d9f67602b25449bde809132bf3d18e93cefdcded8336d9e0727e1edfee4.md") for p in paths))
        # It is one software work, not a paper for each input, test or receipt.
        own = [x for x in self.cross["works"] if any(self.cross["sources"][k]["path"].endswith("/integer-v3/src/exact_budget.py") for k in x["source_keys"])]
        self.assertEqual(len(own), 1)



class ContinuationNormAndAttributeRoutesTests(ContinuationGeometryRoutesTests):
    """Preserve the source-owned positive arguments and their distinct burdens."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owner = json.loads((cls.directory / "OWNER-MAP.json").read_text())
        rows = json.loads(subprocess.check_output(["git", "show", owner["baseline"]["commit"] +
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"], cwd=ROOT))["sources"]
        members = (
            "selected-source-union/tranche6/foundations/intrinsic-necessity/freeze-v2/INTRINSIC_NECESSITY_ARGUMENT.md",
            "selected-source-union/tranche6/foundations/world-bridge/freeze-v2/WORLD_BRIDGE_ARGUMENT.md",
            "selected-source-union/tranche6/foundations/world-bridge/freeze-v1/ACT_ONTOLOGY_AND_COMPLETENESS.md",
            "selected-source-union/tranche6/foundations/world-bridge/freeze-v2/EXTERNAL_TERMINUS_AND_ORIGIN_CLOSURE.md",
            "selected-source-union/tranche6/foundations/norm-fixing/freeze-v2/ARGUMENT.md",
            "projections/attributes-delivery/ATTRIBUTE_ASCENT.md",
            "projections/motivation-value-v2/MOTIVATION_VALUE_AND_MALICIOUS_SOURCE.md",
        )
        cls.expected = {}
        cls.original_paths = {}
        for member in members:
            paths = {r["path"] for r in rows if r["origin"].startswith("549ba6a7f094")
                     and r["member"] == member and r.get("path")}
            if len(paths) != 1:
                raise AssertionError("Ambiguous or absent source owner: " + member)
            cls.expected[member] = paths.pop()
        for r in rows:
            if r["origin"].startswith("549ba6a7f094") and r.get("path"):
                cls.original_paths[r["member"]] = r["path"]

    def test_world_bridge_keeps_its_act_and_external_termination_components(self):
        works = {w["key"]: w for w in self.cross["works"]}
        self.assertIn("continuation-world-bridge", works)
        w = works["continuation-world-bridge"]
        paths = {self.cross["sources"][k]["path"] for k in w["source_keys"]}
        expected = {path for member, path in self.expected.items() if "/world-bridge/" in member}
        self.assertEqual(paths, expected)
        support = {self.cross["sources"][k]["path"] for k in w.get("supporting_source_keys", [])}
        self.assertIn(self.original_paths["selected-source-union/tranche6/foundations/world-bridge/freeze-v1/PREMISE_AND_RIVAL_MAP.md"], support)
        # Constituents stay discoverable without manufacturing duplicate work credit.
        for path in expected:
            containing = [x for x in self.cross["works"] if path in {self.cross["sources"][k]["path"] for k in x["source_keys"]}]
            self.assertEqual(len(containing), 1)

    def test_norm_and_attribute_maps_remain_support_not_separate_verdicts(self):
        works = {w["key"]: w for w in self.cross["works"]}
        for key, members in (
            ("continuation-objective-norms", ("selected-source-union/tranche6/foundations/norm-fixing/freeze-v2/ADVERSARIAL_BRIDGES.md", "selected-source-union/tranche6/foundations/norm-fixing/freeze-v2/SEMANTIC_WARRANT_TESTS.md")),
            ("continuation-attribute-wisdom", ("projections/attributes-delivery/DEPENDENCIES_AND_DISCRIMINATION.md",)),
        ):
            self.assertIn(key, works)
            support = {self.cross["sources"][k]["path"] for k in works[key].get("supporting_source_keys", [])}
            for member in members:
                path = self.original_paths[member]
                self.assertIn(path, support)
                self.assertFalse(any(path in {self.cross["sources"][k]["path"] for k in x["source_keys"]} for x in self.cross["works"]))



class ContinuationDisclosureRoutesTests(ContinuationGeometryRoutesTests):
    """The source-owned lineage keeps changes of game and evidence visible."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        owner = json.loads((cls.directory / "OWNER-MAP.json").read_text())
        rows = json.loads(subprocess.check_output(["git", "show", owner["baseline"]["commit"] +
            ":docs/provenance/v5-research-continuations/SOURCE_MAP.json"], cwd=ROOT))["sources"]
        members = (
            "projections/restoration-v1/ARGUMENT.md",
            "projections/positive-error-v2/POSITIVE_ERROR_FRONTIERS.md",
            "projections/two-message-v2/TWO_MESSAGE_THEOREM.md",
            "projections/odd-three-v1/ODD_THREE_MESSAGE_THEOREM.md",
            "addenda/b4-m3-bounded-evidence-v1/author/B4_M3_EXACT_FRONTIER.md",
            "pending/projections/full-private-frontier-pending/GENERAL_FIXED_FRONTIER.md",
            "projections/timing-review/timing-v1/TIMING_RESOURCE_BOUNDARIES.md",
        )
        cls.original_paths = {r["member"]:r["path"] for r in rows
            if r["origin"].startswith("549ba6a7f094") and r.get("path")}
        cls.expected = {m:cls.original_paths[m] for m in members}

    def test_three_message_extension_retains_the_ordinary_and_certified_parts(self):
        works = {w["key"]:w for w in self.cross["works"]}
        self.assertIn("continuation-three-message", works)
        w = works["continuation-three-message"]
        paths = {self.cross["sources"][k]["path"] for k in w["source_keys"]}
        self.assertEqual(paths, {self.original_paths[m] for m in (
            "projections/odd-three-v1/ODD_THREE_MESSAGE_THEOREM.md",
            "addenda/b4-m3-bounded-evidence-v1/author/B4_M3_EXACT_FRONTIER.md")})
        support = {self.cross["sources"][k]["path"] for k in w.get("supporting_source_keys", [])}
        self.assertIn(self.original_paths["addenda/b4-m3-bounded-evidence-v1/review/INDEPENDENT_REVIEW.md"], support)
        certs = {p for m,p in self.original_paths.items() if m.startswith(
            "addenda/b4-m3-bounded-evidence-v1/author/") and m.endswith(".json")}
        self.assertGreaterEqual(len(certs), 3)
        self.assertTrue(certs <= support)
        for path in certs:
            self.assertFalse(any(path in {self.cross["sources"][k]["path"] for k in x["source_keys"]}
                                 for x in self.cross["works"]))

    def test_general_classification_keeps_its_range_clarification_and_actual_reviews(self):
        works = {w["key"]:w for w in self.cross["works"]}
        self.assertIn("continuation-complete-fixed-codebook", works)
        w = works["continuation-complete-fixed-codebook"]
        support = {self.cross["sources"][k]["path"] for k in w.get("supporting_source_keys", [])}
        for member in (
            "addenda/full-frontier-acceptance-v1/GENERAL_SCOPE_CLARIFICATION_V1.md",
            "addenda/full-frontier-acceptance-v1/reviews/broad-review/INDEPENDENT_REVIEW.md",
            "addenda/full-frontier-acceptance-v1/reviews/arithmetic-review/GENERAL_PRIVATE_ARITHMETIC_REVIEW_V1.md",
        ):
            self.assertIn(self.original_paths[member], support)
        # An old pending path and a new acceptance record are different evidence roles.
        self.assertEqual(len(w["source_keys"]), 1)
        self.assertNotEqual(w["review_status"], "INDEPENDENT_REFACTOR_ACCEPTANCE")

    def test_timing_route_uses_the_mathematical_note_not_the_clock_erratum(self):
        works = {w["key"]:w for w in self.cross["works"]}
        self.assertIn("continuation-timing-resources", works)
        w = works["continuation-timing-resources"]
        actual = {self.cross["sources"][k]["path"] for k in w["source_keys"]}
        self.assertEqual(actual, {self.original_paths["projections/timing-review/timing-v1/TIMING_RESOURCE_BOUNDARIES.md"]})
        self.assertNotIn(self.original_paths["projections/frontier-review-continuation/author-addenda/ROOT_TIMING_ERRATUM.md"], actual)
        support = {self.cross["sources"][k]["path"] for k in w.get("supporting_source_keys", [])}
        self.assertIn(self.original_paths["projections/timing-review/TIMING_RESOURCE_REVIEW_V1.md"], support)

if __name__ == "__main__":
    unittest.main()
