import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkLookup lookup2 [.raw,.bottom,A 0] 2 (A 3) = true := by decide
