"""One-checkout protected-body boundary for the actual public reader."""
from contextlib import contextmanager

from pathlib import Path

import hashlib

import importlib

import json

import os

import stat

import subprocess

import sys

RESOLVER_SHA256 = '55d26a9ab9fe7475041bb35bb0e157e9cd72d7622405db45fc12c803c36d75a8'

BASELINE = "0784acddd4770f1190f758f264ba52b2b110bd27"

OWNER_MAP_SHA256 = 'bffb81e2ac979d3fb3fde4a8285910389cd497609d17bd5fdb276b38277dc2eb'

READER_SHA256 = 'b0705ab02cf95858351cb0b3ffe996e19152e6d29f5d997ebb10c7cb0ca1098d'

PATHSPEC_ENV = ("GIT_LITERAL_PATHSPECS", "GIT_GLOB_PATHSPECS", "GIT_NOGLOB_PATHSPECS", "GIT_ICASE_PATHSPECS")

@contextmanager
def bounded_git_environment():
    """Do not let process environment disable literal exclusion pathspecs."""
    values = {"GIT_NO_REPLACE_OBJECTS": "1", "GIT_NO_LAZY_FETCH": "1",
              "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0",
              "GIT_CONFIG_COUNT": "2", "GIT_CONFIG_KEY_0": "core.fsmonitor",
              "GIT_CONFIG_VALUE_0": "false", "GIT_CONFIG_KEY_1": "core.untrackedCache",
              "GIT_CONFIG_VALUE_1": "false"}
    names = set(PATHSPEC_ENV) | set(values)
    old = {name: os.environ.get(name) for name in names}
    try:
        for name in PATHSPEC_ENV:
            os.environ.pop(name, None)
        os.environ.update(values)
        yield
    finally:
        for name, value in old.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

class HeldReaderDiffBoundary:
    """Exact command adapter; constructor also supports isolated native probes."""
    def __init__(self, root, held, baseline, delegate, *, known_links=None):
        self.root = Path(root).resolve()
        self.held = {row["path"]: row for row in held}
        if len(self.held) != len(held) or not self.held:
            raise RuntimeError("Held identity population is ambiguous")
        self.baseline = baseline
        self.delegate = delegate
        self.known_links = known_links
        self.events = []
        self.initial_metadata = self.metadata()

    def git_metadata(self, *args):
        with bounded_git_environment():
            result = subprocess.run(["git", "--no-replace-objects", "--literal-pathspecs", *args],
                                    cwd=self.root, capture_output=True, check=True)
        return result.stdout

    def metadata(self):
        """Only index/tree records and lstat; never ask for held blob bodies."""
        stage = {}
        held_oids = {row["published_metadata"]["git_blob"] for row in self.held.values()}
        for record in self.git_metadata("ls-files", "--stage", "-z").split(b"\0"):
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            mode, oid, level = header.decode("ascii").split()
            path = os.fsdecode(raw_path)
            if path not in self.held and oid in held_oids:
                raise RuntimeError("Held blob has an unexcluded stage alias")
            if path in self.held:
                if path in stage or level != "0":
                    raise RuntimeError("Held stage is missing or conflicted")
                stage[path] = (mode, oid)
        expected = {path: (row["published_metadata"]["mode"], row["published_metadata"]["git_blob"])
                    for path, row in self.held.items()}
        if stage != expected:
            raise RuntimeError("Held stage identity differs from authenticated metadata")
        # Inspect the entire baseline tree metadata to reject historical aliases
        # that a whole-tree diff might otherwise select outside the exclusions.
        tree = {}
        for record in self.git_metadata("ls-tree", "-r", "-z", "--full-tree", self.baseline).split(b"\0"):
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            mode, kind, oid = header.decode("ascii").split()
            path = os.fsdecode(raw_path)
            if path not in self.held and oid in held_oids:
                raise RuntimeError("Held blob has an unexcluded baseline alias")
            if path in self.held:
                if kind != "blob" or path in tree:
                    raise RuntimeError("Held baseline is not an unambiguous blob")
                tree[path] = (mode, oid)
        if tree != expected:
            raise RuntimeError("Held baseline identity differs from authenticated metadata")
        snapshots = {}
        for path, row in self.held.items():
            links = (self.known_links[path] if self.known_links is not None
                     else [(self.root, None)])
            observed = []
            for link_root, expected_metadata in links:
                node = Path(link_root)
                if not stat.S_ISDIR(node.lstat().st_mode):
                    raise RuntimeError("Held root is not an ordinary directory")
                for component in Path(path).parts[:-1]:
                    if component in ("", ".", ".."):
                        raise RuntimeError("Unsafe held metadata path")
                    node = node / component
                    if not stat.S_ISDIR(node.lstat().st_mode):
                        raise RuntimeError("Held path has a nonordinary ancestor")
                info = (Path(link_root) / path).lstat()
                if (not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o644
                        or info.st_size != row["bytes"] or info.st_nlink != len(links)):
                    raise RuntimeError("Held path metadata or hardlink count changed")
                current = {"device": info.st_dev, "inode": info.st_ino, "mode": stat.S_IMODE(info.st_mode),
                           "size": info.st_size, "mtime_ns": info.st_mtime_ns,
                           "ctime_ns": info.st_ctime_ns, "nlink": info.st_nlink}
                if expected_metadata is not None and current != expected_metadata:
                    raise RuntimeError("Known held link differs from authenticated provisioning metadata")
                observed.append((info.st_dev, info.st_ino, info.st_mode, info.st_size,
                                 info.st_mtime_ns, info.st_ctime_ns, info.st_nlink))
            if any(value != observed[0] for value in observed):
                raise RuntimeError("Known held links no longer share the same exact inode metadata")
            snapshots[path] = observed[0]
        return snapshots

    def __call__(self, root, command):
        if Path(root).resolve() != self.root:
            raise RuntimeError("Unexpected repository for bounded reader diff")
        suffix = ["--no-ext-diff", "--no-textconv", "--no-renames", "--name-status", "-z", self.baseline, "--"]
        current = ["git", "diff", *suffix]
        cached = ["git", "diff", "--cached", *suffix]
        command = list(command)
        if command not in (current, cached):
            raise RuntimeError("Unreviewed native reader diff request")
        before = self.metadata()
        if before != self.initial_metadata:
            raise RuntimeError("Held metadata changed after adapter installation")
        rewritten = ["git", "--no-replace-objects", *command[1:]]
        if command == current:
            rewritten += [".", *(":(top,literal,exclude)" + path for path in sorted(self.held))]
        with bounded_git_environment():
            result = self.delegate(self.root, rewritten)
        if self.metadata() != before:
            raise RuntimeError("Held metadata changed during bounded reader diff")
        self.events.append({"surface": "index" if command == cached else "public_worktree",
                            "original_command": command, "executed_command": rewritten,
                            "returncode": result.returncode,
                            "held_worktree_exclusions": 0 if command == cached else len(self.held),
                            "held_stage_tree_metadata": "EXACT",
                            "held_worktree_body_integrity": "UNKNOWN"})
        return result

    def receipt(self):
        if self.metadata() != self.initial_metadata:
            raise RuntimeError("Held metadata changed before receipt")
        return {"scope": "Actual public reader with exact held metadata gate and explicit native worktree exclusions",
                "full_protected_local_reader_cli": "NOT_RUN",
                "held_worktree_body_integrity": "UNKNOWN",
                "baseline": self.baseline, "root": str(self.root), "held_paths": sorted(self.held),
                "known_held_links_per_body": 2 if self.known_links is not None else 1,
                "events": self.events}

