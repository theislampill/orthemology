import RationalTest
import Mathlib.Tactic
-- Deliberately false intended mutations: dropping literal modulo-two cycling
-- and using a non-strict count gate must fail as mathematical equalities.
example : (3 : ℕ) % 2 = 0 := by norm_num
example : decide ((2 : ℕ) < 2) = true := by decide
