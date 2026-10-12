# Source bridge preserved from the literal AST checkpoint

Original Python target: `inputs/prcodec.py`, SHA-256
`dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`.

The seven modules in `inherited/literal` are byte-identical to the independently replayed literal AST checkpoint, final archive SHA-256
`7f4fc218565854d4f23e0da530bdc3061c3e026f7dd0c3cea2b5e255809cb46d`.
Its preserved `SOURCE_BRIDGE.md`, `RESULT.md`, and independent review explain the exact Python-to-typed-AST boundary.

New probability statements refer directly to `P02.LiteralShift.compiledOutput`, defined from `programValue (compileShift body output a b) 2` under the unchanged `ObserverCore.output`. They reuse `compiledOutput_below`, `compiledOutput_copied_prefix`, `compiledOutput_above_tail`, `compiledOutput_unresolved`, and `firstCut_or_unresolved`; no new or alternative shift evaluator occurs.

The source-lowered AST is unchanged, including sorted finite-register support compression and n-ary-sequence lowering. The source transcript was reviewed ordinarily, not kernel-parsed from Python. No source-byte or original numeric-code identity follows merely from a kernel result about that AST. Original Python host limits, recursive-helper failures, and body grammar hypotheses are unchanged.

This supplement closes the actual fair-source probability/atomic-defect bridge for that AST. It does not expand the prior explicit `Set`-trace, Python-host, numeric-serialization, or integration claims.
