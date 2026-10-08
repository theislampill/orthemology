import NativePolicyInputs
import NativeControls

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (interface rootView)
namespace HistoryFixture

def nextPolicy : Policy := OperationalJoin.Typed.Examples.source 1
def samples : List (Nat × Policy) := [(0, Fixture.policy), (1, nextPolicy)]
def requests : List (HistoryRequest 7) :=
  [.request, .acknowledge 0, .acknowledge 2, .acknowledge 3,
    .acknowledge 4, .acknowledge 5, .complete, .deliver 1 1]
def built : Option (FiniteState 7) := reconstruct Fixture.routes Fixture.before samples requests

def missingSamples : List (Nat × Policy) := [(0, Fixture.policy)]
def wrongEpochSamples : List (Nat × Policy) := [(0, Fixture.policy), (1, Fixture.policy)]
def falsePolicy : Policy := { nextPolicy with actor := "intruder" }

def badEnvironment : SharedAlias.Environment (interface 7) :=
  { Fixture.environment with
    actualFaults := {none}
    actual_faults := by decide
    actual_budget := by decide }

theorem bad_routes_match : RoutingMatches Fixture.badRoutes badEnvironment := by
  constructor <;> decide

def corruptedRoot : Root := ⟨Fixture.policy, [17], [Fixture.k.val], [Fixture.reordered.val]⟩
def corrupted : FiniteState 7 :=
  replayUpdate Fixture.badRoutes Fixture.start (.corrupt 0 corruptedRoot)

end HistoryFixture

theorem finite_history_constructor_succeeds :
    HistoryFixture.built.map FiniteState.epoch = some 1 := by decide

theorem finite_history_updates_shared_descriptor :
    (HistoryFixture.built.map (fun C => (rootAt C (rootOf Fixture.routes 0)).policy)) =
      some HistoryFixture.nextPolicy ∧
    (HistoryFixture.built.map (fun C => (rootAt C (rootOf Fixture.routes 1)).policy)) =
      some HistoryFixture.nextPolicy := by decide

theorem finite_history_preserves_complete_plant :
    HistoryFixture.built.map FiniteState.plant = some Fixture.before := by decide

theorem finite_history_retains_real_certificate :
    (HistoryFixture.built.map (fun C => (tableRead C.certificateRows 0 []).toFinset.card)) = some 5 ∧
    (HistoryFixture.built.map (fun C => decide (1 ∈ tableRead C.certificateRows 0 []))) = some false := by decide

theorem missing_policy_constructor_refuses :
    (reconstruct Fixture.routes Fixture.before HistoryFixture.missingSamples HistoryFixture.requests).isNone = true := by decide

theorem wrong_epoch_constructor_refuses :
    (reconstruct Fixture.routes Fixture.before HistoryFixture.wrongEpochSamples HistoryFixture.requests).isNone = true := by decide

theorem first_match_wrong_policy_refuses :
    (policySample [(1, Fixture.policy), (1, HistoryFixture.nextPolicy)] 1).isNone = true := by decide

theorem shared_revocation_without_certificate_fabrication :
    HistoryFixture.built.map (fun C => decide (0 ∈ (rootAt C (rootOf Fixture.routes 1)).revoked)) = some true ∧
    HistoryFixture.built.map (fun C => decide (1 ∈ tableRead C.certificateRows 0 [])) = some false := by decide

theorem finite_corruption_is_shared :
    (rootAt HistoryFixture.corrupted (rootOf Fixture.badRoutes 1)).revoked = [17] ∧
    (rootAt HistoryFixture.corrupted (rootOf Fixture.badRoutes 1)).cancelled = [Fixture.reordered.val] ∧
    (rootAt HistoryFixture.corrupted (rootOf Fixture.badRoutes 2)).revoked = [] := by decide

theorem finite_corruption_has_accepted_step :
    SharedAlias.Step HistoryFixture.badEnvironment (view Fixture.start)
      (.corrupt 0 (rootView HistoryFixture.corruptedRoot)) (view HistoryFixture.corrupted) := by
  change SharedAlias.Step HistoryFixture.badEnvironment (view Fixture.start)
    (.corrupt 0 (rootView HistoryFixture.corruptedRoot))
    (view (setRoot Fixture.start (rootOf Fixture.badRoutes 0) HistoryFixture.corruptedRoot))
  rw [view_setRoot, rootOf_matches Fixture.badRoutes HistoryFixture.badEnvironment HistoryFixture.bad_routes_match]
  exact SharedAlias.Step.corrupt (E := HistoryFixture.badEnvironment) (view Fixture.start) 0 _ (by decide)

/-- Key/epoch consistency cannot establish authority. The external history
premise must reject this false content despite successful finite lookup. -/
theorem successful_sample_is_not_authentication :
    policySample [(1, HistoryFixture.falsePolicy)] 1 = some HistoryFixture.falsePolicy ∧
    HistoryFixture.falsePolicy ≠ Fixture.environment.source 1 := by decide

/- Compiled finite constructor checks, including missing-input rejection. -/
#eval (HistoryFixture.built.map FiniteState.epoch,
  HistoryFixture.built.map (fun C => (rootAt C (rootOf Fixture.routes 0)).policy.epoch),
  (reconstruct Fixture.routes Fixture.before HistoryFixture.missingSamples HistoryFixture.requests).isNone)

end SharedAlias.Native
