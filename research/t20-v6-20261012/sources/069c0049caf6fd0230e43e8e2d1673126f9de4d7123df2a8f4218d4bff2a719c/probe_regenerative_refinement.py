"""Exact controls for summable departure hazards and restorative recovery."""
from fractions import Fraction as F
import json


def run():
    # Irreversible fault: one possible departure, but bad occupancy persists.
    survive=F(1);checks=[]
    for n in range(1,81):
        k=n+1;survive*=1-F(1,k*k)
        assert survive==F(n+2,2*(n+1))
        checks.append({'n':n,'no_departure':str(survive),'absorbing_bad':str(1-survive)})
    # A publicly detectable fault enters geometric recovery, not absorbing failure.
    good,bad=F(1),F(0);expected_bad=F(0);hazard_budget=F(0)
    for t in range(80):
        delta=F(1,(t+2)**2)
        ng=good*(1-delta)+bad*F(1,2)
        nb=good*delta+bad*F(1,2)
        good,bad=ng,nb;expected_bad+=bad;hazard_budget+=delta
        assert good+bad==1 and expected_bad<=2*hazard_budget
    # Finite a.s. recovery can have infinite expected duration.
    tail=F(1);partial_mean=F(0)
    for n in range(1,81):
        tail*=F(n,n+1)
        assert tail==F(1,n+1)
        partial_mean+=tail
    # Constant fault and geometric recovery: stationary bad mass > 0.
    stationary=[]
    for den in range(2,42):
        delta=F(1,den);rho=F(1,2);pi_bad=delta/(delta+rho)
        assert (1-pi_bad)*delta+pi_bad*(1-rho)==pi_bad
        assert pi_bad>0
        stationary.append({'fault_probability':str(delta),'stationary_bad_mass':str(pi_bad)})
    result={'telescoping_square_hazard_checks':len(checks),
        'irreversible_control':{'ever_departure_limit':'1/2','departure_count_at_most':1,
            'restoration_probability':'1/2','reason':'One departure causes permanent bad occupancy.'},
        'geometric_recovery':{'steps_exactly_checked':80,'bad_visit_bound':'E total bad visits <= 2 sum_t delta_t < infinity',
            'restoration_probability':'1','claim_basis':'Analytic regenerative/drift proof, not finite horizon.'},
        'heavy_tail_recovery':{'tail_checks':80,'tail':'P(T > n)=1/(n+1)',
            'almost_sure_finite':True,'mean_duration':'infinite'},
        'constant_hazard_controls':stationary,'mismatches':0}
    with open('regenerative_refinement_results.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='constant_hazard_controls'},indent=2))

if __name__=='__main__':run()
