import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkFinite (.reduce (.app .i .i) .i idType typedII (.refl .i)) .i idType = true := by decide
