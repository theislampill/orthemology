import RationalThresholdComputable

open Set MeasureTheory
open scoped ENNReal NNReal
namespace AtomicMembership.RationalThreshold
open P02A2 P02A2.Q8Measure P02A2.FiniteOutputTable P02.Codec

/-- The upper rational cut is stated for the actual real-valued defect. -/
theorem deficit_cast (q : ℚ≥0) (hq : q ≤ 1) :
    ((1-q : ℚ≥0) : ℝ≥0∞).toReal = 1 - (q : ℝ) := by
  rw [nnrat_cast_real, ENNReal.coe_toReal]
  have hn : (0 : ℝ) ≤ ((1-q : ℚ≥0) : ℚ) := by exact_mod_cast (1-q : ℚ≥0).property
  rw [Real.coe_toNNReal _ hn, NNRat.coe_sub hq]
  push_cast
  rfl

theorem numeric_defect_lt (e : ℕ) (q : ℚ≥0) (hq : q ≤ 1) :
    defect (outputLaw (evaluateIndex e)) < (q : ℝ) ↔
      ∃ i k, ∀ n, lowerCutMatrix (1-q) e i k n := by
  rw [← numeric_mass_gt]
  have hm : mass (outputLaw (evaluateIndex e)) ≠ ∞ :=
    measure_ne_top _ _
  have hr : ((1-q : ℚ≥0) : ℝ≥0∞) ≠ ∞ := by
    rw [nnrat_cast_real]; exact ENNReal.coe_ne_top
  rw [← ENNReal.toReal_lt_toReal hr hm, deficit_cast q hq]
  unfold defect
  constructor <;> intro h <;> linarith

theorem numeric_defect_le (e : ℕ) (q : ℚ≥0) (hq : q ≤ 1) :
    defect (outputLaw (evaluateIndex e)) ≤ (q : ℝ) ↔
      ∀ i, ∃ k, ∀ n, upperCutMatrix (1-q) e i k n := by
  rw [← numeric_mass_ge e (1-q) (tsub_le_self)]
  have hm : mass (outputLaw (evaluateIndex e)) ≠ ∞ := measure_ne_top _ _
  have hr : ((1-q : ℚ≥0) : ℝ≥0∞) ≠ ∞ := by
    rw [nnrat_cast_real]; exact ENNReal.coe_ne_top
  rw [← ENNReal.toReal_le_toReal hr hm, deficit_cast q hq]
  unfold defect
  constructor <;> intro h <;> linarith

theorem numeric_defect_ge (e : ℕ) (q : ℚ≥0) (hq : q ≤ 1) :
    (q : ℝ) ≤ defect (outputLaw (evaluateIndex e)) ↔
      ∀ i k, ∃ n, ¬ lowerCutMatrix (1-q) e i k n := by
  rw [← not_lt, numeric_defect_lt e q hq]
  push_neg
  rfl

theorem numeric_defect_gt (e : ℕ) (q : ℚ≥0) (hq : q ≤ 1) :
    (q : ℝ) < defect (outputLaw (evaluateIndex e)) ↔
      ∃ i, ∀ k, ∃ n, ¬ upperCutMatrix (1-q) e i k n := by
  rw [← not_le, numeric_defect_le e q hq]
  push_neg
  rfl

theorem numeric_defect_eq (e : ℕ) (q : ℚ≥0) (hq : q ≤ 1) :
    defect (outputLaw (evaluateIndex e)) = (q : ℝ) ↔
      (∀ i, ∃ k, ∀ n, upperCutMatrix (1-q) e i k n) ∧
      (∀ i k, ∃ n, ¬ lowerCutMatrix (1-q) e i k n) := by
  rw [le_antisymm_iff, numeric_defect_le e q hq, numeric_defect_ge e q hq]

end AtomicMembership.RationalThreshold
