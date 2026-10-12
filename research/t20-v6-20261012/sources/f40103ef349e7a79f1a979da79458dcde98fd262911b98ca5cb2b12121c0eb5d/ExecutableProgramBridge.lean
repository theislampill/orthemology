import ExecutableBridge

namespace SharedAlias.Executable.Bridge
open ComposedExecution

theorem issueOrdered_exact {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (path : OrderedPath m) :
    issueOrdered actor action next n path = Native.issueOrdered actor action next n path := by
  apply Subtype.ext
  rfl

theorem orderedCommands_exact {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (paths : List (OrderedPath m)) :
    orderedCommands actor action next n paths = Native.orderedCommands actor action next n paths := by
  induction paths generalizing n with
  | nil => rfl
  | cons path paths ih => simp only [orderedCommands, Native.orderedCommands, issueOrdered_exact, ih]

theorem orderedProgram_exact {m} (actor : Actor) (action : Action) (paths : List (OrderedPath m)) :
    orderedProgram actor action paths = Native.orderedProgram actor action paths := by
  unfold orderedProgram Native.orderedProgram
  congr 1
  funext next
  exact orderedCommands_exact actor action next 0 paths

theorem annotationValid_exact {m} (a : Annotation m) :
    annotationValid a = Native.annotationValid (annotationView a) := rfl

theorem annotate_exact {m} (commands : List (Command m)) (annotations : List (Annotation m)) :
    (annotate commands annotations).map (List.map specView) =
      Native.annotate commands (annotations.map annotationView) := by
  induction commands generalizing annotations with
  | nil => cases annotations <;> rfl
  | cons k commands ih =>
      cases annotations with
      | nil => rfl
      | cons a annotations =>
          simp only [annotate, Native.annotate, List.map_cons, ← annotationValid_exact]
          split
          · have later := ih annotations
            cases h : annotate commands annotations with
            | none =>
                have native : Native.annotate commands (annotations.map annotationView) = none := by
                  rw [← later, h]; rfl
                rw [h, native]
                rfl
            | some specs =>
                have native : Native.annotate commands (annotations.map annotationView) = some (specs.map specView) := by
                  rw [← later, h]; rfl
                rw [h, native]
                rfl
          · rfl

theorem compileOrdered_exact {m} (actor : Actor) (action : Action) (paths : List (OrderedPath m))
    (annotations : List (Annotation m)) :
    (compileOrdered actor action paths annotations).map (List.map specView) =
      Native.compileOrdered actor action paths (annotations.map annotationView) := by
  unfold compileOrdered Native.compileOrdered
  rw [← orderedProgram_exact]
  cases h : orderedProgram actor action paths with
  | none => rfl
  | some commands => exact annotate_exact commands annotations

/-- The initial prefix has an explicit event correspondence, rather than
inheriting trace equality from final-state equality. -/
theorem prefixedRun_exact {m} (D : Routing m) (actor : Actor) (specs : List (Spec m)) :
    outcomeView
      (let result := runNative D actor.identity (initial actor.policy actor.observedPlant) specs
       (⟨result.state, List.replicate m .hold ++ result.events⟩ : Outcome m)) =
      (let result := Native.runNative (routingView D) actor.identity
        (Native.initial actor.policy actor.observedPlant) (specs.map specView)
       (⟨result.state, List.replicate m .hold ++ result.events⟩ : Native.Outcome m)) := by
  have run := runNative_exact D actor.identity (initial actor.policy actor.observedPlant) specs
  have states := congrArg Native.Outcome.state run
  have events := congrArg Native.Outcome.events run
  simp only [outcomeView, initial_exact] at states events
  simp only [outcomeView, List.map_append, List.map_replicate, eventView, states, events]

/-- Exact checked entry correspondence, including both success and rejection,
all raw state fields, and the mapped actual event list. -/
theorem runInitial_exact {m} (D : Routing m) (actor : Actor) (action : Action)
    (paths : List (OrderedPath m)) (annotations : List (Annotation m)) :
    (runInitial D actor action paths annotations).map outcomeView =
      Native.runInitial (routingView D) actor action paths (annotations.map annotationView) := by
  unfold runInitial Native.runInitial
  by_cases zero : actor.policy.epoch = 0
  · simp only [if_pos zero]
    have compiled := compileOrdered_exact actor action paths annotations
    cases h : compileOrdered actor action paths annotations with
    | none =>
        have native : Native.compileOrdered actor action paths (annotations.map annotationView) = none := by
          rw [← compiled, h]; rfl
        rw [h, native]
        rfl
    | some specs =>
        have native : Native.compileOrdered actor action paths (annotations.map annotationView) = some (specs.map specView) := by
          rw [← compiled, h]; rfl
        rw [h, native]
        exact congrArg some (prefixedRun_exact D actor specs)
  · simp only [if_neg zero]
    rfl

end SharedAlias.Executable.Bridge
