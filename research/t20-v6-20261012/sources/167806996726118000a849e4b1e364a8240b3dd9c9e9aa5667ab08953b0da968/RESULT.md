# Literal rational-shift probability and defect bridge

## Result

The original literal selector/replay compiler's **source-lowered typed AST** now has the exact fair-source affine defect theorem in Lean:

`compileShift_defect body output a b hb hab`

For every finite `ObserverCore.Stmt` body, every natural output register, and every natural numerator/denominator satisfying `0 < b` and `a ≤ b`,

\[
D(\lambda_*\,\mathrm{compiledOutput}(body,output,a,b))
= a/b+(1-a/b)D(\lambda_*\,\mathrm{baseOutput}(body,output)).
\]

Here `λ` is the existing fair Cantor product measure, the notation means its actual pushforward by the displayed observer, and `D(μ) = 1 - (mass μ).toReal` is the inherited atomic defect. `mass μ` is the measure of the points having positive singleton mass. There is no assumption supplying the compiler's output law, stopping probabilities, or a null exceptional set: all are proved and discharged internally.

The result includes zero and one endpoints and unreduced rational representations. It does not replace the literal compiler with the previously formalised unary-tag compiler.

## Exact coverage

The five new modules export 64 theorems:

- `LiteralShiftPersistence`: 6. Nested literal cells preserve a resolved side. An eventual side classification is equivalent to a first cut on that side.
- `LiteralShiftWeights`: 16. Fair prefix payload fibres, finite lower-cell counts, the limiting below/above probabilities, measurable disjoint side events, and a null indefinitely unresolved boundary.
- `LiteralShiftMixture`: 30. Actual stopping-word cylinders, their disjointness, exact prefix-retaining branch laws, the countable pushforward decomposition, and atomic-mass transport.
- `LiteralShiftDefect`: 8. The final unconditional mixture, total/below/above stopping weights, atomic-mass formula, affine defect formula, and endpoint corollaries.
- `LiteralShiftFirstBit`: 4. Every literal output retains its fair first bit, and zero shift of a constantly-zero base has a law different from the base law. These are semantic/probability guardrails against dropping the stopping prefix.

Seven earlier literal AST/finite/pointwise modules are reused unchanged. The new development relies on their actual copied-prefix and fresh-tail replay statements. The inherited source-lowered AST still uses the original Python sorted-support compression, fresh registers from 12, exact reset/argument sequence, snapshot-loop semantics, suffix sentinel and replay guard.

## Probability argument, now kernel checked

### 1. Actual finite selector probabilities

For a depth `N`, the binary prefix payload is uniformly distributed over the integers below `2^N`. The proof constructs a finite binary-word/payload equivalence and applies the inherited fair-cylinder law.

A cell is below exactly when

`b * (payload + 1) ≤ a * 2^N`.

Thus the below-cell event has measure

\[
\frac{\lfloor a2^N/b\rfloor}{2^N}.
\]

For positive `N`, persistence identifies this event with resolution below by that stage. The source never inspects the empty prefix; no depth-zero scanner stop is introduced.

The floor ratio lies between `a/b − 2^(−N)` and `a/b`. Monotone continuity of measure gives total eventual-below probability `a/b`. At every positive depth, all still-unresolved streams share at most one payload value. Its cylinder has measure `2^(−N)`, which tends to zero. This proves the unresolved event null without selecting a binary expansion, assuming termination, or constructing a real-valued uniform random variable.

The measurable below and above events are disjoint and jointly cover the complement of that null set. Hence above probability is `1 − a/b`. This route does not require a separate finite-stage ceiling-count lemma.

### 2. Actual stopping-prefix law

A stopping leaf records a positive length `k`, an actual word `u : Fin k → Bool`, and its side. Its defining proposition is the literal `FirstCut` condition on a fixed completion of `u`. Prefix causality proves this condition is the same for every stream in that cylinder.

Each source cylinder has weight `2^(−k)`. Distinct leaf cylinders are disjoint and cover almost every source stream. The previously proved literal splice semantics and unchanged `PrefixTail.restricted_tail_law` yield:

