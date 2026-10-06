import Mathlib

namespace AttributionKernel
open Finset
variable {α : Type*} [DecidableEq α]

def rootMap (A : Finset α) (i : α) : Option α :=
  if i ∈ A then none else some i

def rootImage (A P : Finset α) : Finset (Option α) := P.image (rootMap A)

def sharedRoots (A P R : Finset α) : Finset (Option α) :=
  rootImage A P ∩ rootImage A R

def Robust (B c : ℕ) (P R : Finset α) : Prop :=
  ∀ A : Finset α, A.card = c → B < (sharedRoots A P R).card

theorem none_mem_rootImage (A P : Finset α) :
    none ∈ rootImage A P ↔ (A ∩ P).Nonempty := by
  simp only [rootImage, mem_image, mem_inter, Finset.Nonempty]
  constructor
  · rintro ⟨i, hi, h⟩
    refine ⟨i, ?_, hi⟩
    by_contra hn
    simp [rootMap, hn] at h
  · rintro ⟨i, hiA, hiP⟩
    exact ⟨i, hiP, by simp [rootMap, hiA]⟩

theorem some_mem_rootImage (A P : Finset α) (i : α) :
    some i ∈ rootImage A P ↔ i ∈ P ∧ i ∉ A := by
  simp only [rootImage, mem_image]
  constructor
  · rintro ⟨j, hj, h⟩
    by_cases ha : j ∈ A
    · simp [rootMap, ha] at h
    · have heq : j = i := by simpa [rootMap, ha] using h
      subst j
      exact ⟨hj, ha⟩
  · rintro ⟨hi, hn⟩
    exact ⟨i, hi, by simp [rootMap, hn]⟩

def bridge (A P R : Finset α) : Prop :=
  (A ∩ P).Nonempty ∧ (A ∩ R).Nonempty

instance (A P R : Finset α) : Decidable (bridge A P R) := inferInstanceAs
  (Decidable ((A ∩ P).Nonempty ∧ (A ∩ R).Nonempty))

theorem sharedRoots_decomposition (A P R : Finset α) :
    sharedRoots A P R = ((P ∩ R) \ A).image some ∪
      (if bridge A P R then {none} else ∅) := by
  ext z
  cases z with
  | none =>
    simp only [sharedRoots, mem_inter, none_mem_rootImage, mem_union,
      mem_image, Option.some_ne_none, and_false, exists_false, false_or]
    change bridge A P R ↔ none ∈ if bridge A P R then {none} else ∅
    by_cases h : bridge A P R <;> simp [h]
  | some i =>
    simp only [sharedRoots, mem_inter, some_mem_rootImage, mem_union, mem_image,
      mem_sdiff, Option.some.injEq, exists_eq_right]
    by_cases h : bridge A P R <;> simp [h] <;> tauto

theorem sharedRoots_card (A P R : Finset α) :
    (sharedRoots A P R).card = ((P ∩ R) \ A).card +
      (if bridge A P R then 1 else 0) := by
  rw [sharedRoots_decomposition, card_union_of_disjoint]
  · rw [card_image_of_injective _ (Option.some_injective α)]
    split_ifs <;> simp
  · apply disjoint_left.mpr
    intro z hz ht
    rcases mem_image.mp hz with ⟨i, hi, rfl⟩
    by_cases h : bridge A P R <;> simp [h] at ht

theorem cross_image_identity (A P R : Finset α) :
    (sharedRoots A P R).card = (P ∩ R).card - (A ∩ (P ∩ R)).card +
      (if bridge A P R then 1 else 0) := by
  rw [sharedRoots_card]
  congr 1
  have h := card_sdiff_add_card_inter (P ∩ R) A
  rw [inter_comm A] 
  omega

theorem overlap_le_shared_add_class_pred (A P R : Finset α)
    (hc : 1 ≤ A.card) :
    (P ∩ R).card ≤ (sharedRoots A P R).card + A.card - 1 := by
  have hpart := card_sdiff_add_card_inter (P ∩ R) A
  have hsub : ((P ∩ R) ∩ A).card ≤ A.card := card_le_card inter_subset_right
  rw [sharedRoots_card]
  by_cases hb : bridge A P R
  · simp only [hb, ↓reduceIte]
    omega
  · have he : (P ∩ R) ∩ A = ∅ := by
      apply eq_empty_iff_forall_not_mem.mpr
      intro i hi
      simp only [mem_inter] at hi
      exact hb ⟨⟨i, by simp [hi.2, hi.1.1]⟩, ⟨i, by simp [hi.2, hi.1.2]⟩⟩
    simp only [he, card_empty, add_zero] at hpart
    simp only [hb, ↓reduceIte]
    omega

theorem robust_iff [Fintype α] (B c : ℕ) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (P R : Finset α) :
    Robust B c P R ↔ B+c ≤ (P ∩ R).card := by
  constructor
  · intro hrob
    by_contra hsmall
    by_cases hci : c ≤ (P ∩ R).card
    · obtain ⟨A, hAI, hAc⟩ := exists_subset_card_eq hci
      have hnon : A.Nonempty := card_pos.mp (by omega)
      obtain ⟨i, hi⟩ := hnon
      have hiI := hAI hi
      have hb : bridge A P R :=
        ⟨⟨i, by simp_all⟩, ⟨i, by simp_all⟩⟩
      have hcard := sharedRoots_card A P R
      rw [card_sdiff hAI, hAc, if_pos hb] at hcard
      have hsafe := hrob A hAc
      omega
    · obtain ⟨A, hIA, _hAU, hAc⟩ := exists_subsuperset_card_eq
        (subset_univ (P ∩ R)) (by omega : (P ∩ R).card ≤ c)
        (by simpa using hcm : c ≤ (univ : Finset α).card)
      have he : (P ∩ R) \ A = ∅ := sdiff_eq_empty_iff_subset.mpr hIA
      have hcard := sharedRoots_card A P R
      rw [he, card_empty] at hcard
      have hsafe := hrob A hAc
      split_ifs at hcard <;> omega
  · intro hlarge A hAc
    have h := overlap_le_shared_add_class_pred A P R (by omega)
    omega

#print axioms cross_image_identity
#print axioms robust_iff

end AttributionKernel
