#!/usr/bin/env python3
"""Independent finite checks using exact rational arithmetic and active guards."""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import argparse, hashlib, json
HERE=Path(__file__).resolve().parent
N=0

def check(ok, label):
    global N
    N+=1
    if not ok: raise RuntimeError('ACTIVE_REVIEW_FAILURE: '+label)

# An independent representation: forty equiprobable outcomes in each model.
CELLS=((1,1),(0,1),(1,0),(0,0))
COUNTS=((1,9,9,21),(9,1,21,9))
WORLDS=tuple(tuple(cell for cell,n in zip(CELLS,counts) for _ in range(n)) for counts in COUNTS)
DEFER=Q(3,5)
PLANS=tuple(product(('D','R'),repeat=2))

def realized_loss(theta,audit,plan):
    action=plan[0 if audit else 1]
    if action=='D': return DEFER
    # A=1 permits report1; A=0 permits report0.
    return Q(theta!=audit)

def vector(plan):
    return tuple(sum((realized_loss(t,a,plan) for t,a in worlds),Q(0))/len(worlds) for worlds in WORLDS)

def average(vecs,weights): return tuple(sum((w*v[i] for w,v in zip(weights,vecs)),Q(0)) for i in range(len(vecs[0])))

def minimax_hull(vecs):
    # Piecewise-linear convex objective max(x,y) on a polygon. An optimizer
    # occurs at a vertex or an intersection of an edge with x=y. All vertex
    # pairs include every polygon edge; interior pairs add only feasible points.
    candidates=[(max(v),v,('pure',i)) for i,v in enumerate(vecs)]
    for i,j in combinations(range(len(vecs)),2):
        u,v=vecs[i],vecs[j]
        du,dv=u[0]-u[1],v[0]-v[1]
        if du==dv: continue
        w=-dv/(du-dv)
        if 0<=w<=1:
            z=average((u,v),(w,1-w))
            candidates.append((max(z),z,('mix',i,j,str(w))))
    return min(candidates,key=lambda x:x[0])

