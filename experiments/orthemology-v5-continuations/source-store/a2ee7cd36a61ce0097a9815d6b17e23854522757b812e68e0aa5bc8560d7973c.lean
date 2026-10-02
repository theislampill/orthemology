import P02A2.FiniteLaw
import P02A2.MeasureCore
import Mathlib

/-! UNEXECUTED. General finite rational distributions, their actual Measure
interpretation, and deterministic/stochastic transport. No uniformity premise
is inferred from a bare unnormalised list. -/
namespace P02A2.FiniteMeasureBridge
open Set MeasureTheory
open scoped BigOperators
open P02A2.FiniteLaw
variable {X Y : Type*} [Fintype X] [Fintype Y]

noncomputable def bind (p : Law X) (K : X → Law Y) : Law Y where
  weight y := ∑ x, p.weight x * (K x).weight y
  nonneg y := Finset.sum_nonneg (fun x _ => mul_nonneg (p.nonneg x) ((K x).nonneg y))
  total := by
    rw [Finset.sum_comm]
    simp_rw [← Finset.mul_sum, fun x => (K x).total, mul_one]
    exact p.total

theorem bind_event (p : Law X) (K : X → Law Y) (A : Y → Prop) :
    event (bind p K) A = ∑ x, p.weight x * event (K x) A := by
  classical
  unfold event bind
  have hswap : (∑ y : Y, if A y then ∑ x : X,
      p.weight x * (K x).weight y else 0) =
      ∑ y : Y, ∑ x : X, if A y then p.weight x * (K x).weight y else 0 := by
    apply Finset.sum_congr rfl
    intro y hy
    by_cases h : A y <;> simp [h]
  rw [hswap, Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro x hx
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro y hy
  split_ifs <;> ring

variable [MeasurableSpace X] [MeasurableSpace Y]

noncomputable def toMeasure (p : Law X) : Measure X :=
  Measure.sum (fun x => ENNReal.ofReal (p.weight x : ℝ) • Measure.dirac x)

theorem toMeasure_apply (p : Law X) {A : Set X} (hA : MeasurableSet A) :
    toMeasure p A = ENNReal.ofReal (event p (fun x => x ∈ A) : ℝ) := by
  classical
  unfold toMeasure event
  rw [Measure.sum_apply _ hA, tsum_fintype]
  have hn : ∀ x ∈ (Finset.univ : Finset X),
      0 ≤ (if x ∈ A then (p.weight x : ℝ) else 0) := by
    intro x hx
    split_ifs
    · exact_mod_cast p.nonneg x
    · exact le_rfl
  push_cast
  simp only [apply_ite (fun q : ℚ => (q : ℝ)), Rat.cast_zero]
  rw [ENNReal.ofReal_sum_of_nonneg hn]
  apply Finset.sum_congr rfl
  intro x hx
  change ENNReal.ofReal (p.weight x : ℝ) * Measure.dirac x A = _
  rw [Measure.dirac_apply' x hA]
  by_cases h : x ∈ A <;> simp [h]

theorem toMeasure_total (p : Law X) : toMeasure p univ = 1 := by
  rw [toMeasure_apply p MeasurableSet.univ]
  have he : event p (fun x => x ∈ (univ : Set X)) = 1 := by simpa [event] using p.total
  rw [he]
  norm_num

instance toMeasure_probability (p : Law X) : IsProbabilityMeasure (toMeasure p) :=
  ⟨toMeasure_total p⟩

theorem toMeasure_push (p : Law X) {f : X → Y} (hf : Measurable f) :
    toMeasure (push p f) = (toMeasure p).map f := by
  apply Measure.ext
  intro A hA
  rw [toMeasure_apply (push p f) hA, Measure.map_apply hf hA,
    toMeasure_apply p (hA.preimage hf), push_event]
  rfl

theorem toMeasure_bind_event (p : Law X) (K : X → Law Y) {A : Set Y}
    (hA : MeasurableSet A) :
    toMeasure (bind p K) A =
      ENNReal.ofReal ((∑ x, p.weight x * event (K x) (fun y => y ∈ A) : ℚ) : ℝ) := by
  rw [toMeasure_apply (bind p K) hA, bind_event]

variable [MeasurableSingletonClass X]

theorem finite_law_zero_defect (p : Law X) : defect (toMeasure p) = 0 := by
  have hm : mass (toMeasure p) = 1 := countable_carrier_mass_one (toMeasure p)
    (Set.to_countable (univ : Set X)) (by simp) (toMeasure_total p)
  simp [defect, hm]
end P02A2.FiniteMeasureBridge
