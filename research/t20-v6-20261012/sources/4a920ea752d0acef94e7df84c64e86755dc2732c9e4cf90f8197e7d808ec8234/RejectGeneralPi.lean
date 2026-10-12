import P01CanonicalCarrierProjection
open OrthemologyV2 OrthemologyV3 P01D P01R P01DF
example : carrierCode (PiPER totalPER (fun _ => rawPER) (fun _ => rfl)) = dependentPi (carrierCode totalPER) (carrierFamily (fun _ => rawPER) (fun _ => rfl)) := by
  exact raw_pi_carrier_square (fun _ => rawPER) (fun _ => rfl)
