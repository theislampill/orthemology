# T20 interrupted 80-minute continuation: evidence and reconstructed corrections

**Honest status: partial reconstruction, not original workspace recovery.**

## What could actually be recovered

- `T20_Continuation_Readback_Rescue_001.zip` contains 16 saved-file copies. Fresh byte comparison against the corresponding earlier mounted files showed **16/16 identical**, no new or modified research file.
- Its report marks `t20_complete_work` absent, no working directories, zero research tests performed.
- `Orthemology_T20_Operational_Recovery_20261010.zip` contains 25 entries (source archive copies, inventories, earlier synthesis, recovery script). Its `machine_evidence/working_recovery.json` records `t20_complete_work`, `t20_crossfront_delivery`, and `t20_synthesis_work` as NOT_FOUND.
- The earlier `Orthemology_T20_Whole_Corpus_Synthesis_20261010.zip` and corpus remain available and were not overwritten.
- Thus the 80-minute session's unpublished *files*, reading ledger, theorem revisions and replay logs were **not recovered**. The conversation's research pointers survive.

## What was reconstructed now (not found intact)

A byte-exact copy of the provisional reference implementation was extracted into this packet's `research/contracts.py`. Four new tests were first run against unchanged original code and all **four failed as expected**. The defects:

1. `Contract.__post_init__` iterated each transition-row generator to validate total probability, then iterated the already-exhausted generator to freeze it: valid transitions silently became empty.
2. `valid_partition` iterated a supplied partition to flatten it, then re-iterated it: an exhausted generator could make an invalid equivalence class be silently declared valid.
3. `as_reaches` first converted its target iterator to a set for validation, then reused the exhausted iterator, returning false for an almost-sure reachability claim.
4. `closure_basis` iterated the allowed-action generator for dimension checks before iterating it to propagate the invariant row space, silently skipping all actions.

An isolated copy of the code was repaired by snapshotting each one-shot iterable once at the relevant API boundary; the 26 inherited tests and 4 new regression tests passed fresh (30/30), with original input archive unchanged.

`HYBRID_JUMP_TIMING_CORRECTION.md` additionally reconstructs a precise timed-jump preservation condition and a deterministic two-clock counterexample to the overbroad version of the prior D6 proposition. It is **written mathematics awaiting independent review**, not a recovered original or newly Lean-verified theorem.

## Verification boundaries

- ZIP contents and original source file are inherited; four regression failures and 30 successful unit tests are fresh local observations documented in `evidence`.
- No fresh full-corpus semantic reading, Arabic collation, Lean build, end-to-end repository check or independent scholarly review was performed by this reconstruction.
- This packet must not be described as final T20 synthesis or a completed research programme.
