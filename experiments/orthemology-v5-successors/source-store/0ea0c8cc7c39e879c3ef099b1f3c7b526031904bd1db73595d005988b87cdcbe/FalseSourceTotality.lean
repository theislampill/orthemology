import PolicySynthesisReduction
open PolicySynthesis
-- The witness search is not total when every matrix entry is false.
example : (matrixSearch (fun _ => false) (Nat.pair 0 (Nat.pair 0 0))).Dom := by
  simp [matrixSearch_dom_pair]
