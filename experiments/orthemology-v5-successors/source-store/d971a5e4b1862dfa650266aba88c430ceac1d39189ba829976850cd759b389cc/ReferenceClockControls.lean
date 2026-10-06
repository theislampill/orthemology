import MonotoneReferenceTrace
import RuntimeCancellationControls

namespace OperationalJoin.Offset.ReferenceClockControls
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)
open NativeFixture
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

def atThree : ComposedExecution.World := setReferenceTime start 3
def preparedAtThree : ComposedExecution.World := (ComposedExecution.prepare atThree installEnvelope.val "A" false).1
def installedAtThree : ComposedExecution.World := (attempt preparedAtThree installEnvelope.val "A" false).1
def certifiedAtThree : ComposedExecution.World := (certifyTransition installedAtThree [1,2,3] (source 1)).1
def deliveredAtThree : ComposedExecution.World := ComposedExecution.deliver certifiedAtThree certificate
def atFour : ComposedExecution.World := setReferenceTime deliveredAtThree 4
def preparedAtFour : ComposedExecution.World := (ComposedExecution.prepare atFour repairEnvelope.val "A" false).1
def finishedAtFour : ComposedExecution.World := (attempt preparedAtFour repairEnvelope.val "A" false).1

def timedEvents : List (MonotoneReferenceEvent 4) :=
  [.advance 3, .ordinary (.ordinary (.prepare installEnvelope "A" false)),
   .ordinary (.ordinary (.attempt installEnvelope "A" false)),
   .ordinary (.ordinary (.certify 0 [1,2,3])),
   .ordinary (.ordinary (.deliver certificate)), .advance 4,
   .ordinary (.ordinary (.prepare repairEnvelope "A" false)),
   .ordinary (.ordinary (.attempt repairEnvelope "A" false))]

theorem time_advancing_installation_repair_trace :
    MonotoneReferenceTrace authority start timedEvents finishedAtFour := by
  apply MonotoneReferenceTrace.cons (MonotoneReferenceStep.advance start 3 (by decide))
  apply MonotoneReferenceTrace.cons (.ordinary (.ordinary (RuntimeStep.prepare atThree installEnvelope "A" false)))
  apply MonotoneReferenceTrace.cons (.ordinary (.ordinary (RuntimeStep.attempt preparedAtThree installEnvelope "A" false)))
  apply MonotoneReferenceTrace.cons (.ordinary (.ordinary
    (RuntimeStep.certify installedAtThree 0 [1,2,3] (by decide) (by decide) rfl (by decide))))
  apply MonotoneReferenceTrace.cons (.ordinary (.ordinary (RuntimeStep.deliver certifiedAtThree certificate)))
  apply MonotoneReferenceTrace.cons (.advance deliveredAtThree 4 (by decide))
  apply MonotoneReferenceTrace.cons (.ordinary (.ordinary (RuntimeStep.prepare atFour repairEnvelope "A" false)))
  apply MonotoneReferenceTrace.cons (.ordinary (.ordinary (RuntimeStep.attempt preparedAtFour repairEnvelope "A" false)))
  exact .nil _

theorem time_advancing_trace_has_exact_effect :
    (ComposedExecution.prepare atThree installEnvelope.val "A" false).2 = true ∧
    (attempt preparedAtThree installEnvelope.val "A" false).2 = true ∧
    (certifyTransition installedAtThree [1,2,3] (source 1)).2 = some certificate ∧
    (ComposedExecution.prepare atFour repairEnvelope.val "A" false).2 = true ∧
    (attempt preparedAtFour repairEnvelope.val "A" false).2 = true ∧
    finishedAtFour.plant = repaired ∧ finishedAtFour.now = 4 := by
  have prepareInstall : (ComposedExecution.prepare atThree installEnvelope.val "A" false).2 = true := by decide
  have landInstall : (attempt preparedAtThree installEnvelope.val "A" false).2 = true := by decide
  have certify : (certifyTransition installedAtThree [1,2,3] (source 1)).2 = some certificate := by decide
  have prepareRepair : (ComposedExecution.prepare atFour repairEnvelope.val "A" false).2 = true := by decide
  have landRepair : (attempt preparedAtFour repairEnvelope.val "A" false).2 = true := by decide
  refine ⟨prepareInstall, landInstall, certify, prepareRepair, landRepair, ?_, ?_⟩
  · unfold finishedAtFour
    rw [attempt_success_effect preparedAtFour repairEnvelope.val "A" false landRepair]
    rfl
  · rfl

