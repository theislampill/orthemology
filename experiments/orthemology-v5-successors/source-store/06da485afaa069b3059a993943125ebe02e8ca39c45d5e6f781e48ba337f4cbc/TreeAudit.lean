import EffectiveTree
#print axioms EffectiveRenewal.treeCheck_primrec
#print axioms EffectiveRenewal.finitePlan_primrec
#print axioms EffectiveRenewal.finitePlan_admitted
#print axioms EffectiveRenewal.exists_mathematical_path
#print axioms EffectiveRenewal.no_computable_path
#eval (List.range 8).map EffectiveRenewal.finitePlan
#eval (List.range 8).map (fun n => EffectiveRenewal.treeCheck (EffectiveRenewal.finitePlan n))
example : EffectiveRenewal.treeCheck [false] = false := by
  simp [EffectiveRenewal.treeCheck, EffectiveRenewal.coordinateOK, EffectiveRenewal.diagonal,
    Nat.Partrec.Code.ofNatCode_eq, Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
example : EffectiveRenewal.treeCheck [true] = true := by
  simp [EffectiveRenewal.treeCheck, EffectiveRenewal.coordinateOK, EffectiveRenewal.diagonal,
    Nat.Partrec.Code.ofNatCode_eq, Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
