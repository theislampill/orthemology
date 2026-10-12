import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : tsubst (typeImages []) (Ty.all (.all (.param 2))) = Ty.all (.all (.param 0)) := by rfl
