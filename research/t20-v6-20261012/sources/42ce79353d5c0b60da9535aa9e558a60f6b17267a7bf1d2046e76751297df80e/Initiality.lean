import SourceRigidity
import AllStructural
namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem form_inst_source {Γ : Tel} {X P : Ty} {x : Poly}
    (hc : Ctx Γ) (hP : Form (X :: Γ) P) (hx : Has Γ x X) : Form Γ (inst P x) := by
  have s : MixedSubstitution (X :: Γ) Γ (cons x Poly.var) Ty.param := by
    refine ⟨fun _ => .param hc, ?_⟩
    intro n A h
    cases h with
    | zero => simpa only [mixed_param, subst_wk_cancel, subst_id, cons] using hx
    | succ h => simpa only [mixed_param, subst_wk_cancel, subst_id, cons] using
        (Has.var (lookup_form hc h) h)
  simpa only [mixed_param] using form_mixed hP hc s

theorem transport_source {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : Ctx Γ) (hX : Form Γ X) (hP : Form (X :: Γ) P)
    (hx : Has Γ x X) (hy : Has Γ y X)
    (he : HasE Γ e (.identity X x y)) (hd : HasE Γ d (inst P x)) :
    HasE Γ (jPoly d y e) (inst P y) := by
  have hM : Form (theta Γ X x) (wk P) :=
    form_wk hP (.ext hc hX) (form_theta_head hc hX hx)
  have at_eq (v r : Poly) : motiveAt (wk P) v r = inst P v := by
    exact subst_wk_cancel P r (cons v Poly.var)
  have h := HasE.j (form_inclusion hX) (form_inclusion hM)
    (form_inclusion (.identity hX hx hy))
    (form_inclusion (at_eq x (.atom .i) ▸ form_inst_source hc hP hx))
    (form_inclusion (at_eq y e ▸ form_inst_source hc hP hy))
    (has_inclusion hx) (has_inclusion hy) he
    (show HasE Γ d (motiveAt (wk P) x (.atom .i)) from (at_eq x (.atom .i)).symm ▸ hd)
  simpa only [at_eq] using h

/-- Same-source elimination, for any Peano endomorphism, of the explicit
    rigidity hypothesis. No compiler, semantic relation or new rule occurs. -/
theorem rigidity_elim {Γ : Tel} {r u z s : Poly} (hc : Ctx Γ)
    (hu : Has Γ u NT) (hr : HasE Γ r Rigidity)
    (hz : HasE Γ z (ZeroAt u)) (hs : HasE Γ s (StepAt u)) :
    HasE Γ (.app (.app (.app r u) z) s) (ResultAt u) := by
  have hZ := zeroAt_formed hc hu
  have hS := stepAt_formed hc hu
  have hR := resultAt_formed hc hu
  have first : HasE Γ (.app r u) (arr (ZeroAt u) (arr (StepAt u) (ResultAt u))) := by
    have h := HasE.piElim (form_inclusion (rigidity_formed hc))
      (form_inclusion (show Form Γ (inst _ u) from
        (rigidity_inst u).symm ▸ form_arr hZ (form_arr hS hR))) hr (has_inclusion hu)
    simpa only [rigidity_inst] using h
  have second : HasE Γ (.app (.app r u) z) (arr (StepAt u) (ResultAt u)) := by
    have h := HasE.piElim (form_inclusion (form_arr hZ (form_arr hS hR)))
      (form_inclusion (show Form Γ (inst (wk (arr (StepAt u) (ResultAt u))) z) from
        by simpa only [inst_wk] using form_arr hS hR)) first hz
    simpa only [inst_wk] using h
  have h := HasE.piElim (form_inclusion (form_arr hS hR))
    (form_inclusion (show Form Γ (inst (wk (ResultAt u)) s) from
      by simpa only [inst_wk] using hR)) second hs
  simpa only [inst_wk] using h

/-- Evaluate a function equality with orientation suitable for dependent
    transport back from the total-space projection to the input. -/
