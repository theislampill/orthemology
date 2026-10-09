import ScopeTest
open ProductiveSufficiencyScope
open Orthemology.Tranche3.SourceIdentity
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open RouteProbability
example : endpoint oneRoute .A (realization true) ≠ ∅ := by
  rw [failure_endpoint]
  decide
