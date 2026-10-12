# Independent review replay

Run with Python and SymPy 1.14.0 from any working directory. Keep `check_independent.py`, `PREDECESSOR_BINDINGS.json`, and the `inputs/` subtree together.

    python check_independent.py --output-dir /a/fresh/output/directory

The output path must not exist. This runs 151 finite exact controls, verifies every copied predecessor digest, and writes `INDEPENDENT_EXACT_CHECKS.json`. The byte-comparison target is `portable-run/INDEPENDENT_EXACT_CHECKS.json`; its `original_predecessors_preserved` value is null because portable replay does not assume a live original workspace.

Optionally add `--original-root /path/to/original/workspace` to verify the original predecessor bytes as well. The independent review's initial such run is retained in `independent-run/INDEPENDENT_EXACT_CHECKS.json` and at the report root. Its original-preservation field is true. This option does not write to any predecessor and does not alter the core check count.

The copied root-supplement checker is retained in `two_atom_replay/check_exact.py`. It writes its 30-check output beside itself. For a nonmutating replay, first copy that directory to a fresh output location and run the copy. Its result is byte-equal to the frozen supplement's `EXACT_CHECKS.json`.

`ACCEPTED_BINDINGS.json` binds every assessed author/source file by relative path, byte count and SHA-256. Digest verification and exact symbolic replay are evidence-preservation controls; they do not replace the ordinary mathematical arguments in `REVIEW.md` and do not provide kernel proof, integration, or closure authority.

The frozen main author checker was replayed into `main-author-portable-replay/`. Its 699-check report is byte-identical to `joint-atomic-gradient-lift-20261010/portable-author-run/EXACT_CHECKS.json`. Replay it from the retained author tree with `python check_exact.py --output-dir /a/fresh/path`; preserve its `inputs/` subtree and `INPUT_BINDINGS.json`.
