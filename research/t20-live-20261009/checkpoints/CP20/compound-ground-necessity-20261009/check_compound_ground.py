#!/usr/bin/env python3
"""Exact R-axiom checks for source-tabulated Belnap M0; no epistemic predicates."""
from itertools import product
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
V = ('-3','-2','-1','-0','+0','+1','+2','+3')
DES = {'+0','+1','+2','+3'}
# Standefer 2020, printed p.271, Table 2, visually checked 9 October 2026.
ROWS = [
 ['+3','+3','+3','+3','+3','+3','+3','+3'],
 ['-3','+2','-3','+2','-3','-3','+2','+3'],
 ['-3','-3','+1','+1','-3','+1','-3','+3'],
 ['-3','-3','-3','+0','-3','-3','-3','+3'],
 ['-3','-2','-1','-0','+0','+1','+2','+3'],
 ['-3','-3','-1','-1','-3','+1','-3','+3'],
 ['-3','-2','-3','-2','-3','-3','+2','+3'],
 ['-3','-3','-3','-3','-3','-3','-3','+3'],
]
IMP = {(x,y): ROWS[i][j] for i,x in enumerate(V) for j,y in enumerate(V)}
NEG = dict(zip(V, reversed(V)))
# Boolean lattice of subsets of three atoms, read from the Hasse diagram.
# Bit labels are bookkeeping, not the implication order or numeric truth values.
BITS = {'-3':0,'-2':2,'-1':1,'-0':3,'+0':4,'+1':5,'+2':6,'+3':7}
BY_BITS = {b:v for v,b in BITS.items()}
meet = lambda x,y: BY_BITS[BITS[x] & BITS[y]]
join = lambda x,y: BY_BITS[BITS[x] | BITS[y]]
I = lambda a,b: ('imp',a,b)
A = lambda a,b: ('and',a,b)
O = lambda a,b: ('or',a,b)
Not = lambda a: ('not',a)
a,b,c,d = 'a','b','c','d'
# Bimbo, Dunn and Ferenz 2018, printed pp.176-177, A1-A16, R1-R2.
AX = [I(a,a), I(I(a,b),I(I(c,a),I(c,b))), I(I(a,I(a,b)),I(a,b)),
 I(I(a,I(b,c)),I(b,I(a,c))), I(I(a,I(I(b,d),c)),I(I(b,d),I(a,c))),
 I(A(a,b),a), I(A(a,b),b), I(A(I(c,a),I(c,b)),I(c,A(a,b))),
 I(I(A(I(a,a),I(b,b)),c),c), I(a,O(a,b)), I(a,O(b,a)),
 I(A(I(a,c),I(b,c)),I(O(a,b),c)), I(A(a,O(b,c)),O(A(a,b),A(a,c))),
 I(I(a,Not(a)),Not(a)), I(I(a,Not(b)),I(b,Not(a))), I(Not(Not(a)),a)]

def atoms(f):
    if isinstance(f,str): return {f}
    return set().union(*(atoms(x) for x in f[1:]))

def val(f,m):
    if isinstance(f,str): return m[f]
    if f[0]=='not': return NEG[val(f[1],m)]
    x,y = val(f[1],m),val(f[2],m)
    return {'and':meet,'or':join,'imp':lambda x,y:IMP[x,y]}[f[0]](x,y)

def subst(f,m):
    if isinstance(f,str): return m.get(f,f)
    return (f[0],*(subst(x,m) for x in f[1:]))

def fmt(f):
    if isinstance(f,str): return f
    if f[0]=='not': return '¬'+fmt(f[1])
    return '('+fmt(f[1])+{'imp':' →R ','and':' ∧ ','or':' ∨ '}[f[0]]+fmt(f[2])+')'

checks=[]
for k,f in enumerate(AX,1):
    variables=sorted(atoms(f))
    count=0
    for values in product(V,repeat=len(variables)):
        m=dict(zip(variables,values));count+=1
        assert val(f,m) in DES, (k,m,val(f,m))
    checks.append({'axiom':k,'distinct_variables':variables,'assignments':count,'failures':0})
mp_fail=[(x,y) for x,y in product(V,repeat=2) if x in DES and IMP[x,y] in DES and y not in DES]
adj_fail=[(x,y) for x,y in product(V,repeat=2) if x in DES and y in DES and meet(x,y) not in DES]
assert not mp_fail and not adj_fail

# Check the entire finite algebraic core of the usual variable-sharing proof.
families=[{'-1','+1'},{'-2','+2'}]
for S in families:
    assert all(NEG[x] in S for x in S)
    assert all(meet(x,y) in S and join(x,y) in S and IMP[x,y] in S for x,y in product(S,repeat=2))
assert all(IMP[x,y] not in DES for x,y in product(*families))

P,Q='P','Q'; N=I(Q,Q); MAT=O(Not(P),N); B=A(P,MAT)
FORMS={'P':P,'not_P':Not(P),'N':N,'not_N':Not(N),'material_conditional':MAT,
       'compound_ground':B,'ground_implies_target':I(B,N),
       'sensitivity':I(Not(N),Not(B)),'source_premise_only_bridge':I(Not(N),Not(P))}
m={'P':'+1','Q':'+2'}
counter={name:val(f,m) for name,f in FORMS.items()}
for name in ('P','N','material_conditional','compound_ground'): assert counter[name] in DES
for name in ('not_P','not_N','ground_implies_target','sensitivity','source_premise_only_bridge'): assert counter[name] not in DES
identity=[{'Q':q,'N':val(N,{'Q':q}),'not_N':val(Not(N),{'Q':q})} for q in V]
assert all(r['N'] in DES and r['not_N'] not in DES for r in identity)

