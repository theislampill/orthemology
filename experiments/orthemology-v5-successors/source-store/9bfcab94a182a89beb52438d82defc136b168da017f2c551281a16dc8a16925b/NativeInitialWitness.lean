import NativeController
import NativePortfolio
import NativeHistory
import ProgressWitness

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface rootView)

/-- A finite supplied service clock. Slot completion is separate from this
logical timestamp contract; each trial uses one shared sample throughout. -/
structure AnnotationClock {m} (observed lo hi : Nat) (annotations : List (Annotation m)) : Prop where
  monotone : annotations.Pairwise (fun a b => a.time ≤ b.time)
  after_observation : ∀ a ∈ annotations, observed ≤ a.time
  in_window : ∀ a ∈ annotations, lo ≤ a.time ∧ a.time ≤ hi

/-- Specialized epoch-zero entry point. It creates the stated initial finite
reference machine, emits m completed hold/sync slots, then all public trials.
It does not implement nonzero delivery or infer missing source authority. -/
def runInitial {m} (D : Routing m) (actor : Actor) (action : Action)
    (paths : List (OrderedPath m)) (annotations : List (Annotation m)) : Option (Outcome m) :=
  if actor.policy.epoch = 0 then
    (compileOrdered actor action paths annotations).map (fun specs =>
      let result := runNative D actor.identity (initial actor.policy actor.observedPlant) specs
      ⟨result.state, List.replicate m .hold ++ result.events⟩)
  else none

namespace Concrete
abbrev before := OperationalJoin.Typed.Examples.before
abbrev installed := OperationalJoin.Typed.Examples.installed
abbrev policy := OperationalJoin.Typed.Examples.source 0
abbrev installCommand := OperationalJoin.Typed.Examples.installCommand

def actor : Actor := ⟨policy, before, "A", 2, 1000⟩
def action : Action := .install installCommand

def commands : List (BoundedEnvelope 7) := orderedCommands actor action installed 0 sevenOrderedPaths

def start : FiniteState 7 := initial policy before

def execute (D : Routing 7) (annotations : List (Annotation 7)) : Option (Outcome 7) :=
  runInitial D actor action sevenOrderedPaths annotations
end Concrete

noncomputable section
open Classical

theorem holds_trace {m} (E : SharedAlias.Environment (interface m))
    (C : SharedAlias.State (interface m)) (n : Nat) :
    SharedAlias.Trace E C (List.replicate n .hold) C := by
  induction n with
  | zero => exact .nil _
  | succ n ih => exact .cons (.hold _) ih

theorem concrete_source_window (time : Nat) (lo : 2 ≤ time) (hi : time ≤ 22) :
    ComposedExecution.localStep Concrete.before Concrete.policy time Concrete.action = some Concrete.installed :=
  SharedAlias.Progress.Witness.install_window time lo hi

theorem concrete_public_program :
    orderedProgram Concrete.actor Concrete.action sevenOrderedPaths = some Concrete.commands := by
  have step := concrete_source_window 2 (by decide) (by decide)
  simp only [orderedProgram, Concrete.actor, Concrete.commands, step, Option.map_some]
  rfl

theorem concrete_commands_length : Concrete.commands.length = 21 := by
  simp only [Concrete.commands, orderedCommands_length, sevenOrderedPaths_length]

theorem concrete_start_view (E : SharedAlias.Environment (interface 7))
    (source0 : E.source 0 = Concrete.policy) :
    view Concrete.start = SharedAlias.initial E Concrete.before := by
  unfold Concrete.start
  rw [← source0]
  exact initial_view E Concrete.before

theorem concrete_command_member (k : BoundedEnvelope 7) (member : k ∈ Concrete.commands) :
    ∃ n p, p ∈ sevenOrderedPaths ∧ k = issueOrdered Concrete.actor Concrete.action Concrete.installed n p := by
  obtain ⟨n, p, _, _, hp, same⟩ := orderedCommands_member Concrete.actor Concrete.action Concrete.installed
    0 sevenOrderedPaths k member
  exact ⟨n, p, hp, same⟩

theorem concrete_command_fields (k : BoundedEnvelope 7) (member : k ∈ Concrete.commands) :
    k.val.action = Concrete.action ∧ k.val.successor = Concrete.installed ∧ k.val.path.length = 5 := by
  obtain ⟨n, p, hp, rfl⟩ := concrete_command_member k member
  exact ⟨rfl, rfl, by simpa only [issueOrdered, orderedLabelList, List.length_map]
    using sevenOrderedPaths_lengths p hp⟩

/-- The all-good command comes from the fixed public list. It does not choose
or rewrite the actor's next command after inspecting the hidden world. -/
theorem concrete_commands_hit (E : SharedAlias.Environment (interface 7)) (q : E.q = 5) :
    ∃ k ∈ Concrete.commands, ∀ i ∈ OperationalJoin.Typed.path k, OperationalJoin.Good E.labelConfig i := by
  obtain ⟨p, hp, good⟩ := sevenOrderedPaths_hit E q
  obtain ⟨k, member, support⟩ := orderedCommands_has_path Concrete.actor Concrete.action Concrete.installed
    0 sevenOrderedPaths p hp
  refine ⟨k, member, ?_⟩
  intro i selected
  exact good i (List.mem_toFinset.mp (by simpa only [support] using selected))

