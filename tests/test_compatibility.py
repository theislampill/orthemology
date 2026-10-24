"""Named reading, coverage and wrong-source controls for the public CLI."""
import os
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(os.environ.get("ORTHEMOLOGY_TEST_REPO", Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(ROOT / "tools"))
CLI = Path(os.environ.get("ORTHEMOLOGY_TEST_CLI", ROOT / "tools/corpus.py"))

def row(path, data):
    return {"path": path, "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
            "bytes": len(data), "mode": "100644", "pack": "readings"}

class NamedReading(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ.get("ORTHEMOLOGY_TEST_TMPDIR"))
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "corpus").mkdir()
        self.cache = self.root / "cache"
        (self.cache / "objects").mkdir(parents=True)
        self.primary = b"Full theorem: a continuous injective map preserves dimension under the stated assumptions.\n"
        self.review = b"Review: conditional on the norm identity; this is not a fresh kernel proof.\n"
        self.rows = [row("papers/geometry.md", self.primary), row("reviews/geometry.md", self.review)]
        self.manifest = {"schema_version": 1, "repository": "https://github.com/theislampill/orthemology",
                         "baseline": {"commit": "a"*40, "files": 2},
                         "occurrences": self.rows, "packs": {}, "profiles": {}}
        (self.root / "corpus/archives.lock.json").write_text(json.dumps(self.manifest))
        self.work = {"id": "dimension-and-continuity", "title": "Dimension and continuity",
                     "aliases": ["historical-code"], "subjects": ["geometry"], "owner": {},
                     "original_record": {"review_status": "conditional ordinary proof"},
                     "source_owned_status": {"catalogue_review_status": "conditional ordinary proof"},
                     "sources": [dict(self.rows[0], role="primary", version="a"*40),
                                 dict(self.rows[1], role="review", version="a"*40)]}
        catalogue = json.dumps([self.work["original_record"]]).encode()
        owner = row("catalogue.json", catalogue)
        self.rows.append(owner)
        self.work["owner"] = dict(owner, version="a"*40, json_pointer="/0")
        self.manifest["baseline"]["files"] = 3
        (self.root / "corpus/archives.lock.json").write_text(json.dumps(self.manifest))
        self.write_work()
        for r, b in zip(self.rows, (self.primary,self.review,catalogue)):
            (self.cache / "objects" / r["sha256"]).write_bytes(b)

    def write_work(self):
        (self.root / "corpus/works.jsonl").write_text(json.dumps(self.work)+"\n")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(CLI), "--root", str(self.root),
                               "--cache", str(self.cache), "--offline", "--no-git-source", *args],
                              capture_output=True, text=True)

    def test_list_and_search_meaningful_name(self):
        result = self.run_cli("search", "dimension")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dimension and continuity", result.stdout)
        self.assertNotIn("historical-code", result.stdout)

    def test_show_full_primary_review_and_truthful_status_together(self):
        result = self.run_cli("show", "--work", "dimension-and-continuity", "--include-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.primary.decode().strip(), result.stdout)
        self.assertIn(self.review.decode().strip(), result.stdout)
        self.assertIn("conditional ordinary proof", result.stdout)
        self.assertNotIn("FORMALLY_VERIFIED", result.stdout)

    def test_wrong_named_edition_never_selects_current(self):
        result = self.run_cli("show", "--work", "dimension-and-continuity", "--version", "b"*40)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("AMBIGUOUS_VERSION", result.stderr)

    def test_changed_source_binding_rejected(self):
        self.work["sources"][0]["sha256"] = "b"*64
        self.write_work()
        result = self.run_cli("show", "--work", "dimension-and-continuity")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CORRUPT", result.stderr)

    def test_missing_review_does_not_report_complete_reading(self):
        (self.cache / "objects" / self.rows[1]["sha256"]).unlink()
        result = self.run_cli("show", "--work", "dimension-and-continuity", "--include-status")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("NOT_CACHED", result.stderr)

    def test_fulltext_reports_honest_coverage(self):
        result = self.run_cli("search", "norm identity", "--full-text")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("reviews/geometry.md", result.stdout)
        self.assertIn("searched=2", result.stdout)
        (self.cache / "objects" / self.rows[1]["sha256"]).unlink()
        result = self.run_cli("search", "norm identity", "--full-text")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unavailable=1", result.stdout)

    def test_legacy_resolution_requires_context(self):
        result = self.run_cli("resolve", "--legacy-path", "papers/geometry.md", "--context", "a"*40)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.rows[0]["sha256"], result.stdout)


    def test_baseline_materialisation_still_restores_exact_sources(self):
        destination=self.root/"baseline-workspace"
        result=self.run_cli("materialise","--profile",self.work["id"],"--version","a"*40,"--dest",str(destination))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual((destination/"papers/geometry.md").read_bytes(),self.primary)
        self.assertEqual((destination/"reviews/geometry.md").read_bytes(),self.review)

    def test_replay_inherits_global_context_and_preserves_child_option_order(self):
        import importlib.util
        import types
        from unittest.mock import patch
        spec=importlib.util.spec_from_file_location("compatibility_cli_search",CLI.parent/"search.py")
        search_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(search_module)
        captured=[]
        replay=types.SimpleNamespace(main=lambda args:(captured.append(args) or 7))
        with patch.dict(sys.modules,{"search":search_module,"replay":replay}):
            spec=importlib.util.spec_from_file_location("compatibility_cli_dispatch",CLI)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            result=module.main(["--root",str(self.root),"--cache",str(self.cache),"--offline","--no-git-source",
                                "replay","--timeout","19","--bundle","fixture.bundle","list"])
        self.assertEqual(result,7)
        self.assertEqual(captured,[["--root",str(self.root),"--cache",str(self.cache),"--offline","--no-git-source",
                                    "--timeout","19","--bundle","fixture.bundle","list"]])


    def test_historical_fidelity_review_is_not_controlling_scientific_review(self):
        self.work["sources"][1]["review_kind"]="historical_source_fidelity"
        self.write_work()
        result=self.run_cli("show","--work",self.work["id"],"--include-status")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("## Historical source-fidelity review",result.stdout)
        self.assertIn("Controlling scientific review: NOT IDENTIFIED",result.stdout)
        self.assertIn("does not establish controlling scientific review or current adoption",result.stdout)
        self.assertIn(self.review.decode().strip(),result.stdout)
        self.assertNotIn("Scientific review binding identified;",result.stdout)


