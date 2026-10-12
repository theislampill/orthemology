import FullESectionApplication
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.EffectiveCompleteness RigidityInitiality SourceRigidity
example {Γ : Tel} {P : Ty} {p s : Poly} (hc : CtxE Γ) (hP : FormE (N :: Γ) P)
    (hp : HasE Γ p (inst P zero)) (hs : HasE Γ s (dependentStepType P)) :
    HasE Γ (sectionPoly p s) (.pi N P) := by
  exact RigidityInitiality.FullE.section_has hc hP hp hs
