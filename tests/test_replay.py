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
            from unittest.mock import patch
            # The separate 4.32.2 lock records historical inputRev=main but
            # selects an immutable commit. Never resolve or fetch current main.
            with patch.object(session,"run",side_effect=AssertionError("unexpected branch fetch")):
                raw=replay.acquire_locked_package_reference(session,checkout,
                    {"name":"proofwidgets","inputRev":"main","rev":wanted},"4.32.2")
                self.assertEqual(raw["revision"],wanted)
                self.assertEqual(raw["selection"],"locked-commit")
                self.assertFalse(raw["remote_branch_resolved"])
                with self.assertRaisesRegex(ValueError,"revision"):
                    replay.acquire_locked_package_reference(session,checkout,
                        {"name":"proofwidgets","inputRev":"main","rev":"0"*40},"4.32.2")
                with self.assertRaisesRegex(ValueError,"release tag"):
                    replay.acquire_locked_package_reference(session,checkout,
                        {"name":"proofwidgets","inputRev":"main","rev":wanted},"4.19.0")
                with self.assertRaisesRegex(ValueError,"reference contract"):
                    replay.acquire_locked_package_reference(session,checkout,
                        {"name":"proofwidgets","inputRev":"unreviewed-branch","rev":wanted},"4.32.2")

    def test_lake_prefixed_multiline_axiom_inventories_bind_original_names(self):
        source="import T299.Basic\nopen AR8R.T299\n#print axioms positive\n#print axioms empty\n"
        output=("info: T299/Receipts.lean:7:0: 'AR8R.T299.positive' depends on axioms: [propext,\n"
                " Classical.choice,\n Quot.sound]\n"
                "info: T299/Receipts.lean:8:0: 'AR8R.T299.empty' does not depend on any axioms\n")
        got=replay.fable_inventories(output,source,2)
        self.assertEqual(got,{"AR8R.T299.positive":["propext","Classical.choice","Quot.sound"],"AR8R.T299.empty":[]})
        for bad in (output.replace("AR8R.T299.empty","AR8R.T299.foreign"),
                    output.replace("AR8R.T299.empty","AR8R.T299.positive"),
                    output.replace("Quot.sound","sorryAx"),
                    output[:output.index("info: T299/Receipts.lean:8")]):
            with self.subTest(output=bad):
                with self.assertRaises(ValueError):replay.fable_inventories(bad,source,2)

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

    def test_output_boundary_rejects_parent_and_symlink_aliases_before_session(self):
        from unittest.mock import patch
        import types
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder);normal=base/"normal";normal.mkdir()
            bridge=base/"bridge";bridge.mkdir()
            link=base/"linked";link.symlink_to(normal,target_is_directory=True)
            provider=types.SimpleNamespace(root=normal.resolve())
            candidates=[bridge/".."/"normal"/"created",link/"created"]
            for dest in candidates:
                with self.subTest(destination=str(dest)):
                    with patch.object(replay,"SourceProvider",return_value=provider), \
                         patch.object(replay,"load_spec",return_value={}), \
                         patch.object(replay,"Session",side_effect=AssertionError("session started")):
                        with self.assertRaises((ValueError,SourceError)):
                            replay.main(["--root",str(normal),"--cache",str(base/"cache"),
                                "--out",str(dest),"provision","finite-foundation-controls"])
                    self.assertFalse((normal/"created").exists())

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


