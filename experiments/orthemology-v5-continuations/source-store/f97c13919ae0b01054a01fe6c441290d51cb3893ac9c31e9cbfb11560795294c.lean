import Mathlib.Probability.StrongLaw
import Mathlib.InformationTheory.KullbackLeibler.KLFun
import Mathlib.Tactic

/-!
# Finite-alphabet iid log-likelihood drift

The distribution hypotheses concern the actual finite observation variables.
Positive drift and almost-sure convergence are derived, not supplied as an endpoint.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Filter Finset
open scoped Topology

namespace Orthemology.Tranche2

variable {Y Ω : Type*} [Fintype Y]

/-- Log likelihood in favour of the true law `p` against a candidate `q`. -/
def logScore (p q : Y → ℝ) (y : Y) : ℝ := Real.log (p y / q y)

def finiteKL (p q : Y → ℝ) : ℝ := ∑ y, p y * logScore p q y

lemma finiteKL_eq_sum_klFun (p q : Y → ℝ)
    (hq : ∀ y, 0 < q y)
    (hpsum : ∑ y, p y = 1) (hqsum : ∑ y, q y = 1) :
    finiteKL p q = ∑ y, q y * InformationTheory.klFun (p y / q y) := by
  have hpoint : ∀ y, p y * logScore p q y =
      q y * InformationTheory.klFun (p y / q y) + p y - q y := by
    intro y
    unfold logScore InformationTheory.klFun
    field_simp [ne_of_gt (hq y)]
  unfold finiteKL
  simp_rw [hpoint]
  rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, hpsum, hqsum]
  ring

lemma finiteKL_nonneg (p q : Y → ℝ)
    (hp : ∀ y, 0 < p y) (hq : ∀ y, 0 < q y)
    (hpsum : ∑ y, p y = 1) (hqsum : ∑ y, q y = 1) :
    0 ≤ finiteKL p q := by
  rw [finiteKL_eq_sum_klFun p q hq hpsum hqsum]
  exact Finset.sum_nonneg (fun y _ => mul_nonneg (hq y).le
    (InformationTheory.klFun_nonneg (div_nonneg (hp y).le (hq y).le)))

lemma finiteKL_pos (p q : Y → ℝ)
    (hp : ∀ y, 0 < p y) (hq : ∀ y, 0 < q y)
    (hpsum : ∑ y, p y = 1) (hqsum : ∑ y, q y = 1)
    (hne : p ≠ q) : 0 < finiteKL p q := by
  classical
  obtain ⟨y, hy⟩ : ∃ y, p y ≠ q y := by
    by_contra! h
    exact hne (funext h)
  rw [finiteKL_eq_sum_klFun p q hq hpsum hqsum]
  have hz : InformationTheory.klFun (p y / q y) ≠ 0 := by
    intro heq
    have hone := (InformationTheory.klFun_eq_zero_iff
      (div_nonneg (hp y).le (hq y).le)).mp heq
    exact hy ((div_eq_one_iff_eq (ne_of_gt (hq y))).mp hone)
  have hpos : 0 < InformationTheory.klFun (p y / q y) :=
    lt_of_le_of_ne (InformationTheory.klFun_nonneg
      (div_nonneg (hp y).le (hq y).le)) (Ne.symm hz)
  exact Finset.sum_pos' (fun z _ => mul_nonneg (hq z).le
    (InformationTheory.klFun_nonneg (div_nonneg (hp z).le (hq z).le)))
    ⟨y, Finset.mem_univ _, mul_pos (hq y) hpos⟩

omit [Fintype Y] in
lemma logScore_self (p : Y → ℝ) (hp : ∀ y, 0 < p y) (y : Y) :
    logScore p p y = 0 := by
  simp [logScore, ne_of_gt (hp y)]

section ObservationLaw

variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]

lemma logScore_integrable_comp (p q : Y → ℝ) (X : Ω → Y) (hX : Measurable X) :
    Integrable (fun ω => logScore p q (X ω)) μ := by
  have hi : Integrable (logScore p q) (Measure.map X μ) := Integrable.of_finite
  exact hi.comp_measurable hX

lemma logScore_expectation (p q : Y → ℝ) (X : Ω → Y) (hX : Measurable X)
    (hLaw : ∀ y, (Measure.map X μ).real {y} = p y) :
    (∫ ω, logScore p q (X ω) ∂μ) = finiteKL p q := by
  rw [← integral_map hX.aemeasurable (measurable_of_countable (logScore p q)).aestronglyMeasurable]
  rw [integral_fintype _ Integrable.of_finite]
  simp [finiteKL, hLaw, smul_eq_mul]

/-- Strong law for the actual finite-alphabet log-likelihood observations. -/
theorem logScore_strong_law (p q : Y → ℝ) (X : ℕ → Ω → Y)
    (hX : ∀ n, Measurable (X n))
    (hindep : Pairwise (fun i j => IndepFun (X i) (X j) μ))
    (hident : ∀ n, IdentDistrib (X n) (X 0) μ μ)
    (hLaw : ∀ y, (Measure.map (X 0) μ).real {y} = p y) :
    ∀ᵐ ω ∂μ, Tendsto
      (fun n : ℕ => (∑ i ∈ Finset.range n, logScore p q (X i ω)) / n)
      atTop (𝓝 (finiteKL p q)) := by
  have hm : Measurable (logScore p q) := measurable_of_countable _
  have hs := strong_law_ae_real (fun n ω => logScore p q (X n ω))
    (logScore_integrable_comp p q (X 0) (hX 0))
    (fun i j hij => (hindep hij).comp hm hm)
    (fun n => (hident n).comp hm)
  simpa only [logScore_expectation p q (X 0) (hX 0) hLaw] using hs

/-- Positive empirical mean forces the unnormalized partial sums to infinity. -/
lemma sums_tendsto_atTop_of_average {s : ℕ → ℝ} {c : ℝ}
    (hc : 0 < c) (h : Tendsto (fun n : ℕ => s n / n) atTop (𝓝 c)) :
    Tendsto s atTop atTop := by
  have hn : Tendsto (fun n : ℕ => (n : ℝ)) atTop atTop := tendsto_natCast_atTop_atTop
  have hm := h.pos_mul_atTop hc hn
  apply hm.congr'
  filter_upwards [eventually_gt_atTop (0 : ℕ)] with n hn
  exact div_mul_cancel₀ (s n) (by exact_mod_cast (Nat.ne_of_gt hn))

/-- The actual true-vs-false log likelihood diverges almost surely. -/
theorem logScore_sum_tendsto_atTop (p q : Y → ℝ) (X : ℕ → Ω → Y)
    (hp : ∀ y, 0 < p y) (hq : ∀ y, 0 < q y)
    (hpsum : ∑ y, p y = 1) (hqsum : ∑ y, q y = 1) (hne : p ≠ q)
    (hX : ∀ n, Measurable (X n))
    (hindep : Pairwise (fun i j => IndepFun (X i) (X j) μ))
    (hident : ∀ n, IdentDistrib (X n) (X 0) μ μ)
    (hLaw : ∀ y, (Measure.map (X 0) μ).real {y} = p y) :
    ∀ᵐ ω ∂μ, Tendsto
      (fun n : ℕ => ∑ i ∈ Finset.range n, logScore p q (X i ω)) atTop atTop := by
  filter_upwards [logScore_strong_law p q X hX hindep hident hLaw] with ω hω
  exact sums_tendsto_atTop_of_average (finiteKL_pos p q hp hq hpsum hqsum hne) hω

end ObservationLaw

end Orthemology.Tranche2
