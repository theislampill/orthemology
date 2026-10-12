/- Additive Joint port of the credited actual-E total-space proof. -/
import JointInductionInitiality
namespace JointCompletion.InductionComputation
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem pi_body_form {Γ : Tel} {X P : Ty} (h : FormJ Γ (.pi X P)) :
    FormJ (X :: Γ) P := by
  cases h with
  | formBase h => cases h with | pi _ h => exact .formBase h
  | pi _ h => exact h


theorem uncurried_step_has {Γ : Tel} {P : Ty} {s : Poly} (hc : CtxJ Γ)
    (hP : FormJ (N :: Γ) P) (hs : HasJ Γ s (dependentStepType P)) :
    HasJ (total P :: Γ) (uncurriedStep s) (totalStepType P) := by
  have hE : FormJ Γ (total P) := .sigma (N_form hc) hP
  have cE := CtxJ.ext hc hE
  let P' := subst (pup (fun k => .var (k+1))) P
  have hEw : FormJ (total P :: Γ) (.sigma N P') := by
    simpa only [total, wk, subst, N_subst] using form_wk hE hc hE
  have hv : HasJ (total P :: Γ) (.var 0) (.sigma N P') := by
    have h : HasJ (total P :: Γ) (.var 0) (wk (total P)) := .var (form_wk hE hc hE) .zero
    simpa only [total, wk, subst, N_subst] using h
  have hfst := HasJ.sigmaFst (N_form cE) hEw hv
  have hleaf := form_inst_source cE (sigma_body_form hEw) hfst
  have hsnd := HasJ.sigmaSnd hEw hleaf hv
  have hsw : HasJ (total P :: Γ) (pren Nat.succ s)
      (.pi N (subst (pup (fun k => .var (k+1))) (arr P (successorFamily P)))) := by
    simpa only [dependentStepType, wk, subst, N_subst] using has_wk hs hc hE
  have hsform := has_form hsw
  have target := form_inst_source cE (pi_body_form hsform) hfst
  have first := HasJ.piElim hsform target hsw hfst
  have target_eq : inst (subst (pup (fun k => .var (k+1))) (arr P (successorFamily P)))
      (fstPoly (.var 0)) = arr (inst P' (fstPoly (.var 0))) (totalStepType P) := by
    simp only [subst_arr, inst, subst_arr]
    congr 1
    simp only [successorFamily, totalStepType, inst, subst_comp]
    congr 1
    funext k
    cases k with
    | zero =>
      simp [cons, pup, psub, nextIndex,
        P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)]
    | succ k => rfl
  have first' := target_eq ▸ first
  have target' := target_eq ▸ target
  have hresult : FormJ (total P :: Γ) (totalStepType P) := by
    simpa only [inst_wk] using form_inst_source cE (pi_body_form target') hsnd
  exact app_has target' hresult first' hsnd


theorem dependent_section_explicit {Γ : Tel} {P : Ty} {p d r n : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero))
    (hd : HasJ (total P :: Γ) d (totalStepType P))
    (hr : HasJ Γ r Rigidity) (hn : HasJ Γ n N) :
    HasJ Γ (sndPoly (.app (.app n (totalStep d)) (totalSeed p))) (inst P n) := by
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
  have transported := transport_source hc (N_form hc) hP hfst hn back (hsnd)
  exact HasJ.conv ((form_inst_source hc hP hn)) transported
    ((P01AC.Intensional.Plus.PolyConvPlus.app (.k _ _) (.refl _)).trans (.k _ _))
    (has_scoped hsnd)



theorem dependent_section_curried {Γ : Tel} {P : Ty} {p s r n : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero)) (hs : HasJ Γ s (dependentStepType P))
    (hr : HasJ Γ r Rigidity) (hn : HasJ Γ n N) :
    HasJ Γ (sndPoly (.app (.app n (totalStep (uncurriedStep s))) (totalSeed p))) (inst P n) :=
  dependent_section_explicit hc hP hp (uncurried_step_has hc hP hs) hr hn


end JointCompletion.InductionComputation
