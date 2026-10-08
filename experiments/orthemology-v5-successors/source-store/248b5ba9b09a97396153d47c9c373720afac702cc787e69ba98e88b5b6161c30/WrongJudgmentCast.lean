/- Expected type mismatch: an extended identity is not an ordinary Has proof. -/
import InhabitedEndpointControl
open OrthemologyV2 P01D P01AC P01AC.ExtensionalRepair.InhabitedControl
example : Has [] (jPoly (.atom .i) q (.atom .i)) (.identity Q Fp Fq) :=
  inhabited_endpoint_identity
