import ProgressCuts
#check PolicySynthesis.progressCut_primrec
#check PolicySynthesis.lastCut_primrec
#check PolicySynthesis.rowTotal_iff_unbounded_cuts
#check PolicySynthesis.not_rowTotal_eventually_lastCut
open PolicySynthesis
example (q : Nat × Nat) : progressCut q 0 = true := progressCut_zero q
example : lastCut (fun i => decide (i = 0 ∨ i = 3)) 2 = 0 := by decide
example : lastCut (fun i => decide (i = 0 ∨ i = 3)) 3 = 3 := by decide
example : lastCut (fun i => decide (i = 0 ∨ i = 3)) 100 = 3 := by decide
example (q : Nat × Nat) (s : Nat) (hs : 0 < s) :
    progressCut q s = true ↔ progress q (s-1) < progress q s := progressCut_pos hs
#print axioms PolicySynthesis.rowTotal_iff_unbounded_cuts
#print axioms PolicySynthesis.progressCut_primrec
