import TypedHistoryProperties
import JoinOperations

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope path path_card mem_path memory mem_memory)

/-- Only the proof-side control index is offset. Every stored Policy, Grant,
Action and Envelope retains its original raw epoch consumed by localStep. -/
def interface (base n : Nat) : Interface n where
  Policy := ComposedExecution.Policy
  Command := BoundedEnvelope n
  Plant := ComposedExecution.Plant
  Requester := String
  policyEpoch := fun p => p.epoch - base
  commandEpoch := fun e => e.val.action.epoch - base
  commandPath := path
  recipient := fun e => e.val.action.actor
  admits := fun p time policy e requester =>
    requester = e.val.action.actor ∧ localStep p policy time e.val.action = some e.val.successor
  effect := fun _ e => e.val.successor
  admitted_epoch := by
    intro p time policy e requester h
    exact congrArg (fun epoch => epoch - base)
      (local_action_epoch p policy time e.val.action e.val.successor h.2)
  admitted_requester := by intro p time policy e requester h; exact h.1

/-- The source stream begins at base; it does not certify any earlier lifecycle. -/
structure Authority (base n : Nat) where
  source : Nat → ComposedExecution.Policy
  raw_epoch : ∀ index, (source index).epoch = base + index
  budget : Nat
  q : Nat
  r : Nat
  faulty : Finset (Fin n)
  budget_bound : faulty.card ≤ budget
  overlap : n + budget < q + r
  budget_lt_roots : budget < n
  repair_available : q + budget ≤ n
  revoke_available : r + budget ≤ n

def Authority.config {base n} (a : Authority base n) : Config (interface base n) where
  source := a.source
  source_epoch := by intro index; simp [interface, a.raw_epoch]
  budget := a.budget
  q := a.q
  r := a.r
  faulty := a.faulty
  budget_bound := a.budget_bound
  overlap := a.overlap
  budget_lt_roots := a.budget_lt_roots
  repair_available := a.repair_available
  revoke_available := a.revoke_available

/-- Proof-side index e is represented by the actual raw tombstone base+e.
The ordered complete command is otherwise represented without alteration. -/
def RootRepresents {base n} (r : ComposedExecution.Root)
    (z : RootState (interface base n)) : Prop :=
  z.descriptor = r.policy ∧
  (∀ index, index ∈ z.revoked ↔ base + index ∈ r.revoked) ∧
  (∀ e : BoundedEnvelope n, e ∈ z.commitments ↔ e.val ∈ r.commitments) ∧
  (∀ e : BoundedEnvelope n, e ∈ z.cancelled ↔ e.val ∈ r.cancelled)

/-- Low raw epochs remain in the command universe. An honest stored policy at
or above the boundary rejects them directly through unchanged source admission. -/
theorem low_raw_epoch_rejected {base n} (p : ComposedExecution.Plant) (time : Nat)
    (policy : ComposedExecution.Policy) (e : BoundedEnvelope n)
    (policyAbove : base ≤ policy.epoch) (old : e.val.action.epoch < base) :
    localStep p policy time e.val.action ≠ some e.val.successor := by
  intro accepted
  have epoch := local_action_epoch p policy time e.val.action e.val.successor accepted
  omega

theorem root_gate_iff {base n} (p : ComposedExecution.Plant) (time : Nat)
    (r : ComposedExecution.Root) (z : RootState (interface base n))
    (rep : RootRepresents r z) (policyAbove : base ≤ r.policy.epoch)
    (e : BoundedEnvelope n) (requester : String) :
    Permits p time z e requester ↔ rootPermits p time r e.val requester = true := by
  obtain ⟨policy, revoked, committed, cancelled⟩ := rep
  by_cases above : base ≤ e.val.action.epoch
  · have raw : base + (e.val.action.epoch - base) = e.val.action.epoch := by omega
    simp only [Permits, Envelope, interface]
    rw [committed, policy, revoked, raw, cancelled]
    simp [rootPermits, Eligible, and_assoc, and_left_comm, and_comm]
  · have old : e.val.action.epoch < base := by omega
    have rejected := low_raw_epoch_rejected p time r.policy e policyAbove old
    simp [Permits, Envelope, interface, policy, rootPermits, Eligible, rejected]

/-- Low raw commands are rejected by at least one good live gate even when
all faulty runtime gates open. No command is deleted to obtain this result. -/
theorem low_raw_attempt_rejected (w : ComposedExecution.World) (base : Nat)
    (e : ComposedExecution.Envelope) (requester : String) (badOpen : Bool)
    (budget : ChargedInterlock.card w.n w.tainted ≤ w.budget)
    (large : w.budget < ChargedInterlock.card w.n (fun i => decide (i ∈ e.path)))
    (policies : ∀ i, i < w.n → w.tainted i = false → base ≤ (w.roots i).policy.epoch)
    (old : e.action.epoch < base) : (attempt w e requester badOpen).2 ≠ true := by
  intro applied
  obtain ⟨i, hi, good, accepted⟩ := live_landing_refines_imported_step w e requester badOpen
    budget large (attempt_applied_implies_lands w e requester badOpen applied)
  have epoch := local_action_epoch _ _ _ _ _ accepted
  have lower := policies i hi good
  omega

theorem reachable_policy_above {base n} (a : Authority base n)
    {s : State (interface base n)} (reachable : Reachable a.config s)
    (i : Fin n) (good : Good a.config i) : base ≤ (s.roots i).descriptor.epoch := by
  have authentic := (reachable_consistent reachable).local_authentic i good
  rw [authentic]
  change base ≤ (a.source _).epoch
  rw [a.raw_epoch]
  omega

theorem finite_history_raw_current {base n} (a : Authority base n)
    {s : State (interface base n)} (reachable : Reachable a.config s)
    (time : Nat) (e : BoundedEnvelope n) (requester : String)
    (admitted : Lands a.config s time e requester) :
    e.val.action.epoch = base + s.epoch ∧
      localStep s.plant (a.source s.epoch) time e.val.action = some e.val.successor := by
  have auth := (admitted_current_authorized (reachable_consistent reachable) time e requester admitted).2.2
  have epoch := local_action_epoch _ _ _ _ _ auth.2
  exact ⟨by simpa [Authority.config, a.raw_epoch] using epoch, auth.2⟩

#print axioms low_raw_epoch_rejected
#print axioms root_gate_iff
#print axioms low_raw_attempt_rejected
#print axioms finite_history_raw_current
end
end OperationalJoin.Offset
