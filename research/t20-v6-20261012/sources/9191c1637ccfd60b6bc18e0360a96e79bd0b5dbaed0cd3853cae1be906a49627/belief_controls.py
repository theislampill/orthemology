from pathlib import Path
import json,itertools
import sympy as s
r=s.Rational
checks={}
def check(k,b):
 b=bool(b);checks[k]=b
 if not b: raise RuntimeError(k)
def norm(v): return [s.simplify(x/sum(v)) for x in v]
def eq(v,w): return all(s.simplify(x-y)==0 for x,y in zip(v,w))
def F(v): return norm([s.sqrt(x) for x in v])
def G(v): return norm([x*x for x in v])
def B(v,L): return norm([x*l for x,l in zip(v,L)])
def mass(v,L): return s.simplify(sum(x*l for x,l in zip(v,L)))
p=[r(1,14),r(4,14),r(9,14)];q=F(p)
Ls=[[r(3,4),r(1,2),r(1,4)],[r(1,4),r(1,2),r(3,4)]]
check('inverse coordinate readout',eq(G(q),p))
check('belief channel mass normalization',s.simplify(sum(mass(G(q),L) for L in Ls)-1)==0)
check('using transformed coordinate as hidden probability gives wrong mass',mass(q,Ls[1])!=mass(p,Ls[1]))
for word in itertools.product(range(2),repeat=3):
 pt=p[:];qt=q[:];pm=qm=s.Integer(1)
 for o in word:
  L=Ls[o];pm*=mass(pt,L);qm*=mass(G(qt),L)
  pt=B(pt,L);qt=B(qt,[s.sqrt(l) for l in L])
  check('transition intertwining '+str(word)+str(o)+str(len(checks)),eq(qt,F(pt)) and eq(G(qt),pt))
 check('history probability '+str(word),s.simplify(pm-qm)==0)
 direct=sum(p[i]*s.prod(Ls[o][i] for o in word) for i in range(3))
 check('conditional independent observation product '+str(word),s.simplify(qm-direct)==0)
Path(__file__).with_name('BELIEF_CONTROLS.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS',len(checks))
