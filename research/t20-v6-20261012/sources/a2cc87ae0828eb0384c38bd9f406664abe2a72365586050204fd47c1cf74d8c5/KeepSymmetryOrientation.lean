import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkPoly (.symm (.app (.atom .i) (.var 0)) (.var 0) (.i (.var 0))) (.app (.atom .i) (.var 0)) (.var 0) = true := by decide
