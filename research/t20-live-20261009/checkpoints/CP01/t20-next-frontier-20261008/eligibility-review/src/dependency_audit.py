#!/usr/bin/env python3
"""Exact premise-removal audit, not a model of perfected/necessary beings.

The predicates below are proposition or relation interpretations used solely to
check stated implications. They authenticate no metaphysical bearer, causal
support, source interpretation, or pure-perfection classification.
"""
from itertools import product
import json


def implies(a, b):
    return not a or b


def eligibility_audit():
    names = ('O', 'H', 'P', 'R', 'K', 'D', 'identity_acquisition', 'donor', 'consolidation')
    rows = [dict(zip(names, values)) for values in product((False, True), repeat=len(names))]
    # H is the source's unrestricted pure-perfection requirement, NOT merely a
    # maximal element among some restricted set of already admitted bearers.
    premises = {
        'original_requires_unrestricted_perfection': lambda v: implies(v['O'], v['H']),
        'unrestricted_perfection_excludes_pure_deficiency': lambda v: implies(v['H'], not v['D']),
        'receptive_pure_lack_is_deficient': lambda v: implies(v['P'] and v['R'] and not v['K'], v['D']),
        'nonreceptive_pure_lack_is_deficient': lambda v: implies(v['P'] and not v['R'], v['D']),
    }
    conclusion = lambda v: implies(v['O'] and v['P'], v['K'])
    full = [v for v in rows if all(p(v) for p in premises.values())]
    assert full and all(conclusion(v) for v in full)
    positive = [v for v in full if v['O'] and v['P']]
    # No acquisition, donor, or consolidation hypothesis is in the proof.
    assert any(all(not v[k] for k in ('identity_acquisition', 'donor', 'consolidation')) for v in positive)
    irrelevant_combinations = set(tuple(v[k] for k in ('identity_acquisition', 'donor', 'consolidation')) for v in positive)
    assert len(irrelevant_combinations) == 8
    ablations = {}
    for removed in premises:
        witnesses = [v for v in rows if all(p(v) for name, p in premises.items() if name != removed) and not conclusion(v)]
        assert witnesses
        ablations[removed] = witnesses[0]
    return {
        'interpretation': 'Logical implication and minimal premise set only; not a metaphysical countermodel.',
        'valuation_count': len(rows),
        'full_premise_valuation_count': len(full),
        'original_and_pure_valuation_count': len(positive),
        'conclusion': 'O and P imply K',
        'countervaluations_to_full_implication': 0,
        'independent_acquisition_donor_consolidation_combinations': len(irrelevant_combinations),
        'necessary_premise_removal_witnesses': ablations,
    }


def donor_audit():
    cases = []
    for sbits in product((False, True), repeat=4):
        source = {(a, p): sbits[2*a+p] for a in range(2) for p in range(2)}
        if not all(any(source[a,p] for a in range(2)) for p in range(2)):
            continue
        if not all(any(source[a,p] for p in range(2)) for a in range(2)):
            continue
        for hbits in product((False, True), repeat=4):
            has = {(a,p):hbits[2*a+p] for a in range(2) for p in range(2)}
            if all(implies(source[a,p], has[a,p]) for a in range(2) for p in range(2)):
                cases.append((source, has))
    def all_sources_all_perfections(case):
        return all(case[1].values())
    bad = [case for case in cases if not all_sources_all_perfections(case)]
    assert bad
    # The donor principle still guarantees a perfected giver for EACH effect.
    assert all(all(any(s[a,p] and h[a,p] for a in range(2)) for p in range(2)) for s,h in cases)
    source, has = bad[0]
    return {
        'interpretation': 'Quantifier structure only; source and perfection labels do not certify original agents.',
        'satisfying_assignments': len(cases),
        'counterassignments_to_every_source_every_perfection': len(bad),
        'witness': {'gives': [[int(source[a,p]) for p in range(2)] for a in range(2)],
                    'has': [[int(has[a,p]) for p in range(2)] for a in range(2)]},
    }


def dependence_audit():
    counts = {}
    for n in range(1,5):
        edges = [(x,y) for x in range(n) for y in range(n) if x != y]
        accepted = 0
        original_sizes = set()
        for obits in product((False, True), repeat=n):
            originals = {x for x in range(n) if obits[x]}
            for dbits in product((False, True), repeat=len(edges)):
                deps = {edge for edge, present in zip(edges, dbits) if present}
                independent = all(not any(x==o for x,y in deps) for o in originals)
                universal = all((other,o) in deps for o in originals for other in range(n) if other != o)
                if independent and universal:
                    accepted += 1
                    original_sizes.add(len(originals))
                    assert len(originals) <= 1
        counts[str(n)] = {'accepted_relational_assignments': accepted,
                          'possible_original_cardinalities': sorted(original_sizes)}
    # Restricting universality to created effects changes the implication.
    originals = {0,1}
    effects = {2}
    deps = {(2,0),(2,1)}
    assert all(not any(x==o for x,y in deps) for o in originals)
    assert all((e,o) in deps for e in effects for o in originals)
    assert not all((other,o) in deps for o in originals for other in range(3) if other != o)
    # Both material premises are needed, as abstract relation constraints.
    without_universality = {'originals':[0,1], 'depends':[]}
    without_independence = {'originals':[0,1], 'depends':[[0,1],[1,0]]}
    return {
        'interpretation': 'All uses of depends must have the SAME completion relation and respect; own attributes and abstractions are outside the actual distinct external bearer domain.',
        'full_external_domain_exhaustive_checks': counts,
        'conclusion': 'At most one original; existence is not proved.',
        'created_effect_domain_assignment': {'originals':sorted(originals), 'created_effects':sorted(effects), 'depends':[list(x) for x in sorted(deps)]},
        'scope_of_assignment': 'Preserves created-only universality and underivedness relation constraints. Denies universality over distinct external originals. Does not establish genuine joint original efficacy or satisfy the full source hierarchy.',
        'remove_universality_assignment': without_universality,
        'remove_independence_assignment': without_independence,
    }


def main():
    result = {'eligibility':eligibility_audit(), 'donor_quantifiers':donor_audit(), 'universal_dependence':dependence_audit()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
