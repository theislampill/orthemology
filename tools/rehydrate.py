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
            receipt = json.loads(_reject_links(dest / RECEIPT).read_text())
        except (OSError, ValueError) as exc:
            raise SourceError("RECEIPT", "completion receipt absent or malformed") from exc
        if any(receipt.get(k) != v for k, v in result.items()):
            raise SourceError("RECEIPT", "completion identity differs from verified workspace")
        if type(receipt.get("history")) is not bool:
            raise SourceError("RECEIPT", "history claim must be explicit")
        history = _reject_links(dest / ".git")
        if receipt["history"]:
            if not history.is_dir():
                raise SourceError("CORRUPT", "HISTORY missing after restoration")
            for item in history.rglob("*"):
                _reject_links(item)
            alternates = history / "objects/info/alternates"
            if alternates.exists() and alternates.read_bytes().strip():
                raise SourceError("CORRUPT", "HISTORY has undeclared external object storage")
            def history_git(*args):
                cmd = ["git", "--git-dir", str(history), "--work-tree", str(dest), *args]
                check = subprocess.run(cmd, capture_output=True, text=True)
                if check.returncode:
                    raise SourceError("CORRUPT", "HISTORY " + args[0] + ": " + check.stderr)
                return check.stdout.strip()
            if history_git("rev-parse", "HEAD") != provider.baseline["commit"]:
                raise SourceError("CORRUPT", "HISTORY HEAD differs from source context")
            if history_git("rev-parse", "HEAD^{tree}") != tree:
                raise SourceError("CORRUPT", "HISTORY tree differs from restored sources")
            history_git("fsck", "--full")
            for oid in provider.manifest.get("required_git_objects", []):
                history_git("cat-file", "-e", oid)
        elif history.exists():
            raise SourceError("RECEIPT", "unqualified history is present")
        result["history"] = receipt["history"]
    return result

def _attach_history(provider, dest, bundle=None, git_repository=None):
    info = provider.manifest.get("history")
    if not info:
        raise SourceError("UNAVAILABLE", "history lock absent")
    if (bundle is None) == (git_repository is None):
        raise SourceError("UNAVAILABLE", "choose one explicit history bundle or existing Git source")
    if bundle is not None:
        source = _reject_links(Path(bundle))
        raw = source.read_bytes()
        if len(raw) != info["bytes"] or sha256(raw) != info["sha256"]:
            raise SourceError("CORRUPT", "history bundle")
        command = ["git", "clone", "--bare", str(source), str(dest / ".git")]
    else:
        source = _reject_links(Path(git_repository).absolute())
        check = subprocess.run(["git","-C",str(source),"cat-file","-e",
                                provider.baseline["commit"] + "^{commit}"],capture_output=True)
        if check.returncode:
            raise SourceError("CORRUPT","existing Git source lacks exact baseline")
        # --no-local copies objects through Git transport, without hardlinks or alternates.
        command = ["git","clone","--bare","--no-local",str(source),str(dest/".git")]
    result = subprocess.run(command, capture_output=True, text=True)
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
    if info.get("objects"):
        objects = git("rev-list","--objects",provider.baseline["commit"]).splitlines()
        if len(objects) != info["objects"]:
            raise SourceError("CORRUPT","baseline history object population differs")
    if git("rev-parse", "HEAD^{tree}") != provider.baseline["tree"]:
        raise SourceError("CORRUPT", "bundle baseline tree")

def materialise(provider, paths, destination, with_history=False, bundle=None, git_repository=None):
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
            if bundle is None and git_repository is None:
                raise SourceError("NOT_CACHED", "explicit verified history source required")
            _attach_history(provider, stage, bundle, git_repository)
        full = set(selected) == set(provider.occurrences)
        result = verify_workspace(provider, stage, None if full else selected, require_receipt=False)
        result["history"] = bool(with_history)
        result["history_route"] = ("verified-bundle" if bundle is not None else
                                   "verified-existing-git" if git_repository is not None else "none")
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

def restore(provider, destination, with_history=False, bundle=None, git_repository=None):
    return materialise(provider, provider.occurrences, destination, with_history, bundle, git_repository)

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

