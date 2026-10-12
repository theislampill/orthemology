#!/usr/bin/env python3
"""Independent finite-table controls against the recovered Python evaluator."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import importlib.util,sys,random,json,hashlib
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('atomic_prcodec',root/'recovered/prcodec.py');c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
rng=random.Random(20260930)
C=lambda n:('c',n)
V=lambda n:('v',n)
programs=[
 ('zero',c.Program(2,2,('set',2,C(0)))),
 ('one',c.Program(2,2,('set',2,C(1)))),
 ('fresh_bit',c.Program(2,1,('seq',))),
 ('first_bit',c.Program(2,2,('set',2,('div',V(1),('pow2',V(0)))))),
 ('stage_parity',c.Program(2,0,('seq',))),
 ('prefix_parity',c.Program(2,2,('seq',('set',2,C(0)),('loop',3,('add',V(0),C(1)),('set',2,('add',V(2),('mod',('div',V(1),('pow2',V(3))),C(2)))))))),
 ('fresh_and_previous',c.Program(2,2,('set',2,('mul',V(1),('div',V(1),C(2)))))),
 ('wrong_arity',c.Program(1,2,('set',2,C(1)))),
 ('zero_arity',c.Program(0,2,('set',2,C(1)))),
 ('oversized_output_register',c.Program(2,29,('seq',))),
 ('division_by_zero',c.Program(2,2,('set',2,('div',V(1),C(0))))),
 ('subtraction_truncation',c.Program(2,2,('set',2,('sub',V(0),V(1)))))
]
def ge(d):
 if d==0:return rng.choice([C(rng.randrange(5)),V(rng.randrange(4))])
 k=rng.choice(['add','mul','sub','div','mod','le','eq','pow2'])
 if k=='pow2':return (k,('mod',ge(d-1),C(4)))
 return (k,ge(d-1),ge(d-1))
for j in range(12):programs.append((f'random_{j}',c.Program(2,2,('set',2,ge(2)))))
indices=[(label,c.encode(p)) for label,p in programs]+[('invalid_index',0),('invalid_sentinel',2),('sentinel_only',1)]
checks=[];records=[]
def lw(w):return '#['+', '.join('true' if b else 'false' for b in w)+']'
def lq(q):return f'({q.numerator} / {q.denominator} : ℚ≥0)'
for label,e in indices:
 for N in range(5):
  counts={w:0 for w in product([0,1],repeat=N)}
  for src in product([0,1],repeat=N):
   out=tuple(c.evaluate_index(e,n,c.word_code(src[:n+1]),step_limit=None,max_bits=None)%2 for n in range(N))
   counts[out]+=1
  assert sum(counts.values())==2**N
  if label in ['zero','wrong_arity','zero_arity','invalid_index','invalid_sentinel','sentinel_only','division_by_zero','subtraction_truncation','oversized_output_register']:
   assert counts[(0,)*N]==2**N
  if label in ['fresh_bit','prefix_parity']:
   assert all(v==1 for v in counts.values())
  if label=='first_bit' and N:
   assert counts[(0,)*N]==2**(N-1) and counts[(1,)*N]==2**(N-1)
  if label=='one':assert counts[(1,)*N]==2**N
  if label=='stage_parity':assert counts[tuple(n%2 for n in range(N))]==2**N
  probs={w:Fraction(v,2**N) for w,v in counts.items()}
  for w,q in probs.items():
   checks.append((f'{label}/N{N}/word{"".join(map(str,w))}',f'indexTable {e} {N} (fun i => {lw(w)}[i.val]!) == {lq(q)}'))
  for k in range(6):
   q=sum((v for v in probs.values() if v>=Fraction(1,2**k)),Fraction(0))
   checks.append((f'{label}/N{N}/heavy{k}',f'testHeavy {e} {k} {N} == {lq(q)}'))
   if N==4 and k in [0,1,4]:
    for a,b in [(0,1),(1,2),(3,4),(1,1),(3,2),(4,0),(2,4)]:
     coded=Fraction(a,b) if b else Fraction(0)
     expected='true' if coded>=1 or coded<=q else 'false'
     checks.append((f'{label}/matrix/{a}-{b}/k{k}',f'decide (membershipMatrix {e} (Nat.pair {a} {b}) {k} {N}) == {expected}'))
  records.append({'label':label,'index':str(e),'depth':N,'counts':{''.join(map(str,w)):v for w,v in counts.items()}})
header='''import NumericMembership
open P02A2.FiniteOutputTable AtomicMembership

def testHeavy (e k n : ℕ) : ℚ≥0 :=
  rationalHeavyMass (indexTable e) k n
'''
body=''
batches=[checks[i:i+40] for i in range(0,len(checks),40)]
for j,batch in enumerate(batches):
 body+=f'\ndef batch{j} : IO Nat := do\n  let mut passed := 0\n'
 for label,expr in batch:
  body+=f'  if {expr} then\n    passed := passed + 1\n  else\n    throw (IO.userError "FAIL {label}")\n'
 body+='  return passed\n'
body+='\ndef main : IO Unit := do\n  let mut passed := 0\n'
for j in range(len(batches)):body+=f'  passed := passed + (← batch{j})\n'
body+='  IO.println s!"PASS {passed} exact table, heavy-mass, and numerical matrix differential checks"\n'
(root/'Differential.lean').write_text(header+body)
(root/'DIFFERENTIAL_VECTORS.json').write_text(json.dumps({'checks':len(checks),'programs':len(indices),'source_sha256':hashlib.sha256((root/'recovered/prcodec.py').read_bytes()).hexdigest(),'records':records},indent=2)+'\n')
print(json.dumps({'checks':len(checks),'programs':len(indices)}))
