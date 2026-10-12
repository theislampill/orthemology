import Controls
open GuardedTree GuardedTree.Saturation GuardedTree.SaturationControls
-- Expected rejection: this grammar has equal key sets at rounds one and two,
-- but its true-judgement prices are respectively ten and one.
example : round priceDrop 1 true ∅ = round priceDrop 2 true ∅ := by
  norm_num [first_true_price, second_true_price]
