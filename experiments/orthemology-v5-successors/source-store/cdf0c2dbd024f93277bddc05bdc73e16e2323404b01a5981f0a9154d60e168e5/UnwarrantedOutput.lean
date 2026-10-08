import ResetComponent
open EffectiveRenewal PolicySynthesis
-- A programme that sees no positive cut does not acquire any committed output.
example : (blockSnapshots (fun i => decide (i = 0)) 10).length = 10 := by decide
