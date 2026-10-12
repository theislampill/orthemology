import UnaryCertificateSyntax
import OriginalIdentityNoninhabitation

/- Existing T16 certificate rule versus the unchanged HasE judgment.
No new source rule or calculus is introduced. -/
namespace T20SourceIndependence
open P01AC P01D
open P01AC.EffectiveCompleteness (N)
open P01AC.UnaryIdentity
open P01AC.UnaryIdentity.IntensionalBoundary (variableExpr redundantExpr)
open P01AC.UnaryCertificate (HasC)
open P01AC.ExtensionalRepair (HasE)

 theorem inherited_certificate_positive :
    HasC [] (.atom .i) (.identity (arr N N) variableExpr.closed redundantExpr.closed) := by
  apply HasC.certified variableExpr redundantExpr (makeCertificate variableExpr)
  · exact P01AC.UnaryCertificate.form_inclusion (identity_formed variableExpr redundantExpr)
  · exact makeCertificate_complete _ _ ((identityCheck_iff_valid _ _).mp
      P01AC.UnaryIdentity.IntensionalBoundary.checker_accepts)

 theorem no_endpoint_preserving_translation :
    ¬ (∀ {p : Poly} {A : Ty}, HasC [] p A → ∃ q : Poly, HasE [] q A) := by
  intro transport
  obtain ⟨q,hq⟩ := transport inherited_certificate_positive
  exact HomogeneousOriginalIdentity.literal_original_identity_uninhabited q hq

#print axioms inherited_certificate_positive
#print axioms no_endpoint_preserving_translation
end T20SourceIndependence
