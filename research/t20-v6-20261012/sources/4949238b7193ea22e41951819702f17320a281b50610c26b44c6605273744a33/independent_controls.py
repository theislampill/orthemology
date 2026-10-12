"""Independent exact controls for the leafwise Fisher geometry review.

Written from the reviewer's reconstruction, without importing the author's
verification program. Finite checks support, but do not replace, the proofs.
"""
from itertools import product, combinations
from pathlib import Path
import json
import platform
import sympy as S

Q = S.Rational
out = {}


def check(name, condition, details=None):
    assert bool(condition), (name, details)
    out[name] = {"passed": True, "details": details}


def zero(matrix):
    return all(S.simplify(e) == 0 for e in matrix)


def interaction_rows(alphabets, order):
    states = list(product(*(range(n) for n in alphabets)))
    rows = [[S.Integer(1)] * len(states)]
    # Independent categorical contrast basis e_j - e_last on each slot.
    for degree in range(1, order + 1):
        for slots in combinations(range(len(alphabets)), degree):
            for js in product(*(range(alphabets[i] - 1) for i in slots)):
                row = []
                for x in states:
                    val = S.Integer(1)
                    for i, j in zip(slots, js):
                        val *= int(x[i] == j) - int(x[i] == alphabets[i] - 1)
                    row.append(val)
                rows.append(row)
    return S.Matrix(rows)


def stabilizer_basis(M):
    """Solve h dot (v*f)=0 for all null directions h and retained rows v."""
    equations = []
    for h in M.nullspace():
        for row in M.tolist():
            equations.append([sum(h[x] * row[x] * M[j, x]
                                  for x in range(M.cols))
                              for j in range(M.rows)])
    E = S.Matrix(equations) if equations else S.zeros(0, M.rows)
    coeffs = E.nullspace()
    return [M.T * c for c in coeffs], E.rank()


for alphabets, order, expected in [
    ((2, 2), 1, 1), ((2, 2, 2), 1, 1), ((2, 2, 2), 2, 1),
    ((2, 3), 1, 1), ((2, 3, 2), 2, 1), ((2, 2), 2, 4),
    ((2, 3), 2, 6), ((2, 3), 0, 1),
]:
    M = interaction_rows(alphabets, order)
    basis, rank = stabilizer_basis(M)
    check(f"stabilizer_{alphabets}_order_{order}", len(basis) == expected,
          {"states": M.cols, "observable_dimension": M.rows,
           "constraint_rank": rank, "stabilizer_dimension": len(basis)})

states = list(product((-1, 1), repeat=2))
x = S.Matrix([i for i, j in states])
y = S.Matrix([j for i, j in states])
one = S.ones(4, 1)
xy = x.multiply_elementwise(y)
M = S.Matrix.vstack(one.T, x.T, y.T)
u, v, c, cp = S.symbols("u v c cp", real=True)
a, b, gauge = S.symbols("a b gauge", real=True)
p = (one + u*x + v*y + c*xy)/4
q = p.subs(c, cp)
g = S.Matrix([gauge, a, b])
f = M.T*g


def fine_velocity(p, f):
    return -S.diag(*p)*f + p*(p.dot(f))


vel = fine_velocity(p, f)
momvel = S.simplify(M*vel)
cov = S.Matrix([[1-u*u, c-u*v], [c-u*v, 1-v*v]])
check("two_bit_moments", zero(M*p - S.Matrix([1, u, v])))
check("two_bit_covariance_field", zero(momvel - S.Matrix([0, *(-cov*S.Matrix([a,b]))])))
check("mass_gauge_cancels", zero(vel.diff(gauge)))
check("local_fibre_identity", zero(M*(vel-fine_velocity(q, f)) + M*S.diag(*f)*(p-q)))
check("whole_fibre_fixed_objective", zero((M*(vel-fine_velocity(q,f)))[1:, :] + (c-cp)*S.Matrix([b,a])),
      {"difference": [str(e) for e in S.simplify(M*(vel-fine_velocity(q,f)))]})
check("two_bit_null_direction", zero(M*xy))


def expectation(p, f):
    return S.simplify(p.dot(f))


def posterior(p, L):
    numerator = p.multiply_elementwise(L)
    return S.simplify(numerator/sum(numerator))


def odds(p):
    # --, -+, +-, ++ ordering
    return S.factor(p[0]*p[3]/(p[1]*p[2]))


for rho in (Q(1,2), Q(-1,2)):
    r = (one + rho*xy)/4
    C = S.Matrix([[1, rho], [rho, 1]])
    check(f"center_velocity_{rho}", zero((M*fine_velocity(r,x))[1:, :] - S.Matrix([-1,-rho])))
    check(f"center_cometric_inverse_{rho}", C.det() == Q(3,4) and zero(C*C.inv()-S.eye(2)),
          {"cometric": str(C), "metric": str(C.inv()), "odds_ratio": str(odds(r))})
    # Time t=log(2), so exp(-t*x) = 2**(-x), entirely rational.
    rt = posterior(r, S.Matrix([S.Integer(2)**(-xx) for xx, yy in states]))
    check(f"linear_trajectory_at_log_two_{rho}",
          zero((M*rt)[1:, :] - S.Matrix([-Q(3,5), -Q(3,5)*rho])) and odds(rt) == odds(r))
    event = (one + x/2)/2
    re = posterior(r, event)
    check(f"local_event_preserves_leaf_{rho}", odds(re) == odds(r)
          and expectation(r,event)==Q(1,2)
          and zero((M*re)[1:, :] - S.Matrix([Q(1,2),rho/2])))

