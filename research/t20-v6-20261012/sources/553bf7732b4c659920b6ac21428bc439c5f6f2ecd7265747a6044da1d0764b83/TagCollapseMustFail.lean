import Boundary
open OpenTermStandardness TaggedPER SigmaTagBoundary
-- Erasing the tag must not let component equality prove Sigma equality.
example (ρ : TaggedPER.REnv) (η : TaggedPER.Env) :
    TaggedPER.F SigmaRaw ρ η T.i (TaggedPER.pair (first T.i) (second T.i)) := by
  exact ⟨matching_observations.1, matching_observations.2⟩