theorem rigidity_pointwise {Γ : Tel} {u n e : Poly} (hc : Ctx Γ)
    (hu : Has Γ u NT) (hn : Has Γ n N) (he : HasE Γ e (ResultAt u)) :
    HasE Γ (jPoly ident u e) (.identity N (.app u n) n) := by
  let M : Ty := .identity N (.app (.var 1) (pren (fun k => k+2) n))
    (pren (fun k => k+2) n)
  have hNT := form_arr (N_form hc) (N_form hc)
  have hi : Has Γ ident NT := ExactScalarFusion.i_T hc
  have c1 := Ctx.ext hc hNT
  have hP := form_theta_head hc hNT hi
  have ct := ctx_theta hc hNT hi
  have hn2 : Has (theta Γ NT ident) (pren (fun k => k+2) n) N := by
    simpa only [wk, N_subst, pren, psub_comp, psub] using
      has_wk (has_wk hn hc hNT) c1 hP
  have hv : Has (theta Γ NT ident) (.var 1) NT :=
    .var (form_arr (N_form ct) (N_form ct)) (.succ .zero)
  have hM : Form (theta Γ NT ident) M := .identity (N_form ct)
    (app_has (form_arr (N_form ct) (N_form ct)) (N_form ct) hv hn2) hn2
  have at_eq (v r : Poly) : motiveAt M v r = .identity N (.app v n) n := by
    simp [M, motiveAt, N, NBody, arr, subst, wk, psub, pren, psub_comp, cons]
  have hin := app_has hNT (N_form hc) hi hn
  have hun := app_has hNT (N_form hc) hu hn
  have hb : Form Γ (.identity N (.app ident n) n) := .identity (N_form hc) hin hn
  have ht : Form Γ (.identity N (.app u n) n) := .identity (N_form hc) hun hn
  have hd : Has Γ ident (.identity N (.app ident n) n) := .identityIntro hb hin hn (.i n)
  have h := HasE.j (form_inclusion hNT) (form_inclusion hM)
    (form_inclusion (resultAt_formed hc hu))
    (form_inclusion ((at_eq ident ident).symm ▸ hb))
    (form_inclusion ((at_eq u e).symm ▸ ht))
    (has_inclusion hi) (has_inclusion hu) he
    (show HasE Γ ident (motiveAt M ident ident) from (at_eq ident ident).symm ▸ has_inclusion hd)
  simpa only [at_eq] using h

def total (P : Ty) : Ty := .sigma N P

def nextIndex : Poly := .app succPoly (fstPoly (.var 0))
def totalStep (d : Poly) : Poly := abstract (pairPoly nextIndex d)
def totalSeed (p : Poly) : Poly := pairPoly zero p

def totalStepType (P : Ty) : Ty :=
  inst (subst (pup (fun k => .var (k+1))) P) nextIndex

theorem sigma_body_form {Γ : Tel} {X P : Ty} (h : Form Γ (.sigma X P)) :
    Form (X :: Γ) P := by cases h; assumption

theorem total_step_has {Γ : Tel} {P : Ty} {d : Poly} (hc : Ctx Γ)
    (hP : Form (N :: Γ) P) (hd : Has (total P :: Γ) d (totalStepType P)) :
    Has Γ (totalStep d) (arr (total P) (total P)) := by
  have hE : Form Γ (total P) := .sigma (N_form hc) hP
  have cE := Ctx.ext hc hE
  have hEw : Form (total P :: Γ) (wk (total P)) := form_wk hE hc hE
  have hEw' : Form (total P :: Γ) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hEw
  have hv : Has (total P :: Γ) (.var 0) (wk (total P)) := .var hEw .zero
  have hv' : Has (total P :: Γ) (.var 0) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hv
  have hfst := Has.sigmaFst (N_form cE) hEw' hv'
  have hnext : Has (total P :: Γ) nextIndex N :=
    app_has (form_arr (N_form cE) (N_form cE)) (N_form cE) (succ_has_NT cE) hfst
  have hleaf := form_inst_source cE (sigma_body_form hEw') hnext
  have hb := Has.sigmaIntro hEw' hleaf hnext hd
  apply Has.piIntro (form_arr hE hE)
  · simpa only [total, wk, subst, N_subst] using hb
  · exact scoped_abstract (has_scoped hb)

theorem total_seed_has {Γ : Tel} {P : Ty} {p : Poly} (hc : Ctx Γ)
    (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero)) :
    Has Γ (totalSeed p) (total P) :=
  .sigmaIntro (.sigma (N_form hc) hP) (form_inst_source hc hP (zero_has_N hc))
    (zero_has_N hc) hp

def projectedFold (D a : Poly) : Poly :=
  abstract (fstPoly (.app (.app (.var 0) (pren Nat.succ D)) (pren Nat.succ a)))

