"""Independent finite controls, not substitutes for the written proof."""
import json, hashlib
from pathlib import Path
import mpmath as mp
mp.mp.dps=90
root=Path(__file__).resolve().parent

def panel_law(n, routes, joe):
    m=n+1; c=mp.mpf(n)/m
    cuts=[mp.mpf(i)/(m+1) for i in range(m+2)]
    queries=[(cuts[i],cuts[m+1-i]) for i in range(1,m+1)]
    queries += [(cuts[i], cuts[m-i]) for i in range(1,m)]
    F=lambda x,y: 1-(1-x*y)**c if joe else x*y
    one={}
    for i in range(m+1):
        for j in range(m+1):
            x0,x1=cuts[i:i+2]; y0,y1=cuts[j:j+2]
            mask=sum((1<<k) for k,(a,b) in enumerate(queries) if (x0+x1)/2<a and (y0+y1)/2<b)
            p=F(x1,y1)-F(x0,y1)-F(x1,y0)+F(x0,y0)
            assert p>0
            one[mask]=one.get(mask,0)+p
    law={0:mp.mpf(1)}
    for _ in range(routes):
        new={}
        for a,p in law.items():
            for b,q in one.items(): new[a|b]=new.get(a|b,0)+p*q
        law=new
    assert abs(sum(law.values())-1)<mp.mpf('1e-80')
    return law

panels=[]
for n in [1,2,3]:
    p=panel_law(n,n,False); q=panel_law(n,n+1,True)
    assert set(p)<=set(q)
    E=(1<<(n+1))-1
    assert E not in p and q[E]>0
    if n==1: assert abs(q[E]-(30-8*mp.sqrt(14))/9)<mp.mpf('1e-80')
    panels.append(dict(n=n,baseline_support=len(p),alternative_support=len(q),certificate_probability=str(q[E]),reverse_domination_constant=str(max(p[s]/q[s] for s in p))))
strips=[]
for n in [1,2,5,20]:
    m=n+1; c=mp.mpf(n)/m; A=c*3**(2-c)
    B=3**(n-1)*A*(m*(m-1)*c+m)/(n*n)
    for y in [mp.mpf(1)/3,mp.mpf(1)/2,mp.mpf(2)/3]:
        for x in [mp.mpf('0.4'),mp.mpf('1e-3'),mp.mpf('1e-12')]:
            z=x+y-x*y; S=x**c+y**c-z**c
            Sx=c*(x**(c-1)-(1-y)*z**(c-1))
            Sy=c*(y**(c-1)-(1-x)*z**(c-1))
            Sxy=c*z**(c-2)*(1-c*(1-x)*(1-y))
            f1=m*(m-1)*S**(m-2)*Sx*Sy+m*S**(m-1)*Sxy
            f0=n*n*x**(n-1)*y**(n-1)
            ratio=f1/f0
            assert 0<Sxy<=A and 0<Sy<=A*x
            assert 0<ratio<=B*x**(1-c)
            strips.append(dict(n=n,x=str(x),y=str(y),ratio=str(ratio),upper=str(B*x**(1-c))))
result=dict(status='PASS',precision_decimal_digits=90,panel_cases=panels,strip_checks=len(strips),strip_details=strips,scope='Finite deterministic controls only; proofs supply all-n and continuum conclusions.')
(root/'REVIEW_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='strip_details'},indent=2))
