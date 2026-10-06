import SkeletonUnion
#check PolicySynthesis.synthesisCheck_primrec
#check PolicySynthesis.synthesis_prefix_closed
#check PolicySynthesis.synthesis_mathematical_path
#check PolicySynthesis.synthesis_computablePath_iff
open EffectiveRenewal PolicySynthesis
example (p : Nat) : synthesisCheck p [] = true := by rfl
example (p : Nat) : synthesisCheck p [false] = true := by rfl
example (p : Nat) : synthesisCheck p [true] = true := by rfl
example (p : Nat) : synthesisCheck p [false, false] = false := by
  simp [synthesisCheck, synthesisClause, allBelow, controlsClear, skeletonWord, slice,
    treeCheck, coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq,
    Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
example (p : Nat) : synthesisCheck p [false, true] = true := by
  simp [synthesisCheck, synthesisClause, allBelow, controlsClear, skeletonWord, slice,
    treeCheck, coordinateOK, diagonal, Nat.Partrec.Code.ofNatCode_eq,
    Nat.Partrec.Code.ofNatCode, Nat.Partrec.Code.evaln, List.range_succ]
example (p : Nat) : ¬ ∀ n, synthesisTree p (prefixWord (fun _ => false) n) := by
  intro h
  exact no_computable_path _ (Computable.const false) (neverExit_decodes_K h (fun _ => rfl))
#print axioms PolicySynthesis.synthesis_computablePath_iff
#print axioms PolicySynthesis.synthesisCheck_primrec
#eval (List.range 8).map (fun n => synthesisCheck 0 (prefixWord (fun _ => true) n))
#check PolicySynthesis.synthesis_root_exit_iff
