from fractions import Fraction as Q
from pathlib import Path
import sympy as S
import json
R=Path(__file__).resolve().parents[1]
V=[(1,1,1,1,0,0),(0,0,1,0,1,0),(0,0,1,0,0,1),(0,0,0,1,1,0),(0,0,0,1,0,1),(0,0,0,0,1,1)]
p=[Q(1,4)]*2+[Q(1,2)]*4;H=[4,4,100,100,100,100]
def B(v,k):return Q(1,4) if k==0 else 1+9*(Q(1,4)-v[0])-3*(Q(1,4)-v[1])
def grad(v,k):return [(1 if k==0 else H[i])*(p[i]-v[i]) for i in range(6)]
def coef(v,w,k):return B(v,k)-sum(x*y for x,y in zip(grad(v,k),w))
def psi(t):return Q(1,2)*t*t+4*t**4
def dp(t):return t+16*t**3
def div(a,t):return psi(a)-psi(t)-dp(t)*(a-t)
def loss(v,c,k):return sum((x-y)**2 for x,y in zip(v,c))/2 if k==0 else sum(div(v[i],c[i]) for i in range(2))+50*sum((v[i]-c[i])**2 for i in range(2,6))
def main():
 cp=[Q(12,41)]*2+[Q(3,328)]*2+[Q(-3,328)]*2;pp=[Q(15,26)]*2+[Q(0)]*4
 assert cp[0]==cp[1] and sum(cp[2:])==0 and pp[0]==pp[1] and sum(pp[2:])==0
 P=[(a,a)+v[2:] for a in (0,1) for v in V]
 Crows=[coef(v,cp,k) for v in V for k in (0,1)];Prows=[coef(v,pp,k) for v in P for k in (0,1)]
 assert min(Crows)==Q(7,82) and min(Prows)==Q(-1,26)
 cd=[(Q(100,123),V[5],0),(Q(11,123),V[5],1),(Q(12,123),V[0],1)]
 pd=[(Q(6,13),P[0],0),(Q(6,13),P[5],0),(Q(1,26),P[6],1),(Q(1,26),P[11],1)]
 for dual,value in [(cd,Q(7,82)),(pd,Q(-1,26))]:
  assert sum(w for w,v,k in dual)==1 and min(w for w,v,k in dual)>0
  assert [sum(w*grad(v,k)[i] for w,v,k in dual) for i in range(6)]==[0]*6
  assert sum(w*B(v,k) for w,v,k in dual)==value
 # Direct arbitrary-ambient-variable score expansion, independent of author remainder arrays.
 e=S.symbols('e');vv=S.symbols('v0:6');ww=S.symbols('w0:6');base=[p[i]+e*(1 if i==0 else 0) for i in range(6)];curve=[p[i]+e*(Q(1,2) if i<2 else 0)+e*e*ww[i] for i in range(6)]
 for k in (0,1):
  poly=S.Poly(S.expand(loss(vv,base,k)-loss(vv,curve,k)),e)
  assert not poly.as_expr().atoms(S.Float)
  assert poly.nth(0)==0 and S.expand(poly.nth(1)-(vv[1]-vv[0])*(Q(1,2) if k==0 else 2))==0
  assert S.expand(poly.nth(2)-coef(vv,ww,k))==0
 out={'status':'PASS','coupled_value':'7/82','product_value':'-1/26','coupled_primal_rows':list(map(str,Crows)),'product_primal_rows':list(map(str,Prows)),'dual_balance':'all six ambient coordinates exactly zero','ambient_score_coefficient_identities':2,'scope':'Algebraic LP certificates; general optimized-regret asymptotic remains ordinary.'};(R/'evidence/LP_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
