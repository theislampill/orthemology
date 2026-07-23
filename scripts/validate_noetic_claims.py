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
CLAIM_ROLES = {
    "primary-text-verified", "secondary-reconstruction", "cross-source-synthesis",
    "orthemological-extension", "computational-analogy", "creed-internal-inference",
}
MENTAL_SOURCES = {"mental-conceivability", "universal-abstraction", "model-representation"}
EXTERNAL_CONCLUSIONS = {"external-possibility", "external-existence", "unseen-modality"}
ACCESS_STATUS_BY_REGISTRY_STATUS = {
    "PRIMARY_TEXT_EXACT": "primary-text-exact",
    "PRIMARY_WORK_THEME": "primary-work-theme",
    "PRIMARY_LOCUS_EDITION_DEPENDENT": "primary-locus-edition-dependent",
    "SECONDARY_VERIFIED": "secondary-verified",
    "SECONDARY_RECONSTRUCTION": "secondary-reconstruction",
    "COMPILATION_MEDIATED": "compilation-mediated",
    "INFERENCE_CROSS_SOURCE": "cross-source-inference",
    "ORTHEMOLOGICAL_EXTENSION": "orthemological-extension",
    "UNVERIFIED_REMOVE_OR_DOWNSCOPE": "unverified-held",
}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def resolve_target(claim, occ):
    if not isinstance(claim, dict) or not isinstance(occ, dict):
        return None
    bearer = claim.get("target_bearer")
    if not isinstance(bearer, str):
        return None
    o = occ.get(bearer)
    if not o:
        return None
    if o.get("identity") != claim.get("target_id"):
        return None
    if o.get("version") != claim.get("target_version"):
        return None
    return o


def _canonical_evidence_records():
    """Load the authoritative evidence records with bounded failure."""
    try:
        registry = json.loads(read(APP + "/NOETIC-EVIDENCE-REGISTRY.example.json"))
    except (OSError, ValueError, TypeError):
        return {}
    records = registry.get("evidence") if isinstance(registry, dict) else None
    if not isinstance(records, list):
        return {}
    return {
        record.get("evidence_id"): record
        for record in records
        if isinstance(record, dict) and isinstance(record.get("evidence_id"), str)
    }


def _evidence_records(evidence_registry):
    """Normalize a typed registry or a legacy ID collection without inventing records."""
    if isinstance(evidence_registry, dict):
        return {
            evidence_id: record
            for evidence_id, record in evidence_registry.items()
            if isinstance(evidence_id, str) and isinstance(record, dict)
        }
    if isinstance(evidence_registry, (set, list, tuple)):
        if any(not isinstance(evidence_id, str) for evidence_id in evidence_registry):
            return {}
        canonical = _canonical_evidence_records()
        return {
            evidence_id: canonical[evidence_id]
            for evidence_id in evidence_registry
            if evidence_id in canonical
        }
    return {}


