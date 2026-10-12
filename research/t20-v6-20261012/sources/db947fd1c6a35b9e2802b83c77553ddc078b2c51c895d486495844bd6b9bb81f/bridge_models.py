"""Finite structural checks for the source and intentionality research note.

These are models of explicitly stipulated modal/hosting signatures, not proofs
of metaphysical possibility. Analytic proofs are given in the companion note.
No free Personal/Wise truth flags are used to manufacture the principal
countermodels: the key differences are existence, hosting, and grounding
relations, together with a type/occurrence distinction.
"""

from itertools import product
import json
from pathlib import Path


def modal_ground_checks(nworlds=3, nobjects=2, nonempty_worlds=False):
    worlds = range(nworlds)
    objects = range(nobjects)
    edges = [(w, y, x) for w in worlds for y in objects for x in objects if y != x]
    counts = dict(admissible=0, strong_actual_root_cases=0,
                  weak_essential_root_cases=0, weak_actual_counterexamples=0,
                  weak_models_without_any_necessary_bearer=0)
    counterexample = None
    for bits in product((False, True), repeat=nworlds*nobjects):
        exists = {(w, x): bits[w*nobjects+x] for w in worlds for x in objects}
        if nonempty_worlds and not all(any(exists[w, x] for x in objects) for w in worlds):
            continue
        for ebits in product((False, True), repeat=len(edges)):
            ground = {e for e, present in zip(edges, ebits) if present}
            if any(not (exists[w, y] and exists[w, x]) for w, y, x in ground):
                continue
            def has_cycle(w):
                def visit(x, path):
                    return any(y in path or visit(y, path | {y})
                               for ww, xx, y in ground if ww == w and xx == x)
                return any(visit(x, {x}) for x in objects)
            if any(has_cycle(w) for w in worlds):
                continue
            counts['admissible'] += 1
            incoming = lambda w, x: any((w, y, x) in ground for y in objects)
            necessary = lambda x: all(exists[w, x] for w in worlds)
            contingent_actual = lambda x: exists[0, x] and not necessary(x)
            strong = all(not contingent_actual(x) or incoming(0, x) for x in objects)
            # The weaker principle is nevertheless imposed globally: every
            # object existing in any admitted world, if contingent, has a
            # grounding world. Universal accessibility is stipulated here.
            weak = all(not (any(exists[w, x] for w in worlds) and not necessary(x))
                       or any(incoming(w, x) for w in worlds) for x in objects)
            if weak and any(exists[0, x] for x in objects) and not any(necessary(x) for x in objects):
                counts['weak_models_without_any_necessary_bearer'] += 1
            for x in objects:
                actual_root = exists[0, x] and not incoming(0, x)
                essential_root = exists[0, x] and all(not incoming(w, x) for w in worlds)
                if strong and actual_root:
                    counts['strong_actual_root_cases'] += 1
                    assert necessary(x)
                if weak and essential_root:
                    counts['weak_essential_root_cases'] += 1
                    assert necessary(x)
                if weak and actual_root and not necessary(x):
                    counts['weak_actual_counterexamples'] += 1
                    if counterexample is None:
                        counterexample = {
                            'target': x,
                            'exists_by_world': [[z for z in objects if exists[w, z]] for w in worlds],
                            'ground_edges_w_grounder_target': sorted(ground),
                        }
    return {**counts, 'grounding_acyclic_at_each_world': True,
            'each_world_nonempty': nonempty_worlds,
            'first_weak_actual_counterexample': counterexample}


def hosting_checks(nworlds=3, nhosts=3):
    """One stipulated necessarily existing token, varying hosting relations."""
    worlds, hosts = range(nworlds), range(nhosts)
    counts = dict(covered_hosting_relations=0, essential_hosting_cases=0,
                  necessary_token_without_fixed_host_cases=0)
    witness = None
    for bits in product((False, True), repeat=nworlds*nhosts):
        hs = [frozenset(h for h in hosts if bits[w*nhosts+h]) for w in worlds]
        if not all(hs):
            continue
        counts['covered_hosting_relations'] += 1
        common = set.intersection(*(set(h) for h in hs))
        essential = all(hs[w] == hs[0] for w in worlds)
        if essential:
            counts['essential_hosting_cases'] += 1
            assert common
        if not common:
            counts['necessary_token_without_fixed_host_cases'] += 1
            if witness is None:
                witness = [sorted(h) for h in hs]
    return {**counts, 'first_switching_host_witness': witness}


