#!/usr/bin/env python3
"""Source-bound R proof and matrix control. No epistemic predicates are computed."""
import json
from itertools import product
from pathlib import Path

out=Path(__file__).resolve().parent
I=lambda a,b:('imp',a,b)
And=lambda a,b:('and',a,b)
Or=lambda a,b:('or',a,b)
Not=lambda a:('not',a)
a,b,c,d='a','b','c','d'
# Bimbo, Dunn, Ferenz (2018), printed pp.176-177, A1-A16, R1-R2.
AX=[I(a,a), I(I(a,b),I(I(c,a),I(c,b))), I(I(a,I(a,b)),I(a,b)),
 I(I(a,I(b,c)),I(b,I(a,c))), I(I(a,I(I(b,d),c)),I(I(b,d),I(a,c))),
 I(And(a,b),a), I(And(a,b),b), I(And(I(c,a),I(c,b)),I(c,And(a,b))),
 I(I(And(I(a,a),I(b,b)),c),c), I(a,Or(a,b)), I(a,Or(b,a)),
 I(And(I(a,c),I(b,c)),I(Or(a,b),c)),
 I(And(a,Or(b,c)),Or(And(a,b),And(a,c))), I(I(a,Not(a)),Not(a)),
 I(I(a,Not(b)),I(b,Not(a))), I(Not(Not(a)),a)]

def sub(f,m):
 if isinstance(f,str):return m.get(f,f)
 return (f[0],*(sub(x,m) for x in f[1:]))

def fmt(f):
 if isinstance(f,str):return f
 if f[0]=='not':return '¬'+fmt(f[1])
 return '('+fmt(f[1])+{'imp':' →R ','and':' ∧ ','or':' ∨ '}[f[0]]+fmt(f[2])+')'

proof=[]
def ax(k,**m):
 f=sub(AX[k-1],m);proof.append({'formula':f,'kind':'axiom','axiom':k,'substitution':m});return len(proof)
def mp(major,minor):
 mf=proof[major-1]['formula'];nf=proof[minor-1]['formula']
 assert mf[0]=='imp' and mf[1]==nf,(major,minor)
 proof.append({'formula':mf[2],'kind':'modus_ponens','major':major,'minor':minor});return len(proof)

P,N='P','N';B=And(P,I(P,N))
l1=ax(6,a=P,b=I(P,N))             # B -> P
l2=ax(7,a=P,b=I(P,N))             # B -> (P -> N)
l3=ax(2,a=P,b=N,c=B)
l4=ax(4,a=I(P,N),b=I(B,P),c=I(B,N))
l5=mp(l4,l3)
l6=mp(l5,l1)                     # (P -> N) -> (B -> N)
l7=ax(2,a=I(P,N),b=I(B,N),c=B)
l8=mp(l7,l6)
l9=mp(l8,l2)                     # B -> (B -> N)
l10=ax(3,a=B,b=N)
l11=mp(l10,l9)                   # B -> N
l12=ax(1,a=Not(N))
l13=ax(15,a=Not(N),b=N)
l14=mp(l13,l12)                  # N -> ~~N
l15=ax(2,a=N,b=Not(Not(N)),c=B)
l16=mp(l15,l14)
l17=mp(l16,l11)                  # B -> ~~N
l18=ax(15,a=B,b=Not(N))
l19=mp(l18,l17)                  # ~N -> ~B
assert proof[l19-1]['formula']==I(Not(N),Not(B))

# A second pass checks each line from its cited rule, without trusting construction.
def verify(lines):
 for idx,l in enumerate(lines,1):
  if l['kind']=='axiom':
   if l['formula']!=sub(AX[l['axiom']-1],l['substitution']):return False
  elif l['kind']=='modus_ponens':
   if not (0<l['major']<idx and 0<l['minor']<idx):return False
   m=lines[l['major']-1]['formula'];n=lines[l['minor']-1]['formula']
   if not (isinstance(m,tuple) and m[0]=='imp' and m[1]==n and m[2]==l['formula']):return False
  else:return False
 return True
assert verify(proof)
mutant=[dict(x) for x in proof];mutant[-1]['formula']=I(Not(N),B)
assert not verify(mutant)

D=(-2,-1,1,2)
def imp(x,y):return max(-x,y) if x<=y else min(-x,y)
def val(f,m):
 if isinstance(f,str):return m[f]
 if f[0]=='not':return -val(f[1],m)
 x,y=val(f[1],m),val(f[2],m)
 return {'imp':imp,'and':min,'or':max}[f[0]](x,y)
