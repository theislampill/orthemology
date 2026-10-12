#!/usr/bin/env python3
"""The Last Moat, Edition 2: deterministic finite and dimensionless checks.

No network, device interaction, physical discovery, or external dependencies.
These are regressions for examples and proof edge cases, not general proofs,
physical validation, or a trained hypothesis generator.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import platform
import sys
from pathlib import Path
from typing import Any, Callable
import verify_models_v1 as v1

require = v1.require
close = v1.close


def residual_comparison_envelope() -> dict[str, Any]:
    rows = []
    for gain in (0.0, 0.4, 1.2):
        initial, residual, horizon = 0.02, 0.01, 1.0
        integral = v1.midpoint(lambda s: math.exp(gain * (horizon-s)) * residual, horizon)
        computed = math.exp(gain * horizon)*initial + integral
        exact = (initial + residual*horizon if gain == 0 else
                 math.exp(gain*horizon)*initial + residual*math.expm1(gain*horizon)/gain)
        close(computed, exact, tolerance=1e-9)
        # A dissipative scalar error is below the same nonnegative-growth envelope.
        damping = 0.8
        dissipative = initial*math.exp(-damping*horizon)+residual*(-math.expm1(-damping*horizon))/damping
        require(dissipative <= exact, 'Comparison envelope underestimates dissipative error.')
        rows.append({'L': gain, 'quadrature_bound': computed, 'closed_form': exact,
                     'dissipative_scalar_error': dissipative})
    return {'rows': rows, 'scope': 'comparison ODE only, not a fluid simulation'}


def bounded_observation_balls() -> dict[str, Any]:
    gain, initial, residual, c_norm, delta = 0.4, 0.02, 0.01, 1.2, 0.04
    bound = math.exp(gain)*initial + residual*math.expm1(gain)/gain
    nominal_distance = 0.4
    state_to_output = c_norm*bound
    radius = state_to_output+delta
    slack = nominal_distance-2*radius
    require(slack > 0, 'The declared observation balls must be disjoint.')
    # Borderline centres separated by the sum of radii share their touching point.
    centres = (0.0, 2*radius)
    touching_point = radius
    close(abs(touching_point-centres[0]), radius)
    close(abs(touching_point-centres[1]), radius)
    return {'state_error_envelope': bound, 'output_error_envelope': state_to_output,
            'noise_radius': delta, 'nominal_distance': nominal_distance,
            'strict_separation_slack': slack, 'equality_is_ambiguous': True}


def uniform_uncertainty_margin() -> dict[str, Any]:
    sigma, eta, kappa, amplitude, beta, delta = 0.8, 0.1, 0.1, 0.4, 0.03, 0.05
    radius = beta+amplitude*eta+kappa*amplitude**2+delta
    half_gap = amplitude*sigma
    slack = half_gap-radius
    require(slack > 0, 'Uniform-reference condition must hold.')
    checked = 0
    for offset, linear_error, rem_sign, noise in itertools.product(
            (-beta, 0.0, beta), (-eta, 0.0, eta), (-1.0, 0.0, 1.0), (-delta, 0.0, delta)):
        for sign in (-1, 1):
            control = sign*amplitude
            received = offset+(sigma+linear_error)*control+rem_sign*kappa*control**2+noise
            reference = sign*half_gap
            require(abs(received-reference) <= radius+1e-12, 'Observation leaves its ball.')
            require(received*sign > 0, 'Uniform sign decoder failed in toy uncertainty grid.')
            checked += 1
    return {'half_gap': half_gap, 'uncertainty_radius': radius, 'slack': slack,
            'finite_grid_observations': checked,
            'scope': 'grid consistency only; general result is the written norm argument'}


def unknown_polarity_counterexample() -> dict[str, Any]:
    amplitude = 1
    possible = {sign: {theta*sign*amplitude for theta in (-1,1)} for sign in (-1,1)}
    for theta in (-1,1):
        require(theta*amplitude != theta*(-amplitude), 'Each known plant should separate.')
    require(possible[-1] == possible[1], 'Uncalibrated labels should be indistinguishable.')
    return {'class_wide_outputs_by_label': {str(k): sorted(v) for k,v in possible.items()},
            'each_known_plant_separates': True, 'no_single_class_wide_decoder': True}


def attained_image_factorisation() -> dict[str, Any]:
    cases = 0
    for size in range(5):
        for feature in itertools.product(range(2), repeat=size):
            image = sorted(set(feature))
            for target in itertools.product(range(2), repeat=size):
                condition = all(feature[i] != feature[j] or target[i] == target[j]
                                for i in range(size) for j in range(size))
                decoders = [dict(zip(image, values)) for values in itertools.product(range(2), repeat=len(image))]
                witnesses = [d for d in decoders if all(d[feature[i]] == target[i] for i in range(size))]
                require(condition == bool(witnesses), 'Fibre condition disagrees with exhaustive decoder search.')
                require(len(witnesses) <= 1, 'Attained-image decoder must be unique.')
                cases += 1
    # Empty target cannot receive a function from a nonempty off-image codomain.
    empty_image_decoders = list(itertools.product((), repeat=0))
    full_nonempty_codomain_decoders = list(itertools.product((), repeat=1))
    require(len(empty_image_decoders) == 1 and not full_nonempty_codomain_decoders, 'Empty-target guard failed.')
    return {'finite_function_cases': cases, 'domain_sizes': list(range(5)),
            'empty_target_extension_counterexample': True}


def evidence_join_soundness() -> dict[str, Any]:
    universe = frozenset(range(3))
    subsets = v1.powerset(universe)
    sound_cases = duplicate_cases = conflicts = 0
    for left, right in itertools.product(subsets, repeat=2):
        joined = left & right
        require(joined == left & right & left, 'Duplicate evidence changed intersection.')
        duplicate_cases += 1
        conflicts += not bool(joined)
        for truth in universe:
            if truth in left and truth in right:
                require(truth in joined, 'Sound constraints lost their common truth.')
                sound_cases += 1
    require(not (frozenset({0}) & frozenset({1})), 'Conflict example is not empty.')
    return {'sound_cases': sound_cases, 'idempotence_cases': duplicate_cases,
            'conflicting_pairs': conflicts, 'conflict_is_not_certification': True}


def relabelled_representations() -> dict[str, Any]:
    size = 7
    encoder = lambda m: (3*m+1) % size
    decoder = lambda z: (z*z+2) % size
    permutations = 0
    for perm in itertools.permutations(range(size)):
        inverse = {z: i for i,z in enumerate(perm)}
        for message in range(size):
            recoded = perm[encoder(message)]
            require(decoder(inverse[recoded]) == decoder(encoder(message)), 'Relabelling changed external output.')
        permutations += 1
    return {'bijections_checked': permutations, 'message_cases': permutations*size}


def finite_corpus_counterexample() -> dict[str, Any]:
    domain = range(6)
    observed = {0: 0, 1: 1, 2: 0, 3: 1}
    first = {x: observed.get(x, 0) for x in domain}
    second = dict(first); second[4] = 1
    require(all(first[x] == second[x] == y for x,y in observed.items()), 'Observed data differ.')
    require(first[4] != second[4], 'Held-out countermodels must disagree.')
    return {'observed_cases': len(observed), 'unobserved_case': 4,
            'two_consistent_hypotheses_disagree': True}


def serial_conditional_reliability() -> dict[str, Any]:
    distribution = {(True,True,True): 0.6, (False,True,True): 0.1,
                    (True,False,True): 0.2, (True,True,False): 0.1}
    close(sum(distribution.values()), 1.0)
    errors = []
    for index in range(3):
        previous = sum(p for status,p in distribution.items() if all(status[:index]))
        first_failure = sum(p for status,p in distribution.items() if all(status[:index]) and not status[index])
        errors.append(first_failure/previous if previous else 0.0)
    any_failure = sum(p for status,p in distribution.items() if not all(status))
    require(any_failure <= sum(errors)+1e-12, 'Conditional serial bound failed.')
    return {'conditional_errors': errors, 'end_to_end_failure': any_failure,
            'sum_bound': sum(errors), 'independence_assumed': False}


def joint_resource_and_role_countermodels() -> dict[str, Any]:
    budget, first, second = 1.0, 0.75, 0.75
    require(first <= budget and second <= budget and first+second > budget, 'Resource countermodel failed.')
    configurations = [{'storage':True, 'execution':False}, {'storage':False,'execution':True}]
    roles = ('storage','execution')
    each_role_somewhere = all(any(c[r] for c in configurations) for r in roles)
    one_complete_witness = any(all(c[r] for r in roles) for c in configurations)
    require(each_role_somewhere and not one_complete_witness, 'Role quantifier countermodel failed.')
    return {'individual_demands': [first, second], 'joint_budget': budget,
            'all_roles_somewhere': each_role_somewhere, 'one_complete_configuration': one_complete_witness}


def mixed_step_error_bound() -> dict[str, Any]:
    gains, defects, initial = [0.5,1.0,0.4,1.0,1.1], [0.01,0.002,0.03,0.0,0.005], 0.2
    actual = initial
    for gain,defect in zip(gains,defects): actual = gain*actual+defect
    bound = math.prod(gains)*initial + sum(math.prod(gains[j+1:])*defects[j] for j in range(len(gains)))
    close(actual,bound)
    require(0.1 > 0.4*0.1, 'A pure identity migration must not receive an execution contraction.')
    return {'step_gains': gains, 'recurrence_value': actual, 'product_formula': bound,
            'identity_migration_gain': 1.0}


def finite_rank_progress() -> dict[str, Any]:
    targets, safe = {0}, set(range(5))
    def successors(x: int) -> set[int]:
        return {0} if x == 0 else {x-1, max(0,x-2)}
    for state in safe-targets:
        require(all(y in safe and y < state for y in successors(state)), 'Rank must decrease outside target.')
    paths = 0
    max_length = 0
    def visit(start: int, state: int, depth: int) -> None:
        nonlocal paths,max_length
        if state in targets:
            require(depth <= start, 'Hitting time exceeds initial rank.')
            paths += 1; max_length = max(max_length,depth)
            return
        for following in successors(state): visit(start,following,depth+1)
    for start in safe: visit(start,start,0)
    # Invariance by itself: self-loop at unfinished state 1 never reaches target 0.
    idle_successors = {0: {0}, 1:{1}}
    require(all(next_ in {0,1} for row in idle_successors.values() for next_ in row), 'Idle model not safe.')
    require(not all(y < 1 for y in idle_successors[1]), 'Idle loop should fail the progress certificate.')
    return {'completed_finite_paths': paths, 'maximum_path_length': max_length,
            'safe_idle_loop_fails_progress': True}


def bounded_paired_state_decision() -> dict[str, Any]:
    size, checked = 3, 0
    def distinguishes(transition: tuple[int,...], output: tuple[int,...], a: int, b: int) -> bool:
        seen = set()
        while (a,b) not in seen:
            if output[a] != output[b]: return True
            seen.add((a,b)); a,b = transition[a],transition[b]
        return False
    for transition in itertools.product(range(size),repeat=size):
        for output in itertools.product(range(2),repeat=size):
            for a,b in itertools.product(range(size),repeat=2):
                verdict = distinguishes(transition,output,a,b)
                finite_seen = False; x,y = a,b
                for _ in range(size*size+1):
                    finite_seen |= output[x] != output[y]
                    x,y = transition[x],transition[y]
                require(verdict == finite_seen, 'Finite product-state bound failed.')
                checked += 1
    delay = 42
    require(not any(t >= delay for t in range(42)), 'Pre-delay history should be equal.')
    require(any(t >= delay for t in range(43)), 'Post-delay history should differ.')
    return {'finite_automaton_initial_pair_cases': checked,
            'scope': 'known finite deterministic systems; not an unrestricted eventual-horizon oracle'}


def heldout_bound_binomial_checks() -> dict[str, Any]:
    checked = 0; max_ratio = 0.0
    for n,p,m,alpha in itertools.product((10,50,100), (0.05,0.2,0.5,0.8,0.95), (1,5), (0.05,0.2)):
        slack = math.sqrt(math.log(m/alpha)/(2*n))
        tail = math.fsum(math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1) if p-k/n > slack)
        require(tail <= alpha/m+1e-12, 'Binomial tail exceeds the per-candidate bound.')
        max_ratio = max(max_ratio,tail/(alpha/m)); checked += 1
    printed = math.sqrt(math.log(4/0.05)/(2*20000))
    return {'exact_binomial_cases': checked, 'max_tail_to_bound_ratio': max_ratio,
            'example_M4_n20000_alpha005_slack': printed}


ADDITIONS: list[tuple[str,Callable[[],dict[str,Any]]]] = [
    ('residual_comparison_ode_envelope',residual_comparison_envelope),
    ('bounded_observation_ball_separation',bounded_observation_balls),
    ('uniform_model_uncertainty_margin',uniform_uncertainty_margin),
    ('uncalibrated_polarity_counterexample',unknown_polarity_counterexample),
    ('attained_image_factorisation_and_empty_guard',attained_image_factorisation),
    ('evidential_join_soundness_and_idempotence',evidence_join_soundness),
    ('latent_relabelling_equivalence',relabelled_representations),
    ('finite_corpus_nonidentification',finite_corpus_counterexample),
    ('serial_reliability_without_independence',serial_conditional_reliability),
    ('joint_resource_and_role_countermodels',joint_resource_and_role_countermodels),
    ('mixed_execution_and_migration_error',mixed_step_error_bound),
    ('finite_rank_progress_and_idle_countermodel',finite_rank_progress),
    ('bounded_paired_state_decidability',bounded_paired_state_decision),
    ('heldout_bound_exact_binomial_tails',heldout_bound_binomial_checks),
]


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='Write the complete JSON result here.')
    args=parser.parse_args()
    checks=[]
    for name,function in [*v1.CHECKS,*ADDITIONS]:
        try:
            details=function()
            checks.append({'name':name,'passed':True,'details':details})
        except Exception as error:
            checks.append({'name':name,'passed':False,'error':f'{type(error).__name__}: {error}'})
    base=Path(__file__).resolve().parent
    report={'title':'The Last Moat — Edition 2: reproducible finite checks',
            'scope':'Finite and dimensionless consistency; not physical validation or proof-assistant verification',
            'python_version':platform.python_version(),
            'source_sha256':{name:hashlib.sha256((base/name).read_bytes()).hexdigest()
                             for name in ('verify_models.py','verify_models_v1.py')},
            'total_checks':len(checks),'passed_checks':sum(row['passed'] for row in checks),
            'all_passed':all(row['passed'] for row in checks),'checks':checks}
    encoded=json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(encoded,encoding='utf-8')
    print(encoded,end='')
    return 0 if report['all_passed'] else 1

if __name__=='__main__':
    sys.exit(main())
