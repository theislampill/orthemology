#!/usr/bin/env python3
"""Validate the typed DAEE semantic-operator contract (Task 6)."""

import copy
import io
import json
import os
import sys

import jsonschema
import yaml


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/daee-epistemics"
EXPECTED_OPERATORS = {
    "route-pressure", "event-transition", "field-divergence", "field-curl",
    "loop-break", "whole-state-reread", "runtime-closure",
}
EXPECTED_PREDICATES = {
    "admissible_corrective_transition", "locally_improving_transition",
    "transition_pathway_adequate", "reasoning_path_adequate_q",
    "token_truth_linked_q", "strictly_sound_reasoning_q",
}
REQUIRED_ROW_FIELDS = {
    "semantic_operator_id", "display_name", "symbol", "inputs", "outputs",
    "target_field", "preconditions", "semantic_kind", "claim_role", "owner_binding",
    "sources", "correctness_relation", "pathway_relation", "non_claims",
}


def read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def issue_codes(contract):
    """Return deterministic semantic issue codes without fixture-string matching."""
    issues = []
    if not isinstance(contract, dict):
        return ["malformed-contract-root"]

    declared_types = contract.get("type_registry", [])
    if not isinstance(declared_types, list) or not all(
            isinstance(value, str) and value for value in declared_types):
        issues.append("malformed-type-registry")
        declared_types = []
    declared_types = set(declared_types)

    owner_rows = contract.get("owner_registry", [])
    if not isinstance(owner_rows, list):
        issues.append("malformed-owner-registry")
        owner_rows = []
    declared_owners = set()
    owner_ids = set()
    for owner in owner_rows:
        if not isinstance(owner, dict):
            issues.append("malformed-owner-registry")
            continue
        binding = (owner.get("owner_kind"), owner.get("owner_id"), owner.get("source_ref"))
        if not all(isinstance(value, str) and value for value in binding):
            issues.append("malformed-owner-registry")
            continue
        declared_owners.add(binding)
        owner_ids.add(owner["owner_id"])
    if len(declared_owners) != len(owner_rows):
        issues.append("duplicate-owner-binding")

    rows = contract.get("operator_contracts", [])
    if not isinstance(rows, list):
        issues.append("malformed-operator-registry")
        rows = []
    ids = [r.get("semantic_operator_id") for r in rows if isinstance(r, dict)]
    if set(ids) != EXPECTED_OPERATORS or len(ids) != len(EXPECTED_OPERATORS):
        issues.append("operator-registry-incomplete")
    for row in rows:
        if not isinstance(row, dict):
            issues.append("malformed-operator-row")
            continue
        if not REQUIRED_ROW_FIELDS.issubset(row):
            issues.append("operator-row-incomplete")
            continue
        for field in ("inputs", "outputs"):
            values = row.get(field)
            if not isinstance(values, list) or not all(
                    isinstance(value, str) and value for value in values):
                issues.append("malformed-operator-types")
            elif any(value not in declared_types for value in values):
                issues.append("unresolved-operator-type")
        owner = row.get("owner_binding")
        if not isinstance(owner, dict):
            issues.append("malformed-owner-binding")
        elif (owner.get("owner_kind"), owner.get("owner_id"), owner.get("source_ref")) \
                not in declared_owners:
            issues.append("unresolved-owner-binding")
        target = row.get("target_field", {})
        if not isinstance(target, dict):
            issues.append("malformed-target-field")
            target = {}
        if row.get("semantic_operator_id") in {"field-divergence", "field-curl"}:
            node_types = target.get("node_types")
            if target.get("field_kind") != "typed-multi-node-field" \
                    or not isinstance(node_types, list) or len(node_types) < 2:
                issues.append("untyped-field-target")
        if row.get("semantic_kind") == "differentiable-gradient":
            issues.append("literal-differentiable-gradient")
        if row.get("correctness_relation", {}).get("entails_result_correctness") is not False:
            issues.append("transition-as-correctness")
        forbidden = row.get("non_claims", {})
        if any(forbidden.get(k) is not False for k in
               ("entails_human_uptake", "entails_human_restoration", "entails_soul_access")):
            issues.append("operator-nonclaim-missing")

    predicates = contract.get("predicate_registry", [])
    if not isinstance(predicates, list):
        issues.append("malformed-predicate-registry")
        predicates = []
    predicate_rows = [p for p in predicates if isinstance(p, dict)]
    if len(predicate_rows) != len(predicates):
        issues.append("malformed-predicate-registry")
    canonical_ids = [p.get("canonical_id") for p in predicate_rows]
    symbols = [p.get("normative_symbol") for p in predicate_rows]
    if set(canonical_ids) != EXPECTED_PREDICATES or len(canonical_ids) != len(EXPECTED_PREDICATES):
        issues.append("predicate-registry-incomplete")
    if len(canonical_ids) != len(set(canonical_ids)) or len(symbols) != len(set(symbols)):
        issues.append("duplicate-normative-predicate")
    predicate_ids = set(canonical_ids)
    for predicate in predicate_rows:
        requires = predicate.get("requires")
        if not isinstance(requires, list) or not all(
                isinstance(value, str) and value for value in requires):
            issues.append("malformed-predicate-relation")
        elif any(value not in predicate_ids for value in requires):
            issues.append("unresolved-predicate-relation")
    reason = [p for p in predicate_rows if p.get("canonical_id") == "reasoning_path_adequate_q"]
    if len(reason) != 1 or reason[0].get("normative_symbol") != "ReasoningPathAdequate_q(e)" \
            or reason[0].get("computation") != "decision-0011-required-reason-projection" \
            or reason[0].get("requires") != [] or "alias_of" in reason[0]:
        issues.append("predicate-semantics-changed")
    strict = [p for p in predicate_rows if p.get("canonical_id") == "strictly_sound_reasoning_q"]
    if len(strict) != 1 or strict[0].get("requires") != ["reasoning_path_adequate_q", "token_truth_linked_q"]:
        issues.append("strict-soundness-substitution")
    if "ClaimRelevantReasoningPathAdequate" in canonical_ids:
        issues.append("duplicate-normative-predicate")
    for row in rows:
        if not isinstance(row, dict):
            continue
        relation = row.get("pathway_relation")
        if not isinstance(relation, dict):
            issues.append("malformed-pathway-relation")
            continue
        canonical = relation.get("canonical_predicate")
        if canonical not in predicate_ids:
            issues.append("unresolved-predicate-relation")
        if canonical == "strictly_sound_reasoning_q":
            issues.append("operator-supplies-strict-soundness")
        if canonical == "reasoning_path_adequate_q":
            issues.append("operator-substitutes-claim-relative-predicate")

    aliases = contract.get("owner_aliases", [])
    if not isinstance(aliases, list):
        issues.append("malformed-owner-alias")
        aliases = []
    for alias in aliases:
        if not isinstance(alias, dict) or alias.get("canonical_owner") not in owner_ids:
            issues.append("unresolved-owner-alias")
    statuses = contract.get("predicate_alias_statuses")
    if statuses:
        issues.append("duplicate-alias-status")
        if len(set(statuses.values())) > 1:
            issues.append("predicate-alias-divergence")

    governance = contract.get("governance", {})
    if governance.get("whole_state_reread_required_before_closure") is not True:
        issues.append("whole-state-reread-omitted")
    if governance.get("burden_retention") != "address-or-carry-forward-with-provenance":
        issues.append("hidden-burden-deletion")
    if governance.get("global_revision_requires_explicit_authorization") is not True:
        issues.append("unauthorized-global-revision")
    if governance.get("runtime_closure_entails_human_restoration") is not False:
        issues.append("closure-as-uptake-restoration")
    if governance.get("admissibility_entails_strict_soundness") is not False:
        issues.append("admissibility-as-strict-soundness")
    return sorted(set(issues))


