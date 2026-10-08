import PolicySynthesisReduction
#check PolicySynthesis.computable_matrix_reduction
#check PolicySynthesis.total_checker_code_family
#check PolicySynthesis.policy_synthesis_reduction
open EffectiveRenewal PolicySynthesis Nat.Partrec Encodable Denumerable
example (a x y : Nat) : ¬ (matrixSearch (fun _ => false) (Nat.pair a (Nat.pair x y))).Dom := by
  simp [matrixSearch_dom_pair]
example (a x y : Nat) : (matrixSearch (fun _ => true) (Nat.pair a (Nat.pair x y))).Dom := by
  simp [matrixSearch_dom_pair]
example (a n : Nat) : Code.eval (ofNat Code (specializeIndex Code.zero a)) n = Part.some 0 := by
  rw [specializeIndex_eval]
  rfl
example : ∃ r : Nat → Nat, Primrec r ∧ ∀ a, ¬ HasComputablePath (synthesisTree (r a)) := by
  obtain ⟨r,hr,he⟩ := computable_matrix_reduction (fun _ => false) (Computable.const false)
  refine ⟨r,hr,?_⟩
  intro a h
  simpa using (he a).mpr h
example : ∃ r : Nat → Nat, Primrec r ∧ ∀ a, HasComputablePath (synthesisTree (r a)) := by
  obtain ⟨r,hr,he⟩ := computable_matrix_reduction (fun _ => true) (Computable.const true)
  exact ⟨r,hr,fun a => (he a).mp ⟨0,fun _ => ⟨0,rfl⟩⟩⟩
example (p : Nat) (w : Word) : natChecker p (encode w) = bitNat (synthesisCheck p w) :=
  natChecker_encode p w
#print axioms PolicySynthesis.policy_synthesis_reduction
#print axioms PolicySynthesis.source_search_code
#print axioms PolicySynthesis.total_checker_code_family
-- Even malformed word encodings are handled by a total declared convention.
example (p n : Nat) (hn : decode (α := Word) n = Option.none) : natChecker p n = 1 := by
  simp only [natChecker, hn, Option.getD_none]
  rfl
#check PolicySynthesis.source_search_code_equations
