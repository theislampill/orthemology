/- Additive actual-E support for the literal retained total-space construction. -/
import FullESectionCorollaries
namespace RigidityInitiality.FullE
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem shifted_family_form {Γ : Tel} {P B : Ty} (hc : CtxE Γ)
    (hP : FormE (N :: Γ) P) (hB : FormE Γ B) : FormE (N :: B :: Γ) (shiftedFamily P) := by
  have hE : FormE Γ (total P) := .sigma (N_form hc) hP
  have hEw : FormE (B :: Γ) (.sigma N (shiftedFamily P)) := by
    simpa only [total, wk, subst, N_subst] using form_wk hE hc hB
  exact sigma_body_form hEw


theorem sectionBody_scoped {Γ : Tel} {P : Ty} {p s n : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) (hn : HasE Γ n N) :
    Scoped Γ.length (sectionBody p s n) := by
  have hE : FormE Γ (total P) := .sigma (N_form hc) hP
  have hd := total_step_has hc hP (uncurried_step_has hc hP hs)
  have ha := total_seed_has hc hP hp
  have run := fold_has hc hE hn hd ha
  have first := HasE.sigmaFst (N_form hc) hE run
  exact has_scoped (HasE.sigmaSnd hE (form_inst_source hc hP first) run)

theorem section_has {Γ : Tel} {P : Ty} {p s r : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) (hr : HasE Γ r Rigidity) :
    HasE Γ (sectionPoly p s) (.pi N P) := by
  have cN := CtxE.ext hc (N_form hc)
  have hP' := shifted_family_form hc hP (N_form hc)
  have hp' : HasE (N :: Γ) (pren Nat.succ p) (inst (shiftedFamily P) zero) :=
    shifted_zero P ▸ has_wk hp hc (N_form hc)
  have hs' : HasE (N :: Γ) (pren Nat.succ s) (dependentStepType (shiftedFamily P)) :=
    shifted_step P ▸ has_wk hs hc (N_form hc)
  have hr' : HasE (N :: Γ) (pren Nat.succ r) Rigidity := by
    simpa only [wk, rigidity_subst] using has_wk hr hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have body := dependent_section_curried cN hP' hp' hs' (hr') hn
  apply HasE.piIntro ((.pi (N_form hc) hP))
  · simpa only [shifted_at_var] using body
  · exact scoped_abstract (sectionBody_scoped cN hP' hp' hs' hn)



theorem sectionPoly_scoped {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) : Scoped Γ.length (sectionPoly p s) := by
  have cN := CtxE.ext hc (N_form hc)
  have hP' := shifted_family_form hc hP (N_form hc)
  have hp' : HasE (N :: Γ) (pren Nat.succ p) (inst (shiftedFamily P) zero) :=
    shifted_zero P ▸ has_wk hp hc (N_form hc)
  have hs' : HasE (N :: Γ) (pren Nat.succ s) (dependentStepType (shiftedFamily P)) :=
    shifted_step P ▸ has_wk hs hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  exact scoped_abstract (sectionBody_scoped cN hP' hp' hs' hn)

theorem rigidity_implies_section {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) :
    HasE Γ (abstract (sectionPoly (pren Nat.succ p) (pren Nat.succ s)))
      (arr Rigidity (.pi N P)) := by
  have hR := rigidity_formed hc
  have cR := CtxE.ext hc hR
  have hP' := shifted_family_form hc hP hR
  have hp' : HasE (Rigidity :: Γ) (pren Nat.succ p) (inst (shiftedFamily P) zero) :=
    shifted_zero P ▸ has_wk hp hc hR
  have hs' : HasE (Rigidity :: Γ) (pren Nat.succ s) (dependentStepType (shiftedFamily P)) :=
    shifted_step P ▸ has_wk hs hc hR
  have hr : HasE (Rigidity :: Γ) (.var 0) Rigidity := by
    have hv : HasE (Rigidity :: Γ) (.var 0) (wk Rigidity) := .var (form_wk hR hc hR) .zero
    simpa only [wk, rigidity_subst] using hv
  have body := section_has cR hP' hp' hs' hr
  apply HasE.piIntro ((form_arr hR (.pi (N_form hc) hP)))
  · simpa only [wk, subst, N_subst] using body
  · exact scoped_abstract (sectionPoly_scoped cR hP' hp' hs')


end RigidityInitiality.FullE
