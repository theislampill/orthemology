import GenericAuditControls
open MeasureTheory
example : ∀ b : Bool, (Measure.dirac false : Measure Bool) {b} ≠ 0 := by
  intro b
  cases b <;> norm_num
