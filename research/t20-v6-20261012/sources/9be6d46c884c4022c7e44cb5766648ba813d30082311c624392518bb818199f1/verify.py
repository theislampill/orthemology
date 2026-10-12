#!/usr/bin/env python3
"""Exact author controls; no assert statements, no floating point, stdlib only."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
from math import isqrt
import argparse, hashlib, json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
N = 0
GROUPS = {}

def check(condition, message, group='main'):
    global N
    N += 1
    GROUPS[group] = GROUPS.get(group, 0) + 1
    if not condition:
        raise RuntimeError('ACTIVE_CHECK_FAILED: ' + message)

def dot(a,b): return sum((x*y for x,y in zip(a,b)), F(0))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(s,a): return tuple(s*x for x in a)
def mat(M,v): return tuple(dot(row,v) for row in M)
def compose(M,N): return tuple(tuple(dot(row,col) for col in zip(*N)) for row in M)
def mix(v,w,t): return add(scale(1-t,v),scale(t,w))
def normalized(v):
    z=sum(v)
    return tuple(x/z for x in v) if z else None

# Exact inherited L, same cell order as the source report.
L=((F(1,40),F(9,40),F(9,40),F(21,40)),
   (F(9,40),F(1,40),F(21,40),F(9,40)))
MASKS=((1,1,0,0),(0,0,1,1))  # A=1, A=0
P=tuple(tuple(tuple(F(int(i==j))*mask[i] for j in range(4)) for i in range(4)) for mask in MASKS)
RISK=(tuple(map(F,(0,1,0,0))),tuple(map(F,(0,0,1,0))))
SAFE=F(3,5)
AUDIT=F(1,40)

def loss(v, alpha, beta):
    # alpha/beta are private risk-action probabilities after A=1/A=0.
    return alpha*v[1]+(1-alpha)*SAFE*sum(v[:2])+beta*v[2]+(1-beta)*SAFE*sum(v[2:])

def policy_vector(alpha,beta): return tuple(loss(v,alpha,beta) for v in L)

def solve(A,b):
    a=[list(row)+[rhs] for row,rhs in zip(A,b)]
    n=len(b)
    for j in range(n):
        piv=next((i for i in range(j,n) if a[i][j]),None)
        if piv is None:return None
        a[j],a[piv]=a[piv],a[j]
        z=a[j][j];a[j]=[v/z for v in a[j]]
        for i in range(n):
            if i!=j:
                z=a[i][j];a[i]=[v-z*w for v,w in zip(a[i],a[j])]
    return tuple(row[-1] for row in a)

def randomized_lp():
    # A*x <= b for x=(alpha,beta,t). The two risk rows bound the epigraph.
    A=[(-F(1),0,0),(F(1),0,0),(0,-F(1),0),(0,F(1),0),
       (F(3,40),-F(9,40),-F(1)),(-F(1,8),F(3,40),-F(1))]
    b=[F(0),F(1),F(0),F(1),-SAFE,-SAFE]
    candidates=[]
    for ids in combinations(range(len(A)),3):
        x=solve([A[i] for i in ids],[b[i] for i in ids])
        if x is not None and all(dot(row,x)<=rhs for row,rhs in zip(A,b)):
            candidates.append(x)
    return min(candidates,key=lambda x:x[2]), candidates

def exact_sqrt_ratio(z):
    a,b=isqrt(z.numerator),isqrt(z.denominator)
    check(a*a==z.numerator and b*b==z.denominator,'inverse escort ratio is rational square','escort')
    return F(a,b)

def escort(v):
    return normalized(tuple(x*x for x in v))

def decode(q):
    if q is None:return None
    pivot=next(x for x in q if x)
    return normalized(tuple(exact_sqrt_ratio(x/pivot) for x in q))

def dynamic_sets(rs,depth,operators,costs,terminal,early_stop=False):
    """Unnormalized vectors; common actions. Globally impossible nodes need no menu."""
    if all(not any(r) for r in rs):
        return {tuple(F(0) for r in rs)}
    if depth==0:
        return {tuple(dot(l,r) for r in rs) for l in terminal}
    out={tuple(dot(l,r) for r in rs) for l in terminal} if early_stop else set()
    for a,Ms in enumerate(operators):
        kids=[dynamic_sets(tuple(mat(M,r) for r in rs),depth-1,operators,costs,terminal,early_stop) for M in Ms]
        for child_vectors in product(*kids):
            out.add(tuple(dot(costs[a],rs[i])+sum(v[i] for v in child_vectors) for i in range(len(rs))))
    return out

def all_trees(depth,operators,terminal,early_stop=False):
    stops=[('stop',j) for j in range(len(terminal))]
    if depth==0:return stops
    continued=[(a,children) for a,Ms in enumerate(operators)
               for children in product(all_trees(depth-1,operators,terminal,early_stop),repeat=len(Ms))]
    return stops+continued if early_stop else continued

def loss_row(tree,operators,costs,terminal):
    # Independent backward observable-row evaluation, against set recursion.
    a,kids=tree
    if a=='stop':return terminal[kids]
    row=costs[a]
    for M,kid in zip(operators[a],kids):
        f=loss_row(kid,operators,costs,terminal)
        row=add(row,tuple(dot(f,col) for col in zip(*M)))
    return row

def run(negative=None):
    if negative=='guard': check(False,'deliberate guard control','negative')
    source=(WORK/'cumulative-credal-audit-coupling-20261011/REPORT.md').read_text()
    check('(1,9,9,21)/40' in source and '(9,1,21,9)/40' in source,'actual inherited fixture','binding')
    for v in L:
        check(sum(v)==1 and min(v)>0,'normalized strict positive vertex','fixture')
        check(sum(v[:2])==F(1,4),'same audit mass','fixture')
    for j in range(101):
        v=mix(*L,F(j,100))
        check(min(v)>0 and sum(v)==1,'positive mixture','fixture')
        check(sum(v[:2])==F(1,4),'mixture audit mass','fixture')
        for alpha,beta in product((F(0),F(1,3),F(2,3),F(1)),repeat=2):
            check(loss(v,alpha,beta)==dot((1-F(j,100),F(j,100)),policy_vector(alpha,beta)),
                  'same model through both branches; affine vertex response','linearity')
    expected={(0,0):(F(3,5),F(3,5)),(1,0):(F(27,40),F(19,40)),
              (0,1):(F(3,8),F(27,40)),(1,1):(F(9,20),F(11,20))}
    values={p:policy_vector(*p) for p in product((0,1),repeat=2)}
    check(values==expected,'four deterministic policies','policy')
    check(min(max(v) for v in values.values())==F(11,20),'deterministic fixed-model optimum','policy')
    marginal=(F(1,4),F(3,4))
    conditional=tuple(tuple(dot(RISK[o],v)/dot(MASKS[o],v) for v in L) for o in range(2))
    check(conditional==((F(9,10),F(1,10)),(F(3,10),F(7,10))),'paired conditional losses','policy')
    rectangular_fixed=sum(marginal[o]*max(conditional[o]) for o in range(2))
    check(rectangular_fixed==F(3,4),'switched value for risky/risky','policy')
    check(rectangular_fixed>max(values[1,1]),'strict robust tower inequality','policy')
    if negative=='scalar':
        check(rectangular_fixed==max(values[1,1]),'false fixed equals rectangular','negative')
    rectangular_opt=sum(marginal[o]*min(SAFE,max(conditional[o])) for o in range(2))
    check(rectangular_opt==SAFE,'rectangular optimizer defers','policy')
    pasted=(L[0][0],L[0][1],L[1][2],L[1][3])
    check(sum(pasted)==1 and min(pasted)>0,'pasted law is coherent and positive','pasting')
    # From cell zero, this putative member would force lambda=0, incompatible cell two.
    lam=(pasted[0]-L[0][0])/(L[1][0]-L[0][0])
    check(pasted!=mix(*L,lam),'pasted model outside inherited segment','pasting')
    check(loss(pasted,1,1)==F(3,4),'rectangular value attained by foreign law','pasting')
    lp,candidates=randomized_lp()
    check(lp==(F(1),F(2,3),F(21,40)),'exact rational LP optimum','randomized')
    check(policy_vector(lp[0],lp[1])==(F(21,40),)*2,'randomized primal attainment','randomized')
    for j,k in product(range(31),repeat=2):
        a,b=F(j,30),F(k,30);v=policy_vector(a,b)
        check(dot((F(1,4),F(3,4)),v)==SAFE-F(3,40)*a,'dual identity','randomized')
        check(max(v)>=SAFE-F(3,40)*a>=F(21,40),'dual lower bound','randomized')
        # Locally mixing risk/defer never beats defer against branchwise worst case.
        rect=marginal[0]*(SAFE+F(3,10)*a)+marginal[1]*(SAFE+F(1,10)*b)
        check(rect>=SAFE,'randomized rectangular lower bound','randomized')
    check(AUDIT+F(11,20)==F(23,40)<SAFE,'deterministic inquiry preferred','decision')
    check(AUDIT+F(21,40)==F(11,20)<SAFE,'randomized inquiry preferred','decision')
    check(AUDIT+rectangular_opt>SAFE,'rectangular skips inquiry','decision')

    check(F(1,2)<AUDIT+F(21,40),'free pre-audit fair guess destroys L inquiry advantage','menu_scope')
    check(F(2,3)*F(11,20)+F(1,3)*F(27,40)==F(71,120)>F(21,40),
          'revealed policy draw has different adversary timing','menu_scope')
    # Parent-supplied unrestricted two-label discriminator, separate from L.
    W=((F(4,10),F(2,10),F(1,10),F(3,10)),
       (F(3,10),F(1,10),F(2,10),F(4,10)))
    for j in range(101):
        v=mix(*W,F(j,100));a,b,c,d=v
        check(min(v)>0 and sum(v)==1 and a+c==F(1,2),'unrestricted positive prior','unrestricted')
        check(b+c==F(3,10),'common Bayes classifier exact loss','unrestricted')
        e1,e0=b/(a+b),c/(c+d)
        check(F(1,4)<=e1<=F(1,3) and F(1,4)<=e0<=F(1,3),
              'conditional adverse-error bounds','unrestricted')
        for k,l in product(range(7),repeat=2):
            # x/y probabilities of reporting theta=1 after audit1/audit0.
            x,y=F(k,6),F(l,6)
            actual=x*b+(1-x)*a+y*d+(1-y)*c
            check(actual>=F(3,10),'all tested randomized classifiers Bayes lower bound','unrestricted')
    check(W[0][1]/sum(W[0][:2])==W[1][2]/sum(W[1][2:])==F(1,3),
          'different maximizing endpoint at each branch','unrestricted')
    wstar=(F(1,3),F(1,6),F(1,6),F(1,3))
    check(sum(wstar)==1 and wstar[0]+wstar[2]==F(1,2) and sum(wstar[:2])==F(1,2),
          'unrestricted pasted law preserves target prior and marginal range','unrestricted')
    check(wstar[1]+wstar[2]==F(1,3)!=F(3,10),'unrestricted pasted law excluded','unrestricted')
    price=F(9,50)
    check(F(3,10)+price==F(12,25)<F(1,2),'unrestricted fixed model audits','unrestricted')
    check(F(1,3)+price==F(77,150)>F(1,2),'unrestricted rectangular model skips','unrestricted')

    # Exact proper quotient: discard an irrelevant latent binary record S.
    G=tuple(tuple(F(int(j//2==i)) for j in range(8)) for i in range(4))
    fine=tuple(tuple(x*s for x in v for s in (F(i+1,3),1-F(i+1,3))) for i,v in enumerate(L))
    for i in range(2):check(mat(G,fine[i])==L[i],'fine law projects to inherited vertex','quotient')
    for o in range(2):
        Mf=tuple(tuple(F(int(i==j))*MASKS[o][i//2] for j in range(8)) for i in range(8))
        check(compose(G,Mf)==compose(P[o],G),'common branch intertwining','quotient')
    for j,k in product(range(13),repeat=2):
        a,b=F(j,12),F(k,12)
        row=(SAFE*(1-a),a+SAFE*(1-a),b+SAFE*(1-b),SAFE*(1-b))
        fr=tuple(row[j//2] for j in range(8))
        check(tuple(dot(fr,v) for v in fine)==policy_vector(a,b),'same model-indexed policy vectors','quotient')

    # Escort recoding preserves finite-word masses only with inverse readout.
    for v in L:
        check(decode(escort(v))==v,'escort inverse','escort')
        check(sum(escort(v)[:2])!=sum(v[:2]),'direct transformed-mass reading is wrong','escort')
        for n in range(7):
            for w in product(range(2),repeat=n):
                raw=v;q=escort(v);mass=F(1)
                for o in w:
                    raw=mat(P[o],raw)
                    if q is not None:
                        next_raw=mat(P[o],decode(q));z=sum(next_raw);mass*=z
                        q=escort(next_raw) if z else None
                check(mass==sum(raw),'original path mass preserved','escort')
                check(decode(q)==normalized(raw),'decoded finite-history law','escort')
    # Generic 2-state, 2-action, 2-outcome common instruments, fixed-depth stops.
    # Every outcome has positive total mass from every nonzero nonnegative state.
    operators=(
      (((F(1,2),0),(0,F(1,3))),((F(1,2),0),(0,F(2,3)))),
      (((F(1,4),F(1,2)),(0,0)),((F(3,4),0),(0,F(1,2)))))
    costs=((F(1,20),F(1,10)),(F(1,8),F(1,16)))
    terminal=((F(0),F(1)),(F(1),F(0)),(SAFE,SAFE))
    roots=((F(1,4),F(3,4)),(F(3,4),F(1,4)),(F(1),F(0)))
    enumerated=0
    for depth in range(3):
        trees=all_trees(depth,operators,terminal);enumerated+=len(trees)
        direct={tuple(dot(loss_row(t,operators,costs,terminal),r) for r in roots) for t in trees}
        recursive=dynamic_sets(roots,depth,operators,costs,terminal)
        check(direct==recursive,'set-valued recursion equals independent tree enumeration','set_recursion')
        check(min(map(max,direct))==min(map(max,recursive)),'root robust scalarization','set_recursion')
        # Componentwise pruning is safe. Equal components use one representative.
        front={v for v in recursive if not any(w!=v and all(x<=y for x,y in zip(w,v)) for w in recursive)}
        check(min(map(max,front))==min(map(max,recursive)),'componentwise dominance safe','set_recursion')
    # Full rectangular hull does not retain the original balanced target prior.
    hull_priors=[m*q1+(1-m)*q0 for m,q1,q0 in product(
        (F(2,5),F(3,5)),(F(2,3),F(3,4)),(F(1,4),F(1,3)))]
    check((min(hull_priors),max(hull_priors))==(F(5,12),F(7,12)),
          'full rectangular hull prior range','final_scope')
    check(min(max(hull_priors),1-min(hull_priors))==F(7,12),
          'deterministic full hull skip differs','final_scope')
    for p in hull_priors:
        check(F(1,2)*p+F(1,2)*(1-p)==F(1,2),'private fair skip exact under every hull corner','final_scope')
    for x,y in product((F(0),F(1,3),F(2,3),F(1)),repeat=2):
        a,b,c,d=wstar
        query_loss=x*b+(1-x)*a+y*d+(1-y)*c
        check(query_loss+price>=F(77,150),'balanced paste lower bounds every tested query','final_scope')
        check(x*F(1,2)+(1-x)*F(1,2)==F(1,2),'balanced paste lower bounds every tested skip','final_scope')
    # Globally impossible histories contribute zero even when their menu is empty.
    zero_rs=((F(0),),(F(0),));live_rs=((F(1),),(F(1),))
    unary_ops=((((F(1),),),),);unary_costs=((F(1,4),),);unary_terminal=((F(1,2),),)
    check(dynamic_sets(zero_rs,0,unary_ops,unary_costs,())=={(F(0),F(0))},
          'globally impossible empty-menu leaf contributes singleton zero','final_scope')
    check(dynamic_sets(live_rs,0,unary_ops,unary_costs,())==set(),
          'live empty-menu leaf is infeasible','final_scope')
    child_zero=dynamic_sets(zero_rs,0,unary_ops,unary_costs,())
    child_live=dynamic_sets(live_rs,0,unary_ops,unary_costs,unary_terminal)
    parent_vectors={add(a,b) for a,b in product(child_zero,child_live)}
    check(parent_vectors=={(F(1,2),F(1,2))},'unreachable child does not delete feasible parent','final_scope')
    early=dynamic_sets(live_rs,1,unary_ops,unary_costs,unary_terminal,early_stop=True)
    early_trees=all_trees(1,unary_ops,unary_terminal,early_stop=True)
    early_direct={tuple(dot(loss_row(t,unary_ops,unary_costs,unary_terminal),r) for r in live_rs)
                  for t in early_trees}
    check(early==early_direct=={(F(1,2),F(1,2)),(F(3,4),F(3,4))},
          'optional early stop matches independent enumeration','final_scope')
    fixed=dynamic_sets(live_rs,1,unary_ops,unary_costs,unary_terminal)
    check(fixed=={(F(3,4),F(3,4))} and min(map(max,early))<min(map(max,fixed)),
          'early stop can strictly improve fixed-depth cost','final_scope')
    for item in json.loads((HERE/'INPUT_BINDINGS.json').read_text())['inputs']:
        p=WORK/item['path'];data=p.read_bytes()
        check(len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],
              'unchanged inherited input '+item['path'],'binding')
    return {'status':'PASS','checks':N,'groups':GROUPS,
      'fixed_risky_plan':'11/20','rectangular_risky_plan':'3/4',
      'deterministic_post_audit_optimum':'11/20','randomized_post_audit_optimum':'21/40',
      'rectangular_post_audit_optimum':'3/5','audit_cost':'1/40',
      'deterministic_root_optimum':'23/40','randomized_root_optimum':'11/20','rectangular_root_optimum':'3/5',
      'randomized_policy':{'risk_probability_A1':'1','risk_probability_A0':'2/3'},
      'unrestricted_fixed_audit_risk':'3/10','unrestricted_rectangular_audit_risk':'1/3',
      'unrestricted_fixed_root_value':'12/25','unrestricted_rectangular_root_value':'1/2',
      'lp_feasible_vertices':len(candidates),'independently_enumerated_policy_trees':enumerated,
      'scope':'Author rational controls, not an independent review or kernel proof.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--negative-control',choices=['guard','scalar']);args=p.parse_args()
    result=run(args.negative_control);out=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(out)
    print(out,end='')
