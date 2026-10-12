import ObservedEmpiricalRows

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Adaptive HiddenParity.Empirical
open scoped BigOperators ENNReal Topology

namespace IndependentEmpiricalProbe
local instance : MeasurableSpace Bool := ⊤
local instance : MeasurableSingletonClass Bool := ⟨fun _ => trivial⟩
local instance : MeasurableSpace Unit := ⊤
local instance : MeasurableSingletonClass Unit := ⟨fun _ => trivial⟩

def repeatFalse (_ : Unit) (_ : History Bool Bool) : Bool := false
def ones : Unit × FlatStack Bool Bool := ((),fun _ => true)

lemma actual_count (n : ℕ) : countBefore repeatFalse ones false n=n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [countBefore_succ,stackActionTrajectory,repeatFalse,ih]

lemma actual_frequency_one (n : ℕ) :
    historyFrequency false true (stackHistoryTrajectory repeatFalse ones (n+1))=1 := by
  rw [historyFrequency_eq_rawFrequency,actual_count]
  simp only [rawFrequency,seededStackCoordinate,ones,symbolIndicator,if_pos rfl,
    Finset.sum_const,Finset.card_range,nsmul_eq_mul,ite_true,mul_one]
  exact div_self (by positivity)

/-- Equality of the coordinate gap and tolerance does not force strict rejection. -/
lemma strict_gap_is_necessary (n : ℕ) :
    |historyFrequency false true (stackHistoryTrajectory repeatFalse ones (n+1))-(3/4:ℝ)|=1/4 ∧
    ¬ ((1/4:ℝ) < |historyFrequency false true (stackHistoryTrajectory repeatFalse ones (n+1))-3/4|) := by
  rw [actual_frequency_one]
  norm_num [abs_of_nonneg]

/-- Without positive epsilon every nonempty-family raw tail event is the whole space. -/
lemma zero_tolerance_tail (P : Bool → Bool → ℝ) (N : ℕ) :
    RawTailDeviation (R:=Unit) P 0 N=Set.univ := by
  ext z
  constructor
  · intro _;trivial
  · intro _;exact ⟨false,false,N,le_rfl,abs_nonneg _⟩

lemma no_zero_tolerance_true_test (n : ℕ) :
    ¬ |historyFrequency false true (stackHistoryTrajectory repeatFalse ones (n+1))-(1:ℝ)|<0 := by
  rw [actual_frequency_one]
  norm_num

def deterministicRows (_a y : Bool) : ℝ := if y then 1 else 0
lemma rows_nonneg (a y : Bool) : 0≤deterministicRows a y := by cases y <;> norm_num [deterministicRows]
lemma rows_normalized (a : Bool) : ∑ y : Bool, deterministicRows a y=1 := by simp [deterministicRows]

lemma actual_symbol_mean_one (a : Bool) (n : ℕ) :
    (∫ z : Unit × FlatStack Bool Bool, symbolIndicator true (seededStackCoordinate a n z)
      ∂(Measure.dirac ()).prod (stackMeasure deterministicRows rows_nonneg rows_normalized))=1 := by
  simpa [deterministicRows] using seeded_symbol_integral (Measure.dirac ()) deterministicRows
    rows_nonneg rows_normalized a true n

lemma actual_symbol_mean_zero (a : Bool) (n : ℕ) :
    (∫ z : Unit × FlatStack Bool Bool, symbolIndicator false (seededStackCoordinate a n z)
      ∂(Measure.dirac ()).prod (stackMeasure deterministicRows rows_nonneg rows_normalized))=0 := by
  simpa [deterministicRows] using seeded_symbol_integral (Measure.dirac ()) deterministicRows
    rows_nonneg rows_normalized a false n

lemma zero_probability_symbol_consistency (a : Bool) :
    ∀ᵐ z ∂(Measure.dirac ()).prod (stackMeasure deterministicRows rows_nonneg rows_normalized),
      Tendsto (fun n => rawFrequency a false n z) atTop (𝓝 (0:ℝ)) := by
  simpa [deterministicRows] using seeded_rawFrequency_tendsto (Measure.dirac ()) deterministicRows
    rows_nonneg rows_normalized a false

set_option pp.fullNames true
#check @IndependentEmpiricalProbe.actual_count
#check @IndependentEmpiricalProbe.actual_frequency_one
#check @IndependentEmpiricalProbe.strict_gap_is_necessary
#check @IndependentEmpiricalProbe.zero_tolerance_tail
#check @IndependentEmpiricalProbe.no_zero_tolerance_true_test
#check @IndependentEmpiricalProbe.actual_symbol_mean_one
#check @IndependentEmpiricalProbe.actual_symbol_mean_zero
#check @IndependentEmpiricalProbe.zero_probability_symbol_consistency
#print axioms IndependentEmpiricalProbe.actual_count
#print axioms IndependentEmpiricalProbe.actual_frequency_one
#print axioms IndependentEmpiricalProbe.strict_gap_is_necessary
#print axioms IndependentEmpiricalProbe.zero_tolerance_tail
#print axioms IndependentEmpiricalProbe.no_zero_tolerance_true_test
#print axioms IndependentEmpiricalProbe.actual_symbol_mean_one
#print axioms IndependentEmpiricalProbe.actual_symbol_mean_zero
#print axioms IndependentEmpiricalProbe.zero_probability_symbol_consistency
#check @HiddenParity.Empirical.exists_uniform_summable_burnin
#check @HiddenParity.Empirical.seeded_true_phase_rejections_bounded
#check @HiddenParity.Empirical.seeded_false_rows_eventually_rejected
end IndependentEmpiricalProbe
