import NativeExecutionData
import NativeUniformEffect

namespace SharedAlias.Native
open ComposedExecution

/-- Closed finite counts follow structurally, with no unfolding of the full
259-step state through a giant kernel decide expression. -/
theorem withholding_length : Executed.withholding.length = 21 := by
  simp [Executed.withholding]

theorem withholding_valid : ∀ a ∈ Executed.withholding, annotationValid a = true := by
  intro a member
  obtain ⟨n, _, rfl⟩ := List.mem_map.mp member
  simp [annotationValid]

theorem withholding_clock : AnnotationClock 2 2 22 Executed.withholding := by
  refine ⟨?_, ?_, ?_⟩
  · apply List.pairwise_map.mpr
    exact (List.pairwise_le_range (n := 21)).imp (by intro a b lower; dsimp; omega)
  · intro a member
    obtain ⟨n, _, rfl⟩ := List.mem_map.mp member
    dsimp
    omega
  · intro a member
    obtain ⟨n, hn, rfl⟩ := List.mem_map.mp member
    have bound := List.mem_range.mp hn
    dsimp
    omega

theorem worst_routing_matches : RoutingMatches Executed.worstRouting SharedAlias.Progress.Witness.worstWorld := by
  constructor <;> decide

/-- Apply the universal verified refinement to the ACTUAL executable values;
Option extraction is justified by successful compilation, never by a fallback. -/
theorem executed_trace_bundle :
    compileOrdered Concrete.actor Concrete.action sevenOrderedPaths Executed.withholding = some Executed.specs ∧
    Executed.specs.length = 21 ∧ Concrete.execute Executed.worstRouting Executed.withholding = some Executed.full ∧
    SharedAlias.Trace SharedAlias.Progress.Witness.worstWorld
      (SharedAlias.initial SharedAlias.Progress.Witness.worstWorld Concrete.before)
      Executed.full.events (view Executed.full.state) ∧
    Executed.full.events.length = 259 ∧ Executed.full.state.plant = Concrete.installed ∧
    OperationalJoin.Typed.installCount Executed.full.events = 1 ∧
    OperationalJoin.Typed.repairCount Executed.full.events = 0 := by
  obtain ⟨specs, result, compiled, _, length, executed, trace, count, plant, installs, repairs⟩ :=
    concrete_native_initial_effects Executed.worstRouting SharedAlias.Progress.Witness.worstWorld
      worst_routing_matches rfl rfl Executed.withholding withholding_length withholding_valid withholding_clock
  have specsEq : Executed.specs = specs := by
    unfold Executed.specs
    rw [compiled]
    rfl
  have resultEq : Executed.full = result := by
    unfold Executed.full
    rw [executed]
    rfl
  rw [specsEq, resultEq]
  exact ⟨compiled, length, executed, trace, count, plant, installs, repairs⟩

theorem executed_complete_plant : Executed.full.state.plant = Concrete.installed :=
  executed_trace_bundle.2.2.2.2.2.1

theorem executed_exact_effect_counters :
    OperationalJoin.Typed.installCount Executed.full.events = 1 ∧
    OperationalJoin.Typed.repairCount Executed.full.events = 0 :=
  executed_trace_bundle.2.2.2.2.2.2

theorem executed_no_source_or_draft_mutation :
    Executed.full.state.plant.source = Concrete.before.source ∧
    Executed.full.state.plant.destination = Concrete.before.destination ∧
    Executed.full.state.plant.standard = Concrete.before.standard ∧
    Executed.full.state.plant.unrelated = Concrete.before.unrelated ∧
    Executed.full.state.plant.draft = Concrete.before.draft ∧
    Executed.full.state.plant.draftRevision = Concrete.before.draftRevision ∧
    Executed.full.state.plant.draftHistory = Concrete.before.draftHistory := by
  rw [executed_complete_plant]
  exact ⟨rfl,rfl,rfl,rfl,rfl,rfl,rfl⟩

end SharedAlias.Native
