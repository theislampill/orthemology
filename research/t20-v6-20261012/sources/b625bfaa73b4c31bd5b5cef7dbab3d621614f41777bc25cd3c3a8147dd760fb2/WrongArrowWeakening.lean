import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : arr Ty.raw (.identity .raw (.var 0) (.var 3)) = Ty.pi .raw (.identity .raw (.var 0) (.var 3)) := by rfl
