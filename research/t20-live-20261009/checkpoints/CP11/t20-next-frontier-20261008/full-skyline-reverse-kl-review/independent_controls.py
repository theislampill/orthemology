"""Independent deterministic diagnostics; no imports from author code."""
from pathlib import Path
from fractions import Fraction as F
from math import comb, factorial
import hashlib
import json
import mpmath as mp

mp.mp.dps = 100
BASE = Path(__file__).resolve().parent
rows = []

def asmp(x):
    return mp.mpf(x.numerator) / x.denominator if isinstance(x, F) else mp.mpf(x)

def skyline(points):
    out=[]
    h=F(1)
    for x,y in sorted(points):
        if y<h:
            out.append((x,y))
            h=y
    return out

def area(s):
    xprev=F(0)
    h=F(1)
    u=F(0)
    for x,y in s:
        u+=(x-xprev)*h
        xprev,h=x,y
    return u+(1-xprev)*h

def height(s,a):
    return min([F(1)]+[y for x,y in s if x<=a])

def dyadic_j(n):
    return (n-1).bit_length()

# Exact geometry, including n=1, powers of two, partial last bands, and ties
# in deterministic diagnostic samples (ties do not enter the density claims).
geo=[]
for n in [1,2,3,4,5,7,8,9,16,17,31,32,33]:
    for kind in range(5):
        points=[]
        for i in range(n):
            x=F(i+1,n+1)
            yi=[i+1,n-i,(7*i+3)%n+1,(i*i+1)%n+1,1][kind]
            y=F(yi,n+1)
            points.append((x,y))
        s=skyline(points)
        u=area(s)
        j=dyadic_j(n)
        ts=[n*F(1,2**(r+1))*height(s,F(1,2**(r+1))) for r in range(j)]
        bound=1+sum(ts,F(0))
        assert n*u<=bound
        geo.append({'n':n,'kind':kind,'K':len(s),'area':str(u),'scaled_area':str(n*u),'dyadic_bound':str(bound)})
rows.append({'name':'exact_dyadic_geometry','cases':len(geo),'status':'PASS','details':geo})

# Integrate the strict tail exactly. The atom at T=na is included by layer cake.
hm=[]
for n in [1,2,3,5,8,12,20]:
    for a in [F(1,64),F(1,8),F(1,2),F(9,10),F(1)]:
        moment=4*n**4*sum(((-1)**j*comb(n,j)*a**(j+4)/F(j+4) for j in range(n+1)),F(0))
        assert 0<moment<=24
        hm.append({'n':n,'a':str(a),'fourth_moment':str(moment),'upper_bound':'24'})
rows.append({'name':'exact_height_fourth_moments','cases':len(hm),'status':'PASS','details':hm})

# Independent Bernoulli convolution, rather than the author's formula routine.
rm=[]
dist=[F(1)]
H=F(0)
for m in range(1,65):
    p=F(1,m)
    nxt=[F(0)]*(len(dist)+1)
    for k,v in enumerate(dist):
        nxt[k]+=v*(1-p)
        nxt[k+1]+=v*p
    dist=nxt
    H+=p
    exact=sum((k**4*v for k,v in enumerate(dist)),F(0))
    bound=H**4+6*H**3+7*H**2+H
    assert exact<=bound and sum(dist)==1
    mgf=sum(asmp(v)*mp.exp(k) for k,v in enumerate(dist))
    assert mgf<=mp.exp((mp.e-1)*asmp(H))*(1+mp.mpf('1e-95'))
    rm.append({'m':m,'fourth_moment':str(exact),'bound':str(bound)})
rows.append({'name':'record_fourth_moment_and_mgf','cases':len(rm),'status':'PASS','details':rm})

# Explicit eventual threshold independently verifies the unspecified "eventually".
# For m>=2^20: H_m<=1+log m, J<=1+log(m)/log(2), m/n<=2.
def benv(m):
    l=mp.log(m)
    return mp.e*(1+l)+20*l+2*(1+20*l*(1+l/mp.log(2)))
threshold=2**20
b=benv(threshold)/threshold
assert b<mp.mpf('0.02') and 23*b*b<1
# For l>=20 log 2, (polynomial in l)*exp(-l) is decreasing:
# B = A*l^2+B*l+C, B-B' = A*l^2+(B-2A)*l+(C-B).
A=40/mp.log(2); BB=mp.e+60; C=mp.e+2
l0=mp.log(threshold)
assert A*l0*l0+(BB-2*A)*l0+C-BB>0
assert 2*A*l0+BB-2*A>0
rows.append({'name':'all_m_eventual_window_from_2_pow_20','status':'PASS','threshold':threshold,'upper_B_over_m':mp.nstr(b,25),'upper_23_B_over_m_squared':mp.nstr(23*b*b,25),'method':'analytic positive increasing derivative of B-Bprime thereafter'})

