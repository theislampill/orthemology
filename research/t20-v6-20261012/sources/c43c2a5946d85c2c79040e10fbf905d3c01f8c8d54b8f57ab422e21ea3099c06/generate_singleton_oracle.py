"""Independent finite-policy/bottom-SCC oracle for singleton observed-state MDPs.
Produces source-only Lean region checks. It does not edit the frozen packet.
"""
from pathlib import Path
from itertools import product
import random, json, hashlib
ROOT=Path(__file__).resolve().parent

def closure(start,edges):
    seen={start}; todo=[start]
    while todo:
        s=todo.pop()
        for t in edges[s]:
            if t not in seen: seen.add(t); todo.append(t)
    return seen

def oracle(rows,prios,menu):
    wins=set()
    for pol in product(*(v if v else [0] for v in menu)):
        edges=[set(rows[2*s+pol[s]]) for s in range(2)]
        reaches=[closure(s,edges) for s in range(2)]
        components={frozenset(t for t in range(2) if t in reaches[s] and s in reaches[t]) for s in range(2)}
        bottom=[C for C in components if all(edges[s]<=C for s in C)]
        bad={s for C in bottom if min(prios[2*t+pol[t]] for t in C)%2==1 for s in C}
        dead={s for s in range(2) if not menu[s]}
        for s in range(2):
            if not reaches[s]&(bad|dead): wins.add(s)
    return sorted(wins)

rng=random.Random(20261001)
cases=[]
# Mix dead menus, all actions, single actions, varied recurrent minima and support.
for i in range(48):
    rows=[rng.choice([[0],[1],[0,1]]) for _ in range(4)]
    prios=[rng.randrange(8) for _ in range(4)]
    menu=[rng.choice([[],[0],[1],[0,1]]) for _ in range(2)]
    cases.append(dict(id=i,rows=rows,priorities=prios,menu=menu,expected=oracle(rows,prios,menu)))

def fs(v): return '∅' if not v else '{'+','.join(map(str,v))+'}'
def val(row): return '1' if row==[0] else '0' if row==[1] else 'half'
def select(vals):
    return f'if e.1 = 0 then (if e.2 = 0 then {vals[0]} else {vals[1]}) else (if e.2 = 0 then {vals[2]} else {vals[3]})'
lines=['import GlobalParitySufficiency','noncomputable section','namespace IndependentSingletonOracle',
       'open HiddenParity HiddenParity.Necessity','set_option maxRecDepth 100000','set_option maxHeartbeats 12000000',
       'def half : ℚ := ⟨1,2,by decide,by decide⟩',
       "theorem half_value : half = 1/2 := by norm_num [half,Rat.mk'_eq_divInt,Rat.divInt_eq_div]"]
for c in cases:
    i=c['id']
    lines += [f'def weight{i} (e : Fin 2 × Fin 2) : ℚ := {select([val(r) for r in c["rows"]])}',
              f'def complement{i} (e : Fin 2 × Fin 2) : ℚ := {select(["0" if r==[0] else "1" if r==[1] else "half" for r in c["rows"]])}',
              f'def kernel{i} : RationalKernel (Fin 1) (Fin 2 × Fin 2) (Fin 2) where',
              f'  row := fun _ e y => if y = 0 then weight{i} e else complement{i} e',
              f'  nonnegative := by intro m e y; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> fin_cases y <;> norm_num [weight{i},complement{i},half_value]',
              f'  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases a <;> norm_num [Fin.sum_univ_two,weight{i},complement{i},half_value]',
              f'def priority{i} (_ : Fin 1) (e : Fin 2 × Fin 2) : ℕ := {select(c["priorities"])}',
              f'def menu{i} (_ : Finset (Fin 1)) (s : Fin 2) : Finset (Fin 2) := if s = 0 then {fs(c["menu"][0])} else {fs(c["menu"][1])}',
              f'theorem oracle_case_{i} : winningRegion kernel{i} menu{i} priority{i} Finset.univ = ({fs(c["expected"])} : Finset (Fin 2)) := by decide',
              f'#print axioms oracle_case_{i}']
lines+=['end IndependentSingletonOracle']
(ROOT/'SingletonOracleProbes.lean').write_text('\n'.join(lines)+'\n')
(ROOT/'SINGLETON_ORACLE_CASES.json').write_text(json.dumps({'seed':20261001,'case_count':len(cases),'method':'Enumerate deterministic stationary policies; reject reachable empty menus and any reachable bottom SCC whose minimum state/action priority is odd','cases':cases},indent=2)+'\n')
print('generated',len(cases),'cases; output cardinalities', {k:sum(len(c['expected'])==k for c in cases) for k in range(3)})
print('lean_sha256',hashlib.sha256((ROOT/'SingletonOracleProbes.lean').read_bytes()).hexdigest())
