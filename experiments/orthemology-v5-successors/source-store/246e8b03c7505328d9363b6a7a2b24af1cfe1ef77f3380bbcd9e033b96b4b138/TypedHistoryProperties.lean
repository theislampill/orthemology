import TypedInstantiation

namespace OperationalJoin.Typed
noncomputable section
open Classical
open ComposedExecution

theorem reachable_safe {n} {I : Interface n} {c : Config I} {s : State I}
    (reachable : Reachable c s) : s.damaged = false := by
  obtain ⟨plant, events, history⟩ := reachable
  exact (finite_history_safety c plant history).2.1

/-- This is the exact typed plant-level effect of each allowed primitive event. -/
def PlantStep {n} (c : Config (interface n))
    (s : State (interface n)) (a : Event (interface n)) (t : State (interface n)) : Prop :=
  match a with
  | .land e _requester time =>
      localStep s.plant (c.source s.epoch) time e.val.action = some e.val.successor ∧
        t.plant = e.val.successor
  | _ => t.plant = s.plant

theorem step_plant {n} {c : Config (interface n)} {s t : State (interface n)}
    {a : Event (interface n)} (consistent : Consistent c s) (safe : s.damaged = false)
    (step : Step c s a t) : PlantStep c s a t := by
  cases step with
  | land e requester time admitted =>
      have auth := (admitted_current_authorized consistent time e requester admitted).2.2
      refine ⟨auth.2, ?_⟩
      have noDamage : ¬(s.damaged = true ∨
          ¬(interface n).admits s.plant time (c.source s.epoch) e requester) := by
        simp only [safe, Bool.false_eq_true, false_or, not_not]
        exact auth
      rw [land, if_neg noDamage]
      rfl
  | _ =>
      simp [PlantStep, request, acknowledge, complete, deliver, prepare, cancelAck, setRoot]
        <;> split_ifs <;> rfl

def Custody (original p : ComposedExecution.Plant) : Prop :=
  p.source = original.source ∧ p.destination = original.destination ∧
    p.standard = original.standard ∧ p.unrelated = original.unrelated

theorem finite_history_custody {n} (c : Config (interface n))
    (original : ComposedExecution.Plant) {s : State (interface n)}
    {events : List (Event (interface n))}
    (history : Trace c (Initial c original) events s) : Custody original s.plant := by
  apply trace_preserves (Custody original) ?_ (consistent_initial c original) rfl ?_ history
  · intro p time policy e requester admitted custody
    obtain ⟨source, destination, standard, unrelated⟩ :=
      local_source_and_custody_frame p policy time e.val.action e.val.successor admitted.2
    exact ⟨source.trans custody.1, destination.trans custody.2.1,
      standard.trans custody.2.2.1, unrelated.trans custody.2.2.2⟩
  · exact ⟨rfl, rfl, rfl, rfl⟩

def installDelta {n} : Event (interface n) → Nat
  | .land e _ _ => match e.val.action with | .install _ => 1 | .repair _ => 0
  | _ => 0

def repairDelta {n} : Event (interface n) → Nat
  | .land e _ _ => match e.val.action with | .install _ => 0 | .repair _ => 1
  | _ => 0

def installCount {n} (events : List (Event (interface n))) : Nat := (events.map installDelta).sum
def repairCount {n} (events : List (Event (interface n))) : Nat := (events.map repairDelta).sum

theorem step_counters {n} {c : Config (interface n)} {s t : State (interface n)}
    {a : Event (interface n)} (consistent : Consistent c s) (safe : s.damaged = false)
    (step : Step c s a t) :
    t.plant.ruleVersion = s.plant.ruleVersion + installDelta a ∧
    t.plant.draftRevision = s.plant.draftRevision + repairDelta a ∧
    t.plant.ruleHistory.length = s.plant.ruleHistory.length + installDelta a ∧
    t.plant.draftHistory.length = s.plant.draftHistory.length + repairDelta a := by
  have effect := step_plant consistent safe step
  cases a with
  | land e requester time =>
      obtain ⟨accepted, successor⟩ := effect
      rw [successor]
      cases kind : e.val.action with
      | install command =>
          rw [kind] at accepted
          rw [local_install_full_effect _ _ _ _ _ accepted]
          simp [installDelta, repairDelta, kind]
      | repair command =>
          rw [kind] at accepted
          rw [local_repair_full_effect _ _ _ _ _ accepted]
          simp [installDelta, repairDelta, kind]
  | _ =>
      simp only [PlantStep] at effect
      simp [effect, installDelta, repairDelta]

theorem trace_counters {n} {c : Config (interface n)} {s t : State (interface n)}
    {events : List (Event (interface n))} (consistent : Consistent c s)
    (safe : s.damaged = false) (history : Trace c s events t) :
    t.plant.ruleVersion = s.plant.ruleVersion + installCount events ∧
    t.plant.draftRevision = s.plant.draftRevision + repairCount events ∧
    t.plant.ruleHistory.length = s.plant.ruleHistory.length + installCount events ∧
    t.plant.draftHistory.length = s.plant.draftHistory.length + repairCount events := by
  induction history with
  | nil => simp [installCount, repairCount]
  | cons step _ ih =>
      have one := step_counters consistent safe step
      have tail := ih (consistent_step consistent step) (step_safe consistent safe step)
      simp only [installCount, repairCount, List.map_cons, List.sum_cons] at *
      omega

/-- A fixed command remains unusable after any later lawful finite history,
not merely at the immediate successor; versions cannot rewind. -/
theorem fixed_action_excluded_after_continuation {n} {c : Config (interface n)}
    (p : ComposedExecution.Plant) (policy : ComposedExecution.Policy) (time : Nat)
    (e : BoundedEnvelope n) (accepted : localStep p policy time e.val.action = some e.val.successor)
    {s t : State (interface n)} {events : List (Event (interface n))}
    (same : s.plant = e.val.successor) (reachable : Reachable c s)
    (history : Trace c s events t) (laterPolicy : ComposedExecution.Policy) (laterTime : Nat) :
    localStep t.plant laterPolicy laterTime e.val.action = none := by
  have counters := trace_counters (reachable_consistent reachable) (reachable_safe reachable) history
  cases result : localStep t.plant laterPolicy laterTime e.val.action with
  | none => rfl
  | some next =>
      exfalso
      cases kind : e.val.action with
      | install command =>
          rw [kind] at accepted result
          have before := local_install_expected_version p policy time command e.val.successor accepted
          have after := local_install_expected_version t.plant laterPolicy laterTime command next result
          have full := local_install_full_effect p policy time command e.val.successor accepted
          rw [same, full] at counters
          simp only at counters
          omega
      | repair command =>
          rw [kind] at accepted result
          have before := local_repair_expected_revision p policy time command e.val.successor accepted
          have after := local_repair_expected_revision t.plant laterPolicy laterTime command next result
          have full := local_repair_full_effect p policy time command e.val.successor accepted
          rw [same, full] at counters
          simp only at counters
          omega

#print axioms step_plant
#print axioms finite_history_custody
#print axioms trace_counters
#print axioms fixed_action_excluded_after_continuation
end
end OperationalJoin.Typed