/-- Fixed public source proposal, every accepted hidden shared world, every
complete finite valid service decoration in the source window. Success is a
conclusion, not a trace, landing, or actor-observation premise. -/
theorem concrete_native_initial_progress (D : Routing 7)
    (E : SharedAlias.Environment (interface 7)) (matchD : RoutingMatches D E)
    (q : E.q = 5) (source0 : E.source 0 = Concrete.policy)
    (annotations : List (Annotation 7)) (count : annotations.length = 21)
    (validAnnotations : ∀ a ∈ annotations, annotationValid a = true)
    (clock : AnnotationClock 2 2 22 annotations) :
    ∃ specs result, compileOrdered Concrete.actor Concrete.action sevenOrderedPaths annotations = some specs ∧
      specs.map NativeSpec.command = Concrete.commands ∧ specs.length = 21 ∧
      Concrete.execute D annotations = some result ∧
      SharedAlias.Trace E (SharedAlias.initial E Concrete.before) result.events (view result.state) ∧
      result.events.length = 259 ∧ result.state.plant = Concrete.installed := by
  obtain ⟨specs, annotated⟩ := annotate_complete Concrete.commands annotations
    (count.trans concrete_commands_length.symm) validAnnotations
  have erased := annotate_erases Concrete.commands annotations specs annotated
  have annotationMap := annotate_member_annotation Concrete.commands annotations specs annotated
  have lengthSpecs : specs.length = 21 := by
    have sizes := congrArg List.length erased
    simpa only [List.length_map, concrete_commands_length] using sizes
  have compiled : compileOrdered Concrete.actor Concrete.action sevenOrderedPaths annotations = some specs := by
    simp only [compileOrdered, concrete_public_program]
    exact annotated
  have commandMember : ∀ s ∈ specs, s.command ∈ Concrete.commands := by
    intro s member
    rw [← erased]
    exact List.mem_map.mpr ⟨s, member, rfl⟩
  have annotationMember : ∀ s ∈ specs, s.annotation ∈ annotations := by
    intro s member
    rw [← annotationMap]
    exact List.mem_map.mpr ⟨s, member, rfl⟩
  have progress : (runNative D Concrete.actor.identity Concrete.start specs).state.plant = Concrete.installed := by
    apply runNative_progress D E matchD Concrete.start Concrete.actor.identity specs Concrete.policy Concrete.installed
    · intro s member
      change (OperationalJoin.Typed.path s.command).card = E.q
      rw [OperationalJoin.Typed.path_card, q]
      exact (concrete_command_fields s.command (commandMember s member)).2.2
    · intro s member
      rw [(concrete_command_fields s.command (commandMember s member)).1]
      rfl
    · intro s member
      exact (concrete_command_fields s.command (commandMember s member)).2.1
    · exact annotate_pairwise Concrete.commands annotations specs annotated
        (orderedCommands_fresh Concrete.actor Concrete.action Concrete.installed 0 sevenOrderedPaths)
    · intro s member i good
      exact ⟨rfl, by simp [view, Concrete.start, initial, rootAt, tableRead, rootView],
        by
          change s.command ∉ OperationalJoin.Typed.memory []
          intro member
          have absent : s.command.val ∈ ([] : List ComposedExecution.Envelope) :=
            (OperationalJoin.Typed.mem_memory [] s.command).mp member
          exact List.not_mem_nil absent⟩
    · intro s member
      obtain ⟨lo, hi⟩ := clock.in_window s.annotation (annotationMember s member)
      obtain ⟨action, successor, _⟩ := concrete_command_fields s.command (commandMember s member)
      simpa only [action, successor, Concrete.start, initial] using concrete_source_window s.annotation.time lo hi
    · obtain ⟨k, member, good⟩ := concrete_commands_hit E q
      rw [← erased] at member
      obtain ⟨s, hs, same⟩ := List.mem_map.mp member
      exact ⟨s, hs, by simpa only [same] using good⟩
  let result : Outcome 7 :=
    ⟨(runNative D Concrete.actor.identity Concrete.start specs).state,
      List.replicate 7 .hold ++ (runNative D Concrete.actor.identity Concrete.start specs).events⟩
  refine ⟨specs, result, compiled, erased, lengthSpecs, ?_, ?_, ?_, progress⟩
  · simp only [Concrete.execute, runInitial]
    rw [if_pos (show Concrete.actor.policy.epoch = 0 from rfl), compiled]
    rfl
  · have trace := runNative_trace D E matchD Concrete.start Concrete.actor.identity specs
    rw [concrete_start_view E source0] at trace
    exact SharedAlias.Progress.trace_append (holds_trace E _ 7) trace
  · have size := runNative_length D Concrete.start Concrete.actor.identity specs 5
      (fun s member => (concrete_command_fields s.command (commandMember s member)).2.2)
    simp only [result, List.length_append, List.length_replicate, size, lengthSpecs]

end
end SharedAlias.Native
