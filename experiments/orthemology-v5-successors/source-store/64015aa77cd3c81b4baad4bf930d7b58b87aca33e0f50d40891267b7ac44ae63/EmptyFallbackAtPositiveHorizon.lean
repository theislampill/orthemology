import LookaheadBoundary
open EffectiveRenewal
-- A default [] result cannot certify successful completion at positive horizon.
example : ([] : Word).length = 1 := by simp
