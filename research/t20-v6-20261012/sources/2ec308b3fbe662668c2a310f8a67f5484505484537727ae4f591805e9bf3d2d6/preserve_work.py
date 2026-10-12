#!/usr/bin/env python3
"""Preserve mounted predecessor work without treating copying as semantic review."""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import stat
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

if not __debug__:
    raise SystemExit("Run ordinary Python: optimisation-disabled execution is not accepted.")

BASE = Path(__file__).resolve().parents[1]
ROOT = Path("/mnt/data")
DEST = BASE / "preserved_work"
FONT_EXTS = {".ttf", ".otf", ".ttc", ".otc", ".woff", ".woff2", ".eot",
             ".pfb", ".pfm", ".dfont"}
PRIVATE_PATTERNS = [
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
]
inventory = []
exclusions = []
errors = []
manifest_receipts = []

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def save_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")

def unsafe_name(name: str) -> bool:
    p = PurePosixPath(name.replace("\\", "/"))
    return p.is_absolute() or ".." in p.parts

def screen(name: str, data: bytes, depth: int = 0) -> list[str]:
    problems = []
    if Path(name).suffix.lower() in FONT_EXTS:
        problems.append("font_file")
    if any(p.search(data) for p in PRIVATE_PATTERNS):
        problems.append("possible_secret_or_private_key")
    # Font files are not allowed under a different filename either.
    if data[:4] in (b"OTTO", b"wOFF", b"wOF2", b"ttcf", b"\x00\x01\x00\x00"):
        problems.append("font_signature")
    if data.startswith(b"PK\x03\x04"):
        if depth >= 8:
            return problems + ["archive_recursion_screening_limit"]
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                items = z.infolist()
                if sum(i.file_size for i in items) > 512 * 1024 * 1024:
                    return problems + ["archive_expansion_screening_limit"]
                if z.testzip() is not None:
                    problems.append("archive_crc_failure")
                for item in items:
                    if item.is_dir():
                        continue
                    if unsafe_name(item.filename):
                        problems.append("unsafe_archive_member_path")
                        continue
                    mode = item.external_attr >> 16
                    if stat.S_ISLNK(mode):
                        problems.append("archive_symlink")
                        continue
                    nested = screen(item.filename, z.read(item), depth + 1)
                    if nested:
                        # Only a path and reason are retained, never secret bytes.
                        problems.extend(f"member:{item.filename}:{p}" for p in nested)
        except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as exc:
            problems.append("archive_not_screenable:" + type(exc).__name__)
    return sorted(set(problems))

def check_zip_manifests(source: Path, data: bytes) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = set(z.namelist())
            roots = sorted((n for n in names if PurePosixPath(n).name == "SHA256SUMS"),
                           key=lambda n: (len(PurePosixPath(n).parts), n))
            for manifest in roots:
                parent = PurePosixPath(manifest).parent
                good, bad = 0, []
                text = z.read(manifest).decode("utf-8")
                for n, line in enumerate(text.splitlines(), 1):
                    if not line.strip():
                        continue
                    match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](.+)", line)
                    if match is None:
                        bad.append({"manifest_line": n, "reason": "unrecognised_manifest_syntax"})
                        continue
                    expected, rel = match.groups()
                    if unsafe_name(rel):
                        bad.append({"manifest_line": n, "reason": "unsafe_manifest_path"})
                        continue
                    member = (parent / rel).as_posix()
                    if member.startswith("./"):
                        member = member[2:]
                    if member not in names:
                        bad.append({"manifest_line": n, "member": member, "reason": "missing"})
                    elif digest(z.read(member)).lower() != expected.lower():
                        bad.append({"manifest_line": n, "member": member, "reason": "hash_mismatch"})
                    else:
                        good += 1
                manifest_receipts.append({
                    "archive": source.name,
                    "archive_sha256": digest(data),
                    "manifest": manifest,
                    "verified_entries": good,
                    "failures": bad,
                    "status": "PASS" if good and not bad else "FAIL_OR_EMPTY",
                    "method": "independently authored byte-manifest comparison; not the inherited verifier",
                    "semantic_review_credit": 0,
                })
    except Exception as exc:
        errors.append({"operation": "manifest_check", "path": str(source),
                       "error_type": type(exc).__name__, "message": str(exc)})


