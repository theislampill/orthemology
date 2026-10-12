import CertificateSeparation
import IdentityReviewControls

namespace ReviewHenkinCertificate
open P01AC P01D
open P01AC.ExtensionalRepair (HasE)
open P01AC.UnaryCertificate (HasC)

/-- A literal checked witness, without claiming either calculus includes the other. -/
theorem exact_certificate_only_witness :
    HasC [] (.atom .i) ReviewHenkinIdentity.literalIdentity ∧
    (∀ q : Poly, ¬ HasE [] q ReviewHenkinIdentity.literalIdentity) :=
  ⟨T20SourceIndependence.inherited_certificate_positive,
    HomogeneousOriginalIdentity.literal_original_identity_uninhabited⟩

theorem no_type_preserving_compiler (compile : Poly → Poly) :
    ¬ (∀ {p : Poly} {A : Ty}, HasC [] p A → HasE [] (compile p) A) := by
  intro h
  exact exact_certificate_only_witness.2 (compile (.atom .i))
    (h exact_certificate_only_witness.1)

#print axioms exact_certificate_only_witness
#print axioms no_type_preserving_compiler
end ReviewHenkinCertificate
