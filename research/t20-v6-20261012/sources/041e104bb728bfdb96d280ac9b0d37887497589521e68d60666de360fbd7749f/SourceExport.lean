import ScalarCertificates
namespace SourceExport
open OrthemologyV2 P01D

def term : Term → String
  | .i => "[\"i\"]"
  | .k => "[\"k\"]"
  | .s => "[\"s\"]"
  | .zero => "[\"zero\"]"
  | .one => "[\"one\"]"
  | .app f x => "[\"app\"," ++ term f ++ "," ++ term x ++ "]"

def poly : Poly → String
  | .var n => "[\"var\"," ++ toString n ++ "]"
  | .atom a => "[\"atom\"," ++ term a ++ "]"
  | .app f x => "[\"app\"," ++ poly f ++ "," ++ poly x ++ "]"

/-- The actual frozen source, including every atom/application boundary. -/
def exported : String := "{\"originalQ\":" ++ poly FullPER.Application.originalQ ++
  ",\"numerals\":[" ++ String.intercalate "," ((List.range 7).map fun k =>
    poly (P01AC.EffectiveCompleteness.inputNumeral k)) ++
  "],\"omega\":" ++ term OrthemologyV3.omega ++ "}"
end SourceExport

def main : IO Unit := IO.println SourceExport.exported
