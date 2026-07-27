#!/usr/bin/env python3
"""Concrete Task 14 control/mutation adapters for production validators.

This module never assigns an outcome from the requested role.  Each adapter
constructs one explicit input, invokes the declared validator or semantic API,
and derives the outcome only from that returned result.
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _cli_result(inputs: Any, code: int, output: str) -> dict:
    if code == 0:
        outcome = "accepted"
    elif code == 1:
        outcome = "rejected"
    else:
        raise RuntimeError("production validator failed with rc=%d: %s" % (code, output))
    return {"outcome": outcome, "input_sha256": _digest(inputs)}


def _api_result(inputs: Any, issues: Any) -> dict:
    if not isinstance(issues, (list, tuple)):
        raise RuntimeError("production semantic owner returned a non-list issue result")
    return {
        "outcome": "accepted" if not issues else "rejected",
        "input_sha256": _digest(inputs),
    }


def _candidate_state(variant_id: str, role: str) -> dict:
    from tests import test_candidate_state as source

    case = source.CandidateStateTests()
    case.setUp()
    data = copy.deepcopy(case.data)
    if role == "mutation":
        if variant_id == "R7E-T14-A01-V01":
            data["pull_requests"] = [
                row for row in data["pull_requests"] if row["pr"] != 11
            ]
        elif variant_id == "R7E-T14-A01-V02":
            data["observed_at_utc"] = "2026-07-21T18:10:21Z"
        elif variant_id == "R7E-T14-A02-V01":
            decisions = copy.deepcopy(case.decisions)
            decisions["0034"]["status"] = "adopted-merged"
            return _api_result(
                {"data": data, "decisions": decisions},
                source.collect_issues(data, decisions),
            )
        else:
            raise KeyError(variant_id)
    return _api_result(
        {"data": data, "decisions": case.decisions},
        source.collect_issues(data, case.decisions),
    )


def _semantic_operator(variant_id: str, role: str) -> dict:
    from tests import test_semantic_operator_contract as source

    source.SemanticOperatorContractTests.setUpClass()
    contract = copy.deepcopy(source.SemanticOperatorContractTests.contract)
    if role == "control":
        return _api_result(contract, source.semantic.validate_contract(contract))
    fixture_ids = {
        "R7E-T14-A03-V01": "SO-01",
        "R7E-T14-A04-V01": "SO-02",
        "R7E-T14-A04-V02": "SO-03",
        "R7E-T14-A05-V01": "SO-04",
        "R7E-T14-A06-V01": "SO-05",
        "R7E-T14-A07-V01": "SO-06",
        "R7E-T14-A08-V01": "SO-07",
        "R7E-T14-A09-V01": "SO-08",
        "R7E-T14-A10-V01": "SO-09",
    }
    fixture = next(
        row
        for row in source.SemanticOperatorContractTests.fixtures["fixtures"]
        if row["id"] == fixture_ids[variant_id]
    )
    mutated = source.semantic.contract_for_case(contract, fixture)
    return _api_result(mutated, source.semantic.issue_codes(mutated))


def _task7(variant_id: str, role: str) -> dict:
    from tests import test_task7_epistemology_semantics as source

    if variant_id.startswith("R7E-T14-A11-"):
        document = source.valid_warrant()
        if role == "mutation":
            field = {
                "R7E-T14-A11-V01": "witness_count",
                "R7E-T14-A11-V02": "popularity",
            }[variant_id]
            document["assessments"][0][field] = 100
        return _api_result(
            document, source.MEMETIC.validate_tawatur_document(document, {"ELT-3"})
        )
    if variant_id.startswith("R7E-T14-A12-"):
        case = source.FitrahBoundaryTests()
        document = case.boundary()
        if role == "mutation":
            if variant_id == "R7E-T14-A12-V01":
                document["field_coordinate"] = [0.2, 0.8]
            elif variant_id == "R7E-T14-A12-V02":
                document["model_properties"].append("quantitative")
        return _api_result(document, source.META.validate_fitrah_boundary(document))
    if variant_id == "R7E-T14-A13-V01":
        case = source.ClaimRoleAndMentalBoundaryTests()
        document, occurrences, statuses = case.external_claim_context()
        if role == "mutation":
            document["inference_boundary"] = {
                "source_kind": "mental-conceivability",
                "conclusion_kind": "external-possibility",
                "bridge_status": "direct-entailment",
                "bridge_evidence_ids": [],
            }
        result = source.NOETIC.claim_supported(
            document, case.evidence_records(), occurrences, statuses
        )
        return {
            "outcome": "accepted" if result[0] else "rejected",
            "input_sha256": _digest(
                {
                    "claim": document,
                    "occurrences": occurrences,
                    "source_statuses": statuses,
                }
            ),
        }
    raise KeyError(variant_id)


def _dynamic_orthing(variant_id: str, role: str) -> dict:
    from tests import test_osm_claim_boundaries as source

    document = source.valid_mapping()
    if role == "mutation":
        if variant_id == "R7E-T14-A14-V01":
            document["objects"][6]["id"] = "biological_single_cell_response"
        elif variant_id == "R7E-T14-A14-V02":
            document["objects"][5]["id"] = "biological_single_cell_response"
        elif variant_id == "R7E-T14-A14-V03":
            document["relations"][5]["object"] = "world_task_state"
        elif variant_id == "R7E-T14-A14-V04":
            document["asserted_identities"] = [
                ["latent_posterior", "inferred_orthemic_profile"]
            ]
        elif variant_id == "R7E-T14-A14-V05":
            document["asserted_identities"] = [
                ["model_parameter_state", "model_representation_output"]
            ]
        else:
            raise KeyError(variant_id)
    return _api_result(document, source.issues_for(document))


def _argument_map(variant_id: str, role: str) -> dict:
    from tests import test_argument_map_semantics as source

    source.ArgumentMapSemanticsTests.setUpClass()
    document = copy.deepcopy(source.ArgumentMapSemanticsTests.model)
    if role == "mutation":
        if variant_id == "R7E-T14-A15-V01":
            document["nodes"][8]["conclusion"]["text"] = (
                "the OSM result validates the metaphysical and theological conclusion"
            )
        elif variant_id == "R7E-T14-A16-V01":
            document["speech_bearers"][5]["created_status"] = "created"
        elif variant_id == "R7E-T14-A16-V02":
            document["speech_bearers"][1]["created_status"] = "uncreated"
        else:
            raise KeyError(variant_id)
    issues = source.validator.validate_mapping(
        document, source.ArgumentMapSemanticsTests.registry
    )
    return _api_result(document, issues)


def _witness(variant_id: str, role: str) -> dict:
    from tests import test_r7e_llm_witness as source

    witness, crosswalk, narrative = source.bounded_control()
    if role == "mutation":
        if variant_id == "R7E-T14-A17-V01":
            witness["claim_boundaries"]["correctness"] = "established"
        elif variant_id == "R7E-T14-A17-V02":
            next(
                row
                for row in witness["witness_objects"]
                if row["object_kind"] == "case-bound-applications"
            )["description"] = "The original system is deployed and correct."
        elif variant_id == "R7E-T14-A17-V03":
            next(
                row
                for row in witness["witness_objects"]
                if row["object_kind"] == "executor-subagent-roles"
            )["evidence_refs"] = ["E-WORKFLOW-JOURNAL"]
        elif variant_id.startswith("R7E-T14-A49-"):
            field = {
                "R7E-T14-A49-V01": "full_somnus_writeback_chain",
                "R7E-T14-A49-V02": "nightly_autonomy",
                "R7E-T14-A49-V03": "runtime_deployment",
            }[variant_id]
            witness["claim_boundaries"][field] = "implemented"
        else:
            raise KeyError(variant_id)
    code, output = source.production_exit(witness, crosswalk, narrative)
    return _cli_result(
        {"witness": witness, "crosswalk": crosswalk, "narrative": narrative},
        code,
        output,
    )


def _math_source(variant_id: str, role: str) -> dict:
    from tests import test_math_source_inventory as source

    if variant_id != "R7E-T14-A18-V01":
        raise KeyError(variant_id)
    status = source.APPROVED_DIAGNOSTIC_TEXT
    if role == "mutation":
        status = "μ̄_3: wrong\n  claim scope; μ̄_2: stale calibration"
    inventory, source_texts = source.diagnostic_inventory(status=status)
    return _api_result(
        {"inventory": inventory, "source_texts": source_texts},
        source.inventory_issues(inventory, source_texts),
    )


def _somnic(variant_id: str, role: str) -> dict:
    from tests import test_somnic_orthing as source

    case = source.SomnicOrthingTests()
    case.setUp()
    activation = copy.deepcopy(case.activation)
    records = copy.deepcopy(case.records)
    history = copy.deepcopy(case.history)
    inventory = copy.deepcopy(case.inventory)
    adoption = copy.deepcopy(case.adoption)
    collective = copy.deepcopy(case.collective)
    decision = source.DECISION.read_text(encoding="utf-8")
    if role == "mutation":
        _mutate_somnic(
            variant_id, source, activation, records, inventory, adoption, collective
        )
    inputs = {
        "activation": activation,
        "records": records,
        "history": history,
        "inventory": inventory,
        "adoption": adoption,
        "collective": collective,
        "decision": decision,
    }
    code, output = source.production_exit(
        activation, records, inventory, adoption, collective, decision, history
    )
    return _cli_result(inputs, code, output)


def _mutate_somnic(variant_id, source, activation, records, inventory, adoption, collective):
    item = source.item
    if variant_id == "R7E-T14-A19-V01":
        item(records["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")[
            "target_history_mutated"
        ] = True
    elif variant_id == "R7E-T14-A20-V01":
        row = item(records["orthing_events"], "event_id", "EV-WAKE-001")
        row["episode_id"] = row["session_id"]
        row["occurrence_id"] = row["session_id"]
        row["orthing_id"] = row["session_id"]
    elif variant_id in {"R7E-T14-A21-V01", "R7E-T14-A21-V02"}:
        assessment = item(activation["fixture_outcomes"], "fixture_id", "ACT-POS-001")[
            "claimant_assessments"
        ][0]
        assessment.pop(
            "evaluator_version"
            if variant_id.endswith("V01")
            else "activation_contract_version"
        )
    elif variant_id == "R7E-T14-A22-V01":
        item(activation["fixture_outcomes"], "fixture_id", "ACT-MIXED-LEXICAL-001")[
            "claimant_assessments"
        ][0]["result"] = "applicable"
    elif variant_id == "R7E-T14-A23-V01":
        activation["contracts"][0]["evaluator_vocabulary"] = [
            "applicable",
            "inapplicable",
        ]
    elif variant_id == "R7E-T14-A24-V01":
        row = item(
            records["somnic_assessments"],
            "assessment_id",
            "SA-EVIDENCE-TIMING-001",
        )
        row["evidence_timing"]["observed_at_t1"].append(
            row["evidence_timing"]["discovered_after_t1"].pop()
        )
    elif variant_id == "R7E-T14-A25-V01":
        item(records["orthing_events"], "event_id", "EV-R7E-RETRO-001")[
            "capture_mode"
        ] = "live_capture"
    elif variant_id == "R7E-T14-A26-V01":
        activation["contracts"][0]["fixture_outcomes"] = []
    elif variant_id == "R7E-T14-A27-V01":
        activation["contracts"][0]["authorship"] = {"mode": "normal"}
    elif variant_id == "R7E-T14-A28-V01":
        item(records["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")[
            "retroactive_conformity_rewrite"
        ] = True
    elif variant_id == "R7E-T14-A29-V01":
        item(records["somnus_runs"], "somnus_run_id", "RUN-REOPEN-001")[
            "material_delta_ids"
        ] = []
    elif variant_id == "R7E-T14-A30-V01":
        row = copy.deepcopy(
            item(records["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        )
        row["somnus_run_id"] = "RUN-RECURRENCE-DUPLICATE"
        row["output_ids"] = ["RR-NON-EQUIVALENT"]
        records["somnus_runs"].append(row)
    elif variant_id == "R7E-T14-A31-V01":
        row = item(records["recurrence_reports"], "recurrence_report_id", "RR-001")
        row["supporting_occurrences"] = [row["supporting_occurrences"][0]] * 3
        row["dependence_dimensions"]["episode_count"] = 3
    elif variant_id == "R7E-T14-A32-V01":
        item(records["recurrence_reports"], "recurrence_report_id", "RR-001")[
            "systemic_defect_proven"
        ] = True
    elif variant_id == "R7E-T14-A33-V01":
        item(records["recurrence_reports"], "recurrence_report_id", "RR-001")[
            "emitted_actions"
        ] = ["automatic_patch"]
    elif variant_id == "R7E-T14-A34-V01":
        item(records["authorizations"], "authorization_id", "AUTH-INDEPENDENT-001")[
            "source"
        ] = "provisional_placement"
    elif variant_id == "R7E-T14-A35-V01":
        inventory["candidates"][0]["status"] = "implemented"
        inventory["candidates"][0]["execution"] = "deployed"
    elif variant_id == "R7E-T14-A37-V01":
        capture = item(records["orthing_events"], "event_id", "EV-WAKE-001")
        assessment = item(records["orthing_events"], "event_id", "EV-WAKE-001-ASSESS")
        capture["sequence"], assessment["sequence"] = assessment["sequence"], capture["sequence"]
    elif variant_id == "R7E-T14-A38-V01":
        item(records["claimant_routing_cases"], "case_id", "ROUTE-MULTI-001")[
            "selected_claimant_id"
        ] = "claimant-c"
    elif variant_id == "R7E-T14-A39-V01":
        row = item(records["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")
        row["historical_comparator_ids"] = copy.deepcopy(row["anchor_subject_ids"])
    elif variant_id == "R7E-T14-A40-V01":
        item(records["somnus_runs"], "somnus_run_id", "RUN-RECURRENCE-001")[
            "historical_comparators_reopened"
        ] = True
    elif variant_id == "R7E-T14-A41-V01":
        item(records["somnic_assessments"], "assessment_id", "SA-CLOSED-001")[
            "auto_requeue"
        ] = True
    elif variant_id == "R7E-T14-A43-V01":
        item(records["recurrence_reports"], "recurrence_report_id", "RR-001")[
            "causal_diagnosis"
        ] = "established"
    elif variant_id == "R7E-T14-A45-V01":
        item(records["somnic_assessments"], "assessment_id", "SA-NO-CHANGE-001")[
            "proposal_id"
        ] = "PROP-FORCED"
    elif variant_id == "R7E-T14-A46-V01":
        for row in records["writeback_timeline"]:
            row["time_role"] = "t3"
    elif variant_id == "R7E-T14-A46-V02":
        item(records["somnic_assessments"], "assessment_id", "SA-RECURRENCE-001")[
            "proposal_id"
        ] = "PROP-MEMORY-001"
    elif variant_id == "R7E-T14-A47-V01":
        row = item(records["proposals"], "proposal_id", "PROP-CONTRACT-001")
        row.update(
            provenance_mode="legacy_reflective_proposal",
            supporting_assessment_id="unavailable",
        )
    elif variant_id == "R7E-T14-A48-V01":
        item(records["outcome_evaluations"], "outcome_evaluation_id", "OUTCOME-001")[
            "self_validating"
        ] = True
    elif variant_id == "R7E-T14-A50-V01":
        collective["modes"][1]["mode_id"] = "C1"
    elif variant_id == "R7E-T14-A51-V01":
        collective["shared_types_supply_transport"] = True
    elif variant_id == "R7E-T14-A52-V01":
        collective["event_instances"]["actor_ledger_version_indexed"] = False
    elif variant_id == "R7E-T14-A53-V01":
        collective["receipt_can_govern_or_execute"] = True
    elif variant_id == "R7E-T14-A54-V01":
        collective["source_applicability_auto_propagates"] = True
    elif variant_id == "R7E-T14-A55-V01":
        collective["transclusion"]["semantic_character"] = (
            "structural-not-semantic-and-lossless"
        )
    elif variant_id.startswith("R7E-T14-A56-"):
        if variant_id == "R7E-T14-A56-V04":
            collective["semantic_boundaries"][
                "multi_operator_recurrence_proves_tawatur"
            ] = True
        else:
            promotion = {
                "R7E-T14-A56-V01": "source-independence",
                "R7E-T14-A56-V02": "warrant",
                "R7E-T14-A56-V03": "truth",
            }[variant_id]
            collective["multi_operator_count_implies"] = [promotion]
    elif variant_id == "R7E-T14-A57-V01":
        collective["collective_closure"]["preserves_dissent"] = False
    elif variant_id == "R7E-T14-A58-V01":
        collective["privacy"]["redacted_projection_may_claim_complete"] = True
    elif variant_id == "R7E-T14-A59-V01":
        collective["status"] = "implemented"
    else:
        raise KeyError(variant_id)


def _provenance(variant_id: str, role: str) -> dict:
    from tests import test_candidate_provenance as source

    case = source.CandidateProvenanceTests()
    case.setUp()
    ledger = copy.deepcopy(case.ledger)
    provenance = copy.deepcopy(case.provenance)
    if role == "mutation":
        boundary_id = {
            "R7E-T14-A36-V01": "R7E-PROV-B001-IDENTITY-COLLAPSE",
            "R7E-T14-A42-V01": "R7E-PROV-B002-EPISODE-INDEPENDENCE",
            "R7E-T14-A44-V01": "R7E-PROV-B005-DEFECT-LOCUS-COLLAPSE",
        }[variant_id]
        provenance["provenance_boundaries"] = copy.deepcopy(
            source.PROVENANCE_BOUNDARIES
        )
        next(
            row
            for row in provenance["provenance_boundaries"]
            if row["boundary_id"] == boundary_id
        )["status"] = "allowed"
    inputs = {
        "ledger": ledger,
        "provenance": provenance,
        "backlog": case.backlog_text,
    }
    code, output = source.production_exit(ledger, provenance, case.backlog_text)
    return _cli_result(inputs, code, output)


HANDLERS = {
    "scripts/generate_candidate_state.py": _candidate_state,
    "scripts/validate_semantic_operator_contract.py": _semantic_operator,
    "scripts/validate_memetic_ecology.py": _task7,
    "scripts/validate_meta_noetic_memetics.py": _task7,
    "scripts/validate_noetic_claims.py": _task7,
    "scripts/validate_dynamic_orthing.py": _dynamic_orthing,
    "scripts/validate_argument_map.py": _argument_map,
    "scripts/validate_r7e_llm_witness.py": _witness,
    "scripts/validate_math_source.py": _math_source,
    "scripts/validate_somnic_orthing.py": _somnic,
    "scripts/validate_candidate_provenance.py": _provenance,
}


def execute_direct_probe(binding, role: str) -> dict:
    """Run one exact concrete input through its independently bound owner."""
    if role not in {"control", "mutation"}:
        raise ValueError("invalid Task 14 direct-probe role")
    try:
        handler = HANDLERS[binding.validator_entry_point]
    except KeyError as exc:
        raise ValueError("no direct adapter for production owner") from exc
    return handler(binding.variant_id, role)
