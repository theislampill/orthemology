# Literal rational-cell compiler: bounded implementation assurance

11 October 2026. PASS within the bounds below. No implementation defect found, no repair proposed, and no protected or original source changed. This is an incremental implementation audit of the actual P02 Python `compile_shift`, not another rational-threshold classification result and not a Lean verification.

## Prior assurance, explicitly inherited

Inspected the literal compiler, `Builder.inline`, register discovery/renaming, sentinel encoding, serializer/decoder, evaluator, and the existing P02 tests and mutation evidence before constructing this check. `CompilerTests.test_rational_shift_compilation` already compares the original compiler to an exact Fraction-based cell specification on all six-bit words, five bases and five ratios. The old suite already checks generic repeated-inline reset; its mutation evidence detects omission of reset and a wrong shift-tail mask. These are old results, not discoveries here. The existing rational-shift independent review expressly excludes this literal compiler and instead kernel-verifies a unary-tag construction.

The missing bounded check was the actual compiler's full assignment trace: output-only tests can pass even when a base is invoked too early, a tail word lacks its sentinel, or resolution happens at the wrong stage. We therefore bound fresh evidence to the original source and compare both output and every assignment event to an exact rational-cell specification plus a fresh direct invocation of the same base program.

## Executed scope and results

`check_literal.py` imports the unchanged P02 source without writing bytecode. For every exhaustive case the literal generated program passes through its original numeric encode/decode codec. It executes `run(..., trace=True)` and compares the complete assignment sequence, not just the final output.

- 89,408 exhaustive comparisons: every nonempty binary word through length seven, each integer representation 0 <= a <= b for 1 <= b <= 8, eight bases.
- 5,376 exact equivalence comparisons: ratios 0, 1, 1/2, 1/3, 2/3, 3/7, 7/8, multiplied by 2, 7 and 2^80+1, all eight-bit words. Both output and assignment trace agree with the reduced representation. No floating-point arithmetic is used.
- 640 finite prefixes of the non-dyadic boundaries 1/3, 2/3, 1/5, 3/7, 127/257, through depth 128. Every one remains unresolved, copies its current bit, and makes no base call.
- 1,280 source-guided neighboring branches: flip a generated boundary bit and append two-bit suffixes, checking both resulting tail behaviors exactly.
- 752 dyadic boundary cases: values immediately below and at selected grid endpoints through denominator 2^32, with empty, one-bit and three-bit suffixes.

The boundary generation is deterministic exact arithmetic, not random sampling or an SMT proof. The eight bases include output-register aliasing with either input, a tail-index observer, first-tail-bit observer, sentinel/length dependence, writes to input and scratch registers overlapping compiler register numbers before renaming, loop-counter/input aliasing with snapshot bounds, and an unwritten high output register. These exercise several cases outside the old five-base suite. Finite-stage comparisons imply prefix agreement only over these tested stages; they do not exhaust arbitrary programs or inputs.

## Source-faithful invariants checked

The inspected Builder allocates scan registers 3 through 11, and mapped base registers beginning at 12. The oracle binds to that literal allocation; it is intentionally not a supposedly independent replacement compiler. For each prefix it forms exact cells [v/2^j,(v+1)/2^j], chooses the first upper endpoint <= q or lower endpoint >= q, then predicts the entire trace:

1. Before resolution, scan visits every available bit and emits the source's current bit.
2. At the first resolved cell, the stopping bit is still copied; scan stops changing selector state thereafter.
3. Below q, all subsequent observed bits remain copied and no base locals are touched.
4. Above q, base execution starts strictly after the stopping prefix. The base index is tail length minus one and the input word is exactly 2^(tail length) plus the tail value.
5. Every source register, including arguments, output, read-only locals, assignment targets and loop counters, is mapped freshly and zeroed before argument installation. Direct base execution on the fresh suffix has the same mapped trace and final output modulo two.
6. q=0 and q=1 still copy one initial bit. At zero the base starts at stage one with a fresh one-bit tail; at one it is never invoked.

Reset nuance: this literal shift invokes its inlined base at most once per fresh evaluator run, and its mapped locals are disjoint from selector locals. Omitted explicit resets need not change this isolated shift's output because default absent registers already read as zero. We check that the actual helper emits all resets, but do not claim a new history-leak bug or pretend an omitted-reset output witness exists here. The original repeated-inline test remains the relevant generic reset regression.

## Negative controls and limits of independence

Four AST mutations are created only in memory; original compiler bytes are untouched. The trace comparator detects early base invocation on [1], wrong tail index on [1,0], omission of the tail sentinel on [1,0], and strict rather than inclusive boundary comparisons on [0]. The wrong-index control changes the visible bit; the other first witnesses change trace while leaving that bit unchanged. This distinction is recorded explicitly in RESULTS.json. These are deliberately injected guard controls, not found defects or claims of novel bugs.

The cell oracle uses Fraction comparisons independently of the compiler's multiplication inequalities. However, it deliberately shares the original interpreter for compiled and direct-base execution, and uses original codec/helper routines. Thus this does not independently verify `run`, the parser, register collection, the Python runtime, or arbitrary resource behavior. Resource exhaustion raises rather than becoming a semantic zero, but this audit does not prove resource bounds.

## Exact remaining formal gap

The implementation search found no repair warranted. Remaining assurance is universal, not a demonstrated finite bug: prove for every well-formed arity-two base, unit rational representation, valid sentinel prefix and stage that evaluation of this *literal generated AST* equals the rational-cell stopping/preserved-prefix/reset-tail specification, including the unresolved case. Connect that finite-stage theorem to the rational-cell stopping-word partition, fresh-tail conditional laws, prefix preservation and affine defect formula in the actual codec's semantics. Establish the required computability/code-transformer bridge at its claimed quantifier scope.

At each depth there is at most one unresolved dyadic cell: a cell strictly straddling q. A non-dyadic boundary follows such a cell at every finite depth; a dyadic cut resolves once it lies on the grid. The mathematical probability/null-boundary and affine-law arguments are inherited from P02's prose, not new discoveries or consequences of our finite tests. This audit does not establish an infinite-output law, universal termination of the selector, hardness or completeness, or T20 closure. The alternative unary-tag Lean theorem cannot substitute for verifying this literal compiler.

## Replay and byte binding

From the workspace root:

    PYTHONDONTWRITEBYTECODE=1 python literal-shift-implementation-audit-20261011/check_literal.py

RESULTS.json and replay.log record the successful execution; BINDINGS.json records source, inherited evidence, new audit, and report hashes. The original source hash before and after execution is dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c. No dependency installation or acquisition was required.
