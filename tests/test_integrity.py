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

    def alias_owners(self, disposition="REUSE", public_sha=None, conflict=False):
        from source_provider import sha256
        claim_path = "research/t20-v6-20261012/research-v6/foundations/CURRENT_FOUNDATIONAL_CLAIMS.json"
        map_path = "research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json"
        alias = "historical-catalogue/objects/exact-theorem"
        claims = {"claims":[{"canonical_source":{"canonical_byte_home":alias,"sha256":digest(self.a)},
                             "supporting_sources":[{"original_read_path":"older/theorem-source.md",
                              "canonical_byte_home":alias,"sha256":digest(self.a)}]}]}
        if conflict:
            claims["claims"].append({"canonical_source":{"canonical_byte_home":alias,"sha256":digest(self.b)}})
        mapping = {"objects":[{"source_sha256":digest(self.a),"public_sha256":public_sha or digest(self.a),
                              "repository_path":"papers/theorem.md","disposition":disposition}]}
        for path,obj in ((claim_path,claims),(map_path,mapping)):
            data=json.dumps(obj).encode()
            self.rows.append(record(path,data))
            (self.cache/"objects").mkdir(exist_ok=True)
            (self.cache/"objects"/sha256(data)).write_bytes(data)
        self.manifest["baseline"]["files"]=len(self.rows)
        self.write_manifest()
        return alias

    def test_source_owned_alias_resolves_exact_public_bytes_and_keeps_logical_path(self):
        self.cache_bytes()
        alias=self.alias_owners()
        p=self.provider(git_repo=False)
        row=p.resolve_legacy(alias,"a"*40)
        self.assertEqual(row["path"],"papers/theorem.md")
        self.assertEqual(row["legacy_path"],alias)
        self.assertEqual(p.read_bytes(alias),self.a)
        self.assertEqual(p.read_bytes("older/theorem-source.md"),self.a)
        self.assertIn("json_pointer",row["alias_owners"][0])

    def test_source_owned_alias_requires_exact_public_equivalence(self):
        self.cache_bytes()
        alias=self.alias_owners(public_sha=digest(self.b))
        with self.assertRaisesRegex(Exception,"CORRUPT|NONEXACT"):
            self.provider(git_repo=False).read_bytes(alias)

    def test_alias_does_not_substitute_projected_or_held_body(self):
        for disposition,expected in (("PROJECT","NONEXACT"),("IDENTITY_ONLY","IDENTITY_ONLY")):
            with self.subTest(disposition=disposition):
                self.setUp()
                self.cache_bytes()
                alias=self.alias_owners(disposition=disposition)
                with self.assertRaisesRegex(Exception,expected):
                    self.provider(git_repo=False).read_bytes(alias)

    def test_conflicting_alias_owner_is_rejected(self):
        self.cache_bytes()
        alias=self.alias_owners(conflict=True)
        with self.assertRaisesRegex(Exception,"COLLISION|CORRUPT"):
            self.provider(git_repo=False).read_bytes(alias)

    def test_alias_has_no_newest_or_hash_basename_fallback(self):
        self.cache_bytes()
        alias=self.alias_owners()
        p=self.provider(git_repo=False)
        with self.assertRaisesRegex(Exception,"AMBIGUOUS_VERSION"):
            p.resolve_legacy(alias,"b"*40)
        with self.assertRaisesRegex(Exception,"UNAVAILABLE"):
            p.read_bytes("some-other-catalogue/"+digest(self.a))

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

    def test_history_loss_invalidates_prior_completion(self):
        self.cache_bytes()
        import subprocess
        import shutil
        r = importlib.import_module("rehydrate")
        source = self.root / "history-source"
        source.mkdir()
        for row, data in zip(self.rows, (self.a,self.b,self.a)):
            file = source / row["path"]
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_bytes(data)
        def git(*args):
            return subprocess.check_output(["git","-C",str(source),*args],
                                           stderr=subprocess.DEVNULL,text=True).strip()
        git("init","-b","main")
        git("add",".")
        git("-c","user.name=Fixture","-c","user.email=fixture@example.test",
            "-c","commit.gpgsign=false","commit","-m","restoration fixture")
        self.manifest["baseline"]["commit"] = git("rev-parse","HEAD")
        self.manifest["baseline"]["tree"] = git("rev-parse","HEAD^{tree}")
        bundle = self.root / "fixture.bundle"
        git("bundle","create",str(bundle),"refs/heads/main")
        raw = bundle.read_bytes()
        self.manifest["history"] = {"bytes":len(raw),"sha256":digest(raw)}
        self.manifest["required_git_objects"] = [self.rows[0]["git_blob"]]
        self.write_manifest()
        p = self.provider()
        dest = self.root / "restored-history"
        r.restore(p,dest,with_history=True,bundle=bundle)
        shutil.move(str(dest/".git"),str(self.root/"saved-history"))
        with self.assertRaisesRegex(Exception,"HISTORY|CORRUPT"):
            r.verify_workspace(p,dest)

        second = self.root / "from-existing-git"
        receipt = r.restore(p,second,with_history=True,git_repository=source)
        self.assertEqual(receipt["tree"],self.manifest["baseline"]["tree"])
        self.assertTrue(receipt["history"])
        self.assertFalse((second/".git/objects/info/alternates").exists())
        self.assertEqual(r.verify_workspace(p,second)["tree"],receipt["tree"])

    def test_explicit_current_edition_and_preserved_predecessor(self):
        new = b"A newly proposed research finding.\n"
        entry = record("research/new-finding.md",new,version="proposal-1")
        self.manifest["current_sources"] = [entry]
        self.write_manifest()
        path = self.repo / entry["path"]
        path.parent.mkdir(parents=True);path.write_bytes(new)
        p = self.provider()
        self.assertEqual(p.read_bytes(entry["path"],context="proposal-1"),new)
        with self.assertRaisesRegex(Exception,"UNAVAILABLE"):
            p.read_bytes(entry["path"])
        with self.assertRaisesRegex(Exception,"AMBIGUOUS_VERSION|UNAVAILABLE"):
            p.read_bytes(entry["path"],context="proposal-2")
        (self.cache/"objects").mkdir()
        (self.cache/"objects"/entry["sha256"]).write_bytes(new)
        path.write_text("different later text")
        self.assertEqual(p.read_bytes(entry["path"],context="proposal-1"),new)

    def test_current_edition_cannot_borrow_changed_working_bytes(self):
        new = b"An exact proposal."
        entry = record("research/new.md",new,version="proposal-1")
        self.manifest["current_sources"]=[entry];self.write_manifest()
        path=self.repo/entry["path"];path.parent.mkdir();path.write_text("other")
        with self.assertRaisesRegex(Exception,"CORRUPT"):
            self.provider().read_bytes(entry["path"],context="proposal-1")

    def test_committed_current_predecessor_survives_cache_loss(self):
        import subprocess
        original=b"Exact first proposed edition.\n"
        entry=record("research/current.md",original,version="proposal-1",access="public")
        self.manifest["current_sources"]=[entry];self.write_manifest()
        path=self.repo/entry["path"];path.parent.mkdir();path.write_bytes(original)
        def git(*args):
            return subprocess.check_output(["git","-C",str(self.repo),*args],
                                           stderr=subprocess.DEVNULL,text=True).strip()
        git("init","-b","main");git("add",entry["path"])
        git("-c","user.name=Fixture","-c","user.email=fixture@example.test",
            "-c","commit.gpgsign=false","commit","-m","exact proposed source")
        path.write_bytes(b"A different unselected edition.\n")
        provider=self.provider()
        self.assertEqual(provider.read_bytes(entry["path"],context="proposal-1"),original)
        self.assertEqual(provider.sources_used[entry["path"]],"pinned-current-git-blob")
        with self.assertRaisesRegex(Exception,"CORRUPT"):
            self.provider(git_repo=False).read_bytes(entry["path"],context="proposal-1")

    def test_assembly_refuses_omitted_current_primary_owner(self):
        self.cache_bytes()
        self.manifest["profiles"]={"ordinary":{"initial_target":2,
            "existing_paths":{"papers/theorem.md":"paper.md"},"new_paths":["tools/cli.py"]}}
        self.manifest["current_works"]=[{"path":"research/new.md","version":"proposal-1"}]
        self.write_manifest()
        (self.repo/"tools").mkdir();(self.repo/"tools/cli.py").write_text("pass\n")
        r=importlib.import_module("rehydrate")
        with self.assertRaisesRegex(Exception,"PROFILE"):
            r.assemble(self.provider(),self.root/"thin")
        self.assertFalse((self.root/"thin").exists())

    def test_small_candidate_counts_every_file_and_rewrites_source_links(self):
        self.a = b"Theorem. [Review](../reviews/theorem.md). [Earlier](../historical/copy.md). [Archive](../historical/).\n"
        self.rows[0] = record("papers/theorem.md",self.a)
        self.rows[2] = record("historical/copy.md",self.a)
        self.manifest["occurrences"] = self.rows
        self.manifest["profiles"] = {"ordinary":{"initial_target":3,
            "existing_paths":{"papers/theorem.md":"mathematics/theorem.md",
                              "reviews/theorem.md":"mathematics/review.md"},
            "new_paths":["tools/cli.py"]}}
        self.write_manifest();self.cache_bytes()
        (self.repo/"tools").mkdir()
        (self.repo/"tools/cli.py").write_text("print(1)\n")
        r=importlib.import_module("rehydrate")
        dest=self.root/"thin"
        report=r.assemble(self.provider(),dest)
        self.assertEqual(report["files"],3)
        self.assertEqual(len([p for p in dest.rglob("*") if p.is_file()]),3)
        text=(dest/"mathematics/theorem.md").read_text()
        self.assertIn("[Review](review.md)",text)
        self.assertIn("github.com/theislampill/orthemology/blob/"+"a"*40+"/historical/copy.md",text)
        self.assertIn("github.com/theislampill/orthemology/tree/"+"a"*40+"/historical",text)
        self.assertFalse((dest/"historical").exists())

    def test_small_candidate_fails_before_writing_missing_new_interface(self):
        self.cache_bytes()
        self.manifest["profiles"]={"ordinary":{"initial_target":2,
            "existing_paths":{"papers/theorem.md":"paper.md"},"new_paths":["tools/missing.py"]}}
        self.write_manifest()
        r=importlib.import_module("rehydrate");dest=self.root/"thin"
        with self.assertRaisesRegex(Exception,"UNAVAILABLE"):
            r.assemble(self.provider(),dest)
        self.assertFalse(dest.exists())

    def scientific_profile_fixture(self):
        self.cache_bytes()
        self.manifest["profiles"]={"ordinary":{"initial_target":2,
            "existing_paths":{"papers/theorem.md":"foundations/current-claims.json"},
            "new_paths":["tools/cli.py"]}}
        self.write_manifest()
        (self.repo/"tools").mkdir();(self.repo/"tools/cli.py").write_text("pass\n")
        target=self.repo/"foundations/current-claims.json";target.parent.mkdir();target.write_bytes(self.a)
        return target

    def test_working_scientific_drift_rejected_before_assembly(self):
        target=self.scientific_profile_fixture()
        target.write_bytes(b"A different unsupported scientific assertion.\n")
        r=importlib.import_module("rehydrate")
        with self.assertRaisesRegex(Exception,"WORKING_SOURCE"):
            r.validate_working_sources(self.provider())
        with self.assertRaisesRegex(Exception,"WORKING_SOURCE"):
            r.assemble(self.provider(),self.root/"thin")
        self.assertFalse((self.root/"thin").exists())

    def test_scientific_source_cannot_be_exempted_as_editorial_interface(self):
        target=self.scientific_profile_fixture()
        target.write_bytes(b"An editorially promoted scientific claim.\n")
        self.manifest["profiles"]["ordinary"]["working_interfaces"]={
            "foundations/current-claims.json":record("foundations/current-claims.json",target.read_bytes())}
        self.write_manifest()
        with self.assertRaisesRegex(Exception,"INTERFACE|WORKING_SOURCE"):
            importlib.import_module("rehydrate").assemble(self.provider(),self.root/"thin")
        self.assertFalse((self.root/"thin").exists())

    def test_declared_current_scientific_edition_is_preserved_without_acceptance_claim(self):
        target=self.scientific_profile_fixture()
        new=b"A separately declared proposed research edition.\n";target.write_bytes(new)
        row=record("foundations/current-claims.json",new,version="proposal-2")
        self.manifest["current_sources"]=[row]
        self.manifest["current_works"]=[{"path":row["path"],"version":"proposal-2"}]
        self.write_manifest()
        r=importlib.import_module("rehydrate")
        receipt=r.assemble(self.provider(),self.root/"thin")
        self.assertEqual((self.root/"thin"/row["path"]).read_bytes(),new)
        self.assertEqual(receipt["mappings"][0]["origin"],"declared-exact-current-edition")
        target.write_bytes(b"Undeclared subsequent change")
        with self.assertRaisesRegex(Exception,"WORKING_SOURCE"):
            r.validate_working_sources(self.provider())

    def test_materialised_alias_tree_matches_independent_git_tree(self):
        import subprocess
        self.cache_bytes();alias=self.alias_owners()
        r=importlib.import_module("rehydrate");dest=self.root/"alias-workspace"
        result=r.materialise(self.provider(),[alias],dest)
        def git(*args):
            return subprocess.check_output(["git","-C",str(dest),*args],
                stderr=subprocess.DEVNULL,text=True).strip()
        git("init","-b","fixture");git("add","--",alias)
        self.assertEqual(result["tree"],git("write-tree"))
        self.assertEqual(result["files"],1)
        self.assertEqual((dest/alias).read_bytes(),self.a)

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
