import IndependentSourceControls
open AuxiliaryCertificates OrthemologyV2 OrthemologyV3 P01D P01AC IndependentAuxiliarySourceReview
set_option maxRecDepth 8192
example : checkFinite instCert .i (.all (.arrow (.var 2) (.var 2))) = true := by decide
