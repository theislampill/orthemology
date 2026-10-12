# Continuous signed controls: a finite-rank safeguard and a remaining boundary

10 October 2026 UTC. Additive ordinary mathematical investigation. The parent proposed the bounded-rank proof route; the worker checked and developed it. No independent review, formal-kernel verification, field-priority claim, protected-source change, empirical identification, or T20 closure is claimed.

## 1. Outcome and exact scope

The unrestricted question remains unresolved here: a compact initial probability law, coordinatewise C1 normalized polynomial functional path, full square positivity, and the signed linear hierarchy with arbitrary continuous changing-direction control have not been proved sufficient, and no counterexample is supplied.

There is, however, a structural sufficient condition which settles the actual finite-support case within a substantially wider control repertoire than the autonomous proof:

**Finite-rank theorem (arbitrary signed polynomial killing).** Let h_t be real polynomials with continuous time-dependent coefficients and a uniform degree bound on each compact time interval. Suppose L_t is a real polynomial functional satisfying, for every real polynomial p,q,

    L_t(1)=1,   L_t(q²)≥0,
    dL_t(p)/dt = −L_t(h_t p)+L_t(h_t)L_t(p),

with every coordinate C1 (right-sided at zero). Suppose in addition that the full polynomial Hankel rank is bounded on every compact time interval:

    for each H<T there is a finite R_H with rank H(L_t)≤R_H for 0≤t≤H.   (R)

Then there are fixed distinct points ξ_1,…,ξ_r and positive weights w_j summing to one such that

    L_0(p)=Σ_j w_j p(ξ_j),
    L_t(p)=Σ_j w_j exp(−H_t(ξ_j))p(ξ_j) / Z(t),
    H_t(x)=∫_0^t h_s(x)ds,   Z(t)=Σ_j w_j exp(−H_t(ξ_j)).

Every time has a unique representing probability, on exactly the same r points, and the full rank equals r throughout. The signed-linear case h_t(x)=g(t)·x gives H_t(x)=U(t)·x for U(t)=∫_0^t g(s)ds. No sign, SOS, or coercivity restriction is imposed on h_t. The theorem does not assume a positive-time joint law, an a priori atom location bound, a moment growth bound, or that the rank is already constant. Even the initial law is a consequence of (R) and positivity. In the intended application, its atoms are precisely the positive-mass distinct channel columns of the supplied initial law.

Condition (R) is an additional promise on the supplied abstract path. Initial finite rank alone does not establish it. The condition is sufficient, not necessary for a valid hierarchy: the exact tilt of the uniform law on [−1,1] has infinite full Hankel rank, since every nonzero polynomial has strictly positive square integral. It cannot be replaced here by a rank bound on one arbitrarily fixed truncated moment matrix, and pointwise finite rank without local uniform boundedness is not covered.

A second, independent corollary covers compact initial laws for rank-one controls g(t)=a(t)v when continuous a has one sign, including arbitrary zero sets. It is proved in §5 by a justified change of clock. Locally finite concatenations of such sign-monotone clock segments are also covered. Arbitrary infinitely sign-oscillating schedules are not inferred from that argument.

## 2. Static finite-rank representation

For a square-positive functional L, put I={p:L(p²)=0}. Polynomial Cauchy–Schwarz implies L(pr)=0 for all r when p∈I. It also makes I an ideal: applying this equality to r=p s² gives L((ps)²)=0.

The quotient E=R[x]/I has inner product ⟨[p],[q]⟩=L(pq), and dimension equal to the full Hankel rank. If that rank is r<∞, coordinate multiplication X_i[p]=[x_i p] is well-defined, symmetric, and pairwise commuting. Finite-dimensional simultaneous diagonalization gives joint eigenvalues ξ_j and orthogonal joint eigenspaces. The vector [1] is cyclic because polynomial applications of the X_i span E. Thus every joint eigenspace is one-dimensional and its projection of [1] is nonzero: otherwise cyclicity would fail. Consequently there are exactly r distinct joint eigenvalues and

    L(p)=Σ_{j=1}^r w_j p(ξ_j),   w_j>0.

Normalization gives Σw_j=1. This is the classical full finite-rank moment theorem; see Schmüdgen, *Ten Lectures on the Moment Problem*, Theorem 9.5 and its stated GNS proof idea, printed p.69, https://arxiv.org/pdf/2008.12698 . The argument above is included to expose what positivity supplies.

Uniqueness also follows directly. The polynomial F(x)=∏_j ||x−ξ_j||² is nonnegative and vanishes precisely on these r points. Any positive representing measure has integral F=L(F)=0, so is supported there. Lagrange interpolation in any scalar projection separating the points fixes its weights. Thus a second representative cannot hide extra support elsewhere.

## 3. Local atomic coordinates on a maximal-rank region

Fix a compact interval [0,H] and let r be the largest attained rank there, finite by (R). The rank-r set is relatively open: some r-by-r polynomial Gram determinant is positive at each of its points, remains positive nearby by coordinate continuity, and larger rank is excluded.

