#!/usr/bin/env python3
"""Recursive, path-aware mutation testing for the R4 semantic contract (R4 7.5).

The R3 engine applied three TOP-LEVEL operators (drop-required, bad-enum,
extra-field). The read-only audit's finding B7 was that "208 mutants, 0
survivors" therefore said much less than it sounded like: nothing nested,
nothing referential, nothing cardinality-bearing, nothing cross-record was ever
mutated.

This engine walks every positive example part RECURSIVELY, resolving the
effective schema at each node (through $ref, allOf and the applicable if/then
and anyOf/oneOf branches) so that it knows, at every path, which fields are
required, which arrays are sets, and which values are references. It then
applies eighteen operator families. A mutant is KILLED if it is rejected at a
declared layer:

  schema   — the hardened JSON Schema rejects the mutated part; or
  semantic — validate_cross_record_semantics.collect_issues flags the mutated
             bundle (the unmutated bundles are all issue-free, so any issue is
             attributable to the mutation).

Everything is deterministic: mutants are enumerated in sorted path order, never
sampled. There is no randomness and no seed.

A SURVIVOR is a mutant both layers accept. Survivors are failures unless they
are declared, with a reason, in tests/schema-mutations/mutation-spec.json under
"justified_equivalents" — i.e. unless the mutation provably does not change what
the record claims. The report always prints every operator family with its own
counts; "N mutants killed" alone is exactly the kind of summary this engine
exists to replace.
"""
import argparse
import copy
import json
import os
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from validate_cross_record_semantics import collect_issues, aggregate  # noqa: E402

FAMILIES = [
    ("1", "delete-nested-required",
     "delete each required field at EVERY depth, not only the top level"),
    ("2", "empty-required-string",
     "blank each required string ('' is not a declaration)"),
    ("3", "empty-required-array-or-map",
     "empty each required array or map that the contract requires to be nonempty"),
    ("4", "duplicate-unique-member",
     "duplicate a member of an array-as-set, and collide two ids that must differ"),
    ("5", "unknown-reference-id",
     "repoint each resolvable reference (claim, token, evidence, episode) at nothing"),
    ("6", "analysis-version-mismatch",
     "desynchronise an analysis version between records that must share it"),
    ("7", "occurrence-version-mismatch",
     "desynchronise an occurrence version between records that must share it"),
    ("8", "delete-disposition-conditional-field",
     "delete the field a residual's own disposition makes mandatory"),
    ("9", "claim-dependency-cycle",
     "make a claim depend on itself, directly or through another claim"),
    ("10", "remove-required-verdict-status",
     "delete the status of a verdict the required path demands"),
    ("11", "contradict-pathway-summary",
     "state a pathway or reasoning-path summary the statuses do not support"),
    ("12", "na-without-reason",
     "strip the reason from a not-applicable status, anywhere in the record"),
    ("13", "plural-metaorthemma-type",
     "give one token several of_type entries (unimplemented many-to-many MetaInst)"),
    ("14", "empty-metaorthemma-binding",
     "empty the binding map (a token with no material binding)"),
    ("15", "postdate-reliability-declaration",
     "declare a RelSpec at or after the result it is used to assess"),
    ("16", "violate-perturbation-invariant",
     "vary a field the PerturbSpec declares invariant"),
    ("17", "collapse-candidate-set-into-partial-profile",
     "collapse a candidate SET of complete profiles into one partial profile (B1)"),
    ("18", "collapse-claim-path-into-episode-path",
     "overwrite a claim's reasoning adequacy with the episode-level pathway state (B2)"),
]

MUTANT_MARK = "MUTANT-NO-SUCH-ID"


# --------------------------------------------------------------- schema loading
def load_schemas():
    sdir = os.path.join(ROOT, "schemas")
    schemas, resources = {}, []
    for fn in sorted(os.listdir(sdir)):
        if fn.endswith(".schema.json"):
            doc = json.load(open(os.path.join(sdir, fn), encoding="utf-8"))
            schemas[fn] = doc
            resources.append((fn, Resource.from_contents(doc)))
            resources.append((doc.get("$id", fn), Resource.from_contents(doc)))
    return schemas, Registry().with_resources(resources)