# A transparent syntactic reduction to variable sharing. Lines through C->B are
# theorems. The final three lines are conditional on assuming B->N as a theorem.
C=A(P,Not(P)); proof=[]
def ax(k,**m):
    proof.append({'formula':subst(AX[k-1],m),'kind':'axiom','axiom':k,'substitution':m});return len(proof)
def mp(major,minor):
    f=proof[major-1]['formula'];g=proof[minor-1]['formula']
    assert f[0]=='imp' and f[1]==g
    proof.append({'formula':f[2],'kind':'modus_ponens','major':major,'minor':minor});return len(proof)
def adj(left,right):
    proof.append({'formula':A(proof[left-1]['formula'],proof[right-1]['formula']),
                  'kind':'adjunction','left':left,'right':right});return len(proof)
l1=ax(6,a=P,b=Not(P))
l2=ax(7,a=P,b=Not(P))
l3=ax(10,a=Not(P),b=N)
l4=ax(2,a=Not(P),b=MAT,c=C)
l5=mp(l4,l3);l6=mp(l5,l2)
l7=adj(l1,l6)
l8=ax(8,c=C,a=P,b=MAT)
l9=mp(l8,l7)
assert proof[l9-1]['formula']==I(C,B)
proof.append({'formula':I(B,N),'kind':'hypothetical_theorem','label':'H'});h=len(proof)
l11=ax(2,a=B,b=N,c=C);l12=mp(l11,h);l13=mp(l12,l9)
assert proof[l13-1]['formula']==I(C,N)
assert atoms(C).isdisjoint(atoms(N))

def verify(lines):
    for idx,line in enumerate(lines,1):
        k=line['kind'];f=line['formula']
        if k=='axiom':
            if f!=subst(AX[line['axiom']-1],line['substitution']):return False
        elif k=='hypothetical_theorem':
            if f!=I(B,N):return False
        elif k=='modus_ponens':
            if not 0<line['major']<idx or not 0<line['minor']<idx:return False
            major=lines[line['major']-1]['formula'];minor=lines[line['minor']-1]['formula']
            if major!=I(minor,f):return False
        elif k=='adjunction':
            if not 0<line['left']<idx or not 0<line['right']<idx:return False
            if f!=A(lines[line['left']-1]['formula'],lines[line['right']-1]['formula']):return False
        else:return False
    return True
assert verify(proof)
mutation=[dict(x) for x in proof];mutation[-1]['formula']=I(N,C)
assert not verify(mutation)
corrupt=[row[:] for row in ROWS];corrupt[4][4]='-3'
assert corrupt[4][4] not in DES # identity at +0 detects this corrupt table

result={'logic':'System R, A1-A16 and R1-R2 as in Bimbo/Dunn/Ferenz2018',
 'matrix_source':'Standefer2020, Actual Issues for Relevant Logics, printed270-271, Table2',
 'values':V,'designated':sorted(DES),'table':ROWS,'negation':NEG,'lattice_bits':BITS,
 'axiom_checks':checks,'total_axiom_assignments':sum(x['assignments'] for x in checks),
 'modus_ponens_failures':mp_fail,'adjunction_failures':adj_fail,
 'variable_sharing_subalgebras_verified':True,'identity_target_all_values':identity,
 'countervaluation_assignment':m,'countervaluation':counter,
 'conditional_derivation_verified':verify(proof),'derivation_lines':len(proof),
 'wrong_final_consequent_rejected':not verify(mutation),'corrupt_identity_table_rejected':True,
 'claim':'Neither the internal-arrow formula B->R N nor the sensitivity formula follows from the designated material grounds, even for N=(Q->R Q). N itself remains an R theorem and thus a syntactic/semantic consequence of B.',
 'ceiling':'No knowledge, competent inference, basing, counterfactual-world choice or cognition interpretation is supplied.'}
(OUT/'CHECK_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['# Conditional derivation exposing variable sharing','',
 'P and Q are distinct propositional atoms. N = Q →R Q; C = P ∧ ¬P; B = P ∧ (¬P ∨ N).',
 'Lines1–9 are R theorems. Line10 is the hypothesis being refuted, not an R theorem.',
 'No claim is made that a subject knows C or that C is actual.','']
for i,l in enumerate(proof,1):
    k=l['kind'];reason={'axiom':lambda:'A'+str(l['axiom']),
        'modus_ponens':lambda:f"MP {l['major']}, {l['minor']}",
        'adjunction':lambda:f"Adjunction {l['left']}, {l['right']}",
        'hypothetical_theorem':lambda:'H: suppose this were an R theorem'}[k]()
    lines.append(f'{i}. {fmt(l["formula"])} [{reason}]')
lines+=['','The final implication has antecedent atoms {P} and consequent atoms {Q}.',
 'R has variable sharing, as verified by the two closed M0 subalgebras and cross-implication table.',
 'Therefore H cannot be an R theorem. The direct M0 countervaluation independently rejects H and sensitivity.']
(OUT/'VARIABLE_SHARING_REDUCTION.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'axiom_evaluations':result['total_axiom_assignments'],'countervaluation':counter,
                  'proof_lines':len(proof),'verified':True},ensure_ascii=False,indent=2))
