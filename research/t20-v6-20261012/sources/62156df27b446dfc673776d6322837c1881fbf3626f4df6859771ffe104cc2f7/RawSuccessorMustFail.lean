import FullESectionApplication
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.EffectiveCompleteness RigidityInitiality SourceRigidity
example {Γ : Tel} {P : Ty} {p s r n : Poly} (hc : CtxE Γ) (hP : FormE (N :: Γ) P)
    (hp : HasE Γ p (inst P zero)) (hs : HasE Γ s (dependentStepType P))
    (hr : HasE Γ r Rigidity) (hn : HasE Γ n N) :
    P01DF.PolyConv (sectionBody p s (.app succPoly n)) (.app (.app s n) (sectionBody p s n)) := by
  exact RigidityInitiality.FullE.section_successor_law hc hP hp hs hr hn