def validate_contract(contract):
    schema = json.loads(read(APP + "/SEMANTIC-OPERATOR-CONTRACT.schema.json"))
    errors = ["schema-invalid"] if list(jsonschema.Draft7Validator(schema).iter_errors(contract)) else []
    return sorted(set(errors + issue_codes(contract)))


def contract_for_case(base, case):
    doc = copy.deepcopy(base)
    mutation = case.get("mutation")
    by_id = {r["semantic_operator_id"]: r for r in doc["operator_contracts"]}
    if mutation == "literal-differentiable-gradient":
        by_id["route-pressure"]["semantic_kind"] = "differentiable-gradient"
    elif mutation == "untyped-field-target":
        by_id[case.get("operator", "field-divergence")]["target_field"] = {
            "field_kind": "scalar", "node_types": ["burden-node"]}
    elif mutation == "transition-as-correctness":
        by_id["event-transition"]["correctness_relation"]["entails_result_correctness"] = True
    elif mutation == "whole-state-reread-omitted":
        doc["governance"]["whole_state_reread_required_before_closure"] = False
    elif mutation == "closure-as-uptake-restoration":
        doc["governance"]["runtime_closure_entails_human_restoration"] = True
    elif mutation == "hidden-burden-deletion":
        doc["governance"]["burden_retention"] = "delete-on-closure"
    elif mutation == "unauthorized-global-revision":
        doc["governance"]["global_revision_requires_explicit_authorization"] = False
    elif mutation == "admissibility-as-strict-soundness":
        doc["governance"]["admissibility_entails_strict_soundness"] = True
    return doc


def main():
    contract = yaml.safe_load(read(APP + "/SEMANTIC-OPERATOR-CONTRACT.yaml"))
    fixtures = yaml.safe_load(read(APP + "/SEMANTIC-OPERATOR-FIXTURES.yaml"))["fixtures"]
    failures = []
    base_issues = validate_contract(contract)
    print("[%s] base semantic operator contract" % ("PASS" if not base_issues else "FAIL"))
    failures.extend(base_issues)
    for case in fixtures:
        issues = issue_codes(contract_for_case(contract, case))
        ok = (not issues) == case["expected_valid"]
        if not case["expected_valid"]:
            ok = ok and case["violates"] in issues
        print("[%s] %s" % ("PASS" if ok else "FAIL", case["id"]))
        if not ok:
            failures.append(case["id"])
    print("TOTAL: %d failures" % len(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
