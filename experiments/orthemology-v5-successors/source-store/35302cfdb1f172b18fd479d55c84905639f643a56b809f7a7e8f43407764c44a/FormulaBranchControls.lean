import SignedService
import SmallFixtures
import CertificateFixtures
open OrthemicCertificate OrthemicCertificate.Signed OrthemicCertificate.Fixtures

private def generatedLocal (I : Input q n k) (c : Body q n k) (B : Support q) (s : Fin n) :=
  refutationCandidate Atom.eval (positiveFormula I c B s)

-- The full-row rival implication changes exactly when the rational rows match.
#guard (positiveFormula latent [latentNode] {0,1} 0).eval Atom.eval
#guard !((positiveFormula latentEqualRows [latentNode] {0,1} 0).eval Atom.eval)
#guard localReject latentEqualRows {0,1} 0 [latentNode] (generatedLocal latentEqualRows [latentNode] {0,1} 0)
#guard !(localReject latent {0,1} 0 [latentNode] (generatedLocal latent [latentNode] {0,1} 0))
#guard (componentFormula latent {0,1} 0 Finset.univ (latentComponent 0) 0).eval Atom.eval
#guard !((componentFormula latentEqualRows {0,1} 0 Finset.univ (latentComponent 0) 0).eval Atom.eval)
-- Missing one possible live-support child requires a true structural rejection.
#guard !((positiveFormula reveal [child₀,parent] {0,1,2} 0).eval Atom.eval)
#guard localReject reveal {0,1,2} 0 [child₀,parent] (generatedLocal reveal [child₀,parent] {0,1,2} 0)
#guard (positiveFormula reveal revealedBody {0,1,2} 0).eval Atom.eval
#guard !(localReject reveal {0,1,2} 0 revealedBody (generatedLocal reveal revealedBody {0,1,2} 0))
-- An even-minimum failure has a locally checked finite refutation.
#guard localReject OrthemicCertificate.Signed.Fixtures.oddInput {0} 0
  OrthemicCertificate.Signed.Fixtures.singletonBody
  (generatedLocal OrthemicCertificate.Signed.Fixtures.oddInput
    OrthemicCertificate.Signed.Fixtures.singletonBody {0} 0)
-- A single leaf cannot stand in for an aggregate body check.
#guard !(localReject reveal {0,1,2} 0 [child₀,parent] .leaf)
-- Primitive equalities are recomputed, including true-atom forgery rejection.
#guard !(rejectCheck (Atom.eval (q := 1) (n := 1) (k := 1))
  (.literal (.ratEq 1 1) true) .leaf)
#eval (localReject latentEqualRows {0,1} 0 [latentNode]
  (generatedLocal latentEqualRows [latentNode] {0,1} 0),
  localReject reveal {0,1,2} 0 [child₀,parent] (generatedLocal reveal [child₀,parent] {0,1,2} 0))
