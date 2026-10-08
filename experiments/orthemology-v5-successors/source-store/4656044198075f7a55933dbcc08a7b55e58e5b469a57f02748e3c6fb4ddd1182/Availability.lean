import RootImage

namespace AttributionKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

def actualRoots (A : Finset α) : Finset (Option α) := rootImage A univ

def taintedLabels (A : Finset α) (S : Finset (Option α)) : Finset α :=
  univ.filter (fun i => rootMap A i ∈ S)

def Available (B c : ℕ) (F : Set (Finset α)) : Prop :=
  ∀ A : Finset α, A.card = c →
    ∀ S : Finset (Option α), S ⊆ actualRoots A → S.card ≤ B →
      ∃ P ∈ F, Disjoint (rootImage A P) S

def LabelAvailable (k : ℕ) (F : Set (Finset α)) : Prop :=
  ∀ T : Finset α, T.card = k → ∃ P ∈ F, Disjoint P T

theorem disjoint_image_iff (A P : Finset α) (S : Finset (Option α)) :
    Disjoint (rootImage A P) S ↔ Disjoint P (taintedLabels A S) := by
  simp only [Finset.disjoint_left, rootImage, mem_image, taintedLabels,
    mem_filter, mem_univ, true_and]
  constructor
  · intro h i hi hs
    exact h ⟨i, hi, rfl⟩ hs
  · intro h z hz hs
    rcases hz with ⟨i, hi, rfl⟩
    exact h hi hs

omit [Fintype α] in
theorem rootImage_mono (A : Finset α) {P R : Finset α} (h : P ⊆ R) :
    rootImage A P ⊆ rootImage A R := image_subset_image h

theorem tainted_rootImage_subset (A : Finset α) (S : Finset (Option α)) :
    rootImage A (taintedLabels A S) ⊆ S := by
  intro z hz
  obtain ⟨i, hi, rfl⟩ := mem_image.mp hz
  simpa [taintedLabels] using hi

theorem tainted_label_budget (A : Finset α) (S : Finset (Option α))
    (hc : 1 ≤ A.card) :
    (taintedLabels A S).card ≤ S.card + A.card - 1 := by
  have h := overlap_le_shared_add_class_pred A (taintedLabels A S)
    (taintedLabels A S) hc
  simp only [inter_self, sharedRoots] at h
  have hsub := card_le_card (tainted_rootImage_subset A S)
  omega

omit [Fintype α] in
theorem rootImage_card_of_class_subset (A T : Finset α) (hAT : A ⊆ T)
    (hc : 1 ≤ A.card) :
    (rootImage A T).card = T.card - A.card + 1 := by
  have hb : bridge A T T := by
    obtain ⟨i, hi⟩ := card_pos.mp (show 0 < A.card by omega)
    exact ⟨⟨i, mem_inter.mpr ⟨hi, hAT hi⟩⟩, ⟨i, mem_inter.mpr ⟨hi, hAT hi⟩⟩⟩
  have h := sharedRoots_card A T T
  simpa [sharedRoots, hb, card_sdiff hAT] using h

theorem tainted_realization (A T : Finset α) (hAT : A ⊆ T) :
    taintedLabels A (rootImage A T) = T := by
  ext i
  simp only [taintedLabels, mem_filter, mem_univ, true_and]
  by_cases hiA : i ∈ A
  · have hiT := hAT hiA
    simp [rootMap, hiA, none_mem_rootImage, hiT]
    exact ⟨i, mem_inter.mpr ⟨hiA, hiT⟩⟩
  · simp [rootMap, hiA, some_mem_rootImage]

theorem maximal_taint_realizable (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (T : Finset α) (hT : T.card = B+c-1) :
    ∃ A : Finset α, A.card = c ∧
      ∃ S : Finset (Option α), S ⊆ actualRoots A ∧ S.card = B ∧
        taintedLabels A S = T := by
  obtain ⟨A, hAT, hAc⟩ := exists_subset_card_eq (show c ≤ T.card by omega)
  refine ⟨A, hAc, rootImage A T, rootImage_mono A (subset_univ T), ?_,
    tainted_realization A T hAT⟩
  rw [rootImage_card_of_class_subset A T hAT (by omega), hAc, hT]
  omega

theorem available_iff (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (_hcm : c ≤ Fintype.card α) (hk : B+c-1 ≤ Fintype.card α)
    (F : Set (Finset α)) :
    Available B c F ↔ LabelAvailable (B+c-1) F := by
  constructor
  · intro hav T hT
    obtain ⟨A, hAc, S, hSroots, hSB, hST⟩ := maximal_taint_realizable B c hB hc T hT
    obtain ⟨P, hPF, hdis⟩ := hav A hAc S hSroots (by omega)
    refine ⟨P, hPF, ?_⟩
    rw [disjoint_image_iff, hST] at hdis
    exact hdis
  · intro hav A hAc S _hSroots hSB
    have hbudget := tainted_label_budget A S (by omega)
    obtain ⟨T, hsub, _hTU, hT⟩ := exists_subsuperset_card_eq
      (subset_univ (taintedLabels A S))
      (show (taintedLabels A S).card ≤ B+c-1 by omega)
      (by simpa using hk : B+c-1 ≤ (univ : Finset α).card)
    obtain ⟨P, hPF, hdis⟩ := hav T hT
    exact ⟨P, hPF, (disjoint_image_iff A P S).mpr (hdis.mono_right hsub)⟩

theorem actual_root_count (A : Finset α) (hc : 1 ≤ A.card) :
    (actualRoots A).card = Fintype.card α - A.card + 1 := by
  simpa [actualRoots] using rootImage_card_of_class_subset A univ (subset_univ A) hc

#print axioms tainted_label_budget
#print axioms maximal_taint_realizable
#print axioms available_iff
#print axioms actual_root_count

end AttributionKernel
