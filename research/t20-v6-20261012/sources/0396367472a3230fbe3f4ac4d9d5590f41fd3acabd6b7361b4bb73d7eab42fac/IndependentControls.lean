import TypedFamilyContract

/- Independent controls. No author or predecessor declaration is changed. -/
namespace TypedObserverReview
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral)
open TypedStructuredObserver TypedObserverFamilyContract TypeIndexedFamilyObstructions
set_option maxRecDepth 8192

-- B depends genuinely on both an outer type parameter and an outer term.
def DepΓ : Tel := [.param 0]
def DepB : Ty := .identity (.param 0) (.var 0) (.var 0)

theorem dep_context : Ctx DepΓ := .ext .nil (.param .nil)
theorem dep_value : Has DepΓ (.var 0) (.param 0) :=
  .var (.param dep_context) .zero
theorem dep_formed : Form DepΓ DepB :=
  .identity (.param dep_context) dep_value dep_value
theorem dep_inhabitant : Has DepΓ (.atom .i) DepB :=
  .identityIntro dep_formed dep_value dep_value (.refl _)
theorem dep_update : Has DepΓ (.atom .i) (arr DepB DepB) :=
  .i dep_formed (form_arr dep_formed dep_formed)

theorem dep_term_weakened :
    wk DepB = .identity (.param 0) (.var 1) (.var 1) := rfl
theorem dep_type_weakened :
    twk DepB = .identity (.param 1) (.var 0) (.var 0) := rfl
theorem dep_telescope_weakened : twkTel DepΓ ≠ DepΓ := by decide
theorem dep_type_not_fixed : twk DepB ≠ DepB := by decide
theorem dep_term_not_fixed : wk DepB ≠ DepB := by decide

-- The body must shift B's term dependency beneath its state binder.
theorem dependent_body :
    Has (Carrier DepB :: DepΓ) (body (.atom .i))
      (Carrier (.identity (.param 0) (.var 1) (.var 1))) := body_has dep_update

theorem dependent_fresh :
    Has (twkTel DepΓ) (observe (inputNumeral 0) (.atom .i) (.atom .i))
      (.identity (.param 1) (.var 0) (.var 0)) :=
  observe_fresh_has
    (P01AC.BooleanPrimitive.closed_has (EffectiveCompleteness.inputNumeral_has 0)
      P01AC.BooleanPrimitive.N_subst dep_context) dep_update dep_inhabitant

theorem dependent_all :
    Has DepΓ (observe (inputNumeral 0) (.atom .i) (.atom .i))
      (.all (.identity (.param 1) (.var 0) (.var 0))) :=
  observe_all_has
    (P01AC.BooleanPrimitive.closed_has (EffectiveCompleteness.inputNumeral_has 0)
      P01AC.BooleanPrimitive.N_subst dep_context) dep_update dep_inhabitant

theorem dependent_specialize_any {T : Ty} (hT : Form DepΓ T) :
    Has DepΓ (observe (inputNumeral 0) (.atom .i) (.atom .i)) DepB :=
  observe_specialized_has
    (P01AC.BooleanPrimitive.closed_has (EffectiveCompleteness.inputNumeral_has 0)
      P01AC.BooleanPrimitive.N_subst dep_context) dep_update dep_inhabitant hT

theorem dependent_zero_identity : HasE DepΓ (.atom .i)
    (.identity DepB (observe (inputNumeral 0) (.atom .i) (.atom .i)) (.atom .i)) :=
  zero_source_identity dep_update dep_inhabitant

theorem dependent_constant_one_identity : HasE DepΓ (.atom .i)
    (.identity DepB (observe (inputNumeral 1) (constUpdate (.atom .i)) (.atom .i))
      (.atom .i)) := one_constant_source_identity dep_inhabitant dep_inhabitant

-- Dropping erased-cycle coherence allows varying family values despite
-- perfectly compositional constant-body reintroduction.
def freeDecode (x : Bool → Bool) (i : Bool) : Bool := x i
def freeReintro (r : Bool) (x : Bool → Bool) : Bool → Bool := fun _ => x r

