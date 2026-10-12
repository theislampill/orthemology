# Exact continuation equivalence and two reading clarifications

9 October 2026 UTC. Added after the author RESULT.md was frozen, without changing its bytes. This is an explicit corollary of its proofs, not an additional independent mathematical novelty claim.

## Complete continuation equivalence for the declared half-line interface

On the state class P∞ of RESULT.md, let qμ(t) be the mean under the constant control g=1. For any two initial laws μ,ν and any fixed nonempty open interval I⊂(0,∞), the following are equivalent:

1. μ=ν.
2. The means agree at every time under every common admitted nonnegative piecewise-constant control.
3. qμ(t)=qν(t) for all t>0 under the single constant control g=1.
4. qμ(t)=qν(t) for every t∈I under that control.

The first implication follows from the explicit semigroup; the next two are immediate. For (4)⇒(1), q=−L′/L and positivity give Lμ=cLν on I for some c>0. Both Laplace transforms are holomorphic on the right half-plane, so the identity theorem extends this equality to t>0. As t↓0, both converge to 1, which fixes c=1. Classical Laplace uniqueness then gives μ=ν.

Thus full-law equality is precisely continuation equivalence for this particular control/output interface. The Laplace-profile record is complete for it. The all-polynomial-moment record is strictly coarser, as the countermodel proves.

This is a statement about equality of exact continuous real response functions on a nonzero interval. It is not statistical, empirical, noisy, finite-sample, or effective identification, and it supplies no reconstruction-cost or stability guarantee. Restricting controls or required outputs further can change the equivalence relation.

## Clarifications from independent reading

- In RESULT.md §5, the sentence saying the functions are analytic at positive times but not at the boundary zero refers to the Laplace transforms L±. It does not assert nonanalyticity of the constant zeroth moment M₀=1.
- In §7, the intended point concerning the shared point-concentration defect d=1 is that this value does not decide moment determinacy. Both lognormal countermodel laws and, for example, an atomless uniform compactly supported law have d=1, while the latter is moment-determinate. The inherited defect theory remains intact.
