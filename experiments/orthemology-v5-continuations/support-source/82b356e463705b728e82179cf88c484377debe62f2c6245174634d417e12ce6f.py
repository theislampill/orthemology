#!/usr/bin/env python3
"""Finite controls for modal and relation-typing transitions.

These tests do not certify metaphysical possibility or infer real cognition.
The exact retained source predicate conjunction is separately checked in Lean.
"""
import argparse
import itertools
import json
from pathlib import Path


def imply(a, b):
    return not a or b


def giver_priority(source_k, recipient_k):
    return all(imply(r, k) for k, r in zip(source_k, recipient_k))


def complete_nature_determines(nature, source_k):
    return all(imply(n, k) for n, k in zip(nature, source_k))


def check():
    # All rows have one and the same necessarily existing, externally
    # unreceived source. A complete source and noncognitive dependent effect
    # are assumed at both worlds. The variable r table concerns a cognitive
    # dependent effect in addition to that nonvacuous productive background.
    rows = []
    for k0, k1, r0, r1 in itertools.product([False, True], repeat=4):
        k, r = (k0, k1), (r0, r1)
        priority = giver_priority(k, r)
        if priority and r[0]:
            assert k[0], 'Actual giver-priority conditional failed'
        if priority and all(r):
            assert all(k), 'Everywhere cognitive-giving conditional failed'
        if complete_nature_determines((True, True), k):
            assert all(k), 'Intrinsic-determination conditional failed'
        rows.append({'source_k': k, 'cognitive_recipient': r,
                     'worldwise_actual_giver_priority': priority,
                     'source_actually_knows': k[0],
                     'source_standing_knowledge': all(k),
                     'possible_cognitive_giving_everywhere': any(r)})

    gap = next(r for r in rows if r['source_k'] == (True, False)
               and r['cognitive_recipient'] == (True, False))
    assert gap['worldwise_actual_giver_priority']
    assert gap['source_actually_knows']
    assert gap['possible_cognitive_giving_everywhere']
    assert not gap['source_standing_knowledge']
    gap.update({
        'same_source_exists': [True, True],
        'external_cognitive_supplier': [False, False],
        'productive_background_present': [True, True],
        'eligible_cognitive_perfection': [True, True],
        'same_intrinsic_response_law': 'source_k(w) = intrinsic_active_state(w)',
        'intrinsic_active_state': [True, False],
        'complete_standing_determination': False,
    })

    # Merely possible giving does not fix present K. Universal accessibility
    # permits cognitive giving at the other world. This is modal possibility,
    # not a proof of a physically or metaphysically available causal power.
    possible_only = next(r for r in rows if r['source_k'] == (False, True)
                         and r['cognitive_recipient'] == (False, True))
    assert possible_only['worldwise_actual_giver_priority']
    assert possible_only['possible_cognitive_giving_everywhere']
    assert not possible_only['source_actually_knows']

    capacity_only = {
        'capacity': [True, True], 'actual_source_cognition': [False, False],
        'actual_recipient_cognition': [True, False],
        'productive_completeness_granted': True,
        'actual_cognitive_giver_priority': False,
    }
    assert not giver_priority(capacity_only['actual_source_cognition'],
                              capacity_only['actual_recipient_cognition'])

    entities = {'u', 'r', 't'}
    productive = {('u', 'r'), ('u', 't')}
    teaching = {('t', 'r')}
    knows = {'r', 't'}
    roots = lambda rel: sorted(x for x in entities if not any(b == x for a, b in rel))
    cognitive_roots = sorted(x for x in knows if not any(b == x for a, b in teaching))
    assert roots(productive) == ['u']
    assert cognitive_roots == ['t']
    assert all(a in knows and b in knows for a, b in teaching)
    assert ('u', 't') in productive
    relation_typing = {
        'entities': sorted(entities), 'productive_edges': sorted(productive),
        'teaching_edges': sorted(teaching), 'knowers': sorted(knows),
        'productive_roots': roots(productive),
        'terminal_knowing_teachers': cognitive_roots,
        'terminal_teacher_is_productively_received': True,
    }

    noncollapse = {
        'source_exists': [True, True],
        'standing_source_cognition': [True, True],
        'recipient_exists': [True, False],
        'act': ['produce_r', 'produce_z'],
        'truths': [['source_exists', 'r_exists'], ['source_exists', 'r_absent']],
        'source_knows': [['source_exists', 'r_exists'], ['source_exists', 'r_absent']],
        'source_thought_token': ['ta', 'tb'],
    }
    assert all(noncollapse['standing_source_cognition'])
    assert noncollapse['act'][0] != noncollapse['act'][1]
    assert noncollapse['recipient_exists'][0] != noncollapse['recipient_exists'][1]
    assert set(noncollapse['source_thought_token']).__len__() == 2
    for true, known in zip(noncollapse['truths'], noncollapse['source_knows']):
        assert set(known) <= set(true)

    # A no-first-onset restriction alone does not imply persistence into the
    # future. Nor does any temporal restriction connect distinct histories.
    temporal_rows = []
    for row in itertools.product([False, True], repeat=3):
        no_onset = all(imply(row[t], row[t - 1]) for t in [1, 2])
        if no_onset and row[1]:
            assert row[0]
        temporal_rows.append({'cognition_by_time': row, 'no_new_onset': no_onset,
                              'standing_at_every_time': all(row)})
    loss = next(r for r in temporal_rows if r['cognition_by_time'] == (True, True, False))
    assert loss['no_new_onset'] and not loss['standing_at_every_time']

    # Overall and respect-specific comparison are different formal orders.
    # These scores are a mathematical separator, not measured metaphysical
    # worth. A lexicographic power-first aggregate need not preserve K ranking.
    source, recipient = (2, 0), (1, 1)
    assert source > recipient and source[1] < recipient[1]
    comparison = {'coordinates': ['productive_range', 'cognition'],
                  'source': source, 'recipient': recipient,
                  'source_greater_in_power_first_lexicographic_order': True,
                  'source_greater_in_cognition': False}

    # Deliberately false implications must actually have counterinstances.
    negative_controls = {
        'actual_priority_and_actual_knowledge_imply_standing': not any(
            r['worldwise_actual_giver_priority'] and r['source_actually_knows']
            and not r['source_standing_knowledge'] for r in rows),
        'possible_giving_and_priority_imply_present_knowledge': not any(
            r['worldwise_actual_giver_priority'] and r['possible_cognitive_giving_everywhere']
            and not r['source_actually_knows'] for r in rows),
        'no_onset_and_present_knowledge_imply_all_time_knowledge': not any(
            r['no_new_onset'] and r['cognition_by_time'][1]
            and not r['standing_at_every_time'] for r in temporal_rows),
    }
    assert all(v is False for v in negative_controls.values())
    return {
        'status': 'PASS_FINITE_BRIDGE_CONTROLS',
        'modal_assignments_exhaustively_checked': len(rows),
        'temporal_assignments_exhaustively_checked': len(temporal_rows),
        'positive_conditionals': [
            'Actual cognitive giving + priority implies actual source Knowledge',
            'Everywhere cognitive giving + priority implies standing source Knowledge',
            'Everywhere source nature + intrinsic determination implies standing Knowledge',
        ],
        'modal_recipient_gap': gap,
        'possible_giving_without_present_knowledge': possible_only,
        'capacity_without_actuality': capacity_only,
        'relation_root_separation': relation_typing,
        'standing_without_token_or_effect_invariance': noncollapse,
        'no_onset_without_no_loss': loss,
        'comparison_respect_separator': comparison,
        'negative_controls_claims_are_false': negative_controls,
        'semantic_limits': [
            'Cognition is granted, not inferred from behaviour',
            'Finite frames do not certify metaphysical possibilities',
            'No completeness result for all possible metaphysical accounts',
            'Exact retained source predicate validation is in the separate Lean replay',
        ],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = check()
    rendered = json.dumps(result, indent=2) + '\n'
    if args.out:
        args.out.write_text(rendered)
    print(rendered, end='')
