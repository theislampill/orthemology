import ControlTests
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example : executableOutput singleSource singleSucc Finset.univ sameSingleRow oppositePriority 0 Finset.univ =
    (∅ : Finset (Finset One)) := equal_row_odd_rival_rejects
-- Incorrect mutation: consult candidate 0 alone rather than every matching live model.
example : executableOutput singleSource singleSucc {0} sameSingleRow oppositePriority 0 Finset.univ =
    (∅ : Finset (Finset One)) := by decide
