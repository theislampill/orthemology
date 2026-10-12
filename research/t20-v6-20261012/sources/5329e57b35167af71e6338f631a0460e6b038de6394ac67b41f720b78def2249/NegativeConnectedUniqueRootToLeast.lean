import InfiniteRootlessBranch
open Orthemology.Tranche3.ProductiveCompleteness
open Orthemology.Tranche6.ConnectedUnity
open Orthemology.Tranche6.ConnectedUnity.Controls
open Orthemology.Tranche6.ConnectedUnity.InfiniteControls
local instance : Decidable (∃ g, LeastAncestor Fork g) := isFalse unique_root_connected_without_least.2.2
example : ∃ g, LeastAncestor Fork g := by
  decide
