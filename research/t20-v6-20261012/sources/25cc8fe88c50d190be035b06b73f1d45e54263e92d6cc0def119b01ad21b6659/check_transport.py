from pathlib import Path
from itertools import product
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'stochastic-exact-inquiry-20261010'))
from solver import classify
X=list(product(range(2),repeat=4))
Z=list(product(range(2),repeat=3))
f=lambda x:Z.index((x[0],x[1],int(x[3]!=x[2])))
rx={'audit':[{(i,(x[1],int(x[3]!=x[2])))} for i,x in enumerate(X)]}
rz={'audit':[{(j,(z[1],z[2]))} for j,z in enumerate(Z)]}
B={i for i,x in enumerate(X) if x[2]==1}
a=classify(rx,[x[0] for x in X],B)
b=classify(rz,[z[0] for z in Z],{f(X[i]) for i in B})
image=lambda C:frozenset(f(X[i]) for i in C)
assert {image(C) for C in a['supports']}==b['supports']
assert len(a['supports'])==len(b['supports'])==5
for (C,act),obs in a['transitions'].items():
 for o,D in obs.items():assert b['transitions'][image(C),act][o]==image(D)
assert (a['sure'],a['almost_sure'])==(b['sure'],b['almost_sure'])==(False,False)
# Holding the hypothetical observation instrument fixed does not hold its legal menu fixed.
rows={'read':[{(0,0)},{(1,1)}]}
allowed=classify(rows,[0,1],{0,1},[{'read'},{'read'}])
blocked=classify(rows,[0,1],{0,1},[set(),set()])
assert allowed['sure'] and not blocked['almost_sure']
out={'status':'PASS','eight_mass_quotient':{'fine_states':16,'aggregate_states':8,'fine_supports':5,'aggregate_supports':5,'support_and_observation_intertwining':True,'sure':False,'almost_sure':False},'permission_control':{'same_target_and_potential_instrument':True,'universally_licensed_sure':True,'unlicensed_almost_sure':False},'scope':'Exact current audit transport and permission necessity control; no new general theorem or reviewer claim'}
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
