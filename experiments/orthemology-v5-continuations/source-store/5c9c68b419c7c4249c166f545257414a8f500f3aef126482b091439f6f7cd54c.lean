import FullControllerSource
import RationalGateSufficiency
set_option autoImplicit false

namespace Orthemology.RuntimeBridge.PhaseUpdate.FullController
open HiddenParity HiddenParity.Sufficiency HiddenParity.Necessity HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding
open MeasureTheory

/-- This constructor changes only the tolerance to a literal computable positive
rational separation value. It does not preserve an arbitrary old controller's
policy decisions or the opaque tolerance inside the explicit winning record. -/
def withComputedTolerance (c : Config) : Config := { c with
  toleranceNumerator := (RationalGate.tolerance c.kernel c.initialSupport).num.natAbs
  toleranceDenominator := (RationalGate.tolerance c.kernel c.initialSupport).den }

theorem computed_tolerance_exact (c : Config) :
    ((withComputedTolerance c).toleranceNumerator : ℚ)/(withComputedTolerance c).toleranceDenominator =
      RationalGate.tolerance c.kernel c.initialSupport := by
  let q := RationalGate.tolerance c.kernel c.initialSupport
  have hq : 0 < q := (RationalGate.tolerance_spec _ _).1
  have hn : 0 ≤ q.num := le_of_lt (Rat.num_pos.mpr hq)
  have ha : (q.num.natAbs : ℤ) = q.num := Int.natAbs_of_nonneg hn
  have hrat : (q.num.natAbs : ℚ) = (q.num : ℚ) := by
    calc
      (q.num.natAbs : ℚ) = ((q.num.natAbs : ℤ) : ℚ) := by rw [Int.cast_natCast]
      _ = (q.num : ℚ) := congrArg (fun z : ℤ => (z : ℚ)) ha
  change (q.num.natAbs : ℚ)/q.den = q
  rw [hrat,Rat.num_div_den]

theorem computed_tolerance_certificate (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) :
    Certificate (withComputedTolerance c) menu priority := by
  exact ⟨hc.selectors,(RationalGate.tolerance c.kernel c.initialSupport).den_pos,
    hc.rowDenominator_pos,hc.row_exact⟩

/-- Once supplied finite selectors are bound, the full literal source has the
computed rational tolerance and the retained generator's original success
proof. No arbitrary-real comparison oracle or whole-history equality is assumed. -/
theorem computed_policy_parity (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ)
    (hs : c.initialState ∈ winningRegion c.kernel menu priority c.initialSupport)
    (σ : Bool) (hσ : σ ∈ c.initialSupport) (d : Bool × Bool) :
    ∀ᵐ H ∂markovHistoryLaw c.kernel σ c.initialState
      (fun (_ : Unit) h => policy (withComputedTolerance c) menu priority h) (Measure.dirac ()),
      ParitySuccess (priority σ) (historyAction d H) := by
  have he : (fun (_ : Unit) h => policy (withComputedTolerance c) menu priority h) =
      generatedPhasePolicy c.kernel menu priority c.initialSupport c.initialState c.fallbackModel c.fallbackAction
        (RationalGate.reject c.kernel (RationalGate.tolerance c.kernel c.initialSupport)) := by
    funext u h
    cases u
    unfold policy
    rw [computed_tolerance_exact]
    rfl
  rw [he]
  exact RationalGate.rational_gate_parity c.kernel menu priority c.initialSupport c.initialState
    c.fallbackModel c.fallbackAction hs σ hσ d

end Orthemology.RuntimeBridge.PhaseUpdate.FullController
