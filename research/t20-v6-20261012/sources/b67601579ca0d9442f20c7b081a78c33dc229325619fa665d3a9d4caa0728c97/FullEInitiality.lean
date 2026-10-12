/- Additive actual-E support for the literal retained total-space construction. -/
import FullESupport
namespace RigidityInitiality.FullE
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem transport_source {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : CtxE Γ) (hX : FormE Γ X) (hP : FormE (X :: Γ) P)
    (hx : HasE Γ x X) (hy : HasE Γ y X)
    (he : HasE Γ e (.identity X x y)) (hd : HasE Γ d (inst P x)) :
    HasE Γ (jPoly d y e) (inst P y) := by
  have hM : FormE (theta Γ X x) (wk P) :=
    form_wk hP (.ext hc hX) (form_theta_head hc hX hx)
  have at_eq (v r : Poly) : motiveAt (wk P) v r = inst P v := by
    exact subst_wk_cancel P r (cons v Poly.var)
  have h := HasE.j (hX) (hM)
    ((.identity hX hx hy))
    ((at_eq x (.atom .i) ▸ form_inst_source hc hP hx))
    ((at_eq y e ▸ form_inst_source hc hP hy))
    (hx) (hy) he
    (show HasE Γ d (motiveAt (wk P) x (.atom .i)) from (at_eq x (.atom .i)).symm ▸ hd)
  simpa only [at_eq] using h

theorem rigidity_elim {Γ : Tel} {r u z s : Poly} (hc : CtxE Γ)
    (hu : HasE Γ u NT) (hr : HasE Γ r Rigidity)
    (hz : HasE Γ z (ZeroAt u)) (hs : HasE Γ s (StepAt u)) :
    HasE Γ (.app (.app (.app r u) z) s) (ResultAt u) := by
  have hZ := zeroAt_formed hc hu
  have hS := stepAt_formed hc hu
  have hR := resultAt_formed hc hu
  have first : HasE Γ (.app r u) (arr (ZeroAt u) (arr (StepAt u) (ResultAt u))) := by
    have h := HasE.piElim ((rigidity_formed hc))
      ((show FormE Γ (inst _ u) from
        (rigidity_inst u).symm ▸ form_arr hZ (form_arr hS hR))) hr (hu)
    simpa only [rigidity_inst] using h
  have second : HasE Γ (.app (.app r u) z) (arr (StepAt u) (ResultAt u)) := by
    have h := HasE.piElim ((form_arr hZ (form_arr hS hR)))
      ((show FormE Γ (inst (wk (arr (StepAt u) (ResultAt u))) z) from
        by simpa only [inst_wk] using form_arr hS hR)) first hz
    simpa only [inst_wk] using h
  have h := HasE.piElim ((form_arr hS hR))
    ((show FormE Γ (inst (wk (ResultAt u)) s) from
      by simpa only [inst_wk] using hR)) second hs
  simpa only [inst_wk] using h

theorem rigidity_pointwise {Γ : Tel} {u n e : Poly} (hc : CtxE Γ)
    (hu : HasE Γ u NT) (hn : HasE Γ n N) (he : HasE Γ e (ResultAt u)) :
    HasE Γ (jPoly ident u e) (.identity N (.app u n) n) := by
  let M : Ty := .identity N (.app (.var 1) (pren (fun k => k+2) n))
    (pren (fun k => k+2) n)
  have hNT := form_arr (N_form hc) (N_form hc)
  have hi : HasE Γ ident NT := i_T hc
  have c1 := CtxE.ext hc hNT
  have hP := form_theta_head hc hNT hi
  have ct := ctx_theta hc hNT hi
  have hn2 : HasE (theta Γ NT ident) (pren (fun k => k+2) n) N := by
    simpa only [wk, N_subst, pren, psub_comp, psub] using
      has_wk (has_wk hn hc hNT) c1 hP
  have hv : HasE (theta Γ NT ident) (.var 1) NT :=
    .var (form_arr (N_form ct) (N_form ct)) (.succ .zero)
  have hM : FormE (theta Γ NT ident) M := .identity (N_form ct)
    (app_has (form_arr (N_form ct) (N_form ct)) (N_form ct) hv hn2) hn2
  have at_eq (v r : Poly) : motiveAt M v r = .identity N (.app v n) n := by
    simp [M, motiveAt, N, NBody, arr, subst, wk, psub, pren, psub_comp, cons]
  have hin := app_has hNT (N_form hc) hi hn
  have hun := app_has hNT (N_form hc) hu hn
  have hb : FormE Γ (.identity N (.app ident n) n) := .identity (N_form hc) hin hn
  have ht : FormE Γ (.identity N (.app u n) n) := .identity (N_form hc) hun hn
  have hd : HasE Γ ident (.identity N (.app ident n) n) := identityIntro_raw hb hin hn (.i n)
  have h := HasE.j (hNT) (hM)
    ((resultAt_formed hc hu))
    (((at_eq ident ident).symm ▸ hb))
    (((at_eq u e).symm ▸ ht))
    (hi) (hu) he
    (show HasE Γ ident (motiveAt M ident ident) from (at_eq ident ident).symm ▸ hd)
  simpa only [at_eq] using h


