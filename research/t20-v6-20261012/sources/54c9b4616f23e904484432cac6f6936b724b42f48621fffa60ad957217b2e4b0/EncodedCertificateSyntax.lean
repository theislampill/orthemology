import CertificateCompleteness
import CodecDeriveEncodable
set_option maxRecDepth 32768
set_option maxHeartbeats 32000000
namespace JointCertificates
deriving instance Encodable for OrthemologyV2.Term
deriving instance Encodable for OrthemologyV2.TypeCode
deriving instance Encodable for P01D.Poly
deriving instance Encodable for P01AC.Ty
deriving instance Encodable for AuxiliaryCertificates.StepCert
deriving instance Encodable for AuxiliaryCertificates.RedCert
deriving instance Encodable for AuxiliaryCertificates.FiniteCert
end JointCertificates
