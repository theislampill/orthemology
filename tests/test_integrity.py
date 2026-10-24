"""Behavioural safety tests for exact corpus access and fresh restoration."""
import hashlib
import importlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def record(path, data, **extra):
    return dict(path=path, bytes=len(data), sha256=digest(data),
                git_blob=blob(data), mode="100644", pack="scholarship", **extra)

class CorpusIntegrity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        (self.repo / "corpus").mkdir(parents=True)
        self.cache = self.root / "cache"
        self.cache.mkdir()
        self.a = b"A substantive theorem.\n"
        self.b = b"Review: conditional on the stated hypothesis.\n"
        self.rows = [record("papers/theorem.md", self.a), record("reviews/theorem.md", self.b),
                     record("historical/copy.md", self.a)]
        self.manifest = {"schema_version": 1,
            "repository": "https://github.com/theislampill/orthemology",
            "baseline": {"commit": "a"*40, "tree": None, "files": 3},
            "occurrences": self.rows, "packs": {}, "profiles": {}}
        self.write_manifest()

    def write_manifest(self):
        (self.repo / "corpus/archives.lock.json").write_text(json.dumps(self.manifest))

    def provider(self, **kw):
        source = importlib.import_module("source_provider")
        return source.SourceProvider(self.repo, self.cache, offline=True, **kw)

    def cache_bytes(self):
        dest = self.cache / "objects"
        dest.mkdir(exist_ok=True)
        for data in (self.a, self.b):
            (dest / digest(data)).write_bytes(data)

    def test_exact_bytes_and_equal_byte_logical_aliases(self):
        self.cache_bytes()
        p = self.provider()
        self.assertEqual(p.read_bytes(self.rows[0]["path"]), self.a)
        self.assertEqual(p.read_bytes(self.rows[2]["path"]), self.a)
        self.assertNotEqual(p.resolve_legacy(self.rows[0]["path"], "a"*40)["path"],
                            p.resolve_legacy(self.rows[2]["path"], "a"*40)["path"])

    def test_missing_has_explicit_unavailable_state(self):
        p = self.provider()
        with self.assertRaisesRegex(Exception, "NOT_CACHED|UNAVAILABLE"):
            p.read_bytes("papers/theorem.md")

    def test_cache_corruption_is_not_silently_repaired(self):
        self.cache_bytes()
        (self.cache / "objects" / digest(self.a)).write_bytes(b"wrong edition")
        with self.assertRaisesRegex(Exception, "CORRUPT"):
            self.provider().read_bytes("papers/theorem.md")

    def test_same_name_wrong_context_rejected(self):
        self.cache_bytes()
        with self.assertRaisesRegex(Exception, "AMBIGUOUS_VERSION|UNAVAILABLE"):
            self.provider().resolve_legacy("papers/theorem.md", "b"*40)

    def test_basename_does_not_resolve(self):
        with self.assertRaisesRegex(Exception, "UNAVAILABLE"):
            self.provider().read_bytes("theorem.md")

    def test_restricted_has_no_fallback(self):
        self.rows[0]["access"] = "restricted"
        self.write_manifest()
        self.cache_bytes()
        with self.assertRaisesRegex(Exception, "RESTRICTED"):
            self.provider().read_bytes("papers/theorem.md")

    def test_identity_only_does_not_fabricate_body(self):
        self.rows[0]["access"] = "identity-only"
        self.write_manifest()
        with self.assertRaisesRegex(Exception, "IDENTITY_ONLY"):
            self.provider().read_bytes("papers/theorem.md")

    def test_traversal_absolute_backslash_and_normalisation_rejected(self):
        for path in ("../escape", "/absolute", "a/../b", "a//b", "a\\b", "a/./b", "C:/evil", "e\u0301"):
            with self.subTest(path=path):
                self.manifest["occurrences"] = [record(path, self.a)]
                self.manifest["baseline"]["files"] = 1
                self.write_manifest()
                with self.assertRaisesRegex(Exception, "UNSAFE_PATH"):
                    self.provider()

    def test_duplicate_path_rejected(self):
        self.manifest["occurrences"].append(dict(self.rows[0]))
        self.manifest["baseline"]["files"] = 4
        self.write_manifest()
        with self.assertRaisesRegex(Exception, "DUPLICATE|COLLISION"):
            self.provider()

    def test_case_and_file_directory_collision_rejected(self):
        for path in ("PAPERS/theorem.md", "papers"):
            self.manifest["occurrences"] = [self.rows[0], record(path, self.b)]
            self.manifest["baseline"]["files"] = 2
            self.write_manifest()
            with self.assertRaisesRegex(Exception, "COLLISION"):
                self.provider()

    def test_duplicate_json_key_rejected(self):
        (self.repo / "corpus/archives.lock.json").write_text('{"schema_version":1,"schema_version":2}')
        with self.assertRaisesRegex(Exception, "DUPLICATE"):
            self.provider()

    def test_zero_population_does_not_pass(self):
        self.manifest["occurrences"] = []
        self.manifest["baseline"]["files"] = 0
        self.write_manifest()
        with self.assertRaisesRegex(Exception, "EMPTY|POPULATION"):
            self.provider()

    def test_cache_symlink_rejected(self):
        (self.cache / "objects").mkdir()
        external = self.root / "external"
        external.write_bytes(self.a)
        (self.cache / "objects" / digest(self.a)).symlink_to(external)
        with self.assertRaisesRegex(Exception, "UNSAFE_PATH"):
            self.provider().read_bytes("papers/theorem.md")

    def make_pack(self, mutate=None):
        path = self.cache / "scholarship.tar.xz"
        with tarfile.open(path, "w:xz") as archive:
            for row, data in zip(self.rows, (self.a, self.b, self.a)):
                info = tarfile.TarInfo(row["path"])
                info.size = len(data); info.mode = 0o644; info.mtime = 0
                if mutate:
                    info, data = mutate(info, data)
                archive.addfile(info, io.BytesIO(data) if info.isfile() else None)
        self.manifest["packs"]["scholarship"] = {
            "file": path.name, "bytes": path.stat().st_size,
            "sha256": digest(path.read_bytes()), "members": 3}
        self.write_manifest()
        return path

    def test_verified_pack_returns_exact_member(self):
        self.make_pack()
        self.assertEqual(self.provider().read_bytes("papers/theorem.md"), self.a)

    def test_truncated_pack_cannot_return_success(self):
        path = self.make_pack()
        path.write_bytes(path.read_bytes()[:-3])
        with self.assertRaisesRegex(Exception, "CORRUPT"):
            self.provider().read_bytes("papers/theorem.md")

    def test_rehashed_pack_with_unsafe_member_still_fails(self):
        def mutate(info, data):
            info.name = "../" + info.name
            return info, data
        self.make_pack(mutate)
        with self.assertRaisesRegex(Exception, "UNSAFE_PATH|CORRUPT"):
            self.provider().read_bytes("papers/theorem.md")

    def test_rehashed_pack_with_symlink_still_fails(self):
        def mutate(info, data):
            info.type = tarfile.SYMTYPE; info.linkname = "/tmp/escape"; info.size = 0
            return info, data
        self.make_pack(mutate)
        with self.assertRaisesRegex(Exception, "UNSAFE_PATH|CORRUPT"):
            self.provider().read_bytes("papers/theorem.md")

    def test_restore_is_exact_and_reused_destination_refused(self):
        self.cache_bytes()
        r = importlib.import_module("rehydrate")
        p = self.provider()
        dest = self.root / "restored"
        receipt = r.restore(p, dest)
        self.assertEqual(receipt["files"], 3)
        self.assertEqual((dest / "papers/theorem.md").read_bytes(), self.a)
        self.assertEqual(r.verify_workspace(p, dest)["tree"], receipt["tree"])
        with self.assertRaisesRegex(Exception, "EXISTS"):
            r.restore(p, dest)

    def test_completion_receipt_is_moved_last(self):
        self.cache_bytes()
        r = importlib.import_module("rehydrate")
        from unittest.mock import patch
        real_rename = r.os.rename
        moves = []
        def record_move(src, dest):
            moves.append(Path(src).name)
            return real_rename(src, dest)
        with patch.object(r.os, "rename", side_effect=record_move):
            r.restore(self.provider(), self.root / "restored")
        self.assertEqual(moves[-1], ".corpus-receipt.json")

    def test_missing_preflight_leaves_no_completion_receipt(self):
        r = importlib.import_module("rehydrate")
        dest = self.root / "missing"
        with self.assertRaises(Exception):
            r.restore(self.provider(), dest)
        self.assertFalse((dest / ".corpus-receipt.json").exists())

    def test_changed_workspace_and_extra_body_fail(self):
        self.cache_bytes()
        r = importlib.import_module("rehydrate")
        p = self.provider()
        dest = self.root / "restored"
        r.restore(p, dest)
        (dest / "undeclared.txt").write_text("unindexed")
        with self.assertRaisesRegex(Exception, "EXTRA|POPULATION"):
            r.verify_workspace(p, dest)
        (dest / "undeclared.txt").unlink()
        (dest / "papers/theorem.md").write_text("changed")
        with self.assertRaisesRegex(Exception, "CORRUPT"):
            r.verify_workspace(p, dest)

    def test_receipt_is_bound_to_manifest_and_not_a_validation_substitute(self):
        self.cache_bytes()
        r = importlib.import_module("rehydrate")
        p = self.provider()
        dest = self.root / "restored"
        r.restore(p, dest)
        receipt_path = dest / ".corpus-receipt.json"
        receipt = json.loads(receipt_path.read_text())
        receipt["baseline_commit"] = "b"*40
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(Exception, "RECEIPT"):
            r.verify_workspace(p, dest)

if __name__ == "__main__":
    unittest.main()
