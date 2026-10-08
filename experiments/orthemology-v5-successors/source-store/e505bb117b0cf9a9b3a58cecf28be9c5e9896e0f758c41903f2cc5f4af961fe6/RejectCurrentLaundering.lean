import GenericIdentityCarrierProbe
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.ExtensionalRepair
open GenericIdentityCarrierProbe (F G)
-- The closed extensional conclusion belongs to HasE, not current Has.
-- Statement mismatch is not noninhabitation.
example : Has [] (.atom .i) (.identity (arr N .raw) F G) :=
  GenericIdentityCarrierProbe.closed_probe_identity
