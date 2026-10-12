import SectionCorollaries
namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def shiftedFamily (P : Ty) := subst (pup (fun k => .var (k+1))) P

theorem shifted_family_form {Γ : Tel} {P B : Ty} (hc : Ctx Γ)
    (hP : Form (N :: Γ) P) (hB : Form Γ B) : Form (N :: B :: Γ) (shiftedFamily P) := by
  have hE : Form Γ (total P) := .sigma (N_form hc) hP
  have hEw : Form (B :: Γ) (.sigma N (shiftedFamily P)) := by
    simpa only [total, wk, subst, N_subst] using form_wk hE hc hB
  exact sigma_body_form hEw

theorem shifted_zero (P : Ty) : wk (inst P zero) = inst (shiftedFamily P) zero := by
  rw [wk, subst_inst]
  simp only [SourceRigidity.zero, P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))]
  rfl

theorem shifted_step (P : Ty) : wk (dependentStepType P) = dependentStepType (shiftedFamily P) := by
  simp only [wk, dependentStepType, subst, N_subst, subst_arr]
  congr 2
  simp only [successorFamily, shiftedFamily, subst_comp]
  congr 1
  funext k
  cases k with
  | zero => simp [cons, pup, psub, P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)]
  | succ k => rfl

theorem shifted_at_var (P : Ty) : inst (shiftedFamily P) (.var 0) = P := by
  simp only [inst, shiftedFamily, subst_comp]
  have he : (fun n => psub (cons (.var 0) Poly.var) ((pup (fun k => .var (k+1))) n)) = Poly.var := by
    funext n; cases n <;> rfl
  rw [he, subst_id]

def sectionBody (p s n : Poly) : Poly :=
  sndPoly (.app (.app n (totalStep (uncurriedStep s))) (totalSeed p))

def sectionPoly (p s : Poly) : Poly :=
  abstract (sectionBody (pren Nat.succ p) (pren Nat.succ s) (.var 0))

theorem sectionBody_scoped {Γ : Tel} {P : Ty} {p s n : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hs : Has Γ s (dependentStepType P)) (hn : Has Γ n N) :
    Scoped Γ.length (sectionBody p s n) := by
  have hE : Form Γ (total P) := .sigma (N_form hc) hP
  have hd := total_step_has hc hP (uncurried_step_has hc hP hs)
  have ha := total_seed_has hc hP hp
  have run := SourceFoldContract.fold_has hc hE hn hd ha
  have first := Has.sigmaFst (N_form hc) hE run
  exact has_scoped (Has.sigmaSnd hE (form_inst_source hc hP first) run)

/-- A single source polynomial inhabits Πn.P(n), provided the rigidity
    evidence has original-Has typing and can therefore use inherited weakening. -/
theorem section_has {Γ : Tel} {P : Ty} {p s r : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hs : Has Γ s (dependentStepType P)) (hr : Has Γ r Rigidity) :
    HasE Γ (sectionPoly p s) (.pi N P) := by
  have cN := Ctx.ext hc (N_form hc)
  have hP' := shifted_family_form hc hP (N_form hc)
  have hp' : Has (N :: Γ) (pren Nat.succ p) (inst (shiftedFamily P) zero) :=
    shifted_zero P ▸ has_wk hp hc (N_form hc)
  have hs' : Has (N :: Γ) (pren Nat.succ s) (dependentStepType (shiftedFamily P)) :=
    shifted_step P ▸ has_wk hs hc (N_form hc)
  have hr' : Has (N :: Γ) (pren Nat.succ r) Rigidity := by
    simpa only [wk, rigidity_subst] using has_wk hr hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have body := dependent_section_curried cN hP' hp' hs' (has_inclusion hr') hn
  apply HasE.piIntro (form_inclusion (.pi (N_form hc) hP))
  · simpa only [shifted_at_var] using body
  · exact scoped_abstract (sectionBody_scoped cN hP' hp' hs' hn)


theorem sectionPoly_scoped {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hs : Has Γ s (dependentStepType P)) : Scoped Γ.length (sectionPoly p s) := by
  have cN := Ctx.ext hc (N_form hc)
  have hP' := shifted_family_form hc hP (N_form hc)
  have hp' : Has (N :: Γ) (pren Nat.succ p) (inst (shiftedFamily P) zero) :=
    shifted_zero P ▸ has_wk hp hc (N_form hc)
  have hs' : Has (N :: Γ) (pren Nat.succ s) (dependentStepType (shiftedFamily P)) :=
    shifted_step P ▸ has_wk hs hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  exact scoped_abstract (sectionBody_scoped cN hP' hp' hs' hn)

/-- A genuine source implication, uniform in every formed family and its
    original-Has seed/step. Rigidity is bound as an ordinary hypothesis.
    Families are quantified metatheoretically, not through a new universe. -/
theorem rigidity_implies_section {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P) (hp : Has Γ p (inst P zero))
    (hs : Has Γ s (dependentStepType P)) :
    HasE Γ (abstract (sectionPoly (pren Nat.succ p) (pren Nat.succ s)))
      (arr Rigidity (.pi N P)) := by
  have hR := rigidity_formed hc
  have cR := Ctx.ext hc hR
  have hP' := shifted_family_form hc hP hR
  have hp' : Has (Rigidity :: Γ) (pren Nat.succ p) (inst (shiftedFamily P) zero) :=
    shifted_zero P ▸ has_wk hp hc hR
  have hs' : Has (Rigidity :: Γ) (pren Nat.succ s) (dependentStepType (shiftedFamily P)) :=
    shifted_step P ▸ has_wk hs hc hR
  have hr : Has (Rigidity :: Γ) (.var 0) Rigidity := by
    have hv : Has (Rigidity :: Γ) (.var 0) (wk Rigidity) := .var (form_wk hR hc hR) .zero
    simpa only [wk, rigidity_subst] using hv
  have body := section_has cR hP' hp' hs' hr
  apply HasE.piIntro (form_inclusion (form_arr hR (.pi (N_form hc) hP)))
  · simpa only [wk, subst, N_subst] using body
  · exact scoped_abstract (sectionPoly_scoped cR hP' hp' hs')

#print axioms section_has
#print axioms rigidity_implies_section
end RigidityInitiality
