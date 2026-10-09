#!/usr/bin/env python3
"""Independent finite exact controls for the separately reviewed efficiency appendix."""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'global-calibration-ambiguity'
EXPECTED={
 'RESULT.md':'ec620e491fd1c58cdc9dc0bcc8700784b79b4b399247ca1e2a235438138cf827',
 'POLYNOMIAL_EFFICIENCY_APPENDIX.md':'4242d8cbcc9fd576266e2ee01f902b45c93e6701b5c01d07a5a0c3909f97f0f4'}
counts=Counter()
def check(ok,family):
    if not ok: raise AssertionError(family)
    counts[family]+=1

def dec(q): return Decimal(q.numerator)/Decimal(q.denominator)

def clipped(k,u,eta):
    d=u**k*(1-u)/2
    x=1-(u**k+u**(k+1))/2
    clip=min(d,eta)
    rk=x+clip; rn=x-clip
    return x,d,rk,rn,(1-rk)**k,(1-rn)**(k+1)

for name,h in EXPECTED.items():
    check(sha256((AUTHOR/name).read_bytes()).hexdigest()==h,'input_digest')

with localcontext() as ctx:
    ctx.prec=110
    eps=Decimal('1e-90')
    for k in list(range(1,25))+[32,48,64]:
        b=Q(k,k+1)
        critical=b**k/(2*(k+1))
        grid=sorted(set([Q(i,19) for i in range(20)]+[b,Q(1,1000),Q(999,1000)]),reverse=True)
        for eta in [Q(0),critical/17,critical/2,critical,Q(3,2)*critical]:
            prev=None
            for u in grid:
                x,d,rk,rn,pk,pn=clipped(k,u,eta)
                check(d<=x/(2*k+1),'boundary_error_geometry')
                check(0<=rn<=x<=rk<=1,'clipped_rate_domain')
                check(abs(rk-x)<=eta and abs(rn-x)<=eta,'clipped_error_band')
                if prev is not None:
                    check(x>prev[0] and rk>prev[1] and rn>prev[2],'clipped_strict_monotonicity')
                prev=(x,rk,rn)
                if d<=eta:
                    check(pk==pn,'unmodified_region_identity')
                else:
                    check(x>(2*k+1)*eta and x+eta>2*(k+1)*eta,'modified_region_command_bound')
                    check(x-eta>=0 and x+eta<1,'modified_region_no_clipping')
                    boundary=u**(k*(k+1))
                    check(pk>=boundary>=pn,'modified_region_probability_order')
                    check(0<=pk-pn<=pk==(1-x-eta)**k,'modified_region_tv_envelope')
                    check(dec(pk-pn)<=(Decimal(-2*k*(k+1))*dec(eta)).exp()+eps,'numerical_exponential_kernel_bound')
            check(clipped(k,Q(0),eta)[2:4]==(1,1),'clipped_endpoint_one')
            check(clipped(k,Q(1),eta)[2:4]==(0,0),'clipped_endpoint_zero')

    for M in list(range(2,49))+[64,127]:
        for eta in [Q(0),Q(1,32*M*M),Q(1,16*M*M),Q(1,8*M*M),Q(1,32*M),Q(1,16*M)]:
            x=max(Q(1,M),8*M*eta)
            A=1-x-eta; B=1-x+eta
            check(Q(1,M)<=x<=Q(1,2) and eta<=x/(8*M),'sufficient_command_domain')
            check(0<A<=B<1 and B>=Q(1,2),'sufficient_survival_domain')
            g=A**(M-1)-B**M
            bracket=x-eta-2*(M-1)*eta/B
            check(g>=B**(M-1)*bracket,'bernoulli_inequality_step')
            check(bracket>=x-(4*M-3)*eta>=x/2,'bracket_constants')
            check(g>=x/2*B**(M-1)>=x/2*(1-x)**(M-1)>0,'exact_sufficient_gap')
            check(dec(g)>=dec(x)/2*(Decimal(-2*(M-1))*dec(x)).exp()-eps,'numerical_exponential_gap')
            gaps=[A**j-B**(j+1) for j in range(M)]
            check(all(z>=g>0 for z in gaps),'catalogue_final_gap_minimum')
            check(all(gaps[j+1]<gaps[j] for j in range(M-1)),'catalogue_strict_gap_order')
            lhs=-2*dec(x).ln()+4*(M-1)*dec(x)
            rhs=4+2*Decimal(M).ln()+32*M*(M-1)*dec(eta)
            check(lhs<=rhs+eps,'looser_budget_log_comparison')

    # Independently enumerate a history-adaptive protocol under the clipped maps.
    def law(k,eta,which,depth):
        states={():Q(1)}
        for n in range(depth):
            new={}
            for hist,mass in states.items():
                u=Q(1+(3*n+sum((i+1)*bit for i,bit in enumerate(hist)))%9,11)
                p=clipped(k,u,eta)[4+which]
                new[hist+(0,)]=mass*(1-p)
                new[hist+(1,)]=mass*p
            states=new
        return states
    for k in [1,3,10,20]:
        critical=Q(k,k+1)**k/(2*(k+1))
        for depth in [1,3,4]:
            for eta in [Q(0),critical/2,Q(9,10)*critical,critical]:
                P=law(k,eta,0,depth); R=law(k,eta,1,depth)
                check(sum(P.values())==sum(R.values())==1,'clipped_adaptive_law_normalization')
                tv=sum(abs(P[h]-R[h]) for h in P)/2
                bound=min(Decimal(1),depth*(Decimal(-2*k*(k+1))*dec(eta)).exp())
                check(dec(tv)<=bound+eps,'clipped_adaptive_exponential_tv_bound')
                if eta==critical: check(P==R,'clipped_boundary_adaptive_identity')

for name,h in EXPECTED.items():
    check(sha256((AUTHOR/name).read_bytes()).hexdigest()==h,'input_digest_unchanged')
result={
 'status':'passed',
 'scope':'Finite independent controls, not substitutes for the general proof; no simulated observations.',
 'arithmetic':'Exact fractions and 110-digit Decimal exponential/logarithm diagnostics.',
 'reviewed_hashes':EXPECTED,
 'families':dict(sorted(counts.items())),
 'total_assertions':sum(counts.values()),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'appendix_independent_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
