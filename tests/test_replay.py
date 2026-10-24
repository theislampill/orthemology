"""Consumer rejection controls. Set test roots to an exact archive-backed fixture."""
import copy, io, json, os, sys, tarfile, tempfile, unittest
from pathlib import Path

ROOT=Path(os.environ.get("ORTHEMOLOGY_TEST_ROOT",Path(__file__).resolve().parents[1]))
CACHE=Path(os.environ.get("ORTHEMOLOGY_TEST_CACHE",ROOT/"cache"))
sys.path.insert(0,str(ROOT/"tools"))
import replay
from source_provider import SourceProvider, SourceError
from publication import package_members

class ConsumerControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provider=SourceProvider(ROOT,CACHE,offline=True,git_repo=False)
        cls.spec=replay.load_spec(cls.provider)

    def altered_provider(self):
        provider=copy.copy(self.provider)
        provider.manifest=copy.deepcopy(self.provider.manifest)
        provider.occurrences=dict(self.provider.occurrences)
        return provider

    def test_exact_upstream_release_tag_survives_pinned_shallow_acquisition(self):
        import subprocess
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);origin=root/"origin";origin.mkdir()
            def run(*args,cwd=origin):
                return subprocess.check_output(["git",*map(str,args)],cwd=cwd,
                                               stderr=subprocess.DEVNULL,text=True).strip()
            run("init","-b","main");(origin/"source").write_text("Exact official fixture.\n")
            run("add","source");run("-c","user.name=Fixture","-c","user.email=fixture@example.test",
                                     "-c","commit.gpgsign=false","commit","-m","official fixture")
            wanted=run("rev-parse","HEAD");run("tag","v0.0.57")
            (origin/"source").write_text("Different source.\n");run("add","source")
            run("-c","user.name=Fixture","-c","user.email=fixture@example.test",
                "-c","commit.gpgsign=false","commit","-m","different fixture")
            run("tag","v9.9.9")
            checkout=root/"checkout";checkout.mkdir();run("init",cwd=checkout)
            run("remote","add","origin",origin,cwd=checkout)
            run("fetch","--depth","1","origin",wanted,cwd=checkout)
            run("checkout","--detach","FETCH_HEAD",cwd=checkout)
            before=subprocess.run(["git","describe","--tags","--exact-match","HEAD"],
                                  cwd=checkout,capture_output=True)
            self.assertNotEqual(before.returncode,0)
            session=replay.Session(root/"run")
            got=replay.acquire_release_tag(session,checkout,
                    {"name":"proofwidgets","inputRev":"v0.0.57","rev":wanted})
            self.assertEqual(got["revision"],wanted)
            self.assertEqual(run("describe","--tags","--exact-match","HEAD",cwd=checkout),"v0.0.57")
            self.assertEqual(run("status","--porcelain",cwd=checkout),"")
            with self.assertRaisesRegex(ValueError,"release tag.*revision"):
                replay.acquire_release_tag(session,checkout,
                    {"name":"proofwidgets","inputRev":"v9.9.9","rev":wanted})
            self.assertEqual(run("rev-parse","HEAD",cwd=checkout),wanted)

    def test_complete_workflow_population_and_fixed_cases(self):
        self.assertEqual(len(self.spec["workflow"]["steps"]),71)
        self.assertEqual(sum(len(x["command"].splitlines()) for x in self.spec["workflow"]["steps"]),158)
        self.assertEqual(len(self.spec["cases"]),8)
        self.assertFalse(any(x["retired"] for x in self.spec["workflow"]["steps"]))

    def test_zero_population_rejected(self):
        p=self.altered_provider();p.occurrences={}
        with self.assertRaisesRegex(ValueError,"population"): replay.load_spec(p)

    def test_missing_workflow_gate_rejected(self):
        p=self.altered_provider();p.manifest["replay"]["workflow"]["steps"].pop()
        with self.assertRaisesRegex(ValueError,"CI obligation"): replay.load_spec(p)

    def test_replaced_assertion_rejected_even_with_updated_hash(self):
        p=self.altered_provider();step=p.manifest["replay"]["workflow"]["steps"][4]
        step["command"]="python -c 'pass'";step["command_sha256"]=replay.sha256(step["command"].encode())
        with self.assertRaisesRegex(ValueError,"denominator|original workflow"): replay.load_spec(p)

    def test_undeclared_retirement_rejected(self):
        p=self.altered_provider();p.manifest["replay"]["workflow"]["steps"][4]["retired"]=True
        with self.assertRaisesRegex(ValueError,"retirement"): replay.load_spec(p)

    def test_wrong_runner_pin_rejected(self):
        p=self.altered_provider();p.manifest["replay"]["cases"][3]["runner"]["sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"runner or descriptor|fixed selection"): replay.load_spec(p)

    def test_wrong_edition_rejected(self):
        p=self.altered_provider();p.manifest["replay"]["baseline"]["commit"]="0"*40
        with self.assertRaisesRegex(ValueError,"baseline"): replay.load_spec(p)

    def test_no_loose_source_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/"root";(root/"corpus").mkdir(parents=True)
            (root/"corpus/archives.lock.json").write_bytes(self.provider.lock_bytes)
            relative=self.spec["cases"][0]["runner"]["path"]
            (root/relative).parent.mkdir(parents=True);(root/relative).write_bytes(self.provider.read_bytes(relative))
            p=SourceProvider(root,Path(folder)/"empty-cache",offline=True,git_repo=False)
            with self.assertRaises(SourceError): p.read_bytes(relative)

    def test_borrowed_receipt_directory_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/"RUN.json").write_text('{"status":"PASS"}')
            with self.assertRaisesRegex(ValueError,"receipt reuse"): replay.Session(folder)

    def test_exact_interpreter_digest_cannot_be_waived(self):
        version=".".join(map(str,sys.version_info[:3]))
        with self.assertRaisesRegex(ValueError,"digest differs"):
            replay.python_preflight(sys.executable,version,"0"*64)

    def test_wrong_interpreter_version_is_blocked(self):
        with self.assertRaises(replay.Blocked):
            replay.python_preflight(sys.executable,"0.0.0")

    def test_timeout_never_becomes_negative_theorem_success(self):
        with tempfile.TemporaryDirectory() as folder:
            s=replay.Session(Path(folder)/"run")
            with self.assertRaises(TimeoutError):
                s.run([sys.executable,"-E","-B","-c","import time; time.sleep(10)"],folder,timeout=0.1)
            self.assertTrue(s.receipt["commands"][0]["timeout"])
            self.assertFalse(s.receipt["execution_credit"])

    def test_nonzero_process_exit_remains_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            s=replay.Session(Path(folder)/"run")
            with self.assertRaises(replay.ProcessFailure):
                s.run([sys.executable,"-E","-B","-c","raise SystemExit(7)"],folder)
            self.assertEqual(s.receipt["commands"][0]["exit"],7)
            self.assertFalse(s.receipt["execution_credit"])

    def package_fixture(self,folder):
        root=Path(folder);artifact="orthemma-ortheme-systems-draft"
        (root/"artifacts").mkdir()
        for suffix in [".source-manifest.json",".source.tar.gz"]:
            relative="artifacts/"+artifact+suffix
            (root/relative).write_bytes(self.provider.read_bytes(relative))
        return root,artifact

    def test_complete_publication_package(self):
        with tempfile.TemporaryDirectory() as folder:
            root,artifact=self.package_fixture(folder)
            self.assertEqual(len(package_members(root,artifact)["members"]),4)

    def test_main_tex_alone_cannot_replace_complete_package(self):
        with tempfile.TemporaryDirectory() as folder:
            root,artifact=self.package_fixture(folder);base=root/"artifacts"
            archive=base/(artifact+".source.tar.gz");buffer=io.BytesIO()
            with tarfile.open(fileobj=io.BytesIO(archive.read_bytes()),mode="r:gz") as original:
                members=[(m,original.extractfile(m).read()) for m in original if m.name.endswith("/main.tex")]
            with tarfile.open(fileobj=buffer,mode="w:gz") as replacement:
                for member,data in members: replacement.addfile(member,io.BytesIO(data))
            archive.write_bytes(buffer.getvalue())
            manifest_path=base/(artifact+".source-manifest.json")
            manifest=json.loads(manifest_path.read_text());manifest["archive"]["sha256"]=replay.sha256(archive.read_bytes())
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,"missing complete"): package_members(root,artifact)

    def test_wrong_suite_selection_rejected(self):
        p=self.altered_provider();p.manifest["replay"]["cases"][3]["selection"]="another-suite"
        with self.assertRaisesRegex(ValueError,"fixed selection"): replay.load_spec(p)

    def test_foreign_imported_helper_rejected(self):
        import types
        previous=sys.modules.get("validate_research_continuations")
        sys.modules["validate_research_continuations"]=types.SimpleNamespace(__file__="/foreign/helper.py")
        try:
            with tempfile.TemporaryDirectory() as folder:
                with self.assertRaisesRegex(ValueError,"foreign helper"):
                    replay.load_original(Path(folder),"scripts/replay_research_continuations.py","wrong_helper")
        finally:
            if previous is None: sys.modules.pop("validate_research_continuations",None)
            else: sys.modules["validate_research_continuations"]=previous

    def test_download_wrong_digest_leaves_no_installable_artifact(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/"source";source.write_bytes(b"public fixture")
            dest=Path(folder)/"download"
            with self.assertRaisesRegex(ValueError,"identity differs"):
                replay.download_exact(source.as_uri(),dest,{"bytes":source.stat().st_size,"sha256":"0"*64})
            self.assertFalse(dest.exists())

    def test_release_link_cannot_escape_fresh_runtime(self):
        import subprocess
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);buffer=io.BytesIO()
            with tarfile.open(fileobj=buffer,mode="w") as tar:
                member=tarfile.TarInfo("runtime/bin/lean");member.type=tarfile.SYMTYPE;member.linkname="../../../../outside"
                tar.addfile(member)
            archive=root/"runtime.tar.zst"
            subprocess.run(["zstd","-q","-o",str(archive)],input=buffer.getvalue(),check=True)
            with self.assertRaises((ValueError,SourceError)):
                replay.extract_official_release(archive,root/"runtime")
            self.assertFalse((root/"outside").exists())

    def test_ci_provisioned_path_is_consumed_between_steps(self):
        with tempfile.TemporaryDirectory() as folder:
            session=replay.Session(Path(folder)/"run");path=replay.ci_environment(session)
            binary=session.out/"tmp/pinned-poppler/bin";binary.mkdir(parents=True)
            path.write_text(str(binary)+"\n")
            replay.apply_ci_paths(session,path)
            self.assertTrue(session.env["PATH"].startswith(str(binary)+os.pathsep))
            self.assertEqual(path.read_text(),"")
            self.assertEqual(session.env["GITHUB_ACTIONS"],"true")

    def test_ci_path_cannot_escape_isolated_session(self):
        with tempfile.TemporaryDirectory() as folder:
            session=replay.Session(Path(folder)/"run");path=replay.ci_environment(session)
            path.write_text(str(Path(folder))+"\n")
            with self.assertRaisesRegex(ValueError,"escapes"):
                replay.apply_ci_paths(session,path)

    def test_keep_going_preserves_failure_and_attempts_later_obligations(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            session=replay.Session(Path(folder)/"run");seen=[]
            def run(argv,cwd,**kwargs):
                if argv[-1]=="command -v python": return sys.executable
                seen.append(argv[-1])
                if argv[-1]=="first-fails": raise replay.ProcessFailure("first failure")
                return ""
            session.run=run
            spec={"workflow":{"steps":[{"id":"first","command":"first-fails"},{"id":"second","command":"second-runs"}]}}
            with patch.object(replay,"python_preflight",return_value={}):
                with self.assertRaisesRegex(replay.ProcessFailure,"1 original CI obligations failed"):
                    replay.run_ci(Path(folder),spec,session,sys.executable,"all",True)
            self.assertEqual(seen,["first-fails","second-runs"])
            self.assertEqual(session.receipt["ci_failures"][0]["id"],"first")
            self.assertFalse(session.receipt["execution_credit"])

    def test_current_head_not_old_reviewed_publication_tree(self):
        with tempfile.TemporaryDirectory() as folder:
            root,artifact=self.package_fixture(folder);path=root/"artifacts"/(artifact+".source-manifest.json")
            manifest=json.loads(path.read_text());manifest["source_commit"]=replay.BASELINE;path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,"reviewed publication commit"): package_members(root,artifact)

if __name__=="__main__": unittest.main()
