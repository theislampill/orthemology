#!/usr/bin/env python3
"""Independent reviewer controls, derived from count laws and symbolic moments.
No imports from author controls. Explicit exceptions survive python -O.
"""
import hashlib,json,itertools,sys
from pathlib import Path
from functools import lru_cache
from math import comb
import sympy as S
Q=S.Rational
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'t20-depth-reassessment-20261011/uncertainty_inquiry'
n=0

def ck(v,label):
 global n
 n+=1
 if not bool(v): raise RuntimeError(label)
def eq(x,y,label): ck(S.simplify(x-y)==0,label)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
 # Verify actual owner bytes as well as copies, and every author-manifest binding.
 ledger=json.loads((A/'READ_LEDGER.json').read_text())
 for r in ledger:
  for key in ('path','copy'): ck(digest(ROOT/r[key])==r['sha256'],'source digest '+r['id'])
 manifest=json.loads((A/'MANIFEST.json').read_text())['files']
 for name,r in manifest.items():
  ck(digest(A/name)==r['sha256'],'manifest '+name)
  ck((A/name).stat().st_size==r['bytes'],'length '+name)
 t,s=S.symbols('t s',real=True)
 H=S.Matrix([[1,Q(1,2),Q(1,3)],[Q(1,2),Q(1,3),t],[Q(1,3),t,s]])
 G=S.Matrix([[Q(1,6),Q(1,3)-t],[Q(1,3)-t,t-s]])
 L=12*t*t-4*t+Q(4,9); U=-6*t*t+5*t-Q(2,3)
 eq(H.det(),(s-L)/12,'lower Schur determinant')
 eq(G.det(),(U-s)/6,'upper Schur determinant')
 eq(U-L,-18*(t-Q(2,9))*(t-Q(5,18)),'interval factor')
 # Root recurrence, avoiding a copied root sampler.
 alpha=12*t-2; beta=Q(4,3)-6*t
 moments=[S.Integer(1),Q(1,2)]
 for k in range(3): moments.append(S.expand(alpha*moments[-1]+beta*moments[-2]))
 for actual,want in zip(moments,[1,Q(1,2),Q(1,3),t,L]): eq(actual,want,'two-atom recurrence')
 z=2-6*t
 atoms=[(0,Q(1,2)-1/(6*z)),(z,1/(6*z*(1-z))),(1,Q(1,2)-1/(6*(1-z)))]
 for k,want in enumerate([1,Q(1,2),Q(1,3),t,U]): eq(sum(w*p**k for p,w in atoms),want,'upper atoms')
 # Independently solve count-probability polytope basic feasible solutions.
 M=S.Matrix([[1]*5,[Q(k,4) for k in range(5)],[Q(k*(k-1),12) for k in range(5)]])
 target=S.Matrix([1,Q(1,2),Q(1,3)]); counts=set()
 for ix in itertools.combinations(range(5),3):
  B=M[:,ix]
  if B.det()==0: continue
  x=B.inv()*target
  if min(x)<0: continue
  row=[S.Integer(0)]*5
  for i,v in zip(ix,x): row[i]=v
  counts.add(tuple(row))
 ck(len(counts)==3,'three count-law vertices')
 order=sorted(counts,key=lambda w: sum(w[k]*Q(comb(k,3),4) for k in range(3,5)))
 words=list(itertools.product((0,1),repeat=4))
 laws=[{word:w[sum(word)]/comb(4,sum(word)) for word in words} for w in order]
 ts=[]
 for law in laws:
  eq(sum(law.values()),1,'normalised word law')
  for i,j in itertools.combinations(range(4),2):
   pair=[sum(p for word,p in law.items() if (word[i],word[j])==o) for o in itertools.product((0,1),repeat=2)]
   ck(pair==[Q(1,3),Q(1,6),Q(1,6),Q(1,3)],'same ordered pair')
  ts.append((sum(p for w,p in law.items() if w[:3]==(1,1,1)),law[(1,1,1,1)]))
 ck(ts==[(Q(1,6),0),(Q(1,4),Q(1,4)),(Q(1,3),Q(1,3))],'independently recovered triangle')
 # Complete-path evaluation: six plans, all labels available.
 policies=[(False,(0,0)),(False,(1,1))]+[(True,r) for r in itertools.product((0,1),repeat=2)]
 def matrix(ls,c):
  out=[]
  for law in ls:
   mass=sum(p for word,p in law.items() if word[:2]==(1,1)); eq(mass,Q(1,3),'positive common conditioning')
   out.append([sum(p*(int(r[word[2]]!=word[3])+c*int(query)) for word,p in law.items() if word[:2]==(1,1))/mass for query,r in policies])
  return S.Matrix(out)
 c=S.symbols('c',nonnegative=True); V=matrix(laws,c)
 primal=S.Matrix([0,Q(4,5),0,0,Q(1,5),0]); dual=S.Matrix([ (3+4*c)/5,(2-4*c)/5,0])
 for x,y in zip(V*primal,[Q(2,5)+c/5,Q(2,5)+c/5,Q(1,5)+c/5]): eq(x,y,'primal general c')
 gaps=list((dual.T*V-S.ones(1,6)*(Q(2,5)+c/5)))
 for actual,want in zip(gaps,[(1-2*c)/5,0,(3*c+1)/5,(8*c+1)/5,0,c]): eq(actual,want,'strict dual gaps and uniqueness')
 # Mixing must precede nature's adversarial maximization; public coin mutation fails.
 num=V.subs(c,Q(1,10))
 ck(max(num*primal)==Q(21,50),'private minimax')
 ck(sum(primal[j]*max(num[:,j]) for j in range(6))==Q(31,50),'public-plan cost')
 # Strictly positive perturbation built directly on words, not t,s.
 uniform={w:Q(1,5*comb(4,sum(w))) for w in words}
 positive=[{w:Q(9,10)*law[w]+Q(1,10)*uniform[w] for w in words} for law in laws]
 ck(min(p for law in positive for p in law.values())==Q(1,300),'positive margin')
 W=matrix(positive,Q(1,10)); d=S.Matrix([Q(164,225),Q(61,225),0])
 ck(max(W*primal)==min(d.T*W)==Q(207,500),'positive saddle')
 ck(min(max(W[:,j]) for j in range(6))==Q(19,40),'positive deterministic optimum')
 ck([j for j,v in enumerate(d.T*W) if v==Q(207,500)]==[1,4],'positive strict support')
 # Symbolic general-moment certificates for all three saturation regimes.
 mu,nu,tau=S.symbols('mu nu tau',positive=True)
 measures=[[(0,1-mu**2/nu),(nu/mu,mu**2/nu)],
 [((mu-nu)/(1-mu),(1-mu)**2/(1-2*mu+nu)),(1,1-(1-mu)**2/(1-2*mu+nu))],
 [(0,(nu-(1+tau)*mu+tau)/tau),(tau,(mu-nu)/(tau*(1-tau))),(1,(nu-mu*tau)/(1-tau))]]
 for rho in measures:
  for k,want in enumerate([1,mu,nu]): eq(sum(w*p**k for p,w in rho),want,'symbolic LFD moments')
 eq(measures[2][1][1]*tau*(1-tau),mu-nu,'middle oracle scaled risk')
 # Exact known-model Bayesian DP over arbitrarily selectable distinct iid observations.
 # Depth eight exercises all adaptive stop/report choices implicitly, including history costs.
 cases=0
 for m in [Q(1,7),Q(1,2),Q(5,6)]:
  for f in [0,Q(1,3),1]:
   v=m*m+(m-m*m)*f
   for a,b in [(Q(1,3),Q(5,2)),(S.Integer(1),S.Integer(1)),(S.Integer(3),Q(1,2))]:
    th=a/(a+b);q0=(m-v)/(1-m);q1=v/m
    regime=0 if q1<=th else 1 if q0>=th else 2
    rho=[(S.cancel(p.subs({mu:m,nu:v,tau:th})) if hasattr(p,'subs') else S.Integer(p),S.cancel(w.subs({mu:m,nu:v,tau:th}))) for p,w in measures[regime]]
    ck(min(w for p,w in rho)>=0,'LFD nonnegative')
    r0=min(b*m,a*(1-m)); r1=min(b*(m-v),a*(1-2*m+v))+min(b*v,a*(m-v))
    eq(sum(w*min(b*p,a*(1-p)) for p,w in rho),r1,'oracle equality')
    for firstcost in [0,Q(1,10),Q(2,3)]:
     @lru_cache(None)
     def dp(heads,tails):
      weights=[w*p**heads*(1-p)**tails for p,w in rho]
      skip=min(sum(ww*b*p for ww,(p,w) in zip(weights,rho)),sum(ww*a*(1-p) for ww,(p,w) in zip(weights,rho)))
      if heads+tails==8:return skip
      price=firstcost if heads+tails==0 else Q((heads+2*tails)%3,17)
      return min(skip,price*sum(weights)+dp(heads+1,tails)+dp(heads,tails+1))
     eq(dp(0,0),min(r0,firstcost+r1),'adaptive DP saturation with nonuniform later costs')
     cases+=1
 # Independent finite difference pair and complete law equality.
 rs=[[(Q(k,5),Q((5+sign*(-1)**k)*comb(5,k),192)+(Q(1,12) if k in [0,5] else 0)) for k in range(6)] for sign in [1,-1]]
 ms=[[sum(w*p**j for p,w in rho) for j in range(6)] for rho in rs]
 ck(ms[0][:5]==ms[1][:5]==[1,Q(1,2),Q(1,3),Q(1,4),Q(61,300)],'four moments same')
 ck([m[5]/m[4] for m in ms]==[Q(1311,1525),Q(1314,1525)],'fifth prediction separates')
 for word in words: eq(sum(w*p**sum(word)*(1-p)**(4-sum(word)) for p,w in rs[0]),sum(w*p**sum(word)*(1-p)**(4-sum(word)) for p,w in rs[1]),'all four-path laws identical')
 negatives={'identify_C_with_E':Q(1,3)==Q(21,50),'reveal_private_plan':Q(21,50)==Q(31,50),'claim_horizon_closure':ms[0][5]==ms[1][5],'scalar_prune':Q(1,2)==Q(21,50)}
 for name,bad in negatives.items():
  try: ck(bad,'deliberate false mutation '+name)
  except RuntimeError: pass
  else: raise RuntimeError('mutation survived '+name)
 return {'status':'PASS','explicit_checks':n,'adaptive_DP_cases':cases,'adaptive_depth':8,'rejected_mutations':list(negatives),'reviewed_result_sha256':digest(A/'RESULT.md'),'source_records':len(ledger),'sympy':S.__version__}
if __name__=='__main__':
 if '--fail' in sys.argv: ck(False,'explicit guard must reject under -O')
 print(json.dumps(run(),indent=2,sort_keys=True))
