import MapTransport
import Correspondence
import ImageMinima

namespace AttributionKernel.IndependentReview
open Finset
variable {α β : Type*} [Fintype α] [DecidableEq α] [DecidableEq β]

/-- The transport is an actual bijection between actual images, not all root names. -/
theorem rename_bijective (A : Finset α) (ρ : α → β) (r : α)
    (hr : r ∈ A) (hρ : ExactOneClassMap A ρ) :
    ∃ f : {z // z ∈ actualRoots A} → {z // z ∈ (univ : Finset α).image ρ},
      Function.Bijective f ∧ ∀ z, (f z).val = renameRoot ρ r z.val := by
  have maps : ∀ z ∈ actualRoots A, renameRoot ρ r z ∈ (univ : Finset α).image ρ := by
    intro z hz
    rw [← renamed_image A univ ρ r hr hρ]
    exact mem_image.mpr ⟨z, hz, rfl⟩
  let f : {z // z ∈ actualRoots A} → {z // z ∈ (univ : Finset α).image ρ} :=
    fun z => ⟨renameRoot ρ r z.val, maps z.val z.property⟩
  refine ⟨f, ⟨?_, ?_⟩, fun _ => rfl⟩
  · intro x y h
    apply Subtype.ext
    exact rename_injOn A ρ r hr hρ x.property y.property (congrArg Subtype.val h)
  · intro z
    obtain ⟨i, hi, he⟩ := mem_image.mp z.property
    refine ⟨⟨rootMap A i, mem_image.mpr ⟨i, mem_univ i, rfl⟩⟩, ?_⟩
    apply Subtype.ext
    simpa [f, rename_commutes A ρ r hr hρ] using he

/-- Every actual c-class exists under the advertised cardinal validity. -/
theorem valid_class_nonvacuous (c : ℕ) (hc : 1 ≤ c) (hcm : c ≤ Fintype.card α) :
    ∃ A : Finset α, A.card = c ∧ A.Nonempty ∧
      ExactOneClassMap A (rootMap A) := by
  obtain ⟨A, _, hA⟩ := exists_subset_card_eq
    (show c ≤ (univ : Finset α).card by simpa using hcm)
  exact ⟨A, hA, card_pos.mp (by omega), canonical_exact A⟩

omit [DecidableEq α] in
/-- Central assumptions imply strictly fewer tainted labels than all labels. -/
theorem central_strict_nonsaturation (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hBn : B < Fintype.card α-c+1) :
    B+c-1 < Fintype.card α ∧ 0 < B+c-1 := by omega

/-- Generic transported actual-root count for arbitrary names. -/
theorem arbitrary_actual_root_count (A : Finset α) (ρ : α → β)
    (hc : 1 ≤ A.card) (hρ : ExactOneClassMap A ρ) :
    ((univ : Finset α).image ρ).card = Fintype.card α-A.card+1 := by
  have h := arbitrary_map_shared_card A univ univ ρ (card_pos.mp (by omega)) hρ
  simp only [sharedRoots, inter_self] at h
  exact h.trans (actual_root_count A hc)

/-- No new map names or fixed map can change robust safety. -/
theorem all_maps_robust_iff (B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (P R : Finset α) :
    (∀ A : Finset α, A.card = c → ∀ ρ : α → Option α,
      ExactOneClassMap A ρ → B < ((P.image ρ) ∩ (R.image ρ)).card) ↔
    B+c ≤ (P ∩ R).card := by
  constructor
  · intro h
    apply (robust_iff B c hB hc hcm P R).mp
    intro A hA
    exact h A hA (rootMap A) (canonical_exact A)
  · intro hs A hA ρ hρ
    rw [arbitrary_map_shared_card A P R ρ (card_pos.mp (by omega)) hρ]
    exact ((robust_iff B c hB hc hcm P R).mpr hs) A hA

/-- All c-subsets, every exact map, and fault sets retain fixed F/G scope. -/
theorem arbitrary_world_contract_iff (B c : ℕ) (hc : 1 ≤ c)
    (F G : Set (Finset α)) :
    FixedFamilyContract B c F G ↔
    (∀ A : Finset α, A.card = c → ∀ ρ : α → Option α,
      ExactOneClassMap A ρ →
      MapAvailable B ρ F ∧ MapAvailable B ρ G ∧
      ∀ P ∈ F, ∀ R ∈ G, B < ((P.image ρ) ∩ (R.image ρ)).card) := by
  constructor
  · intro h A hA ρ hρ
    have hp : A.Nonempty := card_pos.mp (by omega)
    have hF : MapAvailable B (rootMap A) F := h.1 A hA
    have hG : MapAvailable B (rootMap A) G := h.2.1 A hA
    refine ⟨(arbitrary_map_available_iff B A ρ hp hρ F).mpr hF,
      (arbitrary_map_available_iff B A ρ hp hρ G).mpr hG, ?_⟩
    intro P hP R hR
    rw [arbitrary_map_shared_card A P R ρ hp hρ]
    exact h.2.2 P hP R hR A hA
  · intro h
    refine ⟨?_, ?_, ?_⟩
    · intro A hA
      exact (h A hA (rootMap A) (canonical_exact A)).1
    · intro A hA
      exact (h A hA (rootMap A) (canonical_exact A)).2.1
    · intro P hP R hR A hA
      exact (h A hA (rootMap A) (canonical_exact A)).2.2 P hP R hR

/-- Known actual-root fault membership agrees with the original pulledFault. -/
theorem old_fault_membership (m representative : ℕ) (hr : representative < m)
    (a fault : ℕ → Bool) (i : Fin m) :
    (representativeMap (booleanLabels m a) ⟨representative, hr⟩ i) ∈ booleanLabels m fault ↔
      UnknownRootAttribution.pulledFault a representative fault i.val = true := by
  have mem_b (j : Fin m) : j ∈ booleanLabels m fault ↔ fault j.val = true := by
    simp only [booleanLabels, mem_filter, mem_univ, true_and]
  rw [mem_b, old_rootOf_correspondence m representative hr a i]
  rfl

/-- Generic actual fault sets yield the same recursive cardinal budget. -/
theorem old_fault_cardinality (m : ℕ) (S : Finset (Fin m)) :
    ChargedInterlock.card m (setPredicate S) = S.card := by
  rw [← booleanLabels_card, booleanLabels_setPredicate]

#print axioms rename_bijective
#print axioms valid_class_nonvacuous
#print axioms central_strict_nonsaturation
#print axioms arbitrary_actual_root_count
#print axioms all_maps_robust_iff
#print axioms arbitrary_world_contract_iff
#print axioms old_fault_membership
#print axioms old_fault_cardinality
end AttributionKernel.IndependentReview
