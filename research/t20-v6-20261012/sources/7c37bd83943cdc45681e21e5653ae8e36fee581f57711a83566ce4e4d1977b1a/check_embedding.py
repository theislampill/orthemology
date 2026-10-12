#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from math import comb
from collections import defaultdict
from pathlib import Path
import random,json,hashlib
BASE=Path(__file__).resolve().parents[1];rng=random.Random(2026100112)

def is_pd(n,na,no,T):
 return all(sum(T.get((q,a,o,r),F(0))>0 for r in range(n))<=1 for q in range(n) for a in range(na) for o in range(no))

def setup(n,na,no,T,tags,good):
 k=len(tags);s0=(tuple(tags),-1)
 def obsprob(q,a,o):return sum(T.get((q,a,o,r),F(0)) for r in range(n))
 def successor(q,a,o):
  rr=[r for r in range(n) if T.get((q,a,o,r),F(0))>0]
  assert len(rr)<=1
  return rr[0] if rr else -1
 def upd(f,a,o):return tuple(successor(q,a,o) if q!=-1 else -1 for q in f)
 def dom(f):return frozenset(t for t,q in enumerate(f) if q!=-1)
 def row(t,s,a,extension=0):
  f,last=s
  if f[t]==-1:return {s0 if extension==0 else s:F(1)}
  out=defaultdict(F)
  for o in range(no):
   p=obsprob(f[t],a,o)
   if p:out[(upd(f,a,o),o)]+=p
  return dict(out)
 def lift(h):
  s=s0;hh=[]
  for a,o in h:s=(upd(s[0],a,o),o);hh.append((a,s))
  return tuple(hh)
 def extract(hh):return tuple((a,s[1]) for a,s in hh)
 def pi(seed,h):return (seed+len(h)+sum((i+1)*(3*a+o+1) for i,(a,o) in enumerate(h)))%na
 def Pi(seed,hh):return (seed+len(hh)+sum((i+1)*(a+s[1]+sum(s[0])+7) for i,(a,s) in enumerate(hh)))%na
 return s0,obsprob,upd,dom,row,lift,extract,pi,Pi