- Below leaf: `2^(−k)` times the fair law embedded after copied prefix `u`.
- Above leaf: `2^(−k)` times the base observer's law embedded after copied prefix `u`.

`compileShift_probability_law` states their exact countable sum. `compileShift_total_weight`, `compileShift_below_weight`, and `compileShift_above_weight` give total coefficients `1`, `a/b`, and `1−a/b` over these actual stopping leaves.

### 3. Atomic mass and defect

Prefix embedding has a measurable left inverse (drop the prefix), so it preserves atomic mass by the inherited two-direction `mass_map_mono` argument. A narrowly adapted countable-index version of inherited `mass_mixture` permits finite-word leaves instead of a natural-number index. Fair Cantor measure has zero atomic mass.

Consequently:

\[
\operatorname{mass}(\mathrm{compiledLaw})
=(1-a/b)\operatorname{mass}(\mathrm{baseLaw}).
\]

The real-valued affine defect theorem follows with the required ENNReal subtraction bounds and finiteness established. No probability premise survives in the final theorem.

## Guardrails

The actual law is generally **not** the bare mixture `q · fair + (1−q) · baseLaw`. Every literal output has first-bit-one probability `1/2`, including at `q=0`. With a constantly-zero base, zero shift therefore has a different whole law from the base, although it has the same defect. `literal_zero_law_ne_base` proves this distinction.

Two intended-false files are required to fail for actual contradiction:

1. Zero-shift law equals the constantly-zero base law, dropping the copied prefix.
2. Unit-shift defect is zero rather than one.

Their known true kernel consequences simplify each false assertion to `False`; `decide` rejects it. Import, name-resolution or reduction failure does not count as a successful negative control.

## Credit and remaining boundaries

The original P02 ordinary proofs already own universal stream correspondence, rational stopping-cylinder probability mathematics, affine defect correctness, and the ordinary uniform primitive-recursive coding/construction argument. In particular, retained `CV_C_CODEC_AND_CORRESPONDENCE.md` and `CV_C_HIERARCHY.md` are inputs here. This is a kernel completion at the literal-AST probability boundary, not a new ordinary probability result or threshold classification.

Existing kernel owners supply the evaluator, finite-support hygiene/inlining, fair product measure, arbitrary-prefix tail disintegration, measurability of productive numerical prefix observers, and atomic-mass principles. The earlier unary-tag rational realisation remains valid but proves a different compiler. No unary tag law is substituted for the literal stopping-word law.

The new kernel theorem concerns the pinned source-lowered `ObserverCore` AST. The Python-source transcription is an ordinary reviewed correspondence, preserved from the prior artifact. No new theorem parses Python source, proves the Python host implementation, proves exact original variadic-serialization byte/numeric-code identity, or guarantees successful host compilation/execution under arbitrary resource limits. The Python body must be a finite grammar-wellformed arity-two observer; raw `Program` instances do not establish that hypothesis automatically.

Explicit `Set`-event trace refinement remains ordinary. The probability bridge does not add a trace model. It also does not separately classify existence/uniqueness of every binary boundary expansion; the null-set theorem is sufficient and is proved directly. No protected repository edit, integration, owner acceptance, or whole-project/T20 closure is asserted.

## Reproduction and evidence

Use the pinned official Lean 4.19.0 toolchain and exact Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`, whose acquisition manifest is included. The dependency environment is external to this small proof package.

1. Set `LEAN_HOME`, `PATH`, and the pinned dependency `LEAN_PATH` (the restoration environment script is available in the current workspace).
2. Run `python build_prerequisites.py` to rebuild only the unchanged required prerequisite closure.
3. Run `python verify_final.py` for an isolated replay of the seven inherited literal modules and all five new modules, theorem-type/axiom readback, and the two intended-false controls.

`SOURCE_PINS.json`, `PREREQUISITE_REBUILD.json`, and `FINAL_REPLAY.json` bind source bytes and observed outputs. Independent review is included separately when final. Toolchain acquisition and dependency setup are not mathematical research results. Integrity verification is not a substitute for a Lean replay.
