import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Tactic
noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators
namespace Orthemology.PolynomialTail

lemma quadratic_cover (z : ℝ≥0∞) (hz : z ≠ ⊤) (K : ℝ) (hK : 0 < K) :
    ∃ n : ℕ, z ≤ ENNReal.ofReal K * ((n+1:ℕ):ℝ≥0∞)^2 := by
  obtain ⟨n,hn⟩ := exists_nat_gt (z.toReal/K)
  refine ⟨n,?_⟩
  have hb : z.toReal < (n:ℝ)*K := (div_lt_iff₀ hK).mp hn
  have hnr : (0:ℝ) ≤ n := by positivity
  have hbound : z.toReal ≤ K*((n:ℝ)+1)^2 := by nlinarith [sq_nonneg (n:ℝ)]
  have hh := ENNReal.ofReal_le_ofReal hbound
  simpa [ENNReal.ofReal_toReal hz, ENNReal.ofReal_mul hK.le,
    ENNReal.ofReal_pow (show 0 ≤ (n:ℝ)+1 by positivity),
    ENNReal.ofReal_add (show 0 ≤ (n:ℝ) by positivity) (by norm_num : (0:ℝ)≤1), Nat.cast_add, Nat.cast_one] using hh

lemma power_le_quadratic_tail_sum (z : ℝ≥0∞) (K : ℝ) (hK : 0 < K)
    (k : ℕ) (hk : 0 < k) :
    z^k ≤ ∑' n : ℕ, if ENNReal.ofReal K*(n:ℝ≥0∞)^2 < z then
      (ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2)^k else 0 := by
  by_cases hz : z = ⊤
  · subst z
    have hKn : ENNReal.ofReal K ≠ 0 := ENNReal.ofReal_ne_zero_iff.mpr hK
    have hh : (∑' _ : ℕ, (ENNReal.ofReal K)^k) ≤
        ∑' n : ℕ, if ENNReal.ofReal K*(n:ℝ≥0∞)^2 < ⊤ then
          (ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2)^k else 0 := by
      apply ENNReal.tsum_le_tsum
      intro n
      have hfin : ENNReal.ofReal K*(n:ℝ≥0∞)^2 < ⊤ := ENNReal.mul_lt_top ENNReal.ofReal_lt_top (ENNReal.pow_lt_top (by simp))
      rw [if_pos hfin]
      apply pow_le_pow_left'
      have hn : (1:ℝ≥0∞) ≤ ((n+1:ℕ):ℝ≥0∞)^2 := by
        norm_cast
        exact Nat.one_le_pow 2 (n+1) (by omega)
      simpa using mul_le_mul_left' hn (ENNReal.ofReal K)
    rw [ENNReal.tsum_const_eq_top_of_ne_zero (pow_ne_zero k hKn)] at hh
    simpa [hk.ne'] using hh
  by_cases hz0 : z = 0
  · subst z; simp [hk.ne']
  have he := quadratic_cover z hz K hK
  let n := Nat.find he
  have hu : z ≤ ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2 := Nat.find_spec he
  have hl : ENNReal.ofReal K*(n:ℝ≥0∞)^2 < z := by
    cases hn : n with
    | zero => simp [hn]; exact bot_lt_iff_ne_bot.mpr hz0
    | succ j =>
      have hj : j < Nat.find he := by change j<n; omega
      have hnot := Nat.find_min he hj
      exact lt_of_not_ge (by simpa [← hn] using hnot)
  have ht := ENNReal.le_tsum n (f := fun j : ℕ =>
    if ENNReal.ofReal K*(j:ℝ≥0∞)^2 < z then
      (ENNReal.ofReal K*((j+1:ℕ):ℝ≥0∞)^2)^k else 0)
  rw [if_pos hl] at ht
  exact (pow_le_pow_left' hu k).trans ht

theorem integral_power_le_quadratic_tails {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (K : ℝ) (hK : 0 < K) (k : ℕ) (hk : 0 < k) :
    (∫⁻ ω, (C ω)^k ∂μ) ≤ ∑' n : ℕ,
      (ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2)^k *
        μ {ω | ENNReal.ofReal K*(n:ℝ≥0∞)^2 < C ω} := by
  let f : ℕ → Ω → ℝ≥0∞ := fun n ω =>
    if ENNReal.ofReal K*(n:ℝ≥0∞)^2 < C ω then
      (ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2)^k else 0
  have hf : ∀ n, Measurable (f n) := fun n =>
    Measurable.ite (measurableSet_lt measurable_const hC) measurable_const measurable_const
  calc
    (∫⁻ ω, (C ω)^k ∂μ) ≤ ∫⁻ ω, ∑' n, f n ω ∂μ :=
      lintegral_mono (fun ω => power_le_quadratic_tail_sum (C ω) K hK k hk)
    _ = ∑' n, ∫⁻ ω, f n ω ∂μ := lintegral_tsum (fun n => (hf n).aemeasurable)
    _ = _ := by
      apply tsum_congr
      intro n
      have hs : MeasurableSet {ω | ENNReal.ofReal K*(n:ℝ≥0∞)^2 < C ω} :=
        measurableSet_lt measurable_const hC
      simpa [Set.indicator,f] using lintegral_indicator_const (μ := μ) hs
        ((ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2)^k)

lemma summable_shifted_power_geometric (k : ℕ) (ρ : ℝ) (hρ : 0 < ρ) (hρ1 : ρ < 1) :
    Summable (fun n : ℕ => ((n:ℝ)+1)^k * ρ^n) := by
  have hs := summable_pow_mul_geometric_of_norm_lt_one k
    (show ‖ρ‖ < 1 by simpa [Real.norm_eq_abs,abs_of_pos hρ] using hρ1)
  have ht := (summable_nat_add_iff 1).mpr hs
  have hm := ht.mul_left (ρ⁻¹)
  apply hm.congr
  intro n
  simp only [Nat.cast_add,Nat.cast_one,pow_succ]
  field_simp
  ring

lemma summable_quadratic_envelope (K A L ρ : ℝ) (k : ℕ)
    (hρ : 0 < ρ) (hρ1 : ρ < 1) :
    Summable (fun n : ℕ => (K*((n:ℝ)+1)^2)^k * (A+L*((n:ℝ)+1))*ρ^n) := by
  have h₁ := (summable_shifted_power_geometric (2*k) ρ hρ hρ1).mul_left (K^k*A)
  have h₂ := (summable_shifted_power_geometric (2*k+1) ρ hρ hρ1).mul_left (K^k*L)
  apply (h₁.add h₂).congr
  intro n
  simp only [mul_pow,pow_mul,pow_add,pow_one]
  ring

/-- A quadratic threshold with polynomial-times-geometric failure probability
implies every finite power moment, without assuming the cost is finite a.s. -/
theorem quadratic_geometric_tail_all_moments
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (K A L ρ : ℝ) (hK : 0 < K) (hA : 0 ≤ A) (hL : 0 ≤ L)
    (hρ : 0 < ρ) (hρ1 : ρ < 1)
    (htail : ∀ n : ℕ, 1 ≤ n →
      μ {ω | ENNReal.ofReal K*(n:ℝ≥0∞)^2 < C ω} ≤
        ENNReal.ofReal ((A+L*((n:ℝ)+1))*ρ^n)) :
    ∀ k : ℕ, (∫⁻ ω, (C ω)^k ∂μ) < ⊤ := by
  intro k
  by_cases hk : k=0
  · subst k; simp
  have hkp : 0<k := Nat.pos_of_ne_zero hk
  have hall : ∀ n : ℕ,
      μ {ω | ENNReal.ofReal K*(n:ℝ≥0∞)^2 < C ω} ≤
        ENNReal.ofReal ((A+1+L*((n:ℝ)+1))*ρ^n) := by
    intro n
    cases n with
    | zero =>
      calc
        _ ≤ 1 := prob_le_one
        _ ≤ _ := by
          have hh : (1:ℝ) ≤ (A+1+L*((0:ℝ)+1))*ρ^0 := by simp; linarith
          exact_mod_cast ENNReal.ofReal_le_ofReal hh
    | succ n =>
      apply (htail (n+1) (by omega)).trans
      apply ENNReal.ofReal_le_ofReal
      have hp : 0 ≤ ρ^(n+1) := pow_nonneg hρ.le _
      nlinarith
  let term : ℕ → ℝ := fun n => (K*((n:ℝ)+1)^2)^k * (A+1+L*((n:ℝ)+1))*ρ^n
  have hn : ∀ n, 0 ≤ term n := by intro n; dsimp [term]; positivity
  have hs : Summable term := summable_quadratic_envelope K (A+1) L ρ k hρ hρ1
  have hb : ∀ n : ℕ,
      (ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2)^k *
        μ {ω | ENNReal.ofReal K*(n:ℝ≥0∞)^2 < C ω} ≤ ENNReal.ofReal (term n) := by
    intro n
    apply (mul_le_mul_left' (hall n) _).trans_eq
    have hbase : 0 ≤ K*((n:ℝ)+1)^2 := by positivity
    have hval : ENNReal.ofReal (K*((n:ℝ)+1)^2) =
        ENNReal.ofReal K*((n+1:ℕ):ℝ≥0∞)^2 := by
      rw [ENNReal.ofReal_mul hK.le, ENNReal.ofReal_pow (by positivity)]
      congr 2
      have hcast : ((n:ℝ)+1) = ((n+1:ℕ):ℝ) := by simp
      rw [hcast,ENNReal.ofReal_natCast]
    rw [← hval, ← ENNReal.ofReal_pow hbase,
      ← ENNReal.ofReal_mul (pow_nonneg hbase k)]
    congr 1
    dsimp [term]
    ring
  apply lt_of_le_of_lt ((integral_power_le_quadratic_tails μ C hC K hK k hkp).trans
    (ENNReal.tsum_le_tsum hb))
  rw [← ENNReal.ofReal_tsum_of_nonneg hn hs]
  exact ENNReal.ofReal_lt_top

/-- Direct consequence of the cutoff-plus-union tail used for the actual
controller. No independence of a future cutoff event is assumed here. -/
theorem cutoff_union_tail_all_moments
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (C : Ω → ℝ≥0∞) (hC : Measurable C)
    (D α β A c r : ℝ) (hD : 0 < D) (hα : 0 ≤ α) (hβ : 0 ≤ β)
    (hαβ : 0 < α+β) (hA : 0 ≤ A) (hc : 0 < c) (hr : 0 < r) (hr1 : r ≤ 1)
    (htail : ∀ N k : ℕ, 1 ≤ N → 1 ≤ k →
      μ {ω | ENNReal.ofReal (D*(k:ℝ)*(α*(N:ℝ)+β)) < C ω} ≤
        ENNReal.ofReal (A*Real.exp (-c*(N:ℝ))+(α*(N:ℝ)+β)*(1-r)^k)) :
    ∀ k : ℕ, (∫⁻ ω, (C ω)^k ∂μ) < ⊤ := by
  let K := D*(α+β)
  let ρ := max (Real.exp (-c)) (1-r)
  have hK : 0 < K := mul_pos hD hαβ
  have hρ : 0 < ρ := (Real.exp_pos (-c)).trans_le (le_max_left _ _)
  have hρ1 : ρ < 1 := max_lt (Real.exp_lt_one_iff.mpr (by linarith)) (by linarith)
  apply quadratic_geometric_tail_all_moments μ C hC K A (α+β) ρ hK hA hαβ.le hρ hρ1
  intro n hn
  have hnreal : (1:ℝ) ≤ n := by exact_mod_cast hn
  have hn0 : (0:ℝ) ≤ n := by positivity
  have hthreshold : D*(n:ℝ)*(α*(n:ℝ)+β) ≤ K*(n:ℝ)^2 := by
    dsimp [K]
    have hnn : (n:ℝ) ≤ (n:ℝ)^2 := by nlinarith
    have hh := mul_le_mul_of_nonneg_left hnn hβ
    have hd := mul_le_mul_of_nonneg_left hh hD.le
    nlinarith
  have hsets : {ω | ENNReal.ofReal K*(n:ℝ≥0∞)^2 < C ω} ⊆
      {ω | ENNReal.ofReal (D*(n:ℝ)*(α*(n:ℝ)+β)) < C ω} := by
    intro ω hω
    have he := ENNReal.ofReal_le_ofReal hthreshold
    rw [ENNReal.ofReal_mul hK.le, ENNReal.ofReal_pow hn0,ENNReal.ofReal_natCast] at he
    exact he.trans_lt hω
  apply ((measure_mono hsets).trans (htail n n hn hn)).trans
  apply ENNReal.ofReal_le_ofReal
  have hp₁ : Real.exp (-c*(n:ℝ)) ≤ ρ^n := by
    rw [mul_comm (-c) (n:ℝ), Real.exp_nat_mul]
    exact pow_le_pow_left₀ (Real.exp_pos _).le (le_max_left _ _) n
  have hp₂ : (1-r)^n ≤ ρ^n :=
    pow_le_pow_left₀ (by linarith) (le_max_right _ _) n
  have hcoef : α*(n:ℝ)+β ≤ (α+β)*((n:ℝ)+1) := by
    nlinarith [mul_nonneg hβ hn0]
  have hb : 0 ≤ α*(n:ℝ)+β := by positivity
  have ht₁ := mul_le_mul_of_nonneg_left hp₁ hA
  have ht₂ := mul_le_mul hp₂ hcoef hb (pow_nonneg hρ.le n)
  nlinarith

#print axioms cutoff_union_tail_all_moments
#print axioms quadratic_geometric_tail_all_moments
#print axioms integral_power_le_quadratic_tails
#print axioms summable_shifted_power_geometric
#print axioms summable_quadratic_envelope
#print axioms power_le_quadratic_tail_sum
end Orthemology.PolynomialTail
