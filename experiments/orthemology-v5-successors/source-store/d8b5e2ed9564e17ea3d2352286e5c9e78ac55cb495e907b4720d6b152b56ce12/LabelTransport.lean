import CoveringPortfolio

namespace CoveringKernel
open Finset
variable {α β : Type*} [Fintype α] [Fintype β] [DecidableEq α] [DecidableEq β]

omit [Fintype α] [Fintype β] [DecidableEq α] [DecidableEq β] in
theorem transport_cover (e : α ≃ β) (b k : ℕ) (G : Finset (Finset α))
    (hu : Uniform b G) (hc : Covers k G) :
    Uniform b (G.map e.finsetCongr.toEmbedding) ∧
      Covers k (G.map e.finsetCongr.toEmbedding) := by
  constructor
  · intro A hA
    obtain ⟨P, hP, rfl⟩ := mem_map.mp hA
    simpa [Equiv.finsetCongr_apply] using hu P hP
  · intro T hT
    have hpre : (e.symm.finsetCongr T).card = k := by
      simpa [Equiv.finsetCongr_apply] using hT
    obtain ⟨A, hA, hsub⟩ := hc (e.symm.finsetCongr T) hpre
    refine ⟨e.finsetCongr A, mem_map.mpr ⟨A, hA, rfl⟩, ?_⟩
    have hm : e.finsetCongr (e.symm.finsetCongr T) ⊆ e.finsetCongr A := by
      simpa only [Equiv.finsetCongr_apply] using (map_subset_map.mpr hsub :
        (e.symm.finsetCongr T).map e.toEmbedding ⊆ A.map e.toEmbedding)
    have he : e.symm.finsetCongr = e.finsetCongr.symm := rfl
    rw [he, Equiv.apply_symm_apply] at hm
    exact hm

omit [Fintype α] [Fintype β] [DecidableEq α] [DecidableEq β] in
theorem cover_sizes_equiv (e : α ≃ β) (b k t : ℕ) :
    (∃ G : Finset (Finset α), Uniform b G ∧ Covers k G ∧ G.card = t) ↔
    (∃ G : Finset (Finset β), Uniform b G ∧ Covers k G ∧ G.card = t) := by
  constructor
  · rintro ⟨G, hu, hc, ht⟩
    obtain ⟨hu', hc'⟩ := transport_cover e b k G hu hc
    exact ⟨_, hu', hc', (card_map _).trans ht⟩
  · rintro ⟨G, hu, hc, ht⟩
    obtain ⟨hu', hc'⟩ := transport_cover e.symm b k G hu hc
    exact ⟨_, hu', hc', (card_map _).trans ht⟩

theorem coveringNumber_equiv (e : α ≃ β) (b k : ℕ) :
    coveringNumber α b k = coveringNumber β b k := by
  unfold coveringNumber
  congr 1
  ext t
  exact cover_sizes_equiv e b k t

/-- Standard numeric covering notation, independent of the names of labels. -/
noncomputable def C (m b k : ℕ) : ℕ := coveringNumber (Fin m) b k

theorem coveringNumber_eq_C (b k : ℕ) :
    coveringNumber α b k = C (Fintype.card α) b k :=
  coveringNumber_equiv (Fintype.equivFin α) b k

#print axioms coveringNumber_equiv
#print axioms coveringNumber_eq_C
end CoveringKernel
