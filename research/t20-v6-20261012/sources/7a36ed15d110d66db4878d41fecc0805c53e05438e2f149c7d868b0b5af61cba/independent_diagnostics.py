"""Independent floating-point diagnostics, not proof or exact arithmetic."""
import math, json
from pathlib import Path

def curve(t,p,a):
    def logtotal(lam):
        v=[math.log(x)-t+lam/w for x,w in zip(p,a)]
        m=max(v)
        return m+math.log(sum(math.exp(x-m) for x in v))
    lo=min(a)*t; hi=max(a)*t+1
    for _ in range(180):
        mid=(lo+hi)/2
        if logtotal(mid)>0: hi=mid
        else: lo=mid
    lam=(lo+hi)/2
    q=[math.exp(math.log(x)-t+lam/w) for x,w in zip(p,a)]
    z=sum(q); q=[x/z for x in q]
    mup=sum(x*w for x,w in zip(p,a)); muq=sum(x*w for x,w in zip(q,a))
    invH=sum(x/w for x,w in zip(q,a))
    # This positive pairwise formula avoids cancellation in muq-H near concentration.
    gap=sum(q[i]*q[j]*(a[i]-a[j])**2/(a[i]*a[j])
            for i in range(len(a)) for j in range(i))/invH
    regret=sum(w*(x*math.log(x/y)-x+y) for x,y,w in zip(p,q,a))
    formula=t*mup-lam-mup+muq
    assert abs(regret-formula)<2e-12
    return lam,q,regret,mup-muq,gap

results=[]
for p,a in [([.5,.5],[1,2]),([.1,.4,.5],[1,1,3]),([.2,.3,.5],[1,2,4])]:
    last=-1
    for k in range(301):
        t=k*math.log(2)
        lam,q,d,slope,curvature=curve(t,p,a)
        assert abs(sum(q)-1)<1e-12
        assert d>last
        assert slope>=-1e-12 and curvature>0
        last=d
    amin=min(a); PM=sum(x for x,w in zip(p,a) if w==amin)
    target=[x/PM if w==amin else 0 for x,w in zip(p,a)]
    qe=max(abs(x-y) for x,y in zip(q,target))
    le=abs(lam-(amin*t-amin*math.log(PM)))
    assert qe<1e-12 and le<1e-12
    results.append({'weights':a,'prior':p,'steps_checked':301,'k_final':300,
        'regret':d,'limit_q_error':qe,'lambda_asymptotic_error':le,
        't_slope':slope,'predicted_t_slope':sum(x*w for x,w in zip(p,a))-amin})

max_exact_error=0
for k in range(80):
    _,q,_,_,_=curve(k*math.log(2),[.5,.5],[1,2])
    q2=(math.sqrt(1+2**(k+3))-1)/2**(k+2)
    max_exact_error=max(max_exact_error,abs(q[1]-q2))
assert max_exact_error<1e-14
out={'status':'pass','scope':'Independent floating-point diagnostics; not proof or exact controls',
     'path_points':903,'radical_comparisons':80,'maximum_radical_error':max_exact_error,
     'cases':results}
print(json.dumps(out,indent=2))