theorem sigma_body_form {Γ : Tel} {X P : Ty} (h : FormE Γ (.sigma X P)) :
    FormE (X :: Γ) P := by cases h; assumption


theorem total_step_has {Γ : Tel} {P : Ty} {d : Poly} (hc : CtxE Γ)
    (hP : FormE (N :: Γ) P) (hd : HasE (total P :: Γ) d (totalStepType P)) :
    HasE Γ (totalStep d) (arr (total P) (total P)) := by
  have hE : FormE Γ (total P) := .sigma (N_form hc) hP
  have cE := CtxE.ext hc hE
  have hEw : FormE (total P :: Γ) (wk (total P)) := form_wk hE hc hE
  have hEw' : FormE (total P :: Γ) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hEw
  have hv : HasE (total P :: Γ) (.var 0) (wk (total P)) := .var hEw .zero
  have hv' : HasE (total P :: Γ) (.var 0) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hv
  have hfst := HasE.sigmaFst (N_form cE) hEw' hv'
  have hnext : HasE (total P :: Γ) nextIndex N :=
    app_has (form_arr (N_form cE) (N_form cE)) (N_form cE) (succ_has_NT cE) hfst
  have hleaf := form_inst_source cE (sigma_body_form hEw') hnext
  have hb := HasE.sigmaIntro hEw' hleaf hnext hd
  apply HasE.piIntro (form_arr hE hE)
  · simpa only [total, wk, subst, N_subst] using hb
  · exact scoped_abstract (has_scoped hb)


theorem total_seed_has {Γ : Tel} {P : Ty} {p : Poly} (hc : CtxE Γ)
    (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero)) :
    HasE Γ (totalSeed p) (total P) :=
  .sigmaIntro (.sigma (N_form hc) hP) (form_inst_source hc hP (zero_has_N hc))
    (zero_has_N hc) hp


