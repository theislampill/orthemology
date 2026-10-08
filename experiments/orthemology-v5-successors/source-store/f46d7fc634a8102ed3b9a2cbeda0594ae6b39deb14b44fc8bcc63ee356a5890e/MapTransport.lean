import FixedFamilies

namespace AttributionKernel
open Finset
variable {α β : Type*} [Fintype α] [DecidableEq α] [DecidableEq β]

/-- The equality fibers are exactly A and all singleton labels outside A. -/
def ExactOneClassMap (A : Finset α) (ρ : α → β) : Prop :=
  ∀ i j, ρ i = ρ j ↔ i = j ∨ (i ∈ A ∧ j ∈ A)

def renameRoot (ρ : α → β) (r : α) : Option α → β
  | none => ρ r
  | some i => ρ i

omit [Fintype α] [DecidableEq β] in
 theorem rename_commutes (A : Finset α) (ρ : α → β) (r : α)
    (hr : r ∈ A) (hρ : ExactOneClassMap A ρ) (i : α) :
    renameRoot ρ r (rootMap A i) = ρ i := by
  by_cases hi : i ∈ A
  · simpa [rootMap, hi, renameRoot] using (hρ r i).mpr (Or.inr ⟨hr, hi⟩)
  · simp [rootMap, hi, renameRoot]

omit [DecidableEq β] in
theorem rename_injOn (A : Finset α) (ρ : α → β) (r : α)
    (hr : r ∈ A) (hρ : ExactOneClassMap A ρ) :
    Set.InjOn (renameRoot ρ r) (actualRoots A) := by
  intro x hx y hy he
  cases x with
  | none =>
    cases y with
    | none => rfl
    | some j =>
      have hj := (some_mem_rootImage A univ j).mp hy
      rcases (hρ r j).mp he with heq | ha
      · exact False.elim (hj.2 (heq ▸ hr))
      · exact False.elim (hj.2 ha.2)
  | some i =>
    cases y with
    | none =>
      have hi := (some_mem_rootImage A univ i).mp hx
      rcases (hρ i r).mp he with heq | ha
      · exact False.elim (hi.2 (heq.symm ▸ hr))
      · exact False.elim (hi.2 ha.1)
    | some j =>
      have hi := (some_mem_rootImage A univ i).mp hx
      rcases (hρ i j).mp he with heq | ha
      · exact congrArg some heq
      · exact False.elim (hi.2 ha.1)

omit [Fintype α] in
 theorem renamed_image (A P : Finset α) (ρ : α → β) (r : α)
    (hr : r ∈ A) (hρ : ExactOneClassMap A ρ) :
    (rootImage A P).image (renameRoot ρ r) = P.image ρ := by
  simp only [rootImage, image_image, Function.comp_def, rename_commutes A ρ r hr hρ]

theorem arbitrary_map_shared_card (A P R : Finset α) (ρ : α → β)
    (hA : A.Nonempty) (hρ : ExactOneClassMap A ρ) :
    ((P.image ρ) ∩ (R.image ρ)).card = (sharedRoots A P R).card := by
  obtain ⟨r, hr⟩ := hA
  have hi := rename_injOn A ρ r hr hρ
  rw [← renamed_image A P ρ r hr hρ, ← renamed_image A R ρ r hr hρ,
    ← image_inter_of_injOn]
  · apply card_image_of_injOn
    exact hi.mono (fun _ hz => rootImage_mono A (subset_univ P) (mem_inter.mp hz).1)
  · apply hi.mono
    intro z hz
    rcases hz with hz | hz
    · exact rootImage_mono A (subset_univ P) hz
    · exact rootImage_mono A (subset_univ R) hz

/-- Arbitrary real-root faults can be pulled back along the bijection of actual images. -/
theorem arbitrary_faults_pullback (A : Finset α) (ρ : α → β)
    (hA : A.Nonempty) (hρ : ExactOneClassMap A ρ)
    (S : Finset β) (hS : S ⊆ univ.image ρ) :
    ∃ T : Finset (Option α), T ⊆ actualRoots A ∧ T.card = S.card ∧
      ∀ i, rootMap A i ∈ T ↔ ρ i ∈ S := by
  obtain ⟨r, hr⟩ := hA
  let T := (actualRoots A).filter (fun z => renameRoot ρ r z ∈ S)
  have hT : T ⊆ actualRoots A := filter_subset _ _
  have heq : T.image (renameRoot ρ r) = S := by
    apply Subset.antisymm
    · intro z hz
      obtain ⟨x, hx, rfl⟩ := mem_image.mp hz
      exact (mem_filter.mp hx).2
    · intro z hz
      obtain ⟨i, _hi, hzi⟩ := mem_image.mp (hS hz)
      refine mem_image.mpr ⟨rootMap A i, ?_, ?_⟩
      · apply mem_filter.mpr
        refine ⟨mem_image.mpr ⟨i, mem_univ i, rfl⟩, ?_⟩
        simpa [rename_commutes A ρ r hr hρ, hzi] using hz
      · simpa [rename_commutes A ρ r hr hρ] using hzi
  refine ⟨T, hT, ?_, ?_⟩
  · rw [← heq, card_image_of_injOn ((rename_injOn A ρ r hr hρ).mono hT)]
  · intro i
    simp only [T, mem_filter, rename_commutes A ρ r hr hρ]
    exact and_iff_right (mem_image.mpr ⟨i, mem_univ i, rfl⟩)

