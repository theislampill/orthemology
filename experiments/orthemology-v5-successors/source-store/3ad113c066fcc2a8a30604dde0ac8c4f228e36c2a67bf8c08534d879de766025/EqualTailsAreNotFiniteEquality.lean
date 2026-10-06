import UnaryNormalForm
open P01AC.UnaryIdentity
example : identityCheck (.ifEq (.add .variable (.constant 0)) .variable
    (.constant 7) (.constant 0)) (.constant 0) = true := by decide
