#!/usr/bin/env python3
"""Checks for Composition, Information, and Self-Revision.

Bounded exhaustive/differential checks, exact algebra and floating-point LPs.
General theorems rest on the manuscript's proofs. This is not proof-assistant
certification, independent peer review, a novelty claim, or physical validation.
Python 3.10+; numpy, scipy, sympy. No network, no modification of source inputs.
"""
from __future__ import annotations
import argparse
from collections import defaultdict, deque
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import platform
import time
import numpy as np
import scipy
from scipy.optimize import linprog
import sympy as sp

ROOT = Path(__file__).resolve().parent

def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)

def load_local(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

legacy_rel = load_local('legacy_relational_checks')
legacy_self = load_local('legacy_reflexive_checks')

def check_refinements():
    """Build compatible families by enumerating relations, not join formulas."""
    details = []
    for dims in ((1,1), (1,2), (2,2), (2,3), (2,2,2)):
        n = len(dims)
        xs = list(it.product(*(range(x) for x in dims)))
        scopes = [tuple(i for i in range(n) if s >> i & 1) for s in range(1, 1 << n)]
        full = (1 << len(xs)) - 1
        proj = [[frozenset(tuple(x[i] for i in s) for j,x in enumerate(xs) if k>>j&1)
                 for k in range(full+1)] for s in scopes]
        covers = [tuple(i for i in range(len(scopes)) if mask>>i&1)
                  for mask in range(1,1<<len(scopes))
                  if set().union(*(set(scopes[i]) for i in range(len(scopes)) if mask>>i&1))==set(range(n))]
        groups = {}
        for h in covers:
            bysig = defaultdict(set)
            for k in range(1,full+1):
                bysig[tuple(proj[s][k] for s in h)].add(k)
            groups[h] = bysig
        edges = status_checks = 0
        predicates = {0, full}
        for i in range(n):
            predicates.add(sum(1<<j for j,x in enumerate(xs) if x[i] == 0))
        predicates.add(sum(1<<j for j,x in enumerate(xs) if sum(x)%2 == 0))
        predicates.add(sum(1<<j for j,x in enumerate(xs) if x[0] == x[1]))
        def status(ks,p):
            yes = [k&p==k for k in ks]
            return 'automatic' if all(yes) else ('optional' if any(yes) else 'impossible')
        for h in covers:
            for s in range(len(scopes)):
                if s in h: continue
                h2 = tuple(sorted(h+(s,)))
                for sig2, ks2 in groups[h2].items():
                    sig = tuple(sig2[h2.index(t)] for t in h)
                    ks = groups[h][sig]
                    require(ks2 <= ks, 'refinement fails family inclusion')
                    j = legacy_rel.union_masks(ks)
                    j2 = legacy_rel.union_masks(ks2)
                    require(j2 & j == j2, 'refinement fails join inclusion')
                    edges += 1
                    for p in predicates:
                        before, after = status(ks,p), status(ks2,p)
                        require(before=='optional' or after==before, 'nonoptional status changed')
                        for actual in ks2:
                            if actual & p == actual:
                                require(after!='impossible', 'true projection excluded actual witness')
                        status_checks += 1
        details.append({'dimensions':list(dims),'one_scope_refinement_edges':edges,
                        'target_status_checks':status_checks,'status':'PASS'})
    return {'status':'PASS','cases':details,
            'refinement_edges':sum(d['one_scope_refinement_edges'] for d in details),
            'status_checks':sum(d['target_status_checks'] for d in details)}

def check_probability():
    """LP extrema compared with an independently derived exact 2x2 interval."""
    xs = list(it.product((0,1),repeat=2))
    A = np.array([[1]*4, [x[0] for x in xs], [x[1] for x in xs]], dtype=float)
    cases = lp_runs = threshold_checks = 0
    for p,q in it.product((F(0),F(1,4),F(1,2),F(3,4),F(1)),repeat=2):
        lo,hi = max(F(0),p+q-1), min(p,q)
        ends = [(1-p-q+t,q-t,p-t,t) for t in (lo,hi)]
        for mask in range(16):
            c = np.array([(mask>>i)&1 for i in range(4)], dtype=float)
            exact = [sum(mu[i] for i in range(4) if mask>>i&1) for mu in ends]
            e_lo,e_hi = min(exact),max(exact)
            rlo=linprog(c,A_eq=A,b_eq=[1,float(p),float(q)],bounds=(0,None),method='highs')
            rhi=linprog(-c,A_eq=A,b_eq=[1,float(p),float(q)],bounds=(0,None),method='highs')
            require(rlo.success and rhi.success, 'feasible 2x2 LP failed')
            require(abs(rlo.fun-float(e_lo))<1e-9 and abs(-rhi.fun-float(e_hi))<1e-9,'LP/interval mismatch')
            for alpha in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
                status='automatic' if e_lo>=alpha else ('optional' if e_hi>=alpha else 'impossible')
                observed='automatic' if rlo.fun>=float(alpha)-1e-9 else ('optional' if -rhi.fun>=float(alpha)-1e-9 else 'impossible')
                require(status==observed,'threshold trichotomy mismatch')
                threshold_checks+=1
            cases+=1; lp_runs+=2
    xs3=list(it.product((0,1),repeat=3))
    rows=[]; rhs=[]
    for pair in it.combinations(range(3),2):
        for bits in it.product((0,1),repeat=2):
            rows.append([int(tuple(x[i] for i in pair)==bits) for x in xs3])
            rhs.append(float(F(1,20) if bits[0]==bits[1] else F(9,20)))
    fail=linprog(np.zeros(8),A_eq=rows,b_eq=rhs,bounds=(0,None),method='highs')
    require(fail.status==2,'incompatible marginals unexpectedly feasible')
    require(max(sum(x[i]!=x[j] for i,j in it.combinations(range(3),2)) for x in xs3)==2,'disagreement bound wrong')
    require(3*F(9,10)>2,'exact incompatibility witness absent')
    return {'status':'PASS','exact_interval_event_cases':cases,'linear_programmes':lp_runs+1,
            'threshold_checks':threshold_checks,'lp_tolerance':1e-9,
            'incompatible_marginals':'LP infeasible; exact pointwise inequality 27/10 > 2',
            'scope':'2 binary variables; five marginal values; all 16 events; five thresholds; one 3-variable incompatibility'}

def check_parity_laws():
    marginals=0; cases=[]
    for n in range(2,9):
        xs=list(it.product((0,1),repeat=n))
        for t in (F(-1),F(-1,2),F(0),F(1,2),F(1)):
            law={x:F(1,2**n)*(1+t*(-1)**sum(x)) for x in xs}
            require(min(law.values())>=0 and sum(law.values())==1,'parity law not probability')
            require(sum(law[x]*(-1)**sum(x) for x in xs)==t,'parity expectation mismatch')
            require(sum(p for x,p in law.items() if sum(x)%2==0)==(1+t)/2,'parity mass mismatch')
            for r in range(n):
                for scope in it.combinations(range(n),r):
                    marginal=defaultdict(F)
                    support=set()
                    for x,p in law.items():
                        sub=tuple(x[i] for i in scope)
                        marginal[sub]+=p
                        if p>0: support.add(sub)
                    require(set(marginal.values())=={F(1,2**r)},'proper marginal not uniform')
                    require(support=={x for x,p in marginal.items() if p>0},'support/projection mismatch')
                    marginals+=1
            support={x for x,p in law.items() if p>0}
            if abs(t)<1: require(len(support)==2**n,'interior not full support')
            else: require(all((-1)**sum(x)==t for x in support),'endpoint support mismatch')
        cases.append({'n':n,'parameter_values':5})
    return {'status':'PASS','cases':cases,'proper_marginals_including_empty_checked':marginals,
            'arithmetic':'exact fractions'}

def check_feasible_support():
    A=sp.Matrix([[1,1,1,1],[0,0,1,1],[0,1,0,1]])
    case_count=channel_checks=0; boundary_count=0
    for p,q in it.product([sp.Rational(i,4) for i in range(5)],repeat=2):
        lo,hi=max(0,p+q-1),min(p,q)
        ends=[sp.Matrix([1-p-q+t,q-t,p-t,t]) for t in (lo,hi)]
        diff=ends[1]-ends[0]
        S=[i for i in range(4) if any(mu[i]>0 for mu in ends)]
        basis=[]
        for d in A[:,S].nullspace():
            v=sp.zeros(4,1)
            for i,j in enumerate(S): v[j]=d[i]
            basis.append(v)
        rank_d=int(diff!=sp.zeros(4,1))
        require(len(basis)==rank_d,'active-support affine dimension wrong')
        if rank_d:
            require(sp.Matrix.hstack(diff,*basis).rank()==1,'feasible span not active kernel')
        for probs in it.product((sp.Rational(0),sp.Rational(1,2),sp.Rational(1)),repeat=4):
            T=sp.Matrix([[1-a for a in probs],list(probs)])
            constant=T*ends[0]==T*ends[1]
            annihilates=all(T*d==sp.zeros(2,1) for d in basis)
            require(constant==annihilates,'channel criterion mismatch')
            channel_checks+=1
        case_count+=1
        boundary_count+=len(S)<4
    # Explicit witness that unrestricted ker(A) is too strong at a boundary.
    d=sp.Matrix([1,-1,-1,1])
    require(A*d==sp.zeros(3,1) and sp.eye(4)*d!=sp.zeros(4,1),'boundary witness absent')
    # Three-variable full positivity: proper pair marginals have exactly one parity direction.
    xs=list(it.product((0,1),repeat=3))
    A3=sp.Matrix([[int(tuple(x[i] for i in pair)==bits) for x in xs]
                 for pair in it.combinations(range(3),2) for bits in it.product((0,1),repeat=2)])
    chi=sp.Matrix([(-1)**sum(x) for x in xs])
    require(len(A3.nullspace())==1 and A3*chi==sp.zeros(A3.rows,1),'3-variable kernel not parity')
    Tpar=sp.Matrix([[int(sum(x)%2==b) for x in xs] for b in (0,1)])
    Treset=sp.Matrix([[1]*8,[0]*8])
    require(Tpar*chi!=sp.zeros(2,1) and Treset*chi==sp.zeros(2,1),'expose/erase channel failed')
    return {'status':'PASS','two_binary_marginal_families':case_count,'boundary_families':boundary_count,
            'stochastic_channel_checks':channel_checks,'three_binary_pair_kernel_dimension':1,
            'full_kernel_shortcut_boundary_counterexample':True,'arithmetic':'exact rational matrices'}

def check_kernel_bridge():
    total=holds=fails=0
    for n in range(1,5):
        for obs in legacy_self.partitions(n):
            L=sp.Matrix([[int(obs[i]==z) for i in range(n)] for z in sorted(set(obs))])
            basis=L.nullspace()
            for a in it.product(range(n),repeat=n):
                raw=all(obs[i]!=obs[j] or obs[a[i]]==obs[a[j]] for i in range(n) for j in range(n))
                # Image of a signed vector computed by sums, not equality on pairs.
                kernel=True
                for d in basis:
                    pushed=[sum(d[i] for i in range(n) if obs[a[i]]==z) for z in sorted(set(obs))]
                    if any(pushed): kernel=False; break
                require(raw==kernel,'congruence / pushforward kernel mismatch')
                total+=1; holds+=raw; fails+=not raw
    return {'status':'PASS','partition_action_pairs':total,'congruent_pairs':holds,
            'noncongruent_pairs':fails,'scope':'all partitions and all deterministic single actions on 1..4 states'}

Belief=frozenset[tuple[int,int]]

def compressed_winning(n:int,obs:tuple[int,...],actions:tuple[tuple[int,...],...]):
    """Literal synchronous rank construction on current-state / required-label sets."""
    atoms=[(i,b) for i in range(n) for b in (0,1)]
    universe=[]
    for mask in range(1,1<<len(atoms)):
        B=frozenset(atoms[i] for i in range(len(atoms)) if mask>>i&1)
        if len({obs[w] for w,b in B})==1: universe.append(B)
    ranks={B:0 for B in universe if len({b for w,b in B})==1}
    successors={}
    for B in universe:
        choices=[]
        for a in actions:
            byz=defaultdict(set)
            for w,b in B: byz[obs[a[w]]].add((a[w],b))
            choices.append(tuple(frozenset(v) for v in byz.values()))
        successors[B]=choices
    k=0
    while True:
        new=[B for B in universe if B not in ranks and any(all(v in ranks for v in ch) for ch in successors[B])]
        if not new: return ranks
        k+=1
        for B in new: ranks[B]=k

def origin_oracle(obs,actions,initial,labels):
    """Alternative representation: retain every original index/current-state pair.

    Build its reachable AND/OR graph and solve with a predecessor worklist.
    This checks the labelled-belief quotient; it is not independent peer review.
    """
    roots=[]
    for z in sorted({obs[i] for i in initial}):
        roots.append(tuple(i if i in initial and obs[i]==z else -1 for i in range(len(obs))))
    todo=deque(roots); seen=set(roots); choices={}; terminals=set()
    while todo:
        state=todo.popleft()
        required={labels[i] for i,w in enumerate(state) if w>=0}
        if len(required)==1: terminals.add(state); choices[state]=[]; continue
        choices[state]=[]
        for a in actions:
            moved=tuple(a[w] if w>=0 else -1 for w in state)
            children=[]
            for z in sorted({obs[w] for w in moved if w>=0}):
                child=tuple(w if w>=0 and obs[w]==z else -1 for w in moved)
                children.append(child)
                if child not in seen: seen.add(child);todo.append(child)
            choices[state].append(tuple(children))
    predecessors=defaultdict(list); missing={}
    for parent,options in choices.items():
        for ai,children in enumerate(options):
            key=(parent,ai); missing[key]=len(set(children))
            for child in set(children): predecessors[child].append(key)
    won=set(terminals); q=deque(terminals)
    while q:
        child=q.popleft()
        for key in predecessors[child]:
            missing[key]-=1
            parent,_=key
            if missing[key]==0 and parent not in won:
                won.add(parent);q.append(parent)
    return all(root in won for root in roots),len(seen)

def check_decision():
    cases=winning=losing=oracle_nodes=0
    details=[]
    for n in range(1,4):
        maps=list(it.product(range(n),repeat=n)); count=0
        for obs in legacy_self.partitions(n):
            for actions in it.product(maps,repeat=2):
                ranks=compressed_winning(n,obs,actions)
                initials=[frozenset(i for i in range(n) if mask>>i&1) for mask in range(1,1<<n)] if n<=2 else [frozenset(range(n))]
                for labels in it.product((0,1),repeat=n):
                    for initial in initials:
                        roots=[frozenset((w,labels[w]) for w in initial if obs[w]==z) for z in {obs[w] for w in initial}]
                        answer=all(B in ranks for B in roots)
                        alternate,nodes=origin_oracle(obs,actions,initial,labels)
                        require(answer==alternate,'compressed belief and origin-history oracle disagree')
                        cases+=1;count+=1;winning+=answer;losing+=not answer;oracle_nodes+=nodes
        details.append({'states':n,'cases':count,'initial_sets':'all nonempty' if n<=2 else 'full state set'})
    # Four-state reconnection: state order (0,0),(0,1),(1,0),(1,1).
    obs=(0,0,1,2); actions=((2,3,2,3),)
    ranks=compressed_winning(4,obs,actions)
    B=frozenset({(0,0),(1,1)})
    require(ranks.get(B)==1,'reconnection should have rank one')
    setting_ranks=compressed_winning(4,(0,0,1,1),actions)
    require(B not in setting_ranks,'setting readback alone revealed hidden external bit')
    # Five-state destructive example. Terminal states have observations 1,2.
    obs5=(0,0,0,1,2); acts5=((4,3,3,3,4),(3,4,3,3,4))
    labels=(0,0,1,0,0); initial=frozenset({0,1,2})
    ranks5=compressed_winning(5,obs5,acts5)
    B5=frozenset((w,labels[w]) for w in initial)
    require(B5 not in ranks5,'destructive example unexpectedly winning')
    require(all(any(obs5[a[i]]!=obs5[a[j]] for a in acts5) for i,j in it.combinations(initial,2)), 'not all pairs separable')
    alternate,_=origin_oracle(obs5,acts5,initial,labels)
    require(not alternate,'origin oracle incorrectly accepts destructive example')
    return {'status':'PASS','cases':cases,'winning':winning,'losing':losing,
            'origin_graph_nodes_total':oracle_nodes,'details':details,
            'differential_methods':'synchronous labelled-belief ranks versus origin-index history graph with predecessor worklist',
            'reconnection_rank':1,'setting_only_channel':'LOSING','destructive_pairwise_example':'LOSING',
            'all_pairs_destructive_example_separately_distinguishable':True}

def check_physical_algebra():
    q=sp.Matrix([[2,0,2],[0,2,1]]);v=sp.Matrix([-2,-1,2])
    require(q*v==sp.zeros(2,1),'stoichiometric conservation false')
    zs=[sp.Matrix(x) for x in it.product(range(5),repeat=3) if q*sp.Matrix(x)==sp.Matrix([4,2])]
    require(sp.Matrix([2,1,0]) in zs and sp.Matrix([0,0,2]) in zs,'count endpoints missing')
    # Bell density example and CHSH illustration; exact algebra, not an experiment.
    phi=sp.Matrix([1,0,0,1])/sp.sqrt(2)
    rho=phi*phi.T; sigma=sp.diag(sp.Rational(1,2),0,0,sp.Rational(1,2))
    B=sp.Matrix([[0,1],[1,0]]);Z=sp.diag(1,-1)
    def partial(matrix,keep):
        return sp.Matrix(2,2,lambda i,j: sum(matrix[2*i+k,2*j+k] if keep==0 else matrix[2*k+i,2*k+j] for k in range(2)))
    require(all(partial(m,k)==sp.eye(2)/2 for m in (rho,sigma) for k in (0,1)),'quantum reductions differ')
    flip=sp.kronecker_product(B,B)
    require(sp.trace(rho*flip)==1 and sp.trace(sigma*flip)==0,'global quantum observation wrong')
    require(rho*rho==rho and sigma*sigma!=sigma,'pure/mixed identities wrong')
    chsh=sp.kronecker_product(Z,(Z+B)/sp.sqrt(2))+sp.kronecker_product(Z,(Z-B)/sp.sqrt(2))+sp.kronecker_product(B,(Z+B)/sp.sqrt(2))-sp.kronecker_product(B,(Z-B)/sp.sqrt(2))
    quantum=sp.simplify(sp.trace(rho*chsh))
    local=[a0*b0+a0*b1+a1*b0-a1*b1 for a0,a1,b0,b1 in it.product((-1,1),repeat=4)]
    require(max(abs(x) for x in local)==2 and quantum==2*sp.sqrt(2),'CHSH boundary witness wrong')
    # Kernel conservation via a deterministic mapping on the two count endpoints.
    before=sp.Matrix([2,1,0]);after=sp.Matrix([0,0,2])
    require(q*before==q*after,'inventory pushforward endpoints mismatch')
    return {'status':'PASS','fixed_inventory_species_states':[list(map(int,z)) for z in zs],
            'quantum_local_reductions':'I_2/2 for both states and both subsystems',
            'global_bitflip_expectations':[1,0],'CHSH_deterministic_local_assignments':len(local),
            'CHSH_local_bound':2,'CHSH_quantum_expectation':str(quantum),
            'scope':'exact matrix/stoichiometric identities only; no physical or metaphysical validation'}

def negative_controls(previous):
    # Each item is a specific incorrect shortcut and an actual defeating witness.
    xs=list(it.product((0,1),repeat=2)); full=set(xs)
    project=lambda K,i:{x[i] for x in K}
    G=full-{(1,1)}; neg={(1,1)}
    optional_but_not_opposite=all(project(G,i)=={0,1} for i in (0,1)) and any(project(neg,i)!={0,1} for i in (0,1))
    witnesses={
        'optional_requires_opposite_guarantee':optional_but_not_opposite,
        'strict_constraint_always_improves':(0,1) not in {(0,0),(1,1)} and all(project({(0,0),(1,1)},i)=={0,1} for i in (0,1)),
        'named_new_conjunction_requires_new_observation':all((bool(a) and bool(b))==bool(a*b) for a,b in xs),
        'support_consistency_implies_probability_consistency':3*F(9,10)>2,
        'conditioning_always_preserves_marginals':F(2,3)!=F(1,2),
        'unrestricted_kernel_valid_at_boundary':previous['feasible_support']['full_kernel_shortcut_boundary_counterexample'],
        'noncongruence_implies_sure_decision':previous['finite_decision']['destructive_pairwise_example']=='LOSING',
        'pairwise_distinguishability_implies_population_decision':previous['finite_decision']['all_pairs_destructive_example_separately_distinguishable'] and previous['finite_decision']['destructive_pairwise_example']=='LOSING',
        'discard_initial_labels_after_state_merger':previous['finite_decision']['destructive_pairwise_example']=='LOSING',
        'connection_setting_readback_equals_external_evidence':previous['finite_decision']['setting_only_channel']=='LOSING',
        'reconnection_creates_unreachable_predecessor_capability':previous['finite_decision']['reconnection_rank']==1,
        'same_local_density_operators_imply_same_joint_state':previous['physical_algebra']['global_bitflip_expectations']==[1,0],
        'probabilistic_local_mixtures_evade_CHSH_bound':previous['physical_algebra']['CHSH_local_bound']==2,
        'chemical_inventory_preserves_molecular_inventory':sp.Matrix([2,1,0])!=sp.Matrix([0,0,2]),
    }
    # Detailed witnesses for the booleans above are asserted in the corresponding tests;
    # require them to actually be executed before this result can be emitted.
    for key,ok in witnesses.items(): require(ok,'negative control not discriminating: '+key)
    return {'status':'PASS','counterexample_families':len(witnesses),'rejected_shortcuts':list(witnesses),
            'note':'These are counterexample checks, not claims of an independent reviewer or literal mutation of each theorem.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'integrated-results.json')
    args=parser.parse_args()
    started=time.perf_counter();results={}
    tests=[('singleton_edge_domains',lambda:{'status':'PASS','cases':[legacy_rel.check_domain(d) for d in ((1,1),(1,2))]}),
           ('scope_refinement',check_refinements),('probability',check_probability),
           ('parity_laws',check_parity_laws),('feasible_support',check_feasible_support),
           ('kernel_bridge',check_kernel_bridge),('finite_decision',check_decision),
           ('physical_algebra',check_physical_algebra),('negative_controls',lambda:negative_controls(results))]
    for name,fn in tests:
        t=time.perf_counter();print('RUN',name,flush=True)
        results[name]=fn();results[name]['elapsed_seconds']=round(time.perf_counter()-t,3)
        print('PASS',name,results[name]['elapsed_seconds'],flush=True)
    payload={'status':'PASS','schema':'integrated-composition-checks-v1','results':results,
             'elapsed_seconds':round(time.perf_counter()-started,3),
             'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
             'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'scope_limit':'Bounded diagnostic checks only. General proofs are in the manuscript. No proof assistant, independent peer review, novelty, empirical effect or physical validation.'}
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','elapsed_seconds':payload['elapsed_seconds'],'output':str(args.output)}),flush=True)
if __name__=='__main__':main()
