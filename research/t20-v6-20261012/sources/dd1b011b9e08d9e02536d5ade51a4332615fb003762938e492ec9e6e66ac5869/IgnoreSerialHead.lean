import CertificateControls
open CertificateCodeValidity.Controls
example : CertificateCodeValidity.certValid 14 (AuxiliaryCodeComputability.pack 1 [0, Encodable.encode JointCertificates.SerialCertList.nil]) = true := by
  rw [rejectBadSerialLeft]
  decide
