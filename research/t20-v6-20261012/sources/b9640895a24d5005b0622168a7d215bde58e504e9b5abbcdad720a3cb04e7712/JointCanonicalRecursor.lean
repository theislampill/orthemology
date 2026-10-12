import JointRecursorUniqueness

namespace JointCompletion.RecursorUniqueness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality InductionComputation
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem shifted_successor_at_variable (P : Ty) :
    inst (shiftedFamily P) (.app succPoly (.var 0)) = successorFamily P := by
  simp only [inst, shiftedFamily, successorFamily, subst_comp]
  congr 1
  funext k
  cases k <;> rfl

/-- The ordinary law family is formed directly from the typed section and step. -/
theorem successor_law_formed {Γ : Tel} {P : Ty} {s u : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hs : HasJ Γ s (dependentStepType P)) (hu : HasJ Γ u (.pi N P)) :
    FormJ (N :: Γ) (successorLawFamily P s u) := by
  have cn := CtxJ.ext hc (N_form hc)
  have hQ := successorFamily_form hc hP
  have hP' := shifted_family_form hc hP (N_form hc)
  have hu' : HasJ (N :: Γ) (pren Nat.succ u) (.pi N (shiftedFamily P)) := by
    simpa only [wk, subst, N_subst, shiftedFamily] using has_wk hu hc (N_form hc)
  have hn : HasJ (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  have hsn := app_has (form_arr (N_form cn) (N_form cn)) (N_form cn) (succ_has_NT cn) hn
  have hl : HasJ (N :: Γ) (.app (pren Nat.succ u) (.app succPoly (.var 0)))
      (successorFamily P) := by
    simpa only [shifted_successor_at_variable] using section_value cn hP' hu' hsn
  have hf : HasJ (N :: Γ) (.app (pren Nat.succ s) (.var 0)) (arr P (successorFamily P)) :=
    section_at_variable hc (pi_body_form (has_form hs)) hs
  exact .identity hQ hl
    (app_has (form_arr hP hQ) hQ hf (section_at_variable hc hP hu))

/-- A literal successor-law section for the canonical recursor. Obtaining the
witness in the generic-variable context suffices; no meta-level choice over n
is converted into a source function. -/
theorem canonical_successor_laws {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero)) (hs : HasJ Γ s (dependentStepType P)) :
    ∃ l, HasJ Γ l (.pi N (successorLawFamily P s (sectionPoly p s))) := by
  have cn := CtxJ.ext hc (N_form hc)
  have hP' := shifted_family_form hc hP (N_form hc)
  have hp' : HasJ (N :: Γ) (pren Nat.succ p) (inst (shiftedFamily P) zero) :=
    shifted_zero P ▸ has_wk hp hc (N_form hc)
  have hs' : HasJ (N :: Γ) (pren Nat.succ s) (dependentStepType (shiftedFamily P)) :=
    shifted_step P ▸ has_wk hs hc (N_form hc)
  have hn : HasJ (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  obtain ⟨e, he⟩ := induction_successor cn hP' hp' hs' hn
  have ren_section : pren Nat.succ (sectionPoly p s) =
      sectionPoly (pren Nat.succ p) (pren Nat.succ s) := Structural.sectionPoly_rename p s Nat.succ
  have he' : HasJ (N :: Γ) e (successorLawFamily P s (sectionPoly p s)) := by
    simpa only [successorLawFamily, ren_section, shifted_successor_at_variable] using he
  exact ⟨abstract e, .piIntro (.pi (N_form hc) (has_form he')) he' (scoped_abstract (has_scoped he'))⟩

/-- Any actual dependent section obeying the supplied recursion laws is
source-identical to the exact sectionPoly returned by natInduction. -/
theorem unique_to_canonical {Γ : Tel} {P : Ty} {p s u zu lu : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero)) (hs : HasJ Γ s (dependentStepType P))
    (hu : HasJ Γ u (.pi N P))
    (hzu : HasJ Γ zu (.identity (inst P zero) (.app u zero) p))
    (hlu : HasJ Γ lu (.pi N (successorLawFamily P s u))) :
    HasJ Γ ident (.identity (.pi N P) u (sectionPoly p s)) := by
  obtain ⟨lv, hlv⟩ := canonical_successor_laws hc hP hp hs
  exact recursor_unique hc hP hp hs hu (induction_section hc hP hp hs)
    hzu (induction_zero hc hP hp hs) hlu hlv

#print axioms canonical_successor_laws
#print axioms unique_to_canonical
end JointCompletion.RecursorUniqueness
