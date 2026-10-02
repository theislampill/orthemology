import EmpiricalChernoff

namespace ExponentialSeries
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment BayesBridge CentredBernoulli EmpiricalGeometry EmpiricalChernoff
open scoped ENNReal

lemma exponential_geometric {c : ℝ} (n : ℕ) :
    2*Real.exp (-((n+1:ℕ):ℝ)*c) =
      (2*Real.exp (-c))*(Real.exp (-c))^n := by
  rw [← Real.exp_nat_mul]
  rw [mul_assoc,← Real.exp_add]
  congr 1
  push_cast
  ring

lemma exponential_summable {c : ℝ} (hc : 0<c) :
    Summable (fun n : ℕ => 2*Real.exp (-((n+1:ℕ):ℝ)*c)) := by
  have hr : ‖Real.exp (-c)‖<1 := by
    rw [Real.norm_eq_abs,abs_of_pos (Real.exp_pos _)]
    simpa using Real.exp_lt_exp.mpr (show -c<0 by linarith)
  simp_rw [exponential_geometric]
  exact (summable_geometric_of_norm_lt_one hr).mul_left _

lemma exponential_series_bound {c : ℝ} (hc : 0<c) :
    (∑' n : ℕ, 2*Real.exp (-((n+1:ℕ):ℝ)*c)) ≤ 2/c := by
  let r := Real.exp (-c)
  have hr0 : 0<r := Real.exp_pos _
  have hr1 : r<1 := by
    dsimp [r]
    simpa using Real.exp_lt_exp.mpr (show -c<0 by linarith)
  have hrnorm : ‖r‖<1 := by rwa [Real.norm_eq_abs,abs_of_pos hr0]
  have hseries : (∑' n : ℕ, 2*Real.exp (-((n+1:ℕ):ℝ)*c)) = 2*r*(1-r)⁻¹ := by
    simp_rw [exponential_geometric]
    rw [tsum_mul_left,tsum_geometric_of_norm_lt_one hrnorm]
  have hcr : (c+1)*r≤1 := by
    have h := mul_le_mul_of_nonneg_right (Real.add_one_le_exp c) hr0.le
    have hexp : Real.exp c*r=1 := by dsimp [r];rw [← Real.exp_add];simp
    rwa [hexp] at h
  rw [hseries,← div_eq_mul_inv]
  apply (div_le_div_iff₀ (by linarith : 0<1-r) hc).mpr
  nlinarith

/-- Integrable geometric envelope, with the exact variance order 1/[a(1-a)]. -/
theorem summed_error_bound {a e : ℝ} (ha : 0<a) (ha1 : a<1)
    (he : 0<e) (he4 : e≤1/4) :
    (∑' n : ℕ, error (n+1) a e) ≤ ENNReal.ofReal ((32/e^2)*(a*(1-a))⁻¹) := by
  let c := e^2*a*(1-a)/16
  have hb : 0<1-a := by linarith
  have hc : 0<c := by dsimp [c];positivity
  have hp : ∀ n : ℕ, error (n+1) a e ≤ ENNReal.ofReal (2*Real.exp (-((n+1:ℕ):ℝ)*c)) := by
    intro n
    convert error_upper (n+1) (by omega) ha.le ha1.le he he4 using 1 <;> congr 2 <;> dsimp [c] <;> ring
  have htotal := ENNReal.tsum_le_tsum hp
  rw [← ENNReal.ofReal_tsum_of_nonneg (fun n => by positivity) (exponential_summable hc)] at htotal
  have heq : 2/c=(32/e^2)*(a*(1-a))⁻¹ := by dsimp [c];field_simp;ring
  exact htotal.trans (by rw [← heq];exact ENNReal.ofReal_le_ofReal (exponential_series_bound hc))

end
end ExponentialSeries
