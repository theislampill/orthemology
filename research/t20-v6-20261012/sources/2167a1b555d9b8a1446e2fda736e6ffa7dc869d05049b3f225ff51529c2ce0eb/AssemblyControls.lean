import GraphBridgeAssembly
import Lean

namespace P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
open P01AC.Intensional.Plus (PolyConvPlus)
open FullPER.Application (originalQ)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

-- The initial assembly retains the graph-invariant witness under erasure.
-- No claim that it raw-converts to I is needed or made.
theorem assembly_erases_to_graph (stateEvidence scalarEvidence : Poly) :
    PolyConvPlus (assembledProof stateEvidence scalarEvidence)
      (sndPoly (sndPoly (graphRun (.var 2) (.var 1) (.var 0)))) :=
  (ExactScalarFusion.j_conversion _ _ _).trans
    ((ExactScalarFusion.j_conversion _ _ _).trans (ExactScalarFusion.j_conversion _ _ _))

-- The additional, typed J reset is what creates an I-convertible witness.
def resetProof (stateEvidence scalarEvidence : Poly) : Poly :=
  jPoly (.atom .i) (ExactScalarFusion.scalarR originalQ)
    (assembledProof stateEvidence scalarEvidence)

theorem reset_proof_hasE {stateEvidence scalarEvidence : Poly}
    (hs : HasE scalarContext stateEvidence stateTransport)
    (hx : HasE scalarContext scalarEvidence scalarTransport) :
    HasE scalarContext (resetProof stateEvidence scalarEvidence)
      (ExactScalarFusion.Leaf originalQ) := by
  have hc := scalar_context_formed
  have hl := ExactScalarFusion.scalar_n_has hc n_has f_has a_has
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have hqn := app_has (ExactScalarFusion.T_form hc) (N_form hc) hq n_has
  have hqr := ExactScalarFusion.scalar_n_has hc hqn f_has a_has
  have hrefl : Has scalarContext (.atom .i)
      (.identity A ExactScalarFusion.scalarL ExactScalarFusion.scalarL) :=
    .identityIntro (.identity (.param hc) hl hl) hl hl (.refl _)
  exact trans_hasE hc hl hl hqr (has_inclusion hrefl) (scalar_leaf_from_bridges hs hx)

theorem reset_proof_erases (stateEvidence scalarEvidence : Poly) :
    PolyConvPlus (resetProof stateEvidence scalarEvidence) (.atom .i) :=
  ExactScalarFusion.j_conversion _ _ _

-- Literal identity of all three retained target objects.
example : originalQ = P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed := rfl
example : ExactScalarFusion.c3 =
    abstract (abstract (abstract (.atom OrthemologyV2.Term.i))) := rfl
example : ExactScalarFusion.W originalQ =
    Ty.pi N (.all (.pi End (.pi A (ExactScalarFusion.Leaf originalQ)))) := rfl

-- No stronger, older Has premise is needed for either bridge.
example (p q : Poly) (hp : HasE scalarContext p stateTransport)
    (hq : HasE scalarContext q scalarTransport) :
    HasE [] ExactScalarFusion.c3 (ExactScalarFusion.W originalQ) :=
  scalar_fusion_from_bridges hp hq

#check @image_congr_hasE
#check @trans_hasE
#check @replace_left_hasE
#check @identity_i_hasE
#check @scalar_leaf_from_bridges
#check @scalar_leaf_i_from_bridges
#check @scalar_fusion_from_bridges
#print axioms reset_proof_hasE
#print axioms reset_proof_erases
end P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.Controls

open Lean Elab Command
run_cmd do
  let env ← getEnv
  let blocked := [``P01AC.F, ``P01AC.G, ``P01AC.predicates,
    ``P01R.finite_fundamental, ``P01AC.form_sound, ``P01AC.has_sound,
    ``P01AC.fundamental, ``P01AC.ExtensionalRepair.form_sound,
    ``P01AC.ExtensionalRepair.has_sound, ``P01AC.ExtensionalRepair.fundamental,
    ``P01AC.ExtensionalRepair.unary_fundamental,
    ``P01AC.EffectiveCompleteness.semantic_church_standardness,
    ``P01AC.EffectiveCompleteness.graph_application,
    ``FullPER.F, ``FullPER.fundamental,
    ``FullPER.Application.scalar_target_valid, ``FullPER.Application.scalar_target_fundamental]
  let targets := [``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.image_congr_hasE,
    ``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.trans_hasE,
    ``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.replace_left_hasE,
    ``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.identity_i_hasE,
    ``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.scalar_leaf_from_bridges,
    ``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.scalar_leaf_i_from_bridges,
    ``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.scalar_fusion_from_bridges]
  for target in targets do
    let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
    for old in blocked do
      if state.visited.contains old then
        throwError "Forbidden semantic dependency {old} in source construction {target}"
    for ax in state.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "Unexpected axiom {ax} in {target}"
    logInfo m!"PASS source-only: {target}; axioms {state.axioms}"
  let target := ``P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.scalar_fusion_from_bridges
  let (_, state) := ((Lean.CollectAxioms.collect target).run env).run {}
  for required in [``P01AC.ExtensionalRepair.HasE.j, ``P01AC.ExtensionalRepair.HasE.conv,
      ``P01AC.ExtensionalRepair.HasE.piIntro, ``P01AC.ExtensionalRepair.HasE.allIntro,
      ``P01AC.ExtensionalRepair.InternalGraph.literal_graph_invariant,
      ``P01AC.ExtensionalRepair.InternalGraph.original_scalar_computation] do
    unless state.visited.contains required do
      throwError "Missing required actual source dependency {required}"
    logInfo m!"PASS required actual dependency: {required}"
