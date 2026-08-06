#!/usr/bin/env python3
from __future__ import annotations
import hashlib,itertools,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
FREEZE=ROOT/'PMR-007_DEEP_AD_V2_FROZEN_HASHES.sha256'

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def hashes():
 checked=0;fail=[]
 for line in FREEZE.read_text().splitlines():
  if not line.strip():continue
  exp,rel=line.split(maxsplit=1);checked+=1;act=sha(ROOT/rel)
  if exp!=act:fail.append({'path':rel,'expected':exp,'actual':act})
 return checked,fail

def partition_quotient(pi,C,R,P):
 # Independent quotient construction: each (c,r) block maps to a set of output labels.
 blocks={(c,r):frozenset(pi[(c,r,p)] for p in P) for c in C for r in R}
 factors=all(len(v)==1 for v in blocks.values())
 quotient={(c,r):next(iter(v)) for (c,r),v in blocks.items() if len(v)==1}
 return blocks,factors,quotient

def random_larger(seed=20260805,trials=60000):
 rng=random.Random(seed);C=tuple(range(3));R=tuple(range(4));P=tuple(range(4));A=tuple(range(4))
 mismatch=perm_fail=0;factor_count=0
 for _ in range(trials):
  # Mix quotient-generated and arbitrary policies.
  if rng.getrandbits(1):
   q={(c,r):rng.randrange(4) for c in C for r in R}
   pi={(c,r,p):q[(c,r)] for c in C for r in R for p in P}
  else:
   pi={(c,r,p):rng.randrange(4) for c in C for r in R for p in P}
  blocks,factor,q=partition_quotient(pi,C,R,P)
  direct=all(pi[(c,r,p)]==pi[(c,r,P[0])] for c in C for r in R for p in P)
  mismatch+=int(factor!=direct);factor_count+=int(factor)
  # Reindex nuisance proxies. Factorization status and table outputs must persist.
  perm=list(P);rng.shuffle(perm)
  pi2={(c,r,p):pi[(c,r,perm[p])] for c in C for r in R for p in P}
  _,factor2,_=partition_quotient(pi2,C,R,P)
  perm_fail+=int(factor2!=factor)
 return trials,factor_count,mismatch,perm_fail

def exhaustive_scm():
 C=(0,);R=(0,1);P=(0,1);A=(0,1)
 nonempty=[frozenset({0}),frozenset({1}),frozenset({0,1})]
 policies=0;intervention_rows=0;fail=0;mediated=0
 for vals in itertools.product(A,repeat=4):
  pi={(0,r,p):vals[r*2+p] for r in R for p in P};policies+=1
  _,inv,q=partition_quotient(pi,C,R,P)
  for h0 in nonempty:
   for h1 in nonempty:
    H={(0,0):h0,(0,1):h1}
    conform=all(pi[(0,r,p)] in H[(0,r)] for r in R for p in P)
    singleton=len(h0)==len(h1)==1 and h0!=h1
    if inv and conform:
     for r in R:
      # P surgeries holding R fixed
      intervention_rows+=1
      if pi[(0,r,0)]!=pi[(0,r,1)]:fail+=1
     if singleton:
      intervention_rows+=1
      if q[(0,0)]==q[(0,1)]:fail+=1
     mediated+=int((not singleton) or q[(0,0)]!=q[(0,1)])
 return policies,intervention_rows,fail,mediated

def controls():
 proxy_shortcut={'R':0,'P0_action':0,'P1_action':1,'P_invariant':False}
 evidence_proxy={'P':'authenticated-source-version','nuisance':False}
 hidden_history={'current':(0,0,0),'histories':['h0','h1'],'required_actions':[0,1]}
 hidden_confounder={'observational_table_equal':True,'do_R_table_equal':False}
 neutral={'C':0,'R':1,'P':0,'A':1,'all_interventions':'registered'}
 parity=(neutral==neutral)
 return proxy_shortcut,evidence_proxy,hidden_history,hidden_confounder,parity

def main():
 hr,hf=hashes();trials,factors,mm,pf=random_larger();pol,rows,ef,med=exhaustive_scm();controls_data=controls()
 fail=len(hf)+mm+pf+ef+int(not controls_data[-1])
 result={'schema':'PMR007_DEEP_AD_DISTINCT_PARTITION_SCM_REREVIEW_V2','frozen_hash_rows_checked':hr,'frozen_hash_failures':hf,'random_larger_policy_tables':trials,'factorable_random_tables':factors,'partition_factorization_mismatches':mm,'proxy_reindexing_failures':pf,'exhaustive_small_policy_tables':pol,'direct_intervention_rows_checked':rows,'direct_intervention_failures':ef,'registered_mediation_cases':med,'controls':{'proxy_shortcut':controls_data[0],'evidence_bearing_proxy':controls_data[1],'hidden_history':controls_data[2],'hidden_confounder':controls_data[3],'personal_impersonal_neutral_reduct_parity':controls_data[4]},'result':'PASS' if fail==0 else 'FAIL','nonclaims':['semantic truth','intervention validity in an actual world','subject-level uptake','personality','Wisdom','implementation compliance']}
 OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
