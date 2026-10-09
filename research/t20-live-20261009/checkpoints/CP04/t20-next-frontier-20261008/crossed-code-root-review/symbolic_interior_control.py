#!/usr/bin/env python3
"""Independent symbolic construction of the swapped-profile joint channel."""
import json
import sympy as s

a,b = s.symbols('a b')
def response(x,y):
    return (x,y,1-(1-x)*(1-y),x*y)
p,q = response(a,b),response(b,a)
channel = s.Matrix([[(1-x)*(1-y),(1-x)*y,x*(1-y),x*y] for x,y in zip(p,q)])
expected = (a-b)*(a+b-2*a*b)*((a-b)**2+2*a*b*(1-a)*(1-b))
difference = s.expand(channel.det()-expected)
assert difference == 0
# Marginal conversion is useful for a separate analytic rank argument.
transform = s.Matrix([[1,0,0,0],[1,0,1,0],[1,1,0,0],[1,1,1,1]])
assert (channel*transform-s.Matrix([[1,x,y,x*y] for x,y in zip(p,q)])).applyfunc(s.expand) == s.zeros(4)
assert transform.det() == -1
print(json.dumps({'status':'PASS','sympy_version':s.__version__,
                 'expanded_polynomial_difference':str(difference),
                 'row_order':['A','B','OR','AND'],
                 'column_order':['00','01','10','11'],
                 'marginal_transform_determinant':str(transform.det())},indent=2))
