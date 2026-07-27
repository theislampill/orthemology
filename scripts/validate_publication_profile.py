#!/usr/bin/env python3
"""Validate the venue-neutral, deferred publication target profile."""
import argparse
import json
import pathlib
import sys

import yaml
from jsonschema import Draft202012Validator


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROFILE_PATH = pathlib.Path("docs/publication-profile.yaml")
SCHEMA_PATH = pathlib.Path("schemas/publication-profile.schema.json")

EXPECTED_MAPPING = {
    "orthemma-ortheme-systems-draft": [
        "manuscript/orthemma-ortheme-systems-revised-draft.md"
    ],
    "orthemic-core-reference-draft": [
        "theory/orthemic-core-formalization.md",
        "theory/orthemic-multi-actor-conflict-note.md",
    ],
    "orthability-ground-of-intelligibility-draft": [
        "companion/orthability-and-the-ground-of-intelligibility.md"
    ],
    "orthability-divine-speech-athari-draft": [
        "companion/orthability-divine-attributes-and-speech-athari.md"
    ],
    "dynamic-orthing-noetic-learning-orthability-draft": [
        "companion/dynamic-orthing-noetic-learning-and-orthability.md"
    ],
    "notation-gallery": ["docs/notation-gallery.md"],
}
BASE_QUALIFICATIONS = [
    "research-stage-draft",
    "not-peer-reviewed",
    "not-externally-peer-reviewed",
    "not-empirically-validated",
]
PAPER_QUALIFICATIONS = BASE_QUALIFICATIONS + [
    "candidate-terminology-not-adopted"
]
COMPANION_QUALIFICATIONS = PAPER_QUALIFICATIONS + [
    "philosophical-conclusions-conditional-on-stated-premises",
    "engineering-evidence-does-not-support-metaphysical-claims",
]
EXPECTED_QUALIFICATIONS = {
    "orthemma-ortheme-systems-draft": PAPER_QUALIFICATIONS,
    "orthemic-core-reference-draft": PAPER_QUALIFICATIONS,
    "orthability-ground-of-intelligibility-draft": COMPANION_QUALIFICATIONS,
    "orthability-divine-speech-athari-draft": PAPER_QUALIFICATIONS
    + [
        "philosophical-conclusions-conditional-on-stated-premises",
        "creed-internal-material-school-labeled",
        "engineering-evidence-does-not-support-metaphysical-claims",
    ],
    "dynamic-orthing-noetic-learning-orthability-draft": COMPANION_QUALIFICATIONS,
    "notation-gallery": BASE_QUALIFICATIONS,
}


def _schema(root):
    return json.loads((pathlib.Path(root) / SCHEMA_PATH).read_text(encoding="utf-8"))


def validate_profile_data(profile, schema=None):
    """Return deterministic issues for one parsed profile."""
    issues = []
    if schema is None:
        schema = _schema(ROOT)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(profile), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.absolute_path) or "<root>"
        issues.append("schema: %s: %s" % (path, error.message))

    artifacts = profile.get("artifacts", []) if isinstance(profile, dict) else []
    if not isinstance(artifacts, list):
        return issues

    by_id = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_id = artifact.get("artifact_id")
        if artifact_id in by_id:
            issues.append("duplicate artifact identity: %s" % artifact_id)
        by_id[artifact_id] = artifact

    actual_mapping = {
        artifact_id: artifact.get("sources")
        for artifact_id, artifact in by_id.items()
    }
    if actual_mapping != EXPECTED_MAPPING:
        issues.append("source-to-artifact mapping must preserve exact seven-to-six ownership")

    bibliography_owner = (
        profile.get("source_ownership", {}).get("bibliography_owner")
        if isinstance(profile, dict)
        else None
    )
    for artifact_id, artifact in by_id.items():
        if artifact.get("bibliography_owner") != bibliography_owner:
            issues.append("bibliography owner conflict for %s" % artifact_id)

    diagnostic = [
        artifact
        for artifact in artifacts
        if isinstance(artifact, dict)
        and artifact.get("profile_kind") == "diagnostic-reference"
    ]
    if (
        len(diagnostic) != 1
        or diagnostic[0].get("artifact_id") != "notation-gallery"
        or diagnostic[0].get("exception")
        != {
            "exception_id": "notation-gallery-diagnostic-reference",
            "reason": "notation-symbol-diagnostic-reference",
        }
    ):
        issues.append("diagnostic-reference exception must be singular and explicit")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        if artifact.get("profile_kind") == "technical-paper" and "exception" in artifact:
            issues.append("diagnostic-reference exception may not attach to a technical paper")
        qualifications = artifact.get("source_qualifications")
        artifact_id = artifact.get("artifact_id")
        if qualifications != EXPECTED_QUALIFICATIONS.get(artifact_id):
            issues.append(
                "source qualifications missing for %s"
                % (artifact_id or "<unknown>")
            )
    return issues


def validate_profile(root=ROOT):
    root = pathlib.Path(root)
    try:
        profile = yaml.safe_load((root / PROFILE_PATH).read_text(encoding="utf-8"))
        schema = _schema(root)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return ["profile load: %s" % exc]
    return validate_profile_data(profile, schema)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    args = parser.parse_args(argv)
    issues = validate_profile(args.root)
    for issue in issues:
        print("[FAIL] %s" % issue)
    if not issues:
        print("[PASS] publication profile schema and semantic ownership")
    print("TOTAL: %d failures" % len(issues))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
