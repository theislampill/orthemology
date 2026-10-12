import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : mixed Poly.var (P01F.cons (Ty.identity (.param 2) (.var 0) (.var 3)) Ty.param) (Ty.sigma .raw (.param 0)) = Ty.sigma .raw (.identity (.param 2) (.var 0) (.var 3)) := by rfl
