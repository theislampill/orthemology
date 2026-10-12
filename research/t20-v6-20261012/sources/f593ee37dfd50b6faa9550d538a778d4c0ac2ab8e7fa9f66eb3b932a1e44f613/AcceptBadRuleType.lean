import CertificateControls
open CertificateCodeValidity.Controls
example : CertificateCodeValidity.certValid 12 (AuxiliaryCodeComputability.pack 13 [SourceFamilyComputability.leaf 0, SourceFamilyComputability.leaf 0]) = true := by
  rw [rejectBadRuleTy]
  decide
