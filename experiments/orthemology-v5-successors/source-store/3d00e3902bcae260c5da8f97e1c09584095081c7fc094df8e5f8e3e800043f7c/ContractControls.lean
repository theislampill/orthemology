import AliasModel

/-! Independent progress-contract controls over the unchanged accepted shared
root relation. These are obstructions, not defects in its safety claims. -/
namespace SharedAlias.ProgressContractReview
open OperationalJoin
noncomputable section
open Classical

theorem arbitrarily_long_holds {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (n : Nat) :
    SharedAlias.Trace E C (List.replicate n .hold) C := by
  induction n with
  | zero => exact .nil C
  | succ n ih =>
      simpa only [List.replicate_succ] using
        SharedAlias.Trace.cons (SharedAlias.Step.hold (E := E) C) ih

/-- No finite event-count guarantee follows from Step alone, even with a
fixed environment, unchanged plant, unchanged epoch, and no bad-root action. -/
theorem no_unconditional_bounded_progress {m} {I : Interface m}
    (E : Environment I) (C : SharedAlias.State I) (goal : I.Plant → Prop)
    (not_done : ¬ goal C.plant) (n : Nat) :
    ∃ events D, events.length = n ∧ SharedAlias.Trace E C events D ∧
      D.epoch = C.epoch ∧ D.plant = C.plant ∧ ¬ goal D.plant := by
  exact ⟨List.replicate n .hold, C, by simp,
    arbitrarily_long_holds E C n, rfl, rfl, not_done⟩

/-- The constant infinite run also refutes universal eventual progress. -/
theorem constant_infinite_failure {m} {I : Interface m}
    (E : Environment I) (C : SharedAlias.State I) (goal : I.Plant → Prop)
    (not_done : ¬ goal C.plant) :
    ∃ run : Nat → SharedAlias.State I,
      (∀ t, SharedAlias.Step E (run t) .hold (run (t + 1))) ∧
      (∀ t, ¬ goal (run t).plant) :=
  ⟨fun _ => C, fun _ => .hold C, fun _ => not_done⟩

/-- Even an execution with a specified eventual successful continuation can
have an arbitrary finite stutter prefix. The transition model cannot turn an
eventual-service premise into a uniform finite delay bound. -/
theorem arbitrary_delay_before_any_trace {m} {I : Interface m}
    (E : Environment I) {C D : SharedAlias.State I}
    {events : List (Event I)} (trace : SharedAlias.Trace E C events D) (n : Nat) :
    SharedAlias.Trace E C (List.replicate n .hold ++ events) D := by
  induction n with
  | zero => simpa only [List.replicate_zero, List.nil_append] using trace
  | succ n ih =>
      simpa only [List.replicate_succ, List.cons_append] using
        SharedAlias.Trace.cons (SharedAlias.Step.hold (E := E) C) ih

def pendingVeto {m} {I : Interface m} (E : Environment I) (p : I.Plant)
    (i : Fin m) : SharedAlias.State I :=
  acknowledge E (request (initial E p)) i

theorem pending_veto_trace {m} {I : Interface m} (E : Environment I)
    (p : I.Plant) (i : Fin m) :
    SharedAlias.Trace E (initial E p) [.request, .acknowledge i]
      (pendingVeto E p i) :=
  .cons (.request _ rfl) (.cons (.acknowledge _ i rfl) (.nil _))

theorem pending_veto_same_epoch_plant {m} {I : Interface m}
    (E : Environment I) (p : I.Plant) (i : Fin m) :
    (pendingVeto E p i).epoch = 0 ∧
      (pendingVeto E p i).plant = p ∧
      (pendingVeto E p i).pending = true := by
  exact ⟨rfl, rfl, rfl⟩

/-- Keeping the epoch fixed is weaker than keeping authorization unrevoked.
A genuine pending acknowledgement creates a veto before epoch completion. -/
theorem pending_veto_blocks_current_command {m} {I : Interface m}
    (E : Environment I) (p : I.Plant) (i : Fin m) (k : I.Command)
    (who : I.Requester) (time : Nat) (good : Good E.labelConfig i)
    (selected : i ∈ I.commandPath k) (current : I.commandEpoch k = 0) :
    ¬ SharedAlias.Lands E (pendingVeto E p i) time k who := by
  intro admitted
  have permits := admitted.2 i selected good
  have revoked : I.commandEpoch k ∈
      ((pendingVeto E p i).roots (E.rootOf i)).revoked := by
    simp only [pendingVeto, acknowledge, if_pos good, Function.update_self]
    simp [request, initial, current]
  exact permits.2.2.1 revoked

/-- The newly created veto belongs to the actual store and therefore applies
to any selected alias, even when that alias did not issue the receipt. -/
theorem pending_veto_blocks_unacknowledged_alias {m} {I : Interface m}
    (E : Environment I) (p : I.Plant) (i j : Fin m) (k : I.Command)
    (who : I.Requester) (time : Nat) (good : Good E.labelConfig i)
    (same : E.rootOf j = E.rootOf i) (selected : j ∈ I.commandPath k)
    (current : I.commandEpoch k = 0) :
    ¬ SharedAlias.Lands E (pendingVeto E p i) time k who := by
  intro admitted
  have jgood : Good E.labelConfig j := (good_same_root E j i same).mpr good
  have permits := admitted.2 j selected jgood
  have revoked : I.commandEpoch k ∈
      ((pendingVeto E p i).roots (E.rootOf j)).revoked := by
    simp only [pendingVeto, acknowledge, if_pos good, same, Function.update_self]
    simp [request, initial, current]
  exact permits.2.2.1 revoked

end
end SharedAlias.ProgressContractReview

#print axioms SharedAlias.ProgressContractReview.arbitrarily_long_holds
#print axioms SharedAlias.ProgressContractReview.no_unconditional_bounded_progress
#print axioms SharedAlias.ProgressContractReview.constant_infinite_failure
#print axioms SharedAlias.ProgressContractReview.arbitrary_delay_before_any_trace
#print axioms SharedAlias.ProgressContractReview.pending_veto_trace
#print axioms SharedAlias.ProgressContractReview.pending_veto_same_epoch_plant
#print axioms SharedAlias.ProgressContractReview.pending_veto_blocks_current_command
#print axioms SharedAlias.ProgressContractReview.pending_veto_blocks_unacknowledged_alias
