# Literal shift invariant and trace refinement supplement

This supplement contains an ordinary mathematical refinement of the original P02 Python `compile_shift`, with exact source binding. It proves its numerical output and explicit Set-event trace for every well-formed arity-two base AST and every natural numerical stage input, including malformed-sentinel inputs interpreted through their low bits. It also makes the corresponding infinite-stream invariant and exceptional boundary path explicit.

Read `RESULT.md`, then `INDEPENDENT_REVIEW.md`. The author proof retains its pre-review submission wording; the separate review binds the final reviewed bytes. Most ordinary source-correspondence and all probability-classification content are inherited. In particular, the original codec document already states ordinary universal source correctness and PR code construction. The narrower increment is the detailed invariant, arbitrary-numerical-word generalization and universal explicit Set-event trace; no first-proof, kernel-verification, classification advance, integration or T20-closure claim is made.

The complete unchanged compiler and three directly relevant prior documents are under `inputs/`. `INPUT_BINDINGS.json` records their original locations and verified copy identity. The original compiler hash is `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`.

Run `python -B verify_integrity.py` from any directory, or pass a supplement-directory path. It uses only the Python standard library and checks the complete file set, byte lengths and SHA-256 hashes against `MANIFEST.json`. It checks integrity only; it does not execute the compiler, rerun bounded controls, inspect a proof kernel, or establish mathematical validity. It rejects missing, changed, additional and symlinked files. The manifest itself is authenticated by the enclosing archive hash retained separately.

Resource scope: the theorem concerns mathematical natural-number operational semantics and successful host executions. It does not promise success under default meters, finite memory or host recursion limits. No original source or repository was changed.
