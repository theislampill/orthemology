import UnaryWitnesses
open P01AC.UnaryIdentity
example : distinguishingInput (.ifEq .variable (.constant 0) (.constant 3) .variable)
    .variable = none := by decide
