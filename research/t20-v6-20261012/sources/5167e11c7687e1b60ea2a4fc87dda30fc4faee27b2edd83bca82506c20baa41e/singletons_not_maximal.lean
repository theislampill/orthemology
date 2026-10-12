import SCCControls
open HiddenParity HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
example :
    (Finset.univ : Finset Three).image (fun a => ({a} : Finset Three)) =
      SCCPruning.mecs sourceOne succOne Finset.univ := by decide
