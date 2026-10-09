from pathlib import Path
from fractions import Fraction
from math import comb
import json,sys
from identifiability import *
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'general-roots/src'))
import design_rank as d


def serial(x):
    if isinstance(x,Fraction):return {'numerator':x.numerator,'denominator':x.denominator}
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def main():
    direct=[]
    for kind in ('coalescence','redundant','priority_A'):
        model=one_effect_fixture(kind)
        direct.append({'model':kind,'anonymous_histogram':model,'exact_panel':endpoint_panel(model,1),
                       'recovered':recover_model(endpoint_panel(model,1),1),
                       'actual_profile_gate_modes':{mode:exact_distribution(occurrences(model),AB,mode)
                                                   for mode in ('incidence','route','shared_frozen','source_deletion','support_route')}})
    bundled={(AB,0,3):1};separate={(AB,0,1):1,(AB,0,2):1}
    bundle_control={'bundled':endpoint_panel(bundled,2),'separate':endpoint_panel(separate,2),
                    'bundled_histogram':recover_model(endpoint_panel(bundled,2),2),
                    'separate_histogram':recover_model(endpoint_panel(separate,2),2)}
    bad=(Q(1,2),Q(1,3),Q(1,5));repair=(Q(1,2),Q(1,3),Q(1,7));good=(Q(1,2),Q(1,5),Q(1,7))
    designs={name:{'probes':probes,'rank':d.rank(probes),'matrix':d.matrix(probes)[0],'row_labels':d.matrix(probes)[1],
                   'integer_kernel':d.kernel(probes)} for name,probes in [('bad',(bad,)),('repair_alone',(repair,)),('stacked',(bad,repair)),('good',(good,))]}
    lifts=[]
    for vector in d.kernel((bad,)):
        left,right=d.lift_guard_kernel(vector,3)
        lifts.append({'kernel':vector,'left':left,'right':right,'bad_left':d.guarded_panel(left,(bad,)),
                      'bad_right':d.guarded_panel(right,(bad,)),
                      'repair_full_left':d.guarded_probability(left,7,repair),
                      'repair_full_right':d.guarded_probability(right,7,repair)})
    sample=[]
    for k,n in ((4,20),(8,20),(12,20)):
        p,q=Q(1,2)**k,Q(1,2)**(k+1)
        tv=sum(abs(comb(n,j)*p**j*(1-p)**(n-j)-comb(n,j)*q**j*(1-q)**(n-j)) for j in range(n+1))/2
        sample.append({'k':k,'trials':n,'probability_absence_k':p,'probability_absence_k_plus_one':q,
                       'exact_total_variation':tv,'optimal_equal_prior_success':(1+tv)/2,
                       'coupling_upper_bound':min(Q(1),n*abs(p-q))})
    output={'scope':'Exact declared stochastic interface; no observations of physical originals or empirical data.',
            'direct':direct,'multi_effect':bundle_control,'general_designs':designs,'guard_kernel_lifts':lifts,'sampling':sample,
            'checked_cases':{'two_root_count_vectors':1024,'multi_effect_generated_models':80,'binary_three_root_models':128,
                             'general_guard_generated_models':32,'two_root_test_groups':20,'general_root_test_groups':8}}
    path=BASE/'results/RESULTS.json';path.write_text(json.dumps(serial(output),indent=2)+'\n')
    print(json.dumps({'result':str(path),'ranks':{k:v['rank'] for k,v in designs.items()},'test_groups':28}))

if __name__=='__main__':main()
