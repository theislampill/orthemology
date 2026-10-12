import UpstreamGround
open Orthemology.Tranche3.SourceIdentity
open Orthemology.Tranche6.UpstreamGround.FiniteControls
example : ∃ g, Split g Item.leftEffect ∧ Split g Item.rightEffect := by
  simp only [Split]
  decide
