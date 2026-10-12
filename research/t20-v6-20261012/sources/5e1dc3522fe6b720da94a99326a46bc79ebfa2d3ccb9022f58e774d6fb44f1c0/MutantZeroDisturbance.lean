import RepairTestingBridge
open Orthemology.Tranche2
-- This assertion MUST be rejected: removing 0 < e is a false extension.
example : ¬ (BinaryGood (1/2:ℝ) 0 (1/2) ∧ BinaryGood (1/2:ℝ) 0 (1/2)) := by
  norm_num [BinaryGood]
