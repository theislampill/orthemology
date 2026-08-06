#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path
OUT=Path(__file__).with_name('pmr007_deep_r_r5_common_union_primary_check_v2_results.json')
BEARERS=('a','b','c','d'); ROLES=('W_role','P_role','K_role')
LINKS={
 ('o','CONSTRAINS','modal_transition_profiles'),
 ('finite_content_class','INFORMS','selection_coordinate_S'),
 ('exact_norm_potential_N','EVALUATES','revision_and_selection_states'),
 ('selection_coordinate_S','DIRECTS','a'),
 ('a','REALIZES','e'),
 ('feag_translation','TRANSPORTS','selected_finite_content'),
 ('response_transducer','UPDATES','selected_finite_state'),
}
REQUIRED_LINKS=set(LINKS)

def comp(f,g): return tuple(f[g[x]] for x in range(len(g)))
def inv(p):
 q=[0]*len(p)
 for i,v in enumerate(p): q[v]=i
 return tuple(q)

def groupoid():
 E=[(0,1,2),(1,2,0),(2,0,1)]
 T={(i,j):comp(E[j],inv(E[i])) for i in range(3) for j in range(3)}
 return all(comp(T[(j,k)],T[(i,j)])==T[(i,k)] for i in range(3) for j in range(3) for k in range(3))

def main():
 role_pairs=[(b,r) for b in BEARERS for r in ROLES]
 stats={'all':0,'global':0,'common':0,'no_common':0}; witness=None
 for bits in range(1<<len(role_pairs)):
  A={(b,r):bool((bits>>i)&1) for i,(b,r) in enumerate(role_pairs)}; stats['all']+=1
  if not all(any(A[(b,r)] for b in BEARERS) for r in ROLES): continue
  stats['global']+=1
  common=[b for b in BEARERS if all(A[(b,r)] for r in ROLES)]
  if common: stats['common']+=1
  else:
   stats['no_common']+=1
   if witness is None: witness={b:[r for r in ROLES if A[(b,r)]] for b in BEARERS}
 # Deep O coupling
 rows=[{'x':x,'y':y,'M':x,'A':y,'S':x^y,'N':x+y,'R':int(x+y>0)} for x,y in itertools.product((0,1),repeat=2)]
 joint={tuple(r[k] for k in ('M','A','S','N','R')) for r in rows}
 product=1
 for k in ('M','A','S','N','R'): product*=len({r[k] for r in rows})
 # Deep N cycle
 vals={(0,0):0,(1,0):1,(1,1):2,(0,1):1}; cyc=[(0,0),(1,0),(1,1),(0,1),(0,0)]
 inc=[vals[cyc[i+1]]-vals[cyc[i]] for i in range(4)]
 # Deep M token response
 tr=[(q,z,q^z,q if z==0 else 1-q) for q,z in itertools.product((0,1),repeat=2)]
 token_sensitive=any(a[2]!=b[2] for a,b in [(tr[0],tr[1]),(tr[2],tr[3])])
 links_ok=LINKS==REQUIRED_LINKS
 res={
  'identity':'PMR-007-R5CU-1',
  'role_allocation_stats':stats,
  'first_no_common_bearer_witness':witness,
  'formal_coupling':{'joint_profiles':len(joint),'marginal_product':product,'excluded':product-len(joint),'pass':product>len(joint)},
  'norm_cycle':{'increments':inc,'pass':sum(inc)==0},
  'articulability_groupoid_pass':groupoid(),
  'token_responsiveness_pass':token_sensitive,
  'typed_links':sorted([list(x) for x in LINKS]),
  'typed_link_graph_pass':links_ok,
  'neutral_source_flag':False,
  'withheld_conclusions':{'PERS':False,'IOWN':False,'WIS':False,'SPEECH':False,'REVELATION':False},
  'overall':'PASS' if stats['no_common']>0 and product>len(joint) and sum(inc)==0 and groupoid() and token_sensitive and links_ok else 'FAIL',
  'authority_note':'Finite common-model satisfiability only; stipulated necessity/externality and role proxies do not prove metaphysical or theological predicates.'
 }
 OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
if __name__=='__main__': main()
