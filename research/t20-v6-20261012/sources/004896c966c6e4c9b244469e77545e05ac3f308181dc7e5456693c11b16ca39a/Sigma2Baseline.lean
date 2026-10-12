import Sigma2Witnesses
open P02A2 P02A2.Sigma2RowLaw P02A2.Sigma2Witnesses
example : defect (rowLaw trueMatrix ()) = 0 := trueMatrix_defect_zero
example : defect (rowLaw falseMatrix ()) = 1 := falseMatrix_defect_one
example : defect (rowLaw swappedMatrix ()) = 1 := swappedMatrix_defect_one
