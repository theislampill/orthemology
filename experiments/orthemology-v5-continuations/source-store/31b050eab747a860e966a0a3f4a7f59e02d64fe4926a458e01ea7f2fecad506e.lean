import Mathlib.MeasureTheory.Integral.MeanInequalities
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.Tactic

/-! A reusable cost-transfer lemma. Shells need not be stopping events and no
conditional iid or independence premise is present. The full stopped second
moment and shell probability remain explicit hypotheses. -/
noncomputable section
open MeasureTheory
open scoped ENNReal
namespace HiddenParity.Cost
variable {Ω : Type*} [MeasurableSpace Ω]

/-- Cauchy–Schwarz on an arbitrary measurable event, stated for extended
nonnegative costs so finiteness is not smuggled into the input type. -/
theorem set_lintegral_le_sqrt_second_moment (μ : Measure Ω)
    (f : Ω → ℝ≥0∞) (hf : AEMeasurable f μ)
    (s : Set Ω) (hs : MeasurableSet s) :
    (∫⁻ ω in s, f ω ∂μ) ≤
      (∫⁻ ω, f ω ^ 2 ∂μ) ^ (1 / 2 : ℝ) * (μ s) ^ (1 / 2 : ℝ) := by
  let g : Ω → ℝ≥0∞ := s.indicator (fun _ => 1)
  have hg : Measurable g := measurable_const.indicator hs
  have hconj : (2 : ℝ).HolderConjugate 2 := by
    apply Real.holderConjugate_iff.mpr
    norm_num
  have h := ENNReal.lintegral_mul_le_Lp_mul_Lq μ hconj hf hg.aemeasurable
  have hprod : f * g = s.indicator f := by
    funext ω
    by_cases hω : ω ∈ s <;> simp [g,hω]
  have hg2 : (fun ω => g ω ^ (2 : ℝ)) = g := by
    funext ω
    by_cases hω : ω ∈ s <;> simp [g,hω]
  rw [hprod,lintegral_indicator hs, hg2] at h
  simpa only [g,lintegral_indicator hs,lintegral_const,one_mul,
    Measure.restrict_apply_univ,ENNReal.rpow_two] using h

/-- Shell gluing with no independence assumptions. Each shell may come from a
non-stopping last-error index; only a.e. coverage and pointwise agreement with
an individually measurable stopped cost are required. -/
theorem shell_cost_transfer (μ : Measure Ω) (cost : Ω → ℝ≥0∞)
    (stopped : ℕ → Ω → ℝ≥0∞) (shell : ℕ → Set Ω)
    (hm : ∀ n, MeasurableSet (shell n))
    (hf : ∀ n, AEMeasurable (stopped n) μ)
    (hcover : ∀ᵐ ω ∂μ, ω ∈ ⋃ n, shell n)
    (hdom : ∀ n, ∀ ω ∈ shell n, cost ω ≤ stopped n ω) :
    (∫⁻ ω, cost ω ∂μ) ≤ ∑' n,
      (∫⁻ ω, stopped n ω ^ 2 ∂μ) ^ (1 / 2 : ℝ) * (μ (shell n)) ^ (1 / 2 : ℝ) := by
  have hrestrict : μ.restrict (⋃ n, shell n) = μ :=
    Measure.restrict_eq_self_of_ae_mem hcover
  calc
    (∫⁻ ω, cost ω ∂μ) = ∫⁻ ω in ⋃ n, shell n, cost ω ∂μ := by rw [hrestrict]
    _ ≤ ∑' n, ∫⁻ ω in shell n, cost ω ∂μ := lintegral_iUnion_le shell cost
    _ ≤ ∑' n, ∫⁻ ω in shell n, stopped n ω ∂μ := by
      apply ENNReal.tsum_le_tsum
      intro n
      exact setLIntegral_mono' (hm n) (hdom n)
    _ ≤ _ := by
      apply ENNReal.tsum_le_tsum
      intro n
      exact set_lintegral_le_sqrt_second_moment μ (stopped n) (hf n) (shell n) (hm n)

/-- The usable finiteness conclusion retains the exact summability obligation. -/
theorem shell_cost_finite (μ : Measure Ω) (cost : Ω → ℝ≥0∞)
    (stopped : ℕ → Ω → ℝ≥0∞) (shell : ℕ → Set Ω)
    (hm : ∀ n, MeasurableSet (shell n)) (hf : ∀ n, AEMeasurable (stopped n) μ)
    (hcover : ∀ᵐ ω ∂μ, ω ∈ ⋃ n, shell n)
    (hdom : ∀ n, ∀ ω ∈ shell n, cost ω ≤ stopped n ω)
    (hfinite : (∑' n, (∫⁻ ω, stopped n ω ^ 2 ∂μ) ^ (1 / 2 : ℝ) *
      (μ (shell n)) ^ (1 / 2 : ℝ)) < ⊤) : (∫⁻ ω, cost ω ∂μ) < ⊤ :=
  lt_of_le_of_lt (shell_cost_transfer μ cost stopped shell hm hf hcover hdom) hfinite

end HiddenParity.Cost
