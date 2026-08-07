from itertools import product
import json
from pathlib import Path

# Neutral profile: accuracy, reliability, corrigibility, coherence.
# Hidden source coordinates: source, designer, truth aim, fitrah health,
# proper operation, suitable environment, undefeated warrant.
worlds=[]
for neutral in product([0,1], repeat=4):
    for hidden in product([0,1], repeat=7):
        src,des,aim,fit,op,env,und=hidden
        acc=neutral[0]
        npf=int(all([src,des,aim,fit,op,env,und,acc]))
        worlds.append((neutral,hidden,npf))

# Factorization through neutral profile fails iff one neutral fibre has both target values.
fibres={}
for q,h,t in worlds:
    fibres.setdefault(q,set()).add(t)
collisions={str(k):sorted(v) for k,v in fibres.items() if len(v)>1}

# The enriched profile including every contract coordinate determines NPF exactly.
enriched_map={}
enriched_failures=[]
for q,h,t in worlds:
    key=q+h
    prior=enriched_map.setdefault(key,t)
    if prior!=t: enriched_failures.append(key)

# One deletion witness for each conjunct: start with all true then set one false.
guard_names=['authentic_source','personal_designer','truth_directed_end','healthy_fitrah','proper_operation','suitable_environment','undefeated_warrant','output_accuracy']
base=[1]*8
deletion=[]
for i,g in enumerate(guard_names):
    x=base.copy();x[i]=0
    deletion.append({'guard':g,'conclusion_after_deletion':int(all(x))})

# Profile twins: Track-N-positive and impersonal selected-effect world.
q=(1,1,1,1)
pos=(1,1,1,1,1,1,1)
imp=(1,0,1,1,1,1,1)
twins={'same_neutral_profile':q,'track_n_target':int(all(pos+(q[0],))), 'impersonal_target':int(all(imp+(q[0],)))}

# Horn checks: none of the neutral horns automatically supplies all Track-N guards.
horn_guard_vectors={
 'retained_meta':          (0,0,1,0,1,1,0,1),
 'trans_state_truth':      (0,0,1,0,1,1,0,1),
 'holistic_fixed_point':   (0,0,0,0,1,1,0,1),
 'primitive_norm':         (0,0,1,0,0,1,0,1),
 'error_or_relative':      (0,0,0,0,1,1,0,0),
 'track_n_full_package':   (1,1,1,1,1,1,1,1),
 'selected_effect_tracker':(0,0,1,0,1,1,0,1),
}
horn_results={k:int(all(v)) for k,v in horn_guard_vectors.items()}

out={
 'schema':'PMR007_DEEP_F_PRIMARY_CHECK_RESULTS_V1',
 'worlds_checked':len(worlds),
 'neutral_fibres_checked':len(fibres),
 'neutral_collision_fibres':len(collisions),
 'neutral_factorization_fails':bool(collisions),
 'enriched_factorization_failures':len(enriched_failures),
 'deletion_witnesses':deletion,
 'all_deletions_block_declared_conclusion':all(x['conclusion_after_deletion']==0 for x in deletion),
 'profile_twins':twins,
 'horn_results':horn_results,
 'expected_only_full_track_n_package_satisfies_declared_contract':sum(horn_results.values())==1 and horn_results['track_n_full_package']==1,
 'pass':bool(collisions) and not enriched_failures and all(x['conclusion_after_deletion']==0 for x in deletion) and twins['track_n_target']==1 and twins['impersonal_target']==0 and sum(horn_results.values())==1,
}
Path(__file__).with_name('pmr007_deep_f_fitrah_proper_function_check_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
