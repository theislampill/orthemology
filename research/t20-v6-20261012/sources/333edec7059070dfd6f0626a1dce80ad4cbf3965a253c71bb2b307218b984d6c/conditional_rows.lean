import ControlTests
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example : executableOutput singleSource singleSucc Finset.univ exitRow oppositePriority 0 Finset.univ =
    ({(Finset.univ : Finset One)} : Finset (Finset One)) := full_row_difference_retains_target
-- The real full rows are (1,0) and (1/2,1/2). Conditioned on internal state 0,
-- both become (1,0), represented by sameSingleRow. Using those rows is incorrect.
example : executableOutput singleSource singleSucc Finset.univ sameSingleRow oppositePriority 0 Finset.univ =
    ({(Finset.univ : Finset One)} : Finset (Finset One)) := by decide
