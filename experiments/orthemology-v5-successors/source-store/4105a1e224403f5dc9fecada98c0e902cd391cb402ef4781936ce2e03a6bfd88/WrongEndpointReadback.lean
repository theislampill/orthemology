/- Expected rejection of a mismatched exact theorem statement only.
   This is not a noninhabitation claim: the reflexive identity is derivable. -/
import InhabitedEndpointControl
open OrthemologyV2 P01D P01AC P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.InhabitedControl
example : HasE [] (jPoly (.atom .i) q (.atom .i)) (.identity Q Fp Fp) :=
  inhabited_endpoint_identity
