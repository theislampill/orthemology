import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : instantiateType (TypeCode.all (.all (.var 2))) (TypeCode.var 0) = TypeCode.all (.all (.var 1)) := by rfl
