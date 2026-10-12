import MixedTypeSubstitution
open P01D P01AC CodedPolyTransformations CodedMixedTransformations
-- A type binder does not shift the term substitution image.
example : mixed (finiteEnv [Poly.var 4] 0) (finiteTyEnv [] true 0)
    (Ty.all (.identity .raw (.var 0) (.var 0))) =
    Ty.all (.identity .raw (.var 5) (.var 5)) := by rfl
