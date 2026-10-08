import ProgressWitness

namespace SharedAlias.Progress
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path mem_path)
noncomputable section
open Classical

/-- A withholding faulty gate rejects the unchanged source attempt on every
path containing that label, independently of the hidden store's contents. -/
theorem bad_path_rejected {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String)
    (time : Nat) (i : Fin m) (selected : i ∈ path k) (bad : i ∈ E.labelConfig.faulty) :
    applied E C k who time false = false := by
  cases success : applied E C k who time false with
  | false => rfl
  | true =>
      have opens := ComposedExecution.attempt_applied_implies_lands
        (SharedAlias.Typed.gateWorld E C time) k.val who false success
      have opened := opens i.val i.isLt (by
        exact decide_eq_true ((mem_path k i).mp selected))
      have actual : E.rootOf i ∈ E.actualFaults := by
        by_contra clean
        exact ((good_iff E i).mpr clean) bad
      simp [ComposedExecution.gateOpen, SharedAlias.Typed.gateWorld, i.isLt, actual] at opened

theorem bad_trial_plant {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k : BoundedEnvelope m) (who : String)
    (time : Nat) (replies : Replies m) (withhold : replies.openGate = false)
    (blocked : ∃ i ∈ path k, i ∈ E.labelConfig.faulty) :
    (trial E C k who time replies).plant = C.plant := by
  obtain ⟨i, selected, bad⟩ := blocked
  have rejected := bad_path_rejected E (preparePath E C k who time replies.prepare) k who time i selected bad
  simp only [trial, cancelPath_plant, attemptSlot, withhold, rejected, Bool.false_eq_true, if_false,
    preparePath_plant]

