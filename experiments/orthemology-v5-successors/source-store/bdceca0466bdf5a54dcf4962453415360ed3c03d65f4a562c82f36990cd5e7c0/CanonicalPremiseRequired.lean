import UnaryFiniteDescription
open P01AC.UnaryIdentity
-- These two descriptions denote the same function but are unequal data.
example : (Description.mk [0, 1] []) = (Description.mk [0, 1, 0] [none]) := by decide
