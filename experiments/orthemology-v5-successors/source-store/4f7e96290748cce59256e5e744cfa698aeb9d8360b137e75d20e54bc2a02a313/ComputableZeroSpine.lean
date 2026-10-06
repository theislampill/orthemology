import SkeletonUnion
open EffectiveRenewal PolicySynthesis
-- A unary all-zero selector spine would admit this prefix. The real skeleton rejects it.
example (p : Nat) : synthesisCheck p [false, false] = true := by
  simp [synthesisCheck, synthesisClause, allBelow, controlsClear, skeletonWord, slice,
    treeCheck, coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq,
    Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
