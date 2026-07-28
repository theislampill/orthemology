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
HISTORICAL_V1_PATH = APP + "/CORRECTIVE-TRANSITION.v1.example.json"
HISTORICAL_V1_DIGEST = "9b19572d7e1e43ed513a910811b21cbd49f9ab8c58a4626ea5347f1175216d5e"


def read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def read_bytes(rel):
    with io.open(os.path.join(ROOT, rel), "rb") as handle:
        return handle.read()


def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def transition_ok(t):
    if not isinstance(t, dict):
        return False, "malformed-transition"
    if t.get("selected_route") not in (t.get("eligible_routes") or []):
        return False, "route-not-admissible"
    if not str(t.get("ranking_witness", "")).strip():
        return False, "no-ranking-witness"
    verdicts = t.get("verdicts")
    if not isinstance(verdicts, dict):
        return False, "malformed-verdicts"
    if verdicts.get("strictly_sound") is True:
        return False, "delta-as-soundness"
    reread = t.get("reread")
    if not isinstance(reread, dict):
        return False, "malformed-reread"
    if t.get("terminal_posture") == "CLOSURE" and not reread.get("performed"):
        return False, "reread-omitted"
    if verdicts.get("runtime_closure") and verdicts.get("human_uptake") == "observed":
        return False, "closure-as-restoration"
    if "burden_accounting" in t:
        accounting = t.get("burden_accounting")
        live = t.get("live_burdens")
        if not isinstance(accounting, dict) or not isinstance(live, list):
            return False, "malformed-burden-accounting"
        addressed = accounting.get("addressed")
        carried = accounting.get("carried_forward")
        if not isinstance(addressed, list) or not isinstance(carried, list):
            return False, "malformed-burden-accounting"
        if not all(isinstance(value, str) for value in live + addressed + carried):
            return False, "malformed-burden-accounting"
        addressed_set = set(addressed)
        carried_set = set(carried)
        if addressed_set & carried_set or addressed_set | carried_set != set(live):
            return False, "burden-deletion"
    revision = t.get("global_revision")
    if revision is not None:
        if not isinstance(revision, dict):
            return False, "malformed-global-revision"
        requested = revision.get("requested")
        authorized = revision.get("authorized")
        reference = revision.get("authorization_ref")
        has_reference = isinstance(reference, str) and bool(reference.strip())
        if not isinstance(requested, bool) or not isinstance(authorized, bool):
            return False, "malformed-global-revision"
        if authorized != has_reference or authorized and not requested \
                or requested and not authorized:
            return False, "unauthorized-global-revision"
    if verdicts.get("runtime_closure") is not (t.get("terminal_posture") == "CLOSURE"):
        return False, "runtime-closure-posture-conflict"
    return True, None


def document_ok(doc):
    if not isinstance(doc, dict):
        return False, "malformed-document-root"
    version = doc.get("schema")
    if version is None:
        return False, "missing-version"
    if version not in {V1, V2}:
        return False, "unknown-version"
    transitions = doc.get("transitions")
    if version == V1 and isinstance(transitions, list) and any(
            isinstance(t, dict) and V2_ONLY & set(t) for t in transitions):
        return False, "v1-claims-v2-guarantee"
    schema = json.loads(read(APP + "/CORRECTIVE-TRANSITION.schema.json"))
    errors = list(jsonschema.Draft7Validator(schema).iter_errors(doc))
    if errors:
        return False, "v1-schema-invalid" if version == V1 else "v2-schema-invalid"
    if version == V1:
        source_bytes = read_bytes(HISTORICAL_V1_PATH)
        if hashlib.sha256(source_bytes).hexdigest() != HISTORICAL_V1_DIGEST:
            return False, "historical-v1-byte-drift"
        if doc != json.loads(source_bytes.decode("utf-8")):
            return False, "historical-v1-content-drift"
    migration = doc.get("migration")
    if migration:
        source_bytes = read_bytes(HISTORICAL_V1_PATH)
        source = json.loads(source_bytes.decode("utf-8"))
        source_transition = source["transitions"][0]
        expected_direct = sorted(source_transition)
        expected_new = sorted(V2_ONLY)
        core = copy.deepcopy(doc)
        core.pop("migration", None)
        if migration.get("resulting_v2_digest") != hashlib.sha256(canonical_bytes(core)).hexdigest():
            return False, "migration-result-digest-mismatch"
        if migration.get("original_content_digest") != hashlib.sha256(source_bytes).hexdigest():
            return False, "migration-source-digest-mismatch"
        if migration.get("original_record_identity") != source_transition["transition_id"]:
            return False, "migration-identity-mismatch"
        if migration.get("fields_mapped_directly") != expected_direct \
                or migration.get("fields_newly_supplied") != expected_new \
                or migration.get("fields_unavailable_or_held") != []:
            return False, "migration-field-ledger-mismatch"
        if not str(migration.get("migration_time", "")).strip() \
                or not str(migration.get("provenance", "")).strip():
            return False, "migration-provenance-missing"
        if len(doc["transitions"]) != 1 or any(
                doc["transitions"][0].get(field) != source_transition[field]
                for field in expected_direct):
            return False, "migration-direct-field-mismatch"
    for t in doc.get("transitions", []):
        ok, reason = transition_ok(t)
        if not ok:
            return False, reason
    return True, None


def historical_v1_control():
    return json.loads(read_bytes(HISTORICAL_V1_PATH).decode("utf-8"))


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
    if not isinstance(supplied, dict) or set(supplied) != V2_ONLY:
        raise ValueError("migration supplied fields must be exactly the v2 additions")
    source_bytes = read_bytes(HISTORICAL_V1_PATH)
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
        "fields_mapped_directly": sorted(v1["transitions"][0]),
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