theorem projectedFold_has {Γ : Tel} {P : Ty} {D a : Poly} (hc : CtxE Γ)
    (hP : FormE (N :: Γ) P) (hD : HasE Γ D (arr (total P) (total P)))
    (ha : HasE Γ a (total P)) : HasE Γ (projectedFold D a) NT := by
  have hE : FormE Γ (total P) := .sigma (N_form hc) hP
  have cN := CtxE.ext hc (N_form hc)
  have hEw := form_wk hE hc (N_form hc)
  have hD1 : HasE (N :: Γ) (pren Nat.succ D) (arr (wk (total P)) (wk (total P))) := by
    simpa only [wk, subst_arr] using has_wk hD hc (N_form hc)
  have ha1 := has_wk ha hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have run := fold_has cN hEw hn hD1 ha1
  have hEw' : FormE (N :: Γ) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hEw
  have run' : HasE (N :: Γ) (.app (.app (.var 0) (pren Nat.succ D)) (pren Nat.succ a))
      (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using run
  have hb := HasE.sigmaFst (N_form cN) hEw' run'
  exact .piIntro (form_arr (N_form hc) (N_form hc)) hb (scoped_abstract (has_scoped hb))


theorem projected_zero_evidence {Γ : Tel} {P : Ty} {d p : Poly} (hc : CtxE Γ)
    (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hd : HasE (total P :: Γ) d (totalStepType P)) :
    HasE Γ ident (ZeroAt (projectedFold (totalStep d) (totalSeed p))) := by
  have hu := projectedFold_has hc hP (total_step_has hc hP hd) (total_seed_has hc hP hp)
  have hz := zero_has_N hc
  have huz := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hz
  exact identityIntro_raw (zeroAt_formed hc hu) huz hz (projected_zero d p)


theorem projected_step_evidence {Γ : Tel} {P : Ty} {d p : Poly} (hc : CtxE Γ)
    (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hd : HasE (total P :: Γ) d (totalStepType P)) :
    HasE Γ (abstract ident) (StepAt (projectedFold (totalStep d) (totalSeed p))) := by
  let u := projectedFold (totalStep d) (totalSeed p)
  have hu := projectedFold_has hc hP (total_step_has hc hP hd) (total_seed_has hc hP hp)
  have c1 := CtxE.ext hc (N_form hc)
  have hu1 : HasE (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form c1) .zero
  have hs := succ_has_NT c1
  have sn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs hn
  have un := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 hn
  have left := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 sn
  have right := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs un
  apply HasE.piIntro (stepAt_formed hc hu)
  · apply identityIntro_raw (.identity (N_form c1) left right) left right
    simp only [u, projected_ren]
    exact projected_succ _ _ _
  · exact scoped_abstract trivial


theorem nat_identity_trans {Γ : Tel} {x y z e d : Poly} (hc : CtxE Γ)
    (hx : HasE Γ x N) (hy : HasE Γ y N) (hz : HasE Γ z N)
    (he : HasE Γ e (.identity N x y)) (hd : HasE Γ d (.identity N y z)) :
    HasE Γ (jPoly e z d) (.identity N x z) := by
  let P : Ty := .identity N (pren Nat.succ x) (.var 0)
  have cN := CtxE.ext hc (N_form hc)
  have hx1 : HasE (N :: Γ) (pren Nat.succ x) N := has_wk hx hc (N_form hc)
  have hP : FormE (N :: Γ) P := .identity (N_form cN) hx1 (.var (N_form cN) .zero)
  have at_eq (v : Poly) : inst P v = .identity N x v := by
    simp [P, inst, subst, N, NBody, arr, wk, pren, psub, psub_comp, cons]
  have h := transport_source hc (N_form hc) hP hy hz hd
    (show HasE Γ e (inst P y) from (at_eq y).symm ▸ he)
  simpa only [at_eq] using h

theorem dependent_section_from_rigidity {Γ : Tel} {P : Ty} {p d r n : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P)
    (hp : HasE Γ p (inst P zero))
    (hd : HasE (total P :: Γ) d (totalStepType P))
    (hr : HasE Γ r Rigidity) (hn : HasE Γ n N) :
    ∃ e, HasE Γ e (inst P n) := by
  let D := totalStep d
  let a := totalSeed p
  let u := projectedFold D a
  let run : Poly := .app (.app n D) a
  have hD := total_step_has hc hP hd
  have ha := total_seed_has hc hP hp
  have hu : HasE Γ u NT := projectedFold_has hc hP hD ha
  have hE : FormE Γ (total P) := .sigma (N_form hc) hP
  have hrun : HasE Γ run (total P) := fold_has hc hE hn hD ha
  have hfst : HasE Γ (fstPoly run) N := .sigmaFst (N_form hc) hE hrun
  have hsnd : HasE Γ (sndPoly run) (inst P (fstPoly run)) :=
    .sigmaSnd hE (form_inst_source hc hP hfst) hrun
  have huN := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hn
  have rid := rigidity_elim hc hu hr
    ((projected_zero_evidence hc hP hp hd))
    ((projected_step_evidence hc hP hp hd))
  have point := rigidity_pointwise hc hu hn rid
  have link : HasE Γ ident (.identity N (fstPoly run) (.app u n)) :=
    identityIntro_raw (.identity (N_form hc) hfst huN) hfst huN (projectedFold_beta D a n).symm
  have back := nat_identity_trans hc hfst huN hn (link) point
  exact ⟨_, transport_source hc (N_form hc) hP hfst hn back (hsnd)⟩


end RigidityInitiality.FullE
