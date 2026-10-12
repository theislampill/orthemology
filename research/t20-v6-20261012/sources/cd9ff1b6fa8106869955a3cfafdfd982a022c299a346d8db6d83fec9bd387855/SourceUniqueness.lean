import SectionApplication
namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def RecFamily (f a u : Poly) : Ty := .identity A
  (.app (pren Nat.succ u) (.var 0))
  (.app (.app (.var 0) (pren Nat.succ f)) (pren Nat.succ a))
def RecZero (a u : Poly) : Ty := .identity A (.app u zero) a
def RecStepBody (f u : Poly) : Ty := .identity A
  (.app (pren Nat.succ u) (.app succPoly (.var 0)))
  (.app (pren Nat.succ f) (.app (pren Nat.succ u) (.var 0)))
def RecStep (f u : Poly) : Ty := .pi N (RecStepBody f u)

theorem rec_family_at (f a u n : Poly) : inst (RecFamily f a u) n =
    .identity A (.app u n) (.app (.app n f) a) := by
  simp [RecFamily, inst, A, subst, pren, psub, psub_comp, cons, psub_id]

theorem rec_step_at (f u n : Poly) : inst (RecStepBody f u) n =
    .identity A (.app u (.app succPoly n)) (.app f (.app u n)) := by
  simp [RecStepBody, inst, A, subst, pren, psub, psub_comp, cons, psub_id,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)]

