import AuxiliaryControls
open Encodable AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC AuxiliaryCodeComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 200000
example : checkStepCode (encode (StepCert.left .i .k .s (.i .k)))
    (encode (Term.app .i .s)) (encode (Term.app .k .s)) = true := by
  rw [checkStepCode_exact]; decide