theorem projectedFold_beta (D a n : Poly) : P01DF.PolyConv
    (.app (projectedFold D a) n) (fstPoly (.app (.app n D) a)) := by
  have h := poly_beta (fstPoly (.app (.app (.var 0) (pren Nat.succ D)) (pren Nat.succ a))) n
  simpa [projectedFold, fstPoly, psub, pren, psub_comp, cons] using h

theorem projectedFold_has {Γ : Tel} {P : Ty} {D a : Poly} (hc : Ctx Γ)
    (hP : Form (N :: Γ) P) (hD : Has Γ D (arr (total P) (total P)))
    (ha : Has Γ a (total P)) : Has Γ (projectedFold D a) NT := by
  have hE : Form Γ (total P) := .sigma (N_form hc) hP
  have cN := Ctx.ext hc (N_form hc)
  have hEw := form_wk hE hc (N_form hc)
  have hD1 : Has (N :: Γ) (pren Nat.succ D) (arr (wk (total P)) (wk (total P))) := by
    simpa only [wk, subst_arr] using has_wk hD hc (N_form hc)
  have ha1 := has_wk ha hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have run := SourceFoldContract.fold_has cN hEw hn hD1 ha1
  have hEw' : Form (N :: Γ) (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using hEw
  have run' : Has (N :: Γ) (.app (.app (.var 0) (pren Nat.succ D)) (pren Nat.succ a))
      (.sigma N (subst (pup (fun k => .var (k+1))) P)) := by
    simpa only [total, wk, subst, N_subst] using run
  have hb := Has.sigmaFst (N_form cN) hEw' run'
  exact .piIntro (form_arr (N_form hc) (N_form hc)) hb (scoped_abstract (has_scoped hb))

