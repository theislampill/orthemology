import AliasObstruction

namespace SharedAlias.ModelControls
open OperationalJoin
noncomputable section

def testInterface : Interface 7 where
  Policy := Nat
  Command := Nat × Finset (Fin 7)
  Plant := Unit
  Requester := Unit
  policyEpoch := id
  commandEpoch := Prod.fst
  commandPath := Prod.snd
  recipient := fun _ => ()
  admits := fun _ _ policy command _ => command.1 = policy
  effect := fun _ _ => ()
  admitted_epoch := by intros; assumption
  admitted_requester := by intros; rfl

def env : Environment testInterface where
  aliasClass := {0,1}
  class_positive := by decide
  budget := 1
  budget_positive := by decide
  actualFaults := {some 6}
  actual_faults := by decide
  actual_budget := by decide
  non_saturated := by decide
  q := 5
  r := 5
  overlap := by decide
  repair_available := by decide
  revoke_available := by decide
  source := id
  source_epoch := by intro e; rfl

def command : testInterface.Command := (0, {0,2,3,4,5})

theorem prepare_is_lawful :
    Step env (initial env ()) (.prepare 0 command () 0)
      (prepare env (initial env ()) 0 command) := by
  apply Step.prepare
  · decide
  · decide
  · right
    simp [Envelope, initial, testInterface, env, command]

theorem cancel_is_lawful :
    Step env (initial env ()) (.cancelAck 0 command ())
      (cancelAck env (initial env ()) 0 command) := by
  apply Step.cancelAck
  · decide
  · exact Or.inr rfl

theorem unselected_alias_obstruction :
    ¬∃ s : OperationalJoin.State testInterface,
      OperationalJoin.Reachable env.labelConfig s ∧
      (command ∈ (s.roots 1).commitments ↔
        command ∈ ((prepare env (initial env ()) 0 command).roots (env.rootOf 1)).commitments) := by
  apply no_reachable_literal_prepare
  · decide
  · decide
  · decide

theorem closure_adds_only_real_reply :
    (acknowledge env (request (initial env ())) 0).acks = {0} ∧
    0 ∈ ((acknowledge env (request (initial env ())) 0).roots (env.rootOf 1)).revoked := by
  decide

theorem cancellation_adds_only_real_reply :
    (cancelAck env (initial env ()) 0 command).cancelAcks command = {0} ∧
    command ∈ ((cancelAck env (initial env ()) 0 command).roots (env.rootOf 1)).cancelled := by
  constructor
  · simp [cancelAck, initial]
  · exact shared_cancel env (initial env ()) 0 1 command (by decide) (by decide)

/-- The maximally tainted class has two bad labels but only one bad actual root. -/
theorem actual_one_can_taint_two :
    (AttributionKernel.taintedLabels ({0,1} : Finset (Fin 7)) {none}).card = 2 ∧
    ({none} : Finset (Option (Fin 7))).card = 1 := by decide

end
end SharedAlias.ModelControls
