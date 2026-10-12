import Boundary
open OpenTermStandardness
-- Universal Raw equality is not available in this faithful model.
example : Conv T.i (TaggedPER.pair (TaggedPER.first T.i) (TaggedPER.second T.i)) := by
  exact Conv.refl _
