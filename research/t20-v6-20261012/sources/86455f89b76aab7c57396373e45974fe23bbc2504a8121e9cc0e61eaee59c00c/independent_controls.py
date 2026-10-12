#!/usr/bin/env python3
"""Independent exact, bounded controls. Does not import the author's program."""
from pathlib import Path
from itertools import combinations, product
import hashlib, json, sys
import sympy as sp

HERE = Path(__file__).resolve().parent
Q = sp.Rational
checks = []

def check(name, condition, detail=None):
    assert condition, name
    record = {'name': name, 'passed': True}
    if detail is not None: record['detail'] = detail
    checks.append(record)
    print(f'PASS {len(checks):02}: {name}', flush=True)

def subsets(s):
    s = sorted(s)
    return [frozenset(t) for k in range(len(s)+1) for t in combinations(s,k)]

def down(facets):
    return set().union(*(set(subsets(t)) for t in facets))

def maximal(family):
    return [s for s in family if not any(s < t for t in family)]

def core(family):
    return set.intersection(*(set(s) for s in maximal(family)))

def contrasts(q):
    # Orthogonal integer Helmert contrasts; not the author's marginal indicators.
    return [[1]*q] + [[1 if x < j else -j if x == j else 0 for x in range(q)]
                      for j in range(1,q)]

def model(sizes, family):
    states = list(product(*(range(q) for q in sizes)))
    local = [contrasts(q) for q in sizes]
    kept, omitted = [], []
    for label in product(*(range(q) for q in sizes)):
        support = frozenset(i for i,a in enumerate(label) if a)
        row = [sp.prod(local[i][a][x[i]] for i,a in enumerate(label)) for x in states]
        (kept if support in family else omitted).append(row)
    return states, sp.Matrix(kept), sp.Matrix(omitted) if omitted else sp.zeros(0,len(states))

def constraints(M, N):
    return sp.Matrix([[a*b for a,b in zip(M.row(i),N.row(j))]
                      for i in range(M.rows) for j in range(N.rows)]) if N.rows else sp.zeros(0,M.cols)

def basis(rows):
    if rows.rows == 0: return rows
    return rows[list(rows.T.rref()[1]),:]

def indicator(states, coords):
    coords = tuple(sorted(coords))
    assignments = sorted({tuple(x[i] for i in coords) for x in states})
    return sp.Matrix([[int(tuple(x[i] for i in coords) == a) for x in states] for a in assignments])

def closed_span(M, generators):
    W = basis(M)
    while True:
        extra = sp.Matrix([[v*l for v,l in zip(W.row(i),g)]
                           for i in range(W.rows) for g in generators])
        new = basis(W.col_join(extra))
        if new.rows == W.rows: return W
        W = new

def bayes(p,L):
    raw = p.multiply_elementwise(L)
    return raw / sum(raw)

def fisher(p,f):
    return -(sp.diag(*p)-p*p.T)*f

# Exhaust all nonempty downward families on three categorical coordinates.
ps = subsets(range(3)); families=[]; details=[]
for flags in product((False,True),repeat=len(ps)):
    F = {s for s,flag in zip(ps,flags) if flag}
    if not F or any(not set(subsets(s)) <= F for s in F): continue
    states,M,N = model((2,3,2),F); K=constraints(M,N); C=core(F)
    B=indicator(states,C)
    assert K*B.T == sp.zeros(K.rows,B.rows)
    assert M.cols-K.rank() == B.rows
    families.append(F)
    details.append({'facets':[sorted(t) for t in sorted(maximal(F),key=lambda s:(len(s),sorted(s)))],
                    'core':sorted(C),'observable_dimension':M.rows,'stabilizer_dimension':B.rows})
check('all 19 nonempty categorical three-coordinate hierarchies',len(families)==19,details)

# Exhaust binary four-coordinate hierarchies by exact Walsh coefficient shifts.
ps4=subsets(range(4)); count=0
for mask in range(1,1<<len(ps4)):
    F={s for j,s in enumerate(ps4) if mask>>j&1}
    if any(not set(subsets(s))<=F for s in F):continue
    admitted={s for s in ps4 if all((s^t) in F for t in F)}
    assert admitted==set(subsets(core(F)))
    count+=1