def salvage_archive_members(origin: str, data: bytes, depth: int = 0) -> None:
    """Retain safe members even when the enclosing raw ZIP is withheld."""
    if depth >= 8:
        errors.append({"operation": "salvage", "path": origin, "error_type": "DepthLimit"})
        return
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if sum(i.file_size for i in z.infolist()) > 512 * 1024 * 1024:
                errors.append({"operation": "salvage", "path": origin, "error_type": "ExpansionLimit"})
                return
            for index, item in enumerate(z.infolist()):
                if item.is_dir():
                    continue
                member_origin = f"{origin}!member[{index}]:{item.filename}"
                if unsafe_name(item.filename) or stat.S_ISLNK(item.external_attr >> 16):
                    exclusions.append({"path": member_origin, "reason": "unsafe_member_or_symlink",
                                       "reading_requirement_reduced": False})
                    continue
                member = z.read(item)
                reasons = screen(item.filename, member, depth + 1)
                record = {"original_path": member_origin, "bytes": len(member),
                          "sha256": digest(member), "new_semantic_reading_credit": 0}
                # Index and content-addressed namespace preserve duplicate member identities.
                namespace = hashlib.sha256(origin.encode("utf-8")).hexdigest()[:20]
                target = BASE / "preserved_archive_members" / namespace / str(index) / item.filename
                if reasons:
                    record["disposition"] = "DISTRIBUTION_EXCLUDED_NOT_READING_EXCLUDED"
                    exclusions.append({**record, "reasons": reasons, "reading_requirement_reduced": False})
                    if member.startswith(b"PK\x03\x04"):
                        salvage_archive_members(member_origin, member, depth + 1)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(member)
                    record.update(disposition="PRESERVED_MEMBER_BYTE_IDENTICAL",
                                  preserved_path=target.relative_to(BASE).as_posix())
                inventory.append(record)
    except Exception as exc:
        errors.append({"operation": "salvage", "path": origin,
                       "error_type": type(exc).__name__, "message": str(exc)})


def preserve(path: Path) -> None:
    relative = path.relative_to(ROOT).as_posix()
    if path.is_symlink():
        exclusions.append({"path": relative, "reason": "symlink_not_followed",
                           "reading_requirement_reduced": False})
        return
    if not path.is_file():
        return
    try:
        data = path.read_bytes()
        reasons = screen(relative, data)
        entry = {"original_path": relative, "sha256": digest(data), "bytes": len(data),
                 "new_semantic_reading_credit": 0}
        if ".git" in path.parts:
            reasons.append("opaque_git_storage_requires_separate_object_level_screening")
        if reasons:
            old_copy = DEST / relative
            if old_copy.is_file() and not old_copy.is_symlink():
                old_copy.unlink()
            entry["disposition"] = "DISTRIBUTION_EXCLUDED_NOT_READING_EXCLUDED"
            exclusions.append({**entry, "reasons": reasons,
                               "reading_requirement_reduced": False})
            if data.startswith(b"PK\x03\x04"):
                salvage_archive_members(relative, data)
        else:
            target = DEST / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            if target.read_bytes() != data:
                raise RuntimeError("copy did not preserve bytes")
            entry.update(disposition="PRESERVED_BYTE_IDENTICAL",
                         preserved_path=target.relative_to(BASE).as_posix())
        inventory.append(entry)
        if path.suffix.lower() == ".zip":
            check_zip_manifests(path, data)
    except Exception as exc:
        errors.append({"operation": "preserve", "path": relative,
                       "error_type": type(exc).__name__, "message": str(exc)})

def main() -> int:
    DEST.mkdir(exist_ok=True)
    candidates = []
    for p in ROOT.iterdir():
        if p == BASE or p.name.startswith("orthemology_consolidation_stage3_delivery"):
            continue
        if p.is_dir():
            # All mounted prior work, not a fabricated list inferred from filenames.
            candidates.extend(q for q in p.rglob("*") if q.is_file() or q.is_symlink())
        else:
            candidates.append(p)
    for p in sorted(set(candidates)):
        preserve(p)
    inherited_receipts = [
        i for i in inventory if any(k in i["original_path"].lower()
                                   for k in ("audit", "review", "receipt", "coverage", "scope"))
    ]
    save_json(BASE / "ledgers/preservation_inventory.json", {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "files": inventory, "errors": errors,
        "note": "Acquisition and exact copying do not establish semantic perusal.",
    })
    save_json(BASE / "ledgers/distribution_exclusions.json", exclusions)
    save_json(BASE / "ledgers/intake_manifest_checks.json", manifest_receipts)
    save_json(BASE / "ledgers/inherited_review_inventory.json", {
        "records": inherited_receipts,
        "meaning": "Located and preserved by filename; not freshly source-reviewed or promoted.",
        "prior_review_status": "Retained unchanged in each original payload; no blanket reset to zero.",
    })
    save_json(BASE / "ledgers/source_coverage_delta.json", {
        "fresh_byte_bound_source_lines_certified_in_resumed_segment": 0,
        "inherited_completed_receipts": "Preserved, not erased and not automatically recredited.",
        "reason": "No usable tool-result body was available to this resumed reviewing segment.",
        "whole_request_status": "OPEN_NOT_APPROVED",
    })
    print(json.dumps({"preserved_files": sum(i["disposition"] == "PRESERVED_BYTE_IDENTICAL"
                                           for i in inventory),
                      "exclusions": len(exclusions), "errors": len(errors),
                      "manifest_checks": len(manifest_receipts)}, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
