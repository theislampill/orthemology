# Independent review: full-functional Lean countermodel

Date: 2026-10-10 UTC.

## Verdict

**PASS. The frozen sources define an actual real-linear functional on the whole algebra `MvPolynomial (Fin 2) ℝ`, prove its normalization and strict positivity on every nonzero polynomial square, and prove that its value on the actual polynomial `1+x⁴y²+x²y⁴−x²y²` is −1 although that polynomial is everywhere at least 3/4. No mathematical or formal repair is required.**

This is an all-degree kernel-checked algebraic countermodel. It is stronger than scalar-only Lean support or finite-prefix testing. The final theorem has no assumed functional, positivity hypothesis, degree bound, or conclusion-shaped premise. The independent review includes an explicitly typed closed-theorem check, a symbolic unbounded-degree check, and a formal demonstration that every finite total-degree tail cutoff loses strict square positivity.

This is an evidence review, not permission to integrate, mutate protected sources, or declare any broader audit closed.

## 1. Exact target and independent replay

Author packet: `full-functional-lean-20261010/`.

Author frozen manifest SHA-256:

`9019e221673e39162216e2d5538ce836ec3d89c07e8350f13e11368b5b5ae8c6`

All 37 files listed in that manifest were verified unchanged before and after the controls. The seven logical sources were copied into this review's `frozen-target/`, checked against the author freeze, and independently compiled into `replay/` using Lean 4.19.0 with `--trust=0`. No author object was used for a local proof-module import. Direct dependency paths and object hashes were recorded immediately before each compilation. The review's `LEAN_PATH` contains its own replay directory followed only by the retained package build-library paths.

Logical source SHA-256 values:

- `Indexing.lean`: `0951cf0a1179fb1e7269e6685670a051a576dd287baed4484e865cc7c2936483`
- `Schur.lean`: `7c915bb42fc3ef8c2a1412e6f92a950036905097b34c4176b02780de6af277e1`
- `Recurrence.lean`: `c70eb5dfad5008c5263e8a504bf17c9446fdee20b61c03658fd7f3b79336a256`
- `Moment.lean`: `e57aee2a07b9827639345e3c2ff6c22cb04c274af501115de5edfa61b1370708`
- `PolynomialBridge.lean`: `40f29f860697ca19bcf7e1372fdb9ffb7af3b9e21b7eea5fba89cbdcd8f7824f`
- `ScalarSupport.lean`: `07098745a89d4948f7fb72fd05b7cf32cb4469d628b6671689a5e4769e16b526`
- `Countermodel.lean`: `7ebe9f1bc3b7e7e8d7fb966a5b0c82f7fa9a53d84e6d0887b260847fed1e443e`

All seven compilations passed. The 22 printed author theorem axiom sets and four independent positive-control axiom sets contain only `propext`, `Classical.choice`, and `Quot.sound`. The seven logical sources contain no `sorry`, `admit`, introduced `axiom`, `native_decide`, `implemented_by`, or `unsafe` token. In particular, the final theorem's transitive axiom audit contains no `sorryAx` or added assumption axiom.

The actual successfully imported environment reports **2,775 modules**. `IMPORT_CLOSURE.json` binds every module to its resolved `.olean` and a source file with SHA-256 hashes. Toolchain executable and shared-library hashes are recorded too. The seven local author modules were freshly compiled from the exact bound source files. For retained dependencies, source/object hashing binds the inspected environment; it is not a claim that this review rebuilt those dependencies or independently established their source-to-object compilation provenance. Their imported objects were subjected to Lean's trust-zero import checking. No baseline build was run.

Primary machine receipts: `BUILD_RECEIPT.json`, `CONTROL_RECEIPT.json`, `SOURCE_MANIFEST.json`, and `IMPORT_CLOSURE.json`. The corresponding source files, generated local objects, and full compiler logs are retained.

## 2. Semantic and code audit

### Indexing, inverse, and universal causality

`Indexing.lean:35–56` implements the exceptional ten-element ordering followed by complete total-degree shells. `index_injective`, `index_successor`, `index_surjective`, and `positiveIndex_bijective` prove the complete bijection with the positive natural numbers. Surjectivity is induction over all naturals, not a bounded enumeration test.

