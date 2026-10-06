import AliasSimulation
import TypedHistoryProperties

namespace SharedAlias.Typed
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope)
noncomputable section
open Classical

theorem finite_history_admission {m} {E : Environment (interface m)}
    {C : SharedAlias.State (interface m)} (reach : SharedAlias.Reachable E C)
    (time : Nat) (k : BoundedEnvelope m) (who : String)
    (admitted : SharedAlias.Lands E C time k who) :
    who = k.val.action.actor ∧ k.val.action.epoch = C.epoch ∧
      ComposedExecution.localStep C.plant (E.source C.epoch) time k.val.action = some k.val.successor := by
  obtain ⟨recipient, epoch, _who, effect⟩ := admitted_current reach time k who admitted
  exact ⟨recipient, epoch, effect⟩

theorem finite_history_custody {m} (E : Environment (interface m))
    (p : ComposedExecution.Plant) {C : SharedAlias.State (interface m)}
    {events : List (Event (interface m))} (trace : SharedAlias.Trace E (initial E p) events C) :
    OperationalJoin.Typed.Custody p C.plant := by
  obtain ⟨s, expanded, common, related, _⟩ := initial_trace_simulation E p trace
  have custody := OperationalJoin.Typed.finite_history_custody E.labelConfig p common
  simpa only [related.plant] using custody

def installWeight {m} (x : BoundedEnvelope m × String × Nat) : Nat :=
  match x.1.val.action with | .install _ => 1 | .repair _ => 0

def repairWeight {m} (x : BoundedEnvelope m × String × Nat) : Nat :=
  match x.1.val.action with | .install _ => 0 | .repair _ => 1

theorem installCount_landings {m} (events : List (Event (interface m))) :
    OperationalJoin.Typed.installCount events = ((landings events).map installWeight).sum := by
  induction events with
  | nil => rfl
  | cons a events ih =>
      simp only [OperationalJoin.Typed.installCount] at ih
      cases a <;> simp [OperationalJoin.Typed.installCount, OperationalJoin.Typed.installDelta,
        landings, installWeight, ih]
      rfl

theorem repairCount_landings {m} (events : List (Event (interface m))) :
    OperationalJoin.Typed.repairCount events = ((landings events).map repairWeight).sum := by
  induction events with
  | nil => rfl
  | cons a events ih =>
      simp only [OperationalJoin.Typed.repairCount] at ih
      cases a <;> simp [OperationalJoin.Typed.repairCount, OperationalJoin.Typed.repairDelta,
        landings, repairWeight, ih]
      rfl

theorem trace_counters {m} {E : Environment (interface m)}
    {C D : SharedAlias.State (interface m)} {events : List (Event (interface m))}
    (reach : SharedAlias.Reachable E C) (trace : SharedAlias.Trace E C events D) :
    D.plant.ruleVersion = C.plant.ruleVersion + OperationalJoin.Typed.installCount events ∧
    D.plant.draftRevision = C.plant.draftRevision + OperationalJoin.Typed.repairCount events ∧
    D.plant.ruleHistory.length = C.plant.ruleHistory.length + OperationalJoin.Typed.installCount events ∧
    D.plant.draftHistory.length = C.plant.draftHistory.length + OperationalJoin.Typed.repairCount events := by
  obtain ⟨s, commonReach, related⟩ := reachable_witness reach
  obtain ⟨t, expanded, common, laterRelated, sameLandings⟩ :=
    trace_simulation related (reachable_consistent commonReach) trace
  have counters := OperationalJoin.Typed.trace_counters (reachable_consistent commonReach)
    related.safe common
  have installs : OperationalJoin.Typed.installCount expanded = OperationalJoin.Typed.installCount events := by
    rw [installCount_landings, sameLandings, ← installCount_landings]
  have repairs : OperationalJoin.Typed.repairCount expanded = OperationalJoin.Typed.repairCount events := by
    rw [repairCount_landings, sameLandings, ← repairCount_landings]
  simpa only [related.plant, laterRelated.plant, installs, repairs] using counters

theorem fixed_action_excluded {m} {E : Environment (interface m)}
    (p : ComposedExecution.Plant) (policy : ComposedExecution.Policy) (time : Nat)
    (k : BoundedEnvelope m)
    (accepted : ComposedExecution.localStep p policy time k.val.action = some k.val.successor)
    {C D : SharedAlias.State (interface m)} {events : List (Event (interface m))}
    (same : C.plant = k.val.successor) (reach : SharedAlias.Reachable E C)
    (trace : SharedAlias.Trace E C events D) (laterPolicy : ComposedExecution.Policy) (laterTime : Nat) :
    ComposedExecution.localStep D.plant laterPolicy laterTime k.val.action = none := by
  obtain ⟨s, commonReach, related⟩ := reachable_witness reach
  obtain ⟨t, expanded, common, laterRelated, _⟩ :=
    trace_simulation related (reachable_consistent commonReach) trace
  have excluded := OperationalJoin.Typed.fixed_action_excluded_after_continuation
    p policy time k accepted (related.plant.trans same) commonReach common laterPolicy laterTime
  simpa only [laterRelated.plant] using excluded

theorem goals_persist {m} {E : Environment (interface m)}
    {C D : SharedAlias.State (interface m)} {events : List (Event (interface m))}
    (reach : SharedAlias.Reachable E C) (goals : ComposedExecution.Goals C.plant)
    (trace : SharedAlias.Trace E C events D) : ComposedExecution.Goals D.plant := by
  obtain ⟨s, commonReach, related⟩ := reachable_witness reach
  obtain ⟨t, expanded, common, laterRelated, _⟩ :=
    trace_simulation related (reachable_consistent commonReach) trace
  have initialGoals : ComposedExecution.Goals s.plant := by simpa only [related.plant] using goals
  have finalGoals := OperationalJoin.Typed.finite_history_goals_persist commonReach related.safe initialGoals common
  simpa only [laterRelated.plant] using finalGoals

theorem install_full_effect {m} {E : Environment (interface m)}
    {C : SharedAlias.State (interface m)} (reach : SharedAlias.Reachable E C)
    (time : Nat) (k : BoundedEnvelope m) (who : String)
    (admitted : SharedAlias.Lands E C time k who)
    (cmd : CriterionInstallation.InstallCommand) (kind : k.val.action = .install cmd) :
    (SharedAlias.land C k).plant = { C.plant with
      rule := .exact, ruleVersion := C.plant.ruleVersion + 1,
      ruleHistory := C.plant.ruleHistory ++ [C.plant.rule] } := by
  have effect := (finite_history_admission reach time k who admitted).2.2
  rw [kind] at effect
  exact ComposedExecution.local_install_full_effect _ _ _ _ _ effect

theorem repair_full_effect {m} {E : Environment (interface m)}
    {C : SharedAlias.State (interface m)} (reach : SharedAlias.Reachable E C)
    (time : Nat) (k : BoundedEnvelope m) (who : String)
    (admitted : SharedAlias.Lands E C time k who)
    (cmd : TypedCriterionGuard.Command) (kind : k.val.action = .repair cmd) :
    (SharedAlias.land C k).plant = { C.plant with
      draft := C.plant.source.content, draftRevision := C.plant.draftRevision + 1,
      draftHistory := C.plant.draftHistory ++ [C.plant.draft] } := by
  have effect := (finite_history_admission reach time k who admitted).2.2
  rw [kind] at effect
  exact ComposedExecution.local_repair_full_effect _ _ _ _ _ effect

end
end SharedAlias.Typed
