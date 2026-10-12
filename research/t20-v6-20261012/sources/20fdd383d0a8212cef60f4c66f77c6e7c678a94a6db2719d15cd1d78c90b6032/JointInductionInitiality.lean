/- Additive Joint port of the credited actual-E total-space proof. -/
import JointInductionSupport
namespace JointCompletion.InductionComputation
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem transport_source {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : CtxJ Γ) (hX : FormJ Γ X) (hP : FormJ (X :: Γ) P)
    (hx : HasJ Γ x X) (hy : HasJ Γ y X)
    (he : HasJ Γ e (.identity X x y)) (hd : HasJ Γ d (inst P x)) :
    HasJ Γ (jPoly d y e) (inst P y) := by
  have hM : FormJ (theta Γ X x) (wk P) :=
    form_wk hP (.ext hc hX) (form_theta_head hc hX hx)
  have at_eq (v r : Poly) : motiveAt (wk P) v r = inst P v := by
    exact subst_wk_cancel P r (cons v Poly.var)
  have h := HasJ.j (hX) (hM)
    ((.identity hX hx hy))
    ((at_eq x (.atom .i) ▸ form_inst_source hc hP hx))
    ((at_eq y e ▸ form_inst_source hc hP hy))
    (hx) (hy) he
    (show HasJ Γ d (motiveAt (wk P) x (.atom .i)) from (at_eq x (.atom .i)).symm ▸ hd)
  simpa only [at_eq] using h

theorem rigidity_elim {Γ : Tel} {r u z s : Poly} (hc : CtxJ Γ)
    (hu : HasJ Γ u NT) (hr : HasJ Γ r Rigidity)
    (hz : HasJ Γ z (ZeroAt u)) (hs : HasJ Γ s (StepAt u)) :
    HasJ Γ (.app (.app (.app r u) z) s) (ResultAt u) := by
  have hZ := zeroAt_formed hc hu
  have hS := stepAt_formed hc hu
  have hR := resultAt_formed hc hu
  have first : HasJ Γ (.app r u) (arr (ZeroAt u) (arr (StepAt u) (ResultAt u))) := by
    have h := HasJ.piElim ((rigidity_formed hc))
      ((show FormJ Γ (inst _ u) from
        (rigidity_inst u).symm ▸ form_arr hZ (form_arr hS hR))) hr (hu)
    simpa only [rigidity_inst] using h
  have second : HasJ Γ (.app (.app r u) z) (arr (StepAt u) (ResultAt u)) := by
    have h := HasJ.piElim ((form_arr hZ (form_arr hS hR)))
      ((show FormJ Γ (inst (wk (arr (StepAt u) (ResultAt u))) z) from
        by simpa only [inst_wk] using form_arr hS hR)) first hz
    simpa only [inst_wk] using h
  have h := HasJ.piElim ((form_arr hS hR))
    ((show FormJ Γ (inst (wk (ResultAt u)) s) from
      by simpa only [inst_wk] using hR)) second hs
  simpa only [inst_wk] using h

theorem rigidity_pointwise {Γ : Tel} {u n e : Poly} (hc : CtxJ Γ)
    (hu : HasJ Γ u NT) (hn : HasJ Γ n N) (he : HasJ Γ e (ResultAt u)) :
    HasJ Γ (jPoly ident u e) (.identity N (.app u n) n) := by
  let M : Ty := .identity N (.app (.var 1) (pren (fun k => k+2) n))
    (pren (fun k => k+2) n)
  have hNT := form_arr (N_form hc) (N_form hc)
  have hi : HasJ Γ ident NT := i_T hc
  have c1 := CtxJ.ext hc hNT
  have hP := form_theta_head hc hNT hi
  have ct := ctx_theta hc hNT hi
  have hn2 : HasJ (theta Γ NT ident) (pren (fun k => k+2) n) N := by
    simpa only [wk, N_subst, pren, psub_comp, psub] using
      has_wk (has_wk hn hc hNT) c1 hP
  have hv : HasJ (theta Γ NT ident) (.var 1) NT :=
    .var (form_arr (N_form ct) (N_form ct)) (.succ .zero)
  have hM : FormJ (theta Γ NT ident) M := .identity (N_form ct)
    (app_has (form_arr (N_form ct) (N_form ct)) (N_form ct) hv hn2) hn2
  have at_eq (v r : Poly) : motiveAt M v r = .identity N (.app v n) n := by
    simp [M, motiveAt, N, NBody, arr, subst, wk, psub, pren, psub_comp, cons]
  have hin := app_has hNT (N_form hc) hi hn
  have hun := app_has hNT (N_form hc) hu hn
  have hb : FormJ Γ (.identity N (.app ident n) n) := .identity (N_form hc) hin hn
  have ht : FormJ Γ (.identity N (.app u n) n) := .identity (N_form hc) hun hn
  have hd : HasJ Γ ident (.identity N (.app ident n) n) := identityIntro_raw hb hin hn (.i n)
  have h := HasJ.j (hNT) (hM)
    ((resultAt_formed hc hu))
    (((at_eq ident ident).symm ▸ hb))
    (((at_eq u e).symm ▸ ht))
    (hi) (hu) he
    (show HasJ Γ ident (motiveAt M ident ident) from (at_eq ident ident).symm ▸ hd)
  simpa only [at_eq] using h


