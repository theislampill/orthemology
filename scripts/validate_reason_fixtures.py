#!/usr/bin/env python3
"""CR-1..CR-8 reason-fixture validator (Decision 0009).

Recomputes, per fixture: pathway aggregation over the registry core path
(zero-burden rule for CR-8), claim-level factivity (TOKEN_TRUTH_LINKED pass
entails RESULT_CORRECT pass), and the DERIVED predicate
StrictlySoundReasoning = PathwayAdequate AND TOKEN_TRUTH_LINKED, checking each
against the fixture's declared expectations. Also enforces the presence of the
required structural cases (rare miss; lucky result; binding-failure-with-
faithful-execution; evaluator symmetry; zero-burden negative control).
Deterministic; no empirical claim."""
import json
import os
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def pathway(statuses, req):
    if any(statuses.get(v) in (None, "not-applicable") for v in req):
        return "MALFORMED"
    if any(statuses[v] == "fail" for v in req):
        return "defective"
    if any(statuses[v] == "undetermined" for v in req):
        return "undetermined"
    return "adequate"


def main():
    reg = yaml.safe_load(open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8"))
    core = list(reg["core_path"])
    reg_ids = {v["id"] for v in reg["verdicts"]}

    data = json.load(open(os.path.join(ROOT, "tests", "reason-fixtures.json"), encoding="utf-8"))
    fixtures = {f["id"]: f for f in data["fixtures"]}
    check("all eight CR fixtures present",
          set(fixtures) == {"CR-%d" % i for i in range(1, 9)}, str(sorted(fixtures)))

    for fid, f in sorted(fixtures.items()):
        st = f["statuses"]
        bad = sorted(set(st) - reg_ids)
        check("%s statuses use registry IDs" % fid, not bad, str(bad))

        req = [v for v in core if v in st or not f.get("no_meta_token")]
        # required path: registry core, minus GOV_TOKEN_ADEQUATE under the zero-burden rule
        req = [v for v in core if not (v == "GOV_TOKEN_ADEQUATE" and f.get("no_meta_token"))]
        missing = [v for v in req if v not in st]
        check("%s covers its required path" % fid, not missing, str(missing))
        state = pathway(st, req)
        check("%s pathway recomputation matches expectation (%s)" % (fid, state),
              state == f["expected"]["pathway_state"],
              "computed=%s declared=%s" % (state, f["expected"]["pathway_state"]))

        claim = f["claim"]
        if claim.get("TOKEN_TRUTH_LINKED") == "pass":
            check("%s factivity: TOKEN_TRUTH_LINKED pass entails RESULT_CORRECT pass" % fid,
                  claim.get("RESULT_CORRECT") == "pass")
        derived = (state == "adequate" and claim.get("TOKEN_TRUTH_LINKED") == "pass")
        check("%s derived strict soundness matches expectation" % fid,
              derived == f["expected"]["strictly_sound"],
              "derived=%s declared=%s" % (derived, f["expected"]["strictly_sound"]))

    # structural guarantees
    cr3, cr4, cr6, cr7, cr8 = (fixtures[k] for k in ("CR-3", "CR-4", "CR-6", "CR-7", "CR-8"))
    check("CR-3 is an adequate-pathway rare miss",
          cr3["expected"]["pathway_state"] == "adequate" and cr3["claim"]["RESULT_CORRECT"] == "fail")
    check("CR-4 is a lucky correct result (defective pathway, no truth link)",
          cr4["expected"]["pathway_state"] == "defective" and cr4["claim"]["RESULT_CORRECT"] == "pass"
          and cr4["claim"]["TOKEN_TRUTH_LINKED"] != "pass")
    check("CR-6 separates binding failure from execution (token fail + faithful execution)",
          cr6["statuses"]["GOV_TOKEN_ADEQUATE"] == "fail"
          and cr6["statuses"]["EXECUTION_FAITHFUL"] == "pass"
          and cr6.get("per_token", [{}])[0].get("failing_conjunct") == "ScopeCorrect")
    aud = cr7.get("audit_of_audit", {})
    check("CR-7 evaluator symmetry: auditor's own episode scored under the same registry",
          bool(aud) and pathway(aud["statuses"], core) == aud["expected_pathway_state"])
    check("CR-8 zero-burden rule: no metaorthemma, GOV_TOKEN_ADEQUATE excluded from path",
          cr8.get("no_meta_token") is True and "GOV_TOKEN_ADEQUATE" not in cr8["statuses"])

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
