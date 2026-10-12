# Exact Lean certificate for the truncated rational moment obstruction

10 October 2026 UTC. Additive bounded formalization of the independently accepted rational diagnostic. This result is about actual ternary multivariate polynomials over the reals. It is not a full-polynomial-algebra positivity theorem, a heat theorem, a representation algorithm, or T20 closure.

## Machine-checked mathematical result

`TruncatedMoment.Poly` is `MvPolynomial (Fin 3) ℝ`. `Lambda` is an actual real linear combination of Mathlib's coefficient linear maps. On total degree at most four its moments are exactly

- Λ(1)=1;
- Λ(xᵢ²)=4;
- Λ(xᵢ⁴)=50;
- Λ(xᵢ²xⱼ²)=1 for i≠j;
- Λ(xyz)=3/2;
- all other nonconstant monomial values are zero.

All 35 moments are separately checked in `MomentValues.lean`. The formula defines a convenient zero-valued continuation on higher monomial coefficients, but no positivity for that continuation is claimed.

`quadratic_parameterization` proves that every actual polynomial p with p.totalDegree≤2 equals the displayed ten-coefficient expression in the basis

    (1,x²,y²,z²,x,yz,y,xz,z,xy).

`Lambda_quadratic_square` proves directly from coefficient extraction and actual polynomial multiplication that Λ(p²) is the indicated moment form. It is not an assumed Gram matrix or a Boolean label. The even and odd square identities, nonnegativity, and zero characterizations are proved over arbitrary real coefficients. Therefore

    every_quadratic_square_positive:
      ∀ p : Poly, p.totalDegree ≤ 2 → p ≠ 0 → 0 < Lambda (p^2).

`quadratic_square_degree` additionally checks that these squared polynomials lie in degree at most four. `finite_sos_positive` checks strict positivity of any finite sum of such quadratic squares when at least one square's polynomial is nonzero. It does not claim a separate formal theorem extracting quadratic summands from an arbitrary unrestricted SOS representation of a degree-four polynomial.

The actual polynomial `witness` is

    F=1−4xyz+x²y²+x²z²+y²z².

`eval_witness` identifies its Mathlib evaluation with the displayed scalar expression. `witness_nonnegative` proves ∀v:Fin 3→ℝ, 0≤MvPolynomial.eval v F, using the two exact square identities split by the sign of xy. `witness_degree` proves totalDegree(F)≤4, while `Lambda_witness` proves Λ(F)=−2.

`truncated_moment_obstruction` bundles the actual-polynomial strict-square-positivity theorem, witness degree, universal pointwise nonnegativity, exact negative functional value, and violation of positivity on nonnegative quartics. `no_positive_functional_agrees` further proves that no real linear functional positive on all pointwise-nonnegative degree-at-most-four polynomials agrees with these degree-four moments.

## Measure boundary

The Lean result is the explicit positivity obstruction above. It does not import MeasureTheory or prove a Bochner-integral representation theorem. In ordinary mathematics, a positive representing measure with the stated moments would integrate F to Λ(F)=−2, contradicting F≥0; integrability of its monomials is part of the usual truncated moment representation, and F is a finite linear combination of them. Thus nonrepresentation is a mathematical corollary, rather than a separately machine-checked MeasureTheory theorem in this packet.

A direct Bochner-measure bridge was considered. The retained environment lacks `Mathlib.MeasureTheory.Integral.Bochner.Basic.olean`; the source dependency audit found 648 additional missing Mathlib modules. No such baseline rebuild was attempted. The unbuilt exploratory source is isolated under `attempts/`, excluded from the compiled module list, and carries no verification claim. This does not affect the actual polynomial, degree, universal positivity, or coefficient-functional proofs.

## Essential negative boundary

The higher-degree zero continuation explicitly fails square positivity:

    Λ((x³−x)²)=−96.

This equality and `not_full_square_positive` are kernel-checked. The degree restriction is therefore mathematically essential even for the exact function defined in Lean. No extension of the 35 moments to a square-positive functional on the entire polynomial algebra is assumed or established.

## Replay and trust

Run

    python3 lean-truncated-moment-obstruction-20261010/replay.py

from the containing workspace. It uses the existing Lean 4.19.0 executable and retained package objects listed in `lean_path.txt`, writes fresh local module objects into `replay-lib`, and passes `--trust=0` on every checked module. It never rebuilds or modifies dependency packages or earlier work.

The checked modules are `TruncatedMoment`, `ScalarPositivity`, `DegreeBridge`, `Certificate`, `Controls`, `MomentValues`, and `Verify`. Sixteen explicitly printed theorem axiom closures must contain only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`. No new axiom, sorry, admitted proof, native_decide, or implementation substitution is used.

Five compiler-negative controls must be rejected: wrong witness value, wrong triple moment, nonnegative-witness positivity, unrestricted square positivity, and negative-mass positivity. These controls reduce false assertions using the checked exact-value theorems and must fail for logical/arithmetic reasons rather than unavailable imports.

`REPLAY_RECEIPT.json` records fresh replay, source/object digests, input digests, and controls. `DIRECT_IMPORTS.json` records actual direct dependencies reported by `lean --deps`; `IMPORTED_OBJECT_MANIFEST.json` records the resolved imported source graph and actual retained object SHA-256 digests. These are a dependency-bound replay record, not a claim to rebuild Mathlib from source. No protected source, original diagnostic, earlier review, or package object is edited.

The exact heat identity, the rational T=1,a=10 witness value −3797/2500, and backward-heat countercertificates remain outside this Lean packet. Their prior written/exact-symbolic results are unchanged.