def ll_exact(m,s):
    k=len(s)
    c=1-mp.mpf(1)/m
    u=asmp(area(s)); d0=1-u
    sm=[(asmp(x),asmp(y)) for x,y in s]
    dc=mp.mpf(0)
    for i,(x,y) in enumerate(sm):
        xp=sm[i+1][0] if i+1<k else mp.mpf(1)
        dc+=(1-x)**c-(1-xp)**c+(1-xp*y)**c-(1-x*y)**c
    assert dc>0 and d0>0
    lf=sum(mp.log(c)+(c-2)*mp.log1p(-x*y)+mp.log1p(-c*x*y) for x,y in sm)
    return mp.log(mp.mpf(m)/(m-k))+lf+(m-k)*mp.log(dc)-(m-1-k)*mp.log(d0)

like=[]
for m in [2,3,4,8,16,64,256,4096]:
    for k in sorted(set([1,min(m-1,2),min(m-1,5)])):
        for scale in [F(1,1000),F(1,10),F(1,2),F(9,10)]:
            s=[(scale*F(i+1,k+1),scale*F(k-i,k+1)) for i in range(k)]
            k=len(s); u=asmp(area(s)); z=mp.mpf(k)/m+u
            ll=ll_exact(m,s)
            # A full baseline latent vector with this skyline is obtained by
            # adding repeated deterministic dominated points at (1-eps,1-eps).
            eps=F(1,10000)
            pts=s+[(1-eps,1-eps)]*(m-1-k)
            W=sum(-mp.log1p(-asmp(x))-mp.log1p(-asmp(y)) for x,y in pts)
            assert abs(ll)<=2*m*(1+W)
            if z<=mp.mpf('.5'):
                assert abs(ll)<=23*z*z
            like.append({'m':m,'k':k,'scale':str(scale),'z':mp.nstr(z,20),'log_likelihood':mp.nstr(ll,24),'bulk_applies':bool(z<=mp.mpf('.5'))})
# The unbounded boundary family is included explicitly, with no bulk use.
for exponent in [4,16,64]:
    s=[(1-F(1,10**exponent),F(1,2))]
    ll=ll_exact(8,s)
    W=sum(-mp.log1p(-asmp(x))-mp.log1p(-asmp(y)) for x,y in s)+12*mp.log(10**(exponent+1))
    assert abs(ll)<=16*(1+W)
    like.append({'m':8,'boundary_exponent':exponent,'log_likelihood':mp.nstr(ll,24),'bulk_applies':False})
rows.append({'name':'exact_likelihood_bulk_and_global_controls','cases':len(like),'status':'PASS','details':like})

# Uniform in n bound for the global logarithm's second moment.
for n in range(1,1001):
    m=n+1
    assert 4*n*n+6*n+1<=4*m*m
rows.append({'name':'global_log_second_moment_envelope','cases':1000,'status':'PASS'})

# Subprobability-likelihood controls: reverse entropy needs the +p correction.
q0=[F(1,3),F(2,3)]
q1=[F(1,4),F(1,2),F(1,4)]
p=q1[2]
L=[q1[i]/q0[i] for i in range(2)]
assert sum(q0[i]*L[i] for i in range(2))==1-p
D=sum(asmp(q0[i])*(-mp.log(asmp(L[i]))) for i in range(2))
phi=sum(asmp(q0[i])*(-mp.log(asmp(L[i]))+asmp(L[i])-1) for i in range(2))
assert abs(D-phi-asmp(p))<mp.mpf('1e-95')
assert abs(D-(phi-asmp(p)))>mp.mpf('.49')
assert abs(D-phi)>mp.mpf('.24')
rows.append({'name':'singular_correction_sign_and_mutants','status':'PASS','D':mp.nstr(D,25),'mass_correction':str(p),'wrong_minus_rejected':True,'wrong_zero_rejected':True})

# Stop after first observation 0; after 1, reveal a second independent symbol.
# A singular first/second alternative symbol has zero baseline mass.
tr0={(0,):q0[0],(1,0):q0[1]*q0[0],(1,1):q0[1]*q0[1]}
tr1={(0,):q1[0],(2,):q1[2],(1,0):q1[1]*q1[0],(1,1):q1[1]*q1[1],(1,2):q1[1]*q1[2]}
Dt=sum(asmp(v)*mp.log(asmp(v/tr1[key])) for key,v in tr0.items())
EN0=1+q0[1]; EN1=1+q1[1]
assert abs(Dt-D*asmp(EN0))<mp.mpf('1e-95')
assert abs(Dt-D*asmp(EN1))>mp.mpf('.04')
rows.append({'name':'stopped_reverse_KL_orientation','status':'PASS','KL_transcript':mp.nstr(Dt,25),'E0_N':str(EN0),'E1_N':str(EN1),'wrong_E1_orientation_rejected':True})

result={'status':'PASS','independent':True,'author_code_imported':False,'working_decimal_digits':mp.mp.dps,'control_groups':len(rows),'controls':rows,'limits':'Deterministic arithmetic diagnostics supplement the written proof; no empirical simulation, certified intervals, kernel verification, optimality, historical-floor verification, integration, or closure.'}
(BASE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','control_groups':len(rows),'geometry_cases':len(geo),'height_moment_cases':len(hm),'record_moment_cases':len(rm),'likelihood_cases':len(like),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
