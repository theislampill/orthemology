import NegativeControls
open InterlockHistory
namespace InterlockHistory.IndependentReview

/-- The compressed delivery guard is backed by a stored, durable certificate
    in every reachable state, rather than an assumption inside a good gate. -/
theorem actual_certificate_for_delivery {n} {c : Config n} {s : State n}
    (reach : Reachable c s) (e : Nat) (allowed : 0 < e ∧ e ≤ s.epoch) :
    (s.certificates (e - 1)).card = c.r ∧
    ∀ i ∈ s.certificates (e - 1), Good c i → e - 1 ∈ (s.roots i).revoked := by
  exact (reachable_consistent reach).past_certificates (e - 1) (by omega)

/-- Strengthen the endpoint formulation into exclusion of that landing event
    at every position of an arbitrary allowed continuation. -/
theorem no_cancelled_land_event {n} {c : Config n} {s t : State n}
    {events : List (Event n)} (h : Consistent c s)
    (run : Trace c s events t) (k : Command n) (closed : Cancelled c s k) :
    ∀ requester, Event.land k requester ∉ events := by
  induction run with
  | nil => simp
  | @cons s u t a rest step tail ih =>
    intro requester member
    rcases List.mem_cons.mp member with first | later
    · subst a
      cases step with
      | land _ _ admitted => exact cancelled_cannot_land h k requester closed admitted
    · exact ih (consistent_step h step)
        (by
          have := Finset.card_le_card (step_cancelAcks step k)
          unfold Cancelled at *
          omega) requester later

/-- No hidden positive-q premise is missing from Config, including B=0. -/
theorem positive_thresholds {n} (c : Config n) : 0 < c.q ∧ 0 < c.r := by
  have := c.overlap
  have := c.repair_available
  have := c.revoke_available
  omega

namespace Pending
open Controls
/-- Request itself is deliberately not effective revocation. The model permits
    a live current landing before root closure, so external consent needs the
    separately declared reservation premise. -/
example : requested.pending = true ∧ requested.epoch = 0 ∧
    Lands cfg requested command 11 := by decide

example : Step cfg requested (.land command 11) (land cfg requested command 11) := by
  exact .land _ _ _ (by decide)

/-- A good acknowledgement closes before completion without learning the new
    descriptor. This prevents the local/global epoch distinction from collapsing. -/
example : ack1.pending = true ∧ ack1.epoch = 0 ∧
    (ack1.roots 1).descriptor.epoch = 0 ∧ 0 ∈ (ack1.roots 1).revoked ∧
    ¬Permits (ack1.roots 1) command 11 := by decide

/-- Authentication is modelled as the requester input; a copied tuple without
    its bound requester does not gain admission. -/
example : ¬Lands cfg prepared command 12 := by decide

/-- The B-only cancellation countermodel really is reachable by an allowed
    prefix, although its closure is not accepted by the original threshold. -/
example : Reachable cfg falselyClosed := by
  apply reachable_after prepared_reachable
  exact .cons (.cancelAck _ 0 command 11 (by decide) (Or.inl (by decide))) (.nil _)
end Pending

namespace AfterClose
open Controls

def clearedBad : RootState 4 := ⟨source 0, ∅, ∅, ∅⟩
def erased : State 4 := setRoot cancelled 0 clearedBad
def repreparedBad : State 4 := prepare erased 0 command

theorem erase_and_reprepare : Trace cfg cancelled
    [.corrupt 0 clearedBad, .prepare 0 command 11] repreparedBad := by
  apply Trace.cons (Step.corrupt _ 0 clearedBad (by decide))
  apply Trace.cons (Step.prepare _ 0 command 11 (by decide) (by decide) (Or.inl (by decide)))
  exact Trace.nil _

example : Reachable cfg repreparedBad :=
  reachable_after (reachable_after prepared_reachable cancellation_trace) erase_and_reprepare

