# P01 qualification and repair plan

Immutable input: recovered P01 attempt-0003, outer SHA256 2e4ea5fa98f0faa71a0dc160560f090e6bf250c32366f64c5e5ce8c9f80ef652. Input hashes recorded in INPUT_IMMUTABILITY.json. Main remains 03e2604d and no owner adoption or repository effects are authorized.

1. Run the original strict driver unchanged and retain outcome. DONE: baseline-0001 failed in dependency copying because symlinks=False dereferenced batteries/docs/README.md, changing a tracked symlink into a regular file. Exact original dependencies and compiler verified before copy.
2. Repair driver only in shadow: resolve each top-level dependency directory, copy each package preserving interior symlinks. All pinned-revision and tracked-clean checks remain intact.
3. Compile original candidate modules topologically in a development harness using exact pinned cached dependencies. Retain compiler diagnostics by run/module.
4. Diagnose and repair proof/elaboration failures only in shadow source, preserving theorem statements unless a mathematical defect requires an explicitly recorded boundary. Never introduce sorry/admit/axioms, weaken statements silently, or drop targets.
5. Test U10 replacement scope and counterexamples against surviving ordinary documents; distinguish newly checked generic interfaces from an unmechanized recursive relational interpretation.
6. Regenerate shadow source inventory/audit targets, qualify the final source in a fresh strict run, and compare original/public declaration targets and load-bearing types. Record source hashes, all edits, scope differences, axiom audit, and untouched original hash check.