theorem free_assembly : ∀ r x i, freeDecode (freeReintro r x) i = freeDecode x r :=
  fun _ _ _ => rfl

theorem free_cycle_fails : ¬ (∀ r x, freeReintro r x = x) := by
  intro h
  have e := congrFun (h false id) true
  have bad : false = true := e
  cases bad

theorem free_varying_assembly : ∃ result : Bool → Bool, ∀ i,
    freeDecode result i = structuredObservation testX varying (fun _ => true) false i := by
  refine ⟨id, ?_⟩
  intro i
  cases i <;> rfl

-- Dropping compositional reintroduction allows the erased-cycle equation.
def badReintro (_ : Bool) (x : Bool → Bool) : Bool → Bool := x

theorem bad_cycle : ∀ r x, badReintro r x = x := fun _ _ => rfl

theorem bad_assembly_fails :
    ¬ (∀ r x i, freeDecode (badReintro r x) i = freeDecode x r) := by
  intro h
  have bad : true = false := h false id true
  cases bad

-- A coherent contract alone is consistent; the rejected candidate needs
-- the separate structured-observer body assembly obligation.
theorem coherent_without_varying_body :
    (∃ _c : FixedAllContract Bool Bool Bool, True) ∧
      ¬ ∃ result : Bool, ∀ i,
        (constant_contract Bool Bool).decode result i =
          structuredObservation testX varying (fun _ => true) false i := by
  exact ⟨⟨constant_contract Bool Bool, trivial⟩,
    collapsed_raw_does_not_remove_this_test.2⟩

-- This particular observation alone does not impose generic naturality.
-- The same varying candidate is invisible to an identity update even in Bool.
theorem varying_invisible_to_identity_update : ∃ result : Bool, ∀ i,
    (constant_contract Bool Bool).decode result i =
      structuredObservation testX varying id false i := by
  refine ⟨false, ?_⟩
  intro i
  cases i <;> rfl

-- Without a discriminator a != b, varying zero/one coordinates do assemble.
def singletonVary (i : Bool) (step : (Unit × (testX i → testX i)) →
    (Unit × (testX i → testX i))) (seed : Unit × (testX i → testX i)) :=
  if i then step seed else seed

theorem singleton_discriminator_survives : ∃ result : Unit, ∀ i,
    (constant_contract Bool Unit).decode result i =
      structuredObservation testX singletonVary (fun _ => ()) () i := by
  refine ⟨(), ?_⟩
  intro i
  exact Subsingleton.elim _ _

-- Constant numeral coordinates satisfy the observer assembly obligation.
def constantZero (i : Bool) (_step : (Bool × (testX i → testX i)) →
    (Bool × (testX i → testX i))) (seed : Bool × (testX i → testX i)) := seed

def constantOne (i : Bool) (step : (Bool × (testX i → testX i)) →
    (Bool × (testX i → testX i))) (seed : Bool × (testX i → testX i)) := step seed

theorem coherent_zero_assembles : ∃ result : Bool, ∀ i,
    (constant_contract Bool Bool).decode result i =
      structuredObservation testX constantZero (fun _ => true) false i :=
  ⟨false, fun _ => rfl⟩

theorem coherent_one_assembles : ∃ result : Bool, ∀ i,
    (constant_contract Bool Bool).decode result i =
      structuredObservation testX constantOne (fun _ => true) false i :=
  ⟨true, fun _ => rfl⟩

#print axioms dependent_body
#print axioms dependent_fresh
#print axioms dependent_all
#print axioms dependent_specialize_any
#print axioms dependent_constant_one_identity
#print axioms free_cycle_fails
#print axioms bad_assembly_fails
#print axioms singleton_discriminator_survives
#print axioms coherent_zero_assembles
#print axioms coherent_one_assembles
end TypedObserverReview
