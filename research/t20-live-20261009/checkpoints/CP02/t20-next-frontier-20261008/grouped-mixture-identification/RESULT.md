# Grouped repeats identify finite mixtures of calibrated histograms

8 October 2026 UTC. Prospective sibling research only. This stage neither changes the countable-signature stage (initially supplied as still-editing, subsequently frozen by its author) nor integrates into the protected repository. No owner acceptance, T20 closure, physical-original count, or source-level bridge is claimed.

## Answer and exact scope

**Yes.** Let a latent inventory be a finite unguarded route histogram from the previously proved base4 class. Let its distribution have at most `k` distinct histograms. Sample the inventory once per group, hold it fixed within that group, and make conditionally independent repetitions of the same calibrated experiment. The exact probabilities of no effect in all of `r` repetitions, for `r=1,...,2k−1`, together with normalization at `r=0`, identify the component histograms and their positive mixture weights, up to permutation.

This is a faithful application of classical finite-atomic moment identification, not a new general mixture theorem. The base4 injection supplies the final map from scalar nodes back to histograms. The consecutive-moment bound is sharp even when every node is an actual permitted histogram code and every weight is a positive rational: two different `k`-component mixtures can agree through order `2k−2`.

Three distinctions matter immediately:

1. `2k−1` is a **maximum within-group order**, not a number of observed groups or a finite experimental sample guarantee.
2. Its uniqueness is against other mixtures with at most `k` components. An additional moment through order `2k` certifies a `k`-node scalar law against arbitrary positive scalar probability laws and supports a stopping test when the component bound is unknown.
3. Uniqueness for real-valued moments is mathematical. An executable exact algorithm requires an explicit representation with exact arithmetic and zero testing. Rational weights and exact numerator/denominator moment inputs supply one such contract; arbitrary Cauchy approximations do not.

See `PROCESS_AND_ORACLE_BOUNDARIES.md` for the grouped tensor, the inherited continuation-observable map, fresh resampling and dependent-emission failures, stationary persistence certification and its adversaries, and the separation from physical ownership. `SOURCE_AUDIT.md` records primary ancestry and source checks. `exact_controls.py` and `results/exact_controls.log` provide finite rational controls, not substitutes for the proofs below.

## 1. Model and imported scalar injection

Ports are indexed by `i=0,1,...`, with fixed calibration

`x_i = 4^(−2^i)`.

A nonempty finite positive support `S` has integer code `e(S)=sum_{i in S}2^i`. A finite unguarded histogram is a finitely supported function `H=(n_e)_{e>=1}`, where each `n_e` is a nonnegative integer. The established independent-route law gives

`q(H) = product_e (1−4^(−e))^(n_e)`, with `0<q(H)<=1`.

The empty histogram has `q=1`. The preceding stage proves that `H -> q(H)` is injective on this finite class, using a base4 primitive-prime separator at the largest differing support code. Its exact rational decoder recovers `H` from `q(H)`. We import that theorem with all its premises, rather than infer finitude or route independence from a probability value.

Let

`Pi = sum_{a=1}^s w_a delta_{H_a}`, where `1<=s<=k`, `w_a>0`, and `sum_a w_a=1`,

and where the `H_a` are distinct. Write `z_a=q(H_a)`. The injection makes these nodes distinct. The scalar pushforward is

`mu = sum_{a=1}^s w_a delta_{z_a}`.

Each group first receives one `H~Pi`. Conditional on that `H`, no-effect indicators `Y_1,...,Y_R` are independent Bernoulli variables with parameter `q(H)`. Thus

`m_r := P(Y_1=...=Y_r=1) = E_mu[z^r] = sum_a w_a z_a^r`, and `m_0=1`.

The repetitions are separate episodes. The grouping assumption does not identify two simultaneous producers of a numerically identical effect. For estimation of mixture weights, the group ensemble must actually exhibit the mixture law, for example by independently drawing `H` afresh between groups. Holding one realised inventory fixed forever produces information about that component, not empirical frequencies of all mixture components. Independence between groups is unnecessary for the distributional identities but is an additional requirement for the usual independent-sample estimation interpretation.

## 2. Identification through order 2k−1

**Proposition 1.** Among probability laws on finite unguarded histograms with at most `k` distinct components, the map `Pi -> (m_0,...,m_(2k−1))` is injective.

**Proof.** Suppose `mu` and `nu` are the scalar pushforwards of two such laws and have the indicated moments. Combine their distinct nodes into `t_1,...,t_N`, where `N<=2k`. Write the signed difference as

`mu−nu = sum_{j=1}^N c_j delta_(t_j)`.

The moment equations imply `sum_j c_j t_j^r=0` for `r=0,...,N−1`. For any chosen node `t_i`, the Lagrange polynomial

