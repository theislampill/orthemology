import AllSyntax
open P01D P01AC OrthemologyV2 OrthemologyV3
example : trename Nat.succ (Ty.identity (.param 0) (.var 0) (.var 3)) = Ty.identity (.param 1) (.var 1) (.var 4) := by rfl
