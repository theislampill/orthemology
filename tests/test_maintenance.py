"""Disposable scientific maintenance simulations; no real adoption/publication."""
from __future__ import annotations
import copy
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(os.environ.get("ORTHEMOLOGY_TEST_REPO",Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(ROOT/"tools"))
import authority
from source_provider import SourceProvider,SourceError,git_blob

def payload(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()

def markdown(meta,body="Fixture-only manuscript body. No scientific result or actual adoption is asserted.\n"):
    return b"---\n"+payload(meta).rstrip()+b"\n---\n"+body.encode()

def snapshot(root):
    return {str(p.relative_to(root)):{"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
            for p in root.rglob("*") if p.is_file() and "cache" not in p.relative_to(root).parts}

@lru_cache(maxsize=1)
def baseline_inputs():
    # Receive exactly the generator's real public source owners from the
    # explicitly supplied verified cache; no old checkout or Git fallback.
    provider=SourceProvider(ROOT,cache=os.environ.get("ORTHEMOLOGY_TEST_CACHE"),
                            offline=True,git_repo=False)
    authority.generate(provider)
    return tuple((provider.resolve_legacy(path)["sha256"],provider.read_bytes(path))
                 for path in sorted(provider.sources_used))

class Fixture:
    def __init__(self):
        self.temp=tempfile.TemporaryDirectory(prefix="orthemology-maintenance-",dir=os.environ.get("ORTHEMOLOGY_TEST_TMPDIR"))
        self.root=Path(self.temp.name)
        self.cache=self.root/"cache"
        (self.cache/"objects").mkdir(parents=True)
        for digest,data in baseline_inputs():
            (self.cache/"objects"/digest).write_bytes(data)
        self.lock=copy.deepcopy(json.loads((ROOT/"corpus/archives.lock.json").read_text()))
        self.lock["current_sources"]=[]
        self.lock["current_works"]=[]
        self.base_source="research/maintenance-fixture.md"
        self.work_id="maintenance-fixture"
        self.owner_id="SIMULATED_OWNER_NOT_A_REAL_ADOPTION"
        self.review_id="SIMULATED_REVIEWER_NOT_A_REAL_REVIEW"
        self.old_meta={
            "schema":authority.CURRENT_SCHEMA,"id":self.work_id,"title":"Maintained manuscript fixture",
            "kind":"historical_source_owner","status":"accepted","statement":"Fixture historical source-owned assertion.",
            "scope":"Disposable maintenance fixture only","hypotheses":["Simulation; no actual scientific result"],
            "responsible_owner":self.owner_id,"attribution":"Earlier fixture attribution","simulation":True
        }
        self.old_bytes=markdown(self.old_meta)
        self.old=self.register(self.base_source,"fixture-original",self.old_bytes)
        appointment={"appointments":[{
            "actor":self.owner_id,"role":"scientific_adoption_owner",
            "work_ids":[self.work_id],"event_kinds":["attribution_correction","supersession","reviewed_manuscript"],
            "scope":"Disposable maintenance fixture only","simulation":True
        }]}
        row=self.register("research/fixture-owner-appointment.json","fixture-owner",payload(appointment))
        self.appointment={**self.exact(row),"json_pointer":"/appointments/0"}
        self.sync()
        authority.write(self.root,self.provider())

    def close(self): self.temp.cleanup()

    def sync(self):
        p=self.root/"corpus/archives.lock.json";p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(payload(self.lock))

    def exact(self,row):
        return {k:row[k] for k in authority.IDENTITY_FIELDS}

    def register(self,path,version,data):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True)
        # Independently retain predecessor bytes before replacement.
        if p.exists():
            prior=p.read_bytes()
            for old in self.lock["current_sources"]:
                if old["path"]==path and old["sha256"]==hashlib.sha256(prior).hexdigest():
                    dest=self.cache/"objects"/old["sha256"];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(prior)
        p.write_bytes(data)
        row={"path":path,"version":version,"sha256":hashlib.sha256(data).hexdigest(),"git_blob":git_blob(data),"bytes":len(data),"mode":"100644","access":"public"}
        self.lock["current_sources"]=[r for r in self.lock["current_sources"] if (r["path"],r["version"])!=(path,version)]+[row]
        return row

    def provider(self):
        self.sync()
        return SourceProvider(self.root,cache=self.cache,offline=True,git_repo=False)

    def perform(self,kind):
        is_find=kind=="finding"
        path="research/new-finding-fixture.md" if is_find else self.base_source
        version="fixture-"+kind
        meta={
            "schema":authority.CURRENT_SCHEMA,"id":"new-finding-fixture" if is_find else self.work_id,
            "title":"Proposed finding fixture" if is_find else "Maintained manuscript fixture",
            "kind":kind,"status":"proposed" if is_find else "reviewed_for_publication" if kind=="reviewed_manuscript" else "accepted",
            "statement":"A proposed simulation finding." if is_find else "Fixture source-owned maintained statement.",
            "scope":"Disposable maintenance fixture only","hypotheses":["Simulation; no actual scientific result"],
            "responsible_owner":self.owner_id,"attribution":self.old_meta["attribution"],
            "subjects":["maintenance simulation"],"simulation":True
        }
        if not is_find:
            meta["predecessor"]=self.exact(self.old)
            meta["predecessor_work_id"]=self.work_id
            meta["decision"]={"path":"research/fixture-review-decision.json","version":"fixture-decision-"+kind}
        if kind=="attribution_correction":
            meta["statement"]=self.old_meta["statement"]
            meta["attribution"]="Corrected fixture attribution"
            meta["correction"]={"field":"attribution","before":self.old_meta["attribution"],"after":meta["attribution"]}
        if kind=="supersession":
            meta["statement"]="Fixture revised result under the explicitly stated stronger premise."
            meta["hypotheses"].append("Explicit additional fixture premise")
        target=self.register(path,version,markdown(meta))
        self.meta=meta;self.target=target
        self.lock["current_works"]=[{"path":path,"version":version}]
        if not is_find:
            target=self.exact(target)
            self.decision={
                "schema":authority.DECISION_SCHEMA,"work_id":self.work_id,"event_kind":kind,
                "target":target,"predecessor":self.exact(self.old),"simulation":True,
                "review":{"state":"complete","reviewer":self.review_id,"target":target,
                          "scope":meta["scope"],"evidence":[self.exact(self.old)],
                          "report":"SIMULATION: this fixture review covers the entire exact target source and its stated predecessor change; it is not a review of actual research.","simulation":True},
                "adoption":{"actor":self.owner_id,"decision":meta["status"],"scope":meta["scope"],
                            "authority_source":self.appointment,
                            "reason":"SIMULATION: fixture owner accepts only this declared maintenance change.","simulation":True}
            }
            if kind=="reviewed_manuscript":
                self.decision["publication"]={"state":"prepared_not_published","reviewed_source":target}
            self.update_decision()
        self.sync()
        return meta,target

    def update_decision(self):
        d=self.meta["decision"]
        self.register(d["path"],d["version"],payload(self.decision))
        self.sync()

    def update_meta(self):
        self.target=self.register(self.target["path"],self.target["version"],markdown(self.meta))
        self.sync()

class MaintenanceTests(unittest.TestCase):
    reports=[]

    def setUp(self):
        self.fixture=Fixture()

    def tearDown(self):
        self.fixture.close()

    @classmethod
    def tearDownClass(cls):
        destination=os.environ.get("ORTHEMOLOGY_MAINTENANCE_REPORT")
        if destination:
            Path(destination).write_bytes(payload({
                "scope":"Disposable source-owned maintenance simulations; no actual scientific adoption, human authentication, or publication",
                "scenarios":cls.reports
            }))

    def test_four_real_source_workflows_and_two_generation_convergence(self):
        self.fixture.close()
        for kind in ("finding","attribution_correction","supersession","reviewed_manuscript"):
            with self.subTest(kind=kind):
                f=Fixture();self.fixture=f
                before=snapshot(f.root)
                meta,target=f.perform(kind)
                p=f.provider()
                authority.write(f.root,p)
                works,events=authority.load(f.root)
                checked=authority.validate(p,works,events,include_views=True)
                self.assertEqual(checked["baseline_works"],448)
                self.assertEqual(checked["current_editions"],1)
                selected=works[-1]
                self.assertEqual(selected["version"],target["version"])
                self.assertEqual(selected["source_owned_status"]["status"],meta["status"])
                self.assertEqual(p.read_bytes(f.old["path"],context=f.old["version"]),f.old_bytes)
                self.assertTrue(selected["source_owned_status"]["simulation"])
                first=snapshot(f.root)
                authority.write(f.root,p)
                self.assertEqual(first,snapshot(f.root))
                changed=sorted(k for k in set(before)|set(first) if before.get(k)!=first.get(k))
                owner_changes=[k for k in changed if k.startswith("research/")]
                self.assertFalse(any("checkpoint" in k or "source-store" in k for k in changed))
                if kind=="attribution_correction":
                    newbody=(f.root/f.base_source).read_bytes().split(b"\n---\n",1)[1]
                    oldbody=f.old_bytes.split(b"\n---\n",1)[1]
                    self.assertEqual(newbody,oldbody)
                    self.assertEqual(owner_changes,["research/fixture-review-decision.json",f.base_source])
                if kind=="reviewed_manuscript":
                    self.assertEqual(events[-1]["decision"]["publication"]["state"],"prepared_not_published")
                self.reports.append({
                    "scenario":kind,"result":checked,"changed_paths":changed,
                    "changed_files":len(changed),"owner_files":owner_changes,
                    "changed_active_bytes_before":sum(before.get(k,{}).get("bytes",0) for k in changed),
                    "changed_active_bytes_after":sum(first.get(k,{}).get("bytes",0) for k in changed),
                    "preserved_predecessor":f.exact(f.old),"new_source":f.exact(f.target),
                    "review_obligations":"none for proposed finding; complete target review and scoped appointed adoption owner for accepted maintenance",
                    "two_generations":"byte-identical","publication_performed":False,
                    "cached_predecessor_bytes":sum(q.stat().st_size for q in f.cache.rglob("*") if q.is_file()) if f.cache.exists() else 0
                })
                f.close()

    def test_new_finding_cannot_begin_accepted(self):
        f=self.fixture;f.perform("finding");f.meta["status"]="accepted";f.update_meta()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_NEW_FINDING"):
            authority.generate(f.provider())

    def test_index_cannot_assign_acceptance(self):
        f=self.fixture;f.perform("finding");f.lock["current_works"][0]["status"]="accepted"
        with self.assertRaisesRegex(SourceError,"AUTHORITY_INDEX_STATUS"):
            authority.generate(f.provider())

    def test_accepted_correction_requires_complete_review_and_owner(self):
        f=self.fixture;f.perform("attribution_correction")
        f.decision["review"]["state"]="not_run";f.update_decision()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_REVIEW_REQUIRED"):
            authority.generate(f.provider())
        f.decision["review"]["state"]="complete"
        f.decision["adoption"]["actor"]="UNAPPOINTED_FIXTURE_ACTOR";f.update_decision()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_OWNER_SCOPE"):
            authority.generate(f.provider())

    def test_review_cannot_bind_a_different_whole_source(self):
        f=self.fixture;f.perform("supersession")
        f.meta["statement"]="An additional unreviewed change";f.update_meta()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_DECISION_TARGET"):
            authority.generate(f.provider())

    def test_predecessor_cannot_be_lost_or_replaced(self):
        f=self.fixture;f.perform("supersession")
        (f.cache/"objects"/f.old["sha256"]).unlink()
        with self.assertRaisesRegex(SourceError,"CORRUPT|NOT_CACHED"):
            authority.generate(f.provider())

    def test_stale_generated_view_rejected_after_source_change(self):
        f=self.fixture;f.perform("finding");p=f.provider();authority.write(f.root,p)
        view=f.root/"docs/reader/CURRENT_SCIENCE.md";view.write_text(view.read_text()+"\nUnsupported acceptance.\n")
        with self.assertRaisesRegex(SourceError,"AUTHORITY_STALE_VIEW"):
            authority.validate(p,include_views=True)

    def test_newest_declared_file_does_not_change_selected_version(self):
        f=self.fixture;f.perform("finding")
        selected=copy.deepcopy(f.target)
        newer=copy.deepcopy(f.meta);newer["title"]="Unselected newer edition"
        f.register(selected["path"],"unselected-newer",markdown(newer));p=f.provider()
        works,_=authority.generate(p)
        self.assertEqual(works[-1]["title"],"Proposed finding fixture")
        self.assertEqual(works[-1]["version"],selected["version"])
        with self.assertRaisesRegex(SourceError,"UNAVAILABLE"):
            p.read_bytes(selected["path"])

    def test_simulation_cannot_be_mixed_with_actual_decision(self):
        f=self.fixture;f.perform("reviewed_manuscript")
        f.decision["adoption"]["simulation"]=False;f.update_decision()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_SIMULATION"):
            authority.generate(f.provider())

    def test_publication_preparation_is_not_publication(self):
        f=self.fixture;f.perform("reviewed_manuscript")
        f.decision["publication"]["state"]="published";f.update_decision()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_PUBLICATION_SCOPE"):
            authority.generate(f.provider())


    def test_current_cli_helper_and_predecessor_review_separation(self):
        f=self.fixture;f.perform("supersession");p=f.provider()
        works,_=authority.generate(p);current=works[-1]
        checked=authority.verify_current_work(p,current)
        self.assertEqual(checked["source_owned_status"]["status"],"accepted")
        old=authority.predecessor_sources(p,current,f.old["version"])
        self.assertEqual(old["sources"],[{**f.exact(f.old),"role":"primary"}])
        self.assertIsNone(old["prior_review_and_adoption"])
        self.assertNotIn(f.meta["decision"]["path"],[r["path"] for r in old["sources"]])
        tampered=copy.deepcopy(current);tampered["source_owned_status"]["scope"]="Whole programme accepted"
        with self.assertRaisesRegex(SourceError,"AUTHORITY_PROJECTION_DRIFT"):
            authority.verify_current_work(p,tampered)
        with self.assertRaisesRegex(SourceError,"AUTHORITY_PREDECESSOR"):
            authority.predecessor_sources(p,current,"some-other-version")

    def test_wrong_predecessor_work_and_owner_scope_rejected(self):
        f=self.fixture;f.perform("supersession")
        old=copy.deepcopy(f.old_meta);old["id"]="different-work"
        other=f.register("research/different-work.md","other-work-version",markdown(old))
        f.meta["predecessor"]=f.exact(other);f.update_meta()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_PREDECESSOR"):
            authority.generate(f.provider())
        f.meta["predecessor"]=f.exact(f.old);f.update_meta()
        f.decision["target"]=f.exact(f.target);f.decision["review"]["target"]=f.exact(f.target)
        appointment={"appointments":[{"actor":f.owner_id,"role":"scientific_adoption_owner","work_ids":[f.work_id],"event_kinds":["supersession"],"scope":"Different scope","simulation":True}]}
        row=f.register("research/fixture-owner-appointment.json","fixture-owner",payload(appointment))
        f.decision["adoption"]["authority_source"]={**f.exact(row),"json_pointer":"/appointments/0"}
        f.update_decision()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_OWNER_SCOPE"):
            authority.generate(f.provider())



    def test_attribution_only_event_cannot_change_scientific_claim(self):
        f=self.fixture;f.perform("attribution_correction")
        f.meta["statement"]="An unannounced stronger scientific claim";f.update_meta()
        with self.assertRaisesRegex(SourceError,"AUTHORITY_ATTRIBUTION_SCOPE"):
            authority.generate(f.provider())

if __name__=="__main__":
    unittest.main()
