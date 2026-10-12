import CertificateDescriptions
namespace CertificateDomainReview
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability CertificateCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 1000000
-- Local shape alone admits invalid children. These controls intentionally do not assert global validity.
example : localShape stepCertDescription (pack 0 [leaf 0]) = true := by decide
example : localShape claimDescription (pack 0 [leaf 1]) = true := by decide
example : localShape serialCertListDescription (pack 1 [0,0]) = true := by decide
example : localChildren serialCertListDescription (pack 1 [0,0]) = [(13,0),(14,0)] := by decide
example : localShape stepCertDescription (pack 5 []) = false := by decide
example : localShape ruleDescription (pack 63 []) = false := by decide
example : localShape stepCertDescription (pack 0 [node 0 0]) = false := by decide
example : localShape stepCertDescription (node (leaf 0) (node (leaf 0) (leaf 1))) = false := by decide
example : encode OrthemologyV2.Term.zero = encode OrthemologyV2.TypeCode.bottom := rfl
-- Sort-indexed languages overlap numerically; no global sort-disjointness is admissible.
end CertificateDomainReview