class Ctx(object):
    def __init__(self, schemas, registry):
        self.schemas = schemas
        self.registry = registry

    def accepts(self, sname, inst):
        v = Draft202012Validator(self.schemas[sname], registry=self.registry)
        return not list(v.iter_errors(inst))

    def valid_against(self, sub, doc, inst):
        """Is `inst` valid against the subschema `sub` living in document `doc`?"""
        probe = dict(sub)
        probe.setdefault("$schema", "https://json-schema.org/draft/2020-12/schema")
        probe["$id"] = doc.get("$id", "orthemology/anonymous.json")
        try:
            v = Draft202012Validator(probe, registry=self.registry)
            return not list(v.iter_errors(inst))
        except Exception:
            return False

    def deref(self, ref, doc):
        if ref.startswith("#"):
            node = doc
            for part in ref.lstrip("#/").split("/"):
                if part:
                    node = node[part]
            return node, doc
        fn = ref.split("/")[-1]
        target = self.schemas[fn]
        return target, target

    def effective(self, sub, doc, inst, depth=0):
        """Merge $ref / allOf / applicable if-then / matching anyOf-oneOf branch."""
        eff = {"properties": {}, "required": set(), "items": None, "additional": None,
               "uniqueItems": False, "doc": doc}
        if depth > 12 or not isinstance(sub, dict):
            return eff

        def merge(other):
            eff["properties"].update(other["properties"])
            eff["required"] |= other["required"]
            eff["items"] = other["items"] or eff["items"]
            eff["additional"] = other["additional"] if other["additional"] is not None \
                else eff["additional"]
            eff["uniqueItems"] = eff["uniqueItems"] or other["uniqueItems"]
            if other["doc"] is not doc:
                eff["doc"] = other["doc"]

        if "$ref" in sub:
            tgt, tdoc = self.deref(sub["$ref"], doc)
            merge(self.effective(tgt, tdoc, inst, depth + 1))
        for k, v in (sub.get("properties") or {}).items():
            eff["properties"][k] = (v, eff["doc"])
        eff["required"] |= set(sub.get("required") or [])
        if "items" in sub:
            eff["items"] = (sub["items"], doc)
        if isinstance(sub.get("additionalProperties"), dict):
            eff["additional"] = (sub["additionalProperties"], doc)
        if sub.get("uniqueItems"):
            eff["uniqueItems"] = True
        for branch in (sub.get("allOf") or []):
            merge(self.effective(branch, doc, inst, depth + 1))
        if "if" in sub:
            taken = "then" if self.valid_against(sub["if"], doc, inst) else "else"
            if taken in sub:
                merge(self.effective(sub[taken], doc, inst, depth + 1))
        for key in ("anyOf", "oneOf"):
            for branch in (sub.get(key) or []):
                if self.valid_against(branch, doc, inst):
                    merge(self.effective(branch, doc, inst, depth + 1))
                    break
        return eff


def walk(ctx, sub, doc, inst, path=()):
    """Yield (path, value, effective_schema) for every node of `inst`."""
    eff = ctx.effective(sub, doc, inst)
    yield path, inst, eff
    if isinstance(inst, dict):
        for k in sorted(inst):
            child = eff["properties"].get(k) or eff["additional"]
            if child is None:
                continue
            for out in walk(ctx, child[0], child[1], inst[k], path + (k,)):
                yield out
    elif isinstance(inst, list) and eff["items"]:
        for i, v in enumerate(inst):
            for out in walk(ctx, eff["items"][0], eff["items"][1], v, path + (i,)):
                yield out


# ------------------------------------------------------------------ path access
def get(root, path):
    node = root
    for p in path:
        node = node[p]
    return node


def setv(root, path, value):
    get(root, path[:-1])[path[-1]] = value


