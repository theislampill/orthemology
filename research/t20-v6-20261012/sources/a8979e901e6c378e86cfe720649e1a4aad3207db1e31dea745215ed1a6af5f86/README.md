# Kernel-checked finite moment recovery

**Result:** the finite algebraic recovery core of the tensor-continuation result has been freshly formalised and checked in Lean 4.19.0 against pinned official mathlib v4.19.0. An exact four-point positive-probability counterexample is checked over the real numbers as well.

This is verification of an already established ordinary mathematical result, not a new discovery, an external-validation claim, or closure of T20/T21. All earlier material is preserved. This directory is a separate additive proof package.

## The substantive general theorem

For every natural number N, every field K, a known injective support a : Fin N → K, and arbitrary weights w : Fin N → K, define

- s(r) = ∑ j, w(j) a(j)^r;
- record(a,w) = (s(0), …, s(N−1));
- V(j,r) = a(j)^r;
- C(j,r) = (V⁻¹)(r,j).

`FiniteMoment.determinant_ne_zero` proves det(V) ≠ 0 from mathlib's proved Vandermonde determinant product and the injectivity of a. Nonsingularity, interpolation and moment-injectivity are **not assumptions**.

`FiniteMoment.recover_record` then proves the actual reconstruction

    w(j) = ∑ r : Fin N, s(r) C(j,r).

Its coordinate form is `FiniteMoment.weight_eq_sum_moments`. The reversed identity is proved by `record_recover`, and `recordLinearEquiv` bundles the two identities as an explicit K-linear equivalence of the full weight and moment spaces.

Consequences proved in the same source:

- `weights_eq_of_moments_eq`: equal degrees 0 through N−1 determine all weights.
- `record_injective`: the finite record is injective.
- `all_moments_eq_of_record_eq`: equality of finite records entails equality of every natural-degree moment.
- `higher_moment_reconstruction`: each higher moment is an explicit fixed linear combination of the retained moments.
- `vector_observable_reconstruction`: for any K-module E with additive commutative group structure, and any fixed f : Fin N → E,

      ∑ j, w(j) • f(j) = ∑ r, s(r) • (∑ j, C(j,r) • f(j)).

This last formula covers arbitrary chosen tensor-valued support observables at the algebraic level. It proves the fixed finite linear representation itself; it does not merely assume an inverse or a factorisation.

There is no positivity, normalization, ordering, characteristic-zero, or nonempty-support requirement on the general theorem. Explicit positive controls instantiate N=0 and N=1. The inverse matrix and classical field operations are noncomputable Lean definitions; the package does not assert a general executable algorithm for unspecified real inputs.

## Exact real four-point control

`FiniteMomentRecovery.FourPoint.positive_probability_counterexample` proves a conjunction about the actual real functions

- x = (0, 1/3, 2/3, 1);
- wPlus = (5, 9, 3, 7)/24;
- wMinus = (7, 3, 9, 5)/24.

It checks pairwise distinct support, all weights strictly positive, each total equal to one, equality of every scalar moment of degree at most two, cubic difference 1/54, and inequality of their atomic mass functions. A separate theorem verifies all support values lie in [0,1]. The exact common moments are (1, 1/2, 7/18); the cubic moments are 37/108 and 35/108.

Moments use genuine sums over Fin 4, defined uniformly for every natural degree. The mass functions are finite atomic mass functions on ℝ, not a claim about a formalised measure-theoretic integral. `Checks.lean` verifies that the concrete moment function is definitionally the same as the generic one at this support.

## What received kernel credit

- The proved determinant-based algebraic reconstruction for arbitrary finite N over an arbitrary field.
- Its explicit linear equivalence and scalar/vector higher-observable representation.
- The exact real positive-probability counterexample and its listed algebraic properties.
- N=0 and N=1 instantiations and the generic/concrete moment-definition bridge.

**Not formalised here:** existence of a separating projection for arbitrary distinct vectors; tensor-space and contraction constructions; derivatives, Fisher metrics or the moment ODE hierarchy; exact ODE closure/conjugacy or preservation of the admissible image; existence/uniqueness of trajectories; exponential tilting and analytic continuation/observation equivalence; the second-derivative interpretation of the cubic difference; general lower-bound sharpness; empirical, statistical, computational-complexity, semantic, or epistemic claims.

