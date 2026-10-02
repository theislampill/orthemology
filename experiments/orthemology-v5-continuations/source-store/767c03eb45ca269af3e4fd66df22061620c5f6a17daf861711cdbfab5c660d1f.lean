import EmpiricalRepairCost

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2
namespace Orthemology.Tranche3.EndpointBridge

def endpointWeight (b : Bool) : ℝ := if b then 1 else 0

lemma endpointWeight_nonneg (b : Bool) : 0 ≤ endpointWeight b := by cases b <;> norm_num [endpointWeight]
lemma endpointWeight_le_one (b : Bool) : endpointWeight b ≤ 1 := by cases b <;> norm_num [endpointWeight]

/-- The endpoint source's actual one-step law is the appropriate point mass. -/
theorem sourceCoin_endpoint (b : Bool) :
    sourceCoinMeasure (endpointWeight b) (endpointWeight_nonneg b) (endpointWeight_le_one b) = Measure.dirac b := by
  apply Measure.ext_of_singleton
  intro x
  rw [sourceCoin_singleton,Measure.dirac_apply]
  cases b <;> cases x <;> norm_num [endpointWeight,coinMass]

/-- The constructed infinite iid source is constant at a degenerate endpoint,
almost surely at every coordinate, not merely eventually or in distribution. -/
theorem auditSource_endpoint_constant (b : Bool) :
    ∀ᵐ ω ∂auditSourceLaw (endpointWeight b) (endpointWeight_nonneg b) (endpointWeight_le_one b),
      ∀ n, ω n = b := by
  apply ae_all_iff.mpr
  intro n
  have hm : (auditSourceLaw (endpointWeight b) (endpointWeight_nonneg b) (endpointWeight_le_one b)).map
      (fun ω => ω n) = Measure.dirac b := by
    rw [auditSourceLaw,infinite_product_coordinate_law,sourceCoin_endpoint]
  have hb : ∀ᵐ y ∂Measure.dirac b, y = b := by simp
  rw [← hm] at hb
  exact ae_of_ae_map (measurable_pi_apply n).aemeasurable hb

lemma observedPrefix_constant (b : Bool) (ω : ℕ → Bool) (h : ∀ n, ω n = b) (n : ℕ) :
    observedPrefix n ω = constantBits b n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [observedPrefix,constantBits,h,ih]

/-- The always-emitting empirical policy is the unique weakly correct report
from its FIRST opportunity at either endpoint of the actual model family. -/
theorem endpoint_empirical_all_time_weak_repair (b : Bool) (e : ℚ)
    (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    ∀ᵐ ω ∂auditSourceLaw (endpointWeight b) (endpointWeight_nonneg b) (endpointWeight_le_one b),
      ∀ n, LiteralRepairGood (endpointWeight b) e
        (empiricalRepair e n (observedPrefix (n+1) ω)) := by
  have he0' : (0:ℝ) ≤ e := by exact_mod_cast he0
  have he1' : (e:ℝ) ≤ 1/4 := by
    have hh : (e:ℝ) ≤ ((1/4:ℚ):ℝ) := by exact_mod_cast he1
    norm_num at hh ⊢
    exact hh
  filter_upwards [auditSource_endpoint_constant b] with ω hω
  intro n
  rw [observedPrefix_constant b ω hω,empiricalRepair_constant]
  cases b
  · apply (zero_weight_unique (e:ℝ) _).mpr
    norm_num
  · apply (one_weight_unique (e:ℝ) _ he0' he1').mpr
    norm_num

/-- The endpoint expected TOTAL count of incorrect literal reports is exactly
zero, despite the interior lower bound becoming unbounded near each endpoint. -/
theorem endpoint_empirical_expected_failure_zero (b : Bool) (e : ℚ)
    (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    (∫⁻ ω, ∑' n, (EmpiricalFailure (endpointWeight b) e n).indicator 1 ω
      ∂auditSourceLaw (endpointWeight b) (endpointWeight_nonneg b) (endpointWeight_le_one b)) = 0 := by
  have he : (fun ω => ∑' n, (EmpiricalFailure (endpointWeight b) e n).indicator
      (1 : (ℕ → Bool) → ℝ≥0∞) ω) =ᵐ[auditSourceLaw (endpointWeight b)
        (endpointWeight_nonneg b) (endpointWeight_le_one b)] 0 := by
    filter_upwards [endpoint_empirical_all_time_weak_repair b e he0 he1] with ω hω
    apply ENNReal.tsum_eq_zero.mpr
    intro n
    exact Set.indicator_of_not_mem (by exact not_not.mpr (hω n)) _
  rw [lintegral_congr_ae he]
  simp
end Orthemology.Tranche3.EndpointBridge
