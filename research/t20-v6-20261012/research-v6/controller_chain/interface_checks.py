#!/usr/bin/env python3
"""Exact finite controls for v6 cross-front interfaces; not a Lean replay."""
from fractions import Fraction as F
from math import lcm
import json, hashlib, pathlib
out={}
# Private seed is recovered from its publicly recorded first action, even if
# physical state and surviving model support agree across both histories.
rho={0:F(1,2),1:F(1,2)}
posterior={a:{r:(rho[r]/rho[a] if r==a else F(0)) for r in rho} for a in rho}
assert posterior[0][0]==1 and posterior[1][1]==1
out['posterior_collision']={'compressed_state':['same_state','same_live_support'],
 'conditional_next_action_distributions':[{str(r):str(p) for r,p in posterior[a].items()} for a in rho],
 'total_variation':'1','meaning':'No state+support-only restart can preserve both given-policy conditional laws.'}
# Old menu residues do not suffice after a menu-size change. A universal LCM
# residue does preserve the cyclic action for every menu size at most a.
assert 0%2==2%2 and 0%3!=2%3
nchecks=0;lcms={}
for a in range(1,9):
 L=lcm(*range(1,a+1)); lcms[a]=L
 for n in range(3*L+1):
  for k in range(1,a+1):
   assert n%k==(n%L)%k;nchecks+=1
out['universal_rotor_residue']={'checks':nchecks,'max_menu':8,'lcm':lcms,
 'old_menu_collision':{'counts':[0,2],'old_size':2,'new_size':3},
 'general_proof':'Every k<=a divides L=lcm(1,...,a); equality mod L implies equality mod k. Store a residue per source and increment only at its departures.',
 'limit':'Preserves scheduler decisions under fixed ordering, not phase index or empirical statistics.'}
# Same current observation and rotor parity can hide different empirical gates.
def gate(n,success,phase=1,p=F(1,2),eps=F(1,4)):
 freq=F(success,n) if n else F(0)
 return phase<n and abs(freq-p)>=eps
assert 1%2==3%2 and not gate(1,0) and gate(3,0)
out['empirical_gate_collision']={'counts':[1,3],'successes':[0,0],'phase':1,
 'same_rotor_modulus':2,'test':[gate(1,0),gate(3,0)],
 'qualification':'An interface-level row-test collision; does not claim two entire generated controller states coincide.'}
# A copied source is not a second independent observation. For Bernoulli(1/4)
# versus Bernoulli(3/4), squared affinity is 3/4; true two-sample tensoring squares it.
out['copy_versus_product_affinity']={'one_squared_affinity':str(F(3,4)),
 'duplicated_observation_squared_affinity':str(F(3,4)),
 'independent_two_sample_squared_affinity':str(F(3,4)**2),
 'qualification':'Duplicate joint law has support {(0,0),(1,1)} and same masses as one observation; genuine tensor law has four cells.'}
# Tail-risk quotient must retain sequential root/index identity: reset counters
# duplicate a pair/index cell whereas actual cumulative counters are injective.
actions=[0,1,0,1,0]; counts={0:0,1:0};cells=[]
for a in actions:cells.append((a,counts[a]));counts[a]+=1
assert len(set(cells))==len(actions)
reset=[(a,0) for a in actions];assert len(set(reset))<len(actions)
out['reset_invalidates_global_charging']={'actual_cells':cells,'reset_cells':reset,
 'meaning':'The linear whole-run low-count budget uses actual globally unique consumed cells, not reset epoch labels.'}
out['status']='PASS: exact finite controls only; no new universal controller proof or Lean replay'
p=pathlib.Path(__file__);out['script_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
p.with_name('INTERFACE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
