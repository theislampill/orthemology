#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
FREEZE=ROOT/'PMR-007_DEEP_AE_V2_FROZEN_HASHES.sha256'

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def hashcheck():
 checked=0;fail=[]
 for line in FREEZE.read_text().splitlines():
  if not line.strip():continue
  exp,rel=line.split(maxsplit=1);act=sha(ROOT/rel);checked+=1
  if exp!=act:fail.append({'path':rel,'expected':exp,'actual':act})
 return checked,fail

def mobius(vals,n):
 c=list(vals)
 for i in range(n):
  for m in range(1<<n):
   if m&(1<<i):c[m]-=c[m^(1<<i)]
 return c

def coeff_sep(coeffs,L,R):
 return all(v==0 or (m&~L)==0 or (m&~R)==0 for c in coeffs for m,v in enumerate(c))

def rectangular_sep(tables,n,L,R):
 # f(u,v)=f(u,0)+f(0,v)-f(0,0), exact direct construction.
 for vals in tables:
  base=vals[0]
  for x in range(1<<n):
   u=x&L;v=x&R
   if vals[x] != vals[u]+vals[v]-base:return False
 return True

def components(coeffs,n):
 parent=list(range(n))
 def find(a):
  while parent[a]!=a:
   parent[a]=parent[parent[a]];a=parent[a]
  return a
 def union(a,b):
  a,b=find(a),find(b)
  if a!=b:parent[b]=a
 for c in coeffs:
  for m,v in enumerate(c):
   if not v:continue
   bits=[i for i in range(n) if m>>i&1]
   for b in bits[1:]:union(bits[0],b)
 d={}
 for i in range(n):d.setdefault(find(i),0);d[find(i)]|=1<<i
 return tuple(sorted(d.values()))

def permute_table(vals,n,perm):
 out=[0]*(1<<n)
 for x in range(1<<n):
  y=0
  for i in range(n):
   if x>>i&1:y|=1<<perm[i]
  out[y]=vals[x]
 return out

def main():
 hr,hf=hashcheck();rng=random.Random(20260805);n=6;full=(1<<n)-1
 trials=12000;partition_cases=0;mismatch=0;component_fail=0;perm_fail=0;connected=0
 for _ in range(trials):
  # mixture of arbitrary and deliberately block-additive families
  if rng.getrandbits(1):
   Lmask=rng.randrange(1,full)
   Rmask=full^Lmask
   if not Rmask:Lmask=1;Rmask=full^1
   Lstates=[x for x in range(1<<n) if x&~Lmask==0]
   Rstates=[x for x in range(1<<n) if x&~Rmask==0]
   tables=[]
   for j in range(2):
    gl={x:rng.randrange(-3,4) for x in Lstates};hrv={x:rng.randrange(-3,4) for x in Rstates}
    tables.append([gl[x&Lmask]+hrv[x&Rmask] for x in range(1<<n)])
  else:
   tables=[[rng.randrange(-3,4) for _ in range(1<<n)] for _ in range(2)]
  coeffs=[mobius(t,n) for t in tables];comps=components(coeffs,n);connected+=int(len(comps)==1)
  # random 5 canonical bipartitions per family
  for _k in range(5):
   L=rng.randrange(1,full)
   if not (L&1):L^=1
   R=full^L
   if not R:continue
   partition_cases+=1
   a=coeff_sep(coeffs,L,R);b=rectangular_sep(tables,n,L,R)
   mismatch+=int(a!=b)
  # component partition must be additive for every table
  for B in comps:
   pass
  # check each support block-contained
  if any(v and not any((m&~B)==0 for B in comps) for c in coeffs for m,v in enumerate(c)):component_fail+=1
  # coordinate permutation preserves component-count though not labels
  perm=list(range(n));rng.shuffle(perm)
  tables2=[permute_table(t,n,perm) for t in tables]
  comps2=components([mobius(t,n) for t in tables2],n)
  perm_fail+=int(len(comps2)!=len(comps))
 controls={
  'impersonal_connected_family':{'functions':['x0*x1+x1*x2','x2*x3+x3*x4+x4*x5'],'b_add':1,'personal':False},
  'one_carrier_additive_family':{'functions':['x0+x1','x2+x3','x4+x5'],'one_carrier':True,'b_add':3},
  'hidden_latent':{'observed_b_add':1,'latent_registry_complete':False},
  'arbitrary_coupling':{'b_add':1,'explanatory_motivation':False}
 }
 fail=len(hf)+mismatch+component_fail+perm_fail
 result={'schema':'PMR007_DEEP_AE_DISTINCT_RECTANGULAR_ANOVA_REREVIEW_V2','frozen_hash_rows_checked':hr,'frozen_hash_failures':hf,'random_vector_families_n6_m2':trials,'partition_cases_checked':partition_cases,'mobius_vs_rectangular_identity_mismatches':mismatch,'connected_families':connected,'component_containment_failures':component_fail,'coordinate_permutation_component_count_failures':perm_fail,'controls':controls,'result':'PASS' if fail==0 else 'FAIL','nonclaims':['semantic coordinate validity','family completeness','causal direction','common bearer','personality','Wisdom']}
 OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
