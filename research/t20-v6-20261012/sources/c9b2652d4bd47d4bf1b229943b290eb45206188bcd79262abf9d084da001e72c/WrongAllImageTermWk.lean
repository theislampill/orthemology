import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : mixed Poly.var (P01F.cons (Ty.identity (.param 2) (.var 0) (.var 3)) Ty.param) (Ty.all (.param 1)) = Ty.all (.identity (.param 3) (.var 1) (.var 4)) := by rfl
