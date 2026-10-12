import GroundedSupport

namespace T20Resumed
open T20Grounded
variable {Root : Type} [DecidableEq Root]

/-- Completeness of minimal supports in a finite retained universe. -/
theorem minimal_operational_support_cover
    (U : Finset Root) (E O : Finset Root → Prop)
    (operation_mono : ∀ A B, A ⊆ B → O A → O B) :
    (∀ A, A ⊆ U → E A → O A) ↔
      (∀ S, S ⊆ U → MinimalFor E S →
        ∃ C, C ⊆ S ∧ MinimalFor O C) := by
  constructor
  · intro h S hSU hmin
    exact exists_minimal_subset O S (h S hSU hmin.1)
  · intro h A hAU hEA
    obtain ⟨S, hSA, hmin⟩ := exists_minimal_subset E A hEA
    obtain ⟨C, hCS, hC⟩ := h S (Finset.Subset.trans hSA hAU) hmin
    exact operation_mono C A (Finset.Subset.trans hCS hSA) hC.1

theorem all_retractions_iff_support_cover
    (U : Finset Root) (E O : Finset Root → Prop)
    (operation_mono : ∀ A B, A ⊆ B → O A → O B) :
    (∀ removed, removed ⊆ U → E (U \ removed) → O (U \ removed)) ↔
      (∀ S, S ⊆ U → MinimalFor E S →
        ∃ C, C ⊆ S ∧ MinimalFor O C) := by
  rw [← minimal_operational_support_cover U E O operation_mono]
  constructor
  · intro h A hAU hEA
    have double_complement : U \ (U \ A) = A := by
      ext x
      simp only [Finset.mem_sdiff]
      constructor
      · intro hx
        by_contra hnot
        exact hx.2 ⟨hx.1, hnot⟩
      · intro hx
        exact ⟨hAU hx, fun hh => hh.2 hx⟩
    have hrem : U \ A ⊆ U := by
      intro x hx
      exact (Finset.mem_sdiff.mp hx).1
    simpa only [double_complement] using h (U \ A) hrem (by simpa only [double_complement] using hEA)
  · intro h removed _ hE
    exact h (U \ removed) (by intro x hx; exact (Finset.mem_sdiff.mp hx).1) hE

/-- Exact instantiation with retained T20 grounded epistemic derivability. -/
theorem grounded_retractions_iff_operational_cover
    (base : Root → Claim → Prop) (rule : Finset Claim → Claim → Prop)
    (claim : Claim) (U : Finset Root) (O : Finset Root → Prop)
    (operation_mono : ∀ A B, A ⊆ B → O A → O B) :
    (∀ removed, removed ⊆ U → Derivable base rule (U \ removed) claim → O (U \ removed)) ↔
      (∀ S, S ⊆ U → MinimalFor (fun A => Derivable base rule A claim) S →
        ∃ C, C ⊆ S ∧ MinimalFor O C) :=
  all_retractions_iff_support_cover U (fun A => Derivable base rule A claim) O operation_mono

end T20Resumed
