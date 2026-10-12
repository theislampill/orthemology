# Independent actual-batch source controls

Verdict: PASS for these controls over the unchanged actual source. The new
author batch refinement/progress extension has not yet been reviewed or accepted.

The source-first specification is `INDEPENDENT_SOURCE_SPEC.md`. Its original
runtime/source bindings are `PRE_AUTHOR_SOURCE_BINDING.json`. No new author
proof was inspected before the independent specification and controls.

Seventeen independent theorems were freshly compiled: fourteen in
`BatchSourceChallenges.lean` and three in `BatchHistoryPremiseChallenges.lean`.
Both compilations returned zero, with no warnings or errors. Every printed
theorem closure uses only a subset of `propext`, `Classical.choice`, and
`Quot.sound`. The ordinary `decide` proofs were checked by the Lean kernel;
there is no `native_decide`, assumed safety law, or Python service evaluator.

The decisive behavioral controls establish:

- All four literal trials run, with exact ordered paths and nonce 1 through 4.
  A successful first trial does not refresh the actor or stop later trials.
- Proposal-none logs four `closed=true` records but records no commitments or
  tombstones. The log bit alone is not a cancellation certificate.
- A false preparation can retain dishonest commitments. Wrong requester and
  stale actor time do not produce actual progress.
- Every zero/one-fault pattern has an intact portfolio path. All two-fault
  patterns hit every path; the direct actual two-fault control stalls.
  Removing any portfolio path admits a one-fault hitting-set witness.
- Cancelling the fourth exact envelope beforehand stalls the only intact path
  when root 0 is faulty. The native pinned-source version is proved genuinely
  aligned and reachable after a permitted cancellation, with current plant,
  policy, and an admissible local proposal. Structural alignment/reachability
  therefore do not imply progress.
- A higher-nonce unrelated tombstone does not prevent actual batch progress.
  The author's proposed global nonce high-water condition is stronger than
  necessary. The unchanged actor reuses its nonce sequence on a second batch.
- q=2 invalidates the fixed three-root paths before mutation. A budget=3
  cancellation threshold can produce false close replies while still adding
  honest tombstones, independently of successful plant progress.

The small fixture source controls use payload `[65]` only to bound reduction
cost. The three history-premise controls use the complete accepted 3,013-byte
native fixture and its raw policy epochs. They do not replace the native source
binding with a toy payload.

## Exact replay boundary

Receipt: `direct-controls-v1/RECEIPT.json`, SHA256
`7bff5c06ccb4c873bc801f76fc3986b4893383ee1873dcbf783c4ce1d81cb330`.

The two fresh compilations used official Lean 4.19.0, commit `6caaee842e94`,
executable SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`,
with `-j1 -s65536`. They took 6.781 and 9.797 seconds respectively. All seventeen
axiom inventories and source/command/log identities are recorded in the receipt.

The replay reused exactly 38 already independently compiled v4/v5 objects.
Their identities were checked against the previous accepted v6 reviewer receipt
before and after this replay, and they were consumed read-only. No reused object
is credited as newly compiled here. Final review of the new author extension
still requires a separate immutable candidate and cold compilation of its exact
custom source closure.

The restored official Lean distribution was independently rechecked across all
5,065 pinned entries. All 6,816 pinned Mathlib source records and all 34,230 cache
inventory entries were checked. Exactly five official cache-fetcher `.trace`
files differ only by the relocated compiler path. Their actual bytes were
preserved; comparison-only prefix normalization reproduces the old five hashes.
Every scientific dependency `.olean`/`.ilean` entry matches its pin. This is
verification of restored official caches, not an independent Mathlib rebuild.

The relocation manifest SHA256 is
`d14ffdea106264773d5b708b765a078e1a8a3f529bd909c08dcc806c3d4c446b`.
The reviewer driver is `replay_direct_controls.py`; it is a local provenance
harness requiring the preserved prior reviewer objects and restored pinned
dependencies, not a standalone public distribution wrapper.
