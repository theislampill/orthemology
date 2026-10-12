import SCCControls
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example :
    (Finset.univ : Finset One).filter (fun e => ∀ t ∈ emptySucc e,
      t ∈ usedStates singleSource (Finset.univ : Finset One) ∧
        singleSource e ∈ FiniteReachability.reachable
          (Edge singleSource emptySucc (Finset.univ : Finset One)) t) =
      (∅ : Finset One) := by decide
