#!/usr/bin/env python3
"""Exact rational tests for the monotone interval-to-uniform reconstruction.
The reconstruction sees interval point evaluations only. Exact fixture values
are used separately to verify the resulting whole-function error.
"""
from fractions import Fraction as F
from bisect import bisect_right
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
stats={'assertions':0,'reconstructions':0,'oracle_calls':0,'largest_mesh_exponent':0,
       'nonmonotone_lower_bound_panels':0}

def check(x):
    stats['assertions']+=1
    assert x

def evaluate(knots,x):
    xs=[p[0] for p in knots]
    j=max(0,min(len(knots)-2,bisect_right(xs,x)-1))
    a,u=knots[j];b,v=knots[j+1]
    return u+(v-u)*(x-a)/(b-a)

def evaluator(knots,style):
    def oracle(x,width,index):
        stats['oracle_calls']+=1
        y=evaluate(knots,x)
        if x==0 or x==1:return (x,x)
        # Both styles are genuine enclosures of width <= requested width.
        # Deliberately oscillating slack makes lower endpoints nonmonotone.
        delta=width*(F(1,2) if style==0 else F(index%3,2))
        return max(F(0),y-delta),min(F(1),y+width-delta)
    return oracle

def reconstruct(oracle,epsilon):
    m=0
    while True:
        den=2**m
        xs=[F(j,den) for j in range(den+1)]
        intervals=[oracle(x,epsilon/8,j) for j,x in enumerate(xs)]
        if max(intervals[j+1][1]-intervals[j][0] for j in range(den))<epsilon/2:
            break
        m+=1
    lo=[p[0] for p in intervals]
    if any(a>b for a,b in zip(lo,lo[1:])):
        stats['nonmonotone_lower_bound_panels']+=1
    running=F(0);a=[]
    for x,(l,u) in zip(xs,intervals):
        running=max(running,l);a.append((x,running))
    eta=epsilon/4
    g=[(x,(1-eta)*y+eta*x) for x,y in a]
    return a,g,intervals,m

fixtures=[
    [(F(0),F(0)),(F(1),F(1))],
    [(F(0),F(0)),(F(3,4),F(1,64)),(F(1),F(1))],
    [(F(0),F(0)),(F(1,2)-F(1,128),F(1,4)),
     (F(1,2)+F(1,128),F(3,4)),(F(1),F(1))],
]
records=[]
for fi,knots in enumerate(fixtures):
    for style in (0,1):
        for epsilon in [F(1,2),F(1,4),F(1,8),F(1,16)]:
            a,g,iv,m=reconstruct(evaluator(knots,style),epsilon)
            stats['reconstructions']+=1
            stats['largest_mesh_exponent']=max(stats['largest_mesh_exponent'],m)
            check(a[0]==(0,0) and a[-1]==(1,1))
            check(g[0]==(0,0) and g[-1]==(1,1))
            check(all(x[1]<=y[1] for x,y in zip(a,a[1:])))
            check(all(x[1]<y[1] for x,y in zip(g,g[1:])))
            check(all(a[j][1]>=iv[j][0] for j in range(len(a))))
            check(all(a[j][1]<=evaluate(knots,a[j][0]) for j in range(len(a))))
            check(max(iv[j+1][1]-iv[j][0] for j in range(len(a)-1))<epsilon/2)
            # Difference of two polygonal functions is affine between every
            # breakpoint in their union, so this maximum is the exact sup norm.
            points=sorted(set(x for x,y in a)|set(x for x,y in knots))
            ae=max(abs(evaluate(a,x)-evaluate(knots,x)) for x in points)
            ge=max(abs(evaluate(g,x)-evaluate(knots,x)) for x in points)
            check(ae<epsilon/2)
            check(ge<epsilon)
            # The same stopped mesh certifies a function-specific modulus.
            # For a polygonal fixture, the exact worst increment over distance
            # h occurs at a source knot, a source knot shifted left by h, or an
            # endpoint of the two relevant pieces.
            h=F(1,2**m)
            shift_points={F(0),F(1),1-h}
            shift_points|={x for x,y in knots}
            shift_points|={x-h for x,y in knots if 0<=x-h<=1}
            worst=max(evaluate(knots,min(F(1),x+h))-evaluate(knots,x)
                      for x in shift_points)
            check(worst<epsilon)
            records.append({'fixture':fi,'interval_style':style,'epsilon':str(epsilon),
                            'mesh_exponent':m,'polygonal_error':str(ae),
                            'strict_homeomorphism_error':str(ge),
                            'certified_modulus_distance':str(h),
                            'exact_maximum_increment_at_modulus_distance':str(worst)})
check(stats['nonmonotone_lower_bound_panels']>0)
# Continuous monotonicity is substantive. A central jump of 1/2 prevents the
# stop certificate for epsilon=1/4 on every tested mesh, even with exact values.
blocked=0
for m in range(1,11):
    xs=[F(j,2**m) for j in range(2**m+1)]
    vals=[x/2 if x<F(1,2) else F(1,2)+x/2 for x in xs]
    check(max(b-a for a,b in zip(vals,vals[1:]))>=F(1,2))
    blocked+=1
stats['discontinuity_no_stop_controls']=blocked
stats['status']='PASS'
stats['scope']='Finite rational polygonal controls support the general proof; observed meshes and calls are not uniform bounds.'
result={'summary':stats,'cases':records}
text=json.dumps(result,indent=2,sort_keys=True)+'\n'
(OUT/'INDEPENDENT_CONTROLS.json').write_text(text)
print(text,end='')
