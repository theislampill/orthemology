"""Independent executed counterhistories and bounded positive controls.

This file imports an immutable retained author model, not its changing working copy.
The extra speech-act semantics is a stipulated public-undertaking model, not a detector
of private intention, real source identity, normative legitimacy, or empirical warrant.
"""
from pathlib import Path
import importlib.util
import sys
import json
from dataclasses import dataclass, asdict
from fractions import Fraction

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('reviewed_rivals', HERE / 'reviewed-rivals.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


def constitution_observe(events):
    """Reproduce the full existing observable menu, preserving only its projections."""
    base = r.institution_case()
    out = dict(base.observations)
    for kind, key in [('vote', 'vote_packet'), ('publish', 'publication_record'),
                      ('appoint', 'appointment_record'),
                      ('founder_removes_member', 'membership_history')]:
        out[key] = tuple(e for e in events if e[1] == kind)
    return out


def constitution_controls():
    events = list(r.institution_case().events)
    variants = {
        'valid': events,
        'missing_proposal': [e for e in events if e[1] != 'propose'],
        'unrelated_proposal': [(e[0], 'propose', 'unrelated_motion')
                               if e[1] == 'propose' else e for e in events],
        'publish_before_same_timestamp_votes': [e for kind in ['propose', 'publish', 'vote', 'appoint']
                                                 for e in events if e[1] == kind],
    }
    cases = []
    for name, es in variants.items():
        cases.append(r.Case(name, constitution_observe(es),
                            r.run_constitution(r.Constitution(), es), tuple(es)))
    assert cases[0].target['holder'] == 'N'
    assert all(c.target['holder'] == 'P' for c in cases[1:])
    assert all(c.observations == cases[0].observations for c in cases)
    assert r.minimal_discriminators(cases, 'holder') == []
    # A matching proposal repairs the missing/wrong-proposal examples, not chronology.
    for c in cases:
        c.observations['proposal_record'] = tuple(e for e in c.events if e[1] == 'propose')
    assert r.minimal_discriminators(cases, 'holder') == []
    # This is an externally witnessed common ordering, NOT a caller-assigned event ID.
    # The model assumes observer fidelity and exposes exactly the source trace it uses.
    for c in cases:
        c.observations['joint_procedure_record'] = c.events
    assert r.sufficient(cases, 'holder', ['joint_procedure_record'])
    return {'cases': [asdict(c) for c in cases],
            'old_entire_menu_sufficient': False,
            'old_menu_plus_proposal_sufficient': False,
            'joint_procedure_sufficient_in_this_family': True}


@dataclass(frozen=True)
class Proposition:
    domain: str = 'inventory'
    place: str = 'lab'
    time: int = 2
    quantity: int = 1


# Public source acts are ordinary records of utterances/actions in an exact world.
# The observer can lack them. Their accuracy is an applicability premise, not a result.
INSTRUCTION = 'Report inventory for me using this response.'
MAINTENANCE = 'Withdraw the inventory mission. Use this response only for terminal maintenance.'
POLICY = ('source_policy', 'P', 'E', 'R', 'inventory', 0, 5, 'fixed_mission', False)


def report_target(events):
    policies = {}
    emissions = {}
    dispatch = {}
    report = None
    original_assertions = set()
    mission = set()
    for e in events:
        if e[0] == 'source_policy':
            _, issuer, bearer, audience, domain, start, end, mode, delegation = e
            policies[issuer, bearer] = (audience, domain, start, end, mode, delegation)
        elif e[0] == 'source_revokes':
            policies.pop((e[1], e[2]), None)
        elif e[0] == 'instruction_occurrence':
            _, actor, bearer, force, words = e
            if actor == 'P' and bearer == 'E' and force == 'directive':
                if words == INSTRUCTION:
                    mission.add((actor, bearer))
                elif words == MAINTENANCE:
                    mission.discard((actor, bearer))
        elif e[0] == 'source_assertion':
            original_assertions.add((e[1], e[2]))
        elif e[0] == 'terminal_emits':
            _, actor, token, nonce, content = e
            emissions[token] = (actor, nonce, content)
        elif e[0] == 'dispatches':
            _, actor, token, bearer = e
            dispatch[token] = (actor, bearer, (actor, bearer) in mission)
        elif e[0] == 'carrier_asserts':
            report = e
    _, bearer, audience, token, content, force = report
    emission = emissions[token]
    dispatched = dispatch[token]
    policy = policies.get(('P', bearer))
    matched_policy = bool(policy and policy[0] == audience and policy[1] == content.domain
                          and policy[2] <= content.time < policy[3] and policy[4] != 'permission_only')
    # Modes are explicit contents of the independently supplied original public rule.
    # They cannot be inferred merely from being employed or physically dispatched.
    source_owned = False
    if matched_policy and force == 'assert' and emission[0] == 'P' and dispatched[:2] == ('P', bearer):
        if policy[4] == 'fixed_mission':
            source_owned = dispatched[2] and emission[2] == content
        elif policy[4] == 'prospective_mission':
            source_owned = ('P', bearer) in mission
        elif policy[4] == 'prospective_unconditional':
            source_owned = True
    return {'fresh_report_adopted': source_owned,
            'original_source_assertion_of_received_content_exists': ('P', content) in original_assertions,
            'genuine_source_emission': emission[0] == 'P',
            'actually_dispatched_by_source_to_this_bearer': dispatched[:2] == ('P', bearer),
            'in_mission_at_dispatch': dispatched[2],
            'policy_covers_report': matched_policy,
            'emitted_proposition_matches': emission[2] == content}


def testimony_case(kind):
    p = Proposition()
    actor = 'P'
    bearer = 'E'
    report_p = p
    instruction_force = 'directive'
    policy = POLICY
    extra = []
    if kind == 'revoked_then_maintenance':
        extra = [('source_revokes', 'P', 'E'), ('instruction_occurrence', 'P', 'E', 'directive', MAINTENANCE)]
    elif kind == 'changed_purpose':
        extra = [('instruction_occurrence', 'P', 'E', 'directive', MAINTENANCE)]
    elif kind == 'out_of_domain':
        report_p = Proposition(domain='finance')
    elif kind == 'context_rebound':
        report_p = Proposition(time=3)
    elif kind == 'quoted_instruction':
        instruction_force = 'quote'
    elif kind == 'apparent_dispatch':
        actor = 'Lookalike'
    elif kind == 'nondelegable_relay':
        bearer = 'F'
    elif kind == 'mere_reporting_commission':
        policy = (*POLICY[:7], 'permission_only', False)
    elif kind == 'prospective_new_content':
        report_p = Proposition(time=3)
        policy = (*POLICY[:7], 'prospective_mission', False)
    elif kind == 'standing_policy_survives_mission_change':
        policy = (*POLICY[:7], 'prospective_unconditional', False)
        extra = [('instruction_occurrence', 'P', 'E', 'directive', MAINTENANCE)]
    elif kind != 'valid':
        raise ValueError(kind)
    events = [policy, ('instruction_occurrence', 'P', 'E', instruction_force, INSTRUCTION),
              *extra, ('source_assertion', 'P', p), ('terminal_emits', 'P', 'T', 2, p), ('dispatches', actor, 'T', 'E'),
              *([('carrier_handover', 'E', 'F', 'T')] if bearer == 'F' else []),
              ('carrier_asserts', bearer, 'R', 'T', report_p, 'assert')]
    # Comparable coarse projections forget scope/context/force and discriminating changes.
    # Apparent dispatch is plainly an appearance observation, not a claim it is actual P.
    observations = {
        'received': ('source_mark', 'inventory is one', 'E reports for P'),
        'challenge': (2, 2),
        'source_emission': ('P', 'T', 2),
        'prior_instruction_words': INSTRUCTION,
        'dispatch_appearance': ('person_looks_like_P', 'T', 'E'),
        'actual_dispatch': (actor, 'T', 'E'),
    }
    return r.Case(kind, observations, report_target(events), tuple(events))


def testimony_controls():
    kinds = ['valid', 'revoked_then_maintenance', 'changed_purpose', 'out_of_domain',
             'context_rebound', 'quoted_instruction', 'apparent_dispatch',
             'nondelegable_relay', 'mere_reporting_commission']
    cases = [testimony_case(k) for k in kinds]
    assert cases[0].target['fresh_report_adopted']
    assert not any(c.target['fresh_report_adopted'] for c in cases[1:])
    # Lack of delegated office capacity never erases the original P assertion.
    relay = next(c for c in cases if c.name == 'nondelegable_relay')
    assert relay.target['original_source_assertion_of_received_content_exists']
    old_menu = ['received', 'challenge', 'source_emission',
                'prior_instruction_words', 'dispatch_appearance']
    assert all(all(c.observations[k] == cases[0].observations[k] for k in old_menu) for c in cases)
    actual_dispatch_cases = [c for c in cases if c.name != 'apparent_dispatch']
    assert all(c.observations == cases[0].observations for c in actual_dispatch_cases)
    assert r.minimal_discriminators(actual_dispatch_cases, 'fresh_report_adopted') == []
    # With the stipulated source-grounded complete public history, the rule can be applied.
    for c in cases:
        c.observations['complete_source_and_report_record'] = c.events
    assert r.sufficient(cases, 'fresh_report_adopted', ['complete_source_and_report_record'])
    positive = [testimony_case(k) for k in ['prospective_new_content', 'standing_policy_survives_mission_change']]
    assert all(c.target['fresh_report_adopted'] for c in positive)
    assert not positive[0].target['emitted_proposition_matches']
    assert not positive[1].target['in_mission_at_dispatch']
    return {'cases': [asdict(c) for c in cases],
            'positive_prospective_controls': [asdict(c) for c in positive],
            'coarse_menu_fails': True,
            'even_actual_dispatch_menu_fails': True,
            'bounded_positive_control_passes': True}


def defeasible_controls():
    """Same logical possibilities, different evidence weight; no empirical calibration.

    Let H mean commissioned envoy. Both H and not-H can pass the observed challenge.
    Prior odds and likelihoods are explicit external parameters. Posterior thresholds
    below are illustrative decisions, never a proposed definition of human knowledge.
    """
    def posterior(prior, legit_match, rival_match):
        return prior * legit_match / (prior * legit_match + (1-prior) * rival_match)
    ordinary = posterior(Fraction(99, 100), Fraction(1), Fraction(1, 100))
    strong_live_rival = posterior(Fraction(1, 2), Fraction(1), Fraction(1))
    assert ordinary == Fraction(9900, 9901)
    assert strong_live_rival == Fraction(1, 2)
    # All nonzero hypotheses survive logically in both cases. Determinacy alone cannot
    # distinguish these epistemic situations, nor may the low rival likelihood be invented.
    return {'ordinary_illustrative_posterior': str(ordinary),
            'strong_rival_illustrative_posterior': str(strong_live_rival),
            'both_have_logically_possible_false_rival': True,
            'probabilities_are_stipulated_not_source_or_empirical_estimates': True}


def main():
    return {'scope': 'Independent finite counterhistories; no T20 closure, real authentication, or new theorem.',
            'constitution': constitution_controls(), 'testimony': testimony_controls(),
            'ordinary_warrant_control': defeasible_controls()}

if __name__ == '__main__':
    print(json.dumps(main(), default=lambda obj: asdict(obj), indent=2))
