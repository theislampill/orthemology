"""Finite exact supplements to the written all-N Vandermonde proof."""
import sympy as s
for N in range(1,7):
 q=s.Rational(1,4)
 H=s.Matrix([[q**(-s.Rational((i+j)**2,2)) for j in range(N+1)] for i in range(N+1)])
 ratio=H.det()/H[1:,1:].det()
 assert s.simplify(ratio-s.prod(1-q**j for j in range(1,N+1)))==0
print('PASS six exact determinant-ratio controls; no verification credit for infinite-dimensional source theorems')
