#!/usr/bin/env python3
"""Live unconditional-path and required-rule configuration regressions.

These are constructed bundle-local controls, not experimental or historical
replays. Conditional closure/robustness shape reconstruction remains outside
this contract. Failed routing must not unsound an unrelated placement claim.
"""
import copy
import importlib.util
import io
import os
from pathlib import Path
import unittest
from unittest import mock
import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "validate_cross_record_semantics.py"
CONFIG_NAMES = ("claim-reason-requirements.yaml", "governance-requirements.yaml",
                "verdict-registry.yaml")
DOCUMENTS = {name: yaml.safe_load((ROOT / "docs" / name).read_text(encoding="utf-8"))
             for name in CONFIG_NAMES}
BASELINE = [name for name in DOCUMENTS["verdict-registry.yaml"]["core_path"]
            if DOCUMENTS["governance-requirements.yaml"]["rules"][name]["when"] == "always"]

# A public synthetic consistency witness: the declared path omits a failing
# unconditional procedure obligation. No private/scoring material is involved.
REDUCED_PARTS = [{'schema': 'orthing-episode.schema.json',
  'instance': {'episode_id': 'e',
               'record_mode': 'audit-ready',
               'occurrence': {'identity_key': 'k', 'version': '1', 'kind': 'case'},
               'actor': 'reviewer',
               'analysis': {'analysis_id': 'AN', 'version': '1'},
               'time': '2026-07-01T12:00:00Z',
               'placement': {'axis': 'value'},
               'observation': 'synthetic declared observation',
               'evidence': [],
               'evidence_absent_reason': 'synthetic consistency countercontrol',
               'warrant': None,
               'policy': 'declared synthetic policy',
               'claim_ledger_ref': 'ledger-e',
               'verdict_record_ref': 'verdict-e',
               'external_refs': [{'kind': 'analysis',
                                  'ref': 'AN@1',
                                  'registry': 'synthetic-analysis-registry',
                                  'resolution_status': 'resolved-external'},
                                 {'kind': 'occurrence',
                                  'ref': 'k@1',
                                  'registry': 'synthetic-occurrence-registry',
                                  'resolution_status': 'resolved-external'}]}},
 {'schema': 'claim-ledger.schema.json',
  'instance': {'episode_id': 'e',
               'claims': [{'claim_id': 'q',
                           'proposition': 'synthetic proposition',
                           'target': {'identity_key': 'k', 'version': '1'},
                           'analysis': {'analysis_id': 'AN', 'version': '1'},
                           'property_class': 'structural',
                           'success_surface': 'synthetic declared surface',
                           'evidence_inapplicable_reason': 'synthetic countercontrol',
                           'verification_status': 'provisional',
                           'claim_type': 'placement'}],
               'residuals': []}},
 {'schema': 'verdict-record.schema.json',
  'instance': {'episode_id': 'e',
               'index': {'analysis_id': 'AN',
                         'analysis_version': '1',
                         'actor': 'reviewer',
                         'decision_time': '2026-07-01T12:00:00Z',
                         'information_state': 'declared countercontrol inputs'},
               'required_path': ['EVIDENCE_SUPPORT'],
               'statuses': {'EVIDENCE_SUPPORT': 'pass',
                            'PROCEDURE_RELIABLE': 'fail',
                            'EVIDENCE_CURRENT': 'pass',
                            'GOV_CONFIG_ADEQUATE': 'pass',
                            'GOV_POLICY_ADEQUATE': 'pass',
                            'EXECUTION_FAITHFUL': 'pass',
                            'EX_ANTE_JUSTIFIED': 'pass'},
               'pathway_state': 'adequate',
               'claim_reasoning_paths': [{'claim_id': 'q',
                                          'req_reason': ['EVIDENCE_SUPPORT'],
                                          'reasoning_path_adequate': 'adequate'}]}}]

def load_validator(documents=None):
    supplied = copy.deepcopy(DOCUMENTS if documents is None else documents)
    def rule_open(path, *args, **kwargs):
        path = Path(path)
        if path.parent != ROOT / "docs" or path.name not in CONFIG_NAMES:
            raise AssertionError("unexpected rule input: " + str(path))
        if path.name not in supplied:
            raise FileNotFoundError(path.name)
        value = supplied[path.name]
        return io.StringIO(value if isinstance(value, str) else yaml.safe_dump(value))
    spec = importlib.util.spec_from_file_location("cross_record_control", SOURCE)
    module = importlib.util.module_from_spec(spec)
    with mock.patch("builtins.open", rule_open):
        spec.loader.exec_module(module)
    return module


def adequate_parts():
    parts = copy.deepcopy(REDUCED_PARTS)
    verdict = parts[2]["instance"]
    verdict["required_path"] = list(BASELINE)
    verdict["statuses"]["PROCEDURE_RELIABLE"] = "pass"
    verdict["claim_reasoning_paths"][0]["req_reason"] = list(BASELINE)
    return parts


class CrossRecordGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self.assertEqual(7, len(BASELINE), "the declared unconditional control population changed")

    def configuration_rejected(self, documents):
        validator = load_validator(documents)
        try:
            issues = validator.collect_issues(adequate_parts())
        except Exception as exc:
            self.fail("malformed configuration escaped as an exception rather than a validation issue: " + repr(exc))
        self.assertTrue(any("required rule configuration" in issue for issue in issues), issues)

    def test_reduced_episode_path_is_rejected(self):
        issues = self.validator.collect_issues(copy.deepcopy(REDUCED_PARTS))
        self.assertTrue(any("unconditional governance requirement" in x for x in issues), issues)

    def test_each_unconditional_obligation_is_not_omittable(self):
        for name in BASELINE:
            with self.subTest(verdict=name):
                parts = adequate_parts()
                verdict = parts[2]["instance"]
                verdict["required_path"].remove(name)
                verdict["claim_reasoning_paths"][0]["req_reason"] = list(verdict["required_path"])
                issues = self.validator.collect_issues(parts)
                self.assertTrue(any("unconditional governance requirement" in x and name in x
                                    for x in issues), issues)

    def test_complete_adequate_path_is_accepted(self):
        self.assertEqual([], self.validator.collect_issues(adequate_parts()))

    def test_complete_failed_procedure_remains_honestly_defective(self):
        parts = adequate_parts()
        verdict = parts[2]["instance"]
        verdict["statuses"]["PROCEDURE_RELIABLE"] = "fail"
        verdict["pathway_state"] = "defective"
        verdict["claim_reasoning_paths"][0]["reasoning_path_adequate"] = "defective"
        self.assertEqual([], self.validator.collect_issues(parts))

    def test_failed_route_preserves_unrelated_placement_claim_adequacy(self):
        parts = adequate_parts()
        parts[0]["instance"]["route"] = "declared route"
        verdict = parts[2]["instance"]
        verdict["required_path"].append("ROUTE_ADMISSIBLE")
        verdict["statuses"]["ROUTE_ADMISSIBLE"] = "fail"
        verdict["pathway_state"] = "defective"
        self.assertEqual("adequate", verdict["claim_reasoning_paths"][0]["reasoning_path_adequate"])
        self.assertEqual([], self.validator.collect_issues(parts))

    def test_complete_episode_still_rejects_claim_projection_omission(self):
        parts = adequate_parts()
        parts[2]["instance"]["claim_reasoning_paths"][0]["req_reason"] = ["EVIDENCE_SUPPORT"]
        self.assertTrue(any("req_reason does not match" in x
                            for x in self.validator.collect_issues(parts)))

    def test_baseline_membership_does_not_invent_path_order(self):
        parts = adequate_parts()
        parts[2]["instance"]["required_path"].reverse()
        self.assertEqual([], self.validator.collect_issues(parts))

    def test_each_required_config_must_be_available(self):
        for name in CONFIG_NAMES:
            with self.subTest(config=name):
                docs = copy.deepcopy(DOCUMENTS)
                del docs[name]
                self.configuration_rejected(docs)

    def test_empty_malformed_and_wrong_type_rule_tables_fail_explicitly(self):
        for name in CONFIG_NAMES[:2]:
            for value in [None, {}, {"rules": {}}, {"rules": []}, "rules: [", {"rules": {"EVIDENCE_SUPPORT": None}}]:
                with self.subTest(config=name, value=value):
                    docs = copy.deepcopy(DOCUMENTS)
                    docs[name] = value
                    self.configuration_rejected(docs)

    def test_partial_or_extra_rule_domains_fail_explicitly(self):
        for name in CONFIG_NAMES[:2]:
            for extra in [False, True]:
                with self.subTest(config=name, extra=extra):
                    docs = copy.deepcopy(DOCUMENTS)
                    if extra:
                        docs[name]["rules"]["NOT_A_CORE_VERDICT"] = {"when": "always"}
                    else:
                        del docs[name]["rules"]["PROCEDURE_RELIABLE"]
                    self.configuration_rejected(docs)

    def test_malformed_rule_conditions_fail_explicitly(self):
        for name in CONFIG_NAMES[:2]:
            for rule in [{}, {"when": None}, {"when": ""}]:
                with self.subTest(config=name, rule=rule):
                    docs = copy.deepcopy(DOCUMENTS)
                    docs[name]["rules"]["PROCEDURE_RELIABLE"] = rule
                    self.configuration_rejected(docs)

    def test_undeclared_rule_conditions_fail_explicitly(self):
        for name in CONFIG_NAMES[:2]:
            with self.subTest(config=name):
                docs = copy.deepcopy(DOCUMENTS)
                docs[name]["rules"]["PROCEDURE_RELIABLE"]["when"] = "undeclared_predicate"
                self.configuration_rejected(docs)

    def test_malformed_registry_core_fails_explicitly(self):
        for core in [[], "EVIDENCE_SUPPORT", ["EVIDENCE_SUPPORT", "EVIDENCE_SUPPORT"], [None]]:
            with self.subTest(core=core):
                docs = copy.deepcopy(DOCUMENTS)
                docs["verdict-registry.yaml"]["core_path"] = core
                self.configuration_rejected(docs)

    def test_existing_zero_token_burden_guard_remains(self):
        parts = adequate_parts()
        verdict = parts[2]["instance"]
        verdict["required_path"].append("GOV_TOKEN_ADEQUATE")
        verdict["statuses"]["GOV_TOKEN_ADEQUATE"] = "pass"
        self.assertTrue(any("zero-burden rule" in x for x in self.validator.collect_issues(parts)))

    def test_existing_claimwise_factivity_guard_remains(self):
        parts = adequate_parts()
        parts[2]["instance"]["claim_verdicts"] = [{"claim_id": "q", "token_truth_linked": "pass", "result_correct": "fail"}]
        self.assertTrue(any("factive claim-wise" in x for x in self.validator.collect_issues(parts)))


if __name__ == "__main__":
    unittest.main()
