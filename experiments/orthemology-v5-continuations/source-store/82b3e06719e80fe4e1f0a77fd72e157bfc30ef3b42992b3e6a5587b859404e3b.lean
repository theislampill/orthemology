import RawWordLaw
import EmpiricalGeometry

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Exponential
open HiddenParity.Empirical CentredBernoulli BernoulliWord EmpiricalGeometry
universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

lemma empiricalMean_symbolWord (a : A) (y : Y) (n : ℕ) (z : R × FlatStack A Y) :
    empiricalMean n (symbolWord a y n z) = rawFrequency a y n z := by
  classical
  unfold empiricalMean rawFrequency
  congr 1
  simp only [symbolWord, decide_eq_true_eq]
  simp only [symbolIndicator]
  exact Fin.sum_univ_eq_sum_range (fun i : ℕ =>
    if seededStackCoordinate a i z = y then (1:ℝ) else 0) n

lemma word_deviation_probability (n : ℕ) {p η : ℝ} (hp : 0 ≤ p) (hp1 : p ≤ 1) :
    (distribution n p hp hp1).toMeasure {w | (n:ℝ)*η ≤ |centredSum n p w|} =
      ENNReal.ofReal (realDeviation n p η) := by
  classical
  rw [PMF.toMeasure_apply_fintype]
  unfold realDeviation
  rw [ENNReal.ofReal_sum_of_nonneg (by
    intro w _
    apply mul_nonneg (realWeight_nonneg n hp hp1 w)
    split <;> norm_num)]
  apply Finset.sum_congr rfl
  intro w _
  by_cases h : (n:ℝ)*η ≤ |centredSum n p w|
  · simp [Set.indicator_apply,h,weight_eq_ofReal]
  · simp [Set.indicator_apply,h]

/-- Exponential concentration at a deterministic raw-tape prefix, derived from
its actual product law. No independence at random acquired counts is assumed. -/
theorem seeded_rawFrequency_exponential
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (y : Y) (n : ℕ) (hn : 0 < n) {η : ℝ} (hη : 0 ≤ η) (hη1 : η ≤ 1) :
    (ρ.prod (stackMeasure P hP hN)) {z | η ≤ |rawFrequency a y n z - P a y|} ≤
      ENNReal.ofReal (2 * Real.exp (-((n:ℝ)*η^2/2))) := by
  have hnpos : (0:ℝ) < n := by exact_mod_cast hn
  have he : {z : R × FlatStack A Y | η ≤ |rawFrequency a y n z - P a y|} =
      symbolWord a y n ⁻¹' {w | (n:ℝ)*η ≤ |centredSum n (P a y) w|} := by
    ext z
    simp only [Set.mem_setOf_eq,Set.mem_preimage]
    rw [centredSum_eq n hn, empiricalMean_symbolWord,abs_mul,abs_of_pos hnpos]
    exact (mul_le_mul_left hnpos).symm
  rw [he, ← Measure.map_apply (symbolWord_measurable a y n) ((Set.toFinite _).measurableSet),
    symbolWord_law,word_deviation_probability]
  exact ENNReal.ofReal_le_ofReal (realDeviation_le n (hP a y)
    (row_probability_le_one P hP hN a y) hη hη1)

#print axioms seeded_rawFrequency_exponential
end HiddenParity.Exponential
