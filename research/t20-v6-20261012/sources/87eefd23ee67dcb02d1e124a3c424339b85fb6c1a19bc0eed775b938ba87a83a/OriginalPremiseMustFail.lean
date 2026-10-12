import IndependentScopeControl
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.EffectiveCompleteness RigidityInitiality SourceRigidity
open FullEIndependentReview
example : HasE [] (abstract (sectionPoly (pren Nat.succ ident) (pren Nat.succ constantStep)))
    (arr Rigidity (.pi N constantFamily)) := by
  exact RigidityInitiality.rigidity_implies_section Ctx.nil family_formed
    ((family_at zero).symm ▸ seed) step
