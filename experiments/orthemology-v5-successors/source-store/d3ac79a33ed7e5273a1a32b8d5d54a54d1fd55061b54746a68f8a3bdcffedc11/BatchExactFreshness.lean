import BatchProgress
import BatchFrames

namespace OperationalJoin.Offset.Batch
noncomputable section
open Classical
open ComposedExecution

/-- Exactly the full envelopes a fixed successful proposal will generate for
this path suffix. This is a mathematical prediction from actor-owned inputs;
it does not read world state, policy sources, or fault information. -/
def trialEnvelopes (action : Action) (successor : Plant) : Nat → List (List Nat) → List ComposedExecution.Envelope
  | _, [] => []
  | nonce, path :: rest =>
      ⟨action, successor, nonce + 1, path⟩ :: trialEnvelopes action successor (nonce + 1) rest

def FreshTrials (w : ComposedExecution.World) (envelopes : List ComposedExecution.Envelope) : Prop :=
  ∀ i, i < w.n → w.tainted i = false → ∀ e ∈ envelopes, e ∉ (w.roots i).cancelled

/-- Identical live-admission/root-policy obligations to the conservative result,
with absence of just the predicted full envelopes replacing global high-water. -/
def ExactReady (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (paths : List (List Nat)) : Prop :=
  requester = action.actor ∧
  localStep w.plant w.effectivePolicy w.now action = some successor ∧
  (∀ i, i < w.n → w.tainted i = false →
    (w.roots i).policy = w.effectivePolicy ∧ action.epoch ∉ (w.roots i).revoked) ∧
  FreshTrials w (trialEnvelopes action successor nonce paths)

theorem trialEnvelopes_nonce_gt (action : Action) (successor : Plant)
    (nonce : Nat) (paths : List (List Nat)) (e : ComposedExecution.Envelope)
    (member : e ∈ trialEnvelopes action successor nonce paths) : nonce < e.nonce := by
  induction paths generalizing nonce with
  | nil => cases member
  | cons path rest ih =>
      rw [trialEnvelopes, List.mem_cons] at member
      rcases member with same | tail
      · subst e
        simp
      · have later := ih (nonce + 1) tail
        omega

theorem freshAbove_implies_freshTrials (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (nonce : Nat) (paths : List (List Nat)) (fresh : FreshAbove w nonce) :
    FreshTrials w (trialEnvelopes action successor nonce paths) := by
  intro i bound good e member cancelled
  have old := fresh i bound good e cancelled
  have newer := trialEnvelopes_nonce_gt action successor nonce paths e member
  omega

theorem ready_implies_exactReady (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (paths : List (List Nat))
    (ready : ReadyFor w action successor requester nonce) :
    ExactReady w action successor requester nonce paths :=
  ⟨ready.1, ready.2.1, ready.2.2.1,
    freshAbove_implies_freshTrials w action successor nonce paths ready.2.2.2⟩

theorem exactReady_head_eligible (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (path : List Nat) (rest : List (List Nat))
    (ready : ExactReady w action successor requester nonce (path :: rest))
    (i : Nat) (bound : i < w.n) (good : w.tainted i = false) :
    Eligible w.plant w.now (w.roots i) ⟨action, successor, nonce + 1, path⟩ requester := by
  obtain ⟨owner, admission, roots, fresh⟩ := ready
  obtain ⟨policy, unrevoked⟩ := roots i bound good
  exact ⟨owner, unrevoked, fresh i bound good _ (by simp [trialEnvelopes]),
    by simpa only [policy] using admission⟩

theorem exactReady_head_lands (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (path : List Nat) (rest : List (List Nat))
    (ready : ExactReady w action successor requester nonce (path :: rest))
    (valid : validPath w ⟨action, successor, nonce + 1, path⟩ = true)
    (intact : ∀ i ∈ path, w.tainted i = false) :
    (serviceTrial w ⟨action, successor, nonce + 1, path⟩ requester).2.landed = true := by
  let e : ComposedExecution.Envelope := ⟨action, successor, nonce + 1, path⟩
  have bounds : ∀ i ∈ path, i < w.n := (of_decide_eq_true valid).2.2
  have eligible : ∀ i ∈ e.path, Eligible w.plant w.now (w.roots i) e requester := by
    intro i member
    exact exactReady_head_eligible w action successor requester nonce path rest ready i
      (bounds i member) (intact i member)
  have prepares := prepare_succeeds w e requester valid (by intro i member _; exact eligible i member)
  have lands := intact_prepared_attempt w e requester valid intact eligible
  change (serviceTrial w e requester).2.landed = true
  simpa only [serviceTrial, prepares, if_true] using lands

theorem prepare_exactReady (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (paths : List (List Nat))
    (ready : ExactReady w action successor requester nonce paths) (e : ComposedExecution.Envelope) :
    ExactReady (ComposedExecution.prepare w e requester true).1 action successor requester nonce paths := by
  unfold ComposedExecution.prepare
  split
  · obtain ⟨owner, admission, roots, fresh⟩ := ready
    refine ⟨owner, admission, ?_, ?_⟩
    · intro i bound good
      dsimp at bound good ⊢
      split <;> first | exact roots i bound good | (split <;> exact roots i bound good)
    · intro i bound good other future cancelled
      dsimp at bound good cancelled
      split at cancelled <;> first
        | exact fresh i bound good other future cancelled
        | (split at cancelled <;> exact fresh i bound good other future cancelled)
  · exact ready

theorem cancel_exactReady_tail (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (path : List Nat) (rest : List (List Nat))
    (ready : ExactReady w action successor requester nonce (path :: rest)) :
    ExactReady (cancelWith w ⟨action, successor, nonce + 1, path⟩ requester path).1
      action successor requester (nonce + 1) rest := by
  let e : ComposedExecution.Envelope := ⟨action, successor, nonce + 1, path⟩
  have tailFresh : FreshTrials w (trialEnvelopes action successor (nonce + 1) rest) := by
    intro i bound good other member
    exact ready.2.2.2 i bound good other (by simp [trialEnvelopes, member])
  have different : ∀ other ∈ trialEnvelopes action successor (nonce + 1) rest, other ≠ e := by
    intro other member same
    have larger := trialEnvelopes_nonce_gt action successor (nonce + 1) rest other member
    rw [same] at larger
    exact Nat.lt_irrefl _ larger
  unfold cancelWith
  split
  · refine ⟨ready.1, ready.2.1, ?_, ?_⟩
    · intro i bound good
      dsimp at bound good ⊢
      split <;> exact ready.2.2.1 i bound good
    · intro i bound good other future cancelled
      dsimp at bound good cancelled
      split at cancelled
      · change other ∈ e :: (w.roots i).cancelled at cancelled
        rw [List.mem_cons] at cancelled
        rcases cancelled with same | old
        · exact different other future same
        · exact tailFresh i bound good other future old
      · exact tailFresh i bound good other future cancelled
  · exact ⟨ready.1, ready.2.1, ready.2.2.1, tailFresh⟩

theorem rejected_trial_exactReady_tail (w : ComposedExecution.World) (action : Action) (successor : Plant)
    (requester : String) (nonce : Nat) (path : List Nat) (rest : List (List Nat))
    (ready : ExactReady w action successor requester nonce (path :: rest))
    (rejected : (serviceTrial w ⟨action, successor, nonce + 1, path⟩ requester).2.landed = false) :
    ExactReady (serviceTrial w ⟨action, successor, nonce + 1, path⟩ requester).1
      action successor requester (nonce + 1) rest := by
  let e : ComposedExecution.Envelope := ⟨action, successor, nonce + 1, path⟩
  change (serviceTrial w e requester).2.landed = false at rejected
  change ExactReady (serviceTrial w e requester).1 action successor requester (nonce + 1) rest
  have afterPrepare := prepare_exactReady w action successor requester nonce (path :: rest) ready e
  cases prepared : (ComposedExecution.prepare w e requester true).2 with
  | false =>
      simp only [serviceTrial, prepared, Bool.false_eq_true, if_false]
      exact cancel_exactReady_tail _ action successor requester nonce path rest afterPrepare
  | true =>
      have rejectedAttempt : (attempt (ComposedExecution.prepare w e requester true).1 e requester false).2 = false := by
        simpa only [serviceTrial, prepared, if_true] using rejected
      simp only [serviceTrial, prepared, if_true,
        rejected_attempt_full_identity _ _ _ _ rejectedAttempt]
      exact cancel_exactReady_tail _ action successor requester nonce path rest afterPrepare

#print axioms freshAbove_implies_freshTrials
#print axioms exactReady_head_lands
#print axioms rejected_trial_exactReady_tail
end
end OperationalJoin.Offset.Batch
