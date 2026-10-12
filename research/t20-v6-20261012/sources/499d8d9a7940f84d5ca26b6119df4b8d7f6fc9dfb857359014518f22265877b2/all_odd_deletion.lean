import ControlTests
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example : executableOutput cycleSource cycleSucc Finset.univ cycleRow cycle23 0 Finset.univ =
    ({(Finset.univ : Finset Two)} : Finset (Finset Two)) := higher_odd_cycle_retained
-- Incorrect mutation: delete every odd-priority pair before target computation.
example : executableOutput cycleSource cycleSucc Finset.univ cycleRow cycle23 0
    ((Finset.univ : Finset Two).filter (fun e => cycle23 0 e % 2 = 0)) =
    ({(Finset.univ : Finset Two)} : Finset (Finset Two)) := by decide
