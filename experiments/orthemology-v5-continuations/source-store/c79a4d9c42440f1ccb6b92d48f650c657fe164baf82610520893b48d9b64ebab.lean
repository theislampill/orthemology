import BernoulliWord

namespace GrowthMoment
noncomputable section
open MeasureTheory Set AnnularLiteral BernoulliWord EndpointMoment
open scoped ENNReal

/-- Common lower-growth factor. Separate positive endpoint factors can be reduced
to their positive minimum; an inactive endpoint profile satisfies this automatically. -/
def LowerGrowth (μ : Measure ℝ) (η : ℝ≥0∞) (x0 : ℝ) : Prop :=
  ∀ x : ℝ, 0<x → x≤x0 →
    (1+η)*μ (Ioc 0 x) ≤ μ (Ioc 0 (2*x)) ∧
    (1+η)*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) 1)

lemma lowerGrowth_of_separate (μ : Measure ℝ) (η0 η1 : ℝ≥0∞) (x0 : ℝ)
    (hg0 : ∀ x : ℝ, 0<x → x≤x0 → (1+η0)*μ (Ioc 0 x) ≤ μ (Ioc 0 (2*x)))
    (hg1 : ∀ x : ℝ, 0<x → x≤x0 → (1+η1)*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) 1)) :
    LowerGrowth μ (min η0 η1) x0 := by
  intro x hx hxx
  constructor
  · exact (mul_le_mul_right' (add_le_add_left (min_le_left η0 η1) 1) _).trans (hg0 x hx hxx)
  · exact (mul_le_mul_right' (add_le_add_left (min_le_right η0 η1) 1) _).trans (hg1 x hx hxx)

lemma min_growth_ne_zero {η0 η1 : ℝ≥0∞} (h0 : η0 ≠ 0) (h1 : η1 ≠ 0) :
    min η0 η1 ≠ 0 := ne_of_gt (lt_min (pos_iff_ne_zero.mpr h0) (pos_iff_ne_zero.mpr h1))

/-- A finite tail sum of finite-word Bayes failure risks forces the actual interior
inverse-variance moment to be finite. This joins the annular proof to Tonelli's exact
counting identity; the moment implication is not an axiom or an assumed hypothesis. -/
theorem finite_tail_risk_implies_inverse_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η ≠ 0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (N : ℕ) (hN : 15≤N) (hscale : 4*(((N+1:ℕ):ℝ)⁻¹)≤x0)
    (report : (n : ℕ) → (Fin n → Bool) → Z → ℝ)
    (hrisk : (∑' t, risk (t+N+1) μ ν e (report (t+N+1))) < ⊤) :
    inverseVarianceMoment μ < ⊤ := by
  let c : ℝ≥0∞ := ENNReal.ofReal (Real.exp (-16)) * η
  have hc : c ≠ 0 := mul_ne_zero (ENNReal.ofReal_ne_zero_iff.mpr (Real.exp_pos _)) hη
  have hpoint : ∀ t : ℕ,
      c*(leftMass μ (t+N) + rightMass μ (t+N)) ≤
        risk (t+N+1) μ ν e (report (t+N+1)) := by
    intro t
    let m : ℕ := t+N+1
    let x : ℝ := (m:ℝ)⁻¹
    have hm : 0 < m := by dsimp [m];omega
    have hmr : 0<(m:ℝ) := by exact_mod_cast hm
    have hx : 0<x := inv_pos.mpr hmr
    have hm16 : (16:ℝ)≤ m := by exact_mod_cast (show 16 ≤ m by dsimp [m];omega)
    have hx16 : x≤1/16 := by
      change (m:ℝ)⁻¹≤1/16
      simpa using (inv_le_inv₀ hmr (by norm_num : (0:ℝ)<16)).mpr hm16
    have hxN : x≤((N+1:ℕ):ℝ)⁻¹ := by
      apply (inv_le_inv₀ hmr (by positivity : (0:ℝ)<((N+1:ℕ):ℝ))).mpr
      exact_mod_cast (show N+1 ≤ m by dsimp [m];omega)
    have hx4 : 4*x≤x0 := (mul_le_mul_of_nonneg_left hxN (by norm_num)).trans hscale
    have hxm : (m:ℝ)*x≤1 := by dsimp [x];rw [mul_inv_cancel₀ (ne_of_gt hmr)]
    obtain ⟨hg0,hg1⟩ := hg x hx (by linarith)
    obtain ⟨hg04,hg14⟩ := hg (4*x) (by positivity) hx4
    have h24 : 2*(4*x)=8*x := by ring
    rw [h24] at hg04 hg14
    have h := all_reports_growth_lower ν μ e x η η m hm (report m)
      he he4 hx hx16 hxm hg0 hg04 hg1 hg14
    rw [leftMass_eq_Ioc μ (t+N) (by omega),rightMass_eq_Ico μ (t+N) (by omega)]
    simpa only [c,m,x,mul_add,mul_assoc] using h
  have htotal : c * (∑' t, (leftMass μ (t+N) + rightMass μ (t+N))) ≤
      ∑' t, risk (t+N+1) μ ν e (report (t+N+1)) := by
    rw [← ENNReal.tsum_mul_left]
    exact ENNReal.tsum_le_tsum hpoint
  apply (endpoint_tail_series_lt_top_iff μ N).mp
  exact ENNReal.lt_top_of_mul_ne_top_right (ne_of_lt (htotal.trans_lt hrisk)) hc

lemma exists_cutoff {x0 : ℝ} (hx0 : 0<x0) :
    ∃ N : ℕ, 15≤N ∧ 4*(((N+1:ℕ):ℝ)⁻¹)≤x0 := by
  obtain ⟨M,hM⟩ := exists_nat_gt (4/x0)
  let N := max 15 M
  refine ⟨N, le_max_left _ _, ?_⟩
  have hMN : (M:ℝ)≤N+1 := by exact_mod_cast (show M≤N+1 by dsimp [N];omega)
  have h4 : 4<(M:ℝ)*x0 := (div_lt_iff₀ hx0).mp hM
  rw [← div_eq_mul_inv]
  apply (div_le_iff₀ (by positivity : (0:ℝ)<((N+1:ℕ):ℝ))).mpr
  push_cast
  nlinarith

/-- The cutoff can be selected from the positive growth radius. Thus any report
family with finite sum of its finite-word risks has a finite interior inverse moment. -/
theorem finite_risk_implies_inverse_moment {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e x0 : ℝ) (η : ℝ≥0∞) (hη : η ≠ 0) (hx0 : 0<x0)
    (he : 0<e) (he4 : e≤1/4) (hg : LowerGrowth μ η x0)
    (report : (n : ℕ) → (Fin n → Bool) → Z → ℝ)
    (hrisk : (∑' t, risk (t+1) μ ν e (report (t+1))) < ⊤) :
    inverseVarianceMoment μ < ⊤ := by
  obtain ⟨N,hN,hscale⟩ := exists_cutoff hx0
  have hsplit : (∑ t ∈ Finset.range N, risk (t+1) μ ν e (report (t+1))) +
      (∑' t, risk (t+N+1) μ ν e (report (t+N+1))) =
      ∑' t, risk (t+1) μ ν e (report (t+1)) :=
    ENNReal.summable.sum_add_tsum_nat_add'
  have htail : (∑' t, risk (t+N+1) μ ν e (report (t+N+1))) < ⊤ := by
    exact lt_of_le_of_lt (by rw [← hsplit];exact le_add_self) hrisk
  exact finite_tail_risk_implies_inverse_moment ν μ e x0 η hη he he4 hg N hN hscale report htail

end
end GrowthMoment
