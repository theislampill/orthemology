import RuntimeCancellationTrace
import RuntimeControls

namespace OperationalJoin.Offset.CancellationControls
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)
open NativeFixture
open RuntimeControls (partialEnvelope partialPrepared)
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- A bad root alone supplies B replies, which are insufficient and store no
good tombstone; the otherwise legitimate prepared action can still land. -/
theorem B_replies_are_insufficient :
    (cancelWith partialPrepared partialEnvelope.val "A" [0]).2 = false ∧
    (attempt (cancelWith partialPrepared partialEnvelope.val "A" [0]).1
      partialEnvelope.val "A" true).2 = true := by decide

/-- One bad and one good selected reply suffice at B=1. The operation is still
unlanded and its version current, so replay/version checks cannot mask this veto. -/
theorem B_plus_one_closes_unlanded_operation :
    (cancelWith partialPrepared partialEnvelope.val "A" [0,1]).2 = true ∧
    (attempt (cancelWith partialPrepared partialEnvelope.val "A" [0,1]).1
      partialEnvelope.val "A" true).2 = false ∧
    (cancelWith partialPrepared partialEnvelope.val "A" [0,1]).1.plant = before := by decide

theorem wrong_requester_cannot_close :
    (cancelWith partialPrepared partialEnvelope.val "B" [0,1,2]).2 = false ∧
    (attempt (cancelWith partialPrepared partialEnvelope.val "B" [0,1,2]).1
      partialEnvelope.val "A" true).2 = true := by decide

def falseFirst : ComposedExecution.World := (cancelWith start installEnvelope.val "A" [1]).1
def falseSecond : ComposedExecution.World := (cancelWith falseFirst installEnvelope.val "A" [2]).1

theorem false_returns_retain_distinct_partial_tombstones :
    (cancelWith start installEnvelope.val "A" [1]).2 = false ∧
    (cancelWith falseFirst installEnvelope.val "A" [2]).2 = false ∧
    installEnvelope.val ∈ (falseFirst.roots 1).cancelled ∧
    installEnvelope.val ∈ (falseSecond.roots 1).cancelled ∧
    installEnvelope.val ∈ (falseSecond.roots 2).cancelled := by decide

def commonStart : State (interface 2 4) := Initial authority.config before
def commonFalseFirst : State (interface 2 4) :=
  cancelMany authority.config installEnvelope commonStart
    (cancelResponders start installEnvelope "A" [1] (by decide))
def commonFalseSecond : State (interface 2 4) :=
  cancelMany authority.config installEnvelope commonFalseFirst
    (cancelResponders falseFirst installEnvelope "A" [2] (by decide))
def commonRepeated : State (interface 2 4) :=
  cancelMany authority.config installEnvelope commonFalseFirst
    (cancelResponders falseFirst installEnvelope "A" [1] (by decide))

theorem first_responders : cancelResponders start installEnvelope "A" [1] (by decide) = [1] := by decide
theorem second_responders : cancelResponders falseFirst installEnvelope "A" [2] (by decide) = [2] := by decide
theorem repeated_responders : cancelResponders falseFirst installEnvelope "A" [1] (by decide) = [1] := by decide

theorem cumulative_acknowledgement_sets :
    commonFalseFirst.cancelAcks installEnvelope = {1} ∧
    commonFalseSecond.cancelAcks installEnvelope = {1,2} ∧
    commonRepeated.cancelAcks installEnvelope = {1} := by
  simp only [commonFalseSecond, commonRepeated, commonFalseFirst,
    first_responders, second_responders, repeated_responders,
    cancelMany_cancelAcks, if_pos rfl, if_true, commonStart, Initial]
  simp [Finset.insert_comm]
  decide

theorem cumulative_certificate_does_not_equal_current_call_boolean :
    Cancelled authority.config commonFalseSecond installEnvelope ∧
    (cancelWith falseFirst installEnvelope.val "A" [2]).2 = false ∧
    ¬Cancelled authority.config commonRepeated installEnvelope := by
  refine ⟨?_, false_returns_retain_distinct_partial_tombstones.2.1, ?_⟩
  · unfold Cancelled
    rw [cumulative_acknowledgement_sets.2.1]
    decide
  · unfold Cancelled
    rw [cumulative_acknowledgement_sets.2.2]
    decide

