# Independent formal review: finite moment recovery

9 October 2026 UTC. **PASS for the bounded algebraic claims below.** No correctness defect or blocking scope mismatch was found in the reviewed proof sources. This is a separate internal formal review, not external peer review, an audit-governor decision, release/integration approval, or T20/T21 closure.

## What was independently verified

The final four author source files were copied into an isolated review package. Its project build directory did not exist before review. Existing pinned dependency repositories and their compiled caches were separately copied, not symlinked; no author project `.olean` was copied. The author package was not modified and dependencies were not downloaded again.

The clean-copy run completed successfully from 22:05:33 to 22:05:58 UTC. It ran `lake build MomentRecovery Counterexample Checks Verify`, then invoked Lean directly on each source to force fresh local re-elaboration. All four modules passed. After the author strengthened only the verifier's audit-row completeness check, the final script was copied and the complete verification repeated from 22:07:12 to 22:07:28 UTC, again with exit 0. This second Lake invocation reused the review package's build, but its four direct Lean invocations still freshly re-elaborated every local source.

Actual command, from the review package:

```sh
LEAN_BIN=private-locator:ef41bb94ad8341423d54 bash verify.sh
```

The relevant commands inside that checked script are:

```sh
lake build MomentRecovery Counterexample Checks Verify
for module in MomentRecovery Counterexample Checks Verify; do
  lake env lean -o ".lake/build/lib/lean/$module.olean" "$module.lean"
done
lake env lean controls/RejectFalseCubic.lean
lake env lean controls/RejectMissingDistinctness.lean
```

The last two commands are required to fail and did fail for the intended type mismatches. The false cubic value `1/53` cannot replace the proved `1/54`; the recovery application without the distinctness argument is rejected. These are API/type-checker sanity controls, not an independent mathematical proof that distinctness is necessary.

Additional reviewer-created `ReviewChecks.lean` passed using `lake env lean ReviewChecks.lean`. It inspects elaborated theorem quantifiers, audits the imported determinant/inverse lemmas, checks that all empty-support moments vanish, checks that the one-point record is literally its arbitrary weight, and applies the general recovery theorem to the displayed four-point support.

## Statement and proof review

1. **The record is genuinely the finite moment record.** `moment a w r` is the actual finite sum of `w j * (a j)^r`. `record` is indexed by `Fin N`, so it contains exactly degrees 0 through N−1. The weights and scalar nodes are arbitrary functions `Fin N → K`, with `K` an arbitrary field.
2. **Invertibility is proved from node distinctness.** `determinant_ne_zero` rewrites mathlib's proved Vandermonde determinant formula and proves each difference factor nonzero using `Function.Injective a`. It does not assume nonsingularity, interpolation, moment injectivity, or an inverse identity.
3. **The matrix orientation and recovery formula match.** Mathlib's Vandermonde has node index in its row and degree in its column. The record is `w ᵥ* V`, and the defined coefficients are `(V⁻¹) r j`. Thus the stated reconstruction is `(w ᵥ* V) ᵥ* V⁻¹`. The two proved nonsingular-inverse identities establish both recovery directions.
4. **Recovery and injectivity are substantive conclusions.** `recover_record`, `record_recover`, `weight_eq_sum_moments`, `weights_eq_of_moments_eq`, and `recordLinearEquiv` establish explicit reconstruction, uniqueness, and a linear equivalence of the full field-valued weight and moment spaces.
5. **Higher-observable reconstruction is genuine algebra.** Scalar observables and all natural-degree scalar moments have fixed support-dependent coefficient formulas. The vector theorem is quantified over any `AddCommGroup V` and `Module K V`; its proof distributes scalar multiplication and exchanges finite sums. No finite-dimensionality, norm, topology, order, positivity, normalisation, or characteristic-zero assumption is hidden in it.
6. **Edge cases are included.** N=0 has empty weights/record and identically zero moments. N=1 has one retained degree-zero moment, equal to the sole arbitrary weight. Both the author's generic instantiations and the reviewer's direct finite-sum checks compile.
7. **The exact four-point example is the intended one.** The support is `(0, 1/3, 2/3, 1)`, the two strictly positive weights are `(5,9,3,7)/24` and `(7,3,9,5)/24`, and both sum to one. Their common moments in degrees 0,1,2 are `1, 1/2, 7/18`. Their cubic moments are `37/108` and `35/108`, giving plus-minus difference `1/54`. The formal conjunction proves these properties and inequality of the atomic mass functions. Support membership in `[0,1]` is proved separately. The concrete moments are definitionally the generic moments at this support.

