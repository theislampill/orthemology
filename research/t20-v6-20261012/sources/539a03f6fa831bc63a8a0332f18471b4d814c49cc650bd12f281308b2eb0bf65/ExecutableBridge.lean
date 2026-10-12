import ExecutableKernel
import NativeUniformEffect

namespace SharedAlias.Executable.Bridge
open ComposedExecution

/-- Preserve every finite routing field. This function is not an actor API. -/
def routingView {m} (D : Routing m) : Native.Routing m :=
  ⟨D.aliasMembers, D.faultyRoots, D.budget, D.q, D.r⟩

/-- Stronger than the accepted set view: preserve every raw finite-state
field, including root/receipt row order, defaults and malformed old memories. -/
def stateView {m} (C : FiniteState m) : Native.FiniteState m :=
  ⟨C.epoch, C.defaultRoot, C.rootRows, C.pending, C.acks, C.certificateRows, C.cancelRows, C.plant⟩

def annotationView {m} (a : Annotation m) : Native.Annotation m :=
  ⟨a.time, a.prepareBits, a.openGate, a.cancelBits⟩

def specView {m} (s : Spec m) : Native.NativeSpec m := ⟨s.command, annotationView s.annotation⟩

def eventView {m} : ServiceEvent m → OperationalJoin.Event (OperationalJoin.Typed.interface m)
  | .prepare i k who time => .prepare i k who time
  | .cancelAck i k who => .cancelAck i k who
  | .land k who time => .land k who time
  | .close k => .close k
  | .hold => .hold

def outcomeView {m} (result : Outcome m) : Native.Outcome m :=
  ⟨stateView result.state, result.events.map eventView⟩

theorem tableRead_exact {α β : Type} [DecidableEq α] (rows : List (α × β)) (key : α) (fallback : β) :
    tableRead rows key fallback = Native.tableRead rows key fallback := by
  induction rows with
  | nil => rfl
  | cons row rows ih => simp only [tableRead, Native.tableRead, ih]

theorem rootOf_exact {m} (D : Routing m) (i : Fin m) :
    rootOf D i = Native.rootOf (routingView D) i := rfl

theorem faulty_exact {m} (D : Routing m) (i : Fin m) :
    faulty D i = Native.faulty (routingView D) i := rfl

theorem rootAt_exact {m} (C : FiniteState m) (r : Option (Fin m)) :
    rootAt C r = Native.rootAt (stateView C) r := tableRead_exact _ _ _

theorem receipts_exact {m} (C : FiniteState m) (k : ComposedExecution.Envelope) :
    receipts C k = Native.receipts (stateView C) k := tableRead_exact _ _ _

theorem setRoot_exact {m} (C : FiniteState m) (r : Option (Fin m)) (z : Root) :
    stateView (setRoot C r z) = Native.setRoot (stateView C) r z := rfl

theorem initial_exact {m} (policy : Policy) (p : Plant) :
    stateView (initial (m := m) policy p) = Native.initial policy p := rfl

theorem gateWorld_exact {m} (D : Routing m) (C : FiniteState m) (time : Nat) (policy : Policy) :
    gateWorld D C time policy = Native.gateWorld (routingView D) (stateView C) time policy := by
  unfold gateWorld Native.gateWorld
  congr 1
  funext i
  split
  · exact rootAt_exact C _
  · rfl

