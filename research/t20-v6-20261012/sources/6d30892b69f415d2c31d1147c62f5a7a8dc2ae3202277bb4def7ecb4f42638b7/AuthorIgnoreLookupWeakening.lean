import AuxiliaryControls
open Encodable AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC AuxiliaryCodeComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
example : checkLookupCode
    (encode (LookupCert.zero [] (.identity .raw (.var 0) (.var 0))))
    (encode ([.identity .raw (.var 0) (.var 0)] : Tel)) 0
    (encode (Ty.identity .raw (.var 0) (.var 0))) = true := by
  rw [checkLookupCode_exact]; decide
