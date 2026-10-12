from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def joint(a,qs):
    t=[a,1-2*a,a]
    return [(t[d]*(1-qs[d]),t[d]*qs[d]) for d in range(3)]
def answer(law,word):
    ds=set(word)
    if len(ds)>1:return None
    cells=law if not ds else [law[next(iter(ds))]]
    mass=sum(x+y for x,y in cells)
    return sum(y for x,y in cells)/mass if mass else None

def risk(p):return p*(1-p)
results={}
for name,qs,cost in [('boundary',[F(0),F(1,2),F(1)],F(3,32)),('interior',[F(1,4),F(1,2),F(3,4)],F(3,128))]:
    laws=[joint(a,qs) for a in [F(1,4),F(1,8)]]
    count=0
    for length in range(7):
        for w in product(range(3),repeat=length):
            assert answer(laws[0],w)==answer(laws[1],w)
            count+=1
    gains=[]
    for law in laws:
        q=answer(law,())
        expected=sum((x+y)*risk(y/(x+y)) for x,y in law)
        gains.append(risk(q)-expected)
    assert gains[0]>cost>gains[1]
    # v=(1,-2,1) preserves normalisation and target probabilities.
    v=[1,-2,1]
    assert sum(v)==0 and sum(v[d]*qs[d] for d in range(3))==0
    hv=sum(v[d]*risk(qs[d]) for d in range(3))
    assert hv<0
    results[name]={'word_comparisons':count,'gains':list(map(str,gains)),'cost':str(cost),'net_values':[str(g-cost) for g in gains],'risk_kernel_pairing':str(hv),'all_joint_cells_positive':all(c>0 for law in laws for pair in law for c in pair)}
assert results['interior']['all_joint_cells_positive']
results['status']='PASS'
out=json.dumps(results,indent=2)+'\n'
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(out)
print(out,end='')
