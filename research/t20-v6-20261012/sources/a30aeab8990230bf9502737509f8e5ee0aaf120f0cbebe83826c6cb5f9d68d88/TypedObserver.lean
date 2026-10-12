import EffectiveObserver
import ExtensionalRepairSyntax

/- A source-typed structured observer at an arbitrary fixed source carrier B.
Only original source constructors and established structural lemmas are used. -/
namespace TypedStructuredObserver
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody N_form inputNumeral inputNumeral_has app_has)
set_option maxRecDepth 8192

def End : Ty := arr (.param 0) (.param 0)
def Carrier (B : Ty) : Ty := .sigma B End
def seed (a : Poly) : Poly := pairPoly a (.atom .i)
def body (f : Poly) : Poly :=
  pairPoly (.app (pren Nat.succ f) (fstPoly (.var 0))) (.atom .i)
def step (f : Poly) : Poly := abstract (body f)
def run (n f a : Poly) : Poly := .app (.app n (step f)) (seed a)
def observe (n f a : Poly) : Poly := fstPoly (run n f a)

theorem end_form {Γ} (hc : Ctx Γ) : Form Γ End :=
  form_arr (.param hc) (.param hc)

theorem carrier_form {Γ B} (hB : Form Γ B) : Form Γ (Carrier B) :=
  .sigma hB (end_form (.ext (form_ctx hB) hB))

theorem seed_has {Γ B a} (ha : Has Γ a B) : Has Γ (seed a) (Carrier B) :=
  .sigmaIntro (carrier_form (has_form ha)) (end_form (form_ctx (has_form ha)))
    ha (.i (.param (form_ctx (has_form ha))) (end_form (form_ctx (has_form ha))))

theorem body_has {Γ B f} (hf : Has Γ f (arr B B)) :
    Has (Carrier B :: Γ) (body f) (wk (Carrier B)) := by
  have hc := form_ctx (has_form hf)
  have hB := form_pi_domain (has_form hf)
  have hC := carrier_form hB
  have hc' := Ctx.ext hc hC
  have hB' := form_wk hB hc hC
  have hC' : Form (Carrier B :: Γ) (Carrier (wk B)) := carrier_form hB'
  have hs : Has (Carrier B :: Γ) (.var 0) (Carrier (wk B)) := .var hC' .zero
  have hx : Has (Carrier B :: Γ) (fstPoly (.var 0)) (wk B) :=
    .sigmaFst hB' hC' hs
  have hf' : Has (Carrier B :: Γ) (pren Nat.succ f) (arr (wk B) (wk B)) := by
    simpa only [wk, subst_arr] using has_wk hf hc hC
  exact .sigmaIntro hC' (end_form hc')
    (app_has (form_arr hB' hB') hB' hf' hx)
    (.i (.param hc') (end_form hc'))

theorem step_has {Γ B f} (hf : Has Γ f (arr B B)) :
    Has Γ (step f) (arr (Carrier B) (Carrier B)) :=
  .piIntro (form_arr (carrier_form (form_pi_domain (has_form hf)))
      (carrier_form (form_pi_domain (has_form hf))))
    (body_has hf) (scoped_abstract (has_scoped (body_has hf)))

theorem church_instance {Γ C n} (hC : Form Γ C) (hn : Has Γ n N) :
    Has Γ n (arr (arr C C) (arr C C)) := by
  have hi : tinst NBody C = arr (arr C C) (arr C C) := by
    simp only [NBody, tinst, tsubst, mixed_arr, mixed, P01F.cons]
  rw [← hi]
  exact .allElim (N_form (form_ctx (has_form hn))) hC
    (hi.symm ▸ form_arr (form_arr hC hC) (form_arr hC hC)) hn

theorem run_has {Γ B n f a}
    (hn : Has Γ n N) (hf : Has Γ f (arr B B)) (ha : Has Γ a B) :
    Has Γ (run n f a) (Carrier B) := by
  have hC := carrier_form (has_form ha)
  exact app_has (form_arr hC hC) hC
    (app_has (form_arr (form_arr hC hC) (form_arr hC hC))
      (form_arr hC hC) (church_instance hC hn) (step_has hf)) (seed_has ha)

