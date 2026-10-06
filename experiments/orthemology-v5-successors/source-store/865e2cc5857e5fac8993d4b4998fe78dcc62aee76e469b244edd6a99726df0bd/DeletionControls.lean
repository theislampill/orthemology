import MapTransport
import ImageMinima
namespace AttributionKernel.IndependentReview
open Finset

/-- Reject B=0: forced bridging really can rescue the empty label overlap. -/
theorem delete_B_positive :
    Robust 0 3 ({0,1} : Finset (Fin 4)) {2,3} ∧
    ¬ (3 ≤ (({0,1} : Finset (Fin 4)) ∩ {2,3}).card) := by
  constructor
  · rw [disjoint_zero_fault_iff 3 (by decide) _ _ (by decide)]
    decide
  · decide

/-- Reject c=0: the canonical map is then injective and the -1 budget is wrong. -/
theorem delete_c_positive :
    1 ≤ (({0} : Finset (Fin 2)) ∩ {0}).card ∧
    ¬ Robust 1 0 ({0} : Finset (Fin 2)) {0} := by
  constructor
  · decide
  · intro h
    have he := h ∅ rfl
    norm_num [sharedRoots, rootImage, rootMap] at he

/-- Reject c>m: no compatible class means universal robustness is vacuous. -/
theorem delete_class_validity :
    Robust 1 3 (∅ : Finset (Fin 2)) ∅ ∧
    ¬ (4 ≤ ((∅ : Finset (Fin 2)) ∩ ∅).card) := by
  constructor
  · intro A hA
    have hm := card_le_univ (s := A)
    simp only [Fintype.card_fin] at hm
    omega
  · decide

/-- If k>m, label availability is vacuous, so the lower bound requires k≤m. -/
theorem delete_k_validity :
    LabelFamilyContract 3 (∅ : Set (Finset (Fin 2))) ∅ ∧ ¬ 3*3+1 ≤ 2 := by
  have hav : LabelAvailable 3 (∅ : Set (Finset (Fin 2))) := by
    intro T hT
    have hm := card_le_univ (s := T)
    simp only [Fintype.card_fin] at hm
    omega
  refine ⟨⟨hav, hav, ?_⟩, by decide⟩
  intro P hP
  exact False.elim hP

/-- Either availability conjunct is needed: an empty other family trivializes safety. -/
theorem delete_one_availability :
    ∃ F G : Set (Finset (Fin 2)), LabelAvailable 1 F ∧
      (∀ P ∈ F, ∀ R ∈ G, 1 < (P ∩ R).card) ∧ ¬ 3*1+1 ≤ 2 := by
  refine ⟨{∅}, ∅, ?_, ?_, by decide⟩
  · intro T _
    exact ⟨∅, rfl, by simp⟩
  · intro P _ R hR
    exact False.elim hR

/-- Both available empty-path families fail only the essential safety conjunct. -/
theorem delete_pair_safety :
    ∃ F G : Set (Finset (Fin 2)), LabelAvailable 1 F ∧ LabelAvailable 1 G ∧ ¬ 3*1+1 ≤ 2 := by
  have hav : LabelAvailable 1 ({∅} : Set (Finset (Fin 2))) := by
    intro T _
    exact ⟨∅, rfl, by simp⟩
  exact ⟨{∅}, {∅}, hav, hav, by decide⟩

/-- The image restriction is necessary for cardinality-preserving fault transport. -/
theorem delete_actual_image_restriction :
    ∃ A : Finset (Fin 1), ∃ ρ : Fin 1 → Bool,
      A.Nonempty ∧ ExactOneClassMap A ρ ∧
      ∃ S : Finset Bool, ¬ S ⊆ (univ : Finset (Fin 1)).image ρ ∧
        ¬∃ T : Finset (Option (Fin 1)), T ⊆ actualRoots A ∧ T.card = S.card ∧
          ∀ i, rootMap A i ∈ T ↔ ρ i ∈ S := by
  refine ⟨{0}, fun _ => false, by decide, ?_, {true}, by decide, ?_⟩
  · intro i j
    have hij : i = j := Subsingleton.elim _ _
    simp [hij]
  · intro ⟨T, hT, hcard, he⟩
    have hne : T.Nonempty := card_pos.mp (by rw [hcard]; decide)
    obtain ⟨z, hz⟩ := hne
    have hzRoots := hT hz
    have hzNone : z = none := by simpa [actualRoots, rootImage, rootMap] using hzRoots
    subst z
    have hh := (he 0).mp hz
    simp at hh

#print axioms delete_B_positive
#print axioms delete_c_positive
#print axioms delete_class_validity
#print axioms delete_k_validity
#print axioms delete_one_availability
#print axioms delete_pair_safety
#print axioms delete_actual_image_restriction
end AttributionKernel.IndependentReview
