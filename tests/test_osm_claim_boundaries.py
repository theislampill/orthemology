#!/usr/bin/env python3
"""Task 8 OSM/CSCG claim-boundary regressions.

Each OSM-T01..T22 mutation changes one field in a complete valid structured
control.  The validator is intentionally called through its pure mapping API;
until that API exists, the compatibility shim models the current permissive
false-pass as an empty issue list.
"""

from __future__ import annotations

import copy
import importlib.util
import os
import pathlib
import shutil
import tempfile
import unittest

import yaml


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR_PATH = os.path.join(ROOT, "scripts", "validate_dynamic_orthing.py")
SPEC = importlib.util.spec_from_file_location("validate_dynamic_orthing_task8", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(VALIDATOR)


OBJECTS = [
    ("world_task_state", "world-task-state", "source-reported"),
    ("concrete_occurrence", "concrete-occurrence", "project"),
    ("biological_sensory_observation", "biological-sensory-observation", "source-reported"),
    ("model_observation_symbol", "model-observation-symbol", "source-reported"),
    ("biological_single_cell_response", "biological-single-cell-response", "source-reported"),
    ("biological_population_representation", "biological-population-representation", "source-reported"),
    ("cscg_clone_latent_state", "cscg-clone-latent-state", "source-reported"),
    ("latent_posterior", "latent-posterior", "source-reported"),
    ("model_parameter_state", "model-parameter-state", "source-reported"),
    ("model_representation_output", "model-representation-output", "source-reported"),
    ("derived_representation_geometry", "derived-representation-geometry", "project"),
    ("inferred_orthemic_profile", "inferred-orthemic-profile", "project"),
    ("actual_orthemic_profile", "actual-orthemic-profile", "project"),
]

RELATIONS = [
    ("rel_world_observation", "world_task_state", "generates", "biological_sensory_observation", "source-reported"),
    ("rel_symbol_abstraction", "model_observation_symbol", "abstracts", "biological_sensory_observation", "source-reported"),
    ("rel_observation_response", "biological_sensory_observation", "elicits-measured", "biological_single_cell_response", "source-reported"),
    ("rel_population_aggregation", "biological_population_representation", "aggregates", "biological_single_cell_response", "source-reported"),
    ("rel_clone_emission", "cscg_clone_latent_state", "deterministically-emits", "model_observation_symbol", "source-reported"),
    ("rel_posterior_support", "latent_posterior", "ranges-over", "cscg_clone_latent_state", "source-reported"),
    ("rel_parameter_output", "model_parameter_state", "generates", "model_representation_output", "source-reported"),
    ("rel_output_geometry", "derived_representation_geometry", "derived-from", "model_representation_output", "project"),
    ("rel_latent_profile", "cscg_clone_latent_state", "partially-relates-to", "inferred_orthemic_profile", "project"),
]

METHODS = [
    {
        "id": "baum_welch_em",
        "model_families": ["cscg"],
        "role": "likelihood-fit",
        "process_class": "expectation-maximization",
        "sequence": 1,
        "primary_cscg_fit": True,
        "phrase": "Baum-Welch expectation-maximization",
        "evidence_access_status": "article-text",
        "source_locator": "DOI 10.1038/s41586-024-08548-w; Methods: CSCG",
    },
    {
        "id": "viterbi_training",
        "model_families": ["cscg"],
        "role": "transition-refinement",
        "process_class": "viterbi-training",
        "sequence": 2,
        "primary_cscg_fit": False,
        "phrase": "Viterbi training",
        "evidence_access_status": "article-text",
        "source_locator": "DOI 10.1038/s41586-024-08548-w; Methods: CSCG transition-matrix extraction",
    },
    {
        "id": "map_decode",
        "model_families": ["cscg"],
        "role": "latent-assignment-decode",
        "process_class": "max-product-backtrace",
        "sequence": 3,
        "primary_cscg_fit": False,
        "phrase": "MAP decode",
        "evidence_access_status": "pinned-official-code",
        "source_locator": (
            "sprustonlab/OSM_Paper_Figures@c1d1788b54c737efe24402e02762eee10da0d0d7;"
            " fig_4/fig_4_CSCG/chmm_actions.py:176-187"
        ),
    },
    {
        "id": "bptt",
        "model_families": ["vanilla-rnn"],
        "role": "gradient-computation",
        "process_class": "backpropagation-through-time",
        "sequence": 1,
        "primary_cscg_fit": False,
        "phrase": "backpropagation through time",
        "evidence_access_status": "article-text",
        "source_locator": "DOI 10.1038/s41586-024-08548-w; Methods: Vanilla RNNs",
    },
    {
        "id": "adam",
        "model_families": ["vanilla-rnn", "lstm", "transformer"],
        "role": "parameter-optimizer",
        "process_class": "gradient-optimizer",
        "sequence": 2,
        "primary_cscg_fit": False,
        "phrase": "Adam",
        "evidence_access_status": "article-text",
        "source_locator": "DOI 10.1038/s41586-024-08548-w; Methods: Vanilla RNNs, LSTM, Transformers",
    },
    {
        "id": "cross_entropy",
        "model_families": ["vanilla-rnn", "lstm", "transformer"],
        "role": "objective",
        "process_class": "cross-entropy",
        "sequence": 0,
        "primary_cscg_fit": False,
        "phrase": "cross-entropy",
        "evidence_access_status": "article-text",
        "source_locator": "DOI 10.1038/s41586-024-08548-w; Methods: Vanilla RNNs, LSTM, Transformers",
    },
    {
        "id": "local_hebbian_timing",
        "model_families": ["hebbian-rnn"],
        "role": "local-timing-weight-update",
        "process_class": "local-hebbian",
        "sequence": 1,
        "primary_cscg_fit": False,
        "phrase": "local timing-based Hebbian update",
        "evidence_access_status": "article-text",
        "source_locator": "DOI 10.1038/s41586-024-08548-w; Methods: Hebbian-RNN",
    },
]


def valid_mapping():
    return {
        "schema": "orthemology-osm-task8-contract-v1",
        "objects": [
            {"id": object_id, "type": object_type, "ownership": ownership}
            for object_id, object_type, ownership in OBJECTS
        ],
        "relations": [
            {
                "id": relation_id,
                "subject": subject,
                "predicate": predicate,
                "object": object_id,
                "ownership": ownership,
                "identity": False,
            }
            for relation_id, subject, predicate, object_id, ownership in RELATIONS
        ],
        "asserted_identities": [],
        "method_roles": copy.deepcopy(METHODS),
        "comparison": {
            "endpoint": {
                "criterion": "similar-reported-final-representational-structure",
                "exact_identity": False,
                "cross_model_parameter_equality": False,
                "mechanism_inferred": False,
            },
            "trajectory": {
                "claim": "cscg-consistently-matched-reported-decorrelation-order",
                "scope": "among-tested-models-under-reported-evaluation",
                "universal_uniqueness": False,
                "unique_biological_mechanism": False,
                "further_research_required": True,
            },
            "performance": {
                "high_performance_without_global_orthogonalization": True,
                "nonorthogonal_controls": ["relu-rnn", "sigmoid-rnn", "lstm", "transformer"],
                "all_non_cscg_failed": False,
                "geometry_necessary": False,
            },
            "adaptation": {
                "subject": "biological-ca1-representations",
                "conditions": ["novel-indicator-cues", "stretched-track-segments"],
                "interpretations": ["new-state-creation", "observation-rebinding-to-existing-state"],
                "model_response": "future-work",
                "promotes_to": [],
            },
        },
        "source_custody": {
            "doi": "10.1038/s41586-024-08548-w",
            "article_loci": [
                "Methods: CSCG",
                "Methods: Vanilla RNNs",
                "Methods: LSTM",
                "Methods: Transformers",
                "Methods: Hebbian-RNN",
                "Figure 4 and accompanying text",
                "Figure 5 and accompanying text",
            ],
            "local_access_copy": {
                "sha256": "0D097CBA7BBB25A949E2BF95AF28B5A2259BD8D60B0E5FAC5A74CDF7D05AA814",
                "locator_role": "custody-only",
                "sole_public_evidence": False,
                "extraction_lines_are_journal_pagination": False,
            },
            "official_code": {
                "repository": "sprustonlab/OSM_Paper_Figures",
                "commit": "c1d1788b54c737efe24402e02762eee10da0d0d7",
                "map_decode_locator": "fig_4/fig_4_CSCG/chmm_actions.py:176-187",
            },
        },
        "claim_boundaries": {
            "overall_claim_role": "computational-analogy",
            "content_kind": "model-comparison",
            "evidence_access_status": "article-text-and-pinned-code",
            "geometry_definition": {
                "content_kind": "project-extension",
                "claim_role": "orthemological-extension",
                "evidence_access_status": "project-owned-definition",
            },
            "supported_domains": [],
            "biological_or_wet_lab_procedure_imported": False,
            "forbidden_promotions": [
                "Orthemology",
                "candidate terminology",
                "human noetics",
                "fitrah",
                "metaphysics",
                "Necessary Being",
                "divine attributes",
                "divine Speech",
                "theology",
            ],
        },
    }


def issues_for(mapping):
    validator = getattr(VALIDATOR, "validate_osm_mapping", None)
    if validator is None:
        return []
    return validator(mapping)


def mutate(path, value):
    doc = valid_mapping()
    target = doc
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return doc


def method_index(method_id):
    return next(i for i, method in enumerate(METHODS) if method["id"] == method_id)


class OSMClaimBoundaryTests(unittest.TestCase):
    def assert_rejected(self, mapping, label):
        self.assertTrue(issues_for(mapping), label)

    def test_osm_t01_clone_neuron_identity_rejects(self):
        doc = mutate(("objects", 6, "id"), "biological_single_cell_response")
        self.assert_rejected(doc, "clone and biological response must remain distinct")

    def test_osm_t02_cell_population_collapse_rejects(self):
        doc = mutate(("objects", 5, "id"), "biological_single_cell_response")
        self.assert_rejected(doc, "cell response and population representation must remain distinct")

    def test_osm_t03_posterior_world_relation_rejects(self):
        doc = mutate(("relations", 5, "object"), "world_task_state")
        self.assert_rejected(doc, "posterior must range over clone/model latent state")

    def test_osm_t04_posterior_profile_identity_rejects(self):
        for profile in ("inferred_orthemic_profile", "actual_orthemic_profile"):
            with self.subTest(profile=profile):
                doc = mutate(("asserted_identities",), [["latent_posterior", profile]])
                self.assert_rejected(doc, "posterior/profile identity must reject")

    def test_osm_t05_parameter_output_or_geometry_identity_rejects(self):
        for target in ("model_representation_output", "derived_representation_geometry"):
            with self.subTest(target=target):
                doc = mutate(("asserted_identities",), [["model_parameter_state", target]])
                self.assert_rejected(doc, "parameter/output/geometry identity must reject")

    def test_osm_t06_exact_unique_firewall_membership_is_required(self):
        for replacement in ("world_task_state", "extra_untyped_layer"):
            with self.subTest(replacement=replacement):
                doc = mutate(("objects", 12, "id"), replacement)
                self.assert_rejected(doc, "exact 13-object membership must reject duplicate/substitute")

    def test_osm_t07_biological_observation_model_symbol_identity_rejects(self):
        doc = mutate(("relations", 1, "predicate"), "identical-to")
        self.assert_rejected(doc, "model symbol must abstract rather than equal biological observation")

    def test_osm_t08_viterbi_only_primary_fit_rejects(self):
        doc = mutate(("method_roles", method_index("baum_welch_em"), "primary_cscg_fit"), False)
        self.assert_rejected(doc, "Baum-Welch must remain the primary CSCG likelihood fit")

    def test_osm_t09_literal_viterbi_training_is_valid_but_forbidding_it_rejects(self):
        self.assertEqual([], issues_for(valid_mapping()))
        doc = mutate(("method_roles", method_index("viterbi_training"), "phrase"), "Viterbi terminology forbidden")
        self.assert_rejected(doc, "the exact source-faithful Viterbi training phrase is required")

    def test_osm_t10_em_as_gradient_method_rejects(self):
        doc = mutate(("method_roles", method_index("baum_welch_em"), "process_class"), "gradient-ascent")
        self.assert_rejected(doc, "Baum-Welch EM is not a generic gradient method")

    def test_osm_t11_bptt_adam_cross_entropy_roles_cannot_collapse(self):
        mutations = [
            (("method_roles", method_index("bptt"), "role"), "parameter-optimizer"),
            (("method_roles", method_index("adam"), "role"), "objective"),
            (("method_roles", method_index("cross_entropy"), "role"), "parameter-optimizer"),
        ]
        for path, value in mutations:
            with self.subTest(path=path, value=value):
                self.assert_rejected(mutate(path, value), "RNN method-role collapse must reject")

    def test_osm_t12_not_every_model_is_gradient_trained(self):
        doc = mutate(("method_roles", method_index("local_hebbian_timing"), "process_class"), "gradient-optimizer")
        self.assert_rejected(doc, "local Hebbian timing update must remain distinct")

    def test_osm_t13_trajectory_uniqueness_requires_reported_scope(self):
        doc = mutate(("comparison", "trajectory", "scope"), "all-models-universally")
        self.assert_rejected(doc, "trajectory claim must be scoped to tested models/evaluation")

    def test_osm_t14_endpoint_and_trajectory_do_not_prove_mechanism(self):
        doc = mutate(("comparison", "trajectory", "unique_biological_mechanism"), True)
        self.assert_rejected(doc, "unique biological mechanism promotion must reject")

    def test_osm_t15_neighboring_endpoint_controls_are_preserved(self):
        doc = mutate(("comparison", "performance", "all_non_cscg_failed"), True)
        self.assert_rejected(doc, "all-non-CSCG-failed claim must reject")

    def test_osm_t16_endpoint_similarity_is_not_identity(self):
        mutations = [
            (("comparison", "endpoint", "exact_identity"), True),
            (("comparison", "endpoint", "cross_model_parameter_equality"), True),
            (("comparison", "endpoint", "criterion"), "same-final-representation"),
        ]
        for path, value in mutations:
            with self.subTest(path=path, value=value):
                self.assert_rejected(mutate(path, value), "endpoint equality overclaim must reject")

    def test_osm_t17_geometry_is_not_necessary_for_high_performance(self):
        doc = mutate(("comparison", "performance", "geometry_necessary"), True)
        self.assert_rejected(doc, "performance/geometry necessity claim must reject")

    def test_osm_t18_adaptation_does_not_promote_to_unreported_guarantees(self):
        for promotion in ("correctness", "convergence", "broad-generalization", "model-transport"):
            with self.subTest(promotion=promotion):
                doc = mutate(("comparison", "adaptation", "promotes_to"), [promotion])
                self.assert_rejected(doc, "adaptation promotion must reject")

    def test_osm_t19_adaptation_preserves_both_live_interpretations(self):
        doc = mutate(
            ("comparison", "adaptation", "interpretations"),
            ["new-state-creation"],
        )
        self.assert_rejected(doc, "new-state and observation-rebinding alternatives are both required")

    def test_osm_t20_project_geometry_methods_are_not_nature_reported(self):
        doc = mutate(
            ("claim_boundaries", "geometry_definition", "claim_role"),
            "primary-text-verified",
        )
        self.assert_rejected(doc, "project geometry definition must remain an orthemological extension")

    def test_osm_t21_cross_domain_support_or_wet_lab_import_rejects(self):
        domains = valid_mapping()["claim_boundaries"]["forbidden_promotions"] + [
            "another external domain",
        ]
        for domain in domains:
            with self.subTest(domain=domain):
                doc = mutate(("claim_boundaries", "supported_domains"), [domain])
                self.assert_rejected(doc, "OSM cross-domain evidential promotion must reject")
        doc = mutate(("claim_boundaries", "biological_or_wet_lab_procedure_imported"), True)
        self.assert_rejected(doc, "biological/wet-lab procedure import must reject")

    def test_osm_t22_unresolved_local_extraction_as_sole_evidence_rejects(self):
        doc = mutate(("source_custody", "local_access_copy", "sole_public_evidence"), True)
        self.assert_rejected(doc, "local extraction may be custody evidence, never sole public evidence")

    def test_pure_root_validation_api_accepts_explicit_root(self):
        validator = getattr(VALIDATOR, "validate_osm_root", None)
        self.assertTrue(callable(validator), "validator must expose pure root validation")
        self.assertEqual([], validator(ROOT))

    def test_malformed_nested_shapes_return_bounded_issues(self):
        mutations = [
            (("relations", 0, "subject"), {"not": "an id"}),
            (("asserted_identities",), [[{"not": "an id"}, "world_task_state"]]),
            (("comparison", "performance", "nonorthogonal_controls"), [{"not": "a control"}]),
            (("claim_boundaries", "supported_domains"), [{"not": "a domain"}]),
            (("claim_boundaries", "forbidden_promotions"), [{"not": "a promotion"}]),
        ]
        for path, value in mutations:
            with self.subTest(path=path):
                self.assertTrue(issues_for(mutate(path, value)))

    def test_pure_root_rejects_crosswalk_object_registry_drift(self):
        with tempfile.TemporaryDirectory(prefix="orthemology-task8-root-") as tmp:
            temp_root = pathlib.Path(tmp)
            for relative in (
                "applications/latent-state-orthing/OSM-DYNAMICS-DEFINITIONS.yaml",
                "applications/latent-state-orthing/OSM-CSCG-ORTHEME-CROSSWALK.yaml",
                "references/source-status.yaml",
            ):
                source = pathlib.Path(ROOT, relative)
                target = temp_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            crosswalk_path = temp_root / (
                "applications/latent-state-orthing/OSM-CSCG-ORTHEME-CROSSWALK.yaml")
            crosswalk = yaml.safe_load(crosswalk_path.read_text(encoding="utf-8"))
            crosswalk["rows"][0]["object_id"] = "unregistered_object"
            crosswalk_path.write_text(
                yaml.safe_dump(crosswalk, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            self.assertTrue(VALIDATOR.validate_osm_root(str(temp_root)))

    def test_pure_root_rejects_crosswalk_role_drift(self):
        with tempfile.TemporaryDirectory(prefix="orthemology-task8-role-root-") as tmp:
            temp_root = pathlib.Path(tmp)
            for relative in (
                "applications/latent-state-orthing/OSM-DYNAMICS-DEFINITIONS.yaml",
                "applications/latent-state-orthing/OSM-CSCG-ORTHEME-CROSSWALK.yaml",
                "references/source-status.yaml",
            ):
                source = pathlib.Path(ROOT, relative)
                target = temp_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            crosswalk_path = temp_root / (
                "applications/latent-state-orthing/OSM-CSCG-ORTHEME-CROSSWALK.yaml")
            crosswalk = yaml.safe_load(crosswalk_path.read_text(encoding="utf-8"))
            crosswalk["rows"][0]["claim_role"] = "orthemological-extension"
            crosswalk_path.write_text(
                yaml.safe_dump(crosswalk, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            self.assertTrue(VALIDATOR.validate_osm_root(str(temp_root)))


if __name__ == "__main__":
    unittest.main()
