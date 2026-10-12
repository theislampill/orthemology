# Separating scalar projections and finite moment recovery

This additive Lean 4.19.0 package closes one previously stated kernel-scope gap in the finite-moment recovery package: a finite set of distinct multivariate vectors over an infinite field has a separating scalar linear functional. It then composes that proved existence result with the previously checked scalar Vandermonde reconstruction.

This is formal verification of an established ordinary mathematical step, not a fresh mathematical discovery, historical active-time certification, protected-source integration, or T20/T21 closure.

## Exact theorem and proof

For every field K with an `Infinite K` instance, every N,d : ℕ, and every injective x : Fin N → (Fin d → K), `FiniteMoment.exists_separating_projection` proves

    ∃ v : Fin d → K,
      Function.Injective (fun i => ∑ j, v j * x i j).

There is no assumed separating direction, nonsingularity, or interpolation premise. The only mathematical assumptions are the displayed field, infinitude, and distinctness assumptions.

The stronger `exists_separating_parameter` proves that the direction can be chosen on the curve v(j)=t^(j.val). The proof is:

1. Encode each vector x(i) by its coordinate polynomial P_i(T)=∑j x(i,j) T^j. Coefficient extraction proves this encoding injective.
2. Form the finite product P(T)=∏(i,j), i≠j, (P_i(T)−P_j(T)). Each factor is nonzero by the support's injectivity, so P≠0.
3. Use mathlib's proved `Polynomial.zero_of_eval_zero` over infinite integral domains to obtain t with P(t)≠0. This is the contraposition of the finite-root argument for a nonzero polynomial.
4. Equality of two projected values would make a factor vanish at t and hence make P(t)=0, a contradiction.

`projectionLinearMap` proves that the sum formula is a K-linear functional. `exists_separating_linearMap` returns a bundled `(Fin d → K) →ₗ[K] K`, injective on the specified support.

Both the ordered-pair product and the empty product are deliberate. Repeating unordered-pair differences does not affect the nonvanishing proof. N=0 and N=1 need no special hidden premise; the product has no factors. d=0 is also honest: `Checks.zero_dimension_card_le_one` proves that injectivity forces N≤1, and the empty and singleton cases are checked explicitly.

## Composition with actual scalar recovery

`MomentRecovery.lean` is a byte-identical copy from `finite-moment-recovery-lean-20261009`, SHA-256:

    3cb16a5ba7f9daa392f407ae5496c0d8dfce9f59f4f2020b2c9a986d6413f96e

It proves the Vandermonde determinant is nonzero and constructs the inverse from known distinct scalar support. It is recompiled freshly here, rather than merely assumed or imported as a local opaque prebuilt artifact.

For a(i)=∑j v(j)x(i,j), define s(r)=∑i w(i)a(i)^r. The new theorem `exists_projection_recovery` supplies one direction v, depending on the support only, such that:

- a is injective;
- for every arbitrary field-valued weight vector w, the inherited explicit inverse reconstructs w from s(0),…,s(N−1).

`exists_injective_projected_record` states the corresponding injectivity in w. `exists_projected_observable_reconstruction` supplies one direction that reconstructs every fixed E-valued support observable, for any K-module E with an additive commutative group:

    ∑i w(i) • f(i)
      = ∑r s(r) • (∑i recoveryCoefficient(a,i,r) • f(i)).

There is no positivity, normalization, characteristic-zero, ordering, or nonempty-support assumption in these statements. The additional infinite-field requirement is used to obtain a separating direction; the inherited scalar recovery theorem itself still works over every field when distinct scalar support is supplied.

## Scope control over finite fields

`Checks.finite_field_counterexample` proves, for every finite field K, that there exist N and an injective x : Fin N → (Fin 2 → K) for which no scalar projection is injective. It enumerates the entire plane K². A hypothetical scalar injection would give |K|²≤|K|, contradicting |K|>1.

Thus dropping the infinite-field assumption from the general existence claim would be false. This is a proved universal finite-field obstruction, not just a typeclass failure. Some smaller supports over finite fields can still be separated; no contrary claim is made.

Expected-failure controls additionally confirm that Lean rejects applying the main theorem without the infinitude or distinctness premise.

## Kernel credit and limits

