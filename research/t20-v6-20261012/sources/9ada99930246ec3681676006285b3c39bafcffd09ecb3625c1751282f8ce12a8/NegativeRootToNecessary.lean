import UpstreamGround
open Orthemology.Tranche3.SourceIdentity
open Orthemology.Tranche6.UpstreamGround.FiniteControls
example : Necessary BruteEx () := by
  simp only [Necessary, BruteEx]
  decide
