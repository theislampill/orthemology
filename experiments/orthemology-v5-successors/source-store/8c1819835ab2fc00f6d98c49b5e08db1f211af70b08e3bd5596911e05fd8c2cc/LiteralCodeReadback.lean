import LiteralRuntimeCounterexample
open Orthemology.Eighth.SemanticControls.LiteralAssessment
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open P02.Codec

def emitPolicy (label : String) (c : Config) : IO Unit :=
  IO.println (label ++ "=" ++ "[" ++ String.intercalate "," ((encodeBytes (pack (policyProgram c))).map toString) ++ "]")
#eval emitPolicy "OLD_FALSE_BYTES" (literalConfig false)
#eval emitPolicy "OLD_TRUE_BYTES" (literalConfig true)
#eval emitPolicy "COMPUTED_FALSE_BYTES" (withComputedTolerance (literalConfig false))
#eval emitPolicy "COMPUTED_TRUE_BYTES" (withComputedTolerance (literalConfig true))
