import NativeControllerControls
import CertificateData
import EmpiricalTestLaw

/-! Exact rational empirical testing and a computed positive separation. -/
namespace OrthemicCertificate.DirectTruncated
open HiddenParity HiddenParity.Sufficiency HiddenParity.Empirical HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding
variable {q n k : ℕ}

/-- Integer acquired count; history is never truncated or reset. -/
def symbolCount (e : Pair n k) (y : Fin n) : History (Pair n k) (Fin n) → ℕ
  | [] => 0
  | (f,z) :: h => (if f = e ∧ z = y then 1 else 0) + symbolCount e y h

def rationalFrequency (e : Pair n k) (y : Fin n) (h : History (Pair n k) (Fin n)) : ℚ :=
  (symbolCount e y h : ℚ) / (actionCount e h : ℚ)

def rationalReject (I : Input q n k) (ε : ℚ) (θ : Fin q) (r : ℕ)
    (h : History (Pair n k) (Fin n)) : Bool :=
  decide (∃ e : Pair n k, ∃ y : Fin n,
    r < actionCount e h ∧ ε ≤ |rationalFrequency e y (h.take 1) - I.row θ e y|)


open OrthemicCertificate.Fixtures
#guard !(rationalReject latent (1/6) 0 0 [((0,0),1),((0,0),0),((0,0),0)])
end OrthemicCertificate.DirectTruncated
