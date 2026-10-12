# Orthemology T20 — recovery readback

**Purpose:** distinguish actual recoverable work from the interrupted continuation from inherited provisional synthesis. This is a recovery record, not a completed all-T20 reading or new Lean proof.

## Files verified in this execution

- `Orthemology_T20_Operational_Recovery_20261010.zip`: 82,563,755 bytes, SHA-256 `d35a571bf5a7da4c14157b96f9c2e52503b3af512c95dee41dd68f03b89e4b44`; ZIP CRC PASS. Its 24 non-manifest payload files match the SHA-256/size MANIFEST exactly.
- `Orthemology_T20_Whole_Corpus_Synthesis_20261010.zip`: 7,301,272 bytes, SHA-256 `38ed92bbec0877b5dc55ea049689cf25945d9d9d5fd253cb4bbfc9e9f88cf753`; ZIP CRC PASS.

## What survived **beyond** the original provisional synthesis ZIP

The recovery checkpoint itself is an independently created, recoverable ZIP containing:

- seven original owner-supplied top-level T20 bundles (unchanged copies);
- the prior synthesis ZIP, field guide, mathematical synthesis, crosswalk, Dot handoff, corpus register, scope statement and prior verification receipt;
- an operational recovery script and separate inventory/identity manifests;
- full recursive inventory records of **118 distinct ZIP objects** and **17,042 member occurrences** (verified by reading the saved inventory JSON in the ZIP);
- SHA-based inventory of **8,161 decoded UTF-8 text objects**. This is metadata and decoding, not evidence of substantive scholarly reading.

No other new research working files or freshly corrected theorem/code files were recovered from the failed continuation: `working_recovery.json` reports the three anticipated `t20_*` working directories `NOT_FOUND` and zero recovered working files.

## Fresh tests of the preserved earlier derivative packet

After safe-path-checked disposable extraction in this turn:

- `python3 -B verification/verify_packet.py .`: PASS; 1,517 files and seven directories verified.
- `python3 -B -m unittest discover -s research -p 'test_contracts.py'`: **26 tests PASS**.
- `python3 -O -B -m unittest discover -s research -p 'test_contracts.py'`: **26 tests PASS**.
- `python3 -B research/exhaustive_oracle.py`: PASS; exact finite controls: 1,728 three-state contracts, 8,640 candidate partitions, 252 value-bound instances, 4,752 conditioning-bound instances.

These outcomes verify that the **earlier archived reference implementation remains runnable**, not that the interrupted continuation's reported repairs were preserved or verified.

## Unrecovered but documented pointers

The interrupted continuation reported (1) a one-shot iterator consumption bug in an iteration/reference implementation, and (2) a missing jump-timing condition in the proposed hybrid preservation theorem. These remain **research/debugging pointers**, not accepted or recovered fixes. Reconstruct them from actual old code and tests; do not count conversation text as a corrected source artifact.

## Outstanding work

A verified exhaustive semantic reading of distinct original T20 substantive sources, full available scientific test/Lean/source replays, correction of any substantive counterexamples, and a final revised synthesis have **not** been completed. The previous narrative and automated inventories cannot independently certify all such work. Preserve all predecessors and audit evidence.

No protected repository was edited, no merge performed, and T20 remains active.
