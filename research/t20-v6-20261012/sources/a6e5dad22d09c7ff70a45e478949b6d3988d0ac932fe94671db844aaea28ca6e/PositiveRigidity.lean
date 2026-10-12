import SchemaSeparation

namespace RigidityInitiality.FullE.PositiveCompletion
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity InductionConverse
open CompletionIndependence
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- An actual unchanged-HasE construction from a supplied equality section.
No induction schema is assumed by this lemma. -/
theorem section_rigidE {Γ : Tel} {u t : Poly} (hc : CtxE Γ)
    (hu : HasE Γ u NT) (ht : HasE Γ t (.pi N (EqFamily u))) :
    HasE Γ ident (ResultAt u) := by
  have cN := CtxE.ext hc (N_form hc)
  have hu1 : HasE (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have ht1 : HasE (N :: Γ) (pren Nat.succ t) (.pi N (EqFamily (pren Nat.succ u))) := by
    simpa [wk, subst, N_subst, EqFamily, pren, psub, psub_comp, pup] using has_wk ht hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have point : HasE (N :: Γ) (.app (pren Nat.succ t) (.var 0))
      (.identity N (.app (pren Nat.succ u) (.var 0)) (.var 0)) := by
    have hf := has_form ht1
    exact family_at _ _ ▸ HasE.piElim hf (form_inst_source cN (pi_body_form hf) hn) ht1 hn
  have hT := form_arr (N_form hc) (N_form hc)
  have hT1 := form_arr (N_form cN) (N_form cN)
  have hi := i_T hc
  have hi1 := i_T cN
  have left := app_has hT1 (N_form cN) hi1 hn
  have right := app_has hT1 (N_form cN) hu1 hn
  obtain ⟨e, he⟩ := nat_symE cN right hn point
  have link := identityIntro_raw (.identity (N_form cN) left hn) left hn (.i _)
  have body := nat_identity_trans cN left hn right link he
  have hM := FormE.identity (N_form cN) left right
  have hPiM := FormE.pi (N_form hc) hM
  have hh := HasE.piIntro hPiM body (scoped_abstract (has_scoped body))
  exact HasE.piExt (N_form hc) (N_form cN) hT hi hu hM hPiM hh
    (resultAt_formed hc hu) (has_scoped hi) (has_scoped hu)
    (scoped_abstract (has_scoped body))
    (Structural.form_scoped (N_form hc)) (Structural.form_scoped (N_form cN))

/-- This source implication isolates all structural work in unchanged HasE. -/
theorem section_implies_rigidE {Γ : Tel} {u : Poly} (hc : CtxE Γ)
    (hu : HasE Γ u NT) :
    HasE Γ (abstract ident) (arr (.pi N (EqFamily u)) (ResultAt u)) := by
  let H : Ty := .pi N (EqFamily u)
  have hH : FormE Γ H := .pi (N_form hc) (family_form hc hu)
  have cH := CtxE.ext hc hH
  have hu1 := has_wk hu hc hH
  have ht0 : HasE (H :: Γ) (.var 0) (wk H) := .var (form_wk hH hc hH) .zero
  have ht : HasE (H :: Γ) (.var 0) (.pi N (EqFamily (pren Nat.succ u))) := by
    simpa [H,wk,subst,N_subst,EqFamily,pren,psub,psub_comp,pup] using ht0
  have body := section_rigidE cH hu1 ht
  apply HasE.piIntro (form_arr hH (resultAt_formed hc hu))
  · simpa only [resultAt_shift] using body
  · exact scoped_abstract trivial

/-- Apply that old source implication to a new section. No weakening or
substitution theorem for the selective extension is assumed. -/
theorem section_rigidX {σ ι : Bool} {Γ : Tel} {u t : Poly} (hc : CtxE Γ)
    (hu : HasE Γ u NT) (ht : HasX σ ι Γ t (.pi N (EqFamily u))) :
    HasX σ ι Γ ident (ResultAt u) := by
  have hH : FormE Γ (.pi N (EqFamily u)) := .pi (N_form hc) (family_form hc hu)
  have hR := resultAt_formed hc hu
  have h := HasX.piElim (.formBase (form_arr hH hR))
    (.formBase (show FormE Γ (inst (wk (ResultAt u)) t) by simpa only [inst_wk] using hR))
    (.hasBase (section_implies_rigidE hc hu)) ht
  have h' : HasX σ ι Γ (.app (abstract ident) t) (ResultAt u) := by
    simpa only [inst_wk] using h
  have beta : Intensional.Plus.PolyConvPlus (.app (abstract ident) t) ident := by
    simpa [ident,abstract,freeZero,drop,pren,psub] using
      (Intensional.Plus.PolyConvPlus.k (.atom .i) t)
  exact .conv (.formBase hR) h' beta trivial

/-- Full induction alone yields literal closed rigidity, with no Sigma rule. -/
theorem induction_only_rigidity_at {Γ : Tel} (hc : CtxE Γ) :
    HasX false true Γ (abstract (abstract (abstract ident))) Rigidity := by
  have hNT := form_arr (N_form hc) (N_form hc)
  have cT := CtxE.ext hc hNT
  have hu0 : HasE (NT :: Γ) (.var 0) NT :=
    .var (form_arr (N_form cT) (N_form cT)) .zero
  have hZ := zeroAt_formed cT hu0
  have cZ := CtxE.ext cT hZ
  have hu1 : HasE (ZeroAt (.var 0) :: NT :: Γ) (.var 1) NT :=
    .var (form_arr (N_form cZ) (N_form cZ)) (.succ .zero)
  have hS := stepAt_formed cZ hu1
  have cS := CtxE.ext cZ hS
  have hu2 : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 2) NT :=
    .var (form_arr (N_form cS) (N_form cS)) (.succ (.succ .zero))
  have hz0 : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 1) (wk (wk (ZeroAt (.var 0)))) :=
    .var (Structural.lookup_form cS (.succ .zero)) (.succ .zero)
  have hz : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 1) (ZeroAt (.var 2)) := by
    simpa only [zeroAt_shift, pren, psub] using hz0
  have hs0 : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 0) (wk (StepAt (.var 1))) :=
    .var (form_wk hS cZ hS) .zero
  have hs : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 0) (StepAt (.var 2)) := by
    simpa only [stepAt_shift, pren, psub] using hs0
  have hP := family_form cS hu2
  obtain ⟨step,hstep⟩ := family_step cS hu2 hs
  have seed : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 1) (inst (EqFamily (.var 2)) zero) :=
    by simpa only [family_at] using hz
  have hsection : HasX false true (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (sectionPoly (.var 1) step) (.pi N (EqFamily (.var 2))) :=
    .natInduction rfl (.ctxBase cS) (.formBase hP) (.hasBase seed) (.hasBase hstep)
  have body := section_rigidX cS hu2 hsection
  have first : HasX false true (ZeroAt (.var 0) :: NT :: Γ) (abstract ident)
      (arr (StepAt (.var 1)) (ResultAt (.var 1))) := by
    apply HasX.piIntro (.formBase (form_arr hS (resultAt_formed cZ hu1)))
    · simpa only [resultAt_shift, pren, psub] using body
    · exact scoped_abstract trivial
  have second : HasX false true (NT :: Γ) (abstract (abstract ident))
      (arr (ZeroAt (.var 0)) (arr (StepAt (.var 0)) (ResultAt (.var 0)))) := by
    apply HasX.piIntro (.formBase (form_arr hZ (form_arr (stepAt_formed cT hu0) (resultAt_formed cT hu0))))
    · have ew (X Y : Ty) : wk (arr X Y) = arr (wk X) (wk Y) := subst_arr X Y _
      simpa only [ew, stepAt_shift, resultAt_shift, pren, psub] using first
    · exact scoped_abstract (scoped_abstract trivial)
  exact HasX.piIntro (.formBase (rigidity_formed hc)) second
    (scoped_abstract (scoped_abstract (scoped_abstract trivial)))

theorem induction_only_rigidity :
    HasX false true [] (abstract (abstract (abstract ident))) Rigidity :=
  induction_only_rigidity_at CtxE.nil

theorem induction_only_compiler_identity :
    ∃ p, HasX false true [] p FullPER.Application.originalIdentity := by
  have hr : FormE [] Rigidity := rigidity_formed .nil
  have hq : HasE [] FullPER.Application.originalQ NT :=
    has_inclusion P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.original_q_has
  have hi := resultAt_formed CtxE.nil hq
  have h := HasX.piElim (.formBase (form_arr hr hi))
    (.formBase (show FormE [] (inst (wk (ResultAt FullPER.Application.originalQ))
      (abstract (abstract (abstract ident)))) by simpa only [inst_wk] using hi))
    (.hasBase (has_inclusion SourceRigidity.rigidity_implies_identity)) induction_only_rigidity
  exact ⟨_,by simpa only [inst_wk,SourceRigidity.result_exact] using h⟩

#print axioms section_rigidE
#print axioms section_implies_rigidE
#print axioms section_rigidX
#print axioms induction_only_rigidity
#print axioms induction_only_compiler_identity
end RigidityInitiality.FullE.PositiveCompletion
