import StackActionLaw
import Mathlib.Probability.StrongLaw

noncomputable section
open MeasureTheory ProbabilityTheory Filter Set
open scoped BigOperators ENNReal Topology
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Empirical
universe u v
variable {A Y : Type u} {R : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- A genuine observed-symbol indicator, not a supplied empirical estimate. -/
def symbolIndicator (y t : Y) : ℝ := by
  classical
  exact if t = y then 1 else 0

/-- Frequency among the first n cells of a particular raw tape. At zero it is 0. -/
def rawFrequency (a : A) (y : Y) (n : ℕ) (z : R × FlatStack A Y) : ℝ :=
  (∑ i ∈ Finset.range n, symbolIndicator y (seededStackCoordinate a i z)) / n

omit [Fintype A] [DecidableEq A] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
lemma rawFrequency_measurable (a : A) (y : Y) (n : ℕ) :
    Measurable (rawFrequency (R := R) a y n) := by
  apply Measurable.div_const
  exact Finset.measurable_sum _ (fun i _ =>
    (measurable_of_finite (symbolIndicator y)).comp (seededStackCoordinate_measurable a i))

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
lemma seeded_symbol_integrable
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (y : Y) (n : ℕ) :
    Integrable (fun z : R × FlatStack A Y => symbolIndicator y (seededStackCoordinate a n z))
      (ρ.prod (stackMeasure P hP hN)) := by
  classical
  have he : (fun z : R × FlatStack A Y => symbolIndicator y (seededStackCoordinate a n z)) =
      Set.indicator {z | seededStackCoordinate a n z = y} (fun _ => (1 : ℝ)) := by
    funext z
    simp [symbolIndicator, Set.indicator_apply]
  rw [he]
  exact (integrable_const (1 : ℝ)).indicator
    ((measurableSet_singleton y).preimage (seededStackCoordinate_measurable a n))

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
lemma seeded_symbol_integral
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (y : Y) (n : ℕ) :
    (∫ z : R × FlatStack A Y, symbolIndicator y (seededStackCoordinate a n z)
      ∂ρ.prod (stackMeasure P hP hN)) = P a y := by
  classical
  have hm : MeasurableSet {z : R × FlatStack A Y | seededStackCoordinate a n z = y} :=
    (measurableSet_singleton y).preimage (seededStackCoordinate_measurable (R := R) a n)
  have he : (fun z : R × FlatStack A Y => symbolIndicator y (seededStackCoordinate a n z)) =
      Set.indicator {z | seededStackCoordinate a n z = y} (fun _ => (1 : ℝ)) := by
    funext z
    simp [symbolIndicator, Set.indicator_apply]
  rw [he, integral_indicator_const (1 : ℝ) hm]
  simp only [smul_eq_mul, mul_one]
  change ((ρ.prod (stackMeasure P hP hN)) (seededStackCoordinate a n ⁻¹' {y})).toReal = _
  rw [← Measure.map_apply (seededStackCoordinate_measurable a n) (measurableSet_singleton y),
    seededStackCoordinate_law ρ P hP hN, actionMeasure_singleton,
    ENNReal.toReal_ofReal (hP a y)]

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- Strong consistency derived from the actual product coordinates and their
exact laws. Independence and convergence are conclusions of imported theorems,
not additional premises about samples taken at random policy counts. -/
theorem seeded_rawFrequency_tendsto
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (y : Y) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN),
      Tendsto (fun n => rawFrequency a y n z) atTop (𝓝 (P a y)) := by
  let X : ℕ → (R × FlatStack A Y) → ℝ :=
    fun n z => symbolIndicator y (seededStackCoordinate a n z)
  have hf : Measurable (symbolIndicator y) := measurable_of_finite _
  have hcoords := (seededStackCoordinates_independent ρ P hP hN).precomp
    (show Function.Injective (fun n : ℕ => (a,n)) from fun _ _ h => congrArg Prod.snd h)
  have hi : Pairwise (fun n m => IndepFun (X n) (X m) (ρ.prod (stackMeasure P hP hN))) := by
    intro n m hnm
    exact (hcoords.indepFun hnm).comp hf hf
  have hd : ∀ n, IdentDistrib (X n) (X 0)
      (ρ.prod (stackMeasure P hP hN)) (ρ.prod (stackMeasure P hP hN)) := by
    intro n
    exact (seededStackCoordinates_identDistrib ρ P hP hN a n 0).comp hf
  have h := strong_law_ae_real X (seeded_symbol_integrable ρ P hP hN a y 0) hi hd
  rw [show (∫ z, X 0 z ∂ρ.prod (stackMeasure P hP hN)) = P a y from
    seeded_symbol_integral ρ P hP hN a y 0] at h
  exact h

omit [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] in
/-- One probability-one event controls every finite pair and every symbol. -/
theorem seeded_all_rawFrequencies_tendsto
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    ∀ᵐ z ∂ρ.prod (stackMeasure P hP hN),
      ∀ a y, Tendsto (fun n => rawFrequency a y n z) atTop (𝓝 (P a y)) := by
  exact ae_all_iff.mpr (fun a => ae_all_iff.mpr (fun y =>
    seeded_rawFrequency_tendsto ρ P hP hN a y))

end HiddenParity.Empirical
