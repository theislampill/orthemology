import AliasTypedControls
import AliasObstruction

namespace SharedAlias.ReviewerTypedControls
open OperationalJoin
open SharedAlias.Typed
open SharedAlias.Typed.Witness (env command prepared start)
open OperationalJoin.Typed (interface BoundedEnvelope)
noncomputable section
open Classical

def installedState : SharedAlias.State (interface 7) := SharedAlias.land prepared command

def installationEvents : List (Event (interface 7)) :=
  [.prepare 0 command "A" 2, .prepare 2 command "A" 2,
    .prepare 3 command "A" 2, .prepare 4 command "A" 2, .land command "A" 2]

theorem full_concrete_installation_trace : SharedAlias.Trace env start installationEvents installedState := by
  exact SharedAlias.Typed.Witness.concrete_trace_append SharedAlias.Typed.Witness.preparation_trace
    (.cons (.land prepared command "A" 2 SharedAlias.Typed.Witness.installation_lands) (.nil _))

theorem concrete_installation_counters :
    installedState.plant.ruleVersion = start.plant.ruleVersion + 1 ∧
    installedState.plant.draftRevision = start.plant.draftRevision ∧
    installedState.plant.ruleHistory.length = start.plant.ruleHistory.length + 1 ∧
    installedState.plant.draftHistory.length = start.plant.draftHistory.length := by
  have reach : SharedAlias.Reachable env start := ⟨SharedAlias.Typed.Witness.Fixture.before, [], .nil _⟩
  have counters := SharedAlias.Typed.trace_counters reach full_concrete_installation_trace
  simpa [installationEvents, OperationalJoin.Typed.installCount, OperationalJoin.Typed.repairCount,
    OperationalJoin.Typed.installDelta, OperationalJoin.Typed.repairDelta, command] using counters

theorem concrete_installation_custody :
    OperationalJoin.Typed.Custody SharedAlias.Typed.Witness.Fixture.before installedState.plant :=
  SharedAlias.Typed.finite_history_custody env SharedAlias.Typed.Witness.Fixture.before full_concrete_installation_trace

/-- Typed compiled rejection is permanent after certification, not only at the fixture endpoint. -/
theorem compiled_cancellation_all_continuations {m} {E : Environment (interface m)}
    {C D : SharedAlias.State (interface m)} {events : List (Event (interface m))}
    (reach : SharedAlias.Reachable E C) (trace : SharedAlias.Trace E C events D)
    (k : BoundedEnvelope m) (cert : E.labelBudget < (C.cancelAcks k).card)
    (time : Nat) (who : String) (badOpen : Bool) :
    (ComposedExecution.attempt (gateWorld E D time) k.val who badOpen).2 = false := by
  cases result : (ComposedExecution.attempt (gateWorld E D time) k.val who badOpen).2 with
  | false => rfl
  | true => exact False.elim (cancellation_persists reach trace k cert time who
      (compiled_success_lands E D time k who badOpen result))

def outOfPathCommand : BoundedEnvelope 7 :=
  ⟨{ command.val with path := [0,2,3,4,5] }, by decide⟩

theorem typed_literal_pullback_not_reachable :
    ¬ OperationalJoin.Reachable env.labelConfig
      (literalSnapshot env (prepare env start 0 outOfPathCommand)) := by
  intro reach
  have impossible := no_reachable_literal_prepare env start 0 1 outOfPathCommand
    (by decide) (by decide) (by decide)
  exact impossible ⟨literalSnapshot env (prepare env start 0 outOfPathCommand), reach, Iff.rfl⟩

#print axioms full_concrete_installation_trace
#print axioms concrete_installation_counters
#print axioms concrete_installation_custody
#print axioms compiled_cancellation_all_continuations
#print axioms typed_literal_pullback_not_reachable
end
end SharedAlias.ReviewerTypedControls
