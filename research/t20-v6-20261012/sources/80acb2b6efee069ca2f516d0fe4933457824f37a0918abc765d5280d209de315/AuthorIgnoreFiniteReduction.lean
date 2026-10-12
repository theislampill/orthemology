import AuxiliaryControls
open Encodable AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC AuxiliaryCodeComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
example : checkFiniteCode
    (encode (FiniteCert.reduce .i .k (.arrow .bottom .bottom) (.i .bottom) (.refl .k)))
    (encode Term.k) (encode (TypeCode.arrow .bottom .bottom)) = true := by
  rw [checkFiniteCode_exact]; decide
