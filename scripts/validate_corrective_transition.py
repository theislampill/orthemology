#!/usr/bin/env python3
"""Validate explicit historical v1 and current v2 corrective transitions."""

import copy
import hashlib
import io
import json
import os
import sys

import jsonschema
import yaml


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/daee-epistemics"
V1 = "orthemology-corrective-transition-v1"
V2 = "orthemology-corrective-transition-v2"
V2_ONLY = {"operator_trace", "burden_accounting", "global_revision"}
HISTORICAL_V1_DIGEST = "dcaa4128efac7b80c696aad6c7cf8e0c1202a77a35cd7fabfe18000948bc0c3a"


def read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def transition_ok(t):
    if t.get("selected_route") not in (t.get("eligible_routes") or []):
        return False, "route-not-admissible"
    if not str(t.get("ranking_witness", "")).strip():
        return False, "no-ranking-witness"
    if t.get("verdicts", {}).get("strictly_sound") is True:
        return False, "delta-as-soundness"
    if t.get("terminal_posture") == "CLOSURE" and not t.get("reread", {}).get("performed"):
        return False, "reread-omitted"
    if t.get("verdicts", {}).get("runtime_closure") and t.get("verdicts", {}).get("human_uptake") == "observed":
        return False, "closure-as-restoration"
    if "burden_accounting" in t:
        accounted = set(t["burden_accounting"].get("addressed", [])) | set(t["burden_accounting"].get("carried_forward", []))
        if accounted != set(t.get("live_burdens", [])):
            return False, "burden-deletion"
    revision = t.get("global_revision")
    if revision and revision.get("requested") and (not revision.get("authorized") or not revision.get("authorization_ref")):
        return False, "unauthorized-global-revision"
    return True, None


def document_ok(doc):
    version = doc.get("schema")
    if version is None:
        return False, "missing-version"
    if version not in {V1, V2}:
        return False, "unknown-version"
    if version == V1 and any(V2_ONLY & set(t) for t in doc.get("transitions", [])):
        return False, "v1-claims-v2-guarantee"
    if version == V1 and hashlib.sha256(canonical_bytes(doc)).hexdigest() != HISTORICAL_V1_DIGEST:
        return False, "historical-v1-byte-drift"
    schema = json.loads(read(APP + "/CORRECTIVE-TRANSITION.schema.json"))
    errors = list(jsonschema.Draft7Validator(schema).iter_errors(doc))
    if errors:
        return False, "v1-schema-invalid" if version == V1 else "v2-schema-invalid"
    migration = doc.get("migration")
    if migration:
        core = copy.deepcopy(doc)
        core.pop("migration", None)
        if migration.get("resulting_v2_digest") != hashlib.sha256(canonical_bytes(core)).hexdigest():
            return False, "migration-result-digest-mismatch"
        if not doc.get("transitions") or migration.get("original_record_identity") != doc["transitions"][0].get("transition_id"):
            return False, "migration-identity-mismatch"
    for t in doc.get("transitions", []):
        ok, reason = transition_ok(t)
        if not ok:
            return False, reason
    return True, None


def historical_v1_control():
    fixtures = yaml.safe_load(read(APP + "/CORRECTIVE-TRANSITION-FIXTURES.yaml"))
    return copy.deepcopy(fixtures["historical_v1_record"])


def v2_migration_supplied_fields():
    return {
        "operator_trace": ["route-pressure", "event-transition", "whole-state-reread"],
        "burden_accounting": {"addressed": ["criterion-import defect"], "carried_forward": ["residual source-independence dependency"]},
        "global_revision": {"requested": False, "authorized": False, "authorization_ref": None},
    }


def migrate_v1_to_v2(v1, supplied):
    ok, reason = document_ok(v1)
    if not ok:
        raise ValueError("source v1 invalid: %s" % reason)
    source_bytes = canonical_bytes(v1)
    result = copy.deepcopy(v1)
    result.pop("compatibility_status", None)
    result["schema"] = V2
    for t in result["transitions"]:
        for key, value in supplied.items():
            t[key] = copy.deepcopy(value)
    core_digest = hashlib.sha256(canonical_bytes(result)).hexdigest()
    result["migration"] = {
        "original_record_identity": result["transitions"][0]["transition_id"],
        "original_content_digest": hashlib.sha256(source_bytes).hexdigest(),
        "source_contract": V1,
        "migration_operation": "explicit-v1-to-v2-copy",
        "migration_version": "orthemology-corrective-transition-migration-v1",
        "migration_time": "2026-07-22T00:00:00Z",
        "provenance": "deterministic repository migration; historical v1 input preserved",
        "fields_mapped_directly": sorted(k for k in v1["transitions"][0] if k not in V2_ONLY),
        "fields_newly_supplied": sorted(supplied),
        "fields_unavailable_or_held": [],
        "resulting_v2_digest": core_digest,
    }
    return result


def main():
    failures = []
    example = json.loads(read(APP + "/CORRECTIVE-TRANSITION.example.json"))
    ok, reason = document_ok(example)
    print("[%s] current v2 example%s" % ("PASS" if ok else "FAIL", "" if ok else ": " + str(reason)))
    if not ok: failures.append("example")
    historical = historical_v1_control()
    ok, reason = document_ok(historical)
    print("[%s] explicit historical v1 branch" % ("PASS" if ok else "FAIL"))
    if not ok: failures.append("historical-v1")
    fixtures = yaml.safe_load(read(APP + "/CORRECTIVE-TRANSITION-FIXTURES.yaml"))["fixtures"]
    ids = {f["id"] for f in fixtures}
    if not {"CT%d" % i for i in range(1, 9)}.issubset(ids): failures.append("CT1-CT8")
    for fixture in fixtures:
        valid, violated = transition_ok(fixture["transition"])
        passed = valid == fixture["expected_valid"]
        if not fixture["expected_valid"]:
            passed = passed and violated == fixture["violates"]
        print("[%s] %s" % ("PASS" if passed else "FAIL", fixture["id"]))
        if not passed: failures.append(fixture["id"])
    print("TOTAL: %d failures" % len(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
