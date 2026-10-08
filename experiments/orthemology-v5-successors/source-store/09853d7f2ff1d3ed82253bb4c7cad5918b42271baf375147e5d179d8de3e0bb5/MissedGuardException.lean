import UnaryNormalForm
open P01AC.UnaryIdentity
example : identityCheck (.ifEq exceptionalExample .variable (.constant 1) (.constant 0))
    (.constant 1) = true := by decide