def claim_semantic_issues(claim, source_status_ids, evidence_registry=None):
    """Return bounded, general Task 7 semantic diagnostics for one claim."""
    if not isinstance(claim, dict):
        return ["claim-not-object"]
    issues = []
    claim_evidence = claim.get("evidence_ids")
    if (not isinstance(claim_evidence, list)
            or any(not isinstance(evidence_id, str) for evidence_id in claim_evidence)):
        issues.append("malformed-evidence-ids")
    role = claim.get("claim_role")
    if not isinstance(role, str) or role not in CLAIM_ROLES:
        issues.append("invalid-claim-role")
    refs = claim.get("source_status_refs")
    if isinstance(source_status_ids, dict):
        known_ids = {item for item in source_status_ids if isinstance(item, str)}
    elif isinstance(source_status_ids, (set, list, tuple)):
        known_ids = {item for item in source_status_ids if isinstance(item, str)}
    else:
        known_ids = set()
    if not isinstance(refs, list) or not refs or any(
            not isinstance(ref, str) or ref not in known_ids for ref in refs):
        issues.append("unresolved-source-status-ref")
    elif isinstance(source_status_ids, dict):
        resolved_access = {
            ACCESS_STATUS_BY_REGISTRY_STATUS.get(source_status_ids[ref]) for ref in refs
        }
        access_status = claim.get("evidence_access_status")
        if not isinstance(access_status, str) or resolved_access != {access_status}:
            issues.append("evidence-access-status-mismatch")
    if claim.get("comparison_scope") == "modern-comparison" and role == "primary-text-verified":
        issues.append("modern-comparison-not-primary")
    boundary = claim.get("inference_boundary")
    if boundary is not None:
        if not isinstance(boundary, dict):
            issues.append("malformed-inference-boundary")
        else:
            source = boundary.get("source_kind")
            conclusion = boundary.get("conclusion_kind")
            status = boundary.get("bridge_status")
            evidence = boundary.get("bridge_evidence_ids")
            if not isinstance(source, str):
                issues.append("malformed-inference-source-kind")
            if not isinstance(conclusion, str):
                issues.append("malformed-inference-conclusion-kind")
            if not isinstance(status, str):
                issues.append("malformed-inference-bridge-status")
            if conclusion is not None and conclusion != claim.get("target_type"):
                issues.append("inference-conclusion-target-mismatch")
            evidence_is_typed = (isinstance(evidence, list)
                                 and all(isinstance(item, str) for item in evidence))
            if isinstance(evidence, list) and not evidence_is_typed:
                issues.append("malformed-bridge-evidence-ids")
            records = _evidence_records(evidence_registry)
            if (evidence_is_typed and evidence_registry is not None
                    and any(item not in records for item in evidence)):
                issues.append("bridge-evidence-unresolved")
            if (isinstance(source, str) and isinstance(conclusion, str)
                    and source in MENTAL_SOURCES and conclusion in EXTERNAL_CONCLUSIONS):
                if status == "direct-entailment":
                    issues.append("mental-external-direct-entailment")
                if status == "independently-warranted" and (not isinstance(evidence, list) or not evidence):
                    issues.append("independent-bridge-without-evidence")
                elif status == "independently-warranted" and evidence_is_typed:
                    for evidence_id in evidence:
                        record = records.get(evidence_id) if isinstance(evidence_id, str) else None
                        roles = record.get("support_roles") if isinstance(record, dict) else None
                        targets = (record.get("supported_target_types")
                                   if isinstance(record, dict) else None)
                        if (not isinstance(record, dict)
                                or record.get("currentness") != "current"
                                or record.get("validity") != "valid"
                                or not isinstance(roles, list)
                                or any(not isinstance(role, str) for role in roles)
                                or "mental-external-bridge" not in roles
                                or not isinstance(targets, list)
                                or any(not isinstance(target, str) for target in targets)
                                or conclusion not in targets):
                            issues.append("bridge-evidence-not-authoritative")
                            break
                if status == "held" and claim.get("status") == "asserted":
                    issues.append("asserted-external-conclusion-without-warranted-bridge")
    return list(dict.fromkeys(issues))


def claim_supported(claim, evidence_registry, occ, source_status_ids=None):
    """Return (ok, rule_violated) under the R7D support discipline."""
    if source_status_ids is not None:
        semantic = claim_semantic_issues(claim, source_status_ids, evidence_registry)
        if semantic:
            return False, semantic[0]
    o = resolve_target(claim, occ)
    if o is None:
        return False, "target-unresolved"
    status = claim.get("status")
    ttype = claim.get("target_type")
    bearer = claim.get("target_bearer")
    if not isinstance(status, str):
        return False, "malformed-claim-status"
    if not isinstance(ttype, str):
        return False, "malformed-target-type"
    if not isinstance(bearer, str):
        return False, "malformed-target-bearer"
    if not o.get("in_scope", False) and status == "asserted":
        return False, "target-out-of-scope-asserted"
    if bearer == "m_discourse" and ttype in SUBJECT_INTERIOR:
        return False, "subject-type-on-discourse"
    evidence_ids = claim.get("evidence_ids")
    if (not isinstance(evidence_ids, list)
            or any(not isinstance(evidence_id, str) for evidence_id in evidence_ids)):
        return False, "malformed-evidence-ids"
    evidence_records = _evidence_records(evidence_registry)
    unresolved = [e for e in evidence_ids if e not in evidence_records]
    if unresolved:
        return False, "evidence-unresolved"
    n_ev = len(evidence_ids)
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
    source_registry = yaml.safe_load(read("references/source-status.yaml"))
    source_status_ids = {row["id"]: row["status"] for row in source_registry.get("claims", [])}

    # 1. schema validation
    for name, obj, sch in [("claim example", claim_ex, claim_schema),
                           ("evidence registry example", ev_reg, ev_schema)]:
        try:
            jsonschema.validate(obj, sch)
            check("%s validates against its schema" % name, True)
        except jsonschema.ValidationError as e:
            check("%s validates against its schema" % name, False, e.message)

    ev_records = {e["evidence_id"]: e for e in ev_reg["evidence"]}
    occ = tmap["occurrences"]

    # 2. every example claim is supported (and every evidence_id resolves)
    for c in claim_ex["claims"]:
        ok, rule = claim_supported(c, ev_records, occ, source_status_ids)
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
        try:
            jsonschema.validate({"schema": claim_ex["schema"], "claims": [f["claim"]]}, claim_schema)
            check("fixture %s is structurally typed" % f["id"], True)
        except jsonschema.ValidationError as e:
            check("fixture %s is structurally typed" % f["id"], False, e.message)
        ok, rule = claim_supported(f["claim"], ev_records, occ, source_status_ids)
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
