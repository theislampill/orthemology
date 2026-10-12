import GeneratedExponentialTail

noncomputable section
attribute [local instance] Classical.propDecidable
open scoped ENNReal BigOperators
open HiddenParity.Cost

namespace IndependentExponentialReview

/-- Time zero is a real bad action, not an omitted or synthetic visit. -/
theorem first_action_counted : badCount (fun n : ℕ => n = 0) id = 1 := by
  simp [badCount]

/-- A zero horizon has no physical action. -/
theorem zero_horizon (progress danger : ℕ → Prop) (j : ℕ) :
    slotLength progress danger 0 j = 0 := by
  simp [slotLength]

/-- The sole action at time zero belongs to chronological slot zero. -/
theorem first_action_slot : slotLength (fun _ => False) (fun _ => True) 1 0 = 1 := by
  simp [slotLength, progressCount]

/-- Dangerous time is counted, safe residence is not converted to cost. -/
theorem safe_residence_zero (progress : ℕ → Prop) (T j : ℕ) :
    slotLength progress (fun _ => False) T j = 0 := by
  simp [slotLength]

/-- Physical progress at time zero begins slot one at time one. -/
theorem next_slot_keeps_next_action :
    slotLength (fun t => t = 0) (fun _ => True) 2 1 = 1 := by
  simp [slotLength, progressCount, Finset.range_succ, Finset.filter_insert, Finset.filter_singleton]

/-- Future slot zero padding has factor one, regardless of the base. -/
theorem zero_padding_factor (a : ℝ≥0∞) (D : ℕ) : a^(0 ⌈/⌉ D) = 1 := by simp

/-- Block rounding must be upward: even one dangerous action has a charge. -/
theorem first_block_rounded_up : (1 : ℕ) ⌈/⌉ 3 = 1 := by decide

/-- Floor division would erase the same first dangerous action. -/
theorem floor_erases_first_block : (1 : ℕ) / 3 = 0 := by decide

/-- A whole block is still one charge, without an extra boundary penalty. -/
theorem complete_block_once : (3 : ℕ) ⌈/⌉ 3 = 1 := by decide

/-- An action beyond a whole block starts the second charge. -/
theorem block_boundary_next_action : (4 : ℕ) ⌈/⌉ 3 = 2 := by decide

#print axioms first_action_counted
#print axioms zero_horizon
#print axioms first_action_slot
#print axioms safe_residence_zero
#print axioms next_slot_keeps_next_action
#print axioms zero_padding_factor
#print axioms first_block_rounded_up
#print axioms floor_erases_first_block
#print axioms complete_block_once
#print axioms block_boundary_next_action
end IndependentExponentialReview
