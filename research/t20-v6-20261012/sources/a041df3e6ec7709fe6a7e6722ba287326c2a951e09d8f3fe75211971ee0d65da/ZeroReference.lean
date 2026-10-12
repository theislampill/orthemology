import CommonObservationFiniteActions
import CommonObservationControls
open MeasureTheory Filter Set
open Orthemology.Tranche2.CommonObservationBoundary CommonObservationControls
open Orthemology.Tranche2.FiniteAlphabetQuery
example : ∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  exact common_action_of_dominated_eventual_success (0 : Measure Bool)
    (fun _ : Bool => 0) (fun _ω _n => false) bitTarget
    zero_reference_counterexample.1 zero_reference_counterexample.2.1
