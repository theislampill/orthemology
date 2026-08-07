#!/usr/bin/env python3
"""Focused schema tests for the Task 13-verified publication target profile."""
import copy
import importlib.util
import json
import pathlib
import unittest

import yaml
from jsonschema import Draft202012Validator


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "publication-profile.schema.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate_publication_profile.py"

if VALIDATOR_PATH.is_file():
    SPEC = importlib.util.spec_from_file_location(
        "validate_publication_profile", VALIDATOR_PATH
    )
    VALIDATOR = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(VALIDATOR)
else:
    VALIDATOR = None


SOURCES = [
    "manuscript/orthemma-ortheme-systems-revised-draft.md",
    "theory/orthemic-core-formalization.md",
    "theory/orthemic-multi-actor-conflict-note.md",
    "companion/orthability-and-the-ground-of-intelligibility.md",
    "companion/orthability-divine-attributes-and-speech-athari.md",
    "companion/dynamic-orthing-noetic-learning-and-orthability.md",
    "docs/notation-gallery.md",
]


def valid_profile():
    artifact_rows = [
        (
            "orthemma-ortheme-systems-draft",
            [SOURCES[0]],
            "technical-paper",
        ),
        (
            "orthemic-core-reference-draft",
            [SOURCES[1], SOURCES[2]],
            "technical-paper",
        ),
        (
            "orthability-ground-of-intelligibility-draft",
            [SOURCES[3]],
            "technical-paper",
        ),
        (
            "orthability-divine-speech-athari-draft",
            [SOURCES[4]],
            "technical-paper",
        ),
        (
            "dynamic-orthing-noetic-learning-orthability-draft",
            [SOURCES[5]],
            "technical-paper",
        ),
        ("notation-gallery", [SOURCES[6]], "diagnostic-reference"),
    ]
    artifacts = []
    for artifact_id, sources, kind in artifact_rows:
        qualifications = [
            "research-stage-draft",
            "not-peer-reviewed",
            "not-externally-peer-reviewed",
            "not-empirically-validated",
        ]
        if kind == "technical-paper":
            qualifications.append("candidate-terminology-not-adopted")
        if artifact_id in {
            "orthability-ground-of-intelligibility-draft",
            "orthability-divine-speech-athari-draft",
            "dynamic-orthing-noetic-learning-orthability-draft",
        }:
            qualifications.extend(
                [
                    "philosophical-conclusions-conditional-on-stated-premises",
                    "engineering-evidence-does-not-support-metaphysical-claims",
                ]
            )
        if artifact_id == "orthability-divine-speech-athari-draft":
            qualifications.insert(
                -1, "creed-internal-material-school-labeled"
            )
        row = {
            "artifact_id": artifact_id,
            "profile_kind": kind,
            "sources": sources,
            "bibliography_owner": "references/orthemology.bib",
            "source_qualifications": qualifications,
            "appendix_mode": (
                "single-column"
                if artifact_id == "orthemma-ortheme-systems-draft"
                else "none"
            ),
        }
        if kind == "diagnostic-reference":
            row["exception"] = {
                "exception_id": "notation-gallery-diagnostic-reference",
                "reason": "notation-symbol-diagnostic-reference",
            }
        artifacts.append(row)
    return {
        "schema": "orthemology-publication-profile-v1",
        "profile_id": "generic-arxiv-compatible-two-column-technical-paper",
        "compatibility_claim": (
            "A venue-neutral, generic arXiv-compatible two-column technical "
            "paper with full-width front matter and single-column technical "
            "appendices."
        ),
        "status": {
            "target_state": "task-13-verified",
            "current_artifact_conformance": "verified-against-declared-profile",
            "venue_selection": "none",
            "submission": "not-submitted",
            "processing": "not-claimed",
            "endorsement": "not-claimed",
            "acceptance": "not-claimed",
            "publication": "not-claimed",
        },
        "source_ownership": {
            "substantive_prose_owner": "authoritative-markdown-sources",
            "generated_latex_semantic_edits": "prohibited",
            "bibliography_owner": "references/orthemology.bib",
        },
        "source_provenance": {
            "source_commit": "d7309d30612ff85ed8f94b93d4a5a610c18b3ea9",
            "source_tree": "cded0130b092d2d13e288d6829298ec3f651e982",
            "source_date_epoch": 1786022580,
            "independently_reviewed_equivalent_source_commit": (
                "d7309d30612ff85ed8f94b93d4a5a610c18b3ea9"
            ),
            "independently_reviewed_equivalent_source_tree": (
                "cded0130b092d2d13e288d6829298ec3f651e982"
            ),
            "source_tree_equivalence": "verified-identical",
        },
        "toolchain": {
            "driver": "latexmk",
            "engine": "pdflatex",
            "tex_live_generation": "texlive-2025",
            "bibliography_processor": "bibtex",
            "shell_escape": "disabled",
            "environment_dependencies": "declared-only",
            "absolute_paths": "prohibited",
            "font_source": "tex-live-distribution-only",
            "lock": "publication/toolchain-lock.yaml",
            "tex_live_package_identities": [
                "fvextra",
                "fancyvrb",
                "etoolbox",
                "upquote",
                "textcomp",
                "lineno",
                "keyval",
            ],
        },
        "package_policy": {
            "policy": "closed",
            "direct_packages": [
                "amsmath",
                "amssymb",
                "booktabs",
                "geometry",
                "hyperref",
                "microtype",
                "natbib",
                "needspace",
                "xcolor",
            ],
            "supported_packages": [
                "amsmath",
                "amssymb",
                "booktabs",
                "geometry",
                "hyperref",
                "microtype",
                "natbib",
                "needspace",
                "xcolor",
                "fvextra",
            ],
            "conversion_steps": "prohibited",
            "files_outside_package": "prohibited",
            "stale_auxiliary_files": "prohibited",
        },
        "layout": {
            "document_class": "article",
            "font_size_pt": 10,
            "paper_size": "us-letter",
            "body_columns": 2,
            "references_columns": 2,
            "front_matter": "full-width-title-and-abstract",
            "technical_appendices": "single-column",
        },
        "hard_limits": {
            "overfull_box_tolerance_pt": 5,
            "page_count": "none",
            "source_package_bytes": "none",
            "runaway_page_guard": 500,
        },
        "appendix_policy": "technical-appendices-single-column",
        "source_package": {
            "owner": "scripts/build_pdfs.py",
            "entry_point": "main.tex",
            "one_package_per_artifact": True,
            "self_contained": True,
            "archive_layout": "repository-relative",
            "build_workdir": "publication/latex/<artifact_id>",
            "bibliography_path": "references/orthemology.bib",
            "compatibility_inputs": [
                "publication/latexmkrc",
                "publication/pdftex-unicode-compat.tex",
            ],
        },
        "gates": {
            "provenance": "verified-task-13",
            "font_embedding": "verified-task-13",
            "text_extraction": "verified-task-13",
            "source_packaging": "verified-task-13",
            "clean_build": "verified-task-13",
            "visual_qa": "verified-task-13",
        },
        "artifacts": artifacts,
    }


