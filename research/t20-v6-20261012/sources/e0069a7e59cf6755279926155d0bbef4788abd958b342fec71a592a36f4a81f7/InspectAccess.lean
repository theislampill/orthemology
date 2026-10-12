import FamilyComputability
open private Mathlib.Deriving.Encodable.S Mathlib.Deriving.Encodable.S.encode Mathlib.Deriving.Encodable.S.decode from CodecDeriveEncodable
open private JointCertificates.encodableTerm_toS JointCertificates.encodableTerm_fromS from EncodedCertificateSyntax
#check Mathlib.Deriving.Encodable.S
#check JointCertificates.encodableTerm_toS
