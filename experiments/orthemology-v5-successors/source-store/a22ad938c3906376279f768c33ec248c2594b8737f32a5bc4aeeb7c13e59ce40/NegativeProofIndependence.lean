import ExactRuntimeCounterexample
import Lean.Util.CollectAxioms
open Lean Elab Command

-- Traverse checked proof and type constants, using the same kernel-environment
-- traversal as Lean's transitive axiom audit. An import alone is not proof use.
run_cmd do
  let env ← getEnv
  let positive : Name := ``Orthemology.RuntimeBridge.PhaseUpdate.FullController.full_phase_computed_tolerance_decoded_parity
  let roots : List Name := [
    ``Orthemology.Eighth.SemanticControls.computedDecoder_wins,
    ``Orthemology.Eighth.SemanticControls.positive_opposite_failure,
    ``Orthemology.Eighth.SemanticControls.mixed_runtime_blind_history_law,
    ``Orthemology.Eighth.SemanticControls.exact_runtime_mutant_positive_failure,
    ``Orthemology.Eighth.SemanticControls.exact_runtime_mutant_not_ae,
    ``Orthemology.Eighth.SemanticControls.exact_mutated_runtime_claim_false]
  for root in roots do
    let (_, s) := ((Lean.CollectAxioms.collect root).run env).run {}
    if s.visited.contains positive then
      throwError "Negative proof depends on original positive runtime target: {root}"
    logInfo m!"PASS_NEGATIVE_PROOF_INDEPENDENCE {root}: original positive runtime target absent from transitive checked proof/type closure"
  let (_, s) := ((Lean.CollectAxioms.collect
    ``Orthemology.Eighth.SemanticControls.exact_runtime_positive_control).run env).run {}
  unless s.visited.contains positive do
    throwError "Positive dependency control failed"
  logInfo "PASS_DEPENDENCY_DETECTOR_POSITIVE_CONTROL: exact_runtime_positive_control uses the original positive runtime theorem"
