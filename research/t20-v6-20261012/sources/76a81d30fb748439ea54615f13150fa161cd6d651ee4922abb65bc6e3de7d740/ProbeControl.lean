import JointNumeralExtraction
import JointExtractionInput
open JointCompletion OpenDevelopments OpenTermStandardness
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances (scalarLeft)
set_option maxRecDepth 16384
set_option maxHeartbeats 16000000
#eval (EffectiveNumerals.extractIteration ExtractionInput.control ExtractionInput.control_has).val
#eval (List.range 100).find? (fun r => (readIteration (run r (interp (scalarLeft ExtractionInput.control) T.var))).isSome)
