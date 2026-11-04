#!/usr/bin/env python3
"""Mechanical reader-pilot controls; not a classifier of philosophical truth.

Fixture-only scientific and profile paths use explicit fixture roots. They are
created in temporary repositories, not citations to missing project documents.
The real reader and generated-publication paths still exercise their actual
production contracts; the repository reference gate is unchanged.
"""
from copy import deepcopy
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import posixpath
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "check_reader_pilot.py"
sys.path.insert(0, str(MODULE.parent))


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


    def test_wrong_staged_source_cannot_hide_under_its_original_worktree_copy(self):
        path = self.repo / 'fixture-theory/core.md'
        original = path.read_bytes()
        path.write_bytes(original + b'\nwrong staged edition\n')
        self.git('add', '--', 'fixture-theory/core.md')
        path.write_bytes(original)
        self.assertEqual(self.git('diff', '--name-only', self.base, '--', 'fixture-theory/core.md'), '')
        self.reject(self.check(), 'corpus-currentness')

    def test_staged_new_source_cannot_hide_by_removing_its_worktree_copy(self):
        path = self.repo / 'fixture-theory/new-index-only.md'
        path.write_bytes(b'new source without an owner\n')
        self.git('add', '--', 'fixture-theory/new-index-only.md')
        path.unlink()
        self.assertEqual(self.git('diff', '--name-only', self.base, '--', 'fixture-theory/new-index-only.md'), '')
        self.reject(self.check(), 'corpus-currentness')

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

    def test_scholarly_display_maintenance_keeps_a_finite_source_boundary(self):
        for directory, name in (("scripts", "validate_math_source.py"),
                                ("tests", "test_math_source_validator.py"),
                                ("tests", "test_v5_twentieth_data.py"),
                                ("docs/project-closure/r7e-sol", "R7E-SOL-ADVERSARIAL-REPORT.md")):
            path = self.repo / directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Synthetic maintenance owner, not a scientific source.\n")
            self.git("add", "--", str(path.relative_to(self.repo)))
        self.assertEqual(self.check(), [])
        unexpected = self.repo / "scripts" / "unregistered_research.py"
        unexpected.write_text("# Synthetic unadmitted research software.\n")
        self.git("add", "--", str(unexpected.relative_to(self.repo)))
        self.reject(self.check(), "corpus-currentness")
        self.git("reset", "--", str(unexpected.relative_to(self.repo)))
        unexpected.unlink()
        self.assertEqual(self.check(), [])
        neighboring = self.repo / "docs" / "project-closure" / "r7e-sol" / "UNREGISTERED-REPORT.md"
        neighboring.write_text("# Synthetic unadmitted neighboring report.\n")
        self.git("add", "--", str(neighboring.relative_to(self.repo)))
        self.reject(self.check(), "corpus-currentness")
        self.git("reset", "--", str(neighboring.relative_to(self.repo)))
        neighboring.unlink()
        self.assertEqual(self.check(), [])
        legacy_neighbor = self.repo / "tests" / "test_v5_twentieth_data_unregistered.py"
        legacy_neighbor.write_text("# Synthetic unadmitted neighboring test owner.\n")
        self.git("add", "--", str(legacy_neighbor.relative_to(self.repo)))
        self.reject(self.check(), "corpus-currentness")
        self.git("reset", "--", str(legacy_neighbor.relative_to(self.repo)))
        legacy_neighbor.unlink()
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

    def test_reader_candidate_requires_every_owner_group_disposition(self):
        altered = deepcopy(self.cross)
        altered["coverage_stage"] = "reader-candidate"
        altered["collection_dispositions"] = {}
        rows = self.mod.entries_at(self.repo, self.base)
        for group in self.owners["collections"]:
            altered["collection_dispositions"][group["key"]] = {
                "scope": "Synthetic collection disposition, not semantic acceptance.",
                "reading_record": "Fixture-only reading record.",
                "basis_sources": [group["owners"][0]],
                "items": [{"path": row["path"], "role": "reference-material", "work": "core"}
                          for row in rows if self.mod.matches(row["path"], group["include"])],
            }
        self.assertEqual(self.check(cross=altered), [])
        for group in self.owners["collections"]:
            with self.subTest(group=group["key"]):
                missing = deepcopy(altered)
                missing["collection_dispositions"].pop(group["key"])
                self.reject(self.check(cross=missing), "collection-missing")

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

    def ci_owner_fixture(self, *, hosted=False):
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
        if hosted:
            anchor = "      - name: Repository hygiene + honesty checks\n"
            before = before.replace(anchor,
                "      - name: Dependency lock consistency\n"
                "        run: python scripts/validate_dependency_lock.py\n" + anchor)
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

    def hosted_ci_owner_fixture(self):
        path, owners, before, candidate, reader_step = self.ci_owner_fixture(hosted=True)
        # Exercise the actual published workflow block, independently of any
        # checker constant. This input contains no source or proof execution.
        workflow = (ROOT / ".github/workflows/validate.yml").read_text()
        start = "      - name: Source-alias admission and evidence controls\n"
        anchor = "      - name: Dependency lock consistency\n"
        self.assertEqual(workflow.count(start), 1)
        self.assertEqual(workflow.count(anchor), 1)
        addition = workflow[workflow.index(start):workflow.index(anchor)]
        self.assertEqual(addition.count("      - name: "), 8)
        self.assertEqual([line for line in addition.splitlines() if line.startswith("      - name: ")], [
            "      - name: Source-alias admission and evidence controls",
            "      - name: Previously failed continuation receipt controls",
            "      - name: Combined public source-alias absence and exact restoration",
            "      - name: Receive bounded source-alias evidence",
            "      - name: Preserve bounded source-alias evidence",
            "      - name: Public123 generated-source absence and exact restoration",
            "      - name: Receive bounded public123 evidence",
            "      - name: Preserve bounded public123 evidence",
        ])
        candidate = candidate.replace(anchor, addition + anchor)
        path.write_text(candidate)
        return path, owners, before, candidate, addition

    def test_exact_hosted_absence_ci_addition_keeps_prior_reader_form(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        path.write_text(candidate.replace(addition, "", 1))
        self.assertEqual(self.check(owners=owners), [])
        path.write_text(candidate)
        self.assertEqual(self.check(owners=owners), [])

    def test_hosted_absence_ci_admission_rejects_weakened_controls(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        changes = (
            ("setsid --wait python", "setsid python"),
            ("scripts/check_source_alias_absence.py run\n",
             "scripts/check_source_alias_absence.py run || true\n"),
            ("if: github.event_name == 'pull_request'", "if: always()"),
            ("always() && github.event_name", "github.event_name"),
            ("include-hidden-files: false", "include-hidden-files: true"),
            ("if-no-files-found: error", "if-no-files-found: warn"),
            ("archive: true", "archive: false"),
            ("${{ runner.temp }}/r0002-source-alias-receipts/", "${{ github.workspace }}/"),
            ("actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9",
             "actions/upload-artifact@v7"),
            ("contents: read", "contents: write"),
            ("python scripts/validate_repo.py", "true"),
            ("python -B scripts/check_reader_pilot.py\n",
             "python -B scripts/check_reader_pilot.py || true\n"),
        )
        for old, new in changes:
            with self.subTest(control=old):
                self.assertIn(old, candidate)
                path.write_text(candidate.replace(old, new, 1))
                self.reject(self.check(owners=owners), "owner")

    def test_hosted_absence_ci_admission_rejects_missing_duplicate_or_reordered_steps(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        markers = (
            "      - name: Source-alias admission and evidence controls\n",
            "      - name: Previously failed continuation receipt controls\n",
            "      - name: Combined public source-alias absence and exact restoration\n",
            "      - name: Receive bounded source-alias evidence\n",
            "      - name: Preserve bounded source-alias evidence\n",
            "      - name: Public123 generated-source absence and exact restoration\n",
            "      - name: Receive bounded public123 evidence\n",
            "      - name: Preserve bounded public123 evidence\n",
        )
        offsets = [addition.index(marker) for marker in markers] + [len(addition)]
        steps = [addition[a:b] for a, b in zip(offsets, offsets[1:])]
        alterations = (
            addition + addition,
            "".join(steps[1:]),
            steps[2] + steps[1] + steps[0] + "".join(steps[3:]),
            steps[0] + steps[1] + steps[2] + steps[4] + steps[3] + "".join(steps[5:]),
            steps[1] + steps[0] + "".join(steps[2:]),
            steps[0] + steps[2] + steps[1] + "".join(steps[3:]),
        )
        # Removing the whole optional receipt step is the preceding accepted form,
        # exercised below. Every previously required step remains mandatory.
        alterations += tuple("".join(steps[:i] + steps[i + 1:]) for i in range(2, len(steps)))
        alterations += tuple("".join(steps[:i] + [steps[i + 1], steps[i]] + steps[i + 2:])
                             for i in range(3, len(steps) - 1))
        for changed in alterations:
            with self.subTest(block=changed):
                path.write_text(candidate.replace(addition, changed, 1))
                self.reject(self.check(owners=owners), "owner")

    def test_hosted_ci_exact_legacy_reader_absence_and_public123_forms(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        receipt_step = (
            '      - name: Previously failed continuation receipt controls\n'
            '        env:\n'
            '          PYTHONDONTWRITEBYTECODE: "1"\n'
            '        run: |\n'
            '          python -B tests/test_research_continuations.py ActualEvidenceAssociationTests.test_array_receipt_has_descriptive_validation_failure ActualEvidenceAssociationTests.test_qualified_original_controls_require_provenance\n'
            '          python -B -O tests/test_research_continuations.py ActualEvidenceAssociationTests.test_array_receipt_has_descriptive_validation_failure ActualEvidenceAssociationTests.test_qualified_original_controls_require_provenance\n'
        )
        self.assertEqual(addition.count(receipt_step), 1)
        with_resources = addition.replace(receipt_step, "", 1)
        plain = with_resources
        for family in ("boundary", "evidence"):
            qualifier = ('PUBLIC123_REVISION_RESOURCES="$(mktemp -d '
                         '"$RUNNER_TEMP/r0002-public123-' + family + '.XXXXXX")" ')
            self.assertEqual(plain.count(qualifier), 1)
            plain = plain.replace(qualifier, "", 1)
        public_start = "      - name: Public123 generated-source absence and exact restoration\n"
        legacy_absence = plain[:plain.index(public_start)]
        self.assertEqual(legacy_absence.count("      - name: "), 4)
        forms = (
            ("reader-only", ""),
            ("legacy-absence", legacy_absence),
            ("public123", plain),
            ("public123-resource-roots", with_resources),
            ("continuation-receipt-controls", addition),
        )
        for label, block in forms:
            with self.subTest(form=label):
                path.write_text(candidate.replace(addition, block, 1))
                self.assertEqual(self.check(owners=owners), [])

    def test_public123_ci_gate_and_export_changes_are_rejected(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        start = "      - name: Public123 generated-source absence and exact restoration\n"
        public = addition[addition.index(start):]
        changes = (
            ("id: public_fixture123", "id: another_consumer"),
            ("steps.source_alias_absence.outcome == 'success'",
             "steps.source_alias_absence.outcome != 'failure'"),
            ("github.event_name == 'pull_request'", "github.event_name == 'push'"),
            ("setsid --wait python", "setsid python"),
            (" run-fixtures --state ", " run --state "),
            (" export-fixtures --state ", " export --state "),
            ("always() && github.event_name", "github.event_name"),
            ("steps.public_fixture123.outcome != 'skipped'",
             "steps.public_fixture123.outcome != 'failure'"),
            ("$RUNNER_TEMP/r0002-public-fixtures123-absence", "$RUNNER_TEMP/another-state"),
            ("${{ runner.temp }}/r0002-public-fixtures123-receipts/", "${{ github.workspace }}/"),
            ("r0002-public-fixtures123-evidence-${{ github.run_id }}-${{ github.run_attempt }}",
             "unbound-public123-evidence"),
            ("actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9",
             "actions/upload-artifact@v7"),
            ("if-no-files-found: error", "if-no-files-found: warn"),
            ("include-hidden-files: false", "include-hidden-files: true"),
            ("archive: true", "archive: false"),
        )
        for old, new in changes:
            with self.subTest(public123_control=old):
                self.assertIn(old, public)
                path.write_text(candidate.replace(public, public.replace(old, new, 1), 1))
                self.reject(self.check(owners=owners), "owner")

    def test_public123_ci_resources_are_exact_and_paired(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        for family in ("boundary", "evidence"):
            qualifier = ('PUBLIC123_REVISION_RESOURCES="$(mktemp -d '
                         '"$RUNNER_TEMP/r0002-public123-' + family + '.XXXXXX")" ')
            self.assertEqual(candidate.count(qualifier), 1)
            alternatives = (
                "",
                qualifier.replace("PUBLIC123_REVISION_RESOURCES", "UNUSED_RESOURCE_ROOT"),
                qualifier.replace("mktemp -d", "mktemp -u"),
                qualifier.replace("$RUNNER_TEMP", "$GITHUB_WORKSPACE"),
                qualifier.replace("r0002-public123-" + family + ".XXXXXX", "shared-fixture-root"),
                'PUBLIC123_REVISION_RESOURCES="$RUNNER_TEMP/reused-resource-root" ',
            )
            for changed in alternatives:
                with self.subTest(resource=family, replacement=changed):
                    path.write_text(candidate.replace(qualifier, changed, 1))
                    self.reject(self.check(owners=owners), "owner")

    def test_public123_ci_requires_both_earlier_operational_blocks(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        public_start = "      - name: Public123 generated-source absence and exact restoration\n"
        split = addition.index(public_start)
        reader_start = "      - name: Reader pilot source, edition and navigation controls (not semantic acceptance)\n"
        reader_end = "      - name: T20 v6 independent public projection and source boundaries\n"
        reader = candidate[candidate.index(reader_start):candidate.index(reader_end)]
        forms = (
            candidate.replace(reader, "", 1),
            candidate.replace(addition, addition[split:], 1),
            candidate.replace(addition, addition[:split], 1),
        )
        for changed in forms:
            with self.subTest(incomplete_increment=changed):
                path.write_text(changed)
                self.reject(self.check(owners=owners), "owner")


    def test_hosted_absence_support_paths_have_a_finite_operational_boundary(self):
        scripts = (
            "check_source_alias_absence.py", "source_alias_absence_boundary.py",
            "source_alias_absence_context.py", "source_alias_absence_continuations.py",
            "source_alias_absence_evidence.py", "source_alias_absence_guard.py",
            "source_alias_absence_metadata.py", "source_alias_absence_population.py",
            "source_alias_absence_reader.py",
        )
        tests = ("test_source_alias_absence_boundary.py", "test_source_alias_absence_evidence.py",
                 "test_source_alias_absence_population.py")
        for directory, names in (("scripts", scripts), ("tests", tests)):
            for name in names:
                node = self.repo / directory / name
                node.parent.mkdir(parents=True, exist_ok=True)
                node.write_text("# Fixture engineering support, not a scholarly source.\n")
                self.git("add", "--", str(node.relative_to(self.repo)))
        self.assertEqual(self.check(), [])
        for directory in ("scripts", "tests"):
            # A similar filename is still an unadmitted fixture source.
            unexpected = self.repo / directory / "source_alias_absence_unreviewed.py"
            unexpected.write_text("# Fixture unreviewed research software.\n")
            self.git("add", "--", str(unexpected.relative_to(self.repo)))
            self.reject(self.check(), "corpus-currentness")
            self.git("reset", "--", str(unexpected.relative_to(self.repo)))
            unexpected.unlink()

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

    def test_continuation_receipt_ci_controls_are_exact(self):
        path, owners, before, candidate, addition = self.hosted_ci_owner_fixture()
        start = "      - name: Previously failed continuation receipt controls\n"
        end = "      - name: Combined public source-alias absence and exact restoration\n"
        receipt = addition[addition.index(start):addition.index(end)]
        commands = [line for line in receipt.splitlines(keepends=True)
                    if line.startswith("          python ")]
        self.assertEqual(len(commands), 2)
        self.assertTrue(commands[0].startswith("          python -B tests/"))
        self.assertTrue(commands[1].startswith("          python -B -O tests/"))
        changes = (
            (commands[0], ""),
            (commands[1], ""),
            (commands[0] + commands[1], commands[1] + commands[0]),
            (commands[0], commands[0] + commands[0]),
            ('PYTHONDONTWRITEBYTECODE: "1"', 'PYTHONDONTWRITEBYTECODE: "0"'),
            ("test_array_receipt_has_descriptive_validation_failure", "test_unreviewed_receipt"),
            ("test_qualified_original_controls_require_provenance", "test_unreviewed_original_controls"),
            ("        run: |\n", "        continue-on-error: true\n        run: |\n"),
        )
        for old, new in changes:
            with self.subTest(receipt_control=old):
                self.assertIn(old, receipt)
                changed = receipt.replace(old, new, 1)
                path.write_text(candidate.replace(receipt, changed, 1))
                self.reject(self.check(owners=owners), "owner")
        path.write_text(candidate.replace(receipt, receipt + receipt, 1))
        self.reject(self.check(owners=owners), "owner")




class CompactCollectionDispositionTests(unittest.TestCase):
    """Residual support cannot conceal actual or independently required works."""
    def setUp(self):
        spec = importlib.util.spec_from_file_location("compact_collection_under_test", MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.paths = ["fixture-collection/paper.md", "fixture-collection/edition.pdf",
                      "fixture-collection/required.md", "fixture-collection/history.json",
                      "fixture-collection/check.py", "fixture-other/paper.md"]
        self.rows = [{"path": path} for path in self.paths]
        self.owners = {
            "collections": [{"key": "collection", "include": ["fixture-collection/"],
                             "exclude": [], "owners": [self.paths[3]]}],
            "disposition_required_groups": ["collection"],
            "required_work_sources": [self.paths[2]],
        }
        self.cross = {
            "sources": {key: {"path": path} for key, path in
                        zip(["paper", "edition", "required", "basis", "check", "outside"],
                            self.paths)},
            "works": [{"key": "paper", "source_keys": ["paper", "required"],
                       "reading_forms": [{"source": "edition", "relationship": "preserved-edition"}]},
                      {"key": "outside", "source_keys": ["outside"]}],
            "collection_dispositions": {"collection": {
                "scope": "Synthetic scholarly work and residual support.",
                "reading_record": "Fixture-only reading record.",
                "basis_sources": ["basis"],
                "items": [{"path": path, "role": role, "work": "paper"}
                          for path, role in zip(self.paths[:3],
                                                ["work-source", "historical-edition", "work-source"])],
                "supporting_population": {
                    "work_keys": ["paper"], "roles": ["provenance-record", "test-fixture"],
                    "scope_note": "Frozen paths outside the explicit scholarly items retain support roles.",
                },
            }},
        }

    def check(self, cross=None):
        return self.mod.check_collection_dispositions(self.rows, self.owners, cross or self.cross)

    def reject(self, errors, code):
        self.assertTrue(any(error.startswith(code + ":") for error in errors), errors)

    def test_compact_support_population_covers_only_the_residual_frozen_paths(self):
        self.assertEqual(self.check(), [])
        full = deepcopy(self.cross)
        record = full["collection_dispositions"]["collection"]
        record.pop("supporting_population")
        record["items"].extend({"path": path, "role": "provenance-record", "work": "paper"}
                               for path in self.paths[3:5])
        self.assertEqual(self.check(full), [])
        record["items"].pop()
        self.reject(self.check(full), "collection-coverage")

    def test_support_population_cannot_hide_work_reading_form_or_owner_required_source(self):
        self.assertEqual(self.check(), [])
        for path in self.paths[:3]:
            with self.subTest(path=path):
                altered = deepcopy(self.cross)
                record = altered["collection_dispositions"]["collection"]
                record["items"] = [item for item in record["items"] if item["path"] != path]
                self.reject(self.check(altered), "collection-coverage")

    def test_support_population_requires_defined_distinct_works_roles_and_scope(self):
        self.assertEqual(self.check(), [])
        cases = [("work_keys", [], "collection-work"),
                 ("work_keys", ["absent-work"], "collection-work"),
                 ("work_keys", ["paper", "paper"], "collection-work"),
                 ("work_keys", "paper", "collection-work"),
                 ("roles", [], "collection-role"),
                 ("roles", ["miscellaneous"], "collection-role"),
                 ("roles", ["work-source"], "collection-role"),
                 ("roles", ["historical-edition"], "collection-role"),
                 ("roles", ["provenance-record", "provenance-record"], "collection-role"),
                 ("scope_note", "  ", "collection-coverage")]
        for field, value, code in cases:
            with self.subTest(field=field, value=value):
                altered = deepcopy(self.cross)
                altered["collection_dispositions"]["collection"]["supporting_population"][field] = value
                self.reject(self.check(altered), code)
        for value in (None, [], "support"):
            with self.subTest(population=value):
                altered = deepcopy(self.cross)
                altered["collection_dispositions"]["collection"]["supporting_population"] = value
                self.reject(self.check(altered), "collection-coverage")

    def test_compact_records_reject_duplicate_extra_or_invalid_items(self):
        self.assertEqual(self.check(), [])
        for change, code in [("duplicate", "collection-duplicate"),
                             ("extra", "collection-coverage"),
                             ("work", "collection-work"), ("role", "collection-role")]:
            with self.subTest(change=change):
                altered = deepcopy(self.cross)
                items = altered["collection_dispositions"]["collection"]["items"]
                if change == "duplicate":
                    items.append(deepcopy(items[0]))
                elif change == "extra":
                    items.append({"path": self.paths[-1], "work": "paper", "role": "work-source"})
                else:
                    items[0][change] = "undefined"
                self.reject(self.check(altered), code)

    def test_compact_records_reject_undefined_source_references(self):
        self.assertEqual(self.check(), [])
        for field in ("source_keys", "reading_forms", "basis_sources"):
            with self.subTest(field=field):
                altered = deepcopy(self.cross)
                if field == "source_keys":
                    altered["works"][0][field].append("undefined-source")
                elif field == "reading_forms":
                    altered["works"][0][field][0]["source"] = "undefined-source"
                else:
                    altered["collection_dispositions"]["collection"][field] = ["undefined-source"]
                self.reject(self.check(altered), "collection-coverage" if field == "basis_sources"
                            else "collection-source")

    def test_compact_primary_items_require_their_actual_bound_work(self):
        self.assertEqual(self.check(), [])
        for path in self.paths[:3]:
            with self.subTest(path=path):
                altered = deepcopy(self.cross)
                item = next(i for i in altered["collection_dispositions"]["collection"]["items"]
                            if i["path"] == path)
                item["work"] = "outside"
                self.reject(self.check(altered), "collection-work")
        unbound = deepcopy(self.cross)
        unbound["works"][0]["source_keys"].remove("required")
        self.reject(self.check(unbound), "collection-work")

    def test_shared_primary_and_reading_form_allow_either_bound_work(self):
        self.assertEqual(self.check(), [])
        shared = deepcopy(self.cross)
        shared["works"][1]["source_keys"].append("paper")
        shared["works"][1]["reading_forms"] = [{"source": "edition", "relationship": "preserved-edition"}]
        for item in shared["collection_dispositions"]["collection"]["items"][:2]:
            item["work"] = "outside"
        self.assertEqual(self.check(shared), [])

    def test_compact_primary_roles_preserve_scholarly_and_component_dispositions(self):
        self.assertEqual(self.check(), [])
        for role in ("work-source", "historical-edition", "formal-component",
                     "executable-component", "collection-guide", "test-fixture",
                     "provenance-record", "reference-material", "integration-adapter"):
            with self.subTest(role=role):
                altered = deepcopy(self.cross)
                for item in altered["collection_dispositions"]["collection"]["items"]:
                    item["role"] = role
                if role in ("test-fixture", "provenance-record", "reference-material", "integration-adapter"):
                    self.reject(self.check(altered), "collection-role")
                else:
                    self.assertEqual(self.check(altered), [])

    def test_compact_basis_sources_must_all_name_declared_collection_owners(self):
        self.assertEqual(self.check(), [])
        for basis in (["paper"], ["outside"], ["basis", "outside"]):
            with self.subTest(basis=basis):
                altered = deepcopy(self.cross)
                altered["collection_dispositions"]["collection"]["basis_sources"] = basis
                self.reject(self.check(altered), "collection-coverage")

    def test_support_work_destinations_require_a_bound_path_inside_the_group(self):
        self.assertEqual(self.check(), [])
        for owners_also_present in (False, True):
            with self.subTest(owners_also_present=owners_also_present):
                altered = deepcopy(self.cross)
                support = altered["collection_dispositions"]["collection"]["supporting_population"]
                support["work_keys"] = ["outside"]
                if owners_also_present:
                    support["owner_paths"] = [self.paths[3]]
                self.reject(self.check(altered), "collection-work")
        for field, value in (("source_keys", ["outside", "paper"]),
                             ("reading_forms", [{"source": "edition", "relationship": "preserved-edition"}]),
                             ("supporting_source_keys", ["check"])):
            with self.subTest(binding=field):
                spanning = deepcopy(self.cross)
                spanning["works"][1][field] = value
                spanning["collection_dispositions"]["collection"]["supporting_population"]["work_keys"] = ["outside"]
                self.assertEqual(self.check(spanning), [])

    def test_supporting_source_references_must_resolve(self):
        self.cross["works"][1]["supporting_source_keys"] = ["check"]
        self.cross["collection_dispositions"]["collection"]["supporting_population"]["work_keys"] = ["outside"]
        self.assertEqual(self.check(), [])
        for value in (["undefined-source"], [None], None, "check"):
            with self.subTest(value=value):
                altered = deepcopy(self.cross)
                altered["works"][1]["supporting_source_keys"] = value
                self.reject(self.check(altered), "collection-source")

    def test_pure_support_collection_can_route_through_its_existing_owner(self):
        self.rows = [row for row in self.rows if row["path"] in self.paths[3:]]
        self.owners["required_work_sources"] = []
        self.cross["works"] = [self.cross["works"][1]]
        record = self.cross["collection_dispositions"]["collection"]
        record["items"] = []
        record["supporting_population"].pop("work_keys")
        record["supporting_population"]["owner_paths"] = [self.paths[3]]
        self.assertEqual(self.check(), [])

    def test_owner_only_support_keeps_all_primary_and_independent_required_paths_explicit(self):
        support = self.cross["collection_dispositions"]["collection"]["supporting_population"]
        support.pop("work_keys")
        support["owner_paths"] = [self.paths[3]]
        self.assertEqual(self.check(), [])
        for path in self.paths[:3]:
            with self.subTest(path=path):
                altered = deepcopy(self.cross)
                if path == self.paths[2]:
                    altered["works"][0]["source_keys"].remove("required")
                record = altered["collection_dispositions"]["collection"]
                record["items"] = [item for item in record["items"] if item["path"] != path]
                self.reject(self.check(altered), "collection-coverage")

    def test_owner_paths_are_validated_even_when_a_valid_work_destination_remains(self):
        self.cross["collection_dispositions"]["collection"]["supporting_population"]["owner_paths"] = [self.paths[3]]
        self.assertEqual(self.check(), [])
        for value in (None, [], self.paths[3], ["undefined-owner"], [self.paths[0]],
                      [self.paths[-1]], [self.paths[3], self.paths[3]], [self.paths[3], self.paths[-1]], [{}]):
            with self.subTest(value=value):
                altered = deepcopy(self.cross)
                altered["collection_dispositions"]["collection"]["supporting_population"]["owner_paths"] = value
                self.reject(self.check(altered), "collection-owner")
        altered = deepcopy(self.cross)
        support = altered["collection_dispositions"]["collection"]["supporting_population"]
        support.pop("work_keys")
        support.pop("owner_paths")
        self.reject(self.check(altered), "collection-coverage")

    def test_exhaustive_records_retain_their_existing_work_role_and_basis_semantics(self):
        record = self.cross["collection_dispositions"]["collection"]
        record.pop("supporting_population")
        record["items"].extend({"path": path, "role": "provenance-record", "work": "paper"}
                               for path in self.paths[3:5])
        record["items"][0].update(work="outside", role="test-fixture")
        record["basis_sources"] = ["outside"]
        self.assertEqual(self.check(), [])


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

    def test_reader_candidate_requires_a_real_catalogue_anchor_for_every_work(self):
        self.cross["coverage_stage"] = "reader-candidate"
        self.cross["works"] = [{"key": key, "catalogue_entry": "docs/reader/PAPER-CATALOGUE.md#" + anchor}
                               for key, anchor in (("first", "overview"), ("second", "fixture-work"))]
        page = self.page("PAPER-CATALOGUE.md")
        page.write_text(page.read_text() + '\n<a id="fixture-work"></a>\nA second scholarly entry.\n')
        self.assertEqual(self.check(), [])
        for work in self.cross["works"]:
            with self.subTest(work=work["key"]):
                altered = deepcopy(self.cross)
                next(w for w in altered["works"] if w["key"] == work["key"]).pop("catalogue_entry")
                errors = self.check(altered)
                self.assertTrue(any(error.startswith("catalogue-entry:") for error in errors), errors)

    def test_reader_candidate_rejects_absent_unsafe_or_fenced_catalogue_entries(self):
        self.cross["coverage_stage"] = "reader-candidate"
        self.cross["works"] = [{"key": "paper", "catalogue_entry": "docs/reader/PAPER-CATALOGUE.md#overview"}]
        page = self.page("PAPER-CATALOGUE.md")
        page.write_text(page.read_text() + '\n```html\n<a id="fenced-entry"></a>\n```\n')
        self.assertEqual(self.check(), [])
        for entry in (None, "", "docs/reader/PAPER-CATALOGUE.md", "docs/reader/PAPER-CATALOGUE.md#",
                      "docs/reader/PAPER-CATALOGUE.md#absent", "docs/reader/PAPER-CATALOGUE.md#fenced-entry",
                      "fixture-missing/catalogue.md#overview", "../outside.md#overview",
                      "https://example.invalid/catalogue#overview"):
            with self.subTest(entry=entry):
                altered = deepcopy(self.cross)
                altered["works"][0]["catalogue_entry"] = entry
                errors = self.check(altered)
                self.assertTrue(any(error.startswith("catalogue-entry:") for error in errors), errors)
        self.cross["coverage_stage"] = "representative-pilot"
        self.cross["works"][0].pop("catalogue_entry")
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
    def test_packet_successor_references_resolve_from_repository_root(self):
        import sys
        import yaml
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_internal_references as refs
        status_path = "experiments/experiment-status.yaml"
        document = yaml.safe_load((ROOT / status_path).read_text(encoding="utf-8"))
        for packet in document["packets"]:
            if "consumer_successor" not in packet:
                continue
            for path in packet["consumer_successor"]["files"]:
                with self.subTest(packet=packet["packet_id"], path=path):
                    self.assertTrue(path.startswith(packet["path"]))
                    self.assertTrue(refs._resolves(status_path, path))
        for owner in (status_path, "scripts/validate_experiment_readiness.py"):
            text = (ROOT / owner).read_text(encoding="utf-8")
            missing = sorted({path for path, _ in refs._citation_occurrences(
                owner, text, root=str(ROOT), successor_sources={})
                if not refs._resolves(owner, path)})
            self.assertEqual(missing, [], owner)

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



    def test_packet_member_exemption_is_exact_to_replay_owner_and_body(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_internal_references as refs
        owner = "/".join(("scripts", "replay_v5_successors.py"))
        text = (ROOT / owner).read_text(encoding="utf-8")
        expected = {"/".join(("scripts", name))
                    for name in ("verify-inputs.py", "verify-sources.py")}
        self.assertEqual(refs._original_driver_members(owner, text), expected)
        changed = text + "\n# changed owner body\n"
        other_owner = "/".join(("scripts", "unrelated-owner.py"))
        for source, body in ((owner, changed), (other_owner, text)):
            with self.subTest(owner=source):
                self.assertEqual(refs._original_driver_members(source, body), set())
                citations = {path for path, _ in refs._citation_occurrences(
                    source, body, root=str(ROOT), successor_sources={})}
                self.assertTrue(expected <= citations)
        citations = {path for path, _ in refs._citation_occurrences(
            owner, text, root=str(ROOT), successor_sources={})}
        self.assertFalse(expected & citations)
        unrelated = "/".join(("scripts", "unexpected-packet-member.py"))
        citations = {path for path, _ in refs._citation_occurrences(
            owner, text + "\n# " + unrelated, root=str(ROOT), successor_sources={})}
        self.assertIn(unrelated, citations)


class HistoricalMetadataPinTests(unittest.TestCase):
    """Historical source custody survives an authorised current-index addition."""
    TYPED_REVISION = "a7ff0e33d1a299db640041c46b1af81ca70851f6"
    TYPED_PINS = (
        ("experiments/orthemology-v5-successors/source-store/b99fb16058f99ce5db66dd7a02e7515ede5157a002a6e76fc29d0f1bd8d65236/OPAQUE_ATOM_COMPLETENESS_PROOF_v3.md",
         "ab7ccee9a98d5a88b8b79a6f0d6a010298bf3204"),
        ("experiments/orthemology-v5-successors/source-store/7ff286710275b8873e2847ef21b9a30e70c20f465b6bb680569b8f107b484f3e/RESIDUAL_IDENTITY_COMPLETENESS_FEASIBILITY_v1.md",
         "0692dd6d775e0391498c97c5b77e8c83cf32eb41"),
        ("experiments/orthemology-v5-successors/source-store/02f2ba85547a0798288ec5d307f06fa5b239b8cb9e0faa4b7c7a6ba303097bbe/HYPOTHETICAL_ATOM_APPLICATION_BRIDGE_v2.md",
         "a4d90c7d566d79394ca4755bf1d792e810d66880"),
        ("experiments/orthemology-v5-successors/source-store/5d58087eab7e247235ec159abc17f6dc6d5779dc7722518f06d5040b25414e3a/Intensional_Identity_Separation_and_Closed_Identity_Conversion.md",
         "4920e71de4ac0c17fa8a93f02cd891d65ea8ad74"),
    )

    def prior_to_typed_pins(self):
        """Build the exact prior form before testing its earlier pin sequence."""
        value = json.loads(subprocess.check_output(
            ["git", "show", "1beacf590a4f11079039582b42d98d63c563378b:" + self.manifest_path], cwd=ROOT))
        for path, blob in self.TYPED_PINS:
            row = next(r for r in value["objects"] if r.get("repository_path") == path)
            self.assertEqual((row["repository_revision"], row["git_blob"]),
                             (self.TYPED_REVISION, blob))
            del row["repository_revision"]
            del row["git_blob"]
        return value

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
        contributor = next(r for r in value["objects"] if r["source_sha256"] ==
                           "5e00b728e533c019b656032a86b5427f820d281056c40d78df0d0cf2c1549bc1")
        contributor.update(repository_revision="7efc6217c090b92d65f2c4cb8b011c18eb96bf7c",
                           git_blob="790eb3546a0db6627d3a51df43b1e178f464b067")
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


    def test_actual_manifest_binds_both_original_bodies_not_mutable_roots(self):
        expected, _ = self.candidate()
        # Preserve the exact original document, adding only the separately
        # qualified four prose bindings, three mediator/evidence bindings,
        # two math-code evidence bindings, the Fisher ADD_EXACT binding,
        # the legacy guide-test code binding, the two old pins, and the four
        # exact typed-prose bindings introduced after that ordered form.
        for path in HistoricalProseReaderTests.PATHS:
            for row in expected["objects"]:
                if row.get("repository_path") == path:
                    row.update(repository_revision=HistoricalProseReaderTests.BASE,
                               git_blob=subprocess.check_output(
                                   ["git", "rev-parse", HistoricalProseReaderTests.BASE + ":" + path],
                                   cwd=ROOT, text=True).strip())
        for path, revision, blob in (
            ("research/t20-v6-20261012/research-v6/type_collective/ROBUST_FINITE_MEDIATOR_BOUND.md",
                "a7ff0e33d1a299db640041c46b1af81ca70851f6", "8c8b327bb642570307e50ddaef35850b508a80e6"),
            ("experiments/orthemology-v5-successors/source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/BOUNDED_COORDINATION_INFORMATION_v1.md",
                "a7ff0e33d1a299db640041c46b1af81ca70851f6", "a949e7e8fdb1fcf386d3580a034d9cb14f34e7d5"),
            ("scripts/validate_v5_successors.py",
                "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c", "62457f5f61e6e433b7714948e1b0c2545a00fbb1"),
            ("tests/test_math_source_validator.py",
                "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c", "dcb9a7171c3f82114936c36529093674e98417ca"),
            ("scripts/validate_math_source.py",
                "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c", "7a72d773ca5248b26383624ee1837448b9a2479c"),
            ("research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md",
                "a7ff0e33d1a299db640041c46b1af81ca70851f6", "4dd0bce99ab60c34752bda1e4102341b67350c79"),
            ("tests/test_v5_twentieth_data.py",
                "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c", "e1bad4344f949d9ddbe32ca6c4e6bd4158515a86"),
        ):
            row = next(r for r in expected["objects"] if r.get("repository_path") == path)
            row.update(repository_revision=revision, git_blob=blob)
        for path, blob in self.TYPED_PINS:
            row = next(r for r in expected["objects"] if r.get("repository_path") == path)
            row.update(repository_revision=self.TYPED_REVISION, git_blob=blob)
        actual = json.loads((ROOT / self.manifest_path).read_bytes())
        # Receive the exact earlier form independently. The later 587-row
        # extension has its own whole-document and native-object controls.
        prior = json.loads(subprocess.check_output(
            ["git", "show", "1beacf590a4f11079039582b42d98d63c563378b:" + self.manifest_path], cwd=ROOT))
        self.assertEqual(prior, expected, "earlier historical owner metadata changed outside its finite bindings")
        self.assertTrue(self.permitted(prior), "the earlier complete ordered pin form must remain admitted")
        self.assertTrue(self.permitted(actual), "the complete current ordered pin form must be admitted")

    def test_fisher_pin_follows_all_prior_pins_without_resetting_the_manifest(self):
        path = "research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md"
        value = self.prior_to_typed_pins()
        legacy = next(r for r in value["objects"]
                      if r.get("repository_path") == "tests/test_v5_twentieth_data.py")
        legacy.pop("repository_revision")
        legacy.pop("git_blob")
        row = next(r for r in value["objects"] if r.get("repository_path") == path)
        self.assertEqual((row["disposition"], row["repository_revision"], row["git_blob"]),
                         ("ADD_EXACT", "a7ff0e33d1a299db640041c46b1af81ca70851f6",
                          "4dd0bce99ab60c34752bda1e4102341b67350c79"))
        self.assertTrue(self.permitted(value))
        old = deepcopy(value)
        previous = next(r for r in old["objects"] if r.get("repository_path") == path)
        previous.pop("repository_revision")
        previous.pop("git_blob")
        self.assertTrue(self.permitted(old), "the prior seven-path/math-code form must remain valid")
        for field, replacement in (("repository_revision", "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c"),
                                   ("repository_revision", "HEAD"), ("git_blob", "0" * 40),
                                   ("disposition", "REUSE"), ("public_bytes", 29667),
                                   ("public_sha256", "0" * 64), ("role", "reclassified")):
            with self.subTest(field=field, replacement=replacement):
                changed = deepcopy(value)
                next(r for r in changed["objects"] if r.get("repository_path") == path)[field] = replacement
                self.assertFalse(self.permitted(changed))
        wrong = deepcopy(value)
        prior = next(r for r in wrong["objects"] if r.get("repository_path") == "scripts/validate_math_source.py")
        prior.pop("git_blob")
        self.assertFalse(self.permitted(wrong), "Fisher cannot hide a missing prior evidence pin")

    def test_legacy_guide_code_pin_follows_fisher_without_resetting_prior_forms(self):
        path = "tests/test_v5_twentieth_data.py"
        value = self.prior_to_typed_pins()
        row = next(r for r in value["objects"] if r.get("repository_path") == path)
        self.assertEqual((row["disposition"], row["repository_revision"], row["git_blob"]),
                         ("REUSE", "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c",
                          "e1bad4344f949d9ddbe32ca6c4e6bd4158515a86"))
        self.assertTrue(self.permitted(value))
        prior = deepcopy(value)
        previous = next(r for r in prior["objects"] if r.get("repository_path") == path)
        previous.pop("repository_revision")
        previous.pop("git_blob")
        self.assertTrue(self.permitted(prior), "the exact Fisher checkpoint must remain valid")
        for field, replacement in (("repository_revision", "HEAD"),
                                   ("repository_revision", "a7ff0e33d1a299db640041c46b1af81ca70851f6"),
                                   ("git_blob", "0" * 40), ("repository_path", "/".join(("tests", "unrelated.py"))),
                                   ("source_bytes", 6820), ("public_bytes", 6820),
                                   ("public_sha256", "0" * 64), ("role", "reclassified")):
            with self.subTest(field=field, replacement=replacement):
                wrong = deepcopy(value)
                next(r for r in wrong["objects"] if r.get("repository_path") == path)[field] = replacement
                self.assertFalse(self.permitted(wrong))
        for earlier in (
                "scripts/validate_math_source.py",
                "research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md"):
            with self.subTest(missing_prior=earlier):
                wrong = deepcopy(value)
                missing = next(r for r in wrong["objects"] if r.get("repository_path") == earlier)
                missing.pop("repository_revision")
                missing.pop("git_blob")
                self.assertFalse(self.permitted(wrong), "the later pin cannot hide a missing prior pin")
        unrelated = deepcopy(value)
        unrelated["objects"][0]["role"] = "reclassified"
        self.assertFalse(self.permitted(unrelated))

    def test_contributor_pin_is_required_and_only_exact_metadata_is_admitted(self):
        identity = "5e00b728e533c019b656032a86b5427f820d281056c40d78df0d0cf2c1549bc1"
        value, _ = self.candidate()
        self.assertTrue(self.permitted(value))
        for field, replacement in (("repository_revision", "HEAD"),
                                   ("git_blob", "0" * 40),
                                   ("repository_path", "README.md"),
                                   ("public_sha256", "0" * 64),
                                   ("source_bytes", 7858),
                                   ("role", "reclassified")):
            with self.subTest(field=field):
                changed = deepcopy(value)
                next(r for r in changed["objects"] if r["source_sha256"] == identity)[field] = replacement
                self.assertFalse(self.permitted(changed))
        missing = deepcopy(value)
        row = next(r for r in missing["objects"] if r["source_sha256"] == identity)
        del row["repository_revision"]
        del row["git_blob"]
        self.assertFalse(self.permitted(missing), "removing historical binding must fail")

    def test_contributor_original_is_byte_identical_and_live_policy_is_preserved(self):
        identity = "5e00b728e533c019b656032a86b5427f820d281056c40d78df0d0cf2c1549bc1"
        value, _ = self.candidate()
        row = next(r for r in value["objects"] if r["source_sha256"] == identity)
        original = subprocess.check_output(["git", "show", row["repository_revision"] + ":CONTRIBUTING.md"], cwd=ROOT)
        blob = subprocess.check_output(["git", "rev-parse", row["repository_revision"] + ":CONTRIBUTING.md"], cwd=ROOT).decode().strip()
        self.assertEqual(blob, row["git_blob"])
        self.assertEqual(len(original), 3392)
        self.assertEqual(hashlib.sha256(original).hexdigest(), identity)
        live = (ROOT / "CONTRIBUTING.md").read_bytes()
        self.assertTrue(live.startswith(original))
        self.assertNotEqual(live, original)
        self.assertTrue(self.permitted(value), "intact historical body and live navigation must coexist")

    def test_arbitrary_additional_historical_pin_is_not_an_admitted_escape(self):
        value, _ = self.candidate()
        row = next(r for r in value["objects"] if r["disposition"] == "REUSE" and
                   "repository_revision" not in r)
        row["repository_revision"] = "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c"
        self.assertFalse(self.permitted(value))


class SnapshotProjectionPinTests(unittest.TestCase):
    """The manifest can route the finite duplicate class without changing its evidence."""
    @classmethod
    def setUpClass(cls):
        HistoricalMetadataPinTests.setUpClass()
        cls.mod = HistoricalMetadataPinTests.mod
        cls.owner = HistoricalMetadataPinTests.row
        cls.path = HistoricalMetadataPinTests.manifest_path
        cls.original = json.loads(subprocess.check_output(
            ['git', 'show', '1beacf590a4f11079039582b42d98d63c563378b:' + cls.path], cwd=ROOT))
        cls.current = json.loads(subprocess.check_output(
            ['git', 'show', '7719a7e58400b1e72809738063720492d43609c0:' + cls.path], cwd=ROOT))
        cls.before = {r['source_sha256']:r for r in cls.original['objects']}
        cls.after = {r['source_sha256']:r for r in cls.current['objects']}
        cls.changed = [s for s in cls.before if cls.before[s] != cls.after[s]]

    def permitted(self, value):
        return self.mod.permitted_historical_status_pin(ROOT, self.owner, json.dumps(value).encode())

    def test_exact_complete_extension_preserves_every_original_identity(self):
        self.assertEqual(len(self.before), 28478)
        self.assertEqual(self.before.keys(), self.after.keys())
        self.assertEqual(len(self.changed), 587)
        self.assertEqual({k:v for k,v in self.original.items() if k!='objects'},
                         {k:v for k,v in self.current.items() if k!='objects'})
        aliases = self.mod.pmr007_deep_duplicate_paths(ROOT)
        duplicate_rows = [s for s in self.changed if self.after[s]['repository_path'] in aliases]
        self.assertEqual(len(aliases), 824)
        self.assertEqual(len(duplicate_rows), 584)
        self.assertEqual({self.after[s]['repository_path'] for s in set(self.changed)-set(duplicate_rows)}, {
            'tests/test_ar8r_v11_reconciliation.py', 'scripts/validate_ar8r_reconciliation.py',
            'docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-DEEP-A-AP-ADOPTION-BOUNDARY-CORRECTION.md'})
        for source in self.changed:
            old, new = self.before[source], self.after[source]
            self.assertEqual({k:v for k,v in old.items() if k!='publication_basis'},
                             {k:v for k,v in new.items() if k not in ('repository_revision','git_blob','publication_basis')})
            self.assertEqual(new['repository_revision'], '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')
            original = subprocess.check_output(['git', '--no-replace-objects', 'show',
                new['repository_revision'] + ':' + new['repository_path']], cwd=ROOT)
            self.assertEqual(hashlib.sha256(original).hexdigest(), source)
            self.assertEqual(len(original), new['source_bytes'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest(), new['git_blob'])
        self.assertTrue(self.permitted(self.current))

    def test_extension_rejects_identity_role_route_and_incomplete_pin_changes(self):
        sample = self.changed[0]
        for field, value in (('source_sha256','0'*64), ('public_sha256','0'*64),
                ('source_bytes',1), ('public_bytes',1), ('repository_revision','HEAD'),
                ('git_blob','0'*40), ('disposition','PROJECT'), ('role','reclassified'),
                ('publication_basis','unreviewed'), ('repository_path','README.md')):
            with self.subTest(field=field):
                candidate = deepcopy(self.current)
                next(r for r in candidate['objects'] if r['source_sha256']==sample)[field] = value
                self.assertFalse(self.permitted(candidate))
        missing = deepcopy(self.current)
        next(r for r in missing['objects'] if r['source_sha256']==sample).pop('git_blob')
        self.assertFalse(self.permitted(missing))

    def test_extension_rejects_unrelated_rows_and_excluded_snapshot_metadata(self):
        aliases = self.mod.pmr007_deep_duplicate_paths(ROOT)
        excluded = [r for r in self.current['objects'] if r.get('repository_path','').startswith(
            'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-ap/')
            and r['repository_path'] not in aliases]
        self.assertEqual(len(excluded), 3)
        for source in excluded:
            with self.subTest(path=source['repository_path']):
                candidate = deepcopy(self.current)
                next(r for r in candidate['objects'] if r['source_sha256']==source['source_sha256'])['repository_revision'] = \
                    '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
                self.assertFalse(self.permitted(candidate))
        unrelated = deepcopy(self.current)
        next(r for r in unrelated['objects'] if r['source_sha256'] not in self.changed)['role'] = 'reclassified'
        self.assertFalse(self.permitted(unrelated))


class BulkConsumerProjectionPinTests(unittest.TestCase):
    """Changed current consumers retain three exact original T20 evidence bodies."""
    PINS = {
        'scripts/validate_research_continuations.py':
            ('5157341400df0d327cb39f698838ac8ba49f82eb6bf71c8e40f84f670b3e55f7', 29272, 'ef5422f8e877f628e8aedbe61dc4dd2af614cb0a'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-ROUNDS11-20-ADOPTION-BOUNDARY-CORRECTION.md':
            ('66cc0fbc5ab06ab0dfffdb1e6fe1845775cfa0f12233f7517d12042ae16d9486', 1354, '6240db1cb6e2f844506a989ee2cfa14783c6d6d6'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/README.md':
            ('d20707cf0d24dd5b2b966f2b1f3640ec7672092ef8a19b57f60fc61897cd6b50', 4073, '9628152cf22670418bc2c88aa13e496047fba40c'),
    }

    # Independently admitted coordinate additions; all original row fields stay exact.
    # The fixture cohort keeps its original complete 22-coordinate contract.
    BASE_COORDINATE_PINS = {'docs/provenance/v5-research-continuations/notes/002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e.md': ('002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e',
                                                                                                                             6680,
                                                                                                                             '2804e7b196437dd437f0099b15aa45a76249e63b',
                                                                                                                             'a7ff0e33d1a299db640041c46b1af81ca70851f6'),
     'docs/provenance/v5-research-continuations/notes/34c1f25cd1144b386ff4c70a2fbfacc7da2a0fc87f5cd78b430badf260ab49f6.md': ('34c1f25cd1144b386ff4c70a2fbfacc7da2a0fc87f5cd78b430badf260ab49f6',
                                                                                                                             1017,
                                                                                                                             '6bcd9f7c0faea3fe3037c1f188288555312517b1',
                                                                                                                             'b4d58482ae00f138782276ee5c4034c48bb2df19'),
     'docs/provenance/v5-research-continuations/notes/36bf84b786280660b3ec4a5e3a110f04d98598cdbe49e7680a438de344a0dd06.md': ('36bf84b786280660b3ec4a5e3a110f04d98598cdbe49e7680a438de344a0dd06',
                                                                                                                             7718,
                                                                                                                             'f43d9ffc34ad19eb1e4d14cb1a176a916d408a36',
                                                                                                                             'd0abc116b51f04c064fc60ebbdd511b63a795f45'),
     'docs/provenance/v5-research-continuations/notes/4878fd0a4cf6c952af7cdbcb7e8a386c2730ff9986b74b8e39bf9b5077815b0f.md': ('4878fd0a4cf6c952af7cdbcb7e8a386c2730ff9986b74b8e39bf9b5077815b0f',
                                                                                                                             15286,
                                                                                                                             'f419024deb2a40bf50f7315cdf2dfdde9ede77f6',
                                                                                                                             'a7ff0e33d1a299db640041c46b1af81ca70851f6'),
     'docs/provenance/v5-research-continuations/notes/71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e.md': ('71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e',
                                                                                                                             16844,
                                                                                                                             '75bb17ddd69e37db6530357307078d056b97ec16',
                                                                                                                             'd0abc116b51f04c064fc60ebbdd511b63a795f45'),
     'docs/provenance/v5-research-continuations/notes/7d3cbeb8bcacdb5d28cb457801ba41de9b21f91542866fe5c5f13a4a632dadd9.md': ('7d3cbeb8bcacdb5d28cb457801ba41de9b21f91542866fe5c5f13a4a632dadd9',
                                                                                                                             14328,
                                                                                                                             '07a1df58ff170334e07261c93af8345093b0f160',
                                                                                                                             'b4d58482ae00f138782276ee5c4034c48bb2df19'),
     'docs/provenance/v5-research-continuations/notes/9438fdcbea8747c7e5599483096eca9541cfdf673d6a96866c019c5ced06519a.md': ('9438fdcbea8747c7e5599483096eca9541cfdf673d6a96866c019c5ced06519a',
                                                                                                                             11145,
                                                                                                                             '80e45c60c8f4e71a8191f906d04afd4ab0384b06',
                                                                                                                             'b4d58482ae00f138782276ee5c4034c48bb2df19'),
     'docs/provenance/v5-research-continuations/notes/b092780b29dd9fa00ac276142b090a5b8b88da79da9c278268264669e08f3d8c.md': ('b092780b29dd9fa00ac276142b090a5b8b88da79da9c278268264669e08f3d8c',
                                                                                                                             29013,
                                                                                                                             '4e69862256f3014f8e94d528b13ff0f63dd7f3eb',
                                                                                                                             'b4d58482ae00f138782276ee5c4034c48bb2df19'),
     'experiments/episode-reification-v2/README.md': ('cf660c095bf11d03bec1f13d36eaf994226b63329dbd53f31a714d7899767da4',
                                                      1561,
                                                      '62c5a4b3b4af1d0860a0d9b6184a0f5604670836',
                                                      '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/episode-reification-v2/analysis/analyze_er2.py': ('448d7f598916a94855dd6e1060361f7686240ab542caef1a44b8fb9637026f3b',
                                                                    10418,
                                                                    '2addf30dab7b3b6f4f094a37250bd11f50718cc2',
                                                                    '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/episode-reification-v2/harness/run_er.py': ('bd84fdfa3d8973b39f04a9dc0014f3dc1b5574caf61ed7643ca78ae782455d20',
                                                              7347,
                                                              'c4fa618a88160e0b4da89644abb3e9a49d49626a',
                                                              '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/episode-reification-v2/scripts/generate_cases.py': ('d4ae498ed5b992ec366a752300a949ba64a3d90ce01c63c28392dacbe9827aa3',
                                                                      8526,
                                                                      '7eab184f0ff3cdc4869600528ceae1665865e9b8',
                                                                      '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/episode-reification-v2/tests/test_smoke.py': ('41517fa67f0998e92ccbaff09843bac86b20a7144a9c7016927fb4bc4d6f412f',
                                                                8543,
                                                                '4da6e02cdf9777b74afa2f6a2d19f236d8a9ccab',
                                                                '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/episode-reification/README.md': ('ca21e76e775fe1637098aa90b6e6544fa732ef4a82c874de5aab6cbf6f4451b6',
                                                   1197,
                                                   '28f48c3f8ef3c56bca366fbf6fac0b9bf54a4f40',
                                                   '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/episode-reification/scripts/generate_fixtures.py': ('7ce757842bf2e9fa87a23004675d147687009b1a84a4cf3fc08908f227d45564',
                                                                      8187,
                                                                      '2d971fd8c236334a9a2069e48cc53333d141b7c1',
                                                                      '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/episode-reification/tests/test_smoke.py': ('3606f98b6f2072c5a39fbb24e3d4728b4e9b047b82c65f7d4b8187ef3d010c1c',
                                                             5936,
                                                             '9c74297fd87351299f1223624d8b8e50c76ffd45',
                                                             '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/experiment-status.yaml': ('88e59fdfc9e1e4a3ab751fef6e2f6bc1c5a644fc5863bf679b35c2ceb56cf2b2',
                                            6886,
                                            'eb979d8fd40710cbe9adeabd1c76c3571c4f22d6',
                                            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/orthemology-v5-continuations/registry.json': ('51e2cea236dd0a880c7243b2f9ccbd558c6c70f16f03ec0efa274f19d3d105ff',
                                                                192971,
                                                                'd90b5647de1cf290d3b7dbe20a805983c75f0fcf',
                                                                '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'scripts/generate_current_state.py': ('a64b60308dd916505e0e10ce585e3e08c5f20172560b0c1e7deda0e086e830de',
                                           8057,
                                           '84429a260b6084fce35dd0934a9fd6c72efc3a09',
                                           '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'scripts/validate_experiment_readiness.py': ('3c7db3b6a05c9c21a1ef255f083b24842ddebee0512ea61a4a074d9c88f1346b',
                                                  10208,
                                                  'dcb5c2a61e443a8d704b8e9516c1abe444ade712',
                                                  '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'scripts/validate_negative_fixtures.py': ('6631cc99253d14a78b91022b95b646dba48bae1f34a0b86390fbd3e4dd85d92b',
                                               7429,
                                               '5521fbfea42ff7e20a85fdd8c31ee4b85d1bdfc5',
                                               '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'tests/schema-negative/NEGATIVE-FIXTURES.json': ('b342240297511473b5c5568d4662de413d1f69fef20a7a55dc59c24657e7580b',
                                                      10709,
                                                      'a002ee8e159a7678e6c704323ca62670cc389880',
                                                      '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}

    COORDINATE_PINS = {
        # Six reviewed digest176 consumers retain these exact original coordinates.
        'scripts/validate_ar8r_codex_corpus_synthesis_v14.py': (
            'c2153d22937864584ca0310a129cb41badbcbea96e3a2175b53bd1a9a666a626',
            43318, 'bf5693e9eaf14f932a7afef314772c5d6cfd19c3',
            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_ar8r_external_challenges.py': (
            '621c70320e6695ea77d85c7bec7147193d3c3f013bada94ea6bae328a8616c7e',
            9558, '814d716588deff5a8f479deafc8e4d7e91e19c58',
            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_ar8r_six_lane_v14_intake.py': (
            '33de0e6b174499960cc2c521ab5ab5f2f13cb66467247636aa460419073745a3',
            19144, 'd9511107288776ddab58e06e3892bb61f3bd66e9',
            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bk_public_snapshot.py': (
            'ba437ce44adf1ab03d1f797a3c5a72f8991b99186a733bdfc2f9574b02d3d4fd',
            20394, 'b7a701ad73a96d9de760f22778a17f2128eb7799',
            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bv_semantic_reissue.py': (
            '818230667805e3db999dc52bd22376a4425e58a85f75e561da4ca39acd75e680',
            16337, '06a0f45454a02b7c849682e563f0b1aa98cab963',
            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bw_cj_semantic_reissue.py': (
            '0d75bcefc899d15b2d35377fa15b54c6d12d180a74a506bc9cd84212206c3311',
            19380, 'cb72e0de65eb40d0bd659e49e2a4b8a46ef197a9',
            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        **BASE_COORDINATE_PINS,
        # Published26's mock-fixture repair retains this exact historical source coordinate.
        'tests/v5_successor_fixtures.py': (
            '283ea7d698a5bf6a208e45260ee9078f819ecdb25a42c6dd2252d794d2dd3233',
            13030, 'ccf0bd64f34b10f65ed8bd1bdd8a88adcaf03c7f',
            '69f3f9284f2cb94433958c0669fc9b06a9760fe7'),
     'experiments/orthemology-v5-successors/groups/t07-technical/README.md': ('3eb797cdf4925b80e21597fed04fbda0bee7a85f7bb5a141137fbba258cf25c2',
                                                                              32584,
                                                                              '7cd6ff0393556359cecaee0c5b109a6cf8a05345',
                                                                              '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'experiments/orthemology-v5-successors/groups/t08-history/README.md': ('fb21186d2568c38564e0bf23f94df81d05fbad8fe39dcab23b6fd83b0291f7d1',
                                                                            45079,
                                                                            'a49fbf2d3e0691495f5884e3a13ec475aafb1293',
                                                                            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'scripts/replay_v5_successors.py': ('5b4c1b7f0ced9af2599b980fd25fd1a15b819357853753319798b2965fc540ef',
                                         450007,
                                         '8f6641df9d613c0814652a9b2fc338f72ebe2230',
                                         '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}

    @classmethod
    def setUpClass(cls):
        HistoricalMetadataPinTests.setUpClass()
        cls.mod = HistoricalMetadataPinTests.mod
        cls.owner = HistoricalMetadataPinTests.row
        cls.path = HistoricalMetadataPinTests.manifest_path
        cls.prior = json.loads(subprocess.check_output(
            ['git', 'show', '7719a7e58400b1e72809738063720492d43609c0:' + cls.path], cwd=ROOT))
        cls.current = json.loads((ROOT / cls.path).read_bytes())

    def permitted(self, value):
        return self.mod.permitted_historical_status_pin(ROOT, self.owner, json.dumps(value).encode())

    def test_current_three_owner_extension_preserves_complete_original_identities(self):
        before = {r['source_sha256']: r for r in self.prior['objects']}
        after = {r['source_sha256']: r for r in self.current['objects']}
        self.assertEqual(len(before), 28478)
        self.assertEqual(before.keys(), after.keys())
        expected_changes = ({p[0] for p in self.PINS.values()}
                            | {p[0] for p in self.COORDINATE_PINS.values()})
        self.assertEqual({k for k in before if before[k] != after[k]}, expected_changes)
        self.assertEqual({k: v for k, v in self.prior.items() if k != 'objects'},
                         {k: v for k, v in self.current.items() if k != 'objects'})
        for path, (identity, size, blob, revision) in self.COORDINATE_PINS.items():
            old, new = before[identity], after[identity]
            self.assertEqual(old['repository_path'], path)
            self.assertEqual(old['disposition'], 'REUSE')
            self.assertEqual((old['source_sha256'], old['public_sha256'],
                              old['source_bytes'], old['public_bytes']),
                             (identity, identity, size, size))
            self.assertEqual(new, dict(old, repository_revision=revision, git_blob=blob))
        for path, (identity, size, blob) in self.PINS.items():
            old, new = before[identity], after[identity]
            self.assertEqual({k: v for k, v in old.items() if k != 'publication_basis'},
                             {k: v for k, v in new.items() if k not in ('repository_revision', 'git_blob', 'publication_basis')})
            self.assertEqual(new['repository_path'], path)
            self.assertEqual(new['repository_revision'], '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')
            self.assertEqual(new['git_blob'], blob)
            original = subprocess.check_output(['git', '--no-replace-objects', 'show',
                new['repository_revision'] + ':' + path], cwd=ROOT)
            self.assertEqual(len(original), size)
            self.assertEqual(hashlib.sha256(original).hexdigest(), identity)
            self.assertEqual(hashlib.sha1(b'blob ' + str(size).encode() + b'\0' + original).hexdigest(), blob)
            self.assertNotEqual((ROOT / path).read_bytes(), original)
        self.assertTrue(self.permitted(self.current))

    def test_preceding_587_row_form_remains_admissible(self):
        self.assertTrue(self.permitted(self.prior))

    def test_new_owner_identity_and_route_faults_are_rejected(self):
        sample = self.PINS['scripts/validate_research_continuations.py'][0]
        for field, value in (('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                ('source_bytes', 1), ('public_bytes', 1), ('repository_revision', 'HEAD'),
                ('git_blob', '0' * 40), ('disposition', 'PROJECT'), ('role', 'reclassified'),
                ('publication_basis', 'unreviewed'), ('repository_path', 'README.md')):
            with self.subTest(field=field):
                candidate = deepcopy(self.current)
                next(r for r in candidate['objects'] if r['source_sha256'] == sample)[field] = value
                self.assertFalse(self.permitted(candidate))
        for identity, _, _ in self.PINS.values():
            candidate = deepcopy(self.current)
            next(r for r in candidate['objects'] if r['source_sha256'] == identity).pop('git_blob')
            self.assertFalse(self.permitted(candidate))

    def test_partial_pin_set_and_unrelated_changes_are_rejected(self):
        candidate = deepcopy(self.current)
        identity = self.PINS['scripts/validate_research_continuations.py'][0]
        i = next(i for i, row in enumerate(candidate['objects']) if row['source_sha256'] == identity)
        candidate['objects'][i] = deepcopy(next(r for r in self.prior['objects'] if r['source_sha256'] == identity))
        self.assertFalse(self.permitted(candidate))
        candidate = deepcopy(self.current)
        next(r for r in candidate['objects'] if r['source_sha256'] not in {p[0] for p in self.PINS.values()})['role'] = 'reclassified'
        self.assertFalse(self.permitted(candidate))


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
                    if key == "coordination":
                        bindings = [row for row in self.owners["historical_source_bindings"]
                                    if row["path"] == path]
                        self.assertEqual(len(bindings), 1, "The incorporated source needs its exact owner binding")
                        binding = bindings[0]
                        body = self.mod.historical_source_bytes(
                            ROOT, path, binding["repository_revision"], binding["git_blob"])
                    else:
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
                                linked.add(target)
                    self.assert_work_reading_route(work, keys, linked)

    def assert_work_reading_route(self, work, keys, linked, cross=None):
        cross = self.cross if cross is None else cross
        sources = cross["sources"]
        if work["key"] != "finite-mediator" and "coordination" not in keys:
            self.assertTrue(any(sources[key]["path"] == path for key in keys
                                for path, _ in linked),
                            "An unincorporated work must directly reach its source")
            return
        # The whole coordination work now reads through Collective Inquiry §6;
        # J04 separately retains the narrower finite-capacity result in §6.4.
        # This exact, reviewed source relationship is not a general permission
        # to replace an original with any synthesis or collection link.
        self.assertEqual(work["key"], "finite-mediator")
        self.assertEqual(keys, {"coordination"})
        self.assertEqual(work["source_keys"], ["coordination"])
        self.assertEqual(work.get("reading_forms"), [
            {"source": "coordination", "relationship": "historical-source"}])
        self.assertEqual([r for r in cross["relations"] if r.get("from") == "coordination"], [{
            "from": "coordination", "to": "consolidated-collective-inquiry",
            "kind": "logical-content-incorporated-historical-source-retained",
            "basis": "scientific-consolidation-review",
        }])
        self.assertIn("scientific-consolidation-review", sources)
        current = sources.get("consolidated-collective-inquiry", {})
        target = ("mathematics/collective-inquiry-and-strategic-coordination.md",
                  "6-complete-coordination-records-across-a-growing-horizon")
        self.assertEqual(current.get("path"), target[0])
        self.assertIn(target, linked, "The named work must reach its complete incorporated treatment")
        self.assertIn(target[1], self.mod.markdown_index((ROOT / target[0]).read_text())["anchors"])

    def test_current_coordination_route_requires_its_exact_incorporation(self):
        work = next(w for w in self.cross["works"] if w["key"] == "finite-mediator")
        target = ("mathematics/collective-inquiry-and-strategic-coordination.md",
                  "6-complete-coordination-records-across-a-growing-horizon")
        self.assert_work_reading_route(work, {"coordination"}, {target})
        for linked in (set(), {(target[0], "")},
                       {(target[0], "64-exact-finite-alphabet-capacity")},
                       {(target[0], "absent-section")},
                       {(self.cross["sources"]["coordination"]["path"], "")},
                       {("docs/reader/RESULT-INDEX.md", "finite-mediator")}):
            with self.subTest(linked=linked), self.assertRaises(AssertionError):
                self.assert_work_reading_route(work, {"coordination"}, linked)
        for change in ("form", "missing-relation", "duplicate-relation", "kind",
                       "basis", "destination", "source-path", "missing-review", "work-source"):
            altered = deepcopy(self.cross)
            candidate = next(w for w in altered["works"] if w["key"] == "finite-mediator")
            relation = next(r for r in altered["relations"] if r.get("from") == "coordination")
            if change == "form":
                candidate["reading_forms"][0]["relationship"] = "authored-source"
            elif change == "missing-relation":
                altered["relations"].remove(relation)
            elif change == "duplicate-relation":
                altered["relations"].append(deepcopy(relation))
            elif change in ("kind", "basis", "destination"):
                relation[{"kind": "kind", "basis": "basis", "destination": "to"}[change]] = "unrelated"
            elif change == "source-path":
                altered["sources"]["consolidated-collective-inquiry"]["path"] = "docs/reader/RESULT-INDEX.md"
            elif change == "missing-review":
                del altered["sources"]["scientific-consolidation-review"]
            else:
                candidate["source_keys"] = ["consolidated-collective-inquiry"]
            with self.subTest(change=change), self.assertRaises(AssertionError):
                self.assert_work_reading_route(candidate, {"coordination"}, {target}, altered)

    def test_unincorporated_twelfth_sources_still_require_their_own_links(self):
        target = ("mathematics/collective-inquiry-and-strategic-coordination.md",
                  "6-complete-coordination-records-across-a-growing-horizon")
        for member in self.members:
            keys = {k for k, v in self.cross["sources"].items() if v["sha256"] == member["sha256"]}
            if "coordination" in keys:
                continue
            for work in self.cross["works"]:
                if not keys.intersection(work["source_keys"]):
                    continue
                with self.subTest(source=member["path"]):
                    own = {(self.cross["sources"][key]["path"], "") for key in keys}
                    self.assert_work_reading_route(work, keys, own)
                    altered = deepcopy(self.cross)
                    altered["relations"].extend({
                        "from": key, "to": "consolidated-collective-inquiry",
                        "kind": "logical-content-incorporated-historical-source-retained",
                        "basis": "scientific-consolidation-review",
                    } for key in keys)
                    with self.assertRaises(AssertionError):
                        self.assert_work_reading_route(work, keys, {target}, altered)

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
        cls.historical_routes = {
            cls.cross["sources"][key]["path"]: (
                "https://github.com/theislampill/orthemology/blob/a7ff0e33d1a299db640041c46b1af81ca70851f6/"
                + cls.cross["sources"][key]["path"], "../../logic/encodings-and-witnesses.md#" + anchor)
            for key, anchor in {
                "t13-opaque": "103-equal-evaluation-need-not-preserve-a-supplied-typing",
                "t13-residual": "105-the-identity-question-that-packing-leaves-open",
                "t13-bridge": "104-what-the-bridge-repairs",
                "t14-separation": "107-full-rule-separation-and-the-exact-closed-criterion",
            }.items()
        }
        cls.members = set()
        for group in ("t13-identity", "t14-identity"):
            path = "experiments/orthemology-v5-successors/groups/" + group + "/README.md"
            raw = subprocess.check_output(["git", "show", cls.baseline + ":" + path], cwd=ROOT).decode()
            for _, href in cls.mod.markdown_index(raw)["links"]:
                if "source-store/" in href and href.endswith((".md", ".lean")):
                    # The original owner defines all seven identities even when
                    # a qualified prose occurrence is read through exact history.
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(path), href))
                    if not target.startswith("experiments/orthemology-v5-successors/source-store/"):
                        raise ValueError("Original identity owner has an unexpected source route")
                    cls.members.add(target)
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
                if member in self.historical_routes:
                    links = {href for line, href in page["links"] if start <= line < end}
                    original, current = self.historical_routes[member]
                    if original in links and current in links:
                        reachable = True
                    continue
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
            href = self.historical_routes.get(member, ("../../" + member,))[0]
            altered = self.text.replace(href, "../../README.md")
            with self.subTest(source=member):
                self.assertNotEqual(altered, self.text)
                self.assertIn("missing-route: " + member, self.routes(altered, self.cross))

    def test_each_migrated_prose_work_retains_a_direct_current_reading_route(self):
        for member, (_, current) in self.historical_routes.items():
            with self.subTest(source=member):
                altered = self.text.replace(current, "../../README.md")
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
            links = {href for line,href in page["links"] if start <= line < end}
            migrated = [(key, row, family.REV)
                        for family in (ContinuationNoteReaderMigrationTests, T4NoteReaderMigrationTests, Next24HistoricalMigrationTests)
                        for key, row in family.NOTES.items() if row[3] is not None
                        and path == "docs/provenance/v5-research-continuations/notes/" + row[0] + ".md"]
            if migrated:
                key, row, revision = migrated[0]
                relation = {"from": key, "to": row[4],
                    "kind": "logical-content-incorporated-historical-source-retained",
                    "basis": "scientific-consolidation-review"}
                historical = "https://github.com/theislampill/orthemology/blob/" + revision + "/" + path
                if (works[0]["key"] != row[3] or works[0]["source_keys"] != [key]
                        or works[0]["reading_forms"] != [{"source": key, "relationship": "historical-source"}]
                        or works[0].get("supporting_source_keys") != list(row[7])
                        or [r for r in cross["relations"] if r.get("from") == key] != [relation]
                        or cross["sources"].get(row[4], {}).get("path") != row[5]
                        or "../../" + row[5] + "#" + row[6] not in links
                        or historical not in links or "../../" + path in links):
                    errors.append("source:" + member)
            elif "../../" + path not in {href.split("#", 1)[0] for href in links}:
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
            migrated = [row for family in (ContinuationNoteReaderMigrationTests, T4NoteReaderMigrationTests, Next24HistoricalMigrationTests)
                        for row in family.NOTES.values() if row[3] is not None
                        and path == "docs/provenance/v5-research-continuations/notes/" + row[0] + ".md"]
            original = "../../" + migrated[0][5] + "#" + migrated[0][6] if migrated else "../../" + path
            changed = self.text.replace(original, "../../"+replacement)
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
        actual_module = {(v["sha256"], Path(v["member"]).name) for v in rows
                         if v["member"].endswith("/FullControllerCanonicalLaw.lean") and v.get("path")}
        self.assertEqual(len(actual_module), 1)
        digest, filename = actual_module.pop()
        retained = f"experiments/orthemology-v5-successors/source-store/{digest}/{filename}"
        self.assertIn(retained, paths)
        self.assertEqual({self.cross["sources"][k]["sha256"] for k in all_keys
                          if self.cross["sources"][k]["path"] == retained}, {digest})
        self.assertEqual(hashlib.sha256((ROOT / retained).read_bytes()).hexdigest(), digest)


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


class ContinuationCollectionCompletionTests(unittest.TestCase):
    """Declared source collection, not catalogue size, supplies the denominator."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("continuation_complete_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        d = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.owners = json.loads((d / "OWNER-MAP.json").read_text())
        cls.cross = json.loads((d / "CROSSWALK.json").read_text())
        cls.rows = cls.mod.entries_at(ROOT, cls.owners["baseline"]["commit"])
        cls.registry_path = "experiments/orthemology-v5-continuations/registry.json"
        cls.registry = json.loads((ROOT / cls.registry_path).read_text())
        cls.work = {w["key"]: w for w in cls.cross["works"]}

    def test_entire_continuation_population_has_exact_roles(self):
        records = self.cross.get("collection_dispositions", {})
        self.assertIn("v5-continuations", records)
        self.assertIn("v5-continuations", self.owners.get("disposition_required_groups", []))
        expected = {r["path"] for r in self.rows if r["path"].startswith((
            "experiments/orthemology-v5-continuations/", "docs/provenance/v5-research-continuations/"))}
        record = records["v5-continuations"]
        self.assertEqual({i["path"] for i in record["items"]}, expected)
        self.assertEqual(len(record["items"]), len(expected))
        self.assertEqual(self.mod.check_collection_dispositions(self.rows, self.owners, self.cross), [])
        changed = deepcopy(self.cross)
        changed["collection_dispositions"]["v5-continuations"]["items"].pop()
        self.assertTrue(self.mod.check_collection_dispositions(self.rows, self.owners, changed))

    def test_every_declared_result_has_a_work_route_without_new_scientific_ids(self):
        self.assertTrue(hasattr(self.mod, "check_collection_result_routes"), "Missing independent result-owner route check")
        record = self.cross["collection_dispositions"]["v5-continuations"]
        self.assertEqual(set(record["result_routes"]), {x["id"] for x in self.registry["results"]})
        self.assertEqual(self.mod.check_collection_result_routes(ROOT, self.owners, self.cross), [])
        for mutation in ("missing", "unknown-result", "unknown-work", "wrong-owner"):
            changed = deepcopy(self.cross)
            routes = changed["collection_dispositions"]["v5-continuations"]["result_routes"]
            if mutation == "missing": routes.pop("T6-CONCENTRATION")
            elif mutation == "unknown-result": routes["NEW-UNREGISTERED-SCIENCE"] = ["continuation-raw-concentration"]
            elif mutation == "unknown-work": routes["T6-MOMENTS"] = ["nonexistent-work"]
            else: changed["collection_dispositions"]["v5-continuations"]["result_owner"] = "docs/notation-gallery.md"
            self.assertTrue(self.mod.check_collection_result_routes(ROOT, self.owners, changed), mutation)

    def test_formal_concentration_and_moment_works_remain_distinct(self):
        expected = {
            "continuation-raw-concentration": "211febf4a1cf053563e4cefd1adc21a4778932bc6e39c9c414c09c9020e86853.md",
            "continuation-affine-moments": "2d7ec3409db14cb075da9d60a8c0ebdcd564de32f3994a5e227fffacb31d4a42.md",
        }
        for key, filename in expected.items():
            self.assertIn(key, self.work)
            w = self.work[key]
            self.assertEqual(w["role"], "research-note")
            self.assertEqual(len(w["source_keys"]), 1)
            self.assertTrue(self.cross["sources"][w["source_keys"][0]]["path"].endswith(filename))
            path, anchor = w["catalogue_entry"].split("#", 1)
            idx = self.mod.markdown_index((ROOT / path).read_text())
            self.assertIn(anchor, idx["anchors"])
            self.assertGreaterEqual(len(w["supporting_source_keys"]), 2)

    def test_original_restart_and_actual_cost_keep_their_proof_interfaces(self):
        expected = {
            "continuation-observed-restart": (
                "1547d34d2a53302e070e7a02131f242f9cb1d80f6aa0f96fc478844f630703a3",
                "ConditionalContinuationLaw.lean"),
            "continuation-generated-cost": (
                "8b4014de8d7ae893631060dbe780cce434bccbce16524e6303e2c692f3fce46b",
                "ActualCostMoments.lean"),
        }
        for key, (digest, filename) in expected.items():
            retained = f"experiments/orthemology-v5-successors/source-store/{digest}/{filename}"
            sources = [self.cross["sources"][s] for s in self.work[key]["supporting_source_keys"]
                       if self.cross["sources"][s]["path"] == retained]
            self.assertEqual(len(sources), 1, key)
            self.assertEqual(sources[0]["sha256"], digest)
            self.assertEqual(hashlib.sha256((ROOT / retained).read_bytes()).hexdigest(), digest)
            self.assertFalse(any(digest + ".lean" in w["title"] for w in self.cross["works"]))

    def test_shared_collection_records_and_future_agenda_are_not_proofs(self):
        self.assertIn("continuation-corpus-reference", self.work)
        self.assertIn("continuation-sixth-handoff", self.work)
        self.assertEqual(self.work["continuation-corpus-reference"]["role"], "supporting-reference")
        self.assertEqual(self.work["continuation-sixth-handoff"]["role"], "synthesis")
        record = self.cross["collection_dispositions"]["v5-continuations"]
        self.assertEqual(record["result_routes"]["S6F-01"], ["continuation-corpus-reference"])
        self.assertEqual(record["result_routes"]["S6F-26"], ["continuation-sixth-handoff"])
        self.assertTrue(any(i["role"] == "historical-edition" for i in record["items"]))
        self.assertTrue(any(i["role"] == "formal-component" for i in record["items"]))

    def test_original_collection_owner_is_not_a_copied_scientific_ledger(self):
        self.assertIn("v5-continuations", self.cross.get("collection_dispositions", {}))
        record = self.cross["collection_dispositions"]["v5-continuations"]
        self.assertEqual(record["result_owner"], self.registry_path)
        for item in record["items"]:
            self.assertNotIn("claim", item)
            self.assertNotIn("scientific_status", item)
        self.assertEqual(self.mod.check_collection_result_routes(ROOT, self.owners, self.cross), [])


class SeventhSourceFamilyTests(unittest.TestCase):
    """Source-owned result/component expectations, not a catalogue count."""
    EXPECTED = {
        "T07-CRITERION-V3": "t07-criterion-installation",
        "T07-DYNAMIC-V2": "t07-live-interlocks",
        "T07-UNKNOWN-ROOT-ABC": "t07-unknown-attribution",
        "T07-COVERING-OPAQUE": "t07-opaque-covering",
        "T07-FINITE-HISTORY": "t07-finite-history",
        "T07-COMPILED-COMPOSITION": "t07-compiled-repair",
    }

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("seventh_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.work = {w["key"]: w for w in cls.cross["works"]}
        cls.results = {r["id"]: r for r in json.loads((ROOT / "docs/provenance/v5-successors/RESULT_STATUS.json").read_text())["results"]}
        cls.original_sources = {r["id"]: r for r in json.loads((ROOT / "docs/provenance/v5-successors/SOURCE_MAP.json").read_text())["sources"]}

    def test_each_seventh_result_reaches_its_named_work_and_original_components(self):
        for result_id, key in self.EXPECTED.items():
            self.assertTrue(key in self.work, result_id)
            w = self.work[key]
            self.assertIn(result_id, w.get("existing_result_ids", []))
            paths = {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}
            required = {self.original_sources[k]["public_path"] for k in self.results[result_id]["source_ids"]}
            self.assertTrue(required <= paths, (result_id, sorted(required - paths)))

    def test_seventh_catalogue_routes_to_substance_and_scoped_evidence(self):
        text = (ROOT / "docs/reader/PAPER-CATALOGUE.md").read_text()
        page = self.mod.markdown_index(text)
        for result_id, key in self.EXPECTED.items():
            self.assertTrue(key in self.work, key)
            w = self.work[key]
            rel, anchor = w["catalogue_entry"].split("#", 1)
            self.assertEqual(rel, "docs/reader/PAPER-CATALOGUE.md")
            start = next((h[2] for h in page["headings"] if h[0] == anchor), None)
            self.assertIsNotNone(start, key)
            end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= 3), page["line_count"])
            paths = set()
            for line, href in page["links"]:
                if start <= line < end:
                    target = self.mod.resolve_reader_link(ROOT, rel, href)
                    if target: paths.add(target[0])
            self.assertTrue({self.cross["sources"][k]["path"] for k in w["source_keys"]} <= paths, key)
            self.assertIn("experiments/orthemology-v5-successors/groups/t07-technical/README.md", paths)

    def test_theorem_components_and_old_reviews_do_not_multiply_seventh_works(self):
        for result_id, key in self.EXPECTED.items():
            self.assertTrue(key in self.work, key)
            w = self.work[key]
            self.assertIn(w["role"], {"research-note", "research-software"})
            self.assertNotIn("scientific_status", w)
            support = w.get("supporting_source_keys", [])
            self.assertTrue(support)
            # A support relation is not a blanket grant of independent-work credit.
            primary = set(w["source_keys"])
            for k in support:
                path = self.cross["sources"][k]["path"]
                if path.endswith(".lean"):
                    self.assertNotIn(k, primary)
                    self.assertFalse(any(x["source_keys"] == [k] for x in self.cross["works"]), path)




class EighthHistoryWorkTests(unittest.TestCase):
    """The independently owned twelve results belong to six related works."""
    EXPECTED = {
        "T08-COMMON-HISTORY": "t08-common-lifecycle",
        "T08-TYPED-HISTORY": "t08-common-lifecycle",
        "T08-LIFECYCLE-V4": "t08-common-lifecycle",
        "T08-CANCELLATION-V5": "t08-aggregate-cancellation",
        "T08-MONOTONE-CLOCK-V6": "t08-reference-clock",
        "T08-ACTUAL-BATCH": "t08-actual-batch",
        "T08-NATIVE-TWO-BATCH": "t08-actual-batch",
        "T08-SHARED-OBSTRUCTION": "t08-shared-alias",
        "T08-SHARED-TYPED": "t08-shared-alias",
        "T08-PROTECTED-CONTROLLER": "t08-protected-controller",
        "T08-ATTAINED-21ST": "t08-protected-controller",
        "T08-FINITE-BAD-STORE": "t08-protected-controller",
    }

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("eighth_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.results = {r["id"]: r for r in json.loads((ROOT / "docs/provenance/v5-successors/RESULT_STATUS.json").read_text())["results"]}
        cls.sources = {s["id"]: s for s in json.loads((ROOT / "docs/provenance/v5-successors/SOURCE_MAP.json").read_text())["sources"]}

    def test_original_eighth_results_reach_work_and_exact_formal_components(self):
        self.assertEqual(set(self.EXPECTED), {k for k in self.results if k.startswith("T08-")})
        for rid, key in self.EXPECTED.items():
            self.assertTrue(key in self.works, rid)
            w = self.works[key]
            self.assertIn(rid, w.get("existing_result_ids", []))
            got = {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}
            want = {self.sources[s]["public_path"] for s in self.results[rid]["source_ids"]}
            self.assertTrue(want <= got, (rid, sorted(want - got)))

    def test_each_work_has_direct_argument_and_scoped_evidence_routes(self):
        rel = "docs/reader/PAPER-CATALOGUE.md"
        idx = self.mod.markdown_index((ROOT / rel).read_text())
        for key in set(self.EXPECTED.values()):
            self.assertTrue(key in self.works, key)
            w = self.works[key]
            target, anchor = w["catalogue_entry"].split("#", 1)
            self.assertEqual(target, rel)
            heading = next((h for h in idx["headings"] if h[0] == anchor), None)
            self.assertIsNotNone(heading, key)
            _, level, start = heading
            end = next((h[2] for h in idx["headings"] if h[2] > start and h[1] <= level), idx["line_count"])
            reached = {self.mod.resolve_reader_link(ROOT, rel, href)[0]
                       for line, href in idx["links"] if start <= line < end
                       and self.mod.resolve_reader_link(ROOT, rel, href) is not None}
            self.assertTrue({self.cross["sources"][k]["path"] for k in w["source_keys"]} <= reached, key)
            self.assertIn("experiments/orthemology-v5-successors/groups/t08-history/README.md", reached)

    def test_successive_batch_and_clock_contracts_keep_distinct_sources(self):
        for key in ["t08-common-lifecycle", "t08-aggregate-cancellation", "t08-reference-clock", "t08-actual-batch"]:
            self.assertTrue(key in self.works, key)
        paths = {Path(self.cross["sources"][k]["path"]).name
                 for k in self.works["t08-actual-batch"]["source_keys"]}
        self.assertEqual(paths, {"BATCH_ARGUMENT.md", "BATCH_SUCCESSOR_ARGUMENT.md", "BATCH_SURVIVAL_ARGUMENT.md", "BATCH_RETRY_ARGUMENT_CORRECTED.md"})
        # A classical controller and its execution clarification are one work;
        # the distinct source-level four-path implementation is not substituted.
        self.assertTrue("t08-protected-controller" in self.works)
        w = self.works["t08-protected-controller"]
        names = {Path(self.cross["sources"][k]["path"]).name
                 for k in w["source_keys"] + w.get("supporting_source_keys", [])}
        self.assertIn("EXECUTION_CLARIFICATION.md", names)
        self.assertIn("BadStoreErasure.lean", names)
        self.assertNotIn("scientific_status", w)




class NinthInterfaceWorkTests(unittest.TestCase):
    """Exact finite evidence, modeled evaluation and runtime remain distinct."""
    EXPECTED = {**{f"D08-0{i}": "t09-finite-certificate-calculus" for i in range(1,5)},
                "D08-05": "t09-expression-correspondence", "D08-06": "t09-expression-correspondence",
                "T09-FINITE-HISTORY-REP": "t09-finite-native-controller",
                "T09-FINITE-PRIMITIVES": "t09-finite-native-controller",
                "T09-ORDERED-INITIAL": "t09-finite-native-controller",
                "T09-WHOLE-COMMAND-TRANSPORT": "t09-whole-command-transport"}

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("ninth_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.results = {r["id"]: r for r in json.loads((ROOT / "docs/provenance/v5-successors/RESULT_STATUS.json").read_text())["results"]}
        cls.sources = {s["id"]: s for s in json.loads((ROOT / "docs/provenance/v5-successors/SOURCE_MAP.json").read_text())["sources"]}

    def test_exact_result_population_and_component_ownership(self):
        self.assertEqual(set(self.EXPECTED), {k for k in self.results if k.startswith(("T09-", "D08-"))})
        for rid,key in self.EXPECTED.items():
            self.assertTrue(key in self.works, rid)
            w=self.works[key];self.assertIn(rid,w.get("existing_result_ids",[]))
            got={self.cross["sources"][k]["path"] for k in w["source_keys"]+w.get("supporting_source_keys",[])}
            want={self.sources[s]["public_path"] for s in self.results[rid]["source_ids"]}
            self.assertTrue(want <= got, (rid,sorted(want-got)))

    def test_actual_reader_sections_reach_substantive_sources_and_evidence(self):
        rel="docs/reader/PAPER-CATALOGUE.md";idx=self.mod.markdown_index((ROOT/rel).read_text())
        for key in set(self.EXPECTED.values()):
            self.assertTrue(key in self.works,key);w=self.works[key]
            target,anchor=w["catalogue_entry"].split("#",1);self.assertEqual(target,rel)
            h=next((h for h in idx["headings"] if h[0]==anchor),None);self.assertIsNotNone(h,key)
            _,level,start=h;end=next((x[2] for x in idx["headings"] if x[2]>start and x[1]<=level),idx["line_count"])
            reached={self.mod.resolve_reader_link(ROOT,rel,href)[0] for line,href in idx["links"]
                     if start<=line<end and self.mod.resolve_reader_link(ROOT,rel,href) is not None}
            want={self.cross["sources"][k]["path"] for k in w["source_keys"]}
            self.assertTrue(want<=reached,(key,sorted(want-reached)))
            self.assertTrue(any(p.startswith("experiments/orthemology-v5-successors/groups/t09-") for p in reached),key)

    def test_composition_source_binding_and_cost_keep_separate_evidence(self):
        key="t09-finite-certificate-calculus";self.assertTrue(key in self.works,key);w=self.works[key]
        names={Path(self.cross["sources"][k]["path"]).name for k in w["source_keys"]+w.get("supporting_source_keys",[])}
        self.assertTrue({"CertificateBinding.lean","CertificateComposition.lean","COST_SCOPE.md","INDEPENDENT_REVIEW.md"}<=names)
        self.assertNotIn("scientific_status",w)
        key="t09-expression-correspondence";self.assertTrue(key in self.works,key);w=self.works[key]
        names={Path(self.cross["sources"][k]["path"]).name for k in w["source_keys"]+w.get("supporting_source_keys",[])}
        self.assertTrue({"prcodec.py","P1_SCOPE.md","SOURCE_CORRESPONDENCE.md","WORDING_CLARIFICATION.md","PythonExprSafety.lean"}<=names)

    def test_transport_is_a_distinct_work_not_controller_adoption(self):
        a,b="t09-finite-native-controller","t09-whole-command-transport"
        self.assertTrue(a in self.works and b in self.works)
        self.assertNotEqual(self.works[a]["source_keys"],self.works[b]["source_keys"])
        for key in (a,b):
            self.assertNotIn("scientific_status",self.works[key])
            self.assertTrue(self.works[key].get("supporting_source_keys"))



class TenthWorkAndEvidenceTests(unittest.TestCase):
    """The independent Tenth result owner determines this work-family boundary."""
    EXPECTED = {
        "T10-OCCURRENCE-EFFECTS": "t10-occurrence-reacquisition",
        "T10-READ-COST": "t10-occurrence-reacquisition",
        "T10-INTERVAL-QUOTIENT": "t10-occurrence-reacquisition",
        "T10-TWO-CARD-FRONTIER": "t10-bounded-handoff",
        "T10-MODEL-CHECKER": "t10-occurrence-reference",
        "T10-UNIFORM-COMPLETION": "t10-law-completion",
        "T10-NONUNIFORM-COMPLETION": "t10-law-completion",
        "T10-COMPLETION-WRITTEN-FRONTIER": "t10-law-completion",
        "T10-ROBUST-COMPACT-CERTIFICATES": "t10-finite-limit-warrant",
        "T10-EXACT-THRESHOLD-BOUNDARY": "t10-finite-limit-warrant",
        "T10-PRINTED-COLLATION": "t10-printed-collation",
        "T10-SOURCE-VERSION": "t10-source-version",
    }

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("tenth_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.results = {r["id"]: r for r in json.loads((ROOT / "docs/provenance/v5-successors/RESULT_STATUS.json").read_text())["results"]}
        cls.sources = {s["id"]: s for s in json.loads((ROOT / "docs/provenance/v5-successors/SOURCE_MAP.json").read_text())["sources"]}

    def test_all_original_tenth_results_reach_real_work_and_component_owners(self):
        self.assertEqual(set(self.EXPECTED), {r for r in self.results if r.startswith("T10-")})
        for rid, key in self.EXPECTED.items():
            self.assertTrue(key in self.works, rid)
            w = self.works[key]
            self.assertIn(rid, w.get("existing_result_ids", []))
            got = {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}
            want = {self.sources[k]["public_path"] for k in self.results[rid]["source_ids"]}
            self.assertTrue(want <= got, (rid, sorted(want-got)))

    def test_reader_entries_reach_original_arguments_not_only_collection_labels(self):
        rel = "docs/reader/PAPER-CATALOGUE.md"
        idx = self.mod.markdown_index((ROOT / rel).read_text())
        for key in set(self.EXPECTED.values()):
            self.assertTrue(key in self.works, key)
            w = self.works[key]; target, anchor = w["catalogue_entry"].split("#", 1)
            self.assertEqual(target, rel)
            h = next((h for h in idx["headings"] if h[0] == anchor), None)
            self.assertIsNotNone(h, key)
            _, level, start = h
            end = next((h[2] for h in idx["headings"] if h[2] > start and h[1] <= level), idx["line_count"])
            reached = {t[0] for line, href in idx["links"] if start <= line < end
                       if (t := self.mod.resolve_reader_link(ROOT, rel, href)) is not None}
            want = {self.cross["sources"][k]["path"] for k in w["source_keys"]}
            self.assertTrue(want <= reached, (key, sorted(want-reached)))
            self.assertIn("experiments/orthemology-v5-successors/groups/t10-technical/README.md", reached)

    def test_inverse_limit_formal_parts_and_ordinary_correction_remain_together(self):
        self.assertTrue("t10-law-completion" in self.works)
        w = self.works["t10-law-completion"]
        names = {Path(self.cross["sources"][k]["path"]).name for k in w["source_keys"] + w.get("supporting_source_keys", [])}
        self.assertTrue({"INVERSE_LIMIT_AND_CONVERGENCE_CORRECTION.md", "LawCompletionCompact.lean",
                         "LawCompletionBranches.lean", "IndexedCompletionCompact.lean",
                         "IndexedCompletionForgetting.lean", "IndexedCompletionDiameter.lean"} <= names)
        self.assertNotIn("scientific_status", w)

    def test_finite_reference_and_source_assessments_do_not_gain_paper_or_replay_credit(self):
        for key, role in {"t10-occurrence-reference": "research-software",
                          "t10-printed-collation": "supporting-reference",
                          "t10-source-version": "supporting-reference"}.items():
            self.assertTrue(key in self.works, key); self.assertEqual(self.works[key]["role"], role)
            self.assertNotIn("scientific_status", self.works[key])
        self.assertNotEqual(self.works["t10-occurrence-reacquisition"]["source_keys"],
                            self.works["t10-occurrence-reference"]["source_keys"])



class EleventhWorkAndEvidenceTests(unittest.TestCase):
    """Source-owned calculus distinctions, not new formal theorem acceptance."""
    EXPECTED = {
        "T11-RAW-INDEX-SUBSTITUTION": "t11-raw-index-substitution",
        "T11-TYPED-TELESCOPE-NUCLEUS": "t11-telescope-nucleus",
        "T11-DEPENDENT-ALL": "t11-dependent-all",
        "T11-NORMALIZATION-BOUNDARY": "t11-source-normalisation",
    }

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("eleventh_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.results = {r["id"]: r for r in json.loads((ROOT / "docs/provenance/v5-successors/RESULT_STATUS.json").read_text())["results"]}
        cls.sources = {s["id"]: s for s in json.loads((ROOT / "docs/provenance/v5-successors/SOURCE_MAP.json").read_text())["sources"]}

    def test_exact_four_calculus_work_routes_keep_all_owned_components(self):
        self.assertEqual(set(self.EXPECTED), {r for r in self.results if r.startswith("T11-")})
        for rid,key in self.EXPECTED.items():
            self.assertTrue(key in self.works, rid)
            w=self.works[key]; self.assertIn(rid,w.get("existing_result_ids",[]))
            got={self.cross["sources"][k]["path"] for k in w["source_keys"]+w.get("supporting_source_keys",[])}
            want={self.sources[k]["public_path"] for k in self.results[rid]["source_ids"]}
            self.assertTrue(want<=got,(rid,sorted(want-got)))
            self.assertNotIn("scientific_status",w)

    def test_substantive_guide_and_review_routes_are_in_each_work_section(self):
        rel="docs/reader/PAPER-CATALOGUE.md"; idx=self.mod.markdown_index((ROOT/rel).read_text())
        for key in self.EXPECTED.values():
            self.assertTrue(key in self.works,key); w=self.works[key]
            page,anchor=w["catalogue_entry"].split("#",1); self.assertEqual(page,rel)
            heading=next((x for x in idx["headings"] if x[0]==anchor),None); self.assertIsNotNone(heading,key)
            _,level,start=heading
            end=next((x[2] for x in idx["headings"] if x[2]>start and x[1]<=level),idx["line_count"])
            reached={t[0] for line,href in idx["links"] if start<=line<end
                     if (t:=self.mod.resolve_reader_link(ROOT,rel,href)) is not None}
            self.assertTrue({self.cross["sources"][k]["path"] for k in w["source_keys"]}<=reached,key)
            self.assertIn("experiments/orthemology-v5-successors/groups/t11-types/README.md",reached)
            self.assertTrue(any(Path(x).name=="REVIEW.md" for x in reached),key)

    def test_normalisation_keeps_the_same_exposed_witness_and_controls(self):
        key="t11-source-normalisation";self.assertTrue(key in self.works,key)
        w=self.works[key]
        names={Path(self.cross["sources"][k]["path"]).name for k in w["source_keys"]+w.get("supporting_source_keys",[])}
        self.assertTrue({"PolymorphicNormalizationBoundary.lean","IndependentBoundaryControls.lean","REVIEW.md"}<=names)
        self.assertNotEqual(w["source_keys"],self.works["t11-dependent-all"]["source_keys"])

    def test_recursive_all_keeps_mixed_substitution_and_legacy_qualification(self):
        key="t11-dependent-all";self.assertTrue(key in self.works,key)
        w=self.works[key]
        names={Path(self.cross["sources"][k]["path"]).name for k in w["source_keys"]+w.get("supporting_source_keys",[])}
        self.assertTrue({"AllMixedAlgebra.lean","AllLegacyDerivations.lean","AllStructural.lean","IndependentMalformedReplacement.lean"}<=names)
        nucleus=self.works.get("t11-telescope-nucleus"); self.assertIsNotNone(nucleus)
        self.assertNotEqual(nucleus["source_keys"],w["source_keys"])


class SixteenthConstituentWorkTests(unittest.TestCase):
    """Check the original paper/claim/component routes, not proof or comprehension."""
    EXPECTED = {'T16-RENEWAL': 't16-certified-renewal', 'T16-RANDOMISED-ZERO': 't16-private-random-renewal', 'T16-POPULATION': 't16-closed-generation-populations', 'T16-COMPETENCE': 't16-renewal-competence', 'T16-LOOKAHEAD': 't16-finite-lookahead', 'T16-SYNTHESIS-REDUCTION': 't16-policy-certification', 'T16-SYNTHESIS-CLASSIFICATIONS': 't16-policy-certification', 'T16-UNARY-CHECKER': 't16-unary-equality', 'T16-UNARY-SPARSE': 't16-unary-equality', 'T16-CURRENT-HAS': 't16-compiled-identity-obstruction', 'T16-BRIDGE-HASPLUS': 't16-compiled-identity-obstruction', 'T16-HASC-SOUND': 't16-certificate-extension', 'T16-HASC-CLOSED': 't16-certificate-extension', 'T16-TEMPORAL': 't16-temporal-witness', 'T16-ALMOST-SURE': 't16-almost-sure-renewal', 'T16-SIGNED-SERVICE': 't16-signed-synthesis', 'T16-DIRECT-CONTROLLER': 't16-submitted-controller', 'T16-SOURCE-ASSESSMENT': 't16-research-report', 'T16-OCCURRENCE': 't16-research-report', 'T16-EMPIRICAL': 't16-game-reanalysis', 'T16-CORE-ASSURANCE': 't16-proof-recovery-reference'}
    READER = "experiments/orthemology-v5-successors/source-store/10903b3260522cec902c7213a1b93a2c3280922126994c76f95755baadc2a91e/FULL_READER_TEXT_v5.md"
    GUIDE = "experiments/orthemology-v5-successors/groups/t16-successor/README.md"
    SOURCE_INDEX = "experiments/orthemology-v5-successors/groups/t16-successor/SOURCE_INDEX.json"
    CLAIM_MAP = "experiments/orthemology-v5-successors/groups/t16-successor/CLAIM_MAP.json"

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("sixteenth_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.results = {r["id"]: r for r in json.loads((ROOT / cls.CLAIM_MAP).read_text())["results"]}
        cls.sources = {r["id"]:r for r in json.loads((ROOT / cls.SOURCE_INDEX).read_text())["sources"]}

    def test_twenty_one_original_scopes_have_sixteen_work_destinations(self):
        self.assertEqual(set(self.EXPECTED), set(self.results))
        self.assertEqual(len(set(self.EXPECTED.values())), 16)
        for rid,key in self.EXPECTED.items():
            self.assertTrue(key in self.works,rid)
            self.assertIn(rid,self.works[key].get("existing_result_ids",[]))
            self.assertNotIn("scientific_status",self.works[key])
        # Thirteen papers, one report, software and source-assurance reference.
        mathematical={self.EXPECTED[k] for k in self.EXPECTED if self.results[k]["paper"]!="report"}
        self.assertEqual(len(mathematical),13)

    def test_original_thirteen_headings_are_direct_substantive_reading_routes(self):
        index=self.mod.markdown_index((ROOT/self.READER).read_text())
        chapters=[h[0] for h in index["headings"] if h[1]==1][1:-1]
        self.assertEqual(len(chapters),13)
        rel="docs/reader/PAPER-CATALOGUE.md";page=self.mod.markdown_index((ROOT/rel).read_text())
        got=[]
        for key in dict.fromkeys(self.EXPECTED.values()):
            self.assertTrue(key in self.works,key);work=self.works[key]
            node,anchor=work["catalogue_entry"].split("#",1);self.assertEqual(node,rel)
            h=next((h for h in page["headings"] if h[0]==anchor),None);self.assertIsNotNone(h,key)
            _,level,start=h;end=next((q[2] for q in page["headings"] if q[2]>start and q[1]<=level),page["line_count"])
            targets={t for line,href in page["links"] if start<=line<end
                     if (t:=self.mod.resolve_reader_link(ROOT,rel,href)) is not None}
            self.assertIn((self.GUIDE,""),targets,key)
            for s in work["source_keys"]:
                self.assertTrue(any(t[0]==self.cross["sources"][s]["path"] for t in targets),key)
            if key not in {"t16-research-report","t16-game-reanalysis","t16-proof-recovery-reference"}:
                found=[t[1] for t in targets if t[0]==self.READER and t[1] in chapters]
                self.assertEqual(len(found),1,key);got+=found
        self.assertEqual(set(got),set(chapters))

    def test_claim_owned_components_remain_bound_without_recounting_the_volume(self):
        for rid,key in self.EXPECTED.items():
            self.assertTrue(key in self.works,rid);w=self.works[key]
            paths={self.cross["sources"][k]["path"] for k in w["source_keys"]+w.get("supporting_source_keys",[])}
            self.assertIn(self.SOURCE_INDEX,paths)
            self.assertIn(self.CLAIM_MAP,paths)
            if rid!="T16-CORE-ASSURANCE":
                wanted={self.sources[k]["public_path"] for k in self.results[rid]["source_ids"]}
                self.assertTrue(wanted<=paths,(rid,sorted(wanted-paths)))
        self.assertNotIn("t16-mathematical-volume",self.works)
        self.assertNotIn("t16-hasc-theorem-map",self.works)

    def test_hasC_map_supports_the_same_paper_and_keeps_both_scope_ids(self):
        key="t16-certificate-extension";self.assertTrue(key in self.works,key)
        w=self.works[key];self.assertEqual(set(w["existing_result_ids"]),{"T16-HASC-SOUND","T16-HASC-CLOSED"})
        paths={self.cross["sources"][k]["path"] for k in w["source_keys"]+w.get("supporting_source_keys",[])}
        self.assertTrue(any(Path(p).name=="UnaryCertificateSoundness.lean" for p in paths),sorted(paths))
        self.assertNotEqual(w["key"],self.EXPECTED["T16-CURRENT-HAS"])

    def test_reanalysis_and_proof_recovery_are_not_extra_mathematical_papers(self):
        for key,role in {"t16-game-reanalysis":"research-software","t16-proof-recovery-reference":"supporting-reference","t16-research-report":"synthesis"}.items():
            self.assertTrue(key in self.works,key);self.assertEqual(self.works[key]["role"],role)
            self.assertNotIn("scientific_status",self.works[key])
        self.assertNotEqual(self.works["t16-game-reanalysis"]["source_keys"],self.works["t16-research-report"]["source_keys"])

    def test_signed_and_submitted_controller_share_support_not_work_identity(self):
        for rid in ("T16-SIGNED-SERVICE","T16-DIRECT-CONTROLLER"):
            key=self.EXPECTED[rid];self.assertTrue(key in self.works,key)
            w=self.works[key]
            paths={self.cross["sources"][k]["path"] for k in w["source_keys"]+w.get("supporting_source_keys",[])}
            self.assertTrue(any(Path(p).name=="PROOF_SCOPE_AND_OWNERSHIP.md" for p in paths))
        self.assertNotEqual(self.EXPECTED["T16-SIGNED-SERVICE"],self.EXPECTED["T16-DIRECT-CONTROLLER"])


class SeventeenthWorkAndWarrantTests(unittest.TestCase):
    """Preserve source-owned work, model and historical-evidence boundaries."""
    GROUP="experiments/orthemology-v5-successors/groups/t17-successor"
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location("seventeenth_reader",MODULE)
        cls.mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.mod)
        cls.cross=json.loads((ROOT/"docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works={w["key"]:w for w in cls.cross["works"]}
        cls.claims=json.loads((ROOT/cls.GROUP/"CLAIM_MAP.json").read_text())["results"]
        cls.sources={s["id"]:s for s in json.loads((ROOT/cls.GROUP/"SOURCE_INDEX.json").read_text())["sources"]}
        cls.keys={"t17-foundational-report","t17-foundational-source-guide","t17-finite-assignment-inference","t17-closed-placement-evidence"}
    def work(self,key):
        self.assertTrue(key in self.works,key);return self.works[key]
    def targets(self,key):
        w=self.work(key);rel,anchor=w["catalogue_entry"].split("#",1)
        page=self.mod.markdown_index((ROOT/rel).read_text())
        h=next((x for x in page["headings"] if x[0]==anchor),None);self.assertIsNotNone(h,key)
        _,level,start=h;end=next((x[2] for x in page["headings"] if x[2]>start and x[1]<=level),page["line_count"])
        return {t for line,href in page["links"] if start<=line<end if (t:=self.mod.resolve_reader_link(ROOT,rel,href)) is not None}
    def paths(self,key):
        w=self.work(key);return {self.cross["sources"][k]["path"] for k in w["source_keys"]+w.get("supporting_source_keys",[])}
    def test_eleven_owned_result_scopes_do_not_become_eleven_papers(self):
        for key in self.keys:self.work(key)
        expected={c["id"]:("t17-finite-assignment-inference" if c["id"] in {"T17-ASSIGNMENT-UNCERTAINTY","T17-BLOCK-ORBIT-CONTRACT"} else "t17-closed-placement-evidence" if c["id"]=="T17-CLOSED-PLACEMENT-CHECK" else "t17-foundational-report") for c in self.claims}
        self.assertEqual(len(expected),11)
        for c in self.claims:
            w=self.work(expected[c["id"]]);self.assertIn(c["id"],w.get("existing_result_ids",[]));self.assertNotIn("scientific_status",w)
            self.assertTrue({self.sources[s]["public_path"] for s in c["source_ids"]}<=self.paths(w["key"]),c["id"])
    def test_report_source_guide_mathematics_and_software_keep_distinct_roles(self):
        roles={"t17-foundational-report":"synthesis","t17-foundational-source-guide":"supporting-reference","t17-finite-assignment-inference":"manuscript","t17-closed-placement-evidence":"research-software"}
        for k,v in roles.items():self.assertEqual(self.work(k)["role"],v)
        self.assertNotEqual(self.work("t17-foundational-report")["source_keys"],self.work("t17-foundational-source-guide")["source_keys"])
        self.assertTrue(set(self.work("t17-foundational-source-guide").get("existing_result_ids",[]))==set())
    def test_each_work_reaches_actual_bodies_and_the_unchanged_source_owner(self):
        for key in self.keys:
            w=self.work(key);targets=self.targets(key)
            self.assertIn((self.GROUP+"/README.md",""),targets,key)
            for k in w["source_keys"]:self.assertTrue(any(p==self.cross["sources"][k]["path"] for p,a in targets),key)
    def test_probability_contract_and_positive_epistemic_routes_have_precise_sections(self):
        expected={
            "t17-foundational-report":{"ordinary-reports-can-warrant-belief","objective-fittingness-and-the-scope-of-authority"},
            "t17-foundational-source-guide":{"actual-knowledge-and-the-role-of-basic-cognition","tawatur-and-cumulative-warrant"},
            "t17-finite-assignment-inference":{"2-the-finite-experiment-and-conditioning-contract","7-sharp-recursion-for-sequential-interval-bounds","12-conditional-inference-from-block-complement-symmetry"}}
        for key,anchors in expected.items():
            paths={self.cross["sources"][s]["path"] for s in self.work(key)["source_keys"]}
            got={a for p,a in self.targets(key) if p in paths};self.assertTrue(anchors<=got,(key,sorted(anchors-got)))
    def test_all_supplied_components_have_roles_without_raw_data_or_new_lean_claim(self):
        for k in self.keys:self.work(k)
        union=set().union(*(self.paths(k) for k in self.keys))
        self.assertTrue({s["public_path"] for s in self.sources.values()}<=union)
        w=self.work("t17-closed-placement-evidence");names={Path(p).name for p in self.paths(w["key"])}
        self.assertTrue({"FINITE_MATH_SCOPE.md","post_inspection_tail_certificate.json","verify_manifest.py","run_checks.py"}<=names)
        self.assertFalse(any(p.endswith(".lean") for p in self.paths(w["key"])))
        math=self.work("t17-finite-assignment-inference")
        self.assertTrue(any(Path(self.cross["sources"][v["source"]]["path"]).name=="Mathematical_Companion_Content_v2.md" for v in math["reading_forms"]))
        self.assertTrue(any(Path(self.cross["sources"][v.get("basis","")]["path"]).name=="RELATED_ARTIFACTS.json" for v in self.cross["relations"] if v.get("from") in {x["source"] for x in math["reading_forms"]} and v.get("basis") in self.cross["sources"]))



class EighteenthWorkAndRepresentationTests(unittest.TestCase):
    """The source-owned one-change, formal, software and appraisal contracts."""
    GROUP = "experiments/orthemology-v5-successors/groups/t18-successor"
    KEYS = {"t18-one-change-parity", "t18-semantic-endpoint", "t18-hase-countercontrols",
            "t18-exact-implementations", "t18-foundational-report", "t18-source-validation-guide"}

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("eighteenth_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.claims = json.loads((ROOT / cls.GROUP / "CLAIM_MAP.json").read_text())["results"]
        cls.sources = {s["id"]: s for s in json.loads((ROOT / cls.GROUP / "SOURCE_INDEX.json").read_text())["sources"]}

    def work(self, key):
        self.assertTrue(key in self.works, key); return self.works[key]

    def paths(self, key):
        w = self.work(key)
        return {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}

    def targets(self, key):
        w = self.work(key); rel, anchor = w["catalogue_entry"].split("#", 1)
        idx = self.mod.markdown_index((ROOT / rel).read_text())
        heading = next((h for h in idx["headings"] if h[0] == anchor), None)
        self.assertIsNotNone(heading, key)
        _, level, start = heading
        end = next((h[2] for h in idx["headings"] if h[2] > start and h[1] <= level), idx["line_count"])
        return {t for line, href in idx["links"] if start <= line < end
                if (t := self.mod.resolve_reader_link(ROOT, rel, href)) is not None}

    def test_eleven_original_results_keep_six_work_roles_and_exact_sources(self):
        for key in self.KEYS: self.work(key)
        self.assertEqual(len(self.claims), 11)
        for claim in self.claims:
            rid = claim["id"]
            key = ("t18-semantic-endpoint" if rid == "T18-RATIONAL-LEAN-ENDPOINT" else
                   "t18-hase-countercontrols" if rid.startswith("T18-HASE-") else
                   "t18-exact-implementations" if rid == "T18-IMPLEMENTATION-QUALIFICATION" else
                   "t18-foundational-report" if rid == "T18-NONCAUSAL-EXTENSION-STOP" else
                   "t18-one-change-parity")
            self.assertIn(rid, self.work(key).get("existing_result_ids", []))
            self.assertTrue({self.sources[s]["public_path"] for s in claim["source_ids"]} <= self.paths(key), rid)
            self.assertNotIn("scientific_status", self.work(key))

    def test_main_bodies_and_original_collection_are_directly_readable(self):
        for key in self.KEYS:
            w = self.work(key); got = self.targets(key)
            self.assertIn((self.GROUP + "/README.md", ""), got, key)
            for source in w["source_keys"]:
                self.assertTrue(any(path == self.cross["sources"][source]["path"] for path, anchor in got), key)

    def test_mathematics_has_input_certificate_and_uniformity_sections(self):
        paths = {self.cross["sources"][s]["path"] for s in self.work("t18-one-change-parity")["source_keys"]}
        actual = {anchor for path, anchor in self.targets("t18-one-change-parity") if path in paths}
        self.assertTrue({"2-the-operational-model", "4-the-finite-certificate-and-main-theorem",
                         "11-real-kernels-and-the-boundary-of-representation",
                         "12-common-priorities-permit-uniform-support-only-synthesis"} <= actual)

    def test_formal_and_python_work_preserve_distinct_endpoints(self):
        formal = self.work("t18-semantic-endpoint"); software = self.work("t18-exact-implementations")
        self.assertEqual(formal["role"], "research-software")
        self.assertEqual(software["role"], "research-software")
        self.assertNotEqual(formal["source_keys"], software["source_keys"])
        self.assertIn("HiddenChangeSemanticEndpoint.lean", {Path(p).name for p in self.paths(formal["key"])})
        self.assertTrue({"API.md", "VERIFICATION_SUMMARY.md", "COMPONENT_STATUS.json"} <=
                        {Path(p).name for p in self.paths(software["key"])})
        self.assertIn("InhabitedEndpointControl.lean", {Path(p).name for p in self.paths("t18-hase-countercontrols")})

    def test_report_and_source_guide_do_not_duplicate_mathematical_credit(self):
        self.assertEqual(self.work("t18-foundational-report")["role"], "synthesis")
        self.assertEqual(self.work("t18-source-validation-guide")["role"], "supporting-reference")
        self.assertEqual(self.work("t18-source-validation-guide").get("existing_result_ids", []), [])
        self.assertIn("the-foundational-result-and-the-closed-extension", {a for p, a in self.targets("t18-foundational-report")})
        self.assertIn("restricting-the-final-type-does-not-repair-the-method", {a for p, a in self.targets("t18-hase-countercontrols")})

class NineteenthSourceAndWarrantTests(unittest.TestCase):
    """Source-bound report/reference roles; not a philosophical truth test."""
    GROUP = "experiments/orthemology-v5-successors/groups/t19-successor"
    KEYS = {"t19-common-source-appraisal", "t19-source-evidence-guide", "t19-arabic-reading-index"}

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("nineteenth_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.claims = json.loads((ROOT / cls.GROUP / "CLAIM_MAP.json").read_text())["results"]
        cls.sources = {s["id"]: s for s in json.loads((ROOT / cls.GROUP / "SOURCE_INDEX.json").read_text())["sources"]}

    def work(self, key):
        self.assertTrue(key in self.works, key); return self.works[key]

    def paths(self, key):
        w = self.work(key)
        return {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}

    def targets(self, key):
        rel, anchor = self.work(key)["catalogue_entry"].split("#", 1)
        idx = self.mod.markdown_index((ROOT / rel).read_text())
        h = next((h for h in idx["headings"] if h[0] == anchor), None)
        self.assertIsNotNone(h, key)
        _, level, start = h
        end = next((h[2] for h in idx["headings"] if h[2] > start and h[1] <= level), idx["line_count"])
        return {t for line, href in idx["links"] if start <= line < end
                if (t := self.mod.resolve_reader_link(ROOT, rel, href)) is not None}

    def test_eight_original_scopes_have_one_appraisal_owner_not_eight_papers(self):
        w = self.work("t19-common-source-appraisal")
        self.assertEqual(len(self.claims), 8)
        self.assertEqual(set(w["existing_result_ids"]), {c["id"] for c in self.claims})
        for c in self.claims:
            self.assertTrue({self.sources[k]["public_path"] for k in c["source_ids"]} <= self.paths(w["key"]), c["id"])
        self.assertNotIn("scientific_status", w)

    def test_report_and_source_references_remain_distinct_with_all_components(self):
        self.assertEqual(self.work("t19-common-source-appraisal")["role"], "synthesis")
        for key in self.KEYS - {"t19-common-source-appraisal"}:
            self.assertEqual(self.work(key)["role"], "supporting-reference")
            self.assertEqual(self.work(key).get("existing_result_ids", []), [])
        paths = set().union(*(self.paths(k) for k in self.KEYS))
        self.assertTrue({s["public_path"] for s in self.sources.values()} <= paths)
        for key in self.KEYS:
            got = self.targets(key)
            self.assertIn((self.GROUP + "/README.md", ""), got)
            for k in self.work(key)["source_keys"]:
                self.assertTrue(any(p == self.cross["sources"][k]["path"] for p, a in got), key)

    def test_positive_common_source_and_obligation_transfer_have_exact_sections(self):
        paths = {self.cross["sources"][k]["path"] for k in self.work("t19-common-source-appraisal")["source_keys"]}
        got = {a for p, a in self.targets("t19-common-source-appraisal") if p in paths}
        self.assertTrue({"the-present-judgement", "the-positive-causal-rationale",
                         "from-local-coverage-to-the-connected-field",
                         "a-positive-route-with-independent-evidential-content",
                         "avenue-3-and-rightful-guidance"} <= got)

    def test_index_preserves_scope_and_revision_method_not_fresh_primary_reading(self):
        got = {a for p, a in self.targets("t19-arabic-reading-index")}
        self.assertTrue({"scope-of-this-index", "how-later-readings-revise-earlier-entries"} <= got)
        self.assertIn("Arabic_Volume_Reading_Index.json", {Path(p).name for p in self.paths("t19-arabic-reading-index")})


class TwentiethFormalWorkTests(unittest.TestCase):
    """Exact source/work/section contracts, not semantic or proof acceptance."""
    GROUP = "experiments/orthemology-v5-successors/groups/t20-successor"
    EXPECTED = {
        "t20-church-probe": ("generic-church-probe", "T20-CHURCH-RAW-PROBE"),
        "t20-scalar-fusion": ("exact-scalar-fusion", "T20-SCALAR-FUSION-IFF"),
        "t20-hase-negative-routes": ("literal-HasE-written-negative-route", "T20-HASE-FURTHER-FAILED-ROUTES"),
        "t20-cnd-scope": ("CND-essential-independence-scope", "T20-CND-ESSENTIALITY-SCOPE"),
        "t20-modal-union": ("modal-union-v2", "T20-MODAL-CROSSING-COMPLETENESS"),
        "t20-ground-extension": ("existential-ground", "T20-ORIGINAL-GROUND-ROBUSTNESS"),
        "t20-grounded-support": ("grounded-attestation", "T20-GROUNDED-CONTINUATION-SUPPORT"),
    }

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("twentieth_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        cls.cross = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json").read_text())
        cls.works = {w["key"]: w for w in cls.cross["works"]}
        cls.claims = {r["id"]: r for r in json.loads((ROOT / cls.GROUP / "CLAIM_MAP.json").read_text())["results"]}
        cls.sources = json.loads((ROOT / cls.GROUP / "SOURCE_INDEX.json").read_text())["selected_sources"]
        cls.by_id = {s["id"]: s for s in cls.sources}

    def work(self, key):
        self.assertTrue(key in self.works, "Missing substantive work: " + key)
        return self.works[key]

    def targets(self, key):
        rel, anchor = self.work(key)["catalogue_entry"].split("#", 1)
        idx = self.mod.markdown_index((ROOT / rel).read_text())
        h = next((h for h in idx["headings"] if h[0] == anchor), None)
        self.assertIsNotNone(h, key)
        _, level, start = h
        end = next((h[2] for h in idx["headings"] if h[2] > start and h[1] <= level), idx["line_count"])
        return {t for line, href in idx["links"] if start <= line < end
                if (t := self.mod.resolve_reader_link(ROOT, rel, href)) is not None}

    def test_seven_distinct_works_preserve_declared_result_owners(self):
        for key, (component, result_id) in self.EXPECTED.items():
            with self.subTest(work=key):
                w = self.work(key)
                self.assertEqual(w.get("existing_result_ids", []), [result_id] if result_id else [])
                self.assertNotIn("scientific_status", w)
                self.assertNotEqual(w["role"], "application-proposal")

    def test_every_declared_component_is_attached_without_extra_work_credit(self):
        for key, (component, _) in self.EXPECTED.items():
            with self.subTest(work=key):
                w = self.work(key)
                actual = {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}
                expected = {s["public_path"] for s in self.sources if s["component"] == component}
                self.assertTrue(expected <= actual, "Missing source component: " + key)

    def test_original_result_evidence_and_direct_reading_routes_survive(self):
        for key, (_, result_id) in self.EXPECTED.items():
            with self.subTest(work=key):
                w = self.work(key); targets = self.targets(key)
                self.assertIn((self.GROUP + "/README.md", ""), targets)
                for source in w["source_keys"]:
                    self.assertTrue(any(p == self.cross["sources"][source]["path"] for p, _ in targets), key)
                if result_id:
                    paths = {self.cross["sources"][k]["path"] for k in w["source_keys"] + w.get("supporting_source_keys", [])}
                    self.assertTrue({self.by_id[k]["public_path"] for k in self.claims[result_id]["source_ids"]} <= paths)

    def test_scientific_owner_not_local_expectation_defines_result_registration(self):
        for key, (component, _) in self.EXPECTED.items():
            with self.subTest(work=key):
                source_ids = {r["id"] for r in self.sources if r["component"] == component}
                declared = {r["id"] for r in self.claims.values() if source_ids.intersection(r.get("source_ids", []))}
                self.assertEqual(set(self.work(key).get("existing_result_ids", [])), declared)

    def test_fixed_witness_and_negative_route_have_different_source_sections(self):
        self.assertIn("exact-statement", {a for p, a in self.targets("t20-scalar-fusion")})
        self.assertIn("what-each-direction-does", {a for p, a in self.targets("t20-scalar-fusion")})
        self.assertIn("route-one-fixed-proof-syntax-does-not-give-introduction-inversion", {a for p, a in self.targets("t20-hase-negative-routes")})
        self.assertIn("result-of-this-pass", {a for p, a in self.targets("t20-hase-negative-routes")})




class TwentiethRemainingFamilyTests(unittest.TestCase):
    """The original finite selection, not catalogue totals, defines this unit.

    These are source/role/route regression checks, not independent scholarly
    review, theorem replay, or a certificate for the later reader addenda.
    """
    GROUP = TwentiethFormalWorkTests.GROUP
    EXPECTED = {
        "t20-original-bearer-bridge": ("original-bearer-bridge", "research-note"),
        "t20-anchored-source-bridge": ("anchored-source-bridge", "research-note"),
        "t20-veracity-dependencies": ("veracity-boundary", "research-note"),
        "t20-same-bearer-joint-model": ("joint-foundational-model", "research-note"),
        "t20-copied-trace-observation": ("math122-observation-controls", "research-note"),
        "t20-external-transfer-assessment": ("openai-corpus-transfer-synthesis", "review"),
        "t20-foundational-synthesis": ("foundational-final-synthesis", "synthesis"),
        "t20-premise-dependency-map": ("foundational-dependency-dag", "supporting-reference"),
        "t20-prior-formal-reuse": ("foundational-prior-formal-reuse", "supporting-reference"),
    }
    setUpClass = classmethod(TwentiethFormalWorkTests.setUpClass.__func__)
    work = TwentiethFormalWorkTests.work
    targets = TwentiethFormalWorkTests.targets

    def test_each_remaining_source_family_has_its_substantive_role(self):
        for key, (component, role) in self.EXPECTED.items():
            with self.subTest(work=key):
                work = self.work(key)
                self.assertEqual(work["role"], role)
                self.assertNotIn("scientific_status", work)
                ids = {r["id"] for r in self.sources if r["component"] == component}
                owned = {r["id"] for r in self.claims.values() if ids.intersection(r.get("source_ids", []))}
                self.assertEqual(set(work.get("existing_result_ids", [])), owned)

    def test_complete_frozen_selection_is_attached_without_new_paper_per_file(self):
        keys = set(self.EXPECTED) | set(TwentiethFormalWorkTests.EXPECTED)
        components = {v[0] for v in self.EXPECTED.values()} | {v[0] for v in TwentiethFormalWorkTests.EXPECTED.values()}
        self.assertEqual(components, {s["component"] for s in self.sources})
        attached = set()
        for key in sorted(keys):
            work = self.work(key)
            paths = {self.cross["sources"][s]["path"] for s in work["source_keys"] + work.get("supporting_source_keys", [])}
            component = (self.EXPECTED.get(key) or TwentiethFormalWorkTests.EXPECTED[key])[0]
            self.assertTrue({s["public_path"] for s in self.sources if s["component"] == component} <= paths, key)
            attached.update(paths)
        self.assertTrue({s["public_path"] for s in self.sources} <= attached)
        self.assertEqual(set(self.claims), set().union(*(set(self.work(k).get("existing_result_ids", [])) for k in keys)))

    def test_primary_arguments_have_real_direct_section_and_evidence_routes(self):
        for key in self.EXPECTED:
            with self.subTest(work=key):
                work = self.work(key)
                targets = self.targets(key)
                self.assertIn((self.GROUP + "/README.md", ""), targets)
                primary = {self.cross["sources"][s]["path"] for s in work["source_keys"]}
                self.assertTrue(primary <= {p for p, _ in targets}, key)
                self.assertTrue(any(p in primary and anchor for p, anchor in targets), "No substantive section: " + key)
                support = {self.cross["sources"][s]["path"] for s in work.get("supporting_source_keys", [])}
                self.assertTrue(support.intersection(p for p, _ in targets), "No support/evidence route: " + key)

    def test_each_original_result_retains_its_exact_source_evidence(self):
        for key in self.EXPECTED:
            with self.subTest(work=key):
                work = self.work(key)
                paths = {self.cross["sources"][s]["path"] for s in work["source_keys"] + work.get("supporting_source_keys", [])}
                for result_id in work.get("existing_result_ids", []):
                    self.assertTrue({self.by_id[s]["public_path"] for s in self.claims[result_id]["source_ids"]} <= paths, result_id)


class RootNavigationAndMaintenanceTests(unittest.TestCase):
    """Real three-root routes and negative controls, without a corpus rescan.

    Text mutations are in-memory fixtures. No scientific owner is edited by
    these tests and link resolution still uses the actual checkout.
    """
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("root_reader_under_test", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        evidence = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.owners = json.loads((evidence / "OWNER-MAP.json").read_text())
        cls.cross = json.loads((evidence / "CROSSWALK.json").read_text())
        cls.texts = {p: (ROOT / p).read_text() for p in
                     ("README.md", "STATUS.md", "CONTRIBUTING.md")}

    def errors(self, texts=None):
        self.assertTrue(hasattr(self.mod, "check_root_navigation"),
                        "root routes and inherited-policy controls are absent")
        return self.mod.check_root_navigation(ROOT, self.owners, self.cross,
                                              texts=texts or self.texts)

    def mutated(self, path, old, new):
        self.assertIn(old, self.texts[path], "mutation must actually change the root")
        texts = dict(self.texts)
        texts[path] = texts[path].replace(old, new, 1)
        return texts

    def reject(self, texts, prefix):
        errors = self.errors(texts)
        self.assertTrue(any(e.startswith(prefix + ":") for e in errors), errors)

    def test_three_roots_supply_real_research_and_maintenance_routes(self):
        self.assertEqual(self.errors(), [])

    def test_six_distinct_reader_destinations_not_six_valid_wrong_links(self):
        for name in self.mod.READER_PAGES:
            if name == "VERIFICATION-GUIDE.md":
                wrong = "RESEARCH-ATLAS.md"
            else:
                wrong = "VERIFICATION-GUIDE.md"
            with self.subTest(page=name):
                texts = self.mutated("README.md", "(docs/reader/" + name + ")",
                                     "(docs/reader/" + wrong + ")")
                self.reject(texts, "root-route")

    def test_fenced_link_decoy_does_not_restore_the_missing_route(self):
        texts = self.mutated("README.md", "(docs/reader/RESULT-INDEX.md)",
                             "(docs/reader/PAPER-CATALOGUE.md)")
        texts["README.md"] += "\n```md\n[decoy](docs/reader/RESULT-INDEX.md)\n```\n"
        self.reject(texts, "root-route")

    def test_exact_source_section_is_not_replaced_by_an_existing_wrong_anchor(self):
        texts = self.mutated("README.md", "examples/compaction-stale-steer.md#3-five-predicates-that-must-not-be-collapsed",
                             "examples/compaction-stale-steer.md#1-the-pattern")
        self.reject(texts, "root-example")

    def test_generated_example_marker_is_not_hand_edited(self):
        texts = self.mutated("README.md", "<!-- state:example-json-count -->nine",
                             "<!-- state:example-json-count -->ten")
        self.reject(texts, "root-state")

    def test_generated_lane_block_is_not_erased_or_duplicated(self):
        marker = "<!-- state:claim-status-by-lane -->"
        self.reject(self.mutated("STATUS.md", marker, ""), "root-state")
        self.reject(self.mutated("STATUS.md", marker, marker + "\n" + marker), "root-state")

    def test_historical_snapshots_do_not_precede_the_research_entrance(self):
        texts = dict(self.texts)
        readme = texts["README.md"]
        self.assertIn("## Integration history", readme)
        start = readme.index("## Integration history")
        texts["README.md"] = readme[start:] + "\n" + readme[:start]
        self.reject(texts, "root-order")

    def test_inherited_contributor_policy_cannot_be_changed_with_navigation(self):
        texts = self.mutated("CONTRIBUTING.md", "No force-pushes to `main`.",
                             "Force-pushes to `main` are permitted.")
        self.reject(texts, "root-policy")

    def test_absent_and_machine_local_links_are_rejected(self):
        for target in ("fixture-missing-reader-root.md", "file:///fixture-private-note"):
            with self.subTest(target=target):
                texts = self.mutated("README.md", "(docs/reader/RESULT-INDEX.md)",
                                     "(" + target + ")")
                self.reject(texts, "root-link")

    def test_contributor_admission_is_exact_path_and_preserves_original_bytes(self):
        self.assertTrue(hasattr(self.mod, "permitted_contributor_navigation"))
        base = self.owners["baseline"]["commit"]
        oid = subprocess.check_output(["git", "rev-parse", base + ":CONTRIBUTING.md"],
                                      cwd=ROOT).decode().strip()
        row = {"path": "CONTRIBUTING.md", "git_oid": oid}
        body = self.texts["CONTRIBUTING.md"].encode()
        self.assertTrue(self.mod.permitted_contributor_navigation(ROOT, row, body))
        self.assertFalse(self.mod.permitted_contributor_navigation(
            ROOT, dict(row, path="fixture-other-policy.md"), body))
        self.assertFalse(self.mod.permitted_contributor_navigation(
            ROOT, row, body.replace(b"No force-pushes", b"Permit force-pushes")))


class MaintenanceFootprintTests(unittest.TestCase):
    """M01--M05 execute changes in disposable repositories, never real science.

    Receipts count independent edits, not test functions. The rendering bodies
    are explicit synthetic stand-ins; no PDF build or scientific replay is
    inferred. Semantic review remains separate from these mechanical checks.
    """
    git = ReaderPilotTests.git
    reject = ReaderPilotTests.reject
    EVIDENCE = 'docs/project-closure/reader-refactor-issue-35/'
    OWNER_FILE = EVIDENCE + 'OWNER-MAP.json'
    CROSS_FILE = EVIDENCE + 'CROSSWALK.json'
    CATALOGUE = 'docs/reader/PAPER-CATALOGUE.md'
    ATLAS = 'docs/reader/RESEARCH-ATLAS.md'
    LOOKUP = 'docs/reader/RESULT-INDEX.md'
    RESULT_OWNER = 'fixture-theory/result-owner.json'

    def setUp(self):
        ReaderPilotTests.setUp(self)
        self.results = {'results': [{'id': 'fixture-R1', 'title': 'Scoped fixture',
                                   'source': 'fixture-theory/note.md#note'}]}
        self.write(self.RESULT_OWNER, json.dumps(self.results, indent=2) + '\n')
        self.git('add', self.RESULT_OWNER)
        self.git('commit', '-qm', 'fixture result owner')
        self.owners['baseline']['commit'] = self.git('rev-parse', 'HEAD').strip()
        self.bind(self.RESULT_OWNER)
        group = self.owners['collections'][0]
        group['owners'].append(self.RESULT_OWNER)
        group['result_owner'] = self.RESULT_OWNER
        self.cross['works'][1]['existing_result_ids'] = ['fixture-R1']
        self.cross['collection_dispositions'] = {'fixture-theory': {
            'scope': 'Disposable maintenance fixture only.',
            'reading_record': 'Known synthetic statements and explicit exercise changes.',
            'basis_sources': ['fixture-theory/lineage.md', self.RESULT_OWNER],
            'result_owner': self.RESULT_OWNER,
            'result_routes': {'fixture-R1': ['note']},
            'items': [
                {'path': p, 'role': role, 'work': work} for p, role, work in (
                    ('fixture-theory/core.md', 'work-source', 'core'),
                    ('fixture-theory/multi.md', 'formal-component', 'core'),
                    ('fixture-theory/note.md', 'work-source', 'note'),
                    ('fixture-theory/related.tex', 'work-source', 'related'),
                    ('fixture-theory/edition.pdf', 'historical-edition', 'edition'),
                    ('fixture-theory/lineage.md', 'collection-guide', 'related'),
                    (self.RESULT_OWNER, 'provenance-record', 'note'),
                )],
        }}
        self.write(self.CATALOGUE,
                   '# Fixture catalogue\n\n## Composite core\n'
                   '[Core](../../fixture-theory/core.md#core) and '
                   '[component](../../fixture-theory/multi.md#multi).\n'
                   '[Rendering](../../artifacts/core.pdf).\n\n'
                   '## Substantive note\nA substantive work without a PDF.\n'
                   '[Source](../../fixture-theory/note.md#note).\n')
        self.write(self.ATLAS, '# Fixture atlas\n\n## Existing subject\n'
                   '[Substantive note](PAPER-CATALOGUE.md#substantive-note).\n')
        for name in ('CURRENT-FRONTIERS.md', 'APPLICATIONS.md', 'VERIFICATION-GUIDE.md'):
            self.write('docs/reader/' + name,
                       '# Distinct fixture reader\n'
                       '[Scoped original work](PAPER-CATALOGUE.md#substantive-note).\n')
        self.cross['reader_journeys'] = [
            {'id': 'J%02d' % i, 'entry': self.CATALOGUE + '#substantive-note',
             'source_keys': ['fixture-theory/note.md'],
             'source_fragments': {'fixture-theory/note.md': 'note'}}
            for i in range(1, 8)]
        self.persist()
        self.derive_lookup()
        self.assertEqual(self.check(), [])
        self.initial = self.snapshot()
        self.initial_work_count = len(self.cross['works'])
        self.observed_red = []

    def write(self, path, body):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding='utf-8')

    def append(self, path, body):
        self.write(path, (self.repo / path).read_text(encoding='utf-8') + body)

    def bind(self, path, scope='Synthetic fixture source; changed statement examined in exercise.'):
        self.cross['sources'][path] = {
            'path': path, 'sha256': hashlib.sha256((self.repo / path).read_bytes()).hexdigest(),
            'read_scope': scope}

    def persist(self):
        self.write(self.OWNER_FILE, json.dumps(self.owners, indent=2) + '\n')
        self.write(self.CROSS_FILE, json.dumps(self.cross, indent=2) + '\n')

    def readback(self):
        # Exercise the persisted owner files, not only transient Python objects.
        return (json.loads((self.repo / self.OWNER_FILE).read_text()),
                json.loads((self.repo / self.CROSS_FILE).read_text()))

    def check(self):
        owners, cross = self.readback()
        return self.mod.check(self.repo, owners, cross) + self.mod.check_reader_pages(self.repo, cross)

    def red(self, code):
        errors = self.check()
        self.reject(errors, code)
        self.observed_red.append(code)

    def reanchor(self, paths):
        # Only named fixture science is committed. Reader owners are not source
        # authorities and cannot become their own corpus digest inputs.
        self.git('add', '--', *paths)
        self.git('commit', '-qm', 'explicit finite fixture source admission')
        self.owners['baseline']['commit'] = self.git('rev-parse', 'HEAD').strip()
        for path in paths:
            self.bind(path)

    def derive_lookup(self):
        # Read the actual fixture result owner. Do not copy status judgements
        # into five prose surfaces; the original statement remains one owner.
        original = json.loads((self.repo / self.RESULT_OWNER).read_text())
        routes = self.cross['collection_dispositions']['fixture-theory']['result_routes']
        lines = ['# Fixture result lookup', '']
        for row in original['results']:
            self.assertIn(row['id'], routes)
            lines.append('**' + row['id'] + '** [' + row['title'] + '](../../' +
                         row['source'] + '); work `' + routes[row['id']][0] + '`.')
        self.write(self.LOOKUP, '\n'.join(lines) + '\n')

    def snapshot(self):
        return {p.relative_to(self.repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.repo.rglob('*') if p.is_file()
                and '.git' not in p.relative_to(self.repo).parts}

    def record(self, exercise, expected, facts, edited_sections, generated=(), limitations=()):
        self.persist()
        self.assertEqual(self.check(), [])
        after = self.snapshot()
        changed = sorted(p for p in set(self.initial) | set(after)
                         if self.initial.get(p) != after.get(p))
        self.assertEqual(set(changed), set(expected), 'Unexpected maintenance footprint')
        before_check = self.snapshot()
        self.assertEqual(self.check(), [])
        self.assertEqual(self.snapshot(), before_check, 'Validation must remain read-only')
        # A second projection from the unchanged result owner must converge.
        before_lookup = (self.repo / self.LOOKUP).read_bytes()
        self.derive_lookup()
        self.assertEqual((self.repo / self.LOOKUP).read_bytes(), before_lookup)
        receipt = {
            'exercise': exercise, 'scope': 'executed disposable fixture; not real scientific change',
            'independent_facts': facts, 'manually_edited_sections': edited_sections,
            'changed_files': changed, 'derived_outputs': list(generated),
            'unchanged_reader_pages': sorted('docs/reader/' + p for p in self.mod.READER_PAGES
                                             if 'docs/reader/' + p not in changed),
            'observed_rejections': self.observed_red,
            'checks': ['persisted owner/source/publication check', 'six-page real-link check',
                       'seven fixture source routes', 'exact file footprint',
                       'read-only validation', 'second lookup generation byte equality'],
            'work_count_before': self.initial_work_count,
            'work_count_after': len(self.cross['works']),
            'before_changed_sha256': {p: self.initial.get(p) for p in changed},
            'after_changed_sha256': {p: after.get(p) for p in changed},
            'limitations': list(limitations), 'outcome': 'PASS'}
        print('MAINTENANCE_RECEIPT ' + json.dumps(receipt, sort_keys=True))

    def test_m01_existing_work_adds_one_rendering_not_another_paper(self):
        profile = 'fixture-docs/profile.yaml'
        edition = 'artifacts/core-second.pdf'
        self.append(profile, '- artifact_id: core-second\n'
                    '  sources: [fixture-theory/core.md, fixture-theory/multi.md]\n'
                    '  profile_kind: technical-paper\n')
        self.write(edition, 'synthetic second governed rendering, not a real PDF')
        self.git('add', profile, edition)
        self.red('corpus-currentness')
        self.reanchor([profile, edition])
        self.persist()
        self.red('artifact')
        self.cross['works'][0]['reading_forms'] = [
            {'source': 'artifacts/core.pdf', 'relationship': 'governed-rendering'},
            {'source': edition, 'artifact_id': 'core-second', 'relationship': 'governed-rendering'}]
        self.append(self.CATALOGUE, '\n## Additional core reading form\n'
                    '[Second rendering](../../artifacts/core-second.pdf). Same composite work.\n')
        self.assertEqual(len(self.cross['works']), self.initial_work_count)
        self.record('M01', [profile, edition, self.OWNER_FILE, self.CROSS_FILE, self.CATALOGUE],
                    ['one governed edition of the existing composite with unchanged component owners'],
                    {profile: ['artifact binding'], self.CROSS_FILE: ['one work reading_forms; source bindings'],
                     self.OWNER_FILE: ['finite fixture source admission'],
                     self.CATALOGUE: ['additional reading form']},
                    limitations=['Rendering bytes are an explicit stand-in; this exercise is not a PDF rebuild.'])

    def test_m02_result_owner_changes_lookup_and_only_affected_synopsis(self):
        source = 'fixture-theory/note.md'
        self.append(source, '\n## Added scope\nA new synthetic bound requires n at least two.\n')
        self.results['results'].append({'id': 'fixture-R2', 'title': 'Additional scoped bound',
                                       'source': source + '#added-scope'})
        self.write(self.RESULT_OWNER, json.dumps(self.results, indent=2) + '\n')
        self.red('result-routes')
        self.red('source-drift')
        self.reanchor([source, self.RESULT_OWNER])
        self.cross['collection_dispositions']['fixture-theory']['result_routes']['fixture-R2'] = ['note']
        self.cross['works'][1]['existing_result_ids'].append('fixture-R2')
        self.append(self.CATALOGUE, '\n## Additional note result\n'
                    '[Scoped extension](../../fixture-theory/note.md#added-scope) requires n at least two.\n')
        self.derive_lookup()
        self.record('M02', [source, self.RESULT_OWNER, self.OWNER_FILE, self.CROSS_FILE,
                            self.CATALOGUE, self.LOOKUP],
                    ['one additional scoped result inside the existing note and subject'],
                    {source: ['new statement and its hypothesis'], self.RESULT_OWNER: ['new result record'],
                     self.OWNER_FILE: ['finite fixture source admission'],
                     self.CROSS_FILE: ['existing work result route; changed source bindings'],
                     self.CATALOGUE: ['affected synopsis addendum only']}, generated=[self.LOOKUP])

    def test_m03_new_non_pdf_work_is_detected_then_admitted_once(self):
        source = 'fixture-unexpected/substantive-note.unbuilt'
        self.write(source, '# Fixture outside paper roots\nA synthetic substantive construction.\n')
        self.git('add', source)
        self.red('corpus-currentness')
        self.reanchor([source])
        self.persist()
        self.red('unassigned-source')
        self.owners['collections'].append({'key': 'fixture-unexpected', 'include': ['fixture-unexpected/'],
                                          'exclude': [], 'owners': [source]})
        self.owners['required_work_sources'].append(source)
        self.persist()
        self.red('missing-work')
        self.cross['works'].append({'key': 'new-note', 'title': 'New fixture note',
                                   'role': 'research-note', 'source_keys': [source]})
        self.append(self.CATALOGUE, '\n## New fixture note\n'
                    '[Original construction](../../fixture-unexpected/substantive-note.unbuilt).\n')
        self.append(self.ATLAS, '\n[New work in this subject](PAPER-CATALOGUE.md#new-fixture-note).\n')
        self.assertEqual(len(self.cross['works']), self.initial_work_count + 1)
        self.record('M03', [source, self.OWNER_FILE, self.CROSS_FILE, self.CATALOGUE, self.ATLAS],
                    ['one substantive non-PDF work in a previously unknown root'],
                    {source: ['new source'], self.OWNER_FILE: ['new finite collection and required source'],
                     self.CROSS_FILE: ['one new work and source'], self.CATALOGUE: ['new work synopsis'],
                     self.ATLAS: ['existing subject link to the new contribution']})

    def test_m04_repeated_checkpoint_bodies_keep_aliases_not_new_work_credit(self):
        prefix = 'fixture-checkpoint/'
        copies = {'core-copy.md': ('fixture-theory/core.md', 'core'),
                  'note-copy.md': ('fixture-theory/note.md', 'note')}
        for filename, (original, _) in copies.items():
            self.write(prefix + filename, (self.repo / original).read_text())
        source = prefix + 'new-item.md'
        index = prefix + 'INDEX.json'
        self.write(source, '# Checkpoint addition\nOne genuinely new synthetic work.\n')
        aliases = [{'path': prefix + filename, 'original': original, 'work': work}
                   for filename, (original, work) in copies.items()]
        self.write(index, json.dumps({'retained_aliases': aliases, 'new_items': [source]}, indent=2) + '\n')
        paths = [index, source] + [a['path'] for a in aliases]
        self.git('add', *paths)
        self.red('corpus-currentness')
        self.reanchor(paths)
        self.owners['collections'].append({'key': 'fixture-checkpoint', 'include': [prefix],
                                          'exclude': [], 'owners': [index]})
        self.owners['required_work_sources'].append(source)
        self.cross['works'].append({'key': 'checkpoint-addition', 'title': 'Checkpoint addition',
                                   'role': 'research-note', 'source_keys': [source]})
        for a in aliases:
            self.assertEqual((self.repo / a['path']).read_bytes(), (self.repo / a['original']).read_bytes())
            work = next(w for w in self.cross['works'] if w['key'] == a['work'])
            work.setdefault('supporting_source_keys', []).append(a['path'])
            self.cross['relations'].append({'from': a['original'], 'to': a['path'],
                                           'kind': 'retained-provenance-alias', 'basis': index})
        self.cross['collection_dispositions']['fixture-checkpoint'] = {
            'scope': 'Known copies plus one addition; no extra independent-evidence credit.',
            'reading_record': 'Exact fixture alias index, body comparison and new item examined.',
            'basis_sources': [index],
            'items': [{'path': a['path'], 'role': 'historical-edition', 'work': a['work']} for a in aliases]
                     + [{'path': source, 'role': 'work-source', 'work': 'checkpoint-addition'},
                        {'path': index, 'role': 'provenance-record', 'work': 'checkpoint-addition'}]}
        self.append(self.CATALOGUE, '\n## Checkpoint addition\n'
                    '[New item](../../fixture-checkpoint/new-item.md#checkpoint-addition); '
                    '[retained aliases](../../fixture-checkpoint/INDEX.json) remain with their old works.\n')
        self.persist()
        valid = deepcopy(self.cross)
        self.cross['collection_dispositions']['fixture-checkpoint']['items'].pop(0)
        self.persist()
        self.red('collection-coverage')
        self.cross = valid
        self.assertEqual(len(self.cross['works']), self.initial_work_count + 1)
        self.assertEqual(len(json.loads((self.repo / index).read_text())['retained_aliases']), 2)
        self.record('M04', paths + [self.OWNER_FILE, self.CROSS_FILE, self.CATALOGUE],
                    ['checkpoint contains two explicitly identified copied bodies and one new work'],
                    {index: ['two retained provenance aliases and one addition'],
                     self.OWNER_FILE: ['finite checkpoint admission'],
                     self.CROSS_FILE: ['existing-work copy attachments; one new work; complete dispositions'],
                     self.CATALOGUE: ['new item and provenance route']},
                    limitations=['Work equivalence uses the explicit fixture provenance owner, not byte equality alone.'])

    def test_m05_source_change_blocks_stale_synopsis_until_explicit_review(self):
        source = 'fixture-theory/note.md'
        old = (self.repo / source).read_text()
        corrected = old.replace('A substantive work without a PDF.',
                                'A corrected synthetic claim holds only for nonempty inputs.')
        self.assertNotEqual(old, corrected)
        self.write(source, corrected)
        self.red('source-drift')
        before_refresh = self.snapshot()
        self.derive_lookup()
        self.persist()
        self.assertEqual(self.snapshot(), before_refresh,
                         'Lookup regeneration cannot inspect or repair the changed synopsis')
        self.red('source-drift')
        # A manual hash-only change still cannot evade the independent source pin.
        self.bind(source)
        self.persist()
        self.red('baseline-source')
        self.reanchor([source])
        self.bind(source, 'Reviewed corrected synthetic statement: only nonempty inputs; note synopsis updated.')
        body = (self.repo / self.CATALOGUE).read_text()
        self.assertIn('A substantive work without a PDF.', body)
        self.write(self.CATALOGUE, body.replace('A substantive work without a PDF.',
                                                'The corrected fixture claim requires nonempty inputs.'))
        self.record('M05', [source, self.OWNER_FILE, self.CROSS_FILE, self.CATALOGUE],
                    ['one corrected supporting statement narrows the note to nonempty inputs'],
                    {source: ['corrected statement'], self.OWNER_FILE: ['explicit finite source readmission'],
                     self.CROSS_FILE: ['reviewed source binding and exact read scope'],
                     self.CATALOGUE: ['the affected synopsis, not every subject page']},
                    limitations=['Mechanical identity checks cannot authenticate a dishonest claim of reading; C05 must review fidelity.'])



class LateTwentiethContextRoutesTests(unittest.TestCase):
    """The original context selection and result owner define this finite unit.

    Source routes and preserved roles are testable; philosophical warrant,
    historical authentication and independent C05 acceptance are not inferred.
    """
    GROUP = TwentiethFormalWorkTests.GROUP
    EXPECTED = {
        "t20-cooperation-context": (
            "synthesis", {"cooperation", "warrant-review", "scope"},
            ["t20/cooperation-reassessment/SOURCE_ARGUMENT.md",
             "t20/cooperation-reassessment/MODEL_AUDIT.md",
             "t20/cooperation-reassessment/ROOT_REASSESSMENT.md"]),
        "t20-emergence-type-control": (
            "research-note", {"ontology"},
            ["t20/ontology-type-control/AUDIT.md",
             "t20/ontology-type-control/OriginationTypeControl.lean"]),
        "t20-divine-action-context": (
            "review", {"causal-action", "uthaymin"},
            ["t20/targeted-final-loci/causal-action/LOCUS_AUDIT.md",
             "t20/targeted-final-loci/uthaymin/LOCUS_AUDIT.md"]),
    }

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("late_twentieth_routes", MODULE)
        cls.mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.mod)
        directory = ROOT / "docs/project-closure/reader-refactor-issue-35"
        cls.cross = json.loads((directory / "CROSSWALK.json").read_text())
        owners = json.loads((directory / "OWNER-MAP.json").read_text())
        def original(path):
            return json.loads(subprocess.check_output(
                ["git", "show", owners["baseline"]["commit"] + ":" + path], cwd=ROOT))
        cls.selected = original(cls.GROUP + "/CONTEXT_SOURCE_INDEX.json")["public_sources"]
        cls.aliases = {s["owner_archive_path"]: s for s in cls.selected}
        cls.claims = {r["id"]: r for r in original("docs/provenance/v5-successors/RESULT_STATUS.json")["results"]}
        cls.source_rows = {r["id"]: r for r in original("docs/provenance/v5-successors/SOURCE_MAP.json")["sources"]}
        cls.text = (ROOT / "docs/reader/PAPER-CATALOGUE.md").read_text()

    def errors(self, cross, text):
        errors = []
        works = {w["key"]: w for w in cross["works"]}
        idx = self.mod.markdown_index(text)
        for key, (role, parts, primaries) in self.EXPECTED.items():
            w = works.get(key)
            if not w:
                errors.append("missing-work:" + key); continue
            if w["role"] != role:
                errors.append("role:" + key)
            attached = {cross["sources"][s]["path"] for s in w["source_keys"] + w.get("supporting_source_keys", [])}
            expected = {s["public_path"] for s in self.selected if s["part"] in parts}
            if not expected <= attached:
                errors.append("context-coverage:" + key)
            rel, _, anchor = w.get("catalogue_entry", "").partition("#")
            h = next((h for h in idx["headings"] if h[0] == anchor), None)
            if rel != "docs/reader/PAPER-CATALOGUE.md" or h is None:
                errors.append("entry:" + key); continue
            _, level, start = h
            end = next((v[2] for v in idx["headings"] if v[2] > start and v[1] <= level), idx["line_count"])
            targets = {t for line, href in idx["links"] if start <= line < end
                       if (t := self.mod.resolve_reader_link(ROOT, rel, href)) is not None}
            for alias in primaries:
                path = self.aliases[alias]["public_path"]
                if path not in {cross["sources"][s]["path"] for s in w["source_keys"]}:
                    errors.append("primary:" + alias)
                if path not in {p for p, _ in targets}:
                    errors.append("source-route:" + alias)
            if not any(a for p,a in targets if p in {self.aliases[n]["public_path"] for n in primaries}):
                errors.append("section:" + key)
            if (self.GROUP + "/CONTEXT_SOURCE_INDEX.json", "") not in targets:
                errors.append("context-owner:" + key)
        return errors

    def test_late_context_and_typed_control_are_not_hidden_in_old_component_routes(self):
        self.assertEqual(self.errors(self.cross, self.text), [])

    def test_removing_a_late_work_preserves_links_but_fails_coverage(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for key in self.EXPECTED:
            altered = deepcopy(self.cross)
            altered["works"] = [w for w in altered["works"] if w["key"] != key]
            self.assertIn("missing-work:" + key, self.errors(altered, self.text))

    def test_existing_wrong_source_and_dropped_context_support_are_rejected(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for key, (_, parts, primary) in self.EXPECTED.items():
            path = self.aliases[primary[0]]["public_path"]
            wrong = self.aliases[next(v[2][0] for k,v in self.EXPECTED.items() if k != key)]["public_path"]
            changed = self.text.replace("../../" + path, "../../" + wrong)
            self.assertNotEqual(changed, self.text)
            self.assertIn("source-route:" + primary[0], self.errors(self.cross, changed))
            altered = deepcopy(self.cross)
            work = next(w for w in altered["works"] if w["key"] == key)
            work["supporting_source_keys"] = []
            self.assertIn("context-coverage:" + key, self.errors(altered, self.text))

    def test_late_result_keeps_original_formal_evidence_and_distinct_current_context(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        work = next(w for w in self.cross["works"] if w["key"] == "t20-emergence-type-control")
        result_id = "T20-EMERGENCE-TYPE-CONTROL"
        self.assertEqual(work["existing_result_ids"], [result_id])
        paths = {self.cross["sources"][s]["path"] for s in work["source_keys"] + work.get("supporting_source_keys", [])}
        required = {self.source_rows[s]["public_path"] for s in self.claims[result_id]["source_ids"]}
        self.assertTrue(required <= paths)
        for role, parts, primaries in self.EXPECTED.values():
            for alias in primaries:
                self.assertTrue(any(self.cross["sources"][s]["path"] == self.aliases[alias]["public_path"]
                                    for w in self.cross["works"] for s in w["source_keys"]))
        # No owner-only DOCX is smuggled into the declared public reading forms.
        for w in self.cross["works"]:
            if w["key"] in self.EXPECTED:
                self.assertTrue(all(not self.cross["sources"][s]["path"].endswith(".docx") for s in w["source_keys"]))


class MethodologyRoutesMixin:
    """Original selection, native reader routes and support/credit boundaries.

    Family classes supply their exact aliases and verification section. This
    reuses the Arabic controls without inferring scholarly truth from prose.
    """
    GROUP = TwentiethFormalWorkTests.GROUP
    ADDITIONAL_READING_ALIASES = ()
    setUpClass = classmethod(LateTwentiethContextRoutesTests.setUpClass.__func__)

    def errors(self, cross, text):
        errors = LateTwentiethContextRoutesTests.errors(self, cross, text)
        work = next((w for w in cross["works"] if w["key"] == self.KEY), None)
        if work is None:
            return errors
        if work.get("existing_result_ids") != []:
            errors.append("methodology-result-credit")
        primaries = {self.aliases[a]["public_path"] for a in self.PRIMARY_ALIASES}
        forms = {cross["sources"][f["source"]]["path"]
                 for f in work.get("reading_forms", [])}
        if {cross["sources"][s]["path"] for s in work["source_keys"]} != primaries:
            errors.append("methodology-primary-components")
        expected_forms = primaries | {self.aliases[a]["public_path"]
                                      for a in self.ADDITIONAL_READING_ALIASES}
        if forms != expected_forms:
            errors.append("methodology-reading-forms")
        attached = {cross["sources"][s]["path"]: cross["sources"][s]
                    for s in work["source_keys"] + work.get("supporting_source_keys", [])}
        for row in self.selected:
            if row["part"] == self.PART and row["public_path"] in attached:
                if attached[row["public_path"]]["sha256"] != row["public_sha256"]:
                    errors.append("methodology-source-identity:" + row["owner_archive_path"])
        return errors

    def test_complete_methodology_family_has_native_primary_and_support_routes(self):
        self.assertEqual(self.errors(self.cross, self.text), [])

    def test_missing_reference_or_promotion_to_a_new_result_is_rejected(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        altered = deepcopy(self.cross)
        altered["works"] = [w for w in altered["works"] if w["key"] != self.KEY]
        self.assertIn("missing-work:" + self.KEY, self.errors(altered, self.text))
        for field, value, error in [
                ("role", "research-note", "role:" + self.KEY),
                ("existing_result_ids", ["T20-CHURCH-RAW-PROBE"], "methodology-result-credit")]:
            with self.subTest(field=field):
                altered = deepcopy(self.cross)
                work = next(w for w in altered["works"] if w["key"] == self.KEY)
                self.assertNotEqual(work[field], value)
                work[field] = value
                self.assertIn(error, self.errors(altered, self.text))

    def test_each_support_component_and_its_public_identity_are_required(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for row in self.selected:
            if row["part"] != self.PART or row["owner_archive_path"] in self.PRIMARY_ALIASES:
                continue
            with self.subTest(alias=row["owner_archive_path"]):
                altered = deepcopy(self.cross)
                work = next(w for w in altered["works"] if w["key"] == self.KEY)
                key = next(s for s in work["supporting_source_keys"]
                           if altered["sources"][s]["path"] == row["public_path"])
                work["supporting_source_keys"].remove(key)
                self.assertIn("context-coverage:" + self.KEY, self.errors(altered, self.text))
                work["source_keys"].append(key)
                self.assertIn("methodology-primary-components", self.errors(altered, self.text))
                altered = deepcopy(self.cross)
                self.assertNotEqual(altered["sources"][key]["sha256"], "0" * 64)
                altered["sources"][key]["sha256"] = "0" * 64
                self.assertIn("methodology-source-identity:" + row["owner_archive_path"],
                              self.errors(altered, self.text))

    def test_existing_json_cannot_replace_the_narrative_reading_route(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for alias in self.PRIMARY_ALIASES:
            with self.subTest(alias=alias):
                path = self.aliases[alias]["public_path"]
                companion = getattr(self, "NARRATIVE_COMPANIONS", {}).get(
                    alias, alias.removesuffix(".md") + ".json")
                wrong = self.aliases[companion]["public_path"]
                changed = self.text.replace("../../" + path, "../../" + wrong)
                self.assertNotEqual(changed, self.text)
                self.assertIn("source-route:" + alias, self.errors(self.cross, changed))
                altered = deepcopy(self.cross)
                work = next(w for w in altered["works"] if w["key"] == self.KEY)
                source_key = next(s for s in work["supporting_source_keys"]
                                  if altered["sources"][s]["path"] == wrong)
                work["reading_forms"][0]["source"] = source_key
                self.assertIn("methodology-reading-forms", self.errors(altered, self.text))

    def test_verification_route_reaches_the_method_and_original_context_owner(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        page = "docs/reader/VERIFICATION-GUIDE.md"
        text = (ROOT / page).read_text()
        heading = self.VERIFICATION_HEADING
        required = {
            (self.aliases[self.PRIMARY_ALIASES[0]]["public_path"], self.METHOD_ANCHOR),
            ("docs/reader/PAPER-CATALOGUE.md", self.CATALOGUE_ANCHOR),
            (self.GROUP + "/CONTEXT_SOURCE_INDEX.json", ""),
        }

        def reached(body):
            return self.section_targets(body, page, heading)

        self.assertTrue(required <= reached(text))
        path = self.aliases[self.PRIMARY_ALIASES[0]]["public_path"]
        changed = text.replace("../../" + path + "#" + self.METHOD_ANCHOR, "PAPER-CATALOGUE.md")
        self.assertNotEqual(changed, text)
        self.assertFalse(required <= reached(changed))


    def section_targets(self, text, page, heading):
        idx = self.mod.markdown_index(text)
        found = next((h for h in idx["headings"] if h[0] == heading), None)
        if found is None:
            return set()
        _, level, start = found
        end = next((h[2] for h in idx["headings"] if h[2] > start and h[1] <= level), idx["line_count"])
        return {t for line, href in idx["links"] if start <= line < end
                if (t := self.mod.resolve_reader_link(ROOT, page, href)) is not None}


class ArabicMethodologyRoutesTests(MethodologyRoutesMixin, unittest.TestCase):
    """The six-source Arabic audit stays one reference, not new proof credit."""
    PART = "arabic"
    KEY = "t20-arabic-reading-methodology"
    PRIMARY_ALIASES = [
        "t20/methodology/arabic/ARABIC_READING_METHOD.md",
        "t20/methodology/arabic/CROSS_STREAM_CASES.md",
    ]
    EXPECTED = {KEY: ("supporting-reference", {PART}, PRIMARY_ALIASES)}
    CATALOGUE_ANCHOR = "arabic-reading-methodology-and-source-formal-feedback"
    VERIFICATION_HEADING = "checking-what-a-source-reading-receipt-establishes"
    METHOD_ANCHOR = "reading-stages"


class DriveMethodologyRoutesTests(MethodologyRoutesMixin, unittest.TestCase):
    """Five audit projections connect inherited reading to existing owners."""
    PART = "drive"
    KEY = "t20-drive-corpus-methodology"
    PRIMARY_ALIASES = ["t20/methodology/drive/DRIVE_CORPUS.md"]
    EXPECTED = {KEY: ("supporting-reference", {PART}, PRIMARY_ALIASES)}
    CATALOGUE_ANCHOR = "six-supplied-drive-inputs-inherited-reading-and-t20-use"
    VERIFICATION_HEADING = "checking-the-six-input-drive-corpus-audit"
    METHOD_ANCHOR = "what-was-actually-read-and-revisited"

    def test_catalogue_exposes_support_and_existing_reading_result_owners(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        page = "docs/reader/PAPER-CATALOGUE.md"
        works = {w["key"]: w for w in self.cross["works"]}
        peers = ["t17-foundational-source-guide", "t20-original-bearer-bridge",
                 "t20-anchored-source-bridge", "t20-veracity-dependencies",
                 "t20-copied-trace-observation", "t20-foundational-synthesis",
                 "t20-cooperation-context"]
        required = {(page, works[k]["catalogue_entry"].split("#", 1)[1]) for k in peers}
        required |= {(r["public_path"], "") for r in self.selected
                     if r["part"] == self.PART and r["owner_archive_path"] not in self.PRIMARY_ALIASES}
        reached = lambda text: self.section_targets(text, page, self.CATALOGUE_ANCHOR)
        self.assertTrue(required <= reached(self.text))
        for path, anchor in required:
            with self.subTest(path=path, anchor=anchor):
                href = "#" + anchor if path == page else "../../" + path
                changed = self.text.replace("(" + href + ")", "(VERIFICATION-GUIDE.md)")
                self.assertNotEqual(changed, self.text)
                self.assertFalse(required <= reached(changed))


class ResultLedgerMethodologyRoutesTests(MethodologyRoutesMixin, unittest.TestCase):
    """The original fifteen-result handoff routes existing owners once each."""
    PART = "result-ledger"
    KEY = "t20-result-method-handoff"
    PRIMARY_ALIASES = ["t20/methodology/result-ledger/METHOD_INTEGRATION_HANDOFF.md"]
    LEDGER_ALIAS = "t20/methodology/result-ledger/RESULT_EVIDENCE_LEDGER.json"
    NARRATIVE_COMPANIONS = {PRIMARY_ALIASES[0]: LEDGER_ALIAS}
    EXPECTED = {KEY: ("supporting-reference", {PART}, PRIMARY_ALIASES)}
    CATALOGUE_ANCHOR = "the-original-fifteen-result-evidence-and-method-handoff"
    VERIFICATION_HEADING = "checking-original-result-credit-and-receiving-execution"
    METHOD_ANCHOR = "receiving-and-finalisation-boundary"
    OWNER_WORKS = {
        "T20-CHURCH-RAW-PROBE": "t20-church-probe",
        "T20-CND-ESSENTIALITY-SCOPE": "t20-cnd-scope",
        "T20-SCALAR-FUSION-IFF": "t20-scalar-fusion",
        "T20-MODAL-CROSSING-COMPLETENESS": "t20-modal-union",
        "T20-ORIGINAL-GROUND-ROBUSTNESS": "t20-ground-extension",
        "T20-GROUNDED-CONTINUATION-SUPPORT": "t20-grounded-support",
        "T20-HASE-FURTHER-FAILED-ROUTES": "t20-hase-negative-routes",
        "T20-TYPED-ORIGINAL-BEARER-ABC": "t20-original-bearer-bridge",
        "T20-ANCHORED-FIELD-SOURCE": "t20-anchored-source-bridge",
        "T20-VERACITY-DEPENDENCY-AUDIT": "t20-veracity-dependencies",
        "T20-PTS-NORMALIZATION-TRANSFER": "t20-external-transfer-assessment",
        "T20-TRACE-OBSERVATION-COPYING": "t20-copied-trace-observation",
        "T20-JOINT-SAME-BEARER-MODEL": "t20-same-bearer-joint-model",
        "T20-CONTROLLER-COMPLETENESS-TRANSFER": "t20-external-transfer-assessment",
        "T20-FOUNDATIONAL-PREMISE-SYNTHESIS": "t20-foundational-synthesis",
    }

    @classmethod
    def setUpClass(cls):
        LateTwentiethContextRoutesTests.setUpClass.__func__(cls)
        owner_path = ROOT / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json"
        baseline = json.loads(owner_path.read_text())["baseline"]["commit"]
        def original(path):
            return json.loads(subprocess.check_output(["git", "show", baseline + ":" + path], cwd=ROOT))
        cls.ledger = original(cls.aliases[cls.LEDGER_ALIAS]["public_path"])
        cls.frozen_claims = original(cls.GROUP + "/CLAIM_MAP.json")["results"]

    def errors(self, cross, text):
        errors = MethodologyRoutesMixin.errors(self, cross, text)
        work = next((w for w in cross["works"] if w["key"] == self.KEY), None)
        if work is not None:
            attached = {cross["sources"][s]["path"] for s in
                        work["source_keys"] + work.get("supporting_source_keys", [])}
            later = {r["public_path"] for r in self.selected if r["part"] == "result-ledger-v2"}
            if attached & later:
                errors.append("later-ledger-in-original-family")
        return errors

    def test_all_original_owners_and_support_have_scoped_reader_routes(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        owner_ids = [r["result_id"] for r in self.ledger["results"]]
        self.assertEqual(len(owner_ids), len(set(owner_ids)))
        self.assertEqual(set(owner_ids), {r["id"] for r in self.frozen_claims})
        self.assertEqual(set(self.OWNER_WORKS), set(owner_ids))
        works = {w["key"]: w for w in self.cross["works"]}
        page = "docs/reader/PAPER-CATALOGUE.md"
        required = set()
        for result_id, key in self.OWNER_WORKS.items():
            self.assertIn(result_id, works[key]["existing_result_ids"])
            rel, anchor = works[key]["catalogue_entry"].split("#", 1)
            self.assertEqual(rel, page)
            required.add((rel, anchor))
        # Two transfer findings share one work; the later appraisal is separate.
        self.assertEqual(len(required), 14)
        required.add((page, works["t20-cooperation-context"]["catalogue_entry"].split("#", 1)[1]))
        required |= {(r["public_path"], "") for r in self.selected if r["part"] == self.PART
                     and r["owner_archive_path"] not in self.PRIMARY_ALIASES}
        required.add((self.GROUP + "/CLAIM_MAP.json", ""))
        required.add(("docs/provenance/v5-successors/RESULT_STATUS.json", ""))
        reached = lambda text: self.section_targets(text, page, self.CATALOGUE_ANCHOR)
        self.assertTrue(required <= reached(self.text))
        for path, anchor in required:
            with self.subTest(path=path, anchor=anchor):
                href = "#" + anchor if path == page else (
                    "../provenance/v5-successors/RESULT_STATUS.json" if path.startswith("docs/provenance/") else "../../" + path)
                changed = self.text.replace("(" + href + ")", "(VERIFICATION-GUIDE.md)")
                self.assertNotEqual(changed, self.text)
                self.assertFalse(required <= reached(changed))

    def test_later_ledger_cannot_be_counted_as_original_family_support(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        later = next(r for r in self.selected if r["part"] == "result-ledger-v2")
        altered = deepcopy(self.cross)
        key = "fixture-later-ledger-binding"
        self.assertNotIn(key, altered["sources"])
        altered["sources"][key] = {"path": later["public_path"], "sha256": later["public_sha256"],
                                   "read_scope": "Fixture-only later-family admission."}
        work = next(w for w in altered["works"] if w["key"] == self.KEY)
        work["supporting_source_keys"].append(key)
        self.assertIn("later-ledger-in-original-family", self.errors(altered, self.text))


class MathMethodologyRoutesTests(MethodologyRoutesMixin, unittest.TestCase):
    """Exact component inspection and local applications keep their owners."""
    PART = "math"
    KEY = "t20-math-utilisation-methodology"
    PRIMARY_ALIASES = ["t20/methodology/math/MATH_UTILISATION.md"]
    LEDGER_ALIAS = "t20/methodology/math/MATH_UTILISATION.json"
    EXPECTED = {KEY: ("supporting-reference", {PART}, PRIMARY_ALIASES)}
    CATALOGUE_ANCHOR = "mathematical-reading-local-applications-and-transfer-limits"
    VERIFICATION_HEADING = "checking-mathematical-reading-and-transfer-credit"
    METHOD_ANCHOR = "coverage-and-inspection-levels"
    CORE_WORKS = {
        "arabic": "t20-arabic-reading-methodology",
        "drive": "t20-drive-corpus-methodology",
        "math": KEY,
        "result-ledger": "t20-result-method-handoff",
    }

    @classmethod
    def setUpClass(cls):
        LateTwentiethContextRoutesTests.setUpClass.__func__(cls)
        owners = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json").read_text())
        def original(path):
            return subprocess.check_output(["git", "show", owners["baseline"]["commit"] + ":" + path],
                                           cwd=ROOT, text=True)
        cls.ledger = json.loads(original(cls.aliases[cls.LEDGER_ALIAS]["public_path"]))
        cls.method_text = original(cls.aliases[cls.PRIMARY_ALIASES[0]]["public_path"])

    def test_component_questions_reach_exact_method_sections_and_existing_owners(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        components = self.ledger["components"]
        manuscripts = [r for r in components if r["component_kind"] == "upstream_manuscript"]
        local = [r for r in components if r["component_kind"] == "local_orthemology_application"]
        self.assertEqual((len(components), len(manuscripts), len(local)), (53, 52, 1))
        families = {r["family_id"] for r in manuscripts}
        self.assertEqual(families, set(self.ledger["coverage"]["family_priority_ids"]))
        self.assertEqual(len(families), 18)
        self.assertEqual(local[0]["id"], "MATH-122-APPLICATION")
        for status in ["FORMAL_SOURCE_REPLAYED", "ORTHEMOLOGY_TRANSFER_PROVED"]:
            self.assertEqual({r["id"] for r in components if status in r["statuses"]}, {local[0]["id"]})
        self.assertTrue(all(r["replay_status"]["upstream"] == "NOT_RUN" and
                            not r["direct_upstream_theorem_transfer"] for r in components))
        page = "docs/reader/PAPER-CATALOGUE.md"
        method = self.aliases[self.PRIMARY_ALIASES[0]]["public_path"]
        headings = {h[0] for h in self.mod.markdown_index(self.method_text)["headings"]}
        sections = {self.METHOD_ANCHOR, "boundaries-and-source-binding",
                    "all-remaining-priority-manuscripts",
                    "two-further-manuscripts-affected-the-method-comparison"}
        # The 373 lemma shares a narrative section with the targeted 235 lemma;
        # 235's remaining abstract-only manuscripts have their own family section.
        for family in families - {373}:
            matches = {h for h in headings if h.startswith("family-" + str(family) + "-")}
            self.assertEqual(len(matches), 1, family)
            sections |= matches
        self.assertTrue(sections <= headings)
        required = {(method, h) for h in sections}
        required |= {(r["public_path"], "") for r in self.selected if r["part"] == self.PART
                     and r["owner_archive_path"] not in self.PRIMARY_ALIASES}
        works = {w["key"]: w for w in self.cross["works"]}
        peers = ["t20-copied-trace-observation", "t20-external-transfer-assessment",
                 "information-composition", "t09-finite-certificate-calculus",
                 "t16-signed-synthesis", "t16-submitted-controller",
                 "t20-scalar-fusion", "t20-hase-negative-routes"]
        required |= {(page, works[k]["catalogue_entry"].split("#", 1)[1]) for k in peers}
        for result_id in ["T20-TRACE-OBSERVATION-COPYING", "T20-PTS-NORMALIZATION-TRANSFER",
                          "T20-CONTROLLER-COMPLETENESS-TRANSFER"]:
            owner = ResultLedgerMethodologyRoutesTests.OWNER_WORKS[result_id]
            self.assertIn(result_id, works[owner]["existing_result_ids"])
        reached = lambda body: self.section_targets(body, page, self.CATALOGUE_ANCHOR)
        self.assertTrue(required <= reached(self.text))
        for path, anchor in required:
            with self.subTest(path=path, anchor=anchor):
                href = ("#" + anchor if path == page else
                        "../../" + path + ("#" + anchor if anchor else ""))
                changed = self.text.replace("(" + href + ")", "(VERIFICATION-GUIDE.md)")
                self.assertNotEqual(changed, self.text)
                self.assertFalse(required <= reached(changed))

    def test_original_nineteen_source_core_is_complete_without_later_context_credit(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        core = [r for r in self.selected if r.get("selection_layer") == "methodology-core"]
        self.assertEqual(len(core), 19)
        self.assertEqual({r["part"] for r in core}, set(self.CORE_WORKS))
        def covered(cross):
            works = {w["key"]: w for w in cross["works"]}
            return all(any(cross["sources"][s]["path"] == row["public_path"] and
                           cross["sources"][s]["sha256"] == row["public_sha256"]
                           for s in works[self.CORE_WORKS[row["part"]]]["source_keys"] +
                           works[self.CORE_WORKS[row["part"]]].get("supporting_source_keys", []))
                       for row in core)
        self.assertTrue(covered(self.cross))
        for row in core:
            with self.subTest(alias=row["owner_archive_path"]):
                altered = deepcopy(self.cross)
                work = next(w for w in altered["works"] if w["key"] == self.CORE_WORKS[row["part"]])
                for field in ["source_keys", "supporting_source_keys"]:
                    work[field] = [s for s in work[field] if altered["sources"][s]["path"] != row["public_path"]]
                self.assertFalse(covered(altered))


class MathematicalCompanionRoutesTests(MethodologyRoutesMixin, unittest.TestCase):
    """Exposition preserves original proof owners and documentary QA limits."""
    PART = "math-companion"
    KEY = "t20-mathematical-companion"
    PRIMARY_ALIASES = ["t20/reports/MATHEMATICAL_COMPANION.md"]
    QA_ALIAS = "t20/reports/MATHEMATICAL_COMPANION_QA.json"
    NARRATIVE_COMPANIONS = {PRIMARY_ALIASES[0]: QA_ALIAS}
    EXPECTED = {KEY: ("supporting-reference", {PART}, PRIMARY_ALIASES)}
    CATALOGUE_ANCHOR = "the-twentieth-mathematical-companion-and-its-original-result-owners"
    VERIFICATION_HEADING = "checking-the-mathematical-companion-and-its-document-qa"
    METHOD_ANCHOR = "finding-the-source-evidence"
    OWNER_KEYS = {
        "t20-original-bearer-bridge", "t20-anchored-source-bridge",
        "t20-veracity-dependencies", "t20-same-bearer-joint-model",
        "t20-foundational-synthesis", "t20-prior-formal-reuse",
        "t20-church-probe", "t20-scalar-fusion", "t20-cnd-scope",
        "t20-modal-union", "t20-ground-extension", "t20-grounded-support",
        "t20-copied-trace-observation", "t20-external-transfer-assessment",
        "t20-cooperation-context",
    }

    def errors(self, cross, text):
        errors = MethodologyRoutesMixin.errors(self, cross, text)
        primary = self.aliases[self.PRIMARY_ALIASES[0]]["public_path"]
        supports = {r["public_path"] for r in self.selected
                    if r["part"] == self.PART and r["owner_archive_path"] not in self.PRIMARY_ALIASES}
        for work in cross["works"]:
            paths = {cross["sources"][s]["path"] for s in work["source_keys"]}
            paths |= {cross["sources"][f["source"]]["path"] for f in work.get("reading_forms", [])}
            if paths & supports:
                errors.append("companion-support-promoted")
            if work["key"] != self.KEY and primary in paths:
                errors.append("companion-duplicate-primary")
        return errors

    def test_support_or_a_copied_primary_cannot_become_a_second_work(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        work = next(w for w in self.cross["works"] if w["key"] == self.KEY)
        selected_paths = {r["public_path"] for r in self.selected if r["part"] == self.PART}
        for key in work["source_keys"] + work["supporting_source_keys"]:
            if self.cross["sources"][key]["path"] not in selected_paths:
                continue
            with self.subTest(source=key):
                altered = deepcopy(self.cross)
                duplicate = deepcopy(work)
                duplicate.update(key="fixture-companion-duplicate", source_keys=[key],
                                 supporting_source_keys=[],
                                 reading_forms=[{"source": key, "relationship": "retained-source-reading-projection"}])
                altered["works"].append(duplicate)
                error = "companion-duplicate-primary" if key in work["source_keys"] else "companion-support-promoted"
                self.assertIn(error, self.errors(altered, self.text))

    def test_exposition_and_original_owner_routes_reject_plausible_retargeting(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        page = "docs/reader/PAPER-CATALOGUE.md"
        works = {w["key"]: w for w in self.cross["works"]}
        source = self.aliases[self.PRIMARY_ALIASES[0]]["public_path"]
        sections = {
            "part-1-what-the-computer-checked", "part-2-foundational-audit-synthesis",
            "part-3-further-mathematical-results", "appraisal-distinction-on-7-october-2026",
            "exact-hase-scalar-fusion-reduction", "modal-union-consequence-completeness",
            "original-ground-extension-and-preservation",
            "a-productive-nonduplication-route-to-essential-nonreceipt",
            "grounded-support-retraction-and-later-root-aliasing",
            "the-deletion-observation-control",
            "external-results-considered-without-false-transfer-credit",
        }
        required = {(source, anchor) for anchor in sections}
        required |= {(page, works[k]["catalogue_entry"].split("#", 1)[1])
                     for k in self.OWNER_KEYS}
        required |= {(r["public_path"], "") for r in self.selected
                     if r["part"] == self.PART and r["owner_archive_path"] not in self.PRIMARY_ALIASES}
        reached = lambda body: self.section_targets(body, page, self.CATALOGUE_ANCHOR)
        self.assertTrue(required <= reached(self.text), required - reached(self.text))
        for path, anchor in required:
            with self.subTest(path=path, anchor=anchor):
                href = "#" + anchor if path == page else "../../" + path + ("#" + anchor if anchor else "")
                changed = self.text.replace("(" + href + ")", "(VERIFICATION-GUIDE.md)")
                self.assertNotEqual(changed, self.text)
                self.assertFalse(required <= reached(changed))

    def test_document_qa_and_derivation_do_not_admit_an_unavailable_edition(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        records = {r["owner_archive_path"]: r for r in self.selected if r["part"] == self.PART}
        qa = json.loads((ROOT / records[self.QA_ALIAS]["public_path"]).read_text())
        eq = json.loads((ROOT / records["t20/reports/MATHEMATICAL_COMPANION_EQUATIONS.json"]["public_path"]).read_text())
        derivation = json.loads((ROOT / records["t20/reports/MATHEMATICAL_COMPANION_DERIVATION.json"]["public_path"]).read_text())
        primary = records[self.PRIMARY_ALIASES[0]]
        self.assertEqual(primary["projection"], "EXACT")
        for alias, row in records.items():
            if alias != self.PRIMARY_ALIASES[0]:
                self.assertEqual(row["projection"], "DERIVED")
                self.assertNotEqual(row["original_sha256"], row["public_sha256"])
        self.assertFalse(qa["scientific_replay"])
        self.assertTrue(qa["Microsoft_Word_application_UI_render"].startswith("NOT_RUN"))
        self.assertTrue(all(not p["image_body_included"] for p in qa["pages"]))
        self.assertEqual(qa["source"]["sha256"], primary["public_sha256"])
        self.assertEqual(eq["source"], qa["source"])
        self.assertEqual(derivation["output"], qa["source"])
        self.assertEqual(len(eq["equations"]), qa["native_editable_OMML_equations"])
        self.assertTrue(any(r.get("body_included") is False for r in derivation["inputs"]))
        work = next(w for w in self.cross["works"] if w["key"] == self.KEY)
        self.assertEqual(len(work["reading_forms"]), 1)
        self.assertTrue(all(self.cross["sources"][f["source"]]["path"].endswith(".md")
                            for f in work["reading_forms"]))
        # A recorded final-document identity is not an admitted public edition.
        altered = deepcopy(self.cross)
        altered["sources"]["fixture-unavailable-word-edition"] = {
            "path": qa["final_document"]["path"], "sha256": qa["final_document"]["sha256"],
            "read_scope": "Isolated unavailable-edition promotion control."}
        candidate = next(w for w in altered["works"] if w["key"] == self.KEY)
        candidate["reading_forms"].append({"source": "fixture-unavailable-word-edition",
                                           "relationship": "retained-source-reading-projection"})
        self.assertIn("methodology-reading-forms", self.errors(altered, self.text))
        page = "docs/reader/VERIFICATION-GUIDE.md"
        body = (ROOT / page).read_text()
        required = {(r["public_path"], "") for a, r in records.items() if a not in self.PRIMARY_ALIASES}
        required.add((primary["public_path"], "appraisal-distinction-on-7-october-2026"))
        reached = lambda text: self.section_targets(text, page, self.VERIFICATION_HEADING)
        self.assertTrue(required <= reached(body), required - reached(body))
        for path, anchor in required:
            href = "../../" + path + ("#" + anchor if anchor else "")
            changed = body.replace("(" + href + ")", "(PAPER-CATALOGUE.md)")
            self.assertNotEqual(changed, body)
            self.assertFalse(required <= reached(changed))


class FinalReportRoutesTests(MethodologyRoutesMixin, unittest.TestCase):
    """A dated synthesis retains original evidence and independent review limits."""
    PART = "final-report"
    KEY = "t20-final-research-report"
    PRIMARY_ALIASES = ["t20/reports/REPORT.md"]
    QA_ALIAS = "t20/reports/REPORT_QA_MANIFEST.json"
    READBACK_ALIAS = "t20/reports/REPORT_FINAL_SOURCE_READBACK.json"
    READBACK_TEXT_ALIAS = "t20/reports/REPORT_FINAL_SOURCE_READBACK.md"
    REPORT_SOURCE_KEY = "t20-context-5e119dcd4fa30ec7"
    READBACK_SOURCE_KEY = "t20-context-efd1da7e8edf7f31"
    V2_ALIAS = "t20/reports/REPORT_v2.md"
    V2_QA_ALIAS = "t20/reports/REPORT_v2_QA_MANIFEST.json"
    V2_READBACK_TEXT_ALIAS = "t20/reports/REPORT_GUIDE_V2_READBACK.md"
    V2_READBACK_ALIAS = "t20/reports/REPORT_GUIDE_V2_READBACK.json"
    ADDITIONAL_READING_ALIASES = (V2_ALIAS,)
    SUCCESSOR_ALIASES = (V2_ALIAS, V2_QA_ALIAS, V2_READBACK_TEXT_ALIAS, V2_READBACK_ALIAS)
    ORIGINAL_SUPPORT_KEYS = ("t20-context-187307ed2144d821", READBACK_SOURCE_KEY,
                             "t20-context-47f0fbeaf04dfc44", "t20-context-50e3ae6b35c1b914")
    SUCCESSOR_RELATION = "expanded-reading-edition-preserves-dated-assessment"
    V2_CATALOGUE_HEADING = "the-expanded-report-v2-and-its-separately-owned-additions"
    V2_VERIFICATION_HEADING = "checking-report-v2-and-shared-successor-source-readback"
    NARRATIVE_COMPANIONS = {PRIMARY_ALIASES[0]: QA_ALIAS}
    EXPECTED = {KEY: ("synthesis", {PART}, PRIMARY_ALIASES)}
    CATALOGUE_ANCHOR = "the-twentieth-final-report-and-its-dated-research-assessment"
    VERIFICATION_HEADING = "checking-the-final-report-source-readback-and-document-qa"
    METHOD_ANCHOR = "repository-and-evidence-boundary"
    OWNER_KEYS = {
        "t20-original-bearer-bridge", "t20-anchored-source-bridge",
        "t20-veracity-dependencies", "t20-same-bearer-joint-model",
        "t20-cnd-scope", "t20-church-probe", "t20-scalar-fusion",
        "t20-modal-union", "t20-ground-extension", "t20-grounded-support",
        "t20-copied-trace-observation", "t20-external-transfer-assessment",
        "t20-cooperation-context", "t20-mathematical-companion",
        "t20-math-utilisation-methodology", "t20-arabic-reading-methodology",
        "t20-hase-negative-routes", "t20-foundational-synthesis",
    }

    @classmethod
    def setUpClass(cls):
        LateTwentiethContextRoutesTests.setUpClass.__func__(cls)
        owners = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json").read_text())
        def original(alias):
            path = cls.aliases[alias]["public_path"]
            return json.loads(subprocess.check_output(
                ["git", "show", owners["baseline"]["commit"] + ":" + path], cwd=ROOT))
        cls.qa = original(cls.QA_ALIAS)
        cls.readback = original(cls.READBACK_ALIAS)
        cls.v2_qa = original(cls.V2_QA_ALIAS)
        cls.v2_readback = original(cls.V2_READBACK_ALIAS)

    def source_key(self, alias):
        return "t20-context-" + hashlib.sha256(self.aliases[alias]["public_path"].encode()).hexdigest()[:16]

    def errors(self, cross, text):
        errors = MethodologyRoutesMixin.errors(self, cross, text)
        work = next((w for w in cross["works"] if w["key"] == self.KEY), None)
        if work is None:
            return errors
        family = {r["public_path"] for r in self.selected if r["part"] == self.PART}
        primary = self.aliases[self.PRIMARY_ALIASES[0]]["public_path"]
        successors = {self.aliases[a]["public_path"] for a in self.SUCCESSOR_ALIASES}
        edition_paths = {primary, self.aliases[self.V2_ALIAS]["public_path"]}
        supports = (family | successors) - edition_paths
        attached = {cross["sources"][s]["path"]
                    for s in work["source_keys"] + work.get("supporting_source_keys", [])}
        if not attached <= family | successors | {self.GROUP + "/CONTEXT_SOURCE_INDEX.json"}:
            errors.append("report-family-boundary")
        expected_support = list(self.ORIGINAL_SUPPORT_KEYS) + [self.source_key(a) for a in self.SUCCESSOR_ALIASES]
        if work.get("supporting_source_keys") != expected_support:
            errors.append("report-ordered-support-preservation")
        expected_forms = [{"source": k, "relationship": "retained-source-reading-projection"}
                          for k in (self.REPORT_SOURCE_KEY, self.source_key(self.V2_ALIAS))]
        if work.get("reading_forms") != expected_forms:
            errors.append("report-ordered-reading-forms")
        for alias in self.SUCCESSOR_ALIASES:
            row = self.aliases[alias]
            bound = cross["sources"].get(self.source_key(alias))
            if (bound is None or bound.get("path") != row["public_path"]
                    or bound.get("sha256") != row["public_sha256"] or not bound.get("read_scope")):
                errors.append("report-successor-identity:" + alias)
        relations = [r for r in cross["relations"] if r.get("from") == self.REPORT_SOURCE_KEY
                     and r.get("to") == self.source_key(self.V2_ALIAS)]
        if relations != [{"from": self.REPORT_SOURCE_KEY, "to": self.source_key(self.V2_ALIAS),
                          "kind": self.SUCCESSOR_RELATION, "basis": self.source_key(self.V2_READBACK_ALIAS)}]:
            errors.append("report-successor-relation")
        if (work["source_keys"] != [self.REPORT_SOURCE_KEY]
                or self.READBACK_SOURCE_KEY not in work.get("supporting_source_keys", [])):
            errors.append("report-existing-binding-reuse")
        cooperation = next((w for w in cross["works"] if w["key"] == "t20-cooperation-context"), None)
        if cooperation is None or not {self.REPORT_SOURCE_KEY, self.READBACK_SOURCE_KEY} <= set(
                cooperation.get("supporting_source_keys", [])):
            errors.append("report-cooperation-support")
        for candidate in cross["works"]:
            paths = {cross["sources"][s]["path"] for s in candidate["source_keys"]}
            paths |= {cross["sources"][f["source"]]["path"] for f in candidate.get("reading_forms", [])}
            if paths & supports:
                errors.append("report-support-promoted")
            if candidate["key"] != self.KEY and edition_paths & paths:
                errors.append("report-duplicate-primary")
        return errors

    def test_all_four_public_identities_and_existing_cooperation_support_are_required(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        selected = [r for r in self.selected if r["part"] == self.PART]
        self.assertEqual((len(selected), sum(r["public_bytes"] for r in selected)), (4, 59821))
        work = next(w for w in self.cross["works"] if w["key"] == self.KEY)
        for row in selected:
            with self.subTest(alias=row["owner_archive_path"]):
                key = next(k for k in work["source_keys"] + work["supporting_source_keys"]
                           if self.cross["sources"][k]["path"] == row["public_path"])
                altered = deepcopy(self.cross)
                self.assertNotEqual(altered["sources"][key]["sha256"], "0" * 64)
                altered["sources"][key]["sha256"] = "0" * 64
                self.assertIn("methodology-source-identity:" + row["owner_archive_path"],
                              self.errors(altered, self.text))
        for key in (self.REPORT_SOURCE_KEY, self.READBACK_SOURCE_KEY):
            with self.subTest(inherited_support=key):
                altered = deepcopy(self.cross)
                cooperation = next(w for w in altered["works"] if w["key"] == "t20-cooperation-context")
                cooperation["supporting_source_keys"].remove(key)
                self.assertIn("report-cooperation-support", self.errors(altered, self.text))

    def test_support_duplicate_and_later_report_inflation_are_rejected(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        work = next(w for w in self.cross["works"] if w["key"] == self.KEY)
        selected_paths = {r["public_path"] for r in self.selected if r["part"] == self.PART}
        for key in work["source_keys"] + work["supporting_source_keys"]:
            if self.cross["sources"][key]["path"] not in selected_paths:
                continue
            with self.subTest(source=key):
                altered = deepcopy(self.cross)
                duplicate = deepcopy(work)
                duplicate.update(key="fixture-final-report-duplicate", source_keys=[key],
                                 supporting_source_keys=[], reading_forms=[{
                                     "source": key, "relationship": "retained-source-reading-projection"}])
                altered["works"].append(duplicate)
                error = "report-duplicate-primary" if key in work["source_keys"] else "report-support-promoted"
                self.assertIn(error, self.errors(altered, self.text))
        later = next(r for r in self.selected if r["owner_archive_path"] == "t20/reading/GUIDE_v2.md")
        self.assertNotEqual(later["part"], self.PART)
        altered = deepcopy(self.cross)
        altered["sources"]["fixture-later-report"] = {
            "path": later["public_path"], "sha256": later["public_sha256"],
            "read_scope": "Isolated later-family admission control; no body reading."}
        candidate = next(w for w in altered["works"] if w["key"] == self.KEY)
        candidate["supporting_source_keys"].append("fixture-later-report")
        self.assertIn("report-family-boundary", self.errors(altered, self.text))

    def test_report_sections_and_original_owners_reject_scoped_retargeting(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        page = "docs/reader/PAPER-CATALOGUE.md"
        source = self.aliases[self.PRIMARY_ALIASES[0]]["public_path"]
        sections = {
            "current-philosophical-assessment", "foundational-inference-and-its-philosophical-premises",
            "grounded-testimony-and-warranted-continuation", "original-ground-and-the-limits-of-observation",
            "the-exact-hase-identity-remains-open", "modal-crossings-and-scoped-completeness",
            "openai-mathematical-corpus-study", "arabic-source-study-and-rereading",
            "position-across-the-twelve-research-avenues", "remaining-obligations",
        }
        works = {w["key"]: w for w in self.cross["works"]}
        required = {(source, anchor) for anchor in sections}
        required |= {(page, works[k]["catalogue_entry"].split("#", 1)[1]) for k in self.OWNER_KEYS}
        required |= {(r["public_path"], "") for r in self.selected
                     if r["part"] == self.PART and r["owner_archive_path"] not in self.PRIMARY_ALIASES}
        reached = lambda body: self.section_targets(body, page, self.CATALOGUE_ANCHOR)
        self.assertTrue(required <= reached(self.text), required - reached(self.text))
        for path, anchor in required:
            with self.subTest(path=path, anchor=anchor):
                href = "#" + anchor if path == page else "../../" + path + ("#" + anchor if anchor else "")
                changed = self.text.replace("(" + href + ")", "(VERIFICATION-GUIDE.md)")
                self.assertNotEqual(changed, self.text)
                self.assertFalse(required <= reached(changed))

        # The existing companion provides an inbound route to the new synthesis.
        companion = works["t20-mathematical-companion"]["catalogue_entry"].split("#", 1)[1]
        inbound = (page, self.CATALOGUE_ANCHOR)
        self.assertIn(inbound, self.section_targets(self.text, page, companion))
        changed = self.text.replace("(#" + self.CATALOGUE_ANCHOR + ")", "(VERIFICATION-GUIDE.md)")
        self.assertNotEqual(changed, self.text)
        self.assertNotIn(inbound, self.section_targets(changed, page, companion))

    def test_document_qa_and_source_readback_keep_distinct_identity_and_scope(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        records = {r["owner_archive_path"]: r for r in self.selected if r["part"] == self.PART}
        report = records[self.PRIMARY_ALIASES[0]]
        readback_text = records[self.READBACK_TEXT_ALIAS]
        qa, readback = self.qa, self.readback
        for alias, row in records.items():
            exact = alias in self.PRIMARY_ALIASES + [self.READBACK_TEXT_ALIAS]
            self.assertEqual(row["projection"], "EXACT" if exact else "DERIVED")
            self.assertEqual(row["original_sha256"] == row["public_sha256"], exact)
        self.assertEqual(qa["source"], {"path": "REPORT.md", "sha256": report["public_sha256"],
                                      "bytes": report["public_bytes"]})
        self.assertEqual(readback["report"]["sha256"], report["public_sha256"])
        self.assertEqual(readback["readback"]["sha256"], readback_text["public_sha256"])
        public_receipt = qa["source_readback"]["public_record"]
        self.assertEqual(public_receipt["sha256"], records[self.READBACK_ALIAS]["public_sha256"])
        self.assertEqual(public_receipt["bytes"], records[self.READBACK_ALIAS]["public_bytes"])
        self.assertEqual(qa["source_readback"]["historical_original"]["sha256"],
                         records[self.READBACK_ALIAS]["original_sha256"])
        self.assertEqual(readback["original_review_receipt_sha256"], records[self.READBACK_ALIAS]["original_sha256"])
        self.assertEqual(qa["original_qa_manifest_sha256"], records[self.QA_ALIAS]["original_sha256"])
        self.assertFalse(qa["science_rerun"])
        self.assertFalse(readback["scientific_sources_replayed"])
        self.assertFalse(readback["source_changes_made"])
        self.assertEqual((qa["page_count"], len(qa["page_inspections"])), (11, 11))
        self.assertTrue(all(p["image_body_included"] is False for p in qa["page_inspections"]))
        self.assertEqual(readback["previous_evidence_bindings_rechecked"], 108)
        self.assertTrue(readback["previous_evidence_bindings_unchanged"])
        omitted = [r for r in readback["inspected_bindings"] if r.get("original_record_body_included") is False]
        self.assertEqual(len(omitted), 3)
        altered = deepcopy(self.cross)
        altered["sources"]["fixture-final-report-word-edition"] = {
            "path": qa["document"]["path"], "sha256": qa["document"]["sha256"],
            "read_scope": "Isolated owner-only document promotion control."}
        candidate = next(w for w in altered["works"] if w["key"] == self.KEY)
        candidate["reading_forms"].append({"source": "fixture-final-report-word-edition",
                                           "relationship": "retained-source-reading-projection"})
        self.assertIn("methodology-reading-forms", self.errors(altered, self.text))
        page = "docs/reader/VERIFICATION-GUIDE.md"
        body = (ROOT / page).read_text()
        required = {
            (records[self.QA_ALIAS]["public_path"], ""),
            (records[self.READBACK_ALIAS]["public_path"], ""),
            (readback_text["public_path"], "scope-of-acceptance"),
        }
        reached = lambda text: self.section_targets(text, page, self.VERIFICATION_HEADING)
        self.assertTrue(required <= reached(body), required - reached(body))
        for path, anchor in required:
            href = "../../" + path + ("#" + anchor if anchor else "")
            changed = body.replace("(" + href + ")", "(PAPER-CATALOGUE.md)")
            self.assertNotEqual(changed, body)
            self.assertFalse(required <= reached(changed))

    def test_prepared_comprehension_protocol_keeps_existing_evidence_routes(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        page = "docs/reader/VERIFICATION-GUIDE.md"
        body = (ROOT / page).read_text()
        heading = "independent-reader-comprehension-tasks-for-the-final-candidate"
        prefix = "docs/project-closure/reader-refactor-issue-35/"
        required = {
            (prefix + "PILOT-QUALIFICATION.md", "source-based-answers-and-paired-adverse-readings"),
            (prefix + "PILOT-QUALIFICATION.md", "mechanical-controls-and-maintenance-finding"),
            (prefix + "PILOT.md", ""),
            ("docs/reader/RESULT-INDEX.md", "finite-mediator"),
            ("docs/reader/RESEARCH-ATLAS.md", "recognition-sound-cognition-and-correction"),
            ("docs/reader/PAPER-CATALOGUE.md", "formal-reference"),
            ("docs/reader/PAPER-CATALOGUE.md", "decisive-and-reflexive-revision"),
            ("docs/reader/CURRENT-FRONTIERS.md", "a-historical-tensor-frontier-has-a-written-successor"),
            ("docs/reader/CURRENT-FRONTIERS.md", "exact-geometry-versus-weaker-retained-tasks"),
            ("docs/reader/APPLICATIONS.md", "joint-feasibility-across-avenues"),
        }
        reached = lambda text: self.section_targets(text, page, heading)
        self.assertTrue(required <= reached(body), required - reached(body))
        for path, anchor in required:
            href = (path.removeprefix("docs/reader/") if path.startswith("docs/reader/")
                    else "../" + path.removeprefix("docs/"))
            href += "#" + anchor if anchor else ""
            changed = body.replace("(" + href + ")", "(PAPER-CATALOGUE.md)")
            self.assertNotEqual(changed, body)
            self.assertFalse(required <= reached(changed))

    def test_expanded_report_is_one_work_with_exact_ordered_editions_and_support(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        # Other authorised families may grow without changing this report's
        # identity: both reading editions belong to this same unique work.
        for alias in self.PRIMARY_ALIASES + list(self.ADDITIONAL_READING_ALIASES):
            path = self.aliases[alias]["public_path"]
            owners = [w["key"] for w in self.cross["works"]
                      if path in {self.cross["sources"][k]["path"] for k in
                                  w["source_keys"] + [f["source"] for f in w.get("reading_forms", [])]}]
            self.assertEqual(owners, [self.KEY], alias)
        expected = [(258, self.V2_ALIAS, 53358), (262, self.V2_QA_ALIAS, 10194),
                    (260, self.V2_READBACK_TEXT_ALIAS, 3925), (261, self.V2_READBACK_ALIAS, 17333)]
        for index, alias, size in expected:
            self.assertEqual((self.selected[index]["owner_archive_path"], self.selected[index]["public_bytes"]),
                             (alias, size))
            row = self.aliases[alias]
            body = (ROOT / row["public_path"]).read_bytes()
            self.assertEqual((len(body), hashlib.sha256(body).hexdigest()), (size, row["public_sha256"]))
            keys = [k for k, v in self.cross["sources"].items() if v["path"] == row["public_path"]]
            self.assertEqual(keys, [self.source_key(alias)])

    def test_successor_identity_relation_credit_and_old_support_reject_mutation(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for alias in self.SUCCESSOR_ALIASES:
            for field, value in [("path", self.aliases[self.QA_ALIAS]["public_path"]),
                                 ("sha256", "0" * 64), ("read_scope", "")]:
                with self.subTest(alias=alias, field=field):
                    altered = deepcopy(self.cross)
                    altered["sources"][self.source_key(alias)][field] = value
                    self.assertIn("report-successor-identity:" + alias, self.errors(altered, self.text))
        for mutation in ("remove", "kind", "basis"):
            altered = deepcopy(self.cross)
            relation = next(r for r in altered["relations"] if r.get("kind") == self.SUCCESSOR_RELATION)
            if mutation == "remove":
                altered["relations"].remove(relation)
            else:
                relation[mutation] = "unqualified-successor" if mutation == "kind" else self.READBACK_SOURCE_KEY
            self.assertIn("report-successor-relation", self.errors(altered, self.text))
        for rid in ("T20-EMERGENCE-TYPE-CONTROL", "T20-FIXTURE-INVENTED-REPORT-RESULT"):
            altered = deepcopy(self.cross)
            next(w for w in altered["works"] if w["key"] == self.KEY)["existing_result_ids"] = [rid]
            self.assertIn("methodology-result-credit", self.errors(altered, self.text))
        for key in self.ORIGINAL_SUPPORT_KEYS + tuple(self.source_key(a) for a in self.SUCCESSOR_ALIASES):
            altered = deepcopy(self.cross)
            next(w for w in altered["works"] if w["key"] == self.KEY)["supporting_source_keys"].remove(key)
            self.assertIn("report-ordered-support-preservation", self.errors(altered, self.text))

    def test_either_report_edition_cannot_become_another_work_or_documentary_primary(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        work = next(w for w in self.cross["works"] if w["key"] == self.KEY)
        for alias in self.PRIMARY_ALIASES + list(self.SUCCESSOR_ALIASES):
            key = self.REPORT_SOURCE_KEY if alias in self.PRIMARY_ALIASES else self.source_key(alias)
            for field in ("source_keys", "reading_forms"):
                altered = deepcopy(self.cross)
                duplicate = deepcopy(work)
                duplicate.update(key="fixture-v2-credit", source_keys=[], reading_forms=[], supporting_source_keys=[])
                duplicate[field] = [key] if field == "source_keys" else [
                    {"source": key, "relationship": "retained-source-reading-projection"}]
                altered["works"].append(duplicate)
                error = "report-duplicate-primary" if alias in self.PRIMARY_ALIASES + [self.V2_ALIAS] else "report-support-promoted"
                self.assertIn(error, self.errors(altered, self.text))
        for alias in (self.QA_ALIAS, self.V2_QA_ALIAS, self.V2_READBACK_TEXT_ALIAS, self.V2_READBACK_ALIAS):
            altered = deepcopy(self.cross)
            candidate = next(w for w in altered["works"] if w["key"] == self.KEY)
            key = next(k for k, v in altered["sources"].items() if v["path"] == self.aliases[alias]["public_path"])
            candidate["reading_forms"][1]["source"] = key
            self.assertIn("report-ordered-reading-forms", self.errors(altered, self.text))

    def report_preservation_errors(self, original, revised):
        old, new = original.splitlines(True), revised.splitlines(True)
        operations = difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()
        changed = [op for op in operations if op[0] != "equal"]
        expected = [("replace", 10, 11, 10, 11), ("insert", 79, 79, 79, 93),
                    ("insert", 190, 190, 204, 240)]
        preserved = sum(sum(map(len, old[i:j])) for op, i, j, _, _ in operations if op == "equal")
        errors = []
        if changed != expected or preserved != 41018:
            errors.append("report-v2-byte-preservation")
        heading = b"## Current philosophical assessment\n"
        def assessment(body):
            start = body.index(heading)
            end = body.find(b"\n## ", start + len(heading))
            return body[start:] if end < 0 else body[start:end]
        if assessment(original) != assessment(revised):
            errors.append("report-v2-philosophical-assessment")
        return errors

    def test_actual_report_bytes_establish_the_precise_successor_delta(self):
        original = (ROOT / self.aliases[self.PRIMARY_ALIASES[0]]["public_path"]).read_bytes()
        revised = (ROOT / self.aliases[self.V2_ALIAS]["public_path"]).read_bytes()
        self.assertEqual(self.report_preservation_errors(original, revised), [])
        self.assertIn("report-v2-byte-preservation", self.report_preservation_errors(
            original, revised.replace(b"The sources' affirmative", b"The sources' unsupported", 1)))
        self.assertIn("report-v2-philosophical-assessment", self.report_preservation_errors(
            original, revised.replace(b"The sources' affirmative", b"The sources' unsupported", 1)))
        record = self.v2_readback["preservation"][0]
        for label, alias in (("baseline", self.PRIMARY_ALIASES[0]), ("successor", self.V2_ALIAS)):
            row = self.aliases[alias]
            self.assertEqual(record[label]["included_projection"], {
                "owner_archive_path": alias, "sha256": row["public_sha256"], "bytes": row["public_bytes"]})
        self.assertEqual(record["allowed_replacement_baseline_line"], 11)
        self.assertEqual(record["changes"], [
            {"operation": "replace", "old_line_start": 11, "old_line_end": 11, "new_line_start": 11, "new_line_end": 11},
            {"operation": "insert", "old_line_start": 80, "old_line_end": 79, "new_line_start": 80, "new_line_end": 93},
            {"operation": "insert", "old_line_start": 191, "old_line_end": 190, "new_line_start": 205, "new_line_end": 240}])

    def successor_record_errors(self, qa, readback):
        errors = []
        for field, alias in (("source", self.V2_ALIAS), ("source_review", self.V2_READBACK_ALIAS)):
            row = self.aliases[alias]
            if qa[field]["included_record"] != {"owner_archive_path": alias,
                    "sha256": row["public_sha256"], "bytes": row["public_bytes"]}:
                errors.append("report-v2-qa-identity:" + field)
        if (qa["source_review"]["historical_original_identity"]["sha256"] !=
                self.aliases[self.V2_READBACK_ALIAS]["original_sha256"]
                or qa["original_document_record_sha256"] != self.aliases[self.V2_QA_ALIAS]["original_sha256"]
                or readback["original_review_receipt_sha256"] != self.aliases[self.V2_READBACK_ALIAS]["original_sha256"]):
            errors.append("report-v2-original-public-distinction")
        if (qa["science_runs"] is not False or readback["proofs_replayed_by_this_reviewer"] is not False
                or readback["scientific_sources_changed_by_this_reviewer"] is not False
                or readback["methodology_new_reading_or_science_credit"] != 0):
            errors.append("report-v2-retrospective-execution-scope")
        if (readback["predecessor_15_result_objects_raw_json_preserved"] is not True
                or readback["current_1434_philosophical_section_verbatim_preserved"] is not True):
            errors.append("report-v2-historical-preservation-scope")
        return errors

    def test_successor_qa_and_shared_readback_keep_actor_identity_and_scope(self):
        qa, readback = self.v2_qa, self.v2_readback
        self.assertEqual(self.successor_record_errors(qa, readback), [])
        for record, field in (("qa", "science_runs"), ("readback", "proofs_replayed_by_this_reviewer"),
                              ("readback", "scientific_sources_changed_by_this_reviewer"),
                              ("readback", "methodology_new_reading_or_science_credit")):
            changed_qa, changed_readback = deepcopy(qa), deepcopy(readback)
            (changed_qa if record == "qa" else changed_readback)[field] = True if field != "methodology_new_reading_or_science_credit" else 1
            self.assertIn("report-v2-retrospective-execution-scope", self.successor_record_errors(changed_qa, changed_readback))
        changed = deepcopy(qa)
        changed["source_review"]["included_record"]["sha256"] = self.aliases[self.V2_READBACK_ALIAS]["original_sha256"]
        self.assertIn("report-v2-qa-identity:source_review", self.successor_record_errors(changed, readback))
        changed = deepcopy(qa)
        changed["source"]["included_record"]["sha256"] = self.aliases[self.PRIMARY_ALIASES[0]]["public_sha256"]
        self.assertIn("report-v2-qa-identity:source", self.successor_record_errors(changed, readback))
        for field in ("predecessor_15_result_objects_raw_json_preserved",
                      "current_1434_philosophical_section_verbatim_preserved"):
            changed = deepcopy(readback)
            changed[field] = False
            self.assertIn("report-v2-historical-preservation-scope", self.successor_record_errors(qa, changed))
        self.assertEqual((qa["authored_records_exact"], qa["native_numbered_items"],
                          qa["relative_references_as_exact_labels_and_literal_paths"], qa["page_count"]), (140, 12, 9, 14))
        self.assertEqual(len(qa["pages"]), 14)
        self.assertTrue(all(p["original_body_included"] is False for p in qa["pages"]))
        self.assertTrue(all(qa[k]["original_body_included"] is False
                            for k in ("source_finalisation", "content_qa", "build_receipt")))
        bindings = readback["source_bindings"]
        included = [b["included_projection"] for b in bindings if "included_projection" in b]
        omitted = [b for b in bindings if b["historical_original"].get("body_included") is False]
        self.assertEqual((len(bindings), len(included), len(omitted)), (20, 18, 2))
        for binding in included:
            row = self.aliases[binding["owner_archive_path"]]
            self.assertEqual((binding["sha256"], binding["bytes"]), (row["public_sha256"], row["public_bytes"]))
        altered = deepcopy(self.cross)
        altered["sources"]["fixture-v2-owner-word"] = {
            "path": qa["document"]["included_record"]["owner_archive_path"],
            "sha256": qa["document"]["included_record"]["sha256"], "read_scope": "Unavailable owner-only Word control."}
        candidate = next(w for w in altered["works"] if w["key"] == self.KEY)
        candidate["reading_forms"].append({"source": "fixture-v2-owner-word", "relationship": "retained-source-reading-projection"})
        self.assertIn("report-ordered-reading-forms", self.errors(altered, self.text))

    def section_body(self, text, heading):
        idx = self.mod.markdown_index(text)
        found = next((h for h in idx["headings"] if h[0] == heading), None)
        self.assertIsNotNone(found, heading)
        _, level, start = found
        end = next((h[2] for h in idx["headings"] if h[2] > start and h[1] <= level), idx["line_count"])
        return "".join(text.splitlines(True)[start:end])

    def test_expanded_catalogue_and_verification_reject_scoped_route_substitution(self):
        page = "docs/reader/PAPER-CATALOGUE.md"
        guide = "docs/reader/VERIFICATION-GUIDE.md"
        body = (ROOT / guide).read_text()
        works = {w["key"]: w for w in self.cross["works"]}
        source_targets = {(self.aliases[a]["public_path"], "") for a in self.SUCCESSOR_ALIASES + tuple(self.PRIMARY_ALIASES)}
        owners = {"t20-emergence-type-control", "t20-arabic-reading-methodology", "t20-drive-corpus-methodology",
                  "t20-math-utilisation-methodology", "t20-result-method-handoff", "t20-cooperation-context"}
        owner_targets = {(page, works[k]["catalogue_entry"].split("#", 1)[1]) for k in owners}
        for text, rel, heading, required in (
                (self.text, page, self.V2_CATALOGUE_HEADING, source_targets | owner_targets),
                (body, guide, self.V2_VERIFICATION_HEADING, source_targets)):
            reached = lambda value: self.section_targets(value, rel, heading)
            self.assertTrue(required <= reached(text), required - reached(text))
            for path, anchor in required:
                href = "#" + anchor if path == rel else ("../../" + path + ("#" + anchor if anchor else ""))
                changed = text.replace("(" + href + ")", "(PAPER-CATALOGUE.md)")
                self.assertNotEqual(changed, text)
                self.assertFalse(required <= reached(changed))
        index = self.mod.markdown_index(self.text)
        original = next(h for h in index["headings"] if h[0] == self.CATALOGUE_ANCHOR)
        expanded = next(h for h in index["headings"] if h[0] == self.V2_CATALOGUE_HEADING)
        self.assertGreater(expanded[1], original[1])
        self.assertIn(self.section_body(self.text, self.V2_CATALOGUE_HEADING), self.section_body(self.text, self.CATALOGUE_ANCHOR))

    def report_bridge_errors(self, section, references, expected_rows):
        errors = []
        for literal, row in zip(references, expected_rows):
            matches = [line for line in section.splitlines() if "`" + literal + "`" in line]
            if len(matches) != 1:
                errors.append("report-v2-bridge-row:" + literal)
                continue
            targets = [self.mod.resolve_reader_link(ROOT, "docs/reader/VERIFICATION-GUIDE.md", href)
                       for _, href in self.mod.markdown_index(matches[0])["links"]]
            if targets != [(row["public_path"], "")]:
                errors.append("report-v2-bridge-pair:" + literal)
        return errors

    def test_nine_literal_report_references_have_exact_public_bridge_rows(self):
        report = (ROOT / self.aliases[self.V2_ALIAS]["public_path"]).read_text()
        references = [href for _, href in self.mod.markdown_index(report)["links"] if href.startswith("../")]
        self.assertEqual(len(references), 9)
        expected_rows = [self.selected[i] for i in (233, 234, 231, 232, 213, 215, 219, 224, 254)]
        aliases = [posixpath.normpath(posixpath.join("t20/reports", href)) for href in references]
        self.assertEqual(aliases, [r["owner_archive_path"] for r in expected_rows])
        text = (ROOT / "docs/reader/VERIFICATION-GUIDE.md").read_text()
        section = self.section_body(text, self.V2_VERIFICATION_HEADING)
        reached = self.section_targets(text, "docs/reader/VERIFICATION-GUIDE.md", self.V2_VERIFICATION_HEADING)
        self.assertEqual(self.report_bridge_errors(section, references, expected_rows), [])
        for literal, row in zip(references, expected_rows):
            self.assertIn((row["public_path"], ""), reached)
            changed = section.replace("(../../" + row["public_path"] + ")", "(PAPER-CATALOGUE.md)")
            self.assertNotEqual(changed, section)
            self.assertIn("report-v2-bridge-pair:" + literal,
                          self.report_bridge_errors(changed, references, expected_rows))
        # Swapping two valid public targets preserves the complete target set;
        # each literal must still bind its own source on that same table row.
        first, second = ("(../../" + row["public_path"] + ")" for row in expected_rows[:2])
        changed = section.replace(first, "FIXTURE_BRIDGE_SWAP").replace(second, first).replace("FIXTURE_BRIDGE_SWAP", second)
        original_targets = {href for _, href in self.mod.markdown_index(section)["links"]}
        changed_targets = {href for _, href in self.mod.markdown_index(changed)["links"]}
        self.assertEqual(original_targets, changed_targets)
        errors = self.report_bridge_errors(changed, references, expected_rows)
        self.assertEqual(set(errors), {"report-v2-bridge-pair:" + literal for literal in references[:2]})

    def test_report_v2_keeps_historical_owner_counts_and_original_comprehension_tasks(self):
        readback = self.v2_readback
        self.assertTrue(readback["predecessor_15_result_objects_raw_json_preserved"])
        self.assertTrue(readback["current_1434_philosophical_section_verbatim_preserved"])
        # Existing source-owned ledger tests establish the fifteen frozen rows,
        # proposed sixteenth control and present native owner separately.
        self.assertEqual(len(ResultLedgerMethodologyRoutesTests.OWNER_WORKS), 15)
        guide = (ROOT / "docs/reader/VERIFICATION-GUIDE.md").read_text()
        section = self.section_body(guide, self.V2_VERIFICATION_HEADING)
        targets = self.section_targets(guide, "docs/reader/VERIFICATION-GUIDE.md", self.V2_VERIFICATION_HEADING)
        self.assertIn(("docs/provenance/v5-successors/RESULT_STATUS.json", ""), targets)
        # Unavailable images and author-reported page checks cannot become a
        # new curation render or a scientific execution claim.
        self.assertTrue("author-reported" in section.lower() or "author reported" in section.lower())
        tasks = self.section_body(guide, "independent-reader-comprehension-tasks-for-the-final-candidate")
        # section_body includes the trailing blank line before the next peer
        # heading. The frozen protocol digest uses that same slice convention.
        self.assertEqual(hashlib.sha256(tasks.encode()).hexdigest(),
                         "b45ff7603fbeb4e701d4b86f7aa65f66ea3044722986525ed68042f61e16ba28")

    def ledger_ownership_errors(self, original, successor, native):
        errors = []
        if (len(original["results"]) != 15 or len(successor["results"]) != 16
                or successor["results"][:15] != original["results"]
                or successor["counting_boundary"]["t20_native_result_owners_at_capture"] != 15
                or successor["counting_boundary"]["late_proposed_owners"] != 1):
            errors.append("report-v2-historical-owner-count")
        late = successor["results"][-1]
        captured = late["fresh_and_inherited"]["receiving_native_status"]
        if (late["result_id"] != "T20-EMERGENCE-TYPE-CONTROL"
                or late["registration_state"] != "PROPOSED_OWNER_NATIVE_ADMISSION_PENDING"
                or captured["registration"] != "NOT_REGISTERED_AT_CAPTURE"
                or captured["independent_evidence_count"] is not None
                or native["research_disposition"] != "CANDIDATE"
                or native["fresh_evidence"] != "NOT_RUN" or native["independent_evidence_count"] != 0):
            errors.append("report-v2-captured-current-owner-conflation")
        return errors

    def test_fifteen_historical_owners_and_proposed_control_reject_currentness_conflation(self):
        prefix = "t20/methodology/result-ledger/"
        def record(alias):
            return json.loads((ROOT / self.aliases[alias]["public_path"]).read_text())
        original = record(prefix + "RESULT_EVIDENCE_LEDGER.json")
        successor = record(prefix + "RESULT_EVIDENCE_LEDGER_v2.json")
        statuses = json.loads((ROOT / "docs/provenance/v5-successors/RESULT_STATUS.json").read_text())["statuses"]
        native = next(s for s in statuses if s["id"] == "T20-EMERGENCE-TYPE-CONTROL")
        self.assertEqual(self.ledger_ownership_errors(original, successor, native), [])
        changed = deepcopy(successor)
        changed["counting_boundary"]["t20_native_result_owners_at_capture"] = 16
        self.assertIn("report-v2-historical-owner-count", self.ledger_ownership_errors(original, changed, native))
        changed = deepcopy(successor)
        changed["results"][-1]["fresh_and_inherited"]["receiving_native_status"]["independent_evidence_count"] = 0
        self.assertIn("report-v2-captured-current-owner-conflation", self.ledger_ownership_errors(original, changed, native))
        changed_native = deepcopy(native)
        changed_native["fresh_evidence"] = "PASS"
        self.assertIn("report-v2-captured-current-owner-conflation", self.ledger_ownership_errors(original, successor, changed_native))
        changed_native = deepcopy(native)
        changed_native["research_disposition"] = "HISTORICAL"
        self.assertIn("report-v2-captured-current-owner-conflation", self.ledger_ownership_errors(original, successor, changed_native))


class LateResultLedgerSupportTests(unittest.TestCase):
    """A successor documentary case supports the already-owned typed control."""
    GROUP = TwentiethFormalWorkTests.GROUP
    KEY = "t20-emergence-type-control"
    RESULT_ID = "T20-EMERGENCE-TYPE-CONTROL"
    PART = "result-ledger-v2"
    PREFIX = "t20/methodology/result-ledger/"
    NOTE_ALIAS = PREFIX + "RESULT_EVIDENCE_SUCCESSOR_NOTE_v2.md"
    LEDGER_ALIAS = PREFIX + "RESULT_EVIDENCE_LEDGER_v2.json"
    ORIGINAL_ALIAS = PREFIX + "RESULT_EVIDENCE_LEDGER.json"
    EXPECTED = {KEY: ("research-note", {"ontology", PART},
                     LateTwentiethContextRoutesTests.EXPECTED[KEY][2])}
    CATALOGUE_HEADING = "late-evidence-handoff-for-the-typed-emergence-control"
    VERIFICATION_HEADING = "checking-the-late-result-evidence-handoff"
    section_targets = MethodologyRoutesMixin.section_targets

    @classmethod
    def setUpClass(cls):
        LateTwentiethContextRoutesTests.setUpClass.__func__(cls)
        owners = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json").read_text())
        def original(path):
            return json.loads(subprocess.check_output(
                ["git", "show", owners["baseline"]["commit"] + ":" + path], cwd=ROOT))
        cls.original_ledger = original(cls.aliases[cls.ORIGINAL_ALIAS]["public_path"])
        cls.successor = original(cls.aliases[cls.LEDGER_ALIAS]["public_path"])
        cls.bindings = original(cls.aliases[cls.PREFIX + "SOURCE_BINDINGS_v2.json"]["public_path"])
        native = original("docs/provenance/v5-successors/RESULT_STATUS.json")
        cls.native_status = next(r for r in native["statuses"] if r["id"] == cls.RESULT_ID)

    def errors(self, cross, text):
        errors = LateTwentiethContextRoutesTests.errors(self, cross, text)
        work = next((w for w in cross["works"] if w["key"] == self.KEY), None)
        if work is None:
            return errors
        primaries = {self.aliases[a]["public_path"] for a in self.EXPECTED[self.KEY][2]}
        paths = lambda keys: {cross["sources"][s]["path"] for s in keys}
        if paths(work["source_keys"]) != primaries:
            errors.append("late-control-primary-components")
        if paths(f["source"] for f in work.get("reading_forms", [])) != primaries or any(
                f["relationship"] != "retained-source-reading-projection" for f in work["reading_forms"]):
            errors.append("late-control-reading-forms")
        result_owners = [w["key"] for w in cross["works"]
                         if self.RESULT_ID in w.get("existing_result_ids", [])]
        if work["existing_result_ids"] != [self.RESULT_ID] or result_owners != [self.KEY]:
            errors.append("late-control-result-credit")
        selected = [r for r in self.selected if r["part"] == self.PART]
        support = paths(work.get("supporting_source_keys", []))
        if not {r["public_path"] for r in selected} <= support:
            errors.append("late-support-coverage")
        for row in selected:
            for key in work.get("supporting_source_keys", []):
                source = cross["sources"][key]
                if source["path"] == row["public_path"] and source["sha256"] != row["public_sha256"]:
                    errors.append("late-support-identity:" + row["owner_archive_path"])
        late_paths = {r["public_path"] for r in selected}
        for candidate in cross["works"]:
            if late_paths & paths(candidate["source_keys"] +
                                  [f["source"] for f in candidate.get("reading_forms", [])]):
                errors.append("late-support-promoted-to-work")
        return errors

    def test_complete_successor_family_supports_the_existing_control(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        selected = [r for r in self.selected if r["part"] == self.PART]
        self.assertEqual(len(selected), 4)
        self.assertEqual({r["selection_layer"] for r in selected}, {"methodology-successors"})
        for field, value, error in [
                ("role", "supporting-reference", "role:" + self.KEY),
                ("existing_result_ids", [], "late-control-result-credit")]:
            altered = deepcopy(self.cross)
            next(w for w in altered["works"] if w["key"] == self.KEY)[field] = value
            self.assertIn(error, self.errors(altered, self.text))

    def test_each_support_identity_and_nonprimary_role_are_required(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        for row in [r for r in self.selected if r["part"] == self.PART]:
            with self.subTest(alias=row["owner_archive_path"]):
                key = next(k for k,v in self.cross["sources"].items() if v["path"] == row["public_path"])
                altered = deepcopy(self.cross)
                work = next(w for w in altered["works"] if w["key"] == self.KEY)
                work["supporting_source_keys"].remove(key)
                self.assertIn("late-support-coverage", self.errors(altered, self.text))
                altered = deepcopy(self.cross)
                altered["sources"][key]["sha256"] = "0" * 64
                self.assertIn("late-support-identity:" + row["owner_archive_path"], self.errors(altered, self.text))
                for field in ["source_keys", "reading_forms"]:
                    altered = deepcopy(self.cross)
                    work = next(w for w in altered["works"] if w["key"] == self.KEY)
                    work[field].append(key if field == "source_keys" else {
                        "source": key, "relationship": "retained-source-reading-projection"})
                    self.assertIn("late-support-promoted-to-work", self.errors(altered, self.text))
                altered = deepcopy(self.cross)
                duplicate = deepcopy(next(w for w in altered["works"] if w["key"] == self.KEY))
                duplicate.update({"key": "fixture-inflated-successor", "title": "Fixture duplicated documentary support",
                                  "role": "supporting-reference", "source_keys": [key], "reading_forms": [],
                                  "supporting_source_keys": [], "existing_result_ids": []})
                altered["works"].append(duplicate)
                self.assertIn("late-support-promoted-to-work", self.errors(altered, self.text))

    def test_frozen_rows_and_captured_receiving_absence_keep_their_owners(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        old = self.original_ledger["results"]
        self.assertEqual(len(old), 15)
        self.assertEqual(self.successor["results"][:15], old)
        self.assertEqual(len(self.successor["results"]), 16)
        late = self.successor["results"][-1]
        self.assertEqual(late["result_id"], self.RESULT_ID)
        self.assertEqual(late["registration_state"], "PROPOSED_OWNER_NATIVE_ADMISSION_PENDING")
        self.assertEqual(self.successor["counting_boundary"]["t20_native_result_owners_at_capture"], 15)
        self.assertEqual(self.successor["counting_boundary"]["late_proposed_owners"], 1)
        captured = late["fresh_and_inherited"]["receiving_native_status"]
        self.assertEqual(captured["registration"], "NOT_REGISTERED_AT_CAPTURE")
        self.assertIsNone(captured["independent_evidence_count"])
        self.assertEqual(self.native_status["fresh_evidence"], "NOT_RUN")
        self.assertEqual(self.native_status["independent_evidence_count"], 0)
        self.assertIn(self.RESULT_ID, self.claims)
        case = self.successor["late_cross_stream_case"]
        self.assertEqual(case["case_id"], "OTC-X01")
        self.assertTrue(case["new_primary_reading"] and case["new_kernel_replay"])
        self.assertFalse(case["new_primary_reading_by_this_ledger_assembler"])
        self.assertFalse(case["new_kernel_replay_by_this_ledger_assembler"])
        works = {w["key"]: w for w in self.cross["works"]}
        for result in old:
            result_id = result["result_id"]
            self.assertIn(result_id, works[ResultLedgerMethodologyRoutesTests.OWNER_WORKS[result_id]]["existing_result_ids"])
        # Documentary aliases preserve nineteen included paths, not 23 bodies.
        inputs = self.bindings["late_input_bindings"]
        included = [r["included_projection"] for r in inputs if "included_projection" in r]
        omitted = [r for r in inputs if r.get("body_included") is False]
        self.assertEqual((len(inputs), len(included), len({r["owner_archive_path"] for r in included}), len(omitted)),
                         (23, 21, 19, 2))
        for row in included:
            source = self.aliases[row["owner_archive_path"]]
            self.assertEqual((row["sha256"], row["bytes"]), (source["public_sha256"], source["public_bytes"]))

    def required_catalogue_targets(self):
        page = "docs/reader/PAPER-CATALOGUE.md"
        note = self.aliases[self.NOTE_ALIAS]["public_path"]
        required = {(note, a) for a in ["what-changed", "new-source-credit-and-its-limit", "evidence-and-receiving-boundary"]}
        required |= {(r["public_path"], "") for r in self.selected if r["part"] == self.PART and r["owner_archive_path"] != self.NOTE_ALIAS}
        works = {w["key"]: w for w in self.cross["works"]}
        peers = [self.KEY, "t20-result-method-handoff", "t20-arabic-reading-methodology",
                 "t20-divine-action-context", "t20-cooperation-context"]
        peers += [ResultLedgerMethodologyRoutesTests.OWNER_WORKS[result_id]
                  for result_id in self.successor["late_application_scope_overlay"]["existing_result_ids"]]
        required |= {(page, works[k]["catalogue_entry"].split("#", 1)[1]) for k in peers}
        required |= {(self.GROUP + "/CONTEXT_SOURCE_INDEX.json", ""),
                     (self.GROUP + "/LATE_RESULT_MAP.json", ""),
                     ("docs/provenance/v5-successors/RESULT_STATUS.json", "")}
        for alias in ["t20/ontology-type-control/ACT_PRODUCT_CONTEXT.json",
                      "t20/ontology-type-control/SOURCE_BINDINGS.json",
                      "t20/ontology-type-control/EXECUTION_RECEIPT.json",
                      "t20/ontology-type-control/review/EXECUTION_RECEIPT.json",
                      "t20/ontology-type-control/review/SOURCE_BINDINGS.json",
                      "t20/ontology-type-control/review/REVIEW.json"]:
            required.add((self.aliases[alias]["public_path"], ""))
        return required

    def test_scoped_catalogue_exposes_the_delta_case_overlay_and_status_owners(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        page = "docs/reader/PAPER-CATALOGUE.md"
        required = self.required_catalogue_targets()
        reached = lambda text: self.section_targets(text, page, self.CATALOGUE_HEADING)
        self.assertTrue(required <= reached(self.text))
        for path, anchor in required:
            with self.subTest(path=path, anchor=anchor):
                href = ("#" + anchor if path == page else
                        "../provenance/v5-successors/RESULT_STATUS.json" if path.startswith("docs/provenance/") else
                        "../../" + path + ("#" + anchor if anchor else ""))
                changed = self.text.replace("(" + href + ")", "(VERIFICATION-GUIDE.md)")
                self.assertNotEqual(changed, self.text)
                self.assertFalse(required <= reached(changed))

    def test_verification_keeps_historical_pending_and_present_ownership_separate(self):
        self.assertEqual(self.errors(self.cross, self.text), [])
        page = "docs/reader/VERIFICATION-GUIDE.md"
        text = (ROOT / page).read_text()
        required = {(self.aliases[self.NOTE_ALIAS]["public_path"], "evidence-and-receiving-boundary"),
                    (self.aliases[self.LEDGER_ALIAS]["public_path"], ""),
                    (self.aliases[self.ORIGINAL_ALIAS]["public_path"], ""),
                    ("docs/reader/PAPER-CATALOGUE.md", self.CATALOGUE_HEADING),
                    (self.GROUP + "/CONTEXT_SOURCE_INDEX.json", ""),
                    (self.GROUP + "/LATE_RESULT_MAP.json", ""),
                    ("docs/provenance/v5-successors/RESULT_STATUS.json", "")}
        reached = lambda body: self.section_targets(body, page, self.VERIFICATION_HEADING)
        self.assertTrue(required <= reached(text))
        for path, anchor in required:
            href = ("PAPER-CATALOGUE.md#" + anchor if path == "docs/reader/PAPER-CATALOGUE.md" else
                    "../provenance/v5-successors/RESULT_STATUS.json" if path.startswith("docs/provenance/") else
                    "../../" + path + ("#" + anchor if anchor else ""))
            changed = text.replace("(" + href + ")", "(PAPER-CATALOGUE.md)")
            self.assertNotEqual(changed, text)
            self.assertFalse(required <= reached(changed))

class SourceReadingGuideRoutesTests(unittest.TestCase):
    """One guide, two dated reading editions; documentary scope is not science."""
    GROUP = TwentiethFormalWorkTests.GROUP
    KEY = "t20-source-reading-guide"
    ORIGINAL = "t20/reading/GUIDE.md"
    V2 = "t20/reading/GUIDE_v2.md"
    QA = "t20/reports/GUIDE_v2_QA_MANIFEST.json"
    REVIEW_MD = "t20/reports/REPORT_GUIDE_V2_READBACK.md"
    REVIEW = "t20/reports/REPORT_GUIDE_V2_READBACK.json"
    CURRENT = "t20/reports/CURRENT_DOCUMENTS_v2.json"
    INDEX = "t20/reading/READING_INDEX.json"
    QUESTIONS = "t20/reading/SPECIALIST_REVIEW_QUESTIONS.md"
    SUPPORT = (V2, QA, REVIEW_MD, REVIEW, CURRENT, INDEX)
    TAIL = (QUESTIONS, "t20/reading/READING_INDEX_VALIDATION.json",
            "t20/reports/GUIDE_QA_MANIFEST.json", "t20/reports/FINAL_DOCUMENTS.json")
    NEW = (V2, QA, CURRENT)
    CATALOGUE = "the-twentieth-source-guide-and-its-expanded-reading-edition"
    VERIFICATION = "checking-the-source-guide-editions-and-reading-boundaries"
    RELATION = "expanded-reading-edition-preserves-dated-assessment"
    OWNER_KEYS = ("t20-arabic-reading-methodology", "t20-drive-corpus-methodology",
                  "t20-math-utilisation-methodology", "t20-result-method-handoff",
                  "t20-emergence-type-control", "t20-divine-action-context",
                  "t20-cooperation-context", "t20-final-research-report",
                  "t20-mathematical-companion")
    setUpClass = classmethod(LateTwentiethContextRoutesTests.setUpClass.__func__)
    section_targets = MethodologyRoutesMixin.section_targets
    section_body = FinalReportRoutesTests.section_body
    source_key = FinalReportRoutesTests.source_key

    def record(self, alias):
        return json.loads((ROOT / self.aliases[alias]["public_path"]).read_text())

    def work(self, cross):
        return next((w for w in cross["works"] if w["key"] == self.KEY), None)

    def guide_errors(self, cross):
        errors = []
        work = self.work(cross)
        if work is None:
            return ["guide-missing-work"]
        keys = [self.source_key(a) for a in self.SUPPORT] + ["t20-context-50e3ae6b35c1b914"]
        keys += [self.source_key(a) for a in self.TAIL]
        if work.get("role") != "supporting-reference" or work.get("existing_result_ids") != []:
            errors.append("guide-role-or-result-credit")
        if work.get("source_keys") != [self.source_key(self.ORIGINAL)]:
            errors.append("guide-original-primary")
        forms = [{"source": self.source_key(a), "relationship": "retained-source-reading-projection"}
                 for a in (self.ORIGINAL, self.V2)]
        if work.get("reading_forms") != forms:
            errors.append("guide-ordered-editions")
        if work.get("supporting_source_keys") != keys:
            errors.append("guide-finite-ordered-support")
        for alias in (self.ORIGINAL,) + self.SUPPORT + self.TAIL:
            row = self.aliases[alias]
            key = self.source_key(alias)
            source = cross["sources"].get(key)
            if (source is None or source.get("path") != row["public_path"]
                    or source.get("sha256") != row["public_sha256"] or not source.get("read_scope")):
                errors.append("guide-source-identity:" + alias)
            if [k for k, s in cross["sources"].items() if s.get("path") == row["public_path"]] != [key]:
                errors.append("guide-source-alias:" + alias)
        editions = {self.aliases[a]["public_path"] for a in (self.ORIGINAL, self.V2)}
        documentary = {self.aliases[a]["public_path"] for a in
                       (self.QA, self.REVIEW_MD, self.REVIEW, self.CURRENT, self.INDEX) + self.TAIL}
        for candidate in cross["works"]:
            paths = {cross["sources"].get(k, {}).get("path") for k in candidate.get("source_keys", [])}
            paths |= {cross["sources"].get(f.get("source"), {}).get("path") for f in candidate.get("reading_forms", [])}
            if candidate["key"] != self.KEY and editions & paths:
                errors.append("guide-duplicate-edition")
            if documentary & paths:
                errors.append("guide-documentary-primary")
        expected = {"from": self.source_key(self.ORIGINAL), "to": self.source_key(self.V2),
                    "kind": self.RELATION, "basis": self.source_key(self.REVIEW)}
        relations = [r for r in cross["relations"] if r.get("from") == expected["from"] and r.get("to") == expected["to"]]
        if relations != [expected]:
            errors.append("guide-successor-relation")
        for owner, aliases in (("t20-cooperation-context", (self.ORIGINAL, self.INDEX)),
                               ("t20-arabic-reading-methodology", (self.INDEX,)),
                               ("t20-final-research-report", (self.REVIEW_MD, self.REVIEW))):
            existing = next(w for w in cross["works"] if w["key"] == owner)
            if not {self.source_key(a) for a in aliases} <= set(existing.get("supporting_source_keys", [])):
                errors.append("guide-existing-support:" + owner)
        return errors

    def required_routes(self):
        page = "docs/reader/PAPER-CATALOGUE.md"
        works = {w["key"]: w for w in self.cross["works"]}
        targets = {(self.aliases[a]["public_path"], "") for a in (self.ORIGINAL,) + self.SUPPORT + self.TAIL}
        targets |= {(page, works[k]["catalogue_entry"].split("#", 1)[1]) for k in self.OWNER_KEYS}
        targets |= {(page, "late-evidence-handoff-for-the-typed-emergence-control"),
                    (self.GROUP + "/CONTEXT_SOURCE_INDEX.json", "")}
        return targets

    def test_one_reference_has_exact_editions_support_and_preserved_existing_edges(self):
        self.assertEqual(self.guide_errors(self.cross), [])

    def test_missing_work_role_credit_forms_and_support_reject_mutation(self):
        self.assertEqual(self.guide_errors(self.cross), [])
        changed = deepcopy(self.cross)
        changed["works"] = [w for w in changed["works"] if w["key"] != self.KEY]
        self.assertIn("guide-missing-work", self.guide_errors(changed))
        for field, value, error in (("role", "research-note", "guide-role-or-result-credit"),
                ("existing_result_ids", ["T20-EMERGENCE-TYPE-CONTROL"], "guide-role-or-result-credit"),
                ("existing_result_ids", ["T20-INVENTED-GUIDE-RESULT"], "guide-role-or-result-credit"),
                ("source_keys", [self.source_key(self.V2)], "guide-original-primary"),
                ("reading_forms", list(reversed(self.work(self.cross)["reading_forms"])), "guide-ordered-editions")):
            changed = deepcopy(self.cross)
            self.work(changed)[field] = value
            self.assertIn(error, self.guide_errors(changed))
        for key in self.work(self.cross)["supporting_source_keys"]:
            changed = deepcopy(self.cross)
            self.work(changed)["supporting_source_keys"].remove(key)
            self.assertIn("guide-finite-ordered-support", self.guide_errors(changed))

    def test_exact_public_bindings_reject_wrong_existing_source_and_alias_copy(self):
        self.assertEqual(self.guide_errors(self.cross), [])
        for alias in (self.ORIGINAL,) + self.SUPPORT + self.TAIL:
            key = self.source_key(alias)
            for field, value in (("path", self.aliases["t20/reports/REPORT_v2.md"]["public_path"]),
                                 ("sha256", "0" * 64), ("read_scope", "")):
                changed = deepcopy(self.cross)
                changed["sources"][key][field] = value
                self.assertIn("guide-source-identity:" + alias, self.guide_errors(changed))
            changed = deepcopy(self.cross)
            changed["sources"]["fixture-guide-alias"] = deepcopy(changed["sources"][key])
            self.assertIn("guide-source-alias:" + alias, self.guide_errors(changed))

    def test_duplicate_editions_and_documentary_credit_cannot_hide_under_aliases(self):
        self.assertEqual(self.guide_errors(self.cross), [])
        for alias in (self.ORIGINAL,) + self.SUPPORT + self.TAIL:
            for field in ("source_keys", "reading_forms"):
                changed = deepcopy(self.cross)
                key = self.source_key(alias)
                changed["sources"]["fixture-guide-alias"] = deepcopy(changed["sources"][key])
                duplicate = deepcopy(self.work(changed))
                duplicate.update(key="fixture-guide-credit", source_keys=[], reading_forms=[], supporting_source_keys=[])
                duplicate[field] = ["fixture-guide-alias"] if field == "source_keys" else [
                    {"source": "fixture-guide-alias", "relationship": "retained-source-reading-projection"}]
                changed["works"].append(duplicate)
                error = "guide-duplicate-edition" if alias in (self.ORIGINAL, self.V2) else "guide-documentary-primary"
                self.assertIn(error, self.guide_errors(changed))
        for mutation in ("remove", "kind", "basis", "duplicate"):
            changed = deepcopy(self.cross)
            relation = next(r for r in changed["relations"] if r.get("from") == self.source_key(self.ORIGINAL)
                            and r.get("to") == self.source_key(self.V2))
            if mutation == "remove":
                changed["relations"].remove(relation)
            elif mutation == "duplicate":
                changed["relations"].append(deepcopy(relation))
            else:
                relation[mutation] = "unqualified-successor" if mutation == "kind" else self.source_key(self.QA)
            self.assertIn("guide-successor-relation", self.guide_errors(changed))

    def test_catalogue_and_verification_route_every_identity_and_existing_owner(self):
        required = self.required_routes()
        for page, heading in (("docs/reader/PAPER-CATALOGUE.md", self.CATALOGUE),
                              ("docs/reader/VERIFICATION-GUIDE.md", self.VERIFICATION)):
            text = (ROOT / page).read_text()
            reached = lambda body: self.section_targets(body, page, heading)
            self.assertTrue(required <= reached(text), required - reached(text))
            for target in required:
                changed_lines = []
                for line in text.splitlines(True):
                    changed = line
                    for _, href in self.mod.markdown_index(line)["links"]:
                        if self.mod.resolve_reader_link(ROOT, page, href) == target:
                            changed = changed.replace("(" + href + ")", "(RESULT-INDEX.md)")
                    changed_lines.append(changed)
                changed = "".join(changed_lines)
                self.assertNotEqual(changed, text)
                self.assertFalse(required <= reached(changed), target)

    def bridge_errors(self, section, references):
        errors = []
        for literal in dict.fromkeys(references):
            alias = posixpath.normpath(posixpath.join("t20/reading", literal))
            row = self.aliases[alias]
            matches = [line for line in section.splitlines() if "`" + literal + "`" in line]
            targets = [] if len(matches) != 1 else [self.mod.resolve_reader_link(
                ROOT, "docs/reader/VERIFICATION-GUIDE.md", href)
                for _, href in self.mod.markdown_index(matches[0])["links"]]
            if targets != [(row["public_path"], "")]:
                errors.append("guide-bridge:" + literal)
        return errors

    def test_eleven_relative_occurrences_have_ten_exact_paired_bridge_rows(self):
        source = (ROOT / self.aliases[self.V2]["public_path"]).read_text()
        references = [href for _, href in self.mod.markdown_index(source)["links"] if not href.startswith(("http:", "https:", "#"))]
        self.assertEqual((len(references), len(set(references)), references.count("READING_INDEX.json")), (11, 10, 2))
        text = (ROOT / "docs/reader/VERIFICATION-GUIDE.md").read_text()
        section = self.section_body(text, self.VERIFICATION)
        self.assertEqual(self.bridge_errors(section, references), [])
        rows = [self.aliases[posixpath.normpath(posixpath.join("t20/reading", literal))]
                for literal in dict.fromkeys(references)]
        for literal, row in zip(dict.fromkeys(references), rows):
            changed = section.replace("(../../" + row["public_path"] + ")", "(PAPER-CATALOGUE.md)")
            self.assertNotEqual(changed, section)
            self.assertIn("guide-bridge:" + literal, self.bridge_errors(changed, references))
        first, second = ["(../../" + row["public_path"] + ")" for row in rows[:2]]
        changed = section.replace(first, "FIXTURE_GUIDE_SWAP").replace(second, first).replace("FIXTURE_GUIDE_SWAP", second)
        self.assertEqual({href for _, href in self.mod.markdown_index(section)["links"]},
                         {href for _, href in self.mod.markdown_index(changed)["links"]})
        self.assertEqual(set(self.bridge_errors(changed, references)),
                         {"guide-bridge:" + literal for literal in list(dict.fromkeys(references))[:2]})

    def projection(self, alias):
        row = self.aliases[alias]
        return {"owner_archive_path": alias, "sha256": row["public_sha256"], "bytes": row["public_bytes"]}

    def record_errors(self, qa, current, review):
        errors = []
        if qa["schema"] != "t20-successor-guide-document-qa-v2":
            errors.append("guide-qa-schema")
        for field, alias in (("source", self.V2), ("source_review", self.REVIEW)):
            if qa[field]["included_record"] != self.projection(alias):
                errors.append("guide-qa-public:" + field)
        if (qa["source_review"]["historical_original_identity"]["sha256"] != self.aliases[self.REVIEW]["original_sha256"]
                or qa["original_document_record_sha256"] != self.aliases[self.QA]["original_sha256"]):
            errors.append("guide-original-public-distinction")
        expected_counts = (255, 20, 11, 62, 20)
        if tuple(qa[k] for k in ("authored_records_exact", "external_hyperlinks_exact",
                "relative_references_as_exact_labels_and_literal_paths", "arabic_codepoints_exact_in_source_order", "page_count")) != expected_counts:
            errors.append("guide-document-counts")
        if (len(qa["pages"]) != 20 or any(p["original_body_included"] is not False for p in qa["pages"])
                or qa["render_route"]["qa_only_pdf"]["original_body_included"] is not False):
            errors.append("guide-render-body-limit")
        if (qa["source_edited"] is not False or qa["scientific_replay"] is not False
                or current["scientific_replay"] is not False or current["qa_renders_selected_for_delivery"] is not False
                or review["methodology_new_reading_or_science_credit"] != 0
                or review["proofs_replayed_by_this_reviewer"] is not False
                or review["scientific_sources_changed_by_this_reviewer"] is not False):
            errors.append("guide-retrospective-science-scope")
        if review["current_1434_philosophical_section_verbatim_preserved"] is not True:
            errors.append("guide-dated-appraisal")
        if tuple(review[k] for k in ("ontology_author_theorems", "ontology_author_selected_readbacks",
                "ontology_author_semantic_rejections", "ontology_reviewer_probes",
                "ontology_final_review_bound_files_verified")) != (9, 7, 2, 7, 26):
            errors.append("guide-separately-dated-ontology-credit")
        roles = current["current_documents"]
        if current["schema"] != "t20-current-three-role-documents-v2":
            errors.append("guide-current-schema")
        expected_roles = [("research report", "current v2 successor"),
                          ("source and reading guide", "current v2 successor"),
                          ("mathematical companion", "current unchanged mathematical v2")]
        if [(r["role"], r["status"]) for r in roles] != expected_roles:
            errors.append("guide-document-role-selection")
        if [r["page_count"] for r in roles] != [14, 20, 19] or current["total_current_pages"] != 53:
            errors.append("guide-current-document-pages")
        qa_roles = {"research report": "t20/reports/REPORT_v2_QA_MANIFEST.json",
                    "source and reading guide": self.QA,
                    "mathematical companion": "t20/reports/MATHEMATICAL_COMPANION_QA.json"}
        for row in roles:
            alias = qa_roles.get(row["role"])
            if (alias is None or row["qa"]["included_record"] != self.projection(alias)
                    or row["qa"]["historical_original_identity"]["sha256"] != self.aliases[alias]["original_sha256"]):
                errors.append("guide-current-role-qa")
        for role, alias in (("research report", "t20/reports/REPORT_v2.md"), ("source and reading guide", self.V2)):
            rows = [r for r in roles if r["role"] == role]
            if len(rows) != 1 or rows[0]["source"]["included_record"] != self.projection(alias):
                errors.append("guide-current-source:" + role)
        guides = [r for r in roles if r["role"] == "source and reading guide"]
        if len(guides) == 1:
            guide = guides[0]
            if (guide["qa"]["included_record"] != self.projection(self.QA)
                    or guide["qa"]["historical_original_identity"]["sha256"] != self.aliases[self.QA]["original_sha256"]):
                errors.append("guide-current-qa-identity")
            if guide["document"] != qa["document"]:
                errors.append("guide-owner-word-identity")
        if [(r["role"], r["status"]) for r in current["retained_historical_documents"]] != [
                ("research report", "retained historical v1"), ("source and reading guide", "retained historical v1")]:
            errors.append("guide-retained-history")
        return errors

    def test_document_qa_current_map_and_shared_review_have_distinct_mutable_controls(self):
        qa, current, review = self.record(self.QA), self.record(self.CURRENT), self.record(self.REVIEW)
        self.assertEqual(self.record_errors(qa, current, review), [])
        cases = [(0, ("schema",), "t20-successor-report-document-qa-v2", "guide-qa-schema"),
                 (0, ("source", "included_record"), self.projection("t20/reports/REPORT_v2.md"), "guide-qa-public:source"),
                 (0, ("source_review", "included_record", "sha256"), self.aliases[self.REVIEW]["original_sha256"], "guide-qa-public:source_review"),
                 (0, ("source_review", "historical_original_identity", "sha256"), self.aliases[self.REVIEW]["public_sha256"], "guide-original-public-distinction"),
                 (0, ("original_document_record_sha256",), self.aliases[self.QA]["public_sha256"], "guide-original-public-distinction"),
                 (0, ("pages", 0, "original_body_included"), True, "guide-render-body-limit"),
                 (1, ("current_documents", 1, "qa", "included_record", "sha256"), self.aliases[self.QA]["original_sha256"], "guide-current-qa-identity"),
                 (1, ("current_documents", 1, "source", "included_record"), self.projection("t20/reports/REPORT_v2.md"), "guide-current-source:source and reading guide"),
                 (1, ("current_documents", 2, "status"), "current v2 successor", "guide-document-role-selection"),
                 (1, ("current_documents", 1, "role"), "scientific result owner", "guide-document-role-selection"),
                 (1, ("current_documents", 2, "qa"), current["current_documents"][0]["qa"], "guide-current-role-qa"),
                 (1, ("schema",), "current-scientific-owner-admission", "guide-current-schema"),
                 (1, ("total_current_pages",), 54, "guide-current-document-pages"),
                 (1, ("retained_historical_documents", 1, "status"), "current v2 successor", "guide-retained-history"),
                 (2, ("current_1434_philosophical_section_verbatim_preserved",), False, "guide-dated-appraisal"),
                 (2, ("ontology_author_selected_readbacks",), 0, "guide-separately-dated-ontology-credit")]
        cases += [(0, (k,), 256, "guide-document-counts") for k in ("authored_records_exact", "external_hyperlinks_exact",
                   "relative_references_as_exact_labels_and_literal_paths", "arabic_codepoints_exact_in_source_order", "page_count")]
        cases += [(n, (k,), 1 if k == "methodology_new_reading_or_science_credit" else True, "guide-retrospective-science-scope")
                  for n, fields in ((0, ("source_edited", "scientific_replay")),
                                    (1, ("scientific_replay", "qa_renders_selected_for_delivery")),
                                    (2, ("methodology_new_reading_or_science_credit", "proofs_replayed_by_this_reviewer", "scientific_sources_changed_by_this_reviewer")))
                  for k in fields]
        for number, path, value, error in cases:
            records = [deepcopy(qa), deepcopy(current), deepcopy(review)]
            target = records[number]
            for part in path[:-1]:
                target = target[part]
            target[path[-1]] = value
            self.assertIn(error, self.record_errors(*records), path)

    def preservation_errors(self, original, revised):
        changes = difflib.SequenceMatcher(None, original.splitlines(True), revised.splitlines(True), autojunk=False).get_opcodes()
        errors = []
        if [op for op in changes if op[0] != "equal"] != [("replace", 8, 9, 8, 9), ("insert", 13, 13, 13, 29)]:
            errors.append("guide-v2-delta")
        preserved = sum(sum(map(len, original.splitlines(True)[i:j])) for op, i, j, _, _ in changes if op == "equal")
        if preserved != 63254:
            errors.append("guide-v2-preserved-bytes")
        heading = b"## Relation to the final judgement\n"
        def appraisal(body):
            start = body.index(heading)
            end = body.find(b"\n## ", start + len(heading))
            return body[start:] if end < 0 else body[start:end]
        if appraisal(original) != appraisal(revised):
            errors.append("guide-v2-appraisal")
        return errors

    def test_actual_guide_delta_and_shared_receipt_preserve_dated_appraisal(self):
        original = (ROOT / self.aliases[self.ORIGINAL]["public_path"]).read_bytes()
        revised = (ROOT / self.aliases[self.V2]["public_path"]).read_bytes()
        self.assertEqual(self.preservation_errors(original, revised), [])
        changed = revised.replace(b"I provisionally accept an actual Necessary Being.", b"I certify an actual Necessary Being.", 1)
        self.assertIn("guide-v2-appraisal", self.preservation_errors(original, changed))
        self.assertIn("guide-v2-preserved-bytes", self.preservation_errors(original, changed))
        receipt = self.record(self.REVIEW)["preservation"][1]
        self.assertEqual(receipt["baseline"]["included_projection"], self.projection(self.ORIGINAL))
        self.assertEqual(receipt["successor"]["included_projection"], self.projection(self.V2))
        self.assertEqual(receipt["allowed_replacement_baseline_line"], 9)
        self.assertEqual(receipt["changes"], [
            {"operation": "replace", "old_line_start": 9, "old_line_end": 9, "new_line_start": 9, "new_line_end": 9},
            {"operation": "insert", "old_line_start": 14, "old_line_end": 13, "new_line_start": 14, "new_line_end": 29}])

    def test_owner_primary_and_prepared_comprehension_protocol_are_preserved(self):
        owners = json.loads((ROOT / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json").read_text())
        self.assertEqual(owners["required_work_sources"].count(self.aliases[self.ORIGINAL]["public_path"]), 1)
        text = (ROOT / "docs/reader/VERIFICATION-GUIDE.md").read_text()
        tasks = self.section_body(text, "independent-reader-comprehension-tasks-for-the-final-candidate")
        self.assertEqual(hashlib.sha256(tasks.encode()).hexdigest(),
                         "b45ff7603fbeb4e701d4b86f7aa65f66ea3044722986525ed68042f61e16ba28")

    def index_scope_errors(self, index):
        """Only selected index fields; this does not claim reading its full body."""
        errors = []
        summary = index["final_scope_summary"]
        counts = ("source_work_entries", "completed_ordered_study_groups", "principal_return_points_in_ordered_groups",
                  "broader_return_points_in_ordered_groups", "witness_objects", "original_evidence_records",
                  "records_with_verified_public_aliases")
        if tuple(summary[k] for k in counts) != (13, 8, 42, 48, 42, 200, 132):
            errors.append("guide-index-distinct-count-units")
        if (summary["all_primary_reading_credit_remains_with_original_receipts"] is not True
                or summary["no_new_primary_reading_by_this_compilation"] is not True
                or index["public_projection"]["new_primary_reading_credit"] != 0
                or index["public_projection"]["source_body_selection"] is not False):
            errors.append("guide-index-compilation-not-body-admission")
        if (index["schema_version"] != 1 or index["status"] != "FINAL_COMPLETED_SOURCE_GUIDE_INDEX"
                or index["as_of_utc"] != "2026-10-07T14:49:59Z"
                or index["current_appraisal"]["as_of_utc"] != "2026-10-07T14:34:00Z"
                or index["current_appraisal"]["universal_source_mode"] != "Sufficient warrant withheld."):
            errors.append("guide-index-dated-scope")
        groups = ("DAR", "MINHAJ", "SAWAIQ", "SHIFA", "JAMI6", "MIFTAH", "NUBUWWAT", "SAFADIYYA")
        works = {w["id"]: w for w in index["works"]}
        if set(works) != set(groups) | {"ASBAHANI", "AKMALIYYA", "ALDA", "RICHARD", "ONENESS"}:
            errors.append("guide-index-groups-and-earlier-returns")
        bounded = {
            "ASBAHANI": "Bounded Twentieth rereading of the historically indexed volume",
            "RICHARD": "Selected comparison; not a whole-book study",
            "DAR": "Selected received bodies completed",
            "MINHAJ": "Selected received bodies completed",
            "SAWAIQ": "Entire selected received original electronic body completed; historical composition incomplete",
            "JAMI6": "All eighteen received treatises and modern contents traversed by mixed electronic and image reading; complete historical originals not claimed",
            "NUBUWWAT": "Entire selected received electronic body completed; bounded critical-edition controls only"}
        if any(works.get(key, {}).get("status") != status for key, status in bounded.items()):
            errors.append("guide-index-work-specific-body-limits")
        coordinates = index["coordinate_conventions"]
        if (coordinates["Dar8"] != "Stable V08-P0001–V08-P1873 paragraph IDs; exact character offsets in the recorded extraction, zero-based and end-exclusive."
                or coordinates["Dar9"] != "Physical newline numbers in the retained Islamicbook section text; not printed page labels."
                or coordinates["PDF"] != "One-based positions in the specifically hashed PDF; printed front matter and main-text sequences are named separately."):
            errors.append("guide-index-coordinate-units")
        return errors

    def test_targeted_index_fields_reject_group_body_credit_and_chronology_inflation(self):
        # These targeted fields support this guide's limited index use. No
        # completion inference is drawn from its empty pending_studies array.
        index = self.record(self.INDEX)
        self.assertEqual(self.index_scope_errors(index), [])
        cases = [(("final_scope_summary", "completed_ordered_study_groups"), 13, "guide-index-distinct-count-units"),
                 (("final_scope_summary", "source_work_entries"), 8, "guide-index-distinct-count-units"),
                 (("final_scope_summary", "all_primary_reading_credit_remains_with_original_receipts"), False, "guide-index-compilation-not-body-admission"),
                 (("public_projection", "source_body_selection"), True, "guide-index-compilation-not-body-admission"),
                 (("public_projection", "new_primary_reading_credit"), 1, "guide-index-compilation-not-body-admission"),
                 (("as_of_utc",), "2026-10-07T16:49:45Z", "guide-index-dated-scope"),
                 (("current_appraisal", "universal_source_mode"), "Accepted by current document selection", "guide-index-dated-scope"),
                 (("coordinate_conventions", "Dar9"), index["coordinate_conventions"]["PDF"], "guide-index-coordinate-units")]
        for path, value, error in cases:
            changed = deepcopy(index)
            target = changed
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            self.assertIn(error, self.index_scope_errors(changed), path)
        changed = deepcopy(index)
        next(w for w in changed["works"] if w["id"] == "RICHARD")["status"] = "Complete whole-book study"
        self.assertIn("guide-index-work-specific-body-limits", self.index_scope_errors(changed))

    def test_unavailable_owner_word_and_unselected_support_remain_outside_finite_forms(self):
        self.assertEqual(self.guide_errors(self.cross), [])
        qa = self.record(self.QA)
        changed = deepcopy(self.cross)
        changed["sources"]["fixture-owner-only-guide-word"] = {
            "path": qa["document"]["included_record"]["owner_archive_path"],
            "sha256": qa["document"]["included_record"]["sha256"],
            "read_scope": "Isolated unavailable owner-only Word admission control."}
        self.work(changed)["reading_forms"].append({"source": "fixture-owner-only-guide-word",
                                                   "relationship": "retained-source-reading-projection"})
        self.assertIn("guide-ordered-editions", self.guide_errors(changed))
        # The authorised four-document tail is now part of this finite support
        # contract. An extra report receipt or repeated existing support is not.
        for alias in ("t20/reports/REPORT_QA_MANIFEST.json", self.V2):
            changed = deepcopy(self.cross)
            self.work(changed)["supporting_source_keys"].append(self.source_key(alias))
            self.assertIn("guide-finite-ordered-support", self.guide_errors(changed))


class SourceGuideSupportTailTests(unittest.TestCase):
    """Finite historical support receipt controls, without replaying their claims."""
    GROUP = SourceReadingGuideRoutesTests.GROUP
    KEY = SourceReadingGuideRoutesTests.KEY
    TAIL = ("t20/reading/SPECIALIST_REVIEW_QUESTIONS.md",
            "t20/reading/READING_INDEX_VALIDATION.json",
            "t20/reports/GUIDE_QA_MANIFEST.json",
            "t20/reports/FINAL_DOCUMENTS.json")
    setUpClass = classmethod(LateTwentiethContextRoutesTests.setUpClass.__func__)
    source_key = FinalReportRoutesTests.source_key
    record = SourceReadingGuideRoutesTests.record
    work = SourceReadingGuideRoutesTests.work
    section_body = FinalReportRoutesTests.section_body
    ORIGINAL = SourceReadingGuideRoutesTests.ORIGINAL
    V2 = SourceReadingGuideRoutesTests.V2
    INDEX = SourceReadingGuideRoutesTests.INDEX
    CURRENT = SourceReadingGuideRoutesTests.CURRENT
    QUESTIONS, VALIDATION, QA, FINAL = TAIL
    QUESTION_PAIRS = (("the-scope-of-causal-nonduplication", "h02-ability-to-act-alone-and-actual-whole-production"),
                      ("necessary-agreement-and-productive-conditioning", "m03-agreement-and-voluntary-particularisation"),
                      ("textual-verification-priorities", "s05-textual-controls-that-affect-inference"),
                      ("dated-current-position-and-comparative-defeaters", "relation-to-the-final-judgement"))
    QUALIFICATIONS = (
        (QUESTIONS, ("Prepared questions are not answered external specialist review.",
                     "A provisional assessment is neither an established theorem nor an unresolved question merely because it appears in this document.")),
        (VALIDATION, ("Complete check logs and the finite source-list body are omitted; no new primary reading or scientific replay follows.",)),
        (QA, ("this curation performs no visual review or rendering.",)),
        (FINAL, ("Neither map owns their science or proves current research adoption.",)))

    def tail_errors(self, cross):
        errors = []
        work = self.work(cross)
        expected = [self.source_key(a) for a in SourceReadingGuideRoutesTests.SUPPORT]
        expected += ["t20-context-50e3ae6b35c1b914"]
        expected += [self.source_key(a) for a in self.TAIL]
        if work is None or work.get("supporting_source_keys") != expected:
            errors.append("tail-exact-ordered-support")
        for alias in self.TAIL:
            row = self.aliases[alias]
            source = cross["sources"].get(self.source_key(alias), {})
            if (source.get("path") != row["public_path"]
                    or source.get("sha256") != row["public_sha256"]
                    or not source.get("read_scope")):
                errors.append("tail-source:" + alias)
        return errors

    def test_original_tail_has_exact_selected_support(self):
        self.assertEqual(self.tail_errors(self.cross), [])

    def projection(self, alias):
        row = self.aliases[alias]
        return {"owner_archive_path": alias, "sha256": row["public_sha256"], "bytes": row["public_bytes"]}

    def changed(self, record, path, value):
        result = deepcopy(record)
        target = result
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        return result

    def validation_errors(self, record):
        errors = []
        if (record["schema"] != "t20-public-reading-index-validation-summary-v1"
                or record["as_of_utc"] != "2026-10-07T14:49:59Z"
                or record["original_validation_sha256"] != self.aliases[self.VALIDATION]["original_sha256"]):
            errors.append("tail-validation-identity")
        expected = [{"owner_archive_path": alias,
                     "original_sha256": self.aliases[alias]["original_sha256"],
                     "projected_sha256": self.aliases[alias]["public_sha256"],
                     "projected_bytes": self.aliases[alias]["public_bytes"]}
                    for alias in (self.ORIGINAL, self.INDEX, self.QUESTIONS)]
        if record["selected_documents"] != expected:
            errors.append("tail-validation-selected-originals")
        counts = ("source_work_entries", "completed_ordered_study_groups", "principal_return_points_in_ordered_groups",
                  "broader_return_points_in_ordered_groups", "witness_objects", "original_evidence_records",
                  "records_with_verified_public_aliases")
        if tuple(record["final_summary"][k] for k in counts) != (13, 8, 42, 48, 42, 200, 132):
            errors.append("tail-validation-distinct-counts")
        if (record["author_recorded_checks"] != 6359 or record["author_final_consistency_checks"] != 392
                or record["author_recorded_all_passed"] is not True):
            errors.append("tail-validation-reported-checks")
        credit_fields = ("new_compilation_reading_credit", "new_primary_reading_credit_by_this_compilation",
                         "new_compilation_primary_reading_credit", "new_compilation_primary_reading_credit",
                         "new_compilation_primary_reading_credit", "new_compilation_reading_credit")
        supplements = record["supplements"]
        if (len(supplements) != len(credit_fields)
                or any(row.get(field) != 0 for row, field in zip(supplements, credit_fields))
                or record["new_primary_reading_credit"] != 0
                or record["substantive_review"]["additional_primary_credit"] != 0
                or record["no_source_records_modified"] is not True
                or record["final_summary"]["all_primary_reading_credit_remains_with_original_receipts"] is not True
                or record["final_summary"]["no_new_primary_reading_by_this_compilation"] is not True):
            errors.append("tail-validation-inherited-reading")
        if (record["source_list_body_included"] is not False
                or any(row["body_included"] is not False for field in
                       ("historical_predecessor_inputs", "historical_supporting_records") for row in record[field])):
            errors.append("tail-validation-omitted-originals")
        if record["verification_scope"] != (
                "Body-free summary of reported author validation plus curation identity/reference checks. "
                "The complete check log remains a separately hashed original; no scientific replay or new primary reading is credited."):
            errors.append("tail-validation-receipt-not-replay")
        return errors

    def test_validation_selection_rejects_public_original_and_edition_swaps(self):
        record = self.record(self.VALIDATION)
        self.assertEqual(self.validation_errors(record), [])
        cases = [(("schema",), "t20-current-three-role-documents-v2", "tail-validation-identity"),
                 (("original_validation_sha256",), self.aliases[self.VALIDATION]["public_sha256"], "tail-validation-identity"),
                 (("as_of_utc",), "2026-10-07T16:49:45Z", "tail-validation-identity"),
                 (("selected_documents", 1, "original_sha256"), self.aliases[self.INDEX]["public_sha256"], "tail-validation-selected-originals"),
                 (("selected_documents", 1, "projected_sha256"), self.aliases[self.INDEX]["original_sha256"], "tail-validation-selected-originals"),
                 (("selected_documents", 0, "owner_archive_path"), self.V2, "tail-validation-selected-originals"),
                 (("selected_documents", 0, "projected_sha256"), self.aliases[self.V2]["public_sha256"], "tail-validation-selected-originals"),
                 (("selected_documents", 2), record["selected_documents"][0], "tail-validation-selected-originals"),
                 (("source_list_body_included",), True, "tail-validation-omitted-originals"),
                 (("historical_predecessor_inputs", 0, "body_included"), True, "tail-validation-omitted-originals"),
                 (("historical_supporting_records", 1, "body_included"), True, "tail-validation-omitted-originals")]
        for path, value, error in cases:
            with self.subTest(path=path):
                self.assertIn(error, self.validation_errors(self.changed(record, path, value)))

    def test_validation_counts_and_historical_receipts_cannot_award_fresh_reading_or_replay(self):
        record = self.record(self.VALIDATION)
        self.assertEqual(self.validation_errors(record), [])
        cases = [(("final_summary", "completed_ordered_study_groups"), 13, "tail-validation-distinct-counts"),
                 (("final_summary", "source_work_entries"), 8, "tail-validation-distinct-counts"),
                 (("author_recorded_checks",), 392, "tail-validation-reported-checks"),
                 (("author_final_consistency_checks",), 6359, "tail-validation-reported-checks"),
                 (("author_recorded_all_passed",), False, "tail-validation-reported-checks"),
                 (("new_primary_reading_credit",), 1, "tail-validation-inherited-reading"),
                 (("substantive_review", "additional_primary_credit"), 1, "tail-validation-inherited-reading"),
                 (("no_source_records_modified",), False, "tail-validation-inherited-reading"),
                 (("final_summary", "all_primary_reading_credit_remains_with_original_receipts"), False, "tail-validation-inherited-reading"),
                 (("final_summary", "no_new_primary_reading_by_this_compilation"), False, "tail-validation-inherited-reading"),
                 (("verification_scope",), "The current reader executor independently replayed all scientific and author checks.", "tail-validation-receipt-not-replay")]
        credit_fields = ("new_compilation_reading_credit", "new_primary_reading_credit_by_this_compilation",
                         "new_compilation_primary_reading_credit", "new_compilation_primary_reading_credit",
                         "new_compilation_primary_reading_credit", "new_compilation_reading_credit")
        cases += [(("supplements", n, field), 1, "tail-validation-inherited-reading")
                  for n, field in enumerate(credit_fields)]
        for path, value, error in cases:
            with self.subTest(path=path):
                self.assertIn(error, self.validation_errors(self.changed(record, path, value)))

    def qa_errors(self, qa):
        errors = []
        if (qa["schema"] != "t20-final-source-guide-document-qa-v1"
                or qa["created_at_utc"] != "2026-10-07T14:49:32.567322+00:00"
                or qa["original_qa_manifest_sha256"] != self.aliases[self.QA]["original_sha256"]):
            errors.append("tail-v1-qa-identity")
        if qa["source"] != self.projection(self.ORIGINAL):
            errors.append("tail-v1-qa-original-guide")
        current = self.record(self.CURRENT)
        original_guide = next(r for r in current["retained_historical_documents"] if r["role"] == "source and reading guide")
        if qa["document"] != original_guide["document"]["included_record"]:
            errors.append("tail-v1-qa-historical-word")
        counts = ("authored_content_records", "external_hyperlinks_exact", "relative_link_labels_and_paths_preserved",
                  "arabic_codepoints_preserved_in_order", "page_count")
        if tuple(qa[k] for k in counts) != (247, 20, 4, 62, 18):
            errors.append("tail-v1-qa-counts")
        pages = qa["page_inspections"]
        if (len(pages) != 18 or [p["page"] for p in pages] != list(range(1, 19))
                or any(p["result"] != "PASS" or p["final_render_identical_to_individually_viewed_image"] is not True for p in pages)):
            errors.append("tail-v1-qa-reported-pages")
        if (any(p["image_body_included"] is not False for p in pages)
                or any(qa[k]["original_record_body_included"] is not False for k in
                       ("content_qa", "build_receipt", "layout_correction", "source_narrative_approval"))
                or qa["historical_first_builds_retained_separately_not_included"] is not True):
            errors.append("tail-v1-qa-omitted-bodies")
        if (qa["science_rerun"] is not False
                or qa["acceptance_scope"] != "Document content, links, typography and rendering only."):
            errors.append("tail-v1-qa-documentary-scope")
        expected_corrections = ["Author-approved removal of one hyphen from the SF04 heading; all body text unchanged.",
                                "Kept the SF06 locator paragraph with its following explanation, avoiding a stranded section opening."]
        if qa["corrections"] != expected_corrections:
            errors.append("tail-v1-qa-specific-corrections")
        companion = next(r for r in current["current_documents"] if r["role"] == "mathematical companion")
        if qa["mathematical_companion_unchanged"] != companion["document"]["included_record"]:
            errors.append("tail-v1-qa-unchanged-companion")
        return errors

    def test_original_guide_qa_rejects_v2_identity_and_unperformed_body_or_science_admission(self):
        qa = self.record(self.QA)
        current = self.record(self.CURRENT)
        guide_v2 = next(r for r in current["current_documents"] if r["role"] == "source and reading guide")
        self.assertEqual(self.qa_errors(qa), [])
        cases = [(("schema",), "t20-successor-guide-document-qa-v2", "tail-v1-qa-identity"),
                 (("original_qa_manifest_sha256",), self.aliases[self.QA]["public_sha256"], "tail-v1-qa-identity"),
                 (("source",), self.projection(self.V2), "tail-v1-qa-original-guide"),
                 (("document",), guide_v2["document"]["included_record"], "tail-v1-qa-historical-word"),
                 (("authored_content_records",), 255, "tail-v1-qa-counts"),
                 (("relative_link_labels_and_paths_preserved",), 11, "tail-v1-qa-counts"),
                 (("page_count",), 20, "tail-v1-qa-counts"),
                 (("page_inspections", 0, "page"), 18, "tail-v1-qa-reported-pages"),
                 (("page_inspections", 0, "result"), "NOT_RUN", "tail-v1-qa-reported-pages"),
                 (("page_inspections", 0, "image_body_included"), True, "tail-v1-qa-omitted-bodies"),
                 (("historical_first_builds_retained_separately_not_included",), False, "tail-v1-qa-omitted-bodies"),
                 (("science_rerun",), True, "tail-v1-qa-documentary-scope"),
                 (("acceptance_scope",), "Fresh scientific and independent visual acceptance.", "tail-v1-qa-documentary-scope"),
                 (("corrections",), ["Applied the v2 locator keepNext correction to 37 paragraphs."], "tail-v1-qa-specific-corrections"),
                 (("mathematical_companion_unchanged",), qa["document"], "tail-v1-qa-unchanged-companion")]
        cases += [((key, "original_record_body_included"), True, "tail-v1-qa-omitted-bodies")
                  for key in ("content_qa", "build_receipt", "layout_correction", "source_narrative_approval")]
        for path, value, error in cases:
            with self.subTest(path=path):
                self.assertIn(error, self.qa_errors(self.changed(qa, path, value)))

    def final_errors(self, record):
        errors = []
        if (record["schema"] != "t20-three-final-documents-v1"
                or record["created_at_utc"] != "2026-10-07T14:49:32.567962+00:00"
                or record["original_delivery_binding_sha256"] != self.aliases[self.FINAL]["original_sha256"]):
            errors.append("tail-v1-final-identity")
        rows = record["documents"]
        expected_roles = ["research report", "source and reading guide", "mathematical companion"]
        if [r["role"] for r in rows] != expected_roles:
            errors.append("tail-v1-final-role-order")
        if record["total_pages"] != 48 or record["all_document_qa_passed"] is not True:
            errors.append("tail-v1-final-reported-total")
        qa_aliases = {"research report": "t20/reports/REPORT_QA_MANIFEST.json",
                      "source and reading guide": self.QA,
                      "mathematical companion": "t20/reports/MATHEMATICAL_COMPANION_QA.json"}
        current = self.record(self.CURRENT)
        comparison = {r["role"]: r for r in current["retained_historical_documents"]}
        comparison["mathematical companion"] = next(r for r in current["current_documents"]
                                                    if r["role"] == "mathematical companion")
        for row in rows:
            role = row["role"]
            alias = qa_aliases.get(role)
            if alias is None:
                continue
            if row["document"] != comparison[role]["document"]["included_record"]:
                errors.append("tail-v1-final-word:" + role)
            original = row["original_qa_record"]
            if (original["sha256"] != self.aliases[alias]["original_sha256"]
                    or original["bytes"] != comparison[role]["qa"]["historical_original_identity"]["bytes"]
                    or original["body_included"] is not False
                    or row["public_qa_record"] != self.projection(alias)):
                errors.append("tail-v1-final-qa-pair:" + role)
        return errors

    def test_historical_role_map_rejects_cross_role_swaps_and_current_v2_substitution(self):
        record = self.record(self.FINAL)
        current = self.record(self.CURRENT)
        guide_v2 = next(r for r in current["current_documents"] if r["role"] == "source and reading guide")
        self.assertEqual(self.final_errors(record), [])
        cases = [(("schema",), "t20-current-three-role-documents-v2", "tail-v1-final-identity"),
                 (("original_delivery_binding_sha256",), self.aliases[self.FINAL]["public_sha256"], "tail-v1-final-identity"),
                 (("total_pages",), 53, "tail-v1-final-reported-total"),
                 (("all_document_qa_passed",), False, "tail-v1-final-reported-total"),
                 (("documents", 1, "role"), "scientific result owner", "tail-v1-final-role-order"),
                 (("documents", 1, "document"), guide_v2["document"]["included_record"], "tail-v1-final-word:source and reading guide"),
                 (("documents", 1, "public_qa_record"), guide_v2["qa"]["included_record"], "tail-v1-final-qa-pair:source and reading guide")]
        for n, row in enumerate(record["documents"]):
            error = "tail-v1-final-qa-pair:" + row["role"]
            cases += [(("documents", n, "original_qa_record", "sha256"), row["public_qa_record"]["sha256"], error),
                      (("documents", n, "public_qa_record", "sha256"), row["original_qa_record"]["sha256"], error),
                      (("documents", n, "original_qa_record", "body_included"), True, error)]
        for path, value, error in cases:
            with self.subTest(path=path):
                self.assertIn(error, self.final_errors(self.changed(record, path, value)))
        # Retain the same two valid QA identities while attaching each to the
        # wrong document role. A mere set-of-links check would miss this swap.
        swapped = deepcopy(record)
        for field in ("original_qa_record", "public_qa_record"):
            swapped["documents"][0][field], swapped["documents"][1][field] = (
                swapped["documents"][1][field], swapped["documents"][0][field])
        self.assertEqual({row["public_qa_record"]["sha256"] for row in record["documents"]},
                         {row["public_qa_record"]["sha256"] for row in swapped["documents"]})
        self.assertEqual(set(self.final_errors(swapped)),
                         {"tail-v1-final-qa-pair:research report", "tail-v1-final-qa-pair:source and reading guide"})

    def question_pair_errors(self, section, page):
        """Check these explicit source pairs, not arbitrary philosophical prose."""
        blocks, paragraph = [], []
        for line in section.splitlines():
            if not line.strip() or line.lstrip().startswith("|"):
                if paragraph:
                    blocks.append("\n".join(paragraph))
                    paragraph = []
                if line.lstrip().startswith("|"):
                    blocks.append(line)
            else:
                paragraph.append(line)
        if paragraph:
            blocks.append("\n".join(paragraph))
        questions = self.aliases[self.QUESTIONS]["public_path"]
        original = self.aliases[self.ORIGINAL]["public_path"]
        linked_blocks = [[self.mod.resolve_reader_link(ROOT, page, href)
                          for _, href in self.mod.markdown_index(block)["links"]] for block in blocks]
        errors = []
        for question, guide in self.QUESTION_PAIRS:
            pairs = []
            for links in linked_blocks:
                for n, target in enumerate(links):
                    if target == (questions, question):
                        # Another question stops the relation; a collection of
                        # valid destinations alone does not identify its ground.
                        pairs.append(next((dest for dest in links[n + 1:]
                                           if dest is not None and dest[0] in (questions, original)), None))
            if pairs != [(original, guide)]:
                errors.append("tail-question-pair:" + question)
        return errors

    def test_prepared_questions_reach_their_specific_original_arguments_and_textual_controls(self):
        questions = self.aliases[self.QUESTIONS]["public_path"]
        original = self.aliases[self.ORIGINAL]["public_path"]
        for alias, number in ((self.QUESTIONS, 0), (self.ORIGINAL, 1)):
            anchors = {h[0] for h in self.mod.markdown_index((ROOT / self.aliases[alias]["public_path"]).read_text())["headings"]}
            self.assertTrue({pair[number] for pair in self.QUESTION_PAIRS} <= anchors)
        for page, heading in (("docs/reader/PAPER-CATALOGUE.md", "original-guide-questions-and-documentary-support"),
                              ("docs/reader/VERIFICATION-GUIDE.md", "checking-the-original-support-records")):
            section = self.section_body((ROOT / page).read_text(), heading)
            self.assertEqual(self.question_pair_errors(section, page), [])
            for question, guide in self.QUESTION_PAIRS:
                question_href = "(../../" + questions + "#" + question + ")"
                original_href = "(../../" + original + "#" + guide + ")"
                for href in (question_href, original_href):
                    changed = section.replace(href, "(PAPER-CATALOGUE.md)")
                    self.assertNotEqual(changed, section)
                    self.assertIn("tail-question-pair:" + question, self.question_pair_errors(changed, page))
                changed = section.replace(original_href,
                    "(../../" + self.aliases[self.V2]["public_path"] + "#" + guide + ")")
                self.assertIn("tail-question-pair:" + question, self.question_pair_errors(changed, page))
            first, second = ["(../../" + original + "#" + pair[1] + ")" for pair in self.QUESTION_PAIRS[:2]]
            swapped = section.replace(first, "FIXTURE_TAIL_PAIR").replace(second, first).replace("FIXTURE_TAIL_PAIR", second)
            self.assertEqual({href for _, href in self.mod.markdown_index(section)["links"]},
                             {href for _, href in self.mod.markdown_index(swapped)["links"]})
            self.assertEqual(set(self.question_pair_errors(swapped, page)),
                             {"tail-question-pair:" + pair[0] for pair in self.QUESTION_PAIRS[:2]})

    def qualification_errors(self, section):
        """Preserve four reviewed, source-specific table qualifications."""
        page = "docs/reader/PAPER-CATALOGUE.md"
        errors = []
        for alias, clauses in self.QUALIFICATIONS:
            target = (self.aliases[alias]["public_path"], "")
            rows = [line for line in section.splitlines() if line.lstrip().startswith("|") and
                    target in [self.mod.resolve_reader_link(ROOT, page, href)
                               for _, href in self.mod.markdown_index(line)["links"]]]
            if len(rows) != 1 or any(clause not in rows[0] for clause in clauses):
                errors.append("tail-reader-qualification:" + alias)
        return errors

    def test_source_specific_reader_qualifications_reject_false_review_and_execution_credit(self):
        section = self.section_body((ROOT / "docs/reader/PAPER-CATALOGUE.md").read_text(),
                                    "original-guide-questions-and-documentary-support")
        self.assertEqual(self.qualification_errors(section), [])
        substitutions = (
            (self.QUESTIONS, self.QUALIFICATIONS[0][1][0], "Specialists answered and accepted these conclusions."),
            (self.QUESTIONS, self.QUALIFICATIONS[0][1][1], "Every statement in this document remains an unanswered question."),
            (self.VALIDATION, self.QUALIFICATIONS[1][1][0], "The current executor replayed the complete log and established whole-index reading."),
            (self.QA, self.QUALIFICATIONS[2][1][0], "this curation independently rendered and visually inspected every page."),
            (self.FINAL, self.QUALIFICATIONS[3][1][0], "This map establishes scientific correctness and current research adoption."))
        for alias, original, false_claim in substitutions:
            changed = section.replace(original, false_claim)
            self.assertNotEqual(changed, section)
            self.assertIn("tail-reader-qualification:" + alias, self.qualification_errors(changed))
        qa_clause, final_clause = self.QUALIFICATIONS[2][1][0], self.QUALIFICATIONS[3][1][0]
        swapped = section.replace(qa_clause, "FIXTURE_TAIL_QUALIFICATION").replace(final_clause, qa_clause).replace(
            "FIXTURE_TAIL_QUALIFICATION", final_clause)
        self.assertEqual({href for _, href in self.mod.markdown_index(section)["links"]},
                         {href for _, href in self.mod.markdown_index(swapped)["links"]})
        self.assertEqual(set(self.qualification_errors(swapped)),
                         {"tail-reader-qualification:" + self.QA, "tail-reader-qualification:" + self.FINAL})



class ScholarlyAdditionTests(unittest.TestCase):
    """Finite new scholarly editions retain the historical population boundary."""
    setUp = ReaderPilotTests.setUp
    git = ReaderPilotTests.git
    check = ReaderPilotTests.check
    reject = ReaderPilotTests.reject

    def addition_fixture(self):
        owners, cross = deepcopy(self.owners), deepcopy(self.cross)
        keys = sorted(w["key"] for w in cross["works"])
        owners["baseline_work_population"] = {
            "count": len(keys),
            "keys_sha256": hashlib.sha256(json.dumps(keys, separators=(",", ":")).encode()).hexdigest(),
        }
        paths = {"consolidated-core": "fixture-scholarly/core.md",
                 "consolidated-note": "fixture-scholarly/note.md",
                 "synthesis-review": "fixture-docs/synthesis-review.md"}
        for key in ("consolidated-core", "consolidated-note"):
            path = self.repo / paths[key]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# " + key + "\nA complete fixture exposition, not an original result.\n")
        review = "# Exact reviewed works\n\n| Work | SHA-256 | Bytes |\n|---|---|---:|\n"
        for key in ("consolidated-core", "consolidated-note"):
            body = (self.repo / paths[key]).read_bytes()
            review += "| [" + key + "](../" + paths[key] + ") | `" + hashlib.sha256(body).hexdigest() + "` | " + str(len(body)) + " |\n"
        (self.repo / paths["synthesis-review"]).write_text(review)
        self.git("add", "--", *paths.values())
        additions = []
        for key, path in paths.items():
            body = (self.repo / path).read_bytes()
            work_keys = [key + "-work"] if key != "synthesis-review" else ["consolidated-core-work", "consolidated-note-work"]
            support = ["synthesis-review"] if key != "synthesis-review" else []
            additions.append({"key": key, "path": path, "mode": "100644",
                              "git_oid": self.git("hash-object", path).strip(),
                              "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                              "role": "work-source" if support else "review",
                              "work_keys": work_keys, "supporting_source_keys": support})
            cross["sources"][key] = {"path": path, "sha256": hashlib.sha256(body).hexdigest(),
                                      "read_scope": "Complete fixture body and exact work/review binding inspected."}
            if support:
                cross["works"].append({"key": work_keys[0], "title": key, "role": "synthesis",
                                       "source_keys": [key], "supporting_source_keys": support,
                                       "reading_forms": [{"source": key, "relationship": "authored-synthesis"}]})
        owners["source_additions"] = additions
        return owners, cross

    def test_exact_new_syntheses_and_shared_review_preserve_historical_denominator(self):
        owners, cross = self.addition_fixture()
        self.assertEqual(self.check(owners, cross), [])
        self.assertEqual(owners["baseline"]["commit"], self.base)
        self.assertEqual(owners["baseline_work_population"]["count"], len(self.cross["works"]))
        self.assertEqual(len(cross["works"]), len(self.cross["works"]) + 2)
        self.assertFalse({r["path"] for r in owners["source_additions"]} & self.mod.REFACTOR_EDIT_PATHS)

    def test_missing_duplicate_or_extra_addition_is_rejected(self):
        owners, cross = self.addition_fixture()
        for change in ("missing", "duplicate", "extra"):
            with self.subTest(change=change):
                altered = deepcopy(owners)
                if change == "missing":
                    altered["source_additions"].pop()
                elif change == "duplicate":
                    altered["source_additions"].append(deepcopy(altered["source_additions"][0]))
                else:
                    extra = deepcopy(altered["source_additions"][0])
                    extra["key"] = "undefined-addition"
                    extra["path"] = "fixture-scholarly/absent.md"
                    altered["source_additions"].append(extra)
                self.reject(self.check(altered, cross), "source-addition")

    def test_new_source_identity_requires_every_exact_field(self):
        owners, cross = self.addition_fixture()
        for field, wrong in (("path", "fixture-scholarly/note.md"), ("mode", "100755"),
                             ("bytes", 1), ("git_oid", "0" * 40), ("sha256", "0" * 64)):
            with self.subTest(field=field):
                altered = deepcopy(owners)
                altered["source_additions"][0][field] = wrong
                self.reject(self.check(altered, cross), "source-addition")
        altered = deepcopy(cross)
        altered["sources"]["consolidated-core"]["sha256"] = "0" * 64
        self.reject(self.check(owners, altered), "source-addition")

    def test_absent_reading_scope_and_aliased_source_are_rejected(self):
        owners, cross = self.addition_fixture()
        for scope in (None, "", " ", []):
            altered = deepcopy(cross)
            altered["sources"]["consolidated-core"]["read_scope"] = scope
            self.reject(self.check(owners, altered), "source-addition")
        altered = deepcopy(cross)
        altered["sources"]["second-key-same-body"] = deepcopy(altered["sources"]["consolidated-core"])
        self.reject(self.check(owners, altered), "source-addition")

    def test_untracked_missing_worktree_or_changed_index_is_not_admitted(self):
        for change in ("untracked", "missing", "index"):
            with self.subTest(change=change):
                owners, cross = self.addition_fixture()
                path = owners["source_additions"][0]["path"]
                if change == "untracked":
                    self.git("reset", "-q", "HEAD", "--", path)
                elif change == "missing":
                    (self.repo / path).unlink()
                else:
                    self.git("update-index", "--cacheinfo", "100644," + owners["source_additions"][1]["git_oid"] + "," + path)
                self.reject(self.check(owners, cross), "source-addition")

    def test_symlink_and_unsafe_additions_are_rejected(self):
        owners, cross = self.addition_fixture()
        path = self.repo / owners["source_additions"][0]["path"]
        path.unlink()
        path.symlink_to(self.repo / owners["source_additions"][1]["path"])
        self.reject(self.check(owners, cross), "source-addition")
        path.unlink()
        owners, cross = self.addition_fixture()
        for unsafe in ("../outside.md", "/absolute.md", ".git/config", "fixture-scholarly/../note.md"):
            altered = deepcopy(owners)
            altered["source_additions"][0]["path"] = unsafe
            self.reject(self.check(altered, cross), "source-addition")

    def test_work_and_review_support_require_the_exact_relationship(self):
        owners, cross = self.addition_fixture()
        for field, wrong in (("source_keys", ["consolidated-note"]), ("role", "review"),
                             ("supporting_source_keys", []),
                             ("supporting_source_keys", ["synthesis-review", "synthesis-review"]),
                             ("supporting_source_keys", ["synthesis-review", "fixture-theory/lineage.md"]),
                             ("supporting_source_keys", ["fixture-theory/lineage.md"])):
            with self.subTest(field=field, wrong=wrong):
                altered = deepcopy(cross)
                altered["works"][-2][field] = wrong
                self.reject(self.check(owners, altered), "source-addition")
        altered = deepcopy(cross)
        altered["works"].append({"key": "false-third-work", "title": "Review is not a work",
                                 "role": "review", "source_keys": ["synthesis-review"]})
        self.reject(self.check(owners, altered), "source-addition")

    def test_wrong_review_work_pair_and_undeclared_work_use_are_rejected(self):
        owners, cross = self.addition_fixture()
        altered = deepcopy(owners)
        altered["source_additions"][-1]["work_keys"].pop()
        self.reject(self.check(altered, cross), "source-addition")
        altered = deepcopy(cross)
        altered["works"][1]["supporting_source_keys"] = ["synthesis-review"]
        self.reject(self.check(owners, altered), "source-addition")

    def test_refreshing_new_science_hashes_cannot_inherit_an_old_review(self):
        owners, cross = self.addition_fixture()
        row = owners["source_additions"][0]
        path = self.repo / row["path"]
        path.write_text(path.read_text() + "A changed conclusion requiring a new review.\n")
        body = path.read_bytes()
        self.git("add", "--", row["path"])
        row.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                   git_oid=self.git("hash-object", row["path"]).strip())
        cross["sources"][row["key"]]["sha256"] = row["sha256"]
        self.reject(self.check(owners, cross), "source-addition")

    def test_review_row_cannot_swap_correct_hashes_between_work_paths(self):
        owners, cross = self.addition_fixture()
        row = owners["source_additions"][-1]
        path = self.repo / row["path"]
        first, second = [r["sha256"] for r in owners["source_additions"][:2]]
        text = path.read_text().replace(first, "FIXTURE_HASH_SWAP").replace(second, first).replace("FIXTURE_HASH_SWAP", second)
        path.write_text(text)
        body = path.read_bytes()
        self.git("add", "--", row["path"])
        row.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                   git_oid=self.git("hash-object", row["path"]).strip())
        cross["sources"][row["key"]]["sha256"] = row["sha256"]
        self.reject(self.check(owners, cross), "source-addition")

    def test_baseline_sources_cannot_masquerade_as_additions(self):
        owners, cross = self.addition_fixture()
        row = owners["source_additions"][0]
        source = cross["sources"]["fixture-theory/note.md"]
        body = (self.repo / source["path"]).read_bytes()
        row.update(path=source["path"], bytes=len(body), sha256=source["sha256"],
                   git_oid=self.git("hash-object", source["path"]).strip())
        cross["sources"][row["key"]] = deepcopy(source)
        self.reject(self.check(owners, cross), "source-addition")

    def test_historical_work_population_cannot_be_reset_or_substituted(self):
        owners, cross = self.addition_fixture()
        for field, wrong in (("count", len(cross["works"])), ("keys_sha256", "0" * 64)):
            altered = deepcopy(owners)
            altered["baseline_work_population"][field] = wrong
            self.reject(self.check(altered, cross), "source-addition")
        altered = deepcopy(cross)
        altered["works"][1]["key"] = "substituted-historical-work"
        self.reject(self.check(owners, altered), "source-addition")

    def test_new_tracked_science_beside_admitted_files_remains_rejected(self):
        owners, cross = self.addition_fixture()
        p = self.repo / "fixture-scholarly/unadmitted.md"
        p.write_text("Another fixture source, outside the finite admission.\n")
        self.git("add", "--", str(p.relative_to(self.repo)))
        self.reject(self.check(owners, cross), "corpus-currentness")


    def test_new_reading_forms_cannot_promote_review_or_substitute_an_old_source(self):
        owners, cross = self.addition_fixture()
        for forms in ([], [{"source": "fixture-theory/note.md", "relationship": "authored-synthesis"}],
                      [{"source": "consolidated-core", "relationship": "governed-rendering"}]):
            altered = deepcopy(cross)
            altered["works"][-2]["reading_forms"] = forms
            self.reject(self.check(owners, altered), "source-addition")
        altered = deepcopy(cross)
        altered["works"][1]["reading_forms"] = [{"source": "synthesis-review", "relationship": "authored-source"}]
        self.reject(self.check(owners, altered), "source-addition")

    def test_malformed_admission_and_historical_population_fail_closed(self):
        owners, cross = self.addition_fixture()
        for value in (None, {}, "unexpected"):
            altered = deepcopy(owners)
            altered["source_additions"] = value
            self.reject(self.check(altered, cross), "source-addition")
        for value in (None, [], "unexpected"):
            altered = deepcopy(owners)
            altered["baseline_work_population"] = value
            self.reject(self.check(altered, cross), "source-addition")



class HistoricalProseReaderTests(unittest.TestCase):
    """Explicit history keeps identity, readable scholarship and the old census."""

    BASE = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
    PATHS = (
        'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/REPORT.md',
        'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md',
        'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md',
        'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/VARIABLE_SHARING_REDUCTION.md',
        'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/REPORT.md',
    )
    KEY = 't20-c03-52631c602c1c8fed'

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('reader_finite_history', MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        directory = ROOT / 'docs/project-closure/reader-refactor-issue-35'
        cls.original_owners = json.loads((directory / 'OWNER-MAP.json').read_text())
        cls.original_cross = json.loads((directory / 'CROSSWALK.json').read_text())
        cls.indexed = {r['path']: r for r in cls.mod.entries_at(
            ROOT, cls.original_owners['baseline']['commit'])}
        cls.bindings = [dict(
            path=path, repository_revision=cls.BASE,
            git_blob=subprocess.check_output(['git', 'rev-parse', cls.BASE + ':' + path],
                                             cwd=ROOT, text=True).strip(),
            role='historical-source', reading_source='consolidated-recognition-and-restoration',
            basis='scientific-consolidation-review') for path in cls.PATHS]
        cls.additions, errors = cls.mod.check_source_additions(
            ROOT, cls.indexed, cls.original_owners, cls.original_cross)
        if errors:
            raise AssertionError(errors)

    def setUp(self):
        self.owners = deepcopy(self.original_owners)
        self.owners['historical_source_bindings'] = deepcopy(self.bindings)
        self.cross = deepcopy(self.original_cross)

    def history(self):
        gate = getattr(self.mod, 'check_historical_sources', None)
        self.assertTrue(callable(gate), 'finite historical source owner is not implemented')
        return gate(ROOT, self.indexed, self.owners, self.cross, self.additions)

    def test_explicit_bindings_authenticate_all_five_original_occurrences(self):
        before = deepcopy((self.owners, self.cross))
        admitted, errors = self.history()
        self.assertEqual(errors, [])
        self.assertEqual(set(admitted), set(self.PATHS))
        self.assertEqual((self.owners, self.cross), before, 'verification may not rewrite its evidence')
        self.assertEqual(self.owners['baseline_work_population']['count'], 448)
        self.assertEqual(len(self.cross['sources']), 1632)

    def test_full_reader_uses_explicit_history_for_missing_predecessors(self):
        saved = {}
        for path in self.PATHS:
            node = ROOT
            for part in path.split('/'):
                node = node / part
                self.assertFalse(node.is_symlink(), "unsafe initial historical path")
            saved[path] = ((node.read_bytes(), node.stat().st_mode & 0o777)
                           if node.exists() else (None, None))
            if saved[path][0] is not None:
                self.assertEqual(saved[path][0], subprocess.check_output(
                    ['git', 'show', self.BASE + ':' + path], cwd=ROOT))
                self.assertFalse(saved[path][1] & 0o111, "wrong initial historical Git mode")
        try:
            for path in self.PATHS:
                if (ROOT / path).exists():
                    (ROOT / path).unlink()
            errors = self.mod.check(ROOT, self.owners, self.cross)
            self.assertEqual(errors, [])
            self.assertTrue(all(not (ROOT / path).exists() for path in self.PATHS),
                            'absence changed during reader validation')
        finally:
            for path, (body, mode) in saved.items():
                node = ROOT / path
                if body is None:
                    if node.exists() or node.is_symlink():
                        node.unlink()
                else:
                    node.write_bytes(body)
                    node.chmod(mode)

    def test_missing_duplicate_and_extra_dispositions_are_rejected(self):
        for change in ('missing', 'duplicate', 'extra'):
            with self.subTest(change=change):
                self.owners['historical_source_bindings'] = deepcopy(self.bindings)
                rows = self.owners['historical_source_bindings']
                if change == 'missing':
                    rows.pop()
                elif change == 'duplicate':
                    rows.append(deepcopy(rows[0]))
                else:
                    rows.append(dict(rows[0], path='README.md'))
                self.assertTrue(self.history()[1])

    def test_revision_blob_role_and_current_source_require_exact_owner_binding(self):
        for field, value in (('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                             ('path', '../report.md'), ('role', 'work-source'),
                             ('reading_source', self.KEY), ('basis', self.KEY)):
            with self.subTest(field=field):
                self.owners['historical_source_bindings'] = deepcopy(self.bindings)
                self.owners['historical_source_bindings'][0][field] = value
                self.assertTrue(self.history()[1])

    def test_old_source_requires_explicit_historical_reading_form_and_incorporation(self):
        for change in ('form', 'relation'):
            with self.subTest(change=change):
                self.cross = deepcopy(self.original_cross)
                if change == 'form':
                    for work in self.cross['works']:
                        for form in work.get('reading_forms', []):
                            if form.get('source') == self.KEY:
                                form['relationship'] = 'authored-source'
                else:
                    self.cross['relations'] = [r for r in self.cross['relations']
                                               if r.get('from') != self.KEY]
                self.assertTrue(self.history()[1])

    def test_wrong_current_scholarship_cannot_be_replaced_by_historical_evidence(self):
        path = ROOT / self.cross['sources']['consolidated-recognition-and-restoration']['path']
        body = path.read_bytes()
        try:
            path.write_bytes(body + b'\nwrong current edition\n')
            self.assertTrue(self.history()[1])
        finally:
            path.write_bytes(body)

    def test_projection_owner_allows_only_four_exact_additional_history_pins(self):
        original = json.loads(subprocess.check_output(
            ['git', 'show', self.owners['baseline']['commit'] + ':' +
             'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'], cwd=ROOT))
        legacy = HistoricalMetadataPinTests()
        legacy.original = original
        legacy.identity = '94fb4c0a0fbe7406570711b222ac0e5dbc7493867cd28cb6f0ef08c6fea99074'
        candidate, _ = legacy.candidate()
        for binding in self.bindings:
            if binding['path'] == self.PATHS[2]:
                continue
            row = next(r for r in candidate['objects'] if r.get('repository_path') == binding['path'])
            row.update(repository_revision=self.BASE, git_blob=binding['git_blob'])
        manifest_path = 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
        owner = self.indexed[manifest_path]
        self.assertTrue(self.mod.permitted_historical_status_pin(ROOT, owner, json.dumps(candidate).encode()))
        changed = deepcopy(candidate)
        row = next(r for r in changed['objects'] if r.get('repository_path') == self.PATHS[0])
        row['repository_revision'] = 'HEAD'
        self.assertFalse(self.mod.permitted_historical_status_pin(ROOT, owner, json.dumps(changed).encode()))
        changed = deepcopy(candidate)
        next(r for r in changed['objects'] if r.get('repository_path') == self.PATHS[0]).pop('git_blob')
        self.assertFalse(self.mod.permitted_historical_status_pin(ROOT, owner, json.dumps(changed).encode()))


    def test_staged_historical_identity_and_conflict_cannot_hide_in_worktree(self):
        path = self.PATHS[0]
        node = ROOT / path
        self.assertFalse(node.is_symlink())
        saved_body = node.read_bytes() if node.exists() else None
        saved_mode = node.stat().st_mode & 0o777 if node.exists() else None
        original_body = subprocess.check_output(['git', 'show', self.BASE + ':' + path], cwd=ROOT)
        if saved_body is not None:
            self.assertEqual(saved_body, original_body)
            self.assertEqual(saved_mode, 0o644)
        index = Path(subprocess.check_output(['git', 'rev-parse', '--git-path', 'index'],
                                            cwd=ROOT, text=True).strip())
        if not index.is_absolute():
            index = ROOT / index
        saved_index = index.read_bytes()
        original = next(row['git_blob'] for row in self.bindings if row['path'] == path)
        wrong = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                        cwd=ROOT, input=b'wrong staged historical body\n').decode().strip()
        link = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                       cwd=ROOT, input=b'REPORT.md').decode().strip()
        try:
            for kind, mode, blob in (('blob', '100644', wrong), ('mode', '100755', original),
                                     ('symlink', '120000', link), ('unmerged', None, None)):
                for present in (False, True):
                    with self.subTest(kind=kind, present=present):
                        index.write_bytes(saved_index)
                        subprocess.run(['git', 'update-index', '--force-remove', '--', path], cwd=ROOT, check=True)
                        if mode:
                            subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                                            mode + ',' + blob + ',' + path], cwd=ROOT, check=True)
                        else:
                            entries = ''.join('100644 ' + oid + ' ' + stage + '\t' + path + '\n'
                                              for oid, stage in ((original, '1'), (wrong, '2'), (original, '3')))
                            subprocess.run(['git', 'update-index', '--index-info'], cwd=ROOT,
                                           input=entries.encode(), check=True)
                        if present:
                            node.write_bytes(original_body)
                            node.chmod(0o644)
                        elif node.exists():
                            node.unlink()
                        errors = self.mod.check(ROOT, self.owners, self.cross)
                        self.assertTrue(any(e.startswith('historical-source: ' + path) for e in errors), errors)
                        self.assertEqual(node.exists(), present, 'reader verification changed physical presence')
        finally:
            index.write_bytes(saved_index)
            if saved_body is None:
                if node.exists():
                    node.unlink()
            else:
                node.write_bytes(saved_body)
                node.chmod(saved_mode)
        self.assertEqual(index.read_bytes(), saved_index)




class ReadOnlyCurrentnessDiffTests(unittest.TestCase):
    """Tiny Git fixtures for diff's stat-cache side effect, not corpus acceptance."""

    def setUp(self):
        import os
        from unittest.mock import patch
        self.env = patch.dict(os.environ, {"GIT_OPTIONAL_LOCKS": "0",
                              "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.relative = "fixture-read-only/source.txt"
        self.node = self.repo / self.relative
        self.node.parent.mkdir(parents=True)
        self.original = b"synthetic unchanged source\n"
        self.node.write_bytes(self.original)
        self._git("init", "-q")
        self._git("config", "diff.autoRefreshIndex", "true")
        self._git("add", "--", self.relative)
        self._git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                  "commit", "-qm", "synthetic baseline")
        self.baseline = self._git("rev-parse", "HEAD").decode().strip()
        self.initial = self._snapshot()

        spec = importlib.util.spec_from_file_location("read_only_currentness_owner", MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.rejection = ["corpus-currentness: " + self.relative +
                          " requires source-baseline and work/support disposition review"]

    def _gate(self):
        return self.mod.check_corpus_currentness(self.repo, self.baseline)

    def _git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, capture_output=True, check=True).stdout

    def _snapshot(self):
        raw = (self.repo / ".git" / "index").read_bytes()
        info = self.node.stat()
        return {
            "raw_index_sha256": hashlib.sha256(raw).hexdigest(), "raw_index_bytes": len(raw),
            "logical_entries": self._git("ls-files", "--stage", "-z").decode(),
            "flags": self._git("ls-files", "-v", "-z").decode(),
            "debug_metadata": self._git("ls-files", "--debug", "-z").decode(),
            "source_sha256": hashlib.sha256(self.node.read_bytes()).hexdigest(),
            "physical_stat": {"mode": info.st_mode & 0o777, "inode": info.st_ino,
                              "device": info.st_dev, "size": info.st_size,
                              "ctime_ns": info.st_ctime_ns, "mtime_ns": info.st_mtime_ns},
        }

    def _require_read_only(self, expected):
        before = self._snapshot()
        result = self._gate()
        after = self._snapshot()
        self._diff_observation = {"initial": self.initial, "before": before,
                                  "after": after, "result": result}
        self.assertEqual(result, expected)
        for key in ("logical_entries", "flags", "source_sha256", "physical_stat"):
            self.assertEqual(before[key], after[key], key)
        self.assertEqual(before["raw_index_sha256"], after["raw_index_sha256"],
                         "read-only diff refreshed the raw index")
        self.assertEqual(before["debug_metadata"], after["debug_metadata"])

    def test_stat_only_replacement_preserves_exact_index(self):
        import os
        info = self.node.stat()
        replacement = self.node.with_name("replacement.tmp")
        replacement.write_bytes(self.original)
        replacement.chmod(info.st_mode & 0o777)
        os.utime(replacement, ns=(info.st_atime_ns, info.st_mtime_ns - 2_000_000_000))
        replacement.replace(self.node)
        self.assertEqual(self.node.read_bytes(), self.original)
        self.assertEqual(self._snapshot()["logical_entries"], self.initial["logical_entries"])
        self._require_read_only([])

    def test_staged_tamper_cannot_hide_behind_original_worktree(self):
        self.node.write_bytes(b"synthetic staged tampering\n")
        self._git("add", "--", self.relative)
        self.node.write_bytes(self.original)
        self.assertNotEqual(self._snapshot()["logical_entries"], self.initial["logical_entries"])
        self._require_read_only(self.rejection)




class ContinuationCollectionRelocationTests(unittest.TestCase):
    """A moved reading form stays explicit in its destination collection."""
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("relocated_collection_reader", MODULE)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        folder = Path("docs/project-closure/reader-refactor-issue-35")
        cls.owners = json.loads((ROOT / folder / "OWNER-MAP.json").read_text())
        cls.cross = json.loads((MODULE.parent.parent / folder / "CROSSWALK.json").read_text())
        cls.rows = cls.mod.entries_at(ROOT, cls.owners["baseline"]["commit"])
        cls.paths = (
            "experiments/orthemology-v5-successors/source-store/"
            "98c1923c5c9ef77094ca28a63c32866fae56ae04b7a1597da59874935d9b1167/IndexedObserver.lean",
            "experiments/orthemology-v5-successors/source-store/"
            "73b3cb0b813ff303a6735c3cf8ac3c8dbbc1ed5c5dd335d4e0c239b8ddb23cc3/IndexedRuntime.lean",
        )

    def test_relocated_primary_forms_have_explicit_successor_dispositions(self):
        self.assertEqual(self.mod.check_collection_dispositions(self.rows, self.owners, self.cross), [])
        items = self.cross["collection_dispositions"]["v5-successors"]["items"]
        for path in self.paths:
            self.assertEqual([row for row in items if row["path"] == path], [
                {"path": path, "role": "formal-component", "work": "continuation-indexed-observer"}])

    def test_neither_relocated_primary_form_can_hide_in_support(self):
        self.assertEqual(self.mod.check_collection_dispositions(self.rows, self.owners, self.cross), [])
        for path in self.paths:
            with self.subTest(path=path):
                altered = deepcopy(self.cross)
                record = altered["collection_dispositions"]["v5-successors"]
                record["items"] = [row for row in record["items"] if row["path"] != path]
                errors = self.mod.check_collection_dispositions(self.rows, self.owners, altered)
                self.assertIn("collection-coverage: v5-successors has extra paths or omitted work sources", errors)


class RoundsParentNavigationTests(unittest.TestCase):
    """Current custody wording must not replace the original source identity."""
    PARENT = "docs/project-closure/ar8r-v11/post-merge-proposals/README.md"
    PREFIX = "docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-rounds11-20"
    ORIGINAL_REVISION = "a7ff0e33d1a299db640041c46b1af81ca70851f6"
    OLD_PARAGRAPH = (
        b"The `pmr007-rounds11-20` directory is an exact, public-safe copy of the final sanitized "
        b"repository-update proposal recovered from the authenticated research thread. Its internal "
        b"files are preserved without correction so their original hashes remain testable."
    )
    NEW_PARAGRAPH = (
        b"The original `pmr007-rounds11-20` import is the exact, public-safe copy of the final sanitized "
        b"repository-update proposal recovered from the authenticated research thread. Its complete "
        b"131-file edition is retained at Git commit `a7ff0e33d1a299db640041c46b1af81ca70851f6`. "
        b"The current snapshot preserves its unchanged 130-row hash manifest and requires its 32 "
        b"distinct or context-dependent members; 98 exact same-relative copies may resolve through "
        b"`pmr007-deep-a-bk` under the finite snapshot gate. The existing rounds adoption-boundary "
        b"correction records those current routes and their limits; original source bytes and hashes "
        b"remain testable."
    )

    @classmethod
    def setUpClass(cls):
        cls.original = subprocess.check_output(
            ["git", "--no-replace-objects", "cat-file", "blob", cls.ORIGINAL_REVISION + ":" + cls.PARENT],
            cwd=ROOT)
        if (len(cls.original) != 4073 or hashlib.sha256(cls.original).hexdigest() !=
                "d20707cf0d24dd5b2b966f2b1f3640ec7672092ef8a19b57f60fc61897cd6b50"
                or cls.original.count(cls.OLD_PARAGRAPH) != 1):
            raise AssertionError("The independent original parent fixture has changed")
        cls.adapted = cls.original.replace(cls.OLD_PARAGRAPH, cls.NEW_PARAGRAPH, 1)
        if (len(cls.adapted) != 4459 or hashlib.sha256(cls.adapted).hexdigest() !=
                "40e644bd7f9eb9728756364a348d2c08e6199578dbd056a466ebe1f6e5a15e78"):
            raise AssertionError("The reviewed parent adaptation fixture has changed")
        tree = subprocess.check_output([
            "git", "--no-replace-objects", "--literal-pathspecs", "ls-tree", "-r", "-z",
            cls.ORIGINAL_REVISION, "--", cls.PREFIX], cwd=ROOT)
        cls.members = [entry.split(b"\t", 1)[1].decode() for entry in tree.split(b"\0") if entry]
        if len(cls.members) != 131:
            raise AssertionError("The original parent fixture requires its finite 131-entry edition")

    def setUp(self):
        spec = importlib.util.spec_from_file_location("rounds_parent_reader", MODULE)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.tmp = tempfile.TemporaryDirectory(prefix="rounds-parent-navigation-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.target = self.repo / self.PARENT
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(self.original)
        for path in self.members:
            target = self.repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"Synthetic public member; no scientific evidence.\n")
        self.profile = "fixture-publication.yaml"
        (self.repo / self.profile).write_text("artifacts: []\n")
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "Synthetic public parent navigation fixture")
        self.baseline = self.git("rev-parse", "HEAD").decode().strip()
        # Only the native fixture's commit coordinate changes. Original bytes,
        # expected transformation, source hashes and every Git operation are real.
        self.mod.PMR007_ROUNDS_PARENT_REVISION = self.baseline
        self.owners = {
            "schema": "orthemology-reader-owner-map-v1",
            "baseline": {"commit": self.baseline},
            "external_body_admissions": [],
            "collections": [
                {"key": "parent", "include": ["docs/"], "owners": [self.PARENT]},
                {"key": "profile", "include": [self.profile], "owners": [self.profile]},
            ],
            "publication_profile": self.profile,
        }
        self.cross = {
            "schema": "orthemology-reader-crosswalk-v1", "coverage_stage": "representative-pilot",
            "sources": {
                "parent": {"path": self.PARENT, "sha256": hashlib.sha256(self.original).hexdigest(),
                           "read_scope": "Original public custody owner; no scientific credit."},
                "profile": {"path": self.profile, "sha256": hashlib.sha256(b"artifacts: []\n").hexdigest(),
                            "read_scope": "Synthetic publication owner."},
            },
            "works": [
                {"key": "one", "title": "Fixture one", "role": "supporting-reference", "source_keys": ["parent"]},
                {"key": "two", "title": "Fixture two", "role": "supporting-reference", "source_keys": ["parent"]},
            ],
            "probes": [
                {"key": "recognition-correction", "works": ["one"], "sources": ["parent"]},
                {"key": "tensor-geometry", "works": ["two"], "sources": ["parent"]},
                {"key": "cross-avenue", "works": ["one", "two"], "sources": ["parent"]},
            ],
        }

    def git(self, *args, input=None):
        return subprocess.check_output(["git", "--no-replace-objects", "--literal-pathspecs", *args],
                                       cwd=self.repo, input=input, stderr=subprocess.STDOUT)

    def source(self):
        gate = getattr(self.mod, "pmr007_rounds_parent_source_bytes", None)
        self.assertTrue(callable(gate), "The finite parent README navigation owner is missing")
        return gate(self.repo)

    def reader(self):
        return self.mod.check(self.repo, self.owners, self.cross)

    def test_exact_adaptation_preserves_both_owner_and_source_identity(self):
        self.target.write_bytes(self.adapted)
        before = (self.repo / ".git/index").read_bytes()
        self.assertEqual(self.reader(), [])
        self.assertEqual(self.source(), self.original)
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)
        self.git("add", "--", self.PARENT)
        before = (self.repo / ".git/index").read_bytes()
        self.assertEqual(self.reader(), [])
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)

    def test_original_wording_is_valid_while_the_original_edition_is_present(self):
        self.assertEqual(self.source(), self.original)
        self.assertEqual(self.reader(), [])

    def test_unrelated_prose_changes_are_not_navigation(self):
        self.target.write_bytes(self.adapted)
        self.assertEqual(self.source(), self.original)
        for body in (self.adapted + b"\nUnreviewed addition.\n",
                     self.adapted.replace(b"not adopted repository theory", b"adopted repository theory", 1),
                     self.adapted.replace(b"98 exact same-relative", b"99 exact same-relative", 1)):
            with self.subTest(body_sha=hashlib.sha256(body).hexdigest()):
                self.target.write_bytes(body)
                with self.assertRaises(ValueError):
                    self.source()
                self.assertTrue(any(e.startswith("navigation-source:") for e in self.reader()))

    def test_current_parent_missing_mode_and_symlink_changes_fail(self):
        self.target.write_bytes(self.adapted)
        self.assertEqual(self.source(), self.original)
        self.target.chmod(0o755)
        with self.assertRaises(ValueError):
            self.source()
        self.target.chmod(0o644)
        self.target.unlink()
        with self.assertRaises((ValueError, OSError)):
            self.source()
        other = self.repo / "ordinary-public-readme.md"
        other.write_bytes(self.adapted)
        self.target.symlink_to(other)
        with self.assertRaises(ValueError):
            self.source()
        self.target.unlink()
        self.target.write_bytes(self.adapted)
        directory = self.target.parent
        moved = self.repo / "ordinary-public-directory"
        directory.rename(moved)
        directory.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.source()

    def test_bad_staged_blob_cannot_hide_behind_the_exact_worktree(self):
        self.target.write_bytes(self.adapted + b"\nUnreviewed staged change.\n")
        self.git("add", "--", self.PARENT)
        self.target.write_bytes(self.adapted)
        before = (self.repo / ".git/index").read_bytes()
        with self.assertRaises(ValueError):
            self.source()
        self.assertTrue(any(e.startswith("navigation-source:") for e in self.reader()))
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)

    def test_staged_mode_removal_and_conflict_are_rejected(self):
        self.target.write_bytes(self.adapted)
        self.assertEqual(self.source(), self.original)
        original_blob = self.git("rev-parse", self.baseline + ":" + self.PARENT).decode().strip()
        for fault in ("mode", "missing", "conflict"):
            with self.subTest(fault=fault):
                self.git("reset", "-q", self.baseline, "--", self.PARENT)
                if fault == "mode":
                    self.git("update-index", "--chmod=+x", "--", self.PARENT)
                elif fault == "missing":
                    self.git("update-index", "--force-remove", "--", self.PARENT)
                else:
                    self.git("update-index", "--index-info", input=(
                        "0 " + "0" * 40 + "\t" + self.PARENT + "\n" +
                        "100644 " + original_blob + " 1\t" + self.PARENT + "\n" +
                        "100644 " + original_blob + " 2\t" + self.PARENT + "\n").encode())
                with self.assertRaises(ValueError):
                    self.source()

    def test_unavailable_staged_object_is_rejected(self):
        self.target.write_bytes(self.adapted)
        self.git("add", "--", self.PARENT)
        self.assertEqual(self.source(), self.original)
        oid = self.git("rev-parse", ":" + self.PARENT).decode().strip()
        (self.repo / ".git/objects" / oid[:2] / oid[2:]).unlink()
        with self.assertRaises(ValueError):
            self.source()

    def test_same_size_corrupted_original_object_is_rejected(self):
        import zlib
        self.target.write_bytes(self.adapted)
        self.assertEqual(self.source(), self.original)
        oid = self.git("rev-parse", self.baseline + ":" + self.PARENT).decode().strip()
        target = self.repo / ".git/objects" / oid[:2] / oid[2:]
        altered = b"!" + self.original[1:]
        target.unlink()
        target.write_bytes(zlib.compress(b"blob " + str(len(altered)).encode() + b"\0" + altered))
        with self.assertRaises(ValueError):
            self.source()

    def test_wrong_original_revision_and_original_path_identity_are_rejected(self):
        self.target.write_bytes(self.adapted)
        self.assertEqual(self.source(), self.original)
        for revision in ("HEAD", "0" * 40):
            with self.subTest(revision=revision):
                self.mod.PMR007_ROUNDS_PARENT_REVISION = revision
                with self.assertRaises(ValueError):
                    self.source()
        self.mod.PMR007_ROUNDS_PARENT_REVISION = self.baseline
        self.git("add", "--", self.PARENT)
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "Different current reading is not the original source")
        self.mod.PMR007_ROUNDS_PARENT_REVISION = self.git("rev-parse", "HEAD").decode().strip()
        with self.assertRaises(ValueError):
            self.source()

    def test_original_tree_mode_cannot_be_hidden_by_an_ordinary_current_file(self):
        self.assertEqual(self.source(), self.original)
        self.target.chmod(0o755)
        self.git("add", "--", self.PARENT)
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "Wrong original tree mode")
        self.mod.PMR007_ROUNDS_PARENT_REVISION = self.git("rev-parse", "HEAD").decode().strip()
        self.target.chmod(0o644)
        self.target.write_bytes(self.adapted)
        self.git("reset", "-q", self.baseline, "--", self.PARENT)
        with self.assertRaises(ValueError):
            self.source()

    def test_incomplete_worktree_edition_requires_current_adapted_wording(self):
        self.assertEqual(self.source(), self.original)
        (self.repo / self.members[0]).unlink()
        with self.assertRaises(ValueError):
            self.source()
        self.target.write_bytes(self.adapted)
        self.assertEqual(self.source(), self.original)

    def test_incomplete_index_edition_requires_staged_adapted_wording(self):
        self.target.write_bytes(self.adapted)
        self.assertEqual(self.source(), self.original)
        self.git("update-index", "--force-remove", "--", self.members[0])
        with self.assertRaises(ValueError):
            self.source()
        self.git("add", "--", self.PARENT)
        self.assertEqual(self.source(), self.original)

    def test_current_hash_refresh_cannot_replace_original_source_identity(self):
        self.target.write_bytes(self.adapted)
        self.cross["sources"]["parent"]["sha256"] = hashlib.sha256(self.adapted).hexdigest()
        self.assertTrue(any(e.startswith("source-drift: parent") for e in self.reader()))

    def test_discovery_owner_baseline_must_still_match_the_original(self):
        self.target.write_bytes(self.adapted)
        self.git("add", "--", self.PARENT)
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "Different discovery baseline")
        self.owners["baseline"]["commit"] = self.git("rev-parse", "HEAD").decode().strip()
        errors = self.reader()
        self.assertTrue(any(e.startswith("owner: " + self.PARENT) for e in errors), errors)
        self.assertTrue(any(e.startswith("baseline-source: " + self.PARENT) for e in errors), errors)

    def test_unrelated_discovery_owner_remains_strict(self):
        self.target.write_bytes(self.adapted)
        (self.repo / self.profile).write_text("artifacts: []\n# Unreviewed source change.\n")
        errors = self.reader()
        self.assertTrue(any(e.startswith("owner: " + self.profile) for e in errors), errors)
        self.assertTrue(any(e.startswith("baseline-source: " + self.profile) for e in errors), errors)


class ContinuationOwnerEditionTests(unittest.TestCase):
    """The four existing owners change only as one exact staged/readable edition."""
    PATHS = (
        "docs/provenance/v5-research-continuations/EVIDENCE_BINDINGS.json",
        "docs/provenance/v5-research-continuations/README.md",
        "docs/provenance/v5-research-continuations/SOURCE_MAP.json",
        "experiments/orthemology-v5-continuations/registry.json",
    )

    def setUp(self):
        ReaderPilotTests.setUp(self)
        self.original = {path: ("Synthetic original owner %d.\n" % number).encode()
                         for number, path in enumerate(self.PATHS)}
        self.current = {path: ("Synthetic consolidated owner %d.\n" % number).encode()
                        for number, path in enumerate(self.PATHS)}
        for path, body in self.original.items():
            node = self.repo / path
            node.parent.mkdir(parents=True, exist_ok=True)
            node.write_bytes(body)
            self.cross["sources"][path] = {
                "path": path, "sha256": hashlib.sha256(body).hexdigest(),
                "read_scope": "Synthetic exact continuation discovery owner.",
            }
        self.owners["collections"].extend([
            {"key": "continuation-docs", "include": ["docs/provenance/v5-research-continuations/"],
             "owners": list(self.PATHS[:3])},
            {"key": "continuation-data", "include": ["experiments/orthemology-v5-continuations/"],
             "owners": [self.PATHS[3]]},
        ])
        self.git("add", "--", *self.PATHS)
        self.git("commit", "-qm", "Synthetic original continuation owners")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.owners["baseline"]["commit"] = self.base
        # Only the finite edition identities change for this synthetic repository.
        # Native stage queries, ordinary reads, and all three reader gates are real.
        self.mod.CONTINUATION_OWNER_ORIGINAL = self.identities(self.original)
        self.mod.CONTINUATION_OWNER_CURRENT = self.identities(self.current)

    def git(self, *args, input=None):
        return subprocess.check_output(["git", "--no-replace-objects", "--literal-pathspecs", *args],
                                       cwd=self.repo, input=input, stderr=subprocess.DEVNULL).decode()

    @staticmethod
    def identities(bodies):
        return {path: (hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest(),
                       hashlib.sha256(body).hexdigest(), len(body))
                for path, body in bodies.items()}

    def edition(self, bodies, *, stage=True):
        for path, body in bodies.items():
            (self.repo / path).write_bytes(body)
            self.cross["sources"][path]["sha256"] = hashlib.sha256(body).hexdigest()
        if stage:
            self.git("add", "--", *self.PATHS)

    def check(self):
        return self.mod.check(self.repo, self.owners, self.cross)

    def rejected(self, *, currentness=False):
        before = (self.repo / ".git/index").read_bytes()
        errors = self.check()
        self.assertTrue(errors, "An incomplete or unregistered owner edition was accepted")
        if currentness:
            self.assertTrue(any(e.startswith("corpus-currentness:") for e in errors), errors)
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)

    def test_original_four_owner_edition_remains_accepted(self):
        before = (self.repo / ".git/index").read_bytes()
        self.assertEqual(self.check(), [])
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)

    def test_complete_current_edition_crosses_all_three_original_census_gates(self):
        self.edition(self.current)
        before = (self.repo / ".git/index").read_bytes()
        self.assertEqual(self.check(), [])
        self.assertEqual((self.repo / ".git/index").read_bytes(), before)

    def test_original_index_cannot_authorize_current_worktree(self):
        self.edition(self.current, stage=False)
        self.rejected(currentness=True)

    def test_current_index_cannot_authorize_original_worktree(self):
        self.edition(self.current)
        self.edition(self.original, stage=False)
        self.rejected(currentness=True)

    def test_each_mixed_worktree_owner_is_rejected(self):
        for path in self.PATHS:
            with self.subTest(path=path):
                self.edition(self.current)
                (self.repo / path).write_bytes(self.original[path])
                self.rejected(currentness=True)

    def test_each_mixed_staged_owner_is_rejected(self):
        for path in self.PATHS:
            with self.subTest(path=path):
                self.edition(self.current)
                self.git("reset", "-q", self.base, "--", path)
                self.rejected(currentness=True)

    def test_tampered_worktree_cannot_refresh_its_source_hash(self):
        self.edition(self.current)
        path = self.PATHS[0]
        body = self.current[path] + b"Unregistered owner change.\n"
        (self.repo / path).write_bytes(body)
        self.cross["sources"][path]["sha256"] = hashlib.sha256(body).hexdigest()
        self.rejected(currentness=True)

    def test_tampered_stage_cannot_hide_behind_exact_current_bytes(self):
        self.edition(self.current)
        path = self.PATHS[2]
        (self.repo / path).write_bytes(self.current[path] + b"Unregistered staged owner.\n")
        self.git("add", "--", path)
        (self.repo / path).write_bytes(self.current[path])
        self.rejected(currentness=True)

    def test_staged_mode_missing_and_conflicted_owners_are_rejected(self):
        path = self.PATHS[1]
        for fault in ("mode", "missing", "conflict"):
            with self.subTest(fault=fault):
                self.edition(self.current)
                if fault == "mode":
                    self.git("update-index", "--chmod=+x", "--", path)
                elif fault == "missing":
                    self.git("update-index", "--force-remove", "--", path)
                else:
                    oid = self.identities(self.current)[path][0]
                    self.git("update-index", "--index-info", input=(
                        "0 " + "0" * 40 + "\t" + path + "\n" +
                        "100644 " + oid + " 1\t" + path + "\n" +
                        "100644 " + oid + " 2\t" + path + "\n").encode())
                self.rejected()

    def test_nonordinary_worktree_owners_are_rejected(self):
        import os
        path = self.PATHS[1]
        node = self.repo / path
        for fault in ("executable", "symlink", "hardlink", "directory"):
            with self.subTest(fault=fault):
                self.edition(self.current)
                other = self.repo / ("ordinary-fixture-" + fault)
                if fault == "executable":
                    node.chmod(0o755)
                elif fault == "symlink":
                    other.write_bytes(self.current[path]); node.unlink(); node.symlink_to(other)
                elif fault == "hardlink":
                    os.link(node, other)
                else:
                    node.unlink(); node.mkdir()
                self.rejected()
                if fault == "directory":
                    node.rmdir()
                elif fault == "symlink":
                    node.unlink(); other.unlink()
                elif fault == "hardlink":
                    other.unlink()
                node.write_bytes(self.current[path]); node.chmod(0o644)

    def test_owner_deletion_and_adjacent_unregistered_addition_are_not_modifications(self):
        self.edition(self.current)
        path = self.PATHS[0]
        (self.repo / path).unlink()
        self.git("add", "--", path)
        self.rejected(currentness=True)
        self.edition(self.current)
        extra = "/".join(("docs", "provenance", "v5-research-continuations", "UNREGISTERED.json"))
        (self.repo / extra).write_bytes(b"Synthetic unregistered source.\n")
        self.git("add", "--", extra)
        self.rejected(currentness=True)

    def test_current_edition_cannot_replace_the_original_census(self):
        self.edition(self.current)
        self.git("commit", "-qm", "Synthetic changed census is not an original edition")
        self.owners["baseline"]["commit"] = self.git("rev-parse", "HEAD").strip()
        self.rejected()


class ContinuationNoteReaderMigrationTests(unittest.TestCase):
    """Four incorporated readers keep exact historical identity and current science.

    The command double below checks Python validation against exact public note
    bodies. It is not native Git, restoration, custody or deletion evidence.
    """

    REV = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
    OWNER = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    CROSS = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    REVIEW = 'docs/scientific-consolidation-review.md'
    NOTES = {
        'continuation-note-41': (
            'a9eb8521054eb3769ff424037f438ae38f0f0c113d73624efc9d05dea3b35483',
            'ae198b6530ccb5cdce3e15616d939575f7878d28', 13358,
            'continuation-local-rigidity', 'consolidated-common-repair',
            'mathematics/common-repair-and-geometric-obstructions.md',
            '2-quadratic-repair-exact-compatibility-and-quantitative-separation',
            ('continuation-note-40',)),
        'continuation-note-37': (
            '002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e',
            '2804e7b196437dd437f0099b15aa45a76249e63b', 6680,
            'continuation-statistical-repair', 'consolidated-information-and-inquiry',
            'mathematics/information-and-inquiry.md',
            'a-finite-sample-lower-bound-and-the-meaning-of-a-fresh-observation',
            ('continuation-note-34',)),
        'continuation-note-28': (
            '4878fd0a4cf6c952af7cdbcb7e8a386c2730ff9986b74b8e39bf9b5077815b0f',
            'f419024deb2a40bf50f7315cdf2dfdde9ede77f6', 15286,
            'continuation-finite-query', 'consolidated-information-and-inquiry',
            'mathematics/information-and-inquiry.md',
            'finite-harmful-probing-and-eventual-exact-repair',
            ('continuation-note-34',)),
        'continuation-note-31': (
            'b0672a56d007c718a42a7ee6fdc875c915630ad95dff5cfbae7f7e9a419d5349',
            '937f0464dcaa515f1c002a8b36add0c4cb511b42', 5601,
            'continuation-binary-experiment', 'consolidated-information-and-inquiry',
            'mathematics/information-and-inquiry.md',
            'a-shared-feedback-controller-with-literal-score-targets',
            ('continuation-note-34', 'continuation-note-1')),
    }

    @classmethod
    def setUpClass(cls):
        import check_reader_pilot
        import resolve_t20_v6_source
        cls.reader, cls.resolver = check_reader_pilot, resolve_t20_v6_source
        cls.original_owners = json.loads((ROOT / cls.OWNER).read_bytes())
        # Keep the accepted sixteen-path fixture distinct from the later T4 extension.
        earlier = (set(cls.resolver.ORIGINAL_HISTORICAL_PROSE_PATHS)
                   | set(cls.resolver.MEDIATOR_PROSE) | {cls.resolver.FISHER_AUDIT}
                   | set(cls.resolver.TYPED_PROSE) | set(cls.resolver.CONTINUATION_READER_PROSE))
        cls.original_owners['historical_source_bindings'] = [row
            for row in cls.original_owners['historical_source_bindings'] if row['path'] in earlier]
        cls.original_cross = json.loads((ROOT / cls.CROSS).read_bytes())
        cls.catalogue = (ROOT / 'docs/reader/PAPER-CATALOGUE.md').read_text()
        cls.paths = {key: 'docs/provenance/v5-research-continuations/notes/' + row[0] + '.md'
                     for key, row in cls.NOTES.items()}
        cls.current = {path: (ROOT / path).read_bytes()
                       for path in {cls.REVIEW, *(row[5] for row in cls.NOTES.values())}}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='continuation-note-reader-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.owners = deepcopy(self.original_owners)
        self.cross = deepcopy(self.original_cross)
        for path, body in self.current.items():
            self.put(path, body)
        self.save()

    def put(self, path, body):
        node = self.root / path
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(body)
        node.chmod(0o644)

    def save(self):
        self.put(self.OWNER, json.dumps(self.owners).encode())
        self.put(self.CROSS, json.dumps(self.cross).encode())

    def context(self):
        gate = getattr(self.resolver, 'require_continuation_note_context', None)
        self.assertTrue(callable(gate), 'the exact four-note historical context is not implemented')
        return gate(self.root)

    def original(self, key):
        row = self.NOTES[key]
        body = subprocess.check_output(
            ['git', '--no-replace-objects', 'cat-file', 'blob', row[1]], cwd=ROOT)
        self.assertEqual((len(body), hashlib.sha256(body).hexdigest()), (row[2], row[0]))
        return body

    def resolve(self, key, *, stage=b'', tree_mode='100644', unavailable=False,
                historical_body=None, revision=None, blob=None):
        from unittest.mock import patch
        row, path = self.NOTES[key], self.paths[key]
        original = self.original(key)
        command_body = original if historical_body is None else historical_body
        prefix = ['git', '--no-replace-objects', '--literal-pathspecs']
        answers = {
            ('cat-file', '-t', self.REV): b'commit\n',
            ('ls-tree', '-z', self.REV, '--', path):
                (tree_mode + ' blob ' + row[1] + '\t' + path + '\0').encode(),
            ('cat-file', 'blob', row[1]): command_body,
            ('ls-files', '--stage', '-z', '--', path): stage,
        }

        def command(args, *, cwd, capture_output, check):
            if (Path(cwd) != self.root or list(args[:3]) != prefix
                    or tuple(args[3:]) not in answers or capture_output is not True or check is not False):
                raise AssertionError('unexpected historical command outside the four-note Python fixture')
            return subprocess.CompletedProcess(args, 1 if unavailable else 0,
                b'' if unavailable else answers[tuple(args[3:])], b'')

        with patch.object(self.resolver.subprocess, 'run', command):
            return self.resolver.historical_source_bytes(
                self.root, path, self.REV if revision is None else revision,
                row[1] if blob is None else blob)

    def test_exact_four_note_context_accepts_current_scholarship(self):
        self.context()

    def test_four_catalogue_sections_reach_current_treatments_and_exact_history(self):
        page = self.reader.markdown_index(self.catalogue)
        for key, row in self.NOTES.items():
            with self.subTest(source=key):
                works = [w for w in self.cross['works'] if w['key'] == row[3]]
                self.assertEqual(len(works), 1)
                work = works[0]
                self.assertEqual(work['source_keys'], [key])
                self.assertEqual(work['reading_forms'], [{'source': key, 'relationship': 'historical-source'}])
                fragment = work['catalogue_entry'].partition('#')[2]
                selected = [h for h in page['headings'] if h[0] == fragment]
                self.assertEqual(len(selected), 1)
                _, level, start = selected[0]
                end = next((h[2] for h in page['headings'] if h[2] > start and h[1] <= level), page['line_count'])
                links = {href for line, href in page['links'] if start <= line < end}
                self.assertIn('../../' + row[5] + '#' + row[6], links)
                self.assertIn('https://github.com/theislampill/orthemology/blob/' + self.REV + '/' + self.paths[key], links)
                self.assertNotIn('../../' + self.paths[key], links)
                self.assertIn(row[6], self.reader.markdown_index(self.current[row[5]].decode())['anchors'])

    def test_missing_duplicate_partial_or_fifth_historical_binding_is_rejected(self):
        self.context()
        original = deepcopy(self.owners)
        for fault in ('missing-note', 'duplicate-note', 'missing-earlier', 'fifth-note'):
            with self.subTest(fault=fault):
                self.owners = deepcopy(original)
                rows = self.owners['historical_source_bindings']
                if fault == 'missing-note':
                    rows[:] = [r for r in rows if r['path'] != self.paths['continuation-note-31']]
                elif fault == 'duplicate-note':
                    rows.append(deepcopy(next(r for r in rows if r['path'] == self.paths['continuation-note-31'])))
                elif fault == 'missing-earlier':
                    rows.pop(0)
                else:
                    row = deepcopy(next(r for r in rows if r['path'] == self.paths['continuation-note-31']))
                    row['path'] = 'docs/provenance/v5-research-continuations/notes/' + '0' * 64 + '.md'
                    rows.append(row)
                self.save()
                with self.assertRaises(ValueError):
                    self.context()

    def test_each_note_requires_its_exact_owner_and_incorporation(self):
        self.context()
        original_owners, original_cross = deepcopy(self.owners), deepcopy(self.cross)
        for key, item in self.NOTES.items():
            for fault in ('revision', 'blob', 'reading-owner', 'source-path', 'source-hash',
                          'work-source', 'reading-form', 'support', 'missing-relation',
                          'duplicate-relation', 'wrong-destination', 'wrong-basis', 'wrong-kind', 'journey'):
                with self.subTest(source=key, fault=fault):
                    self.owners, self.cross = deepcopy(original_owners), deepcopy(original_cross)
                    binding = next(r for r in self.owners['historical_source_bindings'] if r['path'] == self.paths[key])
                    work = next(w for w in self.cross['works'] if w['key'] == item[3])
                    relation = next(r for r in self.cross['relations'] if r.get('from') == key)
                    if fault == 'revision': binding['repository_revision'] = 'HEAD'
                    elif fault == 'blob': binding['git_blob'] = '0' * 40
                    elif fault == 'reading-owner': binding['reading_source'] = 'consolidated-encodings-and-witnesses'
                    elif fault == 'source-path': self.cross['sources'][key]['path'] += '.wrong'
                    elif fault == 'source-hash': self.cross['sources'][key]['sha256'] = '0' * 64
                    elif fault == 'work-source': work['source_keys'] = [item[4]]
                    elif fault == 'reading-form': work['reading_forms'][0]['relationship'] = 'retained-source-reading-projection'
                    elif fault == 'support': work['supporting_source_keys'] = []
                    elif fault == 'missing-relation': self.cross['relations'].remove(relation)
                    elif fault == 'duplicate-relation': self.cross['relations'].append(deepcopy(relation))
                    elif fault == 'wrong-destination': relation['to'] = 'consolidated-encodings-and-witnesses'
                    elif fault == 'wrong-basis': relation['basis'] = key
                    elif fault == 'wrong-kind': relation['kind'] = 'related-source'
                    else: self.cross['reader_journeys'][0]['source_keys'].append(key)
                    self.save()
                    with self.assertRaises(ValueError):
                        self.context()

    def test_changed_or_missing_current_chapter_and_review_are_rejected(self):
        self.context()
        for path, body in self.current.items():
            with self.subTest(path=path):
                self.put(path, body + b'\nchanged current edition\n')
                with self.assertRaises(ValueError):
                    self.context()
                self.put(path, body)
                (self.root / path).unlink()
                with self.assertRaises((ValueError, OSError)):
                    self.context()
                self.put(path, body)

    def test_absent_and_exact_present_notes_use_exact_history_without_recreation(self):
        self.context()
        for key in self.NOTES:
            with self.subTest(source=key):
                node = self.root / self.paths[key]
                self.assertFalse(node.exists())
                self.assertEqual(self.resolve(key), self.original(key))
                self.assertFalse(node.exists(), 'historical validation must not recreate a note')
                self.put(self.paths[key], self.original(key))
                self.assertEqual(self.resolve(key), self.original(key))

    def test_wrong_present_note_mode_and_symlink_cannot_fall_back(self):
        self.context()
        for key in self.NOTES:
            with self.subTest(source=key):
                path = self.paths[key]
                node = self.root / path
                self.put(path, self.original(key) + b'wrong edition\n')
                with self.assertRaises(ValueError): self.resolve(key)
                self.put(path, self.original(key))
                node.chmod(0o755)
                with self.assertRaises(ValueError): self.resolve(key)
                node.unlink()
                target = node.with_suffix('.exact-fixture')
                target.write_bytes(self.original(key))
                node.symlink_to(target)
                with self.assertRaises(ValueError): self.resolve(key)
                node.unlink()

    def test_wrong_history_and_index_cannot_be_hidden_by_absence(self):
        self.context()
        for key, row in self.NOTES.items():
            with self.subTest(source=key):
                path = self.paths[key]
                for kwargs in (
                    {'revision': 'HEAD'}, {'blob': '0' * 40}, {'tree_mode': '100755'},
                    {'stage': ('100644 ' + '0' * 40 + ' 0\t' + path + '\0').encode()},
                    {'stage': ('100755 ' + row[1] + ' 0\t' + path + '\0').encode()},
                    {'stage': ('100644 ' + row[1] + ' 1\t' + path + '\0').encode()},
                    {'unavailable': True}, {'historical_body': self.original(key) + b'corrupted object\n'},
                ):
                    with self.subTest(fault=tuple(kwargs)), self.assertRaises(ValueError):
                        self.resolve(key, **kwargs)

    def test_reader_note_history_does_not_create_new_t20_public_forms(self):
        self.context()
        from unittest.mock import patch
        manifest = json.loads((ROOT / 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json').read_bytes())
        public_rows = {row.get('repository_path'): row for row in manifest['objects']
                       if row.get('disposition') in ('REUSE', 'ADD_EXACT', 'PROJECT')}
        # These six already-published identities retain REUSE. Their genuine
        # present/absent Git route is exercised by the projection tests; this
        # reader fixture has no Git history and cannot prove their rejection.
        existing = {
            '002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e',
            '4878fd0a4cf6c952af7cdbcb7e8a386c2730ff9986b74b8e39bf9b5077815b0f',
            '7d3cbeb8bcacdb5d28cb457801ba41de9b21f91542866fe5c5f13a4a632dadd9',
            'b092780b29dd9fa00ac276142b090a5b8b88da79da9c278268264669e08f3d8c',
            '34c1f25cd1144b386ff4c70a2fbfacc7da2a0fc87f5cd78b430badf260ab49f6',
            '9438fdcbea8747c7e5599483096eca9541cfdf673d6a96866c019c5ced06519a',
        }
        for key, row in self.NOTES.items():
            with self.subTest(source=key):
                if row[0] in existing:
                    selected = public_rows[self.paths[key]]
                    self.assertEqual((selected['disposition'], selected['source_sha256'],
                                      selected['public_sha256'], selected['source_bytes'],
                                      selected['public_bytes']),
                                     ('REUSE', row[0], row[0], row[2], row[2]))
                    continue
                self.assertNotIn(self.paths[key], public_rows)
                public = dict(repository_path=self.paths[key], repository_revision=self.REV,
                    git_blob=row[1], disposition='REUSE', source_sha256=row[0],
                    source_bytes=row[2], public_sha256=row[0], public_bytes=row[2])
                with patch.object(self.resolver, 'historical_source_bytes',
                                  side_effect=AssertionError('nonpublic reader source reached a body read')), \
                     self.assertRaises(ValueError):
                    self.resolver.source_bytes(self.root, public)




class T4NoteReaderMigrationTests(unittest.TestCase):
    """Ten exact reader aliases: six works and four support-only originals.

    The inherited byte controls test Python admission using a command adapter;
    genuine Git qualification is a separate fixture and custody is not inferred.
    """

    REV = 'b4d58482ae00f138782276ee5c4034c48bb2df19'
    OWNER = ContinuationNoteReaderMigrationTests.OWNER
    CROSS = ContinuationNoteReaderMigrationTests.CROSS
    REVIEW = ContinuationNoteReaderMigrationTests.REVIEW
    NOTES = {'continuation-note-83': ('285a7061f8f090946e27e5ff6bd7597b7a0f0472100c7e4b3cb57ea5ac12f6a7',
                          '40d509699e094815d445af4b3fb63cbb1079c4b0',
                          6182,
                          'continuation-beta-budget',
                          'consolidated-information-and-inquiry',
                          'mathematics/information-and-inquiry.md',
                          'a-sharp-beta-prior-lifetime-boundary',
                          ('continuation-note-88', 'continuation-note-86')),
 'continuation-note-84': ('3b7cdb283b858339136beb1e0d62cbd32adce0ee9f0562db8961a9f819f52000',
                          'a12e7f7c10894591e1b1e13c26ba99377492563d',
                          2966,
                          'continuation-reporting-clock',
                          'consolidated-information-and-inquiry',
                          'mathematics/information-and-inquiry.md',
                          'a-declared-deterministic-reporting-clock',
                          ('continuation-note-85', 'continuation-note-90')),
 'continuation-note-85': ('3b8f7d96fa99674b73cb8f822cc3291d455c52879b2f1110630be67660883317',
                          '9715b8685253581e9187c44b2b4a4d81ad74ae73',
                          8219,
                          'continuation-beta-rates',
                          'consolidated-information-and-inquiry',
                          'mathematics/information-and-inquiry.md',
                          'finite-horizon-rates-and-an-exact-bayes-existence-statement',
                          ('continuation-note-83', 'continuation-note-90')),
 'continuation-note-86': ('196728a62cb7bdb24160b33c0ae3627a822f8b2b031fe033e275d6d284efa7df',
                          'af853c549ee6b1b320cf38e14358ded327f9dced',
                          10906,
                          'continuation-all-policy-cost',
                          'consolidated-information-and-inquiry',
                          'mathematics/information-and-inquiry.md',
                          'pointwise-finite-expectation-and-an-unavoidable-endpoint-cost',
                          ('continuation-note-89',)),
 'continuation-note-87': ('7d3cbeb8bcacdb5d28cb457801ba41de9b21f91542866fe5c5f13a4a632dadd9',
                          '07a1df58ff170334e07261c93af8345093b0f160',
                          14328,
                          'continuation-endpoint-density',
                          'consolidated-information-and-inquiry',
                          'mathematics/information-and-inquiry.md',
                          'endpoint-density-robustness-with-atoms-handled-separately',
                          ('continuation-note-85', 'continuation-note-90')),
 'continuation-note-88': ('826c824188b79a5e734c77f4aaa24f5ecf15d1a73e7af0d68ad8b8955bb674ab',
                          'fbd42a9270e356e4c361695ea28df58aaba773c9',
                          6121,
                          None,
                          'consolidated-information-and-inquiry',
                          'mathematics/information-and-inquiry.md',
                          'a-sharp-beta-prior-lifetime-boundary',
                          None),
 'continuation-note-89': ('575700cb383a6f0849e2a952ba6652e6de75920eb74ebcb9a7eb0ed21517a696',
                          '9be9a40bb2d6b3a4e94d6e06ae8e68b8b3198bda',
                          5443,
                          None,
                          'consolidated-information-and-inquiry',
                          'mathematics/information-and-inquiry.md',
                          'pointwise-finite-expectation-and-an-unavoidable-endpoint-cost',
                          None),
 'continuation-note-92': ('b092780b29dd9fa00ac276142b090a5b8b88da79da9c278268264669e08f3d8c',
                          '4e69862256f3014f8e94d528b13ff0f63dd7f3eb',
                          29013,
                          'continuation-markov',
                          'consolidated-collective-inquiry',
                          'mathematics/collective-inquiry-and-strategic-coordination.md',
                          '714-stateful-learning-with-revealing-observations',
                          ('continuation-note-96', 'continuation-note-97')),
 'continuation-note-96': ('34c1f25cd1144b386ff4c70a2fbfacc7da2a0fc87f5cd78b430badf260ab49f6',
                          '6bcd9f7c0faea3fe3037c1f188288555312517b1',
                          1017,
                          None,
                          'consolidated-collective-inquiry',
                          'mathematics/collective-inquiry-and-strategic-coordination.md',
                          'exact-computation-and-reduction-to-the-earlier-models',
                          None),
 'continuation-note-97': ('9438fdcbea8747c7e5599483096eca9541cfdf673d6a96866c019c5ced06519a',
                          '80e45c60c8f4e71a8191f906d04afd4ab0384b06',
                          11145,
                          None,
                          'consolidated-collective-inquiry',
                          'mathematics/collective-inquiry-and-strategic-coordination.md',
                          'deterministic-scheduling-without-resetting-away-progress',
                          None)}
    SUPPORT_USERS = {'continuation-note-83': ['continuation-beta-rates'],
 'continuation-note-84': [],
 'continuation-note-85': ['continuation-endpoint-density', 'continuation-reporting-clock'],
 'continuation-note-86': ['continuation-beta-budget'],
 'continuation-note-87': [],
 'continuation-note-88': ['continuation-beta-budget'],
 'continuation-note-89': ['continuation-all-policy-cost'],
 'continuation-note-92': [],
 'continuation-note-96': ['continuation-markov'],
 'continuation-note-97': ['continuation-markov']}

    @classmethod
    def setUpClass(cls):
        import check_reader_pilot
        import resolve_t20_v6_source
        cls.reader, cls.resolver = check_reader_pilot, resolve_t20_v6_source
        cls.original_owners = json.loads((ROOT / cls.OWNER).read_bytes())
        cls.original_cross = json.loads((ROOT / cls.CROSS).read_bytes())
        cls.catalogue = (ROOT / 'docs/reader/PAPER-CATALOGUE.md').read_text()
        cls.paths = {key: 'docs/provenance/v5-research-continuations/notes/' + row[0] + '.md'
                     for key, row in cls.NOTES.items()}
        cls.current = {path: (ROOT / path).read_bytes()
                       for path in {cls.REVIEW, *(row[5] for row in cls.NOTES.values())}}

    setUp = ContinuationNoteReaderMigrationTests.setUp
    put = ContinuationNoteReaderMigrationTests.put
    save = ContinuationNoteReaderMigrationTests.save
    original = ContinuationNoteReaderMigrationTests.original
    resolve = ContinuationNoteReaderMigrationTests.resolve

    def context(self):
        gate = getattr(self.resolver, 'require_t4_note_context', None)
        self.assertTrue(callable(gate), 'the exact T4 historical context is not implemented')
        return gate(self.root)

    def test_exact_ten_alias_context_requires_current_scholarship(self):
        self.context()

    def test_six_work_routes_and_four_support_roles_reach_current_treatments(self):
        self.context()
        page = self.reader.markdown_index(self.catalogue)
        for key, row in self.NOTES.items():
            with self.subTest(source=key):
                works = [w for w in self.cross['works'] if key in w['source_keys']]
                forms = [form for w in self.cross['works'] for form in w.get('reading_forms', [])
                         if form.get('source') == key]
                users = sorted(w['key'] for w in self.cross['works']
                               if key in w.get('supporting_source_keys', []))
                self.assertEqual(users, self.SUPPORT_USERS[key])
                if row[3] is None:
                    self.assertEqual(works, [])
                    self.assertEqual(forms, [])
                else:
                    self.assertEqual([w['key'] for w in works], [row[3]])
                    self.assertEqual(forms, [{'source': key, 'relationship': 'historical-source'}])
                    fragment = works[0]['catalogue_entry'].partition('#')[2]
                    heading = [h for h in page['headings'] if h[0] == fragment]
                    self.assertEqual(len(heading), 1)
                    _, level, start = heading[0]
                    end = next((h[2] for h in page['headings'] if h[2] > start and h[1] <= level), page['line_count'])
                    links = {href for line, href in page['links'] if start <= line < end}
                    self.assertIn('../../' + row[5] + '#' + row[6], links)
                    self.assertIn('https://github.com/theislampill/orthemology/blob/' + self.REV + '/' + self.paths[key], links)
                    self.assertNotIn('../../' + self.paths[key], links)
                self.assertIn(row[6], self.reader.markdown_index(self.current[row[5]].decode())['anchors'])

    def test_partial_extra_duplicate_or_live_residual_cannot_enter_the_finite_population(self):
        from unittest.mock import patch
        self.context()
        original = deepcopy(self.owners)
        for fault in ('partial25', 'extra27', 'duplicate27', 'missing-earlier', 'residual-substitution'):
            with self.subTest(fault=fault):
                self.owners = deepcopy(original)
                rows = self.owners['historical_source_bindings']
                selected = next(r for r in rows if r['path'] == self.paths['continuation-note-88'])
                if fault == 'partial25': rows.remove(selected)
                elif fault == 'duplicate27': rows.append(deepcopy(selected))
                elif fault == 'missing-earlier': rows.pop(0)
                elif fault == 'residual-substitution':
                    selected['path'] = 'docs/provenance/v5-research-continuations/notes/9412522bec33bc12a790e1610d328b160a00cf25eea03126ec219f01abc5e5ac.md'
                else:
                    rows.append(dict(selected, path='docs/provenance/v5-research-continuations/notes/' + '0' * 64 + '.md'))
                self.save()
                with self.assertRaises(ValueError): self.context()
                with patch.object(self.reader.subprocess, 'run', side_effect=AssertionError('native access before finite gate')):
                    admitted, errors = self.reader.check_historical_sources(self.root, {}, self.owners, self.cross, {})
                self.assertEqual(admitted, {})
                self.assertTrue(any('expected exactly' in error for error in errors), errors)

    def test_each_alias_preserves_its_exact_work_or_support_ownership(self):
        self.context()
        initial_owner, initial_cross = deepcopy(self.owners), deepcopy(self.cross)
        for key, row in self.NOTES.items():
            faults = ('revision', 'blob', 'source-hash', 'relation', 'role', 'support', 'journey')
            for fault in faults:
                with self.subTest(source=key, fault=fault):
                    self.owners, self.cross = deepcopy(initial_owner), deepcopy(initial_cross)
                    binding = next(r for r in self.owners['historical_source_bindings'] if r['path'] == self.paths[key])
                    relation = next(r for r in self.cross['relations'] if r.get('from') == key)
                    if fault == 'revision': binding['repository_revision'] = 'HEAD'
                    elif fault == 'blob': binding['git_blob'] = '0' * 40
                    elif fault == 'source-hash': self.cross['sources'][key]['sha256'] = '0' * 64
                    elif fault == 'relation': relation['to'] = 'consolidated-encodings-and-witnesses'
                    elif fault == 'journey': self.cross['reader_journeys'][0]['source_keys'].append(key)
                    elif row[3] is None:
                        work = next(w for w in self.cross['works'] if w['key'] == self.SUPPORT_USERS[key][0])
                        if fault == 'role': work['reading_forms'].append({'source': key, 'relationship': 'historical-source'})
                        else: work['supporting_source_keys'].remove(key)
                    else:
                        work = next(w for w in self.cross['works'] if w['key'] == row[3])
                        if fault == 'role': work['reading_forms'][0]['relationship'] = 'retained-source-reading-projection'
                        else: work['supporting_source_keys'] = []
                    self.save()
                    with self.assertRaises(ValueError): self.context()

    test_changed_or_missing_current_chapter_and_review_are_rejected = ContinuationNoteReaderMigrationTests.test_changed_or_missing_current_chapter_and_review_are_rejected
    test_absent_and_exact_present_notes_use_exact_history_without_recreation = ContinuationNoteReaderMigrationTests.test_absent_and_exact_present_notes_use_exact_history_without_recreation
    test_wrong_present_note_mode_and_symlink_cannot_fall_back = ContinuationNoteReaderMigrationTests.test_wrong_present_note_mode_and_symlink_cannot_fall_back
    test_wrong_history_and_index_cannot_be_hidden_by_absence = ContinuationNoteReaderMigrationTests.test_wrong_history_and_index_cannot_be_hidden_by_absence
    test_reader_note_history_does_not_create_new_t20_public_forms = ContinuationNoteReaderMigrationTests.test_reader_note_history_does_not_create_new_t20_public_forms


class Next24HistoricalMigrationTests(unittest.TestCase):
    """Exact public native Git originals, finite owner roles and negative controls.

    The literal cohort comes from the independently frozen scientific inputs.
    Only selected public objects enter each fixture; no full checkout is made.
    """
    REV = 'd0abc116b51f04c064fc60ebbdd511b63a795f45'
    OWNER = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    CROSS = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    REVIEW = 'docs/scientific-consolidation-review.md'
    MANIFEST = 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
    ROWS = {1: ('e46c8d347ed1864c6c65270b0b7e90eef0146815804bb9f783fa465cd3fbc8bc',
     'a95a68888f591e035b04baa14075445fd25325b7',
     4411,
     'consolidated-common-repair'),
 2: ('b0ec9163de7f6deb49f44bb10ef1f279151ee78a30b9d2dd7ca9736d8bb62750',
     '7d1536017f2dd2a22a2137f05c9cde0820908787',
     12456,
     'consolidated-common-repair'),
 3: ('ad15c28206a020cc7c063c17309d6bd3c05e182377a398c7507875523df7feb4',
     '848f8f45967ddc66c76550ec2b44d233ba7966e9',
     5091,
     'consolidated-information-and-inquiry'),
 4: ('1b7488aeafc74b7115479a8cf73c0abf04d89c3924109aa922ee6099e32be2d8',
     '2c9205fdd87f3702af3e238f5cfd1b6240013ee4',
     11570,
     'consolidated-information-and-inquiry'),
 5: ('9e00aaaaa63828e05d252e134dc225e2718461540301138a30567fbb63a24eb9',
     'bcf29dd85a92b76483cbeacd9a6fd63343687dc1',
     6770,
     'consolidated-information-and-inquiry'),
 6: ('4f3d54cd93718e479f1485c182058bcd5ee40c13e4b9f598e4a011e6a92adaa0',
     'd981100cdefce3b7534ce08c599b0706e5b2a231',
     9552,
     'consolidated-common-repair'),
 7: ('3efb043df2749e965a70ae815003952d0f7e3c1d203d4e04e04e24fd0892a20c',
     '4d2aafcd49f2b088cb4afebdb67846cece5f922b',
     6124,
     'consolidated-common-repair'),
 8: ('5c9fcd3012d9c41bc951cf78e2ccc29591ab8151a0037e6cd0ff07cabb0e54f4',
     'bd414fc2b16dcd53116d3ed772e27b3c792237c2',
     6384,
     'consolidated-common-repair'),
 9: ('36bf84b786280660b3ec4a5e3a110f04d98598cdbe49e7680a438de344a0dd06',
     'f43d9ffc34ad19eb1e4d14cb1a176a916d408a36',
     7718,
     'consolidated-common-repair'),
 10: ('1fa9f620cbab16c728d931520d777e8ef25090c52520dca39144ed43e2790459',
      'cbf93e2e9912045c58946dc8a936e54c2dff5b95',
      5847,
      'consolidated-common-repair'),
 11: ('673111801ec83a2118743de3cd851f7a3db8e6c9580750f3fe766a9626b0f498',
      '8cfcd82cce15b5df64f964f81b2424c97fc1bb7c',
      9541,
      'consolidated-information-and-inquiry'),
 12: ('bd5e18cb3616a7ead45cc407da8ebe72274358edcd12459f4109ad155e2f53b2',
      'dd8f4908d7a733aa8f08481da568318d458fc584',
      4770,
      'consolidated-information-and-inquiry'),
 13: ('50cf2306b486db59fd7a2ecf77d07b3b54c3e486745f0b7308cb091de1c3ec61',
      '1f0bf3a48055fed1aa24dcfbba617d855d9c3c2e',
      15300,
      'consolidated-information-and-inquiry'),
 14: ('1f97b7f6e879f4ebe42b26620aac0c75095345f4ec65bfe2979ecd32aa538dbf',
      '952acfcb7a6f7e52731ff3b26c85dd5362a0e4f1',
      4995,
      'consolidated-information-and-inquiry'),
 15: ('e6be2257c2dabfd15057f1c59603518d1ba20976068579bd31512ec1f5bfafce',
      '00dcece21824577e981a8dd1c103056fea60e0a0',
      5605,
      'consolidated-information-and-inquiry'),
 16: ('ad4909aa4015f759a7494c5a0b5ddfa0c4ccaaf6d14ad7c89386db53e01385d6',
      '4a91c34083b0df5658a437fdf86a471471524b30',
      5551,
      'consolidated-information-and-inquiry'),
 17: ('63494364aeb423cecee01e1b347a4dfed7e2c4b544c90d456465520378810d40',
      '1cc325aad1ee71001f5f4c7eb2881211d78a56df',
      7100,
      'consolidated-information-and-inquiry'),
 18: ('18c1e07537712caaadf60d6bf8f25272aaf8c1767722bd56b3b5f1ed7258ee73',
      '38e462ee8c12a50cce8fd6bccf5ca3dde2597458',
      10150,
      'consolidated-information-and-inquiry'),
 19: ('71899f46c0346c901fd19697436beaa511b9814f879835604bbe23264d062aeb',
      '75476c99f17cf81258a6066bd12e2802c9f32f99',
      5518,
      'consolidated-information-and-inquiry'),
 20: ('51c98ce4cbc011f1e4d4d2af7fa9a34319f53713b876977bc9b16c74f0e258dc',
      '772e3d5300525c24c56da93fd2574ce4d4a1e1a0',
      3154,
      'consolidated-information-and-inquiry'),
 21: ('890c6bc8949f630878e9d3de6bed22c7070d0b4f0d7c43d7fa96f4c7a6d91607',
      'd2f19e3562852bbb3fc0d849e421921949fddacb',
      10678,
      'consolidated-information-and-inquiry'),
 22: ('71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e',
      '75bb17ddd69e37db6530357307078d056b97ec16',
      16844,
      'consolidated-common-repair'),
 23: ('45ffbb9679d23bd16a43b4930ec615bb55f4c0c56705e5a0c90f0fec425a2a3e',
      '02390e5f62fc4f5ab97263fa548b56f412c17ce3',
      9045,
      'consolidated-common-repair'),
 24: ('21f9e48328bfbf843b5f0371168f84c51768dec6260b3798fca4a461900aa006',
      'b5f6e9140796030880f6dbc723514bfb393d23c2',
      18202,
      'consolidated-objective-normativity')}
    NOTES = {
        'continuation-note-27': ('71899f46c0346c901fd19697436beaa511b9814f879835604bbe23264d062aeb', '75476c99f17cf81258a6066bd12e2802c9f32f99', 5518, 'continuation-common-observation',
            'consolidated-information-and-inquiry', 'mathematics/information-and-inquiry.md',
            'a-common-lower-reference-and-compatible-eventual-targets', ('continuation-note-1',)),
        'continuation-note-48': ('21f9e48328bfbf843b5f0371168f84c51768dec6260b3798fca4a461900aa006', 'b5f6e9140796030880f6dbc723514bfb393d23c2', 18202, 'continuation-source-bridge',
            'consolidated-objective-normativity', 'foundations/objective-normativity-and-corrective-cognition.md',
            '73-transporting-a-correction-scale-through-time',
            ('continuation-note-40', 'continuation-note-39', 'continuation-note-35')),
    }
    ALIASES = {
        19: ('continuation-note-27', 'continuation-common-observation', 'research-note',
             ('continuation-note-1',), ()),
        22: ('continuation-note-40', None, None, None,
             ('continuation-anchor-repair', 'continuation-dependency-quadratic',
              'continuation-local-approximate', 'continuation-local-rigidity',
              'continuation-nudge', 'continuation-smooth-blocks',
              'continuation-smooth-rigidity', 'continuation-source-bridge')),
        24: ('continuation-note-48', 'continuation-source-bridge', 'synthesis',
             ('continuation-note-40', 'continuation-note-39', 'continuation-note-35'), ()),
    }

    @classmethod
    def setUpClass(cls):
        import os
        import check_reader_pilot
        import resolve_t20_v6_source
        import validate_v5_successors
        cls.reader, cls.resolver, cls.successors = check_reader_pilot, resolve_t20_v6_source, validate_v5_successors
        cls.env = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_ALLOW_PROTOCOL='',
                       GIT_TERMINAL_PROMPT='0', GIT_OPTIONAL_LOCKS='0',
                       GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
                       GIT_CONFIG_NOSYSTEM='1')
        common = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT,
                                env=cls.env, capture_output=True, check=True).stdout.decode().strip()
        cls.object_store = (ROOT / common / 'objects').resolve()
        cls.original_owners = json.loads((ROOT / cls.OWNER).read_bytes())
        # Keep this original fifty-source campaign independent of later cohorts.
        # The literal published owner coordinate and digest are external evidence.
        coordinate = subprocess.run(['git', 'ls-tree', '-z',
            '254a48e595ae9b2966f4d4fa406b908a05150452', '--', cls.OWNER], cwd=ROOT,
            env=cls.env, capture_output=True, check=True).stdout
        expected = ('100644 blob 3e51e9d8c931493b4b1d8dd36248df5fbc7835b6\t' + cls.OWNER + '\0').encode()
        if coordinate != expected:
            raise AssertionError('original fifty owner coordinate differs')
        historical_body = subprocess.run(['git', 'cat-file', 'blob',
            '3e51e9d8c931493b4b1d8dd36248df5fbc7835b6'], cwd=ROOT,
            env=cls.env, capture_output=True, check=True).stdout
        if hashlib.sha256(historical_body).hexdigest() != 'bffb81e2ac979d3fb3fde4a8285910389cd497609d17bd5fdb276b38277dc2eb':
            raise AssertionError('original fifty owner bytes differ')
        history = json.loads(historical_body)['historical_source_bindings']
        paths = {row['path'] for row in history}
        current = [row for row in cls.original_owners['historical_source_bindings'] if row['path'] in paths]
        if len(history) != 50 or current != history:
            raise AssertionError('original fifty historical declarations changed')
        cls.original_owners['historical_source_bindings'] = history
        cls.original_cross = json.loads((ROOT / cls.CROSS).read_bytes())
        cls.paths = {n: 'docs/provenance/v5-research-continuations/notes/' + r[0] + '.md'
                     for n, r in cls.ROWS.items()}
        cls.current = {r['path']: (ROOT / r['path']).read_bytes()
                       for r in cls.original_owners['source_additions']}
        cls.guides = (cls.resolver.MEDIATOR_GUIDE, *cls.resolver.TYPED_GUIDES)
        cls.current.update({p: (ROOT / p).read_bytes() for p in cls.guides})
        cls.original_manifest = json.loads((ROOT / cls.MANIFEST).read_bytes())

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('-c', 'init.templateDir=', 'init', '-q')
        (self.root / '.git/objects/info/alternates').write_text(str(self.object_store) + '\n')
        self.owners = deepcopy(self.original_owners)
        self.cross = deepcopy(self.original_cross)
        self.manifest = deepcopy(self.original_manifest)
        for path, body in self.current.items():
            self.put(path, body)
        self.save()
        self.git('add', '--', *self.current, self.OWNER, self.CROSS, self.MANIFEST)

    def git(self, *args, check=True):
        return subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                              cwd=self.root, env=self.env, check=check, capture_output=True)

    def put(self, path, body):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        target.chmod(0o644)

    def save(self):
        for path, value in ((self.OWNER, self.owners), (self.CROSS, self.cross), (self.MANIFEST, self.manifest)):
            self.put(path, (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode())

    def context(self):
        gate = getattr(self.resolver, 'require_next24_note_context', None)
        self.assertTrue(callable(gate), 'finite next24 historical context is not implemented')
        return gate(self.root)

    def original(self, n):
        row = self.ROWS[n]
        body = self.git('cat-file', 'blob', row[1]).stdout
        self.assertEqual((hashlib.sha256(body).hexdigest(), len(body)), (row[0], row[2]))
        return body

    def resolve(self, n):
        return self.resolver.historical_source_bytes(self.root, self.paths[n], self.REV, self.ROWS[n][1])

    def test_fifty_originals_require_exact_accepted_science(self):
        rows = self.owners['historical_source_bindings']
        self.assertEqual(len(rows), 50)
        baseline = {}
        for row in rows:
            entry = self.git('ls-tree', '-z', row['repository_revision'], '--', row['path']).stdout
            meta, name = entry.rstrip(b'\0').split(b'\t')
            mode, kind, blob = meta.decode().split()
            self.assertEqual(name.decode(), row['path'])
            size = int(self.git('cat-file', '-s', blob).stdout)
            baseline[row['path']] = dict(mode=mode, kind=kind, git_oid=blob, bytes=size)
        before = (self.root / '.git/index').read_bytes()
        additions = {r['path']: r for r in self.owners['source_additions']}
        received, errors = self.reader.check_historical_sources(self.root, baseline, self.owners, self.cross, additions)
        self.assertEqual(errors, [])
        self.assertEqual(set(received), {r['path'] for r in rows})
        self.assertEqual((self.root / '.git/index').read_bytes(), before)
        self.assertTrue(all(not (self.root / r['path']).exists() for r in rows))

    def test_exact_public_originals_are_received_without_recreation(self):
        self.context()
        before = (self.root / '.git/index').read_bytes()
        for n in self.ROWS:
            with self.subTest(source=n):
                body = self.original(n)
                self.assertEqual(self.resolve(n), body)
                self.assertFalse((self.root / self.paths[n]).exists())
                self.put(self.paths[n], body)
                self.assertEqual(self.resolve(n), body)
        self.assertEqual((self.root / '.git/index').read_bytes(), before)

    def test_earlier_twenty_six_context_is_still_a_complete_accepted_population(self):
        self.owners['historical_source_bindings'] = [
            row for row in self.owners['historical_source_bindings']
            if row['path'] not in set(self.paths.values())]
        self.assertEqual(len(self.owners['historical_source_bindings']), 26)
        self.save()
        self.resolver.require_t4_note_context(self.root)
        self.resolver.require_continuation_note_context(self.root)

    def test_partial_extra_duplicate_and_unknown_declarations_reject_before_git(self):
        from unittest.mock import patch
        self.context()
        original = deepcopy(self.owners)
        for fault in ('partial49', 'extra51', 'duplicate51', 'unknown-substitution'):
            with self.subTest(fault=fault):
                self.owners = deepcopy(original)
                rows = self.owners['historical_source_bindings']
                if fault == 'partial49': rows.pop()
                elif fault == 'duplicate51': rows.append(deepcopy(rows[-1]))
                elif fault == 'extra51': rows.append(dict(rows[-1], path='unqualified-public-original.md'))
                else: rows[-1]['path'] = 'unqualified-public-original.md'
                self.save()
                with patch.object(self.reader.subprocess, 'run', side_effect=AssertionError('Git before finite gate')):
                    received, errors = self.reader.check_historical_sources(self.root, {}, self.owners, self.cross, {})
                self.assertEqual(received, {})
                self.assertTrue(any('expected exactly' in e for e in errors), errors)
                with self.assertRaises(ValueError): self.context()

    def test_both_manifested_originals_bind_revision_blob_and_source_identity(self):
        self.context()
        for n in (9, 22):
            with self.subTest(source=n):
                row = next(r for r in self.manifest['objects'] if r.get('repository_path') == self.paths[n])
                self.assertEqual(self.resolver.source_bytes(self.root, row), self.original(n))
                for field, bad in (('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                                   ('source_sha256', '0' * 64), ('source_bytes', 0),
                                   ('public_sha256', '0' * 64), ('public_bytes', 0),
                                   ('disposition', 'ADD_EXACT')):
                    with self.subTest(field=field), self.assertRaises(ValueError):
                        self.resolver.source_bytes(self.root, dict(row, **{field: bad}))
        ordinary = dict(next(r for r in self.manifest['objects'] if r.get('repository_path') == self.paths[9]),
                        repository_path=self.paths[1], source_sha256=self.ROWS[1][0], source_bytes=self.ROWS[1][2],
                        public_sha256=self.ROWS[1][0], public_bytes=self.ROWS[1][2], git_blob=self.ROWS[1][1])
        with self.assertRaises(ValueError): self.resolver.source_bytes(self.root, ordinary)

    def test_three_alias_roles_and_twenty_one_history_only_roles_remain_exact(self):
        self.context()
        own0, cross0 = deepcopy(self.owners), deepcopy(self.cross)
        for n, (key, work, role, supports, users) in self.ALIASES.items():
            for fault in ('relation', 'role', 'support', 'identity', 'journey'):
                with self.subTest(source=n, fault=fault):
                    self.owners, self.cross = deepcopy(own0), deepcopy(cross0)
                    if fault == 'identity': self.cross['sources'][key]['sha256'] = '0' * 64
                    elif fault == 'relation': next(r for r in self.cross['relations'] if r.get('from') == key)['to'] = 'consolidated-encodings-and-witnesses'
                    elif fault == 'journey': self.cross['reader_journeys'][0]['source_keys'].append(key)
                    elif work:
                        item = next(w for w in self.cross['works'] if w['key'] == work)
                        if fault == 'role': item['role'] = 'component'
                        else: item['supporting_source_keys'] = []
                    else:
                        item = next(w for w in self.cross['works'] if w['key'] == users[0])
                        if fault == 'role': item['reading_forms'].append({'source': key, 'relationship': 'historical-source'})
                        else: item['supporting_source_keys'].remove(key)
                    self.save()
                    with self.assertRaises(ValueError): self.context()
        self.owners, self.cross = deepcopy(own0), deepcopy(cross0)
        self.cross['sources']['invented-reading-alias'] = dict(path=self.paths[1], sha256=self.ROWS[1][0], read_scope='unreviewed')
        self.save()
        with self.assertRaises(ValueError): self.context()

    def test_wrong_owner_coordinates_and_current_science_reject(self):
        self.context()
        original = deepcopy(self.owners)
        for n in self.ROWS:
            for field, value in (('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                                 ('role', 'work-source'), ('reading_source', 'consolidated-encodings-and-witnesses'),
                                 ('basis', 'unreviewed')):
                with self.subTest(source=n, field=field):
                    self.owners = deepcopy(original)
                    next(r for r in self.owners['historical_source_bindings'] if r['path'] == self.paths[n])[field] = value
                    self.save()
                    with self.assertRaises(ValueError): self.context()
        self.owners = deepcopy(original)
        self.save()
        for path in ('mathematics/common-repair-and-geometric-obstructions.md',
                     'mathematics/information-and-inquiry.md',
                     'foundations/objective-normativity-and-corrective-cognition.md', self.REVIEW):
            with self.subTest(current=path):
                old = (self.root / path).read_bytes()
                self.put(path, old + b'changed')
                with self.assertRaises(ValueError): self.context()
                self.put(path, old)

    def test_present_corruption_modes_symlinks_and_staged_conflicts_cannot_fall_back(self):
        self.context()
        for n in (1, 9, 19, 22, 24):
            path, body = self.paths[n], self.original(n)
            target = self.root / path
            with self.subTest(source=n):
                self.put(path, body + b'changed')
                with self.assertRaises(ValueError): self.resolve(n)
                self.put(path, body)
                target.chmod(0o755)
                with self.assertRaises(ValueError): self.resolve(n)
                target.unlink()
                target.symlink_to('absent-target')
                with self.assertRaises(ValueError): self.resolve(n)
                target.unlink()
                self.git('update-index', '--add', '--cacheinfo', '100755,' + self.ROWS[n][1] + ',' + path)
                with self.assertRaises(ValueError): self.resolve(n)
                self.git('update-index', '--force-remove', '--', path)
                conflict = ('100644 ' + self.ROWS[n][1] + ' 1\t' + path + '\n').encode()
                subprocess.run(['git', 'update-index', '--index-info'], input=conflict, cwd=self.root,
                               env=self.env, capture_output=True, check=True)
                with self.assertRaises(ValueError): self.resolve(n)
                self.git('update-index', '--force-remove', '--', path)

    def test_complete_public_coordinate_groups_admit_two_seven_or_nine_only(self):
        base = deepcopy(self.manifest)
        next_paths = {self.paths[n] for n in (9, 22)}
        seven_paths = set(self.resolver.PUBLIC_READER_NOTE_PATHS) | {
            'experiments/orthemology-v5-continuations/registry.json'}
        self.assertEqual((len(next_paths), len(seven_paths), len(next_paths & seven_paths)), (2, 7, 0))
        pinned = {row['repository_path']: deepcopy(row) for row in base['objects']
                  if row.get('repository_path') in next_paths | seven_paths}
        self.assertEqual(len(pinned), 9)
        for row in base['objects']:
            if row.get('repository_path') in pinned:
                row.pop('repository_revision', None)
                row.pop('git_blob', None)
        def candidate(paths):
            value = deepcopy(base)
            for row in value['objects']:
                path = row.get('repository_path')
                if path in paths:
                    row.update(repository_revision=pinned[path]['repository_revision'],
                               git_blob=pinned[path]['git_blob'])
            return value
        gate = self.reader._permitted_projection_consumer_pins
        for paths in (next_paths, seven_paths, next_paths | seven_paths):
            with self.subTest(complete=len(paths)):
                self.assertTrue(gate(base, candidate(paths)))
        for paths in (set(), {self.paths[9]}, seven_paths - {next(iter(seven_paths))},
                      seven_paths | {self.paths[9]}):
            with self.subTest(partial=len(paths)):
                self.assertFalse(gate(base, candidate(paths)))
        wrong = candidate(next_paths | seven_paths)
        selected = next(r for r in wrong['objects'] if r.get('repository_path') == self.paths[22])
        selected['git_blob'] = '0' * 40
        self.assertFalse(gate(base, wrong))
        wrong = candidate(next_paths | seven_paths)
        wrong['objects'][0]['publication_basis'] = 'unrelated edit'
        self.assertFalse(gate(base, wrong))

    def test_earlier_twenty_six_references_authenticate_history_before_existence(self):
        from unittest.mock import patch
        import validate_internal_references as references
        earlier = [r for r in self.owners['historical_source_bindings']
                   if r['path'] not in set(self.paths.values())]
        self.assertEqual(len(earlier), 26)
        self.context()
        with patch.object(references, 'ROOT', str(self.root)):
            for row in earlier:
                path = row['path']
                body = self.git('cat-file', 'blob', row['git_blob']).stdout
                citations = ((self.REVIEW, '../' + path),
                    ('docs/provenance/v5-successors/PRESERVATION.json', path))
                for source, cited in citations:
                    with self.subTest(path=path, citation=cited, state='absent'):
                        self.assertTrue(references._resolves(source, cited))
                self.put(path, body + b'changed original')
                for source, cited in citations:
                    with self.subTest(path=path, citation=cited, state='present-corrupt'):
                        self.assertFalse(references._resolves(source, cited))
                (self.root / path).unlink()

    def test_historical_metadata_references_require_exact_originals(self):
        from unittest.mock import patch
        import validate_internal_references as references
        self.context()
        with patch.object(references, 'ROOT', str(self.root)):
            for n in self.ROWS:
                with self.subTest(source=n):
                    self.assertTrue(references._resolves(
                        'docs/provenance/v5-successors/PRESERVATION.json', self.paths[n]))
            self.assertFalse(references._resolves(
                'docs/provenance/v5-successors/PRESERVATION.json',
                '/'.join(('docs', 'provenance', 'v5-research-continuations', 'notes', 'unqualified.md'))))
            path = self.paths[22]
            self.put(path, self.original(22) + b'changed')
            self.assertFalse(references._resolves(self.MANIFEST, path))

    def test_preservation_recovers_all_bound_historical_continuation_originals(self):
        self.context()
        files = {}
        for row in self.owners['historical_source_bindings']:
            path = row['path']
            if not any(path.startswith(p + '/') for p in self.successors.FROZEN_ROOTS):
                continue
            body = self.git('cat-file', 'blob', row['git_blob']).stdout
            files[path] = dict(path=path, bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                               git_blob_sha1=row['git_blob'])
        self.assertEqual(len(files), 38)
        anchor = dict(self.successors.BASELINE_ANCHOR, git_required=False)
        inventory = dict(schema='orthemology-v5-preservation-v1', base_commit=anchor['base_commit'],
                         base_tree=anchor['base_tree'], roots=self.successors.FROZEN_ROOTS, files=list(files.values()))
        # The fixture has the 38 real originals in the frozen continuation roots and two legacy anchors.
        # It deliberately uses the public explicit-fixture anchor; production four-owner
        # authentication is qualified separately and is not bypassed by this seam.
        for field in ('legacy_registry', 'legacy_overlay'):
            name = anchor[field]['path']
            body = b'bounded public fixture anchor\n'
            self.put(name, body)
            row = dict(path=name, bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                       git_blob_sha1=hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest())
            files[name] = row
            inventory['files'].append(row)
            anchor[field] = dict(path=name, sha256=row['sha256'])
        bundle = dict(baseline_binding=dict(schema='orthemology-v5-baseline-binding-v1', **{k:v for k,v in anchor.items() if k != 'git_required'}),
                      preservation=inventory,
                      registry=dict(records={'PRESERVATION': {'sha256': anchor['preservation_sha256']}},
                                    baseline_commit=anchor['base_commit'], baseline_tree=anchor['base_tree']))
        self.assertEqual(set(self.successors._preservation(bundle, self.root, anchor)), set(files))
        wrong = deepcopy(bundle)
        wrong['preservation']['files'][0]['sha256'] = '0' * 64
        with self.assertRaises(ValueError): self.successors._preservation(wrong, self.root, anchor)
        unknown = deepcopy(bundle)
        unknown['preservation']['files'][0]['path'] = '/'.join(('docs', 'provenance', 'v5-research-continuations', 'notes', 'unqualified.md'))
        with self.assertRaises(ValueError): self.successors._preservation(unknown, self.root, anchor)


    def test_source_relative_historical_references_authenticate_before_existence(self):
        from unittest.mock import patch
        import validate_internal_references as references
        self.context()
        with patch.object(references, 'ROOT', self.root):
            for n in self.ROWS:
                path = self.paths[n]
                citations = (
                    (self.REVIEW, '../' + path),
                    ('docs/provenance/v5-research-continuations/README.md',
                     'notes/' + path.rsplit('/', 1)[1]),
                )
                for source, cited in citations:
                    with self.subTest(source=n, citation=cited, state='absent'):
                        self.assertTrue(references._resolves(source, cited))
                self.put(path, self.original(n) + b'changed')
                for source, cited in citations:
                    with self.subTest(source=n, citation=cited, state='present-corrupt'):
                        self.assertFalse(references._resolves(source, cited))
                (self.root / path).unlink()
            self.assertFalse(references._resolves(self.REVIEW,
                '../docs/provenance/v5-research-continuations/notes/unqualified-relative.md'))




class FixtureConsumerProjectionPinTests(unittest.TestCase):
    """Current fixture readers keep their exact original public evidence."""
    FIXTURE_PATHS = ('experiments/episode-reification-v2/README.md',
     'experiments/episode-reification-v2/analysis/analyze_er2.py',
     'experiments/episode-reification-v2/harness/run_er.py',
     'experiments/episode-reification-v2/scripts/generate_cases.py',
     'experiments/episode-reification-v2/tests/test_smoke.py',
     'experiments/episode-reification/README.md',
     'experiments/episode-reification/scripts/generate_fixtures.py',
     'experiments/episode-reification/tests/test_smoke.py',
     'experiments/experiment-status.yaml',
     'scripts/generate_current_state.py',
     'scripts/validate_experiment_readiness.py',
     'scripts/validate_negative_fixtures.py',
     'tests/schema-negative/NEGATIVE-FIXTURES.json')

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('fixture_pin_reader', MODULE)
        cls.reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.reader)
        cls.pins = BulkConsumerProjectionPinTests.BASE_COORDINATE_PINS
        if len(cls.pins) != 22 or len(cls.FIXTURE_PATHS) != 13:
            raise AssertionError('complete independently admitted coordinate population required')
        document = json.loads((ROOT / 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json').read_text())
        selected = [deepcopy(row) for row in document['objects'] if row.get('repository_path') in cls.pins]
        if len(selected) != 22:
            raise AssertionError('original coordinate population missing or repeated')
        unrelated = next(deepcopy(row) for row in document['objects'] if row.get('repository_path') not in cls.pins)
        # This bounded fixture keeps complete real rows and one unrelated row.
        # The separate full-manifest test retains its 28,478-identity assertion.
        cls.base = dict(document, objects=selected + [unrelated])
        for row in selected:
            row.pop('repository_revision', None)
            row.pop('git_blob', None)

    def candidate(self, paths):
        value = deepcopy(self.base)
        for row in value['objects']:
            path = row.get('repository_path')
            if path in paths:
                identity, size, blob, revision = self.pins[path]
                self.assertEqual((row['source_sha256'], row['source_bytes'], row['public_sha256'], row['public_bytes']),
                                 (identity, size, identity, size))
                row.update(repository_revision=revision, git_blob=blob)
        return value

    def test_complete_current_extension_and_previous_nine_admit(self):
        gate = self.reader._permitted_projection_consumer_pins
        older = set(self.pins) - set(self.FIXTURE_PATHS)
        self.assertEqual(len(older), 9)
        self.assertTrue(gate(self.base, self.candidate(older)))
        self.assertTrue(gate(self.base, self.candidate(set(self.pins))))

    def test_partial_fixture_groups_and_unjoined_extension_reject(self):
        gate = self.reader._permitted_projection_consumer_pins
        self.assertFalse(gate(self.base, self.candidate(set(self.FIXTURE_PATHS))))
        for path in self.FIXTURE_PATHS:
            with self.subTest(missing=path):
                self.assertFalse(gate(self.base, self.candidate(set(self.pins) - {path})))

    def test_each_identity_field_role_and_unrelated_drift_reject(self):
        gate = self.reader._permitted_projection_consumer_pins
        changes = [('git_blob', '0' * 40), ('repository_revision', '0' * 40),
                   ('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                   ('source_bytes', -1), ('public_bytes', -1),
                   ('disposition', 'PROJECT'), ('publication_basis', 'unqualified change'),
                   ('repository_path', '/'.join(('scripts', 'unadmitted-fixture-owner.py')))]
        for path in self.FIXTURE_PATHS:
            for key, value in changes:
                with self.subTest(path=path, field=key):
                    candidate = self.candidate(set(self.pins))
                    row = next(row for row in candidate['objects'] if row.get('repository_path') == path)
                    row[key] = value
                    self.assertFalse(gate(self.base, candidate))
        candidate = self.candidate(set(self.pins))
        candidate['objects'][-1]['publication_basis'] = 'unrelated drift'
        self.assertFalse(gate(self.base, candidate))
        candidate = self.candidate(set(self.pins))
        candidate['objects'].append(deepcopy(candidate['objects'][0]))
        self.assertFalse(gate(self.base, candidate))

    def test_original_public_rows_resolve_as_inert_exact_native_bytes(self):
        import validate_t20_v6_projection as projection
        import resolve_t20_v6_source as resolver
        candidate = self.candidate(set(self.pins))
        for row in candidate['objects']:
            if row.get('repository_path') in self.FIXTURE_PATHS:
                with self.subTest(path=row['repository_path']):
                    body = resolver.source_bytes(ROOT, row)
                    self.assertEqual((hashlib.sha256(body).hexdigest(), len(body)),
                                     (row['source_sha256'], row['source_bytes']))
                    self.assertEqual(projection.check_object(ROOT, row), [])



class FixtureConsumerEditionTests(unittest.TestCase):
    """An old public view never hides corrupt or mixed current consumers."""
    STATUS = 'experiments/experiment-status.yaml'

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('fixture_edition_reader', MODULE)
        cls.reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.reader)
        cls.paths = FixtureConsumerProjectionPinTests.FIXTURE_PATHS
        cls.original = {path: subprocess.check_output(
            ['git', 'show', '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c:' + path], cwd=ROOT)
            for path in cls.paths}
        cls.current = {path: (ROOT / path).read_bytes() for path in cls.paths}
        cls.objects = subprocess.check_output(
            ['git', 'rev-parse', '--path-format=absolute', '--git-path', 'objects'], cwd=ROOT).decode().strip()

    def fixture(self, current=True, baseline=False):
        directory = tempfile.TemporaryDirectory(prefix='fixture-consumer-edition-')
        self.addCleanup(directory.cleanup)
        repo = Path(directory.name)
        subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
        (repo / '.git/objects/info/alternates').write_text(self.objects + '\n')
        for path, body in self.original.items():
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        subprocess.run(['git', 'add', '--', *self.paths], cwd=repo, check=True)
        revision = None
        if baseline:
            subprocess.run(['git', '-c', 'user.name=Fixture test', '-c',
                            'user.email=fixture-test@example.invalid', 'commit', '-qm',
                            'Original public fixture consumers'], cwd=repo, check=True)
            revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode().strip()
        if current:
            for path, body in self.current.items():
                (repo / path).write_bytes(body)
            subprocess.run(['git', 'add', '--', *self.paths], cwd=repo, check=True)
        return repo, revision

    def edition(self, repo):
        gate = getattr(self.reader, 'check_fixture_consumer_edition', None)
        self.assertTrue(callable(gate), 'the original public view needs an authenticated current edition')
        index = (repo / '.git/index').read_bytes()
        result = gate(repo)
        self.assertEqual((repo / '.git/index').read_bytes(), index)
        return result

    def test_complete_original_and_current_editions_keep_original_status(self):
        original, _ = self.fixture(current=False)
        self.assertEqual(self.edition(original), ({}, None, []))
        current, _ = self.fixture()
        owners, status, errors = self.edition(current)
        self.assertEqual(errors, [])
        self.assertEqual(set(owners), set(self.paths))
        self.assertEqual(status, self.original[self.STATUS])
        self.assertNotEqual(status, self.current[self.STATUS])

    def test_each_current_body_and_a_mixed_edition_are_rejected(self):
        repo, _ = self.fixture()
        for path in self.paths:
            with self.subTest(path=path):
                target = repo / path
                target.write_bytes(self.current[path] + b'\ncorrupt fixture successor\n')
                owners, status, errors = self.edition(repo)
                self.assertEqual((owners, status), ({}, None))
                self.assertTrue(errors)
                target.write_bytes(self.current[path])
        target = repo / self.paths[0]
        target.write_bytes(self.original[self.paths[0]])
        subprocess.run(['git', 'add', '--', self.paths[0]], cwd=repo, check=True)
        self.assertTrue(self.edition(repo)[2])

    def test_staged_body_mode_symlink_and_absence_cannot_hide_behind_history(self):
        for fault in ('staged', 'mode', 'symlink', 'missing'):
            with self.subTest(fault=fault):
                repo, _ = self.fixture()
                path = self.paths[0]
                target = repo / path
                if fault == 'staged':
                    target.write_bytes(self.current[path] + b'\nwrong staged body\n')
                    subprocess.run(['git', 'add', '--', path], cwd=repo, check=True)
                    target.write_bytes(self.current[path])
                elif fault == 'mode':
                    target.chmod(0o755)
                elif fault == 'symlink':
                    target.unlink()
                    target.symlink_to(repo / self.paths[1])
                else:
                    target.unlink()
                owners, status, errors = self.edition(repo)
                self.assertEqual((owners, status), ({}, None))
                self.assertTrue(errors)

    def test_real_census_comparison_requires_the_complete_qualified_edition(self):
        repo, baseline = self.fixture(baseline=True)
        owners, status, errors = self.edition(repo)
        self.assertEqual(errors, [])
        self.assertEqual(status, self.original[self.STATUS])
        before = self.reader.check_corpus_currentness(repo, baseline)
        self.assertEqual(len(before), 13)
        self.assertEqual(self.reader.check_corpus_currentness(
            repo, baseline, fixture_owners=owners), [])


class ConsolidatedSuccessorInputTests(unittest.TestCase):
    """Exact public original inputs remain live through one existing registry."""
    REGISTRY = 'experiments/orthemology-v5-successors/registry.json'

    @classmethod
    def setUpClass(cls):
        import os
        import resolve_t20_v6_source as source
        import validate_v5_successors as successors
        import replay_v5_successors as replay
        import validate_t20_v6_projection as projection
        import validate_internal_references as references
        import check_reader_pilot as reader
        cls.os, cls.source, cls.successors, cls.replay = os, source, successors, replay
        cls.projection, cls.references, cls.reader = projection, references, reader
        cls.compact = (ROOT / cls.REGISTRY).read_bytes()
        document = json.loads(cls.compact)
        cls.originals = {path: value.encode() for path, value in document.pop('preserved_source_inputs').items()}
        document['records']['CALCULUS_MAP'] = {'path': 'docs/provenance/v5-successors/CALCULUS_MAP.json',
            'sha256': 'd0644ef40458d17ac19710e4d1ecdc2cc974a54d73b4053641979f9ce1f74759'}
        cls.original_registry = (json.dumps(document, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
        if set(cls.originals) != source.SUCCESSOR_INPUT_PATHS or len(cls.originals) != 19:
            raise ValueError('the current registry requires all nineteen original inputs')
        source_map = json.loads((ROOT / 'docs/provenance/v5-successors/SOURCE_MAP.json').read_bytes())
        cls.rows = [row for row in source_map['sources'] if row.get('public_path') in cls.originals]
        allowlist = json.loads((ROOT / 'docs/provenance/v5-successors/PUBLIC_PROJECTION.json').read_bytes())['allowlist']
        cls.allowlist = [row for row in allowlist if row['path'] in cls.originals]
        cls.manifest = json.loads((ROOT / 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json').read_bytes())
        cls.public = [row for row in cls.manifest['objects'] if row.get('repository_path') in cls.originals]
        cross = json.loads((ROOT / 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json').read_bytes())
        cls.aliases = {key: row for key, row in cross['sources'].items() if row['path'] in cls.originals}
        if (len(cls.rows), len(cls.allowlist), len(cls.public), len(cls.aliases)) != (29, 19, 3, 2):
            raise ValueError('original source/allowlist/public/reader incidences differ')
        cls.objects = subprocess.check_output(['/usr/bin/git', '--no-replace-objects', 'rev-parse',
            '--path-format=absolute', '--git-path', 'objects'], cwd=ROOT).decode().strip()

    def git(self, *args, data=None):
        env = {k: v for k, v in self.os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='',
                   GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=self.os.devnull,
                   GIT_CONFIG_SYSTEM=self.os.devnull, GIT_TERMINAL_PROMPT='0',
                   GIT_AUTHOR_NAME='Fixture test', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                   GIT_COMMITTER_NAME='Fixture test', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        return subprocess.check_output(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args],
                                       cwd=self.repo, env=env, input=data)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='consolidated-inputs-')
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.git('-c', 'init.templateDir=', 'init', '-q')
        (self.repo / '.git/objects/info/alternates').write_text(self.objects + '\n')
        for name, body in {**self.originals, self.REGISTRY: self.original_registry}.items():
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            target.chmod(0o644)
        self.git('add', '--', self.REGISTRY, *self.originals)
        self.git('commit', '-qm', 'Original public input records and registry')
        self.baseline = self.git('rev-parse', 'HEAD').decode().strip()
        (self.repo / self.REGISTRY).write_bytes(self.compact)
        self.git('add', '--', self.REGISTRY)
        self.index = self.repo / '.git/index'
        self.saved_index = self.index.read_bytes()
        self.sample = sorted(self.originals)[0]

    def original_bytes(self, path):
        before = self.index.read_bytes()
        try:
            return self.source.successor_input_bytes(self.repo, path)
        finally:
            self.assertEqual(self.index.read_bytes(), before)

    def remove_originals(self):
        for path in self.originals:
            (self.repo / path).unlink()

    def test_original_and_compact_editions_preserve_original_bytes(self):
        registry = self.repo / self.REGISTRY
        registry.write_bytes(self.original_registry)
        self.git('add', '--', self.REGISTRY)
        self.assertEqual(self.original_bytes(self.sample), self.originals[self.sample])
        (self.repo / self.sample).unlink()
        with self.assertRaises((ValueError, OSError)):
            self.original_bytes(self.sample)
        (self.repo / self.sample).write_bytes(self.originals[self.sample])
        registry.write_bytes(self.compact)
        self.index.write_bytes(self.saved_index)
        for state in ('present', 'unstaged', 'staged'):
            if state == 'unstaged':
                self.remove_originals()
            elif state == 'staged':
                self.git('update-index', '--force-remove', '--', *self.originals)
            for path, body in self.originals.items():
                self.assertEqual(self.original_bytes(path), body)
            self.assertEqual(self.source.successor_input_absences(self.repo),
                             set() if state == 'present' else set(self.originals))

    def test_registry_inverse_and_distinct_original_statuses_remain_exact(self):
        self.assertEqual(self.source.successor_input_registry_original_bytes(self.repo), self.original_registry)
        reconstructed = json.loads(self.compact)
        del reconstructed['preserved_source_inputs']
        reconstructed['records']['CALCULUS_MAP'] = {'path': 'docs/provenance/v5-successors/CALCULUS_MAP.json',
            'sha256': 'd0644ef40458d17ac19710e4d1ecdc2cc974a54d73b4053641979f9ce1f74759'}
        self.assertEqual(reconstructed, json.loads(self.original_registry))
        pending = next(path for path in self.originals if path.endswith('/CANDIDATE_v1.json'))
        reviewed = next(path for path in self.originals if path.endswith('/VERIFICATION.json'))
        self.assertEqual(json.loads(self.original_bytes(pending))['status'], 'kernel-checked; independent review pending')
        self.assertEqual(json.loads(self.original_bytes(reviewed))['verdict'], 'ACCEPT bounded syntactic admissibility extension')

    def test_each_original_body_and_staged_concealment_are_rejected(self):
        for name, body in self.originals.items():
            with self.subTest(path=name):
                path = self.repo / name
                path.write_bytes(body + b'\nwrong\n')
                with self.assertRaises((ValueError, OSError)):
                    self.original_bytes(name)
                self.git('add', '--', name)
                path.write_bytes(body)
                with self.assertRaises((ValueError, OSError)):
                    self.original_bytes(name)
                path.unlink()
                with self.assertRaises((ValueError, OSError)):
                    self.original_bytes(name)
                self.index.write_bytes(self.saved_index)
                path.write_bytes(body)

    def test_registry_changed_mixed_missing_mode_and_link_states_fail(self):
        registry = self.repo / self.REGISTRY
        for fault in ('body', 'original-mixed', 'staged-wrong', 'missing', 'mode', 'symlink', 'hardlink'):
            with self.subTest(fault=fault):
                alias = self.repo / 'registry-copy'
                try:
                    if fault == 'body':
                        document = json.loads(self.compact)
                        document['preserved_source_inputs'][self.sample] += '\nwrong'
                        registry.write_text(json.dumps(document))
                    elif fault == 'original-mixed':
                        registry.write_bytes(self.original_registry)
                    elif fault == 'staged-wrong':
                        registry.write_bytes(self.compact + b'\nwrong')
                        self.git('add', '--', self.REGISTRY)
                        registry.write_bytes(self.compact)
                    elif fault == 'missing':
                        registry.unlink()
                    elif fault == 'mode':
                        registry.chmod(0o755)
                    elif fault == 'symlink':
                        alias.write_bytes(self.compact)
                        registry.unlink()
                        registry.symlink_to(alias)
                    else:
                        self.os.link(registry, alias)
                    with self.assertRaises((ValueError, OSError)):
                        self.original_bytes(self.sample)
                finally:
                    if registry.is_symlink():
                        registry.unlink()
                    if alias.exists():
                        alias.unlink()
                    registry.write_bytes(self.compact)
                    registry.chmod(0o644)
                    self.index.write_bytes(self.saved_index)

    def test_original_mode_conflict_stage_and_symlink_are_rejected(self):
        path = self.repo / self.sample
        oid = self.git('rev-parse', self.baseline + ':' + self.sample).decode().strip()
        self.git('update-index', '--cacheinfo', '100755,' + oid + ',' + self.sample)
        with self.assertRaises((ValueError, OSError)):
            self.original_bytes(self.sample)
        self.index.write_bytes(self.saved_index)
        self.git('update-index', '--force-remove', '--', self.sample)
        self.git('update-index', '-z', '--index-info', data=('100644 ' + oid + ' 2\t' + self.sample + '\0').encode())
        with self.assertRaises((ValueError, OSError)):
            self.original_bytes(self.sample)
        self.index.write_bytes(self.saved_index)
        path.unlink()
        path.symlink_to(self.repo / self.REGISTRY)
        with self.assertRaises((ValueError, OSError)):
            self.original_bytes(self.sample)

    def test_source_allowlist_and_public_rows_keep_all_original_roles(self):
        for original in self.rows:
            for field, value in (('id', 'unadmitted-id'), ('projection', 'DERIVED'), ('review_scope', 'new acceptance')):
                row = deepcopy(original)
                row[field] = value
                with self.assertRaises(ValueError):
                    self.source.successor_input_source_bytes(self.repo, row)
        for original in self.allowlist:
            for field, value in (('kind', 'AUTHORED'), ('source_ids', [])):
                row = deepcopy(original)
                row[field] = value
                with self.assertRaises(ValueError):
                    self.source.successor_input_allowlist_bytes(self.repo, row)
        for original in self.public:
            for field, value in (('role', 'new_proof'), ('disposition', 'ADD_EXACT'), ('public_sha256', '0' * 64)):
                row = deepcopy(original)
                row[field] = value
                self.assertTrue(self.projection.check_object(self.repo, row))

    def test_json_strictness_and_nonmember_boundaries_are_retained(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1e999}'):
            with self.assertRaises(ValueError):
                self.successors._input_json_bytes(raw)
        for path in ('experiments/episode-reification-v2/fixtures/KEYS.json', 'not-an-admitted-input.json'):
            with self.assertRaises(ValueError):
                self.source.successor_input_bytes(self.repo, path)

    def test_actual_sources_allowlist_and_replay_bytes_accept_absent_inputs(self):
        self.remove_originals()
        bundle = {'sources': self.rows, 'reviews': [], 'projection_reviews': []}
        sources, _, _ = self.successors._sources(bundle, self.repo)
        self.assertEqual(len(sources), 29)
        self.successors._allowlist({'public_allowlist': self.allowlist}, self.repo, sources)
        for row in self.rows:
            self.assertEqual(self.replay.public_bytes(self.repo, row), self.originals[row['public_path']])
        for row in self.public:
            self.assertEqual(self.projection.check_object(self.repo, row), [])

    def test_reader_currentness_discovery_and_two_aliases_keep_original_identity(self):
        self.remove_originals()
        self.assertEqual(self.reader.check_corpus_currentness(self.repo, self.baseline), [])
        self.git('update-index', '--force-remove', '--', *self.originals)
        self.assertEqual(self.reader.check_corpus_currentness(self.repo, self.baseline), [])
        owners = {'schema': 'orthemology-reader-owner-map-v1', 'baseline': {'commit': self.baseline},
                  'external_body_admissions': [], 'collections': [{'key': 'input19-fixture', 'include': ['**'],
                  'exclude': [], 'owners': [self.REGISTRY]}], 'required_work_sources': []}
        cross = {'schema': 'orthemology-reader-crosswalk-v1', 'coverage_stage': 'reader-candidate',
                 'sources': self.aliases, 'works': []}
        errors = self.reader.check(self.repo, owners, cross)
        self.assertFalse([error for error in errors if error.startswith((
            'unsafe-source:', 'baseline-source:', 'source-mode:', 'source-drift:', 'source-scope:', 'owner:', 'navigation-source:'))])
        self.assertTrue(errors, 'the deliberately finite context must not be relabelled whole-reader PASS')
        (self.repo / 'unadmitted.txt').write_text('new source\n')
        self.git('add', '--', 'unadmitted.txt')
        self.assertTrue(self.reader.check_corpus_currentness(self.repo, self.baseline))

    def test_references_and_exact_public_replay_pin_reject_unrelated_changes(self):
        previous = self.references.ROOT
        self.references.ROOT = self.repo
        try:
            path = self.repo / self.sample
            path.write_bytes(self.originals[self.sample] + b'wrong')
            self.assertFalse(self.references._resolves('/'.join(('docs', 'input.md')), self.sample))
            path.write_bytes(self.originals[self.sample])
            self.remove_originals()
            self.assertTrue(self.references._resolves('/'.join(('docs', 'input.md')), self.sample))
            self.assertTrue(self.references._resolves('/'.join(('docs', 'input.md')), '../' + self.sample))
        finally:
            self.references.ROOT = previous
        replay_path = 'scripts/replay_v5_successors.py'
        row = next(row for row in self.manifest['objects'] if row.get('repository_path') == replay_path)
        self.assertEqual(self.projection.check_object(self.repo, row), [])
        original = deepcopy(self.manifest)
        old = next(item for item in original['objects'] if item.get('repository_path') == replay_path)
        del old['repository_revision']
        del old['git_blob']
        self.assertTrue(self.reader._permitted_projection_consumer_pins(original, self.manifest))
        for field, value in (('git_blob', '0' * 40), ('repository_revision', '0' * 40), ('role', 'new_proof')):
            changed = deepcopy(self.manifest)
            item = next(item for item in changed['objects'] if item.get('repository_path') == replay_path)
            item[field] = value
            self.assertFalse(self.reader._permitted_projection_consumer_pins(original, changed))


    def projection_errors(self):
        """Exercise the real preservation predicate over this native20-file baseline."""
        from unittest.mock import patch
        before = self.index.read_bytes()
        with patch.object(self.projection, 'BASE', self.baseline), \
             patch.object(self.projection, 'HISTORICAL_PROSE', {}):
            errors = self.projection.check_preserved_roots(self.repo, {})
        self.assertEqual(self.index.read_bytes(), before)
        return errors

    def test_projection_accepts_authenticated_registry_and_exact_absence_states(self):
        self.assertEqual(self.projection_errors(), [])
        self.remove_originals()
        self.assertEqual(self.projection_errors(), [])
        self.git('update-index', '--force-remove', '--', *self.originals)
        self.assertEqual(self.projection_errors(), [])

    def test_projection_rejects_bad_registry_and_unrelated_protected_changes(self):
        registry = self.repo / self.REGISTRY
        extra = self.repo / '/'.join(('experiments', 'orthemology-v5-successors', 'unadmitted-input.json'))
        alias = self.repo / 'registry-link'
        for fault in ('body', 'mixed-edition', 'staged-body', 'staged-mode',
                      'missing', 'mode', 'symlink', 'hardlink', 'unrelated-addition'):
            with self.subTest(fault=fault):
                try:
                    if fault == 'body':
                        registry.write_bytes(self.compact + b'changed')
                    elif fault == 'mixed-edition':
                        registry.write_bytes(self.original_registry)
                    elif fault == 'staged-body':
                        registry.write_bytes(self.compact + b'changed')
                        self.git('add', '--', self.REGISTRY)
                        registry.write_bytes(self.compact)
                    elif fault == 'staged-mode':
                        self.git('update-index', '--chmod=+x', '--', self.REGISTRY)
                    elif fault == 'missing':
                        registry.unlink()
                    elif fault == 'mode':
                        registry.chmod(0o755)
                    elif fault == 'symlink':
                        alias.write_bytes(self.compact)
                        registry.unlink()
                        registry.symlink_to(alias)
                    elif fault == 'hardlink':
                        self.os.link(registry, alias)
                    else:
                        extra.write_text('{"new": "unqualified"}\n')
                        self.git('add', '--', str(extra.relative_to(self.repo)))
                    self.assertTrue(self.projection_errors())
                finally:
                    if registry.is_symlink():
                        registry.unlink()
                    if alias.exists():
                        alias.unlink()
                    if extra.exists():
                        extra.unlink()
                    registry.write_bytes(self.compact)
                    registry.chmod(0o644)
                    self.index.write_bytes(self.saved_index)
                self.assertEqual(self.projection_errors(), [])

    def test_projection_rejects_source_changes_and_concealed_index_states(self):
        target = self.repo / self.sample
        original = self.originals[self.sample]
        alias = self.repo / 'input-link'
        for fault in ('body', 'staged-body-hidden-by-absence', 'staged-mode',
                      'mode', 'symlink', 'hardlink', 'staged-deletion-with-present-copy'):
            with self.subTest(fault=fault):
                try:
                    if fault == 'body':
                        target.write_bytes(original + b'changed')
                    elif fault == 'staged-body-hidden-by-absence':
                        target.write_bytes(original + b'changed')
                        self.git('add', '--', self.sample)
                        target.unlink()
                    elif fault == 'staged-mode':
                        self.git('update-index', '--chmod=+x', '--', self.sample)
                    elif fault == 'mode':
                        target.chmod(0o755)
                    elif fault == 'symlink':
                        target.unlink()
                        target.symlink_to(self.repo / self.REGISTRY)
                    elif fault == 'hardlink':
                        self.os.link(target, alias)
                    else:
                        self.git('update-index', '--force-remove', '--', self.sample)
                    self.assertTrue(self.projection_errors())
                finally:
                    if target.is_symlink():
                        target.unlink()
                    if alias.exists():
                        alias.unlink()
                    target.write_bytes(original)
                    target.chmod(0o644)
                    self.index.write_bytes(self.saved_index)
                self.assertEqual(self.projection_errors(), [])


class LiveDerivedFixtureConsumerTests(unittest.TestCase):
    """Original public identities survive only through their exact live owners."""
    OWNERS = {
        'experiments/episode-reification/scripts/generate_fixtures.py': '9c39be153165e8d1c5a074243fc5f4ba467862ccc0d433bb42e7471230e4b929',
        'experiments/episode-reification-v2/scripts/generate_cases.py': '3b449a7580426fdf89f85612018473f92c3c2c274d4eea47e7046d1bcfe1bc89',
        'tests/schema-negative/NEGATIVE-FIXTURES.json': 'b229103cc93bb15d046cb15a1794d99d0cb40200fbc8fe9ac7ceff358c88d3e9',
    }

    @classmethod
    def setUpClass(cls):
        import os
        import resolve_t20_v6_source as source
        import validate_t20_v6_projection as projection
        import validate_internal_references as references
        import check_reader_pilot as reader
        cls.os, cls.source, cls.projection, cls.references, cls.reader = os, source, projection, references, reader
        cls.owner_bodies = {name: (ROOT / name).read_bytes() for name in cls.OWNERS}
        cls.originals = {}
        for name, identity in cls.OWNERS.items():
            body = cls.owner_bodies[name]
            if hashlib.sha256(body).hexdigest() != identity:
                raise ValueError('the test requires the exact public generator/consolidation owner')
            if name.endswith('.py'):
                scope = {'__name__': 'episode_public_renderer', '__file__': str(ROOT / name)}
                exec(compile(body, name, 'exec'), scope)
                prefix = name.split('/scripts/')[0] + '/fixtures/'
                cls.originals.update({prefix + path: text.encode() for path, text in scope['public_files']().items()})
            else:
                for row in json.loads(body)['invalid_fixtures']:
                    cls.originals['tests/invalid/' + row['id'] + '.json'] = (
                        json.dumps(row, ensure_ascii=False, indent=2) + '\n').encode()
        if len(cls.originals) != 123:
            raise ValueError('the finite original fixture population differs')
        manifest = json.loads((ROOT / 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json').read_bytes())
        cls.rows = {row['repository_path']: row for row in manifest['objects']
                    if row.get('repository_path') in cls.originals}
        if set(cls.rows) != set(cls.originals):
            raise ValueError('every original requires its real public row')
        cls.samples = [next(path for path in cls.originals if path.startswith(prefix)) for prefix in (
            'experiments/episode-reification/fixtures/',
            'experiments/episode-reification-v2/fixtures/', 'tests/invalid/')]

    def git(self, *args, data=None):
        env = {k: v for k, v in self.os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='',
                   GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=self.os.devnull,
                   GIT_CONFIG_SYSTEM=self.os.devnull, GIT_TERMINAL_PROMPT='0',
                   GIT_AUTHOR_NAME='Fixture test', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                   GIT_COMMITTER_NAME='Fixture test', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        return subprocess.check_output(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args],
                                       cwd=self.repo, env=env, input=data)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='live-derived-fixtures-')
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.git('-c', 'init.templateDir=', 'init', '-q')
        for name, body in {**self.owner_bodies, **self.originals}.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            path.chmod(0o644)
        self.git('add', '--', *self.owner_bodies, *self.originals)
        self.git('commit', '-qm', 'Finite original public fixture identities')
        self.baseline = self.git('rev-parse', 'HEAD').decode().strip()
        self.index = self.repo / '.git/index'
        self.raw_index = self.index.read_bytes()

    def read_original(self, path):
        gate = getattr(self.source, 'generated_fixture_bytes', None)
        self.assertTrue(callable(gate), 'live-derived original fixture resolver is absent')
        before = self.index.read_bytes()
        try:
            return gate(self.repo, path)
        finally:
            self.assertEqual(self.index.read_bytes(), before)

    def remove_originals(self):
        for name in self.originals:
            (self.repo / name).unlink()

    def test_present_unstaged_and_staged_originals_have_identical_public_bytes(self):
        for state in ('present', 'unstaged', 'staged'):
            with self.subTest(state=state):
                if state == 'unstaged':
                    self.remove_originals()
                elif state == 'staged':
                    self.git('update-index', '--force-remove', '--', *self.originals)
                for path in self.samples:
                    self.assertEqual(self.read_original(path), self.originals[path])
                    self.assertEqual(self.source.source_bytes(self.repo, self.rows[path]), self.originals[path])
                    self.assertEqual(self.projection.check_object(self.repo, self.rows[path]), [])
                self.assertEqual(self.source.generated_fixture_absences(self.repo),
                                 set() if state == 'present' else set(self.originals))

    def test_each_owner_body_and_staged_identity_are_required(self):
        for name, body in self.owner_bodies.items():
            with self.subTest(owner=name):
                path = self.repo / name
                path.write_bytes(body + b'\nwrong source\n')
                with self.assertRaises((ValueError, OSError)):
                    self.read_original(self.samples[0])
                self.git('add', '--', name)
                path.write_bytes(body)
                with self.assertRaises((ValueError, OSError)):
                    self.read_original(self.samples[0])
                self.index.write_bytes(self.raw_index)
                self.assertEqual(self.read_original(self.samples[0]), self.originals[self.samples[0]])

    def test_missing_executable_symlink_and_hardlinked_owners_are_rejected(self):
        for name, body in self.owner_bodies.items():
            for fault in ('missing', 'executable', 'symlink', 'hardlink'):
                with self.subTest(owner=name, fault=fault):
                    path = self.repo / name
                    extra = self.repo / 'owner-alias'
                    if fault == 'missing':
                        path.unlink()
                    elif fault == 'executable':
                        path.chmod(0o755)
                    elif fault == 'symlink':
                        extra.write_bytes(body)
                        path.unlink()
                        path.symlink_to(extra)
                    else:
                        self.os.link(path, extra)
                    with self.assertRaises((ValueError, OSError)):
                        self.read_original(self.samples[0])
                    if path.is_symlink():
                        path.unlink()
                    if extra.exists():
                        extra.unlink()
                    path.write_bytes(body)
                    path.chmod(0o644)

    def test_present_original_corruption_and_staged_concealment_are_rejected(self):
        for name in self.samples:
            with self.subTest(original=name):
                path = self.repo / name
                path.write_bytes(self.originals[name] + b'\nwrong original\n')
                with self.assertRaises((ValueError, OSError)):
                    self.read_original(name)
                self.assertTrue(self.projection.check_object(self.repo, self.rows[name]))
                self.git('add', '--', name)
                path.write_bytes(self.originals[name])
                with self.assertRaises((ValueError, OSError)):
                    self.read_original(name)
                path.unlink()
                with self.assertRaises((ValueError, OSError)):
                    self.read_original(name)
                self.index.write_bytes(self.raw_index)
                path.write_bytes(self.originals[name])

    def test_original_index_mode_and_unmerged_stage_and_symlink_are_rejected(self):
        name = self.samples[0]
        oid = self.git('rev-parse', self.baseline + ':' + name).decode().strip()
        self.git('update-index', '--cacheinfo', '100755,' + oid + ',' + name)
        with self.assertRaises((ValueError, OSError)):
            self.read_original(name)
        self.index.write_bytes(self.raw_index)
        self.git('update-index', '--force-remove', '--', name)
        self.git('update-index', '-z', '--index-info', data=('100644 ' + oid + ' 2\t' + name + '\0').encode())
        with self.assertRaises((ValueError, OSError)):
            self.read_original(name)
        self.index.write_bytes(self.raw_index)
        path = self.repo / name
        path.unlink()
        path.symlink_to(self.repo / self.samples[1])
        with self.assertRaises((ValueError, OSError)):
            self.read_original(name)

    def test_original_public_role_identity_and_complete_row_cannot_be_relabelled(self):
        for name in self.samples:
            self.assertEqual(self.read_original(name), self.originals[name])
            mutations = {'source_sha256': '0' * 64, 'public_sha256': '0' * 64,
                         'source_bytes': 1, 'public_bytes': 1, 'disposition': 'ADD_EXACT',
                         'role': 'accepted_proof', 'source_action': 'omit',
                         'declared_eligibility_basis': 'new_claim', 'required_dependencies': ['invented'],
                         'publication_basis': 'new_authority', 'repository_revision': self.baseline,
                         'git_blob': '0' * 40, 'unreviewed_extra': True}
            for field, value in mutations.items():
                with self.subTest(path=name, field=field):
                    row = deepcopy(self.rows[name])
                    row[field] = value
                    with self.assertRaises((ValueError, OSError)):
                        self.source.source_bytes(self.repo, row)
                    self.assertTrue(self.projection.check_object(self.repo, row))
        for outside in ('/'.join(('tests', 'invalid', 'not-admitted.json')),
                        'experiments/episode-reification-v2/fixtures/KEYS.json'):
            with self.assertRaises(ValueError):
                self.source.generated_fixture_bytes(self.repo, outside)

    def test_currentness_admits_only_the_exact_physically_absent_class(self):
        self.read_original(self.samples[0])
        self.remove_originals()
        self.assertEqual(self.reader.check_corpus_currentness(self.repo, self.baseline), [])
        self.git('update-index', '--force-remove', '--', *self.originals)
        self.assertEqual(self.reader.check_corpus_currentness(self.repo, self.baseline), [])
        name = self.samples[0]
        (self.repo / name).write_bytes(self.originals[name] + b'wrong')
        self.git('add', '--', name)
        self.assertTrue(self.reader.check_corpus_currentness(self.repo, self.baseline))
        (self.repo / name).unlink()
        self.git('update-index', '--force-remove', '--', name)
        (self.repo / 'unadmitted-source.txt').write_text('new material\n')
        self.git('add', '--', 'unadmitted-source.txt')
        self.assertTrue(self.reader.check_corpus_currentness(self.repo, self.baseline))

    def test_references_authenticate_present_and_absent_originals_before_exists(self):
        self.read_original(self.samples[0])
        previous = self.references.ROOT
        self.references.ROOT = self.repo
        try:
            for name in self.samples:
                path = self.repo / name
                path.write_bytes(self.originals[name] + b'wrong')
                self.assertFalse(self.references._resolves('/'.join(('docs', 'historical.md')), name))
                path.write_bytes(self.originals[name])
            self.remove_originals()
            for name in self.samples:
                self.assertTrue(self.references._resolves('/'.join(('docs', 'historical.md')), name))
                self.assertTrue(self.references._resolves('/'.join(('docs', 'historical.md')), '../' + name))
            self.assertFalse(self.references._resolves('/'.join(('docs', 'historical.md')), '/'.join(('tests', 'invalid', 'not-admitted.json'))))
        finally:
            self.references.ROOT = previous


class Digest176ReaderContractTests(unittest.TestCase):
    """Finite operational controls; original research bodies remain inert."""

    # Original coordinates joined to the immutable digest176 source admission.
    # The current consumer editions intentionally have distinct identities.
    PINS = {
        'scripts/validate_ar8r_codex_corpus_synthesis_v14.py': (
            'bf5693e9eaf14f932a7afef314772c5d6cfd19c3',
            'c2153d22937864584ca0310a129cb41badbcbea96e3a2175b53bd1a9a666a626',
            43318, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_ar8r_external_challenges.py': (
            '814d716588deff5a8f479deafc8e4d7e91e19c58',
            '621c70320e6695ea77d85c7bec7147193d3c3f013bada94ea6bae328a8616c7e',
            9558, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_ar8r_six_lane_v14_intake.py': (
            'd9511107288776ddab58e06e3892bb61f3bd66e9',
            '33de0e6b174499960cc2c521ab5ab5f2f13cb66467247636aa460419073745a3',
            19144, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bk_public_snapshot.py': (
            'b7a701ad73a96d9de760f22778a17f2128eb7799',
            'ba437ce44adf1ab03d1f797a3c5a72f8991b99186a733bdfc2f9574b02d3d4fd',
            20394, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bv_semantic_reissue.py': (
            '06a0f45454a02b7c849682e563f0b1aa98cab963',
            '818230667805e3db999dc52bd22376a4425e58a85f75e561da4ca39acd75e680',
            16337, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bw_cj_semantic_reissue.py': (
            'cb72e0de65eb40d0bd659e49e2a4b8a46ef197a9',
            '0d75bcefc899d15b2d35377fa15b54c6d12d180a74a506bc9cd84212206c3311',
            19380, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
    }

    @classmethod
    def setUpClass(cls):
        import ast
        source = (ROOT / 'scripts/check_reader_pilot.py').read_text()
        names = {'_permitted_projection_consumer_pins', 'check_corpus_currentness'}
        nodes = [node for node in ast.parse(source).body
                 if (isinstance(node, ast.FunctionDef) and node.name in names)
                 or (isinstance(node, ast.Assign) and any(
                     isinstance(target, ast.Name) and target.id == 'REFACTOR_EDIT_PATHS'
                     for target in node.targets))]
        if len(nodes) != 3:
            raise AssertionError('the exact operational function/constant population changed')
        cls.namespace = {'Path': Path, 'REVIEWED_AUTHORITY_EDITS': {}}
        exec(compile(ast.Module(body=nodes, type_ignores=[]),
                     'reader-digest176-operational-interface', 'exec'), cls.namespace)
        # Preserve the actual finite status selector in this metadata-only
        # fixture. An unrelated status absence qualifier still must not run.
        resolver = (ROOT / 'scripts/resolve_t20_v6_source.py').read_text()
        status_functions = {'digest', 'status_record_candidate'}
        status_constants = {'STATUS_RECORD_PATH_HASHES', 'STATUS_RECORD_OWNERS'}
        status_nodes, found = [], set()
        for node in ast.parse(resolver).body:
            if isinstance(node, ast.FunctionDef) and node.name in status_functions:
                status_nodes.append(node); found.add(node.name)
            elif isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id in status_constants:
                    status_nodes.append(node); found.add(target.id)
        if found != status_functions | status_constants:
            raise AssertionError('exact finite status selector population differs')
        cls.namespace['hashlib'] = hashlib
        exec(compile(ast.Module(body=status_nodes, type_ignores=[]),
                     'reader-status-selector-interface', 'exec'), cls.namespace)

    def setUp(self):
        import types
        self.namespace = dict(type(self).namespace)
        self.registry = 'synthetic/continuation-registry.json'
        self.prerequisites = {
            self.registry: ('1' * 40, '1' * 64, 11, '2' * 40),
            'scripts/replay_v5_successors.py': ('3' * 40, '3' * 64, 13, '2' * 40),
            'tests/v5_successor_fixtures.py': (
                'ccf0bd64f34b10f65ed8bd1bdd8a88adcaf03c7f',
                '283ea7d698a5bf6a208e45260ee9078f819ecdb25a42c6dd2252d794d2dd3233',
                13030, '69f3f9284f2cb94433958c0669fc9b06a9760fe7'),
        }
        self.owners = types.ModuleType('validate_v5_successors')
        self.owners.PRESERVATION_OWNER_ORIGINAL = {
            self.registry: self.prerequisites[self.registry][:3]}
        self.namespace.update(
            HISTORICAL_PROSE={}, HISTORICAL_PROSE_REVISIONS={},
            PUBLIC_READER_NOTE_PATHS=set(), NEXT24_PUBLIC_PROSE=set(),
            CONTINUATION_REGISTRY_PATH=self.registry,
            CONTINUATION_REGISTRY_REVISION=self.prerequisites[self.registry][3],
            FIXTURE_CONSUMER_ORIGINAL={}, FIXTURE_CONSUMER_REVISION='2' * 40,
            SUCCESSOR_INPUT_REPLAY_ORIGINAL=self.prerequisites['scripts/replay_v5_successors.py'])
        # Rebind the selected functions to this case's isolated metadata namespace.
        for name in ('_permitted_projection_consumer_pins', 'check_corpus_currentness'):
            original = type(self).namespace[name]
            self.namespace[name] = types.FunctionType(
                original.__code__, self.namespace, name, original.__defaults__)
        bindings = dict(self.prerequisites, **self.PINS)
        self.original = {
            'schema': 'inert-digest176-interface-fixture',
            'objects': [dict(repository_path=path, source_sha256=identity,
                             public_sha256=identity, source_bytes=size, public_bytes=size,
                             disposition='REUSE', role='unchanged-public-role',
                             declared_eligibility_basis='unchanged-basis',
                             required_dependencies=[], publication_basis='unchanged-publication')
                        for path, (_, identity, size, _) in bindings.items()],
        }
        self.prior = self.pinned(self.original, self.prerequisites)
        self.current = self.pinned(self.prior, self.PINS)

    @staticmethod
    def pinned(document, bindings):
        result = deepcopy(document)
        for path, (blob, _, _, revision) in bindings.items():
            row = next(row for row in result['objects'] if row['repository_path'] == path)
            row.update(git_blob=blob, repository_revision=revision)
        return result

    def permitted(self, candidate, original=None):
        from unittest.mock import patch
        with patch.dict(sys.modules, {'validate_v5_successors': self.owners}):
            return self.namespace['_permitted_projection_consumer_pins'](
                self.original if original is None else original, candidate)

    def test_preceding_coordinate_form_remains_admissible(self):
        self.assertTrue(self.permitted(self.prior))

    def test_complete_six_consumer_extension_is_admitted(self):
        self.assertEqual(len(self.PINS), 6)
        self.assertTrue(self.permitted(self.current))
        for path, (blob, identity, size, revision) in self.PINS.items():
            old = next(row for row in self.original['objects'] if row['repository_path'] == path)
            new = next(row for row in self.current['objects'] if row['repository_path'] == path)
            self.assertEqual((old['source_sha256'], old['public_sha256'],
                              old['source_bytes'], old['public_bytes']),
                             (identity, identity, size, size))
            self.assertEqual(new, dict(old, repository_revision=revision, git_blob=blob))

    def test_partial_six_consumer_extensions_are_refused(self):
        for path in self.PINS:
            with self.subTest(missing=path):
                candidate = deepcopy(self.current)
                row = next(row for row in candidate['objects'] if row['repository_path'] == path)
                row.pop('repository_revision')
                row.pop('git_blob')
                self.assertFalse(self.permitted(candidate))

    def test_six_consumer_identity_role_and_coordinate_tampering_is_refused(self):
        changes = (('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                   ('source_bytes', 1), ('public_bytes', 1),
                   ('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                   ('repository_path', 'scripts/' 'unreviewed_consumer.py'),
                   ('disposition', 'PROJECT'), ('role', 'reclassified'),
                   ('declared_eligibility_basis', 'changed'),
                   ('required_dependencies', ['unreviewed']),
                   ('publication_basis', 'unreviewed'))
        for path in self.PINS:
            for field, value in changes:
                with self.subTest(path=path, field=field):
                    candidate = deepcopy(self.current)
                    next(row for row in candidate['objects']
                         if row['repository_path'] == path)[field] = value
                    self.assertFalse(self.permitted(candidate))
            for field in ('git_blob', 'repository_revision'):
                with self.subTest(path=path, missing=field):
                    candidate = deepcopy(self.current)
                    next(row for row in candidate['objects']
                         if row['repository_path'] == path).pop(field)
                    self.assertFalse(self.permitted(candidate))

    def test_corrupt_original_identity_is_not_rebound(self):
        for path in self.PINS:
            for field, value in (('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                                 ('source_bytes', 1), ('public_bytes', 1), ('disposition', 'PROJECT')):
                with self.subTest(path=path, field=field):
                    original = deepcopy(self.original)
                    next(row for row in original['objects']
                         if row['repository_path'] == path)[field] = value
                    candidate = self.pinned(original, dict(self.prerequisites, **self.PINS))
                    self.assertFalse(self.permitted(candidate, original))

    def test_duplicate_missing_reordered_and_unlisted_records_are_refused(self):
        path = next(iter(self.PINS))
        for change in ('duplicate', 'missing', 'reorder', 'unlisted', 'metadata'):
            with self.subTest(change=change):
                candidate = deepcopy(self.current)
                row = next(row for row in candidate['objects'] if row['repository_path'] == path)
                if change == 'duplicate':
                    candidate['objects'].append(deepcopy(row))
                elif change == 'missing':
                    candidate['objects'].remove(row)
                elif change == 'reorder':
                    candidate['objects'].reverse()
                elif change == 'unlisted':
                    candidate['objects'].append(dict(row, repository_path='scripts/' 'nearby_unreviewed.py'))
                else:
                    candidate['schema'] = 'unreviewed'
                self.assertFalse(self.permitted(candidate))

    def currentness(self, entries, *, cached=None, worktree=None):
        # Only the name/status routing interface is exercised here. Every
        # unrelated qualification callable fails if this fixture invokes it.
        def unexpected(*args, **kwargs):
            raise AssertionError('unrelated original-body qualifier was invoked')
        ns = self.namespace
        for name in ('CHECKPOINT_PUBLIC_COPY_PATHS', 'CHECKPOINT_COPY_PATHS', 'CHECKPOINT_RECORD_COPY_PATHS',
                     'CHECKPOINT_PACKAGE_COPY_PATHS', 'FORMAL_COPY_PATHS','FORMAL_PROVIDER_PATHS',
                     'CHECKPOINT_CODE_COPY_PATHS', 'DIGEST_RECORD_PATHS','ADMISSION_RECORD_PATHS',
                     'SUCCESSOR_INPUT_PATHS', 'GENERATED_FIXTURE_PATHS',
                     'ADMIN_RECORD_PATHS', 'ADMIN_GUIDES', 'CONTINUATION_OWNER_PATHS',
                     'TYPED_GUIDES', 'SUCCESSOR_CALCULUS_GUIDES'):
            ns[name] = set()
        for name in ('PMR007_DEEP_PREFIX', 'PMR007_ROUNDS_PREFIX',
                     'PMR007_ROUNDS_FORMALIZATION', 'CONTINUATION_COPY_ROOT',
                     'SUCCESSOR_INPUT_REGISTRY', 'SUCCESSOR_CALCULUS_MAP', 'MEDIATOR_GUIDE'):
            ns[name] = 'synthetic-unrelated/' + name
        for name in ('pmr007_deep_duplicate_paths', 'pmr007_rounds_duplicate_paths',
                     'checkpoint_public_duplicate_paths', 'checkpoint_duplicate_paths', 'checkpoint_record_duplicate_paths',
                     'checkpoint_package_duplicate_paths', 'formal_duplicate_paths','formal_provider_absences',
                     'checkpoint_code_duplicate_paths', 'digest_record_absences',
                     'pmr007_rounds_formalization_navigation', 'continuation_duplicate_paths',
                     'successor_input_absences', 'successor_calculus_map_absences',
                     'generated_fixture_absences', 'binding_record_absences',
                     'administrative_record_absences', 'administrative_guide_source_bytes',
                     'status_record_absences'):
            ns[name] = unexpected
        ns['binding_record_candidate'] = lambda path: path.startswith('synthetic-binding/')
        body = ''.join(status + '\0' + path + '\0' for status, path in entries).encode()
        calls = []
        def diff(repo, argv):
            calls.append(tuple(argv))
            value = cached if '--cached' in argv else worktree
            return subprocess.CompletedProcess(argv, 0, body) if value is None else value
        ns['readonly_git_diff'] = diff
        errors = ns['check_corpus_currentness'](Path('inert-routing-fixture'), 'synthetic-baseline')
        return errors, calls

    def test_exact_six_engineering_paths_are_admitted(self):
        errors, calls = self.currentness([('M', path) for path in self.PINS])
        self.assertEqual(errors, [])
        self.assertEqual(len(calls), 2)
        self.assertIn('--cached', calls[0])
        self.assertNotIn('--cached', calls[1])

    def test_unlisted_engineering_paths_and_deletions_still_require_review(self):
        paths = [path + '.unreviewed' for path in self.PINS]
        paths.append('scripts/' 'validate_ar8r_unreviewed.py')
        for status in ('A', 'M', 'D'):
            with self.subTest(status=status):
                errors, calls = self.currentness([(status, path) for path in paths])
                self.assertEqual(len(calls), 2)
                self.assertEqual(errors, [
                    'corpus-currentness: ' + path +
                    ' requires source-baseline and work/support disposition review' for path in paths])

    def test_index_worktree_and_malformed_diff_fail_closed(self):
        bad = [('M', 'scripts/' 'unlisted_engineering_owner.py')]
        empty = subprocess.CompletedProcess([], 0, b'')
        for which in ('cached', 'worktree'):
            with self.subTest(empty_side=which):
                errors, calls = self.currentness(bad, **{which: empty})
                self.assertEqual(len(errors), 1)
                self.assertEqual(len(calls), 2)
        for result in (subprocess.CompletedProcess([], 1, b''),
                       subprocess.CompletedProcess([], 0, b'M\0'),
                       subprocess.CompletedProcess([], 0, b'M\0\xff\0')):
            with self.subTest(result=(result.returncode, result.stdout)):
                errors, _ = self.currentness([], cached=result)
                self.assertEqual(len(errors), 1)
                self.assertTrue(errors[0].startswith('corpus-currentness:'))


class ReviewedSourcingLedgerControls(unittest.TestCase):
    """Finite actual-interface controls, without native Git or source replay."""
    SOURCE = Path(__file__).resolve().parents[1] / 'scripts/check_reader_pilot.py'

    def _module(self):
        import ast, os, stat, types
        names={'safe_path','reviewed_indexed_modification','reviewed_sourcing_ledger_modifications','check_corpus_currentness'}
        nodes=[n for n in ast.parse(self.SOURCE.read_bytes()).body
               if isinstance(n,ast.FunctionDef) and n.name in names]
        self.assertEqual({n.name for n in nodes}, names)
        module=types.ModuleType('inert_sourcing_ledger')
        module.__dict__.update(Path=Path,hashlib=hashlib,os=os,stat=stat,subprocess=subprocess,REVIEWED_AUTHORITY_EDITS={})
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(self.SOURCE),'exec'),module.__dict__)
        return module

    def _fixture(self, *, state='valid'):
        import types
        module=self._module();tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        repo=Path(tmp.name);path='docs/sourcing/R3-SOURCING-LEDGER.md'
        node=repo/path;node.parent.mkdir(parents=True);original=b'original scoped attribution\n'
        current=original+b'additive VIA-COMPILATION attribution\n';node.write_bytes(current)
        identity=lambda b:(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),hashlib.sha256(b).hexdigest(),len(b))
        module.REVIEWED_SOURCING_LEDGER=(path,'a'*40,identity(original),identity(current))
        before='100644 blob '+identity(original)[0]+'\t'+path+'\0'
        stage=('100644 '+identity(current)[0]+' 0\t'+path+'\0').encode();calls=[]
        def git(argv,**kwargs):
            self.assertEqual(kwargs,dict(cwd=repo,capture_output=True,check=False));calls.append(argv)
            if 'ls-tree' in argv:body=before.encode()
            elif 'cat-file' in argv:body=original if state!='history-bytes' else original+b'wrong'
            elif 'ls-files' in argv:
                body=stage
                if state=='index':body=stage.replace(b'100644',b'100755')
                if state=='conflict':body=stage.replace(b' 0\t',b' 1\t')
                if state=='late-index' and sum('ls-files' in a for a in calls)>1:body=b''
                if state=='late-body' and sum('ls-files' in a for a in calls)>1:node.write_bytes(current+b'late')
            else:raise AssertionError('unexpected native command '+repr(argv))
            return subprocess.CompletedProcess(argv,1 if state=='native-failure' else 0,body,b'')
        module.subprocess=types.SimpleNamespace(run=git)
        if state=='wrong-bytes':node.write_bytes(current+b'wrong')
        if state=='missing':node.unlink()
        if state=='executable':node.chmod(0o755)
        if state=='symlink':
            target=repo/'ordinary';target.write_bytes(current);node.unlink();node.symlink_to(target)
        if state=='hardlink':
            import os
            os.link(node,repo/'ordinary')
        return module,repo,calls

    def test_exact_postimage_and_original_history_are_admitted(self):
        module,repo,calls=self._fixture()
        self.assertEqual(module.reviewed_sourcing_ledger_modifications(repo),{'docs/sourcing/R3-SOURCING-LEDGER.md'})
        self.assertEqual(sum('ls-files' in a for a in calls),2)

    def test_wrong_missing_executable_symlink_hardlink_worktree_refuse(self):
        for state in ('wrong-bytes','missing','executable','symlink','hardlink'):
            with self.subTest(state=state):
                module,repo,_=self._fixture(state=state)
                with self.assertRaises((ValueError,OSError)):module.reviewed_sourcing_ledger_modifications(repo)

    def test_wrong_conflicted_or_late_changed_index_refuse(self):
        for state in ('index','conflict','late-index'):
            with self.subTest(state=state):
                module,repo,_=self._fixture(state=state)
                with self.assertRaises((ValueError,OSError)):module.reviewed_sourcing_ledger_modifications(repo)

    def test_wrong_history_failed_native_and_late_body_refuse(self):
        for state in ('history-bytes','native-failure','late-body'):
            with self.subTest(state=state):
                module,repo,_=self._fixture(state=state)
                with self.assertRaises((ValueError,OSError)):module.reviewed_sourcing_ledger_modifications(repo)

    def _currentness(self, changes, qualification='valid'):
        module=self._module();calls=[]
        namespace=module.__dict__
        namespace.update(REFACTOR_EDIT_PATHS=set(),PMR007_DEEP_PREFIX='unused-deep',
            PMR007_ROUNDS_PREFIX='unused-rounds',PMR007_ROUNDS_FORMALIZATION='unused-round-guide',
            CONTINUATION_COPY_ROOT='unused-continuation/',SUCCESSOR_INPUT_REGISTRY='unused-input',
            SUCCESSOR_CALCULUS_MAP='unused-calculus',MEDIATOR_GUIDE='unused-guide')
        for name in ('CHECKPOINT_PUBLIC_COPY_PATHS', 'CHECKPOINT_COPY_PATHS','CHECKPOINT_RECORD_COPY_PATHS','CHECKPOINT_PACKAGE_COPY_PATHS',
            'FORMAL_COPY_PATHS','FORMAL_PROVIDER_PATHS','CHECKPOINT_CODE_COPY_PATHS','DIGEST_RECORD_PATHS','ADMISSION_RECORD_PATHS','SUCCESSOR_INPUT_PATHS',
            'GENERATED_FIXTURE_PATHS','ADMIN_RECORD_PATHS','CONTINUATION_OWNER_PATHS','STATUS_RECORD_OWNERS',
            'FIXTURE_CONSUMER_ORIGINAL','HISTORICAL_PROSE','ADMIN_GUIDES','TYPED_GUIDES','SUCCESSOR_CALCULUS_GUIDES'):
            namespace[name]=set()
        for name in ('pmr007_deep_duplicate_paths','pmr007_rounds_duplicate_paths','checkpoint_public_duplicate_paths', 'checkpoint_duplicate_paths',
            'checkpoint_record_duplicate_paths','checkpoint_package_duplicate_paths','formal_duplicate_paths','formal_provider_absences',
            'checkpoint_code_duplicate_paths','digest_record_absences'):
            namespace[name]=lambda *a:set()
        namespace.update(binding_record_candidate=lambda p:False,status_record_candidate=lambda p:False)
        def qualify(repo):
            calls.append('qualify')
            if qualification=='error':raise ValueError('wrong reviewed edition')
            return {'docs/sourcing/R3-SOURCING-LEDGER.md'} if qualification=='valid' else set()
        namespace['reviewed_sourcing_ledger_modifications']=qualify
        namespace['readonly_git_diff']=lambda *a,**k:subprocess.CompletedProcess([],0,
            ''.join(s+'\0'+p+'\0' for s,p in changes).encode(),b'')
        return module.check_corpus_currentness(Path('unused-inert-root'),'unused-baseline'),calls

    def test_gate_admits_only_qualified_named_modification(self):
        errors,calls=self._currentness([('M','docs/sourcing/R3-SOURCING-LEDGER.md')])
        self.assertEqual(errors,[]);self.assertEqual(calls,['qualify','qualify'])

    def test_gate_rejects_unqualified_modification(self):
        for state in ('empty','error'):
            with self.subTest(state=state):
                errors,_=self._currentness([('M','docs/sourcing/R3-SOURCING-LEDGER.md')],state)
                self.assertTrue(errors)

    def test_gate_rejects_deletion_type_addition_and_unrelated_modification(self):
        for status,path in [('D','docs/sourcing/R3-SOURCING-LEDGER.md'),('T','docs/sourcing/R3-SOURCING-LEDGER.md'),
                            ('A','docs/sourcing/R3-SOURCING-LEDGER.md'),('M','docs/sourcing/unrelated.md')]:
            with self.subTest(status=status,path=path):
                errors,calls=self._currentness([(status,path)])
                self.assertTrue(errors);self.assertEqual(calls,[])

    def test_gate_unchanged_liveness_and_extra_path_refusal(self):
        errors,calls=self._currentness([]);self.assertEqual((errors,calls),([],[]))
        errors,_=self._currentness([('M','docs/sourcing/R3-SOURCING-LEDGER.md'),('M','unrelated.md')])
        self.assertTrue(errors)


class ReviewedAuthorityControls(unittest.TestCase):
    """Exact current owner editions, not an arbitrary operational-edit waiver."""
    PATHS = ('scripts/validate_candidate_state.py', 'scripts/validate_review_state.py',
             'tests/test_candidate_state.py')

    def fixture(self, state='valid'):
        import ast,os,stat,types
        source=(ROOT/'scripts/check_reader_pilot.py').read_bytes()
        names={'safe_path','reviewed_indexed_modification','reviewed_authority_modifications','check_corpus_currentness'}
        nodes=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in names]
        self.assertEqual({n.name for n in nodes},names,'exact reviewed authority owner is missing')
        module=types.ModuleType('isolated_reviewed_authority')
        module.__dict__.update(Path=Path,hashlib=hashlib,os=os,stat=stat,subprocess=subprocess)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual-reviewed-authority-functions','exec'),module.__dict__)
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);repo=Path(temp.name)
        identity=lambda b:(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),hashlib.sha256(b).hexdigest(),len(b))
        originals={p:('original authority '+p+'\n').encode() for p in self.PATHS}
        currents={p:b+b'reviewed exact successor\n' for p,b in originals.items()}
        module.REVIEWED_AUTHORITY_EDITS={p:(p,'a'*40,identity(originals[p]),identity(currents[p])) for p in self.PATHS}
        for path,body in currents.items():
            node=repo/path;node.parent.mkdir(parents=True,exist_ok=True);node.write_bytes(body)
        calls=[];counts={}
        def git(argv,**kwargs):
            self.assertEqual(kwargs,dict(cwd=repo,capture_output=True,check=False));calls.append(argv)
            path=argv[-1].split(':',1)[-1] if 'cat-file' in argv else argv[-1]
            self.assertIn(path,self.PATHS)
            if 'ls-tree' in argv:
                body=('100644 blob '+identity(originals[path])[0]+'\t'+path+'\0').encode()
                if state=='wrong-tree':body=body.replace(b'100644',b'100755')
            elif 'cat-file' in argv:body=originals[path]+(b'wrong' if state=='wrong-history' else b'')
            elif 'ls-files' in argv:
                counts[path]=counts.get(path,0)+1
                body=('100644 '+identity(currents[path])[0]+' 0\t'+path+'\0').encode()
                if state=='index':body=body.replace(b' 0\t',b' 1\t')
                if state=='late-index' and counts[path]>1:body=b''
            else:raise AssertionError('Unexpected native operation')
            return subprocess.CompletedProcess(argv,1 if state=='native-failure' else 0,body,b'')
        module.subprocess=types.SimpleNamespace(run=git)
        node=repo/self.PATHS[0]
        if state=='wrong-body':node.write_bytes(b'X'+currents[self.PATHS[0]][1:])
        if state=='missing':node.unlink()
        if state=='executable':node.chmod(0o755)
        if state=='symlink':
            target=repo/'ordinary';target.write_bytes(node.read_bytes());node.unlink();node.symlink_to(target)
        if state=='hardlink':os.link(node,repo/'ordinary')
        return module,repo,calls

    def test_exact_three_owner_editions_and_requested_subset(self):
        module,repo,calls=self.fixture()
        self.assertEqual(module.reviewed_authority_modifications(repo,set(self.PATHS)),set(self.PATHS))
        self.assertEqual(module.reviewed_authority_modifications(repo,{self.PATHS[1]}),{self.PATHS[1]})

    def test_wrong_missing_or_nonordinary_current_owner_refuses(self):
        for state in ('wrong-body','missing','executable','symlink','hardlink'):
            with self.subTest(state=state):
                module,repo,_=self.fixture(state)
                with self.assertRaises((ValueError,OSError)):
                    module.reviewed_authority_modifications(repo,set(self.PATHS))

    def test_history_index_and_native_failures_refuse(self):
        for state in ('wrong-tree','wrong-history','index','late-index','native-failure'):
            with self.subTest(state=state):
                module,repo,_=self.fixture(state)
                with self.assertRaises((ValueError,OSError)):
                    module.reviewed_authority_modifications(repo,set(self.PATHS))
        module,repo,_=self.fixture()
        with self.assertRaises(ValueError):module.reviewed_authority_modifications(repo,{'scripts/unrelated.py'})

    def currentness(self,changes,qualification='valid'):
        base=ReviewedSourcingLedgerControls()
        module=base._module();ns=module.__dict__;calls=[]
        ns.update(REFACTOR_EDIT_PATHS=set(),PMR007_DEEP_PREFIX='unused-deep',PMR007_ROUNDS_PREFIX='unused-rounds',
            PMR007_ROUNDS_FORMALIZATION='unused-formal',CONTINUATION_COPY_ROOT='unused-copy/',SUCCESSOR_INPUT_REGISTRY='unused-input',
            SUCCESSOR_CALCULUS_MAP='unused-map',MEDIATOR_GUIDE='unused-guide',REVIEWED_AUTHORITY_EDITS={p:None for p in self.PATHS})
        for name in ('CHECKPOINT_PUBLIC_COPY_PATHS', 'CHECKPOINT_COPY_PATHS','CHECKPOINT_RECORD_COPY_PATHS','CHECKPOINT_PACKAGE_COPY_PATHS','FORMAL_COPY_PATHS','FORMAL_PROVIDER_PATHS',
                     'CHECKPOINT_CODE_COPY_PATHS','DIGEST_RECORD_PATHS','ADMISSION_RECORD_PATHS','SUCCESSOR_INPUT_PATHS','GENERATED_FIXTURE_PATHS',
                     'ADMIN_RECORD_PATHS','CONTINUATION_OWNER_PATHS','STATUS_RECORD_OWNERS','FIXTURE_CONSUMER_ORIGINAL',
                     'HISTORICAL_PROSE','ADMIN_GUIDES','TYPED_GUIDES','SUCCESSOR_CALCULUS_GUIDES'):ns[name]=set()
        for name in ('pmr007_deep_duplicate_paths','pmr007_rounds_duplicate_paths','checkpoint_public_duplicate_paths', 'checkpoint_duplicate_paths',
                     'checkpoint_record_duplicate_paths','checkpoint_package_duplicate_paths','formal_duplicate_paths','formal_provider_absences',
                     'checkpoint_code_duplicate_paths','digest_record_absences'):ns[name]=lambda *a:set()
        ns.update(binding_record_candidate=lambda p:False,status_record_candidate=lambda p:False)
        def qualify(repo,requested):
            calls.append(set(requested))
            if qualification=='error':raise ValueError('wrong exact owner edition')
            return set(requested) if qualification=='valid' else set()
        ns['reviewed_authority_modifications']=qualify
        ns['readonly_git_diff']=lambda *a,**k:subprocess.CompletedProcess([],0,''.join(s+'\0'+p+'\0' for s,p in changes).encode(),b'')
        return module.check_corpus_currentness(Path('inert-authority-root'),'unused-baseline'),calls

    def test_currentness_admits_only_requested_qualified_modifications(self):
        errors,calls=self.currentness([('M',p) for p in self.PATHS])
        self.assertEqual(errors,[]);self.assertEqual(calls,[set(self.PATHS)]*2)
        for state in ('error','empty'):
            with self.subTest(state=state):self.assertTrue(self.currentness([('M',self.PATHS[0])],state)[0])

    def test_deletion_type_change_addition_and_unrelated_edit_refuse(self):
        for path in self.PATHS:
            for status in ('D','T','A'):
                with self.subTest(path=path,status=status):
                    errors,calls=self.currentness([(status,path)])
                    self.assertTrue(errors);self.assertEqual(calls,[])
        self.assertTrue(self.currentness([('M','scripts/unrelated.py')])[0])

    def test_unchanged_positive_and_extra_path_refusal(self):
        self.assertEqual(self.currentness([]),([],[]))
        self.assertTrue(self.currentness([('M',self.PATHS[0]),('M','unrelated.md')])[0])


class ReviewedAttributionPinControls(unittest.TestCase):
    PINS={
        'scripts/validate_review_state.py':('95087964f175e00c5dc1a628bc83d40377c6b911',
            '240dd79778d8fded8744873ddfc298e3206fa120dbe0417b50198983975efff0',34750,'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/sourcing/R3-SOURCING-LEDGER.md':('2ed9e182cb9db7d38d7c56c0f043983c99f8c940',
            '2177de55bb84adc24b69dd8551c12893e7f4dd7eae2a5d5d643b372b9236b770',5421,'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}

    def setUp(self):
        Digest176ReaderContractTests.setUpClass()
        self.base=Digest176ReaderContractTests();self.base.setUp()
        for path,(_,identity,size,_) in self.PINS.items():
            row=dict(repository_path=path,source_sha256=identity,public_sha256=identity,
                     source_bytes=size,public_bytes=size,disposition='REUSE',role='unchanged-role')
            for document in (self.base.original,self.base.prior,self.base.current):
                document['objects'].append(deepcopy(row))
        self.current=self.base.pinned(self.base.current,self.PINS)

    def test_previous_six_pin_form_remains_accepted(self):
        self.assertTrue(self.base.permitted(self.base.current))

    def test_complete_two_original_coordinates_are_admitted(self):
        self.assertTrue(self.base.permitted(self.current))

    def test_partial_original_coordinate_pair_refuses(self):
        for path in self.PINS:
            with self.subTest(path=path):
                changed=deepcopy(self.current);row=next(r for r in changed['objects'] if r['repository_path']==path)
                row.pop('repository_revision');row.pop('git_blob')
                self.assertFalse(self.base.permitted(changed))

    def test_identity_coordinate_type_or_role_change_refuses(self):
        mutations=(('source_sha256','0'*64),('public_sha256','0'*64),('source_bytes',1),('public_bytes',1),
                   ('repository_revision','HEAD'),('git_blob','0'*40),('disposition','PROJECT'),('role','reclassified'))
        for path in self.PINS:
            for field,value in mutations:
                with self.subTest(path=path,field=field):
                    changed=deepcopy(self.current);next(r for r in changed['objects'] if r['repository_path']==path)[field]=value
                    self.assertFalse(self.base.permitted(changed))

    def test_missing_duplicate_reordered_and_unrelated_rows_refuse(self):
        for kind in ('missing','duplicate','reordered','unrelated','metadata'):
            with self.subTest(kind=kind):
                changed=deepcopy(self.current)
                if kind=='missing':changed['objects'].pop()
                elif kind=='duplicate':changed['objects'].append(deepcopy(changed['objects'][-1]))
                elif kind=='reordered':changed['objects'].reverse()
                elif kind=='unrelated':changed['objects'][0]['role']='unreviewed'
                else:changed['schema']='unreviewed'
                self.assertFalse(self.base.permitted(changed))


class ReviewedGovernanceEditionControls(unittest.TestCase):
    """Exact original-present and original-absent engineering editions."""
    OWNER = 'scripts/validate_cross_record_semantics.py'
    ADDED = 'tests/test_cross_record_semantics.py'

    def fixture(self, state='valid', selected=None):
        import ast, os, stat, types
        selected = selected or self.ADDED
        names = {'safe_path', 'reviewed_indexed_modification', 'reviewed_authority_modifications'}
        nodes = [n for n in ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes()).body
                 if isinstance(n, ast.FunctionDef) and n.name in names]
        self.assertEqual({n.name for n in nodes}, names)
        module = types.ModuleType('reviewed_governance_editions')
        module.__dict__.update(Path=Path, hashlib=hashlib, os=os, stat=stat)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'exact-edition-functions', 'exec'), module.__dict__)
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); repo = Path(tmp.name)
        identity = lambda b: (hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(),
                              hashlib.sha256(b).hexdigest(), len(b))
        original = b'original bounded validator\n'
        bodies = {self.OWNER: original + b'reviewed baseline check\n', self.ADDED: b'reviewed live controls\n'}
        module.REVIEWED_AUTHORITY_EDITS = {
            self.OWNER: (self.OWNER, 'a' * 40, identity(original), identity(bodies[self.OWNER])),
            self.ADDED: (self.ADDED, 'a' * 40, None, identity(bodies[self.ADDED]))}
        for path, body in bodies.items():
            q = repo / path; q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(body)
        calls, counts = [], {}
        def native(argv, **kwargs):
            self.assertEqual(kwargs, dict(cwd=repo, capture_output=True, check=False))
            self.assertEqual(argv[:3], ['git', '--no-replace-objects', '--literal-pathspecs'])
            path = argv[-1].split(':', 1)[-1] if 'cat-file' in argv else argv[-1]
            self.assertIn(path, bodies); calls.append(argv)
            if 'ls-tree' in argv:
                body = b'' if path == self.ADDED else ('100644 blob ' + identity(original)[0] + '\t' + path + '\0').encode()
                if path == selected and state in ('preexisting', 'empty-predecessor', 'wrong-tree'):
                    predecessor = b'' if state == 'empty-predecessor' else original
                    mode = '100755' if state == 'wrong-tree' else '100644'
                    body = (mode + ' blob ' + identity(predecessor)[0] + '\t' + path + '\0').encode()
            elif 'cat-file' in argv:
                self.assertEqual(path, self.OWNER, 'an absent predecessor has no body to read')
                body = original + (b'wrong' if state == 'wrong-history' else b'')
            elif 'ls-files' in argv:
                counts[path] = counts.get(path, 0) + 1
                body = ('100644 ' + identity(bodies[path])[0] + ' 0\t' + path + '\0').encode()
                if path == selected and state == 'index-conflict': body = body.replace(b' 0\t', b' 1\t')
                if path == selected and state == 'late-index' and counts[path] > 1: body = b''
                if path == selected and state == 'late-body' and counts[path] > 1: (repo / path).write_bytes(bodies[path] + b'late')
            else: raise AssertionError('unexpected native command')
            failed = state == 'failed-history-query' and 'ls-tree' in argv and path == selected
            return subprocess.CompletedProcess(argv, 1 if failed else 0, body, b'')
        module.subprocess = types.SimpleNamespace(run=native)
        q = repo / selected
        if state == 'wrong-body': q.write_bytes(b'X' + bodies[selected][1:])
        if state == 'missing': q.unlink()
        if state == 'executable': q.chmod(0o755)
        if state == 'symlink':
            target = repo / 'ordinary-target'; target.write_bytes(q.read_bytes()); q.unlink(); q.symlink_to(target)
        if state == 'hardlink': os.link(q, repo / 'ordinary-link')
        return module, repo, calls

    def test_exact_present_and_absent_original_editions(self):
        module, repo, calls = self.fixture()
        self.assertEqual(module.reviewed_authority_modifications(repo, {self.OWNER, self.ADDED}),
                         {self.OWNER, self.ADDED})
        self.assertEqual(sum('cat-file' in c for c in calls), 1)
        self.assertEqual(sum('ls-files' in c for c in calls), 4)

    def test_absent_original_must_not_be_present_empty_or_unreceived(self):
        for state in ('preexisting', 'empty-predecessor', 'failed-history-query'):
            with self.subTest(state=state):
                module, repo, _ = self.fixture(state)
                with self.assertRaises(ValueError): module.reviewed_authority_modifications(repo, {self.ADDED})

    def test_both_current_editions_require_exact_ordinary_bytes(self):
        for path in (self.OWNER, self.ADDED):
            for state in ('wrong-body', 'missing', 'executable', 'symlink', 'hardlink'):
                with self.subTest(path=path, state=state):
                    module, repo, _ = self.fixture(state, path)
                    with self.assertRaises((ValueError, OSError)):
                        module.reviewed_authority_modifications(repo, {path})

    def test_index_and_TOCTOU_checks_apply_independently_to_both(self):
        for path in (self.OWNER, self.ADDED):
            for state in ('index-conflict', 'late-index', 'late-body', 'failed-history-query'):
                with self.subTest(path=path, state=state):
                    module, repo, _ = self.fixture(state, path)
                    with self.assertRaises(ValueError): module.reviewed_authority_modifications(repo, {path})

    def test_present_original_still_requires_exact_tree_and_body(self):
        for state in ('wrong-tree', 'wrong-history'):
            with self.subTest(state=state):
                module, repo, _ = self.fixture(state, self.OWNER)
                with self.assertRaises(ValueError): module.reviewed_authority_modifications(repo, {self.OWNER})

    def currentness(self, changes, outcome='valid'):
        module = ReviewedSourcingLedgerControls()._module(); ns = module.__dict__; calls = []
        ns.update(REFACTOR_EDIT_PATHS=set(), PMR007_DEEP_PREFIX='unused-deep', PMR007_ROUNDS_PREFIX='unused-rounds',
                  PMR007_ROUNDS_FORMALIZATION='unused-formal', CONTINUATION_COPY_ROOT='unused-copy/',
                  SUCCESSOR_INPUT_REGISTRY='unused-input', SUCCESSOR_CALCULUS_MAP='unused-map', MEDIATOR_GUIDE='unused-guide',
                  REVIEWED_AUTHORITY_EDITS={self.OWNER: (self.OWNER, 'a'*40, ('old', 'old', 1), ('new', 'new', 2)),
                                            self.ADDED: (self.ADDED, 'a'*40, None, ('new', 'new', 2))})
        for name in ('CHECKPOINT_PUBLIC_COPY_PATHS', 'CHECKPOINT_COPY_PATHS','CHECKPOINT_RECORD_COPY_PATHS','CHECKPOINT_PACKAGE_COPY_PATHS','FORMAL_COPY_PATHS','FORMAL_PROVIDER_PATHS',
                     'CHECKPOINT_CODE_COPY_PATHS','DIGEST_RECORD_PATHS','ADMISSION_RECORD_PATHS','SUCCESSOR_INPUT_PATHS','GENERATED_FIXTURE_PATHS',
                     'ADMIN_RECORD_PATHS','CONTINUATION_OWNER_PATHS','STATUS_RECORD_OWNERS','FIXTURE_CONSUMER_ORIGINAL',
                     'HISTORICAL_PROSE','ADMIN_GUIDES','TYPED_GUIDES','SUCCESSOR_CALCULUS_GUIDES'): ns[name] = set()
        for name in ('pmr007_deep_duplicate_paths','pmr007_rounds_duplicate_paths','checkpoint_public_duplicate_paths', 'checkpoint_duplicate_paths',
                     'checkpoint_record_duplicate_paths','checkpoint_package_duplicate_paths','formal_duplicate_paths','formal_provider_absences',
                     'checkpoint_code_duplicate_paths','digest_record_absences'): ns[name] = lambda *a: set()
        ns.update(binding_record_candidate=lambda p: False, status_record_candidate=lambda p: False)
        def qualify(repo, requested):
            calls.append(set(requested))
            if outcome == 'error': raise ValueError('unreviewed edition')
            return set(requested) if outcome == 'valid' else set()
        ns['reviewed_authority_modifications'] = qualify
        ns['readonly_git_diff'] = lambda *a, **k: subprocess.CompletedProcess([], 0, ''.join(s+'\0'+p+'\0' for s,p in changes).encode(), b'')
        return module.check_corpus_currentness(Path('inert-governance-currentness'), 'approved-baseline'), calls

    def test_currentness_admits_only_the_qualified_expected_statuses(self):
        errors, calls = self.currentness([('M', self.OWNER), ('A', self.ADDED)])
        self.assertEqual(errors, []); self.assertEqual(calls, [{self.OWNER, self.ADDED}] * 2)
        for outcome in ('error', 'empty'):
            with self.subTest(outcome=outcome):
                self.assertTrue(self.currentness([('M', self.OWNER), ('A', self.ADDED)], outcome)[0])

    def test_opposite_status_deletion_type_change_and_unrelated_edit_refuse(self):
        for path, statuses in [(self.OWNER, ('A','D','T')), (self.ADDED, ('M','D','T'))]:
            for status in statuses:
                with self.subTest(path=path, status=status):
                    errors, calls = self.currentness([(status, path)])
                    self.assertTrue(errors); self.assertEqual(calls, [])
        self.assertTrue(self.currentness([('A', self.ADDED + '.unreviewed')])[0])
        self.assertTrue(self.currentness([('M', 'scripts/unrelated.py')])[0])
        self.assertTrue(self.currentness([('A', self.ADDED), ('M', self.ADDED)])[0])


class ReviewedGovernanceOriginalPinControls(unittest.TestCase):
    """One original source coordinate, preserving the prior complete pin forms."""
    OWNER = 'scripts/validate_cross_record_semantics.py'
    PIN = ('af71a10aa182f32795e7736c23e0a620073b994a',
           '3b75bca002978c6c47dc5120e9114fc8c601b7f7f6da36bdf061799b899fc1e5',
           45554, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')
    def setUp(self):
        previous = ReviewedAttributionPinControls(); previous.setUp(); self.base = previous.base
        row = dict(repository_path=self.OWNER, source_sha256=self.PIN[1], public_sha256=self.PIN[1],
                   source_bytes=self.PIN[2], public_bytes=self.PIN[2], disposition='REUSE', role='unchanged-role')
        for document in (self.base.original, self.base.prior, self.base.current): document['objects'].append(deepcopy(row))
        self.prior = self.base.pinned(self.base.current, previous.PINS)
        self.current = self.base.pinned(self.prior, {self.OWNER: self.PIN})
    def test_prior_and_new_original_coordinate_forms(self):
        self.assertTrue(self.base.permitted(self.prior))
        self.assertTrue(self.base.permitted(self.current))
    def test_original_identity_role_and_coordinate_mutations_refuse(self):
        for field,value in [('repository_revision','HEAD'),('git_blob','0'*40),('source_sha256','0'*64),
                            ('public_sha256','0'*64),('source_bytes',1),('public_bytes',1),
                            ('disposition','PROJECT'),('role','unreviewed')]:
            with self.subTest(field=field):
                candidate=deepcopy(self.current);next(r for r in candidate['objects'] if r.get('repository_path')==self.OWNER)[field]=value
                self.assertFalse(self.base.permitted(candidate))
        candidate=deepcopy(self.current);next(r for r in candidate['objects'] if r.get('repository_path')==self.OWNER).pop('git_blob')
        self.assertFalse(self.base.permitted(candidate))

class ContinuationProviderAdmissionControls(unittest.TestCase):
    """Exact unchanged providers are not newly authored scientific works."""

    def setUp(self):
        import ast
        import os
        import stat
        import types
        self.tmp = tempfile.TemporaryDirectory(prefix='provider-admission-control-')
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.revision = '7' * 40
        self.map_path = 'docs/provenance/v5-research-continuations/SOURCE_MAP.json'
        self.copy_root = 'experiments/orthemology-v5-continuations/source-store/'
        self.originals, self.current, sources = {}, {}, []
        for i in range(39):
            body = ('-- ordinary provider fixture %02d\n' % i).encode()
            identity = hashlib.sha256(body).hexdigest()
            blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            old = self.copy_root + identity + '.lean'
            new = 'formal/type-theory/Fixture%02d.lean' % i
            self.originals[old] = dict(path=old, kind='blob', mode='100644', git_oid=blob, bytes=len(body))
            self.current[new] = (blob, identity, len(body))
            node = self.repo / new
            node.parent.mkdir(parents=True, exist_ok=True)
            node.write_bytes(body)
            sources.append(dict(id='source-%03d' % i, origin='a' * 64, member='Fixture%02d.lean' % i,
                                original_sha256=identity, original_bytes=len(body), path=new,
                                sha256=identity, bytes=len(body), projection='EXACT', derivation=None))
        self.document = {'sources': [dict(sources[i % 39], id='source-%03d' % i) for i in range(206)]}
        self.state = None
        self.index_calls = {}
        self.native_calls = []
        self.owners = {'baseline': {'commit': self.revision, 'tree': '8' * 40},
                       'source_additions': [], 'baseline_work_population': {'count': 448}}
        self.cross = {'sources': {}, 'works': [{'key': 'original-work', 'role': 'component'}]}
        self.continuation_owners = {}
        self.env = dict(Path=Path, os=os, stat=stat, hashlib=hashlib, re=__import__('re'), json=json,
                        subprocess=types.SimpleNamespace(run=self.native), CONTINUATION_COPY_ROOT=self.copy_root,
                        CONTINUATION_OWNER_PATHS=('unused-evidence', 'unused-readme', self.map_path, 'unused-registry'),
                        CONTINUATION_OWNER_CURRENT={})
        names = {'safe_path', 'reviewed_indexed_modification', 'check_continuation_provider_additions',
                 'corpus_currentness_context'}
        tree = ast.parse(MODULE.read_text())
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<actual-provider-admission-owner>', 'exec'), self.env)
        self.env.update(check_continuation_owner_edition=lambda *a:(self.continuation_owners, []),
                        status_owner_edition=lambda *a:{}, check_fixture_consumer_edition=lambda *a:({}, None, []),
                        check_source_additions=lambda *a:({}, []), check_historical_sources=lambda *a:({}, []),
                        SUCCESSOR_INPUT_REGISTRY='unused-input', PMR007_ROUNDS_PARENT='unused-rounds',
                        MEDIATOR_GUIDE='unused-mediator', SUCCESSOR_CALCULUS_GUIDES=(), ADMIN_GUIDES=(), TYPED_GUIDES=())
        self.sync_map()

    def sync_map(self):
        body = (json.dumps(self.document, sort_keys=True) + '\n').encode()
        node = self.repo / self.map_path
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(body)
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        self.env['CONTINUATION_OWNER_CURRENT'][self.map_path] = (blob, hashlib.sha256(body).hexdigest(), len(body))
        self.continuation_owners[self.map_path] = dict(path=self.map_path, kind='blob', mode='100644', git_oid=blob, bytes=len(body))

    def native(self, args, **kwargs):
        self.native_calls.append(tuple(args))
        self.assertEqual(Path(kwargs['cwd']), self.repo)
        names = args[args.index('--') + 1:]
        if 'ls-tree' in args:
            self.assertEqual(args[args.index('ls-tree') + 2], self.revision)
            if all(n in self.originals for n in names):
                self.assertEqual(set(names), set(self.originals))
                rows = []
                for n in sorted(names):
                    row = self.originals[n]
                    mode = '100755' if self.state == 'history-mode' else row['mode']
                    blob = '0' * 40 if self.state == 'history-blob' else row['git_oid']
                    rows.append((mode + ' blob ' + blob + '\t' + n).encode() + b'\0')
                if self.state == 'history-missing': rows.pop()
                return subprocess.CompletedProcess(args, 1 if self.state == 'history-failure' else 0, b''.join(rows), b'')
            self.assertEqual(len(names), 1)
            self.assertIn(names[0], self.current)
            present = (('100644 blob ' + self.current[names[0]][0] + '\t' + names[0]).encode() + b'\0'
                       if self.state == 'original-destination-present' else b'')
            return subprocess.CompletedProcess(args, 1 if self.state == 'absence-query-failure' else 0, present, b'')
        self.assertIn('ls-files', args)
        self.assertEqual(len(names), 1)
        name = names[0]
        self.assertIn(name, self.current)
        self.index_calls[name] = self.index_calls.get(name, 0) + 1
        blob = self.current[name][0]
        if self.state == 'index' or self.state == 'late-index' and self.index_calls[name] == 2:
            blob = '0' * 40
        stage = '1' if self.state == 'conflict' else '0'
        if self.state == 'late-body' and self.index_calls[name] == 2:
            (self.repo / name).write_bytes(b'changed after read\n')
        body = ('100644 ' + blob + ' ' + stage + '\t' + name).encode() + b'\0'
        return subprocess.CompletedProcess(args, 0, b'' if self.state == 'missing-index' else body, b'')

    def admission(self):
        self.assertIn('check_continuation_provider_additions', self.env)
        return self.env['check_continuation_provider_additions'](
            self.repo, self.originals, self.continuation_owners, self.owners['baseline']['commit'])

    def test_current_context_admits_exact_original_provider_copies(self):
        before = deepcopy((self.owners, self.cross, self.originals))
        contexts, errors = self.env['corpus_currentness_context'](
            self.repo, self.originals, self.owners, self.cross)
        self.assertEqual(errors, [])
        self.assertEqual(set(contexts[0]), set(self.current))
        self.assertEqual((self.owners, self.cross, self.originals), before)
        self.assertEqual(self.owners['baseline_work_population']['count'], 448)

    def test_exact_complete_provider_set_has_no_partial_admission(self):
        admitted, errors = self.admission()
        self.assertEqual(errors, [])
        self.assertEqual(set(admitted), set(self.current))
        for name, row in admitted.items():
            self.assertEqual((row['kind'], row['mode'], row['git_oid'], row['bytes']),
                             ('blob', '100644', self.current[name][0], self.current[name][2]))

    def test_original_owner_context_does_not_admit_new_providers(self):
        self.continuation_owners.clear()
        self.assertEqual(self.admission(), ({}, []))
        self.assertEqual(self.native_calls, [])

    def test_map_pin_and_original_census_identity_are_required(self):
        first = next(iter(self.originals))
        for change in ('map-bytes', 'census-blob', 'census-mode', 'census-size', 'destination-in-census'):
            with self.subTest(change=change):
                original = deepcopy(self.originals)
                if change == 'map-bytes': (self.repo / self.map_path).write_bytes(b'{}')
                elif change == 'destination-in-census': self.originals[next(iter(self.current))] = dict(self.originals[first])
                else: self.originals[first][{'census-blob':'git_oid','census-mode':'mode','census-size':'bytes'}[change]] = {'census-blob':'0'*40,'census-mode':'100755','census-size':1}[change]
                admitted, errors = self.admission()
                self.assertEqual(admitted, {}); self.assertTrue(errors)
                self.originals = original
                self.sync_map()

    def test_original_queries_cannot_fail_or_mask_missing_or_changed_rows(self):
        for state in ('history-failure', 'history-mode', 'history-blob', 'history-missing',
                      'original-destination-present', 'absence-query-failure'):
            with self.subTest(state=state):
                self.state = state
                admitted, errors = self.admission()
                self.assertEqual(admitted, {}); self.assertTrue(errors)

    def test_current_index_and_late_changes_are_refused(self):
        for state in ('index', 'missing-index', 'conflict', 'late-index', 'late-body'):
            with self.subTest(state=state):
                self.state = state; self.index_calls = {}
                originals = {n:(self.repo/n).read_bytes() for n in self.current}
                admitted, errors = self.admission()
                self.assertEqual(admitted, {}); self.assertTrue(errors)
                for name, body in originals.items(): (self.repo/name).write_bytes(body)

    def test_missing_corrupt_executable_linked_current_provider_is_refused(self):
        import os
        name = next(iter(self.current)); node = self.repo / name; body = node.read_bytes()
        for state in ('missing', 'corrupt', 'executable', 'symlink', 'hardlink'):
            with self.subTest(state=state):
                peer = self.repo / ('peer-' + state)
                if state == 'missing': node.unlink()
                elif state == 'corrupt': node.write_bytes(b'changed\n')
                elif state == 'executable': node.chmod(0o755)
                else:
                    peer.write_bytes(body); node.unlink()
                    if state == 'symlink': node.symlink_to(peer)
                    else: os.link(peer, node)
                admitted, errors = self.admission()
                self.assertEqual(admitted, {}); self.assertTrue(errors)
                if node.exists() or node.is_symlink(): node.unlink()
                node.write_bytes(body)

    def test_complete_source_ids_provenance_and_exact_projection_are_required(self):
        original = deepcopy(self.document)
        for change in ('missing-row', 'duplicate-id', 'projection', 'derivation', 'original-sha', 'original-size', 'bool-size', 'outside-provider'):
            with self.subTest(change=change):
                row = self.document['sources'][0]
                if change == 'missing-row': self.document['sources'].pop()
                elif change == 'duplicate-id': row['id'] = self.document['sources'][1]['id']
                else:
                    field, value = {'projection':('projection','PROJECT'), 'derivation':('derivation','changed'),
                                    'original-sha':('original_sha256','f'*64), 'original-size':('original_bytes',1),
                                    'bool-size':('bytes',True), 'outside-provider':('path','formal/unreviewed/Fixture00.lean')}[change]
                    row[field] = value
                self.sync_map()
                admitted, errors = self.admission()
                self.assertEqual(admitted, {}); self.assertTrue(errors)
                self.document = deepcopy(original); self.sync_map()

    def test_unrelated_ordinary_file_is_not_an_admitted_provider(self):
        other = 'formal/type-theory/Unreviewed.lean'
        (self.repo / other).write_bytes(b'-- unreviewed\n')
        admitted, errors = self.admission()
        self.assertEqual(errors, [])
        self.assertNotIn(other, admitted)
        self.assertEqual(len(admitted), 39)


class ReviewedFrontierTestEditions(unittest.TestCase):
    """The two exact live-control editions use the existing ordinary-file guard."""
    CONTRACTS = {'tests/test_pmr007_deep_bk_public_snapshot.py': ('tests/test_pmr007_deep_bk_public_snapshot.py',
                                                  '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                                  ('249a89266da20b19a84131e7b27a0814aaadd54f',
                                                   'fd6dbafefb2eb6b24119c0d94634251df621d30122c246f690cce146ed5c9ce5',
                                                   12480),
                                                  ('338a965b1d3464dcc71571057cb3749e6db4d2f6',
                                                   '393836cabe9e060109fa747c907f8d80c4df23cd5c739eb2efe56879e71df900',
                                                   18014)),
 'tests/test_pmr007_deep_bv_semantic_reissue.py': ('tests/test_pmr007_deep_bv_semantic_reissue.py',
                                                   '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                                   ('b932096c9490c9e31bfc3f596f2990a4dfd1e8ba',
                                                    '334034b9019f5f27ca2fcac36e568982bda3d7d6e7c2daca40e565d16792a37f',
                                                    9724),
                                                   ('c58ba28e58995bba573184dac867ef38673abfc1',
                                                    '5ee60a37fb6fa5a18f5bc78a47c1d342a7dee7b3ea4a0862473782ca114e156f',
                                                    14419))}
    PATHS = tuple(CONTRACTS)
    fixture = ReviewedAuthorityControls.fixture
    currentness = ReviewedAuthorityControls.currentness
    test_exact_two_owner_editions_and_requested_subset = ReviewedAuthorityControls.test_exact_three_owner_editions_and_requested_subset
    test_wrong_missing_or_nonordinary_current_owner_refuses = ReviewedAuthorityControls.test_wrong_missing_or_nonordinary_current_owner_refuses
    test_history_index_and_native_failures_refuse = ReviewedAuthorityControls.test_history_index_and_native_failures_refuse
    test_currentness_admits_only_requested_qualified_modifications = ReviewedAuthorityControls.test_currentness_admits_only_requested_qualified_modifications
    test_deletion_type_change_addition_and_unrelated_edit_refuse = ReviewedAuthorityControls.test_deletion_type_change_addition_and_unrelated_edit_refuse
    test_unchanged_positive_and_extra_path_refusal = ReviewedAuthorityControls.test_unchanged_positive_and_extra_path_refusal

    def test_only_exact_reviewed_frontier_test_contracts_are_admitted(self):
        import ast
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        table = next(n for n in tree.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'REVIEWED_AUTHORITY_EDITS'
                             for t in n.targets))
        contracts = ast.literal_eval(table.value)
        for path, expected in self.CONTRACTS.items():
            with self.subTest(path=path):
                self.assertEqual(contracts.get(path), expected)
        self.assertNotIn('tests/', contracts)


class ReviewedFrontierOriginalPinControls(unittest.TestCase):
    """Preserve both original live-test bytes as exact historical REUSE objects."""
    PINS = {'tests/test_pmr007_deep_bk_public_snapshot.py': ('249a89266da20b19a84131e7b27a0814aaadd54f',
                                                  'fd6dbafefb2eb6b24119c0d94634251df621d30122c246f690cce146ed5c9ce5',
                                                  12480,
                                                  '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
 'tests/test_pmr007_deep_bv_semantic_reissue.py': ('b932096c9490c9e31bfc3f596f2990a4dfd1e8ba',
                                                   '334034b9019f5f27ca2fcac36e568982bda3d7d6e7c2daca40e565d16792a37f',
                                                   9724,
                                                   '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}

    def setUp(self):
        previous = ReviewedGovernanceOriginalPinControls()
        previous.setUp()
        self.base = previous.base
        self.prior = previous.current
        for path, (_, identity, size, _) in self.PINS.items():
            row = dict(repository_path=path, source_sha256=identity, public_sha256=identity,
                       source_bytes=size, public_bytes=size, disposition='REUSE', role='unchanged-role')
            for document in (self.base.original, self.prior):
                document['objects'].append(deepcopy(row))
        self.current = self.base.pinned(self.prior, self.PINS)

    def test_prior_and_complete_two_test_coordinates_are_accepted(self):
        self.assertTrue(self.base.permitted(self.prior))
        self.assertTrue(self.base.permitted(self.current))

    def test_partial_pair_and_each_identity_coordinate_or_role_change_refuse(self):
        for path in self.PINS:
            for field, value in (('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                                 ('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                                 ('source_bytes', 1), ('public_bytes', 1),
                                 ('disposition', 'PROJECT'), ('role', 'unreviewed')):
                with self.subTest(path=path, field=field):
                    changed = deepcopy(self.current)
                    next(r for r in changed['objects'] if r.get('repository_path') == path)[field] = value
                    self.assertFalse(self.base.permitted(changed))
            changed = deepcopy(self.current)
            row = next(r for r in changed['objects'] if r.get('repository_path') == path)
            row.pop('repository_revision')
            row.pop('git_blob')
            self.assertFalse(self.base.permitted(changed))

    def test_missing_duplicate_reordered_and_unrelated_objects_refuse(self):
        for kind in ('missing', 'duplicate', 'reordered', 'unrelated', 'metadata'):
            with self.subTest(kind=kind):
                changed = deepcopy(self.current)
                if kind == 'missing':
                    changed['objects'].pop()
                elif kind == 'duplicate':
                    changed['objects'].append(deepcopy(changed['objects'][-1]))
                elif kind == 'reordered':
                    changed['objects'].reverse()
                elif kind == 'unrelated':
                    changed['objects'][0]['role'] = 'unreviewed'
                else:
                    changed['schema'] = 'unreviewed'
                self.assertFalse(self.base.permitted(changed))


class ReviewedCentralIntakeTestEdition(unittest.TestCase):
    """The exact central-intake live-control edition use the existing ordinary-file guard."""
    CONTRACTS = {'tests/test_ar8r_six_lane_v14_intake.py': ('tests/test_ar8r_six_lane_v14_intake.py',
                                            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                            ('c0b79431bafc486c71a083b3b8afdec0db431236',
                                             '548d4358ca89755bbfd29b2df9a4b6b2b6ca36541cc5994e523198c40ddea26c',
                                             11625),
                                            ('9c5c787c71490d4e4f7807df028e02ba510a0dc5',
                                             '8fbf27f3b400015c472a16d4a23ff63ee8ef050409f4f875564b1cda2ef0e6b4',
                                             33249))}
    PATHS = tuple(CONTRACTS)
    fixture = ReviewedAuthorityControls.fixture
    currentness = ReviewedAuthorityControls.currentness
    def test_exact_owner_edition_and_requested_subset(self):
        module, repo, calls = self.fixture()
        self.assertEqual(module.reviewed_authority_modifications(repo, set(self.PATHS)), set(self.PATHS))
        self.assertEqual(module.reviewed_authority_modifications(repo, set()), set())
    test_wrong_missing_or_nonordinary_current_owner_refuses = ReviewedAuthorityControls.test_wrong_missing_or_nonordinary_current_owner_refuses
    test_history_index_and_native_failures_refuse = ReviewedAuthorityControls.test_history_index_and_native_failures_refuse
    test_currentness_admits_only_requested_qualified_modifications = ReviewedAuthorityControls.test_currentness_admits_only_requested_qualified_modifications
    test_deletion_type_change_addition_and_unrelated_edit_refuse = ReviewedAuthorityControls.test_deletion_type_change_addition_and_unrelated_edit_refuse
    test_unchanged_positive_and_extra_path_refusal = ReviewedAuthorityControls.test_unchanged_positive_and_extra_path_refusal

    def test_only_exact_reviewed_intake_test_contract_is_admitted(self):
        import ast
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        table = next(n for n in tree.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'REVIEWED_AUTHORITY_EDITS'
                             for t in n.targets))
        contracts = ast.literal_eval(table.value)
        for path, expected in self.CONTRACTS.items():
            with self.subTest(path=path):
                self.assertEqual(contracts.get(path), expected)
        self.assertNotIn('tests/', contracts)


class ReviewedCentralIntakeOriginalPinControls(unittest.TestCase):
    """Preserve the original intake live-test bytes as exact historical REUSE objects."""
    PINS = {'tests/test_ar8r_six_lane_v14_intake.py': ('c0b79431bafc486c71a083b3b8afdec0db431236',
                                            '548d4358ca89755bbfd29b2df9a4b6b2b6ca36541cc5994e523198c40ddea26c',
                                            11625,
                                            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}

    def setUp(self):
        previous = ReviewedFrontierOriginalPinControls()
        previous.setUp()
        self.base = previous.base
        self.prior = previous.current
        for path, (_, identity, size, _) in self.PINS.items():
            row = dict(repository_path=path, source_sha256=identity, public_sha256=identity,
                       source_bytes=size, public_bytes=size, disposition='REUSE', role='unchanged-role')
            for document in (self.base.original, self.prior):
                document['objects'].append(deepcopy(row))
        self.current = self.base.pinned(self.prior, self.PINS)

    def test_prior_and_complete_intake_coordinate_are_accepted(self):
        self.assertTrue(self.base.permitted(self.prior))
        self.assertTrue(self.base.permitted(self.current))

    def test_partial_pin_and_each_identity_coordinate_or_role_change_refuse(self):
        for path in self.PINS:
            for field, value in (('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                                 ('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                                 ('source_bytes', 1), ('public_bytes', 1),
                                 ('disposition', 'PROJECT'), ('role', 'unreviewed')):
                with self.subTest(path=path, field=field):
                    changed = deepcopy(self.current)
                    next(r for r in changed['objects'] if r.get('repository_path') == path)[field] = value
                    self.assertFalse(self.base.permitted(changed))
            for field in ('repository_revision', 'git_blob'):
                with self.subTest(path=path, missing=field):
                    changed = deepcopy(self.current)
                    row = next(r for r in changed['objects'] if r.get('repository_path') == path)
                    row.pop(field)
                    self.assertFalse(self.base.permitted(changed))

    def test_missing_duplicate_reordered_and_unrelated_objects_refuse(self):
        for kind in ('missing', 'duplicate', 'reordered', 'unrelated', 'metadata'):
            with self.subTest(kind=kind):
                changed = deepcopy(self.current)
                if kind == 'missing':
                    changed['objects'].pop()
                elif kind == 'duplicate':
                    changed['objects'].append(deepcopy(changed['objects'][-1]))
                elif kind == 'reordered':
                    changed['objects'].reverse()
                elif kind == 'unrelated':
                    changed['objects'][0]['role'] = 'unreviewed'
                else:
                    changed['schema'] = 'unreviewed'
                self.assertFalse(self.base.permitted(changed))



class ReviewedCodexTestEdition(unittest.TestCase):
    """The exact Codex live-control edition use the existing ordinary-file guard."""
    CONTRACTS = {'tests/test_ar8r_codex_corpus_synthesis_v14.py': ('tests/test_ar8r_codex_corpus_synthesis_v14.py',
                                                       '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                                       ('b5aa03c18c2e9df149f460955184bec83a6b46a0',
                                                        '7801ae286ca0b8c8c4c1bce7e73aedc9dfb914474d66ea58c029c756ea1ef67e',
                                                        46305),
                                                       ('851669b52eabe0a9262c8f7a5ca9cc2cd57971a8',
                                                        'f535c52b5d47ef2fe21b8663d52505762dac7e7b8124c1b3cc5afb44f9c9f8d6',
                                                        35766))}
    PATHS = tuple(CONTRACTS)
    fixture = ReviewedAuthorityControls.fixture
    currentness = ReviewedAuthorityControls.currentness
    def test_exact_owner_edition_and_requested_subset(self):
        module, repo, calls = self.fixture()
        self.assertEqual(module.reviewed_authority_modifications(repo, set(self.PATHS)), set(self.PATHS))
        self.assertEqual(module.reviewed_authority_modifications(repo, set()), set())
    test_wrong_missing_or_nonordinary_current_owner_refuses = ReviewedAuthorityControls.test_wrong_missing_or_nonordinary_current_owner_refuses
    test_history_index_and_native_failures_refuse = ReviewedAuthorityControls.test_history_index_and_native_failures_refuse
    test_currentness_admits_only_requested_qualified_modifications = ReviewedAuthorityControls.test_currentness_admits_only_requested_qualified_modifications
    test_deletion_type_change_addition_and_unrelated_edit_refuse = ReviewedAuthorityControls.test_deletion_type_change_addition_and_unrelated_edit_refuse
    test_unchanged_positive_and_extra_path_refusal = ReviewedAuthorityControls.test_unchanged_positive_and_extra_path_refusal

    def test_only_exact_reviewed_codex_test_contract_is_admitted(self):
        import ast
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        table = next(n for n in tree.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'REVIEWED_AUTHORITY_EDITS'
                             for t in n.targets))
        contracts = ast.literal_eval(table.value)
        for path, expected in self.CONTRACTS.items():
            with self.subTest(path=path):
                self.assertEqual(contracts.get(path), expected)
        self.assertNotIn('tests/', contracts)


class ReviewedCodexOriginalPinControls(unittest.TestCase):
    """Preserve the original codex live-test bytes as exact historical REUSE objects."""
    PINS = {'tests/test_ar8r_codex_corpus_synthesis_v14.py': ('b5aa03c18c2e9df149f460955184bec83a6b46a0',
                                                       '7801ae286ca0b8c8c4c1bce7e73aedc9dfb914474d66ea58c029c756ea1ef67e',
                                                       46305,
                                                       '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}

    def setUp(self):
        previous = ReviewedCentralIntakeOriginalPinControls()
        previous.setUp()
        self.base = previous.base
        self.prior = previous.current
        for path, (_, identity, size, _) in self.PINS.items():
            row = dict(repository_path=path, source_sha256=identity, public_sha256=identity,
                       source_bytes=size, public_bytes=size, disposition='REUSE', role='unchanged-role')
            for document in (self.base.original, self.prior):
                document['objects'].append(deepcopy(row))
        self.current = self.base.pinned(self.prior, self.PINS)

    def test_prior_and_complete_codex_coordinate_are_accepted(self):
        self.assertTrue(self.base.permitted(self.prior))
        self.assertTrue(self.base.permitted(self.current))

    def test_partial_pin_and_each_identity_coordinate_or_role_change_refuse(self):
        for path in self.PINS:
            for field, value in (('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                                 ('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                                 ('source_bytes', 1), ('public_bytes', 1),
                                 ('disposition', 'PROJECT'), ('role', 'unreviewed')):
                with self.subTest(path=path, field=field):
                    changed = deepcopy(self.current)
                    next(r for r in changed['objects'] if r.get('repository_path') == path)[field] = value
                    self.assertFalse(self.base.permitted(changed))
            for field in ('repository_revision', 'git_blob'):
                with self.subTest(path=path, missing=field):
                    changed = deepcopy(self.current)
                    row = next(r for r in changed['objects'] if r.get('repository_path') == path)
                    row.pop(field)
                    self.assertFalse(self.base.permitted(changed))

    def test_missing_duplicate_reordered_and_unrelated_objects_refuse(self):
        for kind in ('missing', 'duplicate', 'reordered', 'unrelated', 'metadata'):
            with self.subTest(kind=kind):
                changed = deepcopy(self.current)
                if kind == 'missing':
                    changed['objects'].pop()
                elif kind == 'duplicate':
                    changed['objects'].append(deepcopy(changed['objects'][-1]))
                elif kind == 'reordered':
                    changed['objects'].reverse()
                elif kind == 'unrelated':
                    changed['objects'][0]['role'] = 'unreviewed'
                else:
                    changed['schema'] = 'unreviewed'
                self.assertFalse(self.base.permitted(changed))



class CertificateProviderAdditionControls(unittest.TestCase):
    """Eight exact ordinary destinations; no generic formal-source or deletion waiver."""
    CONTRACTS = {'formal/certificate-frontier/CertificateFrontier.lean': ('formal/certificate-frontier/CertificateFrontier.lean', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('208cf6e6250c6ff50d0b03575a6ae7926b70d1ed', '5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0', 12278)), 'formal/certificate-frontier/Controls.lean': ('formal/certificate-frontier/Controls.lean', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('1c6b8900e600c63e30f0aa83f49f7db8211a7cdf', '7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132', 2410)), 'formal/certificate-frontier/ScopeChecks.lean': ('formal/certificate-frontier/ScopeChecks.lean', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('2efba39e95c7b0cf38b246654d64f16e099f8e31', '6218ff6fa7b6e5b304859c2f4ad3d512118f1a3c9b68ec7e446d6cc1cd2d78a6', 1345)), 'formal/certificate-frontier/mutations/CostBlind.lean': ('formal/certificate-frontier/mutations/CostBlind.lean', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('01cef9257fc16b90c16ae14ca9e65aef41cdd787', 'c05bf6d3207aeeaa7dddc222092c73d44f73ecc5eab5c8d465485a9a540d5776', 227)), 'formal/certificate-frontier/mutations/CurrentCost.lean': ('formal/certificate-frontier/mutations/CurrentCost.lean', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('9ad7316c3906603cd262cb781736078b18cd14a5', '876039d480a1415531f1f099679c5094327caf35c7933a36550e09692de1e83d', 249)), 'formal/certificate-frontier/mutations/InfinitePrice.lean': ('formal/certificate-frontier/mutations/InfinitePrice.lean', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('ffa13821c157cd943b1bcb5f6aa514c917f198b1', '0b2d8b2584f48d343d753a373161e28f93c397982ce9ab4c098b8daf16db31fe', 293)), 'formal/certificate-frontier/run-primary.sh': ('formal/certificate-frontier/run-primary.sh', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('fb83caac96791a44fcfb3001cae2e4be03a91b9c', '9a3980fefd48afc8ba9dd2bec1741110c0ab191a088e52fc3e07500c0c88fd95', 3589)), 'formal/certificate-frontier/run-scope-review.sh': ('formal/certificate-frontier/run-scope-review.sh', '0784acddd4770f1190f758f264ba52b2b110bd27', None, ('8402995d37601853f80ddd7f989cc4fe4c600950', '95fb6990e711f319f5bd15e610269bb8bfd462f3f9a718b06324c2ed381495cf', 3298))}
    OWNER = ReviewedGovernanceEditionControls.OWNER

    def contracts(self):
        import ast
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        table = next(n for n in tree.body if isinstance(n, ast.Assign) and
                     any(isinstance(t, ast.Name) and t.id == 'REVIEWED_AUTHORITY_EDITS' for t in n.targets))
        return ast.literal_eval(table.value)

    def test_exact_eight_contracts_are_explicit_not_a_prefix_allowance(self):
        actual = self.contracts()
        self.assertEqual(len(self.CONTRACTS), 8)
        for path, expected in self.CONTRACTS.items():
            with self.subTest(path=path): self.assertEqual(actual.get(path), expected)
        self.assertNotIn('formal/', actual)
        self.assertNotIn('formal/certificate-frontier/', actual)

    def gate(self, changes, qualification='valid'):
        import ast, types
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'check_corpus_currentness')
        module = types.ModuleType('certificate_provider_currentness')
        ns = module.__dict__
        ns.update(Path=Path, subprocess=subprocess, REFACTOR_EDIT_PATHS=set(),
                  PMR007_DEEP_PREFIX='unused-deep', PMR007_ROUNDS_PREFIX='unused-rounds',
                  PMR007_ROUNDS_FORMALIZATION='unused-formal', CONTINUATION_COPY_ROOT='unused-copy/',
                  SUCCESSOR_INPUT_REGISTRY='unused-input', SUCCESSOR_CALCULUS_MAP='unused-map',
                  MEDIATOR_GUIDE='unused-guide', REVIEWED_AUTHORITY_EDITS=self.contracts())
        for name in ('CHECKPOINT_PUBLIC_COPY_PATHS', 'CHECKPOINT_COPY_PATHS','CHECKPOINT_RECORD_COPY_PATHS','CHECKPOINT_PACKAGE_COPY_PATHS',
                     'FORMAL_COPY_PATHS','FORMAL_PROVIDER_PATHS','CHECKPOINT_CODE_COPY_PATHS','DIGEST_RECORD_PATHS','ADMISSION_RECORD_PATHS','SUCCESSOR_INPUT_PATHS',
                     'GENERATED_FIXTURE_PATHS','ADMIN_RECORD_PATHS','CONTINUATION_OWNER_PATHS','STATUS_RECORD_OWNERS',
                     'FIXTURE_CONSUMER_ORIGINAL','HISTORICAL_PROSE','ADMIN_GUIDES','TYPED_GUIDES','SUCCESSOR_CALCULUS_GUIDES'):
            ns[name] = set()
        for name in ('pmr007_deep_duplicate_paths','pmr007_rounds_duplicate_paths','checkpoint_public_duplicate_paths', 'checkpoint_duplicate_paths',
                     'checkpoint_record_duplicate_paths','checkpoint_package_duplicate_paths','formal_duplicate_paths','formal_provider_absences',
                     'checkpoint_code_duplicate_paths','digest_record_absences'):
            ns[name] = lambda *args: set()
        ns.update(binding_record_candidate=lambda p: False, status_record_candidate=lambda p: False)
        calls = []
        def qualify(repo, paths):
            calls.append(set(paths))
            if qualification == 'error': raise ValueError('exact provider receiving failed')
            return set(paths) if qualification == 'valid' else set()
        ns['reviewed_authority_modifications'] = qualify
        ns['readonly_git_diff'] = lambda *a, **k: subprocess.CompletedProcess([], 0,
            ''.join(status+'\0'+path+'\0' for status, path in changes).encode(), b'')
        exec(compile(ast.Module(body=[function],type_ignores=[]),'actual-certificate-currentness','exec'), ns)
        return module.check_corpus_currentness(Path('inert-currentness-root'),'original-baseline'), calls

    def test_all_eight_additions_require_successful_exact_receiving(self):
        expected = set(self.CONTRACTS)
        errors, calls = self.gate([('A', path) for path in expected])
        self.assertEqual(errors, [])
        self.assertEqual(calls, [expected, expected])
        for state in ('error', 'empty'):
            self.assertTrue(self.gate([('A', path) for path in expected], state)[0])

    def test_modification_type_deletion_and_unrelated_addition_refuse(self):
        for path in self.CONTRACTS:
            for status in ('M', 'D', 'T'):
                with self.subTest(path=path, status=status):
                    errors, calls = self.gate([(status, path)])
                    self.assertTrue(errors); self.assertEqual(calls, [])
        self.assertTrue(self.gate([('A', 'formal/certificate-frontier/Unreviewed.lean')])[0])
        self.assertEqual(self.gate([]), ([], []))

    def _absent_fixture(self, path, state='valid'):
        self.ADDED = path
        return ReviewedGovernanceEditionControls.fixture(self, state, path)

    def test_each_destination_requires_successful_empty_original_tree(self):
        for path in self.CONTRACTS:
            module, repo, calls = self._absent_fixture(path)
            self.assertEqual(module.reviewed_authority_modifications(repo, {path}), {path})
            self.assertFalse(any('cat-file' in command for command in calls))
            for state in ('preexisting', 'empty-predecessor', 'failed-history-query'):
                with self.subTest(path=path, state=state):
                    module, repo, _ = self._absent_fixture(path, state)
                    with self.assertRaises(ValueError): module.reviewed_authority_modifications(repo, {path})

    def test_each_destination_requires_current_regular_identity(self):
        for path in self.CONTRACTS:
            for state in ('wrong-body', 'missing', 'executable', 'symlink', 'hardlink'):
                with self.subTest(path=path, state=state):
                    module, repo, _ = self._absent_fixture(path, state)
                    with self.assertRaises((ValueError, OSError)): module.reviewed_authority_modifications(repo, {path})

    def test_each_destination_requires_index_and_TOCTOU_stability(self):
        for path in self.CONTRACTS:
            for state in ('index-conflict', 'late-index', 'late-body'):
                with self.subTest(path=path, state=state):
                    module, repo, _ = self._absent_fixture(path, state)
                    with self.assertRaises(ValueError): module.reviewed_authority_modifications(repo, {path})




class CertificateProviderAbsenceControls(unittest.TestCase):
    """Six authenticated old providers only; current owners are never deletion allowances."""
    EXPECTED = ('research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/CertificateFrontier.lean',
        'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/Controls.lean',
        'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/independent-review/ScopeChecks.lean',
        'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CostBlind.lean',
        'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/CurrentCost.lean',
        'research/t20-live-20261009/supplement/S01/warranted-discrimination-kernel-20261009/mutations/InfinitePrice.lean')

    def gate(self, changes, qualified=None, error=False, population=None, receiver=None, repo=None):
        import ast, types
        function = next(n for n in ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes()).body
                        if isinstance(n, ast.FunctionDef) and n.name == 'check_corpus_currentness')
        module = types.ModuleType('exact_formal_provider_absence_gate')
        ns = module.__dict__
        ns.update(Path=Path, subprocess=subprocess, REFACTOR_EDIT_PATHS=set(), REVIEWED_AUTHORITY_EDITS={},
            PMR007_DEEP_PREFIX='unused-deep', PMR007_ROUNDS_PREFIX='unused-rounds',
            PMR007_ROUNDS_FORMALIZATION='unused-formal', CONTINUATION_COPY_ROOT='unused-copy/',
            SUCCESSOR_INPUT_REGISTRY='unused-input', SUCCESSOR_CALCULUS_MAP='unused-map', MEDIATOR_GUIDE='unused-guide')
        for name in ('CHECKPOINT_PUBLIC_COPY_PATHS', 'CHECKPOINT_COPY_PATHS','CHECKPOINT_RECORD_COPY_PATHS','CHECKPOINT_PACKAGE_COPY_PATHS',
            'FORMAL_COPY_PATHS','CHECKPOINT_CODE_COPY_PATHS','DIGEST_RECORD_PATHS','ADMISSION_RECORD_PATHS','SUCCESSOR_INPUT_PATHS',
            'GENERATED_FIXTURE_PATHS','ADMIN_RECORD_PATHS','CONTINUATION_OWNER_PATHS','STATUS_RECORD_OWNERS',
            'FIXTURE_CONSUMER_ORIGINAL','HISTORICAL_PROSE','ADMIN_GUIDES','TYPED_GUIDES','SUCCESSOR_CALCULUS_GUIDES'):
            ns[name] = set()
        for name in ('pmr007_deep_duplicate_paths','pmr007_rounds_duplicate_paths','checkpoint_public_duplicate_paths', 'checkpoint_duplicate_paths',
            'checkpoint_record_duplicate_paths','checkpoint_package_duplicate_paths','formal_duplicate_paths',
            'checkpoint_code_duplicate_paths','digest_record_absences'):
            ns[name] = lambda *args: set()
        ns['FORMAL_PROVIDER_PATHS'] = set(self.EXPECTED) if population is None else population
        calls = []
        def qualify(repo):
            calls.append(repo)
            if receiver is not None: return receiver(repo)
            if error: raise ValueError('exact native provider receiving failed')
            return set(self.EXPECTED) if qualified is None else qualified
        ns.update(formal_provider_absences=qualify, binding_record_candidate=lambda p: False,
                  status_record_candidate=lambda p: False,
                  readonly_git_diff=lambda *a, **k: subprocess.CompletedProcess([],0,
                    ''.join(status+'\0'+path+'\0' for status,path in changes).encode(),b''))
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'actual-six-provider-currentness', 'exec'), ns)
        return module.check_corpus_currentness(Path('inert-exact-root') if repo is None else repo, 'original-baseline'), calls

    def test_exact_six_absences_require_current_identity(self):
        errors, calls = self.gate([('D', path) for path in self.EXPECTED])
        self.assertEqual(errors, [])
        self.assertEqual(len(calls), 1)

    def test_missing_and_failed_qualification_refuse(self):
        for path in self.EXPECTED:
            with self.subTest(path=path):
                self.assertTrue(self.gate([('D', path)], qualified=set())[0])
                self.assertTrue(self.gate([('D', path)], error=True)[0])
                self.assertTrue(self.gate([('D', path)], qualified=set(self.EXPECTED)-{path})[0])

    def test_modifications_additions_and_type_changes_still_refuse(self):
        for path in self.EXPECTED:
            for status in ('M','A','T'):
                with self.subTest(path=path,status=status):
                    errors,calls=self.gate([(status,path)])
                    self.assertTrue(errors);self.assertEqual(calls,[])

    def test_current_destinations_and_unrelated_old_paths_refuse(self):
        for path in ('formal/certificate-frontier/CertificateFrontier.lean',
                     'formal/certificate-frontier/run-primary.sh', self.EXPECTED[0]+'.unreviewed'):
            for status in ('D','M','A','T'):
                with self.subTest(path=path,status=status):
                    errors,calls=self.gate([(status,path)])
                    self.assertTrue(errors);self.assertEqual(calls,[])

    def test_empty_or_omitted_dispatch_population_fails_closed(self):
        self.assertTrue(self.gate([('D',self.EXPECTED[0])],population=set())[0])
        self.assertEqual(self.gate([]),([],[]))
        self.assertTrue(self.gate([('D',self.EXPECTED[0]),('M','unrelated.md')])[0])


from unittest import mock as frontier_mock


def _frontier_history_test_reader():
    """Isolate exact reader functions with inert unrelated native predicates."""
    import ast, types, os, stat
    module = types.ModuleType('frontier_history_live_controls')
    ns = module.__dict__
    root = 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk'
    ns.update(Path=Path, hashlib=hashlib, subprocess=subprocess, os=os, stat=stat,
        PMR007_DEEP_PREFIX=root, PMR007_ROUNDS_PREFIX='unused-rounds',
        PMR007_ROUNDS_FORMALIZATION='unused-formalization', CONTINUATION_COPY_ROOT='unused-continuation',
        SUCCESSOR_INPUT_REGISTRY='unused-registry', SUCCESSOR_CALCULUS_MAP='unused-calculus',
        MEDIATOR_GUIDE='unused-guide', REVIEWED_AUTHORITY_EDITS={})
    for name in ('REFACTOR_EDIT_PATHS HISTORICAL_PROSE CHECKPOINT_PUBLIC_COPY_PATHS CHECKPOINT_COPY_PATHS CHECKPOINT_RECORD_COPY_PATHS '
                 'CHECKPOINT_PACKAGE_COPY_PATHS FORMAL_COPY_PATHS FORMAL_PROVIDER_PATHS CHECKPOINT_CODE_COPY_PATHS '
                 'DIGEST_RECORD_PATHS ADMISSION_RECORD_PATHS SUCCESSOR_INPUT_PATHS GENERATED_FIXTURE_PATHS ADMIN_RECORD_PATHS ADMIN_GUIDES '
                 'CONTINUATION_OWNER_PATHS STATUS_RECORD_OWNERS FIXTURE_CONSUMER_ORIGINAL TYPED_GUIDES SUCCESSOR_CALCULUS_GUIDES').split():
        ns[name]=set()
    for name in ('pmr007_deep_duplicate_paths pmr007_rounds_duplicate_paths checkpoint_public_duplicate_paths checkpoint_duplicate_paths '
                 'checkpoint_record_duplicate_paths checkpoint_package_duplicate_paths formal_duplicate_paths '
                 'formal_provider_absences checkpoint_code_duplicate_paths digest_record_absences').split():
        ns[name]=lambda *args:set()
    ns['binding_record_candidate']=lambda path:False
    ns['status_record_candidate']=lambda path:False
    ns['readonly_git_diff']=lambda *args:None
    tree=ast.parse((ROOT/'scripts/check_reader_pilot.py').read_bytes())
    names={'_frontier_record_file_state','check_frontier_record_absences','check_corpus_currentness'}
    selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id.startswith('FRONTIER_HISTORY_'):
                    ns[target.id]=ast.literal_eval(node.value)
    exec(compile(ast.Module(body=selected,type_ignores=[]),'actual-reader-frontier-functions','exec'),ns)
    return module


class FrontierHistoryAbsenceTests(unittest.TestCase):
    """Exact synthetic native responses; no original Git/history execution."""
    def setUp(self):
        self.reader = _frontier_history_test_reader()
        import tempfile
        import types
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.paths = ['docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/retired-%02d.yaml' % i for i in range(16)]
        self.bodies = {p: ('original %s\n' % p).encode() for p in self.paths}
        def identity(b):
            return (hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(), hashlib.sha256(b).hexdigest(), len(b))
        self.identity = identity
        self.records = {p: identity(b) for p,b in self.bodies.items()}
        self.support = {'current-a':'science/a.md', 'current-b':'science/b.md', 'current-c':'science/c.md'}
        self.additions = {}
        self.cross = {'sources': {}, 'reader_journeys': []}
        for key,path in dict(self.support, **{'scientific-consolidation-review':'docs/review.md'}).items():
            body = ('accepted '+key+'\n').encode(); node=self.root/path;node.parent.mkdir(parents=True,exist_ok=True);node.write_bytes(body)
            oid,sha,size=identity(body)
            row={'key':key,'path':path,'mode':'100644','git_oid':oid,'sha256':sha,'bytes':size,
                 'role':'review' if key=='scientific-consolidation-review' else 'work-source',
                 'work_keys':['work-a','work-b','work-c'] if key=='scientific-consolidation-review' else ['work-'+key[-1]],
                 'supporting_source_keys':[] if key=='scientific-consolidation-review' else ['scientific-consolidation-review']}
            self.additions[path]=row;self.cross['sources'][key]={'path':path,'sha256':sha}
        self.baseline={p:{'path':p,'kind':'blob','mode':'100644','git_oid':v[0],'bytes':v[2]} for p,v in self.records.items()}
        self.declared={'role':'historical-only','repository_revision':'c'*40,'source_paths':self.paths,
                       'reading_sources':sorted(self.support),'basis':'scientific-consolidation-review'}
        self.owners={'frontier_history_disposition':self.declared}
        self.tree=b''.join(('100644 blob '+self.records[p][0]+'\t'+p+'\0').encode() for p in self.paths)
        self.index=b'';self.original_type=b'commit\n';self.bad_blob=False;self.index_reads=0;self.change_index=False;self.change_presence=False
        def native(argv, **kw):
            args=argv[3:]
            if args==['cat-file','-t','c'*40]: out=self.original_type
            elif args==['ls-tree','-z','c'*40,'--',*self.paths]: out=self.tree
            elif len(args)==3 and args[:2]==['cat-file','blob']:
                out=next(b for p,b in self.bodies.items() if self.records[p][0]==args[2])
                if self.bad_blob: out+=b'wrong'
                if self.change_presence:
                    node=self.root/self.paths[0];node.parent.mkdir(parents=True,exist_ok=True);node.write_bytes(self.bodies[self.paths[0]])
            elif args==['ls-files','--stage','-z','--',*self.paths]:
                self.index_reads+=1;out=self.index
                if self.change_index and self.index_reads>1:out=b'conflict'
            elif args[:4]==['ls-files','--stage','-z','--'] and set(args[4:])==set(self.additions):
                self.support_reads+=1
                out=b''.join(('100644 '+self.additions[p]['git_oid']+' 0\t'+p+'\0').encode() for p in sorted(self.additions))
                if self.bad_support_index or (self.change_support_index and self.support_reads>1):out=b'wrong'
            else: raise AssertionError('unpermitted native command: '+repr(argv))
            return types.SimpleNamespace(returncode=0,stdout=out,stderr=b'')
        self.native=native
        self.bad_support_index=False
        self.change_support_index=False
        self.support_reads=0

    def qualify(self):
        self.assertTrue(callable(getattr(self.reader,'check_frontier_record_absences',None)), 'missing exact absence qualifier')
        with frontier_mock.patch.multiple(self.reader, FRONTIER_HISTORY_RECORDS=self.records, FRONTIER_HISTORY_REVISION='c'*40,
                                 FRONTIER_HISTORY_SUPPORT=self.support, create=True), frontier_mock.patch.object(self.reader.subprocess,'run',side_effect=self.native):
            return self.reader.check_frontier_record_absences(self.root,self.baseline,self.owners,self.cross,self.additions)

    def refuse(self):
        paths,errors=self.qualify();self.assertEqual(paths,set());self.assertTrue(errors)

    def test_exact_all_absent(self):
        paths,errors=self.qualify();self.assertEqual(errors,[]);self.assertEqual(paths,set(self.paths))

    def test_present_exact_is_not_admitted(self):
        p=self.paths[0];n=self.root/p;n.parent.mkdir(parents=True);n.write_bytes(self.bodies[p])
        paths,errors=self.qualify();self.assertEqual(errors,[]);self.assertEqual(paths,set(self.paths[1:]))

    def test_present_corrupt_or_symlink_or_executable_refused(self):
        p=self.paths[0];n=self.root/p;n.parent.mkdir(parents=True);n.write_bytes(b'corrupt');self.refuse()
        n.write_bytes(self.bodies[p]);n.chmod(0o755);self.refuse();n.chmod(0o644);n.unlink();n.symlink_to(self.root/'science/a.md');self.refuse()

    def test_nonregular_present_refused_before_open_and_nonblocking(self):
        import os
        p=self.paths[0];n=self.root/p;n.parent.mkdir(parents=True);os.mkfifo(n)
        with frontier_mock.patch.object(self.reader.os,'open',side_effect=OSError('test blocks FIFO open')) as opened:
            self.refuse();opened.assert_not_called()
        n.unlink()
        real_open=os.open
        with frontier_mock.patch.object(self.reader.os,'open',wraps=real_open) as opened:
            paths,errors=self.qualify();self.assertEqual(errors,[])
            self.assertTrue(opened.call_args_list)
            self.assertTrue(all(call.args[1] & os.O_NONBLOCK for call in opened.call_args_list))

    def test_missing_or_wrong_disposition_refused(self):
        self.owners={};paths,errors=self.qualify();self.assertEqual(paths,set());self.assertEqual(errors,[])
        self.owners={'frontier_history_disposition':dict(self.declared,role='current')};self.refuse()
        self.owners={'frontier_history_disposition':dict(self.declared,source_paths=self.paths[:-1])};self.refuse()

    def test_wrong_original_census_or_native_tree_refused(self):
        self.baseline[self.paths[0]]['mode']='100755';self.refuse();self.baseline[self.paths[0]]['mode']='100644'
        self.tree=self.tree.replace(b'100644',b'100755',1);self.refuse()

    def test_wrong_commit_or_original_blob_refused(self):
        self.original_type=b'blob\n';self.refuse();self.original_type=b'commit\n';self.bad_blob=True;self.refuse()

    def test_changed_or_conflicted_index_refused(self):
        self.index=('100755 '+self.records[self.paths[0]][0]+' 0\t'+self.paths[0]+'\0').encode();self.refuse()
        self.index=b'';self.change_index=True;self.index_reads=0;self.refuse()

    def test_changed_absence_set_refused(self):
        self.change_presence=True;self.refuse()

    def test_wrong_current_science_or_review_refused(self):
        for p in ('science/a.md','docs/review.md'):
            node=self.root/p;before=node.read_bytes();node.write_bytes(before+b'wrong');self.refuse();node.write_bytes(before)

    def test_missing_review_relationship_refused(self):
        self.additions['science/a.md']['supporting_source_keys']=[];self.refuse()
        self.additions['science/a.md']['supporting_source_keys']=['scientific-consolidation-review']
        self.additions['docs/review.md']['role']='work-source';self.refuse()

    def test_current_source_path_dependency_refused(self):
        self.cross['sources']['still-current']={'path':self.paths[0],'sha256':self.records[self.paths[0]][1]};self.refuse()

    def test_native_failure_refused(self):
        import types
        self.native=lambda *a,**k:types.SimpleNamespace(returncode=1,stdout=b'',stderr=b'unavailable')
        self.refuse()

    def test_wrong_or_changed_current_support_index_refused(self):
        self.bad_support_index=True;self.refuse()
        self.bad_support_index=False;self.support_reads=0;self.change_support_index=True;self.refuse()

class FrontierHistoryCurrentnessTests(unittest.TestCase):
    def setUp(self):
        self.reader = _frontier_history_test_reader()

    def check_change(self, status, admitted=True, unknown=False):
        import types
        path=next(iter(self.reader.FRONTIER_HISTORY_RECORDS))
        if unknown: path+='-unreviewed'
        diff=types.SimpleNamespace(returncode=0,stdout=(status+'\0'+path+'\0').encode())
        with frontier_mock.patch.object(self.reader,'readonly_git_diff',return_value=diff), \
             frontier_mock.patch.object(self.reader,'pmr007_deep_duplicate_paths',return_value=set()) as old:
            result=self.reader.check_corpus_currentness(Path('.'),'c'*40,frontier_paths={path} if admitted else set())
        return result,old.call_count

    def test_exact_qualified_d_avoids_unrelated_duplicate_gate(self):
        errors,calls=self.check_change('D');self.assertEqual(errors,[]);self.assertEqual(calls,0)

    def test_modified_added_and_unreviewed_refused(self):
        for status in ('M','A'):
            with self.subTest(status=status): self.assertTrue(self.check_change(status)[0])
        errors,calls=self.check_change('D',unknown=True);self.assertTrue(errors);self.assertEqual(calls,1)

    def test_missing_qualification_retains_original_guard(self):
        errors,calls=self.check_change('D',admitted=False);self.assertTrue(errors);self.assertEqual(calls,1)




class ReviewedReissueBwTestEdition(unittest.TestCase):
    """One exact BW test successor, using the existing native/ordinary guard."""
    CONTRACTS = {
        'tests/test_pmr007_deep_bw_cj_semantic_reissue.py': (
            'tests/test_pmr007_deep_bw_cj_semantic_reissue.py',
            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
            ('a33743bf20cddf6363021f938a1cef2e0e9baf84',
             '22f0d82eabb228d0d6d0b0c10a5146bf93ca17b6877d34a169cb8986c1f0710e', 6275),
            ('1c3cad17a21642e63b1e264f88ef403173c1dd1b',
             '71703c3507b08e5da55e749afc3af8128444e833ac66c9e6b1b57e97235c2afc', 37844)),
    }
    PATHS = tuple(CONTRACTS)
    fixture = ReviewedAuthorityControls.fixture
    currentness = ReviewedAuthorityControls.currentness
    test_wrong_missing_or_nonordinary_current_owner_refuses = ReviewedAuthorityControls.test_wrong_missing_or_nonordinary_current_owner_refuses
    test_history_index_and_native_failures_refuse = ReviewedAuthorityControls.test_history_index_and_native_failures_refuse
    test_currentness_admits_only_requested_qualified_modifications = ReviewedAuthorityControls.test_currentness_admits_only_requested_qualified_modifications
    test_deletion_type_change_addition_and_unrelated_edit_refuse = ReviewedAuthorityControls.test_deletion_type_change_addition_and_unrelated_edit_refuse
    test_unchanged_positive_and_extra_path_refusal = ReviewedAuthorityControls.test_unchanged_positive_and_extra_path_refusal

    def test_exact_guard_accepts_only_requested_subset(self):
        module, repo, calls = self.fixture()
        self.assertEqual(module.reviewed_authority_modifications(repo, set(self.PATHS)), set(self.PATHS))
        self.assertEqual(module.reviewed_authority_modifications(repo, set()), set())
        self.assertTrue(any('ls-tree' in call for call in calls))
        self.assertTrue(any('cat-file' in call for call in calls))
        self.assertEqual(sum('ls-files' in call for call in calls), 2)

    def test_exact_production_contract_not_editable_wildcard(self):
        import ast
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        tables = {}
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in (
                            'REVIEWED_AUTHORITY_EDITS', 'REFACTOR_EDIT_PATHS'):
                        if target.id == 'REFACTOR_EDIT_PATHS':
                            # The existing owner uses finite set unions and
                            # string comprehensions, as in Digest176's setup.
                            namespace = {}
                            exec(compile(ast.Module(body=[node], type_ignores=[]),
                                         'actual-refactor-path-constant', 'exec'),
                                 {'__builtins__': {}}, namespace)
                            tables[target.id] = namespace[target.id]
                        else:
                            tables[target.id] = ast.literal_eval(node.value)
        self.assertEqual(set(tables), {'REVIEWED_AUTHORITY_EDITS', 'REFACTOR_EDIT_PATHS'})
        for path, contract in self.CONTRACTS.items():
            with self.subTest(path=path):
                self.assertEqual(tables['REVIEWED_AUTHORITY_EDITS'].get(path), contract)
                self.assertNotIn(path, tables['REFACTOR_EDIT_PATHS'])
        for wildcard in ('tests/', 'tests/*', 'tests/test_pmr007_deep_'):
            self.assertNotIn(wildcard, tables['REVIEWED_AUTHORITY_EDITS'])
            self.assertNotIn(wildcard, tables['REFACTOR_EDIT_PATHS'])


class ReviewedReissueBwOriginalPinControls(unittest.TestCase):
    """The final complete pin stage follows, and does not replace, Codex pins."""
    PINS = {
        'tests/test_pmr007_deep_bw_cj_semantic_reissue.py': (
            'a33743bf20cddf6363021f938a1cef2e0e9baf84',
            '22f0d82eabb228d0d6d0b0c10a5146bf93ca17b6877d34a169cb8986c1f0710e',
            6275, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
    }

    def setUp(self):
        previous = ReviewedCodexOriginalPinControls()
        previous.setUp()
        self.base = previous.base
        self.prior = previous.current
        for path, (_, identity, size, _) in self.PINS.items():
            row = dict(repository_path=path, source_sha256=identity, public_sha256=identity,
                       source_bytes=size, public_bytes=size, disposition='REUSE', role='unchanged-role')
            for document in (self.base.original, self.prior):
                document['objects'].append(deepcopy(row))
        self.current = self.base.pinned(self.prior, self.PINS)

    def test_codex_prior_and_complete_bw_final_stage_accepted(self):
        self.assertTrue(self.base.permitted(self.prior))
        self.assertTrue(self.base.permitted(self.current))

    test_partial_pin_and_each_identity_coordinate_or_role_change_refuse = ReviewedCodexOriginalPinControls.test_partial_pin_and_each_identity_coordinate_or_role_change_refuse
    test_missing_duplicate_reordered_and_unrelated_objects_refuse = ReviewedCodexOriginalPinControls.test_missing_duplicate_reordered_and_unrelated_objects_refuse

    def test_only_revision_and_blob_are_added_to_original_bw_row(self):
        path, (blob, identity, size, revision) = next(iter(self.PINS.items()))
        old = next(row for row in self.prior['objects'] if row.get('repository_path') == path)
        current = next(row for row in self.current['objects'] if row.get('repository_path') == path)
        self.assertEqual((old['source_sha256'], old['public_sha256'], old['source_bytes'], old['public_bytes']),
                         (identity, identity, size, size))
        self.assertEqual(current, dict(old, repository_revision=revision, git_blob=blob))
        for field, value in (('publication_basis', 'unreviewed'),
                             ('required_dependencies', ['unreviewed']),
                             ('declared_eligibility_basis', 'unreviewed')):
            with self.subTest(field=field):
                changed = deepcopy(self.current)
                next(row for row in changed['objects'] if row.get('repository_path') == path)[field] = value
                self.assertFalse(self.base.permitted(changed))

    def test_final_bw_stage_cannot_omit_prior_codex_stage(self):
        for path in ReviewedCodexOriginalPinControls.PINS:
            for fields in (('git_blob',), ('repository_revision',), ('git_blob', 'repository_revision')):
                with self.subTest(path=path, fields=fields):
                    changed = deepcopy(self.current)
                    row = next(row for row in changed['objects'] if row.get('repository_path') == path)
                    for field in fields:
                        row.pop(field)
                    self.assertFalse(self.base.permitted(changed))

    def test_corrupt_original_identity_cannot_be_rebound(self):
        path = next(iter(self.PINS))
        for field, value in (('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                             ('source_bytes', 1), ('public_bytes', 1), ('disposition', 'PROJECT')):
            with self.subTest(field=field):
                original = deepcopy(self.base.original)
                candidate = deepcopy(self.current)
                for document in (original, candidate):
                    next(row for row in document['objects'] if row.get('repository_path') == path)[field] = value
                self.assertFalse(self.base.permitted(candidate, original))


class FiveAdmissionCurrentnessTests(unittest.TestCase):
    """Actual currentness and ordinary-file guards with inert native suppliers."""
    def setUp(self):
        import ast
        self.reader = _frontier_history_test_reader()
        tree = ast.parse((ROOT / 'scripts/resolve_t20_v6_source.py').read_bytes())
        rows = next(ast.literal_eval(n.value) for n in tree.body
                    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
                    and t.id == 'ADMISSION_RECORD_MEMBERS' for t in n.targets))
        self.paths = sorted(row[0] for row in rows)
        self.assertEqual(len(self.paths), 5)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.bodies = {p: ('inert admission fixture ' + str(i) + '\n').encode()
                       for i, p in enumerate(self.paths)}
        self.reader.ADMISSION_RECORD_MEMBERS = tuple((p,
            hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(),
            hashlib.sha256(b).hexdigest(), len(b)) for p, b in self.bodies.items())
        self.reader.ADMISSION_RECORD_PATHS = frozenset(self.paths)
        self.reader.PMR007_DEEP_PREFIX = ('docs/project-closure/ar8r-v11/'
            'post-merge-proposals/pmr007-deep-a-ap')
        self.reader.PMR007_ROUNDS_PREFIX = ('docs/project-closure/ar8r-v11/'
            'post-merge-proposals/pmr007-rounds11-20')
        self.reader.PMR007_ROUNDS_FORMALIZATION = self.reader.PMR007_ROUNDS_PREFIX + '/formalization.md'
        self.events = []
        self.supplier_failure = None
        self.navigation_failure = None
        self.rounds_failure = None
        self.supplier_effect = None
        self.diffs = {True: [], False: []}
        def supplier(root, path):
            self.events.append(('supplier', path))
            if self.supplier_failure:
                raise self.supplier_failure
            if self.supplier_effect:
                self.supplier_effect(path)
            return self.bodies[path]
        def rounds(root):
            self.events.append(('rounds98', None))
            if self.rounds_failure:
                raise self.rounds_failure
            return set()
        def navigation(root, *, indexed):
            self.events.append(('navigation', indexed))
            if self.navigation_failure:
                raise self.navigation_failure
            return self.reader.PMR007_ROUNDS_FORMALIZATION
        def diff(root, args):
            import types
            cached = '--cached' in args
            self.events.append(('diff', cached))
            raw = ''.join(status + '\0' + path + '\0' for status, path in self.diffs[cached])
            return types.SimpleNamespace(returncode=0, stdout=raw.encode())
        self.reader.admission_record_bytes = supplier
        self.reader.pmr007_rounds_duplicate_paths = rounds
        self.reader.pmr007_rounds_formalization_navigation = navigation
        self.reader.readonly_git_diff = diff

    def run_change(self, changes, *, cached=True):
        self.diffs = {True: [], False: []}
        self.diffs[cached] = changes
        return self.reader.check_corpus_currentness(self.repo, 'c' * 40)

    def write(self, path, body=None):
        node = self.repo / path
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(self.bodies[path] if body is None else body)
        return node

    def test_each_exact_absence_in_index_and_worktree(self):
        for path in self.paths:
            for cached in (True, False):
                with self.subTest(path=path, cached=cached):
                    self.events.clear()
                    self.assertEqual(self.run_change([('D', path)], cached=cached), [])
                    self.assertIn(('supplier', path), self.events)

    def test_all_five_absent(self):
        self.assertEqual(self.run_change([('D', p) for p in self.paths]), [])
        self.assertEqual({p for kind, p in self.events if kind == 'supplier'}, set(self.paths))

    def test_no_change_does_not_request_history(self):
        self.assertEqual(self.run_change([]), [])
        self.assertFalse(any(kind == 'supplier' for kind, _ in self.events))

    def test_added_modified_and_type_changes_are_not_absences(self):
        for status in ('A', 'M', 'T'):
            with self.subTest(status=status):
                self.events.clear()
                self.assertTrue(self.run_change([(status, self.paths[0])]))
                self.assertFalse(any(kind == 'supplier' for kind, _ in self.events))

    def test_unselected_missing_path_is_not_admitted(self):
        self.assertTrue(self.run_change([('D', self.paths[0] + '-other')]))
        self.assertFalse(any(kind == 'supplier' for kind, _ in self.events))

    def test_native_supplier_refusal_cannot_admit(self):
        for exc in (ValueError('original176'), OSError('index'), UnicodeError('body')):
            with self.subTest(exc=type(exc).__name__):
                self.supplier_failure = exc
                self.assertTrue(self.run_change([('D', self.paths[0])]))

    def test_present_exact_record_is_not_an_absence(self):
        self.write(self.paths[0])
        self.assertTrue(self.run_change([('D', self.paths[0])]))

    def test_present_corrupt_record_is_not_an_absence(self):
        self.write(self.paths[0], b'wrong')
        self.assertTrue(self.run_change([('D', self.paths[0])]))

    def test_selected_symlink_refused(self):
        path = self.paths[0]
        target = self.repo / 'target'
        target.write_bytes(self.bodies[path])
        node = self.repo / path
        node.parent.mkdir(parents=True, exist_ok=True)
        node.symlink_to(target)
        self.assertTrue(self.run_change([('D', path)]))

    def test_ancestor_symlink_refused(self):
        (self.repo / 'elsewhere').mkdir()
        (self.repo / 'docs').symlink_to(self.repo / 'elsewhere', target_is_directory=True)
        self.assertTrue(self.run_change([('D', self.paths[0])]))

    def test_absent_to_present_drift_refused(self):
        self.supplier_effect = lambda path: self.write(path)
        self.assertTrue(self.run_change([('D', self.paths[0])]))

    def test_present_to_absent_drift_refused(self):
        path = self.paths[0]
        self.write(path)
        self.supplier_effect = lambda p: (self.repo / p).unlink()
        self.assertTrue(self.run_change([('D', path)]))

    def test_rounds98_and_navigation_remain_mandatory(self):
        path = next(p for p in self.paths if '/pmr007-rounds11-20/' in p)
        self.assertEqual(self.run_change([('D', path)]), [])
        self.assertIn(('rounds98', None), self.events)
        self.assertIn(('navigation', True), self.events)
        self.assertIn(('supplier', path), self.events)
        self.assertLess(self.events.index(('rounds98', None)), self.events.index(('supplier', path)))
        self.assertLess(self.events.index(('navigation', True)), self.events.index(('supplier', path)))

    def test_rounds98_failure_is_not_suppressed(self):
        path = next(p for p in self.paths if '/pmr007-rounds11-20/' in p)
        self.rounds_failure = ValueError('mandatory98')
        self.assertTrue(self.run_change([('D', path)]))

    def test_navigation_failure_is_not_suppressed(self):
        path = next(p for p in self.paths if '/pmr007-rounds11-20/' in p)
        self.navigation_failure = ValueError('mandatory navigation')
        self.assertTrue(self.run_change([('D', path)]))

    def test_worktree_refusal_not_hidden_by_index_pass(self):
        path = self.paths[0]
        self.diffs = {True: [('D', path)], False: [('M', path)]}
        self.assertTrue(self.reader.check_corpus_currentness(self.repo, 'c' * 40))

    def test_index_refusal_not_hidden_by_worktree_pass(self):
        path = self.paths[0]
        self.diffs = {True: [('M', path)], False: [('D', path)]}
        self.assertTrue(self.reader.check_corpus_currentness(self.repo, 'c' * 40))

    def test_unrelated_change_not_hidden_by_qualified_absence(self):
        self.assertTrue(self.run_change([('D', self.paths[0]), ('D', 'unreviewed/source.yaml')]))

    def test_wrong_native_return_refused(self):
        path = self.paths[0]
        self.bodies[path] = b'wrong native body'
        self.assertTrue(self.run_change([('D', path)]))

    def test_nonbytes_native_return_refused(self):
        path = self.paths[0]
        self.bodies[path] = 'not bytes'
        self.assertTrue(self.run_change([('D', path)]))



# Exact47 current-reader admission controls. Synthetic bytes, inert native leaf.
# Append to tests/test_reader_pilot.py; reuse its existing AST fixture classes.
CENTRAL47_EXPECTED_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
CENTRAL47_EXPECTED_RECORDS = {'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cl_anchor_cover_primary_check_v1_results.json': ('5fd34db7773639f256f3ebec7aed4cbafc1aabac',
                                                                                                                                                                                     'cd83895b3ef8ec0501fe0cb21e37d0c9f3c86b03278e51835e51f1876cf76959',
                                                                                                                                                                                     8832),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cl_anchor_cover_primary_check_v2_results.json': ('673281f18f0b593948d2df7ea7dbb734027b5dd5',
                                                                                                                                                                                     '8484e8099295969760ddab0223778b482e260e1eb69a7c0bd2f802e722aa76f6',
                                                                                                                                                                                     2407),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cm_objective_fitted_function_primary_check_v1_results.json': ('204ad8f25f3217bdd67d50e8330287cd51d0ed66',
                                                                                                                                                                                                  '780fd0f7bce609988e0e0e92c468b735c5ee2fe04e587ee459a0f740a2c78381',
                                                                                                                                                                                                  525),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cm_objective_fitted_function_primary_check_v2_results.json': ('f44d983d728803f8c2427f95eaaaf6b8c521e7c7',
                                                                                                                                                                                                  'c82f11ce9d56c5adfde56942cc0b5b725bf445802139aa3ad151ac6908a01f5c',
                                                                                                                                                                                                  565),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v1_failed_results.json': ('785651477832ccbb072cc75af50155b177148a2a',
                                                                                                                                                                                                        '039a58147dd5aa9ea3b96a050971c67293e97a96a13e361dce3db5e714f196fc',
                                                                                                                                                                                                        2799),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v2_results.json': ('1f37d6723ddbd1d13d70c58b550a1e6807e1ad0a',
                                                                                                                                                                                                 'bc5c47709a4e783c6d35327215cd8c0c73402a22fd6cebcfb4a554a18aab5646',
                                                                                                                                                                                                 2795),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v3_results.json': ('45f0bccbd77cd6ca4af186884b012a8ed968a037',
                                                                                                                                                                                                 '4bf52e1ff74a0384a6db5645cd44f5b0871f84a083a6b18317283409c652a0d1',
                                                                                                                                                                                                 2795),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_co_profile_correction_primary_check_v1_results.json': ('e1eb7e352c4fe70e59ae0cff91ddeeb04c4cbb4e',
                                                                                                                                                                                           'a5a8b61ed789e0ee3aa3eee2aad28a2da8f16c5e58c3aa61eff9b6e92913f6a6',
                                                                                                                                                                                           408),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_co_profile_correction_primary_check_v2_results.json': ('b355d3d8ec253779fa4a4998d486d6c11c128a7f',
                                                                                                                                                                                           '17d3572cc0866dff23438a8b5cd185d7052456e8dbded683f65dd3304955c5a6',
                                                                                                                                                                                           603),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_distinct_bisimulation_rereview_results.json': ('f89950fa8dea2251d7f2a5c9f98b126e30d07e6b',
                                                                                                                                                                                      'a185c8b2f37dbd743de6abfa2e109a10e125a155e143235498910e6b5f10592f',
                                                                                                                                                                                      1053),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_eligible_ui_experiment_primary_check_v1_results.json': ('6c6063513181fee22875150d9e36f8b8296bd6f4',
                                                                                                                                                                                               '1e3f646e1df4be1c865c2b1a052237196c1db486f77aa7f76c95f1d6409bdc83',
                                                                                                                                                                                               757),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_eligible_ui_experiment_primary_check_v2_results.json': ('80f42ef3444bc86186c3979c5c9027b274bdd0b1',
                                                                                                                                                                                               '430e46e3e718fcbbce9688139b8e7e2418be806f662a2fabd36688ed5eb5ca5b',
                                                                                                                                                                                               740),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_distinct_fibre_cover_rereview_results.json': ('dd4f79acaeb8395d8612d5500305e1df090a7a78',
                                                                                                                                                                                     '2384534787c19c7c8a27c7cf59ad32a865a4e25fc18d2918c5a55424d2437c4f',
                                                                                                                                                                                     248),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_partition_refinement_primary_check_v1_results.json': ('0adc064cf4b9d7e2b3ba05687f6a48e72d30b98d',
                                                                                                                                                                                             '9f9266588d75cbc61b3b763bbd2ff6c1daf04986ef4087e1123ba569d4328d02',
                                                                                                                                                                                             352),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_partition_refinement_primary_check_v2_results.json': ('7a2fa6e4e6180ca950b3b44dfdf5f8a3b80588ff',
                                                                                                                                                                                             '8808624a3bbb09426f95603981ca84e104f96c977d4dc091913b2a69040040e8',
                                                                                                                                                                                             369),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_distinct_conflict_graph_rereview_results.json': ('1a5e61df2ecc45fd07d6fbc3d07fbb6f244ec42b',
                                                                                                                                                                                        'fa16d66f6c7527eb0164c6f4a1151fb2d0ab8a760159ab1fe62dc71f55b22494',
                                                                                                                                                                                        975),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_partial_domain_primary_check_v1_results.json': ('9a52c8eb568a33e83f9c1a8f6d0e6b71294eb111',
                                                                                                                                                                                       '26ed4259faa972bbf56f2691de6085a8b3e9c17ae0bac3899612d5d567e8fd8f',
                                                                                                                                                                                       3882),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_partial_domain_primary_check_v2_results.json': ('488f34eeb82faa575976fcfbee7ab2e7ba4a627f',
                                                                                                                                                                                       '3906cf8498d6858014e7112a4238ad6796690dd7c9ffb86e97b66494cdf2946b',
                                                                                                                                                                                       1168),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_CONCRETE_ARCHITECTURE_MAP_V1.yaml': ('ffc8b62232dfc42ce07ea1aa43d8d458f5a4e8d3',
                                                                                                                                                                             'ebcc532f9981f0d2a25be1e05e83f1d2a240e6c5696518f6a896823f0d030853',
                                                                                                                                                                             3918),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_SOURCE_FORMAL_WORLD_MODELS_V1.yaml': ('2a4ec7fecc1bc1c724323d62ecd71dde5ffcea10',
                                                                                                                                                                              '9eae438bebd069f2ada1ab861bda8290c0b44bd2f3ad0202a4093096ef9e7ca4',
                                                                                                                                                                              2491),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_SOURCE_FORMAL_WORLD_MODELS_V2.yaml': ('1f81a89d311d51b6aa77c24c7c0b2f371e80af43',
                                                                                                                                                                              '2da6b0cfdde4ea5d5871d17eb3282169df1daf85bcaf4efdf5a14ff982f7738d',
                                                                                                                                                                              4686),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR-007_DEEP_CL_ADMISSION_OVERLAY.yaml': ('26f53b5f13e3f71a82643d261cc6e1a5f3a593ac',
                                                                                                                                                                   'ef987bf8670007688841e9ddaa2fc6e85455a67644751b010223801a3a926908',
                                                                                                                                                                   1390),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR007_DEEP_CL_ARCHITECTURE_ANCHOR_REGISTRY_V1.yaml': ('f0f12ecc568086ba133836b786dc0cb7b89e5128',
                                                                                                                                                                                '3350c31b6aeae6a13ea23837fb1817fed485f6ad8d11964ba7c22bf6720832bb',
                                                                                                                                                                                2454),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR007_DEEP_CL_ARCHITECTURE_ANCHOR_REGISTRY_V2.yaml': ('9d4365ce30e5d4ba08f622ba925429ef58d83431',
                                                                                                                                                                                '27aa21fac900517a75a0cef30fe99e928c4f43c679c407e7db0bc96fc07d3318',
                                                                                                                                                                                3162),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR-007_DEEP_CM_ADMISSION_OVERLAY.yaml': ('27eaaf7620fa0d9cbb475ef471fb8ab9ec574ef9',
                                                                                                                                                                   '67f7b3d658ea5ace55558ab590fd0c6cfffef95f15bf295f3fc7443bfe49120d',
                                                                                                                                                                   1473),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR007_DEEP_CM_OBJECTIVE_FITTED_FUNCTION_MODELS_V1.yaml': ('da75ddf4e9288e0b788f22837964e14976b6e956',
                                                                                                                                                                                    'da7d7fddfb87dc56eadfd6bcc5a605601ad847aa5ee97263ba2a1a7eecec7160',
                                                                                                                                                                                    2451),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR007_DEEP_CM_OBJECTIVE_FITTED_FUNCTION_MODELS_V2.yaml': ('95dc33114b1b10d7926fd13069ef966e5cbb2ca5',
                                                                                                                                                                                    'c564bf8c94d16ac02b089acb320107a7a7502dbe6b638b6fde987d773b0b9023',
                                                                                                                                                                                    2751),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR-007_DEEP_CN_ADMISSION_OVERLAY.yaml': ('07340bd737e98c68b7bd499398c0b14733473a0b',
                                                                                                                                                                   '4964c5c38a109deb4f680a526deb9b80c9169ed485d6e3e6ec3f8c3524b5c916',
                                                                                                                                                                   1694),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR007_DEEP_CN_AUTHORITY_INDEXED_ANCHOR_MODELS_V1.yaml': ('91eac41938d9363f29b2aaa6cc356d3662f2f721',
                                                                                                                                                                                   'b239062074fcd058f173aed1898fbeece56974673b62cccdce97e8c7cf27c6a8',
                                                                                                                                                                                   2363),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR007_DEEP_CN_AUTHORITY_INDEXED_ANCHOR_MODELS_V2.yaml': ('4ba04371b0d153e2385e770c892dfe08ca992906',
                                                                                                                                                                                   'd3787af3cf0554f39fb62f630fb3804cda9f985036d22aa1d615b48e6fc4e614',
                                                                                                                                                                                   3891),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR-007_DEEP_CO_ADMISSION_OVERLAY.yaml': ('5d7b3607d263060f8cd27f4b70f78c5ea858b03c',
                                                                                                                                                                   '561bd97f52d5b076668e0b643215fc64378499d44c8fd3f3f491d1b9935858ef',
                                                                                                                                                                   1518),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR007_DEEP_CO_PROFILE_MEASURABLE_CORRECTION_MODELS_V1.yaml': ('d5cccbe6b4b76936a304852cdf64a67f4f0bfab7',
                                                                                                                                                                                        '745a3a7e41cc9c452a0be4e76b58468d18add7fe86a229effd0365d5c092d8f6',
                                                                                                                                                                                        1439),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR007_DEEP_CO_PROFILE_MEASURABLE_CORRECTION_MODELS_V2.yaml': ('2ba1b3b358e7505354ac44d20e644a44f2bafb1d',
                                                                                                                                                                                        '8406e983c4c36d7803c8cec61bd97e4ad70b0bb77b9e485a9a67450b18edf317',
                                                                                                                                                                                        1935),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR-007_DEEP_CP_ADMISSION_OVERLAY.yaml': ('3ff592b02ff973d55d457a5b2a17012333a9260f',
                                                                                                                                                                   '87c4d60944526bcbe32ea002d913fbd374e8633270aa11c5aeede226424c76c5',
                                                                                                                                                                   1754),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR007_DEEP_CP_ELIGIBLE_UI_EXPERIMENT_REGISTRY_V1.yaml': ('4c90195800538c0f8bab0841bf61c50a0e975e5e',
                                                                                                                                                                                   'ef27f520e22cab9c3d19c70b8a21287f52695770f98980d2fb310d7feb3b584e',
                                                                                                                                                                                   3033),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR007_DEEP_CP_ELIGIBLE_UI_EXPERIMENT_REGISTRY_V2.yaml': ('d9466caca6cf9213595bdfa489d413251fba67b6',
                                                                                                                                                                                   'a1498322eb840c7cb9d88e4c65d0503ac264da961d96d93fe34d589d52e3e42f',
                                                                                                                                                                                   4084),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR-007_DEEP_CQ_ADMISSION_OVERLAY.yaml': ('4037fcd491eba593dadbaab5a89a3fdca61319ca',
                                                                                                                                                                   '70609844141c6fe0f177ea9f0c0078c1f204f0f49e81975dde97940d94403183',
                                                                                                                                                                   1968),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR007_DEEP_CQ_NORM_UNCERTAIN_RESTORATION_MODEL_V1.yaml': ('45b7c1b3e61ab2616702ae6a291e582f10d3d74c',
                                                                                                                                                                                    'e246434684eaa9e6b5c2e203c1dd5dd6dc7cd0f6aa00cb69f34f178f05823910',
                                                                                                                                                                                    2755),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR007_DEEP_CQ_NORM_UNCERTAIN_RESTORATION_MODEL_V2.yaml': ('dd3ecc53b8c02865acce709205babe160a241c5d',
                                                                                                                                                                                    '258e982a41350546b4bba775088b10cc1a1fc9ca8dbb07be548ddbab85158679',
                                                                                                                                                                                    3383),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cr/PMR007_DEEP_CR_SOURCE_RESTRICTION_MODEL_V1.yaml': ('dd2ec65d7b6bb9732b022cf3ffe9afc06b7af68a',
                                                                                                                                                                            '207dcc4f28697598805b7242776bd8ca0c539111b2fff25eb0f6d3bd999b5c44',
                                                                                                                                                                            1340),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cr/PMR007_DEEP_CR_SOURCE_RESTRICTION_MODEL_V2.yaml': ('e2a37b6a0c1e1584ac209eb8bf0432a13f7d60d9',
                                                                                                                                                                            '7e0ce54a6a3f1fb53e816ba8019314ed7bf037803e340ebac69da34b868b50ba',
                                                                                                                                                                            2515),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR-007_DEEP_CS_ADMISSION_OVERLAY.yaml': ('13b662a5c995a191670c7394335f08ea2fbd4d0a',
                                                                                                                                                                   'fc35f95ca8d802f6191898806961ec1e4dcac0ba9d535253387bc564b8e86ffa',
                                                                                                                                                                   928),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR007_DEEP_CS_REFINEMENT_LATTICE_MODEL_V1.yaml': ('188a4d22366041568a9d3b34816159763176247c',
                                                                                                                                                                            '1aff4e8f6e17bc8625cecbce36ce60b18a60aaedd25872b509f6496d811eb84b',
                                                                                                                                                                            738),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR007_DEEP_CS_REFINEMENT_LATTICE_MODEL_V2.yaml': ('13d956d17c456cc4e05c5f4206cd14fe1c99a9dc',
                                                                                                                                                                            'cbb0e891acd1bd80b5bfeb12951eb92cb63294a37f796ce814aae4f8efe2444f',
                                                                                                                                                                            1319),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR-007_DEEP_CT_ADMISSION_OVERLAY.yaml': ('b4f5b958c6b25087f1d7d934d5700bf85bb3b905',
                                                                                                                                                                   '412593543dd7a13ddf77da5c780125b3b9d47b480176949d5ddc63672050da51',
                                                                                                                                                                   1127),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR007_DEEP_CT_PARTIAL_INTERVENTION_MODEL_V1.yaml': ('f364375dc4acb7bc750c01f112af1fd4253a1aa7',
                                                                                                                                                                              '2051a104e5708ed3d359b10c015db876e8c75a229843598a7c6f660532a828f6',
                                                                                                                                                                              782),
 'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR007_DEEP_CT_PARTIAL_INTERVENTION_MODEL_V2.yaml': ('9cda0d95b4da50eda06e527eb4b75d6771fa67b9',
                                                                                                                                                                              'e4160767e9d9622a6408c0f39868f802688433ad68d86fe342a015dfd1bff5bd',
                                                                                                                                                                              2098)}


def _central47_test_reader():
    import ast, types, os, stat
    module = _frontier_history_test_reader()
    ns = module.__dict__
    ns.update(json=json, Counter=__import__('collections').Counter,
              ADMISSION_RECORD_PATHS=set())
    # No real native operation is available in this isolated namespace.
    def forbidden(*args, **kwargs):
        raise AssertionError('native leaf must be explicitly supplied by the fixture')
    ns['_administrative_git'] = forbidden
    tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ('check_central_public_absences', 'check'):
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.startswith('CENTRAL_PUBLIC_HISTORY_'):
                    ns[target.id] = ast.literal_eval(node.value)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'actual-central47-reader', 'exec'), ns)
    return module


class Central47ProductionContractTests(unittest.TestCase):
    def test_exact47_native_identity_population_and_revision(self):
        module = _central47_test_reader()
        self.assertEqual(getattr(module, 'CENTRAL_PUBLIC_HISTORY_REVISION', None), CENTRAL47_EXPECTED_REVISION)
        self.assertEqual(getattr(module, 'CENTRAL_PUBLIC_HISTORY_RECORDS', None), CENTRAL47_EXPECTED_RECORDS)

    def test_local_complete_pin_table_is_the_same_exact47_plus_revision(self):
        import ast
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == '_permitted_projection_consumer_pins')
        expected = {p: (*v, CENTRAL47_EXPECTED_REVISION) for p, v in CENTRAL47_EXPECTED_RECORDS.items()}
        matching = []
        for node in ast.walk(fn):
            if isinstance(node, ast.Dict):
                try: value = ast.literal_eval(node)
                except (ValueError, TypeError): continue
                if isinstance(value, dict) and set(value) == set(expected): matching.append(value)
        self.assertEqual(matching, [expected], 'one exact literal final pin population is mandatory')


class Central47AbsenceTests(unittest.TestCase):
    """Only tiny synthetic files are written; original metadata paths remain exact."""
    def setUp(self):
        import types
        self.reader = _central47_test_reader()
        self.assertTrue(callable(getattr(self.reader, 'check_central_public_absences', None)),
                        'missing mandatory exact47 current-reader admission')
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.paths = sorted(CENTRAL47_EXPECTED_RECORDS)
        self.bodies = {p: ('central synthetic %02d\n' % i).encode() for i, p in enumerate(self.paths)}
        def identity(body):
            return (hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(),
                    hashlib.sha256(body).hexdigest(), len(body))
        self.identity = identity
        self.records = {p: identity(b) for p, b in self.bodies.items()}
        self.reader.CENTRAL_PUBLIC_HISTORY_RECORDS = self.records
        self.reader.CENTRAL_PUBLIC_HISTORY_REVISION = CENTRAL47_EXPECTED_REVISION
        self.baseline = {p: dict(path=p, kind='blob', mode='100644', git_oid=v[0], bytes=v[2])
                         for p, v in self.records.items()}
        self.manifest = self.root / 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
        self.manifest.parent.mkdir(parents=True)
        self.document = {'schema': 'inert-central47-projection', 'objects': [
            dict(source_sha256=sha, source_action='include', source_bytes=size,
                 role='qualified_metadata', declared_eligibility_basis='reviewed_distribution_metadata',
                 required_dependencies=[], disposition='REUSE', repository_path=p,
                 public_sha256=sha, public_bytes=size, publication_basis='exact_existing_public_repository_object',
                 repository_revision=CENTRAL47_EXPECTED_REVISION, git_blob=blob)
            for p, (blob, sha, size) in self.records.items()]}
        self.save_manifest()
        self.tree = b''.join(('100644 blob '+self.records[p][0]+'\t'+p+'\0').encode() for p in self.paths)
        self.index = b''; self.index_reads = 0; self.native_calls = []
        self.commit_type = b'commit\n'; self.bad_blob = False; self.failure = False
        self.index_drift = False; self.mutate_once = None
        def native(repo, *args):
            self.assertEqual(Path(repo), self.root)
            self.native_calls.append(args)
            if self.failure: raise ValueError('synthetic native evidence unavailable')
            if args == ('cat-file', '-t', CENTRAL47_EXPECTED_REVISION): return self.commit_type
            if args == ('ls-tree', '-z', CENTRAL47_EXPECTED_REVISION, '--', *self.paths): return self.tree
            if args == ('ls-files', '--stage', '-z', '--', *self.paths):
                self.index_reads += 1
                return b'changed\0' if self.index_drift and self.index_reads > 1 else self.index
            if len(args) == 3 and args[:2] == ('cat-file', 'blob'):
                found = [self.bodies[p] for p in self.paths if self.records[p][0] == args[2]]
                self.assertEqual(len(found), 1, 'only selected synthetic native blobs may be queried')
                if self.mutate_once:
                    effect, self.mutate_once = self.mutate_once, None
                    effect()
                return found[0] + (b'wrong' if self.bad_blob is True or self.bad_blob == args[2] else b'')
            raise AssertionError('unexpected native command '+repr(args))
        self.reader._administrative_git = native

    def save_manifest(self):
        self.manifest.write_text(json.dumps(self.document, sort_keys=True)+'\n')

    def present(self, path):
        p = self.root/path; p.parent.mkdir(parents=True, exist_ok=True);p.write_bytes(self.bodies[path]);return p

    def qualify(self):
        return self.reader.check_central_public_absences(self.root, self.baseline)

    def refuse(self):
        absent, errors = self.qualify();self.assertEqual(absent, set());self.assertTrue(errors)

    def test_all47_absent_and_full_present(self):
        absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set(self.paths))
        for p in self.paths: self.present(p)
        absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set())

    def test_staged_absence_and_present_index_subsets_are_accepted(self):
        kept = set(self.paths[::3])
        for p in kept: self.present(p)
        # Original tracked entries can remain for unstaged absence; a subset
        # can remain after staged deletion. Both stay exact mode/blob/stage 0.
        for indexed in (self.paths, sorted(kept), []):
            self.index = b''.join(('100644 '+self.records[p][0]+' 0\t'+p+'\0').encode() for p in indexed)
            absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set(self.paths)-kept)

    def test_each_of13_projection_fields_is_required_and_exact(self):
        original = deepcopy(self.document)
        for field in original['objects'][0]:
            for mutate in ('missing', 'wrong'):
                with self.subTest(field=field, mutate=mutate):
                    self.document = deepcopy(original); row = self.document['objects'][0]
                    if mutate == 'missing': row.pop(field)
                    else: row[field] = ['unexpected'] if field == 'required_dependencies' else 'wrong'
                    self.save_manifest(); self.refuse()
        self.document = original;self.save_manifest()

    def test_each_selected_projection_row_is_mandatory(self):
        original = deepcopy(self.document)
        for i in range(47):
            with self.subTest(omitted=i):
                self.document = deepcopy(original);self.document['objects'].pop(i);self.save_manifest();self.refuse()

    def test_duplicate_extra_field_and_malformed_document_refuse(self):
        original = deepcopy(self.document)
        for kind in ('duplicate', 'extra-field', 'not-list', 'not-dict', 'bad-json'):
            with self.subTest(kind=kind):
                self.document = deepcopy(original)
                if kind == 'duplicate': self.document['objects'].append(deepcopy(self.document['objects'][0]))
                elif kind == 'extra-field': self.document['objects'][0]['extra'] = True
                elif kind == 'not-list': self.document['objects'] = {}
                elif kind == 'not-dict': self.document['objects'][0] = None
                self.save_manifest()
                if kind == 'bad-json': self.manifest.write_text('{')
                self.refuse()

    def test_unrelated_projection_rows_do_not_expand_absence_permission(self):
        unrelated = deepcopy(self.document['objects'][0]);unrelated['repository_path'] = 'unrelated.json'
        self.document['objects'].append(unrelated);self.save_manifest()
        absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set(self.paths));self.assertNotIn('unrelated.json', absent)

    def test_pathless_unrelated_projection_shapes_do_not_expand_permission(self):
        shapes = [
            {'source_sha256': 'a'*64, 'source_action': 'identity_only', 'disposition': 'IDENTITY_ONLY', 'availability': 'held_excluded', 'exclusion_categories': ['explicit_owner_private_custody_only']},
            {'source_sha256': 'b'*64, 'source_action': 'include', 'disposition': 'NOT_PUBLISHED'},
            {'source_sha256': 'c'*64, 'source_action': 'omit', 'disposition': 'IDENTITY_ONLY'},
        ]
        self.document['objects'].extend(shapes); self.save_manifest()
        absent, errors = self.qualify()
        self.assertEqual(errors, []); self.assertEqual(absent, set(self.paths))
        for path in self.paths: self.present(path)
        absent, errors = self.qualify()
        self.assertEqual(errors, []); self.assertEqual(absent, set())

    def test_pathless_or_malformed_selected_rows_still_refuse(self):
        original = deepcopy(self.document)
        for missing, value in [(True, None), (False, None), (False, 7), (False, [])]:
            with self.subTest(missing=missing, value=value):
                self.document = deepcopy(original)
                if missing: del self.document['objects'][0]['repository_path']
                else: self.document['objects'][0]['repository_path'] = value
                self.save_manifest(); self.refuse()

    def test_explicit_malformed_unrelated_path_still_refuses(self):
        original = deepcopy(self.document)
        for value in [None, 7, [], {}]:
            with self.subTest(value=value):
                self.document = deepcopy(original)
                self.document['objects'].append({'repository_path': value})
                self.save_manifest(); self.refuse()

    def test_original_census_each_mode_kind_blob_size_and_missing_refuse(self):
        path=self.paths[0]; original=deepcopy(self.baseline)
        for field,value in [('kind','tree'),('mode','100755'),('git_oid','0'*40),('bytes',1),('absent',None)]:
            with self.subTest(field=field):
                self.baseline=deepcopy(original)
                if field=='absent':self.baseline.pop(path)
                else:self.baseline[path][field]=value
                self.refuse()

    def test_noncommit_wrong_tree_and_native_blob_refuse(self):
        self.commit_type=b'blob\n';self.refuse();self.commit_type=b'commit\n'
        old=self.tree;self.tree=self.tree.replace(b'100644',b'100755',1);self.refuse();self.tree=old
        self.bad_blob=True;self.refuse()

    def test_missing_duplicate_extra_reordered_original_tree_refuse(self):
        original=self.tree; rows=original.split(b'\0')[:-1]
        for candidate in (rows[:-1],rows+rows[:1],rows+[b'100644 blob '+b'0'*40+b'\tunrelated'],list(reversed(rows))):
            with self.subTest(candidate=len(candidate)):
                self.tree=b'\0'.join(candidate)+b'\0';self.refuse()
        self.tree=original

    def test_conflict_wrong_mode_blob_extra_duplicate_and_unterminated_index_refuse(self):
        p=self.paths[0];r=('100644 '+self.records[p][0]+' 0\t'+p).encode()
        for candidate in (r.replace(b' 0\t',b' 1\t')+b'\0',r.replace(b'100644',b'100755')+b'\0',
                          r.replace(self.records[p][0].encode(),b'0'*40)+b'\0',r+b'\0'+r+b'\0',
                          r.replace(p.encode(),b'unrelated')+b'\0',r):
            with self.subTest(candidate=candidate[:20]):self.index=candidate;self.refuse()

    def test_every_selected_native_blob_is_authenticated(self):
        for path in self.paths:
            with self.subTest(path=path):
                self.bad_blob=self.records[path][0];self.refuse()
        self.bad_blob=False

    def test_empty_missing_or_extra_native_population_cannot_bypass_guard(self):
        original=self.records
        for changed in ({},dict(list(original.items())[:-1]),dict(original,unrelated=next(iter(original.values())))):
            with self.subTest(population=len(changed)):
                self.reader.CENTRAL_PUBLIC_HISTORY_RECORDS=changed;self.refuse()
        self.reader.CENTRAL_PUBLIC_HISTORY_RECORDS=original

    def test_native_refusal_does_not_admit_any_path(self):
        self.failure=True;self.refuse()

    def test_present_corrupt_symlink_hardlink_executable_directory_fifo_refuse(self):
        import os
        p=self.present(self.paths[0]);p.write_bytes(b'corrupt');self.refuse();p.unlink()
        target=self.root/'outside';target.write_bytes(self.bodies[self.paths[0]])
        p.symlink_to(target);self.refuse();p.unlink()
        os.link(target,p);self.refuse();p.unlink()
        self.present(self.paths[0]).chmod(0o755);self.refuse();p.chmod(0o644);p.unlink()
        p.mkdir();self.refuse();p.rmdir();os.mkfifo(p)
        with frontier_mock.patch.object(self.reader.os,'open',side_effect=OSError('FIFO must never open')) as opened:
            self.refuse();opened.assert_not_called()

    def test_manifest_missing_symlink_hardlink_executable_refuse(self):
        import os
        saved=self.manifest.read_bytes();self.manifest.unlink();self.refuse()
        other=self.root/'manifest-copy';other.write_bytes(saved)
        self.manifest.symlink_to(other);self.refuse();self.manifest.unlink()
        os.link(other,self.manifest);self.refuse();self.manifest.unlink()
        self.manifest.write_bytes(saved);self.manifest.chmod(0o755);self.refuse()

    def test_index_change_during_qualification_refuses(self):
        self.index_drift=True;self.refuse()

    def test_absent_to_present_and_present_to_absent_drift_refuse(self):
        self.mutate_once=lambda:self.present(self.paths[0]);self.refuse()
        p=self.root/self.paths[0];self.mutate_once=lambda:p.unlink();self.refuse()

    def test_equal_bytes_replacement_and_manifest_drift_refuse(self):
        p=self.present(self.paths[0])
        def replace():p.unlink();self.present(self.paths[0])
        self.mutate_once=replace;self.refuse()
        self.mutate_once=lambda:self.manifest.write_bytes(self.manifest.read_bytes()+b' ')
        self.refuse()


class Central47OriginalPinControls(unittest.TestCase):
    PINS = {p: (*v, CENTRAL47_EXPECTED_REVISION) for p,v in CENTRAL47_EXPECTED_RECORDS.items()}
    def setUp(self):
        previous=ReviewedReissueBwOriginalPinControls();previous.setUp()
        self.base=previous.base;self.prior=previous.current
        for p,(_,sha,size,_) in self.PINS.items():
            row=dict(repository_path=p,source_sha256=sha,public_sha256=sha,source_bytes=size,public_bytes=size,
                     disposition='REUSE',role='qualified_metadata',declared_eligibility_basis='reviewed_distribution_metadata',
                     required_dependencies=[],source_action='include',publication_basis='exact_existing_public_repository_object')
            for doc in (self.base.original,self.prior):doc['objects'].append(deepcopy(row))
        self.current=self.base.pinned(self.prior,self.PINS)

    def test_prior_reissue_stage_and_complete47_stage_remain_accepted(self):
        self.assertTrue(self.base.permitted(self.prior));self.assertTrue(self.base.permitted(self.current))

    def test_partial47_and_each_coordinate_identity_or_role_mutation_refuse(self):
        for path in self.PINS:
            for fields in (('repository_revision',),('git_blob',),('repository_revision','git_blob')):
                with self.subTest(path=path, fields=fields):
                    changed=deepcopy(self.current);r=next(r for r in changed['objects'] if r.get('repository_path')==path)
                    for field in fields:r.pop(field)
                    self.assertFalse(self.base.permitted(changed))
        p=next(iter(self.PINS))
        for field,value in [('repository_revision','HEAD'),('git_blob','0'*40),('source_sha256','0'*64),('public_sha256','0'*64),
                            ('source_bytes',1),('public_bytes',1),('role','authored_code'),('disposition','PROJECT'),
                            ('source_action','exclude'),('required_dependencies',['extra']),('publication_basis','other'),
                            ('declared_eligibility_basis','other')]:
            with self.subTest(field=field):
                changed=deepcopy(self.current);next(r for r in changed['objects'] if r.get('repository_path')==p)[field]=value
                self.assertFalse(self.base.permitted(changed))

    def test_missing_duplicate_reordered_extra_row_and_top_level_change_refuse(self):
        for kind in ('missing','duplicate','reordered','extra','metadata'):
            with self.subTest(kind=kind):
                changed=deepcopy(self.current)
                if kind=='missing':changed['objects'].pop()
                elif kind=='duplicate':changed['objects'].append(deepcopy(changed['objects'][-1]))
                elif kind=='reordered':changed['objects'].reverse()
                elif kind=='extra':changed['objects'].append({'repository_path':'unrelated'})
                else:changed['schema']='changed'
                self.assertFalse(self.base.permitted(changed))

    def test_no_original_identity_rebinding_or_prior_stage_omission(self):
        p=next(iter(self.PINS))
        for field,value in [('source_sha256','0'*64),('public_sha256','0'*64),('source_bytes',1),('public_bytes',1),('disposition','PROJECT')]:
            with self.subTest(field=field):
                original=deepcopy(self.base.original);current=deepcopy(self.current)
                for document in (original,current):next(r for r in document['objects'] if r.get('repository_path')==p)[field]=value
                self.assertFalse(self.base.permitted(current,original))
        prior_paths=set(ReviewedReissueBwOriginalPinControls.PINS)|set(ReviewedCodexOriginalPinControls.PINS)
        for p in prior_paths:
            changed=deepcopy(self.current);r=next(r for r in changed['objects'] if r.get('repository_path')==p)
            r.pop('repository_revision');r.pop('git_blob');self.assertFalse(self.base.permitted(changed))

    def test_exact_candidate_delta_is_only_two_fields_for_all47(self):
        self.assertTrue(self.base.permitted(self.current))
        for p,(blob,sha,size,rev) in self.PINS.items():
            old=next(r for r in self.prior['objects'] if r.get('repository_path')==p)
            new=next(r for r in self.current['objects'] if r.get('repository_path')==p)
            self.assertEqual(new,dict(old,repository_revision=rev,git_blob=blob))


class Central47CurrentnessTests(unittest.TestCase):
    def gate(self, changes, qualified):
        import inspect,types
        reader=_central47_test_reader();fn=reader.check_corpus_currentness
        self.assertIn('central_paths',inspect.signature(fn).parameters,'missing exact47 currentness parameter')
        reader.CENTRAL_PUBLIC_HISTORY_RECORDS=CENTRAL47_EXPECTED_RECORDS
        raw=''.join(status+'\0'+p+'\0' for status,p in changes).encode()
        reader.readonly_git_diff=lambda *a:types.SimpleNamespace(returncode=0,stdout=raw)
        return fn(Path('.'),'c'*40,central_paths=qualified)

    def test_only_qualified_exact_D_paths_are_admitted(self):
        paths=sorted(CENTRAL47_EXPECTED_RECORDS)
        self.assertEqual(self.gate([('D',p) for p in paths],set(paths)),[])
        self.assertEqual(self.gate([],set()),[])

    def test_unqualified_modified_added_renamed_and_unrelated_refuse(self):
        p=next(iter(CENTRAL47_EXPECTED_RECORDS))
        for status in ('M','A','T'):
            with self.subTest(status=status):self.assertTrue(self.gate([(status,p)],{p}))
        self.assertTrue(self.gate([('D',p)],set()))
        self.assertTrue(self.gate([('D',p+'-other')],{p+'-other'}))
        self.assertTrue(self.gate([('D',p),('M','unrelated')],{p}))


class Central47MainDispatchTests(unittest.TestCase):
    def test_main_always_runs_qualifier_retains_errors_and_passes_paths(self):
        import types
        reader=_central47_test_reader();events=[];selected={next(iter(CENTRAL47_EXPECTED_RECORDS))}
        reader.entries_at=lambda *a:[]
        reader.corpus_currentness_context=lambda *a:(({}, {}, {}, {}, {}),['context-sentinel'])
        reader.check_frontier_record_absences=lambda *a:(set(),['frontier-sentinel'])
        def central(repo,baseline):events.append(('central',baseline));return selected,['central-fatal-sentinel']
        reader.check_central_public_absences=central
        reader.check_abk_public_absences=lambda *a:(set(),[])
        def currentness(*args,**kwargs):events.append(('currentness',args,kwargs));return ['currentness-sentinel']
        reader.check_corpus_currentness=currentness
        reader.check_collection_dispositions=lambda *a:['collection-sentinel']
        reader.check_collection_result_routes=lambda *a:['route-sentinel']
        reader.Counter=__import__('collections').Counter;reader.PROBES=set()
        reader.yaml=types.SimpleNamespace(safe_load=lambda _: {'artifacts':[]},YAMLError=ValueError)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);profile=root/'profile';profile.write_text('{}')
            reader.safe_path=lambda *a:profile
            owners={'schema':'orthemology-reader-owner-map-v1','external_body_admissions':[],
                    'baseline':{'commit':'c'*40},'collections':[],'publication_profile':'profile'}
            cross={'schema':'orthemology-reader-crosswalk-v1','coverage_stage':'reader-candidate'}
            errors=reader.check(root,owners,cross)
        self.assertEqual([e[0] for e in events],['central','currentness'])
        self.assertEqual(events[0][1],{})
        call=events[1];supplied=call[2].get('central_paths',call[1][8] if len(call[1])>8 else set())
        self.assertEqual(supplied,selected)
        self.assertEqual(set(errors),{'context-sentinel','frontier-sentinel','central-fatal-sentinel',
                                     'currentness-sentinel','collection-sentinel','route-sentinel'})


# Fixed public87 acceptance controls: no protected bodies or original execution.
import ast
import collections
import os
import types
from unittest import mock
import resolve_t20_v6_source as resolver
EXPECTED_PUBLIC_CATALOG_SHA256 = '8387856c594d746d32f24b06e300ab87b9f539bb74b159638751a7c8db974868'

class PublicCheckpointContractTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(resolver, '_checkpoint_public_copy_catalog', None)),
                        'fixed public87 catalog is required')
        self.assertTrue(callable(getattr(resolver, 'checkpoint_public_duplicate_paths', None)),
                        'fixed public87 guard is required')

    def test_exact_membership_and_retained_graph(self):
        cat = resolver._checkpoint_public_copy_catalog()
        self.assertEqual(len(cat), 87)
        self.assertEqual(set(cat), resolver.CHECKPOINT_PUBLIC_COPY_PATHS)
        self.assertEqual(len({v['canonical'] for v in cat.values()}), 71)
        self.assertFalse(set(cat) & {v['canonical'] for v in cat.values()})
        self.assertEqual(len({v['blob'] for v in cat.values()}), 66)
        encoded = json.dumps(resolver.CHECKPOINT_PUBLIC_COPY_MEMBERS, separators=(',', ':')).encode()
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), EXPECTED_PUBLIC_CATALOG_SHA256)

    def test_changed_catalog_digest_rejected(self):
        with mock.patch.object(resolver, 'CHECKPOINT_PUBLIC_COPY_CATALOG_SHA256', '0'*64):
            with self.assertRaises(ValueError): resolver._checkpoint_public_copy_catalog()

    def test_missing_or_extra_population_rejected(self):
        values = resolver.CHECKPOINT_PUBLIC_COPY_MEMBERS
        for rows in (values[:-1], values + (values[0],)):
            with self.subTest(count=len(rows)), mock.patch.object(resolver, 'CHECKPOINT_PUBLIC_COPY_MEMBERS', rows):
                with self.assertRaises(ValueError): resolver._checkpoint_public_copy_catalog()

    def test_changed_original_catalog_binding_rejected(self):
        original = resolver._checkpoint_copy_catalog()
        selected = next(p for p in original if p in resolver.CHECKPOINT_PUBLIC_COPY_PATHS)
        for key, value in [('canonical', 'wrong/provider'), ('blob', '0'*40), ('sha256', '0'*64),
                           ('bytes', -1), ('mode', '100755'), ('prior_canonical', 'wrong/prior')]:
            changed = {p:dict(row) for p,row in original.items()}; changed[selected][key] = value
            with self.subTest(field=key), mock.patch.object(resolver, '_checkpoint_copy_catalog', return_value=changed):
                with self.assertRaises(ValueError): resolver._checkpoint_public_copy_catalog()

    def test_every_member_checked_even_when_present(self):
        checked=[]
        with mock.patch.object(resolver, '_checkpoint_copy_bound_bytes', side_effect=lambda r,p,b:checked.append(p)), \
             mock.patch.object(resolver.os.path, 'lexists', return_value=True):
            self.assertEqual(resolver.checkpoint_public_duplicate_paths(Path('inert')), set())
        self.assertEqual(collections.Counter(checked), collections.Counter(resolver.CHECKPOINT_PUBLIC_COPY_PATHS))

    def test_only_actual_absence_returned(self):
        paths=sorted(resolver.CHECKPOINT_PUBLIC_COPY_PATHS); absent=set(paths[::2]);checked=[]
        with mock.patch.object(resolver, '_checkpoint_copy_bound_bytes', side_effect=lambda r,p,b:checked.append(p)), \
             mock.patch.object(resolver.os.path, 'lexists', side_effect=lambda p:str(p).removeprefix('inert/') not in absent):
            self.assertEqual(resolver.checkpoint_public_duplicate_paths(Path('inert')), absent)
        self.assertEqual(len(checked), 87)

    def test_provider_predicate_failure_never_grants_absence(self):
        with mock.patch.object(resolver, '_checkpoint_copy_bound_bytes', side_effect=ValueError('provider failed')):
            with self.assertRaisesRegex(ValueError, 'provider failed'):
                resolver.checkpoint_public_duplicate_paths(Path('inert'))

    def test_no_unrestricted_population_argument(self):
        with self.assertRaises(TypeError): resolver.checkpoint_public_duplicate_paths(Path('inert'), set())


class PublicCheckpointCurrentnessTests(unittest.TestCase):
    """Real reader dispatch with inert unrelated gates; native proof is separate."""
    def setUp(self):
        self.assertTrue(hasattr(resolver, 'CHECKPOINT_PUBLIC_COPY_PATHS'), 'fixed public87 population required')
        tree=ast.parse((ROOT/'scripts/check_reader_pilot.py').read_bytes())
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check_corpus_currentness')
        ns={name:set() for name in {n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and n.id.isupper()}}
        ns.update(Path=Path, os=os, PMR007_DEEP_PREFIX='unused-deep', PMR007_ROUNDS_PREFIX='unused-rounds',
                  CONTINUATION_COPY_ROOT='unused-continuation', SUCCESSOR_INPUT_REGISTRY='unused-input',
                  SUCCESSOR_CALCULUS_MAP='unused-calculus', MEDIATOR_GUIDE='unused-guide',
                  PMR007_ROUNDS_FORMALIZATION='unused-formalization', REVIEWED_AUTHORITY_EDITS={})
        self.changed=[];self.legacy=[];self.calls=0;self.allowed=set(resolver.CHECKPOINT_PUBLIC_COPY_PATHS);self.fault=False
        def qualify(root):
            self.calls+=1
            if self.fault:raise ValueError('fixed public gate failed')
            return self.allowed
        ns['checkpoint_public_duplicate_paths']=qualify
        ns['CHECKPOINT_PUBLIC_COPY_PATHS']=resolver.CHECKPOINT_PUBLIC_COPY_PATHS
        for name in ['CHECKPOINT_COPY_PATHS','CHECKPOINT_RECORD_COPY_PATHS','CHECKPOINT_PACKAGE_COPY_PATHS','CHECKPOINT_CODE_COPY_PATHS']:
            ns[name]=getattr(resolver,name)
        for name in ['checkpoint_duplicate_paths','checkpoint_record_duplicate_paths','checkpoint_package_duplicate_paths']:
            def legacy(root, name=name):
                self.legacy.append(name)
                raise ValueError('legacy whole-class evidence required')
            ns[name]=legacy
        for name in ['pmr007_deep_duplicate_paths','pmr007_rounds_duplicate_paths','formal_duplicate_paths','formal_provider_absences','checkpoint_code_duplicate_paths','digest_record_absences']:
            ns[name]=lambda root:set()
        ns.update(binding_record_candidate=lambda p:False,status_record_candidate=lambda p:False)
        def diff(root,args):
            rows=self.changed if not isinstance(self.changed,dict) else self.changed['cached' if '--cached' in args else 'worktree']
            return types.SimpleNamespace(returncode=0,stdout=b''.join((s+'\0'+p+'\0').encode() for s,p in rows))
        ns['readonly_git_diff']=diff
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'real-currentness-function','exec'),ns)
        self.ns=ns;self.paths=sorted(self.allowed)
    def check(self):return self.ns['check_corpus_currentness'](Path('inert'),'inert-base')
    def test_all87_deletions_use_only_fixed_gate(self):
        self.changed=[('D',p) for p in self.paths]
        self.assertEqual(self.check(),[]);self.assertEqual(self.calls,1);self.assertEqual(self.legacy,[])
    def test_no_change_does_not_invoke_gate(self):
        self.assertEqual(self.check(),[]);self.assertEqual(self.calls,0)
    def test_partial_deletion_still_requires_complete_guard(self):
        self.changed=[('D',self.paths[0])];self.assertEqual(self.check(),[]);self.assertEqual(self.calls,1)
    def test_failed_guard_refuses(self):
        self.changed=[('D',self.paths[0])];self.fault=True;self.assertTrue(self.check())
    def test_absence_not_returned_refuses(self):
        self.changed=[('D',self.paths[0])];self.allowed=set();self.assertTrue(self.check())
    def test_modification_never_gets_deletion_permission(self):
        for status in ['M','A','T']:
            with self.subTest(status=status):self.changed=[(status,self.paths[0])];self.assertTrue(self.check())
    def test_unrelated_change_refuses(self):
        self.changed=[('D',self.paths[0]),('D','unrelated/path')];self.assertTrue(self.check())
    def test_mixed_restricted_deletion_keeps_legacy_guard(self):
        restricted=next(p for p in resolver.CHECKPOINT_COPY_PATHS if p not in self.allowed)
        self.changed=[('D',self.paths[0]),('D',restricted)]
        self.assertTrue(self.check());self.assertIn('checkpoint_duplicate_paths',self.legacy)
    def test_cached_and_worktree_are_both_checked(self):
        self.changed={'cached':[('D',self.paths[0])],'worktree':[('M',self.paths[0])]}
        self.assertTrue(self.check());self.assertEqual(self.calls,1)
    def test_code52_deletion_keeps_own_guard(self):
        path=next(iter(resolver.CHECKPOINT_CODE_COPY_PATHS));calls=[]
        self.ns['checkpoint_code_duplicate_paths']=lambda root:calls.append(root) or {path}
        self.changed=[('D',self.paths[0]),('D',path)]
        self.assertEqual(self.check(),[]);self.assertEqual(len(calls),1)

# Additional fixed-public87 controls. Reuse the preceding author fixtures only.
class PublicCheckpointIndependentBindingTests(unittest.TestCase):
    setUp = PublicCheckpointContractTests.setUp

    def test_population_set_drift_refused(self):
        paths = resolver.CHECKPOINT_PUBLIC_COPY_PATHS
        for changed in (set(paths) - {next(iter(paths))}, set(paths) | {'unselected/path'}):
            with self.subTest(population=len(changed)), mock.patch.object(resolver, 'CHECKPOINT_PUBLIC_COPY_PATHS', changed):
                with self.assertRaises(ValueError):
                    resolver._checkpoint_public_copy_catalog()

    def test_record_and_package_source_bindings_cannot_drift(self):
        for name in ('_checkpoint_record_copy_catalog', '_checkpoint_package_copy_catalog'):
            original = getattr(resolver, name)()
            selected = next(p for p in original if p in resolver.CHECKPOINT_PUBLIC_COPY_PATHS)
            for field, value in (('canonical', 'wrong/provider'), ('blob', '0'*40),
                                 ('sha256', '0'*64), ('bytes', -1), ('mode', '100755'),
                                 ('prior_canonical', 'wrong/prior')):
                changed = {p: dict(row) for p, row in original.items()}
                changed[selected][field] = value
                with self.subTest(catalog=name, field=field), mock.patch.object(resolver, name, return_value=changed):
                    with self.assertRaises(ValueError):
                        resolver._checkpoint_public_copy_catalog()

    def test_every_native_call_receives_exact_original_binding(self):
        expected = resolver._checkpoint_public_copy_catalog()
        root = Path('inert')
        calls = []
        def native(r, path, binding):
            self.assertEqual(r, root)
            self.assertIn(path, expected)
            self.assertEqual(binding, expected[path])
            calls.append(path)
        with mock.patch.object(resolver, '_checkpoint_copy_bound_bytes', side_effect=native), \
             mock.patch.object(resolver.os.path, 'lexists', return_value=False):
            self.assertEqual(resolver.checkpoint_public_duplicate_paths(root), set(expected))
        self.assertEqual(collections.Counter(calls), collections.Counter(expected.keys()))
        self.assertTrue(any(row.get('prior_canonical') for row in expected.values()))

    def test_late_native_failure_cannot_return_partial_allowance(self):
        count = []
        def native(root, path, binding):
            count.append(path)
            if len(count) == 87:
                raise ValueError('last selected native predicate failed')
        with mock.patch.object(resolver, '_checkpoint_copy_bound_bytes', side_effect=native), \
             mock.patch.object(resolver.os.path, 'lexists', return_value=False):
            with self.assertRaisesRegex(ValueError, 'last selected native predicate failed'):
                resolver.checkpoint_public_duplicate_paths(Path('inert'))
        self.assertEqual(len(set(count)), 87)

    def test_new_fixed_guard_never_calls_old_whole_classes(self):
        from contextlib import ExitStack
        with ExitStack() as stack:
            for name in ('checkpoint_duplicate_paths', 'checkpoint_record_duplicate_paths', 'checkpoint_package_duplicate_paths'):
                stack.enter_context(mock.patch.object(resolver, name, side_effect=AssertionError('whole-class body execution forbidden')))
            stack.enter_context(mock.patch.object(resolver, '_checkpoint_copy_bound_bytes', return_value=b'inert'))
            stack.enter_context(mock.patch.object(resolver.os.path, 'lexists', return_value=False))
            self.assertEqual(resolver.checkpoint_public_duplicate_paths(Path('inert')), set(resolver.CHECKPOINT_PUBLIC_COPY_PATHS))

    def test_native_old_class_and_public_source_bytes_unchanged(self):
        expected = {
            '_checkpoint_bound_bytes': 'b76238ab942e9ac067ecfdb3bdc8be7ff8cb1b04dc6196e7eef9e8c5bc0f0aad',
            '_checkpoint_copy_bound_bytes': '9c7cea2fadcffc7920831068906a8278df2e8478ef4f1fe3b894cf6ad86a69b8',
            'checkpoint_duplicate_paths': '0a9b1c4f4800d4d5ac017f0c6b379efd570d378363b5fa9bb9da423368409488',
            'checkpoint_record_duplicate_paths': '81683e67dad673cedaae25e6826fafa9ebd7141fedd0c686d49ec6d2373e89b5',
            'checkpoint_package_duplicate_paths': '67473a94e2fbe96877f40d12fbbb15ee86c0a37054ee3ac31a76450a0a4f729c',
            'source_bytes': '495d9d04ab7bbc84c9cadb90e8495928a27b26236151a2e9b246c00765b4d57a',
        }
        source = (ROOT/'scripts/resolve_t20_v6_source.py').read_text()
        tree = ast.parse(source)
        got = {n.name: hashlib.sha256(ast.get_source_segment(source, n).encode()).hexdigest()
               for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in expected}
        self.assertEqual(got, expected)


class PublicCheckpointIndependentCurrentnessTests(unittest.TestCase):
    setUp = PublicCheckpointCurrentnessTests.setUp
    check = PublicCheckpointCurrentnessTests.check

    def _outside(self, population):
        return next(p for p in getattr(resolver, population) if p not in resolver.CHECKPOINT_PUBLIC_COPY_PATHS)

    def test_each_unselected_class_still_requires_its_whole_guard(self):
        for population, guard in (
                ('CHECKPOINT_COPY_PATHS', 'checkpoint_duplicate_paths'),
                ('CHECKPOINT_RECORD_COPY_PATHS', 'checkpoint_record_duplicate_paths'),
                ('CHECKPOINT_PACKAGE_COPY_PATHS', 'checkpoint_package_duplicate_paths')):
            with self.subTest(population=population):
                self.legacy.clear()
                self.changed = [('D', self.paths[0]), ('D', self._outside(population))]
                errors = self.check()
                self.assertTrue(errors)
                self.assertEqual(self.legacy, [guard])
                self.assertTrue(any('legacy whole-class evidence required' in e for e in errors))

    def test_all_three_unselected_triggers_survive_across_both_diffs(self):
        self.changed = {
            'cached': [('D', self.paths[0]), ('D', self._outside('CHECKPOINT_COPY_PATHS'))],
            'worktree': [('D', self._outside('CHECKPOINT_RECORD_COPY_PATHS')),
                         ('D', self._outside('CHECKPOINT_PACKAGE_COPY_PATHS'))],
        }
        errors = self.check()
        self.assertEqual(self.calls, 1)
        self.assertEqual(collections.Counter(self.legacy), collections.Counter((
            'checkpoint_duplicate_paths', 'checkpoint_record_duplicate_paths', 'checkpoint_package_duplicate_paths')))
        self.assertEqual(sum('legacy whole-class evidence required' in e for e in errors), 3)

    def test_unselected_old_guard_success_is_not_disabled(self):
        calls = []
        rows = []
        for population, guard in (
                ('CHECKPOINT_COPY_PATHS', 'checkpoint_duplicate_paths'),
                ('CHECKPOINT_RECORD_COPY_PATHS', 'checkpoint_record_duplicate_paths'),
                ('CHECKPOINT_PACKAGE_COPY_PATHS', 'checkpoint_package_duplicate_paths')):
            path = self._outside(population)
            rows.append(('D', path))
            self.ns[guard] = lambda root, path=path, guard=guard: calls.append(guard) or {path}
        self.changed = [('D', self.paths[0]), *rows]
        self.assertEqual(self.check(), [])
        self.assertEqual(len(calls), 3)
        self.assertEqual(self.calls, 1)

    def test_fixed_guard_error_types_stay_fatal_in_currentness(self):
        for fault in (ValueError('selected-native-value'), OSError('selected-native-os'), UnicodeError('selected-native-unicode')):
            with self.subTest(error=type(fault).__name__):
                self.changed = [('D', self.paths[0])]
                def fail(root):
                    raise fault
                self.ns['checkpoint_public_duplicate_paths'] = fail
                errors = self.check()
                self.assertTrue(any(str(fault) in e for e in errors))
                self.assertTrue(any(self.paths[0] in e for e in errors))

    def test_worktree_only_selected_deletion_is_qualified(self):
        self.changed = {'cached': [], 'worktree': [('D', self.paths[-1])]}
        self.assertEqual(self.check(), [])
        self.assertEqual(self.calls, 1)
        self.assertEqual(self.legacy, [])

    def test_failed_or_malformed_diff_cannot_be_hidden(self):
        for result in (types.SimpleNamespace(returncode=1, stdout=b''),
                       types.SimpleNamespace(returncode=0, stdout=b'D\0'),
                       types.SimpleNamespace(returncode=0, stdout=b'D\0\xff\0')):
            with self.subTest(result=result):
                self.ns['readonly_git_diff'] = lambda root, args, result=result: result
                errors = self.check()
                self.assertTrue(errors)
                self.assertTrue(any('corpus-currentness:' in e for e in errors))

    def test_reader_has_real_fixed_population_and_guard_import(self):
        tree = ast.parse((ROOT/'scripts/check_reader_pilot.py').read_bytes())
        names = {a.asname or a.name for n in tree.body
                 if isinstance(n, ast.ImportFrom) and n.module == 'resolve_t20_v6_source'
                 for a in n.names}
        self.assertTrue({'CHECKPOINT_PUBLIC_COPY_PATHS', 'checkpoint_public_duplicate_paths'} <= names)


# Additive exact32 admission controls. Real original programs/native calls are forbidden.
ABK32_EXPECTED_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
ABK32_EXPECTED_RECORDS = {'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AQ_SOURCE_COMPATIBLE_ARCHITECTURE_MODELS_V2.yaml': ('bb110c6493c333eb7ae8b6b09610f53715424a4c',
                                                                                                                                                                  'b460af8e73d3db6db8ed6223dc24a548b5519efd175eeefca03433d76c690520',
                                                                                                                                                                  3307),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AR_PROVENANCE_ROOT_EVIDENCE_MODELS_V2.yaml': ('475c318bb1ae3b5db3f0fce01f06d4bf66724409',
                                                                                                                                                            'ab7398b15130cdf60bbc1131403a6dbb5008651d876ff56405b43b1716a29a18',
                                                                                                                                                            2004),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AV_NEUTRAL_BRIDGE_INTERPOLATION_MODELS_V2.yaml': ('3c89aa19631f03d2fc1814ad3045cc06bb49fd5c',
                                                                                                                                                                '991763b96ac886e37c4ff01dfb6e4f3961cda00b57ada958f97aa3b18ddd5a05',
                                                                                                                                                                1509),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AW_PROVENANCE_ROOT_ROBUST_DIAGNOSIS_MODELS_V2.yaml': ('0d0a7223aa0ff2ee6e4da155b12ee06df152874c',
                                                                                                                                                                    'be1e7519b3007a18bf856c4e0baf29b0684b729c6d4b42e753274c10198b457a',
                                                                                                                                                                    1444),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AX_SOURCE_TESTIMONY_WORLD_GATE_MODELS_V2.yaml': ('86b3609b228da4e42b50a365bc7b094413719437',
                                                                                                                                                               '1c3a637ff73691d0f4e7303384c17fbd1b4291626073ced5db4d448b58d611c9',
                                                                                                                                                               1461),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AZ_CROSSED_SEMANTIC_INTERVENTION_MODELS_V2.yaml': ('f7e067f1195c13211cd8a067c560ba96b4b49e54',
                                                                                                                                                                 '993a403134973bcd90c3c8ead4b9140ab7a4111f6866bf471150a97deae13f44',
                                                                                                                                                                 1149),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BA_INTERFACE_RELATIVE_CAUSAL_QUOTIENT_MODELS_V1.yaml': ('8c90bb5a7e6608f9219361fb21d14dcd374ab267',
                                                                                                                                                                      '9f01b79e842c9e25a9deccc1f316956a5f25ab52970a87c8a474d89529c66d02',
                                                                                                                                                                      1215),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BB_JOINT_CAUSAL_INTERFACE_MODELS_V1.yaml': ('cf33648d43be6aa32f9f6112abe4be83caeaa5c4',
                                                                                                                                                          'c71f4dd9e225f8fe8da3f5d581daaff8bc37bddfaf886691c068d82db558b053',
                                                                                                                                                          875),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BC_UNIVERSAL_INTERFACE_EXPERIMENT_PARITY_MODELS_V1.yaml': ('d8fe3c0b6b5e38d64a508a95c83ae1810e1a27fe',
                                                                                                                                                                         '82beb4c893c0d12eb9727d20ad1428b1aa45397ae567725ddfece1571b4c833c',
                                                                                                                                                                         660),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BD_LATENT_SOURCE_ORIENTATION_MODELS_V2.yaml': ('c20193aeee354f6fb17727e889062893cd8cc2c8',
                                                                                                                                                             'be48fe63092df4f66ff66a0fe52ffbf50c8bfd11f3c05ce67a443fb54bf4c02d',
                                                                                                                                                             2159),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BE_CROSS_LANE_JOINT_INTERACTION_MODELS_V2.yaml': ('69367d117baefe6702b7bcdc22042042bf8e3923',
                                                                                                                                                                '40e08b9ef186620e9eb988e7e556694bfc94b94e3dd308d15a682ca03dca2291',
                                                                                                                                                                1605),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BF_IMPERSONAL_LATENT_REALIZATION_MODELS_V2.yaml': ('36ad7d6244e5d54eeb650d0f360acd6a45a53c0c',
                                                                                                                                                                 '4ea76f85945aca04192fb5beb74db8b9d3d0307a254de2b329d917d39674aca7',
                                                                                                                                                                 2069),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BG_INTEGRATED_R5_COMMON_MODEL_V2.yaml': ('23ae320500f7788577a3a9e62f37786b93cee2a2',
                                                                                                                                                       '97d7482dbf3ed4b50de79699cedc77067323b095dfd6c7eb3afb557acdfcfcc4',
                                                                                                                                                       1769),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BH_TRUTH_CALIBRATED_CORRECTION_MODELS_V2.yaml': ('e272acb828534d7e09b890f07017e172fb9d7dd4',
                                                                                                                                                               '14bc65a43c165e7c71208fc873160cdcf88cc5be50e49a49cbb68adfbaf55f33',
                                                                                                                                                               1646),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BI_FINITE_ARTICULABILITY_MODELS_V2.yaml': ('ee15782926dbe3ae049c5fc9ccfa530f1866a58f',
                                                                                                                                                         '27a4e79b4b11916d4047ad7677db26735f886ed7cbb2b01d5bd89754f33da080',
                                                                                                                                                         1333),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BK_NECESSITY_CONCRETENESS_MODELS_V2.yaml': ('01adca7afe96d67a0da61ccb8787c9e267e9208e',
                                                                                                                                                          'd6e99abc7d0038a9ff47cb02809d52e8004251b79d5e2164b3aad0dcca66c616',
                                                                                                                                                          1082),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BA_ADMISSION_OVERLAY.yaml': ('132b73791a09d81358e33e1f7d9698959c9146a2',
                                                                                                                                        '49f6ed3dda0270e58cb85b44c762be4e31620af9deac7249eac364be899e90fa',
                                                                                                                                        1560),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BB_ADMISSION_OVERLAY.yaml': ('23e4ce4a982031b1730c365bca1ec6a3684ea436',
                                                                                                                                        '8dd3b5e550662103f8f00b647219d4756a9e182fd6a5b86ae2782812e1e730fe',
                                                                                                                                        1674),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BC_ADMISSION_OVERLAY.yaml': ('0cdaac12accc57d203c0272eda273279d2b792b8',
                                                                                                                                        'c9ead1aeaf5d93742865ef8015556fed11f85b9f9813e9a23c7804400683978a',
                                                                                                                                        1719),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BD_ADMISSION_OVERLAY.yaml': ('6546f5ba202e9fb5e256c22379f61a42069f6665',
                                                                                                                                        'bc66bf8cea8fa9f454ea2cf7c97a0a1e33d50521a1646c519f12c8adbd8e5ab2',
                                                                                                                                        1788),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BE_ADMISSION_OVERLAY.yaml': ('a532439c13d961df272781b0b7d49a6213d136a6',
                                                                                                                                        '12f4e83b712fa0d58b100169644aa17561a74fe6221466e50752d417c07f185b',
                                                                                                                                        1774),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AT_NEUTRAL_INTERVENTIONAL_TRACE_MODELS_V1.yaml': ('81939539fe9ae4b34412e9af80243b69dade62dd',
                                                                                                                                                                  '0ed0bc80aefa85b01a682fbd8d9f0c579b3316372f7dc50a7bd054e0787b7877',
                                                                                                                                                                  2379),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AV_NEUTRAL_BRIDGE_INTERPOLATION_MODELS_V1.yaml': ('8535624b656ca283113d322fecbc566290912f4e',
                                                                                                                                                                  '82cee72fcc9a4135275de39175a69d5b603ca62eaf2d3c9f87df9fabeed5c82c',
                                                                                                                                                                  1292),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AW_PROVENANCE_ROOT_ROBUST_DIAGNOSIS_MODELS_V1.yaml': ('6471321e88bf946175d204afb78650463332f70b',
                                                                                                                                                                      '132d6bc9ea2de7927682ff4822ad611c3f5d43af17329130df2aeeac13cb8b69',
                                                                                                                                                                      1042),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AX_SOURCE_TESTIMONY_WORLD_GATE_MODELS_V1.yaml': ('c7a8d6fa611e9a5f7535f701ceb66b0805fe7c17',
                                                                                                                                                                 'a5429ef4ae52c5a62c13eb56d9b2098673b2b04013a051e22aa87648c853b993',
                                                                                                                                                                 1549),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AZ_CROSSED_SEMANTIC_INTERVENTION_MODELS_V1.yaml': ('84eb89781eb35bbf74dfa74e78ee32bc332a7e89',
                                                                                                                                                                   'b5d353a56596143c1f02001e571e2d4bfd635331c08bf26530f6850b77c3a29f',
                                                                                                                                                                   955),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BD_LATENT_SOURCE_RELIABILITY_ORIENTATION_MODELS_V1.yaml': ('d8fb38df99a36119cdfd9d0cd7b027599d304256',
                                                                                                                                                                           '1433c3131749f686a2823fe0e9d7c27d6f6b1b4b64c05ff7d0bbd747bf3f5c6c',
                                                                                                                                                                           2345),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BE_CROSS_LANE_JOINT_INTERACTION_MODELS_V1.yaml': ('991381e40dbc0a041a79b3375bba389320c3af14',
                                                                                                                                                                  'bcc3caaf8ee5fe6910de9b0f4eb80939388fed07ae02e307437723a5a2825e72',
                                                                                                                                                                  1362),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BF_IMPERSONAL_LATENT_REALIZATION_MODELS_V1.yaml': ('7c94adf7f1f36a636ba8cf24139fcdea66269e9d',
                                                                                                                                                                   'db4f7664cd22dc28425e5fa5da03cac18645ec3b72856b87ec5f11aee5a104fb',
                                                                                                                                                                   1375),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BH_TRUTH_CALIBRATED_CORRECTION_MODELS_V1.yaml': ('3996ff60410db02f1ccd11f9cba4f36b1ba8f0b7',
                                                                                                                                                                 '864b04f56a250ed8ad05dacfbd4970a0343367a0b0feaecab2bba9de34a13066',
                                                                                                                                                                 1455),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BI_FINITE_ARTICULABILITY_MODELS_V1.yaml': ('68add8fc26f0f801b6e4b20ead7d5b93681be1cc',
                                                                                                                                                           '4a4e5b750c57c3b4a65934c7edd4de495a74ce00c0d8eadd511651bb93eda0e5',
                                                                                                                                                           910),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BK_NECESSITY_CONCRETENESS_MODELS_V1.yaml': ('19306d597907bb1fc1508e484d250b82e7905555',
                                                                                                                                                            '1317a7369c5daf99935a085cd03b8b60eeec87c3c6ce640f4494d17acab8f966',
                                                                                                                                                            1041)}

def _abk32_test_reader():
    import ast
    module = _central47_test_reader()
    ns = module.__dict__
    tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'check_abk_public_absences':
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.startswith('ABK_PUBLIC_HISTORY_'):
                    ns[target.id] = ast.literal_eval(node.value)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'actual-abk32-reader', 'exec'), ns)
    return module

class ABK32ProductionContractTests(unittest.TestCase):
    def test_exact32_native_identity_population_and_revision(self):
        module = _abk32_test_reader()
        self.assertEqual(getattr(module, 'ABK_PUBLIC_HISTORY_REVISION', None), ABK32_EXPECTED_REVISION)
        self.assertEqual(getattr(module, 'ABK_PUBLIC_HISTORY_RECORDS', None), ABK32_EXPECTED_RECORDS)

    def test_local_complete_pin_table_is_the_same_exact32_plus_revision(self):
        import ast
        tree = ast.parse((ROOT / 'scripts/check_reader_pilot.py').read_bytes())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == '_permitted_projection_consumer_pins')
        expected = {p: (*v, ABK32_EXPECTED_REVISION) for p, v in ABK32_EXPECTED_RECORDS.items()}
        matching = []
        for node in ast.walk(fn):
            if isinstance(node, ast.Dict):
                try: value = ast.literal_eval(node)
                except (ValueError, TypeError): continue
                if isinstance(value, dict) and set(value) == set(expected): matching.append(value)
        self.assertEqual(matching, [expected], 'one exact literal final pin population is mandatory')


class ABK32AbsenceTests(unittest.TestCase):
    """Only tiny synthetic files are written; original metadata paths remain exact."""
    def setUp(self):
        import types
        self.reader = _abk32_test_reader()
        self.assertTrue(callable(getattr(self.reader, 'check_abk_public_absences', None)),
                        'missing mandatory exact32 current-reader admission')
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.paths = sorted(ABK32_EXPECTED_RECORDS)
        self.bodies = {p: ('abk synthetic %02d\n' % i).encode() for i, p in enumerate(self.paths)}
        def identity(body):
            return (hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(),
                    hashlib.sha256(body).hexdigest(), len(body))
        self.identity = identity
        self.records = {p: identity(b) for p, b in self.bodies.items()}
        self.reader.ABK_PUBLIC_HISTORY_RECORDS = self.records
        self.reader.ABK_PUBLIC_HISTORY_REVISION = ABK32_EXPECTED_REVISION
        self.baseline = {p: dict(path=p, kind='blob', mode='100644', git_oid=v[0], bytes=v[2])
                         for p, v in self.records.items()}
        self.manifest = self.root / 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
        self.manifest.parent.mkdir(parents=True)
        self.document = {'schema': 'inert-central47-projection', 'objects': [
            dict(source_sha256=sha, source_action='include', source_bytes=size,
                 role='qualified_metadata', declared_eligibility_basis='reviewed_distribution_metadata',
                 required_dependencies=[], disposition='REUSE', repository_path=p,
                 public_sha256=sha, public_bytes=size, publication_basis='exact_existing_public_repository_object',
                 repository_revision=ABK32_EXPECTED_REVISION, git_blob=blob)
            for p, (blob, sha, size) in self.records.items()]}
        self.save_manifest()
        self.tree = b''.join(('100644 blob '+self.records[p][0]+'\t'+p+'\0').encode() for p in self.paths)
        self.index = b''; self.index_reads = 0; self.native_calls = []
        self.commit_type = b'commit\n'; self.bad_blob = False; self.failure = False
        self.index_drift = False; self.mutate_once = None
        def native(repo, *args):
            self.assertEqual(Path(repo), self.root)
            self.native_calls.append(args)
            if self.failure: raise ValueError('synthetic native evidence unavailable')
            if args == ('cat-file', '-t', ABK32_EXPECTED_REVISION): return self.commit_type
            if args == ('ls-tree', '-z', ABK32_EXPECTED_REVISION, '--', *self.paths): return self.tree
            if args == ('ls-files', '--stage', '-z', '--', *self.paths):
                self.index_reads += 1
                return b'changed\0' if self.index_drift and self.index_reads > 1 else self.index
            if len(args) == 3 and args[:2] == ('cat-file', 'blob'):
                found = [self.bodies[p] for p in self.paths if self.records[p][0] == args[2]]
                self.assertEqual(len(found), 1, 'only selected synthetic native blobs may be queried')
                if self.mutate_once:
                    effect, self.mutate_once = self.mutate_once, None
                    effect()
                return found[0] + (b'wrong' if self.bad_blob is True or self.bad_blob == args[2] else b'')
            raise AssertionError('unexpected native command '+repr(args))
        self.reader._administrative_git = native

    def save_manifest(self):
        self.manifest.write_text(json.dumps(self.document, sort_keys=True)+'\n')

    def present(self, path):
        p = self.root/path; p.parent.mkdir(parents=True, exist_ok=True);p.write_bytes(self.bodies[path]);return p

    def qualify(self):
        return self.reader.check_abk_public_absences(self.root, self.baseline)

    def refuse(self):
        absent, errors = self.qualify();self.assertEqual(absent, set());self.assertTrue(errors)

    def test_all32_absent_and_full_present(self):
        absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set(self.paths))
        for p in self.paths: self.present(p)
        absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set())

    def test_staged_absence_and_present_index_subsets_are_accepted(self):
        kept = set(self.paths[::3])
        for p in kept: self.present(p)
        # Original tracked entries can remain for unstaged absence; a subset
        # can remain after staged deletion. Both stay exact mode/blob/stage 0.
        for indexed in (self.paths, sorted(kept), []):
            self.index = b''.join(('100644 '+self.records[p][0]+' 0\t'+p+'\0').encode() for p in indexed)
            absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set(self.paths)-kept)

    def test_each_of13_projection_fields_is_required_and_exact(self):
        original = deepcopy(self.document)
        for field in original['objects'][0]:
            for mutate in ('missing', 'wrong'):
                with self.subTest(field=field, mutate=mutate):
                    self.document = deepcopy(original); row = self.document['objects'][0]
                    if mutate == 'missing': row.pop(field)
                    else: row[field] = ['unexpected'] if field == 'required_dependencies' else 'wrong'
                    self.save_manifest(); self.refuse()
        self.document = original;self.save_manifest()

    def test_each_selected_projection_row_is_mandatory(self):
        original = deepcopy(self.document)
        for i in range(32):
            with self.subTest(omitted=i):
                self.document = deepcopy(original);self.document['objects'].pop(i);self.save_manifest();self.refuse()

    def test_duplicate_extra_field_and_malformed_document_refuse(self):
        original = deepcopy(self.document)
        for kind in ('duplicate', 'extra-field', 'not-list', 'not-dict', 'bad-json'):
            with self.subTest(kind=kind):
                self.document = deepcopy(original)
                if kind == 'duplicate': self.document['objects'].append(deepcopy(self.document['objects'][0]))
                elif kind == 'extra-field': self.document['objects'][0]['extra'] = True
                elif kind == 'not-list': self.document['objects'] = {}
                elif kind == 'not-dict': self.document['objects'][0] = None
                self.save_manifest()
                if kind == 'bad-json': self.manifest.write_text('{')
                self.refuse()

    def test_unrelated_projection_rows_do_not_expand_absence_permission(self):
        unrelated = deepcopy(self.document['objects'][0]);unrelated['repository_path'] = 'unrelated.json'
        self.document['objects'].append(unrelated);self.save_manifest()
        absent, errors = self.qualify();self.assertEqual(errors, []);self.assertEqual(absent, set(self.paths));self.assertNotIn('unrelated.json', absent)

    def test_pathless_unrelated_projection_shapes_do_not_expand_permission(self):
        shapes = [
            {'source_sha256': 'a'*64, 'source_action': 'identity_only', 'disposition': 'IDENTITY_ONLY', 'availability': 'held_excluded', 'exclusion_categories': ['explicit_owner_private_custody_only']},
            {'source_sha256': 'b'*64, 'source_action': 'include', 'disposition': 'NOT_PUBLISHED'},
            {'source_sha256': 'c'*64, 'source_action': 'omit', 'disposition': 'IDENTITY_ONLY'},
        ]
        self.document['objects'].extend(shapes); self.save_manifest()
        absent, errors = self.qualify()
        self.assertEqual(errors, []); self.assertEqual(absent, set(self.paths))
        for path in self.paths: self.present(path)
        absent, errors = self.qualify()
        self.assertEqual(errors, []); self.assertEqual(absent, set())

    def test_pathless_or_malformed_selected_rows_still_refuse(self):
        original = deepcopy(self.document)
        for missing, value in [(True, None), (False, None), (False, 7), (False, [])]:
            with self.subTest(missing=missing, value=value):
                self.document = deepcopy(original)
                if missing: del self.document['objects'][0]['repository_path']
                else: self.document['objects'][0]['repository_path'] = value
                self.save_manifest(); self.refuse()

    def test_explicit_malformed_unrelated_path_still_refuses(self):
        original = deepcopy(self.document)
        for value in [None, 7, [], {}]:
            with self.subTest(value=value):
                self.document = deepcopy(original)
                self.document['objects'].append({'repository_path': value})
                self.save_manifest(); self.refuse()

    def test_original_census_each_mode_kind_blob_size_and_missing_refuse(self):
        path=self.paths[0]; original=deepcopy(self.baseline)
        for field,value in [('kind','tree'),('mode','100755'),('git_oid','0'*40),('bytes',1),('absent',None)]:
            with self.subTest(field=field):
                self.baseline=deepcopy(original)
                if field=='absent':self.baseline.pop(path)
                else:self.baseline[path][field]=value
                self.refuse()

    def test_noncommit_wrong_tree_and_native_blob_refuse(self):
        self.commit_type=b'blob\n';self.refuse();self.commit_type=b'commit\n'
        old=self.tree;self.tree=self.tree.replace(b'100644',b'100755',1);self.refuse();self.tree=old
        self.bad_blob=True;self.refuse()

    def test_missing_duplicate_extra_reordered_original_tree_refuse(self):
        original=self.tree; rows=original.split(b'\0')[:-1]
        for candidate in (rows[:-1],rows+rows[:1],rows+[b'100644 blob '+b'0'*40+b'\tunrelated'],list(reversed(rows))):
            with self.subTest(candidate=len(candidate)):
                self.tree=b'\0'.join(candidate)+b'\0';self.refuse()
        self.tree=original

    def test_conflict_wrong_mode_blob_extra_duplicate_and_unterminated_index_refuse(self):
        p=self.paths[0];r=('100644 '+self.records[p][0]+' 0\t'+p).encode()
        for candidate in (r.replace(b' 0\t',b' 1\t')+b'\0',r.replace(b'100644',b'100755')+b'\0',
                          r.replace(self.records[p][0].encode(),b'0'*40)+b'\0',r+b'\0'+r+b'\0',
                          r.replace(p.encode(),b'unrelated')+b'\0',r):
            with self.subTest(candidate=candidate[:20]):self.index=candidate;self.refuse()

    def test_every_selected_native_blob_is_authenticated(self):
        for path in self.paths:
            with self.subTest(path=path):
                self.bad_blob=self.records[path][0];self.refuse()
        self.bad_blob=False

    def test_empty_missing_or_extra_native_population_cannot_bypass_guard(self):
        original=self.records
        for changed in ({},dict(list(original.items())[:-1]),dict(original,unrelated=next(iter(original.values())))):
            with self.subTest(population=len(changed)):
                self.reader.ABK_PUBLIC_HISTORY_RECORDS=changed;self.refuse()
        self.reader.ABK_PUBLIC_HISTORY_RECORDS=original

    def test_native_refusal_does_not_admit_any_path(self):
        self.failure=True;self.refuse()

    def test_present_corrupt_symlink_hardlink_executable_directory_fifo_refuse(self):
        import os
        p=self.present(self.paths[0]);p.write_bytes(b'corrupt');self.refuse();p.unlink()
        target=self.root/'outside';target.write_bytes(self.bodies[self.paths[0]])
        p.symlink_to(target);self.refuse();p.unlink()
        os.link(target,p);self.refuse();p.unlink()
        self.present(self.paths[0]).chmod(0o755);self.refuse();p.chmod(0o644);p.unlink()
        p.mkdir();self.refuse();p.rmdir();os.mkfifo(p)
        with frontier_mock.patch.object(self.reader.os,'open',side_effect=OSError('FIFO must never open')) as opened:
            self.refuse();opened.assert_not_called()

    def test_manifest_missing_symlink_hardlink_executable_refuse(self):
        import os
        saved=self.manifest.read_bytes();self.manifest.unlink();self.refuse()
        other=self.root/'manifest-copy';other.write_bytes(saved)
        self.manifest.symlink_to(other);self.refuse();self.manifest.unlink()
        os.link(other,self.manifest);self.refuse();self.manifest.unlink()
        self.manifest.write_bytes(saved);self.manifest.chmod(0o755);self.refuse()

    def test_index_change_during_qualification_refuses(self):
        self.index_drift=True;self.refuse()

    def test_absent_to_present_and_present_to_absent_drift_refuse(self):
        self.mutate_once=lambda:self.present(self.paths[0]);self.refuse()
        p=self.root/self.paths[0];self.mutate_once=lambda:p.unlink();self.refuse()

    def test_equal_bytes_replacement_and_manifest_drift_refuse(self):
        p=self.present(self.paths[0])
        def replace():p.unlink();self.present(self.paths[0])
        self.mutate_once=replace;self.refuse()
        self.mutate_once=lambda:self.manifest.write_bytes(self.manifest.read_bytes()+b' ')
        self.refuse()


class ABK32OriginalPinControls(unittest.TestCase):
    PINS = {p: (*v, ABK32_EXPECTED_REVISION) for p,v in ABK32_EXPECTED_RECORDS.items()}
    def setUp(self):
        previous=Central47OriginalPinControls();previous.setUp()
        self.base=previous.base;self.prior=previous.current
        for p,(_,sha,size,_) in self.PINS.items():
            row=dict(repository_path=p,source_sha256=sha,public_sha256=sha,source_bytes=size,public_bytes=size,
                     disposition='REUSE',role='qualified_metadata',declared_eligibility_basis='reviewed_distribution_metadata',
                     required_dependencies=[],source_action='include',publication_basis='exact_existing_public_repository_object')
            for doc in (self.base.original,self.prior):doc['objects'].append(deepcopy(row))
        self.current=self.base.pinned(self.prior,self.PINS)

    def test_prior_reissue_stage_and_complete32_stage_remain_accepted(self):
        self.assertTrue(self.base.permitted(self.prior));self.assertTrue(self.base.permitted(self.current))

    def test_partial32_and_each_coordinate_identity_or_role_mutation_refuse(self):
        for path in self.PINS:
            for fields in (('repository_revision',),('git_blob',),('repository_revision','git_blob')):
                with self.subTest(path=path, fields=fields):
                    changed=deepcopy(self.current);r=next(r for r in changed['objects'] if r.get('repository_path')==path)
                    for field in fields:r.pop(field)
                    self.assertFalse(self.base.permitted(changed))
        p=next(iter(self.PINS))
        for field,value in [('repository_revision','HEAD'),('git_blob','0'*40),('source_sha256','0'*64),('public_sha256','0'*64),
                            ('source_bytes',1),('public_bytes',1),('role','authored_code'),('disposition','PROJECT'),
                            ('source_action','exclude'),('required_dependencies',['extra']),('publication_basis','other'),
                            ('declared_eligibility_basis','other')]:
            with self.subTest(field=field):
                changed=deepcopy(self.current);next(r for r in changed['objects'] if r.get('repository_path')==p)[field]=value
                self.assertFalse(self.base.permitted(changed))

    def test_missing_duplicate_reordered_extra_row_and_top_level_change_refuse(self):
        for kind in ('missing','duplicate','reordered','extra','metadata'):
            with self.subTest(kind=kind):
                changed=deepcopy(self.current)
                if kind=='missing':changed['objects'].pop()
                elif kind=='duplicate':changed['objects'].append(deepcopy(changed['objects'][-1]))
                elif kind=='reordered':changed['objects'].reverse()
                elif kind=='extra':changed['objects'].append({'repository_path':'unrelated'})
                else:changed['schema']='changed'
                self.assertFalse(self.base.permitted(changed))

    def test_no_original_identity_rebinding_or_prior_stage_omission(self):
        p=next(iter(self.PINS))
        for field,value in [('source_sha256','0'*64),('public_sha256','0'*64),('source_bytes',1),('public_bytes',1),('disposition','PROJECT')]:
            with self.subTest(field=field):
                original=deepcopy(self.base.original);current=deepcopy(self.current)
                for document in (original,current):next(r for r in document['objects'] if r.get('repository_path')==p)[field]=value
                self.assertFalse(self.base.permitted(current,original))
        prior_paths=set(Central47OriginalPinControls.PINS)|set(ReviewedReissueBwOriginalPinControls.PINS)|set(ReviewedCodexOriginalPinControls.PINS)
        for p in prior_paths:
            changed=deepcopy(self.current);r=next(r for r in changed['objects'] if r.get('repository_path')==p)
            r.pop('repository_revision');r.pop('git_blob');self.assertFalse(self.base.permitted(changed))

    def test_exact_candidate_delta_is_only_two_fields_for_all32(self):
        self.assertTrue(self.base.permitted(self.current))
        for p,(blob,sha,size,rev) in self.PINS.items():
            old=next(r for r in self.prior['objects'] if r.get('repository_path')==p)
            new=next(r for r in self.current['objects'] if r.get('repository_path')==p)
            self.assertEqual(new,dict(old,repository_revision=rev,git_blob=blob))


class ABK32CurrentnessTests(unittest.TestCase):
    def gate(self, changes, qualified):
        import inspect,types
        reader=_abk32_test_reader();fn=reader.check_corpus_currentness
        self.assertIn('abk_paths',inspect.signature(fn).parameters,'missing exact32 currentness parameter')
        reader.ABK_PUBLIC_HISTORY_RECORDS=ABK32_EXPECTED_RECORDS
        raw=''.join(status+'\0'+p+'\0' for status,p in changes).encode()
        reader.readonly_git_diff=lambda *a:types.SimpleNamespace(returncode=0,stdout=raw)
        return fn(Path('.'),'c'*40,abk_paths=qualified)

    def test_only_qualified_exact_D_paths_are_admitted(self):
        paths=sorted(ABK32_EXPECTED_RECORDS)
        self.assertEqual(self.gate([('D',p) for p in paths],set(paths)),[])
        self.assertEqual(self.gate([],set()),[])

    def test_unqualified_modified_added_renamed_and_unrelated_refuse(self):
        p=next(iter(ABK32_EXPECTED_RECORDS))
        for status in ('M','A','T'):
            with self.subTest(status=status):self.assertTrue(self.gate([(status,p)],{p}))
        self.assertTrue(self.gate([('D',p)],set()))
        self.assertTrue(self.gate([('D',p+'-other')],{p+'-other'}))
        self.assertTrue(self.gate([('D',p),('M','unrelated')],{p}))


class ABK32AllMemberControls(unittest.TestCase):
    # Reuse fixture helpers, not inherited test methods. Ordinary discovery
    # therefore runs each of the 33 additive methods exactly once.
    setUp = ABK32AbsenceTests.setUp
    save_manifest = ABK32AbsenceTests.save_manifest
    present = ABK32AbsenceTests.present
    qualify = ABK32AbsenceTests.qualify
    refuse = ABK32AbsenceTests.refuse
    def test_all_present_still_requires_all32_native_bodies(self):
        for path in self.paths: self.present(path)
        absent, errors = self.qualify()
        self.assertEqual(errors, []); self.assertEqual(absent, set())
        queried = [args[2] for args in self.native_calls if args[:2] == ('cat-file', 'blob')]
        self.assertEqual(__import__('collections').Counter(queried),
                         __import__('collections').Counter(v[0] for v in self.records.values()))

    def test_each_current_present_member_corruption_refuses(self):
        for path in self.paths: self.present(path)
        for path in self.paths:
            with self.subTest(path=path):
                file = self.root/path; file.write_bytes(b'corrupt')
                self.refuse(); file.write_bytes(self.bodies[path])


class ABK32MainDispatchTests(unittest.TestCase):
    def test_main_requires_central_then_abk_retains_both_errors_and_paths(self):
        import types
        reader=_abk32_test_reader(); events=[]
        central_selected={next(iter(CENTRAL47_EXPECTED_RECORDS))}
        abk_selected={next(iter(ABK32_EXPECTED_RECORDS))}
        reader.entries_at=lambda *a:[]
        reader.corpus_currentness_context=lambda *a:(({}, {}, {}, {}, {}),['context-sentinel'])
        reader.check_frontier_record_absences=lambda *a:(set(),['frontier-sentinel'])
        def central(repo,baseline):events.append(('central',baseline));return central_selected,['central-fatal-sentinel']
        def abk(repo,baseline):events.append(('abk',baseline));return abk_selected,['abk-fatal-sentinel']
        reader.check_central_public_absences=central
        reader.check_abk_public_absences=abk
        def currentness(*args,**kwargs):events.append(('currentness',args,kwargs));return ['currentness-sentinel']
        reader.check_corpus_currentness=currentness
        reader.check_collection_dispositions=lambda *a:['collection-sentinel']
        reader.check_collection_result_routes=lambda *a:['route-sentinel']
        reader.Counter=__import__('collections').Counter; reader.PROBES=set()
        reader.yaml=types.SimpleNamespace(safe_load=lambda _: {'artifacts':[]},YAMLError=ValueError)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);profile=root/'profile';profile.write_text('{}')
            reader.safe_path=lambda *a:profile
            owners={'schema':'orthemology-reader-owner-map-v1','external_body_admissions':[],
                    'baseline':{'commit':'c'*40},'collections':[],'publication_profile':'profile'}
            cross={'schema':'orthemology-reader-crosswalk-v1','coverage_stage':'reader-candidate'}
            errors=reader.check(root,owners,cross)
        self.assertEqual([e[0] for e in events],['central','abk','currentness'])
        self.assertEqual(events[0][1],{}); self.assertEqual(events[1][1],{})
        call=events[2]
        self.assertEqual(call[2].get('central_paths',call[1][8] if len(call[1])>8 else set()),central_selected)
        self.assertEqual(call[2].get('abk_paths',call[1][9] if len(call[1])>9 else set()),abk_selected)
        self.assertEqual(set(errors),{'context-sentinel','frontier-sentinel','central-fatal-sentinel',
                                     'abk-fatal-sentinel','currentness-sentinel','collection-sentinel','route-sentinel'})


if __name__ == "__main__":
    unittest.main()
