# Corrections incorporated during consolidation

## Finite-memory realization under adversarial memory exposure

A fresh mathematical review identified an implementation boundary in the stochastic migration memory bound. The source theorem concerns a behavioral action kernel sampled freshly from the current observation/action history. If a different finite-state realization pre-samples future action coins into memory and the destination adversary sees that memory, equality of unexposed controller laws does not justify substituting the realization in the theorem.

The SR1 and SR2 memory bounds now require deterministic history-updated source memory and fresh current-action draws, or a separate proof of behavioral-kernel preservation under the declared memory exposure. The main history-based construction is unchanged. The finite checker certifies the supplied plant/interface coupling contract, not implementation equivalence of an arbitrary randomized controller.

## P14 replay dependency

A fresh extraction replay found that the immutable P14 probe imports `restoration.py` from its surrounding control research directory. Its manifest and seven unit tests passed unchanged, but the nested archive alone was not a standalone probe environment.

The complete tranche supplies that dependency through an explicit replay search path and records its SHA-256 in the verification report and receipt. P14's existing archive was not modified. Replaying the complete bundle verifies the predecessor's 15 manifest files before running it from a temporary extracted copy.

## Scope

These are documented proof-interface and reproducibility repairs. They neither change the canonical repository nor establish actual-world model adequacy, normative authority or external peer-review acceptance. Full synthesis review remains a separate step.
