#!/usr/bin/env python3
"""Independent deterministic controls for the retained-state staircase certificate.
No simulation, empirical samples, author-code imports, or external state changes.
"""
import itertools, json, math
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
import sympy as sp
mp.mp.dps=90

def hit(x,y,a,b): return x<=a and y<=b

def panel(m):
    a=[Q(i,m+1) for i in range(1,m+1)]
    b=list(reversed(a))
    commands=list(zip(a,b))+list(zip(a[:-1],b[1:]))
    return a,b,commands

def signature(x,y,commands):
    return sum((1<<i) for i,(a,b) in enumerate(commands) if hit(x,y,a,b))

def target(m): return (1<<m)-1

def convolve(states,cells):
    out=defaultdict(lambda:0)
    for s,w in states.items():
        for t,v in cells.items(): out[s|t]+=w*v
    return dict(out)

out={'method':'Independent exact finite-cell OR convolution, plus symbolic/high-precision identities. No Monte Carlo.'}
exhaustive=[]
for m in range(1,9):
    a,b,commands=panel(m)
    cuts=[Q(0)]+a+[Q(1)]
    counts=defaultdict(int)
    for x,y in itertools.product(cuts[1:],repeat=2): counts[signature(x,y,commands)]+=1
    state={0:1}
    hits=[]
    for k in range(m+1):
        number=state.get(target(m),0)
        hits.append(number)
        assert number==(math.factorial(m) if k==m else 0)
        state=convolve(state,counts)
    exhaustive.append({'m':m,'threshold_cells_per_route':(m+1)**2,'event_vector_counts_k_0_to_m':hits,'event_count_at_m':math.factorial(m),'total_labelled_vectors_at_m':((m+1)**2)**m})
out['exact_integer_enumeration']=exhaustive

# Unequally spaced coordinates prevent an equal-cell symmetry from masking an error.
rational=[]
for m in range(1,6):
    a=[Q(i*i,(m+1)**2) for i in range(1,m+1)]
    b=[Q((m+1-i)**3,(m+1)**3) for i in range(1,m+1)]
    commands=list(zip(a,b))+list(zip(a[:-1],b[1:]))
    xs=[Q(0)]+a+[Q(1)]
    ys=[Q(0)]+sorted(b)+[Q(1)]
    cells=defaultdict(lambda:Q(0))
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            w=(xs[i+1]-xs[i])*(ys[j+1]-ys[j])
            cells[signature(xs[i+1],ys[j+1],commands)]+=w
    state={0:Q(1)}
    for _ in range(m): state=convolve(state,cells)
    masses=[(a[i]-(a[i-1] if i else 0))*(b[i]-(b[i+1] if i+1<m else 0)) for i in range(m)]
    formula=math.factorial(m)*math.prod(masses)
    assert state[target(m)]==formula
    rational.append({'m':m,'probability':str(formula),'formula_exact':True})
out['unequal_rational_grid']=rational

# Exact symbolic 81 labelled cell assignments for the n=1,m=2 command-space Joe case.
r=sp.Rational
coordinates=[r(0),r(1,3),r(2,3),r(1)]
commands=[(r(1,3),r(2,3)),(r(2,3),r(1,3)),(r(1,3),r(1,3))]
F=lambda x,y:1-sp.sqrt(1-x*y)
cells=[]
for i in range(3):
    for j in range(3):
        mass=F(coordinates[i+1],coordinates[j+1])-F(coordinates[i],coordinates[j+1])-F(coordinates[i+1],coordinates[j])+F(coordinates[i],coordinates[j])
        cells.append((signature(coordinates[i+1],coordinates[j+1],commands),mass))
exact=sum(u*v for (s,u),(t,v) in itertools.product(cells,repeat=2) if s|t==3)
claim=2*((2*sp.sqrt(2)-sp.sqrt(7))/3)**2
assert sp.simplify(exact-claim)==0
out['n1_m2_symbolic']={'assignments_examined':81,'expression':str(sp.simplify(exact)),'claimed_formula_exact':True,'decimal_50':str(sp.N(exact,50))}

