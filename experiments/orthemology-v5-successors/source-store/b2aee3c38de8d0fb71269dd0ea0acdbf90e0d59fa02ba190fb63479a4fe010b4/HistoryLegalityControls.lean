import NativeHistoryControls
namespace IndependentHistoryLegalityReview
open SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (interface)

theorem guard_free_complete_is_constructible :
    (reconstruct Fixture.routes Fixture.before HistoryFixture.samples
      ([.complete] : List (HistoryRequest 7))).map FiniteState.epoch = some 1 := by decide

theorem initial_complete_has_no_accepted_step :
    ¬∃ next : SharedAlias.State (interface 7),
      SharedAlias.Step Fixture.environment (view Fixture.start) .complete next := by
  rintro ⟨next, step⟩
  cases step with
  | complete pending quorum => cases pending

#print axioms guard_free_complete_is_constructible
#print axioms initial_complete_has_no_accepted_step
#eval (reconstruct Fixture.routes Fixture.before HistoryFixture.samples
  ([.complete] : List (HistoryRequest 7))).map FiniteState.epoch
end IndependentHistoryLegalityReview
