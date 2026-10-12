#!/usr/bin/env python3
"""Independent finite source/audit transport and author's non-PD probability checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'snapshot/stochastic-exact-inquiry-20261010'
spec=importlib.util.spec_from_file_location('candidate_solver',SRC/'solver.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
classify=mod.classify
states=list(product((0,1),repeat=4))
law={}
for th,t,y,v in states:
    report_acc=F(9,10) if t==0 else F(1,2)
    ychance=report_acc if y==th else 1-report_acc
    vchance=F(4,5) if v==th else F(1,5)
    law[th,t,y,v]=F(1,4)*ychance*vchance
assert sum(law.values())==1 and all(p>0 for p in law.values())
conditional={s:p for s,p in law.items() if s[2]==1}
z=sum(conditional.values());conditional={s:p/z for s,p in conditional.items()}
assert z==F(1,2)
assert sum(p for s,p in conditional.items() if s[0]==1)==F(7,10)
audit=lambda s:(s[1],int(s[3]!=s[2]))
rows={'reread':[{(i,audit(s))} for i,s in enumerate(states)]}
initial={states.index(s) for s in conditional}
r=classify(rows,[s[0] for s in states],initial)
assert not r['almost_sure'] and not r['sure']
expected_supports={frozenset(initial)} | {frozenset(states.index(s) for s in conditional if audit(s)==a) for a in product((0,1),repeat=2)}
assert r['supports']==expected_supports and not r['goals']
# Independent projection of full state law to the (theta,T,D) joint law.
quotient={q:sum(p for s,p in conditional.items() if (s[0],*audit(s))==q) for q in product((0,1),repeat=3)}
comparisons=0
for n in range(5):
    for word in product(list(product((0,1),repeat=2)),repeat=n):
        full=[sum(p for s,p in conditional.items() if s[0]==th and all(audit(s)==a for a in word)) for th in (0,1)]
        reduced=[sum(p for q,p in quotient.items() if q[0]==th and all(q[1:]==a for a in word)) for th in (0,1)]
        assert full==reduced
        comparisons+=1
bad_disagree=[sum(p for s,p in conditional.items() if s[0]==th and audit(s)==(1,1)) for th in (0,1)]
assert sum(bad_disagree)==F(1,4) and bad_disagree[1]/sum(bad_disagree)==F(1,5)
# Known-Bad quotient has all four cells positive and only two target-mixed successors.
badmass=sum(p for s,p in conditional.items() if s[1]==1)
q4={q:sum(p for s,p in conditional.items() if (s[0],int(s[3]!=s[2]))==q and s[1]==1)/badmass for q in product((0,1),repeat=2)}
assert list(q4.values())==[F(1,10),F(2,5),F(2,5),F(1,10)]
# Exact all-word fresh likelihood controls: each word stays target-mixed.
fresh_words=0
for n in range(9):
    for word in product((0,1),repeat=n):
        likelihood=[F(1,2) for _ in (0,1)]
        for d in word:
            v=1-d
            for th in (0,1):likelihood[th]*=F(4,5) if v==th else F(1,5)
        assert all(p>0 for p in likelihood)
        fresh_words+=1
    posterior=F(1,5)**n/(F(1,5)**n+F(4,5)**n)
    assert posterior==F(1,1+4**n)
# Revised author's non-PD example: compute survival by actual substochastic evolution.
survival0=[F(1),F(0)]
survival1=F(1)
for n in range(1,65):
    survival0=[survival0[0]/4,survival0[0]/4]
    survival1/=2
    assert sum(survival0)==2*F(1,4)**n and survival1==F(1,2)**n
# Projecting physical sinks must not forget opposite initial labels.
labels=[0,0,1,0,1,0,1]
rows={'a':[{(5,'1')},{(3,'0')},{(4,'0')},{(3,'0')},{(4,'0')},{(5,'1')},{(6,'1')}],
      'b':[{(3,'0')},{(5,'1')},{(4,'0')},{(3,'0')},{(4,'0')},{(5,'1')},{(6,'1')}]}
r=classify(rows,labels,{0,1,2});assert not r['almost_sure']
assert any(B==frozenset({3,4}) for B in r['supports'])
source=ROOT/'snapshot/audit-continuation-transport-20261010/RESULT.md'
out={'status':'PASS','exact_audit_word_law_comparisons':comparisons,'fresh_positive_likelihood_words':fresh_words,'non_PD_survival_prefixes':64,'fixed_audit_supports':5,'fixed_audit_goal_supports':0,'known_Bad_four_mass_law':[str(x) for x in q4.values()],'posterior_Bad_disagree':'1/5','posterior_two_fresh_disagreements':'1/17','destructive_initial_label_preserved':True,'inherited_audit_result_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'Exact transport of stipulated inherited law; no empirical calibration or source-authentication claim.'}
(ROOT/'SOURCE_TRANSPORT_CONTROLS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