r = (one + xy/2)/4
L = (one + x/3).multiply_elementwise(one+y/4)
rt = posterior(r, L)
check("correlated_leaf_raw_moment_moves", odds(rt)==9
      and expectation(rt,x)==Q(11,25)
      and expectation(rt,y)==Q(2,5)
      and expectation(rt,xy)==Q(14,25),
      {"law": [str(z) for z in rt], "means": ["11/25", "2/5"],
       "raw_interaction": "14/25", "odds_ratio": "9"})
means = S.Matrix([expectation(rt,x), expectation(rt,y)])
Phi = S.Matrix.hstack(x,y)
centered = Phi - one*means.T
D = S.diag(*rt)*centered
C = S.simplify(centered.T*S.diag(*rt)*centered)
check("leaf_pullback_fisher_metric", zero(D.T*S.diag(*(1/z for z in rt))*D-C))
check("leaf_gradient_is_full_gradient", zero(fine_velocity(rt,a*x+b*y)+D*S.Matrix([a,b])))
check("mean_metric_inverse", zero((D*C.inv()).T*S.diag(*(1/z for z in rt))*(D*C.inv())-C.inv()))
check("fibre_leaf_fisher_orthogonality", zero(D.T*S.diag(*(1/z for z in rt))*xy))

Lbad = one + (x+y)/4
bad = posterior(one/4,Lbad)
check("likelihood_in_V_not_leaf_preserving", all(z>0 for z in Lbad)
      and M.col_join(Lbad.T).rank() == M.rank()
      and xy.dot(Lbad)==0 and odds(bad)==Q(3,4))
check("bad_likelihood_valid_event_rescaling", all(0<z<=1 for z in Q(2,3)*Lbad)
      and zero(posterior(one/4,Q(2,3)*Lbad)-bad))
check("bad_likelihood_mixed_log_coefficient", S.simplify(S.log(odds(bad))/4-S.log(Q(3,4))/4)==0)
psi = sum(((1+z)*S.log(1+z)+(1-z)*S.log(1-z))/2 for z in (u,v))
check("product_dual_hessian", zero(S.hessian(psi,(u,v))-S.diag(1/(1-u*u),1/(1-v*v))))
check("unbounded_gradient_can_hit_boundary_in_finite_time",
      zero(-S.diag(1-u*u,1-v*v)*S.Matrix([-1/(1-u*u),0])-S.Matrix([1,0])),
      {"objective": "J(u,v)=-atanh(u)", "initial_mean": [0,0],
       "exact_mean_curve": ["t",0], "positive_interior_interval": "0 <= t < 1"})

# Five-state mixed block: 1_X, 1_B, x*1_B, y*1_B.
MB = S.Matrix([[1,1,1,1,1], [1,1,1,1,0], [*x,0], [*y,0]])
bas, rank = stabilizer_basis(MB)
check("mixed_block_stabilizer", len(bas)==2,
      {"constraint_rank": rank, "stabilizer_dimension": len(bas),
       "basis": [[str(e) for e in z] for z in bas]})
expected_block_space = S.Matrix([[1,0],[1,0],[1,0],[1,0],[0,1]])
check("mixed_block_stabilizer_span", S.Matrix.hstack(*bas, *expected_block_space.columnspace()).rank()==2)
w = S.symbols("w", real=True)
pb = S.Matrix([*p, 0])*w + S.Matrix([0,0,0,0,1-w])
fw = S.Matrix([1,1,1,1,0])
mw = S.simplify(MB*fine_velocity(pb,fw))
check("mixed_block_allowed_objective", zero(mw-S.Matrix([0,-w*(1-w),-w*u*(1-w),-w*v*(1-w)])))
vals=[]
for rho in (Q(1,2),Q(-1,2)):
    pbr = pb.subs({u:0,v:0,c:rho,w:Q(1,2)})
    vb = MB*fine_velocity(pbr,S.Matrix([*x,0]))
    vals.append(vb[3])
check("mixed_block_disallowed_objective", vals==[-Q(1,4),Q(1,4)], {"v_velocity": [str(t) for t in vals]})

# This cone is generated by endpoints; its diagonal observable stabilizer is scalar.
Mcone = S.Matrix([[1,1,1],[-1,0,1]])
bas, rank = stabilizer_basis(Mcone)
left = S.Matrix([[Q(1,2),-Q(1,2)],[-Q(1,2),Q(1,2)]])
right = S.eye(2)-left
check("stabilizer_blocks_not_cone_components", len(bas)==1
      and zero(left*left-left) and zero(right*right-right)
      and zero(left*Mcone[:,0]-Mcone[:,0]) and zero(left*Mcone[:,2])
      and zero(right*Mcone[:,2]-Mcone[:,2]) and zero(right*Mcone[:,0]),
      {"stabilizer_dimension": 1, "cone_extreme_rays": [[1,-1],[1,1]],
       "positive_cone_projections": [str(left),str(right)]})

record = {"purpose": "independent bounded exact controls; no universal proof by enumeration",
          "python": platform.python_version(), "sympy": S.__version__,
          "assertions": len(out), "all_passed": True, "checks": out}
Path(__file__).with_name("INDEPENDENT_CONTROL_RESULTS.json").write_text(json.dumps(record,indent=2)+"\n")
print(f"PASS: {len(out)} independently reconstructed exact controls")
print(f"Python {record['python']}; SymPy {record['sympy']}")
