import SCCControls
open HiddenParity HiddenParity.SCCControls HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example :
    ({0,1,2} : Finset Four).filter (fun e => (reverseSucc e).Nonempty ∧
      ∀ t ∈ reverseSucc e,
        t ∈ usedStates reverseSource ({0,1,2} : Finset Four) ∧
          t ∈ FiniteReachability.reachable
            (Edge reverseSource reverseSucc ({0,1,2} : Finset Four)) (reverseSource e)) =
      ({0,2} : Finset Four) := by decide
