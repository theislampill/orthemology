#!/usr/bin/env python3
"""Dynamic-orthing / latent-state learning validator (R7B, Decision 0024).

Deterministic, offline. Enforces the dynamic extension's discipline:
  1. the four update levels are declared and each is exercised by a fixture;
  2. every fixture is well-formed and carries a non-claim;
  3. the load-bearing separations are each asserted by at least one fixture:
     episode-inference != model-learning (DYN-1), world edge != learner edge
     (DYN-2), analysis-version change blocks transport (DYN-3), ortheme
     admission is by ablation not latent split (DYN-4), no one-to-one
     latent->profile map (DYN-5), orthogonality does not define an ortheme
     (DYN-6), endpoint underdetermines mechanism (DYN-7);
  4. the OSM/CSCG source is bounded to exemplification-not-validation and to no
     human/metaphysical/wet-lab transfer (DYN-8 + crosswalk);
  5. the crosswalk rows carry a valid claim_status and non-claims, and never
     define an ortheme by orthogonality.

Establishes no empirical, human, or metaphysical claim.
"""
import io
import os
import re
import sys

try:
    import yaml
    import jsonschema
    import json
except ImportError as e:
    print("FATAL: requires pyyaml + jsonschema:", e)
    sys.exit(2)

# SEMANTIC guard (R7C, audit B19-2): a latent/model object may be a VEHICLE for
# orthemic distinctions but is never an ortheme "by declaration". This catches
# the tamper probe "latent model state z_t IS an ortheme by declaration".
# Negated forms ("is NOT an ortheme", "not define an ortheme") do not match.
ORTHEME_ASSERT = re.compile(r"\b(is|are|becomes?|declared)\s+(an?\s+)?orthemes?\b", re.I)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "applications/latent-state-orthing"
FAILS = []
LEVELS = {"episode-inference", "representation-learning", "repertoire-revision",
          "analysis-version-change"}
CLAIM_STATUS = {"source-report", "model-mechanics", "synthesis", "orthemology-extension"}

