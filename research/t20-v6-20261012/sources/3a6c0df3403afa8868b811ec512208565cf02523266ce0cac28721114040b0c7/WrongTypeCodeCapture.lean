import TypeCodeSubstitution
open OrthemologyV2 OrthemologyV3
-- The substituted free type variable must shift under all.
example : instantiateType (TypeCode.all (.var 1)) (TypeCode.var 4) = TypeCode.all (.var 4) := by rfl
