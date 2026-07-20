#!/usr/bin/env python3
"""LS-1..LS-7 latent-state fixture validator (Decision 0015).

Checks, per fixture: the six-way typed distinction is populated and pairwise
non-identical (m != z != x != b != y != p-hat); the latent layer is declared
NON-PRIMITIVE; any declared verdicts use registry semantic IDs and the registry
status enum; metaorthemma binding respects the M1 material-binding criteria and
the zero-burden rule (no material binding => no token => GOV_TOKEN_ADEQUATE
not-applicable). Also enforces the per-fixture structural expectations for
LS-1..LS-7 and the TEN anti-conflation assertions, failing closed if any fixture
asserts an identity Decision 0015 forbids.

Deterministic; no network access; no empirical claim."""
import json
import os
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

REQUIRED_OBJECT_KEYS = [
    "orthemma",
    "observation",
    "latent_candidates",
    "belief_or_posterior",
    "internal_representation",
    "inferred_partial_profile",
]

# The identities Decision 0015 forbids. Every fixture must declare all ten and
# every one must be false. These are not configurable.
FORBIDDEN_CONFLATIONS = [
    "observation_is_occurrence",
    "posterior_is_ground_truth",
    "latent_label_is_ortheme_by_declaration",
    "cluster_is_worldly_state_without_declared_bridge",
    "global_orthogonality_required_for_adequacy",
    "nonorthogonality_proves_state_identity",
    "endpoint_match_proves_mechanism_match",
    "state_label_transported_across_versions",
    "every_cue_remapping_is_a_metaorthemma",
    "one_neuron_is_type_token_identity_of_ortheme",
]

