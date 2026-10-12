"""Observationally identical one-state models: independently enumerate all
possible recurrent action sets and test every hidden model's minimum parity."""
from pathlib import Path
from itertools import combinations
import random,json,hashlib
ROOT=Path(__file__).resolve().parent

def oracle(prios,menu):
    qualifying=[]
    for mask in range(1,8):
        U=[a for a in range(3) if mask&(1<<a)]
        if set(U)<=set(menu) and all(min(p[a] for a in U)%2==0 for p in prios): qualifying.append(U)
    return qualifying
rng=random.Random(14857)
cases=[dict(id=0,priorities=[[2,3,1],[3,2,1]],menu=[0,1]),dict(id=1,priorities=[[2,1,1],[1,2,1]],menu=[0,1])]
for i in range(2,66):
    cases.append(dict(id=i,priorities=[[rng.randrange(6) for a in range(3)] for m in range(2)],menu=[a for a in range(3) if rng.randrange(2)]))
for c in cases:c['qualifying_recurrent_sets']=oracle(c['priorities'],c['menu']);c['expected']=bool(c['qualifying_recurrent_sets'])
def fs(v):return '∅' if not v else '{'+','.join(map(str,v))+'}'
def sel(p):return f'if e.2 = 0 then {p[0]} else if e.2 = 1 then {p[1]} else {p[2]}'
lines=['import GlobalParitySufficiency','noncomputable section','namespace IndependentHiddenIdenticalOracle','open HiddenParity HiddenParity.Necessity','set_option maxRecDepth 100000','set_option maxHeartbeats 12000000',
'def kernel : RationalKernel (Fin 2) (Fin 1 × Fin 3) (Fin 1) where','  row := fun _ _ _ => 1','  nonnegative := by intros; norm_num','  normalized := by intros; simp']
for c in cases:
 i=c['id'];out='Finset.univ' if c['expected'] else '∅'
 lines += [f'def priority{i} (m : Fin 2) (e : Fin 1 × Fin 3) : ℕ := if m = 0 then ({sel(c["priorities"][0])}) else ({sel(c["priorities"][1])})',f'def menu{i} (_ : Finset (Fin 2)) (_ : Fin 1) : Finset (Fin 3) := {fs(c["menu"])}',f'theorem hidden_oracle_case_{i} : winningRegion kernel menu{i} priority{i} Finset.univ = ({out} : Finset (Fin 1)) := by decide',f'#print axioms hidden_oracle_case_{i}']
lines+=['end IndependentHiddenIdenticalOracle']
(ROOT/'HiddenIdenticalOracleProbes.lean').write_text('\n'.join(lines)+'\n')
(ROOT/'HIDDEN_IDENTICAL_ORACLE_CASES.json').write_text(json.dumps({'seed':14857,'case_count':len(cases),'method':'All rows identical at one observed state: enumerate nonempty recurrent action subsets and require even minimum in every model','cases':cases},indent=2)+'\n')
print('generated',len(cases),'hidden identical cases; winning',sum(c['expected'] for c in cases),'losing',sum(not c['expected'] for c in cases))
print('lean_sha256',hashlib.sha256((ROOT/'HiddenIdenticalOracleProbes.lean').read_bytes()).hexdigest())
