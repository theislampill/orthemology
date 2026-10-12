import CrossTypedObserver

namespace CrossTypingReview
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral)
open CrossTypedObserver
set_option maxRecDepth 8192

-- The final polynomial, expanded without changing any source encoding.
def literalObserver (n a b : Poly) : Poly :=
  .app (.app (.app n (.app (.atom .k) (pairPoly b b))) (pairPoly a a)) (.atom .k)

theorem literal_endpoint (n a b : Poly) : observe n a b = literalObserver n a b := rfl

theorem dual_literal_typing {Γ B n a b}
    (hn : Has Γ n N) (ha : Has Γ a B) (hb : Has Γ b B) :
    Has Γ (literalObserver n a b) B ∧ Has Γ (literalObserver n a b) B :=
  ⟨observe_via_sigma hn ha hb, observe_via_church hn ha hb⟩

-- Genuinely dependent B verifies all nested arr and Product weakening.
def DepΓ : Tel := [.param 0]
def DepB : Ty := .identity (.param 0) (.var 0) (.var 0)
theorem dep_context : Ctx DepΓ := .ext .nil (.param .nil)
theorem dep_value : Has DepΓ (.var 0) (.param 0) := .var (.param dep_context) .zero
theorem dep_formed : Form DepΓ DepB := .identity (.param dep_context) dep_value dep_value
theorem dep_inhabitant : Has DepΓ (.atom .i) DepB :=
  .identityIntro dep_formed dep_value dep_value (.refl _)

theorem product_dependency : Product DepB =
    .sigma DepB (.identity (.param 0) (.var 1) (.var 1)) := rfl

theorem dependent_dual_pair :
    Has DepΓ (pairPoly (.atom .i) (.atom .i)) (Product DepB) ∧
    Has DepΓ (pairPoly (.atom .i) (.atom .i)) (ChurchPair DepB) :=
  ⟨pair_product_has dep_inhabitant dep_inhabitant,
   pair_church_has dep_inhabitant dep_inhabitant⟩

theorem dependent_dual_step :
    Has DepΓ (step (.atom .i)) (arr (Product DepB) (Product DepB)) ∧
    Has DepΓ (step (.atom .i)) (arr (ChurchPair DepB) (ChurchPair DepB)) :=
  ⟨constant_has (product_form dep_formed) dependent_dual_pair.1,
   constant_has (churchPair_form dep_formed) dependent_dual_pair.2⟩

theorem dependent_dual_observer (k : Nat) :
    Has DepΓ (literalObserver (inputNumeral k) (.atom .i) (.atom .i)) DepB ∧
    Has DepΓ (literalObserver (inputNumeral k) (.atom .i) (.atom .i)) DepB :=
  dual_literal_typing
    (P01AC.BooleanPrimitive.closed_has (EffectiveCompleteness.inputNumeral_has k)
      P01AC.BooleanPrimitive.N_subst dep_context) dep_inhabitant dep_inhabitant

theorem dependent_source_identity (k : Nat) :
    HasE DepΓ (.atom .i) (.identity DepB
      (literalObserver (inputNumeral k) (.atom .i) (.atom .i))
      (literalObserver (inputNumeral k) (.atom .i) (.atom .i))) :=
  same_endpoint_identity
    (P01AC.BooleanPrimitive.closed_has (EffectiveCompleteness.inputNumeral_has k)
      P01AC.BooleanPrimitive.N_subst dep_context) dep_inhabitant dep_inhabitant

theorem dependent_exact_zero : HasE DepΓ (.atom .i) (.identity DepB
    (observe (inputNumeral 0) (.atom .i) (.atom .i)) (.atom .i)) :=
  zero_source_identity dep_inhabitant dep_inhabitant

theorem dependent_exact_one : HasE DepΓ (.atom .i) (.identity DepB
    (observe (inputNumeral 1) (.atom .i) (.atom .i)) (.atom .i)) :=
  one_source_identity dep_inhabitant dep_inhabitant

-- Bare unary membership in the two carrier function spaces is compatible
-- with the incompatible observations. No whole-source model is asserted.
def unarySigma (_ : ((Bool × Bool) → (Bool × Bool)) → (Bool × Bool) → (Bool × Bool)) : Prop := True
def unaryChurch (_ : (((Bool → Bool → Bool) → Bool) → ((Bool → Bool → Bool) → Bool)) →
    ((Bool → Bool → Bool) → Bool) → ((Bool → Bool → Bool) → Bool)) : Prop := True

theorem bare_membership_does_not_identify :
    unarySigma (fun _ seed => seed) ∧
    unaryChurch (fun step seed => step seed) ∧
    sigmaObservation (fun _ seed => seed) false true ≠
      churchObservation (fun step seed => step seed) false true :=
  ⟨trivial, trivial, by decide⟩

theorem singleton_shape_split_survives :
    sigmaObservation (fun _ seed => seed) () () =
      churchObservation (fun step seed => step seed) () () := rfl

-- This observer distinguishes zero from positive counts, not arbitrary
-- different positive counts. Its source-typed update is constant.
def iterate {S : Type} : Nat → (S → S) → S → S
  | 0, _, seed => seed
  | k+1, f, seed => f (iterate k f seed)

theorem all_positive_counts_agree {D : Type} (a b : D) (m n : Nat) :
    sigmaObservation (iterate (m+1)) a b =
      churchObservation (iterate (n+1)) a b := rfl

theorem positive_count_not_forced_equal :
    sigmaObservation (iterate 1) false true =
      churchObservation (iterate 2) false true ∧ (1 : Nat) ≠ 2 :=
  ⟨rfl, by decide⟩

#print axioms dependent_dual_pair
#print axioms dependent_dual_step
#print axioms dependent_source_identity
#print axioms dependent_exact_zero
#print axioms dependent_exact_one
#print axioms bare_membership_does_not_identify
#print axioms all_positive_counts_agree
end CrossTypingReview
