#!/usr/bin/env python3
"""Multi-target noetic-orthing validator (R7C, Decision 0027).

Deterministic, offline. Enforces that a DAEE episode distinguishes the discourse,
subject, runtime, response, and uptake occurrences, and that every noetic claim
names its proper target — so a subject-level (interior) placement is never
attached to the discourse token merely because the token is observed (audit B9).

  1. NOETIC-TARGET-MAP.example.json validates against NOETIC-TARGET-MAP.schema.json;
  2. the example separates the five bearers and keeps m_subject inferential
     (observed: false), with no-soul-access non-claims on every subject claim;
  3. the fixtures NT1..NT10 each match their expected validity under:
       R1 a claim targeting m_discourse must NOT assert a subject-interior type;
       R2 a subject-target claim is held/underdetermined, or (if asserted) claims
          no direct/unique interior access, and carries a no-soul-access non-claim;
       R3 every claim carries at least one non-claim.

Establishes no empirical or theological claim; asserts no soul access.
"""
import io
import json
import os
import re
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
# subject-interior type markers that must never be asserted OF the discourse token
INTERIOR = re.compile(r"noetic-state|soul|interior|deformation|motive|culpab", re.I)
NO_ACCESS = re.compile(r"no soul access|not.*soul|no.*interior access|no.*direct.*access", re.I)
DIRECT_UNIQUE = re.compile(r"\b(direct|unique|uniquely|certain|settled)\b", re.I)


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    return io.open(os.path.join(ROOT, rel), encoding="utf-8").read()


def claim_valid(target, target_type, status, evidence_scope, non_claims):
    """Return (ok, rule_violated) under R1/R2/R3."""
    nc = " ".join(non_claims or []).lower()
    # R1: no subject-interior type asserted of the discourse token (checked first)
    if target == "m_discourse" and INTERIOR.search(target_type or ""):
        return False, "R1"
    # R2: subject-target discipline
    if target == "m_subject":
        if status == "asserted" and DIRECT_UNIQUE.search(evidence_scope or ""):
            return False, "R2"
        if not NO_ACCESS.search(nc):
            return False, "R2"
    # R3: every claim carries at least one substantive non-claim
    if not non_claims or non_claims == ["none stated"] or non_claims == ["none"]:
        return False, "R3"
    return True, None


def main():
    schema = json.loads(read(APP + "/NOETIC-TARGET-MAP.schema.json"))
    example = json.loads(read(APP + "/NOETIC-TARGET-MAP.example.json"))

    # 1. schema validation
    try:
        jsonschema.validate(example, schema)
        check("example validates against the noetic-target-map schema", True)
    except jsonschema.ValidationError as e:
        check("example validates against the noetic-target-map schema", False, e.message)

    # 2. example semantics
    occ = example["occurrences"]
    check("example distinguishes all five bearers",
          set(occ) == {"m_discourse", "m_subject", "m_runtime", "m_response", "m_uptake"},
          str(sorted(occ)))
    check("m_subject is inferential (observed: false)", occ["m_subject"].get("observed") is False)
    for c in example["claims"]:
        ok, rule = claim_valid(c["target"], c["target_type"], c["status"],
                               c["evidence_scope"], c["non_claims"])
        check("example claim %s obeys the target rules" % c["claim_id"], ok, "violates %s" % rule)
    check("example declares the no-soul-access invariant",
          bool(example.get("non_soul_access_invariant")))
    # observation bridge never establishes truth
    for b in example.get("observation_bridge", []):
        check("observation bridge %s does not establish truth" % b["evidence_id"],
              b.get("establishes_truth") is False)

    # 3. fixtures NT1..NT10 match expected validity
    fx = yaml.safe_load(read(APP + "/NOETIC-TARGET-FIXTURES.yaml"))["fixtures"]
    want = {"NT%d" % i for i in range(1, 11)}
    check("all ten target fixtures present", {f["id"] for f in fx} == want)
    for f in fx:
        ok, rule = claim_valid(f["target"], f["target_type"], f["status"],
                               f["evidence_scope"], f["non_claims"])
        expected = f["expected_valid"]
        check("fixture %s (%s) validity == %s" % (f["id"], f["distinction"][:34], expected),
              ok == expected, "got valid=%s (rule %s); expected %s" % (ok, rule, expected))
        if not expected and "violates" in f:
            check("fixture %s violates the declared rule %s" % (f["id"], f["violates"]),
                  rule == f["violates"], "got %s" % rule)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
