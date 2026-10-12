# Independent review: Fisher/Hessian endpoint transport

10 October 2026 UTC. Final-byte scoped ordinary mathematical review.

## Verdict

**PASS within the stated scope.** The proposed Fisher/Hessian/Bregman transport is valid for the inherited lognormal endpoint pair. No mathematical correction remains necessary in the reviewed bytes. The result adds a verified geometric boundary discriminator, not a new equal-moment counterexample, general moment theorem, information-geometry theorem, intrinsic nonisometry result, or claim that metric completion collapses distinct probability laws.

Accepted author result:

- Path: `fisher-endpoint-geometry-20261010/RESULT.md`
- SHA-256: `1b051b438726e2a41bda222f08dfd6e3d9a70499454c9ccef0a62ee9ddac74f6`
- Size: 20,430 bytes

Accepted author control program:

- Path: `fisher-endpoint-geometry-20261010/verify.py`
- SHA-256: `968e36228f46cbc5d34a73278d5b5302f51798493d283a26bdc203e40ebd23eb`

All 17 payload entries of the author's manifest were checked against their exact size and SHA-256. The author's controls were replayed in a separate copied directory: 54 checks passed, exit 0. The independent program `independent_check.py` passed 31 additional source-integrity and finite symbolic checks. The original author packet was not rerun in place, avoiding mutation of its timestamp-bearing control report. The final receipt rechecks the original packet after replay.

The universal analytic claims are accepted by the written proof review below. Finite controls supplement that review; they do not replace its arguments with enumeration or supply a formal-kernel certificate.

## 1. Source-faithful transport and credit

The review read the actual inherited moment and endpoint results, the finite exponential-leaf formulas, the all-points Bregman/Hessian comparison, and the real local-Hessian repair source. This is not an analogy-only approval based on terminology.

- `measure-moment-continuation-boundary-20261009/RESULT.md`, §§2 and 4–6, already owns the scalar Fisher pairing, distinct equal-moment lognormal laws, common one-sided hierarchy jets, different future mean germs, and zero-radius Laplace Taylor series. Its SHA-256 is `a0fa9117ff47df9f07133c1ed49c682c7c2e73d20881e83f3c242dfb3faeb9e3`.
- `exponential-tail-effectivity-20261010/RESULT.md`, §6, already owns the computable reverse-damping endpoint realization and the continuation-congruence obstruction there. Its SHA-256 is `3d84bca98867d77a3c2478883e07a42e456b48404edb1ba4b90fa5e788a1788a`.
- `leafwise-noetic-geometry-20261010/RESULT.md`, §§6–8, already gives z=∇A, covariance Hessian, inverse-covariance mean metric, and the essential reference-class invariant in a finite family. Its SHA-256 is `6d5c3c38f6e89c8f74f3b5d58cabcace7b9cae0eb2d6f8bf3a2f6ef4f4aef724`. The new proof correctly establishes half-line endpoint hypotheses directly instead of importing finite-support global surjectivity or an open natural domain.
- `information-geometry-transport-20261009/RESULT.md`, §2, already distinguishes the all-points Hessian condition from a one-point match. Its SHA-256 is `077fabaf882988d2de23bda85fd40cc03f6f630c0ca859f12864d53c604fbd94`.
- `noetic-gradient-transport-20261009/INHERITED_HESSIAN_SOURCE.md`, Setup and S1–S2, fixes the Bregman orientation and local repair scope. Actual bytes match SHA-256 `3d1c584a1b91f4d0190605cd73d1cba8ae3bf631e461865de301b4711928d9be` and independently recomputed Git blob `0b7f307cabd85b4d73215f024d70112a5dcd07c4`. Its declared repository pin is `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`, at `docs/provenance/v5-research-continuations/notes/3d1c584a1b91f4d0190605cd73d1cba8ae3bf631e461865de301b4711928d9be.md`. Its retained original verification banner is not upgraded by this review.

All eight author-bound snapshots were independently checked against their current original bytes, including the participating root note. Their individual hashes and sizes are recorded in `INDEPENDENT_CONTROLS.json`. The primary Wainwright–Jordan citation is the author's documented focused source inspection, not a claim of a second external-PDF retrieval by this reviewer; the necessary identities were independently derived here and are already present in the read inherited leaf geometry. No wider novelty survey is asserted.

The parent supplied the transport proposal, finite-length estimate, variance check, and participating derivation. The author developed the deliverable and tests. This reviewer supplied the independent derivation, mathematical read, source checks, and replay. The participating root note is not credited as an independent review.

## 2. Integrability, positivity, and finite length

