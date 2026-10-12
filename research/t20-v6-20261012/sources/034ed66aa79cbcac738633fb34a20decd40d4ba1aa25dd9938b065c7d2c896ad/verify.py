#!/usr/bin/env python3
"""Exact selected controls; general-dimensional proof is in RESULT.md."""
import sympy as s
import json, hashlib, argparse
from pathlib import Path
checks=[]
def ck(name,condition):
 if not bool(condition): raise RuntimeError(name)
 checks.append(name)
def zero(A): return all(s.simplify(x)==0 for x in A)
def calc(B,S,Bt,T):
 k=B.cols;m=B.rows;n=k+m;I=s.eye(n)
 Sig=s.eye(k).row_join(B.T).col_join(B.row_join(B*B.T+S))
 Gam=s.eye(k).row_join(Bt.T).col_join(Bt.row_join(Bt*Bt.T+T))
 Q=Gam.inv();H=s.eye(k).col_join(B)
 M=Q[:k,:k]+Q[:k,k:]*B-s.eye(k);N=H.T*Q*H-s.eye(k)
 P=(M+M.T+N)/3;Pb=s.diag(P,s.zeros(m))
 F=2*I+Sig-Q*Sig-Sig*Q-Sig*Q*Sig+Pb*Sig+Sig*Pb+Sig*Pb*Sig
 Bd=F[k:,:k];Sd=F[k:,k:]-Bd*B.T-B*Bd.T
 return Sig,Q,P,Pb,F,Bd,Sd
B=s.Matrix([[1,2],[-1,1],[2,-1]])
Bt=s.Matrix([[0,1],[1,-1],[1,2]])
T=s.Matrix([[3,1,0],[1,2,1],[0,1,3]])
ck('target T positive definite',all(T[:j,:j].det()>0 for j in range(1,4)))
for label,S in [('rank1',s.diag(2,0,0)),('rank0',s.zeros(3)),('rank2',s.Matrix([[2,1,0],[1,2,0],[0,0,0]])),('positive',s.Matrix([[2,1,0],[1,3,1],[0,1,2]]))]:
 Sig,Q,P,Pb,F,Bd,Sd=calc(B,S,Bt,T);k=2;m=3
 ck(label+' observed covariance tangent zero',zero(F[:k,:k]))
 ck(label+' symmetric tangent',zero(F-F.T))
 K=s.Matrix.hstack(*S.nullspace()) if S.nullspace() else s.zeros(m,0)
 if K.cols:
  A=2*K.T*(s.eye(m)+B*B.T)*K
  ck(label+' kernel derivative formula',zero(K.T*Sd*K-A))
  ck(label+' positive kernel derivative',all(A[:j,:j].det()>0 for j in range(1,K.cols+1)))
  # Chosen null bases and range bases here are coordinate orthonormal.
  t=s.symbols('t');r=K.cols
  range_det=s.prod([v for v,mult in S.eigenvals().items() for _ in range(mult) if v!=0])
  ck(label+' determinant leading coefficient',s.expand((S+t*Sd).det()).coeff(t,r)==range_det*A.det())
 else:
  C=Q-Sig.inv()-Pb
  ck('positive covariance polynomial equals potential evolution',zero(F+C*Sig+Sig*C+Sig*C*Sig))
  # Density polynomial coefficients and constants, without sampling x.
  ck('positive full-density quadratic coefficient',zero(Sig.inv()*F*Sig.inv()/2+(Sig.inv()*C+C*Sig.inv())/2+C/2))
  ck('positive full-density constant',s.simplify(-s.trace(Sig.inv()*F)/2-s.trace(C)-s.trace(C*Sig)/2)==0)
  D=s.trace(C*Sig*C)+s.trace(C*Sig*C*Sig)/2
  Ed=s.trace(T.inv()*Sd)/2+s.trace((B-Bt).T*T.inv()*Bd)-s.trace(S.inv()*Sd)/2
  ck('positive exact KL dissipation',s.simplify(Ed+D)==0)
  ck('positive noncommuting control',not zero(S*T-T*S))
Sig,Q,P,Pb,F,Bd,Sd=calc(Bt,T,Bt,T)
ck('target multiplier and flow vanish',zero(P) and zero(F))
b,be,ss,tau=s.symbols('b beta ss tau', real=True, nonzero=True)
Sig,Q,P,Pb,F,Bd,Sd=calc(s.Matrix([b]),s.Matrix([ss]),s.Matrix([be]),s.Matrix([tau]))
ck('scalar multiplier specialization',s.simplify(P[0]-(b-be)*(b-3*be)/(3*tau))==0)
ck('scalar B equation specialization',s.simplify(Bd[0]-(b*(ss-tau)-(b-be)*(1+2*ss+b*b/3))/tau)==0)
ck('scalar S equation specialization',s.simplify(Sd[0]-(2*b*ss*(b-be)-(ss+2+2*b*b)*(ss-tau))/tau)==0)
root=Path(__file__).resolve().parent
for binding in json.loads((root/'INPUT_BINDINGS.json').read_text()):
 ck('input '+binding['original'],hashlib.sha256((root/binding['snapshot']).read_bytes()).hexdigest()==binding['sha256'])
p=argparse.ArgumentParser();p.add_argument('--output',default=str(root/'CHECKS.json'));args=p.parse_args()
Path(args.output).write_text(json.dumps({'status':'pass','exact_controls':checks,'count':len(checks),'scope':'Finite exact symbolic/rational controls supplement, not prove, general-dimensional analytic assertions.'},indent=2)+'\n')
print(json.dumps({'status':'pass','count':len(checks)}))
