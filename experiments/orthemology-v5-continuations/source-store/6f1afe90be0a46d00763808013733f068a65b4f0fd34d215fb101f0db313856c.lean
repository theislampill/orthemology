/- Nonempty dependent witnesses and precise failed generalisations. -/
import P01DependentFundamental
namespace P01DF
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def skk : Term := .app (.app .s .k) .k
def emptyIndices : Env := fun _ => .i
def anchoredIdentity : Ty := .identity (.var 0) (.atom .i)

theorem anchored_identity_inhabited (ρ : OEnv) :
    (((interpret anchoredIdentity).run (cons .i emptyIndices)).obj ρ).dom .i :=
  ⟨.refl _,.refl _,.refl _⟩

theorem anchored_identity_empty (ρ : OEnv) (p : Term) :
    ¬ (((interpret anchoredIdentity).run (cons skk emptyIndices)).obj ρ).dom p := by
  intro h
  exact P01Source.I_SKK_not_convertible h.1.symm

theorem nonconstant_fibres (ρ : OEnv) :
    (((interpret anchoredIdentity).run (cons .i emptyIndices)).obj ρ).dom .i ∧
    (∀ p, ¬ (((interpret anchoredIdentity).run (cons skk emptyIndices)).obj ρ).dom p) :=
  ⟨anchored_identity_inhabited ρ,anchored_identity_empty ρ⟩

/-- This is a nonempty source PER and its legitimate respectful diagonal link.
    Semantic relatedness here is strictly weaker than raw-index equality. -/
theorem heterogeneous_index_transport_fails (ρ : OEnv) :
    ∃ (P Q : PER) (R : Link P Q) (x y : Term), R.rel x y ∧
      (IdPER rawPER x .i).dom .i ∧ ¬ (IdPER rawPER y .i).dom .i := by
  let P := (P01R.interpret identityCode).obj ρ
  refine ⟨P,P,diagonal P,.i,skk,?_,⟨.refl _,.refl _,.refl _⟩,?_⟩
  · exact ((P01R.interpret identityCode).identity ρ _ _).mp
      (recursive_polymorphic_I_skk (diagEnv ρ))
  · intro h; exact P01Source.I_SKK_not_convertible h.1.symm

def totalPER : PER where
  rel := fun _ _ => True
  sym := fun _ => True.intro
  trans := fun _ _ => True.intro
  raw := fun _ _ _ => True.intro

def inspectedFibre (x : Term) : PER := if x = .i then rawPER else totalPER

def naivePiRel (P : PER) (B : Term → PER) (f g : Term) : Prop :=
  ∀ x y, P.rel x y → (B x).rel (.app f x) (.app g y)

/-- Even symmetry can fail if dependent Pi's coherence premise is omitted.
    This does not instantiate the lawful PiPER constructor. -/
theorem omitted_coherence_breaks_pi_symmetry :
    ∃ f g, naivePiRel totalPER inspectedFibre f g ∧
      ¬ naivePiRel totalPER inspectedFibre g f := by
  refine ⟨.i,.app .k .i,?_,?_⟩
  · intro x y hxy
    by_cases hx : x = .i
    · subst x
      change (if Term.i = .i then rawPER else totalPER).rel _ _
      rw [if_pos rfl]
      exact (Conv.step (.i .i)).trans (Conv.step (.k .i y)).symm
    · change (if x = .i then rawPER else totalPER).rel _ _
      rw [if_neg hx]
      exact True.intro
  · intro h
    have bad := h .i skk True.intro
    change (if Term.i = .i then rawPER else totalPER).rel _ _ at bad
    rw [if_pos rfl] at bad
    exact P01Source.I_SKK_not_convertible
      ((Conv.step (.k .i .i)).symm.trans (bad.trans (Conv.step (.i skk))))

def dependentReflType : Ty := .pi (.identity (.var 0) (.var 0))

theorem dependent_reflexivity_typed : Has (abstract (.atom .i)) dependentReflType :=
  .piIntro (.identityIntro (.refl (.var 0)))