## Foundation audit

The review independently enumerated all named definitions/theorems in the two proof modules and matched that inventory exactly against the audit output: **43 declarations, each printed exactly once**. Every axiom set was exactly:

```text
[propext, Classical.choice, Quot.sound]
```

The imported `Matrix.det_vandermonde`, `Matrix.mul_nonsing_inv`, and `Matrix.nonsing_inv_mul` also printed only those standard axioms. There was no `sorryAx`, custom axiom dependency, `sorry`, `admit`, `native_decide`, `unsafe`, `partial`, `implemented_by`, or `run_tac` proof escape in the reviewed proof sources. `Verify.lean` consists only of imports and explicit axiom-print commands. The four anonymous examples in `Checks.lean` and three additional reviewer examples were freshly compiled as well.

## Exact pins and source binding

- Lean: `leanprover/lean4:v4.19.0`, reported commit `6caaee842e94`, release x86_64 Linux.
- Lake: `5.0.0-6caaee8`, Lean 4.19.0.
- Mathlib: tag `v4.19.0`, Git `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
- All nine dependency Git HEADs matched `lake-manifest.json`, with clean tracked worktrees. Exact transitive revisions are retained in the manifest and inventory log.

SHA-256 of the final author source and verifier:

```text
3cb16a5ba7f9daa392f407ae5496c0d8dfce9f59f4f2020b2c9a986d6413f96e  MomentRecovery.lean
b67f13e36948ae748064107ebae114b57fe2f5e81c11905583100803d9b69414  Counterexample.lean
3fc81aaacac49b768536335271f41a0a739c42aaffefc312f8feacbc57101450  Checks.lean
cf1a4f109b2a0a82ef38d8a99519662be7eac83b2ea0b0b5dbbcf6ef5b07ded0  Verify.lean
c91524b5ae254902dc7cbd3e921f4dd2e4a785e6a9395006cc9eef892fbdca38  verify.sh
```

Final byte comparisons confirmed that the proof sources, configuration, manifest, toolchain file, and verifier remained identical to the author's frozen package. The ordinary mathematical source reviewed was `tensor-moment-continuation-20261009/RESULT.md`, SHA-256 `03f027122c0a908f1f6bcfcc61951223ca1fca547d8599aac2aa3437e3c01a11`.

## Precise limits of the result

This is fresh checking of the local finite algebraic proof against pinned imported foundations. The official precompiled dependency cache was reused; the full mathlib dependency tree and Lean compiler/kernel were **not rebuilt independently**. The review shares the existing Lean installation and dependency provenance with the author. The ordinary result and protected source material were read, not modified.

The general theorem starts with **distinct scalar nodes already supplied**. It does not kernel-prove that arbitrary distinct multivariate support has a separating scalar projection. The module-observable theorem applies to any chosen module-valued observables, but no tensor-space/contraction representation is instantiated here. The concrete `law` is a finite atomic mass function, not a formalised probability measure or measure integral.

No kernel credit is assigned to Fisher geometry, differentiation, the tensor moment hierarchy, closed ODEs or their conjugacy, preservation of admissible states, trajectory existence/uniqueness, exponential tilts, analytic observation equivalence, second-derivative interpretation of the cubic gap, or general degree-optimality claims. These remain outside this package. The inverse construction is a noncomputable Lean definition, and the theorem is not an executable real-number reconstruction algorithm or a stability, noise, sampling, complexity, empirical, semantic, source-authentication, or epistemic-warrant result.

## Evidence map

- `logs/independent-build-transcript.log`: first clean-project build and direct re-elaboration.
- `logs/final-verifier-transcript.log`: full repeat after verifier strengthening, exit 0.
- `logs/reviewer-checks.log`: additional reviewer examples, printed actual quantifiers, and imported-lemma axiom audits, exit 0.
- `logs/independent-inventory-audit.log`: 43-declaration completeness, final byte comparisons, all dependency pins and clean tracked worktrees.
- `logs/final-source-sha256.txt`, `logs/toolchain-sha256.txt`, `logs/ordinary-result-sha256.txt`: final input bindings.
- `module-logs/fresh-*.log`: direct fresh local source-check logs, including the full axiom output.
- `module-logs/control-*.log`: exact expected rejection diagnostics.
- `ReviewChecks.lean`: additional reviewer-only test source.

The initial snapshot log binds the earlier version of `verify.sh`; the final source hash list and final-verifier transcript supersede that script binding. The proof files did not change during review. `SHA256SUMS` binds the compact review evidence bundle.
