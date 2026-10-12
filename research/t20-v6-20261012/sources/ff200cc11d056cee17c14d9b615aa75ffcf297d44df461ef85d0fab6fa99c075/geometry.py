"""Exact rational checks of declared flat Riemannian models. No truth metric."""
from fractions import Fraction as F
from itertools import product
import json
I=((F(1),F(0)),(F(0),F(1)))
def transpose(a): return tuple(zip(*a))
def mul(a,b): return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def mv(a,x): return tuple(sum(a[i][k]*x[k] for k in range(2)) for i in range(2))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def det(a): return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def inv(a):
 d=det(a);assert d
 return ((a[1][1]/d,-a[0][1]/d),(-a[1][0]/d,a[0][0]/d))
def spd(a): return a==transpose(a) and a[0][0]>0 and det(a)>0
def energy(q): return dot(q,q)/2

def run():
 mats=[]
 for x in product((-1,0,1),repeat=4):
  a=((F(x[0]),F(x[1])),(F(x[2]),F(x[3])))
  if det(a):mats.append(a)
 metrics=[I,((F(2),F(-1)),(F(-1),F(1))),((F(3),F(1)),(F(1),F(2)))]
 points=list(product(map(F,range(-2,3)),repeat=2))
 failures=critical=checks=0
 for a,h,q in product(mats,metrics,points):
  g=mul(mul(transpose(a),h),a);assert spd(g)
  y=mv(a,q);dj1=mv(transpose(a),y)
  grad1=mv(inv(g),dj1);grad2=mv(inv(h),y)
  failures+=mv(a,grad1)!=grad2
  critical+=(grad1==(0,0))!=(dj1==(0,0))
  checks+=1
 a=((F(1),F(1)),(F(0),F(1)));q=(F(0),F(1));y=mv(a,q)
 naive=mv(a,mv(transpose(a),y))!=y
 g=metrics[1];grad=mv(inv(g),q);v=tuple(-x for x in grad)
 eta=F(1,4);raw=tuple(x+eta*d for x,d in zip(q,v))
 projected=(F(0),v[1]+g[1][0]/g[1][1]*v[0])
 safe=tuple(x+eta*d for x,d in zip(q,projected))
 assert projected==(0,-1)
 # The smooth encoding deliberately forgets authority. The exact audited record
 # remains a separate input. The code cannot authenticate that record.
 records=[{'id':'source-1','authority':'granted','q':q},{'id':'source-2','authority':'withheld','q':q}]
 next_records=[dict(r,q=safe) for r in records]
 return {'scope':'Standard conditional mathematics plus finite exact-rational checks; no empirical or metaphysical warrant',
         'invertible_coordinate_matrices':len(mats),'metrics':len(metrics),'points':len(points),
         'coordinate_checks':checks,'pullback_failures':failures,'criticality_failures':critical,
         'naive_euclidean_coordinate_failure':naive,
         'same_J_metric_changes_direction':grad!=q,
         'descent_can_leave_K':raw[0]<0 and energy(raw)<energy(q),
         'projected_step_preserves_K_and_decreases_J':safe[0]>=0 and energy(safe)<energy(q),
         'raw_step':list(map(str,raw)),'metric_tangent_projected_step':list(map(str,safe)),
         'raw_J':str(energy(raw)),'projected_J':str(energy(safe)),
         'same_smooth_point_different_authority':records[0]['q']==records[1]['q'] and records[0]['authority']!=records[1]['authority'],
         'exact_record_preserved':all(r['id']==s['id'] and r['authority']==s['authority'] for r,s in zip(records,next_records))}
if __name__=='__main__': print(json.dumps(run(),indent=2))
