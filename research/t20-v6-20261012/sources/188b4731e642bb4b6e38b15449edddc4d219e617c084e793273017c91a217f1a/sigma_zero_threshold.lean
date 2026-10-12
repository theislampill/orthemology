import RationalShiftRealisation

/-! The same fixed 0/1-defect numerical family works at every real threshold
0<r≤1. This supplies the lower-side compiler assurance, not a new ordinary
arithmetical-hierarchy classification. -/
namespace OrthemologyRationalShift
open P02A2 P02A2.ObserverCore P02A2.Q8Measure P02.Codec

theorem exists_primrec_sigma2_threshold_reduction
    (R : ℕ → ℕ → ℕ → Prop) [∀ e, DecidableRel (R e)]
    (hR : PrimrecRel (fun p : ℕ × ℕ => R p.1 p.2)) :
    ∃ f : ℕ → ℕ, Primrec f ∧ ∀ e,
      defect (fairCantor.map (output (evaluateIndex (f e)))) =
        defect (Sigma2RowLaw.rowLaw R e) ∧
      ∀ r : ℝ, 0 ≤ r → r ≤ 1 →
      (defect (fairCantor.map (output (evaluateIndex (f e)))) < r ↔
        ∃ s, ∀ t, R e s t) ∧
      (r ≤ defect (fairCantor.map (output (evaluateIndex (f e)))) ↔
        ∀ s, ∃ t, ¬ R e s t) := by
  classical
  obtain ⟨p,hp,hpLaw⟩ := exists_primrec_rational_shift (SurvivorPrimrec.prefixFunction R)
    (Sigma2RowLaw.joint_prefix_primitive_recursive R hR) 0 1 (by omega) (by omega)
  refine ⟨parameterIndex p,hp,fun e => ?_⟩
  have hlaw : defect (fairCantor.map (output (evaluateIndex (parameterIndex p e)))) =
      defect (Sigma2RowLaw.rowLaw R e) := by
    simpa [Sigma2RowLaw.rowLaw, Sigma2RowLaw.observer] using (hpLaw e).2
  refine ⟨hlaw,fun r hr hr1 => ?_⟩
  rw [hlaw]
  by_cases h : ∃ s, ∀ t, R e s t
  · rw [(Sigma2RowLaw.defect_zero_iff_witness R e).mpr h]
    have hn : ¬ (∀ s, ∃ t, ¬ R e s t) := by
      push_neg
      exact h
    simp [h, hn, hr, not_le_of_gt hr]
  · rw [(Sigma2RowLaw.defect_one_iff_no_witness R e).mpr h]
    have hn : ∀ s, ∃ t, ¬ R e s t := by
      push_neg at h
      exact h
    simp [h, hn, hr1, not_lt_of_ge hr1]

end OrthemologyRationalShift
#print axioms OrthemologyRationalShift.exists_primrec_sigma2_threshold_reduction
