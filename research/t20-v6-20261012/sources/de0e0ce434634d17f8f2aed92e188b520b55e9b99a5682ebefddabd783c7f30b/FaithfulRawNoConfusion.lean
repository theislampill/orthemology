import JointSoundness
import JointRegularity

/- A bounded control in the existing faithful full-SatPER interpretation.
   This file imports, and does not replace, the actual source grammars or model.
   In particular, semantic validity below is not asserted to give HasJ typing. -/
namespace JointRawNoConfusion
open P01AC P01D
open P01AC.ExtensionalRepair (FormE form_inclusion)
open OpenTermStandardness (T SatPER Conv)

/-- The two distinct inert Raw constants, at their actual source identity type. -/
def rawIdentity : Ty := .identity .raw (.atom .zero) (.atom .one)

/-- The exact closed source no-confusion type, with the existing arrow operation. -/
def candidate : Ty := arr rawIdentity .bottom

theorem rawIdentity_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ rawIdentity :=
  .identity (.raw hΓ) (.rawAtom (.raw hΓ)) (.rawAtom (.raw hΓ))

theorem candidate_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ candidate :=
  form_arr (rawIdentity_form hΓ) (.bottom hΓ)

theorem rawIdentity_formE : FormE [] rawIdentity :=
  form_inclusion (rawIdentity_form .nil)

theorem candidate_formE : FormE [] candidate :=
  form_inclusion (candidate_form .nil)

theorem candidate_formJ : JointCompletion.FormJ [] candidate :=
  .formBase candidate_formE

/-- Separation uses the inherited reduction/normal-form theorem, transported
    through the existing retraction of open terms to the original raw carrier. -/
theorem zero_not_one : ¬ Conv T.zero T.one := by
  intro h
  exact P01AC.BooleanIdentity.choices_separate (ImportedOpenTermTransport.erase_conv h)

theorem faithful_raw_identity_empty (ρ : FullPER.REnv) (η : FullPER.Env)
    (u v : T) : ¬ FullPER.F rawIdentity ρ η u v := by
  intro h
  exact zero_not_one h.1

/-- Every pair of erased polynomials belongs to this empty-domain arrow.
    This is a fact about the faithful model, with no source proof extracted. -/
theorem faithful_candidate_total (ρ : FullPER.REnv) (η : FullPER.Env)
    (u v : T) : FullPER.F candidate ρ η u v := by
  rw [candidate, FullPER.F_arr]
  intro x y hxy
  exact False.elim (faithful_raw_identity_empty ρ η x y hxy)

/-- In particular, any polynomial is a semantic fundamental witness, whether or
    not it is source scoped or derivable at the candidate type. -/
theorem faithful_fundamental (p : Poly) : FullPER.Fundamental [] p candidate := by
  intro ρ η ξ _ _
  exact faithful_candidate_total ρ η _ _

/-- The existing quantifier still ranges over every saturated PER, without a
    restricted/Henkin subuniverse or additional admissibility predicate. -/
theorem full_universe_exact (B : Ty) (ρ : FullPER.REnv) (η : FullPER.Env)
    (u v : T) : FullPER.F (.all B) ρ η u v ↔
      ∀ P : SatPER, FullPER.F B (FullPER.cons P.rel ρ) η u v := Iff.rfl

/-- Raw remains exactly the inherited open-term conversion relation. -/
theorem faithful_raw_exact (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F .raw ρ η = Conv := rfl

/-- The candidate is definitionally the literal type requested. -/
theorem candidate_exact : candidate =
    arr (.identity .raw (.atom .zero) (.atom .one)) .bottom := rfl

#print axioms candidate_formE
#print axioms candidate_formJ
#print axioms zero_not_one
#print axioms faithful_raw_identity_empty
#print axioms faithful_candidate_total
#print axioms faithful_fundamental
#print axioms full_universe_exact
#print axioms faithful_raw_exact
#print axioms candidate_exact
end JointRawNoConfusion