def delv(root, path):
    parent = get(root, path[:-1])
    if isinstance(parent, list):
        del parent[path[-1]]
    else:
        del parent[path[-1]]


def pstr(path):
    return "/".join(str(p) for p in path) or "<root>"


# ---------------------------------------------------------------- kill checking
class Bundle(object):
    def __init__(self, fn, parts):
        self.fn = fn
        self.parts = parts


class Engine(object):
    def __init__(self, ctx, bundles):
        self.ctx = ctx
        self.bundles = bundles
        self.results = {fid: {"generated": 0, "killed_schema": 0, "killed_semantic": 0,
                              "survivors": []} for fid, _, _ in FAMILIES}

    def emit(self, fam, bundle, idx, path, mutated_part_instance, note=""):
        """Record one mutant: mutate part `idx` of `bundle` and test both layers."""
        r = self.results[fam]
        r["generated"] += 1
        sname = bundle.parts[idx]["schema"]
        sig = "%s#%d %s %s%s" % (bundle.fn, idx, fam, pstr(path), (" " + note) if note else "")
        if not self.ctx.accepts(sname, mutated_part_instance):
            r["killed_schema"] += 1
            return
        parts = [dict(p) for p in bundle.parts]
        parts[idx] = {"schema": sname, "instance": mutated_part_instance}
        if collect_issues(parts):
            r["killed_semantic"] += 1
            return
        r["survivors"].append(sig)


