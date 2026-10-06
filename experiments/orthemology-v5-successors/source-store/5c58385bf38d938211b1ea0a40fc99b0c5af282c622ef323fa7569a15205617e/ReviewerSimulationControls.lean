import SimulationControls

namespace SharedAlias.ReviewerSimulationControls
open OperationalJoin
open ModelControls
noncomputable section
open Classical

/-- The relation includes out-of-path concrete commitments but masks them abstractly. -/
theorem out_of_path_mask_is_real :
    Refines env (prepare env (initial env ()) 0 command)
      (prepareLabels (Initial env.labelConfig ()) (testInterface.commandPath command ∩ aliases env 0) command) ∧
    command ∈ ((prepare env (initial env ()) 0 command).roots (env.rootOf 1)).commitments ∧
    command ∉ ((prepareLabels (Initial env.labelConfig ())
      (testInterface.commandPath command ∩ aliases env 0) command).roots 1).commitments := by
  refine ⟨prepare_refines (initial_refines env ()) 0 command, shared_prepare env _ 0 1 command (by decide), ?_⟩
  simp [prepareLabels, Initial, testInterface, command]

/-- Root-wide propagation creates an extra concrete veto without an extra abstract reply. -/
theorem unmatched_alias_veto_is_allowed :
    Refines env (acknowledge env (request (initial env ())) 0)
      (OperationalJoin.acknowledge env.labelConfig (OperationalJoin.request (Initial env.labelConfig ())) 0) ∧
    0 ∈ ((acknowledge env (request (initial env ())) 0).roots (env.rootOf 1)).revoked ∧
    0 ∉ ((OperationalJoin.acknowledge env.labelConfig (OperationalJoin.request (Initial env.labelConfig ())) 0).roots 1).revoked ∧
    (OperationalJoin.acknowledge env.labelConfig (OperationalJoin.request (Initial env.labelConfig ())) 0).acks = {0} := by
  refine ⟨acknowledge_refines (request_refines (initial_refines env ())) 0, ?_, ?_, ?_⟩
  · decide
  · decide
  · simp [OperationalJoin.acknowledge, OperationalJoin.request]

/-- There are multiple selected aliases; preparation must expand beyond the addressed one. -/
def bothAliases : testInterface.Command := (0, {0,1,2,3,4})

theorem lawful_both_aliases_preparation :
    Step env (initial env ()) (.prepare 0 bothAliases () 0)
      (prepare env (initial env ()) 0 bothAliases) := by
  apply Step.prepare
  · decide
  · decide
  · right; simp [Envelope, initial, testInterface, env, bothAliases]

theorem both_selected_aliases_are_prepared :
    bothAliases ∈ ((prepareLabels (Initial env.labelConfig ())
      (testInterface.commandPath bothAliases ∩ aliases env 0) bothAliases).roots 0).commitments ∧
    bothAliases ∈ ((prepareLabels (Initial env.labelConfig ())
      (testInterface.commandPath bothAliases ∩ aliases env 0) bothAliases).roots 1).commitments := by
  simp [prepareLabels, Initial, testInterface, bothAliases, aliases,
    Environment.rootOf, env, AttributionKernel.rootMap]

theorem lawful_preparation_has_reachable_receipt_exact_witness :
    ∃ t events,
      OperationalJoin.Trace env.labelConfig (Initial env.labelConfig ()) events t ∧
      OperationalJoin.Reachable env.labelConfig t ∧
      Refines env (prepare env (initial env ()) 0 bothAliases) t ∧
      t.acks = ∅ ∧ t.cancelAcks = (fun _ => ∅) ∧ landings events = [] := by
  obtain ⟨t, events, trace, related, lands⟩ := step_simulation
    (initial_refines env ()) (consistent_initial env.labelConfig ()) lawful_both_aliases_preparation
  exact ⟨t, events, trace, ⟨(), events, trace⟩, related, related.acks, related.cancelAcks, lands⟩

#print axioms out_of_path_mask_is_real
#print axioms unmatched_alias_veto_is_allowed
#print axioms lawful_both_aliases_preparation
#print axioms both_selected_aliases_are_prepared
#print axioms lawful_preparation_has_reachable_receipt_exact_witness
end
end SharedAlias.ReviewerSimulationControls
