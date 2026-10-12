# Fair-input Mealy measure bridge

Goal: connect the already kernel-checked finite mismatch theorem to actual fair infinite-product input measure and total atomic output mass.

1. Prove prefix-cylinder probabilities from Q8Measure.fairCantor_cylinder and measurability of finite-state execution.
2. Encode actual successive length-L blocks as accepted BoundedPaths.words and prove cylinder-union probability bound using their checked cardinality bound.
3. Apply the geometric limit to every fixed-output fibre avoiding D.
4. Prove every D-hitting input has an atomic output via its positive prefix cylinder; use countability of positive atoms to prove the converse modulo null sets and equality of atomic mass and hitting probability.
5. Expose only genuinely proved computability consequences; keep finite Markov-chain rationality separately labelled unless its required bridge is completed.

Verification: Lean 4.19.0, pinned mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b; compile with -j1, print axioms of all substantive bridge declarations; no sorry, axiom, source changes, or cache copies. Tests begin as unproved target declarations and are completed by kernel-checkable proof terms.
