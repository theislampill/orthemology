import CompletionSeparation
example : P01AC.ExtensionalRepair.HasE []
  (P01D.Poly.app (.atom .k) (.atom .i)) SigmaTagBoundary.Eta :=
  CompletionSeparation.henkin_eta_valid HomogeneousOriginalW.emptyTypes HenkinSoundness.zeroEnv