TASK8_OBJECTS = {
    "world_task_state": ("world-task-state", "source-reported"),
    "concrete_occurrence": ("concrete-occurrence", "project"),
    "biological_sensory_observation": ("biological-sensory-observation", "source-reported"),
    "model_observation_symbol": ("model-observation-symbol", "source-reported"),
    "biological_single_cell_response": ("biological-single-cell-response", "source-reported"),
    "biological_population_representation": ("biological-population-representation", "source-reported"),
    "cscg_clone_latent_state": ("cscg-clone-latent-state", "source-reported"),
    "latent_posterior": ("latent-posterior", "source-reported"),
    "model_parameter_state": ("model-parameter-state", "source-reported"),
    "model_representation_output": ("model-representation-output", "source-reported"),
    "derived_representation_geometry": ("derived-representation-geometry", "project"),
    "inferred_orthemic_profile": ("inferred-orthemic-profile", "project"),
    "actual_orthemic_profile": ("actual-orthemic-profile", "project"),
}
TASK8_RELATIONS = {
    "rel_world_observation": (
        "world_task_state", "generates", "biological_sensory_observation", "source-reported"),
    "rel_symbol_abstraction": (
        "model_observation_symbol", "abstracts", "biological_sensory_observation", "source-reported"),
    "rel_observation_response": (
        "biological_sensory_observation", "elicits-measured",
        "biological_single_cell_response", "source-reported"),
    "rel_population_aggregation": (
        "biological_population_representation", "aggregates",
        "biological_single_cell_response", "source-reported"),
    "rel_clone_emission": (
        "cscg_clone_latent_state", "deterministically-emits",
        "model_observation_symbol", "source-reported"),
    "rel_posterior_support": (
        "latent_posterior", "ranges-over", "cscg_clone_latent_state", "source-reported"),
    "rel_parameter_output": (
        "model_parameter_state", "generates", "model_representation_output", "source-reported"),
    "rel_output_geometry": (
        "derived_representation_geometry", "derived-from",
        "model_representation_output", "project"),
    "rel_latent_profile": (
        "cscg_clone_latent_state", "partially-relates-to",
        "inferred_orthemic_profile", "project"),
}
TASK8_METHODS = {
    "baum_welch_em": {
        "model_families": ["cscg"], "role": "likelihood-fit",
        "process_class": "expectation-maximization", "sequence": 1,
        "primary_cscg_fit": True, "phrase": "Baum-Welch expectation-maximization",
        "evidence_access_status": "article-text",
    },
    "viterbi_training": {
        "model_families": ["cscg"], "role": "transition-refinement",
        "process_class": "viterbi-training", "sequence": 2,
        "primary_cscg_fit": False, "phrase": "Viterbi training",
        "evidence_access_status": "article-text",
    },
    "map_decode": {
        "model_families": ["cscg"], "role": "latent-assignment-decode",
        "process_class": "max-product-backtrace", "sequence": 3,
        "primary_cscg_fit": False, "phrase": "MAP decode",
        "evidence_access_status": "pinned-official-code",
    },
    "bptt": {
        "model_families": ["vanilla-rnn"], "role": "gradient-computation",
        "process_class": "backpropagation-through-time", "sequence": 1,
        "primary_cscg_fit": False, "phrase": "backpropagation through time",
        "evidence_access_status": "article-text",
    },
    "adam": {
        "model_families": ["vanilla-rnn", "lstm", "transformer"],
        "role": "parameter-optimizer", "process_class": "gradient-optimizer",
        "sequence": 2, "primary_cscg_fit": False, "phrase": "Adam",
        "evidence_access_status": "article-text",
    },
    "cross_entropy": {
        "model_families": ["vanilla-rnn", "lstm", "transformer"],
        "role": "objective", "process_class": "cross-entropy", "sequence": 0,
        "primary_cscg_fit": False, "phrase": "cross-entropy",
        "evidence_access_status": "article-text",
    },
    "local_hebbian_timing": {
        "model_families": ["hebbian-rnn"], "role": "local-timing-weight-update",
        "process_class": "local-hebbian", "sequence": 1,
        "primary_cscg_fit": False, "phrase": "local timing-based Hebbian update",
        "evidence_access_status": "article-text",
    },
}
TASK8_CODE_COMMIT = "c1d1788b54c737efe24402e02762eee10da0d0d7"
TASK8_EXTRACTION_SHA256 = "0D097CBA7BBB25A949E2BF95AF28B5A2259BD8D60B0E5FAC5A74CDF7D05AA814"
TASK8_FORBIDDEN_PROMOTIONS = {
    "Orthemology", "candidate terminology", "human noetics", "fitrah",
    "metaphysics", "Necessary Being", "divine attributes", "divine Speech",
    "theology",
}


def _as_mapping(value, path, issues):
    if not isinstance(value, dict):
        issues.append("%s must be a mapping" % path)
        return {}
    return value


def _as_list(value, path, issues):
    if not isinstance(value, list):
        issues.append("%s must be a list" % path)
        return []
    return value


def _string_set(value, path, issues):
    rows = _as_list(value, path, issues)
    strings = set()
    for index, item in enumerate(rows):
        if not isinstance(item, str) or not item:
            issues.append("%s[%d] must be a nonempty string" % (path, index))
        else:
            strings.add(item)
    return rows, strings


