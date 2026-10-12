"""Independent exact coefficient check and interval integration of B0, B1, B2.

This does not use the author's polynomial-square integration or saved numbers.
The finite numerical enclosure is conditional on mpmath interval arithmetic.
"""
import sys
import sympy as s
import mpmath
from mpmath import iv

x, B0, B1, B2, w_symbol = s.symbols('x B0 B1 B2 w')
c = s.Rational(17, 50)
p = 1 - c*x
assert s.Poly(s.expand(p*p), x).all_coeffs() == [s.Rational(289, 2500), -s.Rational(17, 25), 1]
G = s.Matrix([[B0-w_symbol, B1], [B1, B2]])
v = s.Matrix([1, -c])
Q = B0-s.Rational(17,25)*B1+s.Rational(289,2500)*B2-w_symbol
assert s.expand((v.T*G*v)[0]-Q) == 0
V = s.Matrix([50, -17])
assert s.expand((V.T*G*V)[0]-2500*Q) == 0
print('PASS: exact rational square coefficients and Hankel-form identities')

iv.dps = 70
I = iv.mpf
one = I(1)
time = one/10
q = iv.exp(-one)
partial = one
for j in range(1,65):
    partial *= one-q**j
remainder = q**65/(one-q)
mass = iv.make_mpf(((partial-remainder)._mpi_[0], partial._mpi_[1]))

M = 12
N = 16384
step = I(2*M)/N
root = iv.sqrt(2*iv.pi)
integrals = [I(0), I(0), I(0)]
for j in range(N):
    left = -I(M)+j*step
    right = -I(M)+(j+1)*step
    z = iv.make_mpf((left._mpi_[0],right._mpi_[1]))
    damped_gaussian = iv.exp(-time*iv.exp(z)-z*z/2)/root
    for r in range(3):
        integrals[r] += step*iv.exp(r*z)*damped_gaussian

moments = []
for r in range(3):
    u = I(M-r)
    v = I(M+r)
    tail = iv.exp(I(r*r)/2)*(iv.exp(-u*u/2)/u+iv.exp(-v*v/2)/v)/root
    moments.append(integrals[r]+iv.make_mpf((I(0)._mpi_[0],tail._mpi_[1])))

denominator = moments[0]-mass
objective = moments[0] - I(17)/25*moments[1] + I(289)/2500*moments[2] - mass
safe_margin = one-mass-2*time*iv.exp(one/2)
assert safe_margin > 0
assert denominator > 0
assert objective < -I(13)/400
print('Python:',sys.version.split()[0],'; SymPy:',s.__version__,'; mpmath:',mpmath.__version__)
print('Settings: 70 digits; 16384 cells; [-12,12]; 64 product factors')
for r, interval in enumerate(moments):
    print(f'B_{r}(1/10):', interval)
print('Infinite-product mass:',mass)
print('Denominator B0-w:',denominator)
print('Independent rational quadratic numerator:',objective)
print('PASS: upper endpoint < -13/400 = -0.0325; denominator positive')
print('Scope: finite algebra and conditional interval enclosure; no generic search implementation or kernel certificate')
