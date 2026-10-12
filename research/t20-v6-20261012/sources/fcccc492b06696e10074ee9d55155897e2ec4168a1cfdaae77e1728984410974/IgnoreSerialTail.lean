import CertificateControls
open CertificateCodeValidity.Controls
example : CertificateCodeValidity.certValid 14 (AuxiliaryCodeComputability.pack 1 [Encodable.encode (JointCertificates.SerialCert.node JointCertificates.Rule.CtxJ_nil JointCertificates.SerialCertList.nil),0]) = true := by
  rw [rejectBadSerialRight]
  decide
