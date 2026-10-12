import AuxiliaryControls
open Encodable AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC AuxiliaryCodeComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
example : checkPolyCode (encode (PolyCert.bridge .i .k))
    (encode (Poly.app (.atom .i) (.atom .k))) (encode (Poly.app (.atom .i) (.atom .k))) = true := by
  rw [checkPolyCode_exact]; decide
