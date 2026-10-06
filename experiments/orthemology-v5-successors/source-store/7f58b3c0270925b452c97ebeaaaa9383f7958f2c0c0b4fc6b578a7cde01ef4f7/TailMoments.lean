import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic
noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators
namespace Orthemology.TailMoments

lemma le_tail_indicator_sum (z : ℝ≥0∞) :
    z ≤ ∑' n : ℕ, if (n:ℝ≥0∞) < z then 1 else 0 := by
  by_cases hz : z = ⊤
  · subst z
    simp [ENNReal.tsum_const_eq_top_of_ne_zero]
  let K := Nat.ceil z.toReal
  have hK : z ≤ (K:ℝ≥0∞) := by
    have h := ENNReal.ofReal_le_ofReal (Nat.le_ceil z.toReal)
    simpa [ENNReal.ofReal_toReal hz] using h
  apply hK.trans
  calc
    (K:ℝ≥0∞) = ∑ n ∈ Finset.range K,
        (if (n:ℝ≥0∞) < z then 1 else 0) := by
      have he : ∀ n ∈ Finset.range K, (n:ℝ≥0∞) < z := by
        intro n hn
        have hr : (n:ℝ) < z.toReal := (Nat.lt_ceil).mp (Finset.mem_range.mp hn)
        exact (ENNReal.toReal_lt_toReal (by simp) hz).mp (by simpa using hr)
      rw [Finset.sum_congr rfl (fun n hn => if_pos (he n hn))]
      simp
    _ ≤ _ := ENNReal.sum_le_tsum (Finset.range K)

