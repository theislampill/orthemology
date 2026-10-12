# Response to provisional authorial synthesis: additive preservation

ACTIVE T20 additive response, not final consolidation, integration approval or programme closure. Root assessment, exact diagnostics/logs, independent audit/flow and common-source reviews, iterable correction, positive-time tail repair and independent tail review are preserved without editing their source bytes.

Immutable received input: Orthemology_T20_111min_Recovered_Authored_Work_20261010(1).zip, 1,090,000 bytes, SHA-256 263d3b5bf32e698b8ce2417417072cbfe882159deaacbb84f86d0e3ba83de5fe. This exact ZIP carries the original indices once. Replay extracts it into an isolated temporary directory and overlays the separately preserved corrected-reference research/tests plus verifier and original manifest. The original manifest deliberately DOES NOT seal the repair; this collection's MANIFEST.json seals every correction file and the immutable input. We do not regenerate the original manifest or claim the corrected tree passes it.

Tail author freeze: 68619fdc27c7794e8a98dc24aaedec8e594f62fa191f3280d83e53d4a0f82be3.
Independent tail review freeze: daf9fe354b1da9d882ad4009bfc8dfb6c0bd5ada68ea105071af56f927de13da.

Replay runs source 52 and repaired 55 unittest cases directly in normal and -O Python, tail 10 controls in both modes, and exact reviewer controls in normal mode (their assertions require normal Python). The exact inherited gradient check_exact.py dependency is included. SymPy is required for tail and reviewer controls; no dependency is installed automatically. Written infinite-tail/effective-continuation arguments remain written mathematics, not finite-test proofs. No fresh Arabic-source reading or Lean probability proof is claimed.

## Portable verification

Run `python replay.py /absolute/path/to/new-output-directory` from any location. Python 3.12 was used for the preservation replay. The output directory must not exist. Replay checks the complete collection manifest first, uses only included input files and a fresh temporary workspace, and places fresh logs and a receipt outside this immutable collection. It never uses the original workspace paths.
