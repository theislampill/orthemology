#!/usr/bin/env python3
"""Independent exact algebra controls; not a proof of the analytic theorem."""
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
checks = []

def eq(name, expression):
    residual = S.factor(S.trigsimp(S.expand(expression)))
    if residual != 0:
        raise AssertionError((name, residual))
    checks.append({"name": name, "status": "pass"})

def truth(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append({"name": name, "status": "pass"})

# Independent coordinate expansions supplement the all-dimension chain-rule proof.
for d in range(1, 5):
    xs = S.symbols(f"x0:{d}")
    R = sum(x*x for x in xs)
    for n in range(1, 6):
        eq(f"radial_laplacian_d{d}_n{n}",
           sum(S.diff(R**n, x, 2) for x in xs)
           - 2*n*(2*n+d-2)*R**(n-1))
    for k in range(1, 4):
        fs = [x*R**(k-1) for x in xs]
        gs = [x*R**k for x in xs]
        eq(f"even_CS_left_d{d}_k{k}", sum(f*f for f in fs)-R**(2*k-1))
        eq(f"even_CS_middle_d{d}_k{k}", sum(f*g for f,g in zip(fs,gs))-R**(2*k))
        eq(f"even_CS_right_d{d}_k{k}", sum(g*g for g in gs)-R**(2*k+1))
    for n in range(1, 6):
        for x in xs:
            coeffs = S.Poly(S.expand(R**n-x**(2*n)), *xs).terms()
            truth(f"radial_coordinate_SOS_d{d}_n{n}_{x}",
                  all(co >= 0 and all(e % 2 == 0 for e in mon) for mon,co in coeffs))

t, tau, b, n, d = S.symbols("t tau b n d", positive=True)
Y = S.sqrt(b)*S.coth(S.sqrt(b)*(t-tau)/n)
eq("riccati_coth_exact_solution", S.trigsimp(S.diff(Y,t)-(b-Y**2)/n))
w = S.symbols("w", positive=True)
eq("coth_monotonicity_numerator_derivative",
   S.diff(S.sinh(w)*S.cosh(w)-w,w)-2*S.sinh(w)**2)
eq("dimension_constant_ratio", 2*n*(2*n+d-2)/n**2-(4+(2*d-4)/n))

# Harmonic-oscillator kernel and endpoint Fourier formula, symbolic dimension.
v,c,C,Rx,Ry,Z,A,B = S.symbols("v c C Rx Ry Z A B", real=True)
eq("Gaussian_completion_of_square",
   S.rem(S.together(-v*Ry/2-(Rx-2*c*Z+c*c*Ry)/(2*v)
                     -(-Rx/(2*v)-Ry/(2*v)+c*Z/v)).as_numer_denom()[0],
         S.Poly(c*c+v*v-1,c),c))
fourier_time = -d*v-c*c*(Rx+Ry)-2*S.I*c*v*Z
fourier_generator = -d*v+v*v*Rx-2*S.I*c*v*Z-c*c*Ry-Rx
eq("Fourier_Mehler_PDE",
   S.rem(fourier_time-fourier_generator,S.Poly(c*c+v*v-1,c),c))
kernel_time = -d*A+B*B*(Rx+Ry)-2*A*B*Z
kernel_generator = -d*A+A*A*Rx-2*A*B*Z+B*B*Ry-Rx
eq("spatial_Mehler_PDE",
   S.rem(kernel_time-kernel_generator,S.Poly(A*A-B*B-1,A),A))
eq("maximum_principle_barrier",
   2*d*(1+Rx)-2*d+Rx*(1+Rx)-((2*d+1)*Rx+Rx*Rx))

def moment(k,y):
    if k < 0:
        return S.Integer(0)
    return S.expand(sum(S.factorial(k)/(S.factorial(k-2*j)*S.factorial(j)*2**j)
                        *(c*y)**(k-2*j)*v**j for j in range(k//2+1)))

y,z = S.symbols("y z", real=True)
for k in range(11):
    P = moment(k,y)
    derivative = (-v-c*c*y*y)*P-2*c*v*S.diff(P,c)+2*c*c*S.diff(P,v)
    expected = k*(k-1)*moment(k-2,y)-moment(k+2,y)
    eq(f"unnormalized_moment_1d_degree{k}",
       S.rem(S.expand(derivative-expected),S.Poly(c*c+v*v-1,c),c))
for k,l in [(0,0),(1,1),(2,1),(2,2),(3,3),(4,2),(5,1)]:
    P=moment(k,y)*moment(l,z)
    derivative=(-2*v-c*c*(y*y+z*z))*P-2*c*v*S.diff(P,c)+2*c*c*S.diff(P,v)
    expected=(k*(k-1)*moment(k-2,y)*moment(l,z)
              +l*(l-1)*moment(k,y)*moment(l-2,z)
              -moment(k+2,y)*moment(l,z)-moment(k,y)*moment(l+2,z))
    eq(f"unnormalized_moment_2d_{k}_{l}",
       S.rem(S.expand(derivative-expected),S.Poly(c*c+v*v-1,c),c))

# Negative controls retain the failed pure-killing transplants.
a0 = S.cosh(2*t)**(-d/2)
a1 = d*S.tanh(2*t)*a0
eq("delta0_positive_radial_derivative", S.diff(a1,t).subs(t,0)-2*d)
eq("delta0_negative_even_mass_derivative", S.diff(a0,t,2).subs(t,0)+2*d)

summary = {
    "status": "pass", "exact_checks": len(checks), "checks": checks,
    "proof_boundary": "Exact finite algebra controls only; universal analytic conclusions are independently assessed in REVIEW.md.",
    "sympy_version": S.__version__,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(ROOT/"INDEPENDENT_RESULTS.json").write_text(json.dumps(summary,indent=2)+"\n")
print(f"PASS: {len(checks)} independently authored exact algebra controls")
