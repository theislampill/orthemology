import JoinTrace
import HistoryTrace

namespace OperationalJoin.OriginalTranslation
noncomputable section
open Classical


def interface (n : Nat) : Interface n where
  Policy := InterlockHistory.Descriptor
  Command := InterlockHistory.Command n
  Plant := InterlockHistory.Table
  Requester := Nat
  policyEpoch := InterlockHistory.Descriptor.epoch
  commandEpoch := InterlockHistory.Command.epoch
  commandPath := InterlockHistory.Command.path
  recipient := InterlockHistory.Command.recipient
  admits := fun _ _ d k requester => requester = k.recipient ∧ InterlockHistory.Authorized k d
  effect := fun _ k => k.table
  admitted_epoch := by intro p time d k requester h; exact h.2.2.1
  admitted_requester := by intro p time d k requester h; exact h.1

def config {n} (c : InterlockHistory.Config n) : Config (interface n) where
  budget := c.budget
  q := c.q
  r := c.r
  faulty := c.faulty
  budget_bound := c.budget_bound
  overlap := c.overlap
  budget_lt_roots := c.budget_lt_roots
  repair_available := c.repair_available
  revoke_available := c.revoke_available
  source := c.source
  source_epoch := c.source_epoch

def liftRoot {n} (z : InterlockHistory.RootState n) : RootState (interface n) :=
  ⟨z.descriptor, z.revoked, z.commitments, z.cancelled⟩
def lowerRoot {n} (z : RootState (interface n)) : InterlockHistory.RootState n :=
  ⟨z.descriptor, z.revoked, z.commitments, z.cancelled⟩
def liftState {n} (s : InterlockHistory.State n) : State (interface n) :=
  ⟨s.epoch, fun i => liftRoot (s.roots i), s.pending, s.acks,
    s.certificates, s.cancelAcks, s.table, s.damaged⟩
def lowerState {n} (s : State (interface n)) : InterlockHistory.State n :=
  ⟨s.epoch, fun i => lowerRoot (s.roots i), s.pending, s.acks,
    s.certificates, s.cancelAcks, s.plant, s.damaged⟩

@[simp] theorem lower_lift_root {n} (z : InterlockHistory.RootState n) : lowerRoot (liftRoot z) = z := rfl
@[simp] theorem lift_lower_root {n} (z : RootState (interface n)) : liftRoot (lowerRoot z) = z := rfl
@[simp] theorem lower_lift_state {n} (s : InterlockHistory.State n) : lowerState (liftState s) = s := rfl
@[simp] theorem lift_lower_state {n} (s : State (interface n)) : liftState (lowerState s) = s := rfl

/-- Timestamps are erased only because this exact original admission ignores
its time argument. No original event constructor is omitted. -/
def lowerEvent {n} : Event (interface n) → InterlockHistory.Event n
  | .request => .request
  | .acknowledge i => .acknowledge i
  | .complete => .complete
  | .deliver i e => .deliver i e
  | .prepare i k requester _ => .prepare i k requester
  | .cancelAck i k requester => .cancelAck i k requester
  | .close k => .close k
  | .land k requester _ => .land k requester
  | .hold => .hold
  | .corrupt i z => .corrupt i (lowerRoot z)

def liftEvent {n} (time : Nat) : InterlockHistory.Event n → Event (interface n)
  | .request => .request
  | .acknowledge i => .acknowledge i
  | .complete => .complete
  | .deliver i e => .deliver i e
  | .prepare i k requester => .prepare i k requester time
  | .cancelAck i k requester => .cancelAck i k requester
  | .close k => .close k
  | .land k requester => .land k requester time
  | .hold => .hold
  | .corrupt i z => .corrupt i (liftRoot z)

@[simp] theorem lower_lift_event {n} (time : Nat) (a : InterlockHistory.Event n) :
    lowerEvent (liftEvent time a) = a := by cases a <;> rfl

@[simp] theorem envelope_iff {n} (s : State (interface n)) (time : Nat)
    (i : Fin n) (k : InterlockHistory.Command n) (requester : Nat) :
    Envelope s.plant time (s.roots i) k requester ↔
      InterlockHistory.Envelope ((lowerState s).roots i) k requester := by
  simp [Envelope, InterlockHistory.Envelope, interface, lowerState, lowerRoot, and_assoc]

