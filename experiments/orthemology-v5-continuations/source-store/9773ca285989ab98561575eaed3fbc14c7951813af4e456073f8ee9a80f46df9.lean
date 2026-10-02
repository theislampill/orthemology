import RepairEndpointCells
open Orthemology.Tranche3
#check @positive_weight_punctured_cell
#check @zero_weight_unique
#check @one_weight_unique
#check @below_one_punctured_cell
#print LiteralRepairGood
#print excessZero
#print excessOne
#print axioms positive_weight_punctured_cell
#print axioms zero_weight_unique
#print axioms one_weight_unique
#print axioms below_one_punctured_cell

/-- Endpoint uniqueness survives the two asymmetric baseline coordinates. -/
example : LiteralRepairGood 0 (1/4) (1/2) ∧ LiteralRepairGood 1 (1/4) (3/4) := by
  constructor <;> norm_num [LiteralRepairGood,excessZero,excessOne]

/-- Removing the (1+epsilon) allowance in the left upper bound is unsound. -/
example : LiteralRepairGood (1/2) (1/4) (63/100) ∧
    (1/2:ℝ)+(1/2)*(1/4) < 63/100 := by
  norm_num [LiteralRepairGood,excessZero,excessOne]

/-- Shrinking the right width coefficient from two to one is unsound. -/
example : LiteralRepairGood (99/100) (1/4) (747/1000) ∧
    (747/1000:ℝ) < 1/2+1/4-(1/4)*(1-99/100) := by
  norm_num [LiteralRepairGood,excessZero,excessOne]
