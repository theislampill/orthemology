# Rational actual-source bridge: additive preservation

ACTIVE T20 additive result, not final consolidation or integration approval.
Candidate freeze SHA-256: 741c86af1ae30aaa45df6f8d499280983fd119e96a4a2f40e157e87952606366.

The payload preserves exact current author, independent-review, participating-root files, all 258 non-object inherited source entries named in SOURCE_BOUNDARY.json, and the exact D1 contracts.py needed by Python replay. Source bytes and original metadata are unchanged; original absolute paths remain historical provenance, not portable-path promises.

The recorded Lean logs/receipts concern the historical successful kernel replay over retained dependencies. This collection preserves their custody. No fresh Lean compilation is claimed. Compiled .olean/.ilean objects, Python caches and toolchains are excluded; the inherited object and import inventories remain exact metadata. The original shell/verification harnesses have environment-bound dependencies and are preserved as evidence, not presented as portable commands.

The source theorem is deterministic for explicit seeds. Probability and finite-history transport use separately stated external finite-law conditions; there is no new Lean probability theorem. Reviewer assert-based controls are authoritative in normal mode; optimized execution of those controls is only supplemental. Participating root diagnostics are labelled as such.

## Portable verification

Run `python replay.py /absolute/path/to/new-output-directory` from any location. Python 3.12 was used for the preservation replay. The output directory must not exist. Replay checks the complete collection manifest first, uses only included input files and a fresh temporary workspace, and places fresh logs and a receipt outside this immutable collection. It never uses the original workspace paths.
