#!/usr/bin/env python3
"""Read-only census of an explicitly pinned public Git commit.

Enumerates every tracked object, not only familiar paper extensions. Counts are
file/object counts, never works, results, reading, acceptance or independent
evidence. Owners are explicit discovery bindings, not inferred scientific owners.
No working-tree files, URLs, submodule bodies or bibliographic chains are read.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def git_bytes(repo, *args):
    result = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise ValueError("Git object read failed: " + result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def valid_owner(path):
    return (
        isinstance(path, str) and bool(path) and not path.startswith("/")
        and "\\" not in path and all(p not in ("", ".", "..") for p in path.split("/"))
    )


def census(repo, ref, *, owners=(), include_entries=False):
    """Return deterministic identity metadata; never classify a theorem as proved."""
    if not isinstance(ref, str) or re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", ref) is None:
        raise ValueError("An exact full lowercase commit object ID is required, not a moving ref")
    commit = git_bytes(repo, "rev-parse", "--verify", ref + "^{commit}").decode("ascii").strip()
    if commit != ref:
        raise ValueError("The supplied object is not the requested commit identity")
    tree = git_bytes(repo, "rev-parse", "--verify", ref + "^{tree}").decode("ascii").strip()
    raw = git_bytes(repo, "ls-tree", "-r", "-l", "-z", "--full-tree", ref)
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, path_bytes = record.split(b"\t", 1)
            mode, kind, oid, size = metadata.decode("ascii").split()
            path = path_bytes.decode("utf-8", errors="strict")
            if kind not in ("blob", "commit"):
                raise ValueError("unexpected recursive Git entry type")
            entry = {"path": path, "mode": mode, "kind": kind,
                     "git_oid": oid, "bytes": None if size == "-" else int(size)}
        except (ValueError, UnicodeError) as exc:
            raise ValueError("Cannot losslessly represent a tracked tree entry") from exc
        entries.append(entry)
    entries.sort(key=lambda row: row["path"])
    indexed = {row["path"]: row for row in entries}
    if len(indexed) != len(entries):
        raise ValueError("Duplicate tracked path")
    owners = list(owners)
    if any(not valid_owner(path) for path in owners) or len(set(owners)) != len(owners):
        raise ValueError("Owner bindings must be unique repository-relative paths")
    selected = []
    for path in sorted(owners):
        entry = indexed.get(path)
        if entry is None or entry["kind"] != "blob" or entry["mode"] not in ("100644", "100755"):
            raise ValueError("Owner is missing or not a regular tracked source: " + path)
        selected.append(dict(entry))
    blobs = [entry for entry in entries if entry["kind"] == "blob"]
    canonical = json.dumps(entries, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    result = {
        "schema": "orthemology-reader-census-v1",
        "baseline": {"commit": commit, "tree": tree},
        "scope": "Every tracked entry at the pinned commit; external body set is empty",
        "reading_status": "NOT_SEMANTICALLY_READ",
        "qualification": "Object census only; owner completeness and scholarly dispositions require separate review",
        "entries_sha256": hashlib.sha256(canonical).hexdigest(),
        "population": {
            "tracked_entries": len(entries),
            "blob_paths": len(blobs),
            "distinct_blob_objects": len({entry["git_oid"] for entry in blobs}),
            "gitlinks": sum(entry["kind"] == "commit" for entry in entries),
            "by_root": dict(sorted(Counter(
                entry["path"].split("/", 1)[0] if "/" in entry["path"] else "(root)"
                for entry in entries
            ).items())),
            "by_suffix": dict(sorted(Counter(
                Path(entry["path"]).suffix.lower() or "(none)" for entry in entries
            ).items())),
            "by_mode": dict(sorted(Counter(entry["mode"] for entry in entries).items())),
        },
        "owners": selected,
        "external_body_admissions": [],
    }
    if include_entries:
        result["entries"] = entries
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--ref", required=True, help="Exact full commit object ID; never HEAD")
    parser.add_argument("--owner", action="append", default=[], help="Existing regular discovery-owner path")
    parser.add_argument("--entries", action="store_true", help="Include all identity rows, not just their digest")
    args = parser.parse_args()
    try:
        result = census(args.repo, args.ref, owners=args.owner, include_entries=args.entries)
    except (ValueError, OSError) as exc:
        parser.exit(2, "CENSUS ERROR: " + str(exc) + "\n")
    sys.stdout.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
