import ControllerWorstCase

namespace SharedAlias.Progress.IndependentSharpnessReview
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path)
noncomputable section
open Classical

/-- The actual worst-case prefix has no concealed successful effect. Its
accepted event trace has seven prelude slots plus twenty twelve-slot trials;
accepted counters are both zero, independently of endpoint-only wording. -/
theorem first_twenty_exact_zero_effect_trace (respond : Fin 7 → Bool) :
    ∃ events,
      SharedAlias.Trace Witness.worstWorld
        (SharedAlias.initial Witness.worstWorld Witness.Fixture.before) events
        (run Witness.worstWorld
          (actorSynchronize Witness.worstWorld Witness.actor respond
            (SharedAlias.initial Witness.worstWorld Witness.Fixture.before))
          Witness.actor.identity
          (scheduled Witness.actor Witness.action Witness.Fixture.installed
            Witness.times (fun _ => Witness.withholding) 0 (sevenPaths.take 20))) ∧
      events.length = 247 ∧ OperationalJoin.Typed.installCount events = 0 ∧
      OperationalJoin.Typed.repairCount events = 0 := by
  let E := Witness.worstWorld
  let C := SharedAlias.initial E Witness.Fixture.before
  let D := actorSynchronize E Witness.actor respond C
  let specs := scheduled Witness.actor Witness.action Witness.Fixture.installed
    Witness.times (fun _ => Witness.withholding) 0 (sevenPaths.take 20)
  have valid : ∀ s ∈ specs, ValidPath E.labelConfig s.command := by
    intro s member
    obtain ⟨n, P, _, _, hP, cmd, _⟩ := scheduled_member Witness.actor Witness.action
      Witness.Fixture.installed Witness.times (fun _ => Witness.withholding)
      0 (sevenPaths.take 20) s member
    change (path s.command).card = 5
    rw [cmd, issue_path]
    exact sevenPaths_uniform P (List.mem_of_mem_take hP)
  have auth : ∀ s ∈ specs, Witness.actor.identity = s.command.val.action.actor := by
    intro s member
    obtain ⟨n, P, _, _, _, cmd, _⟩ := scheduled_member Witness.actor Witness.action
      Witness.Fixture.installed Witness.times (fun _ => Witness.withholding)
      0 (sevenPaths.take 20) s member
    rw [cmd]
    rfl
  obtain ⟨prelude, preludeTrace, preludeSize⟩ := synchronize_trace E respond C
  have prelude : SharedAlias.Trace E C prelude D := by
    simpa only [D, actorSynchronize_eq E Witness.actor respond C (by rfl)] using preludeTrace
  obtain ⟨batch, batchTrace, batchSize⟩ := run_trace E D Witness.actor.identity specs valid auth
  have joined := trace_append prelude batchTrace
  have reach : SharedAlias.Reachable E C := ⟨Witness.Fixture.before, [], .nil _⟩
  have counters := SharedAlias.Typed.trace_counters reach joined
  have effect : (run E D Witness.actor.identity specs).plant = Witness.Fixture.before :=
    Witness.first_twenty_no_progress respond
  have installLaw := counters.1
  have repairLaw := counters.2.1
  rw [effect] at installLaw repairLaw
  change 3 = 3 + OperationalJoin.Typed.installCount _ at installLaw
  change 8 = 8 + OperationalJoin.Typed.repairCount _ at repairLaw
  refine ⟨_, joined, ?_, by omega, by omega⟩
  rw [List.length_append, preludeSize, batchSize]
  simp only [specs, scheduled_length, Witness.last_path_position.2]
  rfl

end
end SharedAlias.Progress.IndependentSharpnessReview

#print axioms SharedAlias.Progress.IndependentSharpnessReview.first_twenty_exact_zero_effect_trace
