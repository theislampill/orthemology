# Root derivation and scope for reference geometry classification

11 October 2026 UTC. Ordinary written analysis proposed to the author and independent reviewer. Classical scalar Bregman convexity is to be attributed to its primary source; no field novelty claim.

For scalar b(x,y)=φ(x)−φ(y)−φ′(y)(x−y), its Hessian is

    [[φ″(x), −φ″(y)], [−φ″(y), φ″(y)−(x−y)φ‴(y)]].

With φ″>0, nonnegative determinant is equivalent to

    r(x) ≤ r(y)+(x−y)r′(y),  r=1/φ″.

Thus universal joint convexity is equivalent to concavity of r. The derivative condition is global on (0,∞); a pointwise Hessian check at one pair does not suffice.

For transported positive reference ν=Kμ, each row forms a convex combination of paired ratios (p_i/μ_i,q_i/μ_i), with weights K_ji μ_i/ν_j. Joint convexity yields contraction after multiplying by ν_j and summing. Conversely any two positive paired ratios with weights λ,1−λ can be put into the first two coordinates of normalized p,q using μ_1=ελ and μ_2=ε(1−λ), and sufficiently small ε. A third positive buffer coordinate completes each probability vector. Merge the first two coordinates and retain the buffer unchanged. The buffer Bregman term cancels, recovering precisely the desired scalar Jensen inequality. The reference buffer can also be chosen to normalize μ if that is additionally required. This proof does not silently enlarge the p,q domain from normalized laws to arbitrary measures.

## Strict-interior power family and equality

For φ(t)=t^α, 1<α<2, r(t)=[α(α−1)]^-1 t^(2−α) is strictly concave. The Hessian of b is positive definite away from x=y. A nonconstant straight segment not entirely on the diagonal contains an off-diagonal interval of strictly positive directional curvature. Jensen equality for a finite positive-weight row therefore requires either identical supported pairs, or all those pairs on the diagonal. The latter permits varying common ratios p_i/μ_i=q_i/μ_i.

The endpoint mechanisms differ. Quadratic b depends only on the ratio difference, so equal differences suffice. Entropy b is homogeneous on rays, so equal likelihood ratios p_i/q_i suffice. These are different equality contracts even though all three geometries contract under the stated reference-carrying maps.

## Exact intermediate fixture

Take α=3/2, μ=(1/16,1/16,1), p=(1/4,1/16,11/16), q=(1/16,1/16,7/8), and merge the first two coordinates. The buffer is unchanged. Fine minus coarse divergence is (18−5√10)/32>0. The exact Hessian determinant at x=u²,y=v² is 9(u−v)²/(32uv³).

## Equality does not require recovery of every supplied object

Take p=(1/8,1/8,1/4,1/2), q=(1/8,1/8,1/2,1/4), μ=(1/8,3/8,1/4,1/4). Let K merge the first two coordinates and leave the others. Divergence is unchanged for any strictly convex φ: on the merged coordinates p_i=q_i so their contribution vanishes, while the two other coordinates are unchanged. The overall divergence is positive because p≠q.

But no stochastic reverse simultaneously recovers p,q,μ. Write F=[p q μ]. The matrix KF has determinant −1/16, so any such linear reverse must be F(KF)^-1, which is

    [[1/8,1/8,1/8], [7/8,−1/8,−1/8], [0,1,0], [0,0,1]].

Its negative entries rule out a stochastic reverse. This refines the inherited sufficient triple-recovery criterion without disputing it. It does not imply failure of every other declared observable-recovery contract.

## Boundaries

The entire classification is for this separable reference-weighted family and all maps/laws in its declared domain. It neither classifies all nonseparable geometries nor warrants the reference's cognitive interpretation. Carrying μ is additional structure, so the result cannot refute metric uniqueness statements on probability simplices without that structure. Divergence contraction alone does not establish gradient-field projectability, actual epistemic improvement, or source truth.
