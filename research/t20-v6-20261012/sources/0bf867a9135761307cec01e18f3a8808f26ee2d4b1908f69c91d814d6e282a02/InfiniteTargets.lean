import CommonObservationFiniteActions
import CommonObservationControls
open MeasureTheory Filter Set
open Orthemology.Tranche2.CommonObservationBoundary CommonObservationControls
open Orthemology.Tranche2.FiniteAlphabetQuery
example : ∃ a : ℕ, ∀ θ : ℕ, θ ≤ a := by
  exact common_action_of_dominated_eventual_success (Measure.dirac () : Measure Unit)
    (fun _ : ℕ => Measure.dirac ()) (fun _ω n => n) (fun θ => {a | θ ≤ a})
    (fun _ => Measure.AbsolutelyContinuous.rfl) infinite_targets_same_probability_counterexample.1
