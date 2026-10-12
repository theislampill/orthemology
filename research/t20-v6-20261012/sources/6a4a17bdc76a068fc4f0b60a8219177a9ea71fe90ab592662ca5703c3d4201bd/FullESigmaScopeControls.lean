/- Positive E-only scope controls, with proved exclusions from the old
   judgement. Canonical inputs and constant motives below are scope tests,
   not evidence that eta is needed for those particular instances. -/
import FullESigmaElimination
import TypeSubstitutionControls
namespace SigmaCompletion.FullE.ScopeControls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.InternalGraph
open HasEDependentSubstitutionControls (extId proofId)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

abbrev ident : Poly := .atom .i
abbrev S : Ty := .sigma .raw .raw
abbrev D : Ty := proofId
abbrev E : Ty := extId
abbrev inputType : Ty := .sigma E .raw
abbrev input : Poly := pairPoly ident ident
abbrev motive : Ty := wk D

private theorem d_has : HasE [] ident D :=
  HasEDependentSubstitutionControls.substituted_dependent_branch
private theorem d_formed : FormE [] D := HasETypeSubstitutionControls.beyond_original_image_formed
private theorem e_has : HasE [] ident E := HasEDependentSubstitutionControls.extensional_image
private theorem e_formed : FormE [] E := ClosedProofCanonicalisation.formed e_has

theorem context_only_actual : CtxE [D] := .ext .nil d_formed

theorem context_not_original : ¬ Ctx [D] := by
  intro h
  cases h with
  | ext _ hD => exact HasETypeSubstitutionControls.beyond_original_image_not_formed hD

private theorem s_original : Form [] S := .sigma (.raw .nil) (.raw (.ext .nil (.raw .nil)))
private theorem s_pair_original : Has [] input S :=
  .sigmaIntro s_original (.raw .nil) (.rawAtom (.raw .nil)) (.rawAtom (.raw .nil))

/-- Motive formation itself exceeds original Form even though its context
    is formed in the original calculus. -/
theorem motive_only_actual : FormE [S] motive :=
  Structural.form_wk d_formed .nil (form_inclusion s_original)

theorem motive_not_original : ¬ Form [S] motive := by
  intro hP
  have h := RigidityInitiality.form_inst_source Ctx.nil hP s_pair_original
  have hD : Form [] D := by simpa only [motive, inst_wk] using h
  exact HasETypeSubstitutionControls.beyond_original_image_not_formed hD

/-- The branch can also be genuinely E-only in an original well-formed
    branch telescope; its exclusion is not just context rejection. -/
theorem branch_only_actual : HasE [.raw, .raw] ident (branchType motive) :=
  Structural.has_closed d_has (.ext (.ext .nil (.raw .nil)) (.raw (.ext .nil (.raw .nil))))

theorem branch_not_original (p : Poly) : ¬ Has [.raw, .raw] p (branchType motive) := by
  intro hp
  have h := SigmaCompletion.branch_has Ctx.nil hp
    (Has.rawAtom (t := Term.i) (.raw .nil)) (Has.rawAtom (t := Term.i) (.raw .nil))
  have hD : Has [] (branchAt p ident ident) D := by simpa only [motive, inst_wk] using h
  exact HasEDependentSubstitutionControls.substituted_result_not_original _ hD

theorem input_type_actual : FormE [] inputType :=
  .sigma e_formed (.raw (.ext .nil e_formed))

/-- A closed E-only pair input, independent of the E-only-context test. -/
theorem input_only_actual : HasE [] input inputType :=
  .sigmaIntro input_type_actual (.raw .nil) e_has (.rawAtom (.raw .nil))

theorem input_not_original (p : Poly) : ¬ Has [] p inputType := by
  intro hp
  have hs := P01AC.has_form hp
  have hE : Form [] E := by cases hs; assumption
  exact HasEDependentSubstitutionControls.no_original_image _ (.sigmaFst hE hs hp)

/-- The complete constructive interface is exercised in a context outside
    original Ctx, with a motive outside original Form and an E-only input. -/
theorem combined_context : CtxE [D] := context_only_actual

theorem combined_A : FormE [D] E := by
  exact Structural.form_wk e_formed .nil d_formed

theorem combined_B : FormE (E :: [D]) .raw := .raw (.ext combined_context combined_A)

theorem combined_input : HasE [D] input inputType :=
  Structural.has_closed input_only_actual combined_context

theorem combined_motive : FormE (inputType :: [D]) motive := by
  have hD : FormE [D] D := Structural.form_wk d_formed .nil d_formed
  exact Structural.form_wk hD combined_context (.sigma combined_A combined_B)

theorem combined_branch : HasE (.raw :: E :: [D]) ident (branchType motive) := by
  have hctx := CtxE.ext (.ext combined_context combined_A) combined_B
  exact Structural.has_closed d_has hctx

theorem combined_eta : HasE [D] ident (.identity inputType input (reconstruct input)) := by
  have hp := combined_input
  have hr := reconstruction_has combined_context combined_A combined_B hp
  exact .identityIntro (.identity (.sigma combined_A combined_B) hp hr) hp hr
    (P01AC.Intensional.Plus.polyConv_inclusion
      (pair_poly_congr (pair_first ident ident) (pair_second ident ident)).symm)

theorem combined_elimination : HasE [D] (elim ident input ident) D := by
  have h := elim_of_eta combined_context combined_A combined_B combined_motive
    combined_branch combined_input combined_eta
  simpa only [motive, inst_wk] using h

/-- Raw beta remains the inherited theorem, independently of all E evidence. -/
theorem combined_raw_beta : P01DF.PolyConv (elim ident input ident) ident :=
  elim_pair_computation ident ident ident ident

theorem combined_context_has_no_original_typing (p : Poly) (A : Ty) : ¬ Has [D] p A := by
  intro hp
  exact context_not_original (P01AC.form_ctx (P01AC.has_form hp))

#print axioms context_not_original
#print axioms motive_not_original
#print axioms branch_not_original
#print axioms input_not_original
#print axioms combined_elimination
#print axioms combined_raw_beta
end SigmaCompletion.FullE.ScopeControls
