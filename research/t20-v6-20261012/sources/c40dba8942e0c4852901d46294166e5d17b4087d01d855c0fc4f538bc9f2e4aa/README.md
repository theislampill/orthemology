# Dynamic V2 finite-history kernel safety

Additive formalization of the original accepted dynamic V2 root/table interface.
The central multi-epoch temporal safety, durable cancellation, and stable-epoch
whole-table persistence arguments are now encoded as finite-trace Lean proofs.
Protocol, thresholds and accepted external premises are unchanged.

- `STATEMENT_AND_SOURCE.md`: exact theorem statements, correspondence, proof
  structure, independent premises and claim ceiling.
- `HistoryModel.lean`: concrete root/local-state, event and finite-trace semantics.
- `HistoryInvariant.lean`: structural authenticity and durable-certificate
  invariants proved from the individual transitions and by trace induction.
- `HistorySafety.lean`: root counting, current/exact admission, monotone memory,
  and cancellation exclusion over arbitrary continuations.
- `HistoryTrace.lean`: every-write history theorem, plant safety, stable target
  preservation, and a separately conditional external-reservation corollary.
- `NegativeControls.lean`: concrete authentic prefix traces and mechanism
  deletion witnesses, proved using kernel reduction.
- `tests/Targets.lean`: separately compiled public theorem instantiations.
- `tests/MultiEpoch.lean`: a non-vacuous two-transition trace with partial and
  reordered local delivery, current landing and stale-command exclusion.
- `source_replay.py`: seven bounded scenario replays against the unchanged
  accepted Python source; corroboration rather than a language-refinement proof.
- `SOURCE_BINDING.json`: immutable source/review/compiler bindings.

## Replay

Run `./verify.sh [fresh-output-directory]`. The supplied defaults use exactly
Lean 4.19.0 and the read-only Mathlib cache for commit
`c44e0c8ee63ca166450922a373c7409c5d26b00b` under `private-locator:351b8592ab6e0e21df70`.

The verifier checks source and compiler hashes, recompiles every module into an
isolated output build directory, compiles the public target statements, rejects
warnings/errors/custom proof holes, checks seven false claims are rejected by
kernel reduction, replays seven accepted-source scenarios, then checks both candidate input and
frozen source hashes again. It does not modify the
Mathlib cache or import the development `.olean` files beside these sources.

No complete liveness/covering/randomized theorem or external implementation
assurance is claimed here. This proof does not automatically apply to the typed
compiled composition or unknown-label map extension. Independent cold review
is pending until a separate review sidecar says otherwise.
