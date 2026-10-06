import ProgressWitness

/-! Independent controls of the new controller bridge. The principal endpoint
is checked against accepted typed trace counters, not a second evaluator. -/
namespace SharedAlias.Progress.IndependentReview
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope)
noncomputable section
open Classical

/-- Arbitrary reply and clock annotations cannot change even one full command
in the actor's program. Map and fault parameters are absent from both sides. -/
theorem service_annotations_do_not_choose_commands {m}
    (actor : ComposedExecution.Actor) (action : ComposedExecution.Action)
    (paths : List (Finset (Fin m))) (times₁ times₂ : Nat → Nat)
    (bad₁ bad₂ : Nat → Replies m) :
    (compile actor action paths times₁ bad₁).map (List.map TrialSpec.command) =
      (compile actor action paths times₂ bad₂).map (List.map TrialSpec.command) := by
  rw [compile_public_program, compile_public_program]

/-- Synchronization does not assume cooperation by a bad actual root. The
false bit denotes an already completed withholding/timeout slot. -/
theorem silent_bad_sync_is_hold {m} {I : Interface m}
    (E : Environment I) (epoch : Nat) (C : SharedAlias.State I) (i : Fin m)
    (bad : ¬ Good E.labelConfig i) :
    syncSlot E epoch (fun _ => false) C i = C := by
  have denied : ¬ (epoch ≠ 0 ∧ (Good E.labelConfig i ∨ (false : Bool) = true)) := by
    intro h
    rcases h.2 with good | impossible
    · exact bad good
    · cases impossible
  exact if_neg denied

/-- A root-wide cancellation at i does not manufacture j's label receipt. -/
theorem cancellation_does_not_fabricate_other_label {m} {I : Interface m}
    (E : Environment I) (C : SharedAlias.State I) (i j : Fin m)
    (k : I.Command) (who : I.Requester) (reply : Bool)
    (different : j ≠ i) (absent : j ∉ C.cancelAcks k) :
    j ∉ (cancelSlot E C i k who reply).cancelAcks k := by
  unfold cancelSlot
  split
  · rw [cancelAck_receipts]
    simpa only [Finset.mem_insert, not_or] using And.intro different absent
  · exact absent

/-- The same slot really writes the shared veto, including at an unresponding
alias. Root coherence and exact label receipt accounting hold together. -/
theorem alias_veto_without_alias_receipt {m} {I : Interface m}
    (E : Environment I) (C : SharedAlias.State I) (i j : Fin m)
    (k : I.Command) (who : I.Requester) (reply : Bool)
    (selected : i ∈ I.commandPath k) (good : Good E.labelConfig i)
    (auth : who = I.recipient k) (same : E.rootOf j = E.rootOf i)
    (different : j ≠ i) (absent : j ∉ C.cancelAcks k) :
    k ∈ ((cancelSlot E C i k who reply).roots (E.rootOf j)).cancelled ∧
      j ∉ (cancelSlot E C i k who reply).cancelAcks k := by
  constructor
  · have allowed : cancelAllowed E i k who reply :=
      ⟨selected, by simpa only [if_pos good] using auth⟩
    rw [cancelSlot, if_pos allowed]
    exact shared_cancel E C i j k same good
  · exact cancellation_does_not_fabricate_other_label E C i j k who reply different absent

/-- The intended one-fault/two-alias specialization really uses lifted k=2,
and the accepted threshold assumptions force r=5 as well as public q=5. -/
theorem seven_pair_one_fault_parameters
    (E : Environment (interface 7)) (budget : E.budget = 1)
    (aliases : E.aliasClass.card = 2) (q : E.q = 5) :
    E.labelBudget = 2 ∧ E.r = 5 ∧ sevenPaths.length = 21 ∧
      (∀ P ∈ sevenPaths, P.card = 5) := by
  have lifted : E.labelBudget = 2 := by
    simp only [Environment.labelBudget, budget, aliases]
  have overlap := E.overlap
  have available := E.revoke_available
  change 7 + E.labelBudget < E.q + E.r at overlap
  change E.r + E.labelBudget ≤ 7 at available
  rw [lifted, q] at overlap
  rw [lifted] at available
  exact ⟨lifted, by omega, sevenPaths_length, sevenPaths_uniform⟩

/-- This is an all-world exact typed effect check. The accepted history
counter theorem independently rules out a second actual installation, even
though the controller does not stop on its first successful reply. -/
theorem all_worlds_exactly_one_installation
    (E : Environment (interface 7)) (q : E.q = 5)
    (source0 : E.source 0 = Witness.Fixture.source 0)
    (badSync : Fin 7 → Bool) (bad : Nat → Replies 7) :
    ∃ specs events,
      compile Witness.actor Witness.action sevenPaths Witness.times bad = some specs ∧
      specs.length = 21 ∧
      SharedAlias.Trace E (SharedAlias.initial E Witness.Fixture.before) events
        (run E (actorSynchronize E Witness.actor badSync
          (SharedAlias.initial E Witness.Fixture.before)) Witness.actor.identity specs) ∧
      events.length = 259 ∧
      OperationalJoin.Typed.installCount events = 1 ∧
      OperationalJoin.Typed.repairCount events = 0 := by
  obtain ⟨specs, events, compiled, count, trace, length, effect⟩ :=
    Witness.uniform_unknown_world_installation E q source0 badSync bad
  have reach : SharedAlias.Reachable E (SharedAlias.initial E Witness.Fixture.before) :=
    ⟨Witness.Fixture.before, [], .nil _⟩
  have counters := SharedAlias.Typed.trace_counters reach trace
  have installLaw := counters.1
  have repairLaw := counters.2.1
  rw [effect] at installLaw repairLaw
  change 4 = 3 + OperationalJoin.Typed.installCount events at installLaw
  change 8 = 8 + OperationalJoin.Typed.repairCount events at repairLaw
  exact ⟨specs, events, compiled, count, trace, length, by omega, by omega⟩

end
end SharedAlias.Progress.IndependentReview

#print axioms SharedAlias.Progress.IndependentReview.service_annotations_do_not_choose_commands
#print axioms SharedAlias.Progress.IndependentReview.silent_bad_sync_is_hold
#print axioms SharedAlias.Progress.IndependentReview.cancellation_does_not_fabricate_other_label
#print axioms SharedAlias.Progress.IndependentReview.alias_veto_without_alias_receipt
#print axioms SharedAlias.Progress.IndependentReview.seven_pair_one_fault_parameters
#print axioms SharedAlias.Progress.IndependentReview.all_worlds_exactly_one_installation