check('all 167 nonempty binary four-coordinate hierarchies',count==167,{'families':count})

# Unequal-sized maximal faces and omitted coordinates are not special exceptions.
for sizes,facets in [((3,2,2,2),[(0,1,2),(0,3)]),
                     ((2,3,2,2),[(0,1),(2,)]),
                     ((2,3,2),[(0,1)]),
                     ((),[()])]:
    F=down(facets); states,M,N=model(sizes,F);K=constraints(M,N);B=indicator(states,core(F))
    check('unequal-facet/omitted/empty-product stabilizer '+str((sizes,facets)),
          K*B.T==sp.zeros(K.rows,B.rows) and M.cols-K.rank()==B.rows,
          {'retained_dimension':M.rows,'stabilizer_dimension':B.rows})

# A singleton alphabet invalidates a naive use of the nominal common core.
F=down([(0,),(1,)]);states,M,N=model((2,1),F)
check('nontrivial-alphabet hypothesis is necessary',core(F)==set() and M.rows==2 and constraints(M,N).rows==0)

# Non-pure offending component of smaller degree than a core component.
sizes=(3,2,2,3,2);F=down([(0,1,2,3),(0,1,2,4)])
states,M,N=model(sizes,F)
a=(1,-1,0);b=(1,1,-2)
R=sp.Matrix([a[x[0]]*a[x[3]]+b[x[0]]*b[x[3]] for x in states])
G=sp.Matrix([b[x[0]]*(2*x[1]-1)*(2*x[2]-1) for x in states])
u=sp.Matrix([(2*x[1]-1)*(2*x[2]-1)*(2*x[4]-1) for x in states])
L=sp.ones(len(states),1)/2+(R+G)/64
forbidden=R.multiply_elementwise(u)
raw=L.multiply_elementwise(u)
# Project onto H_all using explicitly factorized orthogonal contrasts.
allrows=[]
local=[contrasts(q) for q in sizes]
for labels in product(*(range(1,q) for q in sizes)):
    allrows.append([sp.prod(local[i][labels[i]][x[i]] for i in range(5)) for x in states])
P=sp.Matrix(allrows)
coeff=P*raw;expected=P*forbidden/64
check('maximal offending component survives higher-degree core and non-pure categorical rank',
      sp.Matrix([[a[i]*a[j]+b[i]*b[j] for j in range(3)] for i in range(3)]).rank()==2
      and all(0<v<1 for v in L) and coeff==expected and any(v!=0 for v in coeff)
      and N*L==sp.zeros(N.rows,1),
      {'core':[0,1,2],'offending_support':[0,3],'higher_core_support':[0,1,2],'forbidden_support':[0,1,2,3,4]})
# Full-support pair with equal retained records and probabilities, different u posterior.
epsilon=Q(1,1024)
pplus=sp.ones(len(states),1)/len(states)+epsilon*forbidden
pminus=sp.ones(len(states),1)/len(states)-epsilon*forbidden
check('non-pure positive-prior Bayesian obstruction',
      min(pplus)>0 and min(pminus)>0 and M*pplus==M*pminus
      and (L.T*pplus)[0]==(L.T*pminus)[0] and u.dot(bayes(pplus,L))!=u.dot(bayes(pminus,L)),
      {'branch_probability':str(L.dot(pplus)),'u_posterior_plus':str(u.dot(bayes(pplus,L))),
       'u_posterior_minus':str(u.dot(bayes(pminus,L)))})

# Closure from only strictly positive probabilities versus the full D algebra.
sizes=(3,2,2);F=down([(0,),(1,),(2,)])
states,M,N=model(sizes,F);D=indicator(states,(0,))
positive_generators=[list(sp.ones(1,len(states))/4+D.row(i)/2) for i in range(D.rows)]
Wpos=closed_span(M,positive_generators)
Wfull=closed_span(M,[list(D.row(i)) for i in range(D.rows)])
_,Wexpected,_=model(sizes,down([(0,),(0,1),(0,2)]))
check('strictly positive likelihood generators give the full all-local module',
      all(0<v<1 for g in positive_generators for v in g)
      and Wpos.rows==Wfull.rows==Wexpected.rows==9
      and Wpos.col_join(Wexpected).rank()==9)

