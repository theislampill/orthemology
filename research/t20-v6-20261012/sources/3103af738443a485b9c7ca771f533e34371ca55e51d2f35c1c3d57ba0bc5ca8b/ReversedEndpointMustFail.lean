import Sigma2Witnesses
open P02A2 P02A2.Sigma2RowLaw P02A2.Sigma2Witnesses
-- A permanent candidate gives defect zero, not defect one.
example : defect (rowLaw trueMatrix ()) = 1 := by rw [trueMatrix_defect_zero]; norm_num
