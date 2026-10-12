import CompactObservationBoundary

open MeasureTheory Filter Set

namespace CompactConfinementAudit

noncomputable def law : Measure Unit := Measure.dirac ()
instance : IsProbabilityMeasure law := by unfold law; infer_instance

/-- Merely naming a compact C does not supply eventual confinement in C. All
other premises hold for one closed target and one common nonzero probability. -/
theorem missing_confinement_counterexample :
    IsCompact ({0} : Set ℝ) ∧ IsClosed ({1} : Set ℝ) ∧
    law ≪ law ∧
    (∀ᵐ _ω ∂law, ∀ᶠ _n : ℕ in atTop, (1 : ℝ) ∈ ({1} : Set ℝ)) ∧
    ¬ (∃ a ∈ ({0} : Set ℝ), a ∈ ({1} : Set ℝ)) := by
  refine ⟨isCompact_singleton, isClosed_singleton, Measure.AbsolutelyContinuous.rfl, ?_, ?_⟩
  · exact Eventually.of_forall (fun _ => Eventually.of_forall (fun _ => rfl))
  · rintro ⟨a,ha,hb⟩
    have h0 : a = 0 := ha
    have h1 : a = 1 := hb
    linarith

theorem confinement_really_fails :
    ¬ (∀ᵐ _ω ∂law, ∀ᶠ _n : ℕ in atTop, (1 : ℝ) ∈ ({0} : Set ℝ)) := by
  intro h
  obtain ⟨ω,hω⟩ := h.exists
  obtain ⟨n,hn⟩ := hω.exists
  norm_num at hn

#print axioms missing_confinement_counterexample
#print axioms confinement_really_fails
end CompactConfinementAudit