def run(negative=None):
    if negative=='guard': check(False,'forced active guard')
    V=tuple(vector(p) for p in PLANS)
    expected=((Q(3,5),Q(3,5)),(Q(3,8),Q(27,40)),(Q(27,40),Q(19,40)),(Q(9,20),Q(11,20)))
    check(V==expected,'atom-enumerated deterministic loss vectors')
    check(min(map(max,V))==Q(11,20),'deterministic minimax')
    optimum=minimax_hull(V)
    check(optimum[0]==Q(21,40),'randomized convex-hull minimax')
    mix=average((V[3],V[2]),(Q(2,3),Q(1,3)))
    check(mix==(Q(21,40),)*2,'private coin mixture')
    # An exact affine polynomial identity is established by all three coefficients.
    base=V[0]
    dx=tuple(a-b for a,b in zip(V[2],base))
    dy=tuple(a-b for a,b in zip(V[1],base))
    check(tuple(base[i]+dx[i]+dy[i] for i in range(2))==V[3],'no mixed action term')
    check(base[0]/4+3*base[1]/4==Q(3,5),'dual constant coefficient')
    check(dx[0]/4+3*dx[1]/4==-Q(3,40),'dual alpha coefficient')
    check(dy[0]/4+3*dy[1]/4==0,'dual beta coefficient')
    # This identity gives max(loss)>=3/5-3 alpha/40>=21/40 for every alpha<=1.
    branch=[]
    for a in (1,0):
        losses=[]
        for worlds in WORLDS:
            selected=tuple(t for t,aa in worlds if aa==a)
            losses.append(sum((Q(t!=a) for t in selected),Q(0))/len(selected))
        branch.append(tuple(losses))
    check(branch==[(Q(9,10),Q(1,10)),(Q(3,10),Q(7,10))],'conditional endpoint pairings')
    rect_risky=Q(1,4)*max(branch[0])+Q(3,4)*max(branch[1])
    check(rect_risky==Q(3,4)>max(V[3]),'rectangular adverse model pasting changes feasible law')
    check(Q(1,4)*min(DEFER,max(branch[0]))+Q(3,4)*min(DEFER,max(branch[1]))==DEFER,'rectangular optimum')
    check(max(branch[0])==Q(9,10)>DEFER,'committed A1 action is not conditional-maxmin optimal')
    check(Q(2,3)*max(branch[1])+Q(1,3)*DEFER==Q(2,3)>DEFER,'committed A0 lottery is not conditional-maxmin optimal')
    for probs in product((Q(i,12) for i in range(13)),repeat=2):
        a,b=probs
        weights=((1-a)*(1-b),(1-a)*b,a*(1-b),a*b)
        z=average(V,weights)
        check(max(z)>=Q(21,40),'behavioral-to-mixed policy check')
        check(z==tuple(base[i]+dx[i]*a+dy[i]*b for i in range(2)),'atom expectation agrees with affine formula')
    cost=Q(1,40)
    check(cost+min(map(max,V))==Q(23,40)<DEFER,'deterministic inquiry advantage with declared skip menu')
    check(cost+optimum[0]==Q(11,20)<DEFER,'private-mixed inquiry advantage')
    check(cost+DEFER==Q(5,8)>DEFER,'rectangular optimizer skips')
    # Scalar worst-case pruning would discard the risk/defer vector needed by optimum.
    best_scalar=tuple(v for v in V if max(v)==min(map(max,V)))
    check(minimax_hull(best_scalar)[0]==Q(11,20)>optimum[0],'scalar pruning counterexample')
    pareto=tuple(v for v in V if not any(u!=v and all(x<=y for x,y in zip(u,v)) for u in V))
    check(minimax_hull(pareto)[0]==optimum[0],'componentwise pruning safe in witness')
    public_coin=Q(2,3)*max(V[3])+Q(1,3)*max(V[2])
    check(public_coin==Q(71,120)>Q(21,40),'adversary sees complete sampled policy before model choice')
    check(min(map(max,V))==Q(11,20),'public revealed-policy mixing cannot improve best pure plan')
    # Explicit relaxed-menu control. At lambda=1/2 target is fair within each branch.
    fair_joint=tuple(Q(a+b,80) for a,b in zip(*COUNTS))
    check(fair_joint==(Q(1,8),Q(1,8),Q(3,8),Q(3,8)),'midpoint independent fair target')
    report_vectors=[]
    for guess in (0,1):
        report_vectors.append(tuple(sum((Q(t!=guess) for t,a in w),Q(0))/40 for w in WORLDS))
    check(average(report_vectors,(Q(1,2),Q(1,2)))==(Q(1,2),)*2,'unrestricted skip fair guess')
    check(Q(1,2)+cost>Q(1,2),'unrestricted all-report menu has no positive-cost audit gain')
    if negative=='scalar': check(minimax_hull(best_scalar)[0]==optimum[0],'deliberately wrong scalar pruning')
    # Distinct root-supplied unrestricted-menu witness, checked separately from L.
    m_endpoints=((Q(4,10),Q(2,10),Q(1,10),Q(3,10)),(Q(3,10),Q(1,10),Q(2,10),Q(4,10)))
    m_cost=Q(9,50)
    for k in range(101):
        lam=Q(k,100)
        a,b,c,d=tuple((1-lam)*u+lam*v for u,v in zip(*m_endpoints))
        check(a+c==Q(1,2),'M balanced initial target')
        check(b+c==Q(3,10),'M common classifier error')
        check(a-b==d-c==Q(1,5),'M positive affine excess coefficients')
        check(b/(a+b)<=Q(1,3) and c/(c+d)<=Q(1,3),'M conditional errors bounded')
    rect_laws=[]
    for mass,q1,q0 in product((Q(2,5),Q(3,5)),(Q(2,3),Q(3,4)),(Q(1,4),Q(1,3))):
        law=(mass*q1,mass*(1-q1),(1-mass)*q0,(1-mass)*(1-q0))
        rect_laws.append(law)
        check(sum(law)==1 and min(law)>0,'M rectangular endpoint law valid')
        check(law[1]+law[2]<=Q(1,3),'M classify A upper bound over rectangular vertices')
    priors=[v[0]+v[2] for v in rect_laws]
    check((min(priors),max(priors))==(Q(5,12),Q(7,12)),'rectangularization may change original target prior')
    check(min(max(priors),1-min(priors))==Q(7,12),'rectangular deterministic skip differs')
    balanced=(Q(1,3),Q(1,6),Q(1,6),Q(1,3))
    check(balanced[1]+balanced[2]==Q(1,3),'balanced foreign law attains robust query lower bound')
    check(balanced[0]>balanced[1] and balanced[3]>balanced[2],'common classifier is Bayes optimal at balanced pasted law')
    for g1,g0 in product((0,1),repeat=2):
        a,b,c,d=balanced
        risk=(1-g1)*a+g1*b+(1-g0)*c+g0*d
        check(risk>=Q(1,3),'balanced foreign law all report plans lower bound')
    check(Q(3,10)+m_cost==Q(12,25)<Q(1,2),'unrestricted fixed-model inquiry preferred')
    check(Q(1,3)+m_cost==Q(77,150)>Q(1,2),'unrestricted rectangular query inferior to private fair skip')
    # The balanced pasted law also shows mixtures of query/skip cannot beat 1/2:
    # every skip report has risk 1/2 there, every query policy costs >=77/150.
    # A globally impossible outcome is not a live obligation to terminate.
    live_values={(Q(0),)}
    forbidden_terminal_values=set()
    naive_parents=list(product(live_values,forbidden_terminal_values))
    check(naive_parents==[],'requiring completion on an impossible outcome falsely rejects its parent')
    guarded_dead={(Q(0),)}  # zero-probability bookkeeping, not a live free stop
    guarded_parents={tuple(x+y for x,y in zip(a,b)) for a,b in product(live_values,guarded_dead)}
    check(guarded_parents=={(Q(0),)},'globally impossible outcome contributes zero')
    partially_live_masses=(Q(0),Q(1,4))
    check(any(partially_live_masses),'model-specific impossible component does not erase a live branch')
    # Kernel versus path-law proof by exact polynomial coefficient arithmetic.
    # Coefficients constant, linear, quadratic in unknown fixed Bernoulli p.
    path=((Q(1),Q(-2),Q(1)),(Q(0),Q(1),Q(-1)),(Q(0),Q(1),Q(-1)),(Q(0),Q(0),Q(1)))
    event=tuple(path[1][i]+path[2][i] for i in range(3))
    check(event==(Q(0),Q(2),Q(-2)),'mismatch polynomial 2p(1-p)')
    evaluate=lambda coeff,p: sum((c*p**i for i,c in enumerate(coeff)),Q(0))
    check(evaluate(event,Q(0))==evaluate(event,Q(1))==0,'endpoint kernel failure')
    check(evaluate(event,Q(1,2))==Q(1,2),'interior mismatch maximum attained')
    ex1=tuple(path[2][i]+path[3][i] for i in range(3))
    exprod=path[3]
    check(ex1==(Q(0),Q(1),Q(0)) and exprod==(Q(0),Q(0),Q(1)),'moment lift coefficients')
    for k in range(29):
        p0=Q(k,28)
        observable=tuple(2*p0*ex1[i]-exprod[i] for i in range(3))
        check(observable==(Q(0),2*p0,Q(-1)),'exposed-point polynomial')
        for j in range(29):
            p=Q(j,28)
            check(evaluate(observable,p)==p0*p0-(p-p0)**2,'exposed-point square identity')
            check((evaluate(observable,p)==p0*p0)==(p==p0),'unique maximizer controls')
    # Input hashes are enforced only when final manifest exists.
    binding=HERE/'REVIEW_BINDINGS.json'
    if binding.exists():
        for item in json.loads(binding.read_text())['reviewed_files']:
            data=(HERE.parent/item['path']).read_bytes()
            check(len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],'unchanged reviewed input '+item['path'])
    return {'status':'PASS','active_checks':N,'deterministic_minimax':'11/20','private_randomized_minimax':'21/40','rectangular_minimax':'3/5','scalar_pruning_error':'11/20 versus 21/40','revealed_optimal_private_coin_loss':'71/120','expanded_skip_menu_minimax':'1/2','kernel_mismatch_maximum':'1/2','scope':'Independent exact controls and coefficient identities; ordinary universal proofs in REVIEW.md; no theorem prover certification.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--negative',choices=['guard','scalar']);args=p.parse_args()
    print(json.dumps(run(args.negative),indent=2))
