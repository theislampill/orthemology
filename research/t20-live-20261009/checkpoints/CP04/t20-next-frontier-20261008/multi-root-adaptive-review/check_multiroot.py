#!/usr/bin/env python3
"""Independent exact-rational controls; finite controls are not a universal proof."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
counts = {}

def prod(xs):
    out = F(1)
    for x in xs: out *= x
    return out

def const(r,k):
    return F(2,k*(k+3))*F(4,(k+1)**2)*F(4,(k+2)**2)**(r-2)

def law(r,k,profile,a,extra):
    # Construct each route separately, rather than invoking the asserted q formula.
    route_supports = [(i,) for i in range(r) for _ in range(k)]
    if extra: route_supports.append(tuple(range(r)))
    return prod(1-prod(a[i] for i in route) for route in route_supports if all(i in profile for i in route))

def qpair(r,k,a):
    q0=prod((1-x)**k for x in a)
    return q0,q0*(1-prod(a))

def chi(p,q):
    if p==q: return F(0)
    assert 0<q<1
    return (p-q)**2/(q*(1-q))

@lru_cache(None)
def log_interval(x,terms=12):
    """Natural-log enclosure using exact powers-of-two reduction and atanh."""
    assert x>0
    if x==1: return F(0),F(0)
    exponent=0
    while x<1: x*=2; exponent-=1
    while x>=2: x/=2; exponent+=1
    def core(z):
        t=(z-1)/(z+1)
        partial=2*sum((t**(2*j+1)/F(2*j+1) for j in range(terms)), F(0))
        tail=2*t**(2*terms+1)/(F(2*terms+1)*(1-t*t))
        return partial,partial+tail
    lo,hi=core(x)
    l2,u2=core(F(2))
    if exponent>=0: return lo+exponent*l2,hi+exponent*u2
    return lo+exponent*u2,hi+exponent*l2

def kl_interval(p,q,terms=12):
    if p==q: return F(0),F(0)
    lo=hi=F(0)
    for mass,other in ((p,q),(1-p,1-q)):
        if not mass: continue
        assert other>0
        l,h=log_interval(mass/other,terms)
        lo+=mass*l; hi+=mass*h
    return lo,hi

# Total route bound, dimensional scaling, and exact reciprocal constant.
n=0
for r in range(2,13):
    for L in range(r+1,r+202):
        k=(L-1)//r
        assert 1<=k and r*k+1<=L
        assert F(k)>=F(L,4*r)
        assert 1/const(r,k)==F(k*(k+3)*(k+1)**2*(k+2)**(2*r-4),2*4**(r-1))
        assert 1/const(r,k)>=F(k**(2*r),2*4**(r-1))
        n+=1
counts['count_budget_scaling_cases']=n

# Independently constructed route-product laws, all profiles, rates, and corners.
n=proper=boundary=0
for r in range(2,5):
    for k in range(1,5):
        for a in product((F(0),F(1,3),F(2,3),F(1)),repeat=r):
            full0,full1=qpair(r,k,a)
            for bits in product((0,1),repeat=r):
                S={i for i,b in enumerate(bits) if b}
                p,q=law(r,k,S,a,False),law(r,k,S,a,True)
                if len(S)==r:
                    assert (p,q)==(full0,full1)
                    if any(x in (0,1) for x in a):
                        assert p==q; boundary+=1
                else: assert p==q; proper+=1
                n+=1
counts.update(route_profile_cases=n,proper_profile_equalities=proper,boundary_full_profile_equalities=boundary)

# Exact rational form of each inequality; no logarithms or floating optimization.
n=0; max_ratio=F(0); max_case=None
for r in range(2,6):
    rates=tuple(F(j,8) for j in range(1,8)) if r<=3 else (F(1,8),F(1,3),F(2,3),F(7,8))
    for k in range(1,17):
        C=const(r,k)
        for a in product(rates,repeat=r):
            u=tuple(1-x for x in a)
            q0,q1=qpair(r,k,a); z=prod(a)
            assert 1-z>=u[1]
            assert 1-q1>=1-u[0]**k
            assert 1-u[0]**k==a[0]*sum((u[0]**j for j in range(k)),F(0))
            upper=chi(q0,q1)
            assert upper==q0*z*z/((1-z)*(1-q1))
            f1=u[0]**k*a[0]/sum((u[0]**j for j in range(k)),F(0))
            f2=u[1]**(k-1)*a[1]**2
            tail=prod(u[i]**k*a[i]**2 for i in range(2,r))
            assert upper<=f1*f2*tail
            assert f1<=F(2,k*(k+3))
            assert f2<=F(4,(k+1)**2)
            for i in range(2,r): assert u[i]**k*a[i]**2<=F(4,(k+2)**2)
            assert upper<=C
            ratio=upper/C
            if ratio>max_ratio: max_ratio=ratio; max_case=(r,k,[str(x) for x in a])
            n+=1
counts['interior_inequality_chains']=n
counts['largest_exact_chi_to_C_ratio']={'value':str(max_ratio),'parameters_r_k_rates':max_case}

# Independent certified natural-log enclosures directly check KL <= chi <= C.
n=0; refinements=[]
for r in range(2,5):
    for k in range(1,7):
        for a in product((F(1,4),F(1,2),F(3,4)),repeat=r):
            q0,q1=qpair(r,k,a)
            lo,hi=kl_interval(q0,q1)
            if hi>chi(q0,q1):
                refinements.append([r,k,[str(x) for x in a]])
                lo,hi=kl_interval(q0,q1,32)
            assert hi<=chi(q0,q1)<=const(r,k), (r,k,a)
            n+=1
counts['certified_log_KL_cases']=n
counts['log_certificate_refinements_to_32_terms']=refinements

# Exact branching transcripts for a randomized, history-dependent action policy.
def actions(history,r):
    s=sum(history)
    if not history:
        return [(F(1,3),tuple(F(1,4) for _ in range(r)),set(range(r))),
                (F(2,3),tuple(F(3,4) for _ in range(r)),set(range(r)))]
    a=tuple(F(1+((s+i+len(history))%3),4) for i in range(r))
    b=tuple(F(3-((s+i)%3),4) for i in range(r))
    # The second branch is a proper issued profile at alternating histories.
    S=set(range(r)) if s%2 else set(range(r-1))
    return [(F(2,5),a,set(range(r))),(F(3,5),b,S)]

def adaptive_control(r,k,N):
    leaves=[]; conditional_lo=conditional_hi=F(0)
    def walk(history,p0,p1,depth):
        nonlocal conditional_lo,conditional_hi
        if depth==N: leaves.append((p0,p1)); return
        for weight,a,S in actions(history,r):
            q0,q1=law(r,k,S,a,False),law(r,k,S,a,True)
            lo,hi=kl_interval(q0,q1)
            conditional_lo+=p0*weight*lo
            conditional_hi+=p0*weight*hi
            for y,t0,t1 in ((0,q0,q1),(1,1-q0,1-q1)):
                if t0: walk(history+(y,),p0*weight*t0,p1*weight*t1,depth+1)
    walk((),F(1),F(1),0)
    assert sum((p for p,q in leaves),F(0))==sum((q for p,q in leaves),F(0))==1
    direct_lo=direct_hi=F(0)
    for p,q in leaves:
        lo,hi=log_interval(p/q)
        direct_lo+=p*lo; direct_hi+=p*hi
    assert max(direct_lo,conditional_lo)<=min(direct_hi,conditional_hi)
    assert direct_hi<=N*const(r,k) and conditional_hi<=N*const(r,k)
    return len(leaves)
counts['adaptive_transcript_leaf_counts']={f'r{r}_k{k}_N{N}':adaptive_control(r,k,N) for r,k,N in ((2,1,3),(2,3,3),(3,1,2),(3,2,3))}

# Negative controls expose invalid enlargements rather than weakening the theorem.
# If only root 1 carries k baseline routes, setting its success to 1/(k+1)
# and every other success to one removes the multi-root k^(−2r) obstruction.
r=3;k=20;a1=F(1,k+1);q0=(1-a1)**k;q1=q0*(1-a1)
lo,hi=kl_interval(q0,q1)
assert lo>F(1,2000)>const(r,k)
counts['negative_control_uncovered_roots']={'r':r,'k':k,'certified_KL_lower_exceeds':'1/2000','claimed_multiroot_C':str(const(r,k)),'result':'An unbalanced baseline does not prove the proposed uniform multi-root inequality.'}
# Route-addressable gating, excluded from the menu, would give deterministic
# absence under H0 and deterministic presence under H1 in one trial.
route_specific_baseline_successes=[F(0)]*6
route_specific_added_success=F(1)
addressed_q0=prod(1-p for p in route_specific_baseline_successes)
addressed_q1=addressed_q0*(1-route_specific_added_success)
assert (addressed_q0,addressed_q1)==(F(1),F(0))
counts['negative_control_route_addressable_gating']='Baseline suppressed, added route enabled: q0=1, q1=0, so one endpoint distinguishes the hard pair. This action is excluded.'
# A single reused random gate per root changes duplicate-route dependence.
shared_q0=shared_q1=F(0)
for root_gates in product((0,1),repeat=2):
    probability=F(1,4)
    baseline_emits=any(root_gates)
    extra_emits=all(root_gates)
    if not baseline_emits: shared_q0+=probability
    if not (baseline_emits or extra_emits): shared_q1+=probability
assert (shared_q0,shared_q1)==(F(1,4),F(1,4))
assert qpair(2,2,(F(1,2),F(1,2)))==(F(1,16),F(3,64))
counts['negative_control_shared_random_gates']='One reused Bernoulli gate per root gives q0=q1=1/4 at r=2,k=2,a=(1/2,1/2); independent-route laws give 1/16 and 3/64.'
# Exact parameter sequences rule out an unjustified positive variance floor.
for j in (10,100,1000):
    q0,q1=qpair(2,2,(F(1,j),F(1,j)))
    assert q1*(1-q1)<=F(4,j)+F(1,j*j)
    q0,q1=qpair(2,2,(1-F(1,j),F(1,2)))
    assert q1*(1-q1)<=F(1,j*j)
counts['negative_control_variance_floor']='Exact near-zero and near-one rate sequences have variance bounded by quantities tending to zero; there is no uniform positive variance floor.'
# The binary-testing KL confidence factor vanishes as delta approaches 1/2.
for j in (10,100,1000):
    delta=F(j-1,2*j)
    lo,hi=kl_interval(1-delta,delta)
    loglo,_=log_interval(1/delta)
    assert hi/loglo<F(10,j*j)
counts['negative_control_confidence_half']='Certified ratios kl(1-delta,delta)/log(1/delta) < 10/j^2 at delta=(j-1)/(2j), j=10,100,1000.'

# Upper menu count and epsilon/sample-coefficient identity are exact.
n=0
for r in range(2,9):
    explicit=sum(2**sum(bits)-1 for bits in product((0,1),repeat=r))
    assert explicit==3**r-2**r
    for L in range(r+1,r+22):
        p=F(1,2*L);eps=p**r/(16*2**r)
        assert 1/(2*eps*eps)==128*(16*L*L)**r
        n+=1
counts['upper_menu_and_budget_checks']=n

out={'status':'PASS','arithmetic':'fractions.Fraction throughout; logarithms enclosed by exact rational series after powers-of-two range reduction','controls':counts,'limitations':['Finite controls supplement the written analytic proof; they do not replace it.','No physical, calibration, independence, or model-validity test was performed.','No unbounded-dimension, mixture-upper, route-addressable, expected-stopping-time, or integration claim.']}
(HERE/'results').mkdir(exist_ok=True)
(HERE/'results'/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
