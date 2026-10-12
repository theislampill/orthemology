"""Exact independent positive and negative controls for fixed grouped audits."""
import sympy as s

w1, w2, w3 = s.symbols('w1 w2 w3', positive=True)
x1, x2, x3 = s.symbols('x1 x2 x3', real=True)
a, b, alpha = s.symbols('a b alpha', positive=True)
w = s.Matrix([w1, w2, w3])
x = s.Matrix([x1, x2, x3])
E = w1*w2/(w1+w2)*(x1-x2)**2
p = s.Matrix([s.diff(E, z) for z in w])
avg = (w.T*p)[0]
F = s.Matrix([-alpha*w[i]*(p[i]-avg) for i in range(3)])
v = s.Matrix([-s.diff(E, x[i])/w[i] for i in range(3)])
Z = a*(w1+w2)+b*w3
T = s.Matrix([a*w1/Z, a*w2/Z, b*w3/Z])
sub = dict(zip(w, T))
weight_residual = s.simplify(F.subs(sub, simultaneous=True)-T.jacobian(w)*F)
position_residual = s.simplify(v.subs(sub, simultaneous=True)-v)
assert all(s.factor(q.subs(w3, 1-w1-w2)) == 0 for q in weight_residual)
assert all(s.factor(q) == 0 for q in position_residual)
print('GROUPED symbolic weight residual:', list(weight_residual))
print('GROUPED symbolic position residual:', list(position_residual))
base = {w1:s.Rational(1,3), w2:s.Rational(1,3), w3:s.Rational(1,3),
        x1:0, x2:1, x3:2, alpha:1}
single = {w1:s.Rational(1,2), w2:s.Rational(1,4), w3:s.Rational(1,4),
          x1:0, x2:1, x3:2, alpha:1}
S = s.Matrix([2*w1/(2*w1+w2+w3), w2/(2*w1+w2+w3), w3/(2*w1+w2+w3)])
actual_v = v.subs(single)
pushed_v = v.subs(base)
actual_F = F.subs(single)
pushed_F = (S.jacobian(w)*F).subs(base)
assert actual_v == s.Matrix([s.Rational(2,3), -s.Rational(4,3), 0])
assert pushed_v == s.Matrix([1,-1,0])
assert actual_v != pushed_v and actual_F != pushed_F
print('SINGLETON actual position field:', list(actual_v))
print('SINGLETON pushed position field:', list(pushed_v))
print('SINGLETON actual weight field:', list(actual_F))
print('SINGLETON pushed weight field:', list(pushed_F))
print('PASS: grouped covariance; FAILS as expected: singleton covariance.')
