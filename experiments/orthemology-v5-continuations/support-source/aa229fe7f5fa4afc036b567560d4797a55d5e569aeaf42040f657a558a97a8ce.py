#!/usr/bin/env python3
"""Finite controls for a human-proved source-bound integration, not a proof assistant.
Enumerates actual corruption scenarios, report observations, transitions and
root-copy policies; formulas are checked against those independent finite objects.
Only Python standard library; no network, mutation of canonical sources, or imports.
"""
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def subsets(items, upper):
    items = tuple(items)
    return [frozenset(x) for k in range(upper + 1) for x in combinations(items, k)]


def compatible(report, theta, faults):
    return all(report[i] == theta for i in range(len(report)) if i not in faults)


def majority(report):
    return int(sum(report) > len(report) // 2)


def live_faults(report, theta, budget):
    return [c for c in subsets(range(len(report)), budget) if compatible(report, theta, c)]


def safe_roots(live, n):
    return [i for i in range(n) if all(i not in c for c in live)]


def transition(mode, state, root, faults):
    # No receipt label influences causal successor.
    if mode == 'destructive':
        if state == 'X':
            return 'X'
        return 'X' if root in faults else 'G'
    if mode == 'fail_silent':
        return state if root in faults else 'G'
    raise ValueError(mode)


def damage_risk(weights, live):
    return max(sum((weights[i] for i in c), Fraction()) for c in live)


def lattice(total, n):
    if n == 1:
        yield (total,)
    else:
        for x in range(total + 1):
            for rest in lattice(total - x, n - 1):
                yield (x,) + rest


results = {'scope': 'Finite executable controls; general claims have separate human proofs', 'families': []}
for f in range(1, 4):
    n = 2 * f + 1
    faults = subsets(range(n), f)
    code0, code1 = (0,) * n, (1,) * n
    distance = sum(x != y for x, y in zip(code0, code1))
    # Transversal of singleton hyperedges, found without using n formula.
    edges = [frozenset({i}) for i in range(n)]
    all_root_sets = subsets(range(n), n)
    transversals = [c for c in all_root_sets if all(c & e for e in edges)]
    kappa = min(map(len, transversals))
    assert distance >= 2 * f + 1 and kappa > f
    report_scenarios = 0
    report_views = 0
    distribution_controls = 0
    for theta in (0, 1):
        for c in faults:
            for corrupt_bits in product((0, 1), repeat=len(c)):
                y = [theta] * n
                for i, b in zip(sorted(c), corrupt_bits):
                    y[i] = b
                report_scenarios += 1
                assert majority(y) == theta
        for y in product((0, 1), repeat=n):
            if majority(y) != theta:
                continue
            live = live_faults(y, theta, f)
            if not live:
                continue
            report_views += 1
            mismatch = frozenset(i for i, b in enumerate(y) if b != theta)
            k = len(mismatch)
            # Independent enumeration of compatible worlds yields exact root integrity.
            assert set(live) == {c for c in faults if mismatch <= c}
            expected_safe = set(range(n)) - mismatch if k == f else set()
            assert set(safe_roots(live, n)) == expected_safe
            uniform = [Fraction(0) if i in mismatch else Fraction(1, n-k) for i in range(n)]
            exact = Fraction(f-k, n-k)
            assert damage_risk(uniform, live) == exact
            if n <= 5:
                for raw in lattice(6, n):
                    p = [Fraction(x, 6) for x in raw]
                    assert damage_risk(p, live) >= exact
                    distribution_controls += 1
    # All distinct-root action orders of the guaranteed batch length, all static faults.
    batch_controls = 0
    for c in faults:
        for order in permutations(range(n), f+1):
            q = 'U'
            for i in order:
                q = transition('fail_silent', q, i, c)
                assert q != 'X'
            assert q == 'G'
            for i in range(n):
                assert transition('fail_silent', q, i, c) == 'G'
            batch_controls += 1
    # Every deterministic first root fails in a static permissible world, even on unanimous y.
    unanimous = live_faults((0,)*n, 0, f)
    for i in range(n):
        assert any(transition('destructive', 'U', i, c) == 'X' for c in unanimous)
    results['families'].append(dict(f=f, n=n, root_distance=distance, kappa=kappa,
        report_scenarios=report_scenarios, report_views=report_views,
        rational_distribution_controls=distribution_controls,
        fail_silent_batch_controls=batch_controls,
        unanimous_minimax_failure=str(Fraction(f,n))))

# A semantic synchronization control, including root-to-report binding.
f, n, theta = 1, 3, 0
y = (0, 0, 1)
full_safe = safe_roots(live_faults(y, theta, f), n)
majority_fibre = [x for x in product((0,1), repeat=n) if majority(x) == theta]
multiset_fibre = sorted(set(permutations(y)))
majority_live = set(c for x in majority_fibre for c in live_faults(x, theta, f))
multiset_live = set(c for x in multiset_fibre for c in live_faults(x, theta, f))
assert full_safe == [0, 1]
assert safe_roots(majority_live, n) == []
assert safe_roots(multiset_live, n) == []
results['synchronization'] = dict(full_report=list(y), full_report_safe_roots=full_safe,
    majority_summary_safe_roots=[], unlabelled_multiset_safe_roots=[])

# Copies are separate numerical carriers with one shared actual fault unit.
copy_roots = [0]*40 + [1] + [2]
copy_weights = [Fraction(copy_roots.count(i), len(copy_roots)) for i in range(n)]
root_weights = [Fraction(1,n)]*n
live = live_faults((0,)*n, theta, f)
assert damage_risk(copy_weights, live) == Fraction(20,21)
assert damage_risk(root_weights, live) == Fraction(1,3)
q='U'
for copied_carrier in (0,1):
    q=transition('fail_silent', q, copy_roots[copied_carrier], frozenset({0}))
assert q=='U'  # f+1 distinct carriers are insufficient: these share one root.
results['copies'] = dict(carriers=42, roots=3, uniform_carrier_failure='20/21',
    uniform_root_failure='1/3', distinct_carrier_batch_can_fail=True)

# Source labels cannot create success: a corrupt route can emit a deceptive SUCCESS.
q=transition('fail_silent', 'U', 0, frozenset({0}))
claimed_receipt='SUCCESS'
assert claimed_receipt=='SUCCESS' and q=='U'
for i in (0,1):
    q=transition('fail_silent', q, i, frozenset({0}))
assert q=='G'  # The fixed batch does not depend on that untrusted receipt.
results['false_success'] = dict(early_stop_fails=True, fixed_batch_succeeds=True)

# Exact loss mismatch: one damage event versus every time step outside the true target.
loss_controls=[]
for horizon in (1,2,10,100):
    q='U'; damage_events=0; target_bad_visits=0
    for t in range(horizon):
        target_bad_visits += int(q!='G')
        q2=transition('destructive',q,0,frozenset({0}))
        damage_events += int(q!='X' and q2=='X')
        q=q2
    assert damage_events==1 and target_bad_visits==horizon
    loss_controls.append(dict(horizon=horizon, damage_events=damage_events,
        literal_nontarget_visits=target_bad_visits))
results['loss_controls']=loss_controls
results['all_checks_passed']=True
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))