/-- Every extended nonnegative cost is bounded by its integer tail sum.
This handles genuinely infinite costs rather than silently converting them to zero. -/
theorem lintegral_le_tail_sum {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (C : Ω → ℝ≥0∞) (hC : Measurable C) :
    (∫⁻ ω, C ω ∂μ) ≤ ∑' n : ℕ, μ {ω | (n:ℝ≥0∞) < C ω} := by
  calc
    (∫⁻ ω, C ω ∂μ) ≤ ∫⁻ ω, ∑' n : ℕ,
        if (n:ℝ≥0∞) < C ω then 1 else 0 ∂μ :=
      lintegral_mono (fun ω => le_tail_indicator_sum (C ω))
    _ = ∑' n : ℕ, ∫⁻ ω, if (n:ℝ≥0∞) < C ω then 1 else 0 ∂μ := by
      apply lintegral_tsum
      intro n
      exact (Measurable.ite (measurableSet_lt measurable_const hC)
        (measurable_const : Measurable (fun _ : Ω => (1:ℝ≥0∞))) measurable_const).aemeasurable
    _ = _ := by
      apply tsum_congr
      intro n
      have hs : MeasurableSet {ω | (n:ℝ≥0∞) < C ω} :=
        measurableSet_lt measurable_const hC
      have hh := lintegral_indicator (μ := μ) hs (fun _ : Ω => (1:ℝ≥0∞))
      simpa [Set.indicator,lintegral_const] using hh


theorem lintegral_le_geometric_tail {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (A r : ℝ≥0∞)
    (htail : ∀ n : ℕ, μ {ω | (n:ℝ≥0∞) < C ω} ≤ A*r^n) :
    (∫⁻ ω, C ω ∂μ) ≤ A*(1-r)⁻¹ := by
  calc
    (∫⁻ ω, C ω ∂μ) ≤ ∑' n : ℕ, μ {ω | (n:ℝ≥0∞) < C ω} :=
      lintegral_le_tail_sum μ C hC
    _ ≤ ∑' n : ℕ, A*r^n := ENNReal.tsum_le_tsum htail
    _ = _ := by rw [ENNReal.tsum_mul_left, ENNReal.tsum_geometric]

theorem geometric_tail_finite_expectation {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (A r : ℝ≥0∞) (hA : A < ⊤) (hr : r < 1)
    (htail : ∀ n : ℕ, μ {ω | (n:ℝ≥0∞) < C ω} ≤ A*r^n) :
    (∫⁻ ω, C ω ∂μ) < ⊤ := by
  apply lt_of_le_of_lt (lintegral_le_geometric_tail μ C hC A r htail)
  apply ENNReal.mul_lt_top hA
  exact ENNReal.inv_lt_top.mpr (tsub_pos_iff_lt.mpr hr)

lemma exponential_le_weighted_tail (z : ℝ≥0∞) (θ : ℝ) (hθ : 0 ≤ θ) :
    ENNReal.ofReal (Real.exp (θ*z.toReal)) ≤ 1 +
      ENNReal.ofReal (Real.exp θ) * ∑' n : ℕ,
        if (n:ℝ≥0∞) < z then ENNReal.ofReal (Real.exp θ)^n else 0 := by
  by_cases hz : z = ⊤
  · subst z; simp
  by_cases hz0 : z = 0
  · subst z; simp
  let K := Nat.ceil z.toReal
  have hx : 0 < z.toReal := ENNReal.toReal_pos hz0 hz
  have hK : 0 < K := Nat.ceil_pos.mpr hx
  let n := K-1
  have hnK : n+1=K := by omega
  have hn : (n:ℝ) < z.toReal := Nat.lt_ceil.mp (by omega : n<K)
  have hnz : (n:ℝ≥0∞) < z :=
    (ENNReal.toReal_lt_toReal (by simp) hz).mp (by simpa using hn)
  have hxupper : z.toReal ≤ (n:ℝ)+1 := by
    have hh : z.toReal ≤ (K:ℝ) := Nat.le_ceil z.toReal
    rw [← hnK, Nat.cast_add, Nat.cast_one] at hh
    exact hh
  have hexp : Real.exp (θ*z.toReal) ≤ Real.exp θ * (Real.exp θ)^n := by
    calc
      Real.exp (θ*z.toReal) ≤ Real.exp (θ*((n:ℝ)+1)) :=
        Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left hxupper hθ)
      _ = Real.exp θ * (Real.exp θ)^n := by
        rw [mul_add, mul_one, Real.exp_add, mul_comm θ (n:ℝ), Real.exp_nat_mul]
        ring
  have hterm : ENNReal.ofReal (Real.exp θ)^n ≤ ∑' j : ℕ,
      if (j:ℝ≥0∞) < z then ENNReal.ofReal (Real.exp θ)^j else 0 := by
    have hh := ENNReal.le_tsum n (f := fun j : ℕ =>
      if (j:ℝ≥0∞) < z then ENNReal.ofReal (Real.exp θ)^j else 0)
    simpa only [if_pos hnz] using hh
  calc
    ENNReal.ofReal (Real.exp (θ*z.toReal)) ≤
      ENNReal.ofReal (Real.exp θ) * ENNReal.ofReal (Real.exp θ)^n := by
        simpa only [ENNReal.ofReal_mul (Real.exp_pos θ).le,
          ENNReal.ofReal_pow (Real.exp_pos θ).le] using ENNReal.ofReal_le_ofReal hexp
    _ ≤ ENNReal.ofReal (Real.exp θ) * _ := mul_le_mul_left' hterm _
    _ ≤ 1 + _ := le_add_self

theorem exponential_moment_le_geometric_tail {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (A r : ℝ≥0∞) (θ : ℝ) (hθ : 0 ≤ θ)
    (htail : ∀ n : ℕ, μ {ω | (n:ℝ≥0∞) < C ω} ≤ A*r^n) :
    (∫⁻ ω, ENNReal.ofReal (Real.exp (θ*(C ω).toReal)) ∂μ) ≤
      1 + ENNReal.ofReal (Real.exp θ)*A*
        (1-ENNReal.ofReal (Real.exp θ)*r)⁻¹ := by
  let b := ENNReal.ofReal (Real.exp θ)
  let f : ℕ → Ω → ℝ≥0∞ := fun n ω => if (n:ℝ≥0∞) < C ω then b^n else 0
  have hf : ∀ n, Measurable (f n) := fun n =>
    Measurable.ite (measurableSet_lt measurable_const hC) measurable_const measurable_const
  have hsum : Measurable (fun ω => ∑' n, f n ω) := Measurable.ennreal_tsum hf
  have hi : ∀ n, (∫⁻ ω, f n ω ∂μ) = b^n * μ {ω | (n:ℝ≥0∞) < C ω} := by
    intro n
    have hs : MeasurableSet {ω | (n:ℝ≥0∞) < C ω} := measurableSet_lt measurable_const hC
    have hh := lintegral_indicator (μ := μ) hs (fun _ : Ω => b^n)
    simpa [Set.indicator,f] using hh
  calc
    (∫⁻ ω, ENNReal.ofReal (Real.exp (θ*(C ω).toReal)) ∂μ) ≤
        ∫⁻ ω, 1+b*∑' n, f n ω ∂μ :=
      lintegral_mono (fun ω => exponential_le_weighted_tail (C ω) θ hθ)
    _ = 1+b*∑' n : ℕ, b^n * μ {ω | (n:ℝ≥0∞) < C ω} := by
      rw [lintegral_add_left measurable_const, lintegral_const_mul b hsum,
        lintegral_tsum (fun n => (hf n).aemeasurable)]
      simp only [lintegral_const,measure_univ,mul_one,hi]
    _ ≤ 1+b*∑' n : ℕ, b^n*(A*r^n) := by
      apply add_le_add_left
      apply mul_le_mul_left'
      apply ENNReal.tsum_le_tsum
      intro n
      exact mul_le_mul_left' (htail n) _
    _ = 1+b*A*(1-b*r)⁻¹ := by
      have hh : (fun n : ℕ => b^n*(A*r^n)) = (fun n => A*(b*r)^n) := by
        funext n; rw [mul_pow]; ring
      rw [hh, ENNReal.tsum_mul_left, ENNReal.tsum_geometric]
      ring

theorem geometric_tail_finite_exponential_moment {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (A r : ℝ≥0∞) (hA : A < ⊤) (θ : ℝ) (hθ : 0 ≤ θ)
    (hr : ENNReal.ofReal (Real.exp θ)*r < 1)
    (htail : ∀ n : ℕ, μ {ω | (n:ℝ≥0∞) < C ω} ≤ A*r^n) :
    (∫⁻ ω, ENNReal.ofReal (Real.exp (θ*(C ω).toReal)) ∂μ) < ⊤ := by
  apply lt_of_le_of_lt (exponential_moment_le_geometric_tail μ C hC A r θ hθ htail)
  apply ENNReal.add_lt_top.mpr
  constructor
  · simp
  · apply ENNReal.mul_lt_top
    · exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top hA
    · exact ENNReal.inv_lt_top.mpr (tsub_pos_iff_lt.mpr hr)

/-- Convert the affine confidence tail into a geometric integer-tail envelope.
The probability law and the original confidence inequality are explicit. -/
theorem affine_tail_geometric_envelope {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (C : Ω → ℝ≥0∞)
    (B V : ℝ) (hV : 0 < V)
    (htail : ∀ u : ℝ, 0 ≤ u →
      μ {ω | ENNReal.ofReal (B+V*u) < C ω} ≤ ENNReal.ofReal (Real.exp (-u))) :
    ∀ n : ℕ, μ {ω | (n:ℝ≥0∞) < C ω} ≤
      ENNReal.ofReal (Real.exp (B/V)) * ENNReal.ofReal (Real.exp (-(1/V)))^n := by
  intro n
  have heq : ENNReal.ofReal (Real.exp ((B-(n:ℝ))/V)) =
      ENNReal.ofReal (Real.exp (B/V))*ENNReal.ofReal (Real.exp (-(1/V)))^n := by
    rw [← ENNReal.ofReal_pow (Real.exp_pos _).le,
      ← ENNReal.ofReal_mul (Real.exp_pos _).le,
      ← Real.exp_nat_mul, ← Real.exp_add]
    congr 2
    ring
  rw [← heq]
  by_cases hn : B ≤ (n:ℝ)
  · have hu : 0 ≤ ((n:ℝ)-B)/V := div_nonneg (sub_nonneg.mpr hn) hV.le
    have hh := htail (((n:ℝ)-B)/V) hu
    have ht : B+V*(((n:ℝ)-B)/V) = (n:ℝ) := by field_simp
    rw [ht] at hh
    simpa only [ENNReal.ofReal_natCast, ← neg_div, neg_sub] using hh
  · have hpos : 0 ≤ (B-(n:ℝ))/V := div_nonneg (by linarith) hV.le
    calc
      μ {ω | (n:ℝ≥0∞) < C ω} ≤ 1 := prob_le_one
      _ ≤ _ := by
        have hh : 1 ≤ Real.exp ((B-(n:ℝ))/V) := Real.one_le_exp hpos
        exact_mod_cast ENNReal.ofReal_le_ofReal hh

theorem affine_tail_finite_moments {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (B V : ℝ) (hV : 0 < V)
    (htail : ∀ u : ℝ, 0 ≤ u →
      μ {ω | ENNReal.ofReal (B+V*u) < C ω} ≤ ENNReal.ofReal (Real.exp (-u))) :
    (∫⁻ ω, C ω ∂μ) < ⊤ ∧ (∀ᵐ ω ∂μ, C ω < ⊤) ∧
      ∀ θ : ℝ, 0 ≤ θ → θ < 1/V →
        (∫⁻ ω, ENNReal.ofReal (Real.exp (θ*(C ω).toReal)) ∂μ) < ⊤ := by
  have ht := affine_tail_geometric_envelope μ C B V hV htail
  have hr : ENNReal.ofReal (Real.exp (-(1/V))) < 1 := by
    have he : Real.exp (-(1/V)) < 1 := Real.exp_lt_one_iff.mpr (neg_neg_of_pos (one_div_pos.mpr hV))
    exact_mod_cast (ENNReal.ofReal_lt_ofReal_iff (by norm_num : (0:ℝ)<1)).mpr he
  have hf := geometric_tail_finite_expectation μ C hC
    (ENNReal.ofReal (Real.exp (B/V))) (ENNReal.ofReal (Real.exp (-(1/V))))
    ENNReal.ofReal_lt_top hr ht
  refine ⟨hf, ae_lt_top hC hf.ne, ?_⟩
  intro θ hθ hθV
  apply geometric_tail_finite_exponential_moment μ C hC
    (ENNReal.ofReal (Real.exp (B/V))) (ENNReal.ofReal (Real.exp (-(1/V))))
    ENNReal.ofReal_lt_top θ hθ ?_ ht
  rw [← ENNReal.ofReal_mul (Real.exp_pos _).le, ← Real.exp_add]
  have he : Real.exp (θ + -(1/V)) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
  exact_mod_cast (ENNReal.ofReal_lt_ofReal_iff (by norm_num : (0:ℝ)<1)).mpr he

lemma power_le_scaled_exponential (x θ : ℝ) (hx : 0 ≤ x) (hθ : 0 < θ) (k : ℕ) :
    x^k ≤ ((Nat.factorial k : ℝ)/θ^k)*Real.exp (θ*x) := by
  have hh := Real.pow_div_factorial_le_exp (θ*x) (mul_nonneg hθ.le hx) k
  have hf : (0:ℝ) < (Nat.factorial k : ℝ) := by exact_mod_cast Nat.factorial_pos k
  have hmul := (div_le_iff₀ hf).mp hh
  rw [mul_pow] at hmul
  rw [div_mul_eq_mul_div, le_div_iff₀ (pow_pos hθ k)]
  nlinarith

theorem finite_power_moment_of_positive_exponential_moment
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (hfinite : ∀ᵐ ω ∂μ, C ω < ⊤) (θ : ℝ) (hθ : 0 < θ)
    (hmgf : (∫⁻ ω, ENNReal.ofReal (Real.exp (θ*(C ω).toReal)) ∂μ) < ⊤)
    (k : ℕ) : (∫⁻ ω, (C ω)^k ∂μ) < ⊤ := by
  let K := ENNReal.ofReal ((Nat.factorial k : ℝ)/θ^k)
  have hd : ∀ᵐ ω ∂μ, (C ω)^k ≤ K*ENNReal.ofReal (Real.exp (θ*(C ω).toReal)) := by
    filter_upwards [hfinite] with ω hω
    have hh := ENNReal.ofReal_le_ofReal
      (power_le_scaled_exponential (C ω).toReal θ ENNReal.toReal_nonneg hθ k)
    have hK : 0 ≤ (Nat.factorial k : ℝ)/θ^k := by positivity
    simpa only [ENNReal.ofReal_pow ENNReal.toReal_nonneg,
      ENNReal.ofReal_toReal hω.ne, ENNReal.ofReal_mul hK] using hh
  apply lt_of_le_of_lt (lintegral_mono_ae hd)
  rw [lintegral_const_mul' K _ ENNReal.ofReal_ne_top]
  exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top hmgf

#print axioms power_le_scaled_exponential
#print axioms finite_power_moment_of_positive_exponential_moment
#print axioms affine_tail_finite_moments
#print axioms geometric_tail_finite_exponential_moment
#print axioms affine_tail_geometric_envelope
#print axioms exponential_le_weighted_tail
#print axioms exponential_moment_le_geometric_tail
#print axioms lintegral_le_tail_sum
#print axioms lintegral_le_geometric_tail
#print axioms geometric_tail_finite_expectation
end Orthemology.TailMoments
