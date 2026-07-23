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

    def issues_with_registry(self, data, registry):
        return validator.validate_mapping(data, registry)

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

    def assert_rejected(self, mutator):
        issues = self.issues(self.mutated(mutator))
        self.assertTrue(issues, "expected invalid mapping to be rejected")

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

    def test_exact_node_identity_set_is_stable(self):
        self.assert_rejected(lambda d: d["nodes"].pop())
        self.assert_rejected(
            lambda d: d["nodes"][-1].__setitem__("id", "ARG-15")
        )

    def test_order_and_dependency_parity(self):
        self.assert_invalid(lambda d: d["nodes"][1].__setitem__("order", 99), "order")
        self.assert_invalid(
            lambda d: d["nodes"][1]["dependencies"].append("ARG-MISSING"),
            "dangling dependency",
        )
        self.assert_rejected(
            lambda d: d["nodes"][5]["dependencies"].append("ARG-08")
        )

    def test_conclusion_cannot_be_its_own_bridge_premise(self):
        self.assert_rejected(
            lambda d: d["nodes"][7]["bridge_premise_refs"].append("ARG-08-C")
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
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("scope", "school-neutral"),
            "invalid scope",
        )

    def test_inference_and_bridge_vocabularies_are_closed(self):
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("inference_type", "obvious"),
            "invalid inference_type",
        )
        self.assert_invalid(
            lambda d: d["nodes"][0].__setitem__("bridge_status", "proven"),
            "invalid bridge_status",
        )

    def test_each_node_keeps_its_exact_typed_semantic_contract(self):
        def substitute_allowed_source(data):
            node = data["nodes"][0]
            status = next(
                row["status"]
                for row in self.registry["claims"]
                if row["id"] == "LAT-1"
            )
            node["source_status_refs"] = ["LAT-1"]
            node["evidence_access_status"] = {"LAT-1": status}
            node["reference_roles"] = {"LAT-1": "comparative"}

        mutations = (
            lambda d: d["nodes"][0].__setitem__(
                "scope", "athari-taymiyyan-operative"
            ),
            lambda d: d["nodes"][0].__setitem__(
                "claim_role", "cross-source-synthesis"
            ),
            lambda d: d["nodes"][3].__setitem__("inference_type", "metaphysical"),
            lambda d: d["nodes"][3].__setitem__("bridge_status", "held"),
            lambda d: d["nodes"][11].__setitem__(
                "warrant_basis", "stated-premises-and-inference"
            ),
            substitute_allowed_source,
            lambda d: d["nodes"][0].__setitem__("label", "neutral tribunal"),
            lambda d: d["nodes"][0]["rival_exit"].__setitem__(
                "joint", "ARG-04"
            ),
            lambda d: d["nodes"][0]["rival_exit"].__setitem__(
                "id", "instrumentalism"
            ),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assert_rejected(mutation)

    def test_non_entailment_firewalls_are_complete(self):
        self.assert_invalid(
            lambda d: d["non_entailments"].pop(),
            "missing non_entailment",
        )

    def test_claims_bind_typed_semantic_boundaries(self):
        boundaries = self.model.get("semantic_boundaries")
        self.assertIsInstance(boundaries, dict)
        self.assertTrue(boundaries)
        for node in self.model["nodes"]:
            for claim in [*node["premises"], node["conclusion"]]:
                with self.subTest(claim=claim["id"]):
                    self.assertIsInstance(claim.get("boundary_refs"), list)
                    self.assertTrue(
                        set(claim["boundary_refs"]).issubset(boundaries),
                        claim,
                    )
        self.assert_rejected(
            lambda d: d["nodes"][-1]["premises"][0]["boundary_refs"].clear()
        )
        self.assert_rejected(
            lambda d: d["semantic_boundaries"][
                "BOUND-RABB-NONCONJUNCTIVE"
            ].__setitem__("owner", "cross_framework_policy")
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
        self.assert_rejected(
            lambda d: d["nodes"][0].__setitem__(
                "warrant_basis",
                "revelation-and-declared-creed-internal-inference",
            )
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
        self.assert_rejected(
            lambda d: d["common_premise_fittingness_to_wisdom"].__setitem__(
                "reason", "the positive inference is established"
            )
        )
        self.assert_rejected(
            lambda d: d["common_premise_fittingness_to_wisdom"].__setitem__(
                "permitted_use", "autonomous proof of divine Wisdom"
            )
        )

    def test_conditional_common_premise_wisdom_control_is_valid(self):
        data = self.mutated(
            lambda d: d["common_premise_fittingness_to_wisdom"].__setitem__(
                "status", "conditional"
            )
        )
        self.assertEqual([], self.issues(data))

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
            "contract drift",
        )
        self.assert_invalid(
            lambda d: d["nodes"][2]["conclusion"].__setitem__(
                "text", "all learners are guaranteed to converge"
            ),
            "contract drift",
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
            "claim identities",
        )

    def test_all_rival_families_are_routed(self):
        self.assertIn("primitivism", self.model["rival_routes"])
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
        self.assert_invalid(
            lambda d: d["rival_routes"]["modal-primitivism"].__setitem__(
                "joint", "ARG-MISSING"
            ),
            "rival route joint",
        )
        self.assert_rejected(
            lambda d: d["rival_routes"]["modal-primitivism"].__setitem__(
                "joint", "ARG-04"
            )
        )
        self.assert_rejected(
            lambda d: d["nodes"][3]["rival_exit"].__setitem__(
                "joint", "actual-Speech"
            )
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

    def test_source_role_and_claim_role_must_match_source_status(self):
        def make_elt_secondary(data):
            node = data["nodes"][0]
            row = next(
                item for item in self.registry["claims"] if item["id"] == "ELT-1"
            )
            node["claim_role"] = "secondary-reconstruction"
            node["source_status_refs"] = ["ELT-1"]
            node["evidence_access_status"] = {"ELT-1": row["status"]}
            node["reference_roles"] = {"ELT-1": "secondary-scholarship"}

        valid = self.mutated(make_elt_secondary)
        self.assertEqual([], self.issues(valid))

        primary_role = copy.deepcopy(valid)
        primary_role["nodes"][0]["reference_roles"]["ELT-1"] = "primary-text"
        self.assertTrue(self.issues(primary_role))

        primary_claim = copy.deepcopy(valid)
        primary_claim["nodes"][0]["claim_role"] = "primary-text-verified"
        self.assertTrue(self.issues(primary_claim))

    def test_research_only_packet_cannot_be_registered_as_support(self):
        data = copy.deepcopy(self.model)
        registry = copy.deepcopy(self.registry)
        discovery = copy.deepcopy(
            next(item for item in registry["claims"] if item["id"] == "EXT-1")
        )
        discovery.update(
            {
                "id": "EXT-DR19",
                "claim": "Deep Research report 19 establishes the positive route",
                "source": "Deep Research report 19",
                "support": "supports the claim",
            }
        )
        registry["claims"].append(discovery)
        node = data["nodes"][0]
        node["source_status_refs"] = ["EXT-DR19"]
        node["evidence_access_status"] = {"EXT-DR19": discovery["status"]}
        node["reference_roles"] = {"EXT-DR19": "comparative"}
        self.assertTrue(self.issues_with_registry(data, registry))

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
        self.assert_rejected(
            lambda d: d["nodes"][0]["conclusion"].__setitem__(
                "citation_locator", "self-asserted local extraction line 1"
            )
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
        self.assert_rejected(
            lambda d: d["nodes"][-1]["premises"][0].__setitem__(
                "text",
                "every lexical sense of Rabb applies conjunctively to every token",
            )
        )
        self.assert_rejected(
            lambda d: d["nodes"][-1]["conclusion"].__setitem__(
                "text", "the etymology of Rabb proves theology and divine Wisdom"
            )
        )
        self.assert_rejected(
            lambda d: d["nodes"][-1]["conclusion"].__setitem__(
                "text", "Rabb brings the creature to complete self-sufficiency"
            )
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
        self.assert_rejected(
            lambda d: d["nodes"][3]["conclusion"].__setitem__(
                "text",
                "Ibn Taymiyya authored Plantingian proper functionalism, which proves a Designer",
            )
        )
        self.assert_rejected(
            lambda d: d["nodes"][3]["premises"][0].__setitem__(
                "text",
                "fitrah is one measurable scalar coordinate and guaranteed attractor",
            )
        )

    def test_allah_is_not_a_formal_object(self):
        self.assert_invalid(
            lambda d: d.__setitem__("divine_formal_object_policy", "internal-formal-object"),
            "Allah",
        )
        self.assert_rejected(
            lambda d: d["nodes"][5]["conclusion"].__setitem__(
                "text", "Allah is represented as an internal formal object"
            )
        )

    def test_structured_nonclaim_boundaries_reject_direct_contradictions(self):
        mutations = (
            lambda d: d["nodes"][8]["conclusion"].__setitem__(
                "text",
                "the OSM result validates the metaphysical and theological conclusion",
            ),
            lambda d: d["nodes"][3]["conclusion"].__setitem__(
                "text",
                "empirical learnability alone yields normative proper function",
            ),
            lambda d: d["nodes"][7]["premises"][0].__setitem__(
                "text", "a personal willing agent performs every contingent selection"
            ),
            lambda d: d["nodes"][5]["conclusion"].__setitem__(
                "text",
                "cross-framework neutrality is a coequal tribunal of soundness",
            ),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assert_rejected(mutation)

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
        self.assert_invalid(
            lambda d: d["speech_bearers"][0].__setitem__(
                "bearer", "generic created thing"
            ),
            "Speech bearer semantics",
        )
        self.assert_rejected(
            lambda d: d["speech_bearers"][-1].update(
                {
                    "id": "SPEECH-BEARER-99",
                    "bearer": None,
                    "created_status": "unknown",
                }
            )
        )

    def test_speech_bearer_collection_order_is_nonsemantic(self):
        data = self.mutated(lambda d: d["speech_bearers"].reverse())
        self.assertEqual([], self.issues(data))

    def test_claim_identity_occurs_exactly_once(self):
        self.assert_rejected(
            lambda d: d["nodes"][0]["premises"].append(
                copy.deepcopy(d["nodes"][0]["premises"][0])
            )
        )

    def test_claim_identity_is_bound_to_canonical_node(self):
        def swap_node_owners(data):
            data["nodes"][0]["premises"][0], data["nodes"][1]["premises"][0] = (
                data["nodes"][1]["premises"][0],
                data["nodes"][0]["premises"][0],
            )

        self.assert_rejected(swap_node_owners)

    def test_claim_identity_is_bound_to_premise_or_conclusion_position(self):
        def swap_premise_and_conclusion(data):
            data["nodes"][0]["premises"][0], data["nodes"][0]["conclusion"] = (
                data["nodes"][0]["conclusion"],
                data["nodes"][0]["premises"][0],
            )

        self.assert_rejected(swap_premise_and_conclusion)

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
            "contract drift",
        )
        self.assert_rejected(
            lambda d: d["speech_boundary"].__setitem__(
                "unsafe_created_arabic_wording", "permitted"
            )
        )
        self.assert_rejected(
            lambda d: d["nodes"][11]["conclusion"].__setitem__(
                "text",
                "capacity for disclosure by itself entails an actual divine Speech event",
            )
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

    def test_generator_pure_validation_rejects_semantic_mutation(self):
        data = self.mutated(
            lambda d: d["cross_framework_policy"].__setitem__(
                "warrant_role", "coequal-neutral-tribunal"
            )
        )
        issues = generator.collect_issues(data, self.registry)
        self.assertTrue(any("dialectical accessibility" in issue for issue in issues))
        with self.assertRaises(ValueError):
            generator.render_argument_map(data)

    def test_malformed_nested_values_return_bounded_issues(self):
        samples = [
            None,
            [],
            {"nodes": None},
            {"nodes": ["not-an-object"]},
            self.mutated(lambda d: d["nodes"][0].__setitem__("premises", "bad")),
            self.mutated(lambda d: d.__setitem__("speech_bearers", {"bad": "shape"})),
            self.mutated(lambda d: d["nodes"][0].__setitem__("id", ["bad"])),
            self.mutated(lambda d: d["nodes"][0].__setitem__("dependencies", [{}])),
            self.mutated(lambda d: d["nodes"][0].__setitem__("source_status_refs", [{}])),
            self.mutated(lambda d: d.__setitem__("non_entailments", [["bad"]])),
            self.mutated(
                lambda d: d["nodes"][0]["reference_roles"].__setitem__("EXT-1", [])
            ),
            self.mutated(lambda d: d["nodes"][0].__setitem__("claim_role", [])),
            self.mutated(lambda d: d["nodes"][9].__setitem__("conclusion", [])),
            self.mutated(
                lambda d: d["rival_routes"]["modal-primitivism"].__setitem__(
                    "joint", []
                )
            ),
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
        with self.assertRaises(ValueError):
            generator.replace_generated_section(
                f"before\n{generator.BEGIN_MARKER}\nold\n"
                f"{generator.END_MARKER}\nafter\n",
                f"payload\n{generator.BEGIN_MARKER}\n",
            )

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

    def test_companion_uses_current_node_count_not_stale_rung_count(self):
        companion = (
            ROOT / "companion/dynamic-orthing-noetic-learning-and-orthability.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("**ten rungs**", companion)
        self.assertIn(f"Argument nodes: **{len(self.model['nodes'])}**.", companion)


if __name__ == "__main__":
    unittest.main()