def typed_architecture_checks():
    worlds = ('w0', 'w1', 'w2')
    # A type exists throughout, while each of its tokens has one essential
    # owner and exists in only one world. Every world has a hosted occurrence.
    tokens = {
        't0': {'worlds': {'w0'}, 'owner': 'h0', 'type': 'p'},
        't1': {'worlds': {'w1'}, 'owner': 'h1', 'type': 'p'},
        't2': {'worlds': {'w2'}, 'owner': 'h2', 'type': 'p'},
    }
    host_worlds = {f'h{i}': {f'w{i}'} for i in range(3)}
    type_exists = set(worlds)
    covered = all(any(w in t['worlds'] for t in tokens.values()) for w in worlds)
    essential_owner = all(t['worlds'] <= host_worlds[t['owner']] for t in tokens.values())
    necessary_host = any(set(worlds) <= ws for ws in host_worlds.values())
    necessary_token = any(set(worlds) <= t['worlds'] for t in tokens.values())
    assert type_exists == set(worlds) and covered and essential_owner
    assert not necessary_host and not necessary_token

    # Grounding-to-bearing counterarchitecture: g supports local h, and h
    # hosts a thought. The hosting extension contains no pair (g,t).
    ground = {('g', 'h')}
    host = {('h', 't')}
    mental_bearers_under_hosting_theory = {h for h, t in host}
    assert ('g', 'h') in ground and 'h' in mental_bearers_under_hosting_theory
    assert 'g' not in mental_bearers_under_hosting_theory

    # Two causal histories end in the same present truth-tracking mechanism.
    # Correspondence = whether a token correctly indicates a target. It is
    # held as an independently interpreted coordinate, not discovered here.
    retention_truth_selected = {0: 0.1, 1: 0.9}
    retention_bottleneck = {0: 0.9, 1: 0.9}
    present_response = {0: 0, 1: 1}
    assert retention_truth_selected[0] != retention_truth_selected[1]
    assert retention_bottleneck[0] == retention_bottleneck[1]

    # A nonempty, unique-root world at every index, but no necessary bearer.
    # Three objects permit a three-world rotation, with no in-world cycle.
    rotation_exists = ({'x', 'y'}, {'y', 'z'}, {'z', 'x'})
    rotation_ground = ({('x', 'y')}, {('y', 'z')}, {('z', 'x')})
    obj = {'x', 'y', 'z'}
    assert all(es for es in rotation_exists)
    assert not any(all(x in es for es in rotation_exists) for x in obj)
    assert all(any(any(v == x for _, v in gs) for gs in rotation_ground) for x in obj)
    assert all(len(es - {v for _, v in gs}) == 1
               for es, gs in zip(rotation_exists, rotation_ground))
    return {
        'necessary_type_worldwise_hosted_essential_token_owners': {
            'type_exists_all_worlds': True,
            'every_world_has_token': covered,
            'every_token_has_essential_owner': essential_owner,
            'some_necessary_token': necessary_token,
            'some_necessary_host': necessary_host,
            'tokens': {k: {**v, 'worlds': sorted(v['worlds'])} for k, v in tokens.items()},
        },
        'grounding_does_not_transfer_hosting': {
            'ground_edges': sorted(ground),
            'hosting_edges': sorted(host),
            'mental_bearers_under_explicit_hosting_theory': sorted(mental_bearers_under_hosting_theory),
        },
        'present_function_vs_historical_fixing': {
            'same_present_response': present_response,
            'truth_selected_retention': retention_truth_selected,
            'bottleneck_retention': retention_bottleneck,
            'ceiling': 'Causal retention contrast only; not proof of truth as an intrinsic normative aim.',
        },
        'nonempty_worlds_rotating_unique_roots': {
            'exists_by_world': [sorted(es) for es in rotation_exists],
            'ground_edges_by_world': [sorted(gs) for gs in rotation_ground],
            'each_world_has_unique_root': True,
            'every_bearer_is_contingent_and_possibly_grounded': True,
            'some_necessary_bearer': False,
        },
    }


if __name__ == '__main__':
    results = {
        'modal_3worlds_2objects': modal_ground_checks(),
        'modal_2worlds_2objects': modal_ground_checks(2, 2),
        'modal_3worlds_2objects_nonempty': modal_ground_checks(3, 2, True),
        'modal_4worlds_2objects_nonempty': modal_ground_checks(4, 2, True),
        'hosting_3worlds_3hosts': hosting_checks(),
        'architectures': typed_architecture_checks(),
        'scope': 'Finite signature consistency and deletion checks, not metaphysical-possibility or probability certificates.',
    }
    out = Path(__file__).with_name('bridge_model_results.json')
    out.write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))
