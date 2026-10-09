#!/usr/bin/env python3
"""Independent finite controls for the digest-bound calibration review.
No author files are modified. These controls do not replace the general proof.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parent
AUTHOR = ROOT.parent / 'global-calibration-ambiguity'
EXPECTED = {
    'RESULT.md': 'ec620e491fd1c58cdc9dc0bcc8700784b79b4b399247ca1e2a235438138cf827',
    'exact_controls.py': '867de73098d4eb210ef4fbbf5758c728efeb4dbe46982bd80941630fed00a2d2',
    'results/exact_controls.json': '1115ba405c6e115f15cc0b7c748a307e2335f2cb4d106cd6a03bf502aab8e596',
}
counts = Counter()
def require(test, family):
    if not test:
        raise AssertionError(family)
    counts[family] += 1

for name, digest in EXPECTED.items():
    require(sha256((AUTHOR/name).read_bytes()).hexdigest() == digest, 'author_digest_match')
replayed = ROOT/'replayed_author_controls/results/exact_controls.json'
require(replayed.read_bytes() == (AUTHOR/'results/exact_controls.json').read_bytes(), 'author_replay_byte_identity')

rng = random.Random(20261008)
ks = list(range(1, 41)) + [64, 127]
for k in ks:
    b = Q(k, k+1)
    t, s = b**(k+1), b**k
    critical = (s-t)/2
    m = (t+s)/2
    require(critical == b**k / (2*(k+1)), 'critical_formula')
    points = {Q(0), Q(1), b, Q(1,10000), Q(9999,10000)}
    points.update(Q(rng.randrange(1,d),d) for d in [17,23,47,89] for _ in range(5))
    for u in points:
        survival_k, survival_next = u**(k+1), u**k
        x = 1-(survival_k+survival_next)/2
        rk, rn = 1-survival_k, 1-survival_next
        require(survival_k**k == survival_next**(k+1), 'independent_rational_curve_identity')
        require(0 <= x <= 1 and 0 <= rk <= 1 and 0 <= rn <= 1, 'independent_rational_domain')
        require(abs(rk-x) == abs(rn-x) <= critical, 'independent_rational_band')
        for lam in [Q(0),Q(2,7),Q(17,19),Q(999,1000),Q(1)]:
            pk=(1-((1-lam)*x+lam*rk))**k
            pn=(1-((1-lam)*x+lam*rn))**(k+1)
            require(0 <= pk-pn <= (2*k+1)*(1-lam)*critical, 'independent_interpolation_bound')
    for ratio in [Q(0),Q(2,7),Q(17,19),Q(999,1000)]:
        eta=ratio*critical
        lo,hi=m-eta,m+eta
        require(0<t<lo<=hi<s<1, 'independent_no_clipping')
        gaps=[lo**j-hi**(j+1) for j in range(k+1)]
        require(all(v>0 for v in gaps), 'independent_catalogue_separation')
        require(all(gaps[j+1]<gaps[j] for j in range(k)), 'independent_gap_order')
        thresholds=[(lo**j+hi**(j+1))/2 for j in range(k+1)]
        require(all(thresholds[j+1]<thresholds[j] for j in range(k)), 'independent_threshold_order')
        for j in range(k+2):
            if j>0:
                require(thresholds[j-1]-hi**j>=gaps[-1]/2, 'independent_decoder_upper_margin')
            if j<k+1:
                require(lo**j-thresholds[j]>=gaps[-1]/2, 'independent_decoder_lower_margin')
    require((m-critical)**k == (m+critical)**(k+1), 'independent_boundary_touch')
    require((m-Q(3,2)*critical)**k < (m+Q(3,2)*critical)**(k+1), 'independent_postboundary_overlap')

# Invert from specified nominal commands, rather than selecting parameter u first.
with localcontext() as ctx:
    ctx.prec=110
    tol=Decimal('1e-90')
    for k in [1,2,7,17,64]:
        b=Decimal(k)/Decimal(k+1)
        eta_star=b**k/(2*Decimal(k+1))
        previous=None
        for xs in ['0','.001','.01','.1','.37','.63','.9','.99','.999','1']:
            x=Decimal(xs)
            if x==0:
                u=Decimal(1)
            elif x==1:
                u=Decimal(0)
            else:
                lower,upper=Decimal(0),Decimal(1)
                for _ in range(400):
                    middle=(lower+upper)/2
                    at=1-(middle**k+middle**(k+1))/2
                    if at>x:
                        lower=middle
                    else:
                        upper=middle
                u=(lower+upper)/2
            rk=1-u**(k+1); rn=1-u**k
            require(abs(1-(u**k+u**(k+1))/2-x)<tol, 'nominal_command_inverse_residual')
            require(abs(rk-x)<=eta_star+tol and abs(rn-x)<=eta_star+tol, 'nominal_command_calibration_band')
            pk=(1-rk)**k; pn=(1-rn)**(k+1)
            require(abs(pk-pn)<=tol*max(Decimal(1),abs(pk),abs(pn)), 'nominal_command_curve_equality')
            if previous is not None:
                require(rk>previous[0] and rn>previous[1], 'nominal_command_strict_monotonicity')
            previous=(rk,rn)

# A different randomized, history-dependent, early-stopping protocol.
# Full retained key is (seed, outcome history); commands are determined by that key.
def stopped_law(k,lam,which,max_trials):
    leaves={}
    def visit(seed,history,mass):
        if len(history)==max_trials or (len(history)>=2 and history[-2:]==(1,1)):
            leaves[(seed,history)]=mass
            return
        code=seed+3*len(history)+sum((i+2)*bit for i,bit in enumerate(history))
        u=Q(1+code%11,13)
        a=u**(k+1); b=u**k
        command_survival=(a+b)/2
        actual_survival=(1-lam)*command_survival+lam*(a if which==0 else b)
        p=actual_survival**(k+which)
        visit(seed,history+(0,),mass*(1-p))
        visit(seed,history+(1,),mass*p)
    for seed,weight in [(0,Q(1,3)),(1,Q(2,3))]:
        visit(seed,(),weight)
    return leaves

for k in [1,2,4,7]:
    critical=Q(k,k+1)**k/(2*(k+1))
    for depth in [2,4,6]:
        P=stopped_law(k,Q(1),0,depth)
        R=stopped_law(k,Q(1),1,depth)
        require(P==R, 'randomized_stopped_transcript_identity')
        require(sum(P.values())==1, 'randomized_stopped_normalization')
        require(any(len(h)<depth for _,h in P) if depth>2 else True, 'early_stopping_exercised')
        for lam in [Q(2,7),Q(17,19),Q(999,1000)]:
            P=stopped_law(k,lam,0,depth)
            R=stopped_law(k,lam,1,depth)
            tv=sum(abs(P[h]-R[h]) for h in P)/2
            require(tv<=min(1,depth*(2*k+1)*(1-lam)*critical), 'randomized_stopped_tv_bound')

for name,digest in EXPECTED.items():
    require(sha256((AUTHOR/name).read_bytes()).hexdigest()==digest, 'author_digest_unchanged_after_controls')
result={
 'status':'passed',
 'arithmetic':'Exact fractions, plus 110-digit Decimal command inversion; no observation simulation.',
 'seed':20261008,
 'scope':'Finite independent diagnostics only; the universal claims rely on the separately reviewed mathematical proofs.',
 'reviewed_author_hashes':EXPECTED,
 'families':dict(sorted(counts.items())),
 'total_assertions':sum(counts.values()),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
}
(ROOT/'independent_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
