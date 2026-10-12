"""Outward interval enclosure, not floating quadrature or a formal-kernel proof.
The analytic tail/rectangle bounds are explained in RESULT.md.
Requires mpmath; no external inputs or network.
"""
from mpmath import iv
import mpmath
iv.dps = 80
I = iv.mpf
zero, one = I(0), I(1)
t = one / 10
coef = -I(17) / 50
q = iv.exp(-one)
P = one
for j in range(1, 41):
    P *= one - q**j
err = q**41 / (one-q)
# The true infinite product is in [P_lower-error_upper, P_upper].
w = iv.make_mpf(((P-err)._mpi_[0], P._mpi_[1]))
# Normalization stays positive with the theorem's elementary lower bound.
safe_margin = one-w-I(2)*t*iv.exp(one/2)
assert safe_margin > 0
M = 10
root = iv.sqrt(2*iv.pi)
# p(e^z)^2 <= 2(1+(17/50)^2 exp(2z)); exponential damping <=1.
tail = zero
for k, c in [(0,one),(1,coef)]:
    shift = I(2*k)
    upper = I(M)-shift
    lower = I(M)+shift
    mills = iv.exp(-upper**2/2)/(root*upper) + iv.exp(-lower**2/2)/(root*lower)
    tail += 2*c**2*iv.exp(shift**2/2)*mills
# Rectangle enclosure: each interval range encloses every integrand value
# on that cell, so sum(width*range) encloses the compact integral.
N = 8192
step = I(2*M)/N
integral = zero
for j in range(N):
    lo = -I(M)+j*step
    hi = -I(M)+(j+1)*step
    z = iv.make_mpf((lo._mpi_[0], hi._mpi_[1]))
    x = iv.exp(z)
    p = one+coef*x
    f = iv.exp(-t*x-z**2/2)/root*p**2
    integral += step*f
objective = integral + iv.make_mpf((zero._mpi_[0],tail._mpi_[1])) - w
assert objective < 0
print('mpmath version:',mpmath.__version__)
print('interval decimal precision:',iv.dps)
print('time: 1/10; polynomial: 1 - 17*x/50')
print('infinite-product mass enclosure:',w)
print('safe-time lower-margin enclosure:',safe_margin)
print('absolute tail upper bound:',iv.make_mpf((zero._mpi_[0],tail._mpi_[1])))
print('compact integral enclosure:',integral)
print('full quadratic-form numerator enclosure:',objective)
print('PASS: strict negative upper bound; D(t)>0, so normalized Hankel form is negative.')
print('Scope: one rigorous interval control, conditional on mpmath interval arithmetic; not a formal-kernel certificate.')
