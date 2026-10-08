import UnaryNormalForm
open P01AC.UnaryIdentity
example : verifyCertificate .variable .variable ⟨[0, 1], [none, some 1]⟩ = true := by decide
