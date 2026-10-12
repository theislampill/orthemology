# Independent review: delayed finite-prefix obstruction

10 October 2026 UTC. Independent ordinary mathematical review of the root
addendum. No formal-kernel verification or effective time threshold is claimed.

## Verdict and exact target

PASS. For every fixed total degree D, a normalized coordinatewise-continuous
path whose initial record has a genuine all-moment probability representative
and is strictly positive on all nonzero polynomial squares has an initial
interval on which its full degree-D record admits a finite atomic probability
representative with at most binomial(d+D,D) atoms.

Reviewed RESULT.md SHA-256:
f7f06518e210b860502c0971aa9ad47a410198d84c519b149a49b953f67c242f.
A byte-identical review target is retained as TARGET_RESULT.md. The author's
“independent review pending” line is a historical statement in the immutable
reviewed target; this separate review supplies the verdict.

## 1. Uniform strict positivity is proved correctly

Fix D and a monomial coefficient norm. If p is a nonzero globally nonnegative
polynomial and its integral under the initial law were zero, positivity would
force p=0 almost everywhere. Then p²=0 almost everywhere and L_0(p²)=0,
contrary to the strict-square hypothesis. The all-moment assumption ensures
both integrals exist. Thus L_0 is strictly positive on every nonzero member
of the degree-D nonnegative cone.

That cone is closed in finite-dimensional coefficient space: it is the
intersection over x∈R^d of the closed halfspaces p(x)≥0. Its intersection
with the coefficient-unit sphere is compact and nonempty (it contains an
appropriately normalized positive constant). Since L_0 is continuous and
strictly positive at every point of this compact set, its attained minimum
delta_D is strictly positive. Pointwise positivity alone would not supply a
uniform margin on an unbounded or noncompact coefficient set; the fixed
degree and normalization are essential.

Continuity of finitely many monomial moments implies convergence in the dual
norm on V_D. Choosing the error below delta_D/2 proves the claimed uniform
strict inequality, including for polynomials whose coefficients depend on t.
No positivity assumption on L_t for t>0 is needed at this step.

## 2. Actual finite representation, not just a closed-cone limit

Let M_D be the finite conic hull of the evaluation vectors. Its dual is
exactly the globally nonnegative polynomial cone C_D. Finite-dimensional
separation (equivalently, the bipolar theorem for a convex cone) identifies
closure(M_D)=C_D*. Mere nonnegative pairing would locate a moment vector only
in this closure, which is not enough for an actual representing measure on
an unbounded domain. The proof correctly avoids that gap.

The strict uniform margin places y_t in the Euclidean interior of C_D*:
every sufficiently small vector perturbation changes its pairing with a
unit coefficient vector by less than that margin. By homogeneity the
perturbed pairing remains nonnegative on all of C_D. This gives a full
ball in closure(M_D), not merely a relative-interior assertion in a mass-one
hyperplane.

The evaluation vectors linearly span R^N. Otherwise a nonzero coefficient
vector would define a polynomial vanishing at every point of R^d, which is
impossible. Selecting N linearly independent evaluations and using all
strictly positive combinations exhibits a nonempty open simplicial cone in
M_D. Thus the full-dimensional convex interior argument is applicable.

For completeness, the needed convex fact can be established without assuming
M_D is closed. Around an interior point y of closure(M_D), choose N+1 small
simplex vertices whose convex hull contains y in its interior and lies in
that closure. Approximate each vertex by a point of M_D. For sufficiently
small approximation, affine independence and the strictly positive
barycentric coordinates of y persist by continuity of the inverse affine
coordinate matrix. Hence y is an exact convex combination of the approximating
vertices and belongs to M_D by convexity. This proves the required
interior(closure(M_D))⊆M_D step. The reverse interior inclusion is immediate.

This reasoning remains valid for odd D, when the nonnegative cone can occupy
a proper coefficient subspace, and for D=0. It does not assume compact support
of the initial measure or closedness of the original evaluation cone.

## 3. Atom bound and normalization

Membership in M_D gives a finite nonnegative combination of evaluation
vectors. If more than N positive weights occur, choose a linear dependence
among their vectors and move along it until one positive weight becomes zero,
without making any weight negative or changing the represented vector.
Repeat to leave at most N weights. This is the conic Caratheodory reduction.
Here all evaluation vectors have constant coordinate one, so every dependence
has coefficient sum zero; any nonzero dependence has both signs, and the
reduction step is valid.

Because L_t(1)=1, the remaining weights sum to one. They define the asserted
finite atomic probability with every absolute moment finite, and it matches
all degree-at-most-D moments. N=binomial(d+D,D) is the correct number of
monomials. No continuous selection of atom locations or weights is asserted.

## 4. Application and limits

The frozen escape path meets all hypotheses. Consequently each fixed degree
prefix has an actual probability representative for sufficiently small time,
despite the absence of one law representing the full record at any positive
time. The quantifier order is crucial: for every D there exists epsilon_D;
one positive epsilon working for all D is neither shown nor compatible with
the escape conclusion.

The degree of every nonnegative-polynomial separator must therefore diverge
as t→0+, whenever such separators exist. The escape theorem and its effective
addendum do supply their existence. This is stronger than a statement just
about the family q²F, and the compact nonnegative-cone argument justifies that
strengthening.

There is no claim of a computable epsilon_D, a uniform atom support, compatible
finite-prefix choices, a representing law for every degree at one time, or a
new general convex-geometric mechanism. The proof is an ordinary application
of finite-dimensional compactness and convex separation to the specified
path. Its stated caution about transferring the result to human cognition or
metaphysical conclusions is appropriate.

No mathematical correction is required. This review is proof inspection, not
an executed moment solver or a formal proof checker.