For each source ν, the derivatives of L(t)=∫e^(−tx)dν are justified on [0,b] by the appropriate finite polynomial moments, with the next moment controlling endpoint difference quotients. On that interval L(t)≥L(b)>0. Thus logarithmic and normalized derivatives remain finite at every order.

The score is −(X−q), and its squared Fisher norm is V=Var(X). Strict positivity follows from the everywhere positive, nondegenerate density, not merely from nonnegative variance. At the endpoint V(0)=e²−e>0. The inequality V(t)≤E_tX²≤e²/L(b) gives the claimed length bound b√(e²/L(b)). Continuity additionally gives a positive lower bound on each fixed compact interval.

The square-root density realization in common L²(ρ) is valid. Derivatives of every order are dominated in squared norm by a finite polynomial moment. Its nonzero derivative provides a one-sided smooth immersion. This does not assert that the entire positive-density cone is an open Hilbert manifold. The path toward the endpoint is a finite-length reverse of the negative-gradient direction, a sign distinction stated correctly by the author.

## 3. Mean-coordinate sign and KL orientation

The natural parameter is η=−t. Consequently q=−F′ and q′=−V, and the correctly signed dual is ψ(q)=−t(q)q−F(t(q)). It satisfies ψ′=−t and ψ″=1/V>0. The one-sided inverse is valid because q′ has a nonzero continuous endpoint limit; repeated inverse differentiation gives all endpoint derivatives without assuming an open statistical domain.

For the same source label σ,

    KL(p_σ,s || p_σ,t)
      =(t−s)q_σ(s)−F_σ(s)+F_σ(t)
      =B_ψσ(q_σ(s),q_σ(t))=B_Fσ(t,s).

The author correctly reverses the natural-parameter Bregman arguments while keeping the mean-coordinate order. These formulas stay finite at endpoints since the first moments exist. They are not used for cross-source KL. The boundary-anchored divergence B_ψσ(q,q₀)=ψ_σ(q) correctly exhibits the differing potential germs.

The original log partition is F_σ(a+u)−log D_σ. Its endpoint constants can differ. Centering F_σ(0)=0 is explicit, and no conclusion is drawn that the uncentered original normalizers have identical complete jets. Additive constants cancel from the metric and Bregman divergence as claimed.

## 4. Equal jets, unequal germs

Equality of all moments yields equality of all centered partition, mean, variance and inverse-coordinate jets by finite algebraic recursions at each derivative order. The nonzero denominator V(0) makes inverse and dual jets legitimate. Each entry is uniformly computable from the inherited computable moment sequence; this does not supply a procedure recovering an arbitrary germ from those entries.

Variance-germ equality would, after two integrations using common F(0) and F′(0), give equality of the Laplace transforms on a positive interval. The inherited analytic continuation and Laplace uniqueness argument excludes this. Mean-Hessian-germ equality similarly integrates using ψ(q₀)=ψ′(q₀)=0, identifies the inverse parameters through t=−ψ′, and then identifies the centered partitions. Therefore the metric and potential germs genuinely differ in the declared coordinates. The Bregman claim follows immediately from its boundary slice, and all of its corner jets follow from the common ψ jets.

The fixed operational mean chart is important. A one-dimensional positive smooth metric can be flattened by arc length. The author explicitly excludes intrinsic nonisometry, and the proof does not claim it.

The finite polynomial covariance guard is also correct: a nonzero linear combination of X,…,X^d cannot be almost surely constant under an everywhere positive density unless that polynomial is constant identically, which its nonzero nonconstant coefficients exclude. The author does not infer invertibility of an infinite covariance operator in an undeclared topology.

## 5. Nonanalyticity and the actual collapse

The inherited zero Taylor radius excludes a real-analytic extension of L at zero. Integration and exponentiation transfer the obstruction to F, q and V. An analytic extension of ψ with its positive endpoint Hessian would admit analytic inversion of η=ψ′, reconstructing an analytic F. The same holds if only ψ″ were analytic, by integration. These are statements about the named affine coordinates and statistical potentials, not about every coordinate representation of an abstract one-dimensional metric.

The actual endpoint probability laws remain distinct in their common square-root representation, with positive L² separation; their mutual KL divergences are finite and positive as well. Each law's finite-distance completion therefore supplies no reason to identify them. The failure is the representation that forgets source/leaf information and retains only the common moments and derivative record. Retaining the original law and normalization history, or another adequate law/continuation representation, lies outside that defective quotient and is correctly preserved as a possible repair.

## Scope ceiling

Acceptance is for the stated ordinary mathematical transport and its exact symbolic/source controls. It gives no empirical, psychological, normative, metaphysical, sampling-optimization, protected-source, canonical-integration, formal-kernel, or programme-closure warrant. The earlier equal-moment and endpoint theorems remain inherited inputs. No required change remains in the pinned author result.
