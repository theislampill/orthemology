import LookaheadBoundary
open EffectiveRenewal EffectiveRenewal.Lookahead
-- The base-T supplementary witness cannot be promoted to an L_1 witness.
example : ∀ s, lookaheadTree (fun _ => 1) s →
    ∃ w, BaseWitness (fun _ => 1) s w ∧ lookaheadTree (fun _ => 1) w :=
  one_step_recursive_witness_failure
