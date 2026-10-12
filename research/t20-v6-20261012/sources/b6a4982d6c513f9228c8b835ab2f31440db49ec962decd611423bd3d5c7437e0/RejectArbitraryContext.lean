import RawContextControls
open P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (iterationPoly)
open P01AC.Intensional.Plus (PolyConvPlus)
open RawContextUniformity
-- An actual Church variable is outside the all-Raw theorem's premise.
example : ∃ k, PolyConvPlus (observe (.var 0)) (iterationPoly k) :=
  raw_uniform_iteration Controls.church_variable_has
