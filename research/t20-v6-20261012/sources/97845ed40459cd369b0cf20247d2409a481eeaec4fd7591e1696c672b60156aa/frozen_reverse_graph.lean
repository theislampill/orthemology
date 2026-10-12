import SCCControls
open HiddenParity HiddenParity.SCCControls HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example :
    ({0,1,2} : Finset Four).filter
      (SCCPruning.Keep reverseSource reverseSucc Finset.univ) =
      ({0,2} : Finset Four) := by decide
