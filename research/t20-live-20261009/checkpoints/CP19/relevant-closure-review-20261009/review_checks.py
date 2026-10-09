#!/usr/bin/env python3
"""Independent source-bound review. Reads author script; does not execute its writes."""
import hashlib, json
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'necessary-truth-operative-basing-20261009/check_relevant_bridge.py'
src=AUTHOR.read_text()
# Execute only formula construction, before the author's verification/output code.
ns={'__file__':str(AUTHOR)}
exec(compile(src.split('# A second pass')[0],str(AUTHOR),'exec'),ns)
I=lambda x,y:('imp',x,y)
A=lambda x,y:('and',x,y)
O=lambda x,y:('or',x,y)
N=lambda x:('not',x)
a,b,c,d='a','b','c','d'
# Independently transcribed from Bimbo-Dunn-Ferenz2018, printed176-177.
axioms=[I(a,a),I(I(a,b),I(I(c,a),I(c,b))),I(I(a,I(a,b)),I(a,b)),
 I(I(a,I(b,c)),I(b,I(a,c))),I(I(a,I(I(b,d),c)),I(I(b,d),I(a,c))),
 I(A(a,b),a),I(A(a,b),b),I(A(I(c,a),I(c,b)),I(c,A(a,b))),
 I(I(A(I(a,a),I(b,b)),c),c),I(a,O(a,b)),I(a,O(b,a)),
 I(A(I(a,c),I(b,c)),I(O(a,b),c)),I(A(a,O(b,c)),O(A(a,b),A(a,c))),
 I(I(a,N(a)),N(a)),I(I(a,N(b)),I(b,N(a))),I(N(N(a)),a)]
assert axioms==ns['AX']
def match(schema,formula,sub=None):
 sub={} if sub is None else sub
 if isinstance(schema,str):
  if schema in sub:return sub if sub[schema]==formula else None
  sub[schema]=formula;return sub
 if not isinstance(formula,tuple) or len(schema)!=len(formula) or schema[0]!=formula[0]:return None
 for s,f in zip(schema[1:],formula[1:]):
  if match(s,f,sub) is None:return None
 return sub
proof=ns['proof']; checked=[]
for line,entry in enumerate(proof,1):
 f=entry['formula']
 if entry['kind']=='axiom':
  assert match(axioms[entry['axiom']-1],f) is not None
 else:
  x,y=entry['major'],entry['minor']
  assert 0<x<line and 0<y<line
  assert proof[x-1]['formula']==I(proof[y-1]['formula'],f)
 checked.append(line)
P,Q='P','Q';B=A(P,I(P,Q));assert proof[-1]['formula']==I(N('N'),N(A(P,I(P,'N'))))
D=(-2,-1,1,2)
# Explicit table independently evaluates the author's arithmetic definition.
TABLE=((2,2,2,2),(-2,1,1,2),(-2,-1,1,2),(-2,-2,-2,2))
def imp(x,y):return TABLE[D.index(x)][D.index(y)]
def ev(f,v):
 if isinstance(f,str):return v[f]
 if f[0]=='not':return -ev(f[1],v)
 x,y=ev(f[1],v),ev(f[2],v)
 return {'imp':imp,'and':min,'or':max}[f[0]](x,y)
assert all(imp(x,y)==(max(-x,y) if x<=y else min(-x,y)) for x,y in product(D,repeat=2))
checks=[]
for j,f in enumerate(axioms,1):
 bad=[v for values in product(D,repeat=4) if ev(f,v:=dict(zip((a,b,c,d),values)))<0]
 assert not bad
 checks.append({'axiom':j,'valuations':256,'failures':0})
assert all(y>0 for x,y in product(D,repeat=2) if x>0 and imp(x,y)>0)
assert all(min(x,y)>0 for x,y in product(D,repeat=2) if x>0 and y>0)
relevant=[];material_general=[];material_true_target=[];material_necessary=[]
for p,q in product(D,repeat=2):
 relevant.append(imp(min(p,imp(p,q)),q))
 matbasis=min(p,max(-p,q))
 if imp(matbasis,q)<0:material_general.append({'p':p,'q':q,'basis':matbasis,'arrow':imp(matbasis,q)})
 if q>0:material_true_target.append(imp(matbasis,q))
 n=imp(q,q);basis=min(p,max(-p,n));material_necessary.append(imp(basis,n))
assert min(relevant)>0 and min(material_true_target)>0 and min(material_necessary)>0
result={
 'author_script_sha256':hashlib.sha256(src.encode()).hexdigest(),
 'syntactic_lines_independently_verified':checked,
 'axioms_match_primary_transcription':True,
 'matrix_axiom_checks':checks,'both_rules_preserve_designation':True,
 'relevant_conjunctive_bridge_all_16_pass':True,
 'material_p_only_bridge_countervaluation':{'p':2,'q':1,'material':1,'p_to_q':-2,'not_q_to_not_p':-2},
 'material_compound_general_schema_failures':material_general,
 'material_compound_all_positive_targets_pass':True,
 'material_compound_necessary_identity_all_16_pass':True,
 'ceiling':'No belief, knowledge, competence, basing, necessity modality or full counterfactual semantics has been interpreted. Object-formula invalidity is not automatically epistemic closure failure.'}
(ROOT/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='matrix_axiom_checks'},indent=2))