def validate_osm_mapping(mapping):
    """Pure Task 8 contract validation; returns bounded path diagnostics."""
    issues = []
    doc = _as_mapping(mapping, "$", issues)
    if doc.get("schema") != "orthemology-osm-task8-contract-v1":
        issues.append("$.schema must be orthemology-osm-task8-contract-v1")

    objects = _as_list(doc.get("objects"), "$.objects", issues)
    object_rows = {}
    for index, value in enumerate(objects):
        row = _as_mapping(value, "$.objects[%d]" % index, issues)
        object_id = row.get("id")
        if not isinstance(object_id, str) or not object_id:
            issues.append("$.objects[%d].id must be a nonempty string" % index)
            continue
        if object_id in object_rows:
            issues.append("$.objects[%d].id duplicates %s" % (index, object_id))
        object_rows[object_id] = row
    if set(object_rows) != set(TASK8_OBJECTS):
        issues.append("$.objects ids must equal the exact Task 8 typed-owner namespace")
    for object_id, (object_type, ownership) in TASK8_OBJECTS.items():
        row = object_rows.get(object_id, {})
        if row.get("type") != object_type:
            issues.append("$.objects[%s].type must be %s" % (object_id, object_type))
        if row.get("ownership") != ownership:
            issues.append("$.objects[%s].ownership must be %s" % (object_id, ownership))

    relations = _as_list(doc.get("relations"), "$.relations", issues)
    relation_rows = {}
    for index, value in enumerate(relations):
        row = _as_mapping(value, "$.relations[%d]" % index, issues)
        relation_id = row.get("id")
        if not isinstance(relation_id, str) or not relation_id:
            issues.append("$.relations[%d].id must be a nonempty string" % index)
            continue
        if relation_id in relation_rows:
            issues.append("$.relations[%d].id duplicates %s" % (index, relation_id))
        relation_rows[relation_id] = row
        for endpoint in ("subject", "object"):
            endpoint_value = row.get(endpoint)
            if not isinstance(endpoint_value, str) or endpoint_value not in object_rows:
                issues.append("$.relations[%s].%s must resolve to an object id"
                              % (relation_id, endpoint))
        if row.get("identity") is not False:
            issues.append("$.relations[%s].identity must be false" % relation_id)
        if row.get("predicate") in {"identity", "identical", "identical-to", "equals"}:
            issues.append("$.relations[%s] may not assert cross-object identity" % relation_id)
    if set(relation_rows) != set(TASK8_RELATIONS):
        issues.append("$.relations ids must equal the exact Task 8 typed-relation set")
    for relation_id, expected in TASK8_RELATIONS.items():
        row = relation_rows.get(relation_id, {})
        actual = (
            row.get("subject"), row.get("predicate"), row.get("object"),
            row.get("ownership"))
        if actual != expected:
            issues.append("$.relations[%s] does not match its typed relation" % relation_id)

    identities = _as_list(doc.get("asserted_identities"), "$.asserted_identities", issues)
    for index, value in enumerate(identities):
        pair = _as_list(value, "$.asserted_identities[%d]" % index, issues)
        if len(pair) != 2 or any(
                not isinstance(item, str) or item not in object_rows for item in pair):
            issues.append("$.asserted_identities[%d] must resolve exactly two object ids" % index)
        elif pair[0] != pair[1]:
            issues.append("$.asserted_identities[%d] may not collapse distinct typed objects" % index)

    methods = _as_list(doc.get("method_roles"), "$.method_roles", issues)
    method_rows = {}
    for index, value in enumerate(methods):
        row = _as_mapping(value, "$.method_roles[%d]" % index, issues)
        method_id = row.get("id")
        if not isinstance(method_id, str) or not method_id:
            issues.append("$.method_roles[%d].id must be a nonempty string" % index)
            continue
        if method_id in method_rows:
            issues.append("$.method_roles[%d].id duplicates %s" % (index, method_id))
        method_rows[method_id] = row
    if set(method_rows) != set(TASK8_METHODS):
        issues.append("$.method_roles ids must equal the exact Task 8 method set")
    for method_id, expected in TASK8_METHODS.items():
        row = method_rows.get(method_id, {})
        for field, expected_value in expected.items():
            if row.get(field) != expected_value:
                issues.append("$.method_roles[%s].%s must be %r"
                              % (method_id, field, expected_value))
        locator = row.get("source_locator")
        if not isinstance(locator, str) or not locator.strip():
            issues.append("$.method_roles[%s].source_locator must be nonempty" % method_id)
        elif expected["evidence_access_status"] == "article-text":
            if "10.1038/s41586-024-08548-w" not in locator:
                issues.append("$.method_roles[%s] article locator must name the DOI" % method_id)
        elif TASK8_CODE_COMMIT not in locator:
            issues.append("$.method_roles[%s] code locator must name the pinned commit" % method_id)

    comparison = _as_mapping(doc.get("comparison"), "$.comparison", issues)
    endpoint = _as_mapping(comparison.get("endpoint"), "$.comparison.endpoint", issues)
    if endpoint.get("criterion") != "similar-reported-final-representational-structure":
        issues.append("$.comparison.endpoint.criterion must declare bounded similarity")
    for field in ("exact_identity", "cross_model_parameter_equality", "mechanism_inferred"):
        if endpoint.get(field) is not False:
            issues.append("$.comparison.endpoint.%s must be false" % field)

    trajectory = _as_mapping(comparison.get("trajectory"), "$.comparison.trajectory", issues)
    if trajectory.get("claim") != "cscg-consistently-matched-reported-decorrelation-order":
        issues.append("$.comparison.trajectory.claim must name the reported order match")
    if trajectory.get("scope") != "among-tested-models-under-reported-evaluation":
        issues.append("$.comparison.trajectory.scope must be among-tested-models-under-reported-evaluation")
    for field in ("universal_uniqueness", "unique_biological_mechanism"):
        if trajectory.get(field) is not False:
            issues.append("$.comparison.trajectory.%s must be false" % field)
    if trajectory.get("further_research_required") is not True:
        issues.append("$.comparison.trajectory.further_research_required must be true")

    performance = _as_mapping(comparison.get("performance"), "$.comparison.performance", issues)
    if performance.get("high_performance_without_global_orthogonalization") is not True:
        issues.append("$.comparison.performance must preserve the high-performance nonorthogonal control")
    required_controls = {"relu-rnn", "sigmoid-rnn", "lstm", "transformer"}
    controls, control_set = _string_set(
        performance.get("nonorthogonal_controls"),
        "$.comparison.performance.nonorthogonal_controls", issues)
    if control_set != required_controls or len(controls) != len(required_controls):
        issues.append("$.comparison.performance.nonorthogonal_controls must preserve all four controls")
    for field in ("all_non_cscg_failed", "geometry_necessary"):
        if performance.get(field) is not False:
            issues.append("$.comparison.performance.%s must be false" % field)

    adaptation = _as_mapping(comparison.get("adaptation"), "$.comparison.adaptation", issues)
    if adaptation.get("subject") != "biological-ca1-representations":
        issues.append("$.comparison.adaptation.subject must remain biological CA1 representations")
    _condition_rows, condition_set = _string_set(
        adaptation.get("conditions"), "$.comparison.adaptation.conditions", issues)
    if condition_set != {"novel-indicator-cues", "stretched-track-segments"}:
        issues.append("$.comparison.adaptation.conditions must preserve both reported alterations")
    _interpretation_rows, interpretation_set = _string_set(
        adaptation.get("interpretations"), "$.comparison.adaptation.interpretations", issues)
    if interpretation_set != {"new-state-creation", "observation-rebinding-to-existing-state"}:
        issues.append("$.comparison.adaptation.interpretations must preserve both live alternatives")
    if adaptation.get("model_response") != "future-work":
        issues.append("$.comparison.adaptation.model_response must remain future-work")
    if _as_list(adaptation.get("promotes_to"), "$.comparison.adaptation.promotes_to", issues):
        issues.append("$.comparison.adaptation.promotes_to must remain empty")

    custody = _as_mapping(doc.get("source_custody"), "$.source_custody", issues)
    if custody.get("doi") != "10.1038/s41586-024-08548-w":
        issues.append("$.source_custody.doi must name the Nature article")
    article_loci = _as_list(custody.get("article_loci"), "$.source_custody.article_loci", issues)
    if not article_loci or any(not isinstance(item, str) or not item.strip() for item in article_loci):
        issues.append("$.source_custody.article_loci must contain exact nonempty article loci")
    access = _as_mapping(
        custody.get("local_access_copy"), "$.source_custody.local_access_copy", issues)
    if access.get("sha256") != TASK8_EXTRACTION_SHA256:
        issues.append("$.source_custody.local_access_copy.sha256 must match retained custody")
    if access.get("locator_role") != "custody-only":
        issues.append("$.source_custody.local_access_copy.locator_role must be custody-only")
    for field in ("sole_public_evidence", "extraction_lines_are_journal_pagination"):
        if access.get(field) is not False:
            issues.append("$.source_custody.local_access_copy.%s must be false" % field)
    code = _as_mapping(custody.get("official_code"), "$.source_custody.official_code", issues)
    if code.get("repository") != "sprustonlab/OSM_Paper_Figures":
        issues.append("$.source_custody.official_code.repository must name the official repository")
    if code.get("commit") != TASK8_CODE_COMMIT:
        issues.append("$.source_custody.official_code.commit must equal the pinned commit")
    if not isinstance(code.get("map_decode_locator"), str) or "chmm_actions.py" not in code.get(
            "map_decode_locator", ""):
        issues.append("$.source_custody.official_code.map_decode_locator must name chmm_actions.py")

    boundaries = _as_mapping(doc.get("claim_boundaries"), "$.claim_boundaries", issues)
    if boundaries.get("overall_claim_role") != "computational-analogy":
        issues.append("$.claim_boundaries.overall_claim_role must be computational-analogy")
    if boundaries.get("content_kind") != "model-comparison":
        issues.append("$.claim_boundaries.content_kind must be model-comparison")
    if boundaries.get("evidence_access_status") != "article-text-and-pinned-code":
        issues.append("$.claim_boundaries.evidence_access_status must preserve both evidence roles")
    geometry = _as_mapping(
        boundaries.get("geometry_definition"), "$.claim_boundaries.geometry_definition", issues)
    if geometry != {
            "content_kind": "project-extension",
            "claim_role": "orthemological-extension",
            "evidence_access_status": "project-owned-definition"}:
        issues.append("$.claim_boundaries.geometry_definition must remain a project extension")
    _supported_rows, supported = _string_set(
        boundaries.get("supported_domains"), "$.claim_boundaries.supported_domains", issues)
    forbidden_supported = sorted(supported & TASK8_FORBIDDEN_PROMOTIONS)
    if forbidden_supported:
        issues.append("$.claim_boundaries.supported_domains contains forbidden promotions: %s"
                      % forbidden_supported)
    if supported:
        issues.append("$.claim_boundaries.supported_domains must remain empty; "
                      "computational analogy supplies no cross-domain support")
    if boundaries.get("biological_or_wet_lab_procedure_imported") is not False:
        issues.append("$.claim_boundaries.biological_or_wet_lab_procedure_imported must be false")
    promotion_rows, promotions = _string_set(
        boundaries.get("forbidden_promotions"), "$.claim_boundaries.forbidden_promotions", issues)
    if promotions != TASK8_FORBIDDEN_PROMOTIONS or len(promotion_rows) != len(
            TASK8_FORBIDDEN_PROMOTIONS):
        issues.append("$.claim_boundaries.forbidden_promotions must equal the complete firewall")
    return issues


