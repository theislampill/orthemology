#!/usr/bin/env python3
"""Verify compact custody; optionally replay with seven exact external sources.

Uses only the Python 3 standard library. Writes no package/source files.
Historical/source-world authentication and semantic truth are outside its scope.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe_path(root, rel):
    p = root / rel
    require(not Path(rel).is_absolute() and ".." not in Path(rel).parts,
            f"Unsafe path: {rel}")
    require(not p.is_symlink(), f"Symlink disallowed: {rel}")
    return p


def verify(root, external_root=None):
    manifest = load(root / "PACKET_MANIFEST.json")
    expected_paths = {r["path"] for r in manifest["files"]}
    require(len(expected_paths) == len(manifest["files"]), "Duplicate manifest paths")
    actual_paths = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}
    require(actual_paths == expected_paths | {"PACKET_MANIFEST.json"}, "Package inventory mismatch")
    for r in manifest["files"]:
        p = safe_path(root, r["path"])
        require(p.stat().st_size == r["bytes"] and digest(p) == r["sha256"],
                f"Package byte mismatch: {r['path']}")
    deps = load(root / "EXTERNAL_DEPENDENCIES.json")["full_source_dependencies"]
    depmap = {r["path"]: r for r in deps}
    require(len(depmap) == 7, "Expected exactly seven omitted full source objects")
    author = root / "wise-reason-asymmetry-20261010"
    review = root / "wise-reason-independent-review-20261010"
    included_bindings = external_bindings = 0

    def identity(rel, sha, size=None):
        nonlocal included_bindings, external_bindings
        p = safe_path(root, rel)
        if p.exists():
            require(digest(p) == sha and (size is None or p.stat().st_size == size),
                    f"Bound included file mismatch: {rel}")
            included_bindings += 1
        else:
            require(rel in depmap, f"Unaccounted missing dependency: {rel}")
            d = depmap[rel]
            require(d["sha256"] == sha and (size is None or d["bytes"] == size),
                    f"External dependency pin mismatch: {rel}")
            external_bindings += 1

    before = load(review / "ORIGINALS_BEFORE.json")["files"]
    for r in before:
        identity(r["path"], r["sha256"], r["bytes"])
    checks = load(review / "BINDING_VERIFICATION.json")["checks"]
    for c in checks:
        require(c["hash_match"] and c["bytes_match"], "Inherited binding attestation failed")
        identity(c["path"], c["expected_sha256"])
    for base in [author, review]:
        for r in load(base / "MANIFEST.json")["files"]:
            p = safe_path(base, r["path"])
            require(digest(p) == r["sha256"] and p.stat().st_size == r["bytes"],
                    f"Frozen internal manifest mismatch: {p}")
    evidence = load(review / "EVIDENCE_CHECK.json")["records"]
    for c in evidence:
        p = safe_path(root, c["path"])
        require(digest(p) == c["source_sha256"] and c["quote"] in p.read_text(encoding="utf-8"),
                f"Exact excerpt mismatch: {c['id']}")
    recorded = load(review / "EXTRACTION_CHECK.json")["checks"]
    require(len(recorded) == 11 and all(c["exact_match"] for c in recorded),
            "Inherited extraction record mismatch")
    require(len(list((author / "sources").glob("*.txt"))) == 11, "Selection count mismatch")
    for r in load(root / "wise-reason-root-20261010/MIFTAH_READING_BINDINGS.json")["readings"]:
        require(digest(root / r["path"]) == r["sha256"], "Root Miftah binding mismatch")
    source_root_record = load(root / "wise-reason-root-20261010/READING_BINDING.json")
    require(depmap[source_root_record["source_path"]]["sha256"] == source_root_record["sha256"],
            "Root Shifa source pin mismatch")
    json_count = 0
    for p in root.rglob("*.json"):
        load(p)
        json_count += 1
    result = {
        "status": "PASS_COMPACT_CUSTODY",
        "manifest_file_count": len(manifest["files"]),
        "author_frozen_report_sha256": digest(author / "REPORT.md"),
        "independent_review_sha256": digest(review / "REVIEW.md"),
        "included_binding_checks": included_bindings,
        "external_pin_consistency_checks": external_bindings,
        "full_sources_omitted": len(deps),
        "exact_included_arabic_excerpts": len(evidence),
        "json_files_parsed": json_count,
        "inherited_extraction_attestations": len(recorded),
        "fresh_selection_reextractions": 0,
        "standalone_raw_source_reextraction": False,
        "historical_or_source_world_authentication": False,
        "metaphysical_or_source_premise_validation": False,
        "integration": False,
        "closure": False,
    }
    if external_root is not None:
        for d in deps:
            p = safe_path(external_root, d["path"])
            require(p.is_file() and p.stat().st_size == d["bytes"] and digest(p) == d["sha256"],
                    f"Exact external object missing or mismatched: {d['path']}")
        for c in recorded:
            selection = root / c["selection"]
            body = (external_root / c["source"]).read_text(encoding="utf-8")
            name = selection.name
            if name.startswith("MIFTAH"):
                lo, hi = map(int, re.fullmatch(r"MIFTAH_2_(\d+)_(\d+)\.txt", name).groups())
                prior, terminal = f"(2/{lo-1})", f"(2/{hi})"
                start = body.index(prior) + len(prior)
                end = body.index(terminal, start) + len(terminal)
                rebuilt = body[start:end].replace("\x0b", "\n").replace("\x01", "")
            else:
                lo, hi = map(int, re.fullmatch(r"SHIFA_e(\d+)_e(\d+)\.txt", name).groups())
                start = body.index(f"ص -{lo}-")
                end = body.index(f"ص -{hi+1}-", start)
                rebuilt = body[start:end]
            require(rebuilt.encode("utf-8") == selection.read_bytes(),
                    f"Fresh extraction mismatch: {c['selection']}")
        body = (external_root / source_root_record["source_path"]).read_text(encoding="utf-8")
        root_selection = body[body.index("ص -179-"):body.index("ص -194-")].encode("utf-8")
        require(root_selection == (root / "wise-reason-root-20261010/SHIFA_e179_e193.txt").read_bytes(),
                "Root continuous selection extraction mismatch")
        # Run the unchanged review script with relative layout preserved, in a disposable copy.
        with tempfile.TemporaryDirectory(prefix="wise-reason-custody-") as tmp:
            replay = Path(tmp) / "packet"
            shutil.copytree(root, replay)
            for d in deps:
                target = replay / d["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(external_root / d["path"], target)
            run = subprocess.run([sys.executable, str(replay / "wise-reason-independent-review-20261010/verify_review.py")],
                                 cwd=replay, text=True, capture_output=True)
            require(run.returncode == 0, f"Unchanged review checker failed: {run.stdout}\n{run.stderr}")
        result.update({
            "status": "PASS_COMPACT_CUSTODY_AND_SOURCE_ASSISTED_REPLAY",
            "external_source_objects_freshly_hash_verified": len(deps),
            "fresh_selection_reextractions": len(recorded),
            "fresh_root_selection_reextractions": 1,
            "existing_review_checker": {
                "path": "wise-reason-independent-review-20261010/verify_review.py",
                "sha256": digest(review / "verify_review.py"),
                "returncode": run.returncode,
                "stdout": run.stdout,
                "stderr": run.stderr,
                "scope_note": "The unchanged checker validates recorded extraction booleans; fresh re-extraction is the additional separate check above.",
            },
        })
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external-root", type=Path,
                        help="Root containing the seven exact dependency paths; no network retrieval")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(Path(__file__).resolve().parent,
                                args.external_root.resolve() if args.external_root else None),
                         ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}), file=sys.stderr)
        sys.exit(1)
