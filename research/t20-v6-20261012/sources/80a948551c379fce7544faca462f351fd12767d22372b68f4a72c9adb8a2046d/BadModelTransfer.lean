import CompletionSeparation
example (ρ : FullPER.REnv) (η : FullPER.Env) (a b : OpenTermStandardness.T) :
  ¬ FullPER.F SourceRigidity.Rigidity ρ η a b :=
  CompletionSeparation.henkin_rigidity_empty a b
