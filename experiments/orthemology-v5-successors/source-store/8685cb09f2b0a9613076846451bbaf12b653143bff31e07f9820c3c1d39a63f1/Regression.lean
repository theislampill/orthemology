import FixedFamilies
import ImageMinima
import Correspondence
import MapTransport

namespace AttributionKernel.Tests
open Finset

/-- The accepted one-pair threshold: seven labels, six actual roots. -/
example : ∃ F G : Set (Finset (Fin 7)), FixedFamilyContract 1 2 F G := by
  apply (fixed_family_feasible_iff 1 2 (by decide) (by decide) (by decide) (by decide)).mpr
  decide

example : ¬∃ F G : Set (Finset (Fin 6)), FixedFamilyContract 1 2 F G := by
  rw [fixed_family_feasible_iff 1 2 (by decide) (by decide) (by decide) (by decide)]
  decide

/-- A larger parameter than the accepted exhaustive m≤7 root-image checks. -/
example : ∃ F G : Set (Finset (Fin 10)), FixedFamilyContract 1 3 F G := by
  apply (fixed_family_feasible_iff 1 3 (by decide) (by decide) (by decide) (by decide)).mpr
  decide

example : ¬∃ F G : Set (Finset (Fin 9)), FixedFamilyContract 1 3 F G := by
  rw [fixed_family_feasible_iff 1 3 (by decide) (by decide) (by decide) (by decide)]
  decide

example : (actualRoots ({0, 1} : Finset (Fin 7))).card = 6 := by
  rw [actual_root_count _ (by decide)]
  decide

/-- Two alias labels are one root, not two votes. -/
example : (rootImage ({0, 1} : Finset (Fin 7)) {0, 1}).card = 1 := by decide

/-- Empty label intersection can still bridge one real root. -/
example : (sharedRoots ({0, 2} : Finset (Fin 4)) {0, 1} {2, 3}).card = 1 := by decide

/-- Removing B≥1 from the iff is genuinely false. -/
theorem zero_fault_counterexample :
    Robust 0 3 ({0, 1} : Finset (Fin 4)) {2, 3} ∧
      ¬(0+3 ≤ (({0, 1} : Finset (Fin 4)) ∩ {2, 3}).card) := by
  constructor
  · rw [disjoint_zero_fault_iff 3 (by decide) _ _ (by decide)]
    decide
  · decide

/-- Removing c≥1 permits a zero-class predicate that is not the admitted model. -/
theorem zero_class_counterexample :
    1+0 ≤ (({0} : Finset (Fin 2)) ∩ {0}).card ∧
      ¬Robust 1 0 ({0} : Finset (Fin 2)) {0} := by
  constructor
  · decide
  · intro h
    have he := h ∅ rfl
    norm_num [sharedRoots, rootImage, rootMap] at he

/-- Without c≤m, the universal map predicate can be vacuous. -/
theorem impossible_class_counterexample :
    Robust 1 3 (∅ : Finset (Fin 2)) ∅ ∧
      ¬(1+3 ≤ ((∅ : Finset (Fin 2)) ∩ ∅).card) := by
  constructor
  · intro A hA
    have hcard := card_le_univ (s := A)
    norm_num at hcard
    omega
  · decide

/-- Maximal-taint realization is not a label-independence hypothesis. -/
example (T : Finset (Fin 10)) (hT : T.card = 3) :
    ∃ A : Finset (Fin 10), A.card = 3 ∧
      ∃ S : Finset (Option (Fin 10)), S ⊆ actualRoots A ∧ S.card = 1 ∧
        taintedLabels A S = T := by
  exact maximal_taint_realizable 1 3 (by decide) (by decide) T hT

/-- Arbitrary root renamings preserve all pair cardinalities. -/
example (A P R : Finset (Fin 8)) (ρ : Fin 8 → ℕ)
    (hA : A.Nonempty) (hρ : ExactOneClassMap A ρ) :
    ((P.image ρ) ∩ (R.image ρ)).card = (sharedRoots A P R).card :=
  arbitrary_map_shared_card A P R ρ hA hρ

end AttributionKernel.Tests
