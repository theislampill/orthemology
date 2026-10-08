import NativeUniformEffect
import NativeExecutionControls
namespace IndependentOrderedContractReview
open SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)

theorem missing_all_annotations_rejects : annotate Concrete.commands [] = none := by
  apply annotate_mismatch_rejects
  rw [concrete_commands_length]
  decide

theorem exact_reference_state_signature {m} (D : Routing m)
    (E : SharedAlias.Environment (interface m)) (h : RoutingMatches D E)
    (C : FiniteState m) (who : String) (specs : List (NativeSpec m)) :
    view (runNative D who C specs).state =
      SharedAlias.Progress.run E (view C) who (specs.map modelSpec) :=
  runNative_exact D E h C who specs

theorem actual_emitted_trace_signature {m} (D : Routing m)
    (E : SharedAlias.Environment (interface m)) (h : RoutingMatches D E)
    (C : FiniteState m) (who : String) (specs : List (NativeSpec m)) :
    SharedAlias.Trace E (view C) (runNative D who C specs).events
      (view (runNative D who C specs).state) := runNative_trace D E h C who specs

/-- No clock, annotation, state or hidden world may change the fixed commands. -/
theorem exact_annotation_erasure (annotations : List (Annotation 7))
    (specs : List (NativeSpec 7))
    (h : compileOrdered Concrete.actor Concrete.action sevenOrderedPaths annotations = some specs) :
    specs.map NativeSpec.command = Concrete.commands := by
  have frozen := compileOrdered_public_program Concrete.actor Concrete.action sevenOrderedPaths annotations specs h
  rw [concrete_public_program] at frozen
  exact (Option.some.inj frozen).symm

#print axioms missing_all_annotations_rejects
#print axioms exact_reference_state_signature
#print axioms actual_emitted_trace_signature
#print axioms exact_annotation_erasure
end IndependentOrderedContractReview
