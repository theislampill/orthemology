#!/usr/bin/env python3
"""Independent symbolic transport controls for the final author packet."""
from itertools import product
from pathlib import Path
import hashlib,json
import sympy as s

root=Path(__file__).resolve().parent
X=list(product(range(2),repeat=4))
Z=list(product(range(2),repeat=3))
audits=list(product(range(2),repeat=2))
G=s.Matrix([[int((th,t,int(v!=y))==z) for th,t,y,v in X] for z in Z])
C=s.Matrix([[int(th==k) for th,t,y,v in X] for k in range(2)])
L=s.Matrix([[int(th==k) for th,t,d in Z] for k in range(2)])
assert G.rank()==8 and L*G==C
Ms=[]
for a in audits:
    M=s.diag(*[int((t,int(v!=y))==a) for th,t,y,v in X])
    P=s.diag(*[int((t,d)==a) for th,t,d in Z])
    assert G*M==P*G
    Ms.append(M)
assert sum(Ms,s.zeros(16))==s.eye(16)
Y=[s.diag(*[int(y==k) for th,t,y,v in X]) for k in range(2)]
rank8=s.Matrix.vstack(*[C*M for M in Ms]).rank()
rank16=s.Matrix.vstack(*[C*M*R for M in Ms for R in Y]).rank()
assert (rank8,rank16)==(8,16)

P4=list(product(range(2),repeat=2))
W=s.Matrix([[1]*4,[(-1)**th for th,d in P4],
            [(-1)**d for th,d in P4],[(-1)**(th+d) for th,d in P4]])
assert W.inv()==W.T/4
m,t,d,h=s.symbols('m t d h')
z=s.Matrix([m,t,d,h])
for b in range(2):
    sign=(-1)**b
    D=s.diag(*[int(dd==b) for th,dd in P4])
    T=W*D*W.inv()
    assert T*z==s.Matrix([(m+sign*d)/2,(t+sign*h)/2,
                         sign*(m+sign*d)/2,sign*(t+sign*h)/2])
    assert T*W==W*D
    assert D*D==D
    assert D*s.diag(*[int(dd!=b) for th,dd in P4])==s.zeros(4)
bad=W.inv()*s.Matrix([1,0,0,2])
assert tuple(bad)==(s.Rational(3,4),-s.Rational(1,4),-s.Rational(1,4),s.Rational(3,4))

alpha=s.symbols('alpha',real=True)
rho=2*alpha-1
for y in range(2):
    pi=s.Matrix([(1+rho*(-1)**(th+y+dd))/4 for th,dd in P4])
    assert s.simplify(sum(pi))==1
    assert W*pi==s.Matrix([1,0,0,(-1)**y*rho])
    post=s.simplify(pi[3]/(pi[1]+pi[3]))
    assert post==(alpha if y==0 else 1-alpha)
fresh_twice=(1-alpha)**2/((1-alpha)**2+alpha**2)
assert fresh_twice.subs(alpha,s.Rational(4,5))==s.Rational(1,17)

tau,q0,q1=s.symbols('tau q0 q1')
q=(1-tau)*q0+tau*q1
signature=s.Matrix([q,q0,q1])
jacobian=s.factor(signature.jacobian([tau,q0,q1]).det())
assert jacobian==q1-q0
assert s.simplify((q-q0)/(q1-q0))==tau
joint=s.Matrix([(1-tau)*(1-q0),tau*(1-q1),(1-tau)*q0,tau*q1])
assert s.simplify(sum(joint))==1
assert s.factor(joint[0]*joint[3]-joint[1]*joint[2])==tau*(tau-1)*(q0-q1)

result={'status':'PASS','exact_transport_ranks':[rank8,rank16],
 'commuting_audit_projectors':len(audits),'walsh_update_formulas':2,
 'symbolic_alpha_posteriors':['alpha','1-alpha'],
 'fresh_two_disagreements_at_alpha_4_over_5':'1/17',
 'binary_signature_jacobian_determinant':str(jacobian),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out=json.dumps(result,indent=2)+'\n'
(root/'FINAL_TRANSPORT_RESULTS.json').write_text(out)
print(out)