# ------------------------------------------------------------- mutation families
def generate(engine, ctx, bundle):
    parts = bundle.parts
    schemas = ctx.schemas

    # bundle-level referent inventories (a reference can only be broken where it
    # currently resolves; mutating an unresolvable reference proves nothing)
    episode_ids = {p["instance"].get("episode_id") for p in parts
                   if p["schema"] == "orthing-episode.schema.json"}
    token_ids = set()
    for p in parts:
        if p["schema"] == "metaorthemma.schema.json":
            token_ids.add(p["instance"]["token_id"])
        if p["schema"] == "orthing-episode.schema.json":
            token_ids |= {t["token_id"] for t in p["instance"].get("meta_tokens", [])}
    ledger_claims = {}
    for p in parts:
        if p["schema"] == "claim-ledger.schema.json":
            ledger_claims[p["instance"].get("episode_id")] = {
                c["claim_id"] for c in p["instance"].get("claims", [])}
    episode_by_id = {p["instance"].get("episode_id"): p["instance"] for p in parts
                     if p["schema"] == "orthing-episode.schema.json"}

    for idx, part in enumerate(parts):
        sname, inst = part["schema"], part["instance"]
        sdoc = schemas[sname]

        # ---- structural families 1-4 over every node
        for path, value, eff in walk(ctx, sdoc, sdoc, inst):
            if isinstance(value, dict):
                for key in sorted(eff["required"]):
                    if key not in value:
                        continue
                    kpath = path + (key,)
                    m = copy.deepcopy(inst)
                    delv(m, kpath)
                    engine.emit("1", bundle, idx, kpath, m)

                    kv = value[key]
                    if isinstance(kv, str) and kv != "":
                        m = copy.deepcopy(inst)
                        setv(m, kpath, "")
                        engine.emit("2", bundle, idx, kpath, m)
                    if isinstance(kv, list) and kv:
                        m = copy.deepcopy(inst)
                        setv(m, kpath, [])
                        engine.emit("3", bundle, idx, kpath, m, note="[]")
                    if isinstance(kv, dict) and kv:
                        m = copy.deepcopy(inst)
                        setv(m, kpath, {})
                        engine.emit("3", bundle, idx, kpath, m, note="{}")
            if isinstance(value, list) and value and eff["uniqueItems"]:
                m = copy.deepcopy(inst)
                get(m, path).append(copy.deepcopy(value[0]))
                engine.emit("4", bundle, idx, path, m, note="duplicate-member")

        # ---- 4b: collide two ids that must differ (unique by id, not by value)
        for coll, key in (("evidence", "evidence_id"), ("meta_tokens", "token_id")):
            seq = inst.get(coll) if isinstance(inst, dict) else None
            if isinstance(seq, list) and len(seq) >= 2:
                m = copy.deepcopy(inst)
                m[coll][1][key] = m[coll][0][key]
                engine.emit("4", bundle, idx, (coll, 1, key), m, note="id-collision")
        if sname == "claim-ledger.schema.json" and len(inst.get("claims", [])) >= 2:
            m = copy.deepcopy(inst)
            m["claims"][1]["claim_id"] = m["claims"][0]["claim_id"]
            engine.emit("4", bundle, idx, ("claims", 1, "claim_id"), m, note="id-collision")

        # ---- 5: unknown-reference-id (only where the reference resolves today)
        def break_ref(path, guard=True):
            if not guard:
                return
            m = copy.deepcopy(inst)
            setv(m, path, MUTANT_MARK)
            engine.emit("5", bundle, idx, path, m)

        if sname == "verdict-record.schema.json":
            claims_here = ledger_claims.get(inst.get("episode_id"), set())
            for i in range(len(inst.get("per_token_v3c", []))):
                break_ref(("per_token_v3c", i, "token_id"), bool(token_ids))
            for i in range(len(inst.get("claim_verdicts", []))):
                break_ref(("claim_verdicts", i, "claim_id"), bool(claims_here))
            for i in range(len(inst.get("claim_reasoning_paths", []))):
                break_ref(("claim_reasoning_paths", i, "claim_id"), bool(claims_here))
            for mapname in ("rel_spec", "perturb_spec"):
                for k in sorted(inst.get(mapname, {})):
                    if claims_here:
                        m = copy.deepcopy(inst)
                        m[mapname][MUTANT_MARK] = m[mapname].pop(k)
                        engine.emit("5", bundle, idx, (mapname, k), m, note="rekey")
        if sname == "claim-ledger.schema.json":
            ep = episode_by_id.get(inst.get("episode_id"))
            for ci, c in enumerate(inst.get("claims", [])):
                for j in range(len(c.get("evidence_ids", []))):
                    break_ref(("claims", ci, "evidence_ids", j), ep is not None)
                for j in range(len(c.get("depends_on_tokens", []))):
                    break_ref(("claims", ci, "depends_on_tokens", j), bool(token_ids))
                for j in range(len(c.get("depends_on_claims", []))):
                    break_ref(("claims", ci, "depends_on_claims", j))
        if sname == "handoff.schema.json":
            for role in ("sender_episode", "receiver_episode"):
                break_ref((role,), bool(episode_ids))

        # ---- 6: analysis-version-mismatch
        if sname == "orthing-episode.schema.json":
            for ti in range(len(inst.get("meta_tokens", []))):
                m = copy.deepcopy(inst)
                m["meta_tokens"][ti]["analysis"]["version"] = "MUTANT-VERSION"
                engine.emit("6", bundle, idx, ("meta_tokens", ti, "analysis", "version"), m)
        if sname == "claim-ledger.schema.json" and episode_by_id.get(inst.get("episode_id")):
            for ci in range(len(inst.get("claims", []))):
                if "analysis" in inst["claims"][ci]:
                    m = copy.deepcopy(inst)
                    m["claims"][ci]["analysis"]["version"] = "MUTANT-VERSION"
                    engine.emit("6", bundle, idx, ("claims", ci, "analysis", "version"), m)
        if sname == "verdict-record.schema.json" and episode_by_id.get(inst.get("episode_id")):
            m = copy.deepcopy(inst)
            m["index"]["analysis_version"] = "MUTANT-VERSION"
            engine.emit("6", bundle, idx, ("index", "analysis_version"), m)

        # ---- 7: occurrence-version-mismatch. Only generated where a SECOND record
        # in the bundle carries the same occurrence version: with nothing to
        # desynchronise from, the mutation is vacuous rather than undetected.
        if sname == "orthing-episode.schema.json":
            occ_key = (inst.get("occurrence") or {}).get("identity_key")
            has_witness = (
                any(p["schema"] == "orthemma.schema.json"
                    and p["instance"].get("identity_key") == occ_key for p in parts)
                or bool(inst.get("meta_tokens"))
                or any(p["schema"] == "handoff.schema.json"
                       and inst.get("episode_id") in (p["instance"].get("sender_episode"),
                                                      p["instance"].get("receiver_episode"))
                       for p in parts))
            if has_witness:
                m = copy.deepcopy(inst)
                m["occurrence"]["version"] = "MUTANT-VERSION"
                engine.emit("7", bundle, idx, ("occurrence", "version"), m)
            for ti in range(len(inst.get("meta_tokens", []))):
                m = copy.deepcopy(inst)
                m["meta_tokens"][ti]["anchor"]["version"] = "MUTANT-VERSION"
                engine.emit("7", bundle, idx, ("meta_tokens", ti, "anchor", "version"), m)
        if sname == "orthemma.schema.json" and episode_by_id:
            m = copy.deepcopy(inst)
            m["version"] = "MUTANT-VERSION"
            engine.emit("7", bundle, idx, ("version",), m)
        if sname == "handoff.schema.json" and episode_ids:
            for field in ("identity_key", "version"):
                m = copy.deepcopy(inst)
                m["subject"][field] = MUTANT_MARK
                engine.emit("7", bundle, idx, ("subject", field), m)

        # ---- 8: delete-disposition-conditional-field
        if sname == "claim-ledger.schema.json":
            cond = {
                "unresolved": ["responsible_queue", "next_review_condition"],
                "deferred": ["trigger", "review_date"],
                "transferred": ["receiver", "transfer_record"],
                "owner-assigned": ["owner", "acceptance_state"],
                "risk-accepted": ["risk_owner", "rationale", "scope", "review_trigger"],
                "validated-resolved": ["evidence_refs", "verdict_refs"],
            }
            for ri, r in enumerate(inst.get("residuals", [])):
                fields = [f for f in cond.get(r.get("disposition"), []) if r.get(f)]
                for f in fields:
                    m = copy.deepcopy(inst)
                    del m["residuals"][ri][f]
                    engine.emit("8", bundle, idx, ("residuals", ri, f), m)
                if len(fields) > 1:
                    m = copy.deepcopy(inst)
                    for f in fields:
                        del m["residuals"][ri][f]
                    engine.emit("8", bundle, idx, ("residuals", ri, "*"), m, note="all-conditionals")

        # ---- 9: claim-dependency-cycle
        if sname == "claim-ledger.schema.json":
            cl = inst.get("claims", [])
            if cl:
                m = copy.deepcopy(inst)
                m["claims"][0]["depends_on_claims"] = [m["claims"][0]["claim_id"]]
                engine.emit("9", bundle, idx, ("claims", 0, "depends_on_claims"), m, note="self")
            if len(cl) >= 2:
                m = copy.deepcopy(inst)
                m["claims"][0]["depends_on_claims"] = [m["claims"][1]["claim_id"]]
                m["claims"][1]["depends_on_claims"] = [m["claims"][0]["claim_id"]]
                engine.emit("9", bundle, idx, ("claims", "0<->1", "depends_on_claims"), m,
                            note="mutual")

        if sname == "verdict-record.schema.json":
            statuses, req = inst["statuses"], inst["required_path"]
            # ---- 10: remove-required-verdict-status
            for v in req:
                if v in statuses:
                    m = copy.deepcopy(inst)
                    del m["statuses"][v]
                    engine.emit("10", bundle, idx, ("statuses", v), m)
            # ---- 11: contradict-pathway-summary
            for state in ("adequate", "defective", "undetermined"):
                if state != inst["pathway_state"]:
                    m = copy.deepcopy(inst)
                    m["pathway_state"] = state
                    engine.emit("11", bundle, idx, ("pathway_state",), m, note="->" + state)
            for ci, crp in enumerate(inst.get("claim_reasoning_paths", [])):
                for state in ("adequate", "defective", "undetermined"):
                    if state == crp["reasoning_path_adequate"] or state == inst["pathway_state"]:
                        continue  # equal-to-episode-state is family 18's business
                    m = copy.deepcopy(inst)
                    m["claim_reasoning_paths"][ci]["reasoning_path_adequate"] = state
                    engine.emit("11", bundle, idx,
                                ("claim_reasoning_paths", ci, "reasoning_path_adequate"), m,
                                note="->" + state)
            # ---- 12: na-without-reason (anywhere, not just on the required path)
            for v in sorted(inst.get("na_reasons", {})):
                m = copy.deepcopy(inst)
                del m["na_reasons"][v]
                engine.emit("12", bundle, idx, ("na_reasons", v), m)
            # ---- 15: postdate-reliability-declaration
            for k in sorted(inst.get("rel_spec", {})):
                m = copy.deepcopy(inst)
                m["rel_spec"][k]["declared_at"] = "2099-01-01T00:00:00Z"
                engine.emit("15", bundle, idx, ("rel_spec", k, "declared_at"), m)
            # ---- 16: violate-perturbation-invariant
            for k in sorted(inst.get("perturb_spec", {})):
                ps = inst["perturb_spec"][k]
                if ps.get("invariants"):
                    m = copy.deepcopy(inst)
                    m["perturb_spec"][k]["varied_fields"] = \
                        list(m["perturb_spec"][k]["varied_fields"]) + [ps["invariants"][0]]
                    engine.emit("16", bundle, idx, ("perturb_spec", k, "varied_fields"), m)
            # ---- 18: collapse-claim-path-into-episode-path
            for ci, crp in enumerate(inst.get("claim_reasoning_paths", [])):
                if crp["reasoning_path_adequate"] != inst["pathway_state"]:
                    m = copy.deepcopy(inst)
                    m["claim_reasoning_paths"][ci]["reasoning_path_adequate"] = \
                        inst["pathway_state"]
                    engine.emit("18", bundle, idx,
                                ("claim_reasoning_paths", ci, "reasoning_path_adequate"), m,
                                note="->episode " + inst["pathway_state"])

        # ---- 13 / 14: metaorthemma typing and binding
        def token_paths():
            if sname == "metaorthemma.schema.json":
                yield ()
            if sname == "orthing-episode.schema.json":
                for ti in range(len(inst.get("meta_tokens", []))):
                    yield ("meta_tokens", ti)

        for tp in token_paths():
            tok = get(inst, tp) if tp else inst
            m = copy.deepcopy(inst)
            second = copy.deepcopy(tok["of_type"])
            second["mu_id"] = second["mu_id"] + "-second"
            target = get(m, tp) if tp else m
            target["of_type"] = [copy.deepcopy(tok["of_type"]), second]
            engine.emit("13", bundle, idx, tp + ("of_type",), m)

            m = copy.deepcopy(inst)
            target = get(m, tp) if tp else m
            target["binding"] = {}
            engine.emit("14", bundle, idx, tp + ("binding",), m)

        # ---- 17: collapse a candidate SET into one partial profile
        if sname == "orthing-episode.schema.json":
            prof = (inst.get("candidates") or {}).get("profile")
            if isinstance(prof, list) and prof:
                merged = {}
                for member in prof:
                    merged.update(member)
                m = copy.deepcopy(inst)
                m["candidates"]["profile"] = merged
                engine.emit("17", bundle, idx, ("candidates", "profile"), m,
                            note="set->single-partial-profile")
                m = copy.deepcopy(inst)
                m["candidates"]["profile"] = ["partial: %s" % sorted(merged)]
                engine.emit("17", bundle, idx, ("candidates", "profile"), m,
                            note="members->prose")


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true",
                    help="list every survivor signature")
    args = ap.parse_args()

    schemas, registry = load_schemas()
    ctx = Ctx(schemas, registry)

    spec_path = os.path.join(ROOT, "tests", "schema-mutations", "mutation-spec.json")
    spec = json.load(open(spec_path, encoding="utf-8"))
    equivalents = {e["signature"]: e["reason"] for e in spec.get("justified_equivalents", [])}

    edir = os.path.join(ROOT, "examples")
    bundles = []
    for fn in sorted(os.listdir(edir)):
        if fn.endswith(".json"):
            ex = json.load(open(os.path.join(edir, fn), encoding="utf-8"))
            if ex.get("parts"):
                bundles.append(Bundle(fn, ex["parts"]))

    # the engine's premise: every unmutated bundle is issue-free, so any issue a
    # mutant raises is attributable to the mutation and to nothing else
    baseline_bad = [b.fn for b in bundles if collect_issues(b.parts)]
    if baseline_bad:
        print("FATAL: baseline bundles already carry semantic issues: %s" % baseline_bad)
        sys.exit(2)

    engine = Engine(ctx, bundles)
    for b in bundles:
        generate(engine, ctx, b)

    declared_ops = {o["id"] for o in spec.get("operators", [])}
    print("Recursive mutation report — %d example bundles, %d operator families"
          % (len(bundles), len(FAMILIES)))
    print("Kill criterion: rejected by the hardened JSON Schema, or flagged by "
          "validate_cross_record_semantics.")
    print("")
    print("%-4s %-46s %9s %8s %9s %10s" %
          ("fam", "operator family", "generated", "schema", "semantic", "survivors"))
    print("-" * 92)

    tot = {"generated": 0, "killed_schema": 0, "killed_semantic": 0, "survivors": 0}
    unjustified, justified, empty_families, undeclared = [], [], [], []
    for fid, name, desc in FAMILIES:
        r = engine.results[fid]
        surv = r["survivors"]
        just = [s for s in surv if s in equivalents]
        unj = [s for s in surv if s not in equivalents]
        justified += [(s, equivalents[s]) for s in just]
        unjustified += unj
        if r["generated"] == 0:
            empty_families.append("%s %s" % (fid, name))
        if name not in declared_ops:
            undeclared.append(name)
        print("%-4s %-46s %9d %8d %9d %10s" %
              (fid, name, r["generated"], r["killed_schema"], r["killed_semantic"],
               ("%d (%d justified)" % (len(surv), len(just))) if surv else "0"))
        tot["generated"] += r["generated"]
        tot["killed_schema"] += r["killed_schema"]
        tot["killed_semantic"] += r["killed_semantic"]
        tot["survivors"] += len(surv)
        if args.verbose and surv:
            for s in surv:
                print("        survivor: %s%s" % (s, "  [justified]" if s in equivalents else ""))
    print("-" * 92)
    print("%-4s %-46s %9d %8d %9d %10d" %
          ("", "TOTAL", tot["generated"], tot["killed_schema"], tot["killed_semantic"],
           tot["survivors"]))
    print("")
    print("Descriptions:")
    for fid, name, desc in FAMILIES:
        print("  %-3s %-46s %s" % (fid, name, desc))
    print("")

    if justified:
        print("Justified equivalent mutants (declared in mutation-spec.json, each with a reason "
              "why the mutation does not change what the record claims):")
        for sig, reason in justified:
            print("  - %s\n      %s" % (sig, reason))
        print("")

    fails = 0
    if empty_families:
        print("FAIL: operator families that generated no mutant at all (a family with nothing to "
              "bite is not evidence): %s" % empty_families)
        fails += 1
    if undeclared:
        print("FAIL: operator families missing from tests/schema-mutations/mutation-spec.json: %s"
              % sorted(set(undeclared)))
        fails += 1
    if unjustified:
        print("FAIL: %d UNJUSTIFIED surviving mutant(s) — accepted by both layers and not declared "
              "equivalent:" % len(unjustified))
        for s in unjustified:
            print("  - %s" % s)
        fails += 1

    if not fails:
        print("PASS: every generated mutant is killed at a declared layer, or is declared "
              "equivalent with a stated reason.")
    print("TOTAL: %d failures" % fails)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