theorem prepareAllowed_exact {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (time : Nat) (bad : Bool) :
    prepareAllowed D C i k who time bad =
      Native.prepareAllowed (routingView D) (stateView C) i k who time bad := by
  simp only [prepareAllowed, Native.prepareAllowed, gateWorld_exact, rootOf_exact,
    rootAt_exact, faulty_exact, stateView]

theorem prepareUpdate_exact {m} (D : Routing m) (C : FiniteState m) (i : Fin m) (k : Command m) :
    stateView (prepareUpdate D C i k) = Native.prepareUpdate (routingView D) (stateView C) i k := by
  simp only [prepareUpdate, Native.prepareUpdate, setRoot_exact, rootOf_exact, rootAt_exact]

theorem prepareSlot_exact {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (time : Nat) (bad : Bool) :
    stateView (prepareSlot D C i k who time bad) =
      Native.prepareSlot (routingView D) (stateView C) i k who time bad := by
  simp only [prepareSlot, Native.prepareSlot, ← prepareAllowed_exact]
  split
  · exact prepareUpdate_exact D C i k
  · rfl

theorem cancelAllowed_exact {m} (D : Routing m) (i : Fin m) (k : Command m) (who : String) (bad : Bool) :
    cancelAllowed D i k who bad = Native.cancelAllowed (routingView D) i k who bad := rfl

theorem cancelUpdate_exact {m} (D : Routing m) (C : FiniteState m) (i : Fin m) (k : Command m) :
    stateView (cancelUpdate D C i k) = Native.cancelUpdate (routingView D) (stateView C) i k := by
  simp only [cancelUpdate, Native.cancelUpdate, ← faulty_exact]
  split
  · simp only [stateView, receipts_exact] <;> rfl
  · simp only [setRoot_exact, rootOf_exact, rootAt_exact, stateView, receipts_exact] <;> rfl

theorem cancelSlot_exact {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (bad : Bool) :
    stateView (cancelSlot D C i k who bad) =
      Native.cancelSlot (routingView D) (stateView C) i k who bad := by
  simp only [cancelSlot, Native.cancelSlot, ← cancelAllowed_exact]
  split
  · exact cancelUpdate_exact D C i k
  · rfl

theorem applied_exact {m} (D : Routing m) (C : FiniteState m) (k : Command m)
    (who : String) (time : Nat) (bad : Bool) :
    applied D C k who time bad = Native.applied (routingView D) (stateView C) k who time bad := by
  simp only [applied, Native.applied, gateWorld_exact, stateView]

theorem attemptSlot_exact {m} (D : Routing m) (C : FiniteState m) (k : Command m)
    (who : String) (time : Nat) (bad : Bool) :
    stateView (attemptSlot D C k who time bad) =
      Native.attemptSlot (routingView D) (stateView C) k who time bad := by
  simp only [attemptSlot, Native.attemptSlot, ← gateWorld_exact,
    show (stateView C).defaultRoot = C.defaultRoot from rfl]
  split <;> rfl

theorem distinctCount_card {α : Type} [DecidableEq α] (xs : List α) :
    distinctCount xs = xs.toFinset.card := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      by_cases member : x ∈ xs
      · simp only [distinctCount, if_pos member, List.toFinset_cons,
          Finset.card_insert_of_mem (List.mem_toFinset.mpr member), ih]
      · have notmem : x ∉ xs.toFinset := fun h => member (List.mem_toFinset.mp h)
        simp only [distinctCount, if_neg member, List.toFinset_cons,
          Finset.card_insert_of_not_mem notmem, ih]

theorem closed_exact {m} (D : Routing m) (C : FiniteState m) (k : Command m) :
    closed D C k = Native.closed (routingView D) (stateView C) k := by
  simp only [closed, Native.closed, distinctCount_card, receipts_exact, routingView]

theorem prepareEvent_exact {m} (D : Routing m) (C : FiniteState m) (i : Fin m)
    (k : Command m) (who : String) (time : Nat) (bad : Bool) :
    eventView (prepareEvent D C i k who time bad) =
      Native.prepareEvent (routingView D) (stateView C) i k who time bad := by
  simp only [prepareEvent, Native.prepareEvent, ← prepareAllowed_exact]
  split <;> rfl

theorem cancelEvent_exact {m} (D : Routing m) (i : Fin m) (k : Command m) (who : String) (bad : Bool) :
    eventView (cancelEvent D i k who bad) = Native.cancelEvent (routingView D) i k who bad := by
  simp only [cancelEvent, Native.cancelEvent, ← cancelAllowed_exact]
  split <;> rfl

theorem attemptEvent_exact {m} (D : Routing m) (C : FiniteState m) (k : Command m)
    (who : String) (time : Nat) (bad : Bool) :
    eventView (attemptEvent D C k who time bad) =
      Native.attemptEvent (routingView D) (stateView C) k who time bad := by
  simp only [attemptEvent, Native.attemptEvent, ← applied_exact]
  split <;> rfl

theorem closeEvent_exact {m} (D : Routing m) (C : FiniteState m) (k : Command m) :
    eventView (closeEvent D C k) = Native.closeEvent (routingView D) (stateView C) k := by
  simp only [closeEvent, Native.closeEvent, ← closed_exact]
  split <;> rfl

theorem commandLabels_exact {m} (k : Command m) : commandLabels k = Native.commandLabels k := rfl

theorem serviceLoop_exact {m}
    (handler : FiniteState m → Fin m → FiniteState m × ServiceEvent m)
    (nativeHandler : Native.FiniteState m → Fin m →
      Native.FiniteState m × OperationalJoin.Event (OperationalJoin.Typed.interface m))
    (states : ∀ C i, stateView (handler C i).1 = (nativeHandler (stateView C) i).1)
    (events : ∀ C i, eventView (handler C i).2 = (nativeHandler (stateView C) i).2)
    (C : FiniteState m) (labels : List (Fin m)) :
    outcomeView (serviceLoop handler C labels) = Native.serviceLoop nativeHandler (stateView C) labels := by
  induction labels generalizing C with
  | nil => rfl
  | cons i labels ih =>
      have later := ih (handler C i).1
      have stateEq := congrArg Native.Outcome.state later
      have eventsEq := congrArg Native.Outcome.events later
      simp only [outcomeView] at stateEq eventsEq
      rw [states] at stateEq eventsEq
      simp only [serviceLoop, Native.serviceLoop, outcomeView, List.map_cons, states, events,
        stateEq, eventsEq]

theorem prepareRun_exact {m} (D : Routing m) (C : FiniteState m) (k : Command m)
    (who : String) (a : Annotation m) :
    outcomeView (prepareRun D C k who a) =
      Native.prepareRun (routingView D) (stateView C) k who (annotationView a) := by
  apply serviceLoop_exact _
    (fun C i => (Native.prepareSlot (routingView D) C i k who a.time (prepareReply a i),
      Native.prepareEvent (routingView D) C i k who a.time (prepareReply a i)))
  · intro C i; exact prepareSlot_exact D C i k who a.time (prepareReply a i)
  · intro C i; exact prepareEvent_exact D C i k who a.time (prepareReply a i)

theorem cancelRun_exact {m} (D : Routing m) (C : FiniteState m) (k : Command m)
    (who : String) (a : Annotation m) :
    outcomeView (cancelRun D C k who a) =
      Native.cancelRun (routingView D) (stateView C) k who (annotationView a) := by
  apply serviceLoop_exact _
    (fun C i => (Native.cancelSlot (routingView D) C i k who (cancelReply a i),
      Native.cancelEvent (routingView D) i k who (cancelReply a i)))
  · intro C i; exact cancelSlot_exact D C i k who (cancelReply a i)
  · intro C i; exact cancelEvent_exact D i k who (cancelReply a i)

theorem trialRun_exact {m} (D : Routing m) (C : FiniteState m) (who : String) (s : Spec m) :
    outcomeView (trialRun D C who s) = Native.trialRun (routingView D) (stateView C) who (specView s) := by
  have prep := prepareRun_exact D C s.command who s.annotation
  have prepState := congrArg Native.Outcome.state prep
  have prepEvents := congrArg Native.Outcome.events prep
  have attempt := attemptSlot_exact D (prepareRun D C s.command who s.annotation).state
    s.command who s.annotation.time s.annotation.openGate
  have attempted := attemptEvent_exact D (prepareRun D C s.command who s.annotation).state
    s.command who s.annotation.time s.annotation.openGate
  have cancel := cancelRun_exact D
    (attemptSlot D (prepareRun D C s.command who s.annotation).state s.command who s.annotation.time s.annotation.openGate)
    s.command who s.annotation
  have cancelState := congrArg Native.Outcome.state cancel
  have cancelEvents := congrArg Native.Outcome.events cancel
  simp only [outcomeView] at prepState prepEvents cancelState cancelEvents
  simp only [prepState] at attempt attempted
  simp only [attempt] at cancelState cancelEvents
  simp only [trialRun, Native.trialRun, specView, outcomeView, List.map_append, List.map_cons,
    List.map_singleton, prepState, prepEvents, attempt, attempted, cancelState, cancelEvents,
    closeEvent_exact]
  rfl

theorem runNative_exact {m} (D : Routing m) (who : String) (C : FiniteState m) (specs : List (Spec m)) :
    outcomeView (runNative D who C specs) =
      Native.runNative (routingView D) who (stateView C) (specs.map specView) := by
  induction specs generalizing C with
  | nil => rfl
  | cons s specs ih =>
      have first := trialRun_exact D C who s
      have stateEq := congrArg Native.Outcome.state first
      have eventsEq := congrArg Native.Outcome.events first
      have later := ih (trialRun D C who s).state
      have laterState := congrArg Native.Outcome.state later
      have laterEvents := congrArg Native.Outcome.events later
      simp only [outcomeView] at stateEq eventsEq laterState laterEvents
      rw [stateEq] at laterState laterEvents
      simp only [runNative, Native.runNative, List.map_cons, outcomeView, List.map_append,
        stateEq, eventsEq, laterState, laterEvents]

end SharedAlias.Executable.Bridge
