import ControlTests
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example : executableOutput cycleSource cycleSucc Finset.univ cycleRow cycle21 0 Finset.univ =
    (∅ : Finset (Finset Two)) := cobuchi_21_cycle_rejected
-- Incorrect mutation: replace good=2/bad=1 by good=0/bad=1.
example : executableOutput cycleSource cycleSucc Finset.univ cycleRow cycle01 0 Finset.univ =
    (∅ : Finset (Finset Two)) := by decide
