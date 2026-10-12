import RawTopSoundness
import FaithfulRawNoConfusion

/- This deliberately nonfaithful interpretation diagnoses source-grammar
incompleteness. It is not an intended-meaning-preserving rival to faithful Raw. -/
namespace JointRawTop
open P01AC P01D
open OpenTermStandardness (T Conv SatPER)
open ImportedOpenTermTransport (interp)
open JointRawNoConfusion (rawIdentity candidate)

/-- Same open carrier and full PER universe, composed with the type translation. -/
abbrev F (A : Ty) (ρ : FullPER.REnv) (η : FullPER.Env) : T → T → Prop :=
  FullPER.F (translate A) ρ η

theorem diagnostic_raw_exact (ρ : FullPER.REnv) (η : FullPER.Env) :
    F .raw ρ η = fun _ _ => True := by
  funext u v
  apply propext
  constructor
  · intro _; trivial
  · intro _ x y h; exact h

theorem diagnostic_full_universe (B : Ty) (ρ : FullPER.REnv) (η : FullPER.Env)
    (u v : T) : F (.all B) ρ η u v ↔
      ∀ P : SatPER, F B (FullPER.cons P.rel ρ) η u v := Iff.rfl

theorem diagnostic_sigma_exact (A B : Ty) (ρ : FullPER.REnv) (η : FullPER.Env)
    (u v : T) : F (.sigma A B) ρ η u v ↔
      F A ρ η (FullPER.first u) (FullPER.first v) ∧
      F B ρ (FullPER.cons (FullPER.first u) η) (FullPER.second u) (FullPER.second v) := Iff.rfl

theorem diagnostic_identity_exact (A : Ty) (p q : Poly) (ρ : FullPER.REnv) (η : FullPER.Env)
    (u v : T) : F (.identity A p q) ρ η u v ↔
      F A ρ η (interp p η) (interp q η) ∧ Conv u .i ∧ Conv v .i := Iff.rfl

theorem diagnostic_N_unchanged (ρ : FullPER.REnv) (η : FullPER.Env) :
    F P01AC.EffectiveCompleteness.N ρ η = FullPER.F P01AC.EffectiveCompleteness.N ρ η := by
  exact congrArg (fun A => FullPER.F A ρ η) translate_N

/-- No narrowing of impredicative quantification and no collapse of the carrier
or conversion relation is used. Raw itself is the deliberate semantic change. -/
theorem diagnostic_raw_not_faithful (ρ : FullPER.REnv) (η : FullPER.Env) :
    F .raw ρ η ≠ Conv := by
  intro h
  have z : F .raw ρ η T.zero T.one := by rw [diagnostic_raw_exact]; trivial
  rw [h] at z
  exact JointRawNoConfusion.zero_not_one z

/-- The translated Raw identity has an explicit pair of proof witnesses. -/
theorem diagnostic_raw_identity_inhabited (ρ : FullPER.REnv) (η : FullPER.Env) :
    F rawIdentity ρ η .i .i :=
  ⟨fun _ _ h => h, .refl _, .refl _⟩

/-- Exact finite translated candidate, with no change to either inert atom. -/
theorem translated_candidate_exact : translate candidate =
    arr (.identity topTy (.atom .zero) (.atom .one)) .bottom := by
  rw [JointRawNoConfusion.candidate, translate_arr]
  rfl

/-- Hence its negation is empty in the diagnostic interpretation. -/
theorem diagnostic_candidate_empty (ρ : FullPER.REnv) (η : FullPER.Env) (u v : T) :
    ¬ F candidate ρ η u v := by
  intro h
  have h' : FullPER.F (translate candidate) ρ η u v := h
  rw [translated_candidate_exact, FullPER.F_arr] at h'
  exact h' .i .i (diagnostic_raw_identity_inhabited ρ η)

/-- The unchanged actual Joint grammar cannot derive this Raw no-confusion type,
even with recursive full Sigma elimination and full dependent induction. -/
theorem no_candidate (p : Poly) : ¬ JointCompletion.HasJ [] p candidate := by
  intro hp
  have h := fundamental hp FullPER.Application.emptyEnv FullPER.zeroEnv FullPER.zeroEnv
    FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  exact diagnostic_candidate_empty _ _ _ _ h

/-- The faithful intended model also excludes a proof of the opposite raw equality. -/
theorem no_raw_equality (p : Poly) : ¬ JointCompletion.HasJ [] p rawIdentity := by
  intro hp
  have h := JointCompletion.fundamental hp FullPER.Application.emptyEnv
    FullPER.zeroEnv FullPER.zeroEnv FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  exact JointRawNoConfusion.zero_not_one h.1

/-- A named, old-formed, finite semantic-validity gap for the completed grammar. -/
theorem explicit_valid_but_unprovable :
    P01AC.ExtensionalRepair.FormE [] candidate ∧
    (∃ p : Poly, Scoped 0 p ∧ FullPER.Fundamental [] p candidate) ∧
    (∀ p : Poly, ¬ JointCompletion.HasJ [] p candidate) :=
  ⟨JointRawNoConfusion.candidate_formE,
    ⟨.atom .i,trivial,JointRawNoConfusion.faithful_fundamental _⟩,no_candidate⟩

/-- Even closed-inhabitation completeness fails for this single explicit type. -/
theorem no_faithful_inhabitation_completeness :
    ¬ (∀ A : Ty, P01AC.ExtensionalRepair.FormE [] A →
      (∃ p : Poly, Scoped 0 p ∧ FullPER.Fundamental [] p A) →
      ∃ p : Poly, JointCompletion.HasJ [] p A) := by
  intro h
  obtain ⟨p,hp⟩ := h candidate explicit_valid_but_unprovable.1
    explicit_valid_but_unprovable.2.1
  exact no_candidate p hp

#print axioms diagnostic_raw_exact
#print axioms diagnostic_full_universe
#print axioms diagnostic_N_unchanged
#print axioms diagnostic_candidate_empty
#print axioms no_candidate
#print axioms no_raw_equality
#print axioms explicit_valid_but_unprovable
#print axioms no_faithful_inhabitation_completeness
end JointRawTop
