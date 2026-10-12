import IndependentBinderJControl
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.EffectiveCompleteness RigidityInitiality SourceRigidity
open FullEIndependentReview HasEDependentSubstitutionControls
example : FormE [N, Rigidity, proofId] (.identity proofId (.var 1) (.var 1)) := by
  exact RigidityInitiality.FullE.shifted_family_form nonoriginal_context contextFamily_formed
    (RigidityInitiality.FullE.rigidity_formed nonoriginal_context)
