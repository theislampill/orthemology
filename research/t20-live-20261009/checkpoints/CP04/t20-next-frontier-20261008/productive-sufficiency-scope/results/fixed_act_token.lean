import ScopeTest
open ProductiveSufficiencyScope
open Orthemology.Tranche3.SourceIdentity
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open RouteProbability
example : ∀ w, actOccurs w .left := by
  simp only [actOccurs]
  decide
