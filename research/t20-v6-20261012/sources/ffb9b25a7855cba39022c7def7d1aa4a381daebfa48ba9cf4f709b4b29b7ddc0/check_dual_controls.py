"""Exact finite algebraic controls, not an ODE solver or an analytic proof."""
from fractions import Fraction as Q
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
checks = 0

def check(x):
    global checks
    checks += 1
    assert x

def field(b, reciprocal, normalized=False):
    r = sum(b) - 1
    mobility = tuple(reciprocal(x) for x in b)
    total = sum(mobility)
    return tuple(-r*x/(total if normalized else 1) for x in mobility)

def main():
    a=(Q(1,5),Q(2,5),Q(4,5))
    b=(Q(3,10),Q(1,2),Q(3,5))
    mobility=lambda x:x*(1-x)
    rates=[]
    normalized_gains=[]
    for xs in (a,b):
        r=sum(xs)-1
        S=sum(map(mobility,xs))
        v=field(xs,mobility)
        w=field(xs,mobility,True)
        check(sum(xs)==Q(7,5))
        check(sum(w)==-r)
        # In dual coordinates y=logit(b), y'=h(b)*b'=-r.
        dual=tuple(vv/mobility(x) for x,vv in zip(xs,v))
        check(dual==(-r,)*3)
        gains=[]
        for j in range(3):
            g=sum((x-int(i==j))*vv/mobility(x)
                  for i,(x,vv) in enumerate(zip(xs,v)))
            gn=sum((x-int(i==j))*ww/mobility(x)
                   for i,(x,ww) in enumerate(zip(xs,w)))
            check(g==-r*r)
            check(gn==-r*r/S)
            gains.append(g)
        check(len(set(gains))==1)
        rates.append(sum(v))
        normalized_gains.append(-r*r/S)
        # The first four power-sum Lie derivative identities at this point.
        for k in range(1,5):
            actual=sum(k*x**(k-1)*vv for x,vv in zip(xs,v))
            expected=-k*r*(sum(x**k for x in xs)-sum(x**(k+1) for x in xs))
            check(actual==expected)
    check(rates==[Q(-28,125),Q(-7,25)])
    check(normalized_gains==[Q(-2,7),Q(-8,35)])
    # Quadratic model: use u=exp(-3t) exactly, not rounded logarithms.
    initial=(Q(1,100),Q(4,5),Q(4,5));r0=sum(initial)-1
    u=Q(58,61)
    at_boundary=tuple(x-r0*(1-u)/3 for x in initial)
    check(at_boundary[0]==0)
    check(sum(at_boundary)==Q(79,50))
    check(all(0<x<1 for x in at_boundary[1:]))
    symmetric=(Q(161,300),)*3
    check(sum(symmetric)==sum(initial))
    sym_boundary=tuple(x-r0*(1-u)/3 for x in symmetric)
    check(sum(sym_boundary)==sum(at_boundary))
    check(all(0<x<1 for x in sym_boundary))
    check(min(initial)<r0/3<min(symmetric))
    for u in (Q(1),Q(99,100),Q(58,61)):
        xs=tuple(x-r0*(1-u)/3 for x in initial)
        check(sum(xs)-1==r0*u)
        check(min(xs)==min(initial)-r0*(1-u)/3)
        # d/ dt [-r0(1-u)/3] = -r0*u when u'=-3u.
        check(tuple(-r0*u for _ in xs)==field(xs,lambda _:Q(1)))
    out={'status':'PASS','assertions':checks,
         'binary_log_original_z_rates':[str(x) for x in rates],
         'binary_log_normalized_state_loss_rates':[str(x) for x in normalized_gains],
         'quadratic_boundary_sum':str(sum(at_boundary)),
         'scope':'Exact finite rational identities. No numerical trajectory, general proof, kernel or empirical verification.'}
    (HERE/'DUAL_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
