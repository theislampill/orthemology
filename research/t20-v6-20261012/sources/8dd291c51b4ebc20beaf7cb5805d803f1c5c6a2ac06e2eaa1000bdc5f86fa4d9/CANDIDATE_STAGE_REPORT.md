# Independent candidate and compiled Sigma2 AST audit

## Disposition

The separately sealed generated-AST extension passes the independent audit. It proves actual generated Lean statement execution equals the least-candidate innovation prefix function and identifies its actual fair-Cantor output law. No semantic defect was found in that scope. It is stronger than the earlier mathematical-prefix-family seal, but not a formally verified Python byte/numeric-code compiler.

Exact seal: `private-locator:92535ac924649977552e`

SHA256: `00b3c06356f9fbdfa4ea1e7bc9fab4b0072faffda6fc834e47ecd2f2c6ff67e0`

Underlying receipt: `receipts/candidate-20260930T150947Z/CANDIDATE_RESULT.json`

SHA256: `2beddd3cab8712b85bfb908afc48b73ebaa4af2b5405d7cadc5a08f7e55086d7`

Both hashes, all seal-listed files, all four source hashes, the audit-source hash, and the three original control hashes were verified. The sources were copied into `observer-measure-audit/candidate-sources` and compiled into a separate `candidate-build`. The existing dependency sources still matched the earlier independent audit. The import path excluded the author's project build outputs and used only the current audit outputs, earlier independently rebuilt dependencies, and the exact pinned Mathlib/package caches.

## Reproduction and controls

`audit_candidate.py`, `candidate-audit.log`, `candidate-receipts/`, and `CANDIDATE_STAGE_AUDIT_RESULT.json` preserve commands, hashes, exits, timings, and all 52 type/axiom readbacks.

- CandidateCompiler, CandidateSource, CandidateWitnesses, Sigma2Compiled, and CandidateAudit each compiled with exit 0 using Lean 4.19.0 commit `6caaee842e94`, `-j1`, and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- Every named target's transitive axiom set is confined to `propext`, `Classical.choice`, and `Quot.sound`
- The theorem census includes all four same-line `@[simp] theorem` declarations in Sigma2Compiled
- CandidateBaseline compiled
- ExcludedUpperTestMustFail and OverwriteFirstSuccessMustFail each failed because kernel reduction proved the claimed equality false, not because of an import or declaration error
- The only positive-build diagnostic was an unused-variable warning in CandidateCompiler; it is not a proof gap

The first control demonstrates the need to include the upper test `t = stage`; the second demonstrates the need to preserve the first successful candidate rather than overwrite it with a later one.

## Semantic inspection

### Candidate control loop

CandidateCompiler's explicit CallSpec requires the call to compute the matrix value on registers 6 and 7 and preserve all registers below 10. `testLoop_good` accumulates conjunction over every test below the snapshotted count. The outer loop resets its good flag per candidate, preserves the stage, and changes the output exactly at the first passing candidate. The intermediate runSearch is separately proved to return the same least candidate as SurvivorCandidates, including the default `N+1` when none passes. `candidateBlock_value` is a theorem about execution of the actual statement, for arbitrary caller store and stage expression; no simulation conclusion is merely postulated.

### Concrete matrix inlining

CandidateSource discharges CallSpec. Its finite register set contains inputs 0/1/2, the designated output, every expression read and statement write/loop index. Sorting and index lookup allocate each used source register at `11 + index`; injection is proved on the actual finite support. Every allocated source-local register is reset before every matrix call. The loaded source state is proved equal to the arity-three zero-extended input store `(parameter,candidate,test)`. Fresh locations are at least 11, so controllers 0–10 cannot be captured.

The general inlining theorem's required output/support, injection, reset and argument-disjointness hypotheses are all discharged, rather than hidden in a user-supplied correctness assumption.

### Second block and complete observer

Sigma2Compiled allocates the second candidate bank at `11 + first-register-list.length`. Its secondMap sends prototype output 3 to 4, swaps otherwise unused prototype 4 back to 3, leaves inputs 0/1/2 fixed, and shifts all prototype locals 5 and above. The resulting map is globally injective for this base. Thus first local 5 maps to the second controller base, and first matrix-local 11 maps to the second controller base plus 6, exactly matching the next Builder allocation.

The generic renaming theorem proves execution correspondence and preservation of the first block's output. The complete statement evaluates the current candidate, resets old output to zero, evaluates the previous-stage candidate only when n is nonzero, and emits the current input-bit residue iff the two candidate values differ. No stale old value survives at n=0. `compiled_value` handles arbitrary caller stores, not only all-zero initial scratch.

`prefixValue_eq` specializes to the binary input store and connects actual statement execution to the already-audited mathematical prefix function. `observer_eq` and `law_eq` connect the actual synchronous observer and fair-product pushforward. The zero endpoint is exactly `∃s∀t` nonzero matrix output, and the one endpoint exactly its negation. Mathlib Primrec membership is proved for each generated fixed binary program.

## Independent source-constructor comparison

Preserved comparison source: `private-locator:d8dc20b3e088111e6617`

SHA256: `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`

The actual `registers`, `Builder.inline`, `_candidate`, and `compile_sigma2` implementations were read. They use the same inclusive candidate/test loops, full-local reset, sorted-register allocation, frozen first success, stage-zero predecessor convention and final word-modulo-two emission.

As an additional independent regression check, `compare_candidate_ast.py` generates 32 arity-three source programs and compares the source Python compiler's AST to the actual evaluated Lean compiler AST, after only flattening sequence associations and removing empty sequence/skip nodes. The tests include constant and bounded predicates, empty code with output in the input bank, sparse output registers, arbitrary source register overlaps with controller numbers, and seeded nested loops/branches and arithmetic expressions. All 32 normalized ASTs matched exactly.

Evidence is in `CANDIDATE_AST_COMPARISON.json`, `candidate-ast-comparison.log`, `candidate-sources/IndependentAstComparison.lean`, and `candidate-receipts/IndependentAstComparison.log`. The independent exporter initially had a local Lean.Expr/ObserverCore.Expr namespace ambiguity; it was qualified and the successful run returned 32 complete JSON outputs with exit 0. This was an audit-harness issue, not a target-source defect.

This is supplementary ordinary source correspondence. It is not a universal formal theorem about Python execution, its resource meter, serializer, parser, or numeric index encoding. The universal kernel theorem is about the given Lean AST construction under ObserverCore semantics.

## Exclusions

No formal numeric-code many-one reduction, arity-index hardness, universal interpreter PR theorem, PR-derivation-to-grammar completeness, byte/numeric serialization refinement, general soft-mass membership, tagged Pi3 compiler correctness, novelty, canonical adoption or whole-programme closure follows merely from this seal. It does close the earlier row-level gap between the mathematical prefix family and a concrete source-layout generated Lean observer statement.
