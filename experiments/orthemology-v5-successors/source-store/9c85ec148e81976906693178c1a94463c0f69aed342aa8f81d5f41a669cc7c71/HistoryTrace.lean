import HistorySafety
namespace InterlockHistory

/-- Authorization at the *pre-state* of each actual landing in a finite trace. -/
def WriteSafe {n} (c : Config n) (s : State n) (a : Event n) : Prop :=
  ∀ k requester, a = .land k requester →
    requester = k.recipient ∧ k.epoch = s.epoch ∧ Authorized k (c.source s.epoch)

inductive AuthorizedTrace {n} (c : Config n) : State n → List (Event n) → State n → Prop where
  | nil (s) : AuthorizedTrace c s [] s
  | cons {s t u a as} : Step c s a t → WriteSafe c s a →
      AuthorizedTrace c t as u → AuthorizedTrace c s (a :: as) u

theorem step_writeSafe {n} {c : Config n} {s t : State n} {a : Event n}
    (h : Consistent c s) (step : Step c s a t) : WriteSafe c s a := by
  intro k requester eq
  subst a
  cases step with
  | land _ _ admitted => exact admitted_current_authorized h k requester admitted

theorem trace_writes_authorized {n} {c : Config n} {s t : State n}
    {as : List (Event n)} (h : Consistent c s) (trace : Trace c s as t) :
    AuthorizedTrace c s as t := by
  induction trace with
  | nil => exact .nil _
  | cons step _ ih => exact .cons step (step_writeSafe h step) (ih (consistent_step h step))

theorem step_safe {n} {c : Config n} {s t : State n} {a : Event n}
    (h : Consistent c s) (safe : s.damaged = false) (step : Step c s a t) :
    t.damaged = false := by
  cases step with
  | land k requester admitted =>
    obtain ⟨requesterEq, _, auth⟩ := admitted_current_authorized h k requester admitted
    simp [land, safe, requesterEq, auth]
  | _ =>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck,
      setRoot] <;> split_ifs <;> simp_all

theorem trace_safe {n} {c : Config n} {s t : State n} {as : List (Event n)}
    (h : Consistent c s) (safe : s.damaged = false) (trace : Trace c s as t) :
    t.damaged = false := by
  induction trace with
  | nil => exact safe
  | cons step _ ih => exact ih (consistent_step h step) (step_safe h safe step)

/-- Main arbitrary finite-history result. The initial table is unrestricted:
    it may be defective, but it starts outside absorbing X. -/
theorem finite_history_safety {n} (c : Config n) (table : Table)
    {s : State n} {events : List (Event n)}
    (trace : Trace c (Initial c table) events s) :
    Consistent c s ∧ s.damaged = false ∧ AuthorizedTrace c (Initial c table) events s := by
  have init := consistent_initial c table
  exact ⟨consistent_trace init trace,
    trace_safe init rfl trace, trace_writes_authorized init trace⟩

/-- Direct universal form for the actual reached pre-state of any finite prefix;
    no choice of a second trace or an existential success certificate is needed. -/
theorem finite_history_admission {n} (c : Config n) (table : Table)
    {s : State n} {events : List (Event n)}
    (trace : Trace c (Initial c table) events s)
    (k : Command n) (requester : Nat) (admitted : Lands c s k requester) :
    requester = k.recipient ∧ k.epoch = s.epoch ∧ Authorized k (c.source s.epoch) := by
  exact admitted_current_authorized
    (consistent_trace (consistent_initial c table) trace) k requester admitted

/-- An event completely determines the next state. The separate AuthorizedTrace
    certificate therefore cannot select a safer nondeterministic execution. -/
theorem step_deterministic {n} {c : Config n} {s t u : State n} {a : Event n}
    (first : Step c s a t) (second : Step c s a u) : t = u := by
  cases first <;> cases second <;> rfl

