import UnaryNormalForm
open P01AC.UnaryIdentity
example : identityCheck (exceptionalExample.substitute (.constant 2))
    (.constant 2) = true := by decide
