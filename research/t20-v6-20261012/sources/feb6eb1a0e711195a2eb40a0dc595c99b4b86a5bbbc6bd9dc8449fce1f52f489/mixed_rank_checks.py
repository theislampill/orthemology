#!/usr/bin/env python3
"""Independent exact Boolean hull, tangent, leading-gain and feasibility checks."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
V=[(1,1,1,1,0,0),(0,0,1,0,1,0),(0,0,1,0,0,1),
   (0,0,0,1,1,0),(0,0,0,1,0,1),(0,0,0,0,1,1)]

def psi(t):return Q(1,2)*t*t+4*t**4
def dp(t):return t+16*t**3
def div(a,t):return psi(a)-psi(t)-dp(t)*(a-t)
def losses(v,c):return (sum((x-y)**2 for x,y in zip(v,c))/2,
    div(v[0],c[0])+div(v[1],c[1])+50*sum((v[i]-c[i])**2 for i in range(2,6)))

def correction(p,h):
    s,_,z,w,u,v=p;h1,h2,*hh=h;m=(h1+h2)/2;k=sum(hh)/4;e=(h1-h2)**2/4;r=1+48*s*s;T=z+w
    gam=96*e*s*s/(T*(100-r));bet=(48*e*s-100*gam)/r
    d=[m,m]+[a-k for a in hh];b=[bet,bet,gam/2,gam/2,-gam/2,-gam/2]
    return d,b,e,2*k*k

def baseline(p,h,eps):return [x+eps*y for x,y in zip(p,h)]
def candidate(p,h,eps):
    d,b,*_=correction(p,h);return [x+eps*y+eps*eps*z for x,y,z in zip(p,d,b)]
def weight_change(d):
    s,_,z,w,u,v=d
    assert z+w+u+v==0
    return [s,Q(0),z-s,u-s+z+w,-u-z,s-z-w]
def reconstruct(a):return [sum(a[i]*V[i][j] for i in range(6)) for j in range(6)]

def symbolic():
    M=S.Matrix([[V[i][j]-V[0][j] for j in range(6)] for i in range(1,6)])
    assert M.rank()==4
    assert all(v[0]==v[1] and sum(v[2:])==2 and all(x in [0,1] for x in v) for v in V)
    assert {tuple(v[2:]) for v in V}=={x for x in product([0,1],repeat=4) if sum(x)==2}
    assert {v[:2] for v in V}=={(0,0),(1,1)}
    # Exact null space of tangent rows has the two stated defining normals.
    N=S.Matrix([[1,-1,0,0,0,0],[0,0,1,1,1,1]])
    assert M*N.T==S.zeros(5,2) and N.rank()==2
    # Every pair in high block supports an elementary tangent, never a singleton.
    supports=[]
    for i in range(2,6):
      for j in range(i+1,6):
        t=S.zeros(6,1);t[i]=1;t[j]=-1;assert N*t==S.zeros(2,1);supports.append([i,j])
    for j in range(6):
      t=S.zeros(6,1);t[j]=1;assert N*t!=S.zeros(2,1)
    s,z,w,u,h1,h2,d1,d2,d3,k,b,g,eps=S.symbols('s z w u h1 h2 d1 d2 d3 k b g eps')
    p=[s,s,z,w,u,2-z-w-u];d=[(h1+h2)/2]*2+[d1,d2,d3,-d1-d2-d3]
    h=[h1,h2]+[x+k for x in d[2:]];c=[p[i]+eps*d[i]+eps*eps*[b,b,g/2,g/2,-g/2,-g/2][i] for i in range(6)];B=[p[i]+eps*h[i] for i in range(6)]
    e=(h1-h2)**2/4;r=1+48*s*s;T=z+w
    for v in V:
      a=v[0];j=v[2]+v[3];LB=losses(v,B);LC=losses(v,c)
      targets=[e-2*(s-a)*b+(j-T)*g+2*k*k,
               r*e+(s-a)*(96*s*e-2*r*b)+100*(j-T)*g+200*k*k]
      for q in range(2):
        P=S.Poly(S.expand(LB[q]-LC[q]),eps)
        assert not P.as_expr().atoms(S.Float)
        assert P.nth(0)==P.nth(1)==0
        assert S.expand(P.nth(2)-targets[q])==0
    # High-block-only normal directions have no nonlinear remainder at all.
    for v in V:
      gg=S.expand((losses(v,B)[0]-losses(v,c)[0]).subs({h2:h1,b:0,g:0}))
      ff=S.expand((losses(v,B)[1]-losses(v,c)[1]).subs({h2:h1,b:0,g:0}))
      assert S.expand(gg-2*k*k*eps*eps)==0
      assert S.expand(ff-200*k*k*eps*eps)==0
    # Product averaging at the genuine interior high-block baseline (1/2,...,1/2).
    H=[v[2:] for v in V];y=S.symbols('y0:4');pH=[S.Rational(1,2)]*4
    expected=sum(sum((S.Rational(1,2)-a)**2-(x-a)**2 for a,x in zip(v,y))/2 for v in H)/6
    assert S.expand(expected+sum((x-S.Rational(1,2))**2 for x in y)/2)==0
    return {'affine_rank':4,'tangent_normals':[[int(x) for x in row] for row in N.tolist()],'high_elementary_pairs':supports,'leading_gain_identities':12,'pure_high_normal_exact_identities':12,'product_average_identity':True}

def rational_cases():
    # Chosen weights are positive; transfer them by a fixed affine right inverse.
    weights=[]
    for bits in product([1,3],repeat=6):weights.append([Q(x,sum(bits)) for x in bits])
    for k in [4,8,12]:
      for j in range(6):
        a=[Q(1)]*6;a[j]=Q(1,10**k);weights.append([x/sum(a) for x in a])
    hs=[(1,0,0,0,0,0),(0,0,1,1,1,1),(2,2,1,2,3,4),(0,1,-1,-2,-3,-4),(100,99,-100,120,50,-70),(Q(1,1000),0,1,-1,1,-1)]
    records=[]
    for a in weights:
      p=reconstruct(a);s=p[0];T=p[2]+p[3];assert 0<s<1 and 2*s<T<1+s
      for hh in hs:
        h=list(map(Q,hh));d,b,e,EH=correction(p,h);assert e+EH>0
        dl=weight_change(d);db=weight_change(b)
        assert reconstruct(dl)==d and reconstruct(db)==b and sum(dl)==sum(db)==0
        # A constructive positive radius for exact barycentric/cube feasibility.
        L=sum(abs(x) for x in dl+db);margin=min(a);cube=min(min(x,1-x) for x in p)
        eps=min(Q(1,1000),margin/(2*(L+1)),cube/(2*(1+sum(abs(x) for x in h))))
        # Monotone shrinking is only a concrete test search, not the universal proof.
        for trial in range(80):
          B=baseline(p,h,eps);C=candidate(p,h,eps);ac=[a[i]+eps*dl[i]+eps*eps*db[i] for i in range(6)]
          assert min(ac)>0 and sum(ac)==1 and reconstruct(ac)==C and all(0<x<1 for x in B)
          gains=[losses(v,B)[j]-losses(v,C)[j] for v in V for j in range(2)]
          assert all(isinstance(x,Q) for x in gains)
          if min(gains)>0:break
          eps/=2
        else:raise AssertionError('No strict repair found within bounded test search')
        records.append({'weights':list(map(str,a)),'direction':list(map(str,h)),'epsilon':str(eps),'halvings':trial,'minimum_gain':str(min(gains)),'e':str(e),'E_H':str(EH)})
    return records

def controls():
    # Omitting high-block normal projection misses an entire family of transverse directions.
    a=[Q(1,6)]*6;p=reconstruct(a);h=[Q(0),Q(0),Q(1),Q(1),Q(1),Q(1)];eps=Q(1,100)
    wrong=baseline(p,h,eps);assert sum(wrong[2:])!=2
    right=candidate(p,h,eps);assert right==p
    assert all(losses(v,wrong)[j]-losses(v,right)[j]>0 for v in V for j in [0,1])
    # Copying the AND free correction (+gamma,+gamma,0,0) violates the high sum constraint.
    h=[Q(1),Q(0),Q(0),Q(0),Q(0),Q(0)];d,b,*_=correction(p,h)
    wrongb=b[:2]+[2*b[2],2*b[3],Q(0),Q(0)];assert sum(wrongb[2:])>0
    # The product comparison must average actual vertices, not insert pH as a truth.
    assert (Q(1,2),)*4 not in [v[2:] for v in V]
    return {'omitted_high_normal_projection_rejected':True,'uncorrected_free_coordinate_formula_rejected':True,'interior_baseline_is_not_a_truth':True}

def main():
    out={'status':'PASS','symbolic':symbolic(),'cases':rational_cases(),'controls':controls()};out['case_count']=len(out['cases']);out['truth_score_comparisons']=12*out['case_count'];out['pure_high_normal_cases']=sum(c['e']=='0' for c in out['cases']);(ROOT/'evidence/MIXED_RANK_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
