import ComputationLaws
namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- The uniform Pi witness computes to the same pointwise polynomial whose
    zero/successor laws were checked separately. -/
theorem section_application_beta (p s n : Poly) :
    P01DF.PolyConv (.app (sectionPoly p s) n) (sectionBody p s n) := by
  have h := poly_beta (sectionBody (pren Nat.succ p) (pren Nat.succ s) (.var 0)) n
  simpa [sectionPoly, sectionBody, totalStep, totalSeed, uncurriedStep,
    nextIndex, fstPoly, sndPoly, pairPoly, zero, psub, pren,
    ← abstraction_naturality, psub_comp, pup, cons, psub_id,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has),
    P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))] using h

#print axioms section_application_beta
end RigidityInitiality
