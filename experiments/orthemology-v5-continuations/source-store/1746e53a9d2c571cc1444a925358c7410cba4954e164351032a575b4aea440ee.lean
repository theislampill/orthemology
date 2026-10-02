import AELicensedEquivalence
import Mathlib.Probability.Distributions.Geometric

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3.ErrorClockControl
open Orthemology.Tranche3.CanonicalMicro

def seedPMF : PMF ℕ := geometricPMF (p := (1/2 : ℝ)) (by norm_num) (by norm_num)
def errorTime (k : ℕ) : ℕ := 2^(k+1)
def oneErrorStream (k : ℕ) (t : ℕ) : Bool := decide (t = errorTime k)
def oneErrorLaw : Measure (ℕ → Bool) := seedPMF.toMeasure.map oneErrorStream

lemma oneErrorStream_measurable : Measurable oneErrorStream := measurable_of_countable _

/-- Every sample path has exactly one target error. -/
theorem total_bad_exactly_one (k : ℕ) :
    (∑' t, badActionCost ({false} : Finset Bool) (oneErrorStream k t)) = 1 := by
  classical
  rw [tsum_eq_single (errorTime k)]
  · simp [badActionCost,oneErrorStream]
  · intro t ht
    simp [badActionCost,oneErrorStream,ht]

/-- The unique bad action occurs at the declared physical time. -/
theorem time_weighted_bad_exactly_errorTime (k : ℕ) :
    (∑' t, if oneErrorStream k t = true then (t : ℝ≥0∞) else 0) = errorTime k := by
  classical
  rw [tsum_eq_single (errorTime k)]
  · simp [oneErrorStream]
  · intro t ht
    simp [oneErrorStream,ht]

/-- Hence the expected total target-error count is exactly one. -/
theorem expected_total_bad_eq_one :
    (∫⁻ x, ∑' t, badActionCost ({false} : Finset Bool) (x t) ∂oneErrorLaw) = 1 := by
  rw [oneErrorLaw,lintegral_map (total_bad_measurable ({false} : Finset Bool)) oneErrorStream_measurable]
  simp_rw [total_bad_exactly_one]
  simp

lemma geometric_time_weight (k : ℕ) : seedPMF k * (errorTime k : ℝ≥0∞) = 1 := by
  have hr : (((1/2 : ℝ)^k)*(1/2))*2^(k+1) = 1 := by
    rw [pow_succ]
    have hp : (1/2 : ℝ)^k * 2^k = 1 := by rw [← mul_pow]; norm_num
    nlinarith
  have hp : seedPMF k = ENNReal.ofReal (((1/2:ℝ)^k)*(1/2)) := by
    change ENNReal.ofReal (((1-(1/2:ℝ))^k)*(1/2)) = _
    norm_num
  have ht : (errorTime k : ℝ≥0∞) = ENNReal.ofReal ((2:ℝ)^(k+1)) := by
    simp [errorTime,ENNReal.ofReal_pow]
  rw [hp,ht,← ENNReal.ofReal_mul (by positivity),hr]
  norm_num

/-- The expected physical time of the unique error is infinite. Thus even an
exact unit total-error budget alone cannot imply a finite expected restoration time. -/
theorem expected_unique_error_time_eq_top :
    (∫⁻ x, ∑' t, if x t = true then (t : ℝ≥0∞) else 0 ∂oneErrorLaw) = ⊤ := by
  have hm : Measurable (fun x : ℕ → Bool => ∑' t, if x t = true then (t : ℝ≥0∞) else 0) := by
    apply Measurable.ennreal_tsum
    intro t
    exact Measurable.ite ((measurableSet_singleton true).preimage (measurable_pi_apply t)) measurable_const measurable_const
  rw [oneErrorLaw,lintegral_map hm oneErrorStream_measurable]
  simp_rw [time_weighted_bad_exactly_errorTime]
  rw [pmf_lintegral_eq_mean,pmfMean]
  simp_rw [geometric_time_weight]
  simp
end Orthemology.Tranche3.ErrorClockControl
