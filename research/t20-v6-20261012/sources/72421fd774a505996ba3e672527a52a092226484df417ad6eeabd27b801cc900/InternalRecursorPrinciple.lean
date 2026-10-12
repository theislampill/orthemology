import SourceFoldApplication
import RecursorUniqueness

/- A candidate principle EXPRESSED in the unchanged source grammar.
   This file forms it; it does not add a constructor or assert an inhabitant. -/
namespace InternalRecursorPrinciple
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Under u,f,a: the zero equation. -/
def ZeroLaw : Ty := .identity A
  (.app (.var 0) (inputNumeral 0)) (.var 2)

/-- Under zero-evidence,u,f,a: a universally quantified successor equation. -/
def StepLaw : Ty := .pi N (.identity A
  (.app (.var 2) (.app succPoly (.var 0)))
  (.app (.var 3) (.app (.var 2) (.var 0))))

/-- Under step-evidence,zero-evidence,u,f,a: pointwise uniqueness. -/
def UniqueConclusion : Ty := .pi N (.identity A
  (.app (.var 3) (.var 0))
  (.app (.app (.var 0) (.var 4)) (.var 5)))

/-- Generic source-internal Church recursor uniqueness. There is no compiler,
    target W, graph carrier or fold-fusion equation in this definition. -/
def Uniqueness : Ty := .all
  (.pi A (.pi End (.pi (arr N A)
    (.pi ZeroLaw (.pi StepLaw UniqueConclusion)))))

theorem zero_law_formed {Γ : Tel} (hc : Ctx Γ) :
    Form (arr N A :: End :: A :: Γ) ZeroLaw := by
  have cA := Ctx.ext hc (show Form Γ A from .param hc)
  have cF := Ctx.ext cA (show Form _ End from form_arr (.param cA) (.param cA))
  have cU := Ctx.ext cF (show Form _ (arr N A) from form_arr (N_form cF) (.param cF))
  have hu : Has (arr N A :: End :: A :: Γ) (.var 0) (arr N A) :=
    .var (form_arr (N_form cU) (.param cU)) .zero
  have ha : Has (arr N A :: End :: A :: Γ) (.var 2) A :=
    .var (.param cU) (.succ (.succ .zero))
  have hz := closed_has (inputNumeral_has 0) N_subst cU
  exact .identity (.param cU)
    (app_has (form_arr (N_form cU) (.param cU)) (.param cU) hu hz) ha

theorem step_law_formed {Γ : Tel} (hc : Ctx Γ) :
    Form (ZeroLaw :: arr N A :: End :: A :: Γ) StepLaw := by
  have cA := Ctx.ext hc (show Form Γ A from .param hc)
  have cF := Ctx.ext cA (show Form _ End from form_arr (.param cA) (.param cA))
  have cU := Ctx.ext cF (show Form _ (arr N A) from form_arr (N_form cF) (.param cF))
  have cZ := Ctx.ext cU (zero_law_formed hc)
  have cN := Ctx.ext cZ (N_form cZ)
  have hn : Has (N :: ZeroLaw :: arr N A :: End :: A :: Γ) (.var 0) N :=
    .var (N_form cN) .zero
  have hu : Has (N :: ZeroLaw :: arr N A :: End :: A :: Γ) (.var 2) (arr N A) :=
    .var (form_arr (N_form cN) (.param cN)) (.succ (.succ .zero))
  have hf : Has (N :: ZeroLaw :: arr N A :: End :: A :: Γ) (.var 3) End :=
    .var (form_arr (.param cN) (.param cN)) (.succ (.succ (.succ .zero)))
  have hs := closed_has succ_has (fun _ => rfl) cN
  have hsn := app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hs hn
  have hun := app_has (form_arr (N_form cN) (.param cN)) (.param cN) hu hn
  exact .pi (N_form cZ) (.identity (.param cN)
    (app_has (form_arr (N_form cN) (.param cN)) (.param cN) hu hsn)
    (app_has (form_arr (.param cN) (.param cN)) (.param cN) hf hun))

theorem unique_conclusion_formed {Γ : Tel} (hc : Ctx Γ) :
    Form (StepLaw :: ZeroLaw :: arr N A :: End :: A :: Γ) UniqueConclusion := by
  have cA := Ctx.ext hc (show Form Γ A from .param hc)
  have cF := Ctx.ext cA (show Form _ End from form_arr (.param cA) (.param cA))
  have cU := Ctx.ext cF (show Form _ (arr N A) from form_arr (N_form cF) (.param cF))
  have cZ := Ctx.ext cU (zero_law_formed hc)
  have cS := Ctx.ext cZ (step_law_formed hc)
  have cN := Ctx.ext cS (N_form cS)
  have hn : Has (N :: StepLaw :: ZeroLaw :: arr N A :: End :: A :: Γ) (.var 0) N :=
    .var (N_form cN) .zero
  have hu : Has (N :: StepLaw :: ZeroLaw :: arr N A :: End :: A :: Γ) (.var 3) (arr N A) :=
    .var (form_arr (N_form cN) (.param cN)) (.succ (.succ (.succ .zero)))
  have hf : Has (N :: StepLaw :: ZeroLaw :: arr N A :: End :: A :: Γ) (.var 4) End :=
    .var (form_arr (.param cN) (.param cN)) (.succ (.succ (.succ (.succ .zero))))
  have ha : Has (N :: StepLaw :: ZeroLaw :: arr N A :: End :: A :: Γ) (.var 5) A :=
    .var (.param cN) (.succ (.succ (.succ (.succ (.succ .zero)))))
  exact .pi (N_form cS) (.identity (.param cN)
    (app_has (form_arr (N_form cN) (.param cN)) (.param cN) hu hn)
    (P01AC.ExtensionalRepair.ExactScalarFusion.scalar_n_has cN hn hf ha))

/-- A checked original-source proposition, not an axiom or source proof. -/
theorem uniqueness_formed {Γ : Tel} (hc : Ctx Γ) : Form Γ Uniqueness := by
  have c := ctx_twk hc
  have cA := Ctx.ext c (show Form (twkTel Γ) A from .param c)
  have cF := Ctx.ext cA (show Form _ End from form_arr (.param cA) (.param cA))
  have cU := Ctx.ext cF (show Form _ (arr N A) from form_arr (N_form cF) (.param cF))
  exact .all hc (.pi (.param c) (.pi (form_arr (.param cA) (.param cA))
    (.pi (form_arr (N_form cF) (.param cF))
      (.pi (zero_law_formed c) (.pi (step_law_formed c) (unique_conclusion_formed c))))))

#print axioms uniqueness_formed
end InternalRecursorPrinciple