def validate_osm_root(root):
    """Pure repository-root validation used by tests and the CLI."""
    issues = []

    def read_yaml(relative):
        path = os.path.join(root, relative)
        try:
            with io.open(path, encoding="utf-8") as handle:
                return yaml.safe_load(handle.read())
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            issues.append("%s could not be parsed: %s" % (relative, exc))
            return {}

    definitions = _as_mapping(
        read_yaml(APP + "/OSM-DYNAMICS-DEFINITIONS.yaml"),
        APP + "/OSM-DYNAMICS-DEFINITIONS.yaml", issues)
    issues.extend(validate_osm_mapping(definitions.get("osm_task8_contract")))

    crosswalk = _as_mapping(
        read_yaml(APP + "/OSM-CSCG-ORTHEME-CROSSWALK.yaml"),
        APP + "/OSM-CSCG-ORTHEME-CROSSWALK.yaml", issues)
    if crosswalk.get("task8_contract_ref") != "OSM-DYNAMICS-DEFINITIONS.yaml#osm_task8_contract":
        issues.append("crosswalk.task8_contract_ref must resolve to the Task 8 contract")
    crosswalk_rows = _as_list(crosswalk.get("rows"), "crosswalk.rows", issues)
    crosswalk_object_ids = [
        row.get("object_id") for row in crosswalk_rows
        if isinstance(row, dict) and row.get("object_id") is not None
    ]
    if (len(crosswalk_object_ids) != len(TASK8_OBJECTS)
            or any(not isinstance(object_id, str) for object_id in crosswalk_object_ids)
            or set(crosswalk_object_ids) != set(TASK8_OBJECTS)):
        issues.append("crosswalk object_id rows must represent every Task 8 object exactly once")
    crosswalk_by_object = {
        row.get("object_id"): row for row in crosswalk_rows
        if isinstance(row, dict) and isinstance(row.get("object_id"), str)
    }
    biological_ids = {
        "world_task_state", "biological_sensory_observation",
        "biological_single_cell_response", "biological_population_representation",
    }
    model_ids = {
        "model_observation_symbol", "cscg_clone_latent_state", "latent_posterior",
        "model_parameter_state", "model_representation_output",
    }
    project_ids = {
        "concrete_occurrence", "inferred_orthemic_profile", "actual_orthemic_profile",
    }
    expected_crosswalk_roles = {}
    for object_id in biological_ids:
        expected_crosswalk_roles[object_id] = (
            "biological-source-report", "primary-text-verified", "article-text")
    for object_id in model_ids:
        expected_crosswalk_roles[object_id] = (
            "model-mechanics", "primary-text-verified", "article-text")
    for object_id in project_ids:
        expected_crosswalk_roles[object_id] = (
            "project-extension", "orthemological-extension", "project-owned-definition")
    expected_crosswalk_roles["derived_representation_geometry"] = (
        "project-extension", "computational-analogy",
        "article-text-and-project-owned-definition")
    for object_id, expected in expected_crosswalk_roles.items():
        row = crosswalk_by_object.get(object_id, {})
        actual = (
            row.get("content_kind"), row.get("claim_role"),
            row.get("evidence_access_status"))
        if actual != expected:
            issues.append("crosswalk object %s must preserve content kind, claim role, "
                          "and evidence-access role" % object_id)

    registry = _as_mapping(
        read_yaml("references/source-status.yaml"), "references/source-status.yaml", issues)
    claims = _as_list(registry.get("claims"), "references/source-status.yaml.claims", issues)
    lat1 = next((row for row in claims if isinstance(row, dict) and row.get("id") == "LAT-1"), {})
    task8_custody = _as_mapping(lat1.get("task8_custody"), "LAT-1.task8_custody", issues)
    if task8_custody.get("access_copy_sha256") != TASK8_EXTRACTION_SHA256:
        issues.append("LAT-1.task8_custody.access_copy_sha256 must match the retained extraction")
    if task8_custody.get("official_code_commit") != TASK8_CODE_COMMIT:
        issues.append("LAT-1.task8_custody.official_code_commit must match the pinned code")
    if task8_custody.get("extraction_lines_are_journal_pagination") is not False:
        issues.append("LAT-1.task8_custody extraction lines may not be journal pagination")
    if task8_custody.get("map_decode_evidence_access_status") != "pinned-official-code":
        issues.append("LAT-1.task8_custody MAP decode must remain pinned-official-code evidence")
    return issues


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def load(rel):
    return yaml.safe_load(io.open(os.path.join(ROOT, rel), encoding="utf-8").read())