theorem trace_epoch {n} {c : Config n} {s t : State n} {as : List (Event n)}
    (trace : Trace c s as t) : s.epoch ≤ t.epoch := by
  induction trace with
  | nil => exact le_rfl
  | cons step _ ih => exact (step_epoch step).trans ih

def Restored {n} (c : Config n) (s : State n) : Prop :=
  s.table = (c.source s.epoch).table ∧ s.damaged = false

theorem authorized_table {n} {k : Command n} {d : Descriptor}
    (h : Authorized k d) : k.table = d.table := h.2.2.2.2.2.2

/-- No claimed progress: this preserves an already established whole-table goal.
    A live admitted repair also establishes it; holding/blocking is identity. -/
theorem step_table_effect {n} {c : Config n} {s t : State n} {a : Event n}
    (h : Consistent c s) (safe : s.damaged = false) (step : Step c s a t) :
    t.table = s.table ∨ t.table = (c.source t.epoch).table := by
  cases step with
  | land k requester admitted =>
    right
    obtain ⟨requesterEq, _, auth⟩ := admitted_current_authorized h k requester admitted
    simpa [land, safe, requesterEq, auth] using authorized_table auth
  | _ =>
    left
    simp [request, acknowledge, complete, deliver, prepare, cancelAck, setRoot] <;>
      split_ifs <;> rfl

theorem step_restored {n} {c : Config n} {s t : State n} {a : Event n}
    (h : Consistent c s) (restored : Restored c s) (step : Step c s a t)
    (stable : s.epoch = t.epoch) : Restored c t := by
  refine ⟨?_, step_safe h restored.2 step⟩
  rcases step_table_effect h restored.2 step with identity | repair
  · rw [identity, ← stable]
    exact restored.1
  · exact repair

/-- Stable endpoints suffice because epoch monotonicity forbids an intervening
    transition and rewind. All arbitrary late preparations/cancellations remain. -/
theorem stable_trace_preserves_goal {n} {c : Config n} {s t : State n}
    {events : List (Event n)} (h : Consistent c s) (restored : Restored c s)
    (trace : Trace c s events t) (stable : s.epoch = t.epoch) : Restored c t := by
  induction trace with
  | nil => exact restored
  | @cons s u t a as step tail ih =>
    have su := step_epoch step
    have ut := trace_epoch tail
    have same : s.epoch = u.epoch := by omega
    exact ih (consistent_step h step) (step_restored h restored step same) (by omega)

theorem admitted_repair_restores {n} {c : Config n} {s : State n}
    (h : Consistent c s) (safe : s.damaged = false)
    (k : Command n) (requester : Nat) (admitted : Lands c s k requester) :
    Restored c (land c s k requester) := by
  obtain ⟨requesterEq, _, auth⟩ := admitted_current_authorized h k requester admitted
  exact ⟨by simpa [land, safe, requesterEq, auth] using authorized_table auth,
    by simp [land, safe, requesterEq, auth]⟩

/-- The reservation/consent institution is a distinct external premise, not a
    gate guard, not certificate algebra, and not a theorem about real consent. -/
def Reservation {n} (c : Config n)
    (externalAllowed : State n → Command n → Nat → Prop) : Prop :=
  ∀ s k requester, Reachable c s → ValidPath c k → requester = k.recipient →
    Authorized k (c.source s.epoch) → externalAllowed s k requester

theorem admitted_externally_authorized {n} {c : Config n} {s : State n}
    {externalAllowed : State n → Command n → Nat → Prop}
    (reservation : Reservation c externalAllowed) (reachable : Reachable c s)
    (k : Command n) (requester : Nat) (admitted : Lands c s k requester) :
    externalAllowed s k requester := by
  obtain ⟨req, _, auth⟩ := admitted_current_authorized (reachable_consistent reachable)
    k requester admitted
  exact reservation s k requester reachable admitted.1 req auth

#print axioms finite_history_safety
#print axioms finite_history_admission
#print axioms step_deterministic
#print axioms stable_trace_preserves_goal
#print axioms admitted_repair_restores
#print axioms admitted_externally_authorized
end InterlockHistory
