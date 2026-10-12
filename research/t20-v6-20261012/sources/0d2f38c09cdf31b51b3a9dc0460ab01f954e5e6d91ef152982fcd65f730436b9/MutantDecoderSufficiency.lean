import RepairTestingBridge
open Orthemology.Tranche2
-- This assertion MUST be rejected: the necessary decoder tolerance is insufficient.
example : BinaryGood (1/2:ℝ) (1/4) (21/32) := by
  norm_num [BinaryGood]
