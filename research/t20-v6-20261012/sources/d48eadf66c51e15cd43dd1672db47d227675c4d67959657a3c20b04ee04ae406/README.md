# SCC-based parity target computation

Fresh isolated fifth-tranche author candidate. The predecessor's eight Lean sources are copied byte-exact. Three new modules replace powerset MEC enumeration with SCC-based deletion and prove the complete parity/normalized-target refinement.

## Exact formal endpoints
- `HiddenParity.SCCPruning.mecs_eq_executable`: the new selector equals the old exhaustive selector for every finite graph input
- `HiddenParity.SCCPruning.parityOutput_exact`: returned components are exactly maximal self-verifying parity components
- `HiddenParity.SCCPruning.markovTarget_exact`: exact qualifying-state predicate for the same normalized rational rows and supplied allowed pairs

The graph proof derives preservation, cardinal stabilization, restricted-path connectivity and maximality. Empty successor sets are rejected because the unchanged end-component predicate requires nonempty successors. Components are recomputed after both source loss and loss of reverse paths.

`COST_ACCOUNT.md` gives a conservative polynomial finite-table operation count. This complexity account is ordinary mathematics; exactness and cardinal invariants are kernel-checked. There is no formal machine-time theorem or promise about arbitrarily expensive function-valued inputs. The selector does not use powersets in its computational definitions.

The supplied allowed-pair, live-candidate and full-row boundaries are unchanged. This is not a new stochastic winning iff, hard-menu recursion, policy compiler, optimal complexity claim or historical novelty claim.

## Qualification

All current sources compile in the pinned Lean 4.19.0 / Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b environment. Twenty new kernel controls and 8,704 finite oracle comparisons pass. These are author checks until a separately identified reviewer accepts the immutable packet.

The final source packet provides `tooling/replay_lean.py`; give it explicit pinned external dependency paths and a fresh output directory. Official installed dependency objects are trusted. Every custom module is cold-rebuilt, with public type/axiom readbacks. No source bootstrap of all official libraries is claimed.
