"""Deterministic 90-digit model checks, not simulations or certified intervals."""
import json
import mpmath as mp
mp.mp.dps=90

def evaluate(m, xs, ys):
    m=mp.mpf(m); e=1/m; c=1-e; k=len(xs)
    xx=list(xs)+[mp.mpf(1)]
    U=xs[0]+sum((xx[i+1]-xx[i])*ys[i] for i in range(k))
    M1=(xs[0]**2+sum((xx[i+1]**2-xx[i]**2)*ys[i]**2 for i in range(k)))/4
    D0=1-U
    Dc=sum((1-xx[i])**c-(1-xx[i+1])**c+(1-xx[i+1]*ys[i])**c-(1-xx[i]*ys[i])**c for i in range(k))
    logf=lambda t: mp.log(c)-e*mp.log1p(-t)+mp.log1p(e*t/(1-t))
    exact=mp.log(m/(m-k))+sum(logf(x*y) for x,y in zip(xs,ys))+(m-k)*mp.log(Dc)-(m-1-k)*mp.log(D0)
    candidate=((k-m*U)**2-k)/(2*m*m)+2*(sum(x*y for x,y in zip(xs,ys))/m-M1)
    bound=40*(k/m+U)**3
    admissible=U<=mp.mpf('.5') and k/m<=mp.mpf('.5')
    if admissible: assert abs(exact-candidate)<=bound
    return dict(m=int(m),k=k,U=str(U),M1=str(M1),exact=str(exact),candidate=str(candidate),error=str(exact-candidate),bound=str(bound),error_over_bound=str(abs(exact-candidate)/bound),admissible=bool(admissible))
rows=[]
for m in [16,64,256,1024,4096,16384]:
    k=int(mp.ceil(mp.log(m)))
    xs=[mp.exp(mp.log(mp.mpf(1)/m)+i*mp.log(mp.mpf('.8')*m)/(k-1)) for i in range(k)]
    ys=[1/(2*m*x) for x in xs]
    rows.append(evaluate(m,xs,ys))
for m in [2,4,16,128]:
    rows.append(evaluate(m,[mp.mpf('.125')],[mp.mpf('.125')]))
boundary=[]
for exponent in [4,16,64]:
    eta=mp.mpf(10)**(-exponent)
    boundary.append(evaluate(8,[1-eta],[mp.mpf('.5')]))
# Exact integration controls for expected U and M1, using 1D product formula.
means=[]
for m in [2,4,16,64]:
    eu=mp.quad(lambda t: -mp.log(t)*(1-t)**(m-1),[0,1])
    em1=mp.quad(lambda t: -t*mp.log(t)*(1-t)**(m-1),[0,1])
    target_u=mp.harmonic(m)/m
    target_m1=(mp.harmonic(m+1)-1)/(m*(m+1))
    assert abs(eu-target_u)<mp.mpf('1e-80')
    assert abs(em1-target_m1)<mp.mpf('1e-80')
    means.append(dict(m=m,U_error=str(eu-target_u),M1_error=str(em1-target_m1)))
with open('CONTROL_RESULTS.json','w') as f:
    json.dump(dict(precision_digits=mp.mp.dps,kind='deterministic model arithmetic; not simulation or certified intervals',admissible_and_comparison_cases=rows,boundary_counterexample=boundary,first_moment_integral_checks=means),f,indent=2)
print('PASS: deterministic expansion checks, boundary examples, first-moment identities')
