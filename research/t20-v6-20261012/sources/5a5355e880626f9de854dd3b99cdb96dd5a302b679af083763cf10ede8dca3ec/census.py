#!/usr/bin/env python3
"""Bounded P02 model census, distinct from preserved historical populations."""
from fractions import Fraction as F
from itertools import product,combinations
from collections import Counter
import hashlib,json,pathlib,sys
import p02_research as r
out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
def require(ok,message):
    if not ok:raise RuntimeError(message)
rows=out/'mealy_3state.jsonl';counts=Counter();checks=Counter()
with rows.open('w') as sink:
    for serial,codes in enumerate(product(range(6),repeat=6)):
        edges=tuple((code//2,code%2) for code in codes)
        m=tuple((edges[2*s],edges[2*s+1]) for s in range(3))
        d=r.deterministic_states(m);d2=r.deterministic_states_independent(m)
        require(d==d2,f'Determinism disagreement {serial}');checks['independent_D_comparisons']+=1
        mass=r.atomic_mass(m)
        for s in range(3):
            require(0<=mass[s]<=1,f'Probability bounds {serial}:{s}')
            require(mass[s]==sum((mass[t] for t,_ in m[s]),F(0))/2,f'Bellman {serial}:{s}')
            if s in d:require(mass[s]==1,f'Boundary {serial}:{s}')
            checks['state_probability_and_Bellman_checks']+=1
        counts[str(mass[0])]+=1
        sink.write(json.dumps({'id':serial,'encoding':codes,'D':sorted(d),'atomic_mass':[str(x) for x in mass]},separators=(',',':'))+'\n')
checks['machines']=serial+1
parity=[]
for n in range(3,9):
    e,o=r.parity_law(n,0),r.parity_law(n,1);checks['parity_dimensions']+=1
    for mask in range((1<<n)-1):
        j=tuple(i for i in range(n) if (mask>>i)&1)
        ep,op=r.marginal(e,j),r.marginal(o,j)
        require(ep==op,f'Proper marginal mismatch {n}:{mask}')
        require(all(p==F(1,2**len(j)) for p in ep.values()),'Not uniform')
        checks['proper_subset_marginal_equalities']+=1;checks['projected_cell_weight_checks']+=len(ep)
    mix=r.mixture(e,{(0,)*n:F(1)},F(1,2))
    require(sum(p for x,p in mix.items() if sum(x)%2==0)==1,'Parity mixture not retained')
    for j in combinations(range(n),2):
        require(r.marginal(mix,j)=={(0,0):F(5,8),(0,1):F(1,8),(1,0):F(1,8),(1,1):F(1,8)},'Pairwise mixture mismatch')
        checks['mixture_pair_profiles']+=1
    flipped={tuple([1-x[0],*x[1:]]):p for x,p in o.items()}
    require(flipped==e,'Declared intervention does not restore even parity')
    parity.append({'n':n,'proper_subsets':2**n-1,'support_per_parity':len(e),'pairwise_mixture':['5/8','1/8','1/8','1/8']})
# Witness-based negative controls, not modifications to accepted source.
m=(((1,0),(2,0)),((1,0),(1,0)),((2,1),(2,1)))
mutants={
 'D_FROM_IMMEDIATE_OUTPUT_ONLY':{s for s,row in enumerate(m) if row[0][1]==row[1][1]}!=r.deterministic_states(m),
 'ATOMIC_MASS_EQUALS_INDICATOR_D':r.atomic_mass(m)[0]!=F(int(0 in r.deterministic_states(m))),
 'ZERO_RESIDUAL_IN_INFINITE_BUDGET':F(1,3)<=F(1,2)<F(1,3)+F(5,12),
 'BLIND_FULL_PARITY_MARGINAL':r.marginal(r.parity_law(3,0),(0,1,2))!=r.marginal(r.parity_law(3,1),(0,1,2)),
 'PROFILE_MOVEMENT_IMPLIES_RESTORATION':r.marginal(r.parity_law(3,0),(0,1))!=r.marginal(r.mixture(r.parity_law(3,0),{(0,0,0):F(1)},F(1,2)),(0,1)),
 'DROP_STRICT_POSITIVE_GAP':all(F(1,2)+F(1,2**n)>F(1,2) for n in range(1,41)),
}
require(all(mutants.values()),'Negative control survived')
# Last control checks 40 exact samples of a sequence whose infimum equality is proved in notes.
report={'status':'PASS_FINITE_POPULATION_ONLY','checks':dict(checks),'start_state_atomic_mass_histogram':dict(sorted(counts.items())), 'negative_controls':mutants,'negative_control_scope':'Five concrete finite/certificate counterexamples; sixth is a finite illustration of an independently proved limit counterexample, not a kernel mutation test.', 'parity':parity,'raw_rows':{'file':rows.name,'bytes':rows.stat().st_size,'sha256':hashlib.sha256(rows.read_bytes()).hexdigest()},'kernel_verified':False,'historical_population_replayed':False}
(out/'CENSUS_RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
