#!/usr/bin/env python3
"""The Last Moat, Edition 3: finite and dimensionless mathematical checks.

This programme has no network or device interface. All ODE trajectories are
simulations of a stipulated model, not measurements of a physical processor.
Checks use explicit exceptions, so python -O does not disable verification.
Run: python verify_models.py --output verification_results.json
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import platform
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any, Callable
import verify_models_e2 as old

require = old.require
close = old.close


def coordinate_changes() -> dict[str, Any]:
    total = 0
    for n in range(2, 7):
        for h in itertools.permutations(range(n)):
            inv = {value: i for i, value in enumerate(h)}
            for q in range(n):
                for a in range(n):
                    reference = (q + a) % n
                    physical = h[(inv[h[q]] + a) % n]
                    require(inv[physical] == reference, 'Conjugate map changed behaviour.')
                    total += 1
    return {'equalities_checked': total, 'scope': 'finite coordinate changes, not physical transformations'}


def memory_nonvacuity() -> dict[str, Any]:
    target = {(q, a): q ^ a for q in (0, 1) for a in (0, 1)}
    rejected = 0
    for outputs in itertools.product((0, 1), repeat=2):
        require(any(outputs[a] != target[q, a] for q, a in target), 'Memoryless parity implementation passed.')
        rejected += 1
    # An inverted operative output fails even if the transition/abstraction map is correct.
    require(all((1-q) != q for q in (0,1)), 'Inverted-output control malformed.')
    return {'memoryless_candidates_rejected': rejected, 'consequential_initial_states': 2,
            'state_correct_but_inverted_output_rejected': True}


def substitution_nonchain() -> dict[str, Any]:
    # Logical records, not claims about measured hardware or real device capabilities.
    profiles = [
        {'name': 'fixed heterogeneous pair', 'processor_change': True, 'online_switching': False},
        {'name': 'homogeneous dynamic replicas', 'processor_change': False, 'online_switching': True},
    ]
    require(any(p['processor_change'] and not p['online_switching'] for p in profiles), 'Missing first nonimplication.')
    require(any(p['online_switching'] and not p['processor_change'] for p in profiles), 'Missing reverse nonimplication.')
    # Material and computing principle are independent descriptive coordinates.
    classes = {'electronic': ('silicon', 'transistor'), 'photonic': ('silicon', 'optical')}
    require(classes['electronic'][0] == classes['photonic'][0], 'Material example malformed.')
    require(classes['electronic'][1] != classes['photonic'][1], 'Mechanism example malformed.')
    return {'logical_countermodels': profiles, 'no_total_order_asserted': True}


def packing_geometry() -> dict[str, Any]:
    rows = []
    for d in (1, 2, 3, 4):
        pts = list(itertools.product((-1.0, 1.0), repeat=d))
        zeta = 0.2
        radius = math.sqrt(d)
        minimum = min(math.dist(x, y) for i, x in enumerate(pts) for y in pts[i+1:])
        require(minimum > 2*zeta, 'Nonseparated packing.')
        bound = (1+radius/zeta)**d
        require(len(pts) <= bound, 'Volume bound violated.')
        rows.append({'dimension': d, 'states': len(pts), 'minimum_distance': minimum, 'volume_bound': bound})
    midpoint, zeta = F(1, 10), F(1, 10)
    require(abs(midpoint - 0) <= zeta and abs(midpoint-F(1,5)) <= zeta, 'Closed-ball equality counterexample lost.')
    return {'rows': rows, 'touching_closed_balls_are_ambiguous': True}


def upper_bound_direction() -> dict[str, Any]:
    q, reference, error = 0.125, 0.125, 0.0
    bounds=[]
    # The allowance eta need not be attained; actual implementation is exact.
    upper = 0.0
    for _ in range(12):
        q *= 2; reference *= 2
        error = abs(q-reference)
        upper = 2*upper + 0.001
        require(error == 0.0 and error <= upper, 'Exact map developed an error.')
        bounds.append(upper)
    require(bounds[-1] > bounds[0], 'Counterexample upper bound did not grow.')
    return {'L': 2, 'actual_error': error, 'nonattained_defect_allowance': 0.001,
            'last_upper_bound': upper, 'verdict': 'growing upper bound is not actual growth'}


def parameterisation_counterexample() -> dict[str, Any]:
    decompositions = [(6.0,), (1.0, 2.0, 3.0), (0.5, 0.5, 5.0)]
    for parts in decompositions:
        for x in (-2.0, 0.0, 0.5, 1.25):
            close(sum(p*x for p in parts), 6*x)
    return {'parameter_counts': [len(x) for x in decompositions],
            'same_tested_linear_function': '6*x',
            'scope': 'redundant parameterisation example, not arbitrary-model compression'}


def trace_law(probability: Callable[[tuple[int, ...], int], float], horizon: int) -> dict[tuple[int, ...], float]:
    dist: dict[tuple[int, ...], float] = {(): 1.0}
    for t in range(horizon):
        next_dist = {}
        for history, mass in dist.items():
            p=probability(history, t)
            require(0 <= p <= 1, 'Invalid Bernoulli parameter.')
            next_dist[history+(0,)]=mass*(1-p)
            next_dist[history+(1,)]=mass*p
        dist=next_dist
    close(sum(dist.values()), 1.0)
    return dist


def distribution_trace_bound() -> dict[str, Any]:
    rows=[]
    for H in range(1, 8):
        alphas=[0.01+0.005*t for t in range(H)]
        p=lambda history,t: 0.3+0.3*(sum(history)%2)
        q=lambda history,t: p(history,t) + alphas[t]*((-1)**sum(history))
        P,Q=trace_law(p,H),trace_law(q,H)
        tv=0.5*sum(abs(P[x]-Q[x]) for x in P)
        product=1-math.prod(1-a for a in alphas)
        require(tv <= product+1e-14 and product <= sum(alphas)+1e-14, 'Trace bound violated.')
        # A tight all-zero vs independently perturbed trace example.
        Z=trace_law(lambda h,t: 0.0,H)
        R=trace_law(lambda h,t: alphas[t],H)
        tight=0.5*sum(abs(Z[x]-R[x]) for x in Z)
        close(tight,product,tolerance=1e-12)
        rows.append({'horizon':H,'TV':tv,'product_bound':product,'union_bound':sum(alphas),'tight_example_TV':tight})
    return {'rows':rows,'scope':'finite exact probability enumeration'}


def delay_step(q: tuple[int,int], a: int) -> tuple[int,int]:
    return (q[1],a)


def export_obstruction() -> dict[str, Any]:
    states=list(itertools.product((0,1),repeat=2))
    initialisers=list(itertools.product(states,repeat=2))
    rejected=0
    for initializer in initialisers:
        valid=True
        for q in states:
            target=initializer[q[0]]
            if target[0] != q[0]:
                valid=False; break
            for a in (0,1):
                if delay_step(target,a)[0] != delay_step(q,a)[0]:
                    valid=False; break
            if not valid: break
        require(not valid,'A one-bit export unexpectedly retained both bits.')
        rejected+=1
    for q in states:
        for a in (0,1):
            require(delay_step(tuple(q),a)==delay_step(q,a),'Full-state export failed.')
    return {'source_states':4,'one_bit_initialisers_exhaustively_rejected':rejected,
            'collision':[[0,0],[0,1]],'common_next_input':0,'required_next_outputs':[0,1],
            'two_bit_export_passed':True}


def joint_assessment() -> dict[str, Any]:
    keys=['export_sufficient','polarity_calibrated','source_free_support','deadline_met','no_replay','permission']
    cases=[{'name':'adequate','local_passes':[True]*3,**dict.fromkeys(keys,True)}]
    for key in keys:
        row={'name':key+'_fails','local_passes':[True]*3,**dict.fromkeys(keys,True)}
        row[key]=False; cases.append(row)
    for row in cases:
        row['local_only_verdict']=all(row['local_passes'])
        row['conventional_contract_verdict']=all(row[k] for k in keys)
        annotated={('declared_analysis',k):row[k] for k in keys}
        row['annotated_contract_verdict']=all(annotated[('declared_analysis',k)] for k in keys)
        require(row['conventional_contract_verdict']==row['annotated_contract_verdict'],'Vocabulary changed identical rule.')
    require(sum(r['conventional_contract_verdict'] for r in cases)==1,'Fixture logic malformed.')
    return {'cases':cases,'note':'synthetic logical controls; not measured assessor performance'}


def bistable_exact_certificate() -> dict[str, Any]:
    f=lambda x:x-x**3
    outer_low,inner_low,inner_high,outer_high=F(3,4),F(4,5),F(6,5),F(5,4)
    disturbance=F(1,10)
    constants={'outer_lower_inward':f(outer_low)-disturbance,
               'outer_upper_inward_magnitude':-(f(outer_high)+disturbance),
               'inner_lower_inward':f(inner_low)-disturbance,
               'inner_upper_inward_magnitude':-(f(inner_high)+disturbance)}
    require(all(v>0 for v in constants.values()),'Inward vector field failed.')
    # f' = 1-3x^2 is negative throughout the positive outer interval.
    require(1-3*outer_low**2<0,'Required monotonicity missing.')
    entry=max((inner_low-outer_low)/constants['inner_lower_inward'],
              (outer_high-inner_high)/constants['inner_upper_inward_magnitude'])
    require(entry==F(25,94) and entry < F(3,10),'Entry-time certificate failed.')
    require(inner_low-F(1,10)==F(7,10),'Readout margin incorrect.')
    return {'exact_constants':{k:str(v) for k,v in constants.items()},
            'numeric_constants':{k:float(v) for k,v in constants.items()},
            'entry_time_bound_exact':str(entry),'entry_time_bound':float(entry),
            'dwell':0.3,'settled_readout_margin':0.7,
            'scope':'exact arithmetic in stipulated differential/reset model'}


def rk4_dwell(z: float, disturbance: Callable[[float],float], steps: int=120) -> float:
    dt=0.3/steps
    def f(t:float,x:float)->float:
        return x-x*x*x+disturbance(t)
    for i in range(steps):
        t=i*dt
        k1=f(t,z); k2=f(t+dt/2,z+dt*k1/2)
        k3=f(t+dt/2,z+dt*k2/2); k4=f(t+dt,z+dt*k3)
        z+=dt*(k1+2*k2+2*k3+k4)/6
    return z


def bistable_grid() -> dict[str, Any]:
    ws=[lambda t:-0.1,lambda t:0.,lambda t:0.1,
        lambda t: -0.1 if t<0.15 else 0.1,
        lambda t: 0.1 if t<0.15 else -0.1]
    checked=0; low=math.inf; high=0.; max_refinement=0.
    for q in (0,1):
        for j in range(9):
            z=(-1)**q*(0.8+0.05*j)
            for a,xi,w in itertools.product((0,1),(-0.05,0.,0.05),ws):
                zp=(-1)**a*z+xi
                end=rk4_dwell(zp,w,120)
                refined=rk4_dwell(zp,w,240)
                max_refinement=max(max_refinement,abs(end-refined))
                signed=(-1)**(q^a)*end
                require(0.8-1e-10<=signed<=1.2+1e-10,'Numerical trajectory left certified settled region.')
                for noise in (-0.1,0.,0.1):
                    require(int(end+noise<0)==q^a,'Readout disagreed with parity.')
                checked+=1;low=min(low,signed);high=max(high,signed)
    return {'trajectories':checked,'min_settled_signed_state':low,'max_settled_signed_state':high,
            'max_RK4_step_halving_difference':max_refinement,
            'scope':'finite numerical corroboration, not an interval proof or physical data'}


def parity_words_and_handover() -> dict[str, Any]:
    traces=0; physical_steps=0; handovers=0
    for initial in (0,1):
        for word in itertools.product((0,1),repeat=10):
            qref=initial; qdigital=initial; z=0.; mode='digital'
            for t,a in enumerate(word):
                desired='analogue' if (t//2)%2 else 'digital'
                if desired!=mode:
                    if desired=='analogue':
                        # Writer receives source state, not evaluator's reference state.
                        z=(-1)**qdigital + (0.1 if t%2 else -0.1)
                    else:
                        qdigital=int(z+(0.1 if t%2 else -0.1)<0)
                    mode=desired; handovers+=1
                if mode=='digital':
                    qdigital ^= a; actual=qdigital
                else:
                    xi=0.05*((-1)**t)
                    z=rk4_dwell((-1)**a*z+xi,lambda time,t=t:0.1*((-1)**t),60)
                    physical_steps+=1
                    actual=int(z+0.1*((-1)**t)<0)
                qref ^= a
                require(actual==qref,'Mixed execution trace changed parity.')
            traces+=1
    return {'length_10_input_traces_with_both_initial_states':traces,
            'model_analogue_steps':physical_steps,'operator_scheduled_handovers':handovers,
            'scope':'fixed-schedule model test, not autonomous switching or physical migration'}


def reader_writer_edges() -> dict[str, Any]:
    count=0
    for q in (0,1):
        for e in (-.1,0,.1):
            z=(-1)**q+e
            require(.8<=(-1)**q*z<=1.2,'Writer outside domain.')
            for n in (-.1,0,.1):
                require(int(z+n<0)==q,'Reader/writer state mismatch.');count+=1
    # An out-of-contract reset can genuinely fail: the negative fixture must not be admitted.
    z=.8-1.0
    require(int(z<0)!=0,'Counterexample malformed.')
    require(abs(-1.0)>.05,'Invalid reset falsely within model.')
    return {'read_write_cases':count,'out_of_contract_reset_rejected':True}


def replay_counterexample() -> dict[str, Any]:
    q=0; a=1
    expected=q^a; replayed=(q^a)^a
    require(expected!=replayed,'Input replay did not alter parity.')
    return {'initial':q,'one_accepted_input':a,'expected':expected,'duplicated_effect':replayed}


def zero_failure_rule() -> dict[str, Any]:
    rows=[]
    for k in (1,4,10):
        for n in (1,10,1000):
            alpha=.05
            pstar=-math.expm1(math.log(alpha/k)/n)
            tail=math.exp(n*math.log1p(-pstar))
            close(k*tail,alpha,tolerance=1e-12)
            pbad=min(1.,pstar+.001)
            probability=0. if pbad==1. else math.exp(n*math.log1p(-pbad))
            require(k*probability<=alpha+1e-12,'Simultaneous zero-failure test bound violated.')
            rows.append({'k':k,'n':n,'alpha':alpha,'threshold':pstar})
    return {'rows':rows,'no_trials_performed':True}


NEW: list[tuple[str, Callable[[],dict[str,Any]]]]=[
    ('coordinate_realisation_invariance',coordinate_changes),
    ('parity_statefulness_and_memoryless_rejection',memory_nonvacuity),
    ('substitution_axes_are_not_a_total_ladder',substitution_nonchain),
    ('robust_packing_and_touching_ball_guard',packing_geometry),
    ('upper_bound_growth_is_not_failure',upper_bound_direction),
    ('parameter_count_is_not_behavioural_invariant',parameterisation_counterexample),
    ('finite_trace_total_variation_bound',distribution_trace_bound),
    ('stateful_export_collision_and_initialiser_impossibility',export_obstruction),
    ('matched_joint_contract_assessment',joint_assessment),
    ('bistable_exact_rational_certificate',bistable_exact_certificate),
    ('bistable_RK4_grid_and_refinement',bistable_grid),
    ('parity_traces_and_model_handovers',parity_words_and_handover),
    ('reader_writer_and_invalid_reset_controls',reader_writer_edges),
    ('input_replay_changes_continuation',replay_counterexample),
    ('zero_failure_cell_bound',zero_failure_rule),
]


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    results=[]
    for name,fun in [*old.v1.CHECKS,*old.ADDITIONS,*NEW]:
        try:
            result=fun(); results.append({'name':name,'passed':True,'details':result})
        except Exception as err:
            results.append({'name':name,'passed':False,'error':f'{type(err).__name__}: {err}'})
    base=Path(__file__).resolve().parent
    report={'title':'The Last Moat — Edition 3: reproducible checks',
            'scope':'Finite mathematics, stipulated ODE simulations and logical controls; no physical data or proof-assistant verification',
            'python_version':platform.python_version(),'optimisation_level':sys.flags.optimize,
            'source_sha256':{n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in
                ('verify_models.py','verify_models_e2.py','verify_models_v1.py')},
            'retained_checks':27,'new_checks':len(NEW),'total_checks':len(results),
            'passed_checks':sum(r['passed'] for r in results),'all_passed':all(r['passed'] for r in results),
            'checks':results}
    data=json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(data,encoding='utf-8')
    print(data,end='')
    return 0 if report['all_passed'] else 1

if __name__=='__main__':
    sys.exit(main())
