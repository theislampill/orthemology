from pathlib import Path
from itertools import product,combinations
import hashlib,json,random,yaml
ROOT=Path(__file__).resolve().parents[1]
# frozen hashes
mis=[]
for line in (ROOT/'PMR-007_DEEP_G_V3_FROZEN_HASHES.sha256').read_text().splitlines():
 if not line.strip(): continue
 exp,rel=line.split(None,1);p=ROOT/rel.strip();got=hashlib.sha256(p.read_bytes()).hexdigest()
 if got!=exp: mis.append({'path':rel.strip(),'expected':exp,'observed':got})
# independent bitmask semantics for eligible-bearer sets
counts={'systems':0,'criterion_failures':0,'local_without_common':0,'pairwise_without_common':0,'fixed_witness_failures':0}
for na in range(1,5):
 for nb in range(1,5):
  full=(1<<nb)-1
  for masks in product(range(1<<nb), repeat=na):
   counts['systems']+=1
   inter=full
   for m in masks: inter &= m
   common=inter!=0
   # compute relation semantics directly
   direct=any(all((m>>b)&1 for m in masks) for b in range(nb))
   if common!=direct: counts['criterion_failures']+=1
   local=all(m!=0 for m in masks)
   if local and not common: counts['local_without_common']+=1
   pair=na>=2 and all(masks[i]&masks[j] for i,j in combinations(range(na),2))
   if pair and not common: counts['pairwise_without_common']+=1
   for d in range(nb):
    if all((m>>d)&1 for m in masks) and not direct: counts['fixed_witness_failures']+=1
# random larger systems
rng=random.Random(881734)
random_cases=25000;random_fail=0
for _ in range(random_cases):
 na=rng.randint(2,8);nb=rng.randint(2,8);masks=[rng.randrange(1<<nb) for _ in range(na)]
 inter=(1<<nb)-1
 for m in masks: inter &= m
 common=bool(inter);direct=any(all((m>>b)&1 for m in masks) for b in range(nb))
 if common!=direct: random_fail+=1
# explicit pairwise-only witness
masks=[0b011,0b110,0b101]
pairwise=all(masks[i]&masks[j] for i,j in combinations(range(3),2));global_inter=masks[0]&masks[1]&masks[2]
source=json.loads((ROOT/'checks/pmr007_deep_g_source_custody_check_v2_results.json').read_text())
model=yaml.safe_load((ROOT/'models/PMR007_DEEP_G_ATTRIBUTE_BEARER_INTEGRATION_MODELS_V3.yaml').read_text())
out={'schema':'PMR007_DEEP_G_V3_DISTINCT_REREVIEW_RESULTS','frozen_hash_mismatches':mis,'exhaustive_systems':counts['systems'],'criterion_failures':counts['criterion_failures'],'local_without_common':counts['local_without_common'],'pairwise_without_common':counts['pairwise_without_common'],'fixed_witness_failures':counts['fixed_witness_failures'],'random_larger_systems':random_cases,'random_failures':random_fail,'pairwise_only_witness':{'pairwise':pairwise,'global_intersection_nonempty':bool(global_inter)},'source_custody_pass':source['pass'],'source_locator_count':source['source']['locator_count'],'arabic_primary_verified':source['arabic_primary_verified'],'source_truth_established':source['source_truth_established'],'cb_inherited_from_qiyas':model['source_rule_coordinates']['new_integration_guard']['inherited_from_qiyas_rule'],'pass':not mis and counts['criterion_failures']==0 and counts['local_without_common']>0 and counts['pairwise_without_common']>0 and counts['fixed_witness_failures']==0 and random_fail==0 and pairwise and not global_inter and source['pass'] and not source['arabic_primary_verified'] and not source['source_truth_established'] and model['source_rule_coordinates']['new_integration_guard']['inherited_from_qiyas_rule'] is False}
Path(__file__).with_name('PMR-007_DEEP_G_V3_DISTINCT_REREVIEW_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
