/- Additive actual-E support for the literal retained total-space construction. -/
import SectionApplication
import TypeSubstitutionApplications
namespace RigidityInitiality.FullE
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

abbrev form_wk := @Structural.form_wk
abbrev has_wk := @Structural.has_wk
abbrev has_form := @ClosedProofCanonicalisation.formed
abbrev has_scoped := @Structural.has_scoped
abbrev form_theta_head := @Structural.form_theta_head
abbrev ctx_theta := @Structural.ctx_theta

theorem form_arr {Γ : Tel} {A B : Ty} (hA : FormE Γ A) (hB : FormE Γ B) :
    FormE Γ (arr A B) := .pi hA (form_wk hB (Structural.form_ctx hA) hA)

theorem app_has {Γ : Tel} {A B : Ty} {f a : Poly}
    (hAB : FormE Γ (arr A B)) (hB : FormE Γ B)
    (hf : HasE Γ f (arr A B)) (ha : HasE Γ a A) : HasE Γ (.app f a) B := by
  have h := HasE.piElim hAB (by simpa only [inst_wk] using hB) hf ha
  simpa only [inst_wk] using h

theorem zero_has_N {Γ : Tel} (hc : CtxE Γ) : HasE Γ zero N :=
  Structural.has_closed (has_inclusion (inputNumeral_has 0)) hc

theorem N_form {Γ : Tel} (hc : CtxE Γ) : FormE Γ N := has_form (zero_has_N hc)

theorem succ_has_NT {Γ : Tel} (hc : CtxE Γ) : HasE Γ succPoly NT :=
  Structural.has_closed (has_inclusion succ_has) hc

theorem i_T {Γ : Tel} (hc : CtxE Γ) : HasE Γ ident NT :=
  .i (N_form hc) (form_arr (N_form hc) (N_form hc))

theorem identityIntro_raw {Γ : Tel} {A : Ty} {p q : Poly}
    (hA : FormE Γ (.identity A p q)) (hp : HasE Γ p A) (hq : HasE Γ q A)
    (h : P01DF.PolyConv p q) : HasE Γ ident (.identity A p q) :=
  .identityIntro hA hp hq (P01AC.Intensional.Plus.polyConv_inclusion h)

theorem conv_raw {Γ : Tel} {A : Ty} {p q : Poly}
    (hA : FormE Γ A) (hp : HasE Γ p A) (h : P01DF.PolyConv p q)
    (hq : Scoped Γ.length q) : HasE Γ q A :=
  .conv hA hp (P01AC.Intensional.Plus.polyConv_inclusion h) hq

abbrev form_inst_source := @Structural.form_inst

theorem fold_has {Γ : Tel} {X : Ty} {n f a : Poly}
    (_hc : CtxE Γ) (hX : FormE Γ X) (hn : HasE Γ n N)
    (hf : HasE Γ f (arr X X)) (ha : HasE Γ a X) :
    HasE Γ (.app (.app n f) a) X := by
  have he := form_arr hX hX
  have hn' : HasE Γ n (arr (arr X X) (arr X X)) := by
    simpa only [church_instantiate] using Structural.allElim_formed hn hX
  exact app_has he hX (app_has (form_arr he he) he hn' hf) ha

theorem zeroAt_formed {Γ : Tel} (hc : CtxE Γ) {u : Poly} (hu : HasE Γ u NT) :
    FormE Γ (ZeroAt u) :=
  .identity (N_form hc)
    (app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu (zero_has_N hc))
    (zero_has_N hc)


theorem stepAt_formed {Γ : Tel} (hc : CtxE Γ) {u : Poly} (hu : HasE Γ u NT) :
    FormE Γ (StepAt u) := by
  have c1 := CtxE.ext hc (N_form hc)
  have hu1 : HasE (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form c1) .zero
  have hs := succ_has_NT c1
  have sn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs hn
  have un := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 hn
  exact .pi (N_form hc) (.identity (N_form c1)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 sn)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs un))


theorem resultAt_formed {Γ : Tel} (hc : CtxE Γ) {u : Poly} (hu : HasE Γ u NT) :
    FormE Γ (ResultAt u) :=
  .identity (form_arr (N_form hc) (N_form hc)) (i_T hc) hu


theorem rigidity_formed {Γ : Tel} (hc : CtxE Γ) : FormE Γ Rigidity := by
  have hT := form_arr (N_form hc) (N_form hc)
  have c1 := CtxE.ext hc hT
  have hu : HasE (NT :: Γ) (.var 0) NT :=
    .var (form_arr (N_form c1) (N_form c1)) .zero
  exact .pi hT (form_arr (zeroAt_formed c1 hu)
    (form_arr (stepAt_formed c1 hu) (resultAt_formed c1 hu)))


end RigidityInitiality.FullE
