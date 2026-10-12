import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : mixed (P01F.cons (.var 5) Poly.var) Ty.param (Ty.all (.identity .raw (.var 0) (.var 1))) = Ty.all (.identity .raw (.var 0) (.var 6)) := by rfl
