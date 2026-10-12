import BoundaryControls
open P02A2 P02A2.Q8Measure AtomicMembershipAudit
example : mass fairCantor = 1 := by
  rw [fair_mass_zero]
  norm_num
