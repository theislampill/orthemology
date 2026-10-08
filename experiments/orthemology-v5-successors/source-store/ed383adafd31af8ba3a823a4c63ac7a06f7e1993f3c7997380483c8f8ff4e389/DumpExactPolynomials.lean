/- Review-only export of exact syntax, not a lambda-calculus formalisation. -/
import InhabitedEndpointControl
open OrthemologyV2 P01D P01AC.ExtensionalRepair.InhabitedControl

def termTree : Term → String
  | .i => "i"
  | .k => "k"
  | .s => "s"
  | .zero => "z"
  | .one => "o"
  | .app f x => "(" ++ termTree f ++ " " ++ termTree x ++ ")"

def polyTree : Poly → String
  | .var n => "v" ++ toString n
  | .atom t => termTree t
  | .app f x => "(" ++ polyTree f ++ " " ++ polyTree x ++ ")"

#eval polyTree Fp
#eval polyTree Fq