theorem time_advancing_trace_has_common_witness :
    ∃ next events, Aligned authority finishedAtFour next ∧
      Trace authority.config (Initial authority.config before) events next :=
  monotone_reference_trace_refines_history authority start_aligned start_reachable
    time_advancing_installation_repair_trace

/-- Cached commitments do not bypass the current clock check. The boundary is
strict and is the command's lease end 90, before the grant's expiry 100. -/
theorem exact_install_lease_boundary :
    (attempt (setReferenceTime installPrepared 89) installEnvelope.val "A" false).2 = true ∧
    (attempt (setReferenceTime installPrepared 90) installEnvelope.val "A" false).2 = false ∧
    (setReferenceTime installPrepared 90).roots = installPrepared.roots := by
  exact ⟨by decide, by decide, rfl⟩

theorem exact_repair_lease_boundary :
    (attempt (setReferenceTime repairPrepared 89) repairEnvelope.val "A" false).2 = true ∧
    (attempt (setReferenceTime repairPrepared 90) repairEnvelope.val "A" false).2 = false := by
  exact ⟨by decide, by decide⟩

/-- Unrestricted structural alignment alone does not imply durable expiry.
Rolling the reference annotation back resurrects this unlanded, uncancelled
complete envelope. Such a rollback is excluded by the monotone trace class. -/
theorem backward_time_resurrects_uncancelled_envelope :
    (attempt (setReferenceTime installPrepared 100) installEnvelope.val "A" false).2 = false ∧
    (attempt (setReferenceTime (setReferenceTime installPrepared 100) 2)
      installEnvelope.val "A" false).2 = true := by decide

theorem backward_time_has_no_monotone_trace :
    ¬∃ events, MonotoneReferenceTrace authority (setReferenceTime installPrepared 100) events
      (setReferenceTime (setReferenceTime installPrepared 100) 2) := by
  rintro ⟨events, history⟩
  have impossible := monotone_reference_trace_time history
  change 100 ≤ 2 at impossible
  omega

theorem reference_update_does_not_refresh_actor_observation :
    installActor.observedTime = 2 ∧ (setReferenceTime start 90).now = 90 ∧
    propose installActor (.install _root_.installCommand) [1,2,3] = some installEnvelope.val ∧
    (attempt (ComposedExecution.prepare (setReferenceTime start 90) installEnvelope.val "A" false).1
      installEnvelope.val "A" false).2 = false := by
  exact ⟨rfl, rfl, install_proposal_from_actor_observation, by decide⟩

theorem advancing_or_rolling_back_does_not_erase_cancellation :
    (attempt (ComposedExecution.prepare
      (setReferenceTime (setReferenceTime CancellationControls.closedBeforePrepare 100) 2)
      installEnvelope.val "A" true).1 installEnvelope.val "A" true).2 = false ∧
    installEnvelope.val ∈
      ((setReferenceTime (setReferenceTime CancellationControls.closedBeforePrepare 100) 2).roots 1).cancelled := by decide

/-- The exact actor proposal remains a separately checked premise: authentic
looking but non-admitting observation 0 does not borrow the live clock 2. -/
theorem earlier_nonadmitting_actor_observation_is_not_repaired :
    (attempt installPrepared installEnvelope.val "A" false).2 = true ∧
    propose { installActor with observedTime := 0 } (.install _root_.installCommand) [1,2,3] = none := by decide

#print axioms time_advancing_trace_has_exact_effect
#print axioms time_advancing_trace_has_common_witness
#print axioms backward_time_resurrects_uncancelled_envelope
#print axioms reference_update_does_not_refresh_actor_observation
end
end OperationalJoin.Offset.ReferenceClockControls
