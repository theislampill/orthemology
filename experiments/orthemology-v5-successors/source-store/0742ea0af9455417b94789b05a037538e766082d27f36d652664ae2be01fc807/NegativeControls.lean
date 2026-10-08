import HistoryTrace
namespace InterlockHistory.Controls
open InterlockHistory

/-- Same target bytes/version/recipient throughout: only the control epoch and
    permission change. These are model fixtures, not extra protocol premises. -/
def source (e : Nat) : Descriptor :=
  ⟨e, 7, 4, 11, 3, (false, true), e == 0⟩

def cfg : Config 4 where
  budget := 1
  q := 3
  r := 3
  faulty := {0}
  budget_bound := by decide
  overlap := by decide
  budget_lt_roots := by decide
  repair_available := by decide
  revoke_available := by decide
  source := source
  source_epoch := by intro e; rfl

def command : Command 4 := ⟨0, 7, 4, 11, 3, (false, true), 5, {0, 1, 2}⟩
def initial : State 4 := Initial cfg (true, true)
def prepared : State 4 := prepare (prepare (prepare initial 0 command) 1 command) 2 command

theorem prepared_reachable : Reachable cfg prepared := by
  refine ⟨(true, true), [.prepare 0 command 11, .prepare 1 command 11,
    .prepare 2 command 11], ?_⟩
  apply Trace.cons (Step.prepare _ 0 command 11 (by decide) (by decide) (Or.inl (by decide)))
  apply Trace.cons (Step.prepare _ 1 command 11 (by decide) (by decide) ?_)
  · apply Trace.cons (Step.prepare _ 2 command 11 (by decide) (by decide) ?_)
    · exact Trace.nil _
    · right
      decide
  · right
    decide

def requested : State 4 := request prepared
def ack1 : State 4 := acknowledge cfg requested 1
def ack2 : State 4 := acknowledge cfg ack1 2
def ack3 : State 4 := acknowledge cfg ack2 3
def revoked : State 4 := complete ack3

theorem revocation_trace : Trace cfg prepared
    [.request, .acknowledge 1, .acknowledge 2, .acknowledge 3, .complete] revoked := by
  apply Trace.cons (Step.request _ rfl)
  apply Trace.cons (Step.acknowledge _ 1 rfl)
  apply Trace.cons (Step.acknowledge _ 2 rfl)
  apply Trace.cons (Step.acknowledge _ 3 rfl)
  apply Trace.cons (Step.complete _ rfl (by decide))
  exact Trace.nil _

theorem trace_append {n} {c : Config n} {s t u : State n}
    {xs ys : List (Event n)} (first : Trace c s xs t) (second : Trace c t ys u) :
    Trace c s (xs ++ ys) u := by
  induction first with
  | nil => exact second
  | cons step tail ih => exact .cons step (ih second)

theorem reachable_after {n} {c : Config n} {s t : State n} {events : List (Event n)}
    (reach : Reachable c s) (trace : Trace c s events t) : Reachable c t := by
  obtain ⟨table, priorEvents, before⟩ := reach
  exact ⟨table, priorEvents ++ events, trace_append before trace⟩

theorem revoked_reachable : Reachable cfg revoked :=
  reachable_after prepared_reachable revocation_trace

/-- A single duty deletion: retain local authorization, full-command commitment,
    requester check and cancellation, but remove durable epoch revocation. -/
abbrev NoRevocation (z : RootState 4) (k : Command 4) (requester : Nat) : Prop :=
  k ∈ z.commitments ∧ requester = k.recipient ∧ Authorized k z.descriptor ∧
  k ∉ z.cancelled

abbrev BrokenLands (s : State 4) (gate : RootState 4 → Command 4 → Nat → Prop)
    (k : Command 4) (requester : Nat) : Prop :=
  ValidPath cfg k ∧ ∀ i ∈ k.path, Good cfg i → gate (s.roots i) k requester

theorem dropped_revocation_admits_stale :
    ¬Lands cfg revoked command 11 ∧
    BrokenLands revoked NoRevocation command 11 ∧
    ¬Authorized command (cfg.source revoked.epoch) ∧
    (land cfg revoked command 11).damaged = true := by
  exact ⟨by decide, by decide, by decide, by decide⟩

