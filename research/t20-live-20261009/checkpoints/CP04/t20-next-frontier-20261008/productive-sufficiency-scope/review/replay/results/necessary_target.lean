import ScopeTest
open ProductiveSufficiencyScope
open Orthemology.Tranche3.SourceIdentity
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open RouteProbability
example : Necessary positive.existsAt true := by
  simp only [Necessary, positive]
  decide
