import JoinSafety
namespace OperationalJoin
noncomputable section
open Classical

def WriteSafe {n} {I : Interface n} (c : Config I) (s : State I) (a : Event I) : Prop :=
  ∀ k requester time, a = .land k requester time →
    requester = I.recipient k ∧ I.commandEpoch k = s.epoch ∧
      I.admits s.plant time (c.source s.epoch) k requester

inductive AuthorizedTrace {n} {I : Interface n} (c : Config I) :
    State I → List (Event I) → State I → Prop where
  | nil (s) : AuthorizedTrace c s [] s
  | cons {s t u a as} : Step c s a t → WriteSafe c s a →
      AuthorizedTrace c t as u → AuthorizedTrace c s (a :: as) u

theorem step_writeSafe {n} {I : Interface n} {c : Config I} {s t : State I} {a : Event I}
    (h : Consistent c s) (step : Step c s a t) : WriteSafe c s a := by
  intro k requester time eq
  subst a
  cases step with
  | land _ _ _ admitted => exact admitted_current_authorized h time k requester admitted

theorem trace_writes_authorized {n} {I : Interface n} {c : Config I} {s t : State I}
    {as : List (Event I)} (h : Consistent c s) (trace : Trace c s as t) :
    AuthorizedTrace c s as t := by
  induction trace with
  | nil => exact .nil _
  | cons step _ ih => exact .cons step (step_writeSafe h step) (ih (consistent_step h step))

theorem step_safe {n} {I : Interface n} {c : Config I} {s t : State I} {a : Event I}
    (h : Consistent c s) (safe : s.damaged = false) (step : Step c s a t) :
    t.damaged = false := by
  cases step with
  | land k requester time admitted =>
    have auth := (admitted_current_authorized h time k requester admitted).2.2
    simp [land, safe, auth]
  | _ =>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck,
      setRoot] <;> split_ifs <;> simp_all

theorem trace_safe {n} {I : Interface n} {c : Config I} {s t : State I}
    {as : List (Event I)} (h : Consistent c s) (safe : s.damaged = false)
    (trace : Trace c s as t) : t.damaged = false := by
  induction trace with
  | nil => exact safe
  | cons step _ ih => exact ih (consistent_step h step) (step_safe h safe step)

theorem finite_history_safety {n} {I : Interface n} (c : Config I) (plant : I.Plant)
    {s : State I} {events : List (Event I)} (trace : Trace c (Initial c plant) events s) :
    Consistent c s ∧ s.damaged = false ∧ AuthorizedTrace c (Initial c plant) events s := by
  have init := consistent_initial c plant
  exact ⟨consistent_trace init trace, trace_safe init rfl trace, trace_writes_authorized init trace⟩

theorem finite_history_admission {n} {I : Interface n} (c : Config I) (plant : I.Plant)
    {s : State I} {events : List (Event I)} (trace : Trace c (Initial c plant) events s)
    (time : Nat) (k : I.Command) (requester : I.Requester) (admitted : Lands c s time k requester) :
    requester = I.recipient k ∧ I.commandEpoch k = s.epoch ∧
      I.admits s.plant time (c.source s.epoch) k requester := by
  exact admitted_current_authorized
    (consistent_trace (consistent_initial c plant) trace) time k requester admitted

theorem step_deterministic {n} {I : Interface n} {c : Config I} {s t u : State I} {a : Event I}
    (first : Step c s a t) (second : Step c s a u) : t = u := by
  cases first <;> cases second <;> rfl

theorem trace_epoch {n} {I : Interface n} {c : Config I} {s t : State I}
    {as : List (Event I)} (trace : Trace c s as t) : s.epoch ≤ t.epoch := by
  induction trace with
  | nil => exact le_rfl
  | cons step _ ih => exact (step_epoch step).trans ih

/-- This is a conditional proof rule, not an interface law. Each concrete
plant invariant must separately discharge its own admitted-effect preservation. -/
theorem step_preserves {n} {I : Interface n} {c : Config I} {s t : State I} {a : Event I}
    (property : I.Plant → Prop)
    (effect_preserves : ∀ p time d k requester,
      I.admits p time d k requester → property p → property (I.effect p k))
    (h : Consistent c s) (safe : s.damaged = false) (old : property s.plant)
    (step : Step c s a t) : property t.plant := by
  cases step with
  | land k requester time admitted =>
    have auth := (admitted_current_authorized h time k requester admitted).2.2
    simpa [land, safe, auth] using effect_preserves _ _ _ _ _ auth old
  | _ =>
    simp_all [request, acknowledge, complete, deliver, prepare, cancelAck, setRoot]
      <;> split_ifs <;> simp_all

theorem trace_preserves {n} {I : Interface n} {c : Config I} {s t : State I}
    {as : List (Event I)} (property : I.Plant → Prop)
    (effect_preserves : ∀ p time d k requester,
      I.admits p time d k requester → property p → property (I.effect p k))
    (h : Consistent c s) (safe : s.damaged = false) (old : property s.plant)
    (trace : Trace c s as t) : property t.plant := by
  induction trace with
  | nil => exact old
  | cons step _ ih =>
    exact ih (consistent_step h step) (step_safe h safe step)
      (step_preserves property effect_preserves h safe old step)

theorem trace_append {n} {I : Interface n} {c : Config I} {s t u : State I}
    {xs ys : List (Event I)} (first : Trace c s xs t) (second : Trace c t ys u) :
    Trace c s (xs ++ ys) u := by
  induction first with
  | nil => exact second
  | cons step _ ih => exact .cons step (ih second)

theorem reachable_after {n} {I : Interface n} {c : Config I} {s t : State I}
    {events : List (Event I)} (reach : Reachable c s) (trace : Trace c s events t) :
    Reachable c t := by
  obtain ⟨plant, prior, before⟩ := reach
  exact ⟨plant, prior ++ events, trace_append before trace⟩

/-- External reservation remains an additional institutional premise. It is
not used by any gate, history invariant, or finite-history safety theorem. -/
def Reservation {n} {I : Interface n} (c : Config I)
    (externalAllowed : State I → Nat → I.Command → I.Requester → Prop) : Prop :=
  ∀ s time k requester, Reachable c s → ValidPath c k →
    I.admits s.plant time (c.source s.epoch) k requester → externalAllowed s time k requester

theorem admitted_externally_authorized {n} {I : Interface n} {c : Config I} {s : State I}
    {externalAllowed : State I → Nat → I.Command → I.Requester → Prop}
    (reservation : Reservation c externalAllowed) (reachable : Reachable c s)
    (time : Nat) (k : I.Command) (requester : I.Requester) (admitted : Lands c s time k requester) :
    externalAllowed s time k requester := by
  have auth := (admitted_current_authorized (reachable_consistent reachable) time k requester admitted).2.2
  exact reservation s time k requester reachable admitted.1 auth

#print axioms finite_history_safety
#print axioms finite_history_admission
#print axioms trace_preserves
#print axioms admitted_externally_authorized
end
end OperationalJoin
