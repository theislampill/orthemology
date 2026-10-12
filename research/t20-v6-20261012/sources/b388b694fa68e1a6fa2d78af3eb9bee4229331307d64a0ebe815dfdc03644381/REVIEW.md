# Independent review: separating scalar projection and finite-moment recovery

9 October 2026 UTC. **PASS for the bounded algebraic claims below.** No correctness defect or blocking scope mismatch was found. This is a separate internal formal review, not external peer review, an audit-governor decision, integration approval, or T20/T21 closure.

## Verification performed

The final ten source/configuration/control/verifier files were copied into an isolated review package. Its local project `.lake/build` directory did not exist at the start. The pinned dependency repositories and artifacts were separately copied, not linked back to the author package; no author-project `.olean` was copied. All 1,526 copied dependency `.olean` files matched before and after review: 1,524 dependency build-library artifacts and two Lake configuration artifacts. The only dependency symlink is the existing relative documentation link `batteries/docs/README.md -> ../README.md`, internal to the copied dependency.

From **22:34:51 to 22:35:19 UTC**, the independent run completed the final author verifier with exit 0:

```sh
LEAN_BIN=private-locator:ef41bb94ad8341423d54 bash verify.sh
```

This ran `lake build` on the four configured targets and then directly invoked Lean on each of `MomentRecovery.lean`, `SeparatingProjection.lean`, `Checks.lean`, and `Verify.lean`, freshly re-elaborating every local successful source. It audited the full declaration inventory and checked both expected failures. No source changes were required by the reviewer.

The additional reviewer-created `ReviewChecks.lean` then passed with exit 0 under `lake env lean ReviewChecks.lean`. It proves eight additional checks and prints the actual elaborated quantifiers plus axiom dependencies of five relevant imported lemmas.

The final integrity audit independently verified all ten frozen source hashes against both the clean copy and the author files; re-enumerated the 34 named author declarations and checked every axiom row; audited all eight reviewer theorems and five imported lemmas; checked the exact negative-control diagnostics; verified all nine dependency revisions and clean tracked worktrees; and rechecked all 69 predecessor-artifact hashes. Its result is in `logs/independent-integrity-audit.log` and `RECEIPT.json`.

An early message cited a pre-final `Checks.lean` inventory hash. Direct checks resolved this before completion: the clean-copy build, final frozen inventory, and author bytes all use **085afba3f65a33d1ae7ea555dcfefefe93ad148f376e25259c953f58851ade31**. The copies have distinct filesystem inodes and are byte-identical.

## Mathematical statement and proof review

1. **The input is an actual finite vector family.** The main theorem takes arbitrary natural N,d and `x : Fin N → Fin d → K`, requiring `Function.Injective x`. K is an arbitrary infinite field. The conclusion is a vector v such that the scalar coordinate sum `∑ j, v j * x i j` is injective in i. There is no assumed separating scalar support, nonsingularity, inverse identity, or interpolation premise.
2. **Vector encoding is proved injective.** `coordinatePolynomial x = ∑ j, monomial j.val (x j)`. The coefficient theorem recovers the coordinate at every j, so polynomial equality entails equality of the original vectors. Distinctness is therefore about the given vectors, not an unrelated surrogate.
3. **The nonzero-polynomial argument is substantive.** The finite product ranges over ordered unequal index pairs. Each coordinate-polynomial difference is nonzero because x is injective. Their product is nonzero over the field. The imported proved theorem `Polynomial.zero_of_eval_zero` implies that over an infinite field some t makes the product nonzero. An equality of two projections along `(1,t,…,t^(d−1))` would zero a factor, hence the product, contradicting that choice. Repeated ordered-pair factors cause no problem.
4. **The returned projection is genuinely linear.** `projectionLinearMap` proves additivity and K-homogeneity of the coordinate sum, and `exists_separating_linearMap` returns a bundled linear functional. Injectivity is restricted to the finite support; no global injection of K^d into K is asserted.
5. **Recovery follows without an extra separation assumption.** `exists_projection_recovery` chooses v before quantifying over all field-valued weight vectors. Its projected nodes are the actual sums `projection v (x i)`. It supplies both their injectivity and `recover a (record a w) = w` for every w. The inherited record contains exactly degrees 0 through N−1 and the recovery coefficients are entries of the inverse Vandermonde matrix. The inherited determinant proof, coefficient orientation, and inverse identities were freshly checked, not taken as new hypotheses.
6. **The same direction serves all weights and observables.** `exists_injective_projected_record` gives injectivity in arbitrary weights. `exists_projected_observable_reconstruction` puts the existential direction before all w and all module-valued observables f and proves the displayed coefficient formula. Thus it is not selecting a new direction separately for each w or f. No positivity, normalization, order, topology, characteristic-zero, or nonempty-support assumption is hidden in these statements.

## Edge and obstruction checks

- **N=0:** The author's existence/recovery checks compile in every finite dimension. Independently, the reviewer proves every empty-support moment is zero and recovery equals the unique empty weight vector, without needing an infinite-field hypothesis for these identities.
- **N=1:** The author obtains recovery for the sole arbitrary weight, including d=0. Independently, the reviewer proves that even the zero-dimensional zero projection retains its degree-zero moment as exactly that sole weight. The empty product in the separator proof is 1, so no extra nonemptiness assumption is needed.
- **d=0:** The author proves, over an arbitrary underlying type, that injectivity forces N≤1. The reviewer separately proves the zero-dimensional projection and coordinate polynomial are zero. The theorem therefore handles the possible cases honestly rather than asserting a nontrivial injection into a zero-dimensional space.
- **d=1:** The reviewer proves directly that the fixed first-coordinate functional already separates any injective family, without an infinitude hypothesis.
- **Duplicate vectors:** The reviewer proves that a two-element constant vector family makes every scalar projection noninjective. This is a mathematical necessity control for the distinctness hypothesis.
- **Finite fields:** The author proves that for every finite field the whole plane K², enumerated injectively by a finite index set, cannot inject into K through any scalar projection: otherwise |K|²≤|K|, contradicting |K|>1. This is a genuine counterexample to omitting infinitude from the unrestricted theorem. It does not claim that every finite-field support is unseparable.
- **Expanded-coordinate composition:** The reviewer proves that some v makes equality of the actual sums `∑ i, w i * (∑ j, v j * x i j)^r` in all retained degrees imply equality of arbitrary w,z. This checks the intended projection/moment composition without hiding it behind a renamed record.