@[simp] theorem permits_iff {n} (s : State (interface n)) (time : Nat)
    (i : Fin n) (k : InterlockHistory.Command n) (requester : Nat) :
    Permits s.plant time (s.roots i) k requester ↔
      InterlockHistory.Permits ((lowerState s).roots i) k requester := by
  simp [Permits, InterlockHistory.Permits, Envelope, InterlockHistory.Envelope, interface, lowerState, lowerRoot, and_assoc]

@[simp] theorem lands_iff {n} (c : InterlockHistory.Config n) (s : State (interface n))
    (time : Nat) (k : InterlockHistory.Command n) (requester : Nat) :
    Lands (config c) s time k requester ↔ InterlockHistory.Lands c (lowerState s) k requester := by
  simp [Lands, InterlockHistory.Lands, ValidPath, InterlockHistory.ValidPath, Good, InterlockHistory.Good, config, interface,
    Permits, InterlockHistory.Permits, Envelope, InterlockHistory.Envelope, lowerState, lowerRoot, and_assoc]

@[simp] theorem lower_initial {n} (c : InterlockHistory.Config n) (table : InterlockHistory.Table) :
    lowerState (Initial (config c) table) = InterlockHistory.Initial c table := rfl

@[simp] theorem lower_setRoot {n} (s : State (interface n)) (i : Fin n)
    (z : RootState (interface n)) :
    lowerState (setRoot s i z) = InterlockHistory.setRoot (lowerState s) i (lowerRoot z) := by
  simp only [lowerState, setRoot, InterlockHistory.setRoot]
  congr 1
  funext j
  by_cases eq : j = i <;> simp [Function.update_apply, eq]

@[simp] theorem lower_request {n} (s : State (interface n)) :
    lowerState (request s) = InterlockHistory.request (lowerState s) := rfl

@[simp] theorem lower_acknowledge {n} (c : InterlockHistory.Config n) (s : State (interface n)) (i : Fin n) :
    lowerState (acknowledge (config c) s i) = InterlockHistory.acknowledge c (lowerState s) i := by
  simp only [lowerState, acknowledge, InterlockHistory.acknowledge, Good, InterlockHistory.Good, config]
  congr 1
  funext j
  by_cases good : i ∉ c.faulty <;> by_cases eq : j = i <;>
    simp [Function.update_apply, good, eq, lowerRoot]

@[simp] theorem lower_complete {n} (s : State (interface n)) :
    lowerState (complete s) = InterlockHistory.complete (lowerState s) := rfl

@[simp] theorem lower_deliver {n} (c : InterlockHistory.Config n) (s : State (interface n)) (i : Fin n) (e : Nat) :
    lowerState (deliver (config c) s i e) = InterlockHistory.deliver c (lowerState s) i e := by
  simp only [deliver, InterlockHistory.deliver, interface, lowerState, lowerRoot, config]
  split_ifs
  · exact lower_setRoot s i { s.roots i with descriptor := c.source e }
  · rfl

@[simp] theorem lower_prepare {n} (s : State (interface n)) (i : Fin n) (k : InterlockHistory.Command n) :
    lowerState (prepare s i k) = InterlockHistory.prepare (lowerState s) i k := by
  unfold prepare InterlockHistory.prepare
  rw [lower_setRoot]
  simp only [lowerRoot, lowerState]
  congr 2
  ext x
  simp

@[simp] theorem lower_cancelAck {n} (c : InterlockHistory.Config n) (s : State (interface n))
    (i : Fin n) (k : InterlockHistory.Command n) :
    lowerState (cancelAck (config c) s i k) = InterlockHistory.cancelAck c (lowerState s) i k := by
  simp only [lowerState, cancelAck, InterlockHistory.cancelAck, Good, InterlockHistory.Good, config]
  congr 1
  · funext j
    by_cases good : i ∉ c.faulty <;> by_cases eq : j = i <;>
      simp [Function.update_apply, good, eq, lowerRoot]
    ext x
    simp
  · funext k'
    by_cases eq : k' = k <;> simp [Function.update_apply, eq]

