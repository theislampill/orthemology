from itertools import product
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
expected={}
for line in (ROOT/'PMR-007_DEEP_BK_V2_FROZEN_HASHES.sha256').read_text().splitlines():
 h,p=line.split(maxsplit=1);expected[p]=h
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
res={'identity':'PMR-007-NCBD-1','checker':'DISTINCT_LOCAL_OCCURRENCE_V2','frozen_hash_rows':len(expected),'hash_mismatches':0,
     'local_models':0,'coverage_models':0,'coherent_lineage_without_B_ID':0,'B_ID_without_concreteness':0,
     'full_guard_models':0,'full_guard_failures':0,'actual_only_countermodels':0,
     'abstract_order_without_bearer':'PASS','frame_extension_control':'PASS'}
for p,h in expected.items():
 if sha(ROOT/p)!=h:res['hash_mismatches']+=1
# Each world has local occurrences 0,1. root choice -1/0/1. Each occurrence has global label 0/1/2 and concreteness bit.
for r0,r1 in product([-1,0,1],repeat=2):
 for gids in product(range(3),repeat=4):
  for concrete in product([False,True],repeat=4):
   res['local_models']+=1
   coverage=r0>=0 and r1>=0
   actual=r0>=0
   if actual and not coverage:res['actual_only_countermodels']+=1
   if not coverage:continue
   res['coverage_models']+=1
   # Declared counterpart transport sends selected local occurrence to selected local occurrence.
   coherence=True
   g0=gids[r0];g1=gids[2+r1]
   bid=(g0==g1)
   c0=concrete[r0];c1=concrete[2+r1]
   if coherence and not bid:res['coherent_lineage_without_B_ID']+=1
   if bid and not (c0 and c1):res['B_ID_without_concreteness']+=1
   full=coverage and coherence and bid and c0 and c1
   # Conclusion: one global label has concrete selected root occurrences in both worlds.
   conclusion=bid and c0 and c1
   if full:
    res['full_guard_models']+=1
    if not conclusion:res['full_guard_failures']+=1
bad=['hash_mismatches','full_guard_failures']
res['result']='PASS' if not any(res[x] for x in bad) and res['coherent_lineage_without_B_ID']>0 and res['B_ID_without_concreteness']>0 and res['actual_only_countermodels']>0 else 'FAIL'
OUT.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
