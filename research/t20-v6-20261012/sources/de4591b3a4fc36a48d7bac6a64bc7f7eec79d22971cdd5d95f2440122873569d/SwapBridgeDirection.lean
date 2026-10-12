import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkPoly (.bridge .i .k) (.app (.atom .i) (.atom .k)) (.atom (.app .i .k)) = true := by decide
