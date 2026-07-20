#!/usr/bin/env python3
"""Deterministic semantic validator for the verdict semantics.

Decisions 0003 (result-free pathway core) + 0004 (verdict registry). The
registry file docs/verdict-registry.yaml DRIVES this validator: the pathway
core, exclusions, status enum, entailments, and alias table are loaded from
it, so reordering or renaming there cannot silently diverge from the checked
semantics. This is a deterministic consistency check over declared fixture
data. It is NOT an empirical experiment and establishes no empirical claim
about the framework's utility.

Usage:
    python validate_verdict_semantics.py [--fixtures PATH] [--registry PATH]
                                         [--hash-manifest PATH]
"""
import argparse
import hashlib
import json
import os
import sys

try:
    import yaml
except ImportError:  # minimal fallback: registry subset parser not provided
    print("FATAL: PyYAML is required (pip install pyyaml)")
    sys.exit(2)

CHECKS = []


def check(num, desc, ok, detail=""):
    CHECKS.append((num, desc, ok, detail))


def pathway_state(fx):
    statuses = fx["statuses"]
    req = fx["required"]
    for v in req:
        if statuses.get(v) in (None, "not-applicable"):
            return "MALFORMED: required verdict %s lacks an evaluable status" % v
    if any(statuses[v] == "fail" for v in req):
        return "defective"
    if any(statuses[v] == "undetermined" for v in req):
        return "undetermined"
    if all(statuses[v] == "pass" for v in req):
        return "adequate"
    return "MALFORMED"


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--fixtures", default=os.path.join(here, "..", "tests", "verdict-fixtures.json"))
    ap.add_argument("--registry", default=os.path.join(here, "..", "docs", "verdict-registry.yaml"))
    ap.add_argument("--hash-manifest", default=None)
    args = ap.parse_args()

    with open(args.registry, "r", encoding="utf-8") as f:
        reg = yaml.safe_load(f)
    with open(args.fixtures, "r", encoding="utf-8") as f:
        data = json.load(f)

    ids = [v["id"] for v in reg["verdicts"]]
    aliases = {v["id"]: v["alias"] for v in reg["verdicts"]}
    core = reg["core_path"]
    excluded = set(reg["excluded_from_core"])
    enum = set(reg["status_enum"])
    fixtures = data["fixtures"]

    # 0a: registry well-formed — IDs unique, aliases unique, core ⊆ ids, excluded ⊆ ids
    check(0, "registry IDs unique", len(ids) == len(set(ids)))
    check(0, "registry aliases unique", len(set(aliases.values())) == len(aliases))
    check(0, "core_path is a subset of registry IDs", set(core) <= set(ids))
    check(0, "excluded_from_core is a subset of registry IDs", excluded <= set(ids))
    check(0, "core_path and excluded_from_core partition the verdict set",
          set(core) | excluded == set(ids) and not (set(core) & excluded))
    # 0b: fixture status enum matches the registry's
    check(0, "fixture status enum matches registry", set(data["status_enum"]) == enum)

    # 1-3: exclusions from the pathway core
    check(1, "RESULT_CORRECT (V1) absent from pathway core", "RESULT_CORRECT" not in core)
    check(2, "TOKEN_TRUTH_LINKED (V2b-T) absent from pathway core", "TOKEN_TRUTH_LINKED" not in core)
    check(3, "ROUTE_QUALITY (V4b) absent from pathway core", "ROUTE_QUALITY" not in core)

    # 4: GOV_TOKEN_ADEQUATE required exactly when MetaTok nonempty
    ok4 = all((fx["metatok_nonempty"]) == ("GOV_TOKEN_ADEQUATE" in fx["required"]) for fx in fixtures)
    check(4, "GOV_TOKEN_ADEQUATE (V3c) required iff MetaTok(e) nonempty (zero-burden rule)", ok4)

    # 5: registry entailments hold claim-wise on every fixture claim
    ok5 = True
    for ent in reg.get("entailments", []):
        if ent["premise"] == "TOKEN_TRUTH_LINKED" and ent["conclusion"] == "RESULT_CORRECT":
            ok5 = all(not (c["token_truth_linked"] == "pass" and c["result_correct"] != "pass")
                      for fx in fixtures for c in fx.get("claims", []))
    check(5, "TOKEN_TRUTH_LINKED_q implies RESULT_CORRECT_q on every fixture claim", ok5)

    # 6: PROCEDURE_RELIABLE does not imply RESULT_CORRECT (witness exists)
    ok6 = any(fx["statuses"].get("PROCEDURE_RELIABLE") == "pass"
              and fx["statuses"].get("RESULT_CORRECT") == "fail" for fx in fixtures)
    check(6, "PROCEDURE_RELIABLE non-factive: witness with pass + RESULT_CORRECT fail exists (F3)", ok6)

    # compute pathway states and expected agreement
    states = {}
    for fx in fixtures:
        st = pathway_state(fx)
        states[fx["id"]] = st
        exp = fx["expected"]["pathway"]
        check(0, "fixture %s pathway state matches expected (%s)" % (fx["id"], exp), st == exp,
              "computed=%s" % st)
        expected_v1 = fx["expected"]["result"]
        check(0, "fixture %s RESULT_CORRECT status matches expected (%s)" % (fx["id"], expected_v1),
              fx["statuses"].get("RESULT_CORRECT") == expected_v1)
        bad = [k for k, v in fx["statuses"].items() if v not in enum]
        check(0, "fixture %s uses only enum statuses" % fx["id"], not bad, str(bad))
        badkeys = [k for k in fx["statuses"] if k not in ids]
        check(0, "fixture %s uses only registry verdict IDs" % fx["id"], not badkeys, str(badkeys))
        badreq = [v for v in fx["required"] if v not in core]
        check(0, "fixture %s required set is inside the registry core" % fx["id"], not badreq, str(badreq))

    # 7: all four resolved result x pathway combinations satisfiable
    combos = set()
    for fx in fixtures:
        st = states[fx["id"]]
        if st in ("adequate", "defective"):
            combos.add((fx["statuses"]["RESULT_CORRECT"], st))
    ok7 = {("pass", "adequate"), ("pass", "defective"), ("fail", "adequate"),
           ("fail", "defective")} <= combos
    check(7, "all four resolved result x pathway combinations witnessed", ok7,
          "witnessed=%s" % sorted(combos))

    # 8: undetermined required verdict prevents PathwayAdequate
    check(8, "undetermined required verdict yields PathwayUndetermined, never adequate",
          states["F5"] == "undetermined")

    # 9: every not-applicable verdict carries a recorded reason
    ok9, detail9 = True, []
    for fx in fixtures:
        for v, s in fx["statuses"].items():
            if s == "not-applicable" and v not in fx.get("na_reasons", {}):
                ok9 = False
                detail9.append("%s:%s" % (fx["id"], v))
    check(9, "every not-applicable verdict has a recorded applicability reason", ok9, str(detail9))

    # 10: 'not evaluated' is never encoded as 'not-applicable'
    ok10 = all(fx["statuses"].get(v) == "undetermined"
               for fx in fixtures for v in fx.get("unevaluated", []))
    check(10, "unevaluated verdicts are 'undetermined', never 'not-applicable'", ok10)

    # 11: stopped-clock fixture is correct + defective
    check(11, "F2 stopped-clock is RESULT_CORRECT pass + PathwayDefective",
          next(fx for fx in fixtures if fx["id"] == "F2")["statuses"]["RESULT_CORRECT"] == "pass"
          and states["F2"] == "defective")

    # 12: rare-miss fixture is incorrect + adequate
    check(12, "F3 rare miss is RESULT_CORRECT fail + PathwayAdequate",
          next(fx for fx in fixtures if fx["id"] == "F3")["statuses"]["RESULT_CORRECT"] == "fail"
          and states["F3"] == "adequate")

    # 13: defective-binding fixture is correct + defective through GOV_TOKEN_ADEQUATE alone
    f4 = next(fx for fx in fixtures if fx["id"] == "F4")
    only_v3c_fails = all(f4["statuses"][v] == "pass" for v in f4["required"] if v != "GOV_TOKEN_ADEQUATE")
    check(13, "F4 defective binding is result-correct + PathwayDefective with GOV_TOKEN_ADEQUATE the sole failing verdict",
          f4["statuses"]["RESULT_CORRECT"] == "pass" and states["F4"] == "defective"
          and f4["statuses"]["GOV_TOKEN_ADEQUATE"] == "fail" and only_v3c_fails)

    # 14: stale-directive fixture (O3): faithful execution + stale token + stale currentness
    f6 = next((fx for fx in fixtures if fx["id"] == "F6"), None)
    check(14, "F6 stale directive: EXECUTION_FAITHFUL pass with GOV_TOKEN_ADEQUATE and EVIDENCE_CURRENT fail, PathwayDefective",
          f6 is not None and f6["statuses"]["EXECUTION_FAITHFUL"] == "pass"
          and f6["statuses"]["GOV_TOKEN_ADEQUATE"] == "fail"
          and f6["statuses"]["EVIDENCE_CURRENT"] == "fail" and states["F6"] == "defective")

    # 15: safe-but-suboptimal fixture: ROUTE_QUALITY fail never defeats adequacy
    f7 = next((fx for fx in fixtures if fx["id"] == "F7"), None)
    check(15, "F7 safe-not-best: ROUTE_QUALITY fail with PathwayAdequate (advisory verdict outside core)",
          f7 is not None and f7["statuses"]["ROUTE_QUALITY"] == "fail" and states["F7"] == "adequate")

    # 16: governed source files match recorded hashes (optional)
    if args.hash_manifest:
        with open(args.hash_manifest, "r", encoding="utf-8") as f:
            hm = json.load(f)
        base = os.path.dirname(os.path.abspath(args.hash_manifest))
        ok16, det = True, []
        for p, expected in hm.items():
            fp = p if os.path.isabs(p) else os.path.join(base, p)
            h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
            if h.lower() != expected.lower():
                ok16 = False
                det.append("%s: %s != %s" % (p, h[:12], expected[:12]))
        check(16, "governed source files match recorded hashes", ok16, "; ".join(det))
    else:
        check(16, "hash-manifest check skipped (no manifest supplied)", True, "SKIPPED")

    failures = [c for c in CHECKS if not c[2]]
    for num, desc, ok, detail in CHECKS:
        tag = "PASS" if ok else "FAIL"
        n = ("%02d" % num) if num else "--"
        print("[%s] %s %s %s" % (tag, n, desc, ("(" + detail + ")") if detail and not ok or detail == "SKIPPED" else ""))
    print("TOTAL: %d checks, %d failures" % (len(CHECKS), len(failures)))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
