# Independent exact computable-matrix review

## Verdict

**PASS: the unchanged AtomicMembership.membershipMatrix is uniformly Mathlib Computable in all four natural inputs.** The natural-coded Boolean endpoint and the standard Nat-to-Nat 0/1 characteristic endpoint are unconditional. Their fully explicit types name the original predicate and standard natural/Boolean representations. No effective-table oracle, evaluator premise, substituted predicate, fixed-index restriction, or hidden well-formedness assumption remains.

This is a new, separately frozen subject and award. The earlier evaluator archive and all 108 sealed evidence files were rechecked and remain unchanged. Its qualification was an identity baseline, not a substitute for this matrix rebuild.

## Frozen subject and reproducibility

- Author seal: `COMPUTABLE_MATRIX_SEAL.json`, SHA256 `8f2c2217b1757d497088ce226281af5605126a16ce33825901f28d089a106175`
- Author 35-target receipt: SHA256 `4b19312debc1d20ff5cb709817a6bc4aecd1a22cd172ed7dfce1144a97e3162c`
- Author 77-module closure: SHA256 `5449b0e3523a1cafd7fb2204536c3b7326f33fac1d6264b5f23cb7e21448c5ce`
- Independent receipt: `receipts/20260930T173417Z/RESULT.json`, SHA256 `651d9d4578808d51a9d6a386e4ab47ecfc546839a44aeee61a3b795579c2d75c`

All 77 frozen sources plus four author/reviewer audit-control modules were copied and freshly rebuilt in an isolated library: **81 custom modules**. No author or other preexisting custom `.olean` was a build input. Lean was exactly 4.19.0, commit `6caaee842e94`. Only the official Mathlib cache at `c44e0c8ee63ca166450922a373c7409c5d26b00b` and its eight exact clean pinned dependency checkouts were reused.

All **321 selected public declarations** had full explicit type and transitive axiom readback. This includes every one of the 35 new author targets, all six root arithmetic theorems, the exact original predicate/table, inherited Uniform declarations, and independent controls. Every axiom footprint is contained in `{propext, Classical.choice, Quot.sound}`. The 81-source token scan found no sorry, admit, axiom, unsafe, implemented_by, native_decide, or opaque tokens outside comments/strings.

Every sealed file, all 77 source hashes, all 35 target identities/axiom sets, and the author audit source match. The new snapshot preserves all 35 shared evaluator sources and all 51 shared original atomic-membership sources. Two older supplemental modules, FixedIndexPrimrec and FiniteTableWitnesses, are not imported by this subject. The original NumericMembership and FiniteOutputTable definitions are unchanged. Source and author-seal drift checks passed. See `SOURCE_BINDING_RESULT.json` and `PRESERVED_EVALUATOR_ARTIFACTS.json`.

## Exactness findings

1. **Enumeration.** `allWords N` contains exactly the Boolean lists of length N and is duplicate-free. The false/true head cases are disjoint. Its Finset image is the entire finite-function word space `Fin N → Bool`, and the generic sum bridge uses the injectivity of `List.ofFn`. Independent controls prove length exactly `2^N`, including one empty word at N=0.
2. **Available prefixes.** `outputList` calls the actual numeric evaluator at position i on the sentinel code of exactly the first i+1 source bits. The list/vector theorem identifies every output coordinate with the original `finiteOutput`. The first stage never receives the whole later source word. Wrong-length output targets have count zero.
3. **Actual fibers.** `wordCount_exact` identifies the duplicate-free list filter length with the original `preimageWords` cardinality. It applies uniformly to arbitrary indices, horizons and words. No cylinder-mass oracle is supplied.
4. **Mass, not class count.** If c(w) is a source-fiber cardinality, `heavyCount` sums c(w), not 1, for each output class satisfying `2^N ≤ c(w)*2^k`. The exact bridge proves `rationalHeavyMass (indexTable e) k N = heavyCount(e,k,N)/2^N`. Threshold comparison is inclusive, and the denominator is exactly `2^N`.
5. **Original rational implication.** For `Nat.unpair i = (a,d)`, the unchanged matrix is proved equivalent to `d=0 ∨ d≤a ∨ a*2^N≤d*heavyCount(e,k,N)`. Root MatrixArithmetic digest `31fc8116bff2b69959c4c198619cd80dc05e1ed3f5529a2fe5ea5e9c33b1d994` is included and independently audited. Its sole positive-denominator-size premise is discharged by `0<2^N`; no unproved bound on the heavy numerator is required.
6. **Uniform computation.** Enumeration, sentinel coding and variable list take are primitive recursive. Computable list mapping is proved by finite range recursion and exact indexed lookup, with the outside-range default proved irrelevant. Actual output, fiber and heavy counts use the already certified joint evaluator computation. The final Boolean equality returns to `decide (AtomicMembership.membershipMatrix ...)`, and the characteristic theorem returns the same decision as standard 0/1 naturals.

