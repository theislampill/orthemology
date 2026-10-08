import HiddenChangePolicyRegions
open HiddenChange
-- Equality t=N already uses mode1. A strict-post-switch convention is false.
example : fixedMode (some 1) 1 = 0 := by decide +kernel