theorem cumulative_states_are_genuine :
    Aligned authority falseFirst commonFalseFirst ∧
    Aligned authority falseSecond commonFalseSecond ∧ Reachable authority.config commonFalseSecond := by
  have first := cancelWith_preserves_alignment authority start commonStart start_aligned
    installEnvelope "A" [1] (by decide) (by decide) (by decide)
  have second := cancelWith_preserves_alignment authority falseFirst commonFalseFirst first.1
    installEnvelope "A" [2] (by decide) (by decide) (by decide)
  exact ⟨first.1, second.1, reachable_after (reachable_after start_reachable first.2) second.2⟩

/-- Duplicates and unselected addresses fail before any partial mutation. -/
theorem duplicate_acknowledgements_are_identity :
    cancelWith start installEnvelope.val "A" [1,1] = (start, false) := by
  apply cancelWith_invalid_identity
  intro guard
  have impossible : ¬([1,1] : List Nat).Nodup := by decide
  exact impossible guard.2.1

theorem unselected_acknowledgements_are_identity :
    cancelWith start installEnvelope.val "A" [0] = (start, false) := by
  apply cancelWith_invalid_identity
  intro guard
  have selected := guard.2.2 0 (by simp)
  have impossible : 0 ∉ installEnvelope.val.path := by decide
  exact impossible selected

theorem cleanup_after_revocation_still_records_tombstones :
    installedWorld.effectivePolicy.epoch = 2 ∧ certified.effectivePolicy.epoch = 3 ∧
    (cancelWith certified installEnvelope.val "A" [1,2]).2 = true ∧
    installEnvelope.val ∈ ((cancelWith certified installEnvelope.val "A" [1,2]).1.roots 1).cancelled := by decide

theorem cancellation_does_not_roll_back_a_lawful_landing :
    (cancelWith installedWorld installEnvelope.val "A" [1,2]).2 = true ∧
    (cancelWith installedWorld installEnvelope.val "A" [1,2]).1.plant = installed := by decide

def closedBeforePrepare : ComposedExecution.World := (cancelWith start installEnvelope.val "A" [1,2]).1

theorem delayed_prepare_cannot_reopen_closed_envelope :
    (cancelWith start installEnvelope.val "A" [1,2]).2 = true ∧
    (attempt (ComposedExecution.prepare closedBeforePrepare installEnvelope.val "A" true).1
      installEnvelope.val "A" true).2 = false := by decide

def reordered : BoundedEnvelope 4 :=
  ⟨{ installEnvelope.val with path := [3,2,1] }, by decide⟩

/-- The same numerical nonce does not imply the same complete command. This
witness deliberately does not satisfy a correct actor's fresh-nonce discipline. -/
theorem cancellation_is_full_command_scoped :
    reordered.val.nonce = installEnvelope.val.nonce ∧ reordered ≠ installEnvelope ∧
    (attempt (ComposedExecution.prepare closedBeforePrepare reordered.val "A" true).1
      reordered.val "A" true).2 = true := by decide

/-- Instantiate durable actual-runtime blocking on an unlanded command. -/
theorem native_cancellation_blocks_every_later_trace
    {later : ComposedExecution.World} {events : List (RuntimeWithCancellationEvent 4)}
    (history : RuntimeWithCancellationTrace authority closedBeforePrepare events later)
    (requester : String) (badOpen : Bool) :
    (attempt later installEnvelope.val requester badOpen).2 ≠ true := by
  exact true_runtime_cancel_blocks_all_continuations authority start commonStart start_aligned
    start_reachable installEnvelope "A" [1,2] delayed_prepare_cannot_reopen_closed_envelope.1
    history requester badOpen

#print axioms B_replies_are_insufficient
#print axioms B_plus_one_closes_unlanded_operation
#print axioms false_returns_retain_distinct_partial_tombstones
#print axioms cumulative_certificate_does_not_equal_current_call_boolean
#print axioms cumulative_states_are_genuine
#print axioms duplicate_acknowledgements_are_identity
#print axioms cleanup_after_revocation_still_records_tombstones
#print axioms cancellation_does_not_roll_back_a_lawful_landing
#print axioms cancellation_is_full_command_scoped
#print axioms native_cancellation_blocks_every_later_trace
end
end OperationalJoin.Offset.CancellationControls
