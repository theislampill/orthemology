import SCCControls
open HiddenParity HiddenParity.SCCControls HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example :
    let V := SCCPruning.step reverseSource reverseSucc (Finset.univ : Finset Four)
    V.image (fun a => SCCPruning.cluster reverseSource reverseSucc V (reverseSource a)) =
      ({({0} : Finset Four), {2}} : Finset (Finset Four)) := by decide
