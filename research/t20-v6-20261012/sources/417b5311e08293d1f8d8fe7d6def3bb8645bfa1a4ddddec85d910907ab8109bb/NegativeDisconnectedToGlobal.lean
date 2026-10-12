import InfiniteRootlessBranch
open Orthemology.Tranche3.ProductiveCompleteness
open Orthemology.Tranche6.ConnectedUnity
open Orthemology.Tranche6.ConnectedUnity.Controls
open Orthemology.Tranche6.ConnectedUnity.InfiniteControls
example : ∃ g, LeastAncestor Split g := by
  simp only [LeastAncestor, Below, Split]
  decide