# A fixed ternary likelihood with repeated levels carries only a two-block algebra.
Lfixed=sp.Matrix([Q(1,4) if x[0]<2 else Q(3,4) for x in states])
Wfixed=closed_span(M,[list(Lfixed)])
Ldistinct=sp.Matrix([Q(x[0]+1,4) for x in states])
Wdistinct=closed_span(M,[list(Ldistinct)])
check('one fixed categorical channel can require strictly less than all-local evidence',
      Wfixed.rows==7<Wfull.rows==9 and Wdistinct.rows==9
      and closed_span(M,[list(Lfixed),list(sp.ones(len(states),1)-Lfixed)]).rows==7,
      {'initial_dimension':M.rows,'two_level_fixed_channel':Wfixed.rows,'three_level_fixed_channel':Wdistinct.rows,'all_D_local':Wfull.rows})
# Every original retained row times every D-indicator must lie in any invariant space.
products=sp.Matrix([[v*l for v,l in zip(M.row(i),D.row(j))] for i in range(M.rows) for j in range(D.rows)])
check('product span supplies all-linear-space minimality certificate',products.rank()==9 and products.col_join(Wfull).rank()==9)
Wall=closed_span(M,[list(indicator(states,(i,)).row(j)) for i in range(3) for j in range(sizes[i])])
check('separate all-local evidence on every coordinate forces full law',Wall.rows==len(states)==12)

# Posterior-only polynomial identity, compared with support-cylinder iff.
# For every kernel basis h and each prior atom i: (MD_L h) L_i = (L.h)(MD_L e_i).
def posterior_identity(M,N,L):
    for hr in N.tolist():
        b=sum(l*h for l,h in zip(L,hr))
        a=[sum(v*l*h for v,l,h in zip(row,L,hr)) for row in M.tolist()]
        for i,l in enumerate(L):
            if any(aj*l!=b*M[j,i]*l for j,aj in enumerate(a)):return False
    return True

grid_cases=0
for sizes,facets,levels in [((2,2,2),[(0,),(1,)],(0,1)),
                           ((2,2,2),[(0,1)],(0,1)),
                           ((2,3),[()],(0,1,2)),
                           ((2,2),[(0,1)],(0,1,2))]:
    F=down(facets);states,M,N=model(sizes,F);K=constraints(M,N);A=set().union(*F)
    casecount=0
    for vals in product(levels,repeat=len(states)):
        support=[i for i,l in enumerate(vals) if l]
        expected=(K*sp.Matrix(vals)==sp.zeros(K.rows,1) or len({tuple(states[i][j] for j in sorted(A)) for i in support})<=1)
        assert posterior_identity(M,N,vals)==expected
        casecount+=1
    grid_cases+=casecount
    check('posterior polynomial/support-cylinder comparison '+str((sizes,facets)),True,{'likelihoods_including_zero':casecount})

# Full A marginal, omitted coordinate: posterior and feasibility close, probability does not.
states,M,N=model((2,2,3),down([(0,1)]))
L=sp.Matrix([Q(x[2]+1,4) if x[:2]==(0,0) else 0 for x in states])
e0,e1=sp.eye(12)[:,0],sp.eye(12)[:,1]
check('full covered marginal plus whole cylinder retains feasibility without probability',
      M*e0==M*e1 and M*bayes(e0,L)==M*bayes(e1,L) and L.dot(e0)!=L.dot(e1)
      and all((l>0)==(x[:2]==(0,0)) for x,l in zip(states,L)))
Lpartial=L.copy();Lpartial[1]=0
check('partial covered cylinder loses feasibility even with full covered marginal',
      M*e0==M*e1 and Lpartial.dot(e0)>0 and Lpartial.dot(e1)==0)
