import ResetComponent
#check PolicySynthesis.componentCheck_primrec
#check PolicySynthesis.blockSnapshots_primrec
#check PolicySynthesis.blockSnapshots_committed
#check PolicySynthesis.blockSnapshots_admitted
#check PolicySynthesis.component_computablePath_iff
open EffectiveRenewal PolicySynthesis
example : componentCheck (fun _ => true) [false] = false := by
  simp [componentCheck, allBelow, slice, lastCut, Nat.findGreatest, treeCheck,
    coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq, Nat.Partrec.Code.ofNatCode,
    Nat.Partrec.Code.evaln, List.range_succ]
example : componentCheck (fun _ => true) [true, true, true] = true := by
  simp [componentCheck, allBelow, slice, lastCut, Nat.findGreatest, treeCheck,
    coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq, Nat.Partrec.Code.ofNatCode,
    Nat.Partrec.Code.evaln, List.range_succ]
example : blockSnapshots (fun _ => true) 3 = [true, true, true] := by
  simp [blockSnapshots, lastCut, Nat.findGreatest, finitePlan, diagonal,
    Nat.Partrec.Code.ofNatCode_eq, Nat.Partrec.Code.ofNatCode,
    Nat.Partrec.Code.evaln, List.range_succ]
example : blockSnapshots (fun i => decide (i = 0)) 5 = [] := by decide
example : HasComputablePath (componentTree (fun _ => true)) :=
  unboundedCuts_component_path _ (Primrec.const true) rfl
    (fun N => ⟨N+1, Nat.lt_succ_self N, rfl⟩)
example : ¬ HasComputablePath (componentTree (fun i => decide (i = 0))) := by
  apply eventuallyLastCut_no_component_path
  refine ⟨0, ?_⟩
  intro i hi
  apply lastCut_eq_of_bounds (by decide) hi
  intro c hc hci
  simp [Nat.ne_of_gt hc]
#print axioms PolicySynthesis.component_computablePath_iff
#print axioms PolicySynthesis.blockSnapshots_primrec
