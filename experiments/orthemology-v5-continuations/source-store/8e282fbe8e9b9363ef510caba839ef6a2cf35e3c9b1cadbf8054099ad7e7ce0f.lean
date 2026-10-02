import ErrorClockCounterexample
noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3.ClockAudit
open ErrorClockControl CanonicalMicro

/-- The exact first index from which all later actions are correct. -/
theorem restoration_iff (k N : ℕ) :
    (∀ t, N ≤ t → oneErrorStream k t = false) ↔ errorTime k < N := by
  constructor
  · intro h
    by_contra hn
    have hz := h (errorTime k) (Nat.le_of_not_gt hn)
    simp [oneErrorStream] at hz
  · intro h t ht
    have hne : t ≠ errorTime k := by omega
    simp [oneErrorStream,hne]

theorem every_path_eventually_correct (k : ℕ) :
    ∀ᶠ t in atTop, oneErrorStream k t = false := by
  apply eventually_atTop.mpr
  exact ⟨errorTime k + 1, fun t ht => (restoration_iff k (errorTime k + 1)).mpr (by omega) t ht⟩

theorem seed_expected_time :
    (∫⁻ k, (errorTime k : ℝ≥0∞) ∂seedPMF.toMeasure) = ⊤ := by
  rw [pmf_lintegral_eq_mean,pmfMean]
  simp_rw [geometric_time_weight]
  simp

theorem expected_first_restoration_eq_top :
    (∫⁻ k, ((errorTime k + 1 : ℕ) : ℝ≥0∞) ∂seedPMF.toMeasure) = ⊤ := by
  apply top_unique
  rw [← seed_expected_time]
  apply lintegral_mono
  intro k
  change (errorTime k : ℝ≥0∞) ≤ ((errorTime k + 1 : ℕ) : ℝ≥0∞)
  simp only [Nat.cast_add, Nat.cast_one]
  exact le_add_of_nonneg_right (by positivity)

theorem no_uniform_deterministic_restoration (N : ℕ) :
    ∃ k t, N ≤ t ∧ oneErrorStream k t = true := by
  refine ⟨N, errorTime N, ?_, ?_⟩
  · exact le_trans (Nat.le_succ N) (Nat.lt_two_pow_self (n := N + 1)).le
  · simp [oneErrorStream]
end Orthemology.Tranche3.ClockAudit
set_option pp.universes true
set_option pp.explicit true
#print Orthemology.Tranche3.ErrorClockControl.seedPMF
#print Orthemology.Tranche3.ErrorClockControl.errorTime
#print Orthemology.Tranche3.ErrorClockControl.oneErrorStream
#print Orthemology.Tranche3.ErrorClockControl.oneErrorLaw
#check Orthemology.Tranche3.ErrorClockControl.total_bad_exactly_one
#check Orthemology.Tranche3.ErrorClockControl.expected_total_bad_eq_one
#check Orthemology.Tranche3.ErrorClockControl.expected_unique_error_time_eq_top
#print axioms Orthemology.Tranche3.ErrorClockControl.total_bad_exactly_one
#print axioms Orthemology.Tranche3.ErrorClockControl.time_weighted_bad_exactly_errorTime
#print axioms Orthemology.Tranche3.ErrorClockControl.expected_total_bad_eq_one
#print axioms Orthemology.Tranche3.ErrorClockControl.geometric_time_weight
#print axioms Orthemology.Tranche3.ErrorClockControl.expected_unique_error_time_eq_top
#check Orthemology.Tranche3.ClockAudit.restoration_iff
#check Orthemology.Tranche3.ClockAudit.expected_first_restoration_eq_top
#print axioms Orthemology.Tranche3.ClockAudit.restoration_iff
#print axioms Orthemology.Tranche3.ClockAudit.every_path_eventually_correct
#print axioms Orthemology.Tranche3.ClockAudit.expected_first_restoration_eq_top
#print axioms Orthemology.Tranche3.ClockAudit.no_uniform_deterministic_restoration
