from fractions import Fraction as F
from itertools import product
from collections import defaultdict
laws=[(F(2,5),F(1,10),F(1,10),F(2,5)),(F(1,10),F(2,5),F(2,5),F(1,10))]
states=list(product((0,1),repeat=2))
N=0
def check(x,msg):
 global N
 if not x:raise RuntimeError(msg)
 N+=1
trans=[]
for law in laws:
 d=defaultdict(F)
 for i,j in product(range(4),repeat=2):
  y1=states[i][0];q2=y1 # theta query0 after0; audit query1 after1
  y2=states[j][q2]
  d[(0,y1,q2,y2)]+=law[i]*law[j]
 check(set(d.values())=={F(1,4)},'each consistent transcript probability1/4')
 check(sum(d.values())==1,'protocol normalized')
 event=sum(w for (q1,y1,q2,y2),w in d.items() if q2==1)
 first_one=sum(w for (q1,y1,q2,y2),w in d.items() if q2==1 and y1==1)
 check(event==F(1,2) and first_one/event==1,'full choice sequence leaks earlier bit')
 check(d[(0,1,1,0)]/event==F(1,2)!=F(1,4),'conditional whole sequence not2^-n')
 trans.append(dict(d))
check(trans[0]==trans[1],'adaptive transcript laws identical')
for law,answer in zip(laws,(F(4,5),F(1,5))):
 check(law[3]/(law[1]+law[3])==answer,'same episode correction differs')
print({'status':'PASS','explicit_checks':N,'scope':'Independent exact adaptive-transcript and correction checks'})
