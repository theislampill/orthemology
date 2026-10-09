"""Deterministic arithmetic/quadrature controls; no random/empirical sampling."""
from fractions import Fraction as Q
from math import comb
from itertools import product
import json
import mpmath as mp
mp.mp.dps=65
H=lambda n: sum((Q(1,k) for k in range(1,n+1)),Q(0))
H2=lambda n: sum((Q(1,k*k) for k in range(1,n+1)),Q(0))
def exact(n):
    c=Q(n,n+1)
    # Expand the polynomial in the actual product-integral formula.
    val=n*sum(((-1)**j*comb(n-2,j)*(Q(1,(j+1)**2)-c*Q(1,(j+2)**2)) for j in range(n-1)),Q(0))
    delta=(H(n)-1)/Q(n*n-1)
    assert val==H(n)+delta
    assert 0<delta<Q(1,n+1)
    W=H(n+1)-H2(n+1)+H(n+1)**2-val**2
    assert W>=0 and W<=H(n+1)-H2(n+1)+2*H(n)/Q(n+1)+Q(1,(n+1)**2)
    return {"n":n,"mean":str(val),"gap":str(delta),"variance_upper":str(W)}
exact_rows=[exact(n) for n in range(2,65)]
quad=[]
for n in [1,2,3,5,10,30,100]:
    c=mp.mpf(n)/(n+1)
    f=lambda z: n*(-mp.log(z))*(1-z)**(n-2)*(1-c*z)
    observed=mp.quad(f,[0,mp.mpf('.5'),mp.mpf('.9'),1])
    hn=mp.fsum(mp.mpf(1)/j for j in range(1,n+1))
    delta=(mp.zeta(2)-1)/2 if n==1 else (hn-1)/(n*n-1)
    error=abs(observed-hn-delta)
    assert error<mp.mpf('1e-55')
    quad.append({"n":n,"mean":mp.nstr(observed,45),"absolute_residual":mp.nstr(error,6)})
norm=[]
for c in [mp.mpf('.5'),mp.mpf('.75'),mp.mpf('.9')]:
    obs=mp.quad(lambda z: (-mp.log(z))*c*(1-z)**(c-2)*(1-c*z),[0,mp.mpf('.5'),mp.mpf('.9'),1])
    assert abs(obs-1)<mp.mpf('1e-25')
    norm.append({"c":str(c),"normalization":mp.nstr(obs,45)})
# Deterministic finite-grid quantile coupling. No random draws.
xs=[mp.mpf(k)/5 for k in range(1,5)]
us=[mp.mpf(k)/6 for k in range(1,6)]
coupling_checks=0
for c in [mp.mpf('.5'),mp.mpf('.75'),mp.mpf('.9')]:
    def inverse(x,u):
        lo,hi=mp.mpf(0),mp.mpf(1)
        for _ in range(160):
            y=(lo+hi)/2
            g=y*((1-x*y)/(1-x))**(c-1)
            if g<u: lo=y
            else: hi=y
        return (lo+hi)/2
    qs=[[inverse(x,u) for u in us] for x in xs]
    for j in range(3):
        assert all(qs[j][a]<=qs[j+1][a] for a in range(len(us)))
    for inds in product(range(len(us)),repeat=4):
        U=[us[a] for a in inds]
        Y=[qs[i][a] for i,a in enumerate(inds)]
        for i in range(1,4):
            assert not all(Y[i]<Y[j] for j in range(i)) or all(U[i]<U[j] for j in range(i))
        coupling_checks+=1
n1delta=(mp.zeta(2)-1)/2
# Falsified controls are deliberately different formula candidates.
wrong={"zero_gap_rejected_n2":exact_rows[0]['gap']!='0',
       "gap_one_over_n_squared_rejected_n2":Q(exact_rows[0]['gap'])!=Q(1,4),
       "n1_gap_wrongly_zero_rejected":n1delta>0,
       "Joe_mean_equal_uniform_m_rejected_n2":Q(exact_rows[0]['mean'])!=H(3)}
assert all(wrong.values())
out={"status":"all deterministic controls passed", "not_empirical":True,
     "exact_polynomial_integral_rows":exact_rows,"quadrature":quad,"density_normalization":norm,
     "quantile_record_grid_configurations":coupling_checks,"wrong_candidate_controls":wrong,
     "n1_exact_variance_decimal":mp.nstr(n1delta*(1-n1delta),45)}
with open('CONTROL_RESULTS.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps({k:v for k,v in out.items() if k not in ['exact_polynomial_integral_rows']},indent=2))
