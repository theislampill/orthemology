import RuntimeFixture
import OffsetHistoryProperties

namespace OperationalJoin.Offset.RuntimeControls
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)
open NativeFixture
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

def partialEnvelope : BoundedEnvelope 4 :=
  ⟨{ installEnvelope.val with nonce := 31, path := [0,1,2] }, by decide⟩
def partialPrepared : ComposedExecution.World :=
  (ComposedExecution.prepare start partialEnvelope.val "A" false).1

/-- A false aggregate return does not erase the two actual intact commitments. -/
theorem partial_prepare_is_not_identity :
    (ComposedExecution.prepare start partialEnvelope.val "A" false).2 = false ∧
    partialEnvelope.val ∈ (partialPrepared.roots 1).commitments ∧
    partialEnvelope.val ∈ (partialPrepared.roots 2).commitments ∧
    partialEnvelope.val ∉ (partialPrepared.roots 0).commitments := by decide

/-- One shared Boolean changes only faulty gate behaviour. Honest commitments
from partial preparation still bind the complete valid source successor. -/
theorem shared_badOpen_has_exact_runtime_force :
    (attempt partialPrepared partialEnvelope.val "A" false).2 = false ∧
    (attempt partialPrepared partialEnvelope.val "A" true).2 = true := by decide

theorem partial_prepare_actual_trace :
    RuntimeTrace authority start
      [.prepare partialEnvelope "A" false, .attempt partialEnvelope "A" true]
      (attempt partialPrepared partialEnvelope.val "A" true).1 := by
  exact .cons (.prepare start partialEnvelope "A" false)
    (.cons (.attempt partialPrepared partialEnvelope "A" true) (.nil _))

theorem partial_prepare_has_common_trace :
    ∃ next events, Aligned authority (attempt partialPrepared partialEnvelope.val "A" true).1 next ∧
      Trace authority.config (Initial authority.config before) events next :=
  runtime_trace_refines_history authority start_aligned start_reachable partial_prepare_actual_trace

/-- Certificate-shape checking alone cannot establish the authentic owner
policy source. This exact runtime accepts the same-epoch altered full Policy. -/
def forgedPolicy : ComposedExecution.Policy :=
  { NativeFixture.source 1 with actor := "unauthenticated-owner" }
def forgedWorld : ComposedExecution.World :=
  (certifyTransition installedWorld [1,2,3] forgedPolicy).1

theorem same_epoch_policy_shape_is_not_authenticity :
    forgedPolicy.epoch = (NativeFixture.source 1).epoch ∧
    forgedPolicy ≠ NativeFixture.source 1 ∧
    (certifyTransition installedWorld [1,2,3] forgedPolicy).2 =
      some ⟨2, forgedPolicy, [1,2,3]⟩ := by decide

theorem forged_effective_policy : forgedWorld.effectivePolicy = forgedPolicy := by decide

theorem forged_policy_cannot_preserve_alignment (s : State (interface 2 4)) :
    ¬Aligned authority forgedWorld s := by
  intro alignment
  have raw := aligned_raw_epoch alignment
  rw [forged_effective_policy] at raw
  have epoch : s.epoch = 1 := by
    change 3 = 2 + s.epoch at raw
    omega
  have policy := alignment.effective_policy
  rw [forged_effective_policy, epoch] at policy
  exact same_epoch_policy_shape_is_not_authenticity.2.1 policy

/-- Old raw commands remain expressible and are rejected by actual good gates. -/
def oldRawCommand : CriterionInstallation.InstallCommand :=
  { _root_.installCommand with authorizationEpoch := 1 }
def oldRawEnvelope : BoundedEnvelope 4 :=
  ⟨⟨.install oldRawCommand, installed, 40, [0,1,2]⟩, by decide⟩

theorem prebase_raw_command_is_rejected :
    oldRawEnvelope.val.action.epoch = 1 ∧
    (attempt (ComposedExecution.prepare start oldRawEnvelope.val "A" true).1
      oldRawEnvelope.val "A" true).2 = false := by decide

def prebaseCertificate : ComposedExecution.Certificate :=
  ⟨0, _root_.policy "replace-derived" 1, [1,2,3]⟩

theorem prebase_certificate_not_in_completed : prebaseCertificate ∉ certified.completed := by decide

theorem prebase_delivery_is_identity :
    ComposedExecution.deliver certified prebaseCertificate = certified := by
  simp [ComposedExecution.deliver, prebase_certificate_not_in_completed]

/-- A genuinely valid actual lease does not rescue a proposal made from the
actor's non-admitting stored clock. The runtime does not substitute World.now. -/
theorem stale_actor_clock_not_replaced_by_actual_clock :
    start.now = 2 ∧
    propose { installActor with observedTime := 100 } (.install _root_.installCommand) [1,2,3] = none ∧
    localStep before (NativeFixture.source 0) start.now (.install _root_.installCommand) = some installed := by
  exact ⟨rfl, by decide, install_local⟩

/-- The raw two-stage fields used by compiled grant checks were never renumbered. -/
theorem raw_fixture_coordinates_retained :
    _root_.installCommand.authorizationEpoch = 2 ∧
    (_root_.repairCommand sourceBytes).authorizationEpoch = 3 ∧
    (NativeFixture.source 0).epoch = 2 ∧ (NativeFixture.source 1).epoch = 3 ∧
    (interface 2 4).commandEpoch installEnvelope = 0 ∧
    (interface 2 4).commandEpoch repairEnvelope = 1 := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

#print axioms partial_prepare_is_not_identity
#print axioms shared_badOpen_has_exact_runtime_force
#print axioms partial_prepare_has_common_trace
#print axioms same_epoch_policy_shape_is_not_authenticity
#print axioms forged_policy_cannot_preserve_alignment
#print axioms prebase_raw_command_is_rejected
#print axioms prebase_delivery_is_identity
#print axioms stale_actor_clock_not_replaced_by_actual_clock
end
end OperationalJoin.Offset.RuntimeControls
