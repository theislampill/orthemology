import InfiniteRootlessBranch
open Orthemology.Tranche3.ProductiveCompleteness
open Orthemology.Tranche6.ConnectedUnity
open Orthemology.Tranche6.ConnectedUnity.Controls
open Orthemology.Tranche6.ConnectedUnity.InfiniteControls
example : ∃ x, (fun (_ _ : Unit) => False) () x := by
  decide