The expected-failure controls separately reject missing `Infinite K` by a typeclass error and missing vector injectivity by a function-versus-proposition type mismatch. These test the API premises; the substantive finite-field and duplicate-support arguments above establish the corresponding mathematical obstructions.

## Foundation and provenance audit

All **34 named author definitions/theorems**, all **eight reviewer theorems**, and the **five imported lemmas** audited have only `propext`, `Classical.choice`, and `Quot.sound`. The imported lemmas are `Polynomial.zero_of_eval_zero`, `Matrix.det_vandermonde`, `Matrix.mul_nonsing_inv`, `Matrix.nonsing_inv_mul`, and `Finset.prod_ne_zero_iff`. No `sorryAx`, custom axiom, `sorry`, `admit`, `native_decide`, `unsafe`, `partial`, `implemented_by`, or `run_tac` occurs in the reviewed proof sources. `Verify.lean` contains only imports and explicit axiom-print commands.

- Lean: `leanprover/lean4:v4.19.0`, reported commit `6caaee842e94`, release x86_64 Linux.
- Lake: `5.0.0-6caaee8`.
- Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
- All nine dependency HEADs match the pinned manifest and have clean tracked worktrees. Full revision and executable-hash evidence is retained.
- The inherited lockfile root label remains `finite_moment_recovery` while the new lakefile names `separating_projection`. This is harmless inherited metadata here: the clean build used the intended current targets and exact pins. No normalization was required for the mathematical or build result.

Final principal source SHA-256 values:

```text
3cb16a5ba7f9daa392f407ae5496c0d8dfce9f59f4f2020b2c9a986d6413f96e  MomentRecovery.lean
f9dd1ffaf94b2d4b6519a59f892c1700c57a59a7df0d3d8d860307a7dec8c3e5  SeparatingProjection.lean
085afba3f65a33d1ae7ea555dcfefefe93ad148f376e25259c953f58851ade31  Checks.lean
88cd905df35be0d509ae800a04fc8aadd725783d8f080657da187fe641f03562  Verify.lean
082fd85b451f64fbdae3a9dae52c083d31901790988213b0871083632f76fbb2  verify.sh
```

All ten frozen source/config/control hashes are in `logs/frozen-source-sha256.txt` and `RECEIPT.json`. `MomentRecovery.lean` and the lockfile are byte-identical to their predecessor. All 69 files in the pre-work preservation snapshot, covering the earlier finite-moment package and ordinary tensor-continuation package including their evidence and archives, match both before and after review. The ordinary mathematical result is bound by SHA-256 `03f027122c0a908f1f6bcfcc61951223ca1fca547d8599aac2aa3437e3c01a11`. No predecessor or protected-repository edits were made.

## Exact limits

This adds kernel-checked existence of a separating scalar linear functional and connects it to the already checked finite algebraic recovery core. It does **not** formalise tensor spaces/contractions or the equality between projected scalar moments and tensor contractions. The broader tensor-moment/ODE theorem is not thereby wholly kernel-checked.

The construction is classical and noncomputable. No executable search over arbitrary fields, finite-grid quantitative bound, unknown-support reconstruction, conditioning/noise guarantee, sample complexity, or optimality claim was checked. Fisher geometry, differentiation, ODE closure/conjugacy, admissible-image invariance, trajectory existence/uniqueness, exponential tilting, and analytic observation equivalence remain outside this package. No empirical, semantic, epistemic, or noetic conclusion follows from this verification alone.

The review reused the pinned Lean installation and copied dependency artifacts, including the author's six additional polynomial dependency builds from pinned source. It did not independently rebuild the full mathlib tree or compiler/kernel. Fresh local proof elaboration, exact source binding, and an axiom audit are the trust boundary, not external attestation.

## Evidence map

- `RECEIPT.json`: machine-readable result, inputs, pins, counts, preservation, and scope.
- `logs/clean-build-transcript.log`: clean project build and direct re-elaboration, exit 0.
- `module-logs/fresh-*.log`: each direct local module check and full axiom output.
- `module-logs/control-*.log`: intended rejection diagnostics.
- `ReviewChecks.lean`, `logs/reviewer-checks.log`: eight reviewer proofs, printed quantifiers, and five imported-lemma audits.
- `logs/independent-integrity-audit.log`: independent inventory, hashes, controls, dependency and predecessor checks.
- `logs/predecessor-before.json`, `logs/predecessor-after.json`: all 69 exact preservation checks.
- `logs/dependency-pins.json`, `logs/dependency-oleans.json`, `logs/toolchain-sha256.txt`: provenance bindings.
- `frozen-sources/`: exact ten checked author inputs, excluding cache/build products.
- `audit_review.py`: original-workspace integrity helper; its workspace paths are intentional. Portable source replay uses the archived source package's `verify.sh` with the pinned dependencies.
- `SHA256SUMS`: compact review-bundle binding, excluding itself.
