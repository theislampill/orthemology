import Controls
open GuardedTree GuardedTree.Saturation GuardedTree.SaturationControls
-- Expected rejection: an unsupported cycle cannot seed a numeric entry.
example : ∃ c, round unsupported 1 () ∅ = some c := by
  simp only [unsupported_all_rounds, reduceCtorEq, exists_false]
