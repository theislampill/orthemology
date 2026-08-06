from itertools import product
from pathlib import Path
import json

counts={'matrices':0,'local':0,'local_without_common':0,'pairwise':0,'pairwise_without_common':0,'criterion_failures':0,'fixed_d_cases':0,'fixed_d_failures':0}
minimal_local=None;minimal_pairwise=None
# exhaustive relation matrices for 1..4 attributes and 1..4 bearers
for na in range(1,5):
  for nb in range(1,5):
    cells=na*nb
    for bits in product([0,1], repeat=cells):
      counts['matrices']+=1
      sets=[]
      for a in range(na):
        sets.append({b for b in range(nb) if bits[a*nb+b]})
      local=all(sets)
      inter=set(range(nb))
      for s in sets: inter &= s
      common=bool(inter)
      criterion=common == bool(set.intersection(*sets) if sets else set())
      if not criterion: counts['criterion_failures']+=1
      if local:
        counts['local']+=1
        if not common:
          counts['local_without_common']+=1
          if minimal_local is None: minimal_local={'attributes':na,'bearers':nb,'sets':[sorted(s) for s in sets]}
      pairwise=na>=2 and all(sets[i]&sets[j] for i in range(na) for j in range(i+1,na))
      if pairwise:
        counts['pairwise']+=1
        if not common:
          counts['pairwise_without_common']+=1
          if minimal_pairwise is None: minimal_pairwise={'attributes':na,'bearers':nb,'sets':[sorted(s) for s in sets]}
      # fixed-d guard test for every possible d
      for d in range(nb):
        if all(d in s for s in sets):
          counts['fixed_d_cases']+=1
          if not common: counts['fixed_d_failures']+=1

# Exact intended witnesses
local_witness=[{0},{1}]
pairwise_witness=[{0,1},{1,2},{0,2}]
def common(ss):
  x=set.union(*ss) if ss else set()
  for s in ss: x &= s
  return bool(x)
def pairwise(ss): return all(ss[i]&ss[j] for i in range(len(ss)) for j in range(i+1,len(ss)))

out={
 'schema':'PMR007_DEEP_G_COMMON_BEARER_CHECK_RESULTS_V1',
 **counts,
 'first_local_without_common':minimal_local,
 'first_pairwise_without_common':minimal_pairwise,
 'declared_local_witness_pass':all(local_witness) and not common(local_witness),
 'declared_pairwise_witness_pass':pairwise(pairwise_witness) and not common(pairwise_witness),
 'pass':counts['criterion_failures']==0 and counts['local_without_common']>0 and counts['pairwise_without_common']>0 and counts['fixed_d_failures']==0 and all(local_witness) and not common(local_witness) and pairwise(pairwise_witness) and not common(pairwise_witness)
}
Path(__file__).with_name('pmr007_deep_g_common_bearer_check_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
