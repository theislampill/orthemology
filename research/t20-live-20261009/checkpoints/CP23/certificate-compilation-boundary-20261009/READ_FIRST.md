# Finite grounded-rule compilation

Start with `RESULT.md`. It proves the missing finite-catalogue interface for cyclic, finite grounded rule systems under explicit proof-substitution and nonnegative checking-cost assumptions.

The two checking contracts are deliberately different:

- `compile_tree`: synchronous Pareto saturation, at most one round per scoped judgement; repeated rule occurrences are charged separately.
- `compile_dag`: finite whole-graph rule-choice enumeration; each checked node is charged once. Intermediate standalone support/cost pruning is not sound for this objective.

Run the complete local verification suite with:

    python certificate-compilation-boundary-20261009/verify.py

It uses only Python's standard library. `CHECK_RESULTS.json` records exact source hashes and checks; `verification.log` is the captured full replay. `review/` contains the independent mathematical/implementation review and its separate exhaustive DAG-pruning control.

`compiler.py` is a transparent research implementation, not an authentication service or a deployed proof checker. Judgement strings stand for fully scoped labels already justified by the caller. The finite evidence universe is inferred from the finitely many rule-support labels; unused additional tokens are irrelevant. Its witness traversals check local premise matching, supports, prices and acyclicity. They do not establish a supplied rule's semantic licence or a measured checking-time calibration. Compiler-produced witnesses use only the admitted input rule records.

No new Lean/kernel certificate is claimed. The inherited kernel certificate remains restricted to finite support/cost-pair mathematics. No HasE decision procedure, unrestricted completeness, philosophical conclusion, protected change, integration, or closure follows from this package.
