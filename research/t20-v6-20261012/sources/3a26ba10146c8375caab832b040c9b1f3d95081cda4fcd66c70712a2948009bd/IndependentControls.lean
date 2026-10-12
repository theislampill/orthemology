import ProjectionBoundary
import Lean

namespace P01AC.ExtensionalRepair.InternalGraph.Review
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair.CompilerBodyControl
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

-- A raw-coordinate check: even after proof erasure, the step keeps f x.
theorem j_erases (d y e : Poly) : P01DF.PolyConv (jPoly d y e) d :=
  (P01DF.PolyConv.app (.k (.app (.atom .k) d) y) (.refl e)).trans (.k d e)

theorem step_evidence_erases (f a z : Poly) :
    P01DF.PolyConv (stepProof f a z) (.atom .i) :=
  (j_erases _ _ _).trans (j_erases _ _ _)

theorem step_retains_scalar (f a z : Poly) :
    P01DF.PolyConv (stepBody f a z)
      (pairPoly (.app diagonalStep (fstPoly z))
        (pairPoly (.app f (fstPoly (sndPoly z))) (.atom .i))) := by
  simp only [stepBody, pairPoly]
  repeat first | apply P01DF.PolyConv.app | exact P01DF.PolyConv.refl _
  exact step_evidence_erases _ _ _

-- Open f and a remain in scope after adding a genuinely dependent graph binder.
def nestedContext : Tel := Graph (.var 1) (.var 0) :: scalarContext

theorem nested_context : Ctx nestedContext :=
  .ext scalar_context_formed (graph_form scalar_context_formed f_has a_has)

theorem nested_graph_variable :
    Has nestedContext (.var 0) (Graph (.var 2) (.var 1)) := by
  have h := graph_form scalar_context_formed f_has a_has
  have hw : wk (Graph (.var 1) (.var 0)) = Graph (.var 2) (.var 1) := graph_wk _ _
  rw [← hw]
  exact .var (form_wk h scalar_context_formed h) .zero

theorem nested_actual_step :
    Has nestedContext (stepBody (.var 2) (.var 1) (.var 0))
      (Graph (.var 2) (.var 1)) := by
  have h := graph_form scalar_context_formed f_has a_has
  exact strong_step_body_has nested_context
    (has_wk f_has scalar_context_formed h)
    (has_wk a_has scalar_context_formed h) nested_graph_variable

-- The base numeral has both expected projections by actual raw computation.
theorem zero_iterates (f a : Poly) :
    P01DF.PolyConv (.app (.app (inputNumeral 0) f) a) a := by
  have hz : inputNumeral 0 = .app (.atom .k) (.atom .i) := by
    simp [inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub]
  rw [hz]
  exact (P01DF.PolyConv.app (.k _ _) (.refl a)).trans (.i a)

theorem zero_state_projection (f a : Poly) :
    P01DF.PolyConv (fstPoly (graphRun (inputNumeral 0) f a))
      (stateRun (inputNumeral 0)) :=
  ((P01DF.PolyConv.app (zero_iterates _ _) (.refl _)).trans
    (state_seed_commutes f a)).trans (zero_iterates _ _).symm

theorem zero_scalar_projection (f a : Poly) :
    P01DF.PolyConv (fstPoly (sndPoly (graphRun (inputNumeral 0) f a)))
      (.app (.app (inputNumeral 0) f) a) :=
  ((P01DF.PolyConv.app (.app (zero_iterates _ _) (.refl _)) (.refl _)).trans
    (scalar_seed_commutes f a)).trans (zero_iterates _ _).symm

theorem zero_source_graph :
    Has scalarContext (graphRun (inputNumeral 0) (.var 1) (.var 0))
      (Graph (.var 1) (.var 0)) :=
  graph_run_has scalar_context_formed
    (closed_has (inputNumeral_has 0) N_subst scalar_context_formed) f_has a_has

-- Scope is checked without adding any naturality or projection premise.
#check @graph_run_has
#check @iterated_invariant
#check @state_transport_formed
#check @scalar_transport_formed
#print axioms step_evidence_erases
#print axioms step_retains_scalar
#print axioms nested_actual_step
#print axioms zero_state_projection
#print axioms zero_scalar_projection
#print axioms zero_source_graph
end P01AC.ExtensionalRepair.InternalGraph.Review

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let blocked := [``P01AC.F, ``P01AC.G, ``P01AC.predicates,
    ``P01R.finite_fundamental, ``P01AC.form_sound, ``P01AC.has_sound,
    ``P01AC.fundamental, ``P01AC.ExtensionalRepair.form_sound,
    ``P01AC.ExtensionalRepair.has_sound, ``P01AC.ExtensionalRepair.fundamental,
    ``P01AC.ExtensionalRepair.unary_fundamental,
    ``P01AC.EffectiveCompleteness.semantic_church_standardness,
    ``P01AC.EffectiveCompleteness.graph_application]
  for target in [``P01AC.ExtensionalRepair.InternalGraph.graph_form,
      ``P01AC.ExtensionalRepair.InternalGraph.congr_app_has,
      ``P01AC.ExtensionalRepair.InternalGraph.trans_has,
      ``P01AC.ExtensionalRepair.InternalGraph.strong_step_has,
      ``P01AC.ExtensionalRepair.InternalGraph.graph_run_has,
      ``P01AC.ExtensionalRepair.InternalGraph.iterated_invariant,
      ``P01AC.ExtensionalRepair.InternalGraph.literal_graph_invariant,
      ``P01AC.ExtensionalRepair.InternalGraph.original_scalar_computation] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for old in blocked do
      if state.visited.contains old then
        throwError "Forbidden semantic dependency {old} in source construction {target}"
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"PASS source-only: {target}; axioms {state.axioms}"
  for target in [``P01AC.ExtensionalRepair.InternalGraph.state_projection_not_conversion,
      ``P01AC.ExtensionalRepair.InternalGraph.scalar_projection_not_conversion] do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"PASS conversion-only boundary: {target}; axioms {state.axioms}"
