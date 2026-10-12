"""Executable specification written before the reference implementations."""
import importlib
import unittest
from dataclasses import replace


class Models(unittest.TestCase):
    def module(self, name):
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError:
            self.fail(f"Required finite model {name} is not implemented")

    def test_occurrence_matrix(self):
        m = self.module("occurrence_model")
        result = m.run_cases()
        self.assertGreaterEqual(len(result["cases"]), 20)
        for row in result["cases"]:
            with self.subTest(row["name"]):
                self.assertEqual(row["actual"], row["expected"])
        self.assertGreaterEqual(result["roundtrip_cases"], 100)
        self.assertTrue(result["discriminating_valuation"])

    def test_service_migration_and_all_retractions(self):
        m = self.module("continuation_model")
        result = m.run_cases()
        for row in result["cases"]:
            with self.subTest(row["name"]):
                self.assertEqual(row["actual"], row["expected"])
        for row in result["profiles"]:
            self.assertEqual(row["direct_implication"], row["support_cover"])
            self.assertTrue(row["operational_monotonicity"])
            self.assertEqual(row["retained_sets_checked"], 64)
        by_name = {p["name"]: p for p in result["profiles"]}
        self.assertFalse(by_name["decoupled"]["support_cover"])
        self.assertTrue(by_name["atomic_bundles"]["support_cover"])
        self.assertEqual(by_name["decoupled"]["epistemic_supports"], [["archive"], ["reserve"]])
        self.assertEqual(by_name["atomic_bundles"]["epistemic_supports"], [["archive"], ["reserve"]])
        self.assertNotEqual(by_name["decoupled"]["operational_supports"], by_name["atomic_bundles"]["operational_supports"])
        self.assertTrue(result["parent_intervention"]["migrated_tracks_parent"])
        self.assertFalse(result["parent_intervention"]["fixed_twin_tracks_parent"])
        self.assertGreaterEqual(result["executed_request_steps"], 1000)

    def test_counterfeit_same_id_parent_is_rejected(self):
        m = self.module("continuation_model")
        w = m.World(0)
        fake = m.Token(0, "direct", 1)
        with self.assertRaises(m.Unavailable):
            w.migrate(fake, "inverse", m.resources(m.ROOTS))

    def test_counterfeit_same_id_operator_is_rejected(self):
        m = self.module("continuation_model")
        w = m.World(0)
        fake = m.Token(0, "direct", 1)
        with self.assertRaises(m.Unavailable):
            w.step(fake, "read", m.resources(m.ROOTS))

    def test_same_rule_id_cannot_substitute_new_owner(self):
        m = self.module("occurrence_model")
        service = self.module("continuation_model")
        w = service.World(0)
        endpoint = w.migrate(w.tokens[0], "inverse", service.resources(service.ROOTS)).identity
        rule = m.Attestation("rule-event", "Principal", w.bearer(endpoint), "service-duty", 1, 3, office_history=w)
        o = m.Occurrence("new", m.Context(w.bearer(endpoint), "Operator", 1, "lab"),
                         "Assert", ("duty", "you", "inspect", "now", 2))
        self.assertEqual(m.prospective_owner(o, rule, {rule.rule_event: rule}, w, endpoint), "Principal")
        self.assertIsNone(m.prospective_owner(o, replace(rule, owner="Counterfeit"), {rule.rule_event: rule}, w, endpoint))

    def test_another_institution_same_named_holder_cannot_inherit_attestation(self):
        m = self.module("occurrence_model")
        service = self.module("continuation_model")
        w, other = service.World(0), service.World(0)
        endpoint = w.migrate(w.tokens[0], "inverse", service.resources(service.ROOTS)).identity
        other_endpoint = other.migrate(other.tokens[0], "inverse", service.resources(service.ROOTS)).identity
        rule = m.Attestation("rule-event", "Principal", w.bearer(endpoint), "service-duty", 1, 3, office_history=w)
        o = m.Occurrence("new", m.Context(w.bearer(endpoint), "Operator", 1, "lab"),
                         "Assert", ("duty", "you", "inspect", "now", 2))
        self.assertEqual(m.prospective_owner(o, rule, {rule.rule_event: rule}, w, endpoint), "Principal")
        self.assertIsNone(m.prospective_owner(o, rule, {rule.rule_event: rule}, other, other_endpoint))

    def test_same_occurrence_id_cannot_substitute_new_content(self):
        m = self.module("occurrence_model")
        original = m.Occurrence("old", m.Context("Principal", "Operator", 0, "lab"),
                                "Assert", ("duty", "you", "inspect", "now", 2))
        p = m.RecipientPremises({original.event: original}, frozenset({("Principal", "service-duty")}))
        altered = replace(original, formula=("duty", "you", "transfer", "now", 2))
        self.assertIsNone(m.warranted(altered, m.relay(altered), p))

    def test_owned_false_report_defeats_scoped_veracity_not_ownership(self):
        m = self.module("occurrence_model")
        service = self.module("continuation_model")
        w = service.World(0)
        endpoint = w.migrate(w.tokens[0], "inverse", service.resources(service.ROOTS)).identity
        rule = m.Attestation("rule", "Principal", w.bearer(endpoint), "service-duty", 1, 3, office_history=w)
        report = m.Occurrence("false-report", m.Context(w.bearer(endpoint), "Operator", 1, "lab"),
                              "Assert", ("duty", "you", "inspect", "now", 2))
        owner = m.prospective_owner(report, rule, {rule.rule_event: rule}, w, endpoint)
        self.assertEqual(owner, "Principal")
        check = m.scoped_veracity_holds
        self.assertFalse(check([(report, owner)], "Principal", "service-duty", set()))


if __name__ == "__main__":
    unittest.main()