`L_i(t) = product_{j!=i}(t−t_j)/(t_i−t_j)`

has degree `N−1` and takes values `L_i(t_j)=1` if `j=i`, otherwise zero. Integrating it against the signed difference therefore gives both zero, by the moment equations, and `c_i`, by its node values. Hence all `c_i=0` and `mu=nu`. Equivalently the corresponding square Vandermonde matrix is invertible. Finally scalar injection recovers the unique histogram at every node and thus `Pi`. This identifies weights and distinct histograms, not arbitrary labels assigned to mixture components. QED.

No bound on the largest port index, route multiplicity, or support code was used. The external component-count bound and per-component finitude are different assumptions.

If the actual law has `s<k` components, order `2k−2` already excludes all competitors of at most `k` components, because the combined support has at most `s+k<=2k−1` nodes. The sharp obstruction below concerns the worst case of `k` versus `k` components.

## 3. Sharpness on actual base4 histogram codes

The following elementary interpolation identity supplies exact positive examples without selecting arbitrary real nodes that might fail histogram eligibility.

**Interpolation identity.** Given `N` distinct real nodes `z_0,...,z_(N−1)`, define

`c_j = 1 / product_(ell!=j)(z_j−z_ell)`.

Then

`sum_j c_j z_j^r = 0` for `0<=r<=N−2`, and `sum_j c_j z_j^(N−1)=1`.

**Proof.** Interpolate the polynomial `t^r` by the Lagrange basis at those `N` nodes. Compare coefficients of `t^(N−1)`: the coefficient of that degree in `L_j(t)` is `c_j`. The coefficient in `t^r` is zero below degree `N−1` and one at that degree. QED.

For any `k>=1`, choose `N=2k` nodes

`z_j=(3/4)^j`, `j=0,...,2k−1`.

These are precisely the codes of histograms with `j` copies of the single route of support `{0}`. They are rational and strictly decreasing. In the denominator defining `c_j`, exactly `j` factors are negative, so `sign(c_j)=(-1)^j`. Let

`C = sum_(j even)c_j = −sum_(j odd)c_j > 0`.

The equality is the interpolation identity at `r=0`. Define

`mu_even = sum_(j even)(c_j/C) delta_(z_j)`,

`mu_odd = sum_(j odd)(−c_j/C) delta_(z_j)`.

Each is a probability law with exactly `k` nodes and strictly positive rational weights. They are different, have disjoint supports, agree in all moments through order `2k−2`, and differ at the next moment by

`m_(2k−1)(mu_even) − m_(2k−1)(mu_odd) = 1/C > 0`.

This proves sharpness for the consecutive moment panel and, by the grouped-law equivalence below, for binary grouped observations of fixed length `2k−2`. It is not a lower bound for every conceivable intervention or every encoding of a restricted hypothesis class.

The empty histogram is dispensable. Replace every node by `(3/4)z_j`, equivalently add one `{0}` route to every component on both sides, retaining the same weights. The order-`r` moments are simply multiplied by `(3/4)^r`; all components are then nonempty. In fact the unshifted examples use one port only and no component has more than `2k−1` routes. The lower bound does not depend on infinitely many active ports, irrational weights, or large unseen supports.

### Explicit k=2 control

Using `H_j` for `j` copies of the `{0}` route:

`Pi_even = (27/175) delta_(H_0) + (148/175) delta_(H_2)`,

`Pi_odd = (111/175) delta_(H_1) + (64/175) delta_(H_3)`.

The nodes are respectively `{1,9/16}` and `{3/4,27/64}`. Both laws have

`m_0=1`, `m_1=63/100`, `m_2=27/64`.

Their third moments are `7803/25600` and `30213/102400`, with difference `999/102400`. Thus two grouped repeats do not identify arbitrary two-component mixtures, even though two repeats separate the earlier specially chosen pair.

For `k=1`, normalization alone obviously does not distinguish the point masses at `1` and `3/4`; the first moment does. This includes the edge case sometimes omitted from general grouped-sample sharpness statements.

## 4. Exact constructive reconstruction under a declared oracle

This is the standard univariate Prony/Hankel reconstruction specialized to these positive rational nodes. It is included to show the transport is effective under a suitable exact input contract.

Assume first that the moments are explicitly represented rational numbers and come from the promised model. With a supplied upper bound `k`, form the `k`-by-`k` matrix

`G_k = [m_(i+j)]_(0<=i,j<k)`.

Let `V_(i,a)=z_a^i`. Then `G_k=V diag(w_a) V^T`. Since `k>=s`, the first `s` rows contain a square invertible Vandermonde matrix, so `rank(G_k)=s`. This uses moments only through `2k−2`. Its leading `s`-by-`s` block `G_s` is positive definite: for a nonzero polynomial `a` of degree at most `s−1`,

