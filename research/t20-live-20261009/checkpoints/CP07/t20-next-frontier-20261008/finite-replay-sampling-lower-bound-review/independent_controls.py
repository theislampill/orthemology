#!/usr/bin/env python3
"""Independent exact controls. No imports from or writes to the author packet.
Rational isolating intervals certify the actual algebraic Joe quantities.
Finite controls supplement, and do not replace, the all-n written proof.
"""
from fractions import Fraction as F
from pathlib import Path
from sympy import integer_nthroot, symbols, simplify
import json

OUT=Path(__file__).resolve().parent
checks=[]
def check(label, condition):
    assert condition, label
    checks.append(label)

def power_enclosure(q,n,m,bits=112):
    """Closed dyadic enclosure of q^(n/m), using checked integer inequalities."""
    scale=1<<bits
    num=q.numerator**n * scale**m
    den=q.denominator**n
    r=int(integer_nthroot(num//den,m)[0])
    assert r**m*den <= num < (r+1)**m*den
    return F(r,scale),F(r+1,scale)

def emit(q):
    return {'numerator':str(q.numerator),'denominator':str(q.denominator)}

def small_display(q):
    return format(float(q),'.15g')

# Universal algebraic identities are checked separately from finite controls.
A,D=symbols('A D',nonzero=True)
check('exact chi-square simplification', simplify(D**2*(1/A**2+2/(A*(1-A))+1/(1-A)**2)-D**2/(A**2*(1-A)**2))==0)
n=symbols('n',integer=True,positive=True)
check('m c (1-c) equals c',simplify((n+1)*(n/(n+1))*(1-n/(n+1))-n/(n+1))==0)
check('advertised Delta constant',F(36,25)*F(1,9)==F(4,25))
check('advertised KL constant',196*F(4,25)**2==F(3136,625))
check('reciprocal lower-bound constant',1/F(3136,625)==F(625,3136))

rows=[]
for n in list(range(1,33))+[64,100,256,1000]:
    m=n+1; p=1-F(1,3*m); t=1-p; a=p**n
    x0,x1=power_enclosure(p,n,m)
    y0,y1=power_enclosure(1-t*t,n,m)
    s0,s1=2*x0-y1,2*x1-y0
    dl,du=s0**m-a*a,s1**m-a*a
    bound=F(4,25*m*m)
    chi_upper=du*du/(a*a*(1-a)**2)
    check(f'n={n}: strict Delta certified',dl>0)
    check(f'n={n}: Delta bound certified',du<=bound)
    check(f'n={n}: all positive replay cells',s0>0 and s1<1 and s1**m<a and 1-2*a+s0**m>0)
    check(f'n={n}: exact baseline interval',F(2,3)<a<=F(5,6))
    check(f'n={n}: exact baseline cell bound',min(a*a,a*(1-a),(1-a)**2)>=F(1,49))
    check(f'n={n}: chi-square bound certified',chi_upper<=F(3136,625*m**4))
    # Useful transparent certificate for roots, rather than enormous Delta fractions.
    rows.append({'n':n,'root_precision_bits':112,'p_power_interval':[emit(x0),emit(x1)],'one_minus_t_squared_power_interval':[emit(y0),emit(y1)],'delta_lower_approx':small_display(dl),'delta_upper_approx':small_display(du),'delta_bound_approx':small_display(bound),'chi_upper_over_claimed_bound_approx':small_display(chi_upper/F(3136,625*m**4))})

# Exact rational finite-tree test of the conditional chain-rule bookkeeping.
# This is a legal four-cell perturbation proxy, not a claim that these
# rational cell masses are the exact Joe masses. Joe is certified above.
a=F(5,6); delta=F(1,1000)
p0=[a*a,a*(1-a),a*(1-a),(1-a)**2]
p1=[p0[k]+delta*([1,-1,-1,1][k]) for k in range(4)]
q=F(1,3)
# state: history tuple, (law0 mass,law1 mass), accumulated replay count
states=[((),F(1),F(1),0)]
terminal=[]
prefix_rows=[]
# Store expected counts of each replay outcome, including earlier terminated paths.
outcome_counts=[F(0)]*4
expected_count=F(0)
for round_number in range(1,6):
    next_states=[]
    for hist,w0,w1,count in states:
        # Stop on replay cell 3. Some branches survive every prefix and have
        # no terminal decision yet; no label is silently assigned to them.
        if hist and hist[-1]==('R',3):
            terminal.append((hist,w0,w1,count)); continue
        # Both randomization and history-dependent allocation are common kernels.
        pr=F(2,3) if sum(z for _,z in hist)%2 else F(1,4)
        for action,pa in [('R',pr),('F',1-pr)]:
            dist0,dist1=(p0,p1) if action=='R' else ([1-q,q],[1-q,q])
            if action=='R':
                expected_count+=w1*pa
                for k in range(4): outcome_counts[k]+=w1*pa*p1[k]
            for k,(z0,z1) in enumerate(zip(dist0,dist1)):
                nh=hist+((action,k),)
                u0,u1=w0*pa*z0,w1*pa*z1
                # Exact likelihood ratio cancels every fresh outcome and policy factor.
                lr=F(1)
                for ac,j in nh:
                    if ac=='R': lr*=p1[j]/p0[j]
                check(f'tree prefix {round_number} path ratio {len(next_states)}',u1/u0==lr)
                next_states.append((nh,u0,u1,count+(action=='R')))
    states=next_states
    all_leaves=terminal+states
    check(f'tree prefix {round_number}: both law masses normalize',sum(x[1] for x in all_leaves)==1 and sum(x[2] for x in all_leaves)==1)
    en=sum(x[2]*x[3] for x in all_leaves)
    check(f'tree prefix {round_number}: count expectation',en==expected_count)
    check(f'tree prefix {round_number}: each KL log coefficient',all(outcome_counts[k]==en*p1[k] for k in range(4)))
    prefix_rows.append({'T':round_number,'leaf_count':len(all_leaves),'expected_replays_law1':emit(en),'terminated_probability_law1':emit(sum(x[2] for x in terminal))})

report={'status':'PASS','control_version':1,'independence':'No author controls imported. Source-result not required by these controls.','check_count':len(checks),'universal_symbolic_controls':checks[:5],'certified_Joe_examples':rows,'adaptive_rational_proxy_prefixes':prefix_rows,'limits':'Finite algebraic examples and finite adaptive trees are supplementary controls, not a proof by exhaustion for all n or all stopping rules. Approximate display columns are not used in any assertion.'}
(OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','check_count':len(checks),'certified_Joe_n':[r['n'] for r in rows],'adaptive_prefixes':len(prefix_rows)},indent=2))
