import AliasRuntime
import TypedExamples

namespace SharedAlias.Typed.Witness
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path path_card mem_path)
namespace Fixture
abbrev before := OperationalJoin.Typed.Examples.before
abbrev installed := OperationalJoin.Typed.Examples.installed
abbrev source := OperationalJoin.Typed.Examples.source
abbrev installCommand := OperationalJoin.Typed.Examples.installCommand
end Fixture
noncomputable section
open Classical

def env : Environment (interface 7) where
  aliasClass := {0,1}
  class_positive := by decide
  budget := 1
  budget_positive := by decide
  actualFaults := {some 6}
  actual_faults := by decide
  actual_budget := by decide
  non_saturated := by decide
  q := 5
  r := 5
  overlap := by decide
  repair_available := by decide
  revoke_available := by decide
  source := Fixture.source
  source_epoch := by intro e; rfl

def command : BoundedEnvelope 7 :=
  ⟨⟨.install Fixture.installCommand, Fixture.installed, 41, [0,1,2,3,4]⟩, by decide⟩

def start : SharedAlias.State (interface 7) := initial env Fixture.before
def prepared : SharedAlias.State (interface 7) :=
  prepare env (prepare env (prepare env (prepare env start 0 command) 2 command) 3 command) 4 command

theorem preparation_preserves_envelope {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (preparedCommand checkedCommand : I.Command)
    (who : I.Requester) (time : Nat) :
    Envelope (prepare E C i preparedCommand).plant time
      ((prepare E C i preparedCommand).roots (E.rootOf j)) checkedCommand who ↔
      Envelope C.plant time (C.roots (E.rootOf j)) checkedCommand who := by
  by_cases same : E.rootOf j = E.rootOf i <;>
    simp [Envelope, prepare, setRoot, Function.update_apply, same]

theorem command_valid : ValidPath env.labelConfig command := by
  change (path command).card = 5
  rw [path_card]
  rfl

theorem initial_ready (i : Fin 7) : Envelope start.plant 2 (start.roots (env.rootOf i)) command "A" := by
  refine ⟨⟨rfl, OperationalJoin.Typed.Examples.install_local⟩, ?_, ?_⟩ <;> simp [start, initial]

theorem preparation_trace : SharedAlias.Trace env start
    [.prepare 0 command "A" 2, .prepare 2 command "A" 2,
      .prepare 3 command "A" 2, .prepare 4 command "A" 2] prepared := by
  apply SharedAlias.Trace.cons (SharedAlias.Step.prepare (E := env) _ 0 command "A" 2
    ((mem_path command 0).mpr (by decide)) command_valid (Or.inr (initial_ready 0)))
  apply SharedAlias.Trace.cons (SharedAlias.Step.prepare (E := env) _ 2 command "A" 2
    ((mem_path command 2).mpr (by decide)) command_valid ?_)
  · apply SharedAlias.Trace.cons (SharedAlias.Step.prepare (E := env) _ 3 command "A" 2
      ((mem_path command 3).mpr (by decide)) command_valid ?_)
    · apply SharedAlias.Trace.cons (SharedAlias.Step.prepare (E := env) _ 4 command "A" 2
        ((mem_path command 4).mpr (by decide)) command_valid ?_)
      · exact .nil _
      · right; simpa only [preparation_preserves_envelope] using initial_ready 4
    · right; simpa only [preparation_preserves_envelope] using initial_ready 3
  · right; simpa only [preparation_preserves_envelope] using initial_ready 2

theorem prepared_reachable : SharedAlias.Reachable env prepared :=
  ⟨Fixture.before, _, preparation_trace⟩

/-- Both selected aliases 0 and 1 are prepared by one actual-root store update.
This is a trace existence witness, not a macro-attempt reply/service guarantee. -/
theorem installation_lands : SharedAlias.Lands env prepared 2 command "A" := by
  refine ⟨command_valid, ?_⟩
  intro i selected _good
  have choices : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by
    change i ∈ path command at selected
    have labels := (mem_path command i).mp selected
    change i.val ∈ ([0,1,2,3,4] : List Nat) at labels
    simpa only [List.mem_cons, List.not_mem_nil, or_false, Fin.ext_iff] using labels
  constructor
  · rcases choices with rfl | rfl | rfl | rfl | rfl <;>
      simp [prepared, prepare, setRoot, start, initial, Environment.rootOf,
        env, AttributionKernel.rootMap, Function.update_apply]
  · simpa only [prepared, preparation_preserves_envelope] using initial_ready i

theorem compiled_installation_succeeds :
    (ComposedExecution.attempt (gateWorld env prepared 2) command.val "A" true).2 = true :=
  (compiled_attempt_iff env prepared 2 command "A").mpr installation_lands

theorem installation_effect :
    (ComposedExecution.attempt (gateWorld env prepared 2) command.val "A" true).1.plant =
      Fixture.installed :=
  ComposedExecution.applied_attempt_exact_successor _ _ _ _ compiled_installation_succeeds

def cancelled : SharedAlias.State (interface 7) :=
  cancelAck env (cancelAck env (cancelAck env prepared 0 command) 2 command) 3 command

theorem cancellation_trace : SharedAlias.Trace env prepared
    [.cancelAck 0 command "A", .cancelAck 2 command "A", .cancelAck 3 command "A"] cancelled := by
  apply SharedAlias.Trace.cons (SharedAlias.Step.cancelAck (E := env) _ 0 command "A"
    ((mem_path command 0).mpr (by decide)) (Or.inr rfl))
  apply SharedAlias.Trace.cons (SharedAlias.Step.cancelAck (E := env) _ 2 command "A"
    ((mem_path command 2).mpr (by decide)) (Or.inr rfl))
  apply SharedAlias.Trace.cons (SharedAlias.Step.cancelAck (E := env) _ 3 command "A"
    ((mem_path command 3).mpr (by decide)) (Or.inr rfl))
  exact .nil _

theorem concrete_trace_append {m} {I : Interface m} {E : Environment I}
    {C D F : SharedAlias.State I} {xs ys : List (Event I)}
    (first : SharedAlias.Trace E C xs D) (second : SharedAlias.Trace E D ys F) :
    SharedAlias.Trace E C (xs ++ ys) F := by
  induction first with
  | nil => exact second
  | cons step _ ih => exact .cons step (ih second)

theorem cancelled_reachable : SharedAlias.Reachable env cancelled :=
  ⟨Fixture.before, _, concrete_trace_append preparation_trace cancellation_trace⟩

theorem cancellation_certificate : env.labelBudget < (cancelled.cancelAcks command).card := by
  have receipts : cancelled.cancelAcks command = {3,2,0} := by
    simp only [cancelled, cancelAck_receipts, prepared, prepare, setRoot, start, initial]
    rfl
  have budget : env.labelBudget = 2 := by decide
  rw [receipts, budget]
  decide

theorem cancellation_is_not_version_rejection :
    ComposedExecution.localStep cancelled.plant (env.source cancelled.epoch) 2
      command.val.action = some command.val.successor :=
  OperationalJoin.Typed.Examples.install_local

theorem cancelled_compiled_attempt_rejected (time : Nat) (badOpen : Bool) :
    (ComposedExecution.attempt (gateWorld env cancelled time) command.val "A" badOpen).2 ≠ true := by
  intro success
  have impossible := cancellation_persists cancelled_reachable (SharedAlias.Trace.nil cancelled)
    command cancellation_certificate time "A"
  exact impossible (compiled_success_lands env cancelled time command "A" badOpen success)

end
end SharedAlias.Typed.Witness
