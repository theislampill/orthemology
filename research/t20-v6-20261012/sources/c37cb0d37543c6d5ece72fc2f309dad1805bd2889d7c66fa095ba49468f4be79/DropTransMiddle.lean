import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkPoly (.trans (.var 0) (.var 1) (.var 0) (.refl (.var 0)) (.refl (.var 0))) (.var 0) (.var 0) = true := by decide
