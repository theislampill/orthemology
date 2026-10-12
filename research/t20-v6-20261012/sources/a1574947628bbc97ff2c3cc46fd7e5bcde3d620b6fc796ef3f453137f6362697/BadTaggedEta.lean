import CompletionSeparation
example (ρ : TaggedPER.REnv) (η : TaggedPER.Env) :
  TaggedPER.F SigmaTagBoundary.Eta ρ η
    (OpenTermStandardness.T.k ⬝ OpenTermStandardness.T.i)
    (OpenTermStandardness.T.k ⬝ OpenTermStandardness.T.i) := by
  intro z w zw
  exact ⟨⟨True.intro, True.intro⟩, .k _ _, .k _ _⟩