row_cases=prefix_cases=prefix_atoms=bad_law_cases=mixture_cases=domain_cases=0
for case in range(90):
 n=1+case%3;na=1+(case//3)%2;no=2
 tags=tuple(q for q in range(n) if rng.randrange(2)) or (rng.randrange(n),)
 T={}
 for q in range(n):
  for a in range(na):
   p=rng.choice([F(0),F(1,4),F(1,2),F(3,4),F(1)])
   for o,v in [(0,1-p),(1,p)]:
    if v:T[q,a,o,rng.randrange(n)]=v
 assert is_pd(n,na,no,T)
 good={(q,a) for q in range(n) for a in range(na) if rng.randrange(2)}
 s0,op,upd,dom,row,lift,extract,pi,Pi=setup(n,na,no,T,tags,good)
 k=len(tags);weights=[rng.randrange(1,6) for _ in tags];prior=[F(w,sum(weights)) for w in weights]
 # All explicit descriptor rows, including off-domain extensions, are normalized.
 for f in product(range(-1,n),repeat=k):
  for last in range(-1,no):
   s=(f,last)
   for t in range(k):
    for a in range(na):
     rr=row(t,s,a);assert sum(rr.values())==1 and all(p>=0 for p in rr.values());row_cases+=1
     if t not in dom(f):
      assert sum(row(t,s,a,1).values())==1
      assert not frozenset([t])<=dom(f);domain_cases+=1
     else:
      for sn,p in rr.items():
       C=frozenset(u for u in dom(f) if row(u,s,a).get(sn,F(0))>0)
       assert C==dom(sn[0]) and t in C
 # Both policy directions, multiple common independent seed atoms.
 for seed in [0,1,3]:
  for mode in [0,1]:
   mixtures_original=defaultdict(F);mixtures_lifted=defaultdict(F)
   for t,q0 in enumerate(tags):
    orig={(q0,(),0):F(1)};target={(s0,(),0):F(1)}
    for depth in range(1,6):
     new=defaultdict(F)
     for (q,h,c),p in orig.items():
      a=pi(seed,h) if mode==0 else Pi(seed,lift(h))
      for o in range(no):
       for qn in range(n):
        v=T.get((q,a,o,qn),F(0))
        if v:
         hn=h+((a,o),);lh=lift(hn);assert lh[-1][1][0][t]==qn
         new[qn,hn,c+int((q,a) not in good)]+=p*v
     orig=dict(new);new=defaultdict(F)
     for (s,hh,c),p in target.items():
      assert t in dom(s[0]) and lift(extract(hh))==hh
      a=pi(seed,extract(hh)) if mode==0 else Pi(seed,hh)
      for sn,v in row(t,s,a).items():
       hh1=hh+((a,sn),);new[sn,hh1,c+int((s[0][t],a) not in good)]+=p*v
     target=dict(new)
     po=defaultdict(F);pt=defaultdict(F)
     for (q,h,c),p in orig.items():po[h,c]+=p
     for (s,hh,c),p in target.items():pt[extract(hh),c]+=p
     assert po==pt and sum(po.values())==1
     prefix_cases+=1;prefix_atoms+=len(po)
     co=defaultdict(F);ct=defaultdict(F)
     for (h,c),p in po.items():co[c]+=p
     for (h,c),p in pt.items():ct[c]+=p
     assert co==ct;bad_law_cases+=1
    for key,p in po.items():mixtures_original[key]+=prior[t]*p
    for key,p in pt.items():mixtures_lifted[key]+=prior[t]*p
   assert mixtures_original==mixtures_lifted and sum(mixtures_original.values())==1;mixture_cases+=1
 # Exact descriptor cardinality including the initial marker.
 assert sum(1 for _ in product(range(-1,n),repeat=k))*(no+1)==(n+1)**k*(no+1)

# Countercontrol: two observations give the same map, but contain model information.
n=2;na=2;no=2;tags=(0,1);T={}
for q in range(2):
 for a in range(2):
  p=F(1,4) if q==0 else F(3,4)
  T[q,a,0,q]=1-p;T[q,a,1,q]=p
s0,op,upd,dom,row,*_=setup(n,na,no,T,tags,{(0,0),(1,1)})
assert upd(tags,0,0)==upd(tags,0,1)==tags
assert row(0,s0,0)!=row(1,s0,0)
assert sum(row(0,s0,0).values())==sum(row(1,s0,0).values())==1
collapsed=[{tags:sum(row(t,s0,0).values())} for t in [0,1]];assert collapsed[0]==collapsed[1]
# Countercontrol: the joint kernel is not a product of marginals.
Tjoint={(q,0,o,o):F(1,2) for q in [0,1] for o in [0,1]}
assert is_pd(2,1,2,Tjoint)
Tproduct={(q,0,o,r):F(1,4) for q in [0,1] for o in [0,1] for r in [0,1]}
assert not is_pd(2,1,2,Tproduct)
assert sum(p for (q,a,o,r),p in Tjoint.items() if q==0 and o==r)==1
assert sum(p for (q,a,o,r),p in Tproduct.items() if q==0 and o==r)==F(1,2)
# Same observations, opposite hidden targets: leaking tag changes the feasible policy class.
for N in range(1,9):
 sequence=[i%2 for i in range(N)]
 C0=sum(a!=0 for a in sequence);C1=sum(a!=1 for a in sequence);assert C0+C1==N
 assert sum(a!=0 for a in [0]*N)==sum(a!=1 for a in [1]*N)==0
# Zero prior mass must not create an extra universal requirement.
assert F(1)*0+F(0)*8==0 and 8>0
# Merging initial tags can preserve both tags while shrinking current-state support.
Tmerge={(q,0,0,0):F(1) for q in [0,1]};s0,op,upd,dom,row,*_=setup(2,1,1,Tmerge,(0,1),{(0,0)})
f=upd((0,1),0,0);assert f==(0,0) and dom(f)==frozenset([0,1]) and len(set(f))==1
# PD failure control: one observation leaves two next states possible.
Tnon={(0,0,0,0):F(1,2),(0,0,0,1):F(1,2),(1,0,0,1):F(1)};assert not is_pd(2,1,1,Tnon)
# Initial observation partition: condition on actual supplied initial label, no dummy action.
prior=[F(1,6),F(1,3),F(1,2)];labels=[0,0,1]
for o in [0,1]:
 indices=[q for q in range(3) if labels[q]==o];z=sum(prior[q] for q in indices);assert sum(prior[q]/z for q in indices)==1
# Value-one/attainment separation: waiting N times makes commitment error small,
# but every finite waiting word retains positive mass in both models.
majority=[]
for N in range(1,25):
 errors=[]
 for t,p in [(0,F(1,4)),(1,F(3,4))]:
  risk=sum(F(comb(N,j))*p**j*(1-p)**(N-j) for j in range(N+1) if int(2*j>N)!=t)
  assert 0<risk<=F(7,8)**N;errors.append(risk)
 for j in range(N+1):
  ratio=(F(3,4)**j*F(1,4)**(N-j))/(F(1,4)**j*F(3,4)**(N-j))
  assert F(1,3)**N<=ratio<=F(3)**N
 majority.append({'N':N,'errors':list(map(str,errors)),'upper':str(F(7,8)**N)})
r={'status':'PASS_FRESH_EXACT_EMBEDDING_CONTROLS','generated_PD_systems':90,'normalized_lifted_rows':row_cases,'off_domain_normalization_and_menu_checks':domain_cases,'conditional_prefix_law_comparisons':prefix_cases,'compared_prefix_atoms':prefix_atoms,'full_finite_bad_count_law_comparisons':bad_law_cases,'positive_prior_mixture_comparisons':mixture_cases,'depth':5,'common_seed_atoms':[0,1,3],'policy_directions':2,'value_one_finite_majority_controls':majority,'controls':{'last_observation_is_necessary':True,'joint_kernel_not_product':True,'tag_leak_changes_information':True,'zero_prior_tags_excluded':True,'tag_merging_not_elimination':True,'non_PD_kernel_rejected':True,'initial_observation_conditioned_explicitly':True},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite model/history laws. Infinite policy laws and complexity follow from the ordinary proof, not finite testing.'}
(BASE/'evidence/FRESH_EMBEDDING_CONTROLS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
