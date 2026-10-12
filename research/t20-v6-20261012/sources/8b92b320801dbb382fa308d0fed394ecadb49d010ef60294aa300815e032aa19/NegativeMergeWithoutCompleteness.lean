import InfiniteRootlessBranch
open Orthemology.Tranche3.ProductiveCompleteness
open Orthemology.Tranche6.ConnectedUnity
open Orthemology.Tranche6.ConnectedUnity.Controls
open Orthemology.Tranche6.ConnectedUnity.InfiniteControls
example : ∃ g, LocalCover Merge g 2 := by
  simp only [LocalCover, Below, Merge]
  decide
