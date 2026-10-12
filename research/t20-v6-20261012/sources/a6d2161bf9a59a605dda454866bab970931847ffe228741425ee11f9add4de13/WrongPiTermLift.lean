import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : mixed (P01F.cons (.var 5) Poly.var) Ty.param (Ty.pi .raw (.identity .raw (.var 1) (.var 0))) = Ty.pi .raw (.identity .raw (.var 5) (.var 0)) := by rfl
