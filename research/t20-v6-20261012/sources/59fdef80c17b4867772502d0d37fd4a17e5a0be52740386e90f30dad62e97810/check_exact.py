#!/usr/bin/env python3
"""Exact author controls. Written universal proofs are in RESULT.md.
No external optimiser, random simulation, or Python assert is used.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

COUNT=0

def check(condition, label):
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError('CONTROL FAILED: '+label)

def moments(rho, n):
    return tuple(sum(w*p**j for p,w in rho) for j in range(n+1))

def valid_rho(rho):
    return all(0<=p<=1 and w>=0 for p,w in rho) and sum(w for p,w in rho)==1

def lower(t): return 12*t*t-4*t+F(4,9)
def upper(t): return -6*t*t+5*t-F(2,3)
def in_c(t,s): return F(2,9)<=t<=F(5,18) and lower(t)<=s<=upper(t)
def bary(t,s): return (6*(t-s),4-24*t+12*s,18*t-6*s-3)
def in_e(t,s): return all(x>=0 for x in bary(t,s))
VERTICES=((F(1,6),F(0)),(F(1,4),F(1,4)),(F(1,3),F(1,3)))

def word_law(t,s):
    by_k=(1-4*t+s,-F(1,2)+3*t-s,F(1,3)-2*t+s,t-s,s)
    return {w:by_k[sum(w)] for w in product((0,1),repeat=4)}

def law_from_rho(rho,n=4):
    return {word:sum(w*p**sum(word)*(1-p)**(n-sum(word)) for p,w in rho)
            for word in product((0,1),repeat=n)}

def conditional_pair(t,s):
    law=word_law(t,s)
    mass=sum(v for w,v in law.items() if w[:2]==(1,1))
    check(mass==F(1,3),'conditioning mass shared and positive')
    return {w[2:]:v/mass for w,v in law.items() if w[:2]==(1,1)}

# A policy is either ('skip',label) or ('query',report after 0, report after 1).
POLICIES=(('skip',0),('skip',1),('query',0,0),('query',0,1),('query',1,0),('query',1,1))

def direct_policy_loss(policy,t,s,c):
    out=F(0)
    for (x,y),mass in conditional_pair(t,s).items():
        query=policy[0]=='query'
        report=policy[x+1] if query else policy[1]
        out+=mass*(F(report!=y)+(c if query else 0))
    return out

def affine_policy_losses(t,s,c):
    return (3*t,1-3*t,c+3*t,c+6*(t-s),c+1-6*t+6*s,c+1-3*t)

def support_c(a,b,d):
    lo,hi=F(2,9),F(5,18)
    if d>0:
        t=max(lo,min(hi,(b+5*d)/(12*d)));s=upper(t)
    elif d<0:
        t=max(lo,min(hi,(4*d-b)/(24*d)));s=lower(t)
    else:
        t=hi if b>0 else lo;s=lower(t)
    return a+b*t+d*s,(t,s)

def boundary_rhos(u):
    """All rational u in [0,1/3] give a rational lower-boundary witness."""
    v=F(1,2)+F(1,12)/(F(1,2)-u)
    rho_l=((u,(v-F(1,2))/(v-u)),(v,(F(1,2)-u)/(v-u)))
    t=moments(rho_l,3)[3]
    z=2-6*t
    rho_u=((F(0),F(1,2)-1/(6*z)),
           (z,1/(6*z*(1-z))),
           (F(1),F(1,2)-1/(6*(1-z))))
    return rho_l,rho_u,t

def mix_rho(rho,sigma,weight):
    out={}
    for p,w in rho:out[p]=out.get(p,F(0))+weight*w
    for p,w in sigma:out[p]=out.get(p,F(0))+(1-weight)*w
    return tuple(sorted(out.items()))

def check_bodies():
    model_points=[]
    for i in range(25):
        rho_l,rho_u,t=boundary_rhos(F(i,72))
        for rho,s in [(rho_l,lower(t)),(rho_u,upper(t))]:
            check(valid_rho(rho),'boundary measure nonnegative and normalized')
            check(moments(rho,4)==(F(1),F(1,2),F(1,3),t,s),'boundary exact moments')
        check(upper(t)-lower(t)==-18*(t-F(2,9))*(t-F(5,18)),'body gap factorization')
        for j in range(9):
            rho=mix_rho(rho_l,rho_u,F(j,8));m=moments(rho,4);s=m[4]
            check(valid_rho(rho),'interior mixture valid')
            check(in_c(t,s) and in_e(t,s),'calibration body lies in exchangeable body')
            check(law_from_rho(rho)==word_law(t,s),'ordered word-law moment reconstruction')
            law=word_law(t,s)
            check(sum(law.values())==1 and min(law.values())>=0,'complete law normalized')
            for pair in combinations(range(4),2):
                check(sum(v for w,v in law.items() if w[pair[0]] and w[pair[1]])==F(1,3),'all pair moments')
            model_points.append((t,s))
    for den in [1,2,3,5,11]:
        for i in range(den+1):
            for j in range(den-i+1):
                weights=(F(i,den),F(j,den),F(den-i-j,den))
                t=sum(w*v[0] for w,v in zip(weights,VERTICES))
                s=sum(w*v[1] for w,v in zip(weights,VERTICES))
                check(bary(t,s)==weights,'triangle inverse coordinates')
                law=word_law(t,s)
                check(sum(law.values())==1 and min(law.values())>=0,'exchangeable law normalized')
                model_points.append((t,s))
    expected_heads=({0:F(1,3),3:F(2,3)}, {0:F(1,4),2:F(1,2),4:F(1,4)}, {1:F(2,3),4:F(1,3)})
    for (t,s),expected in zip(VERTICES,expected_heads):
        law=word_law(t,s)
        heads={k:sum(v for w,v in law.items() if sum(w)==k) for k in range(5)}
        check(all(heads[k]==expected.get(k,0) for k in heads),'vertex head-count representation')
    check(not in_c(*VERTICES[0]) and in_e(*VERTICES[0]),'proper model-class inclusion witness')
    return model_points

def check_support(model_points):
    cpoints=[p for p in model_points if in_c(*p)]
    for a,b,d in product((F(-2),F(-1,3),F(0),F(1,2),F(3)),repeat=3):
        best,(t,s)=support_c(a,b,d)
        check(in_c(t,s),'support maximizer feasible')
        check(best==a+b*t+d*s,'support witness attains value')
        for tt,ss in cpoints:
            check(a+b*tt+d*ss<=best,'all exact sampled measures bounded by support')
        # Independent complete quadratic certificate: after the appropriate boundary
        # substitution, the derivative sign at a clamped endpoint is correct;
        # at an interior maximizer it is zero and the quadratic coefficient is negative.
        if d:
            q2=(-6*d if d>0 else 12*d)
            q1=(b+5*d if d>0 else b-4*d)
            derivative=2*q2*t+q1
            check(q2<0,'support boundary objective strictly concave')
            check((t==F(2,9) and derivative<=0) or (t==F(5,18) and derivative>=0)
                  or (F(2,9)<t<F(5,18) and derivative==0),'global concave maximum certificate')
    # Endpoint-only kernels miss even the inherited two-trial mismatch maximum.
    mismatch=lambda p:2*p*(1-p)
    check(mismatch(F(0))==mismatch(F(1))==0 and mismatch(F(1,2))==F(1,2),'endpoint kernel failure retained')

def check_continuation_game(model_points):
    expected_pairs=({(0,0):0,(0,1):F(1,2),(1,0):F(1,2),(1,1):0},
                    {(0,0):F(1,4),(0,1):0,(1,0):0,(1,1):F(3,4)},
                    {(0,0):0,(0,1):0,(1,0):0,(1,1):1})
    for v,expected in zip(VERTICES,expected_pairs):
        check(conditional_pair(*v)==expected,'conditioned vertex law')
    for t,s in model_points:
        for c in (F(0),F(1,10),F(1,2)):
            direct=tuple(direct_policy_loss(p,t,s,c) for p in POLICIES)
            check(direct==affine_policy_losses(t,s,c),'direct path evaluation equals affine policy profile')
    rho_b=((F(0),F(1,4)),(F(2,3),F(3,4)))
    m=moments(rho_b,4)
    pair=conditional_pair(m[3],m[4])
    check(pair=={w:F(2,3)**sum(w)*F(1,3)**(2-sum(w)) for w in product((0,1),repeat=2)},'least-favourable conditioned iid law')
    check(support_c(F(1),F(-3),F(0))[0]==F(1,3),'skip attains calibration robust upper bound')
    for k in range(31):
        c=F(k,20)
        values=[affine_policy_losses(t,s,c) for t,s in VERTICES]
        check(min(max(row[i] for row in values) for i in range(6))==F(1,2),'deterministic optimum')
        expected=min(F(1,2),F(2,5)+c/5)
        if c<=F(1,2):
            primal=(F(0),F(4,5),F(0),F(0),F(1,5),F(0))
            dual=((3+4*c)/5,(2-4*c)/5,F(0))
        else:
            primal=(F(0),F(1),F(0),F(0),F(0),F(0))
            dual=(F(1),F(0),F(0))
        check(sum(primal)==sum(dual)==1 and min(primal+dual)>=0,'saddle weights valid')
        primal_values=[sum(w*x for w,x in zip(primal,row)) for row in values]
        dual_values=[sum(w*values[j][i] for j,w in enumerate(dual)) for i in range(6)]
        check(max(primal_values)==expected and min(dual_values)==expected,'exact primal-dual equality')
        check(min(affine_policy_losses(m[3],m[4],c))==F(1,3),'iid oracle lower bound on all pure continuation policies')
        if 0<c<F(1,2):
            check([i for i,v in enumerate(dual_values) if v==expected]==[1,4],'only optimal root support survives strict dual')
        if c==F(1,10):
            check(expected==F(21,50),'concrete finite-exchangeable game value')
            revealed=sum(primal[i]*max(row[i] for row in values) for i in range(6))
            check(revealed==F(31,50)>F(1,2),'revealed private plan changes contract')
            check(max(primal_values)<min(max(row[i] for row in values) for i in range(6)), 'scalar pruning destroys randomized optimum')

def check_positive_game():
    delta=F(1,10);c=F(1,10)
    # Uniform-calibration U has t=1/4 and s=1/5.
    vertices=tuple(((1-delta)*t+delta*F(1,4),(1-delta)*s+delta*F(1,5)) for t,s in VERTICES)
    values=[]
    for t,s in vertices:
        law=word_law(t,s)
        check(min(law.values())>=F(1,300),'positive complete-law margin')
        check(in_e(t,s),'positive family remains exchangeable with fixed moments')
        values.append(affine_policy_losses(t,s,c))
    primal=(F(0),F(4,5),F(0),F(0),F(1,5),F(0))
    dual=(F(164,225),F(61,225),F(0))
    pv=[sum(w*x for w,x in zip(primal,row)) for row in values]
    dv=[sum(w*values[j][i] for j,w in enumerate(dual)) for i in range(6)]
    check(max(pv)==min(dv)==F(207,500),'positive-game exact saddle')
    check([i for i,v in enumerate(dv) if v==F(207,500)]==[1,4],'positive-game unique optimal support')
    check(min(max(row[i] for row in values) for i in range(6))==F(19,40),'positive-game deterministic risk')
    rho_b=((F(0),F(1,4)),(F(2,3),F(3,4)))
    check(min(law_from_rho(rho_b).values())>0,'iid least-favourable law has full support')

# Arbitrary first and second moments: a least-favourable law for asymmetric prediction.
def least_favourable(mu,nu,a,b):
    tau=a/(a+b);q0=(mu-nu)/(1-mu);q1=nu/mu
    if q1<=tau:
        return ((F(0),1-mu*mu/nu),(nu/mu,mu*mu/nu)),'lower'
    if q0>=tau:
        mass=(1-mu)**2/(1-2*mu+nu)
        return ((q0,mass),(F(1),1-mass)),'upper'
    return ((F(0),(nu-(1+tau)*mu+tau)/tau),
            (tau,(mu-nu)/(tau*(1-tau))),
            (F(1),(nu-mu*tau)/(1-tau))),'middle'

def one_sample_risk(mu,nu,a,b):
    return min(b*(mu-nu),a*(1-2*mu+nu))+min(b*nu,a*(mu-nu))

def pure_policies(h):
    stops=(('s',0),('s',1))
    if h==0:return stops
    children=pure_policies(h-1)
    return stops+tuple(('q',u,v) for u,v in product(children,repeat=2))

def conditional_policy_risk(tree,p,a,b,c):
    if tree[0]=='s':return a*(1-p) if tree[1] else b*p
    return c+(1-p)*conditional_policy_risk(tree[1],p,a,b,c)+p*conditional_policy_risk(tree[2],p,a,b,c)

def check_saturation():
    cases={'lower':0,'middle':0,'upper':0}
    for mu in (F(1,7),F(1,3),F(1,2),F(3,5),F(6,7)):
        for v in range(9):
            nu=mu*mu+(mu-mu*mu)*F(v,8)
            for a,b in product((F(1,3),F(1),F(2),F(5)),repeat=2):
                rho,case=least_favourable(mu,nu,a,b);cases[case]+=1
                risk=one_sample_risk(mu,nu,a,b)
                check(valid_rho(rho),'least-favourable measure valid')
                check(moments(rho,2)==(F(1),mu,nu),'least-favourable moments')
                oracle=sum(w*min(b*p,a*(1-p)) for p,w in rho)
                check(oracle==risk,'oracle equality certifies every adaptive horizon')
                q0=(mu-nu)/(1-mu);q1=nu/mu
                report0=int(q0>a/(a+b));report1=int(q1>a/(a+b))
                one=('q',('s',report0),('s',report1))
                check(sum(w*conditional_policy_risk(one,p,a,b,F(0)) for p,w in rho)==risk,'one-query rule attains lower certificate')
    trees=pure_policies(3)
    check(len(trees)==1446,'complete optional-stop policy enumeration horizon three')
    fixtures=((F(1,2),F(1,3),F(1),F(1)),(F(1,3),F(2,9),F(2),F(1)),(F(3,5),F(2,5),F(1),F(3)))
    for mu,nu,a,b in fixtures:
        rho,_=least_favourable(mu,nu,a,b)
        r0=min(b*mu,a*(1-mu));r1=one_sample_risk(mu,nu,a,b)
        for c in (F(0),F(1,10),F(1,2)):
            target=min(r0,c+r1)
            vals=[]
            for tree in trees:
                value=sum(w*conditional_policy_risk(tree,p,a,b,c) for p,w in rho)
                check(value>=target,'all bounded adaptive trees respect oracle price lower bound')
                vals.append(value)
            check(min(vals)==target,'finite full tree set attains saturation value')
    check(all(cases.values()),'all three least-favourable regimes exercised')
    return cases

def check_horizon_boundary():
    rhos=[]
    for sign in (1,-1):
        rho=tuple((F(k,5),F(5,192)*comb(5,k)+(F(1,12) if k in (0,5) else 0)
                   +sign*F(1,192)*(-1)**k*comb(5,k)) for k in range(6))
        check(valid_rho(rho) and all(w>0 for p,w in rho),'fifth-trial control fully positive')
        rhos.append(rho)
    mm=[moments(rho,5) for rho in rhos]
    check(mm[0][:5]==mm[1][:5]==(F(1),F(1,2),F(1,3),F(1,4),F(61,300)),'four moments agree exactly')
    check(mm[0][5]==F(437,2500) and mm[1][5]==F(219,1250),'fifth moments differ')
    check(law_from_rho(rhos[0],4)==law_from_rho(rhos[1],4),'all four-bit ordered laws agree')
    check(mm[0][5]/mm[0][4]==F(1311,1525) and mm[1][5]/mm[1][4]==F(1314,1525),'positive-event fifth continuation differs')
    for j in range(5):
        check(sum((-1)**k*comb(5,k)*F(k,5)**j for k in range(6))==0,'finite difference annihilates lower degrees')

def check_sources():
    path=Path(__file__).resolve().parent/'READ_LEDGER.json'
    rows=json.loads(path.read_text())
    for row in rows:
        for field in ('path','copy'):
            if field in row:
                p=Path(row[field])
                check(p.is_file(),'source path exists: '+str(p))
                check(hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],'source hash matches: '+row['id'])
    return len(rows)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--negative',choices=('guard','iid_equals_exchangeable','scalar_pruning','horizon_closed'))
    parser.add_argument('--output');args=parser.parse_args()
    if args.negative:
        conditions={'guard':False,'iid_equals_exchangeable':F(1,3)==F(21,50),
                    'scalar_pruning':F(1,2)==F(21,50),'horizon_closed':F(1311,1525)==F(1314,1525)}
        check(conditions[args.negative],'required false claim '+args.negative)
        raise RuntimeError('negative control unexpectedly passed')
    bound=check_sources();points=check_bodies();check_support(points);check_continuation_game(points);check_positive_game()
    regimes=check_saturation();check_horizon_boundary()
    result={'status':'PASS','active_exact_checks':COUNT,'bound_source_records':bound,
            'law_points_checked':len(points),'saturation_regimes':regimes,
            'continuation_c_1_10':{'calibration':'1/3','exchangeable_randomized':'21/50','exchangeable_deterministic':'1/2','query_probability':'1/5'},
            'scope':'Author exact controls supplement written universal proofs; no independent review, Lean, empirical calibration, or field novelty claim.'}
    out=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:Path(args.output).write_text(out)
    print(out,end='')

if __name__=='__main__':main()
