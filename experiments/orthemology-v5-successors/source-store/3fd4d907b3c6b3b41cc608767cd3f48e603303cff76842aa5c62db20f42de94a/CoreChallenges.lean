import OriginalTranslation
import TypedInstantiation

/- Independent statement-boundary challenges. These use the frozen public
interfaces and do not modify either accepted predecessor or new kernel. -/
namespace CommonModelReview
noncomputable section
open Classical
open OperationalJoin
open OperationalJoin.Typed

/-- This snapshot relation makes no effective-policy claim. Changing that
field cannot affect the relation; any such claim needs a separate premise. -/
theorem runtime_relation_does_not_bind_effective_policy {n}
    {c : Config (interface n)} {w : ComposedExecution.World}
    {s : State (interface n)} (h : RuntimeRepresents c w s)
    (policy : ComposedExecution.Policy) :
    RuntimeRepresents c { w with effectivePolicy := policy } s := by
  exact ⟨h.root_count, h.quorum, h.actual_plant, h.taint, h.roots⟩

/-- Runtime guards intentionally cannot read the effective global policy. -/
theorem changing_effective_policy_does_not_change_gate
    (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badOpen : Bool) (i : Nat)
    (policy : ComposedExecution.Policy) :
    ComposedExecution.gateOpen {w with effectivePolicy := policy} e requester badOpen i =
      ComposedExecution.gateOpen w e requester badOpen i := rfl

/-- Two envelopes can share nonce, action and path while carrying a distinct
complete successor. Full-command memory must retain this distinction. -/
def alteredSuccessor {n} (e : BoundedEnvelope n) : BoundedEnvelope n :=
  ⟨{e.val with successor := {e.val.successor with ruleVersion := e.val.successor.ruleVersion + 1}},
    e.property⟩

theorem altered_successor_same_nonce {n} (e : BoundedEnvelope n) :
    (alteredSuccessor e).val.nonce = e.val.nonce := rfl

theorem altered_successor_distinct {n} (e : BoundedEnvelope n) : alteredSuccessor e ≠ e := by
  intro eq
  have versions := congrArg (fun k : BoundedEnvelope n => k.val.successor.ruleVersion) eq
  simp only [alteredSuccessor] at versions
  omega

theorem tombstone_is_complete_envelope {n} (e : BoundedEnvelope n) :
    alteredSuccessor e ∉ memory [e.val] := by
  rw [mem_memory]
  simp only [List.mem_singleton]
  intro eq
  exact altered_successor_distinct e (Subtype.ext eq)

def path01 (e : ComposedExecution.Envelope) : BoundedEnvelope 4 :=
  ⟨{e with path := [0, 1]}, by
    change ([0, 1] : List Nat).Nodup ∧ ∀ i ∈ ([0, 1] : List Nat), i < 4
    decide⟩
def path10 (e : ComposedExecution.Envelope) : BoundedEnvelope 4 :=
  ⟨{e with path := [1, 0]}, by
    change ([1, 0] : List Nat).Nodup ∧ ∀ i ∈ ([1, 0] : List Nat), i < 4
    decide⟩

theorem path_set_equality_does_not_collapse_identity (e : ComposedExecution.Envelope) :
    path (path01 e) = path (path10 e) ∧ path01 e ≠ path10 e := by
  constructor
  · ext i
    simp [path, path01, path10, or_comm]
  · intro eq
    have p := congrArg (fun k : BoundedEnvelope 4 => k.val.path) eq
    have bad : ([0, 1] : List Nat) ≠ [1, 0] := by decide
    exact bad p

/-- Source specialization really erases time at each event. -/
theorem binary_event_erases_arbitrary_time {n} (e : InterlockHistory.Command n)
    (requester t u : Nat) :
    OriginalTranslation.lowerEvent (.land e requester t) =
      OriginalTranslation.lowerEvent (.land e requester u) := rfl

/-- Concrete root-memory representation exists for every runtime root. -/
theorem no_vacuous_root_representation {n} (r : ComposedExecution.Root) :
    ∃ z : RootState (interface n), RootRepresents r z :=
  ⟨rootView r, rootView_represents r⟩

#print axioms runtime_relation_does_not_bind_effective_policy
#print axioms changing_effective_policy_does_not_change_gate
#print axioms altered_successor_distinct
#print axioms tombstone_is_complete_envelope
#print axioms path_set_equality_does_not_collapse_identity
#print axioms binary_event_erases_arbitrary_time
#print axioms no_vacuous_root_representation
end
end CommonModelReview
