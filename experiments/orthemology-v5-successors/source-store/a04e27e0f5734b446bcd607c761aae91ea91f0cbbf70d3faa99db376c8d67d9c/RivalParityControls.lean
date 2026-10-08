import HiddenChangeRivalParity

open MeasureTheory ProbabilityTheory Set Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic
open HiddenChange

#check all_zeroCompatible_measurable
#check exists_positive_fiber_inter
#check positive_compatible_recurrent_prefix
#check fixedConditional_surviving_recurrent_eq
#check positive_compatible_recurrent_even
#print axioms all_zeroCompatible_measurable
#print axioms exists_positive_fiber_inter
#print axioms positive_compatible_recurrent_prefix
#print axioms fixedConditional_surviving_recurrent_eq
#print axioms positive_compatible_recurrent_even

/-- Interface control: compatibility is only inside the positive event. There
is no global law-safety, fairness, no-exit, or assumed transfer hypothesis. -/
example {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (d : Pair n k)
    (hWin : ∀ κ, ∀ᵐ H ∂fixedLaw I hI κ s ρ π, TaggedParity I d H)
    (κ : ChangeIndex) (E : PairSet n k)
    (hp : 0 < fixedPhysicalLaw I hI κ s ρ π
      {H | recurrentSet (historyAction d H) = E ∧ ∀ t, ZeroCompatible I (H t)}) :
    ∀ σ, Match I.row (finalMode κ) σ E → EvenMinimum I σ E :=
  positive_compatible_recurrent_even I hI s ρ π hπ d hWin κ E hp
