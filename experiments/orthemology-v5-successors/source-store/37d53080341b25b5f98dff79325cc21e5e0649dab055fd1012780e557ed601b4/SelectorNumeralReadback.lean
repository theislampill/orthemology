import LiteralRuntimeCounterexample
open Orthemology.Eighth.SemanticControls.LiteralAssessment
#eval IO.println ("SELECTORS_FALSE=" ++ reprStr (literalConfig false).selectors)
#eval IO.println ("SELECTORS_TRUE=" ++ reprStr (literalConfig true).selectors)