`exponentAt` at line 249 uses `Classical.choose` to obtain the unique exponent for a zero-based position. Both inverse directions and injectivity are proved. This is a sound noncomputable inverse, with its use of choice exposed in the standard axiom audits. It is not an executable integer-square-root implementation or a formal verification of the Python enumerator.

The central `midpoint_precedes` theorem at line 115 covers all distinct exponent pairs with componentwise-even sum. Its finite small-degree case exhausts all ten exceptional pairs; its remaining cases use lower total degree or strict second-coordinate ordering within a shell. Equality of endpoints is handled separately by the weaker `midpoint_index_le`. Thus a new off-diagonal even moment is already assigned, while the diagonal may be new. `seed_parity_separated` correctly establishes that the first four monomials have pairwise different parity classes.

### Schur extension and the actual recursive state

`Schur.lean:14` defines positivity using all nonzero real vectors. The block formulas are actual matrices. `completed_square` proves the quadratic-form identity with the unit slack; `extend_positive` splits the last coordinate into zero/nonzero cases and establishes strict positivity. The inverse block update is proved by its action on every vector and then matrix extensionality. There is no numerical solver, unproved inverse-existence requirement, or positivity oracle.

`Recurrence.lean` constructs the finite index type of size `n+4`, proves the position injection/surjection, and starts from `diag(1,1,1,4)` with the displayed reciprocal diagonal. Its data record contains matrices, not assumed positivity certificates. Initial and extension invariants are theorems about those matrices. The generic `stages` theorem is sound, but the final construction also has its own concrete `Moment.state` and concrete invariant proof; the final result does not rely on an unspecified choice of good columns.

`Moment.lean:33–43` selects each column from parity-compatible midpoint moments, defines the new diagonal as `1 + vᵀ B v`, updates exactly the new index, and recurses over all naturals. The arbitrary placeholder values of `initialJ` beyond its seed do not supply unproved future moments: `column_precedes` establishes that every used off-diagonal entry is within the already assigned range. `first_gram` and `next_gram` bind the matrices to their moment entries, including repeated sums of exponents.

`state_J_stable` and `state_J_compatible` prove prefix consistency. `J k := (state k).J k` chooses a sufficiently advanced finite stage for every index, and `J_eq_state` proves agreement with any stage that contains that index. Consequently this is one global moment sequence, not a collection of unrelated positive prefixes. `gram_eq_state` identifies its Gram matrix with the actual recursively constructed matrix. `gram_positive` proves positivity at every recursive size `n+4`, with no positivity or degree assumption. These sizes suffice for every polynomial support.

### The complete polynomial algebra and finite-support bridge

`PolynomialBridge.lean:12` makes `Polynomial` an abbreviation for standard `MvPolynomial (Fin 2) ℝ`. Encoding and decoding prove the equivalence between pairs of natural exponents and the standard finitely supported multi-exponents.

`functional` at line 39 is `Finsupp.linearCombination ℝ` of the full moment sequence. It is an actual real-linear map on the full polynomial algebra, not a scalar stand-in or a finite-dimensional truncation.

`support_fits` takes the finite supremum of the actual polynomial's support indices and uses position surjectivity and the inverse indexing lemmas. The stage depends on the given polynomial. `expand_of_support_fits` proves coefficientwise equality, including zero coefficients outside the original support and uniqueness of coordinates. `finite_expansion` therefore applies to every polynomial.

`functional_square_expansion` proves that evaluating the square of the finite monomial expansion gives its Gram quadratic form. `square_strict_positive` obtains a nonzero coefficient vector from a nonzero polynomial and applies its explicit Gram-positivity hypothesis. This intermediate general theorem is appropriately conditional. `Countermodel.strict_square_positive` discharges that hypothesis using the actual `FullFunctionalMoment.gram_positive`; it does not carry it into the final theorem.

### Actual witness evaluation and final theorem

`Countermodel.lean:9` defines `Λ` from the actual global moment sequence. Normalization reduces to the actual zeroth moment. `witness` at line 19 is the polynomial expression in the standard generators `X 0` and `X 1`.

`witness_negative` uses the proved monomial-functional evaluation rules and the four proved seed moments to establish `Λ witness = -1`. It is not merely the unrelated scalar arithmetic `1+1+1−4=-1`.

