import Initiality
namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def successorFamily (P : Ty) : Ty :=
  subst (cons (.app succPoly (.var 0)) (fun k => .var (k+1))) P

def dependentStepType (P : Ty) : Ty := .pi N (arr P (successorFamily P))

def uncurriedStep (s : Poly) : Poly :=
  .app (.app (pren Nat.succ s) (fstPoly (.var 0))) (sndPoly (.var 0))

theorem pi_body_form {Γ : Tel} {X P : Ty} (h : Form Γ (.pi X P)) :
    Form (X :: Γ) P := by cases h; assumption

theorem uncurried_step_has {Γ : Tel} {P : Ty} {s : Poly} (hc : Ctx Γ)
    (hP : Form (N :: Γ) P) (hs : Has Γ s (dependentStepType P)) :
    Has (total P :: Γ) (uncurriedStep s) (totalStepType P) := by
  have hE : Form Γ (total P) := .sigma (N_form hc) hP
  have cE := Ctx.ext hc hE
  let P' := subst (pup (fun k => .var (k+1))) P
  have hEw : Form (total P :: Γ) (.sigma N P') := by
    simpa only [total, wk, subst, N_subst] using form_wk hE hc hE
  have hv : Has (total P :: Γ) (.var 0) (.sigma N P') := by
    have h : Has (total P :: Γ) (.var 0) (wk (total P)) := .var (form_wk hE hc hE) .zero
    simpa only [total, wk, subst, N_subst] using h
  have hfst := Has.sigmaFst (N_form cE) hEw hv
  have hleaf := form_inst_source cE (sigma_body_form hEw) hfst
  have hsnd := Has.sigmaSnd hEw hleaf hv
  have hsw : Has (total P :: Γ) (pren Nat.succ s)
      (.pi N (subst (pup (fun k => .var (k+1))) (arr P (successorFamily P)))) := by
    simpa only [dependentStepType, wk, subst, N_subst] using has_wk hs hc hE
  have hsform := has_form hsw
  have target := form_inst_source cE (pi_body_form hsform) hfst
  have first := Has.piElim hsform target hsw hfst
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
        P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)]
    | succ k => rfl
  have first' := target_eq ▸ first
  have target' := target_eq ▸ target
  have hresult : Form (total P :: Γ) (totalStepType P) := by
    simpa only [inst_wk] using form_inst_source cE (pi_body_form target') hsnd
  exact app_has target' hresult first' hsnd


/-- The transported proof has this exact erasure; no witness choice is required. -/
theorem dependent_section_explicit {Γ : Tel} {P : Ty} {p d r n : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P)
    (hp : Has Γ p (inst P zero))
    (hd : Has (total P :: Γ) d (totalStepType P))
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    HasE Γ (sndPoly (.app (.app n (totalStep d)) (totalSeed p))) (inst P n) := by
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
  have transported := transport_source hc (N_form hc) hP hfst hn back (has_inclusion hsnd)
  exact HasE.conv (form_inclusion (form_inst_source hc hP hn)) transported
    ((P01AC.Intensional.Plus.PolyConvPlus.app (.k _ _) (.refl _)).trans (.k _ _))
    (has_scoped hsnd)


theorem dependent_section_curried {Γ : Tel} {P : Ty} {p s r n : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P)
    (hp : Has Γ p (inst P zero)) (hs : Has Γ s (dependentStepType P))
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    HasE Γ (sndPoly (.app (.app n (totalStep (uncurriedStep s))) (totalSeed p))) (inst P n) :=
  dependent_section_explicit hc hP hp (uncurried_step_has hc hP hs) hr hn

#print axioms dependent_section_explicit
#print axioms dependent_section_curried
end RigidityInitiality
