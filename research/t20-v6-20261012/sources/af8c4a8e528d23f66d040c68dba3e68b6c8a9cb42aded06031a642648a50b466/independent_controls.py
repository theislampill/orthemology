"""Independent finite algebra review; does not prove the analytic/topological claims."""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import json
import sympy as s

checks = []

def check(label, condition):
    assert condition, label
    checks.append(label)

def binary_output_jets(b):
    r = sum(b) - 1
    mobility = sum(x * (1-x) for x in b)
    cubic = sum(x * (1-x) * (1-2*x) for x in b)
    return sum(b), -r*mobility, r*mobility**2 + r**2*cubic

a = (Q(1,5), Q(2,5), Q(4,5))
b = (Q(3,10), Q(1,2), Q(3,5))
Sa = sum(x*(1-x) for x in a)
Sb = sum(x*(1-x) for x in b)
check('flow clock-control sums', sum(a) == sum(b) == Q(7,5))
check('flow clock-control mobility', (Sa,Sb) == (Q(14,25),Q(7,10)))
check('flow clock-control original derivatives', (binary_output_jets(a)[1],binary_output_jets(b)[1]) == (Q(-28,125),Q(-7,25)))
check('flow clock-control normalized loss', (-(sum(a)-1)**2/Sa, -(sum(b)-1)**2/Sb) == (Q(-2,7),Q(-8,35)))

a = (Q(1,10),Q(1,2),Q(3,5))
b = (Q(1,5),Q(3,10),Q(7,10))
ja,jb = binary_output_jets(a),binary_output_jets(b)
check('same z and first derivative', ja[:2] == jb[:2] == (Q(6,5),Q(-29,250)))
check('different second derivative independently factored', (ja[2],jb[2]) == (Q(853,12500),Q(889,12500)))

qa = (Q(1,100),Q(4,5),Q(4,5))
qb = (Q(161,300),)*3
check('same-sum lifetime separator', sum(qa) == sum(qb) == Q(161,100))
e = Q(58,61)  # exp(-3 t_exit)
r0 = sum(qa)-1
at_exit = tuple(x-r0*(1-e)/3 for x in qa)
check('quadratic first exit', at_exit == (0,Q(79,100),Q(79,100)))
check('quadratic sum at exit', sum(at_exit) == Q(79,50))
check('symmetric counterpart positive limiting coordinates', all(x-r0/3 == Q(1,3) for x in qb))

for n in range(1,5):
    x = s.symbols('x:'+str(n))
    z = sum(x)
    field = [-(z-1)*u*(1-u) for u in x]
    def lie(expr):
        return s.expand(sum(s.diff(expr,u)*v for u,v in zip(x,field)))
    for k in range(1,5):
        pk = sum(u**k for u in x)
        pk1 = sum(u**(k+1) for u in x)
        check(f'moment hierarchy n={n}, k={k}', s.expand(lie(pk)-k*(z-1)*(pk1-pk)) == 0)
    if n <= 3:
        jet = [z]
        for k in range(1,n):
            jet.append(lie(jet[-1]))
        determinant = s.Matrix(jet).jacobian(x).det()
        expected = s.prod(factorial(k) for k in range(1,n+1)) * (z-1)**(n*(n-1)//2) * s.prod(x[j]-x[i] for i in range(n) for j in range(i+1,n))
        check(f'direct state-coordinate observability determinant n={n}', s.expand(determinant-expected) == 0)

result = {'status':'PASS','check_count':len(checks),'checks':checks,
          'scope':'Finite rational and symbolic checks only. No kernel execution, global ODE proof, arbitrary-dimension induction proof, or topology proof is inferred from these controls.'}
Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
