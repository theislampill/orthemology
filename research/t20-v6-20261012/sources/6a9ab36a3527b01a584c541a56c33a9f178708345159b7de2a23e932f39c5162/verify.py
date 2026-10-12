"""High-precision controls, not a proof of limits or general theorems."""
from decimal import Decimal as D, localcontext
from pathlib import Path
import json, hashlib

def F(x):
    return sum(w*v*v.ln() for w,v in zip((D(1),D(2)),x) if v)
def div(x,y):
    return F(x)-F(y)-sum(w*(v.ln()+1)*(u-v) for w,u,v in zip((D(1),D(2)),x,y))
with localcontext() as ctx:
    ctx.prec=100
    tol=D('1e-85')
    p=(D('.5'),D('.5')); mu=D('1.5'); ln2=D(2).ln()
    prev=None; prevreg=None; rows=[]; checks=0
    for k in range(129):
        q2=D(2)/(D(1)+(D(1)+D(2)**(k+3)).sqrt());q=(D(1)-q2,q2)
        assert all(v>0 for v in q) and sum(q)==1;checks+=1
        t=k*ln2
        lam=2*((q2/p[1]).ln()+t)
        assert abs((q[0]/p[0]).ln()+t-lam)<tol;checks+=1
        reg=div(p,q); mq=q[0]+2*q[1]
        formula=t*mu-lam-mu+mq
        assert abs(reg-formula)<tol;checks+=1
        risk=sum(pi*div(e,q) for pi,e in zip(p,((D(1),D(0)),(D(0),D(1)))))
        baseline=sum(pi*div(e,p) for pi,e in zip(p,((D(1),D(0)),(D(0),D(1)))))
        assert abs(risk-baseline-reg)<tol;checks+=1
        if prev is not None:
            raw=tuple(v/2 for v in prev); gain=div(q,raw)
            assert gain>0 and reg>prevreg;checks+=1
            for e in ((D(1),D(0)),(D(0),D(1))):
                assert abs(div(e,raw)-div(e,q)-gain)<tol;checks+=1
            assert q[1]<prev[1];checks+=1
        if k in (0,1,2,4,8,16,32,64,128):
            rows.append({'k':k,'q2':str(q[1]),'regret':str(reg),'linear_asymptote':str(t/2-ln2-D('.5'))})
        prev,prevreg=q,reg
    assert abs(prevreg-(D(128)*ln2/2-ln2-D('.5')))<D('1e-18');checks+=1
    result={'status':'PASS','scope':'Decimal 100-digit numerical identity controls at 129 finite steps, tolerance1e-85; not exact symbolic, asymptotic proof, empirical test or kernel replay','checks':checks,'rows':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,indent=2))
