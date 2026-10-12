#!/usr/bin/env python3
"""Independent direct-predicate oracle; expected values never use SCC pruning."""
from pathlib import Path
from itertools import product
import hashlib,json,random

OUT=Path(__file__).resolve().parent/'independent-oracles'
def digits(v,b,k):return tuple((v//b**i)%b for i in range(k))
def enc(xs,b):return sum(x*b**i for i,x in enumerate(xs))
def pval(x):return x if x<4 else 2**70+x-4

def ec(src,succ,E):
    if not E:return False
    pairs=[i for i in range(4) if E>>i&1]
    states=0
    for e in pairs:states|=1<<src[e]
    if any(not succ[e] or succ[e]&~states for e in pairs):return False
    reach=[1<<s for s in range(3)]
    for e in pairs:reach[src[e]]|=succ[e]
    for mid in range(3):
        for s in range(3):
            if reach[s]>>mid&1:reach[s]|=reach[mid]
    return all(reach[s]&states==states for s in range(3) if states>>s&1)

def expected(c):
    mode,sc,gc,rc,pc,B,theta,U=c
    src=digits(sc,3,4);succ=digits(gc,8,4);rows=digits(rc,4,12);pri=tuple(pval(x) for x in digits(pc,7,12))
    valid=[]
    for E in range(1,16):
        if E&~U or not ec(src,succ,E):continue
        pairs=[i for i in range(4) if E>>i&1]
        if mode and any(all(rows[4*m+e]==rows[4*theta+e] for e in pairs) and
                        min(pri[4*m+e] for e in pairs)%2
                        for m in range(3) if B>>m&1):continue
        valid.append(E)
    maxima=[E for E in valid if not any(E!=F and E&~F==0 for F in valid)]
    target=0
    for E in maxima:
        for e in range(4):
            if E>>e&1:target|=1<<src[e]
    return sum(1<<E for E in maxima),target

def main():
    OUT.mkdir(exist_ok=True)
    rng=random.Random(202610011705)
    cases=[]
    # Exhaust all 4096 successor tuples, with two actions sharing a source.
    for g in range(8**4):cases.append((0,enc((0,0,1,2),3),g,0,0,0,0,15))
    # Every source assignment, including absent states and complete source aliasing.
    for src in product(range(3),repeat=4):
        for j in range(32):
            succ=[rng.randrange(8) for _ in range(4)]
            if j%8==0:succ[j%4]=0
            cases.append((0,enc(src,3),enc(succ,8),0,0,0,0,rng.randrange(16)))
    # Independent parity corpus includes large binary priorities, restrictions,
    # no live models, non-live candidates, and rivals that can rematch on a subset.
    for j in range(2048):
        src=[rng.randrange(3) for _ in range(4)];succ=[rng.randrange(8) for _ in range(4)]
        if j%8==0:src=[0,0,0,0];succ=[1]*4
        rows=[rng.randrange(4) for _ in range(12)]
        if j%3==0:rows[4:8]=rows[:4]
        if j%3==1:
            rows[8:12]=rows[:4];rows[8+j%4]=(rows[j%4]+1)%4
        pri=[rng.randrange(7) for _ in range(12)]
        cases.append((1,enc(src,3),enc(succ,8),enc(rows,4),enc(pri,7),rng.randrange(8),rng.randrange(3),rng.randrange(16)))
    values=[expected(c) for c in cases]
    payload={'cases':cases,'expected':values}
    (OUT/'CASES.json').write_text(json.dumps(payload,separators=(',',':'))+'\n')
    source='''import SCCParity
namespace IndependentMECOracle
set_option maxRecDepth 200000
set_option maxHeartbeats 0
abbrev S := Fin 3
abbrev E := Fin 4
abbrev M := Fin 3
structure Case where
  mode : Nat
  sources : Nat
  successors : Nat
  rows : Nat
  priorities : Nat
  live : Nat
  candidate : Nat
  allowed : Nat

def digit (x base i : Nat) : Nat := (x / base^i)%base
def source (c : Case) (e : E) : S := ⟨digit c.sources 3 e.val, Nat.mod_lt _ (by decide)⟩
def successors (c : Case) (e : E) : Finset S :=
  Finset.univ.filter (fun s => digit (digit c.successors 8 e.val) 2 s.val = 1)
def rows (c : Case) (m : M) (e : E) : Nat := digit c.rows 4 (m.val*4+e.val)
def pvalue (x : Nat) : Nat := if x<4 then x else 2^70+x-4
def priorities (c : Case) (m : M) (e : E) : Nat := pvalue (digit c.priorities 7 (m.val*4+e.val))
def allowed (c : Case) : Finset E := Finset.univ.filter (fun e => digit c.allowed 2 e.val=1)
def live (c : Case) : Finset M := Finset.univ.filter (fun m => digit c.live 2 m.val=1)
def solve (c : Case) : Nat × Nat :=
  let result := if c.mode=0 then HiddenParity.SCCPruning.mecs (source c) (successors c) (allowed c)
    else HiddenParity.SCCPruning.parityOutput (source c) (successors c) (live c) (rows c) (priorities c)
      ⟨c.candidate%3,Nat.mod_lt _ (by decide)⟩ (allowed c)
  (result.sum (fun D => 2^(D.sum (fun e => 2^e.val))),
    (result.biUnion (HiddenParity.usedStates (source c))).sum (fun s => 2^s.val))
def cases : List Case := [
'''
    source+=',\n'.join('⟨'+','.join(map(str,c))+'⟩' for c in cases)+'\n]\nend IndependentMECOracle\n\ndef main : IO Unit := do\n  for (c,i) in IndependentMECOracle.cases.zipIdx do\n    let (d,s) := IndependentMECOracle.solve c\n    IO.println s!"{i},{d},{s}"\n'
    (OUT/'IndependentOracle.lean').write_text(source)
    report={'status':'EXPECTED_VALUES_GENERATED','total_cases':len(cases),'mec_cases':6688,'parity_cases':2048,'states':3,'pairs':4,'models':3,'all_successor_tuples_for_source_0012':4096,'all_source_assignments':81,'large_priority_bits':71,'method':'Direct exhaustive subset predicates; closure, independent bitset Warshall, full row matching and maximal valid subsets. No pruning algorithm used for expected values.','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cases_sha256':hashlib.sha256((OUT/'CASES.json').read_bytes()).hexdigest()}
    (OUT/'GENERATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