theorem blocked_run_plant {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (who : String) (specs : List (TrialSpec m))
    (withhold : ∀ s ∈ specs, s.replies.openGate = false)
    (blocked : ∀ s ∈ specs, ∃ i ∈ path s.command, i ∈ E.labelConfig.faulty) :
    (run E C who specs).plant = C.plant := by
  induction specs generalizing C with
  | nil => rfl
  | cons s specs ih =>
      calc
        (run E C who (s :: specs)).plant =
            (trial E C s.command who s.time s.replies).plant :=
          ih _ (fun x hx => withhold x (List.mem_cons_of_mem s hx))
            (fun x hx => blocked x (List.mem_cons_of_mem s hx))
        _ = C.plant := bad_trial_plant E C s.command who s.time s.replies
          (withhold s (by simp)) (blocked s (by simp))

theorem scheduled_const_replies {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (times : Nat → Nat) (reply : Replies m) (n : Nat) (paths : List (Finset (Fin m)))
    (s : TrialSpec m) (member : s ∈ scheduled actor action next times (fun _ => reply) n paths) :
    s.replies = reply := by
  induction paths generalizing n with
  | nil => simp [scheduled] at member
  | cons P paths ih =>
      simp only [scheduled, List.mem_cons] at member
      rcases member with rfl | later
      · rfl
      · exact ih (n + 1) later

theorem scheduled_take {m} (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (times : Nat → Nat) (bad : Nat → Replies m) (n count : Nat) (paths : List (Finset (Fin m))) :
    scheduled actor action next times bad n (paths.take count) =
      (scheduled actor action next times bad n paths).take count := by
  induction paths generalizing n count with
  | nil => simp [scheduled]
  | cons P paths ih =>
      cases count with
      | zero => simp [scheduled]
      | succ count => simp only [List.take_succ_cons, scheduled, ih]

namespace Witness
/-- Fixed before any service replies; the actual faulty root is the unknown
shared class itself. This is the worst case for this one public path order. -/
def worstWorld : Environment (interface 7) where
  aliasClass := {0,1}
  class_positive := by decide
  budget := 1
  budget_positive := by decide
  actualFaults := {none}
  actual_faults := by decide
  actual_budget := by decide
  non_saturated := by decide
  q := 5
  r := 5
  overlap := by decide
  repair_available := by decide
  revoke_available := by decide
  source := Fixture.source
  source_epoch := by intro e; rfl

theorem worst_world_counts :
    worstWorld.aliasClass.card = 2 ∧
    (AttributionKernel.actualRoots worstWorld.aliasClass).card = 6 ∧
    worstWorld.actualFaults.card = 1 ∧ worstWorld.labelBudget = 2 := by decide

def withholding : Replies 7 :=
  ⟨fun _ => true, false, fun _ => true⟩

set_option maxRecDepth 8192 in
theorem first_twenty_hit_fault : ∀ P ∈ sevenPaths.take 20, ∃ i ∈ P, i ∈ worstWorld.labelConfig.faulty := by
  decide

theorem first_twenty_no_progress (respond : Fin 7 → Bool) :
    (run worstWorld
      (actorSynchronize worstWorld actor respond (SharedAlias.initial worstWorld Fixture.before))
      actor.identity (scheduled actor action Fixture.installed times (fun _ => withholding) 0 (sevenPaths.take 20))).plant =
        Fixture.before := by
  rw [blocked_run_plant]
  · rw [actorSynchronize_eq worstWorld actor respond _ rfl, synchronize_plant]
    rfl
  · intro s member
    rw [scheduled_const_replies actor action Fixture.installed times withholding 0 (sevenPaths.take 20) s member]
    rfl
  · intro s member
    obtain ⟨n, P, _, _, hP, command, _⟩ :=
      scheduled_member actor action Fixture.installed times (fun _ => withholding) 0 (sevenPaths.take 20) s member
    rw [command, issue_path]
    exact first_twenty_hit_fault P hP


theorem first_twenty_actual_program (respond : Fin 7 → Bool) :
    (run worstWorld
      (actorSynchronize worstWorld actor respond (SharedAlias.initial worstWorld Fixture.before))
      actor.identity ((scheduled actor action Fixture.installed times (fun _ => withholding) 0 sevenPaths).take 20)).plant =
        Fixture.before := by
  rw [← scheduled_take]
  exact first_twenty_no_progress respond

/-- Position is proved for the actual explicit delivered list, not assumed
from an implementation-dependent powerset/toList ordering. -/
theorem last_path_position :
    sevenPaths = sevenPaths.take 20 ++ [{2,3,4,5,6}] ∧
      (sevenPaths.take 20).length = 20 := by decide

theorem before_ne_installed : Fixture.before ≠ Fixture.installed := by decide

/-- Sharpness only for this exact public order and fixed shared world. The
first twenty attempts make no plant progress; running all twenty-one does.
This is not a lower bound on other controllers or an opacity theorem. -/
theorem twenty_one_attained (respond : Fin 7 → Bool) :
    (run worstWorld
      (actorSynchronize worstWorld actor respond (SharedAlias.initial worstWorld Fixture.before))
      actor.identity ((scheduled actor action Fixture.installed times (fun _ => withholding) 0 sevenPaths).take 20)).plant ≠
        Fixture.installed ∧
    ∃ events, SharedAlias.Trace worstWorld (SharedAlias.initial worstWorld Fixture.before) events
      (run worstWorld
        (actorSynchronize worstWorld actor respond (SharedAlias.initial worstWorld Fixture.before)) actor.identity
        (scheduled actor action Fixture.installed times (fun _ => withholding) 0 sevenPaths)) ∧
      events.length = 259 ∧
      (run worstWorld
        (actorSynchronize worstWorld actor respond (SharedAlias.initial worstWorld Fixture.before)) actor.identity
        (scheduled actor action Fixture.installed times (fun _ => withholding) 0 sevenPaths)).plant = Fixture.installed := by
  refine ⟨by rw [first_twenty_actual_program]; exact before_ne_installed, ?_⟩
  obtain ⟨specs, events, compiled, count, trace, size, done⟩ :=
    uniform_unknown_world_installation worstWorld rfl rfl respond (fun _ => withholding)
  have proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some Fixture.installed :=
    install_window 2 (by decide) (by decide)
  rw [compile_eq actor action Fixture.installed sevenPaths times (fun _ => withholding) proposal] at compiled
  have same := (Option.some.inj compiled).symm
  subst specs
  exact ⟨events, trace, size, done⟩

end Witness
end
end SharedAlias.Progress
