import SequentialAuditRepair
open Orthemology.Tranche3

def main (args : List String) : IO Unit := do
  let n := (args.headD "512").toNat!
  let steps := (args[1]?.getD "20").toNat!
  let beta : ℚ := (1/20)/(2*(n:ℚ)*(n+1))
  let l := sequentialReferenceLower n (n/2) beta steps
  let u := sequentialReferenceUpper n (n/2) beta steps
  let result := rationalCertificate l u (1/4) 0
  IO.println s!"samples={n}; successes={n/2}; bisections={steps}"
  IO.println s!"lower={l}; upper={u}; repair={result}"
  IO.println s!"regret={rationalValue l u (1/4)}"
