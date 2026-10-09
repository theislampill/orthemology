# Independent derivations for grouped count/calibration invariants

This is an independent mathematical review supplement, confined to the newly assigned review directory. The author checkpoint is reviewed and digest-bound separately in REVIEW.md and REVIEW_RECEIPT.json. Finite controls supplement the derivations; they are not proofs of the universal statements.

## 1. The equivalence class at an interior survival value

Let the distinct count support be nonnegative integers, with strictly positive weights, and let one count remain fixed within each conditionally independent group. For actual survival t in (0,1), a count j has Bernoulli no-effect propensity t^j. This is strictly decreasing in j, including the zero-count atom at 1. Consequently the scalar propensity law has exactly as many distinct atoms as the count law.

Equality of every grouped law gives equality of all moments of the scalar law. For finite competitors, enough finite moments then identify the scalar law. If both competitors have at most k atoms, equality through order 2k-1 is sufficient: their signed difference has at most 2k distinct nodes, and interpolation polynomials of degree at most 2k-1 isolate each coefficient. A length-R binary grouped law is equivalent to all moments through R by marginalization and polynomial expansion, not to the single moment of order R alone.

After ordering the positive counts increasingly, scalar-law equality gives

    t^j_i = s^l_i,   w_i = w'_i,   w_0 = w'_0.

Taking logarithms is legitimate because both survivals and every positive-count node lie strictly between zero and one. Thus

    l_i / j_i = log(t) / log(s),

independent of i. Its value is positive rational because either side is a ratio of positive integers. If d=gcd(j_1,...,j_m), write j_i=d v_i with gcd(v)=1. Set alpha=(l_i/j_i)d; then l_i=alpha v_i. A Bezout integer combination of the v_i equals 1, so the same combination of the integers l_i equals alpha. Therefore alpha is a positive integer e. This proves the unique primitive positive integer vector v and the integer scales d,e.

The direct rescaling e/d need not be an integer. For example, supports (2,6) and (3,9) share v=(1,3), but their direct factor is 3/2. Calling every direct rescaling an integer dilation would be false. Calling both supports integer dilations of a common primitive support is correct.

Conversely, for any b in (0,1), the survivals t=b^(1/d) and s=b^(1/e) give identical matched propensities b^v_i. With identical weights and zero mass, every grouped law agrees. The invariant does not determine which integer scale is physically or otherwise correctly assigned. An assumption that d=1 excludes all other scales only if warranted independently.

## 2. Static command maps and adaptive grouped observations

Let survival t(x)=1-r(x) be nonincreasing, with t(0)=1 and t(1)=0. For supports d v and e v, define

    s(x)=t(x)^(d/e).

The transformed survival is again nonincreasing and endpoint-preserving. It preserves continuity and strict monotonicity when present. Componentwise, t(x)^(d v_i)=s(x)^(e v_i) for every command. This componentwise equality is stronger than equality of averaged one-trial means.

A held-latent adaptive protocol can be coupled by matching the initial component index, the policy randomness, and every new endpoint uniform random draw. At any common history the next command matches; the matched component has the same conditional endpoint parameter in either world. The histories, group transitions governed by matching kernels, stopping decisions and reports consequently match. This uses the declared complete conditional observation law; equality of unconditional marginal means would not suffice.

If a monotone map is allowed to be discontinuous, endpoint preservation does not guarantee that any command has survival strictly between zero and one. A threshold step map has only endpoint survival values. For such a map, arbitrary positive support shapes with equal zero-count mass share all grouped command laws. Therefore extracting the primitive signature needs an actually observed interior-survival setting, a condition guaranteeing one (such as continuous endpoint-preserving calibration), or an independently supplied signature. The known-signature corollary does not need to infer that signature anew.

## 3. Count bounds and restricted calibration feasibility

With a known maximum M and a recovered positive primitive vector v, let D=floor(M/max(v)). Under unrestricted monotone endpoint-preserving calibration, every scale d in {1,...,D} is available. If D=0 the supplied bound contradicts the recovered signature; if D=1 the count scale is unique. A maximum bound alone generally does not force D=1.

At one interior nominal command x_0 with identified primitive scalar base b, a candidate d forces the actual rate y_d=1-b^(1/d). Under a uniform absolute calibration tolerance eta, necessity is

    |y_d-x_0| <= eta.

It is also sufficient for that one-command evidence. Interpolate linearly from (0,0) to (x_0,y_d) to (1,1). This map is increasing, endpoint-preserving, and its discrepancy from the identity is linear on either side, zero at both endpoints, and maximal in absolute value at x_0. Thus the global uniform bound is exactly the displayed pointwise discrepancy.

Once the full primitive curve b(x) is given, there is no interpolation freedom: the candidate calibration is uniquely r_d(x)=1-b(x)^(1/d). Provided b is a nonincreasing endpoint-preserving survival-type curve, this map automatically has the structural properties. The remaining condition is

    sup_x |1-b(x)^(1/d)-x| <= eta.

The feasible subset can be smaller than {1,...,D}. Our exact control uses x_0=1/2, b=(3/4)^12, D=4 and eta=1/4. Exactly scales 3 and 4 survive.

## 4. The known-signature population reduction and sharp radii

Fix v, its strictly positive associated weights, and zero mass w_0. Assume positive total mass on positive counts. Set

    F(z)=w_0+sum_i w_i z^v_i.