theorem totalStep_projection (d x : Poly) : P01DF.PolyConv
    (fstPoly (.app (totalStep d) x)) (.app succPoly (fstPoly x)) := by
  have h := poly_beta (pairPoly nextIndex d) x
  have h' : P01DF.PolyConv (.app (totalStep d) x)
      (pairPoly (.app succPoly (fstPoly x)) (psub (cons x Poly.var) d)) := by
    simpa [totalStep, nextIndex, pairPoly, fstPoly, psub, cons,
      P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)] using h
  exact (P01DF.PolyConv.app h' (.refl _)).trans (pair_first _ _)

theorem projected_zero (d p : Poly) : P01DF.PolyConv
    (.app (projectedFold (totalStep d) (totalSeed p)) zero) zero :=
  (projectedFold_beta _ _ _).trans
    ((P01DF.PolyConv.app (zero_beta _ _) (.refl _)).trans (pair_first _ _))

theorem projected_succ (d p n : Poly) : P01DF.PolyConv
    (.app (projectedFold (totalStep d) (totalSeed p)) (.app succPoly n))
    (.app succPoly (.app (projectedFold (totalStep d) (totalSeed p)) n)) :=
  (projectedFold_beta _ _ _).trans
    ((P01DF.PolyConv.app (succ_beta n _ _) (.refl _)).trans
      ((totalStep_projection _ _).trans (.app (.refl _) (projectedFold_beta _ _ _).symm)))

theorem projected_ren (d p : Poly) :
    pren Nat.succ (projectedFold (totalStep d) (totalSeed p)) =
    projectedFold (totalStep (psub (pup (fun k => .var (k+1))) d))
      (totalSeed (pren Nat.succ p)) := by
  have hs := has_scoped succ_has
  have hz := has_scoped (inputNumeral_has 0)
  simp [projectedFold, totalStep, totalSeed, nextIndex, pairPoly, fstPoly, zero,
    pren, ← abstraction_naturality, psub, pup, psub_comp,
    P01AC.BooleanPrimitive.psub_closed hs, P01AC.BooleanPrimitive.psub_closed hz]
  congr 15 <;> (first | rfl | (funext n; cases n <;> rfl))

theorem projected_zero_evidence {Γ : Tel} {P : Ty} {d p : Poly} (hc : Ctx Γ)
    (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hd : Has (total P :: Γ) d (totalStepType P)) :
    Has Γ ident (ZeroAt (projectedFold (totalStep d) (totalSeed p))) := by
  have hu := projectedFold_has hc hP (total_step_has hc hP hd) (total_seed_has hc hP hp)
  have hz := zero_has_N hc
  have huz := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hz
  exact .identityIntro (zeroAt_formed hc hu) huz hz (projected_zero d p)

theorem projected_step_evidence {Γ : Tel} {P : Ty} {d p : Poly} (hc : Ctx Γ)
    (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hd : Has (total P :: Γ) d (totalStepType P)) :
    Has Γ (abstract ident) (StepAt (projectedFold (totalStep d) (totalSeed p))) := by
  let u := projectedFold (totalStep d) (totalSeed p)
  have hu := projectedFold_has hc hP (total_step_has hc hP hd) (total_seed_has hc hP hp)
  have c1 := Ctx.ext hc (N_form hc)
  have hu1 : Has (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form c1) .zero
  have hs := succ_has_NT c1
  have sn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs hn
  have un := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 hn
  have left := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 sn
  have right := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs un
  apply Has.piIntro (stepAt_formed hc hu)
  · apply Has.identityIntro (.identity (N_form c1) left right) left right
    change P01DF.PolyConv (.app (pren Nat.succ u) (.app succPoly (.var 0)))
      (.app succPoly (.app (pren Nat.succ u) (.var 0)))
    simp only [u, projected_ren]
    exact projected_succ _ _ _
  · exact scoped_abstract trivial

theorem nat_identity_trans {Γ : Tel} {x y z e d : Poly} (hc : Ctx Γ)
    (hx : Has Γ x N) (hy : Has Γ y N) (hz : Has Γ z N)
    (he : HasE Γ e (.identity N x y)) (hd : HasE Γ d (.identity N y z)) :
    HasE Γ (jPoly e z d) (.identity N x z) := by
  let P : Ty := .identity N (pren Nat.succ x) (.var 0)
  have cN := Ctx.ext hc (N_form hc)
  have hx1 : Has (N :: Γ) (pren Nat.succ x) N := has_wk hx hc (N_form hc)
  have hP : Form (N :: Γ) P := .identity (N_form cN) hx1 (.var (N_form cN) .zero)
  have at_eq (v : Poly) : inst P v = .identity N x v := by
    simp [P, inst, subst, N, NBody, arr, wk, pren, psub, psub_comp, cons]
  have h := transport_source hc (N_form hc) hP hy hz hd
    (show HasE Γ e (inst P y) from (at_eq y).symm ▸ he)
  simpa only [at_eq] using h

/-- Dependent section existence for every original-source formed family.
    The step is expressed on its total space: given (n,p), d returns P(succ n).
    This is a theorem of the unchanged Has/HasE judgements with explicit
    Rigidity evidence. It asserts no zero/successor computation law for
    the transported section and no coherence/uniqueness of proof objects. -/
theorem dependent_section_from_rigidity {Γ : Tel} {P : Ty} {p d r n : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P)
    (hp : Has Γ p (inst P zero))
    (hd : Has (total P :: Γ) d (totalStepType P))
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    ∃ e, HasE Γ e (inst P n) := by
  let D := totalStep d
  let a := totalSeed p
  let u := projectedFold D a
  let run : Poly := .app (.app n D) a
  have hD := total_step_has hc hP hd
  have ha := total_seed_has hc hP hp
  have hu : Has Γ u NT := projectedFold_has hc hP hD ha
  have hE : Form Γ (total P) := .sigma (N_form hc) hP
  have hrun : Has Γ run (total P) := SourceFoldContract.fold_has hc hE hn hD ha
  have hfst : Has Γ (fstPoly run) N := .sigmaFst (N_form hc) hE hrun
  have hsnd : Has Γ (sndPoly run) (inst P (fstPoly run)) :=
    .sigmaSnd hE (form_inst_source hc hP hfst) hrun
  have huN := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hn
  have rid := rigidity_elim hc hu hr
    (has_inclusion (projected_zero_evidence hc hP hp hd))
    (has_inclusion (projected_step_evidence hc hP hp hd))
  have point := rigidity_pointwise hc hu hn rid
  have link : Has Γ ident (.identity N (fstPoly run) (.app u n)) :=
    .identityIntro (.identity (N_form hc) hfst huN) hfst huN (projectedFold_beta D a n).symm
  have back := nat_identity_trans hc hfst huN hn (has_inclusion link) point
  exact ⟨_, transport_source hc (N_form hc) hP hfst hn back (has_inclusion hsnd)⟩

#print axioms dependent_section_from_rigidity
#print axioms transport_source
#print axioms projected_step_evidence
end RigidityInitiality
