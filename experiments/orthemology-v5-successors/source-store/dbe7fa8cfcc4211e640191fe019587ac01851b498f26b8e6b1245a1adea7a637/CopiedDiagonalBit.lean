import EffectiveRenewalBoundary
open EffectiveRenewal
-- Must reject a word agreeing with the discovered zero-program diagonal bit.
example : treeCheck [false] = true := by
  simp [treeCheck, coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq,
    Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
