import HistoryTrace
import NegativeControls
open InterlockHistory

/-- Compile the quantified public statement separately from its authoring file. -/
example {n} (c : Config n) (initialTable : Table) {s : State n}
    {events : List (Event n)} (run : Trace c (Initial c initialTable) events s) :
    s.damaged = false ∧ AuthorizedTrace c (Initial c initialTable) events s := by
  exact (finite_history_safety c initialTable run).2

example {n} {c : Config n} {s t : State n} {events : List (Event n)}
    (reach : Reachable c s) (run : Trace c s events t) (k : Command n)
    (closed : Cancelled c s k) : ∀ requester, ¬Lands c t k requester := by
  intro requester
  exact no_landing_after_cancellation reach run k requester closed

example {n} {c : Config n} {s t : State n} {events : List (Event n)}
    (reach : Reachable c s) (goal : Restored c s) (run : Trace c s events t)
    (unchanged : s.epoch = t.epoch) : Restored c t := by
  exact stable_trace_preserves_goal (reachable_consistent reach) goal run unchanged

example {n} (c : Config n) (table : Table) {s : State n} {events : List (Event n)}
    (trace : Trace c (Initial c table) events s) (k : Command n) (requester : Nat)
    (admitted : Lands c s k requester) :
    k.epoch = s.epoch ∧ Authorized k (c.source s.epoch) := by
  exact (finite_history_admission c table trace k requester admitted).2

#print axioms finite_history_safety
#print axioms no_landing_after_cancellation
#print axioms stable_trace_preserves_goal
