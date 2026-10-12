import JointInductionSectionApplication
import JointSigmaFidelity
import PositiveTransfer

namespace JointCompletion.InductionComputation
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.Intensional.Plus (PolyConvPlus)
open SourceRigidity RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Closed source rigidity is already earned by induction; this uses actual
Joint weakening into arbitrary newly formed contexts. -/
theorem rigidity_in_context {Γ : Tel} (hc : CtxJ Γ) :
    HasJ Γ (abstract (abstract (abstract ident))) Rigidity :=
  DependentExtraction.closed_has RigidityInitiality.FullE.PositiveCompletion.joint_rigidity hc

/-- The constructor's exact literal result, with no external rigidity premise. -/
theorem induction_section {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P) (hp : HasJ Γ p (inst P zero))
    (hs : HasJ Γ s (dependentStepType P)) :
    HasJ Γ (sectionPoly p s) (.pi N P) := .natInduction hc hP hp hs

theorem induction_value {Γ : Tel} {P : Ty} {p s n : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P) (hp : HasJ Γ p (inst P zero))
    (hs : HasJ Γ s (dependentStepType P)) (hn : HasJ Γ n N) :
    HasJ Γ (.app (sectionPoly p s) n) (inst P n) :=
  .piElim (.pi (N_form hc) hP) (Structural.form_inst hc hP hn)
    (induction_section hc hP hp hs) hn

theorem induction_zero {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P) (hp : HasJ Γ p (inst P zero))
    (hs : HasJ Γ s (dependentStepType P)) :
    HasJ Γ ident (.identity (inst P zero) (.app (sectionPoly p s) zero) p) := by
  have hl := induction_value hc hP hp hs (zero_has_N hc)
  exact identityIntro_raw (.identity (has_form hp) hl hp) hl hp
    ((section_application_beta p s zero).trans (section_zero_beta p s))

/-- Full propositional successor computation at the literal constructor result.
The equality is in P(succ n); there is no raw successor-conversion assertion. -/
theorem induction_successor {Γ : Tel} {P : Ty} {p s n : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P) (hp : HasJ Γ p (inst P zero))
    (hs : HasJ Γ s (dependentStepType P)) (hn : HasJ Γ n N) :
    ∃ e, HasJ Γ e (.identity (inst P (.app succPoly n))
      (.app (sectionPoly p s) (.app succPoly n))
      (.app (.app s n) (.app (sectionPoly p s) n))) := by
  have hr := rigidity_in_context hc
  have hsn := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) (succ_has_NT hc) hn
  have hleft := induction_value hc hP hp hs hsn
  have hbody := dependent_section_curried hc hP hp hs hr hsn
  have happ := section_application_identity hc hP hp hs hr hsn
  obtain ⟨e, he⟩ := section_successor_law hc hP hp hs hr hn
  have hd := dependent_section_curried hc hP hp hs hr hn
  have hv := induction_value hc hP hp hs hn
  have hm : HasJ Γ (.app (.app s n) (sectionBody p s n)) (inst P (.app succPoly n)) := by
    simpa only [successorFamily_at] using
      dependent_apply_has hc hP (successorFamily_form hc hP) hs hn hd
  have hright : HasJ Γ (.app (.app s n) (.app (sectionPoly p s) n))
      (inst P (.app succPoly n)) := by
    simpa only [successorFamily_at] using
      dependent_apply_has hc hP (successorFamily_form hc hP) hs hn hv
  have hraw := identityIntro_raw (.identity (has_form hm) hm hright) hm hright
    (P01DF.PolyConv.app (.refl _) (section_application_beta p s n).symm)
  have hab := ExtractionFidelity.identity_trans hc (has_form hm) hleft hbody hm happ he
  exact ⟨ident, ExtractionFidelity.identity_trans hc (has_form hm)
    hleft hm hright hab hraw⟩

/-- The dependent comparison motive keeps the supplied family literally. -/
def comparisonFamily (P : Ty) (u v : Poly) : Ty :=
  .identity P (.app (pren Nat.succ u) (.var 0)) (.app (pren Nat.succ v) (.var 0))

theorem comparison_formed {Γ : Tel} {P : Ty} {u v : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hu : HasJ Γ u (.pi N P)) (hv : HasJ Γ v (.pi N P)) :
    FormJ (N :: Γ) (comparisonFamily P u v) := by
  have cn := CtxJ.ext hc (N_form hc)
  have hn : HasJ (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  have hP' := shifted_family_form hc hP (N_form hc)
  have hw (f : Poly) (hf : HasJ Γ f (.pi N P)) :
      HasJ (N :: Γ) (.app (pren Nat.succ f) (.var 0)) P := by
    have hf' : HasJ (N :: Γ) (pren Nat.succ f) (.pi N (shiftedFamily P)) := by
      simpa only [wk, subst, N_subst, shiftedFamily] using has_wk hf hc (N_form hc)
    have h := HasJ.piElim (.pi (N_form cn) hP') (Structural.form_inst cn hP' hn) hf' hn
    simpa only [shifted_at_var] using h
  exact .identity hP (hw u hu) (hw v hv)

/-- Dependent uniqueness by source induction and the existing Pi extensionality
rule. Its step premise is explicitly the induction step on the comparison
family, not a hidden assumption that algebra laws imply that step. -/
theorem induction_extensionality {Γ : Tel} {P : Ty} {u v z s : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hu : HasJ Γ u (.pi N P)) (hv : HasJ Γ v (.pi N P))
    (hz : HasJ Γ z (inst (comparisonFamily P u v) zero))
    (hs : HasJ Γ s (dependentStepType (comparisonFamily P u v))) :
    HasJ Γ ident (.identity (.pi N P) u v) := by
  have hEq := comparison_formed hc hP hu hv
  have hsec := induction_section hc hEq hz hs
  have hPi := FormJ.pi (N_form hc) hP
  exact .piExt (N_form hc) hP hPi hu hv hEq (.pi (N_form hc) hEq) hsec
    (.identity hPi hu hv) (has_scoped hu) (has_scoped hv) (has_scoped hsec)
    (Structural.form_scoped (N_form hc)) (Structural.form_scoped hP)

#print axioms rigidity_in_context
#print axioms induction_zero
#print axioms induction_successor
#print axioms comparison_formed
#print axioms induction_extensionality
end JointCompletion.InductionComputation
