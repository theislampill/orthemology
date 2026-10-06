# P1 expression model and pinned Python source

P1 v3 proves correspondence for a manually specified expression evaluator with work stack, value stack, dictionary and meter. Its theorem allows arbitrary pending work and prior values. A successful expression leaves its result above the unchanged old stack and preserves the pending tail; failures short-circuit with the same modeled fault and visible step count.

Every pop ticks before dispatch, including ready visits. Children run left then right; a binary reduction pops right then left. Variables bypass width checking, binary arithmetic occurs before the result-width check, and power checks exponent plus one before shifting with a distinct error. The finite-bound result is input dependent in the ideal model and does not supply a fixed universal or physically safe budget.

The Python correspondence is a reviewed source-level connection to the pinned literal implementation. Its domain requires finite immutable correctly aritied tuples, exact builtin natural integers, ordinary dictionaries and valid natural budgets. The evaluator does not validate every such precondition. Booleans, subclasses, custom dictionaries, malformed direct tuples, concurrent changes and host allocation failures are outside this admitted domain.

Independent finite checks compare 266760 cases with a separately written recursive oracle, exercise 1593 pending-stack cases and detect 18 behavioral mutations. These are not a verified Python frontend or a CPython theorem. The accepted scientific and control bytes retain the version-2 cold review through a documentation-only version-3 bridge. Paused P2 runner and P3 work remain excluded, along with statements, loops, parser, serializer and whole-runner claims.

## Claim and source bindings

Fresh evidence for D08-05 is `FRESH_KERNEL_COMPONENTS`; D08-06 has `FINITE_ONLY` evidence through a correlated zero-process view. All results retain candidate research disposition; no operational adoption, external specialist approval or actual-world warrant is established.

The completed `d08-p1-tail-finish-01` continuation reused nine compiled Lean products and the three successful finite observations from the earlier tail. It executed only the remaining Python 3.12.3 control and the missing Lean 4.19.0 audit of 41 declarations. Source and object custody, exact types and safe axiom closure passed; the complete compiler, Mathlib source and cache inventory checks matched before and after. It produced no new Lean objects and did not rerun the original wrapper or those three successful finite children.

Both earlier `FAILED` receipts remain in the record. The original attempt stopped at a source-shape check under Python 3.11.9, while the pinned source AST contract requires Python 3.12. The first tail used Python 3.12.3 but omitted the original driver's output evidence-directory prerequisite; its fourth child failed when writing the report. The final continuation restored that output-only prerequisite without changing scientific source bytes. Four source-prescribed `rfl` rejection controls are retained from the original run. The 18 internal behavioral mutations and five source-text mutations remain finite comparison checks, not additional rejecting subprocesses.

The finite view `d08-p1-tail-finish-reference-01` reads the same physical completion and launches no process. The two continuations and this view add zero independent evidence. Their qualification remains source-expression component proof and finite/source correspondence at the stated input domain; they do not establish a frontend, CPython or whole-runner theorem.

### D08-05 — Expression machine stacks, faults and exact successful ticks

The machine agrees with the recursive model while preserving arbitrary pending work and prior values. Success consumes exact syntax-derived pops and equals the accepted expression semantics; resource failure preserves modeled fault kind and visible count. Input-dependent finite ideal bounds suffice.

Input: Manually specified finite well-formed expression AST, natural dictionary values and initial steps, optional natural step/width bounds, arbitrary pending work and prior value stack.

Limits: This is not a verified Python frontend, CPython semantics or whole runner theorem. No host allocation, physical time, fixed universal budget or continued success under arbitrary budget changes is proved. Paused P2 runner and P3 work are not admitted.

Exact source: [PythonExprBounds.lean](../../source-store/f3a73c94456e1380a0272eb66b3403db803c0c0f37a9941631eb477847a07999/PythonExprBounds.lean), [PythonExprCore.lean](../../source-store/9a120790a308a57f7fa0e8d0480cf80b517197ddd429960244ea2d5f73c66867/PythonExprCore.lean), [PythonExprMachine.lean](../../source-store/22d97f7d120194c258791867028edddc5921b8d3ea65d35f73723336019a1077/PythonExprMachine.lean), [PythonExprSafety.lean](../../source-store/3f962df5e2b98f0b294ee2726b10b0c10e2fdfc11cdecee8b22f965c7ab05a25/PythonExprSafety.lean).

Inherited review: [ACCEPTANCE.md](../../source-store/c31578f82921ea6e25f3c338bebf0e78b2f91ab248c9fc707f86503a2c0ec0b5/ACCEPTANCE.md), [WORDING_CLARIFICATION.md](../../source-store/c0d90d203b0d069e9568b19fb7aa6e2560a19503ef59b80f017914ee48f94610/WORDING_CLARIFICATION.md).

Report keys: T09:V4; original avenues 8, 9.

### D08-06 — Pinned Python expression source correspondence and finite controls

Source review and exact AST/source pins relate the literal Python evaluator to the formal algorithm; independent recursive-oracle tests cover 266760 cases, 1593 pending-stack cases and 18 behavioral mutations.

Input: Finite immutable correctly aritied tuples, exact builtin natural integers, ordinary natural-key/value dictionaries and valid natural meter budgets.

Limits: Booleans, integer subclasses, custom dictionaries, malformed direct tuples and concurrent mutation are excluded. Finite tests and AST identity are not a universal frontend or CPython proof. Physical allocation may fail before modeled width rejection; statements, loops, parser, serializer and complete runner remain outside.

Exact source: [prcodec.py](../../source-store/dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c/prcodec.py), [P1_SCOPE.md](../../source-store/81d31db2010d1e16f0f0f95fc8eefa264d7fd69dbf439908a61a27de43015339/P1_SCOPE.md), [SOURCE_CORRESPONDENCE.md](../../source-store/f40bc24f587245f89eff67da47525e336e0b3731e07b77e4ac25f9f8498770ff/SOURCE_CORRESPONDENCE.md).

Inherited review: [SOURCE_REVIEW.md](../../source-store/3ae1e9e04da476f9960d7d51b617dfaff77168fdc3571e9eaf723aa1cbdb24e2/SOURCE_REVIEW.md), [WORDING_CLARIFICATION.md](../../source-store/c0d90d203b0d069e9568b19fb7aa6e2560a19503ef59b80f017914ee48f94610/WORDING_CLARIFICATION.md).

Report keys: T09:V4; original avenues 8, 9.
