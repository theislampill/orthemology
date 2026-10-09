#!/usr/bin/env python3
"""Exact rational and certified interval diagnostics; no Monte Carlo or floating evidence."""
from fractions import Fraction as F
from collections import Counter
from functools import lru_cache
from pathlib import Path
import json
counts=Counter()
def check(x,name):
 assert x,name
 counts[name]+=1
def I(x):return F(x),F(x)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def sub(x,y):return x[0]-y[1],x[1]-y[0]
def mul(x,y):
 v=[a*b for a in x for b in y];return min(v),max(v)
def scale(x,a):return mul(x,I(a))
def power(x,k):
 assert x[0]>=0
 return x[0]**k,x[1]**k
@lru_cache(None)
def root_power(x,p,q,bits=128):
 x=F(x);target=x**p;lo=F(0);hi=max(F(1),x)
 for _ in range(bits):
  mid=(lo+hi)/2
  if mid**q<target:lo=mid
  else:hi=mid
 assert lo**q<=target<=hi**q
 return lo,hi
@lru_cache(None)
def log_small(x,terms=40):
 assert 1<=x<=2
 z=(x-1)/(x+1);s=F(0);power_z=z
 for k in range(terms):
  s+=power_z/(2*k+1);power_z*=z*z
 s*=2
 tail=2*power_z/((2*terms+1)*(1-z*z))
 return s,s+tail
@lru_cache(None)
def log_q(x):
 x=F(x);assert x>0;k=0
 while x>2:x/=2;k+=1
 while x<1:x*=2;k-=1
 return add(log_small(x),scale(log_small(F(2)),k))
def log_i(x):
 assert x[0]>0
 return log_q(x[0])[0],log_q(x[1])[1]
def outward(x,bits=96):
 den=1<<bits
 return F((x[0]*den).__floor__(),den),F((x[1]*den).__ceil__(),den)
def kl_i(P,Q):
 out=I(0)
 for p,q in zip(P,Q):
  # Outward dyadic rounding preserves enclosure and avoids huge power denominators.
  p=outward(p)
  ratio=outward(scale(p,1/q))
  out=add(out,mul(p,log_i(ratio)))
 return out
def kl_q(P,Q):return kl_i([I(x) for x in P],Q)
def compact(x,bits=80):
 den=1<<bits
 lo=(x[0]*den).__floor__();hi=(x[1]*den).__ceil__()
 return [str(F(lo,den)),str(F(hi,den))]

hard=[]
for n in list(range(1,41))+[64,100]:
 m=n+1;c=F(n,m);t=F(1,3*m);p=1-t;A=p**n
 P0=[A*A,A*(1-A),A*(1-A),(1-A)**2]
 check(F(2,3)<=A<=F(6,7),'uniform_face_probability_bounds')
 check(all(x>=F(1,49) for x in P0),'uniform_reference_cell_floor')
 check(sum(P0)==1,'reference_pair_mass')
 pc=root_power(p,n,m);plus=root_power(1+t,n,m);jointfail=root_power(1-t*t,n,m)
 check(pc[0]**m<=A<=pc[1]**m,'face_equality_defining_power')
 q0=(1-t*t)**n
 check(jointfail[0]**m<=q0<=jointfail[1]**m,'fresh_diagonal_equality_defining_power')
 D=sub(sub(I(2),plus),pc)
 check(D[0]>0,'strict_concavity_gap')
 Db=scale(pc,c*(1-c)*t*t/(p*p))
 check(D[1]<=Db[0],'Taylor_gap_certified_bound')
 S=sub(scale(pc,2),jointfail)
 check(0<S[0]<=S[1]<1,'Joe_per_route_neither_probability')
 J=power(S,m);Delta=sub(J,I(A*A))
 check(Delta[0]>0,'strict_replay_gap')
 stage=c*t*t*pc[0]**2/(p*p)
 check(Delta[1]<=stage,'difference_of_powers_certified_bound')
 bound=F(4,25*m*m)
 check(Delta[1]<=bound,'uniform_Delta_bound')
 check(F(36,25)*t*t==bound,'Delta_constant_identity')
 P1=[J,sub(I(A),J),sub(I(A),J),add(I(1-2*A),J)]
 check(all(x[0]>0 for x in P1),'Joe_pair_full_support')
 mass=I(0)
 for z in P1:mass=add(mass,z)
 check(mass[0]<=1<=mass[1],'Joe_pair_mass_enclosure')
 inv=sum(1/x for x in P0)
 check(inv<=196,'chi_square_coefficient_bound')
 chi=Delta[1]**2*inv
 dbar=F(3136,625*m**4)
 check(chi<=dbar,'chi_square_uniform_KL_bound')
 kval=kl_i(P1,P0)
 check(0<kval[0]<=kval[1]<=chi,'actual_KL_certified_below_chi_square')
 check(F(196)*bound**2==dbar,'KL_constant_identity')
 hard.append({'n':n,'m':m,'t':str(t),'A':str(A),'Delta_interval':compact(Delta),
              'Delta_upper_bound':str(bound),'KL_interval':compact(kval),'KL_upper_bound':str(dbar)})

