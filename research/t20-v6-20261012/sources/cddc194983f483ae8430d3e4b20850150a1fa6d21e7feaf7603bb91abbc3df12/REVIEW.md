# Independent review of reference transported Bregman classification

## Finding

The claimed equivalence is mathematically sound under the stated assumptions: a common scalar generator on the positive half-line, C³ regularity, strictly positive second derivative, arbitrary finite positive input probability laws, a positive transported reference, and nonnegative column-stochastic channels with zero output rows omitted. The normalized-probability necessity proof is valid. The interior-power equality classification and the distinction between pair recovery and simultaneous reference recovery are correct.

This review supplies independent mathematical reasoning and 22 exact symbolic/rational controls. It does not claim formal proof-assistant certification, literature novelty, or programme closure. The scalar characterization and Jensen ancestry remain credited to Bauschke–Borwein and Chafaï. Primary-source acquisition/visual validation is the author's responsibility; this review additionally inspected the locally extracted scalar-characterization statement.

## Normalized necessity

Given two arbitrary positive density pairs and a convex weight, their mean densities X and Y are finite and positive. Put a total reference mass ε on the two tested coordinates, split in the desired proportions, and choose ε smaller than min(1,1/X,1/Y). The remaining reference mass may be 1−ε, so even the reference can be normalized. Complete p and q using masses 1−εX and 1−εY. These are strictly positive probability laws. A deterministic merge leaves the buffer coordinate unchanged, and its divergence term cancels exactly. Dividing the assumed contraction inequality by ε produces the arbitrary scalar Jensen inequality. No limiting argument, approximation, unconstrained p or q, or fourth derivative is needed.

The independent cubic witness uses φ(t)=t³/6, μ=(1/10,1/10,4/5), p=(9/40,7/40,3/5), q=(3/20,1/20,4/5). Merging the first two coordinates increases divergence by exactly 1/80. All three vectors are positive probability laws. This tests the normalization issue with a different generator and fixture from the author's quartic example.

## Hessian equivalence

Write a=φ″ and r=1/a. The Hessian entries are a(x), −a(y), and a(y)−(x−y)a′(y). Its determinant is

    [r(y)+(x−y)r′(y)−r(x)] / [r(x)r(y)²].

The denominator is positive, and the first leading minor is positive. Positive semidefiniteness is therefore equivalent to the tangent-majorant criterion for differentiable concavity of r. C³ for φ gives exactly the needed C² Bregman function and C¹ reciprocal curvature. Replacing this proof with r″≤0 would unnecessarily require extra regularity and was not done.

## Equality and pair recovery

Strict concavity of r makes every off-diagonal Hessian positive definite. Along a nonconstant segment that is not contained in x=y, an open subsegment lies off the diagonal and has positive directional second derivative. Such a restriction cannot be affine. Consequently the only nonconstant Jensen equality sets lie in the diagonal. In a finite supported row, equality holds precisely when all density pairs coincide, or all supported p_i=q_i. The latter permits unequal common densities and is essential.

Both alternatives imply constant p_i/q_i on each channel row. Set R_ij=K_ji q_i/(Kq)_j. This is nonnegative with unit column sums. R(Kq)=q directly. For a supported edge, (Kp)_j/(Kq)_j=p_i/q_i; summing over j therefore gives R(Kp)=p. This proves pair recoverability for the strictly concave reciprocal class, as well as entropy under its likelihood-ratio equality condition. It does not recover the reference in general.

The test suite includes a mixed fiber containing diagonal and off-diagonal pairs and verifies strict contraction for φ=t^(3/2), guarding against an equality classification that accidentally permits mixed cases.

## Independent simultaneous reference recovery obstruction

Take

    μ=(1/6,1/3,1/4,1/4),
    p=(1/12,5/12,1/3,1/6),
    q=(1/12,5/12,1/6,1/3),

and merge the first two coordinates. Divergence equality holds for every strictly convex generator: the merged block has p=q and the other coordinates are unchanged. Divergence is positive because p≠q. For φ=t^(3/2), equality and positivity are also checked symbolically.

After transport Kμ=(Kp+Kq)/2, whereas μ≠(p+q)/2. Any linear map recovering all three vectors would preserve that affine relation, a contradiction. Thus even a linear simultaneous reverse is impossible. The q-Bayes stochastic reverse does recover p and q, and explicitly fails to recover μ. This is a different, especially transparent obstruction from the author's invertible coarse matrix with a negative unique inverse entry.

## Independent endpoint separation

For the quadratic generator φ(t)=t²/2, take μ=(1/3,1/3,1/3), p=(1/4,5/12,1/3), q=(1/6,1/3,1/2), and merge the first two coordinates. The density differences are (1/4,1/4,−1/2), so both divergences equal 1/16.

Nevertheless the signed vector p−(4/3)q has ℓ1 norm 7/18, and its transported vector has norm 1/3. If a common stochastic pair reverse existed, its ℓ1 contractivity would force 7/18≤1/3. Therefore no such reverse exists. This demonstrates a genuine contrast with the strict-reciprocal class without relying on logarithms, numerical optimization, or an assumed form of the reverse channel. The same fixture has strict contraction for the interior power generator.

## Scope and final checks

The interior family 1<α<2 has positive strictly concave reciprocal curvature, as claimed. The normalized power family, rather than unnormalized t^α, has the stated entropy limit. The report properly keeps transported-reference geometry distinct from canonical geometry, epistemic warrant, arbitrary field projectability, and unadorned simplex metric uniqueness.

One minor wording issue was raised before freeze: the proof using contraction forward and backward should explicitly refer to generators in the contractive class. Bare C³/φ″>0 assumptions do not themselves give contraction. The author narrowed that sentence before freeze, and the correction was verified. The conclusion for arbitrary strictly convex generators can alternatively be proved through simultaneous sufficiency, but that broader proof is unnecessary here.

Exact test results are in CONTROLS.json and CONTROLS_OPTIMIZED.json. Both runs execute real failure checks unaffected by Python optimization. Finite controls corroborate the written all-input proofs; they do not replace them.

## Frozen review verdict

PASS with no outstanding mathematical defect found. Reviewed RESULT.md SHA256: 8f06b1ff3f0239b1f9e3d868aae3b880aab7a55f3974106d249938bfb4cc1e01. The author’s 26 exact checks replayed successfully in normal and optimized modes, alongside this review’s independent 22-check suite in both modes.
