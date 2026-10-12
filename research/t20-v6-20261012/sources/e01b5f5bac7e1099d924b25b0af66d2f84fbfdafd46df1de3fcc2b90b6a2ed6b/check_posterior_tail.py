from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'stochastic-exact-inquiry-20261010'))
from solver import classify
# Fixed immutable state order (Theta,R/N): 0R,1R,0N,1N.
labels=(0,1,0,1)
likelihoods=((F(1,2),F(1,2),F(1),F(1)),
             (F(1,2),F(0),F(0),F(0)),
             (F(0),F(1,2),F(0),F(0)))
p=(F(1,2),F(1,2),F(0),F(0));q=(F(1,4),)*4
assert all(sum(l[i] for l in likelihoods)==1 for i in range(4))
rows={'observe':[{(i,o) for o,l in enumerate(likelihoods) if l[i]} for i in range(4)]}
a=classify(rows,labels,{i for i,x in enumerate(p) if x})
b=classify(rows,labels,{i for i,x in enumerate(q) if x})
assert a['almost_sure'] and not b['almost_sure']
assert not a['sure'] and not b['sure']
def posterior(r):
 m=sum(r)
 return None if not m else tuple(sum(x for x,b in zip(r,labels) if b==v)/m for v in (0,1))
def advance(r,w):
 for o in w:r=tuple(x*y for x,y in zip(r,likelihoods[o]))
 return r
# A pair with the same full support but unequal target posteriors.
r=(F(1,2),F(1,4),F(1,8),F(1,8))
s=(F(1,8),F(1,8),F(1,4),F(1,2))
Csr=max(y/x for x,y in zip(r,s));Crs=max(x/y for x,y in zip(r,s))
assert Csr==Crs==4
word_count=0
for n in range(9):
 for w in product(range(3),repeat=n):
  pp,qq=advance(p,w),advance(q,w)
  assert bool(sum(pp))==bool(sum(qq))
  assert posterior(pp)==posterior(qq)
  assert bool(sum(pp))==(not (1 in w and 2 in w))
  rr,ss=advance(r,w),advance(s,w)
  assert sum(ss)<=Csr*sum(rr) and sum(rr)<=Crs*sum(ss)
  for k in (0,1):
   rk=sum(x for x,b in zip(rr,labels) if b==k)
   sk=sum(x for x,b in zip(ss,labels) if b==k)
   assert sk<=Csr*rk and rk<=Crs*sk
  word_count+=1
for n in range(30):
 pp,qq=advance(p,(0,)*n),advance(q,(0,)*n)
 assert sum(pp)==F(1,2)**n
 assert sum(qq)==F(1,2)+F(1,2)**(n+1)
 assert sum(qq)/sum(pp)==F(2)**(n-1)+F(1,2)
# Full invariant cross-product test. Every same-word matrix is diagonal here.
def basis(vectors):
 rows=[list(v) for v in vectors];k=0
 for j in range(16):
  i=next((i for i in range(k,len(rows)) if rows[i][j]),None)
  if i is None:continue
  rows[k],rows[i]=rows[i],rows[k]
  c=rows[k][j];rows[k]=[x/c for x in rows[k]]
  for i in range(len(rows)):
   if i!=k and rows[i][j]:
    c=rows[i][j];rows[i]=[x-c*y for x,y in zip(rows[i],rows[k])]
  k+=1
  if k==len(rows):break
 return tuple(tuple(r) for r in rows[:k])
seed=tuple(F(labels[i]==0)-F(labels[j]==0) for i in range(4) for j in range(4))
B=basis([seed]);dimensions=[len(B)]
while True:
 new=basis(list(B)+[tuple(v[i*4+j]*l[i]*l[j] for i in range(4) for j in range(4)) for v in B for l in likelihoods])
 if new==B:break
 B=new;dimensions.append(len(B))
assert all(sum(v[i*4+j]*p[i]*q[j] for i in range(4) for j in range(4))==0 for v in B)
out={'status':'PASS','finite_word_controls':word_count,'max_word_length':8,'survival_prefix_controls':30,'unbounded_ratio_prefix_controls':30,'same_support_domination_word_cases':word_count,'same_support_two_way_bound':'4','same_support_labelled_bounds_checked':True,'posterior_cross_product_span_dimensions':dimensions,'all_basis_rows_annihilate_p_tensor_q':True,'same_feasible_word_language':'all words omitting at least one of reveal0,reveal1','p_support':[0,1],'q_support':[0,1,2,3],'p_almost_sure_stopping':a['almost_sure'],'q_almost_sure_stopping':b['almost_sure'],'p_sure_stopping':a['sure'],'q_sure_stopping':b['sure'],'p_wait_survival':'2^-n','q_wait_survival':'1/2+2^(-n-1)','scope':'Written all-word proof in ADDENDUM.md; finite controls corroborate it. No new source reliability or human-knowledge claim.'}
Path(__file__).with_name('POSTERIOR_TAIL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