## Adversarial controls

**40 independent successful kernel theorems** cover complete enumeration, output lengths, exact four-input and Nat-coded types, pairing roundtrip, the original/integer Boolean equality, and an independent Nat-to-Nat characteristic formulation. They include:

- N=0: one empty source word, heavy count 1 for every index and threshold, and true matrix for every rational code
- Zero numerator and zero denominator, with arbitrary remaining inputs
- All rationals at or above one, whose implication is vacuous even when heavy mass is zero
- Arbitrary positive common-factor rational scaling; a concrete counterexample explains why zero scaling is excluded
- Inclusive integer/rational ties and rejection above the true mass
- Invalid numeric index and nonbinary arity fallback, retaining the original point-mass zero-output law
- Identity-bit and mixed-output programs, plus an explicit prefix-stream control

At depth two the mixed-output program has fiber sizes 1,1,2,0. Threshold 1/2 selects one class with mass numerator 2. The matrix accepts q=1/2 and its redundant code 2/4, rejects q=3/4, and distinguishes probability mass from merely counting selected classes.

**480 compiled rows / 1,440 exact comparisons** also pass an independent Python Fraction and Boolean-map counting oracle. Each row checks the new heavy numerator, new integer gate, and original rational membership decision. Cases cover invalid, echo and mixed observers; depths and thresholds 0–3; and ten rational codes including zero denominators, redundant fractions, ties, one, and greater than one. These finite rows are supplemental regression evidence, not proofs of the infinite normal form.

All **10 expected-failure controls** failed for the intended reason: unweighted class counting, feeding the whole source word too early, strict heavy threshold, a wrong dyadic denominator, rejecting zero denominator, treating q=1 as nonvacuous, excluding a rational tie, duplicate enumeration, dropping positive scaling, and relabeling the Computable matrix theorem as Primrec. The last is a type-level qualification guard, not a theorem that the matrix is non-Primrec.

## Separate evaluator sharpness supplement

The root-supplied `NonPRBoundary.lean`, SHA256 `23bb1d13eade0f4370c034224a6ca2afb4115e8fb784d9140d2bb4a09ed29857`, was independently inspected, copied, compiled against this freshly built closure, and had both full types and axioms audited. Its separate receipt is `receipts/20260930T173417Z/sharpness/RESULT.json`; both footprints are standard.

It proves `evaluateIndex e n word < 2` for all inputs and then proves the exact triple-input evaluator is **not** Primrec. Under an assumed joint PR evaluator, sealed PR coverage produces a two-input program computing the diagonal evaluation plus one. Its actual serialized self-index forces `v = (v+1)%2` while `v<2`, a contradiction. The argument needs the existence of that compiled program, not an algorithm extracting code from erased proof objects.

Combined with the separately qualified Computable evaluator, this gives the expected sharp boundary: computable universal evaluation, but no uniformly primitive-recursive universal evaluator. It does not prove non-primitive-recursiveness of the membership matrix. This supplement alters neither frozen subject nor the earlier evaluator award.

## Quantified-property boundary

The result supplies an internally certified computable finite matrix for the existing equivalence

`e ∈ zeroDefectIndices ↔ ∀ i, ∃ k, ∀ N, membershipMatrix e i k N`.

The infinite quantified property is not thereby decided. No finite horizon or collection of successful tests decides that property, and the packet does not claim a Computable characteristic function for `zeroDefectIndices`. The exact quantifier order remains in the logical equivalence.

This closes the uniform finite-matrix Computable gap. It does not add a general mechanized arithmetical-hierarchy framework or independently re-award the lower reduction. Uniform PR for evaluator-dependent tables, runtime/bit-complexity bounds, full Python host-resource refinement, historical novelty and canonical adoption remain outside the claim.