/-- Exact even on damaged or unauthorized states, not only safe reachable ones. -/
@[simp] theorem lower_land {n} (c : InterlockHistory.Config n) (s : State (interface n))
    (time : Nat) (k : InterlockHistory.Command n) (requester : Nat) :
    lowerState (land (config c) s time k requester) = InterlockHistory.land c (lowerState s) k requester := by
  simp only [land, InterlockHistory.land, interface, config, lowerState]
  by_cases damaged : s.damaged = true <;>
    by_cases req : requester = k.recipient <;>
    by_cases auth : InterlockHistory.Authorized k (c.source s.epoch) <;>
    simp [damaged, req, auth, lowerState]

theorem lowerState_injective {n} : Function.Injective (@lowerState n) := by
  intro s t eq
  have := congrArg liftState eq
  simpa using this

@[simp] theorem lift_setRoot {n} (s : InterlockHistory.State n) (i : Fin n)
    (z : InterlockHistory.RootState n) :
    liftState (InterlockHistory.setRoot s i z) = setRoot (liftState s) i (liftRoot z) := by
  apply lowerState_injective
  simp
@[simp] theorem lift_request {n} (s : InterlockHistory.State n) :
    liftState (InterlockHistory.request s) = request (liftState s) := by
  apply lowerState_injective
  simp
@[simp] theorem lift_acknowledge {n} (c : InterlockHistory.Config n)
    (s : InterlockHistory.State n) (i : Fin n) :
    liftState (InterlockHistory.acknowledge c s i) = acknowledge (config c) (liftState s) i := by
  apply lowerState_injective
  simp
@[simp] theorem lift_complete {n} (s : InterlockHistory.State n) :
    liftState (InterlockHistory.complete s) = complete (liftState s) := by
  apply lowerState_injective
  simp
@[simp] theorem lift_deliver {n} (c : InterlockHistory.Config n)
    (s : InterlockHistory.State n) (i : Fin n) (e : Nat) :
    liftState (InterlockHistory.deliver c s i e) = deliver (config c) (liftState s) i e := by
  apply lowerState_injective
  simp
@[simp] theorem lift_prepare {n} (s : InterlockHistory.State n) (i : Fin n)
    (k : InterlockHistory.Command n) :
    liftState (InterlockHistory.prepare s i k) = prepare (liftState s) i k := by
  apply lowerState_injective
  simp
@[simp] theorem lift_cancelAck {n} (c : InterlockHistory.Config n)
    (s : InterlockHistory.State n) (i : Fin n) (k : InterlockHistory.Command n) :
    liftState (InterlockHistory.cancelAck c s i k) = cancelAck (config c) (liftState s) i k := by
  apply lowerState_injective
  simp
@[simp] theorem lift_land {n} (c : InterlockHistory.Config n) (s : InterlockHistory.State n)
    (time : Nat) (k : InterlockHistory.Command n) (requester : Nat) :
    liftState (InterlockHistory.land c s k requester) = land (config c) (liftState s) time k requester := by
  apply lowerState_injective
  simp

/-- Every event of every common binary specialization step has the unchanged
original step, including corruption and absorbing-damage cases. -/
theorem lower_step {n} {c : InterlockHistory.Config n} {s t : State (interface n)}
    {a : Event (interface n)} (step : Step (config c) s a t) :
    InterlockHistory.Step c (lowerState s) (lowerEvent a) (lowerState t) := by
  cases step with
  | request idle => simpa [lowerEvent] using InterlockHistory.Step.request (lowerState s) idle
  | acknowledge i pending =>
      simpa [lowerEvent] using InterlockHistory.Step.acknowledge (lowerState s) i pending
  | complete pending quorum =>
      simpa [lowerEvent] using InterlockHistory.Step.complete (lowerState s) pending quorum
  | deliver i e cert =>
      simpa [lowerEvent] using InterlockHistory.Step.deliver (lowerState s) i e cert
  | prepare i k requester time selected path grant =>
      have oldGrant : i ∈ c.faulty ∨ InterlockHistory.Envelope ((lowerState s).roots i) k requester := by
        rcases grant with bad | good
        · exact Or.inl bad
        · exact Or.inr ((envelope_iff s time i k requester).mp good)
      simpa [lowerEvent] using
        InterlockHistory.Step.prepare (lowerState s) i k requester selected path oldGrant
  | cancelAck i k requester selected auth =>
      simpa [lowerEvent] using InterlockHistory.Step.cancelAck (lowerState s) i k requester selected auth
  | close k cert => simpa [lowerEvent] using InterlockHistory.Step.close (lowerState s) k cert
  | land k requester time admitted =>
      simpa [lowerEvent] using InterlockHistory.Step.land (lowerState s) k requester
        ((lands_iff c s time k requester).mp admitted)
  | hold => exact InterlockHistory.Step.hold (lowerState s)
  | corrupt i z bad =>
      simpa [lowerEvent] using InterlockHistory.Step.corrupt (lowerState s) i (lowerRoot z) bad

