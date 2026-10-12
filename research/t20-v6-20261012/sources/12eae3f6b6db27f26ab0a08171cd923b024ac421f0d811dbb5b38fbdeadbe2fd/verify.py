#!/usr/bin/env python3
"""Verify this exact claim-review packet and, optionally, its source return."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(base, name):
    rel = Path(name)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"unsafe member: {name}")
    path = (base / rel).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError(f"escaping member: {name}")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "MANIFEST.json").read_text())
    for row in manifest["files"]:
        path = contained(here, row["path"])
        assert path.is_file(), row["path"]
        assert path.stat().st_size == row["bytes"], row["path"]
        assert digest(path) == row["sha256"], row["path"]
    freeze = json.loads((here / "report-snapshot/REPORT_FREEZE.json").read_text())
    for row in freeze["files"]:
        path = contained(here / "report-snapshot", row["path"])
        assert path.stat().st_size == row["bytes"], row["path"]
        assert digest(path) == row["sha256"], row["path"]
    checked = 0
    if args.package_root:
        record = json.loads((here / "REFERENCE_CHECK.json").read_text())
        for row in record["entries"]:
            path = contained(args.package_root, row["path"])
            assert path.is_file(), row["path"]
            assert path.stat().st_size == row["bytes"], row["path"]
            assert digest(path) == row["sha256"], row["path"]
            checked += 1
    print(json.dumps({"status": "PASS_PACKET_INTEGRITY", "payload_files": len(manifest["files"]),
                      "frozen_reader_files": len(freeze["files"]), "package_members_checked": checked,
                      "scope": "Integrity checks only; ordinary claim review is in FRESH_REVIEW.md."}, sort_keys=True))


if __name__ == "__main__":
    main()