def install(root, held):
    """Install only in the admitted hosted checkout before the reader import."""
    from source_alias_absence_boundary import PROTECTED_PATHS
    root = Path(root).resolve()
    if root != Path(os.environ.get("GITHUB_WORKSPACE", "")).absolute():
        raise RuntimeError("Reader root differs from admitted hosted checkout")
    if len(held) != 5 or {row["path"] for row in held} != set(PROTECTED_PATHS):
        raise RuntimeError("Protected public metadata population differs")
    owner_map = (root / "docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json").read_bytes()
    if (hashlib.sha256(owner_map).hexdigest() != OWNER_MAP_SHA256
            or json.loads(owner_map)["baseline"]["commit"] != BASELINE):
        raise RuntimeError("Reader owner map or pinned currentness baseline changed")
    reader_path = root / "scripts/check_reader_pilot.py"
    if hashlib.sha256(reader_path.read_bytes()).hexdigest() != READER_SHA256:
        raise RuntimeError("Production reader differs from received source")
    resolver_path = root / "scripts/resolve_t20_v6_source.py"
    if hashlib.sha256(resolver_path.read_bytes()).hexdigest() != RESOLVER_SHA256:
        raise RuntimeError("Production resolver differs from received source")
    resolver = importlib.import_module("resolve_t20_v6_source")
    if Path(resolver.__file__).resolve() != resolver_path:
        raise RuntimeError("Resolver is imported from another checkout")
    original = resolver.readonly_git_diff
    if isinstance(original, HeldReaderDiffBoundary):
        raise RuntimeError("Bounded reader adapter is already installed")
    boundary = HeldReaderDiffBoundary(root, held, BASELINE, original)
    resolver.readonly_git_diff = boundary
    for module in tuple(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file and Path(file).resolve() == reader_path:
            if getattr(module, "readonly_git_diff", None) is not original:
                raise RuntimeError("Reader diff was already substituted")
            module.readonly_git_diff = boundary
    return boundary