/-- Source simulator's exact target-only deletion: retain the committed command
    and immutable target fields but omit the live control-authorization envelope.
    It deliberately drops more than epoch equality; retaining a correct revoked
    epoch guard by itself would still stop this permission-only counterexample. -/
abbrev TargetOnly (z : RootState 4) (k : Command 4) (_requester : Nat) : Prop :=
  k ∈ z.commitments ∧ k.targetId = z.descriptor.targetId ∧
  k.targetVersion = z.descriptor.targetVersion ∧ k.table = z.descriptor.table

def delivered : State 4 := deliver cfg (deliver cfg revoked 1 1) 2 1

theorem delivery_trace : Trace cfg revoked [.deliver 1 1, .deliver 2 1] delivered := by
  apply Trace.cons (Step.deliver _ 1 1 (by decide))
  apply Trace.cons (Step.deliver _ 2 1 (by decide))
  exact Trace.nil _

theorem permission_epoch_is_not_payload :
    (cfg.source 0).table = (cfg.source 1).table ∧
    (cfg.source 0).targetVersion = (cfg.source 1).targetVersion ∧
    ¬Lands cfg delivered command 11 ∧
    BrokenLands delivered TargetOnly command 11 ∧
    (land cfg delivered command 11).damaged = true := by
  exact ⟨by decide, by decide, by decide, by decide, by decide⟩

/-- Actual B+1 certificate, with one bad and one honest selected acknowledger. -/
def cancelled : State 4 := cancelAck cfg (cancelAck cfg prepared 0 command) 1 command

theorem cancellation_trace : Trace cfg prepared
    [.cancelAck 0 command 11, .cancelAck 1 command 11, .close command] cancelled := by
  apply Trace.cons (Step.cancelAck _ 0 command 11 (by decide) (Or.inl (by decide)))
  apply Trace.cons (Step.cancelAck _ 1 command 11 (by decide) (Or.inr rfl))
  apply Trace.cons (Step.close _ command (by decide))
  exact Trace.nil _

abbrev NoCancellation (z : RootState 4) (k : Command 4) (requester : Nat) : Prop :=
  k ∈ z.commitments ∧ requester = k.recipient ∧ Authorized k z.descriptor ∧
  k.epoch ∉ z.revoked

theorem dropped_tombstone_admits_after_close :
    Cancelled cfg cancelled command ∧
    ¬Lands cfg cancelled command 11 ∧
    BrokenLands cancelled NoCancellation command 11 ∧
    ¬Envelope (cancelled.roots 1) command 11 ∧
    (land cfg cancelled command 11).table = command.table := by
  exact ⟨by decide, by decide, by decide, by decide, by decide⟩

/-- c=B fails even when every actual good gate keeps its full original contract. -/
def falselyClosed : State 4 := cancelAck cfg prepared 0 command

theorem too_small_cancellation_certificate :
    (falselyClosed.cancelAcks command).card = cfg.budget ∧
    ¬Cancelled cfg falselyClosed command ∧ Lands cfg falselyClosed command 11 := by
  decide

/-- Removing mediation permits the single already-charged root 0 to bypass the
    honest vetoes. No extra uncharged attacker or safety classifier is added. -/
def bypass (s : State 4) : State 4 := { s with damaged := true }

theorem dropped_mediation :
    (0 : Fin 4) ∈ cfg.faulty ∧ ¬Lands cfg revoked command 11 ∧
    revoked.damaged = false ∧ (bypass revoked).damaged = true := by
  decide

/-- Correct physical binding checks the actual tuple, never an approved label. -/
def substituted : Command 4 := { command with table := (true, false) }

theorem dropped_same_command_binding :
    Lands cfg prepared command 11 ∧ ¬Lands cfg prepared substituted 11 ∧
    (land cfg prepared substituted 11).damaged = true := by
  exact ⟨by decide, by decide, by decide⟩

/-- A late preparation of exactly the same command cannot reopen its tombstone. -/
theorem cancelled_replay_stays_blocked :
    ¬Permits ((prepare cancelled 1 command).roots 1) command 11 := by
  decide

#print axioms prepared_reachable
#print axioms revoked_reachable
#print axioms dropped_revocation_admits_stale
#print axioms permission_epoch_is_not_payload
#print axioms dropped_tombstone_admits_after_close
#print axioms too_small_cancellation_certificate
#print axioms dropped_mediation
#print axioms dropped_same_command_binding
end InterlockHistory.Controls