`witness_eval` proves equality between standard `MvPolynomial.eval` of that witness and the scalar function in `ScalarSupport`. The scalar lower bound then yields the actual all-point evaluation bound. `full_polynomial_countermodel` packages a closed existential statement with normalization, universal strict square positivity, the actual evaluation bound, and the negative functional value. `not_pointwise_positive` derives the exact algebraic failure of positivity on pointwise nonnegative polynomials. The added nonnegativity and finite-sum-of-squares lemmas are valid immediate consequences.

## 3. Independent controls

`controls/PositiveChecks.lean` passed at trust zero and supplies:

1. A separately written closed theorem with the full explicit `MvPolynomial (Fin 2) ℝ` type, ordinary real-linear map, universal nonzero-polynomial quantifier, explicit witness expression, standard evaluation, and exact values. This rejects theorem-type or hidden-premise drift.
2. Strict positivity for `((X 0)^(n+1000))²` for **arbitrary natural n**, and for `p*p` for an arbitrary nonzero polynomial without a degree premise.
3. A formal cutoff control for **every natural N**: zeroing the actual moment sequence above total degree N preserves the prefix through N, but sends the square of the nonzero monomial `x^(N+1)` to zero. Hence every such finite truncation fails the universal strict-square assertion. This specifically distinguishes a full construction from long finite testing.

Seven independent false controls all exited unsuccessfully for mathematical proof failures or type mismatches after imports resolved:

- `FalseWitnessPositive`: the claim `0 ≤ Λ witness`.
- `FalseZeroStrict`: strict positivity of the zero polynomial square.
- `FalseArbitraryMomentPositive`: replacing the actual moment sequence by an arbitrary sequence while trying to reuse its Gram-positivity theorem.
- `FalsePremiseErasure`: deleting the essential nonzero-polynomial premise.
- `FalseScalarPolynomialIdentity`: identifying `Λ witness` with the scalar value `F 0 0`.
- `FalseFiniteCutoffStrict`: strict positivity of the high square killed by any finite cutoff.
- `FalseSchurNoSlack`: deleting the unit slack in the two Schur target expressions while retaining their proof. The completed-square equality leaves the missing `t²` term as an unsolved mathematical goal.

No control failed because of a missing import, unknown identifier, or parser error. These are diagnostic controls, not independent axioms and not substitutes for the universal proof.

## 4. Scope boundaries and relation to prior evidence

This review adds full-functional algebraic Lean evidence to the separately accepted ordinary construction with frozen `PROOF.md` SHA-256:

`08fdec67591a4a0639fa4ca721293bd8c480ec405dcd1a7c5a08d3244aa84c80`

The earlier `full-polynomial-moment-independent-review-20261010/REVIEW.md` correctly described its own then-current scalar-only Lean evidence. It remains unchanged as a historical bounded review. The present report is the additive upgrade for this new exact source packet.

The present Lean packet does **not** formalize correspondence to the computable rational Python recurrence, dyadic computability, determinant exactly 4, practical evaluation of arbitrary real inputs, or measure integration/nonexistence within Lean's measure theory. The algebraic separation implies the familiar positive-measure obstruction when combined with the usual integral representation properties; that implication was already covered by the separately accepted ordinary proof. It must not be reported as a new Lean measure-theoretic theorem here.

The construction is bivariate and full-functional. It does not extend the earlier particular finite ternary truncated datum, repair its higher-degree failure, or erase that failure. It also does not by itself constitute a new rank-classification, heat/diffusion, or protected integration certificate.

No author source, prior review, protected source, baseline library, integration state, or closure state was edited. The independent reviewer worked only in this review-owned directory. There are no requested author fixes.

## 5. Replay

From the workspace root, using the existing retained toolchain and dependencies:

    python3 full-functional-lean-independent-review-20261010/replay.py
    python3 full-functional-lean-independent-review-20261010/check_controls.py

The first command independently rebuilds the seven frozen source copies and records import/object bindings. The second checks the author packet freeze, compiles the explicit positive controls, rejects all seven false controls, records the actual complete import closure, and verifies the author packet remained unchanged. Both write only in the independent review directory.
