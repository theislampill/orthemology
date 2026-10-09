#!/usr/bin/env python3
"""Bounded algebra/numerical controls; no sampling and no asymptotic proof by scan."""
from pathlib import Path
from fractions import Fraction
import hashlib,json
import mpmath as mp
mp.mp.dps=140
count=0

def check(value, label):
    global count
    count+=1
    if not value:
        raise AssertionError(label)

def close(a,b,rel='1e-95',absolute='1e-120'):
    return abs(a-b)<=mp.mpf(absolute)+mp.mpf(rel)*max(abs(a),abs(b))

def const(n):
    m=n+1;c=mp.mpf(n)/m
    lam=(2-2**c)**m
    d=lam**2*(1-mp.mpf(2)**(-n))/(1+mp.mpf(2)**(-n))
    return m,c,lam,d

def S(x,y,c):
    return x**c+y**c-(x+y-x*y)**c

def derivatives(x,y,n):
    m,c,_,_=const(n);z=x+y-x*y;s=S(x,y,c)
    sx=c*(x**(c-1)-(1-y)*z**(c-1))
    sy=c*(y**(c-1)-(1-x)*z**(c-1))
    sxy=c*z**(c-2)*(1-c*(1-x)*(1-y))
    f=m*(m-1)*s**(m-2)*sx*sy+m*s**(m-1)*sxy
    return s,sx,sy,sxy,f

def Lfun(r,n):
    m,c,_,_=const(n)
    return (2-(2-r)**c)**m

def partition(n,K):
    _,_,lam,d=const(n);h=mp.mpf(2)**(-n)
    p=[];q=[]
    for k in range(K):
        r=mp.mpf(2)**(-k)
        p.append(r**(2*n)*(1-h*h))
        q.append(r**n*(Lfun(r,n)-h*Lfun(r/2,n)))
        check(q[-1]>0 and p[-1]>0,('positive shell',n,K,k))
        check(q[-1]**2/p[-1]+mp.mpf('1e-120')>=d,('shell lower',n,K,k))
    r=mp.mpf(2)**(-K)
    p.append(r**(2*n));q.append(r**n*Lfun(r,n))
    check(close(sum(p),1) and close(sum(q),1),('partition mass',n,K))
    chi=sum((b-a)**2/a for a,b in zip(p,q))
    kl=sum(b*mp.log(b/a) for a,b in zip(p,q))
    check(chi+mp.mpf('1e-120')>=K*d+lam**2-1,('finite lower',n,K))
    bound=2+mp.log(1+mp.mpf(1)/(n*(n+1)))
    check(0<=kl<=bound,('KL envelope',n,K))
    return chi,kl

# Exact rational c=1 control, not floating point.
for n in [1,2,3,8]:
    for x in [Fraction(0),Fraction(1,3),Fraction(2,3),Fraction(1)]:
        for y in [Fraction(0),Fraction(1,5),Fraction(4,5),Fraction(1)]:
            s=x+y-(x+y-x*y)
            check(s==x*y,('c=1 S',x,y))
            check(s**n==(x*y)**n,('c=1 joint law',n,x,y))

points=list(map(mp.mpf,['0.000001','0.001','0.1','0.5','0.9','0.999','0.999999']))
max_density_ratio=mp.mpf(0)
for n in [1,2,3,7,16,32]:
    m,c,lam,d=const(n)
    C=mp.mpf(n)**2+mp.mpf(n)/(n+1)
    check(close(m*(m-1)*c*c+m*c,C),('constant algebra',n))
    for x in points:
        check(close(S(x,1,c)**m,x**n),('x margin',n,x))
        check(close(S(1,x,c)**m,x**n),('y margin',n,x))
        for y in points:
            s,sx,sy,sxy,f=derivatives(x,y,n)
            check(0<s<=min(x**c,y**c),('tail bounds',n,x,y))
            check(sx>0 and sy>0 and sxy>0 and f>0,('positive derivatives',n,x,y))
            check(close(sx,mp.diff(lambda t:S(t,y,c),x)),('dx',n,x,y))
            check(close(sy,mp.diff(lambda t:S(x,t,c),y)),('dy',n,x,y))
            check(close(sxy,mp.diff(lambda u,v:S(u,v,c),(x,y),(1,1))),('dxy',n,x,y))
            check(close(f,mp.diff(lambda u,v:S(u,v,c)**m,(x,y),(1,1))),('density',n,x,y))
            check(sx<=c/x and sy<=c/y and sxy<=c/(x*y),('derivative envelopes',n,x,y))
            check(f*x*y<=C,('density envelope',n,x,y))
            max_density_ratio=max(max_density_ratio,f*x*y/C)
    r=mp.mpf(2)**(-128)
    q=S(r,r,c)**m;p=r**(2*n)
    check(close(q,r**n*Lfun(r,n)),('corner exact',n))
    check(abs(Lfun(r,n)/lam-1)<mp.mpf('1e-34'),('corner asymptotic check',n))
    pair_chi=(q-p)**2/(r**(2*n)*(1-r**n)**2)
    check(abs(pair_chi/(lam*lam)-1)<mp.mpf('1e-34'),('single-pair finite corner limit',n))

rows=[]
for n in [1,2,3,8,16,32]:
    _,_,lam,d=const(n)
    values={}
    old_chi=old_kl=mp.mpf(-1)
    for K in [1,2,4,8,16,32,64,128,256]:
        chi,kl=partition(n,K)
        check(chi+mp.mpf('1e-120')>=old_chi,('refinement chi',n,K))
        check(kl+mp.mpf('1e-120')>=old_kl,('refinement KL',n,K))
        values[K]=(chi,kl);old_chi,old_kl=chi,kl
    slope=(values[256][0]-values[128][0])/128
    relerr=abs(slope/d-1)
    check(relerr<mp.mpf('1e-25'),('incremental asymptotic slope',n))
    rows.append({'n':n,'lambda_n':mp.nstr(lam,20),'d_n':mp.nstr(d,20),
                 'chi_K256':mp.nstr(values[256][0],20),'KL_K256':mp.nstr(values[256][1],20),
                 'slope_128_to_256_relative_error':mp.nstr(relerr,8)})

out={'status':'PASS','precision_decimal_digits':mp.mp.dps,'assertions':count,
     'scope':'Exact rational equality controls plus finite high-precision formula checks; no Monte Carlo, empirical data, infinite-limit verification by computation, or n-rate theorem.',
     'max_sampled_density_over_envelope':mp.nstr(max_density_ratio,20),
     'partition_controls':rows,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2))
