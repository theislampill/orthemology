import UnaryWitnesses
import UnaryExpressivity
open P01AC.UnaryIdentity
#eval normalise exceptionalExample
#eval identityCheck exceptionalExample .variable
#eval identityCheck (exceptionalExample.substitute (.constant 2)) (.constant 7)
#eval verifyCertificate exceptionalExample exceptionalExample (makeCertificate exceptionalExample)
#eval verifyCertificate .variable .variable ⟨[0, 1], [none, some 1]⟩
#eval distinguishingInput exceptionalExample .variable
#eval distinguishingInput (.ifEq .variable (.constant 0) (.constant 3) .variable) .variable
#eval distinguishingInput (.add .variable (.constant 0)) .variable
#eval (Expr.reify ⟨[0, 1], [none, none, some 7]⟩).denote 2