theorem observe_has {Γ B n f a}
    (hn : Has Γ n N) (hf : Has Γ f (arr B B)) (ha : Has Γ a B) :
    Has Γ (observe n f a) B :=
  .sigmaFst (has_form ha) (carrier_form (has_form ha)) (run_has hn hf ha)

/-- This weakening is real: B may contain existing type parameters or dependent
identity endpoints. Its semantic value is held fixed as fresh parameter 0 varies. -/
theorem observe_fresh_has {Γ B n f a}
    (hn : Has Γ n N) (hf : Has Γ f (arr B B)) (ha : Has Γ a B) :
    Has (twkTel Γ) (observe n f a) (twk B) := by
  have hn' : Has (twkTel Γ) n N := by
    simpa only [N, NBody, twk, trename, arr, wk, subst, liftRen] using has_twk hn
  have hf' : Has (twkTel Γ) f (arr (twk B) (twk B)) := by
    simpa only [twk, trename_arr] using has_twk hf
  exact observe_has hn' hf' (has_twk ha)

theorem fixed_all_form {Γ B} (hB : Form Γ B) : Form Γ (.all (twk B)) :=
  .all (form_ctx hB) (form_twk hB)

theorem observe_all_has {Γ B n f a}
    (hn : Has Γ n N) (hf : Has Γ f (arr B B)) (ha : Has Γ a B) :
    Has Γ (observe n f a) (.all (twk B)) :=
  .allIntro (fixed_all_form (has_form ha)) (observe_fresh_has hn hf ha)

/-- Eliminating at ANY formed type gives precisely B, by actual tinst_twk. -/
theorem observe_specialized_has {Γ B n f a T}
    (hn : Has Γ n N) (hf : Has Γ f (arr B B)) (ha : Has Γ a B)
    (hT : Form Γ T) : Has Γ (observe n f a) B := by
  simpa only [tinst_twk] using
    Has.allElim (fixed_all_form (has_form ha)) hT
      (by simpa only [tinst_twk] using has_form ha) (observe_all_has hn hf ha)

theorem observe_same_endpoint_identity {Γ B n f a T}
    (hn : Has Γ n N) (hf : Has Γ f (arr B B)) (ha : Has Γ a B)
    (hT : Form Γ T) :
    HasE Γ (.atom .i) (.identity B (observe n f a) (observe n f a)) := by
  have hd := has_inclusion (observe_has hn hf ha)
  have hs := has_inclusion (observe_specialized_has hn hf ha hT)
  exact .identityIntro (.identity (form_inclusion (has_form ha)) hd hs) hd hs (.refl _)

/-- The general erased re-abstraction cycle, including the required weakening.
This is not the invalid assertion that All B holds B fixed by definition. -/
theorem fixed_reabstract {Γ B p T} (hB : Form Γ B)
    (hp : Has Γ p (.all (twk B))) (hT : Form Γ T) :
    Has Γ p (.all (twk B)) := by
  have he : Has Γ p B := by
    simpa only [tinst_twk] using
      Has.allElim (fixed_all_form hB) hT (by simpa only [tinst_twk] using hB) hp
  exact .allIntro (fixed_all_form hB) (has_twk he)

/-- A visible nontrivial weakening check: outer B=param 0 shifts to param 1. -/
theorem parameter_is_really_shifted : twk (.param 0) = .param 1 := rfl

theorem original_parameter_recovered (T : Ty) :
    tinst (twk (.param 0)) T = .param 0 := tinst_twk _ _

#print axioms observe_has
#print axioms observe_fresh_has
#print axioms observe_all_has
#print axioms observe_specialized_has
#print axioms observe_same_endpoint_identity
#print axioms fixed_reabstract
end TypedStructuredObserver
