import BatchTrial

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

/-- A conservative, explicit high-water condition on the existing complete
cancellation memory. It is sufficient for fresh trial envelopes; incrementing
an actor nonce alone does not establish it. -/
def FreshAbove (w : ComposedExecution.World) (nonce : Nat) : Prop :=
  ∀ i, i < w.n → w.tainted i = false →
    ∀ e ∈ (w.roots i).cancelled, e.nonce ≤ nonce

/-- Source-level stable admission obligations. The actor's own proposal
obligation is separate; this predicate supplies no observation oracle. -/
def ReadyFor (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) : Prop :=
  requester = action.actor ∧
  localStep w.plant w.effectivePolicy w.now action = some successor ∧
  (∀ i, i < w.n → w.tainted i = false →
    (w.roots i).policy = w.effectivePolicy ∧ action.epoch ∉ (w.roots i).revoked) ∧
  FreshAbove w nonce

theorem ready_eligible (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (ready : ReadyFor w action successor requester nonce)
    (e : ComposedExecution.Envelope) (sameAction : e.action = action)
    (sameSuccessor : e.successor = successor) (fresh : nonce < e.nonce)
    (i : Nat) (bound : i < w.n) (good : w.tainted i = false) :
    Eligible w.plant w.now (w.roots i) e requester := by
  obtain ⟨owner, admission, roots, memory⟩ := ready
  obtain ⟨policy, unrevoked⟩ := roots i bound good
  refine ⟨by simpa only [sameAction] using owner,
    by simpa only [sameAction] using unrevoked, ?_, ?_⟩
  · intro cancelled
    have old := memory i bound good e cancelled
    omega
  · simpa only [sameAction, sameSuccessor, policy] using admission

theorem prepare_eligible_preserved (w : ComposedExecution.World) (e other : ComposedExecution.Envelope)
    (requester : String) (badSign : Bool) (i : Nat) :
    Eligible (ComposedExecution.prepare w e requester badSign).1.plant
      (ComposedExecution.prepare w e requester badSign).1.now
      ((ComposedExecution.prepare w e requester badSign).1.roots i) other requester ↔
      Eligible w.plant w.now (w.roots i) other requester := by
  unfold ComposedExecution.prepare
  split
  · dsimp
    split <;> split <;> rfl
  · rfl

theorem prepare_succeeds (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (valid : validPath w e = true)
    (eligible : ∀ i ∈ e.path, w.tainted i = false → Eligible w.plant w.now (w.roots i) e requester) :
    (ComposedExecution.prepare w e requester true).2 = true := by
  unfold ComposedExecution.prepare
  rw [if_pos valid]
  apply List.all_eq_true.mpr
  intro i member
  cases bad : w.tainted i with
  | true => simp [bad]
  | false => simp only [bad, Bool.false_eq_true, if_false]; exact decide_eq_true (eligible i member bad)

theorem prepare_commits_good_selected (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (valid : validPath w e = true)
    (i : Nat) (member : i ∈ e.path) (good : w.tainted i = false)
    (eligible : Eligible w.plant w.now (w.roots i) e requester) :
    e ∈ ((ComposedExecution.prepare w e requester true).1.roots i).commitments := by
  unfold ComposedExecution.prepare
  rw [if_pos valid]
  have contains : e.path.contains i = true := by simpa using member
  simp [contains, good, eligible, member]

theorem intact_prepared_attempt (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (valid : validPath w e = true)
    (intact : ∀ i ∈ e.path, w.tainted i = false)
    (eligible : ∀ i ∈ e.path, Eligible w.plant w.now (w.roots i) e requester) :
    (attempt (ComposedExecution.prepare w e requester true).1 e requester false).2 = true := by
  unfold attempt
  rw [if_pos]
  apply Bool.and_eq_true_iff.mpr
  constructor
  · simpa only [validPath, (prepare_static w e requester true).1,
      (prepare_static w e requester true).2.1] using valid
  · apply List.all_eq_true.mpr
    intro i member
    have good : (ComposedExecution.prepare w e requester true).1.tainted i = false := by
      rw [(prepare_static w e requester true).2.2.2.2.2]
      exact intact i member
    simp only [gateOpen, good, Bool.false_eq_true, if_false, rootPermits]
    exact decide_eq_true ⟨prepare_commits_good_selected w e requester valid i member
      (intact i member) (eligible i member),
      (prepare_eligible_preserved w e e requester true i).mpr (eligible i member)⟩

theorem ready_intact_trial_lands (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (ready : ReadyFor w action successor requester nonce)
    (e : ComposedExecution.Envelope) (sameAction : e.action = action)
    (sameSuccessor : e.successor = successor) (fresh : nonce < e.nonce)
    (valid : validPath w e = true) (intact : ∀ i ∈ e.path, w.tainted i = false) :
    (serviceTrial w e requester).2.landed = true := by
  have pathBounds : ∀ i ∈ e.path, i < w.n := (of_decide_eq_true valid).2.2
  have eligible : ∀ i ∈ e.path, Eligible w.plant w.now (w.roots i) e requester := by
    intro i member
    exact ready_eligible w action successor requester nonce ready e sameAction sameSuccessor fresh
      i (pathBounds i member) (intact i member)
  have prepares := prepare_succeeds w e requester valid (by intro i member _; exact eligible i member)
  have lands := intact_prepared_attempt w e requester valid intact eligible
  simpa only [serviceTrial, prepares, if_true] using lands

/-- Preparation changes commitments only; it cannot revoke a ready action or
consume a future nonce in cancellation memory. -/
theorem prepare_ready (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (ready : ReadyFor w action successor requester nonce)
    (e : ComposedExecution.Envelope) :
    ReadyFor (ComposedExecution.prepare w e requester true).1 action successor requester nonce := by
  unfold ComposedExecution.prepare
  split
  · obtain ⟨owner, admission, roots, fresh⟩ := ready
    refine ⟨owner, admission, ?_, ?_⟩
    · intro i bound good
      dsimp at bound good ⊢
      split <;> first | exact roots i bound good | (split <;> exact roots i bound good)
    · intro i bound good other member
      dsimp at bound good member
      split at member <;> first | exact fresh i bound good other member | (split at member <;> exact fresh i bound good other member)
  · exact ready

/-- Cleanup can consume this trial's nonce. All larger preexisting fresh
nonces remain fresh. This is the exact full-envelope cancellation operation. -/
theorem cancel_ready (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (ready : ReadyFor w action successor requester nonce)
    (e : ComposedExecution.Envelope) (nextNonce : Nat)
    (monotone : nonce ≤ nextNonce) (current : e.nonce ≤ nextNonce) :
    ReadyFor (cancelWith w e requester e.path).1 action successor requester nextNonce := by
  unfold cancelWith
  split
  · obtain ⟨owner, admission, roots, fresh⟩ := ready
    refine ⟨owner, admission, ?_, ?_⟩
    · intro i bound good
      dsimp at bound good ⊢
      split <;> first | exact roots i bound good | (split <;> exact roots i bound good)
    · intro i bound good other member
      dsimp at bound good member
      split at member
      · change other ∈ e :: (w.roots i).cancelled at member
        rw [List.mem_cons] at member
        rcases member with same | old
        · simpa only [same] using current
        · exact Nat.le_trans (fresh i bound good other old) monotone
      · exact Nat.le_trans (fresh i bound good other member) monotone
  · obtain ⟨owner, admission, roots, fresh⟩ := ready
    refine ⟨owner, admission, roots, ?_⟩
    intro i bound good other member
    exact Nat.le_trans (fresh i bound good other member) monotone

theorem rejected_serviceTrial_ready (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (ready : ReadyFor w action successor requester nonce)
    (e : ComposedExecution.Envelope) (rejected : (serviceTrial w e requester).2.landed = false)
    (nextNonce : Nat) (monotone : nonce ≤ nextNonce) (current : e.nonce ≤ nextNonce) :
    ReadyFor (serviceTrial w e requester).1 action successor requester nextNonce := by
  cases prepared : (ComposedExecution.prepare w e requester true).2 with
  | false =>
      simp only [serviceTrial, prepared, Bool.false_eq_true, if_false]
      exact cancel_ready _ action successor requester nonce
        (prepare_ready w action successor requester nonce ready e) e nextNonce monotone current
  | true =>
      have rejectedAttempt : (attempt (ComposedExecution.prepare w e requester true).1 e requester false).2 = false := by
        simpa only [serviceTrial, prepared, if_true] using rejected
      simp only [serviceTrial, prepared, if_true,
        rejected_attempt_full_identity _ _ _ _ rejectedAttempt]
      exact cancel_ready _ action successor requester nonce
        (prepare_ready w action successor requester nonce ready e) e nextNonce monotone current

#print axioms ready_intact_trial_lands
#print axioms rejected_serviceTrial_ready
end
end OperationalJoin.Offset.Batch
