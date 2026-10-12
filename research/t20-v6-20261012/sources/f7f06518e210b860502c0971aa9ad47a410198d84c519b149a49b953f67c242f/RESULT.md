# Every fixed finite prefix can remain genuinely representable during full-law escape

10 October 2026 UTC. Root ordinary mathematical addendum. Independent review pending. No new field-priority, kernel-verification, uniform computational bound, or project-closure claim.

## Statement

Let L_t be normalised polynomial functionals on R^d with every moment continuous at t=0. Suppose L_0 is represented by a probability mu with all moments, and L_0(q^2)>0 for every nonzero polynomial q. Then for each fixed total degree D there is epsilon_D>0 such that for every 0<=t<epsilon_D:

1. L_t(p)>0 for every nonzero globally nonnegative polynomial p of degree at most D.
2. The entire degree-at-most-D moment record of L_t has a genuine finite atomic probability representative, with at most binomial(d+D,D) atoms.

No square positivity at positive times is needed for this finite-prefix statement. In the accepted valid-initial-partial-escape theorem it holds despite the absence of a representing law for the full record at every positive time. It is therefore stronger than merely saying that a finite list of square tests passes. It also does not provide one probability law valid for all degrees, one fixed representing support, or compatible choices of these finite-prefix representatives.

## Proof of finite-dimensional positivity

Let V_D be the finite-dimensional real vector space of polynomials of degree at most D, with a fixed monomial basis and its Euclidean coefficient norm. Let C_D consist of polynomials nonnegative everywhere on R^d. This is a closed cone: each point evaluation defines a closed halfspace and C_D is their intersection.

For each nonzero p in C_D, integral p dmu is strictly positive. Otherwise p=0 mu-almost everywhere, giving integral p^2 dmu=0, contrary to the initial strict-square hypothesis. All involved moments are finite. Thus L_0 is strictly positive on C_D intersect the coefficient unit sphere. That intersection is compact, so its minimum delta_D is strictly positive.

Moment continuity implies convergence in the dual norm on V_D. For all sufficiently small t, ||L_t-L_0||<delta_D/2. Homogeneity then gives

    L_t(p) >= (delta_D/2)||p|| > 0

for every nonzero p in C_D. This proves the first claim uniformly over every degree-D nonnegative polynomial, including coefficients chosen as a function of t.

## Proof of finite atomic representation

Put N=dim V_D=binomial(d+D,D). Let v_D(x) in R^N be the monomial evaluation vector including the constant coordinate. Define M_D as the conic hull of all v_D(x), x in R^d; by definition its elements are finite nonnegative linear combinations of evaluations. The dual cone M_D* is exactly C_D under the coefficient/moment pairing. Elementary finite-dimensional cone separation gives closure(M_D)=C_D*.

The uniform strict lower bound just proved places the moment vector y_t of L_t in the interior of C_D*: a sufficiently small Euclidean perturbation retains nonnegative pairing with every coefficient-unit member of C_D. The cone M_D is full dimensional. Indeed, if its linear span were proper, some nonzero polynomial in V_D would vanish at every x in R^d, an impossibility. Equivalently, one can select N linearly independent evaluation vectors; their positive combinations supply a nonempty open simplicial cone within M_D.

For a convex set with nonempty interior, the interior of its closure equals its interior. Hence y_t belongs to M_D itself, not merely its closure. This standard finite-dimensional convex fact can be seen by choosing a small simplex around an interior point of the closure, approximating its vertices by points of the convex set, and retaining the point in the perturbed simplex. Therefore y_t is a finite positive combination of evaluation vectors.

Conic Caratheodory reduction leaves at most N summands: whenever more than N active vectors occur, use a linear dependence to move the positive coefficients until one becomes zero without changing their sum vector, and repeat. The constant coordinate of y_t equals L_t(1)=1, so the coefficients sum to one. These evaluations consequently define the asserted atomic probability law.

The compactness in the first proof is coefficient-space compactness, not an assumed compact support for mu. The atomic supports obtained here may depend on D and t and may grow without bound. No finite-prefix extension to a common all-degree law is inferred.

## Application and discriminating consequence

The accepted full-square-positive escape path has genuine initial mu and initial strict-square positivity. Thus each fixed finite tensor prefix is itself the moment record of an actual law for a sufficiently short initial interval, even though the whole tensor hierarchy ceases to be any law immediately.

Consequently the least total degree of any globally nonnegative polynomial with negative L_t value tends to infinity as t approaches zero through positive times. This conclusion concerns all such separators, not only the special family q(z)^2 F(u,v). It gives no rate or effective epsilon_D. The concrete degree-2054 certificate at t=1 and the per-rational-time effective separator search remain compatible with it.

These are classical finite-dimensional cone mechanisms applied to the new explicit path. The implication for Orthemology is narrow and concrete: finite-prefix semantic validity, even when verified as genuine probability representability rather than coordinate positivity, does not by itself certify a compatible infinite hierarchy. It does not establish a fact about actual human cognition or metaphysical possibility without a separately justified model mapping.
