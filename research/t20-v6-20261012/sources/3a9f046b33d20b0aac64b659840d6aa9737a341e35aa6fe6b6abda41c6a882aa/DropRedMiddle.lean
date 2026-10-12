import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkRed (.tail (.app .i .k) .s .s (.i .k) (.refl .s)) (.app .i .k) .s = true := by decide
