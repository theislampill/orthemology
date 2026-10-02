import RawExponentialTail

noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Exponential
open HiddenParity.Empirical
universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

lemma rawTailDeviation_mono_tolerance (P : A → Y → ℝ) (N : ℕ) {η θ : ℝ}
    (h : θ ≤ η) : RawTailDeviation (R := R) P η N ⊆ RawTailDeviation P θ N := by
  rintro z ⟨a,y,n,hn,hz⟩
  exact ⟨a,y,n,hn,h.trans hz⟩

/-- The same derived tail bound for every positive tolerance. Only the rate is
clamped; neither the original bad event nor the controller tolerance changes. -/
theorem seeded_rawTailDeviation_exponential_all_positive
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (N : ℕ) (hNpos : 0 < N) {η : ℝ} (hη : 0 < η) :
    (ρ.prod (stackMeasure P hP hN)) (RawTailDeviation (R := R) P η N) ≤
      ENNReal.ofReal ((Fintype.card A : ℝ) * (Fintype.card Y : ℝ) *
        (2 * Real.exp (-(N:ℝ)*((min η 1)^2/2)) / (1-Real.exp (-((min η 1)^2/2))))) := by
  have hcap : 0 < min η 1 := lt_min hη (by norm_num)
  exact (measure_mono (rawTailDeviation_mono_tolerance P N (min_le_left η 1))).trans
    (seeded_rawTailDeviation_exponential ρ P hP hN N hNpos hcap (min_le_right η 1))

#print axioms seeded_rawTailDeviation_exponential_all_positive
end HiddenParity.Exponential
