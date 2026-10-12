import ControlTests
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
-- Regression sentinel: correct full recomputation proves this.
example : executableOutput sourceOne succOne Finset.univ sameRow cascadePriority 0 Finset.univ =
    ({({2} : Finset Three)} : Finset (Finset Three)) := cascade_output
-- Incorrect mutation: stop after one deleting round.
example : executableMECs sourceOne succOne
    (executableStep sourceOne succOne Finset.univ sameRow cascadePriority 0 Finset.univ) =
    ({({2} : Finset Three)} : Finset (Finset Three)) := by decide
