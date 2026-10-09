#!/usr/bin/env python3
"""Check final source identity and replay the synthetic observation arithmetic."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
AUTHOR=ROOT/'stable-grouped-invariants'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bindings=json.loads((HERE/'FINAL_BINDINGS.json').read_text())
for x in bindings['author_payloads']:
    assert digest(AUTHOR/x['path'])==x['sha256'],x['path']
for x in bindings['inherited_payloads_verified']+bindings['individual_inputs_verified']:
    assert digest(ROOT/x['path'])==x['sha256'],x['path']
for name in ['exact_controls.json','GRID_WITNESS.json']:
    assert (AUTHOR/'results'/name).read_bytes()==(HERE/'author_replay/results'/name).read_bytes()
assert (AUTHOR/'exact_controls.py').read_bytes()==(HERE/'author_replay/exact_controls.py').read_bytes()
assert json.loads((HERE/'author_replay/results/exact_controls.json').read_text())['families_passed']==13

w=json.loads((AUTHOR/'results/GRID_WITNESS.json').read_text())
N=w['synthetic_group_total']; histogram=w['synthetic_count_frequencies']
assert all(isinstance(z,int) and z>=0 for z in histogram) and sum(histogram)==N
obs=[F(sum(count*comb(s,r) for s,count in enumerate(histogram) if s>=r),N*comb(4,r)) for r in range(1,5)]
assert obs==list(map(F,w['empirical_moments']))==list(map(F,w['true_moments'][1:]))
assert obs==[F(2,7)*F(7,10)**r+F(5,7)*F(7,10)**(3*r) for r in range(1,5)]
Q=w['Q']; p=[F(k,Q) for k in w['weight_numerators']]
t=F(1,2)+F(w['grid_t_index'],3*Q)
assert sum(p)==1 and min(p)>=F(1,8)
assert F(1,2)<=t<=F(5,6) and t==F(w['grid_t'])
assert p!=[F(2,7),F(5,7)] and t!=F(7,10)
mm=[sum(weight*t**(r*j) for weight,j in zip(p,w['support'])) for r in range(1,5)]
res=max(abs(a-b) for a,b in zip(obs,mm))
assert res==F(w['max_moment_error'])<=F(w['tau'])<2*F(w['tau'])
assert N>=w['sufficient_budget']
assert 2*N*F(w['tau'])**2>=w['log_upper_integer']
assert 2**w['log_upper_integer']>=F(4*w['C'],1)/F(w['delta'])
print(json.dumps({'status':'PASS','author_payloads_bound':len(bindings['author_payloads']),
                  'inherited_payloads_verified':len(bindings['inherited_payloads_verified']),
                  'individual_inputs_verified':len(bindings['individual_inputs_verified']),
                  'author_replay_families':13,'synthetic_histogram_total':N,
                  'histogram_derived_factorial_moments':list(map(str,obs)),
                  'synthetic_grid_witness':'PASS','empirical_samples_collected':False,
                  'full_candidate_grid_searched':False},indent=2))
