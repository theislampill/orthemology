import IndependentBoundaryChecks
open P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N)
open RawContextUniformity RawContextReview
-- The preserved observation count cannot supply a scoped source typing.
example : HasE (rawTel 1) (psub escapingSubstitution Controls.opaqueInput) N :=
  escaped_observation_count
