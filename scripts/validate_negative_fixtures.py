#!/usr/bin/env python3
"""Negative + mutation testing for the hardened schema layer (R3 §7.3).

Part 1 — negative fixtures (tests/schema-negative/NEGATIVE-FIXTURES.json):
each malformed record must be rejected at its declared layer:
  expect_layer=schema   -> the JSON Schema itself must reject it;
  expect_layer=semantic -> it must be schema-valid (by design) AND flagged by
                           validate_cross_record_semantics.collect_issues.

Part 2 — R4 invalid-fixture corpus (tests/invalid/*.json): one file per
malformed class from the R4 read-only baseline audit's probe, plus the classes
the probe did not reach. Same two-layer contract as Part 1; each file carries
its own {id, why, expect_layer, schema, instance}.

Part 3 — mutation tests (tests/schema-mutations/mutation-spec.json): for every
positive example part, enumerate deterministic mutants (drop each required
top-level field; corrupt each top-level enum; add an undeclared field) and
require the schema to reject every one. Surviving mutants are failures. These
are the three v1 TOP-LEVEL operators only; the eighteen recursive, path-aware
families live in scripts/validate_recursive_mutations.py.
"""
import copy
import json
import os
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from validate_cross_record_semantics import collect_issues  # noqa: E402

FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


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


def schema_accepts(schemas, registry, sname, inst):
    v = Draft202012Validator(schemas[sname], registry=registry)
    return not list(v.iter_errors(inst))


def main():
    schemas, registry = load_schemas()

    # Part 1: negative fixtures
    neg = json.load(open(os.path.join(ROOT, "tests", "schema-negative",
                                      "NEGATIVE-FIXTURES.json"), encoding="utf-8"))
    n_schema = n_semantic = 0
    for f in neg["fixtures"]:
        accepted = schema_accepts(schemas, registry, f["schema"], f["instance"])
        if f["expect_layer"] == "schema":
            n_schema += 1
            check("negative %s rejected by schema" % f["id"], not accepted,
                  "schema ACCEPTED a malformed record")
        else:
            n_semantic += 1
            check("negative %s is schema-valid by design" % f["id"], accepted,
                  "semantic fixture should pass the schema layer")
            issues = collect_issues([{"schema": f["schema"], "instance": f["instance"]}])
            check("negative %s flagged by cross-record semantics" % f["id"], bool(issues))
    check("negative suite covers both layers", n_schema >= 4 and n_semantic >= 3,
          "schema=%d semantic=%d" % (n_schema, n_semantic))

    # Part 2: the R4 invalid-fixture corpus, one file per malformed class.
    # A fixture is either single-record ({schema, instance}) or, for defects
    # that only exist BETWEEN records (inheritance cycles, cross-episode token
    # collisions, scope leakage), a multi-record bundle ({parts: [...]}) — the
    # R4 independent-review extension.
    idir = os.path.join(ROOT, "tests", "invalid")
    i_schema = i_semantic = 0
    for fn in sorted(os.listdir(idir)):
        if not fn.endswith(".json"):
            continue
        f = json.load(open(os.path.join(idir, fn), encoding="utf-8"))
        keys = ("id", "why", "expect_layer") + (("parts",) if "parts" in f
                                                else ("schema", "instance"))
        for key in keys:
            check("invalid fixture %s declares %s" % (fn, key), key in f)
        parts = f["parts"] if "parts" in f else [{"schema": f["schema"],
                                                  "instance": f["instance"]}]
        accepted = all(schema_accepts(schemas, registry, p["schema"], p["instance"])
                       for p in parts)
        if f["expect_layer"] == "schema":
            i_schema += 1
            check("invalid %s rejected by schema" % f["id"], not accepted,
                  "the schema ACCEPTED a malformed record")
        else:
            i_semantic += 1
            check("invalid %s is schema-valid by design" % f["id"], accepted,
                  "a semantic fixture must pass the schema layer, or it proves nothing about "
                  "the semantic layer")
            issues = collect_issues(parts)
            check("invalid %s flagged by cross-record semantics" % f["id"], bool(issues))
    check("invalid corpus covers the audited classes at both layers",
          i_schema >= 15 and i_semantic >= 6,
          "schema=%d semantic=%d" % (i_schema, i_semantic))

    # Part 3: deterministic mutation testing over positive examples
    spec = json.load(open(os.path.join(ROOT, "tests", "schema-mutations",
                                       "mutation-spec.json"), encoding="utf-8"))
    ops = {o["id"] for o in spec["operators"]}
    edir = os.path.join(ROOT, "examples")
    survivors, mutants = [], 0
    for fn in sorted(os.listdir(edir)):
        if not fn.endswith(".json"):
            continue
        ex = json.load(open(os.path.join(edir, fn), encoding="utf-8"))
        for i, part in enumerate(ex.get("parts", [])):
            sname, inst = part["schema"], part["instance"]
            sdoc = schemas[sname]
            if "drop-required" in ops:
                for req in sdoc.get("required", []):
                    if req in inst:
                        m = copy.deepcopy(inst)
                        del m[req]
                        mutants += 1
                        if schema_accepts(schemas, registry, sname, m):
                            survivors.append("%s#%d drop:%s" % (fn, i, req))
            if "bad-enum" in ops:
                for prop, pdoc in sdoc.get("properties", {}).items():
                    if "enum" in pdoc and prop in inst:
                        m = copy.deepcopy(inst)
                        m[prop] = "NOT-A-LEGAL-VALUE"
                        mutants += 1
                        if schema_accepts(schemas, registry, sname, m):
                            survivors.append("%s#%d enum:%s" % (fn, i, prop))
            if "extra-field" in ops:
                m = copy.deepcopy(inst)
                m["__mutant__"] = True
                mutants += 1
                if schema_accepts(schemas, registry, sname, m):
                    survivors.append("%s#%d extra-field" % (fn, i))
    check("mutation testing generated a real corpus (>=100 mutants)", mutants >= 100, str(mutants))
    check("0 surviving mutants (of %d)" % mutants, not survivors, "; ".join(survivors[:6]))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
