#!/usr/bin/env python3
"""Schema validator: every schemas/*.schema.json compiles; every examples/*.json
part validates against its declared schema; verdict-record semantics are
re-checked against docs/verdict-registry.yaml (registry-driven). Deterministic
consistency tool; no empirical implementation claim."""
import json
import os
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as e:
    print("FATAL: requires pyyaml, jsonschema>=4.18 (pip install pyyaml jsonschema):", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    sdir = os.path.join(ROOT, "schemas")
    schemas = {}
    resources = []
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith(".schema.json"):
            continue
        with open(os.path.join(sdir, fn), encoding="utf-8") as f:
            doc = json.load(f)
        schemas[fn] = doc
        resources.append((fn, Resource.from_contents(doc)))
        resources.append((doc.get("$id", fn), Resource.from_contents(doc)))
    registry = Registry().with_resources(resources)

    check("all 8 expected schemas present",
          {"analysis.schema.json", "orthemma.schema.json", "metaortheme.schema.json",
           "metaorthemma.schema.json", "orthing-episode.schema.json", "verdict-record.schema.json",
           "handoff.schema.json", "claim-ledger.schema.json"} <= set(schemas),
          str(sorted(schemas)))

    for fn, doc in schemas.items():
        try:
            Draft202012Validator.check_schema(doc)
            check("schema compiles: " + fn, True)
        except Exception as e:
            check("schema compiles: " + fn, False, str(e)[:200])

    with open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8") as f:
        reg = yaml.safe_load(f)
    reg_ids = {v["id"] for v in reg["verdicts"]}
    core = set(reg["core_path"])

    # verdict-record enum must equal the registry's ID set
    vr_enum = set(schemas["verdict-record.schema.json"]["$defs"]["verdict_id"]["enum"])
    check("verdict-record enum equals registry semantic IDs", vr_enum == reg_ids,
          "enum-only=%s registry-only=%s" % (sorted(vr_enum - reg_ids), sorted(reg_ids - vr_enum)))

    edir = os.path.join(ROOT, "examples")
    n_parts = 0
    for fn in sorted(os.listdir(edir)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(edir, fn), encoding="utf-8") as f:
            ex = json.load(f)
        for i, part in enumerate(ex.get("parts", [])):
            n_parts += 1
            sname = part["schema"]
            validator = Draft202012Validator(schemas[sname], registry=registry)
            errors = sorted(validator.iter_errors(part["instance"]), key=str)
            check("example %s part %d validates against %s" % (fn, i, sname), not errors,
                  "; ".join(e.message[:120] for e in errors[:3]))
            if sname == "verdict-record.schema.json":
                inst = part["instance"]
                st = inst["statuses"]
                # NA reasons present
                miss = [v for v, s in st.items() if s == "not-applicable" and v not in inst.get("na_reasons", {})]
                check("example %s: every not-applicable verdict has a reason" % fn, not miss, str(miss))
                # required path inside registry core
                badreq = [v for v in inst["required_path"] if v not in core]
                check("example %s: required_path inside registry core" % fn, not badreq, str(badreq))
                # claim-wise factivity
                ok = all(not (c.get("token_truth_linked") == "pass" and c["result_correct"] != "pass")
                         for c in inst.get("claim_verdicts", []))
                check("example %s: TOKEN_TRUTH_LINKED implies RESULT_CORRECT claim-wise" % fn, ok)
                # recompute pathway state
                req = inst["required_path"]
                if any(st.get(v) in (None, "not-applicable") for v in req):
                    state = "MALFORMED"
                elif any(st[v] == "fail" for v in req):
                    state = "defective"
                elif any(st[v] == "undetermined" for v in req):
                    state = "undetermined"
                else:
                    state = "adequate"
                check("example %s: pathway_state matches recomputation" % fn,
                      state == inst["pathway_state"], "computed=%s declared=%s" % (state, inst["pathway_state"]))
    check("expected example files present (9)",
          n_parts > 0 and len([f for f in os.listdir(edir) if f.endswith(".json")]) == 9,
          str(sorted(f for f in os.listdir(edir) if f.endswith(".json"))))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
