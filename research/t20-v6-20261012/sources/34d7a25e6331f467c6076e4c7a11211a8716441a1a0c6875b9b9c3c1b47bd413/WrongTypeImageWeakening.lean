import MixedTypeSubstitution
open P01D P01AC CodedPolyTransformations CodedMixedTransformations
-- A stored type image's free term variable must shift beneath pi.
example : mixed (finiteEnv [] 0) (finiteTyEnv [Ty.identity .raw (.var 0) (.var 0)] true 0)
    (Ty.pi .raw (.param 0)) = Ty.pi .raw (.identity .raw (.var 0) (.var 0)) := by rfl
