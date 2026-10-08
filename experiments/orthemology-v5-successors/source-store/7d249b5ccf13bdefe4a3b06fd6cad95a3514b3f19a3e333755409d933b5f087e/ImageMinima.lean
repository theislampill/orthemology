import Availability

namespace AttributionKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

omit [Fintype α] in
theorem shared_nonempty_of_overlap (A P R : Finset α) (h : (P ∩ R).Nonempty) :
    (sharedRoots A P R).Nonempty := by
  obtain ⟨i, hi⟩ := h
  obtain ⟨hiP, hiR⟩ := mem_inter.mp hi
  exact ⟨rootMap A i, mem_inter.mpr
    ⟨mem_image.mpr ⟨i, hiP, rfl⟩, mem_image.mpr ⟨i, hiR, rfl⟩⟩⟩

theorem sharp_nonempty_minimum (c : ℕ) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (P R : Finset α) (hI : (P ∩ R).Nonempty) :
    (∀ A : Finset α, A.card = c →
      (P ∩ R).card-c+1 ≤ (sharedRoots A P R).card) ∧
    (∃ A : Finset α, A.card = c ∧
      (sharedRoots A P R).card = (P ∩ R).card-c+1) := by
  constructor
  · intro A hAc
    have hpos := card_pos.mpr (shared_nonempty_of_overlap A P R hI)
    have hcount := overlap_le_shared_add_class_pred A P R (by omega)
    omega
  · by_cases hci : c ≤ (P ∩ R).card
    · obtain ⟨A, hAI, hAc⟩ := exists_subset_card_eq hci
      obtain ⟨i, hiA⟩ := card_pos.mp (show 0 < A.card by omega)
      have hi := mem_inter.mp (hAI hiA)
      have hb : bridge A P R :=
        ⟨⟨i, mem_inter.mpr ⟨hiA, hi.1⟩⟩, ⟨i, mem_inter.mpr ⟨hiA, hi.2⟩⟩⟩
      refine ⟨A, hAc, ?_⟩
      rw [sharedRoots_card, card_sdiff hAI, hAc, if_pos hb]
    · obtain ⟨A, hIA, _hAU, hAc⟩ := exists_subsuperset_card_eq
        (subset_univ (P ∩ R)) (by omega : (P ∩ R).card ≤ c)
        (by simpa using hcm : c ≤ (univ : Finset α).card)
      obtain ⟨i, hiI⟩ := hI
      have hi := mem_inter.mp hiI
      have hiA := hIA hiI
      have hb : bridge A P R :=
        ⟨⟨i, mem_inter.mpr ⟨hiA, hi.1⟩⟩, ⟨i, mem_inter.mpr ⟨hiA, hi.2⟩⟩⟩
      refine ⟨A, hAc, ?_⟩
      rw [sharedRoots_card, sdiff_eq_empty_iff_subset.mpr hIA, card_empty, if_pos hb]
      omega

theorem meets_if_card_sum_large (A P : Finset α)
    (h : Fintype.card α < A.card + P.card) : (A ∩ P).Nonempty := by
  by_contra hn
  have hd : Disjoint A P := disjoint_iff_inter_eq_empty.mpr (not_nonempty_iff_eq_empty.mp hn)
  have hm := card_le_univ (s := A ∪ P)
  rw [card_union_of_disjoint hd] at hm
  omega

theorem forced_bridge_iff (c : ℕ) (_hcm : c ≤ Fintype.card α) (P R : Finset α) :
    (∀ A : Finset α, A.card = c → bridge A P R) ↔
      Fintype.card α < c + min P.card R.card := by
  constructor
  · intro h
    have hP : Fintype.card α < c+P.card := by
      by_contra hn
      have hb : c ≤ (univ \ P).card := by
        rw [card_sdiff (subset_univ P), card_univ]
        omega
      obtain ⟨A, hA, hAc⟩ := exists_subset_card_eq hb
      obtain ⟨i, hi⟩ := (h A hAc).1
      obtain ⟨hiA, hiP⟩ := mem_inter.mp hi
      exact (mem_sdiff.mp (hA hiA)).2 hiP
    have hR : Fintype.card α < c+R.card := by
      by_contra hn
      have hb : c ≤ (univ \ R).card := by
        rw [card_sdiff (subset_univ R), card_univ]
        omega
      obtain ⟨A, hA, hAc⟩ := exists_subset_card_eq hb
      obtain ⟨i, hi⟩ := (h A hAc).2
      obtain ⟨hiA, hiR⟩ := mem_inter.mp hi
      exact (mem_sdiff.mp (hA hiA)).2 hiR
    omega
  · intro h A hAc
    exact ⟨meets_if_card_sum_large A P (by omega), meets_if_card_sum_large A R (by omega)⟩

theorem disjoint_zero_fault_iff (c : ℕ) (hcm : c ≤ Fintype.card α)
    (P R : Finset α) (hdis : Disjoint P R) :
    Robust 0 c P R ↔ Fintype.card α < c + min P.card R.card := by
  rw [← forced_bridge_iff c hcm P R]
  have hi : P ∩ R = ∅ := disjoint_iff_inter_eq_empty.mp hdis
  simp only [Robust, sharedRoots_card, hi, empty_sdiff, card_empty, zero_add]
  constructor <;> intro h A hA
  · have hb := h A hA
    by_cases hh : bridge A P R <;> simp_all
  · simp [h A hA]

#print axioms sharp_nonempty_minimum
#print axioms forced_bridge_iff
#print axioms disjoint_zero_fault_iff

end AttributionKernel