def profile_issues(profile):
    validate = (
        getattr(VALIDATOR, "validate_profile_data", None) if VALIDATOR else None
    )
    return [] if validate is None else validate(profile)


class PublicationProfileSchemaTests(unittest.TestCase):
    def test_schema_exists_and_is_valid_draft_2020_12(self):
        self.assertTrue(SCHEMA_PATH.is_file(), SCHEMA_PATH)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_valid_profile_conforms_to_schema_and_semantics(self):
        self.assertTrue(SCHEMA_PATH.is_file(), SCHEMA_PATH)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        schema_issues = sorted(
            error.message
            for error in Draft202012Validator(schema).iter_errors(valid_profile())
        )
        self.assertEqual(schema_issues, [])
        self.assertEqual(profile_issues(valid_profile()), [])


class PublicationProfileMutationTests(unittest.TestCase):
    def assertIssue(self, profile, fragment):
        issues = profile_issues(profile)
        self.assertTrue(any(fragment in issue for issue in issues), issues)

    def test_rejects_missing_entry_point_and_owner_fields(self):
        for path in (
            ("source_package", "entry_point"),
            ("source_package", "owner"),
            ("source_ownership", "bibliography_owner"),
            ("source_provenance", "source_commit"),
            ("source_provenance", "source_tree"),
            ("source_provenance", "source_date_epoch"),
            (
                "source_provenance",
                "independently_reviewed_equivalent_source_commit",
            ),
            ("toolchain", "engine"),
            ("toolchain", "tex_live_generation"),
            ("toolchain", "bibliography_processor"),
            ("toolchain", "lock"),
            ("toolchain", "tex_live_package_identities"),
            ("hard_limits", "overfull_box_tolerance_pt"),
            ("hard_limits", "runaway_page_guard"),
        ):
            with self.subTest(path=path):
                profile = valid_profile()
                profile[path[0]].pop(path[1])
                self.assertIssue(profile, "schema:")

    def test_rejects_conflicting_bibliography_owner_and_mapping_drift(self):
        profile = valid_profile()
        profile["artifacts"][0]["bibliography_owner"] = "references/source-status.yaml"
        self.assertIssue(profile, "bibliography owner")

        profile = valid_profile()
        profile["artifacts"][0]["sources"] = [SOURCES[1]]
        self.assertIssue(profile, "source-to-artifact mapping")

    def test_rejects_unrecorded_or_multiple_diagnostic_exceptions(self):
        profile = valid_profile()
        profile["artifacts"][0]["profile_kind"] = "diagnostic-reference"
        profile["artifacts"][0]["exception"] = copy.deepcopy(
            profile["artifacts"][-1]["exception"]
        )
        self.assertIssue(profile, "diagnostic-reference exception")

        profile = valid_profile()
        profile["artifacts"][-1].pop("exception")
        self.assertIssue(profile, "diagnostic-reference exception")

    def test_rejects_venue_or_status_fabrication(self):
        mutations = [
            ("compatibility_claim", None, "official venue template"),
            ("status", "venue_selection", "selected"),
            ("status", "submission", "submitted"),
            ("status", "acceptance", "accepted"),
            ("status", "publication", "published"),
            ("status", "current_artifact_conformance", "officially-conforming"),
        ]
        for owner, key, value in mutations:
            with self.subTest(owner=owner, key=key):
                profile = valid_profile()
                if key is None:
                    profile[owner] = value
                else:
                    profile[owner][key] = value
                self.assertIssue(profile, "schema:")

    def test_rejects_unsafe_toolchain_and_package_dependencies(self):
        mutations = [
            ("toolchain", "shell_escape", "enabled"),
            ("toolchain", "environment_dependencies", "hidden"),
            ("toolchain", "absolute_paths", "allowed"),
            ("toolchain", "font_source", "system-font"),
        ]
        for owner, key, value in mutations:
            with self.subTest(key=key):
                profile = valid_profile()
                profile[owner][key] = value
                self.assertIssue(profile, "schema:")

        profile = valid_profile()
        profile["package_policy"]["supported_packages"].append(
            "unlisted-package"
        )
        self.assertIssue(profile, "schema:")

        for field in ("direct_packages", "supported_packages"):
            profile = valid_profile()
            profile["package_policy"].pop(field)
            self.assertIssue(profile, "schema:")

        profile = valid_profile()
        profile["package_policy"]["direct_packages"].remove("xcolor")
        self.assertIssue(profile, "direct package policy")

        profile = valid_profile()
        profile["package_policy"]["direct_packages"].append("fvextra")
        self.assertIssue(profile, "direct package policy")

        profile = valid_profile()
        profile["package_policy"]["supported_packages"].remove("fvextra")
        self.assertIssue(profile, "supported package policy")

        profile = valid_profile()
        profile["package_policy"]["supported_packages"].insert(0, "fvextra")
        profile["package_policy"]["supported_packages"].pop()
        self.assertIssue(profile, "supported package policy")

        profile = valid_profile()
        profile["toolchain"]["tex_live_package_identities"].remove("fancyvrb")
        self.assertIssue(profile, "schema:")

    def test_rejects_undeclared_limit_missing_appendix_policy_or_qualifications(self):
        profile = valid_profile()
        profile["hard_limits"]["page_count"] = 12
        self.assertIssue(profile, "schema:")

        profile = valid_profile()
        profile.pop("appendix_policy")
        self.assertIssue(profile, "schema:")

        profile = valid_profile()
        profile["artifacts"][0]["source_qualifications"].clear()
        self.assertIssue(profile, "source qualifications")

        profile = valid_profile()
        profile["artifacts"][0]["source_qualifications"].pop()
        self.assertIssue(profile, "source qualifications")

    def test_closed_identity_fields_reject_unlisted_vocabulary(self):
        mutations = [
            ("profile_id", "unlisted-profile-label"),
            ("artifact_id", "unlisted-artifact-label"),
            ("reason", "unlisted-exception-label"),
            ("owner", "unlisted-package-owner"),
        ]
        for field, value in mutations:
            with self.subTest(field=field):
                profile = valid_profile()
                if field == "profile_id":
                    profile["profile_id"] = value
                elif field == "artifact_id":
                    profile["artifacts"][0]["artifact_id"] = value
                elif field == "reason":
                    profile["artifacts"][-1]["exception"]["reason"] = value
                else:
                    profile["source_package"]["owner"] = value
                self.assertIssue(profile, "schema:")


if __name__ == "__main__":
    unittest.main()
