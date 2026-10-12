import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkStep (.right .s (.app .i .k) .k (.i .s)) (.app .s (.app .i .k)) (.app .s .k) = true := by decide