theorem dependent_reflexivity_nonempty (ρ : OEnv) (η : Env) :
    (((interpret dependentReflType).run η).obj ρ).dom (.app .k .i) := by
  have h := unary_soundness dependent_reflexivity_typed ρ η
  simpa only [abstract,freeZero,Bool.false_eq_true,↓reduceIte,drop,pren,psub,eval] using h

theorem dependent_pair_typed :
    Has (pairPoly (.atom .i) (.atom .i)) (.sigma anchoredIdentity) := by
  apply Has.sigmaIntro
  change Has (.atom .i) (.identity (.atom .i) (.atom .i))
  exact .identityIntro (.refl _)

theorem dependent_pair_nonempty (ρ : OEnv) (η : Env) :
    (((interpret (.sigma anchoredIdentity)).run η).obj ρ).dom (pairTerm .i .i) :=
  unary_soundness dependent_pair_typed ρ η

theorem dependent_pair_projection_typed :
    Has (sndPoly (pairPoly (.atom .i) (.atom .i)))
      (instantiate anchoredIdentity (fstPoly (pairPoly (.atom .i) (.atom .i)))) :=
  .sigmaSnd dependent_pair_typed

def convertedProof : Poly := .app (.atom .i) (.atom .i)

theorem converted_identity_proof_typed :
    Has convertedProof (.identity (.atom .i) (.atom .i)) :=
  .conv (.identityIntro (.refl _)) (.symm (.i _))

/-- The motive explicitly contains the proof coordinate at index zero.
    The fundamental theorem handles transport from I to the convertible I I. -/
theorem proof_dependent_j_typed :
    Has (jPoly (.atom .i) (.atom .i) convertedProof)
      (motiveAt (.identity (.var 0) (.atom .i)) (.atom .i) convertedProof) := by
  apply Has.j converted_identity_proof_typed
  change Has (.atom .i) (.identity (.atom .i) (.atom .i))
  exact .identityIntro (.refl _)

theorem proof_dependent_j_nonempty (ρ : OEnv) (η : Env) :
    (((interpret (motiveAt (.identity (.var 0) (.atom .i)) (.atom .i) convertedProof)).run η).obj ρ).dom
      (eval (jPoly (.atom .i) (.atom .i) convertedProof) η) :=
  unary_soundness proof_dependent_j_typed ρ η

/-- Both free sorts survive nested All and raw-index Pi binders. -/
theorem two_sort_substitution_control :
    substType (fun _ => .arrow (.param 0) (.identity (.var 0) (.atom .i)))
      (.all (.pi (.param 1))) =
    .all (.pi (.arrow (.param 1) (.identity (.var 1) (.atom .i)))) := rfl

def dependentPolyBody : Ty := .pi (.arrow (.param 0) (.arrow anchoredIdentity (.param 0)))
def dependentPolyType : Ty := .all dependentPolyBody

theorem dependent_polymorphic_typed : Has (abstract (.atom .k)) dependentPolyType :=
  .allIntro (.piIntro (.k (.param 0) anchoredIdentity))

theorem dependent_polymorphic_nonempty (ρ : OEnv) (η : Env) :
    (((interpret dependentPolyType).run η).obj ρ).dom (eval (abstract (.atom .k)) η) :=
  unary_soundness dependent_polymorphic_typed ρ η

theorem dependent_polymorphic_self_typed :
    Has (abstract (.atom .k)) (instantiateType dependentPolyBody dependentPolyType) :=
  .allElim dependent_polymorphic_typed

theorem raw_index_variable_not_arbitrary_type_parameter : ¬ Has (.var 0) (.param 0) := by
  intro h
  exact unary_soundness h (fun _ => botPER) emptyIndices

/-- Raw indices intentionally include nonnormalizing source terms. The new
    soundness theorem cannot inherit the finite source-SN theorem. -/
theorem raw_omega_typed : Has (.atom omega) .raw := .raw _

theorem raw_omega_has_no_normal_reduct :
    ∀ u, Red omega u → ¬ P01Source.Normal u :=
  fun _ h => P01Source.omega_no_normal_reduct h

end P01DF
