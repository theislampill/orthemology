import SCCPruning
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
