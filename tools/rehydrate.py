"""Standard archive construction and exact, fail-closed source restoration."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
from source_provider import (SourceError, SourceProvider, atomic_bytes, git_blob,
                             sha256, safe_path, validate_paths, verify_bytes, _reject_links)

RECEIPT = ".corpus-receipt.json"

def tree_identity(rows):
    tree = {}
    for row in rows:
        node = tree
        pieces = row["path"].split("/")
        for part in pieces[:-1]:
            node = node.setdefault(part, {})
        node[pieces[-1]] = (row["mode"], row["git_blob"])
    def encode(node):
        items = []
        for name, value in node.items():
            if isinstance(value, dict):
                mode, oid = "40000", encode(value)
                sort_name = name + "/"
            else:
                mode, oid = value
                sort_name = name
            items.append((sort_name.encode(), mode.encode() + b" " + name.encode()
                          + b"\0" + bytes.fromhex(oid)))
        data = b"".join(payload for _, payload in sorted(items))
        return hashlib.sha1(b"tree " + str(len(data)).encode() + b"\0" + data).hexdigest()
    return encode(tree)

def verify_workspace(provider, destination, paths=None, require_receipt=True):
    dest = _reject_links(Path(destination))
    selected = list(paths or provider.occurrences)
    validate_paths(selected)
    expected = set(selected)
    actual = set()
    for base, dirs, files in os.walk(dest, followlinks=False):
        for name in list(dirs):
            p = Path(base) / name
            if p.is_symlink():
                raise SourceError("UNSAFE_PATH", str(p))
            if p == dest / ".git":
                dirs.remove(name)
        for name in files:
            p = Path(base) / name
            rel = p.relative_to(dest).as_posix()
            if rel == RECEIPT:
                continue
            _reject_links(p)
            actual.add(rel)
    if actual != expected:
        raise SourceError("POPULATION", f"missing={len(expected-actual)}, EXTRA={len(actual-expected)}")
    rows = []
    for path in selected:
        row = provider.resolve_legacy(path)
        file = _reject_links(dest / path)
        verify_bytes(row, file.read_bytes())
        if file.stat().st_mode & 0o777 != int(row["mode"], 8) & 0o777:
            raise SourceError("CORRUPT", f"mode: {path}")
        rows.append(row)
    tree = tree_identity(rows)
    if paths is None and provider.baseline.get("tree") and tree != provider.baseline["tree"]:
        raise SourceError("CORRUPT", "restored Git tree differs")
    result = {"baseline_commit": provider.baseline["commit"], "tree": tree,
              "files": len(rows), "logical_bytes": sum(r["bytes"] for r in rows),
              "lock_sha256": sha256(provider.lock_bytes)}
    if require_receipt:
        try:
            receipt = json.loads((dest / RECEIPT).read_text())
        except (OSError, ValueError) as exc:
            raise SourceError("RECEIPT", "completion receipt absent or malformed") from exc
        if any(receipt.get(k) != v for k, v in result.items()):
            raise SourceError("RECEIPT", "completion identity differs from verified workspace")
    return result

def _attach_history(provider, dest, bundle):
    info = provider.manifest.get("history")
    if not info:
        raise SourceError("UNAVAILABLE", "history lock absent")
    bundle = _reject_links(Path(bundle))
    raw = bundle.read_bytes()
    if len(raw) != info["bytes"] or sha256(raw) != info["sha256"]:
        raise SourceError("CORRUPT", "history bundle")
    result = subprocess.run(["git", "clone", "--bare", str(bundle), str(dest / ".git")],
                            capture_output=True, text=True)
    if result.returncode:
        raise SourceError("CORRUPT", f"bundle clone: {result.stderr}")
    def git(*args):
        result = subprocess.run(["git", "-C", str(dest), *args], capture_output=True, text=True)
        if result.returncode:
            raise SourceError("CORRUPT", f"history operation {args[0]}: {result.stderr}")
        return result.stdout.strip()
    git("config", "core.bare", "false")
    git("symbolic-ref", "HEAD", "refs/heads/main")
    git("reset", "--mixed", provider.baseline["commit"])
    (dest / ".git/info/exclude").write_text("/" + RECEIPT + "\n")
    git("fsck", "--full")
    for oid in provider.manifest.get("required_git_objects", []):
        git("cat-file", "-e", oid)
    if git("rev-parse", "HEAD^{tree}") != provider.baseline["tree"]:
        raise SourceError("CORRUPT", "bundle baseline tree")

def materialise(provider, paths, destination, with_history=False, bundle=None):
    selected = list(paths)
    if not selected:
        raise SourceError("POPULATION", "empty materialisation")
    validate_paths(selected)
    dest = _reject_links(Path(destination).absolute())
    if dest.exists():
        raise SourceError("EXISTS", str(dest))
    if RECEIPT in selected:
        raise SourceError("COLLISION", "reserved completion receipt")
    # Verify every required body before creating the requested destination.
    bodies = {path: provider.read_bytes(path) for path in selected}
    dest.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{dest.name}.partial-", dir=dest.parent))
    try:
        for path in selected:
            row = provider.resolve_legacy(path)
            file = stage / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(bodies[path])
            file.chmod(int(row["mode"], 8) & 0o777)
        if with_history:
            if set(selected) != set(provider.occurrences):
                raise SourceError("POPULATION", "history requires complete baseline")
            if bundle is None:
                raise SourceError("NOT_CACHED", "explicit verified history bundle required")
            _attach_history(provider, stage, bundle)
        full = set(selected) == set(provider.occurrences)
        result = verify_workspace(provider, stage, None if full else selected, require_receipt=False)
        result["history"] = bool(with_history)
        result["scope"] = "exact-source-restoration; no scientific replay or custody qualification"
        (stage / RECEIPT).write_text(json.dumps(result, indent=2) + "\n")
        # An exclusive destination reservation prevents accidental overwrite/reuse.
        dest.mkdir(mode=0o700, exist_ok=False)
        try:
            for child in stage.iterdir():
                if child.name != RECEIPT:
                    os.rename(child, dest / child.name)
            verify_workspace(provider, dest, None if full else selected, require_receipt=False)
            os.rename(stage / RECEIPT, dest / RECEIPT)
        except BaseException:
            (dest / RECEIPT).unlink(missing_ok=True)
            raise
        stage.rmdir()
        return verify_workspace(provider, dest, None if full else selected) | {
            "history": bool(with_history), "scope": result["scope"]}
    except FileExistsError as exc:
        raise SourceError("EXISTS", str(dest)) from exc
    finally:
        if stage.exists():
            shutil.rmtree(stage)

def restore(provider, destination, with_history=False, bundle=None):
    return materialise(provider, provider.occurrences, destination, with_history, bundle)

def build_packs(provider, destination):
    dest = Path(destination)
    if dest.exists():
        raise SourceError("EXISTS", str(dest))
    dest.mkdir(parents=True)
    groups = {}
    for row in provider.occurrences.values():
        groups.setdefault(row["pack"], []).append(row)
    fallback = "baseline-" + provider.baseline["commit"][:12]
    groups[fallback] = list(provider.occurrences.values())
    result = {}
    for name, rows in sorted(groups.items()):
        safe_path(name)
        file = dest / (name + ".tar.xz")
        with tarfile.open(file, "w:xz", format=tarfile.PAX_FORMAT, preset=6) as archive:
            for row in sorted(rows, key=lambda r: r["path"]):
                data = provider.read_bytes(row["path"])
                member = tarfile.TarInfo(row["path"])
                member.size = len(data); member.mode = int(row["mode"], 8) & 0o777
                member.uid = member.gid = member.mtime = 0
                member.uname = member.gname = ""
                archive.addfile(member, io.BytesIO(data))
        raw = file.read_bytes()
        result[name] = {"file": file.name, "bytes": len(raw), "sha256": sha256(raw),
                        "members": len(rows), "full_baseline": name == fallback,
                        "custody": "LOCAL_ONLY", "publication": "NOT_AUTHORISED"}
    return result, fallback

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cache", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build-packs"); build.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()
    provider = SourceProvider(args.root, args.cache, offline=True)
    try:
        packs, fallback = build_packs(provider, args.dest)
        print(json.dumps({"packs": packs, "fallback_pack": fallback}, indent=2))
    except SourceError as exc:
        parser.exit(2, str(exc) + "\n")
if __name__ == "__main__":
    main()
