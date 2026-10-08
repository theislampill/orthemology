import NativeControllerControls
import SubmittedFamily
import DirectActualLaw
import RationalTest

/-! Direct witness-parametric endpoint. The executable function reads the body
and rational input; all success claims are subsequently proved about that exact
function under the original actual observation-history law. -/
namespace OrthemicCertificate.DirectWitnessIgnored
open OrthemicCertificate.Direct
open MeasureTheory
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
variable {q n k : ℕ}

/-- Dimension-zero cases are refused by Input.Valid before this total history
policy is constructed. Its proof argument carries no policy-success premise. -/
def compile (I : Input q n k) (hI : I.Valid) (B : Support q) (s : Fin n)
    (c : Body q n k) : Unit → History (Fin k) (Fin n) → Fin k :=
  letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
  generatedPhasePolicy (I.kernel hI) I.menu I.priority (submittedFamily []) B s
    ⟨0,hI.1.1⟩ ⟨0,hI.1.2.2.1⟩ (rationalReject I (tolerance I B))


def checkedAction {q n k : ℕ} (I : Input q n k) (B : Support q) (s : Fin n)
    (c : Body q n k) (h : List (Fin k × Fin n)) : Option (Fin k) :=
  if hc : check I c B s = true then some (compile I ((check_iff I c B s).mp hc).1.1 B s c () h)
  else none
end OrthemicCertificate.DirectWitnessIgnored
open OrthemicCertificate.Fixtures
#guard OrthemicCertificate.DirectWitnessIgnored.checkedAction choices {0} 1 [choicesNode 2 1] [] = some 1
