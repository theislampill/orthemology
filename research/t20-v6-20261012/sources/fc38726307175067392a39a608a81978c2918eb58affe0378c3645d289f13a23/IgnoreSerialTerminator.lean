import CertificateControls
open CertificateCodeValidity.Controls
example : CertificateCodeValidity.certValid 14 (SourceFamilyComputability.node (SourceFamilyComputability.leaf 0) (SourceFamilyComputability.leaf 1)) = true := by
  rw [rejectSerialTerminator]
  decide
