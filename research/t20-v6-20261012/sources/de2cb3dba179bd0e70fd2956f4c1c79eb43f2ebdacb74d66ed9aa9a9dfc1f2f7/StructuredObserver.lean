import EffectiveObserver
import ExtensionalRepairSyntax

/- An actual source observer tying different structured carrier instances to
one type-independent Raw result. It is not the missing scalar projection bridge. -/
namespace TypeIndexedStructuredObserver
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody N_form)
set_option maxRecDepth 8192

def A : Ty := .param 0
def End : Ty := arr A A
def Carrier : Ty := .sigma .raw End
def Γ : Tel := [.raw,.raw,N]
def seed : Poly := pairPoly (.var 0) (.atom .i)
def body : Poly := pairPoly (.app (.var 2) (fstPoly (.var 0))) (.atom .i)
def step : Poly := abstract body
def run : Poly := .app (.app (.var 2) step) seed
def observe : Poly := fstPoly run

theorem end_form {Δ} (hc : Ctx Δ) : Form Δ End :=
  form_arr (.param hc) (.param hc)
theorem carrier_form {Δ} (hc : Ctx Δ) : Form Δ Carrier :=
  .sigma (.raw hc) (end_form (.ext hc (.raw hc)))
theorem context : Ctx Γ := by
  have c1 : Ctx [N] := .ext .nil (N_form .nil)
  have c2 : Ctx [.raw,N] := .ext c1 (.raw c1)
  exact .ext c2 (.raw c2)

theorem seed_has : Has Γ seed Carrier :=
  .sigmaIntro (carrier_form context) (end_form context)
    (.var (.raw context) .zero) (.i (.param context) (end_form context))

theorem body_has : Has (Carrier :: Γ) body Carrier := by
  have c : Ctx (Carrier :: Γ) := .ext context (carrier_form context)
  have hs : Has (Carrier :: Γ) (.var 0) Carrier := .var (carrier_form c) .zero
  have hf : Has (Carrier :: Γ) (.var 2) .raw := .var (.raw c) (.succ (.succ .zero))
  have hx : Has (Carrier :: Γ) (fstPoly (.var 0)) .raw :=
    .sigmaFst (.raw c) (carrier_form c) hs
  exact .sigmaIntro (carrier_form c) (end_form c)
    (.rawApp (.raw c) hf hx) (.i (.param c) (end_form c))

theorem step_has : Has Γ step (arr Carrier Carrier) :=
  .piIntro (form_arr (carrier_form context) (carrier_form context)) body_has
    (scoped_abstract (has_scoped body_has))

theorem n_instance : Has Γ (.var 2) (arr (arr Carrier Carrier) (arr Carrier Carrier)) := by
  have hn : Has Γ (.var 2) N := .var (N_form context) (.succ (.succ .zero))
  exact .allElim (N_form context) (carrier_form context)
    (form_arr (form_arr (carrier_form context) (carrier_form context))
      (form_arr (carrier_form context) (carrier_form context))) hn

theorem run_has : Has Γ run Carrier :=
  Has.piElim (form_arr (carrier_form context) (carrier_form context)) (carrier_form context)
    (Has.piElim (form_arr (form_arr (carrier_form context) (carrier_form context))
      (form_arr (carrier_form context) (carrier_form context)))
      (form_arr (carrier_form context) (carrier_form context)) n_instance step_has) seed_has

theorem observe_has : HasE Γ observe .raw :=
  has_inclusion (.sigmaFst (.raw context) (carrier_form context) run_has)

/-- Its result and surrounding telescope do not mention the fresh parameter. -/
theorem observe_all_has : HasE Γ observe (.all .raw) :=
  .allIntro (.all (ctx_inclusion context) (.raw (ctx_inclusion context))) observe_has

/-- Source allElim retains the literal same observer polynomial. -/
theorem observe_specialized_has : HasE Γ observe .raw :=
  .allElim (.all (ctx_inclusion context) (.raw (ctx_inclusion context)))
    (.raw (ctx_inclusion context)) (.raw (ctx_inclusion context)) observe_all_has

/-- Actual identity syntax sees the same endpoint under both source routes. -/
theorem observe_same_endpoint_identity :
    HasE Γ (.atom .i) (.identity .raw observe observe) :=
  .identityIntro (.identity (.raw (ctx_inclusion context))
    observe_has observe_specialized_has) observe_has observe_specialized_has (.refl _)

/-- Actual source Raw assignments: a=I and f=K K. The numeral assignment is
only a control on the observer's separating capability, not a nonparametric n. -/
def probeEnv (k : Nat) : Env :=
  P01F.cons .i (P01F.cons (.app .k .k)
    (P01F.cons (eval (EffectiveCompleteness.inputNumeral k) zeroEnv) zeroEnv))

theorem raw_zero_observation : Conv (eval observe (probeEnv 0)) .i := by
  have h := Conv.left (EffectiveCompleteness.inputNumeral_applied 0
    (eval step (probeEnv 0)) (eval seed (probeEnv 0)) zeroEnv) .k
  exact h.trans (OrthemologyV3.pair_first .i .i)

theorem raw_one_observation : Conv (eval observe (probeEnv 1)) .k := by
  have h := Conv.left (EffectiveCompleteness.inputNumeral_applied 1
    (eval step (probeEnv 1)) (eval seed (probeEnv 1)) zeroEnv) .k
  have hb := Conv.left (P01Source.red_conv
    (abstraction_beta body (probeEnv 1) (eval seed (probeEnv 1)))) .k
  have hp := OrthemologyV3.pair_first
    (.app (.app .k .k) (OrthemologyV3.firstTerm (OrthemologyV3.pairTerm .i .i))) .i
  exact h.trans (hb.trans (hp.trans (.step (.k .k _))))

theorem raw_i_k_distinct : ¬ Conv Term.i Term.k := by
  intro h
  have e := P01Source.normal_unique (by intro t ht; cases ht)
    (by intro t ht; cases ht) h
  cases e

/-- Separation in the ACTUAL retained Raw conversion, not a finite toy model. -/
theorem raw_observations_distinct :
    ¬ Conv (eval observe (probeEnv 0)) (eval observe (probeEnv 1)) := by
  intro h
  exact raw_i_k_distinct
    (raw_zero_observation.symm.trans (h.trans raw_one_observation))

#print axioms observe_has
#print axioms observe_all_has
#print axioms observe_same_endpoint_identity
#print axioms raw_zero_observation
#print axioms raw_one_observation
#print axioms raw_observations_distinct
end TypeIndexedStructuredObserver
