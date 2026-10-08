import TypedControls

namespace TypedV2Review
noncomputable section
open Classical
open OperationalJoin OperationalJoin.Typed OperationalJoin.Typed.Examples
open ComposedExecution

/-- Isolate grant operation from policy scope and numerical epoch: every other
field remains that of the successful accepted-source installation fixture. -/
def installWrongGrantOperation : ComposedExecution.Policy :=
  { source 0 with grant := (source 0).grant.map (fun g => {g with operation := "replace-derived"}) }

def repairWrongGrantOperation : ComposedExecution.Policy :=
  { source 1 with grant := (source 1).grant.map (fun g => {g with operation := "install-criterion"}) }

theorem isolated_grant_operation_controls :
    installWrongGrantOperation.epoch = installCommand.authorizationEpoch ∧
    policyAllows before installWrongGrantOperation (.install installCommand) = true ∧
    localStep before installWrongGrantOperation 2 (.install installCommand) = none ∧
    repairWrongGrantOperation.epoch = repairCommand.authorizationEpoch ∧
    policyAllows installed repairWrongGrantOperation (.repair repairCommand) = true ∧
    localStep installed repairWrongGrantOperation 3 (.repair repairCommand) = none := by
  decide

/-- Malformed raw lists cannot enter the typed command subtype. -/
theorem no_duplicate_typed_path :
    ¬∃ e : BoundedEnvelope 4, e.val.path = [1,1,2] := by
  rintro ⟨e, h⟩
  have nodup := e.property.1
  rw [h] at nodup
  simp at nodup

theorem no_out_of_range_typed_path :
    ¬∃ e : BoundedEnvelope 4, e.val.path = [1,2,4] := by
  rintro ⟨e, h⟩
  have bound := e.property.2 4
  rw [h] at bound
  have bad := bound (by simp)
  omega

/-- Close a prepared but still-unlanded operation. Its expected version is
still current, so cancellation is not masked by fixed-action replay rejection. -/
def closedUnlanded : State (interface 4) :=
  cancelAck cfg (cancelAck cfg preparedInstall 1 installEnvelope) 2 installEnvelope

theorem close_unlanded_trace : Trace cfg preparedInstall
    [.cancelAck 1 installEnvelope "A", .cancelAck 2 installEnvelope "A"] closedUnlanded := by
  apply Trace.cons (Step.cancelAck (c := cfg) _ 1 installEnvelope "A" ?_ (Or.inr rfl))
  · apply Trace.cons (Step.cancelAck (c := cfg) _ 2 installEnvelope "A" ?_ (Or.inr rfl))
    · exact Trace.nil _
    · exact (mem_path installEnvelope (2 : Fin 4)).mpr (by decide)
  · exact (mem_path installEnvelope (1 : Fin 4)).mpr (by decide)

def NoCancellation (s : State (interface 4)) : Prop :=
  ValidPath cfg installEnvelope ∧
    ∀ i ∈ path installEnvelope, Good cfg i →
      installEnvelope ∈ (s.roots i).commitments ∧
      (interface 4).admits s.plant 2 (s.roots i).descriptor installEnvelope "A" ∧
      (interface 4).commandEpoch installEnvelope ∉ (s.roots i).revoked

theorem unlanded_cancellation_guard_is_essential :
    Reachable cfg closedUnlanded ∧
    Cancelled cfg closedUnlanded installEnvelope ∧
    ¬Lands cfg closedUnlanded 2 installEnvelope "A" ∧
    NoCancellation closedUnlanded := by
  have start : Reachable cfg preparedInstall := ⟨before, _, installation_preparation_trace⟩
  have reachable := reachable_after start close_unlanded_trace
  have closed : Cancelled cfg closedUnlanded installEnvelope := by
    simp only [Cancelled, closedUnlanded, cancelAck, Function.update_self]
    change 1 < (insert 2 (insert 1 (preparedInstall.cancelAcks installEnvelope))).card
    change 1 < ({2,1} : Finset (Fin 4)).card
    decide
  refine ⟨reachable, closed, cancelled_cannot_land (reachable_consistent reachable)
    2 installEnvelope "A" closed, ?_⟩
  constructor
  · exact installation_lands.1
  · intro i selected _good
    have cases : i = 1 ∨ i = 2 ∨ i = 3 := by
      simpa [path, installEnvelope, Fin.ext_iff] using selected
    rcases cases with rfl | rfl | rfl <;>
      simp [closedUnlanded, cancelAck, preparedInstall, OperationalJoin.prepare, setRoot, initial,
        Initial, cfg, Good, interface, installEnvelope, Function.update_apply, install_local] <;> rfl

/-- The cancellation property remains true even if later events are annotated
with arbitrary decreasing times; it is a memory theorem, not a clock theorem. -/
theorem cancellation_survives_any_annotation {t : State (interface 4)}
    {events : List (Event (interface 4))} (history : Trace cfg closedUnlanded events t)
    (annotation : Nat) : ¬Lands cfg t annotation installEnvelope "A" := by
  exact no_landing_after_cancellation unlanded_cancellation_guard_is_essential.1
    history annotation installEnvelope "A" unlanded_cancellation_guard_is_essential.2.1

#print axioms isolated_grant_operation_controls
#print axioms no_duplicate_typed_path
#print axioms no_out_of_range_typed_path
#print axioms close_unlanded_trace
#print axioms unlanded_cancellation_guard_is_essential
#print axioms cancellation_survives_any_annotation
end
end TypedV2Review