theorem rec_family_form {Γ : Tel} {f a u : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (ha : Has Γ a A) (hu : Has Γ u (arr N A)) :
    Form (N :: Γ) (RecFamily f a u) := by
  have cN := Ctx.ext hc (N_form hc)
  have hf1 : Has (N :: Γ) (pren Nat.succ f) End := has_wk hf hc (N_form hc)
  have ha1 : Has (N :: Γ) (pren Nat.succ a) A := has_wk ha hc (N_form hc)
  have hu1 : Has (N :: Γ) (pren Nat.succ u) (arr N A) := has_wk hu hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  exact .identity (.param cN)
    (app_has (form_arr (N_form cN) (.param cN)) (.param cN) hu1 hn)
    (SourceFoldContract.fold_has cN (.param cN) hn hf1 ha1)

theorem scalar_trans {Γ : Tel} {x y z e d : Poly} (hc : Ctx Γ)
    (hx : Has Γ x A) (hy : Has Γ y A) (hz : Has Γ z A)
    (he : Has Γ e (.identity A x y)) (hd : Has Γ d (.identity A y z)) :
    Has Γ e (.identity A x z) := by
  let P : Ty := .identity A (pren Nat.succ x) (.var 0)
  have cA := Ctx.ext hc (show Form Γ A from .param hc)
  have hx1 : Has (A :: Γ) (pren Nat.succ x) A := has_wk hx hc (show Form Γ A from .param hc)
  have hP : Form (A :: Γ) P := .identity (.param cA) hx1 (.var (.param cA) .zero)
  have at_eq (v : Poly) : inst P v = .identity A x v := by
    simp [P, inst, A, subst, pren, psub, psub_comp, cons, psub_id]
  have h := transport_has_erased hc (.param hc) hP hy hz hd ((at_eq y).symm ▸ he)
  simpa only [at_eq] using h

theorem scalar_congr {Γ : Tel} {f x y e : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (hx : Has Γ x A) (hy : Has Γ y A)
    (he : Has Γ e (.identity A x y)) :
    Has Γ ident (.identity A (.app f x) (.app f y)) := by
  let P : Ty := .identity A (pren Nat.succ (.app f x)) (.app (pren Nat.succ f) (.var 0))
  have cA := Ctx.ext hc (show Form Γ A from .param hc)
  have hfx := app_has (form_arr (.param hc) (.param hc)) (.param hc) hf hx
  have hfx1 : Has (A :: Γ) (pren Nat.succ (.app f x)) A := has_wk hfx hc (show Form Γ A from .param hc)
  have hf1 : Has (A :: Γ) (pren Nat.succ f) End := has_wk hf hc (show Form Γ A from .param hc)
  have hv : Has (A :: Γ) (.var 0) A := .var (.param cA) .zero
  have hP : Form (A :: Γ) P := .identity (.param cA) hfx1
    (app_has (form_arr (.param cA) (.param cA)) (.param cA) hf1 hv)
  have at_eq (v : Poly) : inst P v = .identity A (.app f x) (.app f v) := by
    simp [P, inst, A, subst, pren, psub, psub_comp, cons, psub_id]
  have base : Has Γ ident (.identity A (.app f x) (.app f x)) :=
    .identityIntro (.identity (.param hc) hfx hfx) hfx hfx (.refl _)
  have h := transport_has_erased hc (.param hc) hP hx hy he ((at_eq x).symm ▸ base)
  simpa only [at_eq] using h

theorem rec_step_point {Γ : Tel} {f a u n z p : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (ha : Has Γ a A) (hu : Has Γ u (arr N A)) (hn : Has Γ n N)
    (hz : Has Γ z (RecStep f u))
    (hp : Has Γ p (.identity A (.app u n) (.app (.app n f) a))) :
    Has Γ (.app z n) (.identity A (.app u (.app succPoly n))
      (.app (.app (.app succPoly n) f) a)) := by
  have hsn := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) (succ_has_NT hc) hn
  have hun := app_has (form_arr (N_form hc) (.param hc)) (.param hc) hu hn
  have husn := app_has (form_arr (N_form hc) (.param hc)) (.param hc) hu hsn
  have foldn := SourceFoldContract.fold_has hc (.param hc) hn hf ha
  have foldsn := SourceFoldContract.fold_has hc (.param hc) hsn hf ha
  have f_un := app_has (form_arr (.param hc) (.param hc)) (.param hc) hf hun
  have f_foldn := app_has (form_arr (.param hc) (.param hc)) (.param hc) hf foldn
  have step : Has Γ (.app z n) (.identity A (.app u (.app succPoly n)) (.app f (.app u n))) := by
    have h := Has.piElim (has_form hz)
      ((rec_step_at f u n).symm ▸ Form.identity (.param hc) husn f_un) hz hn
    simpa only [rec_step_at] using h
  have mid := scalar_trans hc husn f_un f_foldn step (scalar_congr hc hf hun foldn hp)
  have last : Has Γ ident (.identity A (.app f (.app (.app n f) a))
      (.app (.app (.app succPoly n) f) a)) :=
    .identityIntro (.identity (.param hc) f_foldn foldsn) f_foldn foldsn (succ_beta n f a).symm
  exact scalar_trans hc husn f_foldn foldsn mid last


theorem rec_family_shift (f a u : Poly) : shiftedFamily (RecFamily f a u) =
    RecFamily (pren Nat.succ f) (pren Nat.succ a) (pren Nat.succ u) := by
  simp [shiftedFamily, RecFamily, A, subst, pren, psub, psub_comp, pup]

theorem rec_step_shift (f u : Poly) : wk (RecStep f u) =
    RecStep (pren Nat.succ f) (pren Nat.succ u) := by
  simp [wk, RecStep, RecStepBody, A, N, NBody, arr, subst, pren, psub, psub_comp, pup,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)]

theorem rec_zero_seed {Γ : Tel} {f a u z : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (ha : Has Γ a A) (hu : Has Γ u (arr N A))
    (hz : Has Γ z (RecZero a u)) : Has Γ z (inst (RecFamily f a u) zero) := by
  have hun := app_has (form_arr (N_form hc) (.param hc)) (.param hc) hu (zero_has_N hc)
  have foldz := SourceFoldContract.fold_has hc (.param hc) (zero_has_N hc) hf ha
  have last : Has Γ ident (.identity A a (.app (.app zero f) a)) :=
    .identityIntro (.identity (.param hc) ha foldz) ha foldz (zero_beta f a).symm
  exact (rec_family_at f a u zero).symm ▸ scalar_trans hc hun ha foldz hz last

def recTotalStep (z : Poly) : Poly := .app (pren Nat.succ z) (fstPoly (.var 0))

theorem rec_total_step_has {Γ : Tel} {f a u z : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (ha : Has Γ a A) (hu : Has Γ u (arr N A))
    (hz : Has Γ z (RecStep f u)) :
    Has (total (RecFamily f a u) :: Γ) (recTotalStep z) (totalStepType (RecFamily f a u)) := by
  let P := RecFamily f a u
  have hP := rec_family_form hc hf ha hu
  have hE : Form Γ (total P) := .sigma (N_form hc) hP
  have cE := Ctx.ext hc hE
  have hEw : Form (total P :: Γ) (.sigma N (shiftedFamily P)) := by
    simpa only [total, wk, subst, N_subst] using form_wk hE hc hE
  have hv : Has (total P :: Γ) (.var 0) (.sigma N (shiftedFamily P)) := by
    have v : Has (total P :: Γ) (.var 0) (wk (total P)) := .var (form_wk hE hc hE) .zero
    simpa only [total, wk, subst, N_subst] using v
  have hn := Has.sigmaFst (N_form cE) hEw hv
  have hp := Has.sigmaSnd hEw (form_inst_source cE (sigma_body_form hEw) hn) hv
  have hp' : Has (total P :: Γ) (sndPoly (.var 0)) (.identity A
      (.app (pren Nat.succ u) (fstPoly (.var 0)))
      (.app (.app (fstPoly (.var 0)) (pren Nat.succ f)) (pren Nat.succ a))) := by
    simpa only [P, rec_family_shift, rec_family_at] using hp
  have hf1 : Has (total P :: Γ) (pren Nat.succ f) End := has_wk hf hc hE
  have ha1 : Has (total P :: Γ) (pren Nat.succ a) A := has_wk ha hc hE
  have hu1 : Has (total P :: Γ) (pren Nat.succ u) (arr N A) := has_wk hu hc hE
  have hz1 : Has (total P :: Γ) (pren Nat.succ z)
      (RecStep (pren Nat.succ f) (pren Nat.succ u)) := rec_step_shift f u ▸ has_wk hz hc hE
  have result := rec_step_point cE hf1 ha1 hu1 hn hz1 hp'
  change Has (total P :: Γ) (recTotalStep z) (inst (shiftedFamily P) nextIndex)
  simpa only [P, rec_family_shift, rec_family_at, nextIndex, recTotalStep] using result

/-- Full pointwise generic recursor uniqueness in the actual unchanged source,
    conditional only on explicit Rigidity and original-Has algebra/equation data.
    No compiler, semantic naturality or q-specific property occurs. -/
theorem recursor_unique_source {Γ : Tel} {f a u z t r n : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (ha : Has Γ a A) (hu : Has Γ u (arr N A))
    (hz : Has Γ z (RecZero a u)) (ht : Has Γ t (RecStep f u))
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    HasE Γ (sndPoly (.app (.app n (totalStep (recTotalStep t))) (totalSeed z)))
      (.identity A (.app u n) (.app (.app n f) a)) := by
  have hP := rec_family_form hc hf ha hu
  have hp := rec_zero_seed hc hf ha hu hz
  have hd := rec_total_step_has hc hf ha hu ht
  have h := dependent_section_explicit hc hP hp hd hr hn
  simpa only [rec_family_at] using h

#print axioms rec_step_point
#print axioms recursor_unique_source
end RigidityInitiality