This continuous map is strictly increasing on [0,1], even if its derivative vanishes at zero. The one-trial mean is F(t(x)^d). The full population mean curve therefore determines b(x)=t(x)^d by the inverse of F on [w_0,1]. The full grouped law contains no further distinction between worlds with the same b-curve, since each component propensity is already b(x)^v_i.

For two scales d<e, use u in [0,1] and define

    x(u)=1-(u^e+u^d)/2,
    t_d(x(u))=u^e,  t_e(x(u))=u^d.

This is a continuous bijective command parameterization; the rate maps are continuous, strictly increasing and endpoint-preserving. Their identical primitive bases are u^(de), and their opposite rate discrepancies are ±(u^d-u^e)/2. Differentiate:

    (u^d-u^e)'=u^(d-1)[d-e u^(e-d)].

The unique interior maximum occurs at u_*=(d/e)^(1/(e-d)); hence the required common radius is

    theta(d,e) = (e-d)/(2e) * (d/e)^(d/(e-d)).

This radius is attainable inclusively. To prove necessity at smaller radii, set t_*=u_*^e, s_*=u_*^d, m=(t_*+s_*)/2, and command x_*=1-m. Any eta<theta gives t_*<A=m-eta<=B=m+eta<s_*. Thus

    A^d > t_*^d = s_*^e > B^e.

The scalar-base intervals are disjoint. Strict monotonicity of F preserves their separation, proving that no identical population response curve exists below theta. This proof covers arbitrary nondecreasing maps, including discontinuous ones, because it only uses the local uniform-error bound at the chosen command.

For scales 1,...,D with D>=2, the frozen pure-count catalogue theorem supplies the shared separating command below theta(D-1,D)=eta*_(D-1), and the final adjacent pair supplies all-command ambiguity at and above it. Because F is one-to-one, this population threshold transfers exactly. For D=1 there is no remaining scale decision.

This argument does not import a numerical recovery method for an unknown signature, an empirical inverse of F, the pure-count sample budget, or its conditioning. Under additionally supplied v and weights and independent fresh groups, one can separately derive a finite-sample procedure from the transformed mean gaps F(A^j)-F(B^(j+1)). Those are generally not the pure-count gaps A^j-B^(j+1). Unknown tiny weights or large primitive exponents can make them poorly conditioned. A population quotient theorem should not be advertised as a uniform mixture-recovery algorithm.

## 5. Boundaries, countermodels and representations

- Zero-only law: at an interior survival setting, scalar law delta_1 identifies zero-only count support. There is no positive primitive vector or positive scale. Calibration is uninformative for this law.
- Actual survival 1: all counts have propensity 1, so the endpoint law loses even zero mass.
- Actual survival 0: count zero has propensity 1 by the no-root model, and every positive count has propensity 0. The scalar law identifies only zero mass. No unqualified 0^0 arithmetic is needed.
- The competitor atom bound matters: 2k-1 moments compare at-most-k laws; a k+1 competitor can match that panel. An extra order 2k positive squared-annihilator certificate addresses scalar support, not arbitrary causal or calibration assumptions.
- Exact shifted k=2 obstruction: weights (27,148)/175 on counts (1,3), and (111,64)/175 on counts (2,4), at t=3/4. Their first moments are 189/400, second moments are 243/1024, and third-moment difference is 26973/6553600. Their primitive signatures are (1,3) and (1,2), respectively. Full length-two grouped laws coincide.
- Fresh resampling of counts 1 and 2 with equal probabilities and identity calibration yields no-hit mean s=(t+t^2)/2. Pure count 1 with this survival has rate x+x(1-x)/2, whose maximal discrepancy is 1/8. Fresh independent endpoint sequences agree at every command, including adaptive sequences. Held repeats separate the models by second-moment gap t^2(1-t)^2/4>0 at interior t.
- Rational mixture weights do not imply rational nodes or moments when the survival is arbitrary real. The predecessor had fixed rational nodes, a stronger contract. Mathematical logarithm ratios are not an automatic terminating exact numerical decoder.
- A sufficient exact rational-node contract is available: choose a prime with nonzero valuation in one positive node, factor all rational nodes, and normalize their signed valuations by their common gcd to obtain v; validate the remaining prime valuations, node powers and weights. This is a basic finite procedure, not a bit-complexity claim. It does not cover arbitrary real inputs.
- A direct arbitrary-valid Cauchy-oracle obstruction for primitive signatures uses weights 1/2 on counts (1,2) at any t in (0,1), versus weights 1/2 on counts (n,2n+1) at survival t^(1/n). Both signatures have gcd one. The latter node pair (t,t^(2+1/n)) converges to (t,t^2), but its primitive vector differs for every n>1. Every finite set of moment/grouped-word queries with positive tolerances can share valid replies for sufficiently large n. Thus a universally correct finite-stopping exact primitive-signature algorithm cannot be obtained from that unrestricted approximation contract. The predecessor's k=1 obstruction should not be copied unchanged: every single positive count has primitive signature (1).

## 6. Independent controls

The script independent_controls.py uses Python's exact Fraction arithmetic throughout. It checks scaled node/moment/grouped-word identities with and without zero mass; rational versus integer dilation; interpolation and Vandermonde basis identities; the prescribed countermodels; endpoint collapse; transformed interval separation; general-pair derivative signs and rational critical values; restricted-band interpolation; and exactly enumerated adaptive held-latent transcript distributions with random policy seeds and early stopping. The frozen predecessor digests are checked before and after. These are finite diagnostics, with the mathematical arguments above providing the universal assessment.
