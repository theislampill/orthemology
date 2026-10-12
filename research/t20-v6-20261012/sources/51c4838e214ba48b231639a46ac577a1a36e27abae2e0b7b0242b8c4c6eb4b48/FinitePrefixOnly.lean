import CommonObservationFiniteActions
import CommonObservationControls
open MeasureTheory Filter Set
open Orthemology.Tranche2.CommonObservationBoundary CommonObservationControls
open Orthemology.Tranche2.FiniteAlphabetQuery
example : ∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  exact common_action_of_dominated_eventual_success (Measure.dirac (fun _ : ℕ => true))
    pathLaw detector bitTarget (fixed_reference_prefix_domination 1) path_success