Thus the broader tensor-continuation theorem is **not** represented as wholly kernel-checked. Its central finite-support algebraic recovery step and concrete algebraic control are.

## Reproduce

The selected toolchain is `leanprover/lean4:v4.19.0`. In this workspace it is installed at `../.toolchains/lean-4.19.0-linux/bin`. The exact Lean commit, executable/archive hashes, all dependency Git pins and source/log hashes are in `MANIFEST.json` and `SHA256SUMS`.

With that toolchain available on PATH:

```sh
export PATH="$PWD/../.toolchains/lean-4.19.0-linux/bin:$PATH"
export XDG_CACHE_HOME="$PWD/.cache"
MATHLIB_NO_CACHE_ON_UPDATE=1 lake update
lake exe cache get Mathlib.LinearAlgebra.Vandermonde \
  Mathlib.LinearAlgebra.Matrix.NonsingularInverse \
  Mathlib.Data.Real.Basic Mathlib.Data.Fin.VecNotation \
  Mathlib.Algebra.BigOperators.Fin Mathlib.Tactic.NormNum Mathlib.Tactic.FinCases
./verify.sh
```

For another toolchain location, set `LEAN_BIN` to its bin directory before running `verify.sh`. Keep the version pinned. The manifest pins all packages rather than relying on mutable default branches.

The script first builds the four local modules, then explicitly re-elaborates every local source via `lake env lean -o …`, forcing fresh checking rather than relying on preexisting local `.olean` files. It checks all expected axiom-audit rows and requires rejection of two deliberately invalid sources under `controls/`:

1. A false replacement of the cubic difference by 1/53.
2. An attempt to apply recovery without its distinct-support premise.

Those files are expected-failure tests and are intentionally excluded from the successful library targets.

The official dependency sources and 1,513 required precompiled cache modules were acquired successfully. Dependency proofs were loaded from the official cache; **the entire mathlib source tree was not rebuilt locally**. Fresh local source checking is against those pinned imported foundations. The cache/toolchain/dependency integrity hashes identify the actual local inputs; they are not independent external attestation.

The portable ZIP contains sources, lockfiles, replay instructions, hashes and evidence only. It deliberately excludes the installed Lean toolchain, cloned dependency repositories and cached build files. A machine without those inputs needs network access to the official upstream Git repositories and mathlib cache service during setup. A replay can instead reuse already retained exact pinned dependencies; that is the route used by the fresh-extract replay. All successful local proof checks are still forced from source.

## Foundation audit and evidence

`Verify.lean` prints axioms for all 43 local named definitions and theorems. Every printed set contains only `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx`, new axiom declaration, `sorry`, `admit`, `native_decide`, unsafe proof escape, or proof-cost calculus is used.

Primary evidence:

- `logs/verify-final.log`: final full verification transcript.
- `logs/build.log`: successful Lake build.
- `logs/fresh-*.log`: forced fresh local source checks; `fresh-Verify.log` is the complete axiom report.
- `logs/control-*.log`: both expected type-checking failures.
- `logs/lake-update.log`, `logs/cache-get.log`: dependency acquisition, including the initial default-cache read-only-path failure and successful writable-cache recovery.
- `logs/attempt-01-general.log`, `logs/attempt-02-general.log`: initial vector-lemma name ambiguity and successful exact fix.
- `ACTIVE_WORK.md`: prospective chronology and credit boundary.
- `MANIFEST.json`, `SHA256SUMS`: exact provenance and integrity record.

The general source has 12 named theorem declarations and five definitions; the counterexample source has 21 named theorems and five definitions. Four additional anonymous positive examples live in `Checks.lean`.

## Separate internal review

The frozen evidence in `review/` reports an independent clean-copy project build, fresh source checks, source-inventory/axiom matching, and additional edge/concrete-support tests. Its verdict is PASS for the bounded algebraic scope. It reused the same pinned toolchain/dependency provenance and is not external peer review or a full mathlib/compiler rebuild. See `review/REVIEW.md` and its independent `SHA256SUMS`.
