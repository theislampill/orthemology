"""Exact, versioned source access. Reading never executes archived research code.

The tracked lock indexes logical occurrences; cache objects may share bytes.
Git objects, local standard archives and explicit HTTPS reads are verified against
both SHA-256 and Git blob identity. Old loose source directories are never inputs.
"""
from __future__ import annotations
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request


class SourceError(RuntimeError):
    def __init__(self, code, detail):
        self.code = code
        super().__init__(f"{code}: {detail}")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SourceError("DUPLICATE_KEY", key)
        result[key] = value
    return result


def load_json(data):
    try:
        return json.loads(data, object_pairs_hook=_unique_pairs)
    except (ValueError, TypeError) as exc:
        raise SourceError("CORRUPT", f"invalid JSON: {exc}") from exc


def safe_path(name):
    if (not isinstance(name, str) or not name or name.startswith("/")
            or "\\" in name or ":" in name or "\0" in name
            or unicodedata.normalize("NFC", name) != name
            or any(x in ("", ".", "..") for x in name.split("/"))):
        raise SourceError("UNSAFE_PATH", repr(name))
    return name


def validate_paths(names):
    seen = {}
    paths = set()
    for name in names:
        safe_path(name)
        folded = name.casefold()
        if folded in seen:
            raise SourceError("COLLISION", f"{name} / {seen[folded]}")
        seen[folded] = name
        paths.add(folded)
    for name in paths:
        if any(str(p) in paths for p in PurePosixPath(name).parents if str(p) != "."):
            raise SourceError("COLLISION", f"file/directory: {name}")


def verify_bytes(row, data):
    if (len(data) != row["bytes"] or sha256(data) != row["sha256"]
            or git_blob(data) != row["git_blob"]):
        raise SourceError("CORRUPT", row["path"])
    return data


def _reject_links(path):
    path = Path(path)
    for item in (path, *path.parents):
        if item.is_symlink():
            raise SourceError("UNSAFE_PATH", f"symlink: {item}")
    return path


