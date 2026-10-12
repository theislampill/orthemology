"""Independent exact countermodels and controls; no source mutation or build replay."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True
import json

OUT={}
# Independently quantified Mealy output refinement, not the source phi routine.
def iter_rel(machine):
    n=len(machine); R=set(product(range(n),repeat=2)); layers=[R]
    while True:
        Q={(x,y) for x,y in R if all(machine[x][a][0]==machine[y][b][0]
             and (machine[x][a][1],machine[y][b][1]) in R
             for a,b in product(range(2),repeat=2))}
        if Q==R: return layers
        assert Q<R
        layers.append(Q); R=Q

kb2=[[(0,0),(0,1)],[(1,0),(1,0)]]
kb3=[[(0,0),(0,1)],[(0,2),(0,2)],[(1,0),(1,0)]]
OUT['kopf_literal']={str(len(m)):{'strict_rounds':len(iter_rel(m))-1,
    'relations':[[list(p) for p in sorted(R)] for R in iter_rel(m)]} for m in [kb2,kb3]}
assert len(iter_rel(kb2))-1==3 and len(iter_rel(kb3))-1==5

# Full information revealed after prediction vs hidden pre-sampled random seed.
# At each unsuccessful round, a hidden/fresh fair controller bit determines
# its later response; the adversary predicts before that response. Differing
# response reaches absorbing good G. Memory-revealing adversary copies bit.
OUT['private_future_coin']={'blind_survival_by_round':[], 'revealed_survival_by_round':[]}
for n in range(13):
    OUT['private_future_coin']['blind_survival_by_round'].append(str(F(1,2)**n))
    OUT['private_future_coin']['revealed_survival_by_round'].append('1')
assert OUT['private_future_coin']['blind_survival_by_round'][-1]=='1/4096'

# Weighted Brier quantifiers, evaluated independently.
b=(F(7,10),F(3,5)); truths=[(F(1),F(0)),(F(0),F(1))]
def loss(v,w,t):return w*(v[0]-t[0])**2+(1-w)*(v[1]-t[1])**2
alphas=[F(1,4),F(3,4)]
mins=[min(loss(b,w,t) for w in alphas) for t in truths]
assert mins==[F(63,400),F(97,400)]
assert mins[0]<F(4,25) and mins[1]<F(1,4)
c=(F(11,20),F(9,20)); narrow=[F(9,20),F(11,20)]
gains=[loss(b,w,t)-loss(c,w,t) for w in narrow for t in truths]
assert min(gains)==F(3,500)
OUT['weighted_brier']={'wide_min_losses':list(map(str,mins)), 'narrow_endpoint_gains':list(map(str,gains))}

# A finite-memory stop-and-commit strategy succeeds with positive probability
# despite failure of AS under the other standard. This protects against
# turning HS1 into universal zero-restoration-probability impossibility.
p=F(2,3); error=sum(F(__import__('math').comb(4,k))*p**k*(1-p)**(4-k) for k in range(3))
OUT['finite_memory_commit']={'samples':4,'under_Hplus_error_with_tie_to_minus':str(error), 'restoration_probability':str(1-error)}
assert 0<1-error<1

# Distinguish summable departure from summable occupancy; no stationary trick.
for n in range(1,20):
    z=F(1)
    for k in range(2,n+2):z*=1-F(1,k*k)
    assert z==F(n+2,2*(n+1))
OUT['absorbing_departure']={'survival_limit':'1/2','departure_count_pathwise_max':1,'failure_paths_bad_visits':'infinite'}

# Verify the strongest exposed polytope interface with independently chosen
# lower-dimensional/constant atoms; no producer success is accepted unchecked.
spec=importlib.util.spec_from_file_location('poly',str(Path(__file__).with_name('reference')/'polytope_disclosure.py'))
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
poly={'min_weight':'1/10','extra_le':[], 'extra_eq':[{'coefficients':[1,-1,0],'bound':0}]}
atoms=[{'coefficients':[1,-1,0],'offset':0},{'coefficients':[0,0,0],'offset':'1/1000000000000000000'}]
target={'op':'and','args':[{'op':'ge','atom':0},{'op':'not','arg':{'op':'gt','atom':0}},{'op':'gt','atom':1}]}
cert=mod.audit(poly,atoms,target)
assert cert['status']=='INVARIANT_TRUE' and mod.verify(poly,atoms,target,cert)['accepted']
original_v,original_c=mod._vertices,mod._cone_certificate
mod._vertices=mod._cone_certificate=lambda *a: (_ for _ in ()).throw(AssertionError('search called by verifier'))
assert mod.verify(poly,atoms,target,cert)['accepted']
mod._vertices,mod._cone_certificate=original_v,original_c
OUT['polytope_independent_cases']={'lower_dimensional_tie_tiny_margin':cert['status'],'cells':len(cert['cells']),'verifier_without_search':'accepted'}

Path(__file__).with_name('independent_controls_results.json').write_text(json.dumps(OUT,indent=2)+'\n')
print(json.dumps(OUT,indent=2))

# Stronger literature deletion: genuinely nondeterministic, still input-enabled.
# States 0 and 3 are behaviorally identical clones of state 0 in kb3. A few
# transitions nondeterministically choose either clone, retaining 5 rounds on
# 4 actual states. Thus excluding deterministic instances would not rescue m.
nondet=[ [{(0,0),(0,3)},{(0,1)}],
         [{(0,2)},{(0,2)}],
         [{(1,0),(1,3)},{(1,0),(1,3)}],
         [{(0,0),(0,3)},{(0,1)}] ]
def literal_partition_next(M,R):
    n=len(M);D={i for i in range(n) if (i,i) in R}; excluded=set(range(n))-D
    blocks={frozenset(j for j in D if (i,j) in R) for i in D}
    def succ(i,a,o):return {j for emit,j in M[i][a] if emit==o}
    ans=set()
    for i,j in R:
        keep=True
        for a,b,o in product(range(2),repeat=3):
            left,right=succ(i,a,o),succ(j,b,o)
            if left & excluded or right & excluded:keep=False
            if any(bool(left & C)!=bool(right & C) for C in blocks):keep=False
        if keep:ans.add((i,j))
    return ans
R=set(product(range(4),repeat=2)); layers=[R]
while True:
    Q=literal_partition_next(nondet,R)
    if Q==R:break
    assert Q<R;layers.append(Q);R=Q
assert len(layers)-1==5
OUT['kopf_genuinely_nondeterministic']={'states':4,'strict_rounds':5,
 'positive_nondeterminism':any(len(a)>1 for row in nondet for a in row),
 'relations':[[list(p) for p in sorted(R)] for R in layers]}
Path(__file__).with_name('independent_controls_results.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('Genuinely nondeterministic control: 4 states, 5 strict rounds')