`a^T G_s a = sum_b w_b a(z_b)^2 > 0`,

because a polynomial of that degree cannot vanish at all `s` distinct nodes.

Solve

`sum_(ell=0)^(s−1) p_ell m_(j+ell) = −m_(j+s)`, for `j=0,...,s−1`,

and set `p(t)=t^s+sum_(ell=0)^(s−1)p_ell t^ell`. The polynomial `product_a(t−z_a)` satisfies these equations and uniqueness of the solution makes it the recovered polynomial. The largest moment used is `m_(2s−1)`, available under the bound.

Recover its distinct rational roots exactly, then solve the `s`-by-`s` Vandermonde system `sum_a w_a z_a^r=m_r` for `r=0,...,s−1`. Decode each node using the previously proved exact scalar decoder. Finally verify positive weights, unit sum, root distinctness and range, every histogram eligibility check, and reconstruction of every supplied moment. These checks distinguish a validated promised input from arbitrary malformed rational data.

Exact rational Gaussian elimination and rational-polynomial factorization give a terminating procedure. The rational-root theorem and finite divisor enumeration alone suffice for a basic total root procedure; no efficiency claim is needed here. Under this promised model the polynomial has only rational roots. No new end-to-end polynomial bit-complexity, numerical conditioning, or experimental sampling bound is claimed.

For arbitrary positive **real** mixture weights, the uniqueness proof remains true, but the moments need not be rational and may have no finite computable representation. Executing the displayed procedure then requires a specified exact arithmetic/zero-testing and root-representation facility; ordinary access to convergent approximations is insufficient. Saying the moments are mathematically exact does not itself specify such an oracle.

## 5. The bound on competitors cannot be silently dropped

Use the same interpolation construction with `N=2k+1` nodes `z_j=(3/4)^j`, `j=0,...,2k`. The positive even-index coefficients give `k+1` components and the negative odd-index coefficients give `k` components. After normalization these two permitted-code probability laws agree through order `N−2=2k−1` and differ at order `2k`.

Thus a `k`-component model recovered from `2k−1` moments need not be the only positive finite mixture consistent with the data when larger competitors are admitted. Again every weight is positive rational; shifting all indices by one removes the empty inventory.

**Proposition 2.** If `mu` has `s` distinct scalar nodes, its moments through order `2s` uniquely determine it among all positive Borel probability measures on `[0,1]`, including measures with infinite support.

**Proof.** Put `p(t)=product_(a=1)^s(t−z_a)`. If `nu` has the same moments through `2s`, then

`integral p(t)^2 dnu(t) = integral p(t)^2 dmu(t)=0`.

The integrand is nonnegative, so `p=0` almost surely under `nu`. Thus `nu` is supported on the same `s` roots. Moments `0,...,s−1` then recover its weights by the invertible Vandermonde system, yielding `nu=mu`. The proof uses positivity, not an assumed upper bound on the competitor support. QED.

This is the familiar positive truncated-moment support certificate. It certifies the scalar distribution within a valid moment model. It does not establish that an underlying inventory at one of these scalar values contains finitely many routes: the preceding stage's infinite-route mimic has the same scalar value and therefore every scalar power.

## 6. Unknown finite mixture order and the extra moment

For `r>=0`, let

`M_r = [m_(i+j)]_(0<=i,j<=r)`, a matrix of size `r+1` using moments through `2r`.

Assume genuine moments of a positive probability law and exact arithmetic with decidable zero testing. If the true scalar support has `s` distinct points, `M_0,...,M_(s−1)` are positive definite and `M_s` is singular with rank `s`. Indeed, the associated quadratic forms integrate squares of degree at most `r`; a nonzero such polynomial can vanish on every node exactly when the degree is at least `s`.

Consequently, querying moments in increasing order and stopping at the **first singular `M_r`** terminates at `r=s`, using `m_0,...,m_(2s)`. A nonzero kernel vector supplies a degree-`s` annihilator; its leading coefficient cannot vanish because `M_(s−1)` is positive definite. Normalize it to be monic, reconstruct its roots and weights, and apply Proposition 2. This is a genuine scalar-support certificate rather than a provisional plateau.

If the scalar support is infinite, every `M_r` is positive definite: a nonzero polynomial has only finitely many roots and cannot vanish almost surely on an infinite support. The same procedure then has no finite stopping time. For this reason the finite-support promise guarantees termination, while a witnessed singularity certifies finite scalar support even without that promise.

The algorithmic version is valid, for example, with a promised finite rational-weight mixture and explicitly represented exact rational moment replies. It is not an algorithm for zero testing arbitrary computable reals or for converting empirical frequencies into exact singularity. All per-component finite-histogram, independent-route, grouped-repeat, calibration and visibility premises remain separate. The first-singularity argument is standard moment theory and is not claimed as a new general result.
