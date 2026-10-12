import InductionRigidityConverse
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open SourceRigidity RigidityInitiality RigidityInitiality.FullE
open RigidityInitiality.FullE.InductionConverse
example (Γ : Tel) (hc : CtxE Γ) (hi : WeakInductionAt Γ) : ∃ r, HasE Γ r Rigidity := by
  exact (contextual_weak_induction_iff_rigidity hc).mp hi
