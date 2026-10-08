import VeracityControls
set_option synthInstance.maxSize 100000

/-! Independent reviewer probes. These are signature-level mathematical tests,
not claims about metaphysical realizability or exhaustive knowledge. -/
namespace VeracityIndependentReview
open VeracityBoundary VeracityBoundary.Controls

-- A source that only has labelled assertions, with no actual-exercise bridge,
-- can satisfy all six displayed package premises while asserting falsehood.
def missingExercise : Fixture := { dropP with actual := fun _ _ _ => False }

theorem exercise_bridge_is_substantive :
    K missingExercise false ∧ A missingExercise false ∧ C missingExercise false ∧
    D missingExercise false ∧ N missingExercise false ∧ P missingExercise false ∧
    Factive missingExercise false ∧ ¬ ExerciseBridge missingExercise false ∧
    FalseOwned missingExercise ∧ ¬ Veracity missingExercise false := by
  simp only [K, A, C, D, N, P, Factive, ExerciseBridge, FalseOwned, Veracity,
    Counterfeit, missingExercise, dropP, fixture, id]
  decide

-- Without factivity, a bare knowsFalse label can falsely attach to true
-- content. Truth then need not exclude descriptive counterfeit.
def nonfactive : Fixture := { positive with knowsFalse := fun _ _ _ => True }

theorem factivity_guards_forward_equivalence :
    K nonfactive false ∧ A nonfactive false ∧ C nonfactive false ∧
    Veracity nonfactive false ∧ ¬ Factive nonfactive false ∧
    Counterfeit nonfactive false false false true ∧ ¬ NoCounterfeit nonfactive false := by
  simp only [K, A, C, Veracity, Factive, Counterfeit, NoCounterfeit, nonfactive, positive]
  decide

-- No-counterfeit does not give truth without coverage even with K/factivity.
theorem coverage_guards_reverse_equivalence :
    K dropA false ∧ C dropA false ∧ Factive dropA false ∧
    NoCounterfeit dropA false ∧ ¬ A dropA false ∧ ¬ Veracity dropA false := by
  simp only [K, C, Factive, NoCounterfeit, Counterfeit, A, Veracity, dropA, fixture]
  decide

-- The source-specific package cannot transfer to a distinct false speaker.
theorem package_does_not_transfer_to_created_speaker :
    Package positive false ∧ Factive positive false ∧ supplies false true ∧
    ¬ Veracity positive true ∧ ¬ Package positive true := by
  simp only [Package, K, A, C, D, N, P, ExerciseBridge, Factive, supplies, Veracity,
    Counterfeit, positive, id]
  decide

-- The nonconverse really uses a separate, nonassertoric source exercise.
theorem other_unfitting_exercise_is_nonassertoric :
    Veracity nonconforming false ∧ nonconforming.actual false false true ∧
    ¬ nonconforming.fitting false false true ∧
    ¬ (∃ t q, nonconforming.asserts false false t q ∧ nonconforming.exercise t = true) := by
  simp only [Veracity, nonconforming, positive, id]
  decide

-- Strong ownership is compatible with known falsity, defect and fittingness
-- in the N-removal signature. None of these is erased by strengthening ownership.
theorem strong_false_ownership_retains_D_and_P :
    K (informedOwnership dropN) false ∧ D (informedOwnership dropN) false ∧
    P (informedOwnership dropN) false ∧
    (informedOwnership dropN).asserts false false false false ∧
    (informedOwnership dropN).knowsFalse false false false ∧
    (informedOwnership dropN).shortcoming false false false ∧
    (informedOwnership dropN).fitting false false false ∧
    ¬ N (informedOwnership dropN) false := by
  simp only [K, D, P, N, Counterfeit, informedOwnership, dropN, fixture, id]
  decide

universe u v w x y
variable {S : Type u} {O : Type v} {T : Type w} {Q : Type x} {E : Type y}
variable (m : Model S O T Q E) (g : S)

-- The directions consume different semantic assumptions. Normative predicates
-- enter neither direction; factivity is unnecessary for the reverse direction.
theorem truth_to_no_counterfeit (factive : Factive m g)
    (truth : Veracity m g) : NoCounterfeit m g :=
  fun c t q cf => factive c q cf.2.1 (truth c t q cf.1)

theorem no_counterfeit_to_truth (knowledge : K m g) (awareness : A m g)
    (control : C m g) (integrity : NoCounterfeit m g) : Veracity m g :=
  fun c t q owned => Classical.byContradiction fun hf =>
    integrity c t q ⟨owned, knowledge c t q owned hf,
      awareness c t q owned, control c t q owned⟩

end VeracityIndependentReview
