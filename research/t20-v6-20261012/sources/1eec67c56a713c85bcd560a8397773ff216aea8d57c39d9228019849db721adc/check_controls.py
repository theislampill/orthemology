"""Exact algebraic controls only; the universal measure proof is in RESULT.md."""
import sympy as s
k, r = s.symbols('k r', integer=True)
assert s.simplify(r*k-k*k/2 - (r*r/2-(k-r)**2/2)) == 0
print('PASS: exact discrete-moment index-shift exponent identity')
A0, A1, Ar, Ar1 = s.symbols('A0 A1 Ar Ar1')
quotient_derivative = (-Ar1*A0+Ar*A1)/A0**2
hierarchy = -Ar1/A0+(A1/A0)*(Ar/A0)
assert s.simplify(quotient_derivative-hierarchy) == 0
print('PASS: exact normalized hierarchy quotient identity')
t, eps, Bnext = s.symbols('t eps Bnext')
assert s.simplify((-Bnext-s.diff(eps*s.exp(-t),t))-(-Bnext+eps*s.exp(-t))) == 0
print('PASS: negative-atom term respects A_r prime = -A_(r+1)')
print('Scope: finite exact algebra checks; no sampling, universal positivity, or measure reconstruction claim.')
