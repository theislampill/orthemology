# Replay and scope

Run with Python 3 and SymPy (the executed version is recorded by the report):

    python check_exact.py --output-dir /absolute/path/to/a/fresh-directory

The output directory must not exist. The script creates it and writes `EXACT_CHECKS.json` only after every exact check succeeds. Any assertion failure is a failed run, not a partial pass. The copied predecessor reports in `inputs/` are checked against `INPUT_BINDINGS.json` on every invocation. No external access is needed.

To additionally check the original inspected files in the shared author workspace:

    python check_exact.py --output-dir /absolute/fresh/path --original-root private-locator:8f24556a330b05a11a95

The original-root option is optional so the packet is independently replayable with its copied inputs. Original inputs are read only, never changed. The `author-run` report was generated with that option. The separate `portable-author-run/EXACT_CHECKS.json` omits the nine original-root checks and is the exact-report comparison target for extracted replay. Fresh replay outputs belong outside a frozen copy of the packet.

The script performs exact symbolic/rational identities and finite-dimensional rank checks. It is neither a formal-kernel proof nor a universal theorem by finite enumeration. The ordinary proofs and their full assumptions are in `RESULT.md`; the inherited hierarchy representation theorem is explicitly identified there. Source-reading and independent-review status are separate from author execution.
