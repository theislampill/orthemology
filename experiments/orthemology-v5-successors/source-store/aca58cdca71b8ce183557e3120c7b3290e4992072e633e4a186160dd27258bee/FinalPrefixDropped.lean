import LookaheadBoundary
open EffectiveRenewal EffectiveRenewal.Lookahead
-- The final-prefix check is substantive, not implied by base admission.
example : ¬ ∃ s, diagonalTree s ∧ ¬ lookaheadTree (fun _ => 1) s := by
  intro _
  exact final_prefix_check_is_substantive