# Proper hierarchy covering both coordinates: the whole cylinder can still lose feasibility.
_,Mproper,Nproper=model((2,2,3),down([(0,),(1,)]))
pdiag=sp.Matrix([Q(1,6) if x[0]==x[1] else 0 for x in states])
panti=sp.Matrix([Q(1,6) if x[0]!=x[1] else 0 for x in states])
check('whole cylinder loses feasibility when covered hierarchy is proper',
      Mproper*pdiag==Mproper*panti and L.dot(pdiag)>0 and L.dot(panti)==0)
# All full-support priors give positive alpha for nonzero nonnegative L, but alpha still differs.
uniform=sp.ones(12,1)/12
p1=(e0+uniform)/2;p2=(e1+uniform)/2
check('full-support feasibility is trivial and does not recover cylinder probability',
      min(p1)>0 and min(p2)>0 and M*p1==M*p2 and L.dot(p1)>0 and L.dot(p2)>0 and L.dot(p1)!=L.dot(p2))

# Nonlinear core objective on a correlated ternary star; signed fitness needs no likelihood bound.
sizes=(3,2,2);F=down([(0,1),(0,2)]);states,M,N=model(sizes,F)
w=[Q(1,2),Q(1,3),Q(1,6)]
p1=sp.Matrix([w[x[0]]*(1+Q(1,4)*(2*x[1]-1)*(2*x[2]-1))/4 for x in states])
p2=sp.Matrix([w[x[0]]*(1-Q(1,4)*(2*x[1]-1)*(2*x[2]-1))/4 for x in states])
# Phi=w0^2+(3/2)w1^2-2w2, derivative (2w0,3w1,-2).
b=[2*w[0],3*w[1],-2];f=sp.Matrix([b[x[0]] for x in states]);mean=sum(w[i]*b[i] for i in range(3))
C=indicator(states,(0,));expected=sp.Matrix([-w[i]*(b[i]-mean) for i in range(3)])
check('nonlinear core Fisher objective closes on correlated full-support laws',
      M*p1==M*p2 and p1!=p2 and M*fisher(p1,f)==M*fisher(p2,f)
      and C*fisher(p1,f)==expected and any(v!=0 for v in expected),
      {'core_velocity':[str(v) for v in expected]})
check('Fisher mass gauge leaves the exact field unchanged',fisher(p1,f)==fisher(p1,f+7*sp.ones(len(states),1)))
leaf_f=sp.Matrix([2*x[1]-1 for x in states]);leaf2=sp.Matrix([2*x[2]-1 for x in states])
check('non-core objective detects omitted conditional interaction',
      leaf2.dot(fisher(p1,leaf_f))==Q(-1,4) and leaf2.dot(fisher(p2,leaf_f))==Q(1,4))
# Fixed-leaf likelihood criterion is log L in V, distinct from multiplier algebra.
# Positive unary likelihood on a leaf passes the multiplicative odds-ratio test but fails all-prior descent.
Ll=sp.Matrix([Q(1,4) if x[1]==0 else Q(3,4) for x in states])
q=bayes(p1,Ll)
def odds(p,c):
    idx={x:i for i,x in enumerate(states)}
    return sp.cancel(p[idx[c,0,0]]*p[idx[c,1,1]]/(p[idx[c,0,1]]*p[idx[c,1,0]]))
check('conditional leaf preservation does not imply all-prior marginal closure',
      all(odds(p1,c)==odds(q,c) for c in range(3))
      and constraints(M,N)*Ll!=sp.zeros(M.rows*N.rows,1)
      and M*bayes(p1,Ll)!=M*bayes(p2,Ll))

result={'status':'passed','assertion_groups':len(checks),'python':sys.version,'sympy':sp.__version__,
        'scope':'Independent bounded exact controls; no universal theorem inferred from enumeration.',
        'posterior_likelihood_grid_count':grid_cases,'checks':checks}
(HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'ALL {len(checks)} INDEPENDENT GROUPS PASSED')
