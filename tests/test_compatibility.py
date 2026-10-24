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
        result=self.run_cli("materialise","--profile",self.work["id"],"--version","a"*40,"--context","reading","--dest",str(destination))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual((destination/"papers/geometry.md").read_bytes(),self.primary)
        self.assertEqual((destination/"reviews/geometry.md").read_bytes(),self.review)

    def test_named_workspace_requires_explicit_context_and_replay_history(self):
        for extra in ([],["--context","replay"]):
            destination=self.root/"must-not-exist"
            result=self.run_cli("materialise","--profile",self.work["id"],"--dest",str(destination),*extra)
            self.assertNotEqual(result.returncode,0,result.stdout)
            self.assertIn("WORKSPACE_CONTEXT" if not extra else "HISTORY_REQUIRED",result.stderr)
            self.assertFalse(destination.exists())

    def test_reading_bundle_does_not_claim_replay_dependency_closure(self):
        destination=self.root/"reading-only"
        result=self.run_cli("materialise","--profile",self.work["id"],"--context","reading","--dest",str(destination))
        self.assertEqual(result.returncode,0,result.stderr)
        receipt=json.loads(result.stdout)
        self.assertEqual(receipt["context"],"reading")
        self.assertFalse(receipt["dependency_closure"])
        self.assertFalse(receipt["execution_credit"])
        self.assertFalse((destination/".git").exists())

    def test_named_replay_restores_all_baseline_sources_and_exact_history(self):
        source=self.root/"git-source";source.mkdir()
        def git(*args):
            return subprocess.check_output(["git","-C",str(source),*args],text=True,stderr=subprocess.DEVNULL).strip()
        git("init","-q","-b","main")
        git("config","user.email","fixture@example.invalid");git("config","user.name","Fixture")
        for item in self.rows:
            target=source/item["path"];target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes((self.cache/"objects"/item["sha256"]).read_bytes())
        git("add",".");git("commit","-qm","Exact tiny baseline")
        commit=git("rev-parse","HEAD");tree=git("rev-parse","HEAD^{tree}")
        self.manifest["baseline"].update(commit=commit,tree=tree)
        bundle=self.root/"history.bundle";git("bundle","create",str(bundle),"--all")
        raw=bundle.read_bytes()
        self.manifest["history"]={"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}
        for item in self.work["sources"]+[self.work["owner"]]:item["version"]=commit
        (self.root/"corpus/archives.lock.json").write_text(json.dumps(self.manifest));self.write_work()
        destination=self.root/"complete-replay-context"
        result=self.run_cli("materialise","--profile",self.work["id"],"--context","replay","--bundle",str(bundle),"--dest",str(destination))
        self.assertEqual(result.returncode,0,result.stderr)
        receipt=json.loads(result.stdout)
        self.assertEqual(receipt["context"],"replay")
        self.assertTrue(receipt["dependency_closure"])
        self.assertFalse(receipt["execution_credit"])
        self.assertEqual(receipt["tree"],tree)
        self.assertEqual((destination/"catalogue.json").read_bytes(),(source/"catalogue.json").read_bytes())
        self.assertEqual(subprocess.check_output(["git","-C",str(destination),"rev-parse","HEAD"],text=True).strip(),commit)
        self.assertTrue(receipt["history"])

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


    def test_historical_fidelity_is_explicit_not_ordinary_reading_search_or_fetch(self):
        self.work["sources"][1]["review_kind"]="historical_source_fidelity"
        self.write_work()
        ordinary=self.run_cli("show","--work",self.work["id"],"--include-status")
        self.assertEqual(ordinary.returncode,0,ordinary.stderr)
        self.assertNotIn(self.review.decode().strip(),ordinary.stdout)
        self.assertIn("Controlling scientific review: NOT IDENTIFIED",ordinary.stdout)
        for role in ("all","historical"):
            explicit=self.run_cli("show","--work",self.work["id"],"--role",role,"--include-status")
            self.assertEqual(explicit.returncode,0,explicit.stderr)
            self.assertIn(self.review.decode().strip(),explicit.stdout)
        found=self.run_cli("search","norm identity","--full-text")
        self.assertEqual(found.returncode,0,found.stderr)
        self.assertNotIn("reviews/geometry.md@",found.stdout)
        all_found=self.run_cli("search","norm identity","--full-text","--all-versions")
        self.assertIn("reviews/geometry.md@",all_found.stdout)
        fetched=self.run_cli("fetch","--work",self.work["id"])
        self.assertEqual(fetched.returncode,0,fetched.stderr)
        self.assertNotIn(self.rows[1]["path"],[r["path"] for r in json.loads(fetched.stdout)["sources"]])

    def test_direct_verified_source_read_and_wrong_context(self):
        result=self.run_cli("show","--source","reviews/geometry.md","--version","a"*40)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn(self.review.decode().strip(),result.stdout)
        wrong=self.run_cli("show","--source","reviews/geometry.md","--version","b"*40)
        self.assertNotEqual(wrong.returncode,0)
        missing=self.run_cli("show","--source","unindexed.md","--version","a"*40)
        self.assertNotEqual(missing.returncode,0)
        implicit=self.run_cli("show","--source","reviews/geometry.md")
        self.assertNotEqual(implicit.returncode,0)

    def test_read_delivers_every_primary_and_review_byte_with_explicit_status(self):
        result=self.run_cli("read","--work",self.work["id"])
        self.assertEqual(result.returncode,0,result.stderr)
        records=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(records[0]["type"],"begin")
        self.assertEqual(records[-1]["type"],"end")
        self.assertEqual([r["sequence"] for r in records],list(range(len(records))))
        payloads={}
        for r in records:
            if r["type"]=="chunk":
                payloads.setdefault(r["payload"],[]).append(r)
        decoded={}
        for key,parts in payloads.items():
            content=b""
            for part in parts:
                self.assertEqual(part["offset"],len(content))
                raw=part["text"].encode("utf-8")
                self.assertEqual(part["bytes"],len(raw))
                self.assertLessEqual(len(raw),8192)
                self.assertEqual(part["sha256"],hashlib.sha256(raw).hexdigest())
                content+=raw
            decoded[key]=content
        descriptors=[r for r in records if r["type"]=="payload"]
        self.assertEqual(descriptors[1].get("source",{}).get("path"),"papers/geometry.md")
        self.assertEqual(descriptors[2].get("source",{}).get("role"),"review")
        self.assertEqual(decoded[1],self.primary)
        self.assertEqual(decoded[2],self.review)
        context=json.loads(decoded[0])
        self.assertEqual(context["status"]["catalogue_review_status"],"conditional ordinary proof")
        self.assertEqual(context["sources"][0]["sha256"],self.rows[0]["sha256"])
        self.assertEqual(context["sources"][1]["role"],"review")
        self.assertEqual(records[-1]["reader_receipt"],"NOT_CONFIRMED")
        self.assertFalse(records[-1]["execution_credit"])

    def test_read_chunks_preserve_unicode_bom_crlf_and_large_complete_body(self):
        data=("\ufeff# Long source\r\n"+("fiṭrah ∀x → source-grounded correction.\r\n"*2000)).encode("utf-8")
        self.primary=data
        changed=row(self.rows[0]["path"],data)
        self.rows[0]=changed
        self.work["sources"][0]=dict(changed,role="primary",version="a"*40)
        self.manifest["occurrences"]=self.rows
        (self.root/"corpus/archives.lock.json").write_text(json.dumps(self.manifest))
        (self.cache/"objects"/changed["sha256"]).write_bytes(data)
        self.write_work()
        result=self.run_cli("read","--work",self.work["id"],"--chunk-bytes","4096")
        self.assertEqual(result.returncode,0,result.stderr)
        records=[json.loads(line) for line in result.stdout.splitlines()]
        parts=[r for r in records if r["type"]=="chunk" and r["payload"]==1]
        self.assertGreater(len(parts),20)
        self.assertTrue(all(0<len(p["text"].encode("utf-8"))<=4096 for p in parts))
        self.assertEqual(b"".join(p["text"].encode("utf-8") for p in parts),data)

    def test_read_preflights_missing_review_without_partial_success_stream(self):
        (self.cache/"objects"/self.rows[1]["sha256"]).unlink()
        result=self.run_cli("read","--work",self.work["id"])
        self.assertNotEqual(result.returncode,0)
        self.assertIn("NOT_CACHED",result.stderr)
        self.assertEqual(result.stdout,"")

    def test_read_receiver_rejects_omission_substitution_duplication_and_wrong_work(self):
        result=self.run_cli("read","--work",self.work["id"],"--chunk-bytes","64")
        self.assertEqual(result.returncode,0,result.stderr)
        records=[json.loads(line) for line in result.stdout.splitlines()]
        target=self.root/"received.jsonl"
        def verify(rows,work=None):
            target.write_text("\n".join(json.dumps(x) for x in rows)+"\n")
            return self.run_cli("verify-reading","--work",work or self.work["id"],"--input",str(target))
        good=verify(list(reversed(records)))
        self.assertEqual(good.returncode,0,good.stderr)
        receipt=json.loads(good.stdout)
        self.assertTrue(receipt["complete_received_bytes"])
        self.assertEqual(receipt["scientific_comprehension"],"NOT_ASSESSED")
        bad_sets=[records[:-1],records+[records[1]],records[:2]+records[3:]]
        altered=json.loads(json.dumps(records))
        chunk=next(r for r in altered if r["type"]=="chunk" and r["payload"]==1)
        chunk["text"]="x"+chunk["text"][1:]
        chunk["sha256"]=hashlib.sha256(chunk["text"].encode()).hexdigest()
        bad_sets.append(altered)
        forged=json.loads(json.dumps(records))
        forged[0]["scientific_acceptance"]=True
        encoded=lambda value:json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
        forged[-1]["stream_sha256"]=hashlib.sha256(b"".join(encoded(r)+b"\n" for r in forged[:-1])).hexdigest()
        bad_sets.append(forged)
        for bad in bad_sets:
            with self.subTest(kind=len(bad)):
                rejected=verify(bad)
                self.assertNotEqual(rejected.returncode,0,rejected.stdout)
                self.assertNotIn('"complete_received_bytes": true',rejected.stdout)
        self.assertNotEqual(verify(records,"different-work").returncode,0)


    def test_read_bounds_serialized_frames_even_with_escape_heavy_text(self):
        data=(bytes([92])*30000)+b" exact final source line\n"
        self.primary=data
        changed=row(self.rows[0]["path"],data);self.rows[0]=changed
        self.work["sources"][0]=dict(changed,role="primary",version="a"*40)
        self.manifest["occurrences"]=self.rows
        (self.root/"corpus/archives.lock.json").write_text(json.dumps(self.manifest))
        (self.cache/"objects"/changed["sha256"]).write_bytes(data)
        self.write_work()
        result=self.run_cli("read","--work",self.work["id"])
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue(all(len(line.encode("utf-8"))<=12288 for line in result.stdout.splitlines()))
        records=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(b"".join(r["text"].encode() for r in records if r["type"]=="chunk" and r["payload"]==1),data)


    def test_read_receiver_bounds_raw_input_and_rejects_special_files(self):
        result=self.run_cli("read","--work",self.work["id"])
        self.assertEqual(result.returncode,0,result.stderr)
        target=self.root/"received.jsonl"
        target.write_text(" "*1048576+result.stdout)
        padded=self.run_cli("verify-reading","--work",self.work["id"],"--input",str(target))
        self.assertNotEqual(padded.returncode,0,"oversized raw record was accepted")
        self.assertIn("READING_RECEIPT",padded.stderr)
        fifo=self.root/"input-fifo"
        if hasattr(os,"mkfifo"):
            os.mkfifo(fifo)
            cmd=[sys.executable,"-B",str(CLI),"--root",str(self.root),"--cache",str(self.cache),
                 "--offline","--no-git-source","verify-reading","--work",self.work["id"],"--input",str(fifo)]
            try:
                blocked=subprocess.run(cmd,capture_output=True,text=True,timeout=2)
            except subprocess.TimeoutExpired:
                self.fail("receipt verification blocked on a non-regular file")
            self.assertNotEqual(blocked.returncode,0)
            self.assertIn("READING_RECEIPT",blocked.stderr)
        target.write_text(result.stdout)
        link=self.root/"input-link";link.symlink_to(target)
        rejected=self.run_cli("verify-reading","--work",self.work["id"],"--input",str(link))
        self.assertNotEqual(rejected.returncode,0)

    def test_read_receiver_malformed_record_type_is_attributable(self):
        result=self.run_cli("read","--work",self.work["id"])
        self.assertEqual(result.returncode,0,result.stderr)
        records=[json.loads(line) for line in result.stdout.splitlines()]
        records[1]["type"]=[]
        target=self.root/"bad-type.jsonl"
        target.write_text("\n".join(json.dumps(r) for r in records)+"\n")
        rejected=self.run_cli("verify-reading","--work",self.work["id"],"--input",str(target))
        self.assertNotEqual(rejected.returncode,0)
        self.assertIn("READING_RECEIPT",rejected.stderr)
        self.assertNotIn("Traceback",rejected.stderr)


    def test_read_receiver_deep_json_rejects_without_traceback(self):
        target=self.root/"deep.jsonl"
        target.write_text("["*3000+"0"+"]"*3000+"\n")
        rejected=self.run_cli("verify-reading","--work",self.work["id"],"--input",str(target))
        self.assertNotEqual(rejected.returncode,0)
        self.assertIn("READING_RECEIPT",rejected.stderr)
        self.assertNotIn("Traceback",rejected.stderr)
        self.assertEqual(rejected.stdout,"")

    def test_inline_reading_is_exact_and_response_bounded(self):
        with tempfile.TemporaryDirectory(dir=self.root.parent) as area:
            spool=Path(area)/"reading.jsonl"
            result=self.run_cli("read","--work",self.work["id"],"--spool",str(spool),
                                "--inline-bytes","1048576")
            self.assertEqual(result.returncode,0,result.stderr)
            response=json.loads(result.stdout);frames=response["inline_frames"]
            self.assertIsInstance(frames,list)
            self.assertLessEqual(len(result.stdout.encode()),1048576)
            canonical=lambda r:json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
            self.assertEqual(b"".join(canonical(r)+b"\n" for r in frames),spool.read_bytes())
            self.assertEqual(frames[-1]["reader_receipt"],"NOT_CONFIRMED")
            recovered=self.run_cli("reading-index","--work",self.work["id"],"--input",str(spool))
            self.assertEqual(recovered.returncode,0,recovered.stderr)
            descriptor=json.loads(recovered.stdout)
            self.assertNotIn("inline_frames",descriptor)
            self.assertLessEqual(len(recovered.stdout.encode()),12289)
            self.assertEqual(descriptor["sha256"],response["sha256"])
            self.assertEqual(descriptor["pages"],response["pages"])

    def test_inline_cap_counts_envelope_unicode_escaping_and_final_newline(self):
        data=("\ufeff"+("\\fiṭrah\r\n"*1500)).encode()
        changed=row(self.rows[0]["path"],data);self.rows[0]=changed
        self.work["sources"][0]=dict(changed,role="primary",version="a"*40)
        self.manifest["occurrences"]=self.rows
        (self.root/"corpus/archives.lock.json").write_text(json.dumps(self.manifest))
        (self.cache/"objects"/changed["sha256"]).write_bytes(data);self.write_work()
        with tempfile.TemporaryDirectory(dir=self.root.parent) as area:
            def run(index,limit):
                spool=Path(area)/f"reading-{index:03}.jsonl"
                result=self.run_cli("read","--work",self.work["id"],"--spool",str(spool),
                                    "--inline-bytes",str(limit))
                self.assertEqual(result.returncode,0,result.stderr)
                return result,json.loads(result.stdout)
            first,_=run(0,1048576);second,_=run(1,len(first.stdout.encode()))
            exact_size=len(second.stdout.encode())
            exact,desc=run(2,exact_size)
            self.assertEqual(len(exact.stdout.encode()),exact_size)
            self.assertIsInstance(desc["inline_frames"],list)
            small,desc=run(3,exact_size-1)
            self.assertIsNone(desc["inline_frames"])
            self.assertEqual(desc["inline_omitted"],"serialized response exceeds inline budget")
            self.assertEqual(desc["reader_receipt"],"NOT_CONFIRMED")
            self.assertLess(len(small.stdout.encode()),exact_size)

    def test_inline_controls_refuse_invalid_budget_or_no_spool(self):
        with tempfile.TemporaryDirectory(dir=self.root.parent) as area:
            for value,extra in (("-1",True),("1048577",True),("1048576",False)):
                path=Path(area)/"must-not-exist.jsonl"
                args=["read","--work",self.work["id"],"--inline-bytes",value]
                if extra:args+=["--spool",str(path)]
                result=self.run_cli(*args)
                self.assertNotEqual(result.returncode,0);self.assertIn("READING_FRAME",result.stderr)
                self.assertEqual(result.stdout,"");self.assertFalse(path.exists())

    def test_reading_index_authenticates_selected_owner_and_rejects_replaced_spool(self):
        with tempfile.TemporaryDirectory(dir=self.root.parent) as area:
            spool=Path(area)/"reading.jsonl"
            good=self.run_cli("read","--work",self.work["id"],"--spool",str(spool))
            self.assertEqual(good.returncode,0,good.stderr)
            wrong=self.run_cli("reading-index","--work","other-work","--input",str(spool))
            self.assertNotEqual(wrong.returncode,0);self.assertEqual(wrong.stdout,"")
            raw=spool.read_bytes()
            frames=[json.loads(line) for line in raw.splitlines()]
            body=next(r for r in frames if r["type"]=="chunk" and r["payload"]==1)
            body["text"]="x"+body["text"][1:];body["sha256"]=hashlib.sha256(body["text"].encode()).hexdigest()
            canonical=lambda r:json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
            frames[-1]["stream_sha256"]=hashlib.sha256(b"".join(canonical(r)+b"\n" for r in frames[:-1])).hexdigest()
            spool.write_bytes(b"".join(canonical(r)+b"\n" for r in frames))
            bad=self.run_cli("reading-index","--work",self.work["id"],"--input",str(spool))
            self.assertNotEqual(bad.returncode,0);self.assertEqual(bad.stdout,"")
            spool.write_bytes(raw[:-1])
            partial=self.run_cli("reading-index","--work",self.work["id"],"--input",str(spool))
            self.assertNotEqual(partial.returncode,0);self.assertEqual(partial.stdout,"")
            spool.write_bytes(raw)
            wrong_version=self.run_cli("reading-index","--work",self.work["id"],"--version","b"*40,"--input",str(spool))
            self.assertNotEqual(wrong_version.returncode,0);self.assertEqual(wrong_version.stdout,"")

    def test_read_spool_pages_deliver_large_body_without_monolithic_stdout(self):
        data=(b"Complete source body with exact hypotheses and limitations.\n"*24000)
        changed=row(self.rows[0]["path"],data);self.rows[0]=changed
        self.work["sources"][0]=dict(changed,role="primary",version="a"*40)
        self.manifest["occurrences"]=self.rows
        (self.root/"corpus/archives.lock.json").write_text(json.dumps(self.manifest))
        (self.cache/"objects"/changed["sha256"]).write_bytes(data);self.write_work()
        with tempfile.TemporaryDirectory(dir=os.environ.get("ORTHEMOLOGY_TEST_TMPDIR")) as external:
            spool=Path(external)/"reading.jsonl"
            result=self.run_cli("read","--work",self.work["id"],"--spool",str(spool))
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLess(len(result.stdout.encode()),12288)
            descriptor=json.loads(result.stdout)
            self.assertGreater(descriptor["bytes"],780143)
            self.assertGreater(len(descriptor["pages"]),10)
            wire=b""
            for page in descriptor["pages"]:
                received=self.run_cli("reading-page","--input",str(spool),
                    "--offset",str(page["offset"]),"--bytes",str(page["bytes"]),
                    "--sha256",page["sha256"])
                self.assertEqual(received.returncode,0,received.stderr)
                raw=received.stdout.encode()
                self.assertEqual(len(raw),page["bytes"])
                self.assertLessEqual(len(raw),98304)
                self.assertEqual(hashlib.sha256(raw).hexdigest(),page["sha256"])
                wire+=raw
            self.assertEqual(wire,spool.read_bytes())
            self.assertEqual(hashlib.sha256(wire).hexdigest(),descriptor["sha256"])
            records=[json.loads(line) for line in wire.splitlines()]
            self.assertEqual(b"".join(r["text"].encode() for r in records
                if r["type"]=="chunk" and r["payload"]==1),data)
            self.assertEqual(records[-1]["reader_receipt"],"NOT_CONFIRMED")
            checked=self.run_cli("verify-reading","--work",self.work["id"],"--input",str(spool))
            self.assertEqual(checked.returncode,0,checked.stderr)

    def test_read_spool_refuses_overwrite_checkout_and_partial_missing_source(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("ORTHEMOLOGY_TEST_TMPDIR")) as external:
            spool=Path(external)/"reading.jsonl";spool.write_bytes(b"retain exact original")
            result=self.run_cli("read","--work",self.work["id"],"--spool",str(spool))
            self.assertNotEqual(result.returncode,0);self.assertIn("EXISTS",result.stderr)
            self.assertEqual(spool.read_bytes(),b"retain exact original");self.assertEqual(result.stdout,"")
            result=self.run_cli("read","--work",self.work["id"],"--spool",str(self.root/"bad.jsonl"))
            self.assertNotEqual(result.returncode,0);self.assertIn("OUTPUT_BOUNDARY",result.stderr)
            missing=Path(external)/"must-not-exist.jsonl"
            (self.cache/"objects"/self.rows[1]["sha256"]).unlink()
            result=self.run_cli("read","--work",self.work["id"],"--spool",str(missing))
            self.assertNotEqual(result.returncode,0);self.assertEqual(result.stdout,"")
            self.assertFalse(missing.exists())

    def test_reading_page_rejects_corruption_ranges_symlinks_and_fifo(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("ORTHEMOLOGY_TEST_TMPDIR")) as external:
            spool=Path(external)/"reading.jsonl"
            result=self.run_cli("read","--work",self.work["id"],"--spool",str(spool))
            self.assertEqual(result.returncode,0,result.stderr)
            page=json.loads(result.stdout)["pages"][0]
            def receive(path=spool,offset=page["offset"],size=page["bytes"],digest=page["sha256"]):
                return self.run_cli("reading-page","--input",str(path),"--offset",str(offset),
                    "--bytes",str(size),"--sha256",digest)
            for kwargs in ({"offset":-1},{"size":98305},{"size":0},{"digest":"0"*64},
                           {"offset":1},{"size":page["bytes"]+1}):
                with self.subTest(kwargs=kwargs):
                    rejected=receive(**kwargs)
                    self.assertNotEqual(rejected.returncode,0);self.assertEqual(rejected.stdout,"")
            link=Path(external)/"link";link.symlink_to(spool)
            self.assertNotEqual(receive(path=link).returncode,0)
            if hasattr(os,"mkfifo"):
                fifo=Path(external)/"fifo";os.mkfifo(fifo)
                rejected=receive(path=fifo)
                self.assertNotEqual(rejected.returncode,0)
            spool.write_bytes(b"x"+spool.read_bytes()[1:])
            self.assertNotEqual(receive().returncode,0)

    def test_query_metrics_cover_discovery_and_fulltext_without_changing_results(self):
        with tempfile.TemporaryDirectory(dir=self.root.parent) as area:
            for index,args in enumerate((["list"],["search","dimension"],["search","norm","--full-text"])):
                before=self.run_cli(*args)
                metrics=Path(area)/f"query-{index}.json"
                result=self.run_cli(*args,"--metrics",str(metrics))
                self.assertEqual(result.returncode,before.returncode,result.stderr)
                self.assertEqual(result.stdout,before.stdout)
                record=json.loads(metrics.read_text())
                self.assertEqual(record["operation"],args[0])
                self.assertEqual(record["network_received_payload_bytes"],0)
                self.assertIsNone(record["network_wire_bytes"])
                self.assertTrue(set(record["source_routes"].values())<={"verified-object-cache"})
                if "--full-text" in args:
                    self.assertEqual(set(record["source_routes"].values()),{"verified-object-cache"})
                    self.assertTrue(any("papers/geometry.md" in key for key in record["source_routes"]))
                # This baseline catalogue fixture can be listed/searched directly;
                # a zero-source metadata query must not invent a download.
                self.assertEqual(record["reader_receipt"],"NOT_CONFIRMED")
                self.assertGreaterEqual(record["preflight_seconds"],0)
                saved=metrics.read_bytes()
                again=self.run_cli(*args,"--metrics",str(metrics))
                self.assertNotEqual(again.returncode,0);self.assertIn("EXISTS",again.stderr)
                self.assertEqual(again.stdout,"");self.assertEqual(metrics.read_bytes(),saved)

    def test_query_metrics_refuse_checkout_before_source_access(self):
        (self.cache/"objects"/self.rows[1]["sha256"]).unlink()
        result=self.run_cli("search","norm","--full-text","--metrics",str(self.root/"bad-metrics.json"))
        self.assertNotEqual(result.returncode,0)
        self.assertIn("OUTPUT_BOUNDARY",result.stderr)
        self.assertEqual(result.stdout,"")
        self.assertFalse((self.root/"bad-metrics.json").exists())

    def test_read_metrics_measure_provider_payload_without_claiming_reader_receipt(self):
        with tempfile.TemporaryDirectory(dir=self.root.parent) as area:
            metrics=Path(area)/"reading-metrics.json"
            result=self.run_cli("read","--work",self.work["id"],"--metrics",str(metrics))
            self.assertEqual(result.returncode,0,result.stderr)
            record=json.loads(metrics.read_text())
            self.assertEqual(record["network_received_payload_bytes"],0)
            self.assertIsNone(record["network_wire_bytes"])
            self.assertEqual(set(record["source_routes"].values()),{"verified-object-cache"})
            self.assertEqual(record["reader_receipt"],"NOT_CONFIRMED")
            self.assertGreaterEqual(record["preflight_seconds"],0)
            saved=metrics.read_bytes()
            again=self.run_cli("read","--work",self.work["id"],"--metrics",str(metrics))
            self.assertNotEqual(again.returncode,0)
            self.assertIn("EXISTS",again.stderr)
            self.assertEqual(again.stdout,"")
            self.assertEqual(metrics.read_bytes(),saved)

    def test_read_metrics_refuse_checkout_and_symlink_destinations(self):
        inside=self.root/"must-not-create.json"
        result=self.run_cli("read","--work",self.work["id"],"--metrics",str(inside))
        self.assertNotEqual(result.returncode,0)
        self.assertIn("OUTPUT_BOUNDARY",result.stderr)
        self.assertFalse(inside.exists())
        with tempfile.TemporaryDirectory(dir=self.root.parent) as area:
            link=Path(area)/"linked";link.symlink_to(self.root,target_is_directory=True)
            result=self.run_cli("read","--work",self.work["id"],"--metrics",str(link/"must-not-create.json"))
            self.assertNotEqual(result.returncode,0)
            self.assertIn("UNSAFE_PATH",result.stderr)
            self.assertFalse(inside.exists())

    def test_read_wrong_edition_and_review_absence_never_confer_acceptance(self):
        wrong=self.run_cli("read","--work",self.work["id"],"--version","b"*40)
        self.assertNotEqual(wrong.returncode,0)
        self.assertEqual(wrong.stdout,"")
        self.work["sources"][1]["review_kind"]="historical_source_fidelity"
        self.write_work()
        good=self.run_cli("read","--work",self.work["id"])
        self.assertEqual(good.returncode,0,good.stderr)
        records=[json.loads(line) for line in good.stdout.splitlines()]
        context=json.loads("".join(r["text"] for r in records if r["type"]=="chunk" and r["payload"]==0))
        self.assertEqual(context["review_availability"],"NOT_IDENTIFIED")
        self.assertFalse(context["scientific_acceptance_inferred"])
        self.assertNotIn(self.review.decode().strip(),"".join(r.get("text","") for r in records if r.get("payload",0)>0))




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


class PublicOwnerRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from source_provider import SourceProvider
        cls.provider=SourceProvider(ROOT,cache=os.environ.get("ORTHEMOLOGY_TEST_CACHE"),offline=True,git_repo=False)

    def run_cli(self,*args):
        return subprocess.run([sys.executable,"-B",str(CLI),"--root",str(ROOT),
            "--cache",str(self.provider.cache),"--offline","--no-git-source",*args],capture_output=True,text=True)

    def test_named_claim_population_and_content_discovery(self):
        from search import metadata_search, load_claims
        claims=load_claims(self.provider)
        self.assertEqual(len(claims),34)
        for query in ("Abraham","revivification","productive adequacy"):
            found=metadata_search(self.provider,query)
            self.assertTrue(any(r.get("record_type")=="source_owned_claim" for r in found),query)
        listing=self.run_cli("list")
        self.assertEqual(listing.returncode,0,listing.stderr)
        self.assertIn("448 named work editions; 34 source-owned claim readings",listing.stdout)

    def test_retained_state_source_revision_has_exact_named_primary_and_scope(self):
        from search import metadata_search, work_edition
        title="Historical source revision composed with forward continuation"
        for query in ("retained state source revision","retained-state source-revision","retained–state source_revision"):
            found=metadata_search(self.provider,query)
            self.assertTrue(any(r["title"]==title for r in found),query)
        edition=work_edition(self.provider,title)
        self.assertEqual(edition["kind"],"source_reading")
        primary=[s for s in edition["sources"] if s["role"]=="primary"]
        self.assertEqual(len(primary),1)
        self.assertEqual(primary[0]["sha256"],"06053c55e5b4484b605a203cd90315dbe90615753bb25dbd64862b4c4a1849d2")
        result=self.run_cli("show","--work",title,"--role","reading","--include-status")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn(self.provider.read_bytes(primary[0]["path"],primary[0]["version"]).decode().strip(),result.stdout)
        self.assertIn("proposed baseline; owner acceptance pending",result.stdout)
        self.assertIn("No separate review newly established by this track",result.stdout)
        self.assertIn("Controlling scientific review: NOT IDENTIFIED",result.stdout)

    def test_retained_state_route_rejects_changed_status_title_and_source(self):
        import copy
        from search import find_work,verify_work
        work=find_work(self.provider,"Historical source revision composed with forward continuation")
        changed=copy.deepcopy(work);changed["source_owned_status"]["owner_status"]="accepted"
        retitled=copy.deepcopy(work);retitled["title"]="Unrelated primary theorem"
        swapped=copy.deepcopy(work);swapped["sources"][0]["sha256"]="a"*64
        for row in (changed,retitled,swapped):
            with self.assertRaisesRegex(Exception,"AUTHORITY_PROJECTION_DRIFT"):
                verify_work(self.provider,row)

    def test_full_claim_body_and_nested_qualification_are_exact(self):
        from search import work_edition
        handle="essential-whole-existence-independence"
        edition=work_edition(self.provider,handle)
        self.assertEqual(edition["kind"],"claim")
        result=self.run_cli("show","--work",handle,"--role","reading","--include-status")
        self.assertEqual(result.returncode,0,result.stderr)
        nested=[r for r in edition["sources"] if any(p.startswith("/latest_own_activity_qualification/") for p in r["owner_pointers"])]
        self.assertEqual(len(nested),3)
        for source in nested:
            body=self.provider.read_bytes(source["path"],source["version"]).decode("utf-8-sig")
            self.assertIn(body.strip(),result.stdout)
        self.assertIn("Controlling scientific review: NOT IDENTIFIED",result.stdout)

    def test_private_canonical_refuses_body_but_owner_status_is_readable(self):
        handle="pure-perfection-eligibility-and-participant-sensitive-ends"
        denied=self.run_cli("show","--work",handle,"--role","reading")
        self.assertNotEqual(denied.returncode,0)
        self.assertIn("IDENTITY_ONLY",denied.stderr)
        self.assertNotIn("Complete",denied.stdout)
        status=self.run_cli("show","--work",handle,"--role","status")
        self.assertEqual(status.returncode,0,status.stderr)
        self.assertIn("Source-owned claim record",status.stdout)

    def test_church_reading_exposes_source_owned_later_settlement(self):
        from search import load_works
        church=next(w for w in load_works(self.provider) if w["compatibility"]["legacy_key"]=="t20-church-probe")
        result=self.run_cli("show","--work",church["id"],"--include-status")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("independently nonderivable",result.stdout)
        self.assertIn("faithful FullPER validity",result.stdout)
        for source in church["sources"]:
            if source["role"]=="currentness":
                self.assertIn(self.provider.read_bytes(source["path"],source["version"]).decode().strip(),result.stdout)
        self.assertNotIn("## Historical source-fidelity review",result.stdout)

    def test_claim_projection_and_work_review_route_tampering_rejected(self):
        import copy
        from search import load_claims, load_works, verify_work
        claim=copy.deepcopy(load_claims(self.provider)[7])
        claim["sources"]=[s for s in claim["sources"] if not any(p.startswith("/latest_own_activity_qualification/") for p in s["owner_pointers"])]
        with self.assertRaisesRegex(Exception,"AUTHORITY_PROJECTION_DRIFT"):verify_work(self.provider,claim)
        selector=copy.deepcopy(next(w for w in load_works(self.provider) if w["compatibility"]["legacy_key"]=="successor-certified-selector"))
        selector["sources"]=[s for s in selector["sources"] if s.get("review_kind")!="source_owned_scientific"]
        with self.assertRaisesRegex(Exception,"AUTHORITY_PROJECTION_DRIFT"):verify_work(self.provider,selector)

    def test_valid_source_swap_wrong_role_title_and_omitted_review_fail(self):
        import copy
        from search import load_works, verify_work
        works=load_works(self.provider)
        fisher=next(w for w in works if w["compatibility"]["legacy_key"]=="fisher-audit")
        unrelated=next(row for path,row in self.provider.occurrences.items() if path.endswith("README.md") and path not in {s["path"] for s in fisher["sources"]})
        swapped=copy.deepcopy(fisher)
        swapped["sources"][0]={**unrelated,"role":"primary","version":self.provider.baseline["commit"]}
        wrongrole=copy.deepcopy(fisher);wrongrole["sources"][0]["role"]="review"
        wrongtitle=copy.deepcopy(fisher);wrongtitle["title"]="Unsupported substituted title"
        omitted=copy.deepcopy(fisher);omitted["sources"]=[x for x in omitted["sources"] if x["role"]!="review"]
        for variant in (swapped,wrongrole,wrongtitle,omitted):
            with self.subTest(kind=variant["title"],count=len(variant["sources"])):
                with self.assertRaisesRegex(Exception,"AUTHORITY_PROJECTION_DRIFT"):verify_work(self.provider,variant)

    def test_explicit_claim_transfer_review_is_not_reported_unlocated(self):
        from search import work_edition
        edition=work_edition(self.provider,"cumulative-indications-and-knowledge")
        self.assertTrue(any(s["role"]=="review" and s.get("original_sha256","").startswith("775b7fb") for s in edition["sources"]))

    def test_named_fulltext_has_qualification_and_no_historical_report(self):
        from search import fulltext_search
        result=fulltext_search(self.provider,"occasion",work="essential-whole-existence-independence")
        self.assertTrue(result["complete"])
        self.assertTrue(result["matches"])
        self.assertFalse(any("C05-REVIEW" in m["path"] for m in result["matches"]))
        self.assertIn("Not every research work",result["scope"])

if __name__ == "__main__":
    unittest.main()
