import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.Matrix.Block
import Mathlib.Algebra.MvPolynomial.Basic

-- This probe checks the availability of lower-level algebraic infrastructure.
-- It makes no claim about the infinite recursive moment functional.
#check Matrix
#check Matrix.det
#check Matrix.nonsing_inv_mul
#check Matrix.mul_nonsing_inv
#check Matrix.mulVec
#check Matrix.fromBlocks
#check MvPolynomial
