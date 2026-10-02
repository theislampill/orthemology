import HeldReceiptProjection

set_option maxRecDepth 20000
namespace Orthemology.RationalLaw.ProjectionSourceReadback
open Orthemology.RuntimeBridge P02.Codec
open ProjectionControl HeldStateControl

#eval IO.println ("ACK_BYTES=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (compiled ackMachine 0)).map toString) ++ "]")
#eval IO.println ("ACK_INDEX=" ++ toString (index ackMachine 0))
#eval IO.println ("HELD_BYTES=" ++ "[" ++ String.intercalate ","
  ((encodeBytes (compiled (numberMachine finTwoEquiv.symm heldMachine)
    (finTwoEquiv.symm false))).map toString) ++ "]")
#eval IO.println ("HELD_INDEX=" ++ toString heldIndex)

end Orthemology.RationalLaw.ProjectionSourceReadback
