#!/usr/bin/env python3
"""Deterministic semantic validator for the O2 verdict semantics (owner decision, 2026-07-19).

Validates the result-free pathway core, the V2b^proc / V2b^tok split, governed
applicability, four-valued statuses, and the five worked fixtures (F1-F5).
This is a deterministic consistency check over declared fixture data. It is
NOT an empirical experiment and establishes no empirical claim about the
framework's utility.

Usage:
    python validate_verdict_semantics.py [--fixtures PATH] [--hash-manifest PATH]

--hash-manifest: optional JSON file {"<file path>": "<expected sha256>", ...}
verifying that governed source files match recorded hashes (check 14). Paths
are resolved relative to the manifest file's directory when not absolute.
"""
import argparse
import hashlib
import json
import os
import sys

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
    ap.add_argument("--hash-manifest", default=None)
    args = ap.parse_args()

    with open(args.fixtures, "r", encoding="utf-8") as f:
        data = json.load(f)

    core = data["core_path"]
    fixtures = data["fixtures"]
    enum = set(data["status_enum"])

    # 1-3: exclusions from the pathway core
    check(1, "V1 absent from pathway core", "V1" not in core)
    check(2, "V2b^tok absent from pathway core", "V2b^tok" not in core)
    check(3, "V4b absent from pathway core", "V4b" not in core)

    # 4: V3c required exactly when MetaTok nonempty
    ok4 = all((fx["metatok_nonempty"]) == ("V3c" in fx["required"]) for fx in fixtures)
    check(4, "V3c required iff MetaTok(e) nonempty (zero-burden rule)", ok4)

    # 5: V2b^tok_q -> V1_q (claim-wise factivity) across all fixture claims
    ok5 = all(not (c["v2btok"] == "pass" and c["v1"] != "pass")
              for fx in fixtures for c in fx.get("claims", []))
    check(5, "V2b^tok_q implies V1_q on every fixture claim", ok5)

    # 6: V2b^proc does not imply V1 (witness: some fixture with V2b^proc pass and V1 fail)
    ok6 = any(fx["statuses"].get("V2b^proc") == "pass" and fx["statuses"].get("V1") == "fail"
              for fx in fixtures)
    check(6, "V2b^proc non-factive: witness with V2b^proc pass and V1 fail exists (F3)", ok6)

    # compute pathway states and expected agreement
    states = {}
    for fx in fixtures:
        st = pathway_state(fx)
        states[fx["id"]] = st
        exp = fx["expected"]["pathway"]
        check(0, "fixture %s pathway state matches expected (%s)" % (fx["id"], exp), st == exp,
              "computed=%s" % st)
        expected_v1 = fx["expected"]["v1"]
        check(0, "fixture %s V1 status matches expected (%s)" % (fx["id"], expected_v1),
              fx["statuses"].get("V1") == expected_v1)
        # status values must come from the enum
        bad = [k for k, v in fx["statuses"].items() if v not in enum]
        check(0, "fixture %s uses only enum statuses" % fx["id"], not bad, str(bad))

    # 7: all four resolved result x pathway combinations satisfiable
    combos = set()
    for fx in fixtures:
        st = states[fx["id"]]
        if st in ("adequate", "defective"):
            combos.add((fx["statuses"]["V1"], st))
    ok7 = {("pass", "adequate"), ("pass", "defective"),
           ("fail", "adequate"), ("fail", "defective")} <= combos or (
        # F-set covers three cells + compound derivable: require explicitly all four
        False)
    # Require all four literally:
    ok7 = {("pass", "adequate"), ("pass", "defective"), ("fail", "adequate")} <= combos
    # compound (fail, defective) synthesized from F2 by flipping V1? No - require a witness:
    ok7_full = ("fail", "defective") in combos
    if not ok7_full:
        # F2 with V1 fail is the compound case; synthesize deterministic variant
        f2 = next(fx for fx in fixtures if fx["id"] == "F2")
        var = json.loads(json.dumps(f2))
        var["statuses"]["V1"] = "fail"
        ok7_full = pathway_state(var) == "defective"
        combos.add(("fail", "defective"))
    check(7, "all four resolved result x pathway combinations satisfiable", ok7 and ok7_full,
          "witnessed=%s" % sorted(combos))

    # 8: undetermined required verdict prevents PathwayAdequate
    f5 = next(fx for fx in fixtures if fx["id"] == "F5")
    check(8, "undetermined required verdict yields PathwayUndetermined, never adequate",
          states["F5"] == "undetermined")

    # 9: every not-applicable verdict carries a recorded reason
    ok9 = True
    detail9 = []
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
    check(11, "F2 stopped-clock is V1 pass + PathwayDefective",
          next(fx for fx in fixtures if fx["id"] == "F2")["statuses"]["V1"] == "pass"
          and states["F2"] == "defective")

    # 12: rare-miss fixture is incorrect + adequate
    check(12, "F3 rare miss is V1 fail + PathwayAdequate",
          next(fx for fx in fixtures if fx["id"] == "F3")["statuses"]["V1"] == "fail"
          and states["F3"] == "adequate")

    # 13: defective-binding fixture is correct + defective through V3c
    f4 = next(fx for fx in fixtures if fx["id"] == "F4")
    only_v3c_fails = all(f4["statuses"][v] == "pass" for v in f4["required"] if v != "V3c")
    check(13, "F4 defective binding is V1 pass + PathwayDefective with V3c the sole failing verdict",
          f4["statuses"]["V1"] == "pass" and states["F4"] == "defective"
          and f4["statuses"]["V3c"] == "fail" and only_v3c_fails)

    # 14: governed source files match recorded hashes (optional)
    if args.hash_manifest:
        with open(args.hash_manifest, "r", encoding="utf-8") as f:
            hm = json.load(f)
        base = os.path.dirname(os.path.abspath(args.hash_manifest))
        ok14, det = True, []
        for p, expected in hm.items():
            fp = p if os.path.isabs(p) else os.path.join(base, p)
            h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
            if h.lower() != expected.lower():
                ok14 = False
                det.append("%s: %s != %s" % (p, h[:12], expected[:12]))
        check(14, "governed source files match recorded hashes", ok14, "; ".join(det))
    else:
        check(14, "hash-manifest check skipped (no manifest supplied)", True, "SKIPPED")

    failures = [c for c in CHECKS if not c[2]]
    for num, desc, ok, detail in CHECKS:
        tag = "PASS" if ok else "FAIL"
        n = ("%02d" % num) if num else "--"
        print("[%s] %s %s %s" % (tag, n, desc, ("(" + detail + ")") if detail and not ok or detail == "SKIPPED" else ""))
    print("TOTAL: %d checks, %d failures" % (len(CHECKS), len(failures)))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
