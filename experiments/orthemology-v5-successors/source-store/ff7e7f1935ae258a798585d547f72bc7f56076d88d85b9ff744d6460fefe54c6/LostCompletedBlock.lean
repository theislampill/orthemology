import ResetComponent
open EffectiveRenewal PolicySynthesis
-- A checker that resets at length 1 and forgets the completed block would accept.
-- The real checker must reject the copied diagonal zero, even at a cut endpoint.
example : componentCheck (fun _ => true) [false] = true := by
  simp [componentCheck, allBelow, slice, lastCut, Nat.findGreatest, treeCheck,
    coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq, Nat.Partrec.Code.ofNatCode,
    Nat.Partrec.Code.evaln, List.range_succ]
