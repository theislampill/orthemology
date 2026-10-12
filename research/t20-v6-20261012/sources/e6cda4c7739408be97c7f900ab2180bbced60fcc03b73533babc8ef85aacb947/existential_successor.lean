import SCCControls
open HiddenParity HiddenParity.SCCControls HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example :
    (Finset.univ : Finset Four).filter (fun e => ∃ t ∈ reverseSucc e,
      t ∈ usedStates reverseSource (Finset.univ : Finset Four) ∧
        reverseSource e ∈ FiniteReachability.reachable
          (Edge reverseSource reverseSucc (Finset.univ : Finset Four)) t) =
      ({0,1,2} : Finset Four) := by decide
