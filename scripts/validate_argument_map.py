#!/usr/bin/env python3
"""Pure structured validator for the Task 9 argument map."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "companion" / "DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml"
SOURCE_STATUS_PATH = ROOT / "references" / "source-status.yaml"
MAX_ISSUES = 100

CLAIM_ROLES = {
    "primary-text-verified",
    "secondary-reconstruction",
    "cross-source-synthesis",
    "orthemological-extension",
    "computational-analogy",
    "creed-internal-inference",
}
SCOPES = {
    "cross-framework-dialectical",
    "athari-taymiyyan-operative",
    "source-bounded-proposed-crosswalk",
}
INFERENCE_TYPES = {
    "analytic",
    "explanatory",
    "computational-analogy",
    "teleological",
    "transcendental-scope-limited",
    "metaphysical-explanatory",
    "modal",
    "metaphysical",
    "creed-internal-teleological",
    "revelational-school-internal",
    "typed-creed-internal-distinction",
    "orthemological-extension",
}
BRIDGE_STATUSES = {
    "bounded",
    "conditional",
    "illustrative-only",
    "held",
    "held-pending-source-custody",
    "revelational",
    "held-pending-individually-verified-lexical-sources",
}
REFERENCE_ROLES = {
    "primary-text",
    "secondary-scholarship",
    "comparative",
    "rival",
    "lexical-reference",
}
NODE_FIELDS = {
    "id",
    "order",
    "label",
    "scope",
    "premises",
    "inference_type",
    "bridge_status",
    "bridge_premise_refs",
    "conclusion",
    "dependencies",
    "claim_role",
    "source_status_refs",
    "evidence_access_status",
    "reference_roles",
    "strongest_objection",
    "rival_exit",
    "warrant_basis",
}
EXPECTED_NODE_IDS = tuple(f"ARG-{index:02d}" for index in range(1, 15))
EXPECTED_LABELS = {
    "ARG-01": "local evaluability",
    "ARG-02": "objective corrigibility",
    "ARG-03": "bounded representational adaptation",
    "ARG-04": "normative proper-function bridge",
    "ARG-05": "underived locus",
    "ARG-06": "intellectual ground",
    "ARG-07": "modal status of the ground",
    "ARG-08": "will",
    "ARG-09": "power",
    "ARG-10": "Wisdom and fittingness",
    "ARG-11": "capacity for disclosure",
    "ARG-12": "actual divine Speech",
    "ARG-13": "Speech bearer classification",
    "ARG-14": "Rabb lexical disambiguation candidate",
}
EXPECTED_DEPENDENCIES = {
    "ARG-01": [],
    "ARG-02": ["ARG-01"],
    "ARG-03": ["ARG-02"],
    "ARG-04": ["ARG-02", "ARG-03"],
    "ARG-05": ["ARG-01"],
    "ARG-06": ["ARG-05"],
    "ARG-07": ["ARG-05", "ARG-06"],
    "ARG-08": ["ARG-06"],
    "ARG-09": ["ARG-08"],
    "ARG-10": ["ARG-04", "ARG-06"],
    "ARG-11": ["ARG-06"],
    "ARG-12": ["ARG-11"],
    "ARG-13": ["ARG-12"],
    "ARG-14": [],
}
EXPECTED_BRIDGE_REFS = {
    "ARG-01": [],
    "ARG-02": ["ARG-01-P1"],
    "ARG-03": [],
    "ARG-04": ["ARG-02-C", "ARG-04-P2"],
    "ARG-05": ["ARG-01-C", "ARG-05-P1"],
    "ARG-06": ["ARG-05-C", "ARG-06-P1"],
    "ARG-07": ["ARG-05-C"],
    "ARG-08": ["ARG-06-C", "ARG-08-P1"],
    "ARG-09": ["ARG-08-C", "ARG-09-P1"],
    "ARG-10": ["ARG-04-C", "ARG-10-P1"],
    "ARG-11": ["ARG-06-C", "ARG-11-P1"],
    "ARG-12": ["ARG-11-C"],
    "ARG-13": ["ARG-12-C"],
    "ARG-14": [],
}
EXPECTED_NODE_TYPES = {
    "ARG-01": ("cross-framework-dialectical", "analytic", "bounded", "stated-premises-and-inference"),
    "ARG-02": ("cross-framework-dialectical", "explanatory", "conditional", "stated-premises-and-inference"),
    "ARG-03": ("cross-framework-dialectical", "computational-analogy", "illustrative-only", "stated-premises-and-inference"),
    "ARG-04": ("cross-framework-dialectical", "teleological", "conditional", "stated-premises-and-inference"),
    "ARG-05": ("cross-framework-dialectical", "transcendental-scope-limited", "conditional", "stated-premises-and-inference"),
    "ARG-06": ("cross-framework-dialectical", "metaphysical-explanatory", "conditional", "stated-premises-and-inference"),
    "ARG-07": ("cross-framework-dialectical", "modal", "held", "stated-premises-and-inference"),
    "ARG-08": ("cross-framework-dialectical", "metaphysical", "conditional", "stated-premises-and-inference"),
    "ARG-09": ("cross-framework-dialectical", "metaphysical", "conditional", "stated-premises-and-inference"),
    "ARG-10": ("athari-taymiyyan-operative", "creed-internal-teleological", "held-pending-source-custody", "stated-premises-and-inference"),
    "ARG-11": ("cross-framework-dialectical", "metaphysical", "conditional", "stated-premises-and-inference"),
    "ARG-12": ("athari-taymiyyan-operative", "revelational-school-internal", "revelational", "revelation-and-declared-creed-internal-inference"),
    "ARG-13": ("athari-taymiyyan-operative", "typed-creed-internal-distinction", "bounded", "revelation-and-declared-creed-internal-inference"),
    "ARG-14": ("source-bounded-proposed-crosswalk", "orthemological-extension", "held-pending-individually-verified-lexical-sources", "stated-premises-and-inference"),
}
ALLOWED_SOURCE_CONTRACTS = {
    "ARG-01": {
        ("orthemological-extension", ("EXT-1",), (("EXT-1", "comparative"),)),
        ("secondary-reconstruction", ("ELT-1",), (("ELT-1", "secondary-scholarship"),)),
    },
    "ARG-02": {("orthemological-extension", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-03": {("computational-analogy", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-04": {("cross-source-synthesis", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-05": {("orthemological-extension", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-06": {("cross-source-synthesis", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-07": {("cross-source-synthesis", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-08": {("cross-source-synthesis", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-09": {("cross-source-synthesis", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-10": {("creed-internal-inference", (), ())},
    "ARG-11": {("cross-source-synthesis", ("EXT-1",), (("EXT-1", "comparative"),))},
    "ARG-12": {("creed-internal-inference", ("ATH-1", "ATH-2"), (("ATH-1", "primary-text"), ("ATH-2", "primary-text")))},
    "ARG-13": {("creed-internal-inference", ("ATH-1", "ATH-2", "ATH-3", "ATH-4", "ATH-5"), (("ATH-1", "primary-text"), ("ATH-2", "primary-text"), ("ATH-3", "primary-text"), ("ATH-4", "primary-text"), ("ATH-5", "secondary-scholarship")))},
    "ARG-14": {("orthemological-extension", ("EXT-1",), (("EXT-1", "lexical-reference"),))},
}
EXPECTED_CLAIMS = {
    "ARG-01-P1": "placements under a declared analysis have determinate correctness conditions",
    "ARG-01-C": "a placement is evaluable as correct or incorrect under its declared analysis",
    "ARG-02-P1": "some incorrect placements admit evidence-sensitive revision toward a correct placement",
    "ARG-02-C": "some cases admit objectively rankable correction paths without a scalar or differentiable gradient",
    "ARG-03-P1": "one reported task-model comparison exhibits bounded progressive adaptation and representational differentiation",
    "ARG-03-C": "constrained learning can illustrate access to a lower-level correction task without metaphysical promotion",
    "ARG-04-P1": "truth-linked fittingness is not supplied by empirical adaptation alone",
    "ARG-04-P2": "irreducible teleology would supply a distinct normative bridge if defended",
    "ARG-04-C": "proper-function normativity follows only conditionally on an independently defended teleological premise",
    "ARG-05-P1": "an intelligible norm-governed construction of all intelligibility presupposes the conditions it purports to construct",
    "ARG-05-C": "some conditions of objective evaluability are underived within accounts that model origination as intelligible norm-governed transition",
    "ARG-06-P1": "adequacy to meanings and norms would require an intellective ground if causal adequacy to intelligibility is accepted",
    "ARG-06-C": "an intellectual ground follows only conditionally and does not refute an impersonal or Platonic terminus",
    "ARG-07-P1": "no complete common-premise derivation from underived to metaphysically necessary is encoded",
    "ARG-07-C": "necessity remains a distinct unresolved joint rather than an analytic relabeling",
    "ARG-08-P1": "contingent selection would require a selector only if brute contingency is rejected",
    "ARG-08-C": "Will follows only conditionally on the selection-requires-selector premise",
    "ARG-09-P1": "selection without efficacy institutes nothing",
    "ARG-09-C": "Power follows conditionally if the Will joint is granted",
    "ARG-10-P1": "the declared Athari Taymiyyan route proposes that divine acts and commands proceed for wise ends, but its underlying works require individual custody before citation here",
    "ARG-10-P2": "the common-premise fittingness-to-Wisdom inference remains unestablished",
    "ARG-10-C": "the Athari route is structurally represented with exact inferential limits but its positive source assertion and the cross-framework bridge both remain held",
    "ARG-11-P1": "a proportionate-causality premise for perfection-relevant capacities would exclude intrinsic muteness",
    "ARG-11-C": "at most capacity for determinate disclosure follows and no actual Speech event follows",
    "ARG-12-P1": "revelation identifies Allah as actually speaking within the declared Athari route",
    "ARG-12-C": "actual divine Speech is a revelational creed-internal conclusion and not a philosophical entailment of capacity",
    "ARG-13-P1": "bearer identity must be fixed before created or uncreated status is predicated",
    "ARG-13-C": "seven distinct bearers preserve revealed Arabic wording as Allah's Speech while creaturely acts voices media and reception remain created",
    "ARG-14-P1": "a contextual token may have multiple candidate senses selected through evidence and interpretive rules",
    "ARG-14-C": "token sense rule context binding and disambiguation may be modeled as distinct orthemological layers without theological entailment",
}
EXPECTED_CLAIM_PLACEMENTS = {
    node_id: {
        "premises": frozenset(
            claim_id
            for claim_id in EXPECTED_CLAIMS
            if claim_id.startswith(f"{node_id}-P")
        ),
        "conclusion": f"{node_id}-C",
    }
    for node_id in EXPECTED_NODE_IDS
}
EXPECTED_BOUNDARIES = {
    "BOUND-CROSS-FRAMEWORK-NOT-TRIBUNAL": ("scope-firewall", "cross_framework_policy.warrant_role"),
    "BOUND-WISDOM-HELD": ("source-hold", "common_premise_fittingness_to_wisdom"),
    "BOUND-RABB-NONCONJUNCTIVE": ("non-entailment", "rabb_lexical_crosswalk.lexical_range_semantics"),
    "BOUND-RABB-NONTHEOLOGICAL": ("non-entailment", "rabb_lexical_crosswalk.theological_reach"),
    "BOUND-RABB-DEPENDENT-CREATURE": ("non-entailment", "rabb_lexical_crosswalk.creaturely_completion"),
    "BOUND-PROPER-FUNCTION-MODERN": ("scope-firewall", "proper_function_boundary"),
    "BOUND-FITRAH-QUALITATIVE": ("scope-firewall", "fitrah_boundary"),
    "BOUND-DIVINE-NOT-FORMAL-OBJECT": ("scope-firewall", "divine_formal_object_policy"),
    "BOUND-OSM-DAEE-NONWARRANT": ("non-entailment", "non_entailments.OSM-and-DAEE"),
    "BOUND-EMPIRICAL-NOT-NORMATIVITY": ("non-entailment", "non_entailments.empirical-learnability"),
    "BOUND-WILL-NONCIRCULAR": ("non-circularity", "dependency-graph.ARG-08"),
    "BOUND-SPEECH-UNSAFE-WORDING": ("scope-firewall", "speech_boundary.unsafe_created_arabic_wording"),
    "BOUND-CAPACITY-NOT-ACTUAL-SPEECH": ("non-entailment", "speech_boundary.capacity_entails_actual_speech"),
}
EXPECTED_BOUNDARY_REFS = {
    "ARG-01-P1": [],
    "ARG-01-C": ["BOUND-CROSS-FRAMEWORK-NOT-TRIBUNAL"],
    "ARG-02-P1": [],
    "ARG-02-C": [],
    "ARG-03-P1": [],
    "ARG-03-C": ["BOUND-OSM-DAEE-NONWARRANT", "BOUND-EMPIRICAL-NOT-NORMATIVITY"],
    "ARG-04-P1": ["BOUND-EMPIRICAL-NOT-NORMATIVITY", "BOUND-FITRAH-QUALITATIVE"],
    "ARG-04-P2": ["BOUND-PROPER-FUNCTION-MODERN"],
    "ARG-04-C": ["BOUND-PROPER-FUNCTION-MODERN", "BOUND-EMPIRICAL-NOT-NORMATIVITY"],
    "ARG-05-P1": [],
    "ARG-05-C": [],
    "ARG-06-P1": [],
    "ARG-06-C": ["BOUND-DIVINE-NOT-FORMAL-OBJECT", "BOUND-CROSS-FRAMEWORK-NOT-TRIBUNAL"],
    "ARG-07-P1": [],
    "ARG-07-C": [],
    "ARG-08-P1": ["BOUND-WILL-NONCIRCULAR"],
    "ARG-08-C": ["BOUND-WILL-NONCIRCULAR"],
    "ARG-09-P1": [],
    "ARG-09-C": ["BOUND-OSM-DAEE-NONWARRANT"],
    "ARG-10-P1": ["BOUND-WISDOM-HELD"],
    "ARG-10-P2": ["BOUND-WISDOM-HELD"],
    "ARG-10-C": ["BOUND-WISDOM-HELD"],
    "ARG-11-P1": [],
    "ARG-11-C": ["BOUND-CAPACITY-NOT-ACTUAL-SPEECH"],
    "ARG-12-P1": [],
    "ARG-12-C": ["BOUND-CAPACITY-NOT-ACTUAL-SPEECH", "BOUND-SPEECH-UNSAFE-WORDING"],
    "ARG-13-P1": [],
    "ARG-13-C": ["BOUND-SPEECH-UNSAFE-WORDING"],
    "ARG-14-P1": ["BOUND-RABB-NONCONJUNCTIVE"],
    "ARG-14-C": ["BOUND-RABB-NONCONJUNCTIVE", "BOUND-RABB-NONTHEOLOGICAL", "BOUND-RABB-DEPENDENT-CREATURE"],
}
RIVAL_FAMILIES = {
    "selected-function-naturalism",
    "primitivism",
    "modal-primitivism",
    "platonism-structural-realism",
    "brute-contingency",
    "aseity-bootstrapping",
    "euthyphro-fittingness",
    "impersonal-ground",
}
EXPECTED_RIVAL_ROUTES = {
    "selected-function-naturalism": ("ARG-04", "open-live-exit"),
    "primitivism": ("ARG-05", "open-live-exit"),
    "modal-primitivism": ("ARG-07", "open-live-exit"),
    "platonism-structural-realism": ("ARG-06", "open-live-exit"),
    "brute-contingency": ("ARG-08", "open-live-exit"),
    "aseity-bootstrapping": ("ARG-05", "unresolved-scope-limited-reductio"),
    "euthyphro-fittingness": (
        "ARG-10",
        "held-common-premise-positive-bridge",
    ),
    "impersonal-ground": ("ARG-06", "open-live-exit"),
}
EXPECTED_RIVAL_EXITS = {
    "ARG-01": ("deflationism", "open", "evaluation-truth-aptness"),
    "ARG-02": ("humean-regularity", "open", "truth-linked-correction"),
    "ARG-03": ("instrumentalism", "open", "representational-access"),
    "ARG-04": ("selected-function-naturalism", "open", "ARG-04"),
    "ARG-05": ("aseity-bootstrapping", "unresolved", "ARG-05"),
    "ARG-06": ("impersonal-ground", "open", "ARG-06"),
    "ARG-07": ("modal-primitivism", "open", "ARG-07"),
    "ARG-08": ("brute-contingency", "open", "ARG-08"),
    "ARG-09": ("impersonal-efficacy", "open", "efficacy"),
    "ARG-10": ("euthyphro-fittingness", "held", "ARG-10"),
    "ARG-11": ("capacity-scepticism", "open", "proportionate-causality"),
    "ARG-12": (
        "alternative-kalam-articulations",
        "comparative-only",
        "actual-Speech-articulation",
    ),
    "ARG-13": (
        "alternative-kalam-articulations",
        "comparative-only",
        "bearer-typing",
    ),
    "ARG-14": ("source-custody-hold", "held", "lexical-evidence"),
}
WARRANT_BASES = {
    "stated-premises-and-inference",
    "revelation-and-declared-creed-internal-inference",
}
COPIED_CUSTODY_FIELDS = {
    "citation",
    "citation_locator",
    "edition",
    "translation",
    "repository_extraction",
    "locator",
}
TASK9_SOURCE_IDS = {
    "CIR-1",
    "CIR-1W",
    "CIR-2",
    "CIR-3",
    "CIR-4",
    "ELT-1",
    "ELT-2",
    "ELT-3",
    "ATH-1",
    "ATH-2",
    "ATH-3",
    "ATH-4",
    "ATH-5",
    "ATH-6",
    "ATH-7",
    "LAT-1",
    "LAT-2",
    "LAT-3",
    "EXT-1",
}
PRIMARY_SOURCE_STATUSES = {
    "PRIMARY_TEXT_EXACT",
    "PRIMARY_WORK_THEME",
    "PRIMARY_LOCUS_EDITION_DEPENDENT",
}
PRIMARY_TEXT_REFERENCE_IDS = {
    "ATH-1",
    "ATH-2",
    "ATH-3",
    "ATH-4",
    "ATH-5",
    "ATH-6",
    "LAT-1",
}
SECONDARY_REFERENCE_IDS = {
    "CIR-1",
    "CIR-1W",
    "CIR-2",
    "CIR-3",
    "CIR-4",
    "ELT-1",
    "ELT-2",
    "ELT-3",
    "ATH-5",
    "ATH-7",
    "LAT-2",
    "LAT-3",
}
SPEECH_CREATED = {
    "SPEECH-BEARER-01",
    "SPEECH-BEARER-02",
    "SPEECH-BEARER-03",
    "SPEECH-BEARER-04",
    "SPEECH-BEARER-07",
}
SPEECH_BEARER_TEXT = {
    "SPEECH-BEARER-01": "created human convention",
    "SPEECH-BEARER-02": "created creaturely speaking recitation and writing",
    "SPEECH-BEARER-03": "created voice and breath",
    "SPEECH-BEARER-04": "created ink page screen and media",
    "SPEECH-BEARER-05": "Allah's act of speaking",
    "SPEECH-BEARER-06": "revealed Arabic wording as Allah's Speech",
    "SPEECH-BEARER-07": "created creaturely hearing and reception",
}
SPEECH_BEARER_IDS = frozenset(SPEECH_BEARER_TEXT)
NON_ENTAILMENTS = {
    "OSM and DAEE do not validate metaphysics or theology",
    "empirical learnability does not yield normativity without a separate bridge",
    "a school label or source identity does not supply warrant",
    "a lexical range does not conjunctively entail every sense at every token",
    "capacity for disclosure does not entail an actual divine Speech event",
}


def _add(issues: list[str], message: str) -> None:
    if len(issues) < MAX_ISSUES:
        issues.append(message)


def _source_rows(registry: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(registry, dict) or not isinstance(registry.get("claims"), list):
        return {}
    return {
        row["id"]: row
        for row in registry["claims"]
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }


def _texts(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(_texts(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_texts(item) for item in value)
    return value if isinstance(value, str) else ""

def _copied_custody_paths(value: Any, prefix: str = "") -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key in COPIED_CUSTODY_FIELDS:
                paths.append(path)
            paths.extend(_copied_custody_paths(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.extend(_copied_custody_paths(item, f"{prefix}[{index}]"))
    return paths


def _dependency_cycle(
    dependencies: dict[str, list[str]], node_ids: set[str]
) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str, path: list[str]) -> list[str] | None:
        if node_id in visiting:
            start = path.index(node_id)
            return path[start:] + [node_id]
        if node_id in visited:
            return None
        visiting.add(node_id)
        path.append(node_id)
        for dependency in dependencies.get(node_id, []):
            if dependency in node_ids:
                cycle = visit(dependency, path)
                if cycle:
                    return cycle
        path.pop()
        visiting.remove(node_id)
        visited.add(node_id)
        return None

    for node_id in sorted(node_ids):
        cycle = visit(node_id, [])
        if cycle:
            return cycle
    return None


def validate_mapping(data: Any, source_registry: Any) -> list[str]:
    """Return bounded diagnostics for arbitrary already-loaded inputs."""
    issues: list[str] = []
    if not isinstance(data, dict):
        return ["argument map must be a mapping"]
    if data.get("schema") != "orthemology-dynamic-orthability-argument-map-v2":
        _add(issues, "schema must be orthemology-dynamic-orthability-argument-map-v2")
    if data.get("operative_noetic_frame") != "athari-taymiyyan":
        _add(issues, "operative_noetic_frame must declare athari-taymiyyan")

    policy = data.get("cross_framework_policy")
    if not isinstance(policy, dict):
        _add(issues, "cross_framework_policy must be a mapping")
    elif (
        policy.get("meaning") != "dialectical-accessibility-and-rival-routing"
        or policy.get("warrant_role") != "presentation-only"
        or policy.get("objective_criteria_assessable") is not True
        or policy.get("school_label_is_warrant") is not False
        or policy.get("source_identity_is_warrant") is not False
    ):
        _add(
            issues,
            "cross-framework scope must mean dialectical accessibility, not a neutral tribunal",
        )

    wisdom = data.get("common_premise_fittingness_to_wisdom")
    if (
        not isinstance(wisdom, dict)
        or wisdom.get("status") not in {"held", "conditional", "removed"}
        or wisdom.get("reason")
        != "no verified common-premise source establishes the positive inference"
        or wisdom.get("permitted_use") != "conditional rival routing only"
    ):
        _add(issues, "common-premise fittingness-to-Wisdom bridge must remain held")

    if data.get("divine_formal_object_policy") != "Allah-is-never-an-internal-formal-object":
        _add(issues, "Allah must never be represented as an internal formal object")
    non_entailments = data.get("non_entailments")
    if not isinstance(non_entailments, list):
        _add(issues, "non_entailments must be a list")
    else:
        declared_non_entailments = {
            item for item in non_entailments if isinstance(item, str)
        }
        if len(declared_non_entailments) != len(non_entailments):
            _add(issues, "non_entailments entries must be strings")
        for missing in sorted(NON_ENTAILMENTS - declared_non_entailments):
            _add(issues, f"missing non_entailment: {missing}")
    boundaries = data.get("semantic_boundaries")
    if not isinstance(boundaries, dict):
        _add(issues, "semantic_boundaries must be a mapping")
        boundary_ids: set[str] = set()
    else:
        boundary_ids = {
            boundary_id
            for boundary_id in boundaries
            if isinstance(boundary_id, str)
        }
        if boundary_ids != set(EXPECTED_BOUNDARIES):
            _add(issues, "semantic boundary identities must equal the frozen registry")
        for boundary_id, expected in EXPECTED_BOUNDARIES.items():
            boundary = boundaries.get(boundary_id)
            actual = (
                (boundary.get("kind"), boundary.get("owner"))
                if isinstance(boundary, dict)
                else None
            )
            if actual != expected:
                _add(issues, f"semantic boundary contract drift for {boundary_id}")

    fitrah = data.get("fitrah_boundary")
    if (
        not isinstance(fitrah, dict)
        or fitrah.get("representation") != "qualitative-defeasible-multidimensional"
        or not isinstance(fitrah.get("not"), list)
        or not {
            "scalar",
            "coordinate",
            "algorithm",
            "guaranteed-attractor",
            "discourse-readable-soul-state",
            "metaortheme",
        }.issubset(
            {
                item
                for item in fitrah.get("not", [])
                if isinstance(item, str)
            }
        )
    ):
        _add(issues, "fiṭrah must remain qualitative, defeasible, and multidimensional")

    proper = data.get("proper_function_boundary")
    if (
        not isinstance(proper, dict)
        or proper.get("historical_attribution") != "modern-comparative-reconstruction"
        or proper.get("inferential_reach") != "does-not-by-itself-prove-a-Designer"
    ):
        _add(issues, "proper functionalism is modern comparison, not Ibn Taymiyya's theory")

    rabb = data.get("rabb_lexical_crosswalk")
    required_layers = {
        "token": "orthemma",
        "candidate_senses": "orthemes",
        "interpretive_rules": "metaorthemes",
        "context_binding": "metaorthemma",
        "disambiguation": "orthing",
    }
    if not isinstance(rabb, dict):
        _add(issues, "Rabb lexical crosswalk must be a mapping")
    else:
        if rabb.get("lexical_range_semantics") != "candidate-senses-selected-by-context":
            _add(issues, "Rabb lexical range cannot conjunctively entail all senses")
        if rabb.get("theological_reach") != "none-from-etymology-alone":
            _add(issues, "Rabb lexical evidence cannot prove theology or Wisdom")
        layers = rabb.get("layers")
        if not isinstance(layers, dict):
            _add(issues, "Rabb layers must be a mapping")
        else:
            for key, expected in required_layers.items():
                if layers.get(key) != expected:
                    _add(issues, f"Rabb layer {key} must map to {expected}")
        if rabb.get("creaturely_completion") != "remains-dependent-not-self-sufficient":
            _add(issues, "Rabb crosswalk cannot imply creaturely self-sufficiency")

    speech_boundary = data.get("speech_boundary")
    if (
        not isinstance(speech_boundary, dict)
        or speech_boundary.get("capacity_entails_actual_speech") is not False
        or speech_boundary.get("actual_speech_requires")
        != "revelational-school-internal-dependency"
        or speech_boundary.get("unsafe_created_arabic_wording") != "prohibited"
    ):
        _add(issues, "capacity for disclosure must not entail actual divine Speech")

    bearers = data.get("speech_bearers")
    if not isinstance(bearers, list) or len(bearers) != 7:
        _add(issues, "exactly seven Speech bearers are required")
    else:
        ids: set[str] = set()
        for bearer in bearers:
            if not isinstance(bearer, dict):
                _add(issues, "Speech bearer must be a mapping")
                continue
            bearer_id = bearer.get("id")
            if not isinstance(bearer_id, str) or bearer_id in ids:
                _add(issues, "seven Speech bearers require distinct stable ids")
                continue
            ids.add(bearer_id)
            if bearer.get("bearer") != SPEECH_BEARER_TEXT.get(bearer_id):
                _add(issues, f"Speech bearer semantics drift for {bearer_id}")
            created_status = bearer.get("created_status")
            if bearer_id in SPEECH_CREATED and created_status != "created":
                _add(issues, f"created bearer {bearer_id} must remain created")
            if bearer_id == "SPEECH-BEARER-05" and created_status != "uncreated-divine-attribute-act":
                _add(issues, "Allah's act of speaking must remain distinct")
            if bearer_id == "SPEECH-BEARER-06" and created_status != "uncreated-divine-speech":
                _add(issues, "revealed Arabic wording must remain Allah's Speech")
        if ids != SPEECH_BEARER_IDS:
            _add(issues, "Speech bearer identities must equal the frozen registry")

    routes = data.get("rival_routes")
    if not isinstance(routes, dict):
        for family in sorted(RIVAL_FAMILIES):
            _add(issues, f"missing rival route {family}")
    else:
        route_nodes = data.get("nodes")
        route_node_ids = (
            {
                node.get("id")
                for node in route_nodes
                if isinstance(node, dict) and isinstance(node.get("id"), str)
            }
            if isinstance(route_nodes, list)
            else set()
        )
        route_keys = {key for key in routes if isinstance(key, str)}
        for family in sorted(RIVAL_FAMILIES - route_keys):
            _add(issues, f"missing rival route {family}")
        for family, route in routes.items():
            if family not in RIVAL_FAMILIES:
                _add(issues, f"unexpected rival route {family}")
            expected = EXPECTED_RIVAL_ROUTES.get(family)
            joint = route.get("joint") if isinstance(route, dict) else None
            disposition = (
                route.get("disposition") if isinstance(route, dict) else None
            )
            if (
                not isinstance(route, dict)
                or not isinstance(joint, str)
                or joint not in route_node_ids
                or not isinstance(disposition, str)
                or expected != (joint, disposition)
            ):
                _add(issues, f"rival route joint or disposition invalid for {family}")

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        _add(issues, "nodes must be a non-empty list")
        return issues
    actual_node_ids = [
        node.get("id") if isinstance(node, dict) else None for node in nodes
    ]
    if tuple(actual_node_ids) != EXPECTED_NODE_IDS:
        _add(issues, "node identities and canonical order must equal ARG-01 through ARG-14")

    source_rows = _source_rows(source_registry)
    node_ids = {
        node.get("id")
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    claim_occurrences: list[str] = []
    for raw_node in nodes:
        if not isinstance(raw_node, dict):
            continue
        raw_premises = raw_node.get("premises")
        if isinstance(raw_premises, list):
            claim_occurrences.extend(
                item["id"]
                for item in raw_premises
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            )
        raw_conclusion = raw_node.get("conclusion")
        if isinstance(raw_conclusion, dict) and isinstance(raw_conclusion.get("id"), str):
            claim_occurrences.append(raw_conclusion["id"])
    claim_ids = set(claim_occurrences)
    seen: set[str] = set()
    for index, node in enumerate(nodes, start=1):
        if not isinstance(node, dict):
            _add(issues, f"node {index} must be a mapping")
            continue
        node_id = node.get("id", f"node-{index}")
        for field in sorted(NODE_FIELDS - set(node)):
            _add(issues, f"{node_id}: missing field {field}")
        for field in _copied_custody_paths(node):
            _add(
                issues,
                f"{node_id}: copied source-custody field {field} is prohibited; resolve it from the registry owner",
            )
        if isinstance(node_id, str) and node_id in seen:
            _add(issues, f"duplicate node id {node_id}")
        elif isinstance(node_id, str):
            seen.add(node_id)
        if node.get("order") != index:
            _add(issues, f"{node_id}: order must equal canonical position {index}")
        if not isinstance(node_id, str) or not re.fullmatch(r"ARG-\d{2}", node_id):
            _add(issues, f"{node_id}: id must be stable ARG-NN")
        if isinstance(node_id, str) and node.get("label") != EXPECTED_LABELS.get(
            node_id
        ):
            _add(issues, f"{node_id}: stable label drift")
        scope = node.get("scope")
        if not isinstance(scope, str) or scope not in SCOPES:
            _add(issues, f"{node_id}: invalid scope {node.get('scope')}")
        inference_type = node.get("inference_type")
        if not isinstance(inference_type, str) or inference_type not in INFERENCE_TYPES:
            _add(issues, f"{node_id}: invalid inference_type {node.get('inference_type')}")
        bridge_status = node.get("bridge_status")
        if not isinstance(bridge_status, str) or bridge_status not in BRIDGE_STATUSES:
            _add(issues, f"{node_id}: invalid bridge_status {node.get('bridge_status')}")

        premises = node.get("premises")
        if not isinstance(premises, list) or not premises:
            _add(issues, f"{node_id}: premises must be a non-empty list")
        else:
            for premise in premises:
                if not isinstance(premise, dict) or not isinstance(premise.get("id"), str) or not isinstance(premise.get("text"), str):
                    _add(issues, f"{node_id}: malformed premise")
                elif EXPECTED_CLAIMS.get(premise["id"]) != premise["text"]:
                    _add(issues, f"{node_id}: premise contract drift for {premise['id']}")
                else:
                    boundary_refs = premise.get("boundary_refs")
                    if (
                        not isinstance(boundary_refs, list)
                        or not all(isinstance(ref, str) for ref in boundary_refs)
                    ):
                        _add(issues, f"{node_id}: malformed premise boundary_refs")
                    elif boundary_refs != EXPECTED_BOUNDARY_REFS.get(premise["id"]):
                        _add(issues, f"{node_id}: premise boundary contract drift for {premise['id']}")
                    elif any(ref not in boundary_ids for ref in boundary_refs):
                        _add(issues, f"{node_id}: unresolved premise boundary reference")
            if isinstance(node_id, str) and node_id in EXPECTED_CLAIM_PLACEMENTS:
                premise_ids = {
                    premise.get("id")
                    for premise in premises
                    if isinstance(premise, dict)
                    and isinstance(premise.get("id"), str)
                }
                if premise_ids != EXPECTED_CLAIM_PLACEMENTS[node_id]["premises"]:
                    _add(issues, f"{node_id}: premise identities drift from the frozen placement registry")
        conclusion = node.get("conclusion")
        if not isinstance(conclusion, dict) or not isinstance(conclusion.get("id"), str) or not isinstance(conclusion.get("text"), str):
            _add(issues, f"{node_id}: malformed conclusion")
        elif EXPECTED_CLAIMS.get(conclusion["id"]) != conclusion["text"]:
            _add(issues, f"{node_id}: conclusion contract drift for {conclusion['id']}")
        else:
            boundary_refs = conclusion.get("boundary_refs")
            if (
                not isinstance(boundary_refs, list)
                or not all(isinstance(ref, str) for ref in boundary_refs)
            ):
                _add(issues, f"{node_id}: malformed conclusion boundary_refs")
            elif boundary_refs != EXPECTED_BOUNDARY_REFS.get(conclusion["id"]):
                _add(issues, f"{node_id}: conclusion boundary contract drift for {conclusion['id']}")
            elif any(ref not in boundary_ids for ref in boundary_refs):
                _add(issues, f"{node_id}: unresolved conclusion boundary reference")
        if (
            isinstance(node_id, str)
            and node_id in EXPECTED_CLAIM_PLACEMENTS
            and (
                not isinstance(conclusion, dict)
                or conclusion.get("id")
                != EXPECTED_CLAIM_PLACEMENTS[node_id]["conclusion"]
            )
        ):
            _add(issues, f"{node_id}: conclusion identity drifts from the frozen placement registry")

        dependencies = node.get("dependencies")
        if not isinstance(dependencies, list):
            _add(issues, f"{node_id}: dependencies must be a list")
        else:
            for dependency in dependencies:
                if not isinstance(dependency, str):
                    _add(issues, f"{node_id}: malformed dependency")
                elif dependency not in node_ids:
                    _add(issues, f"{node_id}: dangling dependency {dependency}")
                elif dependency == node_id:
                    _add(issues, f"{node_id}: self dependency")
            if isinstance(node_id, str) and dependencies != EXPECTED_DEPENDENCIES.get(
                node_id
            ):
                _add(issues, f"{node_id}: dependencies drift from the canonical graph")
        bridge_refs = node.get("bridge_premise_refs")
        if not isinstance(bridge_refs, list):
            _add(issues, f"{node_id}: bridge_premise_refs must be a list")
        else:
            for bridge_ref in bridge_refs:
                if not isinstance(bridge_ref, str):
                    _add(issues, f"{node_id}: malformed bridge_premise_ref")
                elif bridge_ref not in claim_ids:
                    _add(issues, f"{node_id}: dangling bridge_premise_ref {bridge_ref}")
                elif (
                    isinstance(conclusion, dict)
                    and bridge_ref == conclusion.get("id")
                ):
                    _add(issues, f"{node_id}: conclusion cannot be its own bridge premise")
            if isinstance(node_id, str) and bridge_refs != EXPECTED_BRIDGE_REFS.get(
                node_id
            ):
                _add(issues, f"{node_id}: bridge premise references drift")

        role = node.get("claim_role")
        if not isinstance(role, str) or role not in CLAIM_ROLES:
            _add(issues, f"{node_id}: invalid claim_role {role}")
        if index >= 4 and role == "computational-analogy":
            _add(issues, f"{node_id}: upper node cannot use computational-analogy")
        if role == "creed-internal-inference" and node.get("scope") != "athari-taymiyyan-operative":
            _add(issues, f"{node_id}: creed-internal claim requires Athari operative scope")
        if node.get("scope") == "cross-framework-dialectical" and role == "creed-internal-inference":
            _add(issues, f"{node_id}: cross-framework node cannot use creed-internal warrant")
        warrant_basis = node.get("warrant_basis")
        if not isinstance(warrant_basis, str) or warrant_basis not in WARRANT_BASES:
            _add(issues, f"{node_id}: invalid warrant_basis")
        if (
            scope == "cross-framework-dialectical"
            and warrant_basis != "stated-premises-and-inference"
        ):
            _add(issues, f"{node_id}: cross-framework warrant must use stated premises")
        if isinstance(node_id, str) and EXPECTED_NODE_TYPES.get(node_id) != (
            scope,
            inference_type,
            bridge_status,
            warrant_basis,
        ):
            _add(issues, f"{node_id}: typed semantic contract drift")
        objection = node.get("strongest_objection")
        if (
            not isinstance(objection, dict)
            or not isinstance(objection.get("id"), str)
            or not isinstance(objection.get("status"), str)
            or not isinstance(objection.get("text"), str)
        ):
            _add(issues, f"{node_id}: strongest_objection must be a typed mapping")
        rival = node.get("rival_exit")
        if (
            not isinstance(rival, dict)
            or not isinstance(rival.get("id"), str)
            or not isinstance(rival.get("disposition"), str)
            or not isinstance(rival.get("joint"), str)
        ):
            _add(issues, f"{node_id}: rival_exit must be a typed mapping")
        elif rival["id"] in EXPECTED_RIVAL_ROUTES:
            expected_joint = EXPECTED_RIVAL_ROUTES[rival["id"]][0]
            if rival["joint"] != expected_joint or expected_joint != node_id:
                _add(issues, f"{node_id}: local rival joint must match global route")
        if (
            isinstance(node_id, str)
            and isinstance(rival, dict)
            and EXPECTED_RIVAL_EXITS.get(node_id)
            != (
                rival.get("id"),
                rival.get("disposition"),
                rival.get("joint"),
            )
        ):
            _add(issues, f"{node_id}: local rival contract drift")

        refs = node.get("source_status_refs")
        access = node.get("evidence_access_status")
        ref_roles = node.get("reference_roles")
        if not isinstance(refs, list):
            _add(issues, f"{node_id}: source_status_refs must be a list")
            refs = []
        valid_refs = [ref for ref in refs if isinstance(ref, str)]
        if len(valid_refs) != len(refs):
            _add(issues, f"{node_id}: source_status_refs entries must be strings")
        if not isinstance(access, dict):
            _add(issues, f"{node_id}: evidence_access_status must be a mapping")
            access = {}
        if not isinstance(ref_roles, dict):
            _add(issues, f"{node_id}: reference_roles must be a mapping")
            ref_roles = {}
        if set(ref_roles) != set(valid_refs):
            _add(issues, f"{node_id}: reference_roles keys must equal source_status_refs")
        if set(access) != set(valid_refs):
            _add(issues, f"{node_id}: evidence_access_status keys must equal source_status_refs")
        source_contract = None
        if (
            isinstance(role, str)
            and len(valid_refs) == len(refs)
            and all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in ref_roles.items()
            )
        ):
            source_contract = (
                role,
                tuple(valid_refs),
                tuple(sorted(ref_roles.items())),
            )
        if (
            isinstance(node_id, str)
            and source_contract not in ALLOWED_SOURCE_CONTRACTS.get(node_id, set())
        ):
            _add(issues, f"{node_id}: claim/source/reference-role contract drift")
        for ref in valid_refs:
            if ref not in TASK9_SOURCE_IDS:
                _add(issues, f"{node_id}: source {ref} is outside the frozen Task 9 registry")
            row = source_rows.get(ref)
            if row is None:
                _add(issues, f"{node_id}: unresolved source_status_ref {ref}")
                continue
            if access.get(ref) != row.get("status"):
                _add(issues, f"{node_id}: evidence access drift for {ref}")
            reference_role = ref_roles.get(ref)
            if (
                not isinstance(reference_role, str)
                or reference_role not in REFERENCE_ROLES
            ):
                _add(issues, f"{node_id}: invalid reference role for {ref}")
            elif (
                reference_role == "primary-text"
                and ref not in PRIMARY_TEXT_REFERENCE_IDS
            ):
                _add(issues, f"{node_id}: primary-text role is incompatible with {ref}")
            elif (
                reference_role == "secondary-scholarship"
                and ref not in SECONDARY_REFERENCE_IDS
            ):
                _add(
                    issues,
                    f"{node_id}: secondary-scholarship role is incompatible with {ref}",
                )
        if role == "primary-text-verified":
            if not valid_refs or any(
                source_rows.get(ref, {}).get("status") not in PRIMARY_SOURCE_STATUSES
                for ref in valid_refs
            ):
                _add(issues, f"{node_id}: primary-text-verified claim requires primary sources")

    if (
        claim_ids != set(EXPECTED_CLAIMS)
        or Counter(claim_occurrences)
        != Counter({claim_id: 1 for claim_id in EXPECTED_CLAIMS})
    ):
        _add(issues, "claim identities must occur exactly once in the frozen Task 9 claim registry")
    dependency_map = {
        node["id"]: node["dependencies"]
        for node in nodes
        if isinstance(node, dict)
        and isinstance(node.get("id"), str)
        and isinstance(node.get("dependencies"), list)
        and all(isinstance(item, str) for item in node["dependencies"])
    }
    cycle = _dependency_cycle(dependency_map, node_ids)
    if cycle:
        _add(issues, "dependency cycle: " + " -> ".join(cycle))

    by_id = {
        node.get("id"): node
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    norm = by_id.get("ARG-04")
    if isinstance(norm, dict):
        dependencies = norm.get("dependencies")
        bridges = norm.get("bridge_premise_refs")
        if (
            not isinstance(dependencies, list)
            or "ARG-02" not in dependencies
            or not isinstance(bridges, list)
            or "ARG-04-P2" not in bridges
        ):
            _add(issues, "ARG-04: normativity bridge must be separate from empirical learnability")

    actual = by_id.get("ARG-12")
    if isinstance(actual, dict):
        if (
            actual.get("bridge_status") != "revelational"
            or actual.get("scope") != "athari-taymiyyan-operative"
            or actual.get("claim_role") != "creed-internal-inference"
        ):
            _add(issues, "actual Speech requires revelational Athari dependency")
    athari_wisdom = by_id.get("ARG-10")
    if isinstance(athari_wisdom, dict):
        if athari_wisdom.get("bridge_status") not in {
            "held",
            "conditional",
            "held-pending-source-custody",
        }:
            _add(issues, "Athari Wisdom route cannot exceed its verified source custody")
        athari_conclusion = athari_wisdom.get("conclusion")
        athari_conclusion_text = (
            athari_conclusion.get("text", "")
            if isinstance(athari_conclusion, dict)
            else ""
        )
        if (
            not athari_wisdom.get("source_status_refs")
            and "remain held" not in str(athari_conclusion_text).lower()
        ):
            _add(issues, "Athari Wisdom source assertion must remain held without verified sources")

    return issues[:MAX_ISSUES]


def main() -> int:
    try:
        data = yaml.safe_load(MAP_PATH.read_text(encoding="utf-8"))
        registry = yaml.safe_load(SOURCE_STATUS_PATH.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"[FAIL] argument map parse: {exc}")
        return 1
    issues = validate_mapping(data, registry)
    if issues:
        for issue in issues:
            print(f"[FAIL] {issue}")
        print(f"Argument-map validation failed: {len(issues)} issue(s)")
        return 1
    print(f"[PASS] structured argument map: {len(data['nodes'])} nodes")
    print("[PASS] source references, roles, and evidence access agree")
    print("[PASS] dialectical, metaphysical, Rabb, fitrah, and Speech firewalls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
