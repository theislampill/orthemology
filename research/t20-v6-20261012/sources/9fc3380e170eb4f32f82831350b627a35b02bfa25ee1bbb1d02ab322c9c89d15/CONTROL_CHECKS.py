"""Exact finite controls for the source-derived calculation, not empirical trials."""
from fractions import Fraction as F
import json

checks = []
def check(label, condition):
    if not condition:
        raise RuntimeError(label)
    checks.append(label)

def laws(delta):
    return ([F(1,4)]*4,
            [F(1,4)+delta,F(1,4)-delta,F(1,4)-delta,F(1,4)+delta])

def inquiry(delta):
    l,p=laws(delta)
    masses=[(x+y)/2 for x,y in zip(l,p)]
    posterior=[y/(x+y) for x,y in zip(l,p)]
    risk=sum(m*q*(1-q) for m,q in zip(masses,posterior))
    return posterior,risk,F(1,4)-risk

for i in range(0,101):
    d=F(i,600)
    l,p=laws(d)
    check(f'positive_normalized_{i}',sum(l)==sum(p)==1 and min(l+p)>0)
    check(f'equal_fair_marginals_{i}', all(z[0]+z[1]==z[0]+z[2]==F(1,2) for z in [l,p]))
    check(f'rank_one_interaction_{i}',[p[j]-l[j] for j in range(4)]==[d,-d,-d,d])
    qs,risk,val=inquiry(d)
    check(f'exact_risk_formula_{i}',val==d*d/(1-4*d*d))
    check(f'posterior_formula_{i}',qs==[(F(1,4)+d)/(F(1,2)+d),(F(1,4)-d)/(F(1,2)-d),(F(1,4)-d)/(F(1,2)-d),(F(1,4)+d)/(F(1,2)+d)])

q0,r0,v0=inquiry(F(1,6))
q1,r1,v1=inquiry(F(1,12))
check('perfect_recording_posterior',q0==[F(5,8),F(1,4),F(1,4),F(5,8)])
check('perfect_recording_risk',r0==F(7,32) and v0==F(1,32))
check('quarter_flip_posterior',q1==[F(4,7),F(2,5),F(2,5),F(4,7)])
check('quarter_flip_value',v1==F(1,140))
check('price_reversal',v1<F(1,64)<v0)
check('half_flip_erases',inquiry(F(0))[2]==0)
old_factor=F(5,3); new_factor=F(4,3)
correct_odds=old_factor*(new_factor/old_factor)
incorrect_odds=old_factor*new_factor
check('replace_same_root',correct_odds/(1+correct_odds)==F(4,7))
check('duplicate_same_root_error',incorrect_odds/(1+incorrect_odds)==F(20,29))

def enc(parity,q): return tuple(1-z for z in q) if parity else q

def step(q,i): return q[1],i

for parity in range(2):
    for u in range(2):
        for v in range(2):
            q=(u,v); stored=enc(parity,q)
            migrated=enc(1-parity,enc(parity,stored))
            check(f'migration_decode_{parity}{u}{v}',enc(1-parity,migrated)==q)
            for i in range(2):
                executed=enc(parity,step(enc(parity,stored),i))
                after_exec_migrate=enc(1-parity,enc(parity,executed))
                after_migrate_exec=enc(1-parity,step(enc(1-parity,migrated),i))
                check(f'migration_execution_commutes_{parity}{u}{v}{i}',after_exec_migrate==after_migrate_exec)

print(json.dumps({'status':'PASS','check_count':len(checks),'checks':checks,
 'exact_values':{'gain_epsilon_0':str(v0),'gain_epsilon_quarter':str(v1),
                 'replacement_posterior':'4/7','duplicate_product_posterior':'20/29'},
 'limits':['finite exact rational controls, not an empirical experiment',
           'no proof of adaptive transcript induction by enumeration',
           'no diagonal-tree theorem or formal kernel replay',
           'no verified numerical sequential classifier']},indent=2))
