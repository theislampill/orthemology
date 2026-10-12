#!/usr/bin/env python3
"""Independent direct definition oracle: enumerate components, then valid maxima.
No pruning rounds or author graph routine is used for the expected output.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, random

def subset_masks(u):
    return [v for v in range(16) if v & ~u == 0]

def digits(n,b,length):
    return [(n//(b**i))%b for i in range(length)]

def encode(xs,b): return sum(x*b**i for i,x in enumerate(xs))

def component(g,e):
    es=[i for i in range(4) if e>>i&1]
    if not es:return False
    states={i//2 for i in es}
    edges={(i//2,t) for i in es for t in range(2) if g[i]>>t&1}
    if any(g[i]==0 or any(g[i]>>t&1 and t not in states for t in range(2)) for i in es): return False
    # Direct Warshall, including zero-length paths. Independent of author saturation.
    r={(s,s) for s in states}|edges
    for k in sorted(states):
        for s in sorted(states):
            for t in sorted(states):
                if (s,k) in r and (k,t) in r:r.add((s,t))
    return all((s,t) in r for s in states for t in states)

def expected(case):
    gc,rc,pc,b,theta,u=case
    g=digits(gc,4,4); rows=digits(rc,4,12); pri=digits(pc,6,12)
    val=[]
    for e in subset_masks(u):
        if not component(g,e):continue
        es=[i for i in range(4) if e>>i&1]
        if all(min(pri[m*4+i] for i in es)%2==0
               for m in range(3) if b>>m&1
               if all(rows[m*4+i]==rows[theta*4+i] for i in es)):
            val.append(e)
    out=[e for e in val if not any(e!=d and e&~d==0 for d in val)]
    targets=0
    for e in out:
        for i in range(4):
            if e>>i&1:targets |= 1<<(i//2)
    return sum(1<<e for e in out),targets

def corpus():
    rng=random.Random(202610011535)
    out=[]
    # Every directed support tuple, including missing successor sets.
    for gc in range(256):
        for j in range(8):
            rows=[rng.randrange(4) for _ in range(12)]
            if j%3==0: rows[4:8]=rows[:4]
            if j%3==1: rows[8:12]=rows[:4]
            pri=[rng.randrange(6) for _ in range(12)]
            out.append((gc,encode(rows,4),encode(pri,6),7,j%3,15))
    # Restriction, empty-live-set and noncandidate-membership boundaries.
    for _ in range(2048):
        gc=rng.randrange(256);rc=rng.randrange(4**12);pc=rng.randrange(6**12)
        out.append((gc,rc,pc,rng.randrange(8),rng.randrange(3),rng.randrange(16)))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    cases=corpus(); values=[expected(c) for c in cases]
    payload={'cases':cases,'expected':values}
    (a.output/'ORACLE_CASES.json').write_text(json.dumps(payload,separators=(',',':'))+'\n')
    lean='''import SCCParity
namespace HiddenParity.IndependentOracle
set_option maxRecDepth 100000
set_option maxHeartbeats 0
abbrev S := Fin 2
abbrev P := Fin 4
abbrev M := Fin 3
structure Case where
  graph : Nat
  rows : Nat
  priority : Nat
  live : Nat
  candidate : Nat
  allowed : Nat

def digit (n b i : Nat) : Nat := (n / b^i) % b

def src (e : P) : S := ⟨e.val / 2, by omega⟩
def successors (c : Case) (e : P) : Finset S :=
  Finset.univ.filter (fun s => digit (digit c.graph 4 e.val) 2 s.val = 1)
def rows (c : Case) (m : M) (e : P) : Nat := digit c.rows 4 (m.val*4+e.val)
def priorities (c : Case) (m : M) (e : P) : Nat := digit c.priority 6 (m.val*4+e.val)
def live (c : Case) : Finset M := Finset.univ.filter (fun m => digit c.live 2 m.val = 1)
def allowed (c : Case) : Finset P := Finset.univ.filter (fun e => digit c.allowed 2 e.val = 1)
def pairMask (E : Finset P) : Nat := E.sum (fun e => 2^e.val)
def solve (c : Case) : Nat × Nat :=
  let result := SCCPruning.parityOutput src (successors c) (live c) (rows c) (priorities c)
    ⟨c.candidate % 3, Nat.mod_lt _ (by decide)⟩ (allowed c)
  (result.sum (fun E => 2 ^ pairMask E), (result.biUnion (usedStates src)).sum (fun s => 2^s.val))
def cases : List Case := [
'''
    lean+=',\n'.join('  ⟨'+', '.join(map(str,c))+'⟩' for c in cases)+'\n]\nend HiddenParity.IndependentOracle\n\ndef main : IO Unit := do\n  for (i,c) in HiddenParity.IndependentOracle.cases.zipIdx |>.map (fun (c,i) => (i,c)) do\n    let (out,tgt) := HiddenParity.IndependentOracle.solve c\n    IO.println s!"{i},{out},{tgt}"\n'
    (a.output/'IndependentOracle.lean').write_text(lean)
    result={'status':'EXPECTED_CORPUS_GENERATED','cases':len(cases),'all_graph_support_tuples':256,
      'method':'all subsets; direct Warshall; all matching model minima; maximal valid subsets',
      'expected_sha256':hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()}
    (a.output/'ORACLE_GENERATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
