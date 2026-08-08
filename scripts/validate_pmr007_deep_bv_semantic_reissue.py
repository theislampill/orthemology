#!/usr/bin/env python3
"""Validate the bounded Deep BL-BV semantic custody reissue."""

import argparse
import hashlib
import importlib.util
import json
import pathlib
import re

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
AR8R_REL = pathlib.Path("docs/project-closure/ar8r-v11")
REISSUE_REL = AR8R_REL / "post-merge-proposals/pmr007-deep-bl-bv-semantic-reissue"
SOURCE_REL = REISSUE_REL / "source-files"
SOURCE_MANIFEST_REL = REISSUE_REL / "SOURCE_SHA256SUMS"
PROVENANCE_RECEIPT_REL = AR8R_REL / "provenance/AR8R-PMR007-DEEP-BL-BV-CUSTODY-REISSUE-V1.yaml"
BK_VALIDATOR_REL = pathlib.Path("scripts/validate_pmr007_deep_bk_public_snapshot.py")
PRIVATE_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/](?:Users|workspace|Temp|Documents|Downloads|Desktop)[\\/]|"
    r"(?<![A-Za-z0-9])/(?:home|Users|root|tmp|var/tmp|private/tmp)/|"
    r"/mnt/data/|sandbox:/|file://|chatgpt\.com/(?:c|g)/|data-message-id|"
    r"screen-threadFlyOut)"
)
EXPECTED_SOURCE_HASHES = {
    "AR8R_PMR007_CURRENT_CONTINUATION_AFTER_DEEP_BV.yaml": "33bb04fd451ce53cddc960b8d68644b94cc9e46d71c3a19fc0ccc907af2dc024",
    "AR8R_PMR007_CURRENT_CONTINUATION_AFTER_DEEP_BV.yaml.sha256": "1d65d1edd623065c56b04476f1f1d04ff1aac639b2bfa0bb6d0227909089c990",
    "AR8R_PMR007_DEEP_BL_BV_BOUNDARY_REPORT.md": "53cd9ed7e0bd238831a814e8a20ccc46f994e8cbc8027f1ed498ac140eb3561f",
    "AR8R_PMR007_DEEP_BL_BV_BOUNDARY_REPORT.md.sha256": "d32217936db92cd99ab45b314633c2cd77894af22001f265d520060059695328",
    "CURRENT_STATE_AFTER_DEEP_BV.yaml": "bc308dd3f282f97a3a37ee07e241f6ff23f28ff0d66f6d90364d5271f2716eb8",
    "EXTERNAL_PDF_CUSTODY_AND_METHOD_NOTE.md": "e0cf25a898886235ac1f2f0b330368328b2c57c36389f10c9fd5df3dcb9d229f",
    "EXTERNAL_PDF_CUSTODY_SANITIZED.json": "65a69b7988394234414ddbfe4f0b201fc00f0aa0020d907849e0774c67914c75",
    "LIVE_GITHUB_AUTHORITY_AFTER_BU.json": "860fb5dcb25a37ff268288b12a36745fa4ba20b0547f7e6351a7aa97da5ad4b1",
    "PMR-007_DEEP_BL_BU_OWNER_REPORT.md": "717128f8e57feaaf877fd9cce2f53a664b491fe7ff7842316e31be14ffe9c774",
    "PMR-007_DEEP_BV_ADMISSION_HASHES.sha256": "b56fc1918d77d262b62934720b9ed158ca69d003d0ddca00c96c082b9455122e",
    "PMR-007_DEEP_BV_ADMISSION_OVERLAY.yaml": "f773831cb11d784fecc50ec62bbaf79bf85faf4f78218b91e254228da224664b",
    "PMR-007_DEEP_BV_V1_COLD_AUDIT.md": "58863afd47ac8bf32c14ac119273cf5ac78918b46e966b558cce9cbe720f4f5d",
    "PMR-007_DEEP_BV_V2_DISTINCT_FRESH_REREVIEW.md": "e1a9efa1081ad3889bb4a64ddf4b662332a69247f6310d9f4807bcacbe4587fd",
    "PMR-007_DEEP_BV_V2_REPAIR_LOG.md": "13eb90032fbee8dd670ac0613de9629fe67bd3215e8c09e11814f16d8612e944",
    "PMR-007_DEEP_ROUND_BV_COMMON_INTERVENTION_IDENTIFIABILITY_V2.md": "d536605dbfb5cef0b16d9bcf13cf8a006ac861a1ade2241d9befd9879ecba77c",
    "PMR007_DEEP_BV_COMMON_INTERVENTION_MODELS_V2.yaml": "edf181477cdaea534cd23826b645587d5d278c4378ee23f0b193e2713e4aec95",
    "PMR007_DEEP_MENISCUS_CROSSWALK_A_BV_V4.yaml": "b33afb5f6e0d59049414827d7832e9e705f0104bc9e563c5d800da512ee3af5b",
    "PMR007_POST_BK_BURDEN_DELTA_BL_BV_V4.yaml": "a3f8ac872dd9cd9c9693a31226d4d4337e308e8d5b3a3ac645c5e866c1596edb",
    "PMR007_POST_BK_FORMALIZATION_QUEUE_THROUGH_BV_V4.yaml": "59265431d8b93edc58275a008a3b89535646cbf6ad514590d45301470d4ac4fd",
    "PMR007_POST_BK_PROPOSED_RESULT_INDEX_THROUGH_BV_V4.json": "47c04c0d42517e028488fef692ffb6dfb2442a80d8dcb063509c30f1935d017f",
    "PMR007_POST_BK_PROPOSED_RESULT_INDEX_THROUGH_BV_V4.yaml": "5d9fd83f92f097bc1e18a98f69f948b1803138bddf9a94fb08adedd45e851cb0",
    "pmr007_deep_bv_distinct_partition_experiment_rereview_results.json": "2ab9a872d22caa5913163799df0f7fc2e0927be7d822151c36d12135e9850fae",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_mapping(path, label, issues):
    if not path.is_file():
        issues.append(f"{label} is missing")
        return {}
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        issues.append(f"{label} is not valid UTF-8 YAML")
        return {}
    if not isinstance(document, dict):
        issues.append(f"{label} must be a mapping")
        return {}
    return document


def load_bk_validator(root, issues):
    path = root / BK_VALIDATOR_REL
    if not path.is_file():
        issues.append("Deep A-BK validator is missing")
        return None
    spec = importlib.util.spec_from_file_location("pmr007_bk_validator_for_bv", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(root=ROOT):
    root = pathlib.Path(root)
    source = root / SOURCE_REL
    issues = []
    actual_paths = set()
    private_path_findings = 0
    structured_parse_errors = 0
    source_hash_mismatches = 0
    manifest_path = root / SOURCE_MANIFEST_REL

    if source.is_dir():
        actual_paths = {
            path.relative_to(source).as_posix()
            for path in source.rglob("*")
            if path.is_file() or path.is_symlink()
        }
    else:
        issues.append("semantic-reissue source directory is missing")
    source_coverage_exact = actual_paths == set(EXPECTED_SOURCE_HASHES)
    if not source_coverage_exact:
        issues.append("semantic-reissue source coverage mismatch")

    for relative in sorted(actual_paths):
        target = source / pathlib.PurePosixPath(relative)
        if target.is_symlink():
            issues.append(f"semantic-reissue symlink is forbidden: {relative}")
            continue
        try:
            text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            issues.append(f"semantic-reissue member is not readable UTF-8: {relative}")
            continue
        private_path_findings += len(PRIVATE_PATTERN.findall(text))
        if relative.endswith((".yaml", ".yml")):
            try:
                yaml.safe_load(text)
            except yaml.YAMLError:
                structured_parse_errors += 1
        elif relative.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError:
                structured_parse_errors += 1
        expected = EXPECTED_SOURCE_HASHES.get(relative)
        if expected is None or sha256(target) != expected:
            source_hash_mismatches += 1

    if private_path_findings:
        issues.append("private path or browser locator leaked into semantic reissue")
    if structured_parse_errors:
        issues.append("semantic-reissue structured file parse failure")
    if source_hash_mismatches:
        issues.append("semantic-reissue source hash mismatch")

    expected_manifest = {
        f"source-files/{relative}": digest
        for relative, digest in EXPECTED_SOURCE_HASHES.items()
    }
    observed_manifest = {}
    manifest_malformed = False
    if manifest_path.is_file():
        try:
            manifest_lines = manifest_path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            manifest_lines = []
            manifest_malformed = True
        for line in manifest_lines:
            if not line.strip():
                continue
            parts = line.split(None, 1)
            if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{64}", parts[0]):
                manifest_malformed = True
                continue
            relative = parts[1]
            if relative in observed_manifest:
                manifest_malformed = True
            observed_manifest[relative] = parts[0]
    else:
        manifest_malformed = True
    source_manifest_exact = not manifest_malformed and observed_manifest == expected_manifest
    if not source_manifest_exact:
        issues.append("semantic-reissue SOURCE_SHA256SUMS mismatch")

    provenance = load_mapping(root / PROVENANCE_RECEIPT_REL, "custody reissue receipt", issues)
    linked = provenance.get("response_linked_custody", {})
    boundary = provenance.get("proposal_boundary", {})
    exact_original_response_linked_files = linked.get("exact_original_files")
    regenerated_response_linked_files = linked.get("regenerated_custody_copies")
    unavailable = linked.get("original_byte_sequences_still_unavailable")
    authority_ceiling_exact = (
        provenance.get("schema") == "ar8r-pmr007-deep-bl-bv-custody-reissue-v1"
        and provenance.get("source_reissue", {}).get("sha256")
        == "6ed381f16d2bbd46dd31a987bdc2b9552aa2ae083874dde650e75ff0794f27d3"
        and provenance.get("repository_copy", {}).get("source_files") == 22
        and provenance.get("repository_copy", {}).get("original_deep_bl_bv_bytes_claimed_for_all_source_files") is False
        and exact_original_response_linked_files == 2
        and regenerated_response_linked_files == 26
        and unavailable == 26
        and boundary.get("independently_rerun_from_reissue") is False
        and boundary.get("historical_identity_assigned") is False
        and boundary.get("historical_theorem_origin_credit") is False
        and boundary.get("owner_adoption") == "PENDING"
        and boundary.get("external_review") == "OPEN"
        and boundary.get("repository_scientific_adoption") == "NONE"
        and boundary.get("general_novelty_credit") == "NOT_GRANTED"
        and boundary.get("lean_source_or_kernel_claim") == "NONE"
        and boundary.get("integrated_champion") == "NONE"
        and boundary.get("meniscus") == "MENISCUS_NOT_REACHED"
        and boundary.get("natural_closure") == "NOT_REACHED"
        and provenance.get("integration", {}).get("private_archive_committed") is False
        and provenance.get("integration", {}).get("source_pdf_bytes_committed") is False
        and provenance.get("integration", {}).get("raw_chat_or_activity_committed") is False
    )
    if not authority_ceiling_exact:
        issues.append("semantic-reissue authority ceiling mismatch")

    result_path = source / "pmr007_deep_bv_distinct_partition_experiment_rereview_results.json"
    try:
        result_document = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        result_document = {}
    if result_document.get("independently_rerun_in_custody_repair") is not False:
        issues.append("transcribed Deep BV counts were promoted to executable reproduction")
    if result_document.get("authority_ceiling") != "CUSTODY_TRANSCRIPTION_NOT_EXECUTABLE_REPRODUCTION":
        issues.append("Deep BV experiment authority ceiling mismatch")
    executable_reproduction_established = False

    index = load_mapping(
        source / "PMR007_POST_BK_PROPOSED_RESULT_INDEX_THROUGH_BV_V4.yaml",
        "Deep BL-BV result index",
        issues,
    )
    results = index.get("results", []) if isinstance(index, dict) else []
    result_index_exact = (
        isinstance(results, list)
        and len(results) == 11
        and [row.get("round") for row in results] == [
            "Deep BL", "Deep BM", "Deep BN", "Deep BO", "Deep BP", "Deep BQ",
            "Deep BR", "Deep BS", "Deep BT", "Deep BU", "Deep BV",
        ]
        and all(row.get("identity") is None for row in results[:10])
        and results[-1].get("identity") == "PMR-007-CIID-1"
        and index.get("custody_class") == "SEMANTIC_REISSUE_OR_REGENERATED_CUSTODY_COPY"
        and index.get("original_bytes_proven_preserved") is False
    )
    if not result_index_exact:
        issues.append("Deep BL-BV result-index identity or custody mismatch")

    bk_validator = load_bk_validator(root, issues)
    if bk_validator is None:
        deep_bk_exact_snapshot_unchanged = False
    else:
        deep_bk_receipt = bk_validator.validate(root)
        deep_bk_exact_snapshot_unchanged = (
            deep_bk_receipt.get("result") == "PASS_WITH_PARTIAL_REPRODUCTION_CEILING"
            and deep_bk_receipt.get("snapshot_hash_mismatches") == 0
            and deep_bk_receipt.get("snapshot_manifest_coverage_exact") is True
        )
    if not deep_bk_exact_snapshot_unchanged:
        issues.append("exact Deep A-BK snapshot changed or failed validation")

    return {
        "schema": "ar8r-pmr007-deep-bv-semantic-reissue-validation-v1",
        "result": "FAIL" if issues else "PASS_WITH_SEMANTIC_REISSUE_CEILING",
        "source_files": len(actual_paths),
        "source_coverage_exact": source_coverage_exact,
        "source_hash_mismatches": source_hash_mismatches,
        "source_manifest_exact": source_manifest_exact,
        "structured_parse_errors": structured_parse_errors,
        "private_path_findings": private_path_findings,
        "exact_original_response_linked_files": exact_original_response_linked_files,
        "regenerated_response_linked_files": regenerated_response_linked_files,
        "original_response_linked_bytes_unavailable": unavailable,
        "authority_ceiling_exact": authority_ceiling_exact,
        "result_index_exact": result_index_exact,
        "deep_bk_exact_snapshot_unchanged": deep_bk_exact_snapshot_unchanged,
        "executable_reproduction_established": executable_reproduction_established,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    args = parser.parse_args()
    receipt = validate(args.root)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["result"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