def _rewrite_reading_links(data, original, target, mapping, provider):
    """Create a declared navigation derivative; frozen originals stay unchanged."""
    import posixpath
    import re
    import urllib.parse
    suffix = Path(original).suffix.lower()
    if suffix not in (".md", ".tex"):
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeError:
        return data
    def address(value, tex=False):
        parts = urllib.parse.urlsplit(value)
        if parts.scheme or parts.netloc or not parts.path:
            return value
        decoded = urllib.parse.unquote(parts.path)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(original),decoded))
        if tex and resolved not in provider.occurrences and resolved + ".tex" in provider.occurrences:
            resolved += ".tex"
        directory = (not tex and resolved not in provider.occurrences and
                     any(path.startswith(resolved.rstrip("/") + "/")
                         for path in provider.occurrences))
        if resolved not in provider.occurrences and not directory:
            return value
        if directory:
            updated = (provider.manifest["repository"] + "/tree/" +
                       provider.baseline["commit"] + "/" +
                       urllib.parse.quote(resolved,safe="/"))
        elif resolved in mapping:
            updated = posixpath.relpath(mapping[resolved],posixpath.dirname(target) or ".")
            if tex and not Path(decoded).suffix and updated.endswith(".tex"):
                updated = updated[:-4]
        elif tex:
            # Archived build-only inputs require the exact reconstructed publication context.
            return value
        else:
            updated = (provider.manifest["repository"] + "/blob/" +
                       provider.baseline["commit"] + "/" +
                       urllib.parse.quote(resolved,safe="/"))
        if parts.query:
            updated += "?" + parts.query
        if parts.fragment:
            updated += "#" + parts.fragment
        return updated
    if suffix == ".md":
        pattern = re.compile(r"(\]\()([^\s)]+)([^)]*\))")
        text = pattern.sub(lambda m:m[1]+address(m[2])+m[3],text)
        refs = re.compile(r"(?m)^(\[[^\]]+\]:\s*)(\S+)")
        text = refs.sub(lambda m:m[1]+address(m[2]),text)
    else:
        pattern = re.compile(r"(\\(?:input|include|addbibresource)\{)([^}]+)(\})")
        text = pattern.sub(lambda m:m[1]+address(m[2],True)+m[3],text)
    return text.encode("utf-8")

def assemble(provider, destination):
    """Assemble the declared ordinary profile in isolation, without pruning a branch."""
    profile = provider.manifest.get("profiles",{}).get("ordinary",{})
    mapping = profile.get("existing_paths",{})
    additions = profile.get("new_paths",[])
    paths = list(mapping.values()) + list(additions)
    if not mapping or not additions or len(paths) != profile.get("initial_target"):
        raise SourceError("POPULATION","ordinary profile is empty or differs from its target")
    validate_paths(paths)
    for locator in provider.manifest.get("current_works",[]):
        if locator.get("path") not in paths:
            raise SourceError("PROFILE",
                "current primary owner is absent from ordinary profile: " +
                str(locator.get("path")) +
                "; explicitly revise its membership and approved budget before assembly")
    dest = _reject_links(Path(destination).absolute())
    if dest.exists():
        raise SourceError("EXISTS",str(dest))
    files = {}
    origins = []
    for original,target in mapping.items():
        row = provider.resolve_legacy(original)
        current = _reject_links(provider.root / target)
        if current.is_file():
            data = current.read_bytes()
            # Already-authored current interfaces/prose are explicit profile members.
            origin = "declared-current-source"
            if data == provider.read_bytes(original):
                data = _rewrite_reading_links(data,original,target,mapping,provider)
        else:
            data = _rewrite_reading_links(provider.read_bytes(original),original,target,mapping,provider)
            origin = "baseline-with-navigation-derivative"
        files[target] = (data,row["mode"])
        origins.append({"original":original,"target":target,"original_sha256":row["sha256"],
                        "current_sha256":sha256(data),"origin":origin,
                        "changed_bytes":sha256(data)!=row["sha256"]})
    for path in additions:
        file = _reject_links(provider.root/path)
        if not file.is_file():
            raise SourceError("UNAVAILABLE","missing new interface: "+path)
        files[path] = (file.read_bytes(),"100644")
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.mkdir(mode=0o700,exist_ok=False)
    for path,(data,mode) in files.items():
        file = dest/path
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_bytes(data);file.chmod(int(mode,8)&0o777)
    actual = {p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file()}
    if actual != set(paths):
        raise SourceError("POPULATION","assembled path population differs")
    rows = []
    dirs = set()
    for path,(data,mode) in files.items():
        written=(dest/path).read_bytes()
        if written!=data:
            raise SourceError("CORRUPT","assembled source "+path)
        rows.append({"path":path,"mode":mode,"git_blob":git_blob(written)})
        for parent in Path(path).parents:
            if str(parent)!=".":
                dirs.add(parent.as_posix())
    return {"files":len(files),"directories":len(dirs),"bytes":sum(len(v[0]) for v in files.values()),
            "tree":tree_identity(rows),"target":profile["initial_target"],
            "source_baseline":provider.baseline["commit"],"mappings":origins,
            "scope":"isolated ordinary candidate; no branch pruning, custody, replay or acceptance claim"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cache", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build-packs"); build.add_argument("--dest", type=Path, required=True)
    thin = sub.add_parser("assemble"); thin.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()
    provider = SourceProvider(args.root, args.cache, offline=True)
    try:
        if args.command == "assemble":
            print(json.dumps(assemble(provider,args.dest),indent=2))
        else:
            packs, fallback = build_packs(provider, args.dest)
            print(json.dumps({"packs": packs, "fallback_pack": fallback}, indent=2))
    except SourceError as exc:
        parser.exit(2, str(exc) + "\n")
if __name__ == "__main__":
    main()
