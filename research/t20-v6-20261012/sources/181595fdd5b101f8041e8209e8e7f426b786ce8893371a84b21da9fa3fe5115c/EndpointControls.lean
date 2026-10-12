import NumericMembership

open Set MeasureTheory
open scoped ENNReal
open P02A2 P02A2.Q8Measure P02A2.FiniteOutputTable P02.Codec AtomicMembership
namespace AtomicMembershipAudit

/-- Positivity and nonzero defect agree for the probability endpoint used here. -/
theorem probability_defect_pos_iff_ne_zero (μ : Measure Cantor) [IsProbabilityMeasure μ] :
    0 < defect μ ↔ defect μ ≠ 0 := by
  have hm : mass μ ≤ 1 := by simpa using positive_le_total μ
  have hmr : (mass μ).toReal ≤ 1 := by
    simpa using ENNReal.toReal_mono (by norm_num : (1 : ℝ≥0∞) ≠ ∞) hm
  have hn : 0 ≤ defect μ := by unfold defect; linarith
  constructor
  · exact ne_of_gt
  · intro h
    rcases lt_or_eq_of_le hn with hl | he
    · exact hl
    · exact (h he.symm).elim

/-- Named corollary for the actual decoded numeric observer law. -/
theorem numeric_positive_defect_iff_not_member (e : ℕ) :
    0 < defect (outputLaw (evaluateIndex e)) ↔
      e ∉ P02A2.Pi3IndexReduction.zeroDefectIndices := by
  exact probability_defect_pos_iff_ne_zero (outputLaw (evaluateIndex e))

/-- Review-derived Σ3 endpoint, preserving the frozen author bridge. -/
theorem numeric_positive_defect_nat_normal (e : ℕ) :
    0 < defect (outputLaw (evaluateIndex e)) ↔
      ∃ i, ∀ k, ∃ n, ¬ membershipMatrix e i k n := by
  exact (numeric_positive_defect_iff_not_member e).trans
    (numeric_not_zero_defect_nat_normal e)

end AtomicMembershipAudit
