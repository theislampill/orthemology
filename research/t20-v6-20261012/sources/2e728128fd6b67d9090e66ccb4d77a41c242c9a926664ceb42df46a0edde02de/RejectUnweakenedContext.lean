import StructuredContextControls
open P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (NBody)
open StructuredContextUniformity StructuredContextUniformity.Controls
-- The allExt body must use the actual type-weakened context.
example : FormE (twkTel [parameterSensitive]) NBody :=
  formBody (ctx_inclusion parameterSensitive_original)
