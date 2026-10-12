import InfiniteRootlessBranch
open Orthemology.Tranche3.ProductiveCompleteness
open Orthemology.Tranche6.ConnectedUnity
open Orthemology.Tranche6.ConnectedUnity.Controls
open Orthemology.Tranche6.ConnectedUnity.InfiniteControls
local instance : Decidable (∃ g, LocalCover Fork g Item.target) := isFalse target_no_local_cover
example : ∃ g, LocalCover Fork g Item.target := by
  decide
