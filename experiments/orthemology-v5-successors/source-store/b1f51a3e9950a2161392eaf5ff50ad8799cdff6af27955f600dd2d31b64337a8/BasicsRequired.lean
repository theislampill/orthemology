import ReductionBasics
#check PolicySynthesis.slice_primrec
#check PolicySynthesis.allBelow_primrec
#check PolicySynthesis.slice_prefix_source
#check PolicySynthesis.HasComputablePath
open EffectiveRenewal PolicySynthesis
example : slice [true, false, true] 1 2 = [false, true] := by decide
example : slice [] 0 0 = [] := by decide
example : allBelow (fun _ => false) 0 = true := by decide
example : allBelow (fun i => decide (i < 3)) 3 = true := by decide
example : allBelow (fun i => decide (i < 3)) 4 = false := by decide
