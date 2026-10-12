# Orthemology v5 frontier research return

## Status and scope

This is the **qualified, scoped Orthemology v5 research return for 30 September 2026**. Original inputs, repaired checkpoint results, new research results and independent audit evidence are identified separately. Open programme obligations remain explicit; these shadow results do not imply canonical adoption or external academic peer review.

The canonical source basis is commit `03e2604dfcef278b01c60d19b05370fcec4194b6`, tree `3d06e80277ce39286c94307e0f14b215bc94ed83`. Its complete source-tree ZIP and raw Git commit object are included. The verifier recomputes the commit object, its tree link, every Git blob and the root tree without needing the original repository. A timestamped read-only origin/main readback also matched that commit at 17:32 UTC on 30 September 2026; this is an as-of observation, with no future-currentness or adoption claim.

For the readable twelve-page research return, open `report/Orthemology_Frontier_Research_Return.docx`. Then use `STATUS_MAP.md` and each lane's original README/findings inside its preserved archive. `ARCHIVE_INVENTORY.json` identifies the outer bytes. `SOURCE_OWNERS.json` maps replay sources to archive members or exact receipt-bound author sources. `DEPENDENCY_GRAPH.json` and `SUITES.json` identify replay dependencies and targets.

## What is portable

All custom Lean source dependencies used by the listed suites are included, including the P01 parent project, repaired P02 predecessors, finite Mealy predecessors, and P03 native source bases. Historical archives remain byte-for-byte unchanged, including historical failed runs and absolute-path drivers. The new `scripts/replay.py` replaces only the environment-dependent orchestration, using the same mathematical source bytes.

This is a **source-complete package with explicit external official prerequisites**, not a fully offline distribution. Lean and the official Mathlib dependency caches are deliberately excluded. There are no multi-gigabyte toolchain or cache copies. See `PREREQUISITES.md` for exact pins, trust boundaries and setup.

## Verify and replay

Run Python 3.11 or later. Commands below assume your shell is in the extracted package. Always choose a new output directory outside the package.

1. Verify all packaged bytes, archive CRCs, canonical Git identities and custom import closure:

   `python3 -B scripts/verify.py --receipt ../integrity.json`

2. Verify that retained completed replay logs and exact type/axiom target sets bind all current included sources, without rerunning Lean:

   `python3 -B scripts/verify_replay_evidence.py --receipt ../recorded-replay-bindings.json`

   This checks recorded evidence consistency. It does not authenticate historical execution or replace a fresh Lean replay.

3. Run the portable validator's own positive and negative tests:

   `python3 -B -m unittest discover -s tests -v`

4. With the official pinned prerequisites available, compile every custom Lean source from scratch, then audit exact target types and axiom sets:

   `python3 -B scripts/replay.py --lean /absolute/path/to/lean-4.19.0-linux/bin/lean --mathlib /absolute/path/to/mathlib4 --out ../fresh-lean-replay`

   Repeat `--suite NAME` to restrict the run. The available names and claim sets are in `SUITES.json`. Each suite has its own fresh custom-artifact directory. No historical custom `.olean` is used. Counts are recorded separately, never summed across overlapping suites.

5. Replay the control/restoration and source/norm-fixing finite executable tests from newly extracted archives:

   `python3 -B scripts/replay_python.py --out ../fresh-python-replay`

6. Replay the archived P03 source/canonical test suites in normal and optimized Python, proposal frontier tests, and all 188 strict-JSON/native cases:

   `python3 -B scripts/replay_p03_runtime.py --out ../fresh-p03-runtime`

7. To check an unopened outer package instead, use a copy of the verifier from a separately inspected package:

   `python3 -B scripts/verify.py --archive /path/to/successor.zip --extract-to /new/absent/directory --receipt /path/to/integrity.json`

A success claim must cite the newly produced receipt. Integrity verification alone is not compilation, and finite tests are not an infinite-horizon proof. Old receipts retain their original status rather than being retrospectively upgraded.

## Evidence limits

- Exact compiler identity and official source commits/cleanliness are checked; already-built official `.olean` caches are reused. Fresh custom-source replay is not a clean-network rebuild of all official dependencies
- Original checkpoint claims may have failed before repair. Use the original/repaired/new status map, not file names or mutable `LATEST` pointers
- No target-count total is meaningful across these suites. P01 successor includes its parent sources; Mealy stage2 includes stage1; root measure has six overlapping helper targets; P02 stages share dependencies
- Historical Python/runtime comparisons and negative controls remain available inside the preserved archives. The portable Lean command verifies its exact declared claim sets, not every historical experiment
- Normative authority, philosophical/modal premises, source adoption and universal runtime/text-export equivalence are not created by these receipts
- The agreed development scope is frozen; exclusions and remaining obligations are stated in the report and STATUS_MAP

The master manifest binds the package payload; its SHA-256 sidecar and the final outer archive hash detect changes. These are integrity records, not third-party digital signatures or proof of author identity.
