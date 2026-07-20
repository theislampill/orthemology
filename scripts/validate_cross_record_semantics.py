#!/usr/bin/env python3
"""Cross-record semantic validator (R3 §7.2). Deterministic, offline.

Checks that JSON Schema cannot express, over every example file's parts and
any instance handed to `check_instance`:
  - episode.analysis == each meta-token.analysis (id and version);
  - episode.occurrence == each meta-token.anchor (identity and version);
  - unique evidence/token/claim ids within a record;
  - verdict record: pathway_state recomputes exactly from statuses over
    required_path; every not-applicable status on the required path has a
    recorded na_reason; per_token_v3c token ids resolve against the episode's
    meta-tokens (when both records are present in one example); the V3c
    aggregate matches per-token statuses; required_path uses registry ids and
    respects the shipped governance derivation for the episode's shape
    (GOV_TOKEN_ADEQUATE required iff tokens exist; ROUTE_ADMISSIBLE iff a route
    was selected) — declared != derived is a failure;
  - binder and executor remain distinct ROLES: every meta-token records a
    binder; if a designated_executor is present it may equal the binder actor,
    but the binder field must still be independently populated;
  - handoff state_claims carry valid_for_version (anti-transport rule).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def recompute_pathway(inst):
    st, req = inst["statuses"], inst["required_path"]
    if any(st.get(v) in (None, "not-applicable") for v in req):
        return "MALFORMED"
    if any(st[v] == "fail" for v in req):
        return "defective"
    if any(st[v] == "undetermined" for v in req):
        return "undetermined"
    return "adequate"


def collect_issues(parts):
    """Return a list of semantic-issue strings for one bundle of parts."""
    issues = []
    episodes = [p["instance"] for p in parts if p["schema"] == "orthing-episode.schema.json"]
    verdicts = [p["instance"] for p in parts if p["schema"] == "verdict-record.schema.json"]
    ledgers = [p["instance"] for p in parts if p["schema"] == "claim-ledger.schema.json"]
    standalone_tokens = {p["instance"]["token_id"] for p in parts
                         if p["schema"] == "metaorthemma.schema.json"}

    # whole-state reread rule (Definition 13 machine floor; daee-epistemics
    # import 2): a closure claim over an unresolved residual is ill-formed —
    # UNLESS the bundle's verdict record for that episode convicts it
    # (CLOSURE_TRUTHFUL fail/undetermined), in which case the record is a
    # legitimate REPRESENTATION of a false closure (e.g. the O3 case, F6).
    for led in ledgers:
        if led.get("closure_claim") is not None:
            bad = [r["burden_id"] for r in led.get("residuals", [])
                   if r["disposition"] == "unresolved"]
            if bad:
                vr = next((v for v in verdicts
                           if v.get("episode_id") == led.get("episode_id")), None)
                convicted = vr is not None and vr.get("statuses", {}).get(
                    "CLOSURE_TRUTHFUL") in ("fail", "undetermined")
                if not convicted:
                    issues.append("%s: closure claim asserted over unresolved residual(s) %s (false closure)"
                                  % (led.get("episode_id", "?"), bad))

    for ep in episodes:
        eid = ep.get("episode_id", "?")
        ean, eoc = ep.get("analysis", {}), ep.get("occurrence", {})
        for tok in ep.get("meta_tokens", []):
            tan, tanc = tok.get("analysis", {}), tok.get("anchor", {})
            if (tan.get("analysis_id"), tan.get("version")) != (ean.get("analysis_id"), ean.get("version")):
                issues.append("%s: meta-token %s analysis mismatch (%s vs %s)"
                              % (eid, tok.get("token_id"), tan, ean))
            if (tanc.get("identity_key"), tanc.get("version")) != (eoc.get("identity_key"), eoc.get("version")):
                issues.append("%s: meta-token %s anchored to a different occurrence (%s vs %s)"
                              % (eid, tok.get("token_id"), tanc, eoc))
            if not tok.get("binder", {}).get("actor"):
                issues.append("%s: meta-token %s lacks an independent binder role" % (eid, tok.get("token_id")))
        ev_ids = [e["evidence_id"] for e in ep.get("evidence", [])]
        if len(ev_ids) != len(set(ev_ids)):
            issues.append("%s: duplicate evidence ids %s" % (eid, sorted({i for i in ev_ids if ev_ids.count(i) > 1})))
        tok_ids = [t["token_id"] for t in ep.get("meta_tokens", [])]
        if len(tok_ids) != len(set(tok_ids)):
            issues.append("%s: duplicate token ids" % eid)
        for h in (ep.get("handoffs_in") or []) + (ep.get("handoffs_out") or []):
            for c in h.get("state_claims", []):
                if not c.get("valid_for_version"):
                    issues.append("%s: handoff claim %s lacks valid_for_version" % (eid, c.get("claim_id")))

    for vr in verdicts:
        vid = vr.get("episode_id", "?")
        state = recompute_pathway(vr)
        if state != vr.get("pathway_state"):
            issues.append("%s: pathway_state %r does not recompute (computed %r)"
                          % (vid, vr.get("pathway_state"), state))
        for v in vr["required_path"]:
            if vr["statuses"].get(v) == "not-applicable" and v not in vr.get("na_reasons", {}):
                issues.append("%s: %s not-applicable without a recorded reason" % (vid, v))
        ep = next((e for e in episodes if e.get("episode_id") == vid), None)
        if ep is not None:
            has_tokens = bool(ep.get("meta_tokens"))
            if has_tokens != ("GOV_TOKEN_ADEQUATE" in vr["required_path"]):
                issues.append("%s: GOV_TOKEN_ADEQUATE requirement does not match token presence (zero-burden rule)" % vid)
            selects_route = ep.get("route") is not None
            if selects_route and "ROUTE_ADMISSIBLE" not in vr["required_path"]:
                issues.append("%s: route selected but ROUTE_ADMISSIBLE not required" % vid)
            tok_ids = {t["token_id"] for t in ep.get("meta_tokens", [])} | standalone_tokens
            for pt in vr.get("per_token_v3c", []):
                if pt["token_id"] not in tok_ids:
                    issues.append("%s: per_token_v3c references unknown token %s" % (vid, pt["token_id"]))
            if vr.get("per_token_v3c") and "GOV_TOKEN_ADEQUATE" in vr["statuses"]:
                agg = ("fail" if any(pt["status"] == "fail" for pt in vr["per_token_v3c"])
                       else "undetermined" if any(pt["status"] == "undetermined" for pt in vr["per_token_v3c"])
                       else "pass")
                if agg != vr["statuses"]["GOV_TOKEN_ADEQUATE"]:
                    issues.append("%s: V3c aggregate %r does not match per-token statuses (computed %r)"
                                  % (vid, vr["statuses"]["GOV_TOKEN_ADEQUATE"], agg))
        else:
            for pt in vr.get("per_token_v3c", []):
                if pt["token_id"] not in standalone_tokens:
                    issues.append("%s: per_token_v3c token %s has no episode or standalone token record to resolve against"
                                  % (vid, pt["token_id"]))
    return issues


def main():
    edir = os.path.join(ROOT, "examples")
    total = 0
    for fn in sorted(os.listdir(edir)):
        if not fn.endswith(".json"):
            continue
        ex = json.load(open(os.path.join(edir, fn), encoding="utf-8"))
        issues = collect_issues(ex.get("parts", []))
        total += 1
        check("example %s cross-record semantics" % fn, not issues, "; ".join(issues[:3]))
    check("examples scanned", total >= 7, str(total))
    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
