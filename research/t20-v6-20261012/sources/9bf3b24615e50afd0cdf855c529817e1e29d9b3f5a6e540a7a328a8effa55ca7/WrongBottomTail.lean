import MixedSpecializations
open P01AC
-- Finite typeImages has a Bottom default, unlike single type instantiation.
example : tsubst (typeImages [Ty.raw]) (Ty.all (.all (.param 3))) = Ty.all (.all (.param 2)) := by rfl