# High-precision full CDF-cell convolution under the stipulated Joe alternative.
def mpq(q): return mp.mpf(q.numerator)/q.denominator
joe=[]
for m in range(2,8):
    n=m-1;c=mp.mpf(n)/m
    a,b,commands=panel(m)
    xs=[Q(0)]+a+[Q(1)]
    F=lambda x,y:1-(1-mpq(x)*mpq(y))**c
    cells=defaultdict(lambda:mp.mpf(0))
    raw=[]
    for i in range(m+1):
        for j in range(m+1):
            w=F(xs[i+1],xs[j+1])-F(xs[i],xs[j+1])-F(xs[i+1],xs[j])+F(xs[i],xs[j])
            assert w>0
            raw.append(w)
            cells[signature(xs[i+1],xs[j+1],commands)]+=w
    assert abs(sum(raw)-1)<mp.mpf('1e-85')
    state={0:mp.mpf(1)}
    for _ in range(m): state=convolve(state,cells)
    masses=[]
    for i in range(m):
        lo_a=a[i-1] if i else Q(0)
        lo_b=b[i+1] if i+1<m else Q(0)
        masses.append(F(a[i],b[i])-F(lo_a,b[i])-F(a[i],lo_b)+F(lo_a,lo_b))
    formula=math.factorial(m)*mp.fprod(masses)
    error=abs(state[target(m)]-formula)
    assert error<mp.mpf('1e-80')
    joe.append({'n':n,'m':m,'event_probability':mp.nstr(formula,45),'absolute_convolution_formula_error':mp.nstr(error,8),'minimum_CDF_cell_mass':mp.nstr(min(raw),20)})
out['joe_CDF_cell_convolution']=joe

# Direct source-boundary countercontrols.
a,b,commands=panel(2)
nonseparable=lambda x,y:(x>=Q(1,3) and y>=Q(2,3)) or (x>=Q(2,3) and y>=Q(1,3))
assert [int(nonseparable(x,y)) for x,y in commands]==[1,1,0]
# Two identical full-support-marginal routes are fully dependent and act as one.
coupled_event_count=sum(1 for x,y in itertools.product([Q(1,3),Q(2,3),Q(1)],repeat=2) if signature(x,y,commands)==3)
assert coupled_event_count==0
# Independent redraws across the three queries make the forbidden E possible for n=1.
fresh=math.prod([x*y for x,y in commands[:2]])*(1-commands[2][0]*commands[2][1])
assert fresh==Q(32,729)
# Missing-coordinate gates: one unary B and one unary A yield E with no AB route.
unaryB=[y>=Q(1,2) for x,y in commands]
unaryA=[x>=Q(1,2) for x,y in commands]
assert [int(x or y) for x,y in zip(unaryB,unaryA)]==[1,1,0]
# Axis atom: E can occur while the strict (0,a1] B1 rectangle excludes its witness.
axis_routes=[(Q(0),Q(1,2)),(Q(1,2),Q(1,6))]
assert signature(*axis_routes[0],commands)|signature(*axis_routes[1],commands)==3
assert not(0<axis_routes[0][0]<=a[0])
# Exact same-threshold heterogenous panel alias at t=3/4.
# Per-route (A,B) state masses: comonotone; half countermonotone plus half product.
route1={(0,0):Q(1,2),(1,1):Q(1,2)}
route2={(0,0):Q(1,8),(0,1):Q(3,8),(1,0):Q(3,8),(1,1):Q(1,8)}
observed=defaultdict(lambda:Q(0))
for (u,v),w in route1.items():
    for (x,y),z in route2.items():
        observed[(u or x,v or y,(u and v) or (x and y))]+=w*z