/-- Conversely every original step lifts; the annotation is arbitrary because
this exact specialization does not consult time. -/
theorem lift_step {n} {c : InterlockHistory.Config n} {s t : InterlockHistory.State n}
    {a : InterlockHistory.Event n} (time : Nat) (step : InterlockHistory.Step c s a t) :
    Step (config c) (liftState s) (liftEvent time a) (liftState t) := by
  cases step with
  | request idle => simpa [liftEvent] using Step.request (c := config c) (liftState s) idle
  | acknowledge i pending =>
      simpa [liftEvent] using Step.acknowledge (c := config c) (liftState s) i pending
  | complete pending quorum =>
      simpa [liftEvent] using Step.complete (c := config c) (liftState s) pending quorum
  | deliver i e cert =>
      simpa [liftEvent] using Step.deliver (c := config c) (liftState s) i e cert
  | prepare i k requester selected path grant =>
      have newGrant : i ∈ (config c).faulty ∨
          Envelope (liftState s).plant time ((liftState s).roots i) k requester := by
        rcases grant with bad | good
        · exact Or.inl bad
        · right
          apply (envelope_iff (liftState s) time i k requester).mpr
          simpa using good
      simpa [liftEvent] using
        Step.prepare (c := config c) (liftState s) i k requester time selected path newGrant
  | cancelAck i k requester selected auth =>
      simpa [liftEvent] using Step.cancelAck (c := config c) (liftState s) i k requester selected auth
  | close k cert => simpa [liftEvent] using Step.close (c := config c) (liftState s) k cert
  | land k requester admitted =>
      have newLands : Lands (config c) (liftState s) time k requester := by
        apply (lands_iff c (liftState s) time k requester).mpr
        simpa using admitted
      simpa only [liftEvent, lift_land c s time k requester] using
        Step.land (c := config c) (liftState s) k requester time newLands
  | hold => exact Step.hold (liftState s)
  | corrupt i z bad =>
      simpa [liftEvent] using Step.corrupt (c := config c) (liftState s) i (liftRoot z) bad

theorem lower_trace {n} {c : InterlockHistory.Config n} {s t : State (interface n)}
    {events : List (Event (interface n))} (trace : Trace (config c) s events t) :
    InterlockHistory.Trace c (lowerState s) (events.map lowerEvent) (lowerState t) := by
  induction trace with
  | nil => exact .nil _
  | cons step _ ih => exact .cons (lower_step step) ih

theorem lift_trace {n} {c : InterlockHistory.Config n} {s t : InterlockHistory.State n}
    {events : List (InterlockHistory.Event n)} (time : Nat) (trace : InterlockHistory.Trace c s events t) :
    Trace (config c) (liftState s) (events.map (liftEvent time)) (liftState t) := by
  induction trace with
  | nil => exact .nil _
  | cons step _ ih => exact .cons (lift_step time step) ih

/-- Full original finite-history correspondence. Neither reachability, safety,
initial-state normality nor a restriction on original event kinds is assumed. -/
theorem trace_iff_lift_exists {n} (c : InterlockHistory.Config n) (s t : InterlockHistory.State n)
    (events : List (InterlockHistory.Event n)) :
    InterlockHistory.Trace c s events t ↔
      ∃ annotated, annotated.map lowerEvent = events ∧
        Trace (config c) (liftState s) annotated (liftState t) := by
  constructor
  · intro trace
    refine ⟨events.map (liftEvent 0), ?_, lift_trace 0 trace⟩
    simp [List.map_map, Function.comp_def]
  · rintro ⟨annotated, eq, trace⟩
    have old := lower_trace trace
    simpa [eq] using old

#print axioms lower_land
#print axioms lower_step
#print axioms lift_step
#print axioms trace_iff_lift_exists
end
end OperationalJoin.OriginalTranslation