example : command ∉ (repreparedBad.roots 0).cancelled ∧
    command ∈ (repreparedBad.roots 0).commitments ∧
    command ∈ (repreparedBad.roots 1).cancelled ∧
    ¬Lands cfg repreparedBad command 11 := by decide

example (t : State 4) : ¬Step cfg cancelled (.prepare 1 command 11) t := by
  intro step
  cases step with
  | prepare =>
    exact (by decide : ¬((1 : Fin 4) ∈ cfg.faulty ∨
      Envelope (cancelled.roots 1) command 11)) (by assumption)

example (t : State 4) : ¬Step cfg prepared (.cancelAck 1 command 12) t := by
  intro step
  cases step with
  | cancelAck =>
    exact (by decide : ¬((1 : Fin 4) ∈ cfg.faulty ∨ (12 : Nat) = command.recipient))
      (by assumption)

/-- An unrelated fresh nonce remains able to repair after prior cancellation. -/
def fresh : Command 4 := { command with nonce := 6 }
def freshPrepared : State 4 := prepare (prepare (prepare cancelled 0 fresh) 1 fresh) 2 fresh

example : Trace cfg cancelled
    [.prepare 0 fresh 11, .prepare 1 fresh 11, .prepare 2 fresh 11,
      .land fresh 11] (land cfg freshPrepared fresh 11) := by
  apply Trace.cons (Step.prepare _ 0 fresh 11 (by decide) (by decide) (Or.inl (by decide)))
  apply Trace.cons (Step.prepare _ 1 fresh 11 (by decide) (by decide) (Or.inr (by decide)))
  apply Trace.cons (Step.prepare _ 2 fresh 11 (by decide) (by decide) (Or.inr (by decide)))
  apply Trace.cons (Step.land _ fresh 11 (by decide))
  exact Trace.nil _

example : Restored cfg (land cfg freshPrepared fresh 11) := by
  unfold Restored
  decide
end AfterClose

/-- Internal authentication/mediation safety cannot conjure external consent. -/
example : ¬Reservation Controls.cfg (fun _ _ _ => False) := by
  intro reserved
  exact reserved Controls.prepared Controls.command 11 Controls.prepared_reachable
    (by decide) rfl (by decide)

/-- Arbitrarily long safe non-repair continuations remain admitted. Thus the
    reviewed finite-history theorem alone cannot entail eventual repair. -/
theorem arbitrary_hold_trace {n} (c : Config n) (s : State n) (length : Nat) :
    Trace c s (List.replicate length Event.hold) s := by
  induction length with
  | zero => exact .nil _
  | succ length ih => exact .cons (.hold _) ih

example : ¬Restored Controls.cfg Controls.initial := by
  unfold Restored
  decide

namespace ZeroBudget

def source (e : Nat) : Descriptor := ⟨e, 0, e, 0, 0, (false, true), true⟩
def cfg : Config 1 where
  budget := 0
  q := 1
  r := 1
  faulty := ∅
  budget_bound := by decide
  overlap := by decide
  budget_lt_roots := by decide
  repair_available := by decide
  revoke_available := by decide
  source := source
  source_epoch := by intro e; rfl

def command : Command 1 := ⟨0, 0, 0, 0, 0, (false, true), 0, {0}⟩
def initial : State 1 := Initial cfg (true, true)
def prepared : State 1 := prepare initial 0 command
def repaired : State 1 := land cfg prepared command 0

theorem repair_trace : Trace cfg initial [.prepare 0 command 0, .land command 0] repaired := by
  apply Trace.cons (Step.prepare _ 0 command 0 (by decide) (by decide) (Or.inr (by decide)))
  apply Trace.cons (Step.land _ command 0 (by decide))
  exact Trace.nil _

example : Restored cfg repaired := by unfold Restored; decide
end ZeroBudget

#print axioms actual_certificate_for_delivery
#print axioms no_cancelled_land_event
#print axioms positive_thresholds
#print axioms arbitrary_hold_trace
#print axioms AfterClose.erase_and_reprepare
#print axioms ZeroBudget.repair_trace
end InterlockHistory.IndependentReview
