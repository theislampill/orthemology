import CertificateControls
open CertificateCodeValidity.Controls
example : CertificateCodeValidity.certValid 11 (AuxiliaryCodeComputability.pack 0 [SourceFamilyComputability.leaf 1]) = true := by
  rw [rejectBadClaimTel]
  decide