New kernel credit consists of coordinate-polynomial encoding/injectivity, existence of a separating scalar direction, its linear-map packaging, the resulting explicit projected finite-moment recovery and observable representation, edge cases, and the finite-field obstruction.

The package uses `noncomputable section` and classical existence. It does not implement an executable search for t or v over arbitrary K. The ordinary result's finite-grid search argument over suitably computable characteristic-zero coefficients is not separately formalised here. No exact-arithmetic oracle, computability, bit-complexity, conditioning, or stability guarantee is claimed.

Still not formalised here: construction of tensor spaces and contractions; a proof identifying projected scalar moments with contractions of tensor moments; derivatives, Fisher metrics, or moment ODEs; ODE closure/conjugacy or admissible-image invariance; existence/uniqueness of trajectories; exponential tilting or analytic observation equivalence; general lower-bound sharpness. No semantic, epistemic, statistical, empirical, or noetic conclusion is added.

In particular, the broader tensor-continuation theorem is not described as wholly kernel-checked. This package closes precisely its finite-support separating-projection gap and joins it to the already checked algebraic recovery core.

## Exact inputs and reproduction

- Lean toolchain: `leanprover/lean4:v4.19.0` (compiler reports commit `6caaee842e94`).
- mathlib: official v4.19.0 commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
- All transitive package pins are retained in `lake-manifest.json` and `MANIFEST.json`. The dependency lock is copied byte-for-byte from the predecessor, including its inert root-name label `finite_moment_recovery`; the new Lake package is named `separating_projection` in `lakefile.toml`. Successful clean builds test this exact configuration.
- Source, configuration, control, and verification-script hashes are in `SOURCE_SHA256SUMS`.
- Toolchain hashes, dependency Git states, and dependency-olean hashes are recorded separately.

With the pinned toolchain on PATH and the pinned dependencies available:

```sh
./verify.sh
```

The workspace default toolchain location is `../.toolchains/lean-4.19.0-linux/bin`; set `LEAN_BIN` to another bin directory if needed. For a fresh machine, run `MATHLIB_NO_CACHE_ON_UPDATE=1 lake update` and optionally `lake exe cache get Mathlib.LinearAlgebra.Vandermonde Mathlib.LinearAlgebra.Matrix.NonsingularInverse Mathlib.Algebra.Polynomial.Roots` before verification. A full source build can instead obtain missing dependency modules through ordinary `lake build`. Respect the exact pins.

Here the predecessor's dependencies were copied into a separate `.lake/packages`, so new build products could not alter the predecessor package. Six additional mathlib polynomial dependencies were compiled from their pinned source: `Algebra.MonoidAlgebra.Division`, `Algebra.Polynomial.Inductions`, `RingTheory.Multiplicity`, `Algebra.Polynomial.Div`, `Algebra.Polynomial.RingDivision`, and `Algebra.Polynomial.Roots`. Other imported dependencies reuse the predecessor's retained official cache artifacts. The entire mathlib source tree and the Lean compiler were not rebuilt.

An optional cache download was interrupted after source builds supplied the needed additional modules; that log is retained and is not presented as a successful full cache acquisition.

`verify.sh` builds the project, then invokes Lean directly on every local successful source to force re-elaboration and kernel checking. It compares the 34 printed axiom audits with the complete named local declaration inventory, accepting only `propext`, `Classical.choice`, and `Quot.sound`; rejects prohibited proof-escape tokens; and requires both negative controls to fail.

The archive excludes dependency repositories, toolchain binaries, `.lake` build outputs, and downloaded caches. A replay needs those exact dependencies, obtained from official sources or an existing verified local copy. It is a source-and-evidence artifact, not a self-contained compiler distribution or external attestation.

## Preservation and evidence

`PRIOR_ARTIFACTS.json` records the pre-work hashes of all non-cache files in the earlier finite-moment package and the ordinary tensor-continuation package, including the earlier ZIP. `PRESERVATION_CHECK.json` reports the exact final comparison. No predecessor source, evidence log, archive, or protected repository is edited.

Final author evidence is in `logs/verify-final.log`, `logs/build.log`, `logs/fresh-*.log`, and `logs/control-*.log`. Early unsuccessful attempts are retained as diagnostic history and do not replace the final successful checks. `MANIFEST.json` and `SHA256SUMS` identify the sealed deliverable. Independent review, if provided separately, is a distinct evidence layer.