def atomic_bytes(path, data):
    path = _reject_links(Path(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".download-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        _reject_links(path)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


class SourceProvider:
    def __init__(self, root, cache=None, offline=False, git_repo=None):
        self.root = Path(root).resolve()
        self.lock_path = self.root / "corpus" / "archives.lock.json"
        self.lock_bytes = self.lock_path.read_bytes()
        self.manifest = load_json(self.lock_bytes)
        if self.manifest.get("schema_version") != 1:
            raise SourceError("SCHEMA", "unsupported archive lock")
        rows = self.manifest.get("occurrences", [])
        if not rows or len(rows) != self.manifest.get("baseline", {}).get("files"):
            raise SourceError("POPULATION", "empty or inconsistent source population")
        validate_paths(row["path"] for row in rows)
        for row in rows:
            if (row.get("mode") not in ("100644", "100755")
                    or not isinstance(row.get("bytes"), int) or row["bytes"] < 0
                    or not re.fullmatch("[0-9a-f]{64}", row.get("sha256", ""))
                    or not re.fullmatch("[0-9a-f]{40}", row.get("git_blob", ""))):
                raise SourceError("SCHEMA", f"invalid identity: {row.get('path')}")
        self.occurrences = {r["path"]: r for r in rows}
        self.baseline = self.manifest["baseline"]
        self.current_sources = {}
        current_rows = self.manifest.get("current_sources", [])
        validate_paths(dict.fromkeys(r["path"] for r in current_rows))
        for row in current_rows:
            version = row.get("version")
            key = (row["path"], version)
            if (not isinstance(version, str) or not version or len(version) > 256
                    or version == self.baseline["commit"] or key in self.current_sources
                    or row.get("mode") not in ("100644", "100755")
                    or not isinstance(row.get("bytes"), int) or row["bytes"] < 0
                    or not re.fullmatch("[0-9a-f]{64}", row.get("sha256", ""))
                    or not re.fullmatch("[0-9a-f]{40}", row.get("git_blob", ""))):
                raise SourceError("SCHEMA", "invalid/duplicate current edition")
            self.current_sources[key] = row
        if not re.fullmatch("[0-9a-f]{40}", self.baseline.get("commit", "")):
            raise SourceError("SCHEMA", "baseline commit must be exact")
        self.cache = _reject_links(Path(cache).absolute() if cache else
                                   Path(os.environ.get("ORTHEMOLOGY_CACHE",
                                   Path.home() / ".cache" / "orthemology")).absolute())
        self.offline = offline
        self.git_repo = None if git_repo is False else Path(git_repo or self.root)
        self._pack_cache = {}
        self.network_bytes = 0
        self.sources_used = {}

    def resolve_legacy(self, path, context=None):
        safe_path(path)
        if context is not None and context != self.baseline["commit"]:
            raise SourceError("AMBIGUOUS_VERSION", "supply an indexed exact edition; no latest fallback")
        try:
            return dict(self.occurrences[path])
        except KeyError as exc:
            raise SourceError("UNAVAILABLE", f"unindexed exact path: {path}") from exc

    def resolve(self, path, context=None):
        safe_path(path)
        if context is None or context == self.baseline["commit"]:
            return self.resolve_legacy(path, context)
        try:
            return dict(self.current_sources[(path, context)])
        except KeyError as exc:
            raise SourceError("AMBIGUOUS_VERSION", "unindexed exact current edition") from exc

    def _pack_bytes(self, pack_name, path):
        info = self.manifest.get("packs", {}).get(pack_name)
        if not info:
            return None
        name = safe_path(info["file"])
        pack_path = _reject_links(self.cache / name)
        if not pack_path.exists():
            pack_path = _reject_links(self.cache / "packs" / name)
        if not pack_path.exists():
            return None
        stat = pack_path.stat()
        signature = (stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
        cached = self._pack_cache.get(pack_name)
        if cached is None or cached[0] != signature:
            raw = pack_path.read_bytes()
            if len(raw) != info["bytes"] or sha256(raw) != info["sha256"]:
                raise SourceError("CORRUPT", f"archive {pack_name}")
            expected = {k: r for k, r in self.occurrences.items()
                        if r["pack"] == pack_name or info.get("full_baseline")}
            contents = {}
            try:
                with tarfile.open(fileobj=io.BytesIO(raw), mode="r:*") as archive:
                    for member in archive:
                        safe_path(member.name)
                        if not member.isfile():
                            raise SourceError("UNSAFE_PATH", f"non-regular archive member: {member.name}")
                        if member.name in contents or member.name not in expected:
                            raise SourceError("CORRUPT", f"extra/duplicate member: {member.name}")
                        row = expected[member.name]
                        if member.mode != int(row["mode"], 8) & 0o777:
                            raise SourceError("CORRUPT", f"mode: {member.name}")
                        if member.size != row["bytes"]:
                            raise SourceError("CORRUPT", f"size: {member.name}")
                        stream = archive.extractfile(member)
                        contents[member.name] = verify_bytes(row, stream.read(row["bytes"] + 1))
                if set(contents) != set(expected) or len(contents) != info["members"]:
                    raise SourceError("CORRUPT", f"incomplete archive {pack_name}")
            except (tarfile.TarError, EOFError, OSError) as exc:
                raise SourceError("CORRUPT", f"archive {pack_name}: {exc}") from exc
            self._pack_cache[pack_name] = (signature, contents)
        return self._pack_cache[pack_name][1].get(path)

    def _git_bytes(self, row, current=False):
        if self.git_repo is None:
            return None
        result = subprocess.run(["git", "-C", str(self.git_repo), "cat-file", "blob",
                                 row["git_blob"] if current else f"{self.baseline['commit']}:{row['path']}"],
                                capture_output=True)
        return result.stdout if result.returncode == 0 else None

    def read_bytes(self, path, context=None):
        row = self.resolve(path, context)
        access = row.get("access", "public")
        if access == "restricted":
            raise SourceError("RESTRICTED", path)
        if access == "identity-only":
            raise SourceError("IDENTITY_ONLY", path)
        if access != "public":
            raise SourceError("UNAVAILABLE", f"unknown access class: {access}")
        obj = _reject_links(self.cache / "objects" / row["sha256"])
        if obj.exists():
            self.sources_used[path] = "verified-object-cache"
            return verify_bytes(row, obj.read_bytes())
        if context is not None and context != self.baseline["commit"]:
            current = _reject_links(self.root / row["path"])
            working = current.read_bytes() if current.is_file() else None
            if working is not None and sha256(working) == row["sha256"]:
                data = verify_bytes(row, working)
                self.sources_used[path] = "declared-working-edition"
                return data
            # A previously committed exact edition remains recoverable after a
            # path is edited or a cache is lost. The declared blob selects bytes;
            # neither HEAD nor a newer file selects scholarly currentness.
            data = self._git_bytes(row, current=True)
            if data is not None:
                self.sources_used[path] = "pinned-current-git-blob"
                return verify_bytes(row, data)
            if working is not None:
                raise SourceError("CORRUPT", f"working bytes differ from exact edition: {path}")
            raise SourceError("NOT_CACHED", f"exact current edition unavailable: {path}")
        for pack in (row["pack"], self.manifest.get("fallback_pack")):
            if pack:
                data = self._pack_bytes(pack, path)
                if data is not None:
                    self.sources_used[path] = f"verified-archive:{pack}"
                    return verify_bytes(row, data)
        data = self._git_bytes(row)
        if data is not None:
            self.sources_used[path] = "pinned-git-object"
            return verify_bytes(row, data)
        if self.offline:
            raise SourceError("NOT_CACHED", f"{path}; offline exact source absent")
        if self.manifest.get("repository") != "https://github.com/theislampill/orthemology":
            raise SourceError("UNAVAILABLE", "unapproved source repository")
        url = ("https://raw.githubusercontent.com/theislampill/orthemology/"
               + self.baseline["commit"] + "/" + urllib.parse.quote(path, safe="/"))
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read(row["bytes"] + 1)
        except (OSError, urllib.error.URLError) as exc:
            raise SourceError("UNAVAILABLE", f"{path}: {exc}") from exc
        verify_bytes(row, data)
        atomic_bytes(obj, data)
        self.network_bytes += len(data)
        self.sources_used[path] = "pinned-public-source"
        return data

    def fetch(self, paths=None):
        chosen = list(paths or self.occurrences)
        for path in chosen:
            row = self.resolve_legacy(path)
            atomic_bytes(self.cache / "objects" / row["sha256"], self.read_bytes(path))
        return {"files": len(chosen), "network_bytes": self.network_bytes,
                "baseline": self.baseline["commit"]}
