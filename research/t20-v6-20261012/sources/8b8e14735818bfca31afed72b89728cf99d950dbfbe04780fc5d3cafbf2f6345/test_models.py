"""Executable specification written before the reference implementations."""
import importlib
import unittest


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


if __name__ == "__main__":
    unittest.main()
