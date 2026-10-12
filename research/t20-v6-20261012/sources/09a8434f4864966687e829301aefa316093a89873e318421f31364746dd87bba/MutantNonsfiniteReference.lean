import CountableIdentification
import Mathlib.MeasureTheory.Measure.Count
open MeasureTheory
-- This use MUST be rejected: uncountable counting measure is not s-finite.
example : Set.Countable {a : ℝ | 0 < (Measure.dirac a) {a}} := by
  apply Orthemology.Tranche2.countable_positive_exact_identification
    (Measure.count : Measure ℝ) (fun a : ℝ => Measure.dirac a) id measurable_id
    (fun a : ℝ => {a}) (by intro a; simp)
  intro a s hs
  have he : s = ∅ := Measure.count_eq_zero_iff.mp hs
  simp [he]
