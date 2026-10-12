#!/usr/bin/env python3
"""Read-only public acquisition; never overrides a successful connected read with public failure."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

if not __debug__:
    raise SystemExit("Use ordinary Python.")
BASE = Path(__file__).resolve().parents[1]
BASELINE = "f50dc1aee52356cc6adbef342387576b02afc124"
EXPECTED_TREE = "afd612bcb4bf2a65727f82283e3a894d497f2865"
REPO = "theislampill/orthemology"
URL = "https://github.com/" + REPO + ".git"
OUT = BASE / "sources"
OUT.mkdir(exist_ok=True)
REC = {"schema": "read-only-git-acquisition-v1",
       "started_utc": datetime.now(timezone.utc).isoformat(),
       "connected_observation_head": BASELINE,
       "connected_observation_tree": EXPECTED_TREE,
       "public_failure_does_not_negate_connector_read": True,
       "repository_writes": 0, "commands": [], "objects": [],
       "distribution_exclusions": [], "discussion_requests": [],
       "semantic_review_credit": 0}

def save():
    (BASE / "ledgers/public_acquisition.json").write_text(
        json.dumps(REC, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def run(args, cwd=None, timeout=80):
    started = time.time()
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout,
                           env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        REC["commands"].append({"argv": args, "exit": p.returncode,
                                "seconds": time.time()-started,
                                "stdout": p.stdout.decode("utf-8", "replace"),
                                "stderr": p.stderr.decode("utf-8", "replace")})
        return p
    except (OSError, subprocess.TimeoutExpired) as exc:
        REC["commands"].append({"argv": args, "error": type(exc).__name__,
                                "message": str(exc)})
        return None

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def screen(name, data):
    spec = importlib.util.spec_from_file_location("preserver", BASE / "verification/preserve_work.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.screen(name, data)
    if data[:4] == b"\x00\x01\x00\x00":
        result.append("possible_true_type_font_signature")
    return result

def main():
    mirror = Path(tempfile.mkdtemp(prefix="orthemology_readonly_stage3_")) / "repository.git"
    REC["local_mirror"] = str(mirror)
    p = run(["git", "clone", "--mirror", URL, str(mirror)], timeout=80)
    if p is None or p.returncode:
        REC["public_acquisition_status"] = "FAILED_OR_INCOMPLETE"
        REC["connected_repository_status"] = "SUCCESSFUL_PRIOR_READ_RETAINED"
        REC["complete_current_tree_obtained_here"] = False
        REC["complete_reachable_history_obtained_here"] = False
        save()
        return 2
    head = run(["git", "-C", str(mirror), "rev-parse", "refs/heads/main"])
    if head is None or head.returncode:
        REC["public_acquisition_status"] = "CLONE_SUCCEEDED_MAIN_UNRESOLVED"
        save()
        return 2
    current = head.stdout.decode().strip()
    treep = run(["git", "-C", str(mirror), "rev-parse", current + "^{tree}"])
    tree = treep.stdout.decode().strip() if treep and treep.returncode == 0 else None
    REC.update(public_main=current, public_tree=tree,
               comparison="IDENTICAL" if current == BASELINE else "LATER_OR_DIFFERENT_VERSION",
               tree_matches_connected_pin=(current == BASELINE and tree == EXPECTED_TREE))
    fsck = run(["git", "-C", str(mirror), "fsck", "--full", "--strict"], timeout=80)
    listing = run(["git", "-C", str(mirror), "ls-tree", "-r", "-z", "--full-tree", current])
    if listing is None or listing.returncode:
        REC["public_acquisition_status"] = "TREE_LIST_FAILED"
        save()
        return 2
    entries = []
    for record in listing.stdout.split(b"\0"):
        if not record:
            continue
        prefix, name = record.split(b"\t", 1)
        mode, kind, oid = prefix.decode().split()
        entries.append({"mode": mode, "type": kind, "oid": oid,
                        "path": name.decode("utf-8", "surrogateescape")})
    REC["current_tree_manifest"] = entries
    revs = run(["git", "-C", str(mirror), "rev-list", "--objects", "--all"], timeout=80)
    if revs is None or revs.returncode:
        REC["public_acquisition_status"] = "HISTORY_LIST_FAILED"
        save()
        return 2
    objnames = {}
    for row in revs.stdout.decode("utf-8", "replace").splitlines():
        parts = row.split(" ", 1)
        objnames.setdefault(parts[0], parts[1] if len(parts) > 1 else "")
    # Add current-tree path information even when the history walker omitted a name.
    for e in entries:
        if e["type"] == "blob":
            objnames[e["oid"]] = e["path"]
    object_dir = OUT / "history_objects"
    object_dir.mkdir(exist_ok=True)
    batch = subprocess.Popen(["git", "-C", str(mirror), "cat-file", "--batch"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exported = {}
    error = None
    try:
        for oid, hint in objnames.items():
            batch.stdin.write((oid + "\n").encode()); batch.stdin.flush()
            header = batch.stdout.readline().decode().strip().split()
            if len(header) != 3:
                raise RuntimeError("Incomplete object header for " + oid)
            actual_oid, kind, length = header
            length = int(length)
            data = batch.stdout.read(length)
            terminator = batch.stdout.read(1)
            if len(data) != length or terminator != b"\n":
                raise RuntimeError("Incomplete object body for " + oid)
            git_oid = hashlib.sha1((kind + " " + str(length) + "\0").encode() + data).hexdigest()
            if git_oid != oid or actual_oid != oid:
                raise RuntimeError("Git object identity mismatch for " + oid)
            problems = screen(hint or oid, data) if kind == "blob" else screen(oid, data)
            row = {"oid": oid, "type": kind, "bytes": length,
                   "sha256": sha256(data), "path_hint": hint}
            if problems:
                row["distribution"] = "EXCLUDED_NOT_READING_EXCLUDED"
                REC["distribution_exclusions"].append({**row, "reasons": problems})
            else:
                dest = object_dir / (oid + "." + kind)
                dest.write_bytes(data)
                row["distribution"] = "PRESERVED"
                row["export"] = str(dest.relative_to(BASE))
                exported[oid] = dest
            REC["objects"].append(row)
    except Exception as exc:
        error = {"error_type": type(exc).__name__, "message": str(exc)}
    finally:
        batch.stdin.close()
        batch.wait(timeout=10)
    if error:
        REC["object_export_error"] = error
    working = OUT / "repository"
    for e in entries:
        pth = Path(e["path"])
        if pth.is_absolute() or ".." in pth.parts:
            REC["distribution_exclusions"].append({**e, "reasons": ["unsafe_tree_path"]})
            continue
        if e["mode"] == "120000" or e["type"] != "blob":
            REC["distribution_exclusions"].append({**e, "reasons": ["symlink_or_submodule_not_followed"]})
            continue
        if e["oid"] in exported:
            dest = working / pth
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(exported[e["oid"]].read_bytes())
    REC["complete_current_tree_obtained_here"] = error is None and fsck is not None and fsck.returncode == 0
    REC["complete_reachable_history_obtained_here"] = REC["complete_current_tree_obtained_here"]
    REC["history_scope"] = "Objects reachable from refs advertised to a public --mirror clone; not deleted/unadvertised commits."
    REC["distribution_scope"] = "Screened exports; exclusions do not reduce the original reading obligation."
    REC["public_acquisition_status"] = "ACQUIRED" if error is None else "PARTIAL_EXPORT"
    # Only metadata/history are fetched; no repository scripts are executed.
    log = run(["git", "-C", str(mirror), "log", "--all", "--date=iso-strict",
               "--format=%H%x09%P%x09%aI%x09%s"], timeout=80)
    if log and log.returncode == 0:
        (OUT / "commit_history.tsv").write_bytes(log.stdout)
    save()
    # Public issue transport has its own receipt, independent of the Git data.
    deadline = time.monotonic() + 60
    pages = []
    for page in range(1, 21):
        if time.monotonic() >= deadline:
            REC["discussion_status"] = "TIME_BOUNDED_PARTIAL"
            break
        endpoint = f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100&page={page}"
        try:
            req = urllib.request.Request(endpoint, headers={"User-Agent": "read-only-research-custody"})
            with urllib.request.urlopen(req, timeout=10) as response:
                payload = response.read()
            values = json.loads(payload)
            dest = OUT / "discussion_metadata" / f"issues-page-{page}.json"
            dest.parent.mkdir(exist_ok=True)
            dest.write_bytes(payload)
            REC["discussion_requests"].append({"url": endpoint, "status": "ACQUIRED",
                                               "sha256": sha256(payload), "items": len(values),
                                               "path": str(dest.relative_to(BASE))})
            pages.extend(values)
            if len(values) < 100:
                REC["discussion_status"] = "ISSUE_COLLECTION_ACQUIRED_COMMENTS_NOT_YET_REVIEWED"
                break
        except Exception as exc:
            REC["discussion_requests"].append({"url": endpoint, "status": "PUBLIC_REQUEST_FAILED",
                                               "error_type": type(exc).__name__, "message": str(exc)})
            REC["discussion_status"] = "PUBLIC_FAILURE_CONNECTOR_READ_STILL_AVAILABLE"
            break
    REC["discussion_comment_queue"] = [
        {"number": x.get("number"), "comments_url": x.get("comments_url"),
         "comments": x.get("comments"), "is_pull_request": "pull_request" in x,
         "status": "FETCH_AND_SEMANTIC_REVIEW_PENDING"} for x in pages]
    REC["finished_utc"] = datetime.now(timezone.utc).isoformat()
    save()
    print(json.dumps({k: REC.get(k) for k in
                      ("public_acquisition_status", "public_main",
                       "complete_current_tree_obtained_here",
                       "complete_reachable_history_obtained_here", "discussion_status")}, indent=2))
    return 0 if error is None else 1

if __name__ == "__main__":
    raise SystemExit(main())
