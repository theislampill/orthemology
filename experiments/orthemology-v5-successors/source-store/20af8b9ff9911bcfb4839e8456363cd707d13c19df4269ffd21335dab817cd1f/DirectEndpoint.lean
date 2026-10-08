import SubmittedFamily
import DirectActualLaw
import RationalTest

/-! Direct witness-parametric endpoint. The executable function reads the body
and rational input; all success claims are subsequently proved about that exact
function under the original actual observation-history law. -/
namespace OrthemicCertificate.Direct
open MeasureTheory
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
variable {q n k : ℕ}

/-- Dimension-zero cases are refused by Input.Valid before this total history
policy is constructed. Its proof argument carries no policy-success premise. -/
def compile (I : Input q n k) (hI : I.Valid) (B : Support q) (s : Fin n)
    (c : Body q n k) : Unit → History (Fin k) (Fin n) → Fin k :=
  letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
  generatedPhasePolicy (I.kernel hI) I.menu I.priority (submittedFamily c) B s
    ⟨0,hI.1.1⟩ ⟨0,hI.1.2.2.1⟩ (rationalReject I (tolerance I B))

theorem compiled_measurable (I : Input q n k) (hI : I.Valid) (B : Support q) (s : Fin n)
    (c : Body q n k) :
    Measurable (fun z : Unit × History (Fin k) (Fin n) => compile I hI B s c z.1 z.2) := by
  exact measurable_of_countable _

theorem compiled_lawful (I : Input q n k) (hI : I.Valid) (B : Support q) (s : Fin n)
    (c : Body q n k) (hc : check I c B s = true) :
    letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
    Lawful (I.kernel hI) I.menu B s (compile I hI B s c) (Measure.dirac ()) := by
  letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
  obtain ⟨hv,hB,N,hN,hNB,hs⟩ := (check_iff I c B s).mp hc
  letI : CertifiedStageFamily (I.kernel hI) I.menu I.priority (submittedFamily c) :=
    submitted_certified hv
  have hstate : s ∈ (submittedFamily c).states B :=
    (mem_submittedStates c B s).mpr ⟨N,hN,hNB,hs⟩
  exact generatedPhasePolicy_lawful (I.kernel hI) I.menu I.priority (submittedFamily c)
    B s hstate ⟨0,hI.1.1⟩ ⟨0,hI.1.2.2.1⟩ (rationalReject I (tolerance I B))

/-- Correctness is universal over submitted accepted bodies and live actual
models; this is not existence of some inherited generated policy. -/
theorem compiled_parity (I : Input q n k) (hI : I.Valid) (B : Support q) (s : Fin n)
    (c : Body q n k) (hc : check I c B s = true) (d : Pair n k) :
    letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
    ∀ σ ∈ B, ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) σ s (compile I hI B s c) (Measure.dirac ()),
      ParitySuccess (I.priority σ) (historyAction d H) := by
  letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
  obtain ⟨hv,hB,N,hN,hNB,hs⟩ := (check_iff I c B s).mp hc
  letI : CertifiedStageFamily (I.kernel hI) I.menu I.priority (submittedFamily c) :=
    submitted_certified hv
  have hstate : s ∈ (submittedFamily c).states B :=
    (mem_submittedStates c B s).mpr ⟨N,hN,hNB,hs⟩
  have htest : rationalReject I (tolerance I B) =
      empiricalReject (I.kernel hI) (tolerance I B : ℝ) := by
    funext θ r h
    exact rationalReject_eq_empiricalReject I hI (tolerance I B) θ r h
  have hpos : (0 : ℝ) < (tolerance I B : ℝ) := by exact_mod_cast tolerance_positive I B
  intro σ hσ
  unfold compile
  rw [htest]
  exact generatedPhasePolicy_parity (I.kernel hI) I.menu I.priority (submittedFamily c) B s
    ⟨0,hI.1.1⟩ ⟨0,hI.1.2.2.1⟩ (tolerance I B : ℝ) hpos hstate σ hσ
    (tolerance_real_separates I hI B σ hσ) d

end OrthemicCertificate.Direct
