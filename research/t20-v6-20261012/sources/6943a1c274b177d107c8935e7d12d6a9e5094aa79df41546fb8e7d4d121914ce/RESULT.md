# Compact initial laws prevent full-square-positive escape

10 October 2026 UTC. Additive T20 investigation. Ordinary proof; independent review pending. No kernel, novelty, empirical, or research-closure claim.

## Question and result

The valid-initial-partial-escape construction shows that initial probability-law representability and all-time full square positivity do not suffice for semantic continuation. Its initial law is indeterminate. Does an independently checkable stronger initial-law condition restore continuation without coercive damping of all, or all but one, coordinates?

Yes for compactly supported initial laws. Let mu be a probability measure on R^d supported on a compact set K. Let g_t be a continuous-coefficient, locally uniformly degree-bounded sum-of-squares polynomial, t in [0,T). Let L_t be a normalised real polynomial functional, coordinatewise C1, satisfying

    L'_t(p) = -L_t(g_t p) + L_t(g_t)L_t(p),
    L_t(q^2) >= 0 for all q and t,
    L_0(p) = integral p dmu.

Then necessarily

    L_t(p) = integral p exp(-integral_0^t g_s ds) dmu
             / integral exp(-integral_0^t g_s ds) dmu.

Every time has a unique representing probability law, supported within K. There is no damping-rank, cumulative coercivity, hidden-dimension, or positive-time representation hypothesis. This applies to the finite-support tensor programme when its energy satisfies the stated SOS/shifted-SOS hypothesis, without requiring a support constraint at later times as an additional premise. It does not automatically cover arbitrary signed linear controls from the wider inherited programme: a nonconstant linear polynomial cannot be made globally SOS merely by a scalar shift.

A continuous scalar shift of the energy is harmless if it makes it SOS; the normalised equation is invariant under that shift. Pointwise nonnegativity without an SOS certificate is not silently substituted in the argument.

## 1. Static square-order domination lemma

Suppose A is a real polynomial functional with

    0 <= A(q^2) <= integral q^2 dmu

for every polynomial q, where mu is a probability measure on compact K. Then A has a unique representation a mu with a measurable density 0 <= a <= 1.

Proof. Cauchy-Schwarz for the positive polynomial functional gives

    |A(p)|^2 <= A(1) A(p^2) <= integral p^2 dmu.

Thus A descends through polynomial equality in L2(mu) and extends continuously to L2(mu). Restricted real polynomials are uniformly dense in C(K), since they contain constants and separate points; C(K) is dense in L2(mu). The Hilbert-space representation theorem supplies a real a in L2(mu) with A(p)=integral p a dmu.

For each nonnegative f in C(K), approximate sqrt(f) uniformly on K by real polynomials q_n. Then q_n^2 converges uniformly to f, hence in L2(mu). Therefore

    0 <= integral f a dmu <= integral f dmu.

The inequalities hold because they hold for q_n^2 before passage to the limit. Positivity of these finite signed measures on nonnegative continuous functions implies 0<=a<=1 almost everywhere. This proves existence and domination.

For uniqueness among arbitrary measures on R^d, take R>=1 with K contained in [-R,R]^d. Any representing positive measure nu satisfies

    integral x_i^(2n) dnu = A(x_i^(2n)) <= R^(2n).

For epsilon>0 its mass on |x_i|>=R+epsilon is at most (R/(R+epsilon))^(2n), hence zero. Thus it is supported on the same bounding box. Polynomial density there identifies it with a mu. This proves uniqueness without supposing another representative was already supported on K.

The compactness hypothesis is doing real work: the new explicit signed-measure counterexample has a nonmoment square-positive functional dominated by an unbounded moment measure. Square-order domination alone is insufficient.

## 2. The hierarchy supplies domination

Put

    b(t)=exp(-integral_0^t L_s(g_s) ds),
    A_t(p)=b(t)L_t(p).

The integrand is continuous by local degree/coefficient bounds and coordinate continuity. Thus b>0, b(0)=1, and A'_t(p)=-A_t(g_t p). In particular, g_t SOS and square positivity imply

    A'_t(q^2)=-A_t(g_t q^2)<=0.

A product of an SOS polynomial with q^2 is SOS. Therefore

    0 <= A_t(q^2) <= A_0(q^2)=integral q^2 dmu.

The static lemma applies at every time, producing unique nu_t=a_t mu, 0<=a_t<=1. No measurable choice of a joint representing measure is required. Also nu_t(1)=b(t).

## 3. Recover the actual measure evolution

Fix a compact time interval [0,H] within [0,T). The functions g_t restricted to K have a common finite bound M and depend continuously on t in the uniform norm. Every polynomial p satisfies the integrated equation

    nu_t(p)=mu(p)-integral_0^t nu_s(g_s p) ds.

Approximate an arbitrary f in C(K) uniformly by polynomials. Since nu_s<=mu and |g_s|<=M on K, both sides and the time integrals converge uniformly, yielding the same equation for f. Moreover nu_t(f) is continuous by the same approximation. Thus nu solves the weak measure equation with initial value mu.

The explicit measure

    nu*_t = exp(-integral_0^t g_s ds) mu

also solves it, by bounded differentiation on K. To prove uniqueness without assuming differentiability of a_t, let delta_t=nu_t-nu*_t. The equation for continuous test functions of sup norm <=1 yields

    D(t):=||delta_t||_TV <= M integral_0^t D(s) ds.

Here D is bounded and measurable: on the compact metric space K, the unit ball of C(K) admits a countable uniformly dense subset, and D is its supremum of continuous scalar functions. Gronwall's elementary integral inequality gives D=0. Hence nu=nu*. Dividing by b=nu_t(1) establishes the theorem. Since H was arbitrary, it holds on the entire supplied interval. Conversely the displayed tilt is a C1 solution, so it supplies a unique continuation whenever the supplied schedule continues.

## 4. Finite support: exact inherited tensor interface

For mu=sum_j w_j delta_(x_j), with distinct numerical support points and nonnegative weights summing to one, the theorem gives

    w_j(t)=w_j exp(-integral_0^t g_s(x_j) ds) / Z(t).

The moment tensor of degree n is sum_j w_j(t) x_j^(tensor n). For these SOS energies, the finite-support contraction hierarchy is forced by the initial record plus square positivity, rather than merely exhibited as one possible lift. This assertion is narrower than the inherited finite-channel mathematics allowing arbitrary signed linear energies; that wider repertoire is not imported into the theorem.

There is also a purely algebraic support check. If p vanishes on the initial finite support, A_0(p^2)=0, so monotonicity gives A_t(p^2)=0. Polynomial Cauchy-Schwarz then gives A_t(pr)=0 for every r. The whole vanishing ideal remains null, and the functional factors through the finite evaluation algebra. Lagrange interpolation in that algebra recovers nonnegative atomic weights. This agrees with, and does not replace or reprove, the inherited finite-support recovery/closure results.

## 5. Scope and research change

This is a sufficient initial-state safeguard complementary to the cumulative/coercive damping safeguards. It prohibits the new escape even with arbitrarily many hidden coordinates, provided the initial law has compact support. It does not settle whether bare multivariate moment determinacy alone suffices, does not infer compact support from finite observations, and supplies no finite cutoff for all-time square positivity.

The proof uses classical polynomial density, Hilbert representation and elementary weak measure uniqueness. No field-priority claim is made. The project-relative contribution is the implication from this hierarchy's initial compact law and SOS monotonicity to forced law-level continuation, and its precise contrast with the accepted valid-initial noncompact escape.