/-- Conversely every canonical fault set denotes an equally large real-root set. -/
theorem canonical_faults_pushforward (A : Finset α) (ρ : α → β)
    (hA : A.Nonempty) (hρ : ExactOneClassMap A ρ)
    (T : Finset (Option α)) (hT : T ⊆ actualRoots A) :
    ∃ S : Finset β, S ⊆ univ.image ρ ∧ S.card = T.card ∧
      ∀ i, ρ i ∈ S ↔ rootMap A i ∈ T := by
  obtain ⟨r, hr⟩ := hA
  have hi := rename_injOn A ρ r hr hρ
  refine ⟨T.image (renameRoot ρ r), ?_, card_image_of_injOn (hi.mono hT), ?_⟩
  · rw [← renamed_image A univ ρ r hr hρ]
    exact image_subset_image hT
  · intro i
    rw [← rename_commutes A ρ r hr hρ i]
    constructor
    · intro h
      obtain ⟨z, hz, he⟩ := mem_image.mp h
      have hzEq := hi (hT hz) (mem_image.mpr ⟨i, mem_univ i, rfl⟩) he
      exact hzEq ▸ hz
    · intro h
      exact mem_image.mpr ⟨rootMap A i, h, rfl⟩

omit [Fintype α] [DecidableEq β] in
 theorem canonical_exact (A : Finset α) : ExactOneClassMap A (rootMap A) := by
  intro i j
  by_cases hi : i ∈ A <;> by_cases hj : j ∈ A <;>
    simp_all [rootMap] <;> aesop

def MapAvailable (B : ℕ) (ρ : α → β) (F : Set (Finset α)) : Prop :=
  ∀ S : Finset β, S ⊆ univ.image ρ → S.card ≤ B →
    ∃ P ∈ F, Disjoint (P.image ρ) S

omit [Fintype α] in
 theorem matching_fault_disjointness (A P : Finset α) (ρ : α → β)
    (S : Finset β) (T : Finset (Option α))
    (he : ∀ i, ρ i ∈ S ↔ rootMap A i ∈ T) :
    Disjoint (P.image ρ) S ↔ Disjoint (rootImage A P) T := by
  constructor
  · intro hd
    apply disjoint_left.mpr
    intro z hz ht
    obtain ⟨i, hi, rfl⟩ := mem_image.mp hz
    exact disjoint_left.mp hd (mem_image.mpr ⟨i, hi, rfl⟩) ((he i).mpr ht)
  · intro hd
    apply disjoint_left.mpr
    intro z hz hs
    obtain ⟨i, hi, rfl⟩ := mem_image.mp hz
    exact disjoint_left.mp hd (mem_image.mpr ⟨i, hi, rfl⟩) ((he i).mp hs)

theorem arbitrary_map_available_iff (B : ℕ) (A : Finset α) (ρ : α → β)
    (hA : A.Nonempty) (hρ : ExactOneClassMap A ρ) (F : Set (Finset α)) :
    MapAvailable B ρ F ↔ MapAvailable B (rootMap A) F := by
  constructor
  · intro hav T hT hTB
    obtain ⟨S, hS, hST, he⟩ := canonical_faults_pushforward A ρ hA hρ T hT
    obtain ⟨P, hPF, hd⟩ := hav S hS (by omega)
    exact ⟨P, hPF, (matching_fault_disjointness A P ρ S T he).mp hd⟩
  · intro hav S hS hSB
    obtain ⟨T, hT, hTS, he⟩ := arbitrary_faults_pullback A ρ hA hρ S hS
    obtain ⟨P, hPF, hd⟩ := hav T hT (by omega)
    exact ⟨P, hPF, (matching_fault_disjointness A P ρ S T (fun i => (he i).symm)).mpr hd⟩

#print axioms canonical_exact
#print axioms arbitrary_map_available_iff
#print axioms arbitrary_map_shared_card
#print axioms arbitrary_faults_pullback
#print axioms canonical_faults_pushforward

end AttributionKernel