At a rank-r time t*, apply §2. Choose a real linear form ℓ(x)=v·x separating its r atoms. The r-by-r matrix

    B_t=(L_t(ℓ^{k+l}))_{0≤k,l≤r−1}

is positive definite at t* and nearby. Work in such a neighborhood inside the rank-r set. At every nearby time §2 gives exactly r atoms, and invertibility of B_t implies their scalar projections are pairwise distinct.

Solve the monic degree-r annihilator coefficients using

    P_t(z)=z^r+Σ_{k=0}^{r−1} c_k(t)z^k,
    L_t(ℓ^l P_t(ℓ))=0,   0≤l≤r−1.

The coefficient matrix is B_t, so c_k are C1. The r distinct projected atoms are exactly the roots of P_t: the equations and the invertible Vandermonde matrix force P_t to vanish at every projected atom. At t* the roots are simple, so they admit local C1 labels λ_j(t). The moments L_t(ℓ^k), 0≤k≤r−1, then give C1 positive weights by a Vandermonde solve. Finally each coordinate ξ_{ji}(t) is recovered through the same invertible matrix from

    L_t(x_i ℓ^k)=Σ_j w_j(t) ξ_{ji}(t) λ_j(t)^k,
    0≤k≤r−1.

Thus all atom positions and weights have local C1 labels, derived from finitely many supplied moment coordinates. No differentiability of an arbitrarily selected representing measure was assumed.

At a fixed time t in this chart, let

    b_j(x)=∏_{k≠j} (ℓ(x)−λ_k(t))/(λ_j(t)−λ_k(t)).

