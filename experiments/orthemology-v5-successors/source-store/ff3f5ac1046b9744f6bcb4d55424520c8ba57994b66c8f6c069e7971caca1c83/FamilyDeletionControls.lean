import FixedFamilies

namespace AttributionKernel.Tests
open Finset

private def pairFamily : Set (Finset (Fin 3)) := thresholdFamily 2
private def wholeFamily : Set (Finset (Fin 3)) := {univ}

private theorem pair_available : LabelAvailable 1 pairFamily := by
  intro T hT
  refine ⟨univ \ T, ?_, sdiff_disjoint⟩
  change (univ \ T).card = 2
  rw [card_sdiff (subset_univ T), card_univ, Fintype.card_fin, hT]

/-- One available family alone cannot support the lower bound. -/
theorem second_availability_is_essential :
    LabelAvailable 1 pairFamily ∧
    (∀ P ∈ pairFamily, ∀ R ∈ wholeFamily, 1 < (P ∩ R).card) ∧
    ¬(3*1+1 ≤ Fintype.card (Fin 3)) := by
  refine ⟨pair_available, ?_, by decide⟩
  intro P hP R hR
  have hRu : R = univ := hR
  subst R
  have hPc : P.card = 2 := hP
  simpa using (show 1 < P.card by omega)

/-- Safety for only the diagonal P=R cannot support the cross-family bound. -/
theorem cross_pair_safety_is_essential :
    LabelAvailable 1 pairFamily ∧
    (∀ P ∈ pairFamily, 1 < (P ∩ P).card) ∧
    (∃ P ∈ pairFamily, ∃ R ∈ pairFamily, (P ∩ R).card = 1) ∧
    ¬(3*1+1 ≤ Fintype.card (Fin 3)) := by
  refine ⟨pair_available, ?_, ?_, by decide⟩
  · intro P hP
    have hPc : P.card = 2 := hP
    simpa using (show 1 < P.card by omega)
  · refine ⟨{0, 1}, ?_, {1, 2}, ?_, ?_⟩
    · change ({0, 1} : Finset (Fin 3)).card = 2
      decide
    · change ({1, 2} : Finset (Fin 3)).card = 2
      decide
    · decide

end AttributionKernel.Tests