def main():
    task8_issues = validate_osm_root(ROOT)
    check("Task 8 pure mapping/root contract", not task8_issues,
          "; ".join(task8_issues[:12]))

    fx = load(APP + "/DYNAMIC-FIXTURES.yaml")
    cw = load(APP + "/OSM-CSCG-ORTHEME-CROSSWALK.yaml")

    # 1. update levels
    declared = set(fx.get("update_levels", []))
    check("all four update levels declared", declared == LEVELS,
          "declared=%s" % sorted(declared))
    fixtures = fx.get("fixtures", [])
    used = {f.get("level") for f in fixtures}
    check("every update level is exercised by a fixture", LEVELS <= used,
          "missing: %s" % sorted(LEVELS - used))

    # 2. fixture well-formedness
    ids = [f.get("id") for f in fixtures]
    for f in fixtures:
        fid = f.get("id", "?")
        for field in ("id", "name", "level", "scenario", "distinction", "forbids", "non_claim"):
            check("fixture %s has %s" % (fid, field), bool(str(f.get(field, "")).strip()))
        check("fixture %s level is valid" % fid, f.get("level") in LEVELS, f.get("level"))

    # 3. required fixtures present (R7C failure families DYN-10..DYN-20;
    # Task 8 method/performance/adaptation controls DYN-21..DYN-24)
    for n in range(1, 25):
        req = "DYN-%d" % n
        check("fixture %s present" % req, req in ids)
    task8_fixture_blob = " ".join(
        str(f) for f in fixtures if f.get("id") in {"DYN-21", "DYN-22", "DYN-23", "DYN-24"})
    for required_term in (
            "Baum-Welch", "Viterbi training", "MAP decode", "BPTT", "Adam",
            "cross-entropy", "Hebbian", "high prediction performance",
            "future work"):
        check("Task 8 neighboring controls preserve %s" % required_term,
              required_term.lower() in task8_fixture_blob.lower())

    # 3b. update coupling (R7C B7; R7D B34/P7): each level is GOVERNED and now
    #     SCHEMA-VALIDATED with STRUCTURED, GATED transport — silent transport fails.
    coupling = load(APP + "/UPDATE-COUPLING.yaml")
    uc_schema = json.loads(io.open(os.path.join(ROOT, APP, "UPDATE-COUPLING.schema.json"), encoding="utf-8").read())
    try:
        jsonschema.validate(coupling, uc_schema)
        check("update-coupling validates against its schema", True)
    except jsonschema.ValidationError as e:
        check("update-coupling validates against its schema", False, e.message)
    ct = {t["level"]: t for t in coupling.get("transitions", [])}
    check("update coupling covers all four levels", set(ct) == LEVELS, str(sorted(ct)))
    for lvl, t in sorted(ct.items()):
        for field in ("trigger", "authority", "input", "version", "transport", "calibration",
                      "catastrophic_forgetting_check", "invalidated", "reopening", "rollback"):
            check("coupling[%s] declares %s" % (lvl, field), bool(t.get(field)))
        # P7: transport is a gated object; silence/blanket transport is forbidden
        tr = t.get("transport", {})
        check("coupling[%s] transport requires an argument (no silent/universal transport, P7)" % lvl,
              isinstance(tr, dict) and tr.get("default") == "no-transport-without-argument"
              and tr.get("argument_required") is True,
              repr(tr if not isinstance(tr, dict) else {k: tr.get(k) for k in ("default", "argument_required")}))
    rr = ct.get("repertoire-revision", {})
    check("repertoire revision changes the DECLARED repertoire, not worldly facts",
          "represent" in str(rr.get("non_claim", "")).lower()
          and "not worldly" in str(rr.get("non_claim", "")).lower())

    # 3c. OSM dynamics definitions (R7D B31/B32/B33/B35): Geom_A, ProfileOf_A, merger
    defs = load(APP + "/OSM-DYNAMICS-DEFINITIONS.yaml")
    geo = defs.get("geometry_definition", {})
    for f in ("representation_extraction", "metric", "alignment", "permutation_invariance",
              "rotation_scale_handling", "uncertainty", "evaluated_distribution"):
        check("Geom_A defines %s (B31)" % f, bool(str(geo.get(f, "")).strip()))
    pr = defs.get("profile_relation", {})
    for f in ("relation_status", "evidence_basis", "analysis_version", "cardinality", "uncertainty", "transport"):
        check("ProfileOf_A defines %s (B32)" % f, bool(str(pr.get(f, "")).strip()))
    check("ProfileOf_A denies latent==ortheme-by-declaration",
          any("not an ortheme" in nc.lower() or "by declaration" in nc.lower() for nc in pr.get("non_claims", [])))
    mc = defs.get("merger_contrast", {})
    for f in ("merge_operation", "evaluation_distribution", "horizon", "action_loss_surfaces",
              "hard_constraints", "uncertainty_interval", "tolerance_source", "admission_rule"):
        check("merger contrast defines %s (B33)" % f, bool(str(mc.get(f, "")).strip()))
    om = defs.get("osm_task8_contract", {}).get("objects", [])
    check("OSM object map keeps the exact 13 typed objects (Task 8)",
          len(om) == 13 and len({row.get("id") for row in om if isinstance(row, dict)}) == 13,
          "got %d rows" % len(om))

    # 4. OSM boundary: DYN-8 forbids validation-use + wet-lab + metaphysical transfer
    dyn8 = next((f for f in fixtures if f.get("id") == "DYN-8"), {})
    blob8 = (str(dyn8.get("forbids", "")) + " " + str(dyn8.get("non_claim", ""))).lower()
    check("DYN-8 forbids citing OSM as validation/support", "support" in blob8 or "validation" in blob8 or "evidence" in blob8)
    check("DYN-8 forbids wet-lab/biological import", "wet-lab" in blob8 or "biological" in blob8)
    check("DYN-8 forbids human/metaphysical transfer",
          ("metaphys" in blob8) and ("human" in blob8 or "noetic" in blob8))

    # 5. crosswalk discipline
    check("crosswalk overall_status is 'not validation'",
          "not validation" in str(cw.get("overall_status", "")).lower())
    rows = cw.get("rows", [])
    check("crosswalk has rows", len(rows) >= 6)
    for r in rows:
        rid = str(r.get("osm_concept", "?"))[:36]
        check("row '%s' claim_status valid" % rid, r.get("claim_status") in CLAIM_STATUS,
              r.get("claim_status"))
        check("row '%s' has non_claims" % rid, bool(r.get("non_claims")))
    # the orthogonality row must deny ortheme-definition-by-orthogonality
    orth = [r for r in rows if "orthogonal" in str(r.get("osm_concept", "")).lower()
            or "decorrelat" in str(r.get("osm_concept", "")).lower()]
    check("an orthogonalization row exists", bool(orth))
    if orth:
        nc = " ".join(orth[0].get("non_claims", [])).lower()
        check("orthogonalization row denies defining an ortheme",
              "not define an ortheme" in nc or "does not define" in nc or "not sufficient" in nc)
    # an endpoint-underdetermines row must exist and deny mechanism identification
    endp = [r for r in rows if "endpoint" in str(r.get("osm_concept", "")).lower()
            or "trajectory" in str(r.get("osm_concept", "")).lower()]
    check("endpoint-underdetermines-mechanism row exists", bool(endp))

    # SEMANTIC: no row asserts a latent/model object IS an ortheme (B19-2)
    for r in rows:
        obj = str(r.get("orthemology_object", ""))
        m = ORTHEME_ASSERT.search(obj)
        check("row '%s' does not assert a latent/model object IS an ortheme"
              % str(r.get("osm_concept", "?"))[:28], m is None,
              "found %r" % (m.group(0) if m else ""))
    # the latent-state row must explicitly deny ortheme status and require ablation
    lat = [r for r in rows if "latent" in str(r.get("osm_concept", "")).lower()
           and "state" in str(r.get("osm_concept", "")).lower()]
    check("a latent-state row exists", bool(lat))
    if lat:
        nc = " ".join(lat[0].get("non_claims", [])).lower()
        check("latent-state row denies ortheme status (admission is by ablation)",
              "not an ortheme" in nc and "ablation" in nc)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
