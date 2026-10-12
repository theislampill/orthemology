import P01CanonicalCarrierProjection
open OrthemologyV2 OrthemologyV3 P01D P01R P01DF
example : carrierCode (IdPER totalPER .i P01DF.skk) = equalityCode (carrierCode totalPER) .i P01DF.skk := by
  exact raw_identity_carrier_square .i P01DF.skk
