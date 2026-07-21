#!/usr/bin/env python3
"""Evidence-bound multi-target noetic-claim validator (R7D, Decision 0030, audit B10/B11).

Deterministic, offline. Closes the probe P2/P3 breach: the R7C noetic-target helper
accepted an ASSERTED subject-level claim with no evidence and no observation bridge as
long as a no-soul-access disclaimer was present — a disclaimer prevents an overclaim
but is not support. This gate binds each NoeticClaim to a resolvable, typed evidence
registry and a support rule:

  * the target must EXIST (bearer+identity+version resolve to the target map) and be
    in scope before it may be ASSERTED;
  * a subject-interior TYPE may never attach to the discourse token;
  * every evidence_id must resolve to the evidence registry — non-claims never count;
  * motive/culpability/soul-state is normally held/out-of-scope, never asserted;
  * an ASSERTED inferred subject-interior claim needs >=2 resolvable evidence ids and
    an observation bridge (thin evidence defaults to HELD/underdetermined); an overt
    AVOWED-COMMITMENT (public) may be asserted on its own wording;
  * any subject claim citing evidence must carry an observation bridge;
  * held/underdetermined subject profiles must keep live candidate alternatives.

Establishes no empirical or theological claim; asserts no soul access.
"""
import io
import json
import os
import sys

try:
    import yaml
    import jsonschema
except ImportError as e:
    print("FATAL: requires pyyaml + jsonschema:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/daee-epistemics"
FAILS = []

# subject-interior types (must never attach to the discourse token)
SUBJECT_INTERIOR = {"avowed-commitment", "reasoning-episode", "inferred-noetic-profile",
                    "faculty-disposition", "motive-culpability-soul-state"}
# inferred (non-overt) interior types subject to the thin-evidence rule
INFERRED_INTERIOR = {"reasoning-episode", "inferred-noetic-profile", "faculty-disposition"}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def resolve_target(claim, occ):
    o = occ.get(claim.get("target_bearer"))
    if not o:
        return None
    if o.get("identity") != claim.get("target_id"):
        return None
    if o.get("version") != claim.get("target_version"):
        return None
    return o


def claim_supported(claim, ev_ids, occ):
    """Return (ok, rule_violated) under the R7D support discipline."""
    o = resolve_target(claim, occ)
    if o is None:
        return False, "target-unresolved"
    status = claim.get("status")
    ttype = claim.get("target_type")
    bearer = claim.get("target_bearer")
    if not o.get("in_scope", False) and status == "asserted":
        return False, "target-out-of-scope-asserted"
    if bearer == "m_discourse" and ttype in SUBJECT_INTERIOR:
        return False, "subject-type-on-discourse"
    unresolved = [e for e in claim.get("evidence_ids", []) if e not in ev_ids]
    if unresolved:
        return False, "evidence-unresolved"
    n_ev = len(claim.get("evidence_ids", []))
    if ttype == "motive-culpability-soul-state" and status == "asserted":
        return False, "motive-asserted"
    # any m_subject claim citing evidence needs an observation bridge
    if bearer == "m_subject" and claim.get("evidence_ids") and not claim.get("bridges"):
        return False, "subject-no-bridge"
    # asserted INFERRED interior needs >=2 resolvable evidence ids (thin -> held)
    if bearer == "m_subject" and status == "asserted" and ttype in INFERRED_INTERIOR:
        if n_ev < 2:
            return False, "subject-asserted-thin"
    # general asserted discipline
    if status == "asserted":
        if n_ev < 1:
            return False, "asserted-no-evidence"
        if not str(claim.get("support_rule", "")).strip():
            return False, "asserted-no-rule"
        if claim.get("uncertainty", {}).get("level") == "underdetermined":
            return False, "asserted-underdetermined"
    # held/underdetermined inferred subject profiles keep live alternatives
    if bearer == "m_subject" and status in ("held", "underdetermined") and ttype in INFERRED_INTERIOR:
        if not claim.get("candidate_alternatives"):
            return False, "held-no-alternatives"
    return True, None


def main():
    claim_schema = json.loads(read(APP + "/NOETIC-CLAIM.schema.json"))
    claim_ex = json.loads(read(APP + "/NOETIC-CLAIM.example.json"))
    ev_schema = json.loads(read(APP + "/NOETIC-EVIDENCE-REGISTRY.schema.json"))
    ev_reg = json.loads(read(APP + "/NOETIC-EVIDENCE-REGISTRY.example.json"))
    tmap = json.loads(read(APP + "/NOETIC-TARGET-MAP.example.json"))

    # 1. schema validation
    for name, obj, sch in [("claim example", claim_ex, claim_schema),
                           ("evidence registry example", ev_reg, ev_schema)]:
        try:
            jsonschema.validate(obj, sch)
            check("%s validates against its schema" % name, True)
        except jsonschema.ValidationError as e:
            check("%s validates against its schema" % name, False, e.message)

    ev_ids = {e["evidence_id"] for e in ev_reg["evidence"]}
    occ = tmap["occurrences"]

    # 2. every example claim is supported (and every evidence_id resolves)
    for c in claim_ex["claims"]:
        ok, rule = claim_supported(c, ev_ids, occ)
        check("example claim %s is evidence-supported" % c["claim_id"], ok, "violates %s" % rule)

    # 2b. evidence-relation records never assert direct interior access
    for e in ev_reg["evidence"]:
        rel = e["relation_to_target"].lower()
        check("evidence %s does not assert direct interior access" % e["evidence_id"],
              "direct interior access" not in rel and "reads the soul" not in rel)

    # 3. fixtures NC1..NC10 match expected validity
    fx = yaml.safe_load(read(APP + "/NOETIC-CLAIM-FIXTURES.yaml"))
    ids = {f["id"] for f in fx["fixtures"]}
    check("all ten claim fixtures present", ids == {"NC%d" % i for i in range(1, 11)}, str(sorted(ids)))
    for f in fx["fixtures"]:
        ok, rule = claim_supported(f["claim"], ev_ids, occ)
        exp = f["expected_valid"]
        check("fixture %s (%s) validity == %s" % (f["id"], f["distinction"][:34], exp),
              ok == exp, "got valid=%s (rule %s)" % (ok, rule))
        if not exp and "violates" in f:
            check("fixture %s violates declared rule %s" % (f["id"], f["violates"]),
                  rule == f["violates"], "got %s" % rule)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
