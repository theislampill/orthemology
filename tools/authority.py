"""Source-owned scientific projection and deterministic reader views.

This module derives navigation from exact public owners. It is not a scientific
adoption registry. Legacy identifiers live in compatibility/source fields.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from source_provider import SourceProvider, SourceError, load_json, atomic_bytes

BASELINE = "a7ff0e33d1a299db640041c46b1af81ca70851f6"
CWPATH = "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json"
CLPATH = "research/t20-v6-20261012/research-v6/foundations/CURRENT_FOUNDATIONAL_CLAIMS.json"
C05 = "docs/project-closure/reader-refactor-issue-35/C05-REVIEW.json"
PUBLIC_MAP = "research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json"
AVPATH = "docs/provenance/v5-successors/TWELVE_AVENUES.json"
GRAPH = "research/t20-v6-20261012/CURRENT_SOURCE_GRAPH.json"
VERSION = "source-owned-projection-v1"

class AuthorityError(SourceError):
    pass

def canonical_bytes(value):
    return (json.dumps(value,ensure_ascii=False,separators=(",",":"))+"\n").encode("utf-8")

def pointer(document, path):
    if path == "":
        return document
    if not isinstance(path,str) or not path.startswith("/"):
        raise AuthorityError("AUTHORITY_POINTER",repr(path))
    value=document
    try:
        for token in path[1:].split("/"):
            token=token.replace("~1","/").replace("~0","~")
            value=value[int(token)] if isinstance(value,list) else value[token]
    except (KeyError,IndexError,ValueError,TypeError) as exc:
        raise AuthorityError("AUTHORITY_POINTER",path) from exc
    return value

def pointer_key(key):
    return key.replace("~","~0").replace("/","~1")

titles={
27:"Finite horizons, infinite paths, and effective continuation: research synthesis",
167:"Identity, computability, collective evidence, and productive sources: research synthesis",
247:"Criterion installation, charged repair, and foundational warrant: research synthesis",
248:"Finite-history runtime, custody, cancellation, and repair: research synthesis",
249:"Foundational warrant, recipient action, and future handoff: research synthesis",
250:"Existential availability, organized care, and protective cooperation: research synthesis",
251:"Composition, originality, and typed substitution: research synthesis",
252:"Bounded capture, finite information, and total reporting: research synthesis",
253:"Task-relative continuation and certificate-sensitive representation: research synthesis",
254:"Epistemic starting points, bearer, and productive-source inferences",
255:"Identity obstruction and typed extensional repair: completion supplement",
107:"Semantic assurance continuation: ordinary proofs and their exact scope",
111:"Repository-native replay and reference package",
198:"Continuation source, result, and execution directory",
218:"Six supplied source inputs and their inherited reading",
221:"Mathematical companion to the original-source assessment",
222:"Original-source assessment: original and expanded reading editions",
223:"Original-source studies: original and expanded reading guides",
263:"Eight source-study appraisals",
266:"Historical theorem corpus and family index",
273:"Matched-intervention and lower-order alignment: historical synthetic pilot",
278:"Source, language, identity, and disclosure results",
281:"Three-track architecture and source-ascent programme",
286:"Specification defects and a scoped matched-intervention formalisation",
333:"Strengthened neutral common model with declared primitive extensions",
364:"Source roles, architecture burdens, and realization: retained semantic research summary",
365:"Common-intervention identifiability",
414:"Corpus synthesis of formal results, source authority, and open identification",
423:"Recovered transfer, information, authority, and restoration notes",
424:"Common-model minimal nonintegration: role-preserving replacement",
425:"Declared-profile exact certification: semantic reconstruction",
447:"Cumulative scientific synthesis",
}

titles.update({
149:"Sound descent: metaphor, route ranking, and differentiable flow",
160:"Typed extensional repair in a separately named judgement",
201:"Extensional transport and inhabited-endpoint countercontrols",
282:"The minimal nonintegration control",
287:"Profile certification and provenance-calculus candidates",
288:"Separation index and three interpretation maps",
289:"Countermodels, failed candidates, and corrected attributions",
290:"Spatial-memory typed extraction and quarantined source readings",
297:"Role-section descent, common-bearer semantics, and plural realization",
318:"Common-model integration control",
338:"Predictive surplus and representation-relative simplicity",
357:"Integrated one-bearer impersonal common model",
418:"False-closure and selective-prediction benchmark",
419:"Episode-reification incremental-value test",
444:"Literal extensional independence and limits of completion",
})

ordinals="Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth"
def named(i,w):
    t=titles.get(i,w["title"])
    t=re.sub(r"^(?:Deep [A-Z]+ V\d+|SPA-R\d+|Specialist B round \d+)\s*[—:–-]\s*","",t)
    t=re.sub(r"\b(?:"+ordinals+r")\s+","",t,flags=re.I)
    t=re.sub(r"\bAR8R\s+","",t)
    t=re.sub(r"\b[TVD]\d+(?:/\w+)?\b","",t)
    t=re.sub(r"\bv\d+\b","",t,flags=re.I)
    t=re.sub(r"\s+"," ",t).strip(" —:-")
    return t[0].upper()+t[1:]
def slug(t):
    t=unicodedata.normalize("NFKD",t).encode("ascii","ignore").decode().lower()
    return re.sub("[^a-z0-9]+","-",t).strip("-")

claimnames=[
"Orthability, actual evaluation, and representation",
"Actual correction and original-ground entry",
"Material generation and the received productive field",
"Global productive adequacy",
"Same-bearer completion witness",
"Intrinsic existential adequacy and necessary being",
"Common original source of a connected created field",
"Essential whole-existence independence",
"Coactive models and entire productive adequacy",
"Noncoincidence of original productive contributions",
"Pure-perfection eligibility and participant-sensitive ends",
"Connected singleton adequacy gluing",
"Particular and comprehensive knowledge",
"Productive cognition and practical self-determination",
"Particular willing and executive intent",
"Wise determination and respect-specific approval",
"Responsive demonstration and further cognitive aims",
"Completed production and beginningless succession",
"Objective normative authority",
"Retained control and specified obligations",
"Permission, undertaking, and surrender of control",
"Assertoric ownership and exceptionless veracity",
"Basic recognition, acquisition, and correction",
"Mediated evidence and particular recognition",
"Prophetic recognition and practical impediments",
"Cumulative indications and knowledge",
"Source-disclosing performance and joint disclosure",
"Responsive attestation and communicative adoption",
"Request provenance and unresolved event transmission",
"Commissioned content and warranted assent",
"Explanatory guidance and continued availability",
"Cumulative source-content appraisal",
"Dependency-sensitive warrant retention",
"Cognitive modes, operative basing, and geometric scope",
]



# Current work bindings are authoring locators, never verdict records.
CURRENT_SCHEMA = "orthemology-work-v1"
DECISION_SCHEMA = "orthemology-scientific-decision-v1"
IDENTITY_FIELDS = ("path","version","sha256","git_blob","bytes","mode")
EVENT_KINDS = {"finding","attribution_correction","supersession","reviewed_manuscript"}

def _current_identity(provider, locator):
    if not isinstance(locator,dict) or not locator.get("path") or not locator.get("version"):
        raise AuthorityError("AUTHORITY_CURRENT_VERSION","an explicit path and version are required")
    row=provider.resolve(locator["path"],context=locator["version"])
    exact={k:(locator["version"] if k=="version" else row[k]) for k in IDENTITY_FIELDS}
    for k in IDENTITY_FIELDS:
        if k in locator and locator[k]!=exact[k]:
            raise AuthorityError("AUTHORITY_CURRENT_IDENTITY",f"{locator['path']}: {k}")
    provider.read_bytes(locator["path"],context=locator["version"])
    return exact

def _source_metadata(provider, locator):
    identity=_current_identity(provider,locator)
    raw=provider.read_bytes(identity["path"],context=identity["version"])
    if identity["path"].endswith(".json"):
        data=load_json(raw)
    else:
        try: text=raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AuthorityError("AUTHORITY_FRONTMATTER","source must be UTF-8") from exc
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            raise AuthorityError("AUTHORITY_FRONTMATTER","expected JSON between initial --- delimiters")
        end=text.index("\n---\n",4)
        data=load_json(text[4:end])
    return pointer(data,locator.get("json_pointer","")),identity

def _exact_ref(provider, ref):
    if not isinstance(ref,dict) or any(k not in ref for k in IDENTITY_FIELDS):
        raise AuthorityError("AUTHORITY_CURRENT_IDENTITY","complete exact source identity required")
    return _current_identity(provider,ref)

def _decision(provider, metadata, target, predecessor):
    ref=metadata.get("decision")
    if not ref:
        raise AuthorityError("AUTHORITY_DECISION_REQUIRED","source status requires a bound review/adoption decision")
    decision,identity=_source_metadata(provider,ref)
    if not isinstance(decision,dict):
        raise AuthorityError("AUTHORITY_DECISION","decision must be an object")
    if decision.get("schema")!=DECISION_SCHEMA or decision.get("work_id")!=metadata["id"]:
        raise AuthorityError("AUTHORITY_DECISION","wrong decision schema or work")
    if decision.get("event_kind")!=metadata["kind"] or decision.get("target")!=target:
        raise AuthorityError("AUTHORITY_DECISION_TARGET","decision must bind this entire exact source edition")
    if decision.get("predecessor")!=predecessor:
        raise AuthorityError("AUTHORITY_PREDECESSOR","decision must preserve the exact predecessor")
    review=decision.get("review",{})
    if (review.get("state")!="complete" or review.get("target")!=target
            or not isinstance(review.get("reviewer"),str) or not review["reviewer"].strip()
            or not isinstance(review.get("report"),str) or not review["report"].strip()
            or review.get("scope")!=metadata["scope"] or not review.get("evidence")):
        raise AuthorityError("AUTHORITY_REVIEW_REQUIRED","complete source-bound review, scope, and evidence required")
    for evidence in review["evidence"]:
        _exact_ref(provider,evidence)
    adoption=decision.get("adoption",{})
    if (adoption.get("decision")!=metadata["status"] or adoption.get("scope")!=metadata["scope"]
            or not adoption.get("actor") or not adoption.get("reason")):
        raise AuthorityError("AUTHORITY_ADOPTION_REQUIRED","actual source-owned decision at exact scope required")
    appointment_ref=adoption.get("authority_source")
    _exact_ref(provider,appointment_ref)
    appointment,_=_source_metadata(provider,appointment_ref)
    if not isinstance(appointment,dict):
        raise AuthorityError("AUTHORITY_OWNER_SCOPE","appointment must be an object")
    if (appointment.get("actor")!=adoption["actor"]
            or metadata.get("responsible_owner")!=adoption["actor"]
            or metadata["id"] not in appointment.get("work_ids",[])
            or metadata["kind"] not in appointment.get("event_kinds",[])
            or appointment.get("role")!="scientific_adoption_owner"
            or appointment.get("scope")!=metadata["scope"]):
        raise AuthorityError("AUTHORITY_OWNER_SCOPE","adoption actor lacks the bound source appointment at this work/event")
    simulation=bool(metadata.get("simulation"))
    if any(bool(obj.get("simulation"))!=simulation for obj in (decision,review,adoption,appointment)):
        raise AuthorityError("AUTHORITY_SIMULATION","simulation and actual records cannot be mixed")
    if metadata["kind"]=="reviewed_manuscript":
        publication=decision.get("publication",{})
        if publication.get("state")!="prepared_not_published" or publication.get("reviewed_source")!=target:
            raise AuthorityError("AUTHORITY_PUBLICATION_SCOPE","reviewed source preparation is not publication")
    return decision,identity

def current_projection(provider, baseline_works):
    """Project explicitly selected source-owned current editions and decisions.

    This checks exact declarations and their accountable owners; it does not
    authenticate people's identities, signatures, or unrecorded human actions.
    """
    bindings=provider.manifest.get("current_works",[])
    if not isinstance(bindings,list):
        raise AuthorityError("AUTHORITY_CURRENT_SCHEMA","current_works must be a locator list")
    records=[];events=[];seen=set();finding_ids=set()
    baseline_ids={w["id"] for w in baseline_works}
    declared_current={(x["path"],x["version"]) for x in provider.manifest.get("current_sources",[])}
    for binding in bindings:
        if not isinstance(binding,dict) or set(binding)-{"path","version","json_pointer"}:
            raise AuthorityError("AUTHORITY_INDEX_STATUS","current_works may contain source locators only")
        if (binding.get("path"),binding.get("version")) not in declared_current:
            raise AuthorityError("AUTHORITY_CURRENT_SOURCE","selected work needs a declared exact current source")
        metadata,identity=_source_metadata(provider,binding)
        if not isinstance(metadata,dict):
            raise AuthorityError("AUTHORITY_CURRENT_SCHEMA","source metadata must be an object")
        if metadata.get("schema")!=CURRENT_SCHEMA:
            raise AuthorityError("AUTHORITY_CURRENT_SCHEMA","unsupported source-owned metadata")
        for key in ("id","title","kind","status","statement","scope","responsible_owner"):
            if not isinstance(metadata.get(key),str) or not metadata[key].strip():
                raise AuthorityError("AUTHORITY_CURRENT_SCHEMA","missing source field "+key)
        if not re.fullmatch("[a-z0-9]+(?:-[a-z0-9]+)*",metadata["id"]) or metadata["kind"] not in EVENT_KINDS:
            raise AuthorityError("AUTHORITY_CURRENT_SCHEMA","invalid named handle or event kind")
        if not isinstance(metadata.get("hypotheses"),list) or not all(isinstance(x,str) for x in metadata["hypotheses"]):
            raise AuthorityError("AUTHORITY_CURRENT_SCHEMA","hypotheses must be explicit")
        key=(metadata["id"],identity["version"])
        if key in seen:
            raise AuthorityError("AUTHORITY_CURRENT_DUPLICATE",str(key))
        seen.add(key)
        kind=metadata["kind"];status=metadata["status"]
        if status not in {"proposed","accepted","reviewed_for_publication"}:
            raise AuthorityError("AUTHORITY_CURRENT_STATUS","no inferred or unsupported status")
        if kind=="finding" and (status!="proposed" or metadata["id"] in baseline_ids or metadata["id"] in finding_ids):
            raise AuthorityError("AUTHORITY_NEW_FINDING","new finding begins proposed with a distinct work handle")
        if kind=="finding":finding_ids.add(metadata["id"])
        if kind=="reviewed_manuscript" and status!="reviewed_for_publication":
            raise AuthorityError("AUTHORITY_PUBLICATION_SCOPE","manuscript event is reviewed preparation only")
        if kind in {"attribution_correction","supersession"} and status!="accepted":
            raise AuthorityError("AUTHORITY_DECISION_REQUIRED","accepted correction/supersession requires source-owned decision")
        predecessor=None
        if kind!="finding":
            predecessor=_exact_ref(provider,metadata.get("predecessor"))
            if predecessor==identity:
                raise AuthorityError("AUTHORITY_PREDECESSOR","an edition cannot replace itself")
            if metadata.get("predecessor_work_id")!=metadata["id"]:
                raise AuthorityError("AUTHORITY_PREDECESSOR","same work continuity must be explicit")
            baseline_match=next((w for w in baseline_works if w["id"]==metadata["id"] and predecessor["version"]==BASELINE and any(s.get("path")==predecessor["path"] and s.get("role")=="primary" for s in w["sources"])),None)
            if baseline_match is None:
                previous_metadata,_=_source_metadata(provider,{**predecessor,"json_pointer":metadata.get("predecessor_json_pointer","")})
                if not isinstance(previous_metadata,dict) or previous_metadata.get("id")!=metadata["id"]:
                    raise AuthorityError("AUTHORITY_PREDECESSOR","predecessor source owner must identify the same work")
            if kind=="attribution_correction":
                correction=metadata.get("correction",{})
                if correction.get("field")!="attribution" or metadata.get("attribution")!=correction.get("after"):
                    raise AuthorityError("AUTHORITY_ATTRIBUTION","correction must specify exact attribution before/after")
                old,_=_source_metadata(provider,{**predecessor,"json_pointer":metadata.get("predecessor_json_pointer","")})
                if old.get("id")!=metadata["id"] or old.get("attribution")!=correction.get("before"):
                    raise AuthorityError("AUTHORITY_ATTRIBUTION","prior attribution must match preserved source owner")
                if any(old.get(field)!=metadata.get(field) for field in ("statement","hypotheses","scope")):
                    raise AuthorityError("AUTHORITY_ATTRIBUTION_SCOPE","attribution-only correction cannot silently change scientific statement, hypotheses, or scope")
        decision=None;decision_identity=None
        if status!="proposed":
            decision,decision_identity=_decision(provider,metadata,identity,predecessor)
        elif metadata.get("decision"):
            raise AuthorityError("AUTHORITY_PROPOSED_DECISION","proposal cannot carry an implicit adoption decision")
        sources=[{**identity,"role":"primary"}]
        if predecessor:sources.append({**predecessor,"role":"predecessor"})
        if decision_identity:sources.append({**decision_identity,"role":"review"})
        owner={**identity,"json_pointer":binding.get("json_pointer",""),"format":"json" if identity["path"].endswith(".json") else "markdown_json_frontmatter"}
        row={
            "id":metadata["id"],"version":identity["version"],"title":metadata["title"],"aliases":[],
            "role":"current_source_work","subjects":metadata.get("subjects",[]),"sources":sources,
            "owner":owner,"original_record":metadata,
            "source_owned_status":{"status":status,"kind":kind,"scope":metadata["scope"],"simulation":bool(metadata.get("simulation")),"external_actor_authentication":"not performed by projection"},
            "review_discovery":{"complete_controlling_review_population_proven":bool(decision),"bound_whole_source_review":bool(decision)},
            "compatibility":{"legacy_key":None,"legacy_title":None,"existing_result_ids":[],"result_id_field_present":False}
        }
        records.append(row)
        events.append({"record_type":"current_source_event","id":metadata["id"],"version":identity["version"],"title":metadata["title"],"owner":owner,"original_record":metadata,"decision":decision,"decision_owner":decision_identity,"predecessor":predecessor,"scientific_status":"source-owned proposal" if status=="proposed" else "hash-bound source-owned decision; no new independent adjudication"})
    return records,events


def generate(provider):
    """Return deterministic (448 work rows, source-owned authority rows)."""
    if provider.manifest.get("baseline",{}).get("commit") != BASELINE:
        raise AuthorityError("AUTHORITY_VERSION","this source map requires the bound public baseline")
    owners={}
    def read(p):
        if p not in owners:
            owners[p]=load_json(provider.read_bytes(p,context=BASELINE))
        return owners[p]
    moves=provider.manifest.get("profiles",{}).get("ordinary",{}).get("existing_paths")
    if not isinstance(moves,dict) or not moves:
        raise AuthorityError("AUTHORITY_PROFILE","ordinary existing-path map is required")
    def record(p):
        try: row=provider.occurrences[p]
        except KeyError as exc:
            raise AuthorityError("AUTHORITY_SOURCE",p) from exc
        return {k:row[k] for k in ("path","sha256","git_blob","bytes","mode")}
    def owner(p,ptr=""):
        return {**record(p),"version":BASELINE,"json_pointer":ptr}
    c=read(CWPATH)
    claims=read(CLPATH)
    pm=read(PUBLIC_MAP)
    read(GRAPH)
    avs=read(AVPATH)["avenues"]
    if len(c.get("works",[]))!=448 or len(c.get("sources",{}))!=1620 or len(claims.get("claims",[]))!=34 or len(avs)!=12:
        raise AuthorityError("AUTHORITY_POPULATION","expected 448 works, 1620 bindings, 34 claims, 12 avenues")
    names=[named(i,w) for i,w in enumerate(c["works"])]
    slugs=[slug(t) for t in names]
    coll=Counter(slugs)
    for i,handle in enumerate(slugs):
        if coll[handle]>1: slugs[i]=handle+"-"+c["works"][i]["role"]
    if len(set(slugs))!=448:
        raise AuthorityError("AUTHORITY_NAMES","subject names collide; explicit disambiguation is required")
    handles={w["key"]:slugs[i] for i,w in enumerate(c["works"])}
    additions=defaultdict(set)
    for rel in c["relations"]:
        for i,w in enumerate(c["works"]):
            bound=set(w["source_keys"]+w.get("supporting_source_keys",[]))
            if rel["from"] in bound:
                for k in (rel["to"],rel.get("basis")):
                    if k in c["sources"]: additions[i].add(k)
    used={k for w in c["works"] for k in w["source_keys"]+w.get("supporting_source_keys",[])}
    used.update(k for ks in additions.values() for k in ks)
    unassigned=sorted(set(c["sources"])-used)
    additions[447].update(unassigned)
    emitted=set()
    def source(k,role):
        original=c["sources"][k]
        identity=record(original["path"])
        if identity["sha256"]!=original["sha256"]:
            raise AuthorityError("AUTHORITY_IDENTITY",f"catalogue/lock disagree for {k}")
        result={**identity,"role":role,"source_key":k}
        # Every complete source object appears exactly once; later occurrences
        # reference the same source key. Runtime resolution may fetch its owner.
        if k not in emitted:
            result["original_source"]=original
            emitted.add(k)
        return result
    works=[]
    for i,w in enumerate(c["works"]):
        ss=[]
        for k in dict.fromkeys(w["source_keys"]+w.get("supporting_source_keys",[])+sorted(additions[i])):
            if k in w["source_keys"]: role="primary"
            elif k in unassigned: role="catalogue-context"
            elif "review" in k.lower() or re.search(r"(REVIEW|review|CORRECTION)",c["sources"][k]["path"]): role="review"
            else: role="support"
            ss.append(source(k,role))
        ss.append({**record(C05),"role":"review","review_kind":"historical_source_fidelity"})
        works.append({
            "id":slugs[i],"title":names[i],"aliases":[w["title"],w["key"]],
            "role":w["role"],
            "subjects":[p for p in w["placement"] if not re.search(r"Twentieth|Eighteenth|Successor|AR8R|work family|avenue \d",p)],
            "sources":ss,
            "owner":{"path":CWPATH,"sha256":record(CWPATH)["sha256"],"json_pointer":"/works/"+str(i)},
            "original_record":w,
            "source_owned_status":{"catalogue_review_status":w["review_status"],"adoption":"not inferred from catalogue; consult exact source owners"},
            "review_discovery":{"historical_fidelity_review_separate":True,"complete_controlling_review_population_proven":False},
            "compatibility":{"legacy_key":w["key"],"legacy_title":w["title"],"existing_result_ids":w.get("existing_result_ids",[]),"result_id_field_present":"existing_result_ids" in w}
        })
    if emitted != set(c["sources"]):
        raise AuthorityError("AUTHORITY_BINDINGS","not every original binding survived")
    by_sha={x["source_sha256"]:x for x in pm["objects"]}
    auth=[]
    for i,cl in enumerate(claims["claims"]):
        refs=[]
        for j,item in enumerate([cl["canonical_source"]]+cl.get("supporting_sources",[])):
            digest=item["sha256"]
            mapping=by_sha.get(digest)
            role="primary" if j==0 else "support"
            if mapping and mapping.get("repository_path"):
                rr=record(mapping["repository_path"])
                if rr["sha256"]!=mapping["public_sha256"]:
                    raise AuthorityError("AUTHORITY_IDENTITY","public mapping/lock mismatch")
                refs.append({**rr,"role":role,"original_sha256":digest,"public_mapping":mapping})
            else:
                refs.append({"role":role,"original_sha256":digest,"availability":"identity_only" if mapping else "unresolved_public_binding","public_mapping":mapping,"body_recovered":False})
        auth.append({
            "record_type":"source_owned_claim","id":slug(claimnames[i]),"title":claimnames[i],
            "owner":{"path":CLPATH,"sha256":record(CLPATH)["sha256"],"json_pointer":"/claims/"+str(i)},
            "original_record":cl,"sources":refs,
            "compatibility":{"legacy_claim_id":cl["id"],"legacy_semantic_owner":cl["semantic_owner"]}
        })
    for i,av in enumerate(avs):
        matched=[works[n]["id"] for n,w in enumerate(c["works"]) if set(w.get("existing_result_ids",[]))&set(av["result_ids"])]
        title=av["scope"].split(". ")[0]
        auth.append({"record_type":"subject_route","id":slug(title),"title":title,"description":av["scope"],"owner":owner(AVPATH,"/avenues/"+str(i)),"original_record":av,"work_ids":matched,"membership_basis":"exact source-owned result-ID intersection; not scientific adoption"})
    topics=[
        ("Orthability and metaphysical grounding",list(range(12)),["ground","modal-grounding","t20-v6-cumulative-synthesis"]),
        ("Divine attributes and objective norms",[12,13,14,15,18,19,20,21],["athari","ar8r-specialist-b-r10","ar8r-specialist-b-r8"]),
        ("Proper cognition, fitrah, and warranted recognition",list(range(22,34)),["t20-recognition-basing","ar8r-specialist-b-r4"]),
        ("Information geometry and tensor dynamics",[33],["fisher-audit","tensor-moments","t20-v6-law-geometry"]),
        ("Certified selectors and effective continuation",[],["successor-certified-selector"]),
        ("DAEE epistemics and application boundaries",[],[w["key"] for w in c["works"] if w["role"]=="application-proposal" or any("daee" in p.lower() for p in w["placement"])]),
    ]
    for title,ci,keys in topics:
        auth.append({"record_type":"topic_route","id":slug(title),"title":title,"claim_ids":[slug(claimnames[x]) for x in ci],"work_ids":[handles[k] for k in keys if k in handles],"classification":"derived_navigation_only"})
    for i,rel in enumerate(c["relations"]):
        kind=rel["kind"]
        if kind=="related-source" and rel["basis"]=="lineage": cls="archive-only context"
        elif kind in ("preserved-edition-no-exact-build-claim","readable-transcription-companion-not-revised-work","included-component-not-separate-work"): cls="exact replay/citation only"
        else: cls="scientific meaning"
        auth.append({"record_type":"relationship","id":"catalogue-relationship-"+str(i+1),"owner":owner(CWPATH,"/relations/"+str(i)),"original_record":rel,"classification":cls,"meaning":kind.replace("-"," "),"changes_adoption":False})
    anchors=[
        (CWPATH,"catalogue"),(CLPATH,"foundational claims"),(C05,"historical source-fidelity review"),
        (PUBLIC_MAP,"public-source eligibility"),(GRAPH,"exact formal source graph"),
        ("research/t20-v6-20261012/research-v6/foundations/CLAIM_CORRECTION_CROSSWALK.json","foundational correction crosswalk"),
        ("research/t20-v6-20261012/research-v6/synthesis/CORRECTION_SUPERSESSION_INDEX.json","correction and supersession owners"),
        ("research/t20-v6-20261012/research-v6/synthesis/CROSS_CONTRIBUTIONS.json","scientific connections"),
        ("docs/project-closure/ar8r-v11/programs/track-t-authority-and-bridge-status.md","formal and philosophical scope"),
        ("applications/daee-epistemics/SOURCE-BOUNDARY.md","application source boundary"),
        ("applications/daee-epistemics/CURRENT-RUNTIME-BOUNDARY.md","application runtime boundary"),
    ]
    for p,label in anchors:
        auth.append({"record_type":"source_owner","id":slug(label),"title":label,"source":record(p),"scope":"Exact original owner controls; projection adds navigation only."})
    auth.append({
        "record_type":"projection_boundary","id":"public-programme-boundaries","schema":VERSION,"baseline":BASELINE,
        "all_catalogue_bindings":1620,"catalogue_context_source_keys":unassigned,
        "catalogue_context_work":works[447]["id"],
        "catalogue_context_semantics":"Global catalogue/relation/render/collection access; not new primary ownership of this synthesis.",
        "status_axes":["custody","reading","formal_entailment","philosophical_warrant","empirical_evidence","independent_review","adoption","currentness"],
        "named_papers_1_to_11":{"status":"unresolved_exact_public_identity","next_owner":"scientific owner supplies permitted title/version/hash/status map","public_baseline_does_not_resolve_private_programme":True},
        "private_canonical_claim":{"claim_id":slug(claimnames[10]),"availability":"identity_only","public_summary_is_not_canonical_body":True},
        "forbidden_inferences":["public inclusion implies adoption","nonacceptance flag rejects all source-owned arguments","newest filename implies currentness","hash match implies semantic reading","finite control implies general theorem","formal entailment establishes actual-world premises","copies create independent testimony","summary recovers private canonical body"]
    })
    # Root fields retain original schema/currentness/probes/collection metadata.
    # Works, sources and relations are losslessly represented elsewhere.
    auth.append({"record_type":"owner_root_metadata","id":"catalogue-root-metadata","owner":owner(CWPATH),"original_metadata":{k:v for k,v in c.items() if k not in ("works","sources","relations")}})
    auth.append({"record_type":"owner_root_metadata","id":"foundational-root-metadata","owner":owner(CLPATH),"original_metadata":{k:v for k,v in claims.items() if k!="claims"}})
    current_works,current_events=current_projection(provider,works)
    return works+current_works,auth+current_events



def verify_current_work(provider, work):
    """Verify an exact selected current row and return its accountable owners."""
    if not work.get("version"):
        raise AuthorityError("AUTHORITY_CURRENT_VERSION","current work requires its exact edition")
    works,events=generate(provider)
    selected=[row for row in works if row.get("version")==work["version"] and row["id"]==work["id"]]
    if len(selected)!=1 or selected[0]!=work:
        raise AuthorityError("AUTHORITY_PROJECTION_DRIFT","current work differs from its exact source-owned projection")
    event=next(row for row in events if row.get("record_type")=="current_source_event" and row["id"]==work["id"] and row["version"]==work["version"])
    return {
        "owner":event["owner"],"source_owned_status":work["source_owned_status"],
        "review_and_adoption_owner":event["decision_owner"],"decision":event["decision"],
        "predecessor":event["predecessor"],"scope":"exact source declarations; no external actor authentication"
    }

def predecessor_sources(provider, work, version):
    """Read only a verified same-work predecessor and its own review, if bound.

    A current edition's review is never reused as review of its predecessor.
    The caller can use baseline_work when available for the baseline owner path.
    Otherwise source_metadata is the exact prior source's metadata, separately
    from any prior verified review/adoption decision.
    """
    current=verify_current_work(provider,work)
    prior=current["predecessor"]
    if not prior or prior["version"]!=version:
        raise AuthorityError("AUTHORITY_PREDECESSOR","requested edition is not this work's bound predecessor")
    _exact_ref(provider,prior)
    all_works,_=generate(provider)
    baseline=next((row for row in all_works if row["id"]==work["id"] and not row.get("version") and version==BASELINE),None)
    if baseline and any(row.get("path")==prior["path"] and row.get("role")=="primary" for row in baseline["sources"]):
        return {"version":version,"sources":[{**row,"version":BASELINE} for row in baseline["sources"]],"baseline_work":baseline,
                "scope":"original baseline primary/support/review bindings; current review not reused"}
    metadata,_=_source_metadata(provider,{**prior,"json_pointer":work["original_record"].get("predecessor_json_pointer","")})
    if metadata.get("id")!=work["id"]:
        raise AuthorityError("AUTHORITY_PREDECESSOR","different work owner")
    sources=[{**prior,"role":"primary"}]
    prior_decision=None
    if metadata.get("decision"):
        earlier=metadata.get("predecessor")
        if earlier:_exact_ref(provider,earlier)
        prior_decision,review_owner=_decision(provider,metadata,prior,earlier)
        sources.append({**review_owner,"role":"review"})
    return {"version":version,"sources":sources,"source_metadata":metadata,"prior_review_and_adoption":prior_decision,
            "review_availability":"exact prior decision" if prior_decision else "no prior review bound here; do not substitute the current review",
            "scope":"verified same-work original edition; no automatic transfer of current review"}


def source_binding_index(works):
    """Lossless original catalogue bindings, independent of work occurrence."""
    bindings={}
    for work in works:
        for source in work["sources"]:
            if "original_source" in source:
                key=source["source_key"]
                if key in bindings and bindings[key]!=source["original_source"]:
                    raise AuthorityError("AUTHORITY_DUPLICATE_BINDING",key)
                bindings[key]=source["original_source"]
    return bindings

def status_for_work(work, authority):
    """Return source-owned fields; never manufacture one overall verdict."""
    paths={r["path"] for r in work["sources"] if "path" in r}
    claims=[]
    for row in authority:
        if row.get("record_type")!="source_owned_claim":
            continue
        owners={r["path"] for r in row["sources"] if "path" in r}
        if paths & owners or row["owner"]["path"] in paths:
            claims.append(row)
    return {
        "catalogue_status":work["original_record"].get("review_status"),
        "current_source_status":work.get("source_owned_status") if work.get("version") else None,
        "catalogue_owner":work["owner"],
        "matching_source_owned_claims":claims,
        "scope":"Source matches expose claims for reading; they are not an adoption decision or a proof that this work establishes every matched claim.",
        "historical_source_fidelity_review_separate":True,
        "complete_controlling_review_population_proven":False
    }


def load(root):
    root=Path(root)
    def rows(name):
        path=root/"corpus"/name
        try: data=path.read_bytes()
        except OSError as exc: raise AuthorityError("AUTHORITY_UNAVAILABLE",str(path)) from exc
        return [load_json(line) for line in data.splitlines() if line.strip()]
    return rows("works.jsonl"),rows("authority.jsonl")

def validate(provider, works=None, authority=None, include_views=False):
    """Reject missing rows, altered owners/statuses, and unsupported promotion."""
    if works is None or authority is None: works,authority=load(provider.root)
    expected_works,expected_authority=generate(provider)
    if len(works)!=len(expected_works):
        raise AuthorityError("AUTHORITY_POPULATION","baseline or explicitly admitted current work population changed")
    documents={}
    def get(p):
        if p not in documents: documents[p]=load_json(provider.read_bytes(p,context=BASELINE))
        return documents[p]
    for row in works+authority:
        own=row.get("owner")
        if own and "original_record" in row:
            if own.get("format"):
                original,_=_source_metadata(provider,own)
            else:
                original=pointer(get(own["path"]),own["json_pointer"])
            if original!=row["original_record"]:
                raise AuthorityError("AUTHORITY_SOURCE_MISMATCH",row["id"])
        if own and "original_metadata" in row:
            omitted={"works","sources","relations"} if own["path"]==CWPATH else {"claims"}
            original={k:v for k,v in get(own["path"]).items() if k not in omitted}
            if original!=row["original_metadata"]:
                raise AuthorityError("AUTHORITY_SOURCE_MISMATCH",row["id"])
    source_originals={}
    for row in works:
        for source in row["sources"]:
            if "original_source" in source:
                key=source["source_key"]
                if key in source_originals:
                    raise AuthorityError("AUTHORITY_DUPLICATE_BINDING",key)
                source_originals[key]=source["original_source"]
    if source_originals!=get(CWPATH)["sources"]:
        raise AuthorityError("AUTHORITY_SOURCE_MISMATCH","complete source binding population")
    if works!=expected_works or authority!=expected_authority:
        raise AuthorityError("AUTHORITY_PROJECTION_DRIFT","derived titles, statuses, routes or bindings differ from exact source projection")
    if include_views:
        for name,body in render_views(works,authority).items():
            p=provider.root/"docs"/"reader"/name
            if not p.exists() or p.read_text(encoding="utf-8")!=body:
                raise AuthorityError("AUTHORITY_STALE_VIEW",name)
    return {"result":"PASS","scope":"projection fidelity only; no new scientific acceptance","works":len(works),"baseline_works":448,"current_editions":len(works)-448,"bindings":1620,"claims":34,"avenues":12,"baseline":BASELINE}

def render_views(works,authority):
    """Derived reader prose; every changing claim comes from original owners."""
    B=chr(96)
    bykey={w["compatibility"]["legacy_key"]:w for w in works}
    claims=[r for r in authority if r["record_type"]=="source_owned_claim"]
    routes=[r for r in authority if r["record_type"]=="subject_route"]
    def show(key):
        return "python tools/corpus.py show --work "+B+bykey[key]["title"]+B+" --role all --include-status"
    def command(key):
        return 'python tools/corpus.py show --work "'+bykey[key]["title"]+'" --role all --include-status'
    def code(*lines):
        return B*3+"bash\n"+"\n".join(lines)+"\n"+B*3+"\n"
    def prose(text):
        # Editorial presentation removes only insider owner names. Exact source
        # statements remain unaltered in original_record and full source access.
        text=re.sub(r"\bT17\b","the inherited foundational source",text)
        text=re.sub(r"\b(?:CP16/CP23/T17|CP16|CP23)\b","the identified source",text)
        text=re.sub(r"\bPro [GH]\b","the source-bound",text)
        return text
    intro=(
        "Orthemology studies correctness, intelligibility, adequate reasoning and production, warranted recognition, and source-grounded correction. "
        "Its philosophical, mathematical, formal, and application results retain distinct premises and evidence.\n\n"
        "This is a derived reading guide. Exact original owners retain statements, hypotheses, review, adoption, currentness, corrections, and residuals. "
        "Public inclusion, preservation, or a newer filename does not confer scientific adoption.\n\n")
    start="# Start with a scientific question\n\n"+intro
    start+="Begin with the [main paper](../../papers/correctness-reasoning-and-systems.md), [orthability argument](../../foundations/orthability-and-the-ground-of-intelligibility.md), [current arguments](../../foundations/current-arguments.md), and [dynamic orthing and noetic learning](../../foundations/dynamic-orthing-noetic-learning-and-orthability.md).\n\n"
    start+="## Programme avenues\n\n"
    for r in routes: start+="- **"+r["title"]+"** — "+r["description"].split(". ",1)[-1]+"\n"
    start+="\n## Full primary text, review, and status\n\nStart with a subject or title. Open all roles together; no hash knowledge or proof toolchain is required for reading.\n\n"
    start+=code('python tools/corpus.py search "Fisher"',command("fisher-audit"))
    start+="\nThis route retains the complete classification source, fixed-fibre corollary, and conditional ordinary review. Their scopes differ; the corollary review does not newly prove the norm identity.\n\n"
    start+=code('python tools/corpus.py search "recognition"',command("t20-recognition-basing"))
    start+="\nThe catalogue preserves 448 records and 1,620 exact source bindings, including works without result identifiers. Historical source-fidelity reviews retain their original candidate and reading scope; they do not replace work-specific scientific review. Unavailable primary or controlling review text must remain visibly unavailable.\n\nSee [current science](CURRENT_SCIENCE.md), [frontiers](RESEARCH_FRONTIERS.md), and [reproduction](REPRODUCIBILITY.md).\n"
    science="# Current science and source-owned claims\n\n"+intro
    science+="The current sources affirm productive adequacy, intrinsic necessity, source-relative normative obligations, basic recognition, and cumulative warrant at their defended philosophical scopes. Earlier neutral-deduction ceilings do not erase later affirmative appraisals; those appraisals are not premise-free kernel proofs.\n\n"
    science+="The [current claim owner](../../foundations/current-claims.json) contains the complete original statements and all status fields. The following presentation removes only insider owner labels; it makes no change to scientific scope.\n\n"
    groups=[("Orthability, productive adequacy, and necessary being",0,12),("Divine attributes, objective norms, and source authority",12,22),("Proper cognition, fitrah, recognition, and transmission",22,32),("Warrant retention and mathematical interpretation",32,34)]
    for label,a,b in groups:
        science+="## "+label+"\n\n"
        for r in claims[a:b]:
            o=r["original_record"]
            science+="### "+r["title"]+"\n\n"+prose(o["exact_statement"])+"\n\n"
            science+="**Scope:** "+prose(o["scope"])+"\n\n"
            if o.get("hypotheses"): science+="**Premises:** "+"; ".join(prose(x) for x in o["hypotheses"])+"\n\n"
    science+="## Mathematical sources and applications\n\n"
    science+="The Fisher work separates posterior-answer sufficiency from an optional ambient-gradient-norm contract. On a fixed positive fibre, exact continuous supplement requirements depend on its dimension; finite labels cannot preserve the stronger contract on a positive-dimensional fibre. Read the classification, corollary, and conditional review together.\n\n"+code(command("fisher-audit"))
    science+="\nThe tensor/coercive sources establish full-hierarchy results under explicit regularity, positivity, and geometric assumptions. Finite controls supplement their ordinary proofs; they do not replace all-degree hypotheses or imported representation theorems.\n\n"+code(command("tensor-moments"))
    science+="\nCertified-selector normalization transforms supplied finite certificate data. Classical existence does not create an arbitrary-kernel extractor or evaluate an opaque retained choice.\n\n"+code(command("successor-certified-selector"))
    science+="\nThe pinned [DAEE runtime boundary](../../applications/daee-epistemics/CURRENT-RUNTIME-BOUNDARY.md) distinguishes route ranking, inferred control state, actual correctness, and human restoration. Later geometry needs an explicit application bridge. The retained eight-seed synthetic pilot reports zero causal landings despite task accuracy; its overlap and unpaired design limit the negative result.\n"
    front="# Research frontiers and continuation owners\n\n"+intro
    front+="Read [current source-owned claims](../../foundations/current-claims.json), [corrections](../../foundations/claim-corrections.json), and the [continuation charter](../../research/open-questions.md) before proposing a new result. Source access failures and unrun migration checks are implementation obligations, not automatically open science.\n\n"
    front+="## Source-owned residuals\n\n"
    for r in claims:
        residuals=r["original_record"].get("residuals",[])
        if residuals:
            front+="### "+r["title"]+"\n\n"
            for residual in residuals: front+="- "+prose(residual)+"\n"
            front+="\nContinuation belongs to the exact semantic owner recorded with this claim; a derived page cannot assign a new scientific verdict.\n\n"
    front+="## Candidates and unresolved identities\n\nThe radical-correction and derivational-unification candidates remain deferred for insufficient audit despite exact recovery. Preserve their substantive arguments and perform the missing evaluation. Requested Papers 1–11 need a permitted owner-supplied title/version/hash/status/currentness map. Topic matches do not resolve those identities. The private canonical pure-perfection source remains identity-only; its public summary is not its body.\n\n"
    front+="## Avoid rediscovery\n\n"+code('python tools/corpus.py search "square positivity" --full-text --all-versions',command("t20-v6-cumulative-synthesis"))
    front+="\nCheck the exact statement, hypotheses, evidence, correction, and current scope before calling a result open. A stronger application or certificate can be useful while the existing theorem retains its original credit. New decisions must name a responsible owner, exact predecessor, evidence/review, and actual change; regenerate this view from that owner.\n"
    repro="# Source access, editions, and reproduction\n\n"+intro
    repro+="## Read without replay\n\nReading complete sources does not require Lean, an experiment, or automatic expansion of the historical tree. Exact bindings record logical path, commit, SHA-256, Git blob, byte length, and mode. Moved exact bodies preserve their edition; changed prose or links are declared derivatives.\n\n"
    repro+=code(command("fisher-audit")+' --version '+BASELINE)
    repro+="\nFetch deliberately through an authorized route before offline use:\n\n"+code('python tools/corpus.py --offline --cache /path/to/source-cache search "productive adequacy" --full-text --all-versions')
    repro+="\nMissing or restricted bytes must produce an exact unavailable result; never substitute another edition, a semantic reissue, a summary, or a nearby hash. Historical source reading and present byte verification remain distinct.\n\n## Compare and maintain\n\n"
    repro+=code("python tools/corpus.py compare --work WORK_HANDLE --from OLD_COMMIT --to NEW_COMMIT","python tools/corpus.py resolve --legacy-path ORIGINAL_PATH --context "+BASELINE)
    repro+="\nUse actual indexed editions. Preserve the predecessor and change the responsible scientific owner before regenerating derived views. Attribution correction should not rewrite frozen copies. A new status must identify actor, exact claim/edition, evidence, review, and scope. Legacy paths support citation recovery; ordinary discovery uses subject names.\n\n## Replay and publication\n\nA fresh proof or experiment binds exact helpers, source closure, toolchain, packages, command, permitted axioms, complete output, and observed result. Exporting declarations, restoring files, or checking finite examples does not earn full execution. Conditional formal entailment does not establish actual-world premises; finite controls do not validate human restoration. Timeout and missing dependencies are inconclusive or blocked.\n\nA publication must bind reviewed source editions, deterministic builds, and rendered mathematics. Keep the old publication/source package. A compact tree is not the original publication identity, and a local build is not hosted publication. This scientific projection makes no claim of fresh kernel, empirical, or PDF-build acceptance.\n"
    current=[r for r in authority if r.get("record_type")=="current_source_event"]
    if current:
        science+="\n## Explicitly selected current source editions\n\n"
        front+="\n## Current source maintenance\n\n"
        for event in current:
            meta=event["original_record"]
            label="SIMULATION — " if meta.get("simulation") else ""
            science+="### "+label+meta["title"]+"\n\n"+meta["statement"]+"\n\n"
            science+="**Source-owned status:** "+meta["status"]+". **Scope:** "+meta["scope"]+". **Exact edition:** "+event["version"]+".\n\n"
            science+="**Premises:** "+"; ".join(meta["hypotheses"])+"\n\n"
            if event["decision"]:
                science+="The complete source edition is bound by a review and adoption-owner decision. Projection checks source declarations, not external actor authentication.\n\n"
            if event["predecessor"]:
                science+="The exact predecessor remains available by its explicit edition; no newest-file inference is used.\n\n"
            front+="- "+label+meta["title"]+" — "+meta["status"]+"; continuation owner: "+meta["responsible_owner"]+".\n"
        repro+="\n## Current source-owned editions\n\nNew findings begin proposed. Accepted attribution changes, supersessions, and reviewed manuscript preparations require a complete hash-bound source decision with review evidence and an appointed adoption owner at that work/scope. The authoring lock contains only source locators and byte identities. Preserve predecessor bytes before changing an edition. Publication preparation grants no external publication.\n"
    return {"START_HERE.md":start,"CURRENT_SCIENCE.md":science,"RESEARCH_FRONTIERS.md":front,"REPRODUCIBILITY.md":repro}

def write(root, provider=None, output_root=None):
    provider=provider or SourceProvider(root)
    dest=Path(output_root or root)
    works,authority=generate(provider)
    for name,rows in (("works.jsonl",works),("authority.jsonl",authority)):
        atomic_bytes(dest/"corpus"/name,b"".join(canonical_bytes(row) for row in rows))
    for name,body in render_views(works,authority).items():
        atomic_bytes(dest/"docs"/"reader"/name,body.encode("utf-8"))
    return {"works":len(works),"authority_records":len(authority),"output_root":str(dest)}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("generate","validate"))
    parser.add_argument("--root",default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output-root")
    parser.add_argument("--cache")
    parser.add_argument("--offline",action="store_true")
    args=parser.parse_args(argv)
    provider=SourceProvider(args.root,cache=args.cache,offline=args.offline)
    try:
        if args.action=="generate": result=write(args.root,provider,args.output_root)
        else: result=validate(provider,include_views=True)
        print(json.dumps(result,ensure_ascii=False,sort_keys=True))
        return 0
    except (SourceError,OSError,ValueError,KeyError) as exc:
        print(json.dumps({"result":"FAIL","error":str(exc)},ensure_ascii=False))
        return 1

if __name__=="__main__":
    raise SystemExit(main())
