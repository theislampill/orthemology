#!/usr/bin/env python3
from pathlib import Path
import argparse,json

def oracle(g,u):
 edges=[(g//8**i)%8 for i in range(3)];valid=[]
 for e in range(1,8):
  if e&~u:continue
  states=[i for i in range(3) if e>>i&1]
  if any(edges[i]==0 or edges[i]&~e for i in states):continue
  r={(i,i) for i in states}|{(i,j) for i in states for j in states if edges[i]>>j&1}
  for k in states:
   for i in states:
    for j in states:
     if (i,k) in r and (k,j) in r:r.add((i,j))
  if all((i,j) in r for i in states for j in states):valid.append(e)
 return sum(1<<e for e in valid if not any(e!=d and e&~d==0 for d in valid))

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 expected=[[g,u,oracle(g,u)] for g in range(512) for u in range(8)]
 (a.output/'EXPECTED.json').write_text(json.dumps(expected,separators=(',',':'))+'\n')
 source='''import SCCPruning
namespace HiddenParity.MECOracle
abbrev V := Fin 3
set_option maxRecDepth 100000
set_option maxHeartbeats 0
def successors (g : Nat) (e : V) : Finset V :=
  Finset.univ.filter (fun s => (g / 8^e.val / 2^s.val) % 2 = 1)
def allowed (u : Nat) : Finset V := Finset.univ.filter (fun e => (u / 2^e.val) % 2 = 1)
def signature (g u : Nat) : Nat :=
  (SCCPruning.mecs (fun e : V => e) (successors g) (allowed u)).sum
    (fun E => 2 ^ E.sum (fun e => 2^e.val))
end HiddenParity.MECOracle

def main : IO Unit := do
  for g in List.range 512 do
    for u in List.range 8 do
      IO.println s!"{g},{u},{HiddenParity.MECOracle.signature g u}"
'''
 (a.output/'MECOracle.lean').write_text(source)
 print('Generated 4096 exhaustive three-state graph/restriction cases')
if __name__=='__main__':main()
