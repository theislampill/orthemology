import RuntimeTrace
import Fixtures
import PinnedSource

namespace OperationalJoin.Offset.NativeFixture
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)
set_option maxRecDepth 40000
set_option maxHeartbeats 8000000

/-- Exactly the accepted native fixture's raw installation epoch 2 and repair
policy at raw epoch 3. Only the proof-side source index starts at zero. -/
def source (index : Nat) : ComposedExecution.Policy :=
  _root_.policy (if index = 0 then "install-criterion" else "replace-derived") (2 + index)

def authority : Authority 2 4 where
  source := source
  raw_epoch := by intro index; rfl
  budget := 1
  q := 3
  r := 3
  faulty := {0}
  budget_bound := by decide
  overlap := by decide
  budget_lt_roots := by decide
  repair_available := by decide
  revoke_available := by decide

def before : ComposedExecution.Plant := _root_.plant sourceBytes
def installed : ComposedExecution.Plant :=
  { before with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] }
def repaired : ComposedExecution.Plant :=
  { installed with draft := sourceBytes, draftRevision := 9
                   draftHistory := [[88], sourceBytes ++ [10]] }

def installEnvelope : BoundedEnvelope 4 :=
  ⟨⟨.install _root_.installCommand, installed, 1, [1,2,3]⟩, by decide⟩
def repairEnvelope : BoundedEnvelope 4 :=
  ⟨⟨.repair (_root_.repairCommand sourceBytes), repaired, 2, [1,2,3]⟩, by decide⟩

def installActor : ComposedExecution.Actor :=
  ⟨source 0, before, "A", 2, 0⟩
def repairActor : ComposedExecution.Actor :=
  ⟨source 1, installed, "A", 2, 1⟩

theorem install_local :
    localStep before (source 0) 2 (.install _root_.installCommand) = some installed := by
  rfl

theorem repair_local :
    localStep installed (source 1) 2 (.repair (_root_.repairCommand sourceBytes)) = some repaired := by
  simp [localStep, policyAllows, installed, before, source, _root_.plant, _root_.policy,
    _root_.repairCommand, CriterionInstallation.accepts, CriterionInstallation.Accepts,
    TypedCriterionGuard.execute, TypedCriterionGuard.guard, TypedCriterionGuard.ContextValid,
    TypedCriterionGuard.GrantValid, TypedCriterionGuard.applyCommand, dataState, repairProjection,
    Action.actor, Action.operation]
  rfl

theorem install_proposal_from_actor_observation :
    propose installActor (.install _root_.installCommand) [1,2,3] = some installEnvelope.val := by
  simp [propose, installActor, install_local, installEnvelope]

theorem repair_proposal_from_predicted_plant :
    propose repairActor (.repair (_root_.repairCommand sourceBytes)) [1,2,3] = some repairEnvelope.val := by
  simp [propose, repairActor, repair_local, repairEnvelope]

def start : ComposedExecution.World := initialWorld before (source 0) [0]
def installPrepared : ComposedExecution.World :=
  (ComposedExecution.prepare start installEnvelope.val "A" false).1
def installedWorld : ComposedExecution.World :=
  (attempt installPrepared installEnvelope.val "A" false).1

def certificate : ComposedExecution.Certificate := ⟨2, source 1, [1,2,3]⟩
def certified : ComposedExecution.World :=
  (certifyTransition installedWorld [1,2,3] (source 1)).1
def delivered : ComposedExecution.World := ComposedExecution.deliver certified certificate
def repairPrepared : ComposedExecution.World :=
  (ComposedExecution.prepare delivered repairEnvelope.val "A" false).1
def finalWorld : ComposedExecution.World :=
  (attempt repairPrepared repairEnvelope.val "A" false).1

theorem runtime_install_prepares :
    (ComposedExecution.prepare start installEnvelope.val "A" false).2 = true := by decide

theorem runtime_install_lands :
    (attempt installPrepared installEnvelope.val "A" false).2 = true := by decide

theorem runtime_certifies_exact_policy :
    (certifyTransition installedWorld [1,2,3] (source 1)).2 = some certificate := by decide

theorem runtime_repair_prepares :
    (ComposedExecution.prepare delivered repairEnvelope.val "A" false).2 = true := by decide

theorem runtime_repair_lands :
    (attempt repairPrepared repairEnvelope.val "A" false).2 = true := by decide

def runtimeEvents : List (RuntimeEvent 4) :=
  [.prepare installEnvelope "A" false, .attempt installEnvelope "A" false,
   .certify 0 [1,2,3], .deliver certificate,
   .prepare repairEnvelope "A" false, .attempt repairEnvelope "A" false]

theorem exact_runtime_history : RuntimeTrace authority start runtimeEvents finalWorld := by
  apply RuntimeTrace.cons (RuntimeStep.prepare start installEnvelope "A" false)
  apply RuntimeTrace.cons (RuntimeStep.attempt installPrepared installEnvelope "A" false)
  apply RuntimeTrace.cons (RuntimeStep.certify installedWorld 0 [1,2,3] ?_ (by decide) rfl (by decide))
  · apply RuntimeTrace.cons (RuntimeStep.deliver certified certificate)
    apply RuntimeTrace.cons (RuntimeStep.prepare delivered repairEnvelope "A" false)
    apply RuntimeTrace.cons (RuntimeStep.attempt repairPrepared repairEnvelope "A" false)
    exact RuntimeTrace.nil _
  · change installedWorld.effectivePolicy.epoch = 2
    unfold installedWorld
    rw [attempt_success_effect installPrepared installEnvelope.val "A" false runtime_install_lands]
    rfl

theorem start_aligned : Aligned authority start (Initial authority.config before) := by
  apply initial_aligned authority before [0] rfl rfl rfl
  intro i
  simp [authority]

theorem start_reachable : Reachable authority.config (Initial authority.config before) :=
  ⟨before, [], Trace.nil _⟩

/-- The six actual aggregate operations have a genuine primitive interlock
history. This is an existence witness on a chosen intact path, not an actor's
fault-discovery strategy or a portfolio progress theorem. -/
theorem exact_runtime_has_common_history :
    ∃ next events, Aligned authority finalWorld next ∧
      Trace authority.config (Initial authority.config before) events next :=
  runtime_trace_refines_history authority start_aligned start_reachable exact_runtime_history

theorem runtime_full_final_plant : finalWorld.plant = repaired := by
  exact applied_attempt_exact_successor repairPrepared repairEnvelope.val "A" false runtime_repair_lands

theorem runtime_full_source_and_audits :
    finalWorld.plant.source = before.source ∧
    finalWorld.plant.destination = before.destination ∧
    finalWorld.plant.standard = before.standard ∧
    finalWorld.plant.unrelated = before.unrelated ∧
    finalWorld.plant.rule = .exact ∧ finalWorld.plant.draft = sourceBytes ∧
    finalWorld.plant.ruleVersion = 4 ∧ finalWorld.plant.draftRevision = 9 ∧
    finalWorld.plant.ruleHistory = [.normalizedLF] ∧
    finalWorld.plant.draftHistory = [[88], sourceBytes ++ [10]] := by
  rw [runtime_full_final_plant]
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

#print axioms install_proposal_from_actor_observation
#print axioms repair_proposal_from_predicted_plant
#print axioms runtime_install_lands
#print axioms runtime_repair_lands
#print axioms exact_runtime_history
#print axioms exact_runtime_has_common_history
#print axioms runtime_full_source_and_audits
end
end OperationalJoin.Offset.NativeFixture
