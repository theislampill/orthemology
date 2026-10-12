#!/usr/bin/env python3
"""Verify the frozen distributed byte set. This is not semantic or scientific verification."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

if not __debug__:
    raise SystemExit("Use ordinary Python, not optimised execution.")

def runtime_cache(relative: str) -> bool:
    parts=PurePosixPath(relative).parts
    return bool(parts and parts[0]=="verification" and "__pycache__" in parts)

def verify(root: Path):
    root=root.resolve()
    manifest=root/"SHA256SUMS"
    if not manifest.is_file():
        return {"status":"FAIL","errors":[{"reason":"missing_root_manifest"}]}
    expected={};errors=[]
    for number,line in enumerate(manifest.read_text(encoding="utf-8").splitlines(),1):
        if not line:
            continue
        match=re.fullmatch(r"([0-9a-f]{64})  (.+)",line)
        if match is None:
            errors.append({"line":number,"reason":"invalid_manifest_line"});continue
        digest,relative=match.groups()
        name=PurePosixPath(relative)
        if name.is_absolute() or ".." in name.parts or relative=="SHA256SUMS":
            errors.append({"line":number,"reason":"unsafe_or_self_reference"});continue
        if relative in expected:
            errors.append({"line":number,"reason":"duplicate_path"});continue
        expected[relative]=digest
    actual=set()
    for path in root.rglob("*"):
        relative=path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append({"path":relative,"reason":"symlink"});continue
        if path.is_file() and relative!="SHA256SUMS" and not runtime_cache(relative):
            actual.add(relative)
    for missing in sorted(set(expected)-actual):
        errors.append({"path":missing,"reason":"missing_file"})
    for extra in sorted(actual-set(expected)):
        errors.append({"path":extra,"reason":"unmanifested_file"})
    good=0
    for relative,digest in expected.items():
        path=root/relative
        if relative not in actual:
            continue
        observed=hashlib.sha256(path.read_bytes()).hexdigest()
        if observed!=digest:
            errors.append({"path":relative,"reason":"hash_mismatch","actual_sha256":observed})
        else:
            good+=1
    return {"status":"PASS" if expected and not errors else "FAIL",
            "manifest_entries":len(expected),"verified_files":good,"errors":errors,
            "ignored_runtime_scope":"Only verification/__pycache__ created by running these utilities.",
            "meaning":"Frozen byte integrity only; no source-reading, proof, physical, novelty or adoption claim."}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("root",nargs="?",type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    result=verify(args.root)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["status"]=="PASS" else 1)
