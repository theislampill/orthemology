#!/usr/bin/env python3
"""CR-1..CR-8 reason-fixture validator (Decision 0009 structural cases;
strict soundness per Decision 0011).

Recomputes, per fixture: EPISODE pathway aggregation over the registry core
path (zero-burden rule for CR-8), claim-level factivity (TOKEN_TRUTH_LINKED
pass entails RESULT_CORRECT pass), and the DERIVED predicate
StrictlySoundReasoning_q = ReasoningPathAdequate_q AND TOKEN_TRUTH_LINKED_q —
the CLAIM-RELATIVE formula of Decision 0011, computed over ReqReason_q derived
from each fixture's declared claim_shape via docs/claim-reason-requirements.yaml.
The superseded whole-episode formula (Decision 0009, superseded by dated
notice) is no longer enforced anywhere; the episode pathway state remains
checked as an episode-level fact. The full claim-relative divergence family
(CR-9..CR-15, CR-OMIT-1) lives in scripts/validate_claim_reasoning_paths.py.
Also enforces the presence of the required structural cases (rare miss; lucky
result; binding-failure-with-faithful-execution; evaluator symmetry;
zero-burden negative control). Deterministic; no empirical claim."""
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


def req_reason(core, rules, claim_shape, req_path):
    """ReqReason_q per docs/claim-reason-requirements.yaml, constrained to ReqPath."""
    out = []
    for v in core:
        rule = rules.get(v)
        if rule is None or v not in req_path:
            continue
        cond = rule["when"]
        if cond == "always":
            needed = True
        elif cond.startswith("claim_type="):
            needed = claim_shape.get("claim_type") == cond.split("=", 1)[1]
        elif cond.startswith("not_"):
            needed = not bool(claim_shape.get(cond[4:], False))
        else:
            needed = bool(claim_shape.get(cond, False))
        if needed:
            out.append(v)
    return out


def main():
    reg = yaml.safe_load(open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8"))
    core = list(reg["core_path"])
    reg_ids = {v["id"] for v in reg["verdicts"]}
    reason_rules = yaml.safe_load(open(os.path.join(ROOT, "docs", "claim-reason-requirements.yaml"),
                                       encoding="utf-8"))["rules"]

    data = json.load(open(os.path.join(ROOT, "tests", "reason-fixtures.json"), encoding="utf-8"))
    fixtures = {f["id"]: f for f in data["fixtures"]}
    check("all eight CR fixtures present",
          set(fixtures) == {"CR-%d" % i for i in range(1, 9)}, str(sorted(fixtures)))

    for fid, f in sorted(fixtures.items()):
        st = f["statuses"]
        bad = sorted(set(st) - reg_ids)
        check("%s statuses use registry IDs" % fid, not bad, str(bad))

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
        # Decision 0011: strict soundness is CLAIM-relative — computed over the
        # governance-derived ReqReason_q projection, never the whole episode path.
        shape = f.get("claim_shape", {"claim_type": "placement",
                                      "depends_on_tokens": not f.get("no_meta_token"),
                                      "robustness_obligation": True})
        rr = req_reason(core, reason_rules, shape, req)
        reasoning_state = pathway(st, rr)
        derived = (reasoning_state == "adequate" and claim.get("TOKEN_TRUTH_LINKED") == "pass")
        check("%s derived strict soundness (claim-relative, Decision 0011) matches expectation" % fid,
              derived == f["expected"]["strictly_sound"],
              "req_reason=%s reasoning_state=%s derived=%s declared=%s"
              % (rr, reasoning_state, derived, f["expected"]["strictly_sound"]))

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