# Guard-deletion controls: these deliberately violate stated contracts and must fail.
# Separate sensor/actuator fault budgets defeat the saturation-to-safe-actuation inference.
sensor_report=(0,0,1)
sensor_faults=frozenset({2})
actuator_faults=frozenset({0})
assert compatible(sensor_report,0,sensor_faults)
assert safe_roots(live_faults(sensor_report,0,1),3)==[0,1]
assert transition('destructive','U',0,actuator_faults)=='X'
# A mobile fault unit can follow each fixed distinct-root attempt, defeating S.
q='U'
for root in (0,1):
    q=transition('fail_silent',q,root,frozenset({root}))
assert q=='U'
# Two aliases of one corrupt root are not two independent root coordinates.
actual_theta=1
actual_roots_of_carriers=[0,0,1]
actual_faults=frozenset({0})
carrier_reports=tuple(0 if root in actual_faults else actual_theta for root in actual_roots_of_carriers)
assert majority(carrier_reports)!=actual_theta
results['guard_deletions']=dict(uncoupled_actuator_fault_breaks_saturation=True,
    mobile_faults_break_fixed_batch=True, alias_count_breaks_majority=True)
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(results, indent=2)+'\n')
print('Guard-deletion controls PASS')

# Whole-rule semantics: two serial modules, exactly one hidden constant-1 fault.
# Correct target is independently specified as identity on both inputs.
def runtime_output(flags, z):
    value=z
    for fault_active in flags:
        value=1 if fault_active else value
    return value

def install_module_repair(flags, module):
    result=list(flags); result[module]=False
    return tuple(result)

whole_rule_controls=0
for hidden_module in (0,1):
    flags=tuple(i==hidden_module for i in (0,1))
    assert [runtime_output(flags,z) for z in (0,1)]==[1,1]
    good=install_module_repair(flags,hidden_module)
    bad=install_module_repair(flags,1-hidden_module)
    assert [runtime_output(good,z) for z in (0,1)]==[0,1]
    assert [runtime_output(bad,z) for z in (0,1)]==[1,1]
    assert install_module_repair(good,hidden_module)==good
    # Correcting a current output value does not change either generator flag.
    current_corrected_output=0
    assert current_corrected_output==0 and runtime_output(flags,0)==1
    whole_rule_controls+=1
results['whole_rule_semantics']=dict(hidden_module_cases=whole_rule_controls,
    correct_repair_handles_entire_binary_input_class=True,
    wrong_module_and_output_clamp_do_not_restore=True)
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(results, indent=2)+'\n')
print('Whole-rule semantic controls PASS')

# Hidden trust-root audit: a common containment gate is a common cut failure.
gate='gate'
actual_supports=[frozenset({gate,i}) for i in range(3)]
root_universe=[gate,0,1,2]
gate_transversals=[c for c in subsets(root_universe,len(root_universe)) if all(c&e for e in actual_supports)]
actual_kappa=min(map(len,gate_transversals))
assert actual_kappa==1
assert all(frozenset({gate})&support for support in actual_supports)
q='U'
for root in (0,1):
    # Gate corruption allows precisely the destructive behavior that S had excluded.
    q='X' if gate in frozenset({gate}) else transition('fail_silent',q,root,frozenset())
assert q=='X'
results['containment_gate']=dict(actual_kappa=actual_kappa,
    common_gate_in_fault_budget_defeats_positive_batch=True,
    gate_exclusion_is_additional_trusted_base_premise=True)
(HERE/'CHECK_RESULTS.json').write_text(json.dumps(results, indent=2)+'\n')
print('Containment trust-root control PASS')
