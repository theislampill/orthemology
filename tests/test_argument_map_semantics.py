#!/usr/bin/env python3
"""Task 9 structured argument-map and generator regressions."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


generator = _load_module("task9_argument_map_generator", "scripts/generate_argument_map.py")
validator = _load_module("task9_argument_map_validator", "scripts/validate_argument_map.py")


class ArgumentMapSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = yaml.safe_load(
            (ROOT / "companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml").read_text(
                encoding="utf-8"
            )
        )
        cls.registry = yaml.safe_load(
            (ROOT / "references/source-status.yaml").read_text(encoding="utf-8")
        )

    def issues(self, data):
        return validator.validate_mapping(data, self.registry)

    def mutated(self, mutator):
        data = copy.deepcopy(self.model)
        mutator(data)
        return data

    def assert_invalid(self, mutator, fragment):
        issues = self.issues(self.mutated(mutator))
        self.assertTrue(
            any(fragment in issue for issue in issues),
            f"expected {fragment!r} in {issues!r}",
        )

    def test_canonical_mapping_is_valid(self):
        self.assertEqual([], self.issues(copy.deepcopy(self.model)))
        self.assertEqual([], generator.collect_issues(copy.deepcopy(self.model), self.registry))

    def test_required_node_fields(self):
        fields = (
            "id",
            "order",
            "label",
            "scope",
            "premises",
            "inference_type",
            "bridge_status",
            "conclusion",
            "dependencies",
            "claim_role",
            "source_status_refs",
            "evidence_access_status",
            "reference_roles",
            "strongest_objection",
            "rival_exit",
            "warrant_basis",
        )
        for field in fields:
            with self.subTest(field=field):
                self.assert_invalid(
                    lambda d, f=field: d["nodes"][0].pop(f),
                    f"missing field {field}",
                )

    def test_duplicate_stable_id_rejects(self):
        self.assert_invalid(
            lambda d: d["nodes"][1].__setitem__("id", d["nodes"][0]["id"]),
            "duplicate node id",
        )

    def test_order_and_dependency_parity(self):
        self.assert_invalid(lambda d: d["nodes"][1].__setitem__("order", 99), "order")
        self.assert_invalid(
            lambda d: d["nodes"][1]["dependencies"].append("ARG-MISSING"),
            "dangling dependency",
        )

    def test_scope_is_not_neutral_tribunal(self):
        self.assert_invalid(
            lambda d: d["cross_framework_policy"].__setitem__(
                "warrant_role", "coequal-neutral-tribunal"
            ),
            "dialectical accessibility",
        )
        self.assert_invalid(
            lambda d: d.pop("operative_noetic_frame"), "operative_noetic_frame"
        )

    def test_school_or_source_label_cannot_be_warrant(self):
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("warrant_basis", "school-label"),
            "warrant_basis",
        )
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("warrant_basis", "source-identity"),
            "warrant_basis",
        )

    def test_common_premise_wisdom_bridge_stays_held(self):
        self.assert_invalid(
            lambda d: d["common_premise_fittingness_to_wisdom"].__setitem__(
                "status", "established"
            ),
            "fittingness-to-Wisdom",
        )
        self.assert_invalid(
            lambda d: d["nodes"][9].__setitem__("bridge_status", "established"),
            "Athari Wisdom",
        )

    def test_upper_nodes_cannot_be_promoted_by_osm_or_daee(self):
        self.assert_invalid(
            lambda d: d["nodes"][-1].__setitem__("claim_role", "computational-analogy"),
            "upper node",
        )
        self.assert_invalid(
            lambda d: d["nodes"][-1].__setitem__("warrant_basis", "DAEE-result"),
            "warrant_basis",
        )

    def test_no_objective_gradient_or_guaranteed_convergence(self):
        self.assert_invalid(
            lambda d: d["nodes"][1]["conclusion"].__setitem__(
                "text", "an objective differentiable correction gradient exists"
            ),
            "gradient",
        )
        self.assert_invalid(
            lambda d: d["nodes"][2]["conclusion"].__setitem__(
                "text", "all learners are guaranteed to converge"
            ),
            "convergence",
        )

    def test_empirical_learnability_does_not_supply_normativity(self):
        self.assert_invalid(
            lambda d: d["nodes"][3].__setitem__("dependencies", ["ARG-03"]),
            "normativity bridge",
        )

    def test_personal_attributes_not_assumed_in_rung_premises(self):
        self.assert_invalid(
            lambda d: d["nodes"][6]["premises"].append(
                {"id": "P-CIRC", "text": "the ground is already personal and intelligent"}
            ),
            "premise assumes its conclusion",
        )

    def test_all_rival_families_are_routed(self):
        for family in (
            "selected-function-naturalism",
            "modal-primitivism",
            "platonism-structural-realism",
            "brute-contingency",
            "aseity-bootstrapping",
            "euthyphro-fittingness",
            "impersonal-ground",
        ):
            with self.subTest(family=family):
                self.assert_invalid(
                    lambda d, f=family: d["rival_routes"].pop(f),
                    f"missing rival route {family}",
                )

    def test_source_references_resolve_and_roles_match(self):
        self.assert_invalid(
            lambda d: d["nodes"][0]["source_status_refs"].append("NO-SUCH-SOURCE"),
            "unresolved source_status_ref",
        )
        self.assert_invalid(
            lambda d: d["nodes"][0]["reference_roles"].__setitem__(
                "NO-SUCH-SOURCE", "comparative"
            ),
            "reference_roles keys",
        )
        self.assert_invalid(
            lambda d: d["nodes"][0]["reference_roles"].__setitem__(
                "EXT-1", "creed-internal-inference"
            ),
            "invalid reference role",
        )

    def test_evidence_access_must_match_registry(self):
        self.assert_invalid(
            lambda d: d["nodes"][0]["evidence_access_status"].__setitem__(
                "EXT-1", "PRIMARY_TEXT_EXACT"
            ),
            "evidence access drift",
        )

    def test_citation_edition_locator_and_extraction_are_not_copied(self):
        for field in (
            "citation_locator",
            "edition",
            "repository_extraction",
        ):
            with self.subTest(field=field):
                self.assert_invalid(
                    lambda d, f=field: d["nodes"][0].__setitem__(f, "self-asserted"),
                    "copied source-custody field",
                )

    def test_claim_roles_are_canonical_hyphenated_values(self):
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("claim_role", "orthemological_extension"),
            "claim_role",
        )

    def test_rabb_crosswalk_is_layered_and_non_entailing(self):
        self.assert_invalid(
            lambda d: d["rabb_lexical_crosswalk"].__setitem__(
                "lexical_range_semantics", "all-senses-conjunctively-entailed"
            ),
            "Rabb lexical range",
        )
        self.assert_invalid(
            lambda d: d["rabb_lexical_crosswalk"].__setitem__(
                "theological_reach", "etymology-proves-divine-Wisdom"
            ),
            "Rabb lexical",
        )
        self.assert_invalid(
            lambda d: d["rabb_lexical_crosswalk"]["layers"].pop("context_binding"),
            "Rabb layer context_binding",
        )

    def test_fitrah_and_proper_function_boundaries(self):
        self.assert_invalid(
            lambda d: d["fitrah_boundary"].__setitem__("representation", "scalar"),
            "fiṭrah",
        )
        self.assert_invalid(
            lambda d: d["proper_function_boundary"].__setitem__(
                "historical_attribution", "Ibn-Taymiyya-authored-Plantingian-theory"
            ),
            "proper functionalism",
        )

    def test_allah_is_not_a_formal_object(self):
        self.assert_invalid(
            lambda d: d.__setitem__("divine_formal_object_policy", "internal-formal-object"),
            "Allah",
        )

    def test_seven_speech_bearers_are_exact_and_distinct(self):
        self.assertEqual(7, len(self.model["speech_bearers"]))
        self.assert_invalid(lambda d: d["speech_bearers"].pop(), "seven Speech bearers")
        self.assert_invalid(
            lambda d: d["speech_bearers"][5].__setitem__("created_status", "created"),
            "revealed Arabic wording",
        )
        self.assert_invalid(
            lambda d: d["speech_bearers"][1].__setitem__("created_status", "uncreated"),
            "created bearer",
        )

    def test_capacity_does_not_imply_actual_speech(self):
        self.assert_invalid(
            lambda d: d["speech_boundary"].__setitem__(
                "capacity_entails_actual_speech", True
            ),
            "capacity",
        )
        self.assert_invalid(
            lambda d: d["nodes"][-3]["conclusion"].__setitem__(
                "text", "created Arabic wording is the receiver's artifact"
            ),
            "created Arabic wording",
        )

    def test_nested_objection_and_exit_shapes_reject(self):
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("strongest_objection", []),
            "strongest_objection",
        )
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("rival_exit", "open"),
            "rival_exit",
        )

    def test_bridge_references_resolve(self):
        self.assert_invalid(
            lambda d: d["nodes"][1]["bridge_premise_refs"].append("NO-SUCH-CLAIM"),
            "dangling bridge_premise_ref",
        )

    def test_malformed_nested_values_return_bounded_issues(self):
        samples = [
            None,
            [],
            {"nodes": None},
            {"nodes": ["not-an-object"]},
            self.mutated(lambda d: d["nodes"][0].__setitem__("premises", "bad")),
            self.mutated(lambda d: d.__setitem__("speech_bearers", {"bad": "shape"})),
        ]
        for sample in samples:
            with self.subTest(sample=repr(sample)[:60]):
                issues = validator.validate_mapping(sample, self.registry)
                self.assertIsInstance(issues, list)
                self.assertTrue(issues)
                self.assertLessEqual(len(issues), validator.MAX_ISSUES)

    def test_render_is_deterministic_lf_and_has_id_count_parity(self):
        first = generator.render_argument_map(self.model)
        second = generator.render_argument_map(copy.deepcopy(self.model))
        self.assertEqual(first, second)
        self.assertNotIn("\r", first)
        self.assertIn(f"Argument nodes: **{len(self.model['nodes'])}**", first)
        for node in self.model["nodes"]:
            self.assertEqual(1, first.count(f"`{node['id']}`"))

    def test_marker_failures_reject(self):
        rendered = generator.render_argument_map(self.model)
        for document in (
            "no markers",
            f"{generator.BEGIN_MARKER}\nonly begin",
            f"{generator.END_MARKER}\n{generator.BEGIN_MARKER}",
            f"{generator.BEGIN_MARKER}\n{generator.BEGIN_MARKER}\n{generator.END_MARKER}",
            f"{generator.BEGIN_MARKER}\n{generator.END_MARKER}\n{generator.END_MARKER}",
        ):
            with self.subTest(document=document):
                with self.assertRaises(ValueError):
                    generator.replace_generated_section(document, rendered)

    def test_marker_replacement_is_singular_and_lf(self):
        document = f"before\r\n{generator.BEGIN_MARKER}\r\nold\r\n{generator.END_MARKER}\r\nafter\r\n"
        rendered = generator.render_argument_map(self.model)
        replaced = generator.replace_generated_section(document, rendered)
        self.assertEqual(1, replaced.count(generator.BEGIN_MARKER))
        self.assertEqual(1, replaced.count(generator.END_MARKER))
        self.assertNotIn("\r", replaced)

    def test_build_matches_checked_in_companion(self):
        path, expected = generator.build()
        self.assertEqual(
            expected,
            path.read_text(encoding="utf-8").replace("\r\n", "\n"),
        )


if __name__ == "__main__":
    unittest.main()