theorem sigma_body_form {Γ : Tel} {X P : Ty} (h : FormJ Γ (.sigma X P)) :
    FormJ (X :: Γ) P := (JointCompletion.DependentExtraction.form_sigma_inv h).2


theorem total_step_has {Γ : Tel} {P : Ty} {d : Poly} (hc : CtxJ Γ)
    (hP : FormJ (N :: Γ) P) (hd : HasJ (total P :: Γ) d (totalStepType P)) :
    HasJ Γ (totalStep d) (arr (total P) (total P)) := by
  have hE : FormJ Γ (total P) := .sigma (N_form hc) hP
  have cE := CtxJ.ext hc hE
  have hEw : FormJ (total P :: Γ) (wk (total P)) := form_wk hE hc hE
  have hEw' : FormJ (total P :: Γ) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hEw
  have hv : HasJ (total P :: Γ) (.var 0) (wk (total P)) := .var hEw .zero
  have hv' : HasJ (total P :: Γ) (.var 0) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hv
  have hfst := HasJ.sigmaFst (N_form cE) hEw' hv'
  have hnext : HasJ (total P :: Γ) nextIndex N :=
    app_has (form_arr (N_form cE) (N_form cE)) (N_form cE) (succ_has_NT cE) hfst
  have hleaf := form_inst_source cE (sigma_body_form hEw') hnext
  have hb := HasJ.sigmaIntro hEw' hleaf hnext hd
  apply HasJ.piIntro (form_arr hE hE)
  · simpa only [total, wk, subst, N_subst] using hb
  · exact scoped_abstract (has_scoped hb)


theorem total_seed_has {Γ : Tel} {P : Ty} {p : Poly} (hc : CtxJ Γ)
    (hP : FormJ (N :: Γ) P) (hp : HasJ Γ p (inst P zero)) :
    HasJ Γ (totalSeed p) (total P) :=
  .sigmaIntro (.sigma (N_form hc) hP) (form_inst_source hc hP (zero_has_N hc))
    (zero_has_N hc) hp


theorem projectedFold_has {Γ : Tel} {P : Ty} {D a : Poly} (hc : CtxJ Γ)
    (hP : FormJ (N :: Γ) P) (hD : HasJ Γ D (arr (total P) (total P)))
    (ha : HasJ Γ a (total P)) : HasJ Γ (projectedFold D a) NT := by
  have hE : FormJ Γ (total P) := .sigma (N_form hc) hP
  have cN := CtxJ.ext hc (N_form hc)
  have hEw := form_wk hE hc (N_form hc)
  have hD1 : HasJ (N :: Γ) (pren Nat.succ D) (arr (wk (total P)) (wk (total P))) := by
    simpa only [wk, subst_arr] using has_wk hD hc (N_form hc)
  have ha1 := has_wk ha hc (N_form hc)
  have hn : HasJ (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have run := fold_has cN hEw hn hD1 ha1
  have hEw' : FormJ (N :: Γ) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hEw
  have run' : HasJ (N :: Γ) (.app (.app (.var 0) (pren Nat.succ D)) (pren Nat.succ a))
      (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using run
  have hb := HasJ.sigmaFst (N_form cN) hEw' run'
  exact .piIntro (form_arr (N_form hc) (N_form hc)) hb (scoped_abstract (has_scoped hb))


theorem projected_zero_evidence {Γ : Tel} {P : Ty} {d p : Poly} (hc : CtxJ Γ)
    (hP : FormJ (N :: Γ) P) (hp : HasJ Γ p (inst P zero))
    (hd : HasJ (total P :: Γ) d (totalStepType P)) :
    HasJ Γ ident (ZeroAt (projectedFold (totalStep d) (totalSeed p))) := by
  have hu := projectedFold_has hc hP (total_step_has hc hP hd) (total_seed_has hc hP hp)
  have hz := zero_has_N hc
  have huz := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hz
  exact identityIntro_raw (zeroAt_formed hc hu) huz hz (projected_zero d p)


theorem projected_step_evidence {Γ : Tel} {P : Ty} {d p : Poly} (hc : CtxJ Γ)
    (hP : FormJ (N :: Γ) P) (hp : HasJ Γ p (inst P zero))
    (hd : HasJ (total P :: Γ) d (totalStepType P)) :
    HasJ Γ (abstract ident) (StepAt (projectedFold (totalStep d) (totalSeed p))) := by
  let u := projectedFold (totalStep d) (totalSeed p)
  have hu := projectedFold_has hc hP (total_step_has hc hP hd) (total_seed_has hc hP hp)
  have c1 := CtxJ.ext hc (N_form hc)
  have hu1 : HasJ (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : HasJ (N :: Γ) (.var 0) N := .var (N_form c1) .zero
  have hs := succ_has_NT c1
  have sn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs hn
  have un := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 hn
  have left := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 sn
  have right := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs un
  apply HasJ.piIntro (stepAt_formed hc hu)
  · apply identityIntro_raw (.identity (N_form c1) left right) left right
    simp only [u, projected_ren]
    exact projected_succ _ _ _
  · exact scoped_abstract trivial


theorem nat_identity_trans {Γ : Tel} {x y z e d : Poly} (hc : CtxJ Γ)
    (hx : HasJ Γ x N) (hy : HasJ Γ y N) (hz : HasJ Γ z N)
    (he : HasJ Γ e (.identity N x y)) (hd : HasJ Γ d (.identity N y z)) :
    HasJ Γ (jPoly e z d) (.identity N x z) := by
  let P : Ty := .identity N (pren Nat.succ x) (.var 0)
  have cN := CtxJ.ext hc (N_form hc)
  have hx1 : HasJ (N :: Γ) (pren Nat.succ x) N := has_wk hx hc (N_form hc)
  have hP : FormJ (N :: Γ) P := .identity (N_form cN) hx1 (.var (N_form cN) .zero)
  have at_eq (v : Poly) : inst P v = .identity N x v := by
    simp [P, inst, subst, N, NBody, arr, wk, pren, psub, psub_comp, cons]
  have h := transport_source hc (N_form hc) hP hy hz hd
    (show HasJ Γ e (inst P y) from (at_eq y).symm ▸ he)
  simpa only [at_eq] using h

theorem dependent_section_from_rigidity {Γ : Tel} {P : Ty} {p d r n : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero))
    (hd : HasJ (total P :: Γ) d (totalStepType P))
    (hr : HasJ Γ r Rigidity) (hn : HasJ Γ n N) :
    ∃ e, HasJ Γ e (inst P n) := by
  let D := totalStep d
  let a := totalSeed p
  let u := projectedFold D a
  let run : Poly := .app (.app n D) a
  have hD := total_step_has hc hP hd
  have ha := total_seed_has hc hP hp
  have hu : HasJ Γ u NT := projectedFold_has hc hP hD ha
  have hE : FormJ Γ (total P) := .sigma (N_form hc) hP
  have hrun : HasJ Γ run (total P) := fold_has hc hE hn hD ha
  have hfst : HasJ Γ (fstPoly run) N := .sigmaFst (N_form hc) hE hrun
  have hsnd : HasJ Γ (sndPoly run) (inst P (fstPoly run)) :=
    .sigmaSnd hE (form_inst_source hc hP hfst) hrun
  have huN := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hn
  have rid := rigidity_elim hc hu hr
    ((projected_zero_evidence hc hP hp hd))
    ((projected_step_evidence hc hP hp hd))
  have point := rigidity_pointwise hc hu hn rid
  have link : HasJ Γ ident (.identity N (fstPoly run) (.app u n)) :=
    identityIntro_raw (.identity (N_form hc) hfst huN) hfst huN (projectedFold_beta D a n).symm
  have back := nat_identity_trans hc hfst huN hn (link) point
  exact ⟨_, transport_source hc (N_form hc) hP hfst hn back (hsnd)⟩


end JointCompletion.InductionComputation
