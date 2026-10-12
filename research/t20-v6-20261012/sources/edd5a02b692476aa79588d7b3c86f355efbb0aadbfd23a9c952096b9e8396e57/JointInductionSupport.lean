/- Additive Joint port of the credited actual-E total-space proof. -/
import SectionApplication
import JointTypeInstantiation
import JointSigmaExtraction
namespace JointCompletion.InductionComputation
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

abbrev form_wk := @JointCompletion.Structural.form_wk
abbrev has_wk := @JointCompletion.Structural.has_wk
abbrev has_form := @JointCompletion.Structural.has_form
abbrev has_scoped := @JointCompletion.Structural.has_scoped
abbrev form_theta_head := @JointCompletion.Structural.form_theta_head
abbrev ctx_theta := @JointCompletion.Structural.ctx_theta

theorem form_arr {Γ : Tel} {A B : Ty} (hA : FormJ Γ A) (hB : FormJ Γ B) :
    FormJ Γ (arr A B) := .pi hA (form_wk hB (JointCompletion.Structural.form_ctx hA) hA)

theorem app_has {Γ : Tel} {A B : Ty} {f a : Poly}
    (hAB : FormJ Γ (arr A B)) (hB : FormJ Γ B)
    (hf : HasJ Γ f (arr A B)) (ha : HasJ Γ a A) : HasJ Γ (.app f a) B := by
  have h := HasJ.piElim hAB (by simpa only [inst_wk] using hB) hf ha
  simpa only [inst_wk] using h

theorem zero_has_N {Γ : Tel} (hc : CtxJ Γ) : HasJ Γ zero N :=
  JointCompletion.DependentExtraction.closed_has (.hasBase (has_inclusion (inputNumeral_has 0))) hc

theorem N_form {Γ : Tel} (hc : CtxJ Γ) : FormJ Γ N := has_form (zero_has_N hc)

theorem succ_has_NT {Γ : Tel} (hc : CtxJ Γ) : HasJ Γ succPoly NT :=
  JointCompletion.DependentExtraction.closed_has (.hasBase (has_inclusion succ_has)) hc

theorem i_T {Γ : Tel} (hc : CtxJ Γ) : HasJ Γ ident NT :=
  .i (N_form hc) (form_arr (N_form hc) (N_form hc))

theorem identityIntro_raw {Γ : Tel} {A : Ty} {p q : Poly}
    (hA : FormJ Γ (.identity A p q)) (hp : HasJ Γ p A) (hq : HasJ Γ q A)
    (h : P01DF.PolyConv p q) : HasJ Γ ident (.identity A p q) :=
  .identityIntro hA hp hq (P01AC.Intensional.Plus.polyConv_inclusion h)

theorem conv_raw {Γ : Tel} {A : Ty} {p q : Poly}
    (hA : FormJ Γ A) (hp : HasJ Γ p A) (h : P01DF.PolyConv p q)
    (hq : Scoped Γ.length q) : HasJ Γ q A :=
  .conv hA hp (P01AC.Intensional.Plus.polyConv_inclusion h) hq

abbrev form_inst_source := @JointCompletion.Structural.form_inst

theorem fold_has {Γ : Tel} {X : Ty} {n f a : Poly}
    (_hc : CtxJ Γ) (hX : FormJ Γ X) (hn : HasJ Γ n N)
    (hf : HasJ Γ f (arr X X)) (ha : HasJ Γ a X) :
    HasJ Γ (.app (.app n f) a) X := by
  have he := form_arr hX hX
  have hn' : HasJ Γ n (arr (arr X X) (arr X X)) := by
    simpa only [church_instantiate] using JointCompletion.Structural.allElim_formed hn hX
  exact app_has he hX (app_has (form_arr he he) he hn' hf) ha

theorem zeroAt_formed {Γ : Tel} (hc : CtxJ Γ) {u : Poly} (hu : HasJ Γ u NT) :
    FormJ Γ (ZeroAt u) :=
  .identity (N_form hc)
    (app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu (zero_has_N hc))
    (zero_has_N hc)


theorem stepAt_formed {Γ : Tel} (hc : CtxJ Γ) {u : Poly} (hu : HasJ Γ u NT) :
    FormJ Γ (StepAt u) := by
  have c1 := CtxJ.ext hc (N_form hc)
  have hu1 : HasJ (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : HasJ (N :: Γ) (.var 0) N := .var (N_form c1) .zero
  have hs := succ_has_NT c1
  have sn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs hn
  have un := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 hn
  exact .pi (N_form hc) (.identity (N_form c1)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 sn)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs un))


theorem resultAt_formed {Γ : Tel} (hc : CtxJ Γ) {u : Poly} (hu : HasJ Γ u NT) :
    FormJ Γ (ResultAt u) :=
  .identity (form_arr (N_form hc) (N_form hc)) (i_T hc) hu


theorem rigidity_formed {Γ : Tel} (hc : CtxJ Γ) : FormJ Γ Rigidity := by
  have hT := form_arr (N_form hc) (N_form hc)
  have c1 := CtxJ.ext hc hT
  have hu : HasJ (NT :: Γ) (.var 0) NT :=
    .var (form_arr (N_form c1) (N_form c1)) .zero
  exact .pi hT (form_arr (zeroAt_formed c1 hu)
    (form_arr (stepAt_formed c1 hu) (resultAt_formed c1 hu)))


end JointCompletion.InductionComputation
