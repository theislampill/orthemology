import NativeInitialWitness

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)
noncomputable section
open Classical

/-- Complete effect counters follow from the ACTUAL emitted accepted trace
and exact full Plant, not from synthetic trial-log success bits. -/
theorem concrete_native_initial_effects (D : Routing 7)
    (E : SharedAlias.Environment (interface 7)) (matchD : RoutingMatches D E)
    (q : E.q = 5) (source0 : E.source 0 = Concrete.policy)
    (annotations : List (Annotation 7)) (count : annotations.length = 21)
    (validAnnotations : ∀ a ∈ annotations, annotationValid a = true)
    (clock : AnnotationClock 2 2 22 annotations) :
    ∃ specs result, compileOrdered Concrete.actor Concrete.action sevenOrderedPaths annotations = some specs ∧
      specs.map NativeSpec.command = Concrete.commands ∧ specs.length = 21 ∧
      Concrete.execute D annotations = some result ∧
      SharedAlias.Trace E (SharedAlias.initial E Concrete.before) result.events (view result.state) ∧
      result.events.length = 259 ∧ result.state.plant = Concrete.installed ∧
      OperationalJoin.Typed.installCount result.events = 1 ∧
      OperationalJoin.Typed.repairCount result.events = 0 := by
  obtain ⟨specs, result, compiled, erased, trials, executed, trace, size, plant⟩ :=
    concrete_native_initial_progress D E matchD q source0 annotations count validAnnotations clock
  have reach : SharedAlias.Reachable E (SharedAlias.initial E Concrete.before) :=
    ⟨Concrete.before, [], .nil _⟩
  have counters := SharedAlias.Typed.trace_counters reach trace
  have install : OperationalJoin.Typed.installCount result.events = 1 := by
    have h := counters.1
    change result.state.plant.ruleVersion = Concrete.before.ruleVersion + _ at h
    rw [plant] at h
    change 4 = 3 + _ at h
    omega
  have repair : OperationalJoin.Typed.repairCount result.events = 0 := by
    have h := counters.2.1
    change result.state.plant.draftRevision = Concrete.before.draftRevision + _ at h
    rw [plant] at h
    change 8 = 8 + _ at h
    omega
  exact ⟨specs, result, compiled, erased, trials, executed, trace, size, plant, install, repair⟩

/-- Quantifier order is explicit: ONE complete public command program is
fixed before every accepted hidden world, finite reification and service
schedule. The actor never obtains rootOf/faultyRoots through this API. -/
theorem uniform_unknown_world_native_program :
    ∃ publicCommands : List (BoundedEnvelope 7),
      orderedProgram Concrete.actor Concrete.action sevenOrderedPaths = some publicCommands ∧
      publicCommands.length = 21 ∧
      ∀ (E : SharedAlias.Environment (interface 7)) (D : Routing 7),
        RoutingMatches D E → E.q = 5 → E.source 0 = Concrete.policy →
        ∀ annotations : List (Annotation 7), annotations.length = 21 →
          (∀ a ∈ annotations, annotationValid a = true) → AnnotationClock 2 2 22 annotations →
          ∃ specs result,
            compileOrdered Concrete.actor Concrete.action sevenOrderedPaths annotations = some specs ∧
            specs.map NativeSpec.command = publicCommands ∧
            Concrete.execute D annotations = some result ∧
            SharedAlias.Trace E (SharedAlias.initial E Concrete.before) result.events (view result.state) ∧
            result.events.length = 259 ∧ result.state.plant = Concrete.installed ∧
            OperationalJoin.Typed.installCount result.events = 1 ∧
            OperationalJoin.Typed.repairCount result.events = 0 := by
  refine ⟨Concrete.commands, concrete_public_program, concrete_commands_length, ?_⟩
  intro E D matchD q source0 annotations count valid clock
  obtain ⟨specs, result, compiled, erased, _, executed, trace, size, plant, installs, repairs⟩ :=
    concrete_native_initial_effects D E matchD q source0 annotations count valid clock
  exact ⟨specs, result, compiled, erased, executed, trace, size, plant, installs, repairs⟩

end
end SharedAlias.Native