checks=[]
for k,f in enumerate(AX,1):
 rows=[dict(zip((a,b,c,d),t)) for t in product(D,repeat=4)]
 bad=[m for m in rows if val(f,m)<1]
 assert not bad
 checks.append({'axiom':k,'assignments':len(rows),'failures':len(bad)})
mp_bad=[(x,y) for x,y in product(D,repeat=2) if x>0 and imp(x,y)>0 and y<1]
and_bad=[(x,y) for x,y in product(D,repeat=2) if x>0 and y>0 and min(x,y)<1]
assert not mp_bad and not and_bad
identity=[{'Q':q,'N':imp(q,q),'not_N':-imp(q,q)} for q in D]
assert all(t['N']>0 and t['not_N']<0 for t in identity)
Q=1;target=imp(Q,Q)
control={'Q':Q,'N_equals_Q_implies_Q':target,'P':2,'material_not_P_or_N':max(-2,target),
'relevant_P_implies_N':imp(2,target),'sensitivity_to_P':imp(-target,-2)}
assert control['material_not_P_or_N']>0 and control['relevant_P_implies_N']<0
compound=[]
for p,q in product(D,repeat=2):
 n=imp(q,q); mat=max(-p,n); basis=min(p,mat)
 compound.append({'P':p,'Q':q,'N':n,'material_conditional':mat,'compound_basis':basis,
 'basis_implies_N':imp(basis,n),'not_N_implies_not_basis':imp(-n,-basis)})
assert all(r['basis_implies_N']>0 and r['not_N_implies_not_basis']>0 for r in compound)
contrast=[]
for ec,eg in ((1,2),(2,1)):
 contrast.append({'N':target,'E_competent':ec,'E_guess':eg,'Basing_C_fact':1,'Basing_G_fact':1,
 'not_N_implies_not_E_C':imp(-target,-ec),'not_N_implies_not_E_G':imp(-target,-eg),
 'ceiling':'Formal reduct only; no competence-to-intension bridge is included.'})
result={'logic_source':'Bimbo, Dunn and Ferenz2018 printed176-177, A1-A16 and R1-R2',
 'proof_lines':len(proof),'syntactic_proof_verified':verify(proof),'wrong_final_consequent_rejected':not verify(mutant),
 'proved_formula':fmt(proof[-1]['formula']), 'arrow':'Relevant implication throughout, never material implication',
 'matrix':{'values':D,'designated':[1,2],'negation':'-x','conjunction':'min','disjunction':'max',
 'conditional':'max(-x,y) if x<=y; min(-x,y) otherwise','axioms':checks,
 'modus_ponens_failures':mp_bad,'adjunction_failures':and_bad,
 'soundness_claim':'R-sound by finite axiom/rule check and induction on proofs; no completeness claim',
 'contradictory_designated_values':[x for x in D if x>0 and -x>0]},
 'necessary_identity_control':identity,'material_to_relevant_upgrade_control':control,
 'compound_material_basis_control':{'rows':compound,'all_pass':True,'ceiling':'Success in one R-sound matrix is not proof of R theoremhood or of general epistemic closure.'},
 'experience_swap_controls':contrast,
 'epistemic_ceiling':'No cognition, proper function, subject knowledge or metaphysical possibility is inferred from this computation.'}
(out/'CHECK_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['# A checked relevant factive ground derivation','',
 '→R is relevant implication. P and N are arbitrary formulas. B abbreviates P ∧ (P →R N).',
 'Each line is an instance of a source-listed axiom or modus ponens from prior lines.','']
for i,l in enumerate(proof,1):
 reason='A'+str(l['axiom']) if l['kind']=='axiom' else f"MP {l['major']}, {l['minor']}"
 lines.append(f"{i}. {fmt(l['formula'])}    [{reason}]")
lines+=['','The checker verifies the syntactic derivation and rejects a mutated final consequent.',
'This is a logical theorem. Calling B the actual epistemic basis additionally requires the subject to know and use its components.']
(out/'RELEVANT_PROOF.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'proof_lines':len(proof),'proof_verified':True,'matrix_axiom_evaluations':sum(x['assignments'] for x in checks),'upgrade_control':control},ensure_ascii=False,indent=2))
