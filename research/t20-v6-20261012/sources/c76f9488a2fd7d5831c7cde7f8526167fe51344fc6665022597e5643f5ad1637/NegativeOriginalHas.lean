import InductionRigidityConverse
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open SourceRigidity RigidityInitiality RigidityInitiality.FullE
open RigidityInitiality.FullE.InductionConverse
example (hi : WeakInduction) : Has [] (abstract (abstract (abstract ident))) Rigidity := by
  exact weak_induction_implies_closed_rigidity hi
