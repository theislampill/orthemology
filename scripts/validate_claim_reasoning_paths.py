#!/usr/bin/env python3
"""Claim-relative reasoning-path validator (Decision 0011; R4 independent review).

For every fixture in tests/claim-reasoning-fixtures.json this validator
recomputes, claim by claim, INDEPENDENTLY of any recorded projection:

  1. ReqPath(e) from the episode shape (docs/governance-requirements.yaml,
     reusing derive_reqpath's derivation);
  2. ReqReason_q(e) from the CLAIM shape via the machine-readable rule table
     docs/claim-reason-requirements.yaml (RequiredReasonBy instance), with a
     per-verdict inclusion/exclusion trace, always intersected with ReqPath(e);
  3. the claim-relative four-valued aggregation over ReqReason_q(e)
     (MALFORMED / defective / undetermined / adequate);
  4. ReasoningPathAdequate_q(e) — non-factive;
  5. token truth-link factivity: TOKEN_TRUTH_LINKED_q pass entails
     RESULT_CORRECT_q pass;
  6. StrictlySoundReasoning_q(e) := ReasoningPathAdequate_q(e) AND
     TOKEN_TRUTH_LINKED_q(e) — the sole current normative formula
     (Decision 0011; Decision 0009's whole-episode formula is superseded);
  7. INDEPENDENCE: for non-routing/non-closure claims, flipping the episode's
     ROUTE_ADMISSIBLE / CLOSURE_TRUTHFUL statuses must not change the claim's
     reasoning state or strict soundness;
  8. OMISSION ATTACK: a recorded projection that omits a derivable requirement
     (CR-OMIT-1) is detected as a mismatch and the derived — never the
     recorded — projection decides the claim's state.

Also asserts the structural presence of the whole Decision-0011 family:
shared-upstream corroboration under evaluator symmetry (CR-9), route-defect and
closure-defect independence (CR-10/11, both diverging from the superseded
formula), the mixed episode (CR-12), correct-by-luck (CR-13), the rare miss
(CR-14), the unresolved claim (CR-15), and the omission attack (CR-OMIT-1).
Deterministic; no empirical claim."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from derive_reqpath import derive as derive_reqpath_set, load as load_gov  # noqa: E402

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


def aggregate(statuses, req):
    if any(statuses.get(v) in (None, "not-applicable") for v in req):
        return "MALFORMED"
    if any(statuses[v] == "fail" for v in req):
        return "defective"
    if any(statuses[v] == "undetermined" for v in req):
        return "undetermined"
    return "adequate"


def derive_req_reason(claim_shape, rules, core, req_path):
    """ReqReason_q(e) with per-verdict trace; constrained to ReqPath(e)."""
    req, trace = [], []
    for v in core:
        rule = rules.get(v)
        if rule is None:
            trace.append((v, "EXCLUDED", "no claim-reason rule names this core verdict"))
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
        if needed and v not in req_path:
            trace.append((v, "EXCLUDED", "episode does not owe this verdict (ReqPath constraint)"))
            continue
        trace.append((v, "REQUIRED" if needed else "EXCLUDED",
                      "when=%s; %s" % (cond, rule["rationale"])))
        if needed:
            req.append(v)
    return req, trace


def eval_claim(cl, statuses, req_path, rules, core):
    """Returns (derived req_reason, reasoning_state, strictly_sound)."""
    req_reason, trace = derive_req_reason(cl["shape"], rules, core, req_path)
    state = aggregate(statuses, req_reason)
    ttl = cl["claim"].get("TOKEN_TRUTH_LINKED")
    sound = (state == "adequate" and ttl == "pass")
    return req_reason, trace, state, sound


def main():
    gov, reg = load_gov()
    core = list(reg["core_path"])
    rules = yaml.safe_load(open(os.path.join(ROOT, "docs", "claim-reason-requirements.yaml"),
                                encoding="utf-8"))["rules"]
    bad_rule_ids = sorted(set(rules) - set(core))
    check("claim-reason rules name only CorePath verdicts", not bad_rule_ids, str(bad_rule_ids))

    data = json.load(open(os.path.join(ROOT, "tests", "claim-reasoning-fixtures.json"),
                          encoding="utf-8"))
    fixtures = {f["id"]: f for f in data["fixtures"]}
    want_ids = {"CR-%d" % i for i in range(9, 16)} | {"CR-OMIT-1"}
    check("claim-relative family is complete (CR-9..CR-15 + CR-OMIT-1)",
          set(fixtures) == want_ids, str(sorted(fixtures)))

    def episode_units(f):
        """Yield (label, episode_shape, statuses, claims) units of a fixture."""
        if "evaluators" in f:
            for ev in f["evaluators"]:
                yield ev["actor"], ev["episode_shape"], ev["statuses"], ev["claims"]
        else:
            yield f["id"], f["episode_shape"], f["statuses"], f["claims"]

    for fid, f in sorted(fixtures.items()):
        for label, eshape, statuses, claims in episode_units(f):
            req_path, _ = derive_reqpath_set(eshape, gov, reg)
            missing = [v for v in req_path if v not in statuses]
            check("%s/%s statuses cover the derived ReqPath" % (fid, label), not missing,
                  str(missing))

            if "expected_episode_pathway_state" in f:
                ep_state = aggregate(statuses, req_path)
                check("%s episode pathway state recomputes (%s)"
                      % (fid, f["expected_episode_pathway_state"]),
                      ep_state == f["expected_episode_pathway_state"],
                      "computed=%s" % ep_state)

            for cl in claims:
                cid = cl["claim_id"]
                req_reason, trace, state, sound = eval_claim(cl, statuses, req_path, rules, core)

                check("%s/%s ReqReason is a subset of ReqPath" % (fid, cid),
                      set(req_reason) <= set(req_path))
                check("%s/%s derivation trace covers every CorePath verdict" % (fid, cid),
                      [t[0] for t in trace] == core)
                check("%s/%s reasoning state recomputes (%s)" % (fid, cid,
                      cl["expected"]["reasoning_state"]),
                      state == cl["expected"]["reasoning_state"],
                      "derived req_reason=%s computed=%s" % (req_reason, state))

                ttl, rc = cl["claim"].get("TOKEN_TRUTH_LINKED"), cl["claim"].get("RESULT_CORRECT")
                if ttl == "pass":
                    check("%s/%s factivity: TOKEN_TRUTH_LINKED pass entails RESULT_CORRECT pass"
                          % (fid, cid), rc == "pass")
                check("%s/%s strict soundness recomputes (%s)" % (fid, cid,
                      cl["expected"]["strictly_sound"]),
                      sound == cl["expected"]["strictly_sound"],
                      "computed=%s" % sound)

                # independence probe: unrelated route/closure flips change nothing
                if cl["shape"]["claim_type"] not in ("routing", "closure"):
                    mut = dict(statuses)
                    for v in ("ROUTE_ADMISSIBLE", "CLOSURE_TRUTHFUL"):
                        if v in mut:
                            mut[v] = "pass" if mut[v] == "fail" else "fail"
                    _, _, mstate, msound = eval_claim(cl, mut, req_path, rules, core)
                    check("%s/%s independent of unrelated route/closure verdicts" % (fid, cid),
                          (mstate, msound) == (state, sound),
                          "flipping route/closure changed the claim: %s->%s sound %s->%s"
                          % (state, mstate, sound, msound))

                # omission attack: recorded projection must match the derivation
                if "recorded_req_reason" in cl:
                    rec = cl["recorded_req_reason"]
                    omitted = sorted(set(req_reason) - set(rec))
                    detected = bool(omitted)
                    check("%s/%s omission attack detected (recorded projection omits %s)"
                          % (fid, cid, omitted), detected == cl["expected"].get(
                              "omission_detected", False),
                          "recorded=%s derived=%s" % (rec, req_reason))
                    if "state_if_recorded_projection_trusted" in cl["expected"]:
                        trusted = aggregate(statuses, rec)
                        check("%s/%s trusting the recorded projection would manufacture %r"
                              % (fid, cid, cl["expected"]["state_if_recorded_projection_trusted"]),
                              trusted == cl["expected"]["state_if_recorded_projection_trusted"],
                              "computed=%s" % trusted)
                        check("%s/%s the derived projection, not the recorded one, decides"
                              % (fid, cid), state != trusted or not detected)

    # -------- structural guarantees for the whole family --------
    cr9 = fixtures["CR-9"]
    evs = cr9.get("evaluators", [])
    all_claims9 = [c for ev in evs for c in ev["claims"]]
    check("CR-9 has >=2 agreeing evaluators with a declared shared upstream",
          len(evs) >= 2 and cr9.get("agreement") is True
          and len(cr9.get("shared_upstream", {}).get("shared_by", [])) >= 2)
    check("CR-9 evaluator symmetry: every evaluator episode is itself scored",
          all("statuses" in ev for ev in evs))
    check("CR-9 corroboration + symmetry do NOT yield truth: all reasoning adequate, "
          "none strictly sound",
          all(c["expected"]["reasoning_state"] == "adequate" for c in all_claims9)
          and not any(c["expected"]["strictly_sound"] for c in all_claims9))

    for fid, why in (("CR-10", "route-defect"), ("CR-11", "closure-defect")):
        f = fixtures[fid]
        check("%s diverges from the superseded whole-episode formula "
              "(episode defective, claim strictly sound)" % fid,
              f.get("diverges_from_superseded_formula") is True
              and f["expected_episode_pathway_state"] == "defective"
              and f["claims"][0]["expected"]["strictly_sound"] is True)

    c12 = fixtures["CR-12"]["claims"]
    check("CR-12 mixed episode carries one strictly sound and one unsound claim",
          sorted(c["expected"]["strictly_sound"] for c in c12) == [False, True])
    c13 = fixtures["CR-13"]["claims"][0]
    check("CR-13 correct-by-luck: result right, not strictly sound",
          c13["claim"]["RESULT_CORRECT"] == "pass"
          and c13["expected"]["strictly_sound"] is False)
    c14 = fixtures["CR-14"]["claims"][0]
    check("CR-14 rare miss: adequate claim-relevant reasoning, false result",
          c14["expected"]["reasoning_state"] == "adequate"
          and c14["claim"]["RESULT_CORRECT"] == "fail")
    c15 = fixtures["CR-15"]["claims"][0]
    check("CR-15 unresolved claim: undetermined reasoning, not strictly sound",
          c15["expected"]["reasoning_state"] == "undetermined"
          and c15["expected"]["strictly_sound"] is False)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
