import EndpointLawfulnessControls
import EndpointFixtures
import HiddenChangeBinding
import HiddenChangeControllerEndpoint
import HiddenChangeNecessity

/-! Signed semantic endpoint for the finite rational one-hidden-change class.
The checked body, literal public-history controller, actual changing-mode laws,
and arbitrary-private-seed necessity are the imported proved constructions.
`WinsAll` expresses parity only. Measurability and all-history common-menu
lawfulness are independent, retained obligations. No runtime correspondence
between this Lean body and the Python certificate format is asserted. -/

open HiddenChange EndpointLawfulness HiddenChangeEndpointTests
noncomputable section
open MeasureTheory ProbabilityTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic
namespace EndpointSemanticMutation
universe uR uZ
variable {n k : ℕ} [NeZero n] [NeZero k]

omit [NeZero n] [NeZero k] in
/-- The source-labelled helper is exactly the original public-history contract. -/
theorem policyLawful_iff_allHistoryLawful {R : Type uR}
    (I : Input n k) (s : State n) (π : Policy R n k) :
    PolicyLawful I s π ↔ AllHistoryLawful I s π := by
  constructor
  · intro hlaw r h
    let q : PairHistory n k := h.map (fun z => ((s,z.1),z.2))
    have hh := hlaw r q
    have he : erasePairSources q = h := by
      simp [q,erasePairSources,List.map_map,Function.comp_def]
    have hs : currentState s q = currentObserved s h := by cases h <;> rfl
    simpa only [he,hs] using hh
  · intro hlaw r h
    have hh := hlaw r (erasePairSources h)
    cases h <;> exact hh

/-- One specified private-seed policy satisfies all three semantic obligations.
`uZ` is the universe of the adversary's private seed; `uR` is the policy seed's
universe. The probability hypothesis on rho is supplied by endpoint theorems. -/
def LawfulMeasurableWinner {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (s : State n) (ρ : Measure R)
    (π : Policy R n k) (d : Pair n k) : Prop :=
  Measurable (fun z : R × PublicHistory n k => π z.1 z.2) ∧
  True ∧ WinsAll.{uZ} I hI s ρ π d


example : ¬ LawfulMeasurableWinner.{0,0} forbiddenEven
    (by decide +kernel : Admissible forbiddenEven).1 0 (Measure.dirac ()) choosesForbidden (0,0) := by
  have hw : LawfulMeasurableWinner.{0,0} forbiddenEven
      (by decide +kernel : Admissible forbiddenEven).1 0 (Measure.dirac ()) choosesForbidden (0,0) :=
    ⟨measurable_of_countable _, trivial, forbidden_winsAll⟩
  simp only [hw, not_true_eq_false]
end EndpointSemanticMutation
