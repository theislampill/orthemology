"""Independent deterministic checks; no author-code imports or random samples.
The mathematical proof is in REVIEW.md. Decimal checks are not interval proofs.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import mpmath as mp
mp.mp.dps = 110
OUT = Path(__file__).resolve().parent
ROOT = OUT.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def asmp(q):
    return mp.mpf(q.numerator) / q.denominator if isinstance(q,F) else mp.mpf(q)

def moments(xs, ys, r):
    x = [F(0)] + xs + [F(1)]
    h = [F(1)] + ys
    return sum((x[i+1]**(r+1)-x[i]**(r+1))*h[i]**(r+1)/(r+1)**2 for i in range(len(h)))

def check(m, xs, ys, name):
    k = len(xs)
    assert 1 <= k <= m-1
    assert all(0 < x < 1 for x in xs) and all(0 < y < 1 for y in ys)
    assert all(xs[i] < xs[i+1] and ys[i] > ys[i+1] for i in range(k-1))
    u = moments(xs,ys,0)
    assert max(x*y for x,y in zip(xs,ys)) <= u
    for r in range(1,5):
        assert moments(xs,ys,r) <= u**(r+1)/(r+1)**2
    w = moments(xs,ys,1)
    x, y = list(map(asmp,xs)), list(map(asmp,ys))
    u, w, e = asmp(u), asmp(w), 1/mp.mpf(m)
    c, a = 1-e, k*e
    xx = x+[mp.mpf(1)]
    dc = mp.fsum((1-xx[i])**c-(1-xx[i+1])**c+(1-xx[i+1]*y[i])**c-(1-xx[i]*y[i])**c for i in range(k))
    d0 = 1-u
    # Direct predecessor density; do not use the author's log-g factorization.
    logf = mp.fsum(mp.log(c)+(c-2)*mp.log1p(-x[i]*y[i])+mp.log1p(-c*x[i]*y[i]) for i in range(k))
    exact = mp.log(mp.mpf(m)/(m-k))+logf+(m-k)*mp.log(dc)-(m-1-k)*mp.log(d0)
    lead = ((k-m*u)**2-k)/(2*mp.mpf(m)**2)+2*(e*mp.fsum(xi*yi for xi,yi in zip(x,y))-w)
    error = exact-lead
    admissible = (2*k <= m and u <= mp.mpf('.5'))
    if admissible:
        envelope = mp.mpf(2)/3*a**3+7*a*u**2+mp.mpf(43)/9*u**3
        assert abs(error) <= envelope+mp.mpf('1e-95')
        assert envelope <= 5*(a+u)**3+mp.mpf('1e-95')
        assert abs(error) <= 40*(a+u)**3
        # Check the independent proof's exact B and nonnegative log ratio.
        B = (dc-d0)/e
        assert -mp.mpf('1e-95') <= B <= u+mp.mpf('1e-95')
        assert B >= mp.mpf(11)/18*u-mp.mpf('1e-95')
    return dict(name=name,m=m,k=k,U=str(u),exact_log_likelihood=str(exact),leading_score=str(lead),error=str(error),admissible=bool(admissible),error_over_cube=str(abs(error)/(a+u)**3))

rows=[]
for m in [2,3,4,8,16,64,256,4096]:
    ks=sorted(set(k for k in [1,2,3,8,m//2] if k <= min(m//2,128)))
    for k in ks:
        for xmin in [F(1,10**12),F(1,100*m),F(1,10),F(49,100)]:
            xs=[xmin] if k==1 else [xmin+(F(99,100)-xmin)*F(i,k-1) for i in range(k)]
            for end in [F(1,50),F(1,4),F(9,10)]:
                base=[F(1)] if k==1 else [1-(1-end)*F(i,k-1) for i in range(k)]
                for scale in [F(1,100),F(1,2),F(99,100)]:
                    ys=[scale*v for v in base]
                    if moments(xs,ys,0) <= F(1,2):
                        rows.append(check(m,xs,ys,f'grid_m{m}_k{k}_x{xmin}_r{end}_s{scale}'))
    # Exact U=1/2, including a=k/m=1/2 when m is even and reasonably small.
    for k in sorted(set([1,min(m//2,128)])):
        xmin=F(1,100*m)
        xs=[xmin] if k==1 else [xmin+(F(99,100)-xmin)*F(i,k-1) for i in range(k)]
        base=[F(1)] if k==1 else [1-F(i,10*(k-1)) for i in range(k)]
        beta=(F(1,2)-xmin)/(moments(xs,base,0)-xmin)
        rows.append(check(m,xs,[beta*v for v in base],f'exact_U_half_m{m}_k{k}'))
# Tiny and near-window-boundary single point configurations.
for xmin in [F(1,10**40),F(1,100),F(1,4),F(499999999,10**9)]:
    for m in [2,4,64]:
        y=(F(1,2)-xmin)/(1-xmin)
        rows.append(check(m,[xmin],[y],f'single_U_half_{m}_{xmin}'))

# Independent mass-integral versus exact strip checks on selected admissible cases.
quad=[]
for m,xs,ys in [
    (2,[F(1,10)],[F(4,9)]),
    (8,[F(1,100),F(1,5),F(3,4)],[F(2,5),F(1,5),F(1,50)]),
    (64,[F(1,10000),F(1,100),F(1,5),F(9,10)],[F(4,5),F(1,5),F(1,50),F(1,1000)])]:
    e=1/mp.mpf(m); c=1-e
    x=[mp.mpf(0)]+list(map(asmp,xs))+[mp.mpf(1)]
    h=[mp.mpf(1)]+list(map(asmp,ys))
    q=mp.fsum(mp.quad(lambda z: c*h[i]*(1-z*h[i])**(c-1),[x[i],x[i+1]]) for i in range(len(h)))
    xx=x[1:]; yy=h[1:]
    dc=mp.fsum((1-xx[i])**c-(1-xx[i+1])**c+(1-xx[i+1]*yy[i])**c-(1-xx[i]*yy[i])**c for i in range(len(ys)))
    err=abs((1-q)-dc)
    assert err<mp.mpf('1e-95')
    quad.append(dict(m=m,k=len(ys),mass_comparison_error=str(err)))

# The scalar density remainder bound includes both end points.
density=[]
for e in [mp.mpf('1e-10'),mp.mpf(1)/4096,mp.mpf('.1'),mp.mpf('.25'),mp.mpf('.5')]:
    for t in [mp.mpf('1e-30'),mp.mpf('.001'),mp.mpf('.25'),mp.mpf('.5')]:
        g=(1-t)**(-e)*(1+e*t/(1-t))
        normalized=(g-1-2*e*t)/(e*t*t)
        assert normalized>=-mp.mpf('1e-35') and normalized<5
        density.append(dict(e=str(e),t=str(t),remainder_over_e_t2=str(normalized)))

boundary=[]
for exponent in [4,16,64]:
    row=check(8,[1-F(1,10**exponent)],[F(1,2)],f'boundary_10^-{exponent}')
    assert not row['admissible']
    row['boundary_exponent']=exponent
    row['log_likelihood_minus_log_eta_over_m']=str(mp.mpf(row['exact_log_likelihood'])+mp.mpf(exponent)*mp.log(10)/8)
    boundary.append(row)
assert all(mp.mpf(boundary[i+1]['exact_log_likelihood'])<mp.mpf(boundary[i]['exact_log_likelihood']) for i in range(2))

# Exact fixed-sample-size expectation integrals, separately for both worlds.
first=[]
for m in [2,3,4,16,64]:
    eu=mp.quad(lambda t: -mp.log(t)*(1-t)**(m-1),[0,1])
    ew=mp.quad(lambda t: -t*mp.log(t)*(1-t)**(m-1),[0,1])
    hu=mp.harmonic(m)/m
    hw=(mp.harmonic(m+1)-1)/(mp.mpf(m)*(m+1))
    assert abs(eu-hu)<mp.mpf('1e-95') and abs(ew-hw)<mp.mpf('1e-95')
    n=m-1
    ek0=mp.harmonic(n)
    ek1=(1+mp.zeta(2))/2 if n==1 else ek0+(ek0-1)/(n*n-1)
    assert ek0<=mp.harmonic(m) and ek1<=mp.harmonic(m)
    first.append(dict(m=m,U_error=str(eu-hu),M1_error=str(ew-hw),E0_K=str(ek0),E1_K=str(ek1),H_m=str(mp.harmonic(m))))

# Wrong-sign/coefficient controls that the localized bound must reject.
negative=[]
m=2**20
for kind,xs,ys in [
    ('omit_minus_k', [F(1,m)], [F(1,m)]),
    ('reverse_M1_sign', [F(1,m)], [F(1,m)]),
    ('reverse_boundary_sum_sign', [F(2**i,m) for i in range(20)], [F(1,2**(i+1)) for i in range(20)])]:
    row=check(m,xs,ys,kind)
    k=len(xs); u=asmp(moments(xs,ys,0)); a=mp.mpf(k)/m
    if kind=='omit_minus_k': shift=mp.mpf(k)/(2*mp.mpf(m)**2)
    elif kind=='reverse_M1_sign': shift=4*asmp(moments(xs,ys,1))
    else: shift=-4*asmp(sum(x*y for x,y in zip(xs,ys)))/m
    bad_ratio=abs(mp.mpf(row['error'])-shift)/(a+u)**3
    assert bad_ratio>40
    negative.append(dict(mutation=kind,m=m,k=k,incorrect_error_over_cube=str(bad_ratio),rejected_by_constant_40=True))

worst=max(rows,key=lambda r:mp.mpf(r['error_over_cube']))
result=dict(status='PASS',precision_digits=mp.mp.dps,scope='Deterministic arithmetic and exact rational geometry; not simulations, empirical evidence, kernel proofs, or certified numeric intervals.',admissible_case_count=len(rows),maximum_error_over_cube=worst,case_rows=rows,mass_quadrature_crosschecks=quad,density_remainder_checks=density,boundary_counterexample=boundary,first_moment_checks=first,wrong_candidate_controls=negative)
(OUT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],admissible_case_count=len(rows),maximum_error_over_cube=worst['error_over_cube'],worst_case=worst['name'],boundary_log_likelihoods=[r['exact_log_likelihood'] for r in boundary]),indent=2))
