"""Exact algebraic diagnostic, not a causal ontology or original-agent model.

No actual-support, causal-route, perfection, or numerical-event-identity
relation is defined. Fractions and integer polynomial coefficients only.
"""
from fractions import Fraction as Q
import json

P = {(1,0):1,(0,1):1,(1,1):-3,(2,1):1,(1,2):1}

def evaluate(p,x,y):
    return sum((Q(c)*x**i*y**j for (i,j),c in p.items()), Q(0))

def derivative(p,axis):
    out={}
    for (i,j),c in p.items():
        n=(i,j)[axis]
        if n:
            k=(i-1,j) if axis==0 else (i,j-1)
            out[k]=out.get(k,0)+n*c
    return out

def f(x,y): return evaluate(P,Q(x),Q(y))

def nonnegative_basis(x,y):
    x,y=Q(x),Q(y)
    return x*(1-y)**2+y*(1-x)**2+x*y

def path_integral_derivative(a,b):
    # F(1,y)=1-y+y^2. Exact primitive of derivative -1+2y.
    a,b=Q(a),Q(b)
    return (-b+b*b)-(-a+a*a)

DX=derivative(P,0)
DY=derivative(P,1)
# Independently expected coefficient dictionaries.
assert DX=={(0,0):1,(0,1):-3,(1,1):2,(0,2):1}
assert DY=={(0,0):1,(1,0):-3,(2,0):1,(1,1):2}
assert all(P.get((j,i),0)==c for (i,j),c in P.items())
assert f(0,0)==0
assert f(1,0)==f(0,1)==f(1,1)==1
assert evaluate(DX,Q(1),Q(1))==evaluate(DY,Q(1),Q(1))==1
assert f(1,Q(1,2))==Q(3,4)
assert evaluate(DY,Q(1),Q(1,4))==-Q(1,2)
assert evaluate(DY,Q(1),Q(3,4))==Q(1,2)
assert path_integral_derivative(0,1)==0
assert path_integral_derivative(0,Q(1,2))==-Q(1,4)
assert path_integral_derivative(Q(1,2),1)==Q(1,4)
assert evaluate(DX,Q(9,10),Q(9,10))==Q(73,100)
# On [9/10,1]^2, DX increases in x and y:
# d(DX)/dx = 2y >= 9/5; d(DX)/dy = -3+2x+2y >= 3/5.
# The same argument holds symmetrically for DY. This proves (not samples)
# the lower bound 73/100 for both partial derivatives on that square.
assert derivative(DX,0)=={(0,1):2}
assert derivative(DX,1)=={(0,0):-3,(1,0):2,(0,1):2}
# The factored identity is exact by polynomial expansion, with this grid
# included only as an independent arithmetic check, not its proof.
for i in range(11):
    for j in range(11):
        x,y=Q(i,10),Q(j,10)
        assert f(x,y)==nonnegative_basis(x,y)
        assert f(x,y)>=0
# Effect-profile lift: any fixed nonzero H is unchanged at these corners.
H=(Q(1),Q(2),Q(3,2))
profiles={name:tuple(f(x,y)*h for h in H) for name,x,y in [('solo_a',1,0),('solo_b',0,1),('joint',1,1)]}
assert profiles['solo_a']==profiles['solo_b']==profiles['joint']==H

result={
 'status':'PASS',
 'scope':'Exact response-algebra diagnostic only; no actual causal support or complete ontology certified.',
 'polynomial':'F(x,y)=x+y-3xy+x^2*y+x*y^2',
 'equivalent_nonnegative_basis':'x*(1-y)^2+y*(1-x)^2+x*y',
 'corner_values':{str(k):str(f(*k)) for k in [(0,0),(1,0),(0,1),(1,1)]},
 'local_partials_at_joint':['1','1'],
 'neighbourhood':'[9/10,1]^2',
 'proved_lower_bound_for_both_partials':'73/100',
 'addition_path':'F(1,y)=1-y+y^2',
 'path_derivative':'-1+2y',
 'path_minimum':{'y':'1/2','value':'3/4'},
 'integrated_changes':{'[0,1/2]':'-1/4','[1/2,1]':'1/4','[0,1]':'0'},
 'profile_lift':{k:[str(v) for v in vs] for k,vs in profiles.items()},
 'unproved':['genuine actual causation','wise admissibility of interventions','numerical transworld identity','complete created-effect inventory','multiple perfected original bearers'],
}
print(json.dumps(result,indent=2))
