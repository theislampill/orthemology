/- The exact retained polynomial, with actual-E typings at its application. -/
import FullEComputationLaws
namespace RigidityInitiality.FullE
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.ExtensionalRepair SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- No replacement section or raw conversion relation is defined. -/
theorem section_application_beta (p s n : Poly) :
    P01DF.PolyConv (.app (sectionPoly p s) n) (sectionBody p s n) :=
  RigidityInitiality.section_application_beta p s n

/-- The raw beta equation also gives a typed identity in the actual family. -/
theorem section_application_identity {Γ : Tel} {P : Ty} {p s r n : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) (hr : HasE Γ r Rigidity)
    (hn : HasE Γ n N) :
    HasE Γ ident (.identity (inst P n) (.app (sectionPoly p s) n) (sectionBody p s n)) := by
  have hF := form_inst_source hc hP hn
  have hleft := HasE.piElim (.pi (N_form hc) hP) hF (section_has hc hP hp hs hr) hn
  have hright := dependent_section_curried hc hP hp hs hr hn
  exact identityIntro_raw (.identity hF hleft hright) hleft hright
    (section_application_beta p s n)

#print axioms dependent_section_curried
#print axioms section_has
#print axioms rigidity_implies_section
#print axioms section_zero_law
#print axioms section_successor_law
#print axioms section_application_identity
end RigidityInitiality.FullE