For a coordinate i, use the fixed polynomial (with the chosen time's coefficients held constant while differentiating)

    p(x)=(x_i−ξ_{ji}(t)) b_j(x)².

At all current atoms p=0. Its gradient is e_i at atom j and zero at every other atom; the square on b_j is essential. The hierarchy's right side is therefore zero. Differentiating the finite atomic representation gives

    0=dL_s(p)/ds|_{s=t}=w_j(t) ξ'_{ji}(t).

Positive weights force every atom velocity to vanish. Hence the unordered support is locally constant, and therefore constant on each connected rank-r component. Testing interpolation polynomials then gives

    w'_j=−w_j(h_t(ξ_j)−Σ_k w_k h_t(ξ_k)).

These are ordinary finite-dimensional equations, with the exact positive solution between any two times in the component

    w_j(t)=w_j(s) exp(−(H_t(ξ_j)−H_s(ξ_j)))
           / Σ_k w_k(s) exp(−(H_t(ξ_k)−H_s(ξ_k))).       (1)

## 4. Why a maximal-rank component cannot end

Let J be any nonempty connected component of the rank-r set in [0,H]. Its support is fixed by §3. If τ∈[0,H] is a finite endpoint in its relative closure, formula (1), continuity of h_t at each fixed ξ_j, and finiteness of the fixed support give strictly positive limiting weights at τ. Every relevant integrated energy is finite across that finite endpoint. For each polynomial p, coordinate continuity identifies L_τ(p) with the resulting r-atom formula. Its full rank is r.

Moreover the ℓ-Hankel determinant for these fixed atoms has a strictly positive limit at τ. It remains positive in a relative neighborhood of τ; the rank bound r then keeps that whole neighborhood in the rank-r set. Thus τ belongs to the same component and cannot be a finite boundary separating it from another rank stratum. The component is both relatively closed and relatively open in connected [0,H], so J=[0,H].

In particular r=rank H(L_0), the support is the initial support, and (1) with s=0 proves the theorem on [0,H]. Since H<T was arbitrary, the theorem holds on the entire supplied horizon. This endpoint argument is why mere local atomic charts are enough; it explicitly rules out atom births, collisions, or finite-time loss within the bounded-rank class.

The theorem also gives equality of every polynomial null ideal and of every finite polynomial Gram kernel throughout the path, because the fixed support weights stay strictly positive. This conclusion is conditional on (R) here; autonomous null-ideal invariance in the predecessor needed no rank promise.

## 5. Compact initial laws and a one-sign rank-one clock

Let μ have compact support, let v∈R^d, and let g(t)=a(t)v with a continuous and nonnegative. Define s(t)=∫_0^t a(u)du. This clock is continuous nondecreasing. If s(t_1)=s(t_2), continuity and nonnegativity imply a=0 on [t_1,t_2]. The hierarchy then makes every polynomial coordinate constant there. Thus L_t descends to a well-defined functional path B_s on the image of the clock.

On any compact time interval, the continuous surjective monotone clock is a quotient map. Since every L-coordinate is constant on its fibres, every B-coordinate is continuous, including at clock values corresponding to flat intervals. Write

    F_p(B)=−B((v·x)p)+B(v·x)B(p).

The integrated original hierarchy gives

    B_{s_2}(p)−B_{s_1}(p)=∫_{s_1}^{s_2} F_p(B_u)du.

To justify the substitution even at clock flats, use the usual substitution formula for an absolutely continuous nondecreasing s and the continuous descended integrand F_p(B_s). The displayed identity makes each B-coordinate C1 in clock time, with derivative F_p(B_s), including the one-sided boundary convention.

B is normalized and fully square-positive. Apply the predecessor's autonomous bounded-energy theorem to h=v·x; compact initial support makes h bounded on μ. Therefore

    L_t(p)=∫p exp(−s(t)v·x)dμ / ∫exp(−s(t)v·x)dμ.

If the clock is identically zero, the original hierarchy is constant and the formula is immediate. For a nonpositive a, replace (a,v) by (−a,−v). Concatenating locally finitely many sign-monotone segments uses the compact exact law at each endpoint.

This proof makes no assertion for a general rank-one a with infinitely many sign changes accumulating at the initial or another finite time. Reparametrization then ceases to be globally monotone. Merely knowing the autonomous answer on individual nonzero-sign intervals does not prove an abstract path cannot choose a different continuation at an accumulation boundary. This is a gap in that proof route, not a counterexample or a claim that the rank-one theorem is false.

## 6. Source-faithful finite-channel and Fisher interface

The inspected tensor-moment-continuation-20261009/RESULT.md §2 explicitly declares locally finite piecewise-constant controls. Its finite-dimensional replicator solution extends immediately to continuous controls by the same finite ODE calculation, but arbitrary continuous controls should not be attributed to that packet's declared repertoire.

A genuinely continuous trajectory-dependent covector can occur in the evolving Fisher correction for a fixed smooth objective, where g(t)=∇J(q(t)). The actual finite-law dynamics already has its finite support by construction. The result here addresses a different question: whether a supplied abstract full hierarchy is forced to coincide with that finite-law lift. Under (R), yes. For the inherited C² objective, the gradient is locally Lipschitz on its domain, so ordinary finite-dimensional uniqueness for the induced weight equation additionally identifies paths with the same initial law while both coarse paths remain in that domain. Global existence is not inferred when the gradient may become unbounded near a domain boundary. If the gradient extends locally Lipschitz to a neighborhood of the compact initial support convex hull, it is bounded there, and the finite weight dynamics extends across every finite horizon. Continuity alone of an arbitrary gradient is not silently promoted to a general feedback-ODE uniqueness condition.

This is conditional numerical mathematics. Neither a rank promise nor a moment law authenticates source tokens, identifies an actual noetic realization, establishes target truth or epistemic warrant, or authorizes record deletion. Channel revision and provenance-sensitive operations remain outside this declared continuation repertoire.

The inspected Curto–di Dio–Korda–Magron v3, Theorem 4.2, https://arxiv.org/pdf/2211.04416v3 , already treats finite-rank moment evolution through atomic transport/reaction. Its proof starts from the finite atomic measure and invokes its evolution. It is important ancestry for the finite-atom picture, but it is not imported as a proof that every supplied square-positive hierarchy with no positive-time measure premise has the requisite rank/support. The current argument supplies its own bounded-rank reverse-lifting and endpoint reasoning. The retained source text from the earlier comparison packet was inspected at Theorem 4.2; no broad literature review is claimed.

## 7. What still blocks the unrestricted claim

For an initially null q, unnormalization A_t=b(t)L_t gives

    (A_t(q²))'=−A_t((g(t)·x)q²),
    |(A_t(q²))'|²≤A_t(q²) A_t((g(t)·x)² q²).

Coordinate continuity bounds the second factor on compact time intervals, but the resulting square-root differential inequality does not force a zero initial value to remain zero. Nonnegative scalar functions proportional to t² already satisfy such an inequality while leaving zero. This is an exact obstruction to this elementary null-ideal proof, not a hierarchy counterexample.

For fixed h, the predecessor differentiates repeatedly to obtain nonnegative even derivatives A_t(q²h^{2n}) and interior factorial bounds. Changing g introduces transverse terms when differentiable, while mere continuous g does not even permit those higher differentiations. No corresponding all-direction moment bound has been obtained from the stated assumptions.

Approximating g by piecewise-constant controls constructs convergent genuine tilted laws on the fixed initial compact support. It does not identify the supplied abstract path without an independent uniqueness or compactness argument about that path. Neither the rank theorem nor the clock corollary is used to disguise this missing step.

## 8. Verification and retained inputs

verify.py checks, by exact symbolic algebra, the Hermite test-polynomial values and gradients, local Vandermonde coordinate recovery, a genuinely changing-direction signed-linear three-atom hierarchy, a time-varying signed-quadratic hierarchy, and the positive finite-boundary weight mechanism. These controls supplement the general proof; they do not establish it by finite enumeration. INPUT_BINDINGS.json records SHA-256 digests of the three requested predecessors and the source comparison text used. All preceding artifacts remain unchanged.
