#!/usr/bin/env python3
"""Read-only finite corroboration and countermodels for the Deep BV challenger packet.

This script does not reproduce the unavailable historical Deep BV checker. It independently
checks the elementary finite fibre/factorization equivalence by two procedures and serializes
explicit stronger-reading countermodels. No repository mutation or authoritative status is made.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from itertools import product
from json import dumps
from pathlib import Path
from typing import Any, Hashable, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "deep_bv_challenger_results.json"


def fibre_constant(profile: Sequence[Hashable], target: Sequence[Hashable]) -> bool:
    if len(profile) != len(target):
        raise ValueError("profile and target must have equal domain length")
    for i in range(len(profile)):
        for j in range(len(profile)):
            if profile[i] == profile[j] and target[i] != target[j]:
                return False
    return True


def partition_homogeneous(profile: Sequence[Hashable], target: Sequence[Hashable]) -> bool:
    """Distinct rereview procedure: form profile blocks, then test target homogeneity."""
    blocks: dict[Hashable, set[Hashable]] = {}
    for p, q in zip(profile, target, strict=True):
        blocks.setdefault(p, set()).add(q)
    return all(len(values) <= 1 for values in blocks.values())


def attained_decoder_exists_bruteforce(
    profile: Sequence[int], target: Sequence[int], target_alphabet: Sequence[int]
) -> bool:
    """Primary finite procedure: enumerate decoders on the attained profile image."""
    attained = tuple(sorted(set(profile)))
    for values in product(target_alphabet, repeat=len(attained)):
        decoder = dict(zip(attained, values, strict=True))
        if all(decoder[p] == q for p, q in zip(profile, target, strict=True)):
            return True
    return False


def full_codom_decoder_exists_bruteforce(
    profile: Sequence[int],
    target: Sequence[int],
    profile_alphabet: Sequence[int],
    target_alphabet: Sequence[int],
) -> bool:
    """Enumerate decoders on the whole profile codomain (nonempty target alphabet only)."""
    for values in product(target_alphabet, repeat=len(profile_alphabet)):
        decoder = dict(zip(profile_alphabet, values, strict=True))
        if all(decoder[p] == q for p, q in zip(profile, target, strict=True)):
            return True
    return False


@dataclass(frozen=True)
class Countermodel:
    id: str
    stronger_reading_refuted: str
    model: Mapping[str, Any]
    failure: str
    firewall_consequence: str


def build_countermodels() -> list[Countermodel]:
    return [
        Countermodel(
            id="CM-BVB-01-PAIRWISE-NOT-CLASSWIDE",
            stronger_reading_refuted="One selected personal/impersonal separation identifies Q over the declared class.",
            model={
                "models": ["personal_P", "impersonal_I", "plural_R"],
                "profile": {"personal_P": 0, "impersonal_I": 1, "plural_R": 0},
                "target_Q": {"personal_P": 1, "impersonal_I": 0, "plural_R": 0},
            },
            failure="P and I are separated, but P and R share one profile value while Q differs.",
            firewall_consequence="Require class-wide fibre constancy, not a selected pair or positive pairwise distance.",
        ),
        Countermodel(
            id="CM-BVB-02-TARGET-LEAKAGE",
            stronger_reading_refuted="A perfectly discriminating operationalization is automatically evidential.",
            model={
                "base_profile": {"m0": 0, "m1": 0},
                "target_Q": {"m0": 0, "m1": 1},
                "implementation_policy": "choose intervention i_Q(m) after consulting Q(m)",
                "reported_output": "Q(m)",
            },
            failure="The experiment re-encodes the answer; the implementation map is not target-blind.",
            firewall_consequence="Freeze implementation before target labels and require invariance under target relabelling.",
        ),
        Countermodel(
            id="CM-BVB-03-SEMANTIC-MISMATCH",
            stronger_reading_refuted="One shared intervention string is a common intervention type.",
            model={
                "label": "request-a-reason",
                "personal_implementation": "solicit intentional justificatory uptake",
                "impersonal_implementation": "append a token sequence tagged REASON",
                "shared_numeric_code": 1,
            },
            failure="Equal labels/codes do not establish equal intervention or output semantics.",
            firewall_consequence="Require an abstract type, architecture-specific implementation map, and semantics-preservation proof.",
        ),
        Countermodel(
            id="CM-BVB-04-ONE-SHOT-NOT-ADAPTIVE",
            stronger_reading_refuted="Equality of all isolated one-shot responses entails equality under adaptive protocols.",
            model={
                "isolated": {
                    "model_A": {"i0": 0, "i1": 0},
                    "model_B": {"i0": 0, "i1": 0},
                },
                "adaptive_sequence_i0_then_i1": {
                    "model_A": [0, 0],
                    "model_B": [0, 1],
                },
            },
            failure="History-sensitive response appears only after the first intervention.",
            firewall_consequence="Type protocol kind and define E_J over complete adaptive transcripts when adaptivity is claimed.",
        ),
        Countermodel(
            id="CM-BVB-05-PROPER-FUNCTION-TWINS",
            stronger_reading_refuted="Complete current behaviour identifies history-sensitive proper function.",
            model={
                "current_behaviour_profile": {"selected_system": "b", "accidental_duplicate": "b"},
                "selected_history": {"selected_system": True, "accidental_duplicate": False},
                "proper_function_Q": {"selected_system": True, "accidental_duplicate": False},
            },
            failure="Behavioural fibres contain different selection/design/norm histories.",
            firewall_consequence="Supply independent function-fixing evidence or record nonidentifiability; do not infer function from success.",
        ),
        Countermodel(
            id="CM-BVB-06-SOURCE-WORLD-TWINS",
            stronger_reading_refuted="Agreement through formal source predicate determines actual-world truth and bearer.",
            model={
                "shared": ["source_bytes", "translation", "morphology", "syntax", "occurrence_meaning", "formal_predicate"],
                "world_0": {"predicate_true": True, "bearer": "w0"},
                "world_1": {"predicate_true": False, "bearer": None},
            },
            failure="The source/formal profile is identical while world truth and bearer application differ.",
            firewall_consequence="Add independently warranted interpretation, world-adequacy, truth, and bearer-applicability bridges.",
        ),
        Countermodel(
            id="CM-BVB-07-UNCREATED-GRAMMAR-TWINS",
            stronger_reading_refuted="Complete linguistic/articulability behaviour identifies uncreatedness, mentality, or Speech.",
            model={
                "shared_linguistic_profile": "all frozen token, syntax, morphology, composition, and response tests agree",
                "model_created": {"ground_status": "created/nomological", "mental_bearer": False, "speech": False},
                "model_uncreated": {"ground_status": "underived", "mental_bearer": True, "speech": True},
            },
            failure="The metaphysical coordinates vary inside the linguistic profile fibre.",
            firewall_consequence="Articulability-to-ground, ground-to-mentality, and mentality-to-Speech remain separate bridges.",
        ),
        Countermodel(
            id="CM-BVB-08-TRANSCENDENTAL-NOGO-TWINS",
            stronger_reading_refuted="A formal non-generation/no-go result identifies a Necessary Being or personal ground.",
            model={
                "shared_formal_no_go_profile": "same-token/same-respect non-generation result",
                "world_A": {"ground": "plural brute modal order", "necessary_being": False, "personal": False},
                "world_B": {"ground": "one necessary personal being", "necessary_being": True, "personal": True},
            },
            failure="The negative formal result is compatible with rival positive grounds.",
            firewall_consequence="Require each positive ground, necessity, concreteness, unity, intellect, and personality bridge separately.",
        ),
        Countermodel(
            id="CM-BVB-09-FINITE-HISTORY-IMPERSONAL-REALIZER",
            stronger_reading_refuted="Matching all frozen finite intervention histories establishes personality or intentional uptake.",
            model={
                "frozen_protocol_set": "finite J with bounded transcripts",
                "personal_model": "personal controller",
                "impersonal_model": "finite lookup table reproducing every registered transcript law",
                "profile_equality": True,
                "personality_Q_differs": True,
            },
            failure="A finite extensional profile can be table-realized without the disputed constitution.",
            firewall_consequence="Either enlarge the profile with independently eligible evidence or retain the impersonal rival in the fibre.",
        ),
        Countermodel(
            id="CM-BVB-10-RESOURCE-AUTHORIZATION",
            stronger_reading_refuted="Formal definability of an intervention establishes operational availability.",
            model={
                "formal_intervention": "reset-and-reinstantiate complete architecture state",
                "cost": 10**30,
                "budget": 10**6,
                "authorization": False,
                "physical_realizability": "not established",
            },
            failure="The intervention is a mathematical label without an eligible implementation.",
            firewall_consequence="Type resource, authorization, version, and physical-realizability guards outside the factorization proof.",
        ),
        Countermodel(
            id="CM-BVB-11-FULL-CODOMAIN-EMPTY-EDGE",
            stronger_reading_refuted="Fibre constancy always implies a decoder on the entire declared profile codomain.",
            model={
                "M": "empty",
                "Profile": "singleton",
                "QVal": "empty",
                "E": "unique empty-domain map",
                "Q": "unique empty-domain map",
            },
            failure="Fibre constancy is vacuous, but no function singleton→empty exists.",
            firewall_consequence="Factor through the quotient/attained image, or add Nonempty QVal / nonempty M for a full-codomain decoder.",
        ),
        Countermodel(
            id="CM-BVB-12-HIGHER-ORDER-PARITY",
            stronger_reading_refuted="All lower-order or pairwise response profiles identify a higher-order architecture coordinate.",
            model={
                "even_parity_law": ["000", "011", "101", "110"],
                "odd_parity_law": ["001", "010", "100", "111"],
                "all_one_and_two_bit_marginals": "uniform and equal",
                "target_Q": {"even": 0, "odd": 1},
            },
            failure="Every registered lower-order profile agrees while the parity target differs.",
            firewall_consequence="The experiment profile must contain the interaction order on which Q depends.",
        ),
        Countermodel(
            id="CM-BVB-13-SOURCE-AUTHORITY-NOT-SEMANTICS",
            stronger_reading_refuted="Source authority can be used as neutral output semantics across architectures.",
            model={
                "same_text_and_translation": True,
                "source_relative_track": {"authority": True, "revelation": True},
                "neutral_track": {"authority": "not independently established", "revelation": "not independently established"},
            },
            failure="A source-relative status does not migrate into a neutral experiment by relabelling it as an output.",
            firewall_consequence="Keep source-relative coordinates explicit and condition conclusions on independently accepted authority/revelation bridges.",
        ),
        Countermodel(
            id="CM-BVB-14-REASON-TRANSPORT-DELETION",
            stronger_reading_refuted="Matching final verdicts preserves the same reason across architecture or contract change.",
            model={
                "source_reason_obligations": ["evidence", "authority", "identity", "lineage"],
                "target_result": "same verdict",
                "deleted_obligation": "authority",
                "remaining_obligations": ["evidence", "identity", "lineage"],
            },
            failure="Verdict equality survives while numerical/justificatory reason identity fails.",
            firewall_consequence="Apply full transport-complete obligation mapping; otherwise classify only a successor reason.",
        ),
    ]


def run_exhaustive() -> dict[str, Any]:
    total = 0
    max_n = 5
    mismatches: list[dict[str, Any]] = []
    full_codom_mismatches_nonempty_target: list[dict[str, Any]] = []
    by_n: dict[str, int] = {}
    for n in range(max_n + 1):
        n_cases = 0
        for p_size in range(1, 4):
            p_alpha = tuple(range(p_size))
            for q_size in range(1, 4):
                q_alpha = tuple(range(q_size))
                for e in product(p_alpha, repeat=n):
                    for q in product(q_alpha, repeat=n):
                        total += 1
                        n_cases += 1
                        fc = fibre_constant(e, q)
                        part = partition_homogeneous(e, q)
                        dec = attained_decoder_exists_bruteforce(e, q, q_alpha)
                        if not (fc == part == dec):
                            mismatches.append({"n": n, "profile": e, "target": q, "fc": fc, "partition": part, "decoder": dec})
                        full = full_codom_decoder_exists_bruteforce(e, q, p_alpha, q_alpha)
                        if fc != full:
                            full_codom_mismatches_nonempty_target.append(
                                {"n": n, "profile": e, "target": q, "fc": fc, "full_decoder": full}
                            )
        by_n[str(n)] = n_cases
    return {
        "domain_sizes": list(range(max_n + 1)),
        "profile_alphabet_sizes": [1, 2, 3],
        "target_alphabet_sizes": [1, 2, 3],
        "total_map_pairs_checked": total,
        "map_pairs_by_domain_size": by_n,
        "attained_range_equivalence_mismatches": mismatches,
        "full_codom_equivalence_mismatches_with_nonempty_target": full_codom_mismatches_nonempty_target,
        "attained_range_equivalence_pass": not mismatches,
        "full_codom_equivalence_pass_under_nonempty_target": not full_codom_mismatches_nonempty_target,
        "empty_edge_countermodel_checked_symbolically": {
            "M": 0,
            "Profile": 1,
            "QVal": 0,
            "fibre_constancy": True,
            "full_codom_decoder_exists": False,
        },
    }


def source_world_firewall() -> dict[str, Any]:
    layers = [
        "source_text_or_bytes",
        "translation",
        "morphology",
        "syntax",
        "occurrence_meaning",
        "formal_predicate",
        "world_truth",
        "bearer_applicability",
        "recipient_warrant",
        "authority",
        "revelation",
    ]
    bridge_obligations = [
        {
            "from": "source_text_or_bytes",
            "to": "translation",
            "required": ["locus/version custody", "translation adequacy"],
            "deletion_countermodel": "same bytes admit two materially different translations",
        },
        {
            "from": "translation",
            "to": "morphology",
            "required": ["vocalization/tokenization", "morphological parse"],
            "deletion_countermodel": "one translation suppresses an old-language morphological ambiguity",
        },
        {
            "from": "morphology",
            "to": "syntax",
            "required": ["valency", "attachment", "case/role constraints"],
            "deletion_countermodel": "same forms support two syntactic attachments",
        },
        {
            "from": "syntax",
            "to": "occurrence_meaning",
            "required": ["composition", "context", "discourse/pragmatics", "sense selection"],
            "deletion_countermodel": "same parse supports distinct occurrence senses or pragmatic force",
        },
        {
            "from": "occurrence_meaning",
            "to": "formal_predicate",
            "required": ["formalization adequacy", "scope/quantifier fidelity"],
            "deletion_countermodel": "formal predicate loses a modality, restriction, relation, or index",
        },
        {
            "from": "formal_predicate",
            "to": "world_truth",
            "required": ["interpretation map", "world adequacy", "actual-world selection"],
            "deletion_countermodel": "two candidate worlds satisfy the same source profile but disagree on predicate truth",
        },
        {
            "from": "world_truth",
            "to": "bearer_applicability",
            "required": ["co-reference", "referent eligibility", "role/bearer instantiation"],
            "deletion_countermodel": "predicate is true somewhere in the world but not of the proposed bearer",
        },
        {
            "from": "bearer_applicability",
            "to": "recipient_warrant",
            "required": ["evidence access", "defeater control", "independence/reliability"],
            "deletion_countermodel": "claim is true of the bearer while recipient lacks warrant or has an undefeated defeater",
        },
        {
            "from": "source_package",
            "to": "authority",
            "required": ["attribution/authentication", "jurisdiction/competence", "authority bridge"],
            "deletion_countermodel": "identical wording occurs in authoritative and nonauthoritative documents",
        },
        {
            "from": "source_package",
            "to": "revelation",
            "required": ["revelation premise", "authenticated transmission", "school-internal or neutral scope declaration"],
            "deletion_countermodel": "a truthful or authoritative text need not be revelation",
        },
    ]
    return {
        "layers_kept_separate": layers,
        "structure_note": "These coordinates form a typed product/partial dependency graph, not an automatic linear ascent.",
        "bridge_obligations": bridge_obligations,
        "neutrality_rule": "Authority and revelation may be experiment inputs only as explicitly source-relative coordinates unless independently established at the target scope.",
    }


def main() -> None:
    exhaustive = run_exhaustive()
    countermodels = [asdict(cm) for cm in build_countermodels()]
    payload: dict[str, Any] = {
        "schema": "bounded-challenger-b-deep-bv-independent-finite-corroboration-v1",
        "authority": {
            "repository": "theislampill/orthemology",
            "reviewed_commit": "a8142c3caf103ee46a2cd759c3d319b1e29b40da",
            "status": "NON_AUTHORITATIVE_READ_ONLY_PROPOSAL_EVIDENCE",
            "historical_checker_reproduction": False,
        },
        "core_theorem": {
            "statement": "Q factors through the E-profile quotient iff Q is constant on every E-fibre.",
            "finite_assumption_logically_required": False,
            "full_profile_codom_warning": "Use the quotient/attained image; otherwise add Nonempty QVal or an equivalent off-image extension assumption.",
        },
        "exhaustive_check": exhaustive,
        "countermodels": countermodels,
        "source_world_firewall": source_world_firewall(),
    }
    canonical = dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    payload["self_hash_note"] = "Hash below covers this object before insertion of the hash fields."
    payload["pre_hash_sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
    RESULTS_PATH.write_text(dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(dumps({
        "results": str(RESULTS_PATH),
        "total_map_pairs_checked": exhaustive["total_map_pairs_checked"],
        "attained_range_equivalence_pass": exhaustive["attained_range_equivalence_pass"],
        "full_codom_equivalence_pass_under_nonempty_target": exhaustive["full_codom_equivalence_pass_under_nonempty_target"],
        "countermodel_count": len(countermodels),
    }, indent=2))


if __name__ == "__main__":
    main()
