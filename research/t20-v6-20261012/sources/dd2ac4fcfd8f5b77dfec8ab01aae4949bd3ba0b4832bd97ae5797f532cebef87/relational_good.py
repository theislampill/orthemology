"""Relational total ends distinct from the numerical created-output target."""
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json

def end_satisfied(q,a,b):return a+b==q and a>0 and b>0

def original_roots(node,parents):
    if not parents.get(node):return {node}
    return set().union(*(original_roots(p,parents) for p in parents[node]))

def run():
    families=[]
    for q in range(1,7):
        good=[(a,b) for a,b in product(range(q+1),repeat=2) if end_satisfied(q,a,b)]
        families.append({'created_target':q,'outcome_optimal_profiles':[(a,b) for a,b in product(range(q+1),repeat=2) if a+b==q], 'relational_good_profiles':good,'A_solo_constructs_same_created_target':q+0==q,'A_solo_attains_relational_good':end_satisfied(q,q,0),'B_solo_attains_relational_good':end_satisfied(q,0,q)})
    derivative={
      'A_original':[],
      'A_intrinsic_act':['A_original'],
      'C_created_capacity':['A_original'],
      'C_created_will':['A_original'],
      'C_intrinsic_act':['C_created_capacity','C_created_will'],
      'e':['A_intrinsic_act','C_intrinsic_act'],
    }
    plural={
      'A_original':[],'B_original':[],
      'A_intrinsic_act':['A_original'],
      'B_intrinsic_act':['B_original'],
      'e':['A_intrinsic_act','B_intrinsic_act'],
    }
    # These edges interpret productive provenance, not numeric identity of acts.
    roots={'derivative_coactor':sorted(original_roots('e',derivative)),'original_coactor':sorted(original_roots('e',plural))}
    return {'schema':'relational-good-rival/1','run_utc':datetime.now(timezone.utc).isoformat(),
      'semantic_sorts':{'created_effect':'q; unchanged in solo/shared comparisons','intrinsic_activity':'distinct bearer-owned acts a and b; not appended as created q coordinates','total_intended_end':'created q AND both distinct bearers actively participate'},
      'relational_good_source_status':'HYPOTHESIS_TO_APPRAISE: not asserted as a pure perfection of ultimate sources',
      'finite_families':families,
      'continuous_countercontrol':{'target':2,'rational_distinct_satisfiers':[[str(a),str(2-a)] for a in [0.5,1.0,1.5]],'therefore_positive_participation_alone_selects_unique_allocation':False},
      'provenance_controls':{'derivative_graph':derivative,'plural_graph':plural,'original_root_supports':roots,'immediate_act_bearers':{'derivative':['A','C'],'plural':['A','B']},'two_actors_equals_two_original_sources':len(roots['derivative_coactor'])==2,
        'scope':'Graph controls only; not a proof of actual metaphysical origins or exhaustive cosmological effect accounting'},
      'three_end_readings':[
        {'end':'q and two distinct actors','one_original_root_can_supply_every_created_requisite_in_graph':len(roots['derivative_coactor'])==1,'distinct_intrinsic_acts_are_identified':False},
        {'end':'q and two independently original actors','solo_original_provision_excluded_by_end_content':True,'is_that_end_eligible_pure_perfection':'UNESTABLISHED'},
        {'end':'q produced through a particular independent original peer','solo_q_constructor_preserves_complete_intention':False,'foreign_original_completion_of_end':'EXPLICIT','received_standing_or_constitutive_perfection':'NOT_INFERRED_FROM_END_SATISFACTION_ALONE'},
      ]}
if __name__=='__main__':
 r=run();p=Path(__file__).resolve().parents[1]/'results/RELATIONAL_GOOD.json';p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