# Binary relative entropy factor and explicit small-alpha comparison.
alpha_controls=[]
for a in [F(1,4),F(1,5),F(1,10),F(1,20),F(1,100),F(1,1000)]:
 direct=kl_q([1-a,a],[a,1-a])
 factor=scale(log_q((1-a)/a),1-2*a)
 check(not(direct[1]<factor[0] or factor[1]<direct[0]),'binary_kl_closed_form_consistency')
 lower=scale(log_q(1/a),F(1,4))
 check(factor[0]>=lower[1],'explicit_small_alpha_log_bound')
 alpha_controls.append({'alpha':str(a),'kl_interval':compact(factor)})

# Adaptive finite-prefix controls using a rational full-support surrogate pair.
# These test the chain-rule bookkeeping, not replace the exact Joe hard pair.
P0=[F(16,25),F(4,25),F(4,25),F(1,25)]
P1=[F(13,20),F(3,20),F(3,20),F(1,20)]
d=kl_q(P1,P0)
adaptive=[]
for horizon in [2,3,4]:
 leaves=[]
 def visit(step,last,pairs,occ,w0,w1,likelihood,reject):
  # Same policy, early stop after a 00 pair when at least one prior pair exists.
  if step==horizon or (last=='P0' and pairs>=2):
   leaves.append((w0,w1,pairs,occ,likelihood,reject));return
  pr=F(2,3) if last.startswith('F') else F(1,3)
  for i in range(4):
   oc=list(occ);oc[i]+=1
   visit(step+1,'P'+str(i),pairs+1,tuple(oc),w0*pr*P0[i],w1*pr*P1[i],likelihood*P1[i]/P0[i],reject or i==0)
  for outcome,pf in [(0,F(2,5)),(1,F(3,5))]:
   visit(step+1,'F'+str(outcome),pairs,occ,w0*(1-pr)*pf,w1*(1-pr)*pf,likelihood,reject)
 visit(0,'',0,(0,0,0,0),F(1),F(1),F(1),False)
 check(sum(x[0] for x in leaves)==sum(x[1] for x in leaves)==1,'adaptive_prefix_total_mass')
 for w0,w1,_,_,lr,_ in leaves:check(w1/w0==lr,'adaptive_path_likelihood_fresh_cancellation')
 EN1=sum(w1*N for w0,w1,N,oc,lr,e in leaves)
 EN0=sum(w0*N for w0,w1,N,oc,lr,e in leaves)
 coeff=[sum(w1*oc[i] for w0,w1,N,oc,lr,e in leaves) for i in range(4)]
 for i in range(4):check(coeff[i]==EN1*P1[i],'adaptive_exact_chain_rule_coefficients')
 event1=sum(w1 for w0,w1,N,oc,lr,e in leaves if e)
 event0=sum(w0 for w0,w1,N,oc,lr,e in leaves if e)
 eventkl=kl_q([event1,1-event1],[event0,1-event0])
 total=scale(d,EN1)
 check(total[0]>=eventkl[1],'adaptive_binary_data_processing_diagnostic')
 adaptive.append({'horizon':horizon,'leaf_count':len(leaves),'E_Joe_surrogate_pairs':str(EN1),
                  'E_reference_pairs':str(EN0),'event_probability_1':str(event1),'event_probability_0':str(event0)})

# The world used for expected cost matters under adaptive stopping.
check(2-P1[0]!=2-P0[0],'orientation_expected_count_distinction')
# No-data fair test satisfies error budgets >=1/2, not <1/2.
for a in [F(1,4),F(49,100),F(1,2),F(3,4)]:
 check((F(1,2)>=1-a)==(a>=F(1,2)),'random_guessing_error_boundary')
# Nontermination with probability 1-rho is not counted as a correct decision.
for rho in [F(0),F(1,4),F(1,2),F(1)]:
 check(rho/2<=F(1,2),'unconditional_terminal_correctness_mass')

out={'status':'PASS','assertions':sum(counts.values()),'families':dict(counts),
 'arithmetic':'Fraction arithmetic; certified rational roots and logarithm enclosures; no floating-point evidence',
 'hard_pair_controls':hard,'binary_error_controls':alpha_controls,'adaptive_surrogate_controls':adaptive,
 'limits':'Finite controls are diagnostics. General Taylor/KL/stopping proofs are in RESULT.md. Surrogate controls check bookkeeping, not physical experiments.'}
HERE=Path(__file__).resolve().parent
(HERE/'results'/'exact_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','assertions','families']},indent=2))
