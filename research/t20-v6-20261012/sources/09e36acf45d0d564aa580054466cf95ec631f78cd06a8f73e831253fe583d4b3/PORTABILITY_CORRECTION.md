# Caller-directory portability correction v3

No scientific source, theorem, dependency pin, exact diagnostic exception, or scientific acceptance changed.

The v2 author full replay passed when invoked from the original workspace ancestor. The independent replay from `/tmp` then failed at the first predecessor source because Lean requires the input source to lie under its compiler working-directory root. The wrapper had inherited the caller's directory, contrary to its portability promise. Its independent failure receipt contains no success claim.

Version 3 sets `cwd=ROOT` explicitly in the single subprocess runner used by the version probe, all positive Lean stages and every mutant. ROOT is the resolved checkpoint directory. The Python caller's directory is not changed: an output argument is resolved first and must remain absent and outside all protected source/compiler/dependency trees. Every stage receipt records `compiler_cwd`.

Two new regression tests run the subprocess helper from an unrelated temporary directory and verify the explicit compiler cwd. They separately verify that a supplied output artifact and logs remain outside the source tree and that the source manifest is unchanged. These tests fail against the v2 runner and pass against v3; the existing 20 boundary tests remain in force.

The full wrapper-v2 manifest and all changed historical helper/test/README/mapping bytes are preserved through `ORIGINAL_TO_PUBLIC.json`. `historical/wrapper-v2/` includes both the author workspace-only PASS receipt and the independent unrelated-directory failure receipt/log. Neither is presented as a standalone v2 portability pass. Corrected full replay must be demonstrated from an unrelated working directory before claiming v3 portability.
