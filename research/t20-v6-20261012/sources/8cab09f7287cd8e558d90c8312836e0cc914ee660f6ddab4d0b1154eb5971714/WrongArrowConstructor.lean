import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : fin (TypeCode.arrow (.var 0) (.var 1)) = Ty.sigma (.param 0) (.param 1) := by rfl