class CurrentEditionReading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import importlib.util
        module_spec=importlib.util.spec_from_file_location("compatibility_maintenance_fixtures",Path(os.environ.get("ORTHEMOLOGY_MAINTENANCE_FIXTURES", ROOT/"tests/test_maintenance.py")))
        module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module)
        cls.Fixture=module.Fixture
        cls.markdown=staticmethod(module.markdown)
        cls.payload=staticmethod(module.payload)

    def setUp(self):
        self.fixture=self.Fixture()
        self.addCleanup(self.fixture.close)
        self.fixture.perform("supersession")
        import authority
        from source_provider import atomic_bytes
        provider=self.fixture.provider()
        # A cold current-work reader needs the immutable original authority
        # owners as well as the actual selected working sources. Populate only
        # those baseline input owners; named fetch must discover/cache the rest.
        for path in (authority.CWPATH,authority.CLPATH,authority.PUBLIC_MAP,authority.GRAPH,authority.AVPATH):
            data=provider.read_bytes(path,context=authority.BASELINE)
            row=provider.resolve(path,context=authority.BASELINE)
            atomic_bytes(self.fixture.cache/"objects"/row["sha256"],data)
        authority.write(self.fixture.root,provider)

    def run_cli(self,*args):
        f=self.fixture
        return subprocess.run([sys.executable,"-B",str(CLI),"--root",str(f.root),"--cache",str(f.cache),
                               "--offline","--no-git-source",*args],capture_output=True,text=True)

    def test_show_current_source_owned_status_and_real_decision(self):
        f=self.fixture
        result=self.run_cli("show","--work",f.work_id,"--version",f.target["version"],"--include-status")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("Source-owned edition status",result.stdout)
        self.assertIn('"simulation": true',result.stdout)
        self.assertIn(f.review_id,result.stdout)
        self.assertNotIn("Source-owned catalogue status",result.stdout)

    def test_predecessor_reading_does_not_borrow_current_review(self):
        f=self.fixture
        result=self.run_cli("show","--work",f.work_id,"--version",f.old["version"],"--include-status")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("Earlier fixture attribution",result.stdout)
        self.assertIn("no prior review bound here",result.stdout)
        self.assertNotIn("SIMULATION: this fixture review covers",result.stdout)
        self.assertNotIn(f.review_id,result.stdout)

    def test_compare_exact_predecessor_and_selected_current(self):
        f=self.fixture
        result=self.run_cli("compare","--work",f.work_id,"--from",f.old["version"],"--to",f.target["version"])
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("--- "+f.old["version"],result.stdout)
        self.assertIn("+++ "+f.target["version"],result.stdout)
        self.assertIn("explicitly stated stronger premise",result.stdout)
        wrong=self.run_cli("compare","--work",f.work_id,"--from","unknown-same-name-edition","--to",f.target["version"])
        self.assertNotEqual(wrong.returncode,0)
        self.assertIn("AMBIGUOUS_VERSION",wrong.stderr)

    def test_fetch_current_caches_owner_closure_and_both_path_versions(self):
        f=self.fixture
        result=self.run_cli("fetch","--work",f.work_id,"--version",f.target["version"])
        self.assertEqual(result.returncode,0,result.stderr)
        receipt=json.loads(result.stdout)
        same_path=[r for r in receipt["sources"] if r["path"]==f.base_source]
        self.assertEqual({r["version"] for r in same_path},{f.old["version"],f.target["version"]})
        for source in (f.target,f.appointment):
            self.assertTrue((f.cache/"objects"/source["sha256"]).is_file())
        self.assertTrue(any(r["path"]==f.meta["decision"]["path"] for r in receipt["sources"]))
        # Prove the fetch result supports exact offline reading after removing
        # every selected current source's loose working copy.
        for source in f.lock["current_sources"]:
            (f.root/source["path"]).unlink(missing_ok=True)
        cold=self.run_cli("show","--work",f.work_id,"--version",f.target["version"],"--include-status")
        self.assertEqual(cold.returncode,0,cold.stderr)
        old=self.run_cli("show","--work",f.work_id,"--version",f.old["version"],"--include-status")
        self.assertEqual(old.returncode,0,old.stderr)
        self.assertNotIn(f.review_id,old.stdout)

    def add_second_selected_edition(self):
        import authority,copy
        f=self.fixture
        first_locator=copy.deepcopy(f.lock["current_works"][0])
        f.meta["statement"]="EVOLUTION_TOKEN first selected result"
        f.update_meta()
        f.decision["target"]=f.exact(f.target);f.decision["review"]["target"]=f.exact(f.target);f.update_decision()
        first=copy.deepcopy(f.target)
        second_meta=copy.deepcopy(f.meta)
        second_meta["statement"]="EVOLUTION_TOKEN second selected result"
        second_meta["decision"]["version"]="fixture-second-decision"
        second=f.register(f.base_source,"fixture-second-selected",self.markdown(second_meta))
        second_decision=copy.deepcopy(f.decision)
        second_decision["target"]=f.exact(second);second_decision["review"]["target"]=f.exact(second)
        f.register(second_meta["decision"]["path"],second_meta["decision"]["version"],self.payload(second_decision))
        f.lock["current_works"]=[first_locator,{"path":second["path"],"version":second["version"]}]
        authority.write(f.root,f.provider())
        return first,second

    def test_multiple_selected_editions_require_explicit_choice(self):
        f=self.fixture
        first,second=self.add_second_selected_edition()
        ambiguous=self.run_cli("show","--work",f.work_id)
        self.assertNotEqual(ambiguous.returncode,0)
        self.assertIn("AMBIGUOUS_VERSION",ambiguous.stderr)
        ambiguous_fetch=self.run_cli("fetch","--work",f.work_id)
        self.assertNotEqual(ambiguous_fetch.returncode,0)
        for selected,word in ((first,"first"),(second,"second")):
            read=self.run_cli("show","--work",f.work_id,"--version",selected["version"])
            self.assertEqual(read.returncode,0,read.stderr)
            self.assertIn("EVOLUTION_TOKEN "+word+" selected result",read.stdout)

    def test_fulltext_preserves_path_and_version_pair(self):
        f=self.fixture
        first,second=self.add_second_selected_edition()
        result=self.run_cli("search","EVOLUTION_TOKEN","--full-text","--all-versions","--work",f.work_id)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn(f.base_source+"@"+first["version"],result.stdout)
        self.assertIn(f.base_source+"@"+second["version"],result.stdout)
        chosen=self.run_cli("search","EVOLUTION_TOKEN","--full-text","--work",f.work_id,"--version",first["version"])
        self.assertEqual(chosen.returncode,0,chosen.stderr)
        self.assertIn("EVOLUTION_TOKEN first",chosen.stdout)
        self.assertNotIn("EVOLUTION_TOKEN second",chosen.stdout)

    def test_current_materialisation_rejects_before_destination_creation(self):
        f=self.fixture
        destination=f.root/"uncreated-current-workspace"
        result=self.run_cli("materialise","--profile",f.work_id,"--version",f.target["version"],"--dest",str(destination))
        self.assertNotEqual(result.returncode,0)
        self.assertIn("CURRENT_MATERIALISATION_UNSUPPORTED",result.stderr)
        self.assertFalse(destination.exists())

    def test_forged_current_status_fails_before_reading(self):
        f=self.fixture
        path=f.root/"corpus/works.jsonl"
        rows=[json.loads(line) for line in path.read_text().splitlines()]
        rows[-1]["source_owned_status"]["scope"]="Unreviewed whole-programme acceptance"
        path.write_text("".join(json.dumps(r)+"\n" for r in rows))
        result=self.run_cli("show","--work",f.work_id,"--version",f.target["version"],"--include-status")
        self.assertNotEqual(result.returncode,0)
        self.assertIn("AUTHORITY_PROJECTION_DRIFT",result.stderr)
        self.assertNotIn("Complete reading",result.stdout)

if __name__ == "__main__":
    unittest.main()
