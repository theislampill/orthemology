import Sigma2Witnesses
open P02A2 P02A2.Sigma2RowLaw P02A2.Sigma2Witnesses
-- forall t exists s holds, but it is not the source normal form.
example : defect (rowLaw swappedMatrix ()) = 0 := by rw [swappedMatrix_defect_one]; norm_num
