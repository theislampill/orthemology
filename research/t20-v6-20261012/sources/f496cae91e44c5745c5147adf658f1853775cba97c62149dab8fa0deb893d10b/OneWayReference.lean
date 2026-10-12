import CountableIdentification
import Mathlib.MeasureTheory.Measure.Count
import Mathlib

open MeasureTheory Set
open scoped ENNReal

namespace FreshProofAudit

/-- Two mutually singular actual experiments can both be dominated by a
single finite reference. Full support across actual laws is unnecessary. -/
theorem finite_singular_family_has_common_reference :
    (Measure.dirac (0:ℝ) ≪ Measure.dirac (0:ℝ) + Measure.dirac (1:ℝ)) ∧
    (Measure.dirac (1:ℝ) ≪ Measure.dirac (0:ℝ) + Measure.dirac (1:ℝ)) ∧
    ¬ (Measure.dirac (0:ℝ) ≪ Measure.dirac (1:ℝ)) := by
  constructor
  · intro s hs
    have h := congrArg (fun x : ℝ≥0∞ => x = 0) hs
    have hz : (Measure.dirac (0:ℝ)) s + (Measure.dirac (1:ℝ)) s = 0 := by
      simpa using hs
    exact (add_eq_zero.mp hz).1
  constructor
  · intro s hs
    have hz : (Measure.dirac (0:ℝ)) s + (Measure.dirac (1:ℝ)) s = 0 := by
      simpa using hs
    exact (add_eq_zero.mp hz).2
  · intro h
    have hz : (Measure.dirac (1:ℝ)) {0} = 0 := by simp
    have ha := h hz
    simp at ha

#print axioms finite_singular_family_has_common_reference
end FreshProofAudit