class EvidenceTransportControls(unittest.TestCase):
    """Synthetic log fixtures test transport only; they never earn proof credit."""
    @classmethod
    def setUpClass(cls):
        cls.provider=SourceProvider(ROOT,CACHE,offline=True,git_repo=False)
        cls.cases={r["id"]:r for r in cls.provider.manifest["replay"]["cases"]}
    def setUp(self):
        from types import SimpleNamespace
        self.temp=tempfile.TemporaryDirectory(dir=os.environ.get("ORTHEMOLOGY_TEST_TMPDIR"))
        self.folder=Path(self.temp.name);self.context=self.folder/"context";self.context.mkdir()
        self.out=self.folder/"run";self.out.mkdir();self.results=self.out/"results";self.results.mkdir()
        self.session=SimpleNamespace(out=self.out,receipt={},save=lambda:None,env={},run=lambda *a,**k:None)
        self.old_helper=sys.modules.pop("validate_research_continuations",None)
    def tearDown(self):
        sys.modules.pop("validate_research_continuations",None)
        if self.old_helper is not None:sys.modules["validate_research_continuations"]=self.old_helper
        self.temp.cleanup()
    def source(self,rel):
        p=self.context/rel;p.parent.mkdir(parents=True,exist_ok=True)
        raw=self.provider.read_bytes(rel);p.write_bytes(raw);return raw
    def put(self,rel,raw):
        p=self.results/rel;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(raw.encode() if isinstance(raw,str) else raw);return replay.sha256(p.read_bytes())
    def put_json(self,rel,row):
        self.put(rel,json.dumps(row,sort_keys=True))
    def case(self,id):
        case=self.cases[id];self.source(case["runner"]["path"])
        if case["kind"]!="native":
            return case,json.loads(self.source(case["descriptor"]["path"]))
        return case,None
    def finite(self):
        case,suite=self.case("finite-foundation-controls");steps=[]
        for row in suite["steps"]:
            step={"id":row["id"],"exit_code":0,"log_sha256":self.put(row["id"]+".log","finite fixture log\n"),
                  "source_hashes":{},"output_hashes":{}}
            for name in row["outputs"]:step["output_hashes"][name]=self.put(row["id"]+"/"+name,'{"fixture":true}\n')
            steps.append(step)
        result={"status":"PASS_NATIVE_CONTROLS","suite_id":suite["id"],"steps":steps}
        self.put_json("RECEIPT.json",result);return case,result
    def json_reference(self):
        case,suite=self.case("json-certificate-reference");rows=[]
        for id in ["_prerequisites"]+[r["id"] for r in suite["replay"]["stages"]]:
            name="prerequisites" if id=="_prerequisites" else id
            rows.append({"id":id,"terminal":"COMPLETED","exit_code":0,
                         "log_sha256":self.put("logs/"+name+".log","JSON fixture log\n"),"output_hashes":{}})
        summary=[{k:r[k] for k in ("id","terminal","exit_code","log_sha256")} for r in rows]
        result={"suite_id":suite["id"],"proof_scope":"FINITE","outcome":"FINITE_ONLY","exit_code":0,
                "stages":summary,"log_sha256":replay.sha256(json.dumps(
                    {r["id"]:r["log_sha256"] for r in rows},sort_keys=True,separators=(",",":")).encode()),
                "replay_evidence":{"stage_results":rows,"output_hashes":{},
                    "tool_fingerprints":{"python":{"version_log_sha256":self.put("logs/tool-python.log","Python fixture\n")}}}}
        self.put_json("RECEIPT.json",result);return case,result
    def hidden(self):
        case,suite=self.case("hidden-parity-pruning");self.source("scripts/validate_research_continuations.py")
        modules=[{"module":n,"status":"FRESH_COMPILE","exit_code":0,
                  "log_sha256":self.put("logs/"+n+".log","")} for n in suite["module_order"]]
        readbacks={};text=""
        for row in suite["targets"]:
            n=row["name"];readbacks[n]={"type":n+" : True","axioms":[]}
            text+=f"CONTINUATION_BEGIN {n}\n{n} : True\n'{n}' does not depend on any axioms\nCONTINUATION_END {n}\n"
        result={"status":"FRESH_KERNEL_COMPONENTS","kernel_verified":True,"modules":modules,"readbacks":readbacks,
                "original_controls":"NOT_RUN","readback_log_sha256":self.put("logs/readback.log",text),
                "compiler_version":"fixture compiler","dependency_checks":[]}
        self.put("logs/compiler.log","fixture compiler\n")
        for pin in suite["pins"]["packages"]:
            self.put("logs/"+pin["name"]+"-head.log",pin["revision"]+"\n")
            self.put("logs/"+pin["name"]+"-status.log","")
            result["dependency_checks"].append({"name":pin["name"]})
        self.put_json("RECEIPT.json",result);return case,result
    def native(self):
        import ast
        case,_=self.case("native-reference-and-formal");base="experiments/orthemology-v5/"
        for rel in ["source/formal_targets.json","formal_project/lake-manifest.json","source/verify.py",
                    "formal_project/build.py","source/build_gate.py","source/check_mutations.py","source/v4_mutations.py"]:
            self.source(base+rel)
        rows=json.loads((self.context/base/"source/formal_targets.json").read_text())["modules"]
        targets=[n for r in rows for n in r["targets"]]
        packages=json.loads((self.context/base/"formal_project/lake-manifest.json").read_text())["packages"]
        def audit(names):
            result={};text=""
            for n in names:
                body=f"{n} : True\n'{n}' does not depend on any axioms"
                text+=f"AUDIT_BEGIN {n}\n{body}\nAUDIT_END {n}\n"
                result[n]={"axioms":[],"type_and_axiom_text":body}
            return text,result
        def cmd(prefix,label,stdout="",stderr=""):
            record={"status":"EXIT","exit_code":0,"ok":True,"output_bytes":len((stdout+stderr).encode()),
                    "command":["fixture",label],"cwd":"fixture","elapsed_seconds":0}
            self.put_json(prefix+label+".json",record)
            self.put(prefix+label+".stdout.txt",stdout);self.put(prefix+label+".stderr.txt",stderr)
            return record
        def literals(rel,name):
            return next(ast.literal_eval(n.value) for n in ast.parse((self.context/base/rel).read_bytes()).body
                        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
        old=[];new=[]
        for r in literals("source/check_mutations.py","MUTATIONS"):
            row={"name":r[0],"test":r[-1],"positive_ok":True,"detected":True}
            old.append(row);self.put_json("v4/mutations/RECORD_"+r[0]+".json",row)
            self.put("v4/mutations/POSITIVE_"+r[0]+".txt","Ran 1 test\nOK\n")
            self.put("v4/mutations/MUTATION_"+r[0]+".txt","Ran 1 test\nAssertionError\nFAILED (failures=1)\n")
        for r in literals("source/v4_mutations.py","MUTANTS"):
            row={"name":r[0],"test":r[-1],"positive_ok":True,"detected_by_intended_test":True}
            new.append(dict(row));row["positive"]={"exit_code":0,"stderr":"Ran 1 test\nOK\n"}
            row["negative"]={"exit_code":1,"stderr":"Ran 1 test\nAssertionError\nFAILED (failures=1)\n"}
            self.put_json("v4/v4_mutations/"+r[0]+".json",row)
        v4={"overall":"REFERENCE_AND_REQUIRED_FORMAL_TARGETS_PASS"}
        for label in ["unit_tests","unit_tests_optimised","census","census_optimised","mutations","v4_mutations","positive_demonstration"]:
            if label.startswith("unit_tests"):v4[label]={**cmd("v4/",label,stderr="Ran 183 tests\n"),"tests":183}
            else:
                result={"results":old} if label=="mutations" else {"results":new} if label=="v4_mutations" else {"fixture":True}
                v4[label]={**cmd("v4/",label,json.dumps(result)),"results":result}
        text,decl=audit(targets)
        v4["lean"]={"kernel_verified":True,"declarations":decl,
                    "version_process":cmd("v4/","LEAN_VERSION"),
                    "builds":[{**cmd("v4/","LEAN_"+r["name"]),"artifact":{}} for r in rows],
                    "audit_process":cmd("v4/","LEAN_REQUIRED_AUDIT",text)}
        text,decl=audit(targets+["OrthemologyConvergence.upstreamGirard"])
        labels=["lean_version","lake_build","mathlib_head"]+["dependency_"+p["name"] for p in packages]+["mandatory_audit"]
        formal={"status":"KERNEL_AND_INVENTORY_PASS","kernel_verified":True,"axiom_audit":decl,"actual_axiom_union":[],
                "commands":[cmd("formal/",n,text if n=="mandatory_audit" else "") for n in labels]}
        self.put_json("v4/VERIFICATION.json",v4);self.put_json("formal/FORMAL_RECEIPT.json",formal)
        labels=["v4","mathematical_normal","mathematical_optimised","build_staging_normal","build_staging_optimised","formal"]
        result={"overall":"NATIVE_REFERENCE_AND_KERNEL_PASS","kernel_verified":True,"original_packet_replay":False,
                "commands":[cmd("",n,json.dumps(v4) if n=="v4" else json.dumps(formal) if n=="formal" else "") for n in labels]}
        self.put_json("VERIFICATION.json",result);return case,result
    def collect(self,pair):
        return replay.collect_original_evidence(self.context,*pair[:1],self.session,pair[1])
    def test_all_four_exact_nonzero_transport_populations(self):
        for factory,count in [(self.finite,30),(self.json_reference,6),(self.hidden,29),(self.native,151)]:
            with self.subTest(factory=factory.__name__):
                # Every fixture lives in a fresh directory; never reuse a receipt.
                self.tearDown();self.setUp()
                pair=factory();self.put("source/DO_NOT_EXPORT.py","private source sentinel")
                self.put("build/DO_NOT_EXPORT.olean","compiled object sentinel")
                doc=self.collect(pair)
                self.assertEqual(len(doc["files"]),count)
                self.assertFalse(doc["execution_credit"])
                self.assertNotIn("execution_credit",self.session.receipt)
                self.assertTrue(all(not r["path"].startswith(("source/","build/")) for r in doc["files"]))
                replay.verify_evidence_transport(self.out/"evidence",self.session.receipt["evidence_transport"]["sha256"])
    def test_every_finite_log_and_generated_output_is_required(self):
        pair=self.finite()
        required=[p for p in self.results.rglob("*") if p.is_file() and p.name!="RECEIPT.json"]
        self.assertEqual(len(required),29)
        for path in required:
            with self.subTest(path=path.relative_to(self.results).as_posix()):
                raw=path.read_bytes();path.unlink()
                with self.assertRaises((ValueError,OSError)):self.collect(pair)
                self.assertFalse((self.out/"evidence").exists())
                path.write_bytes(raw+b"corruption")
                with self.assertRaisesRegex(ValueError,"hash mismatch"):self.collect(pair)
                path.write_bytes(raw)
    def test_every_json_child_log_is_required(self):
        pair=self.json_reference()
        for path in (self.results/"logs").iterdir():
            with self.subTest(path=path.name):
                raw=path.read_bytes();path.unlink()
                with self.assertRaises((ValueError,OSError)):self.collect(pair)
                path.write_bytes(raw+b"corruption")
                with self.assertRaisesRegex(ValueError,"hash mismatch"):self.collect(pair)
                path.write_bytes(raw)
    def test_zero_population_and_removed_declared_output_rejected(self):
        for kind in ("finite","json_reference","hidden"):
            with self.subTest(kind=kind):
                self.tearDown();self.setUp();pair=getattr(self,kind)()
                result=pair[1]
                if kind=="finite":result["steps"]=[]
                elif kind=="json_reference":result["replay_evidence"]["stage_results"]=[]
                else:result["modules"]=[]
                self.put_json("RECEIPT.json",result)
                with self.assertRaisesRegex(ValueError,"population"):self.collect(pair)
        self.tearDown();self.setUp();pair=self.finite()
        row=next(r for r in pair[1]["steps"] if r["output_hashes"]);row["output_hashes"]={}
        self.put_json("RECEIPT.json",pair[1])
        with self.assertRaisesRegex(ValueError,"output population"):self.collect(pair)
    def test_hidden_readback_and_environment_streams_are_required(self):
        pair=self.hidden();log=self.results/"logs/readback.log";raw=log.read_bytes()
        log.write_bytes(raw[:-10])
        with self.assertRaisesRegex(ValueError,"hash mismatch"):self.collect(pair)
        log.write_bytes(raw);(self.results/"logs/compiler.log").unlink()
        with self.assertRaises((ValueError,OSError)):self.collect(pair)
    def test_hidden_receipt_rehash_cannot_mask_missing_target(self):
        pair=self.hidden();log=self.results/"logs/readback.log";raw=log.read_text()
        log.write_text(raw[:raw.rfind("CONTINUATION_BEGIN")])
        pair[1]["readback_log_sha256"]=replay.sha256(log.read_bytes());self.put_json("RECEIPT.json",pair[1])
        with self.assertRaises(ValueError):self.collect(pair)
    def test_native_stream_truncation_and_missing_nested_mutation_are_rejected(self):
        pair=self.native();path=self.results/"formal/mandatory_audit.stdout.txt";raw=path.read_bytes()
        path.write_bytes(raw[:-1])
        with self.assertRaisesRegex(ValueError,"streams truncated"):self.collect(pair)
        path.write_bytes(raw)
        path=next((self.results/"v4/v4_mutations").iterdir());path.unlink()
        with self.assertRaises((ValueError,OSError)):self.collect(pair)
    def test_native_rehashed_command_cannot_mask_missing_target(self):
        pair=self.native();path=self.results/"formal/mandatory_audit.stdout.txt";raw=path.read_text()
        path.write_text(raw[:raw.rfind("AUDIT_BEGIN")])
        formal=json.loads((self.results/"formal/FORMAL_RECEIPT.json").read_text())
        formal["commands"][-1]["output_bytes"]=len(path.read_bytes())
        self.put_json("formal/mandatory_audit.json",formal["commands"][-1]);self.put_json("formal/FORMAL_RECEIPT.json",formal)
        stdout=json.dumps(formal);self.put("formal.stdout.txt",stdout)
        pair[1]["commands"][-1]["output_bytes"]=len(stdout.encode())
        self.put_json("formal.json",pair[1]["commands"][-1]);self.put_json("VERIFICATION.json",pair[1])
        with self.assertRaisesRegex(ValueError,"audit coverage"):self.collect(pair)
    def test_symlink_child_log_rejected_without_export(self):
        pair=self.finite();path=self.results/(pair[1]["steps"][0]["id"]+".log")
        target=self.folder/"outside.log";target.write_bytes(path.read_bytes());path.unlink();path.symlink_to(target)
        with self.assertRaises(SourceError):self.collect(pair)
        self.assertFalse((self.out/"evidence").exists())
    def test_transported_evidence_rejects_loss_corruption_and_unlisted_body(self):
        self.collect(self.json_reference());directory=self.out/"evidence"
        digest=self.session.receipt["evidence_transport"]["sha256"]
        path=directory/"logs/tool-python.log";raw=path.read_bytes();path.unlink()
        with self.assertRaises((ValueError,OSError)):replay.verify_evidence_transport(directory,digest)
        path.write_bytes(raw+b"corrupt")
        with self.assertRaisesRegex(ValueError,"changed"):replay.verify_evidence_transport(directory,digest)
        path.write_bytes(raw);(directory/"foreign.json").write_text("{}")
        with self.assertRaisesRegex(ValueError,"unmanifested"):replay.verify_evidence_transport(directory,digest)
    def test_whole_case_credit_is_not_granted_when_transport_is_missing(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        pair=self.finite();(self.results/"knowledge.log").unlink()
        args=SimpleNamespace(python=sys.executable)
        with patch.object(replay,"python_preflight",return_value={"fixture":True}):
            with self.assertRaises((ValueError,OSError)):
                replay.run_case(self.context,pair[0],{},self.session,args)
        self.assertFalse(self.session.receipt.get("execution_credit",False))

if __name__=="__main__": unittest.main()
