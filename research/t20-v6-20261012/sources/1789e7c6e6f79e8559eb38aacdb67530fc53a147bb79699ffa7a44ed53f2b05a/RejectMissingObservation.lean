import StructuredContextControls
open P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral)
open P01AC.ExtensionalRepair.ExactScalarFusion (i)
open StructuredContextUniformity
-- Actual typing alone does not supply the required observation conversion.
example : HasE [N] i (.identity N (.var 0) (inputNumeral 0)) :=
  opaque_canonicity_at_count RawContextUniformity.Controls.church_variable_has
