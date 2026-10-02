import RuntimeReceiptPath
import HeldReceiptProjection

namespace Orthemology.RationalLaw.Controls
open MeasureTheory Set
open scoped ENNReal
open P02A2.Q8Measure (fairCantor)

/-- D=1 retains a positive one-bit acquisition and a genuine rejection branch. -/
theorem denominator_one_first_clock :
    fairCantor (firstEvent (rejectedBlocks 1 1 (by decide)) (acceptedBlocks 1 1 (by decide)) 0) = 1/2 := by
  rw [rejection_count_probability]
  norm_num [ENNReal.div_self]

/-- At the dyadic boundary all first proposals are accepted. -/
theorem dyadic_boundary_first_clock :
    fairCantor (firstEvent (rejectedBlocks 2 4 (by decide)) (acceptedBlocks 2 4 (by decide)) 0) = 1 := by
  rw [rejection_count_probability]
  norm_num [ENNReal.div_self]

theorem dyadic_boundary_no_rejections (r : ℕ) (hr : 0 < r) :
    fairCantor (firstEvent (rejectedBlocks 2 4 (by decide)) (acceptedBlocks 2 4 (by decide)) r) = 0 := by
  rw [rejection_count_probability]
  norm_num [ne_of_gt hr,ENNReal.div_self]

/-- Zero-weight allocation entries really have zero receipt probability. -/
theorem zero_weight_unreachable {Y : Type*} [DecidableEq Y]
    (L D : ℕ) (hDB : D ≤ 2^L) (row : Fin D → Y) (y : Y) (hy : weight D row y = 0) :
    fairCantor (⋃ r, firstEvent (rejectedBlocks L D hDB) (receiptBlocks L D hDB row y) r) = 0 := by
  rw [receipt_probability,hy]
  simp

/-- Equal deterministic receipt laws can expose different public timing laws if
width/denominator are selected by the row/model rather than globally. -/
theorem row_dependent_timing_distinguishes :
    fairCantor (firstEvent (rejectedBlocks 1 1 (by decide)) (acceptedBlocks 1 1 (by decide)) 0) ≠
    fairCantor (firstEvent (rejectedBlocks 1 2 (by decide)) (acceptedBlocks 1 2 (by decide)) 0) := by
  rw [rejection_count_probability,rejection_count_probability]
  norm_num [ENNReal.div_self]

theorem same_constant_receipt_laws :
    fairCantor (⋃ r, firstEvent (rejectedBlocks 1 1 (by decide))
      (receiptBlocks 1 1 (by decide) (fun _ : Fin 1 => false) false) r) =
    fairCantor (⋃ r, firstEvent (rejectedBlocks 1 2 (by decide))
      (receiptBlocks 1 2 (by decide) (fun _ : Fin 2 => false) false) r) := by
  rw [receipt_probability,receipt_probability]
  norm_num [weight,ENNReal.div_self]

/-- Independent positive stuttering is insufficient for defect preservation,
even though it preserves every parity assignment. -/
theorem parity_safe_stutter_not_defect_safe :
    P02A2.defect (Orthemology.Frontier.MealyMeasure.law HeldStateControl.heldMachine false) = 1 ∧
    P02A2.defect ((Orthemology.Frontier.MealyMeasure.law HeldStateControl.heldMachine false).map
      HeldStateControl.compressHeld) = 0 :=
  ⟨HeldStateControl.held_defect_one,HeldStateControl.compressed_held_defect_zero⟩

end Orthemology.RationalLaw.Controls
