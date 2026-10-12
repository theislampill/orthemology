"""Exact algebra controls for an ordinary analytic theorem, not kernel proof."""
from fractions import Fraction as Q
import json

counts = {}
finite_rows = []
for k in range(1, 33):
    x = Q(k, 64)
    b = (x, Q(1, 2)+x*x/2, Q(1, 2)+x*x/2)
    z = sum(b)
    h = (x, Q(1), Q(1))
    v = tuple((1-z)/hi for hi in h)
    assert z == 1+x+x*x
    assert v[0] == -1-x
    assert v[1] == v[2] == x*v[0]
    alpha = (Q(1,8), Q(5,8), Q(5,8))
    dual = (x*x/2, b[1], b[2])
    shift = dual[0]-alpha[0]
    assert all(dual[i]-alpha[i] == shift for i in range(3))
    assert Q(-1,8) < shift <= 0
    for j in range(3):
        gain = sum(h[i]*(b[i]-(1 if i==j else 0))*v[i] for i in range(3))
        assert gain == -(z-1)**2
    S = 1/x+2
    tau_dot = -(1+2*x)*v[0]/(z-1)
    assert tau_dot == S
    assert all(0<bi<1 for bi in b)
counts['finite_coherent_boundary_exact_points'] = 32
finite_rows.append({'initial':['1/2','5/8','5/8'], 'endpoint':['0','1/2','1/2'],
                    'exact_time':'log(3/2)', 'x_field':'-1-x',
                    'travel_time_integrand_after_substitution':'1/(1+x)',
                    'normalized_time_limit':'+infinity'})

for k in range(1, 33):
    x = Q(k,128)
    b = (x,Q(1,2)+x,Q(1,2)+x)
    v = tuple(1-sum(b) for _ in b)
    assert v == (-3*x,)*3
    assert sum(b)-1 == 3*x
    assert all(0<bi<1 for bi in b)
counts['infinite_coherent_boundary_exact_points'] = 32

# Constant-curvature strict residual: first boundary after common shift 1/100.
b = (Q(1,100),Q(4,5),Q(4,5))
r0 = sum(b)-1
shift = Q(1,100)
c = tuple(bi-shift for bi in b)
assert c == (0,Q(79,100),Q(79,100))
rb = sum(c)-1
assert rb == Q(29,50)
assert rb/r0 == Q(58,61)
counts['strict_residual_boundary'] = 1

logistic = []
for a in (Q(1,3),Q(1),Q(7,2)):
    for b0 in ((Q(1,10),Q(1,5),Q(3,10)),
               (Q(1,5),Q(3,10),Q(1,2)),
               (Q(1,2),Q(3,4),Q(2,3))):
        z0 = sum(b0)
        p = tuple(bi/z0 for bi in b0)
        for j in range(1, 33):
            w = Q(j,32)  # w=exp(-a*t), t>=0.
            den = z0+(1-z0)*w
            z = z0/den
            dz_dw = -z0*(1-z0)/(den*den)
            zdot = dz_dw*(-a*w)
            assert zdot == a*z*(1-z)
            b = tuple(pi*z for pi in p)
            v = tuple(a*(1-z)*bi for bi in b)
            assert sum(v) == zdot
            assert all(v[i] == p[i]*zdot for i in range(3))
            assert all(0<bi<1 for bi in b)
counts['entropy_logistic_exact_points'] = 3*3*32

print(json.dumps({
    'status':'PASS',
    'scope':'finite exact algebra controls; general theorem is ordinary proof',
    'counts':counts,
    'finite_boundary_control':finite_rows,
    'asymptotic_control':{'initial':['1/4','3/4','3/4'],'x_field':'-3*x',
                         'endpoint':['0','1/2','1/2'],'exact_time':'+infinity'},
    'strict_boundary_control':{'residual_initial':str(r0),'residual_boundary':str(rb),
                               'exp_minus_3t':str(rb/r0),'time':'log(61/58)/3'}
}, indent=2))

