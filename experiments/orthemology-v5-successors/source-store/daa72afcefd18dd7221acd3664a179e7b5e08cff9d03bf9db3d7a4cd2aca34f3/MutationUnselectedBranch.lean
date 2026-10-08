import NecessityControls
open HiddenChange HiddenChangeNecessityTests MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic HiddenParity.ResidualSeed
-- False premise deletion: a positive history cannot license an unselected action.
example : PositiveSelected (0 : State 1) (Measure.dirac ()) twoActions [] (0,1) := by
  simp [PositiveSelected,SelectedSeeds,CompatibleSeeds,ActionCompatible,pairPolicy,twoActions]