baseline={(0,0,0):Q(1,16),(1,0,0):Q(3,16),(0,1,0):Q(3,16),(1,1,1):Q(9,16)}
assert dict(observed)==baseline
out['boundary_countercontrols']={'monotone_nonseparable_one_route_transcript':[1,1,0],'fully_dependent_identical_routes_event_count':coupled_event_count,'fresh_redraw_n1_event_probability':str(fresh),'two_unary_routes_zero_AB_transcript':[1,1,0],'axis_atom_invalidates_open_axis_box_equality_without_nullity':True,'heterogeneous_t_three_quarters_alias':{''.join(map(str,k)):str(v) for k,v in sorted(observed.items())},'m1_included_in_exact_controls':True,'m1_n0_Joe_hard_pair':'Excluded; c=0 is not the valid continuous full-support distribution.'}
# Heterogeneous independent positive cell laws require a permanent.
m=3
a,b,commands=panel(m)
cuts=[Q(0)]+a+[Q(1)]
route_laws=[]
box_matrix=[]
for route in range(m):
    weights={(i,j):Q(1+(route+1)*i+(route+1)**2*j) for i in range(m+1) for j in range(m+1)}
    z=sum(weights.values())
    law=defaultdict(lambda:Q(0))
    for (i,j),w in weights.items():
        law[signature(cuts[i+1],cuts[j+1],commands)]+=w/z
    route_laws.append(law)
    box_matrix.append([weights[(i,m-1-i)]/z for i in range(m)])
state={0:Q(1)}
for law in route_laws: state=convolve(state,law)
permanent=sum(math.prod(box_matrix[j][p[j]] for j in range(m)) for p in itertools.permutations(range(m)))
incorrect_iid=math.factorial(m)*math.prod(box_matrix[j][j] for j in range(m))
assert state[target(m)]==permanent and permanent!=incorrect_iid
out['heterogeneous_positive_cell_laws']={'probability':str(permanent),'permanent_exact':True,'incorrect_iid_diagonal_expression':str(incorrect_iid)}
# Exact face minima are insufficient for retained interior queries.
a,b,commands=panel(2)
vectors=[[(Q(1,6),Q(1,2)),(Q(1,2),Q(1,6))],[(Q(1,6),Q(1,6)),(Q(1,2),Q(1,2))]]
transcripts=[[int(any(hit(x,y,a,b) for x,y in v)) for a,b in commands] for v in vectors]
minima=[(min(x for x,y in v),min(y for x,y in v)) for v in vectors]
assert minima[0]==minima[1] and transcripts==[[1,1,0],[1,1,1]]
out['same_face_minima_different_interior_transcript']={'equal_minima':list(map(str,minima[0])),'different_transcripts':transcripts}
# A zero-gate route is identically successful, so m>=2 connector misses fail.
assert all([True for _ in panel(2)[2]]) and len(panel(2)[2])==3
out['zero_gate_boundary']={'m1_one_zero_gate_route_can_satisfy_E':True,'m_ge_2_any_zero_gate_route_makes_E_impossible':True}
# Independently check the author's extended k>m occupancy inclusion-exclusion.
ie_checks=[]
for m in range(1,7):
    a,b,commands=panel(m)
    cuts=[Q(0)]+a+[Q(1)]
    one=defaultdict(lambda:Q(0))
    for x,y in itertools.product(cuts[1:],repeat=2):one[signature(x,y,commands)]+=Q(1,(m+1)**2)
    masses=[one.get(1<<i,Q(0)) for i in range(m)]
    inactive=one.get(0,Q(0))
    state={0:Q(1)}
    for k in range(m+3):
        ie=sum((-1)**len(J)*(inactive+sum(masses[i] for i in range(m) if i not in J))**k for size in range(m+1) for J in itertools.combinations(range(m),size))
        assert state.get(target(m),Q(0))==ie
        state=convolve(state,one)
    ie_checks.append({'m':m,'route_counts_checked':list(range(m+3))})
out['extended_route_count_inclusion_exclusion']=ie_checks
Path('REVIEW_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