# Per-fixture structural expectations (Decision 0015 sections 2-7).
EXPECTED = {
    "LS-1": {
        "distinction_consequential": True,
        "merge_within_tolerance": False,
        "candidates_remain_plural": True,
        "distinction_dependent_claim_withheld": True,
        "new_orthemic_distinction_licensed": True,
    },
    "LS-2": {
        "distinction_consequential": False,
        "merge_within_tolerance": True,
        "candidates_remain_plural": False,
        "distinction_dependent_claim_withheld": False,
        "new_orthemic_distinction_licensed": False,
    },
    "LS-3": {
        "global_orthogonality_present": False,
        "task_requirements_met": True,
        "pathway_defect_from_geometry_alone": False,
        "geometry_and_pathway_adequacy_distinct": True,
    },
    "LS-4": {
        "endpoint_match": True,
        "trajectory_match": False,
        "mechanism_equivalence_established": False,
        "pathway_equivalence_established": False,
        "trajectory_is_stronger_constraint": True,
    },
    "LS-5": {
        "new_latent_state_created": False,
        "new_orthemic_distinction_licensed": False,
        "provenance_and_version_updated": True,
        "metaorthemma_required": False,
    },
    "LS-6": {
        "inferred_state_is_ground_truth": False,
        "belief_confident_and_incorrect": True,
        "revision_explicit": True,
        "transport_auditable": True,
        "claims_transported_silently": False,
    },
    "LS-7": {
        "representation_continuous": True,
        "discrete_structure_under_A_permitted": True,
        "one_cell_one_type_inference_licensed": False,
        "localization_claim_made": False,
        "element_is_ortheme": False,
    },
}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def main():
    reg = yaml.safe_load(open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8"))
    reg_ids = {v["id"] for v in reg["verdicts"]}
    status_enum = set(reg["status_enum"])

    data = json.load(open(os.path.join(ROOT, "tests", "latent-state-fixtures.json"), encoding="utf-8"))
    fixtures = {f["id"]: f for f in data["fixtures"]}

    check("all seven LS fixtures present",
          set(fixtures) == {"LS-%d" % i for i in range(1, 8)}, str(sorted(fixtures)))
    check("fixture file declares the canonical conflation key list",
          list(data.get("conflation_keys", [])) == FORBIDDEN_CONFLATIONS,
          str(data.get("conflation_keys")))

    for fid, f in sorted(fixtures.items()):
        # --- six-way typed distinction -------------------------------------
        objs = f.get("typed_objects", {})
        missing = [k for k in REQUIRED_OBJECT_KEYS if not objs.get(k)]
        check("%s populates the six typed objects" % fid, not missing, str(missing))
        check("%s declares no object kind outside the typed set" % fid,
              not sorted(set(objs) - set(REQUIRED_OBJECT_KEYS)),
              str(sorted(set(objs) - set(REQUIRED_OBJECT_KEYS))))
        vals = [objs.get(k) for k in REQUIRED_OBJECT_KEYS if objs.get(k)]
        check("%s keeps m != z != x != b != y != p-hat (no two objects identified)" % fid,
              len(set(vals)) == len(vals))

        # --- latent layer is optional and NON-PRIMITIVE ---------------------
        lat = f.get("latent_layer", {})
        check("%s declares the latent layer explicitly" % fid, "declared" in lat)
        check("%s marks the latent layer NON-PRIMITIVE" % fid, lat.get("primitive") is False,
              "primitive=%r" % lat.get("primitive"))

        # --- verdict hygiene ------------------------------------------------
        verdicts = f.get("verdicts", {})
        bad_ids = sorted(set(verdicts) - reg_ids)
        check("%s verdicts use registry semantic IDs" % fid, not bad_ids, str(bad_ids))
        bad_st = sorted({s for s in verdicts.values() if s not in status_enum})
        check("%s verdict statuses use the registry enum" % fid, not bad_st, str(bad_st))

        # --- M1 material binding / zero-burden rule -------------------------
        mo = f.get("metaorthemma", {})
        check("%s states its metaorthemma binding status with a reason" % fid,
              isinstance(mo.get("bound"), bool) and isinstance(mo.get("m1_material_binding"), bool)
              and bool(mo.get("reason")))
        check("%s binds a token only where M1 material-binding criteria are met" % fid,
              mo.get("bound") is (mo.get("m1_material_binding") is True),
              "bound=%r material=%r" % (mo.get("bound"), mo.get("m1_material_binding")))
        if mo.get("bound") is False and "GOV_TOKEN_ADEQUATE" in verdicts:
            check("%s zero-burden rule: GOV_TOKEN_ADEQUATE not-applicable without a token" % fid,
                  verdicts["GOV_TOKEN_ADEQUATE"] == "not-applicable",
                  verdicts["GOV_TOKEN_ADEQUATE"])

        # --- declared expectations -------------------------------------------
        exp = f.get("expected", {})
        want = EXPECTED[fid]
        check("%s declares exactly its required expectation keys" % fid,
              set(exp) == set(want), str(sorted(set(exp) ^ set(want))))
        for k, v in sorted(want.items()):
            check("%s expectation %s == %r" % (fid, k, v), exp.get(k) is v, "got %r" % exp.get(k))

        # --- ANTI-CONFLATION: fail closed -------------------------------------
        ca = f.get("conflation_assertions", {})
        check("%s declares all ten anti-conflation assertions" % fid,
              set(ca) == set(FORBIDDEN_CONFLATIONS),
              str(sorted(set(ca) ^ set(FORBIDDEN_CONFLATIONS))))
        for key in FORBIDDEN_CONFLATIONS:
            check("%s does NOT assert forbidden identity: %s" % (fid, key),
                  ca.get(key) is False, "got %r (must be false)" % ca.get(key))

    # --- cross-fixture structural guarantees --------------------------------
    ls1, ls2, ls3, ls4, ls5, ls6, ls7 = (fixtures["LS-%d" % i] for i in range(1, 8))

    check("LS-1/LS-2 contrast: consequential aliasing vs safe merge",
          ls1["expected"]["distinction_consequential"] is True
          and ls2["expected"]["distinction_consequential"] is False
          and ls1["expected"]["merge_within_tolerance"] is False
          and ls2["expected"]["merge_within_tolerance"] is True)
    check("LS-3 separates representational geometry from pathway adequacy",
          ls3["expected"]["global_orthogonality_present"] is False
          and ls3["expected"]["task_requirements_met"] is True
          and ls3["expected"]["pathway_defect_from_geometry_alone"] is False)
    check("LS-4 endpoint match without mechanism or pathway equivalence",
          ls4["expected"]["endpoint_match"] is True
          and ls4["expected"]["trajectory_match"] is False
          and ls4["expected"]["mechanism_equivalence_established"] is False
          and ls4["expected"]["pathway_equivalence_established"] is False)
    check("LS-5 is an observation/emission rebinding, not a metaorthemma",
          ls5.get("rebinding_category") == "observation-emission-rebinding"
          and ls5["expected"]["metaorthemma_required"] is False
          and ls5["metaorthemma"]["bound"] is False
          and ls5["expected"]["provenance_and_version_updated"] is True)
    check("LS-6 posterior confidence without ground truth; revision explicit and auditable",
          ls6["expected"]["inferred_state_is_ground_truth"] is False
          and ls6["expected"]["belief_confident_and_incorrect"] is True
          and ls6["expected"]["revision_explicit"] is True
          and ls6["expected"]["claims_transported_silently"] is False
          and ls6["verdicts"].get("EVIDENCE_CURRENT") == "fail")
    check("LS-7 negative control: continuous elements, no one-cell-one-type, no localization",
          ls7["expected"]["representation_continuous"] is True
          and ls7["expected"]["one_cell_one_type_inference_licensed"] is False
          and ls7["expected"]["localization_claim_made"] is False
          and ls7["expected"]["element_is_ortheme"] is False)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
