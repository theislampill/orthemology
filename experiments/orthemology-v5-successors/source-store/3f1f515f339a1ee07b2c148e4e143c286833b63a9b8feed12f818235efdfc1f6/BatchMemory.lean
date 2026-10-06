import BatchReadiness
import BatchProgress

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

theorem prepare_fresh (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (nonce : Nat) (fresh : FreshAbove w nonce) :
    FreshAbove (ComposedExecution.prepare w e requester true).1 nonce := by
  unfold ComposedExecution.prepare
  split
  · intro i bound good other member
    dsimp at bound good member
    split at member <;> first
      | exact fresh i bound good other member
      | (split at member <;> exact fresh i bound good other member)
  · exact fresh

theorem attempt_fresh (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badOpen : Bool) (nonce : Nat) (fresh : FreshAbove w nonce) :
    FreshAbove (attempt w e requester badOpen).1 nonce := by
  unfold attempt
  split <;> exact fresh

theorem cancel_fresh (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (nonce nextNonce : Nat) (fresh : FreshAbove w nonce)
    (monotone : nonce ≤ nextNonce) (current : e.nonce ≤ nextNonce) :
    FreshAbove (cancelWith w e requester e.path).1 nextNonce := by
  unfold cancelWith
  split
  · intro i bound good other member
    dsimp at bound good member
    split at member
    · change other ∈ e :: (w.roots i).cancelled at member
      rw [List.mem_cons] at member
      rcases member with same | old
      · simpa only [same] using current
      · exact Nat.le_trans (fresh i bound good other old) monotone
    · exact Nat.le_trans (fresh i bound good other member) monotone
  · intro i bound good other member
    exact Nat.le_trans (fresh i bound good other member) monotone

theorem serviceTrial_fresh (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (nonce nextNonce : Nat) (fresh : FreshAbove w nonce)
    (monotone : nonce ≤ nextNonce) (current : e.nonce ≤ nextNonce) :
    FreshAbove (serviceTrial w e requester).1 nextNonce := by
  cases prepared : (ComposedExecution.prepare w e requester true).2 with
  | false =>
      simp only [serviceTrial, prepared, Bool.false_eq_true, if_false]
      exact cancel_fresh _ e requester nonce nextNonce (prepare_fresh w e requester nonce fresh) monotone current
  | true =>
      simp only [serviceTrial, prepared, if_true]
      exact cancel_fresh _ e requester nonce nextNonce
        (attempt_fresh _ e requester false nonce (prepare_fresh w e requester nonce fresh)) monotone current

theorem batchBody_fresh (actor : Actor) (action : Action)
    (acc : ComposedExecution.World × List AttemptTrace) (path : List Nat)
    (fresh : FreshAbove acc.1 (actor.nonce + acc.2.length)) :
    FreshAbove (batchBody actor action acc path).1
      (actor.nonce + (batchBody actor action acc path).2.length) := by
  rw [batchBody_length]
  cases proposal : propose { actor with nonce := actor.nonce + acc.2.length } action path with
  | none =>
      simp only [batchBody, proposal]
      intro i bound good other member
      have old := fresh i bound good other member
      omega
  | some e =>
      have fields := proposal_fields _ _ _ e proposal
      rw [batchBody_of_proposal actor action acc path e proposal]
      exact serviceTrial_fresh acc.1 e actor.identity (actor.nonce + acc.2.length)
        (actor.nonce + (acc.2.length + 1)) fresh (by omega) (by simpa only [fields.2.2] using Nat.le_refl e.nonce)

theorem fold_fresh (actor : Actor) (action : Action) (paths : List (List Nat))
    (acc : ComposedExecution.World × List AttemptTrace)
    (fresh : FreshAbove acc.1 (actor.nonce + acc.2.length)) :
    FreshAbove (paths.foldl (batchBody actor action) acc).1
      (actor.nonce + (paths.foldl (batchBody actor action) acc).2.length) := by
  induction paths generalizing acc with
  | nil => exact fresh
  | cons path rest ih => exact ih _ (batchBody_fresh actor action acc path fresh)

theorem runBatch_fresh (w : ComposedExecution.World) (actor : Actor) (action : Action)
    (fresh : FreshAbove w actor.nonce) :
    FreshAbove (runBatch w actor action).1 (actor.nonce + 4) := by
  have result := fold_fresh actor action fourPaths (w, []) (by simpa using fresh)
  rw [← runBatch_eq_fold, runBatch_length] at result
  exact result

theorem certifyTransition_fresh (w : ComposedExecution.World) (acks : List Nat) (policy : Policy)
    (nonce : Nat) (fresh : FreshAbove w nonce) :
    FreshAbove (certifyTransition w acks policy).1 nonce := by
  unfold certifyTransition
  split
  · intro i bound good e member
    dsimp at bound good member
    split at member <;> exact fresh i bound good e member
  · exact fresh

theorem deliver_fresh (w : ComposedExecution.World) (certificate : ComposedExecution.Certificate)
    (nonce : Nat) (fresh : FreshAbove w nonce) :
    FreshAbove (ComposedExecution.deliver w certificate) nonce := by
  unfold ComposedExecution.deliver
  split
  · intro i bound good e member
    dsimp at bound good member
    split at member <;> exact fresh i bound good e member
  · exact fresh

#print axioms runBatch_fresh
#print axioms certifyTransition_fresh
#print axioms deliver_fresh
end
end OperationalJoin.Offset.Batch
