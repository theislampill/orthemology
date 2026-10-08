import GenericIdentityCarrierProbe
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.ExtensionalRepair
open GenericIdentityCarrierProbe (F G)
-- The new N-to-Raw control is not an identity at the compiler's N-to-N carrier.
-- Statement mismatch is not noninhabitation.
example : HasE [] (.atom .i) (.identity (arr N N) F G) :=
  GenericIdentityCarrierProbe.closed_probe_identity
