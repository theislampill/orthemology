import AuxiliaryControls
open Encodable AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC AuxiliaryCodeComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
example : checkPolyCode
    (encode (PolyCert.trans (.var 0) (.var 1) (.var 0) (.refl (.var 0)) (.refl (.var 0))))
    (encode (Poly.var 0)) (encode (Poly.var 0)) = true := by
  rw [checkPolyCode_exact]; decide
