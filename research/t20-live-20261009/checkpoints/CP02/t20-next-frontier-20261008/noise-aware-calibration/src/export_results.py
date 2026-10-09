from pathlib import Path
from dataclasses import is_dataclass,asdict
from fractions import Fraction
import json
from robust_masks import *
BASE=Path(__file__).resolve().parents[1]

def serial(value):
    if isinstance(value,Fraction):return {'numerator':value.numerator,'denominator':value.denominator}
    if is_dataclass(value):return serial(asdict(value))
    if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [serial(v) for v in value]
    return value

def main():
    model={(3,0,3):1,(1,2,3):1,(2,1,3):1};r=m=2;K=3
    p,epsilon=parameters(r,K);eta=epsilon/Q(2*K*r)
    ideal=exact_panel(model,r,m,K)
    calibrated=exact_panel(model,r,m,K,eta)
    empirical={key:min(Q(1),q+(epsilon/2 if sum(key)%2 else -epsilon/2)) for key,q in calibrated.items()}
    recovered,certificates=certify_guarded_effect_histogram(empirical,r,m,K)
    budgets=[]
    for roots,bound in [(r,k) for r in (1,2,3) for k in (1,2,5,10)]:
        settings=3**roots-2**roots;coordinates=settings
        exact_budget=sample_budget(roots,bound,coordinates,Q(1,20))
        robust_budget=sample_budget(roots,bound,coordinates,Q(1,20),True)
        budgets.append({'roots':roots,'total_route_bound':bound,'effect_count':1,'settings':settings,
                        'exact_calibration':exact_budget,'bounded_calibration_error':robust_budget,
                        'exact_total_trials':settings*exact_budget['per_setting_trials'],
                        'robust_total_trials':settings*robust_budget['per_setting_trials'],
                        'required_series_terms':required_terms(roots,bound)})
    result={'scope':'Synthetic bounded-error rational panels and analytical sampling budgets; no empirical trials performed.',
            'example':{'root_count':r,'effect_count':m,'bound':K,'ideal_rate':p,'epsilon':epsilon,'eta':eta,
                       'histogram':model,'ideal_panel':ideal,'calibrated_panel':calibrated,'synthetic_empirical_panel':empirical,
                       'recovered_histogram':recovered,'arithmetic_certificates':certificates,
                       'maximum_probability_error':max(abs(empirical[k]-ideal[k]) for k in ideal)},
            'sample_budgets':budgets,'author_test_groups':11,
            'test_coverage':{'two_root_extreme_error_panels':272,'noisy_guard_effect_models':18,'combined_error_models':15}}
    path=BASE/'results/RESULTS.json';path.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps({'result':str(path),'recovered':recovered==model,'budget_cases':len(budgets),'author_test_groups':11}))
if __name__=='__main__':main()
