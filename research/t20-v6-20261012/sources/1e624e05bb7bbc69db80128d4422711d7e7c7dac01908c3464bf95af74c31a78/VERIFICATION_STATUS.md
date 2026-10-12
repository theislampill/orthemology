# Freshly observed verification and exclusions — 11 October 2026

## Direct operations performed for this handoff

- Reopened the **unmodified** `Orthemology_T20_111min_Recovered_Authored_Work_20261010.zip` and tested ZIP integrity: no CRC error, 38 ZIP records including 37 authored manifest members.
- Extracted its standalone authorial files to a new staging location, leaving the original untouched.
- Executed `python -m unittest discover -s tests -v` against extracted `research/`, `tests/`: exit **0**, **52 tests passed**.
- Executed `python -m compileall -q research tests verify_packet.py`: exit **0**.
- Executed `python verify_packet.py . --run-tests`: exit **0**, `ok:true`, `files_checked:37`, and reference tests return code 0.
- Independently executed new exact-rational spotchecks: Euler/audit distance `1/117` observed, reciprocal scheme passed **6,561 finite test cases** on a three-weight grid (with positivity, normalisation, monotonicity, common-shift and audit commutation assertions), and the sharp relative-likelihood TV example attained `1/3`.

Logs and spotcheck source are preserved under `fresh_evidence/`; this report does **not** present the program output as general theorem proof.

## Not done / no credit

- No fresh Lean compilation or independent mathematical peer review of general proofs.
- No execution of the actual Dot v2's or original T20 code/test suites; inspecting its narrative does not replay its evidence.
- No exhaustive source-by-source semantic/Arabic-text reading of 2,095 documents; an inventory and excerpts do not equal semantic reading.
- No true R3 state/second-order algorithm/88-test suite inspected or replayed. A supposed R3 preservation ZIP available in the mount contains older documents/ZIP only, not the reported new R3 files. The separately located Library operational ZIP could not be raw-materialised.
- No GitHub writes, acceptance, release authority, claim of worldwide theorem novelty, or empirical DAEE confirmation.

## Reading taxonomy

`MODEL_READ` means the actual source text was inspected with scope; `INVENTORIED` means only listing/hash/index; `TEST_FRESH` means this session executed and read output; `RECEIPT_INHERITED` means previous recorded evidence; `WRITTEN_PROOF` means a detailed mathematical argument requiring review; `LEAN_FRESH` is **not** claimed by this handoff.
