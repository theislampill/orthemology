import CommonObservationFiniteActions
import CommonObservationControls
open MeasureTheory Filter Set
open Orthemology.Tranche2.CommonObservationBoundary CommonObservationControls
open Orthemology.Tranche2.FiniteAlphabetQuery
example [NeZero (Measure.count : Measure Bool)] : ∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  exact common_action_of_dominated_eventual_success (Measure.count : Measure Bool)
    (fun b => Measure.dirac b) (fun ω _n => ω) bitTarget
    reversed_domination_counterexample.1 reversed_domination_counterexample.2.1
