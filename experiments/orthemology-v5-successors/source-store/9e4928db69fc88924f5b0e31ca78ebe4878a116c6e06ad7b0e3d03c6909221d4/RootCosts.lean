import FixedFamilies

namespace AttributionKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Root-level untainted overlap only; physical gate behavior remains a premise. -/
def RootWitnessSafe (B : ℕ) (A P R : Finset α) : Prop :=
  ∀ S : Finset (Option α), S ⊆ actualRoots A → S.card ≤ B →
    ∃ z ∈ sharedRoots A P R, z ∉ S

theorem root_witness_safe_iff (B : ℕ) (A P R : Finset α) :
    RootWitnessSafe B A P R ↔ B < (sharedRoots A P R).card := by
  have hactual : sharedRoots A P R ⊆ actualRoots A :=
    (inter_subset_left).trans (rootImage_mono A (subset_univ P))
  constructor
  · intro h
    by_contra hn
    obtain ⟨z, hz, hnz⟩ := h (sharedRoots A P R) hactual (by omega)
    exact hnz hz
  · intro h S _hS hB
    by_contra hn
    push_neg at hn
    have hs : sharedRoots A P R ⊆ S := hn
    have hc := card_le_card hs
    omega

theorem universal_root_witness_iff (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (P R : Finset α) :
    (∀ A : Finset α, A.card = c → RootWitnessSafe B A P R) ↔
      B+c ≤ (P ∩ R).card := by
  simp only [root_witness_safe_iff]
  exact robust_iff B c hB hc hcm P R

theorem arbitrary_family_actual_root_lower (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hBn : B < Fintype.card α-c+1)
    (F G : Set (Finset α)) (h : FixedFamilyContract B c F G)
    (A : Finset α) (hAc : A.card = c) :
    3*B+2*c-1 ≤ (actualRoots A).card := by
  have hm := (fixed_family_feasible_iff B c hB hc hcm hBn).mp ⟨F, G, h⟩
  rw [actual_root_count A (by omega), hAc]
  omega

theorem sharp_minimum_construction (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c) :
    (∃ F G : Set (Finset (Fin (3*(B+c-1)+1))), FixedFamilyContract B c F G) ∧
    (∀ A : Finset (Fin (3*(B+c-1)+1)), A.card = c →
      (actualRoots A).card = 3*B+2*c-1) ∧
    (3*B+2*c-1)-(3*B+1) = 2*(c-1) := by
  constructor
  · apply (fixed_family_feasible_iff B c hB hc (by simp; omega) (by simp; omega)).mpr
    simp
  · constructor
    · intro A hAc
      rw [actual_root_count A (by omega), hAc, Fintype.card_fin]
      omega
    · omega

#print axioms root_witness_safe_iff
#print axioms universal_root_witness_iff
#print axioms arbitrary_family_actual_root_lower
#print axioms sharp_minimum_construction

end AttributionKernel
