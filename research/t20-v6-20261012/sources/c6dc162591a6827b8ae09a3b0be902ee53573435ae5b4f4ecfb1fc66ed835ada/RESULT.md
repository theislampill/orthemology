# A genuine initial moment record can escape full realizability

10 October 2026 UTC. Additive ordinary mathematical research. Author-side construction, not independent review. No protected source, accepted packet, integration target, or closure status is changed. No field-priority or formal-kernel claim is made.

## 1. Exact answer and scope

Initial joint representability does **not** force later joint representability under partial cumulative SOS damping, even when every full moment matrix remains strictly positive definite and every coordinate satisfies the hierarchy through zero.

More precisely, fix any finite controlled dimension r>=1 and hidden dimension k>=2. Let g_t(z) be any supplied continuous, locally bounded-degree family of SOS polynomials on R^r, on [0,T), with

    K_t(z) = integral_0^t g_s(z) ds,
    K_t - c(t)|z|^2 SOS for every t>0 and some c(t)>0.

There is a normalized, coordinatewise C1 path L_t on the full algebra R[z,y] such that:

1. L_t(q^2)>0 for every nonzero polynomial q and every 0<=t<T.
2. L'_t(p) = -L_t(g_t p) + L_t(g_t)L_t(p) for every polynomial p.
3. L_0 has an explicitly constructed probability representative with every absolute polynomial moment finite.
4. L_t has no positive representing measure at any t>0.

The same initial probability construction works for every supplied schedule in the stated class. For the elementary special case r=1, k=2, g_t(z)=z^2, the path is coordinatewise C-infinity through zero and exists for all t>=0.

The initial record in this construction is moment-indeterminate. Nothing here asserts the stronger claim with a uniquely determined initial joint law. The distinction from the earlier coordinate-positive counterpaths is full strict square positivity. The distinction from the existing tensor sharpness construction is genuine initial representability. The proof is direct and does not depend on the under-review positive-time law-persistence theorem. It defeats automatic validity of the full-square-positive moment hierarchy initialized with the moments of a genuine law; direct measure-level tilting of that supplied law remains valid and gives a different path.

The key auxiliary answer is also negative: a square-positive polynomial functional dominated in square order by a genuine moment functional need not itself be a moment functional. Section 2 supplies actual positive measures establishing that domination.

## 2. Elementary signed representation of an arbitrary moment array

We first prove the precise signed-measure fact needed below, rather than presuming that PSD domination is possible.

**Lemma.** Let (c_alpha) be any real array with finite entries indexed by all multi-indices alpha in N_0^d. There is a finite real signed Borel measure rho on R^d such that every absolute polynomial moment with respect to |rho| is finite and

    integral x^alpha d rho = c_alpha

for every alpha. When c_0=1, one can construct positive all-moment measures P,N with rho=P-N, P(1)=1+N(1), and N(1)<=1/2.

**Proof.** Start with rho_0=c_0 delta_0. For alpha with |alpha|=n>=1 and R>=1 define the finite signed measure

    D_(alpha,R) = [1/(alpha! R^n)]
       sum_(0<=j<=alpha) (-1)^(n-|j|) binom(alpha,j) delta_(R j).

Products, inequalities and factorials in the multi-index notation are coordinatewise. Finite differences give

    integral x^beta d D_(alpha,R) = 1 if beta=alpha,
                                  0 if |beta|<=n and beta!=alpha.       (2.1)

Indeed the numerator factors into the one-variable sums

    sum_(j_i=0)^(alpha_i) (-1)^(alpha_i-j_i)
          binom(alpha_i,j_i) j_i^(beta_i),

which vanish when beta_i<alpha_i and equal alpha_i! when beta_i=alpha_i. If |beta|<=|alpha| and beta!=alpha, at least one coordinate is smaller. The remaining scale factor is R^(|beta|-n). The convention 0^0=1 handles zero exponents.

For m>=0 and n>=1, the support satisfies |Rj|<=nR. Therefore

    integral |x|^m d|D_(alpha,R)|
       <= [2^n n^m/alpha!] R^(m-n).                              (2.2)

Suppose rho_0,...,rho_(n-1) are already fixed. For every |alpha|=n set

    r_alpha = c_alpha - integral x^alpha d sum_(j=0)^(n-1) rho_j,
    B_n = sum_(|alpha|=n) |r_alpha| 2^n/alpha!.

All these are finite, because only finitely supported measures have been used so far. Choose an integer R_n>=1, greater than R_(n-1) if n>1, with

    R_n >= 2^n n^(n-1) B_n,

and put

    rho_n = sum_(|alpha|=n) r_alpha D_(alpha,R_n).

If B_n=0 the block is zero. For every 0<=m<n, (2.2) gives

    integral |x|^m d|rho_n| <= B_n n^m R_n^(m-n) <= 2^(-n). (2.3)

Here n^m<=n^(n-1) and R_n^(m-n)<=1/R_n. Equation (2.1) proves that this block corrects every degree-n moment exactly and does not alter any lower-degree moment.

The series rho=sum_(n>=0)rho_n converges in total variation, by (2.3) with m=0. For any fixed m, the tail n>m has summable m-th absolute radial moments by (2.3); the finitely many earlier blocks have finite support. Thus integral |x|^m d|rho| is finite. Absolute integrability permits interchanging the series with each monomial integral. For |beta|=m, every later block n>m has zero beta moment, and the partial sum through m has exactly c_beta. This proves the claimed full signed representation; it is not just agreement of finite prefixes.

When c_0=1, define

    P = delta_0 + sum_(n>=1) rho_n^+,
    N = sum_(n>=1) rho_n^-,                                      (2.4)

where rho_n^+,rho_n^- are the positive and negative parts of each finite block. Both sums are genuine positive measures and have every absolute polynomial moment by (2.3). Every n>=1 block has total signed mass zero, so its positive and negative masses each equal half its total variation. Consequently N(1)<=1/2 and P(1)=1+N(1). The measures P,N need not be the mutually singular Jordan parts of the final sum, and no such claim is needed. This completes the proof.

For the inherited dyadic-rational functional below, all residuals and finite-block weights are rational. One may choose the least integer meeting the displayed bound and strict-growth condition. This gives a specified countable atomic construction, with no unsolved moment problem inside it.

## 3. A nonmoment functional inside a genuine moment functional

Use the full functional from full-polynomial-moment-countermodel-20261010/PROOF.md. Its ordinary infinite recurrence proves, on R[u,v],

    Lambda(1)=1,
    Lambda(q^2)>0 for every nonzero polynomial q,
    F(u,v)=1+u^4 v^2+u^2 v^4-u^2 v^2 >= 3/4,
    Lambda(F)=-1.                                                (3.1)

This is the same inherited input used by the existing tensor sharpness theorem. Its infinite strict positivity is not inferred anew from numerical or finite-prefix tests.

Apply Section 2 to c_alpha=Lambda(y^alpha). It gives positive all-moment measures P,N on R^2 such that, as full polynomial functionals,

    Lambda = P-N,   P=Lambda+N.

Write n_0=N(1), C=P(1)=1+n_0. Then 1<C<=3/2. Strict inequality follows because N=0 would make Lambda=P a positive measure, contrary to Lambda(F)=-1. Moreover

    0 <= Lambda(q^2) <= integral q^2 dP.

Thus a genuine moment functional dominates a nonmoment functional in the exact square order relevant to the hierarchy. The complement is itself a genuine moment functional. This resolves the proposed domination implication without any operator-domain or strong-commutation assumption.

For k>2, tensor Lambda,P,N with the standard Gaussian probability on the remaining k-2 hidden coordinates; retain the names Lambda_k,P_k,N_k. For k=2 omit this factor. Then

    Lambda_k=P_k-N_k,  Lambda_k(1)=1,
    Lambda_k(F)=-1,    N_k(1)=n_0,    P_k(1)=C.                    (3.2)

The polynomial F still depends only on the first two hidden coordinates. Lambda_k is strictly square-positive: a nonzero hidden polynomial remains a nonzero polynomial in (u,v) for a nonempty open set of the remaining variables, and the Gaussian factor assigns that open set positive mass.

## 4. The inherited moment-equivalent active pair

Let alpha_1 be the standard lognormal probability on (0,infinity), and put

    S = sum_(j in Z) exp(-j^2/2),
    beta_1 = S^(-1) sum_(j in Z) exp(-j^2/2) delta_(exp j).

These are the classical continuous/discrete lognormal representatives already used and directly checked in initial-validity-counterexample-20261010/RESULT.md. For every integer m>=0,

    integral z^m d alpha_1 = exp(m^2/2),
    integral z^m d beta_1
       = exp(m^2/2) S^(-1) sum_(j in Z) exp(-(j-m)^2/2)
       = exp(m^2/2).                                             (4.1)

All absolute moments are finite. The measures are mutually singular: beta_1 is carried by {exp j:j in Z}, which has alpha_1 measure zero.

For controlled dimension r, set

    alpha = alpha_1 tensor gamma_(r-1),
    beta  = beta_1  tensor gamma_(r-1),

with the Gaussian factor omitted for r=1. They have the same full polynomial moments. Let

    E = {z in R^r : z_1 belongs to {exp j:j in Z}}.

Then alpha(E)=0 and beta(E^c)=0. The measure alpha has a positive density on the nonempty open half-space z_1>0. No full topological support claim about P_k or the initial law is made.

## 5. The path and its genuinely valid initial record

For the supplied schedule define finite positive active measures

    alpha_t = exp(-K_t) alpha,
    beta_t  = exp(-K_t) beta.

Both have every absolute polynomial moment, since K_t>=0. Define the full polynomial functional

    A_t(p) = C^(-1) [ integral Lambda_k(p(z, .)) d alpha_t(z)
                      + integral N_k(p(z, .)) d beta_t(z) ],
    a(t) = A_t(1) = C^(-1)[alpha_t(1)+n_0 beta_t(1)],
    L_t(p) = A_t(p)/a(t).                                        (5.1)

Applying either hidden functional to p leaves a finite polynomial in z. Thus every value in (5.1) is finite. The normalizer is strictly positive at every finite time and a(0)=1.

Every square has nonnegative value because each hidden functional is square-positive. Strictness follows from the first term: if p is a nonzero joint polynomial, at least one of its hidden-monomial coefficient polynomials is nonzero on a nonempty open subset of z_1>0. On that set Lambda_k(p(z, .)^2)>0, and alpha_t has positive density. Hence

    A_t(p^2)>0 and L_t(p^2)>0 for every p!=0.                     (5.2)

On a compact time window, the degree and coefficient bounds for g_t give a fixed polynomial majorant. The hidden evaluations leave polynomial functions, alpha and beta have all absolute moments, and exp(-K_t)<=1. Dominated differentiation, including the right derivative at zero, therefore yields

    A'_t(p)=-A_t(g_t p),    a'(t)=-A_t(g_t).

The quotient rule proves the normalized hierarchy and coordinatewise C1 regularity through zero. In the autonomous case g=z^2, repeated differentiation is dominated by successively higher polynomial moments, giving coordinatewise C-infinity through zero.

At time zero, use equality of all alpha and beta polynomial moments to replace beta by alpha in the second term of (5.1). Since Lambda_k+N_k=P_k,

    A_0(p) = C^(-1) integral integral p(z,y) dP_k(y) d alpha(z).

Consequently the explicit genuine probability

    mu_0 = alpha tensor (P_k/C)                                  (5.3)

represents L_0=A_0 and has every absolute polynomial moment. This is a joint representative, not separate compatible marginals or a verbal mixture involving Lambda_k. The different genuine probability beta tensor (P_k/C) has exactly the same full initial moments, so this initial record is indeed indeterminate.

## 6. No positive-time joint representative exists

Fix t>0 and select c=c(t)>0. The certificate implies K_t>=c|z|^2. Suppose, for contradiction, that a probability rho_t represented L_t. Then the positive finite measure nu=a(t)rho_t would represent A_t.

Let R(z)=|z|^2. The nonnegative exponential series and the known active moments give

    integral exp(cR) dnu
       = sum_(n>=0) c^n A_t(R^n)/n!
       = C^(-1)[integral exp(cR-K_t) d alpha
                   + n_0 integral exp(cR-K_t) d beta]
       <= 1.                                                     (6.1)

All exchanges here involve nonnegative terms and genuine positive measures. There is no presumed joint law in the definition of A_t; nu exists only inside the contradiction argument.

Because F>=3/4, the weighted projection

    sigma = pi_z*(F(y) nu)

is a finite positive measure. Its Gaussian integrability follows from Cauchy-Schwarz and the polynomial moment F^2:

    integral exp(cR/2) d sigma
       = integral F exp(cR/2) dnu
       <= [integral F^2 dnu]^(1/2)
          [integral exp(cR) dnu]^(1/2) < infinity.                 (6.2)

On the other hand, its polynomial moments, by (3.2) and (5.1), are those of the explicitly specified finite signed measure

    w_t = C^(-1)[-alpha_t + N_k(F) beta_t].                        (6.3)

The number N_k(F) is finite and nonnegative. This signed measure also has Gaussian absolute integrability:

    integral exp(cR) d|w_t| <= [1+N_k(F)]/C < infinity.           (6.4)

Finite signed measures with a positive Gaussian absolute moment are determined by all their polynomial moments. Here is the exact elementary argument: exp(|xi||z|) is bounded by a constant times exp(b|z|^2) for any b>0. Thus the Fourier exponential series is absolutely integrable for every xi. Equal polynomial moments give equal Fourier transforms at every xi, and uniqueness of the Fourier transform of finite signed measures identifies the measures. Apply this with the common positive exponent c/2 in (6.2)-(6.4). It gives sigma=w_t.

But the Borel set E from Section 4 satisfies

    w_t(E^c) = -alpha_t(R^r)/C < 0,

since alpha(E)=0, beta(E^c)=0, and exp(-K_t)>0 everywhere. This contradicts positivity of sigma. Hence L_t has no joint probability representative for every t>0.

This proof uses an actual nonnegative polynomial F and actual signed measures. It neither assumes that an abstract family of hidden conditional moments has a measure nor infers strong commutation from bounded weak commutation.

## 7. Explicit nonnegative-polynomial separation at each positive time

The preceding proof already establishes nonrepresentability directly. One can additionally show that at each t>0 there is an ordinary nonnegative joint polynomial whose L_t value is negative.

Let m_t=alpha_t+beta_t. Its positive Gaussian moment implies that polynomials are dense in L2(m_t). To verify this fact, suppose h is orthogonal to every polynomial. The signed measure h m_t is finite by Cauchy-Schwarz; it has a positive Gaussian absolute moment after reducing the exponent by half, again by Cauchy-Schwarz. All its polynomial moments vanish. The signed Fourier argument from Section 6 gives h m_t=0, hence h=0 almost everywhere. The Hilbert-space orthogonal-complement criterion proves density. Real polynomials suffice for real functions.

Choose a nonzero real continuous compactly supported function phi whose support lies in the open strip 1<z_1<e and a bounded set of the remaining controlled coordinates. Then phi=0 beta_t-almost everywhere and integral phi^2 d alpha_t>0. Let q_n be real polynomials converging to phi in L2(m_t). Because the Radon-Nikodym density of w_t relative to m_t is bounded in absolute value by max(1,N_k(F))/C,

    integral q_n^2 dw_t -> integral phi^2 dw_t
                         = -C^(-1) integral phi^2 d alpha_t < 0.

The convergence follows from

    integral |q_n^2-phi^2| dm_t
       <= ||q_n-phi||_2 (||q_n||_2+||phi||_2) -> 0.

Consequently, for some finite n,

    H_t(z,y)=q_n(z)^2 F(y) >=0 everywhere,
    A_t(H_t)=integral q_n^2 dw_t<0,
    L_t(H_t)<0.                                                  (7.1)

This is an existential finite-polynomial separator with a proved negative sign. No computed degree bound, efficient search method, or fixed universal polynomial q is asserted. Square positivity remains intact because F is not a sum of polynomial squares.

## 8. Consequences and exact boundaries

- The threshold of one hidden coordinate for automatic existence remains sharp even if a genuine initial joint moment record is imposed: k<=1 is covered by the accepted cumulative/one-hidden results, while k>=2 admits the present counterpath for every supplied schedule in the class.
- A positive-time joint representative and a zero-time representative are logically different hypotheses. The former can propagate under the separate law-persistence result; the latter alone cannot.
- The true tilt of mu_0 is a second full-square-positive hierarchy path with the same initial moments. It is representable at every time and therefore differs from this path at every positive time. Thus initial validity does not imply uniqueness even inside the full-square-positive solution class.
- For g=z^2 the genuine tilt and the escape path are coordinatewise C-infinity and have the same entire derivative jet at zero. The unnormalized difference is C^(-1)(beta_t-alpha_t) tensor N_k; every zero-time derivative of each active polynomial moment vanishes by (4.1). Division by the positive smooth normalizers preserves equality of all jets. This last observation is specific to the stated smooth autonomous example, not a smoothness claim for arbitrary merely continuous schedules.
- The initial record here is indeterminate. A theorem or counterexample assuming a determinate initial **joint** record is a separate question. The earlier determinate scalar initial counterexample kept only coordinate positivity and cannot be substituted for full-square positivity.
- No claim is made for energies that depend on the hidden variables, a changing controlled subspace, finite moment cutoffs, or a law-level initial-value problem in which the actual initial law and the measure evolution are already required.

## 9. Inheritance, verification and attribution

Read inputs were the accepted tensor-realizability, cumulative-square-positivity and active one-hidden results (including GENERAL_SOS_BRIDGE.md and SHARP_HIDDEN_BOUNDARY.md), the exact full-functional proof, and both earlier initial-validity and determinate-initial-positivity counterexamples. The current positive-time persistence candidate was read for its logical boundary, but is not used in this proof.

The full strictly positive nonmoment Lambda is inherited, with its existing Friedrich/Schmudgen attribution. Its original ordinary packet predates the separate full-functional-lean-20261010 package: that later package reports a complete trust-zero Lean proof of the actual full-polynomial linear functional, universal strict square positivity, normalization, and the globally positive polynomial with value -1. Its RESULT.md and retained LEAN_RECEIPT.json are separately hash-bound here. The measure-representation contradiction, signed-measure construction, and analytic hierarchy in this packet are ordinary mathematical arguments and are not claimed as Lean theorems. This work did not rerun that earlier kernel build.

The continuous/discrete lognormal pair is classical and already present in the earlier initial-validity packet; its complete moment calculation is reproduced here. Fourier uniqueness for finite signed measures is the only standard measure-identification input in the present argument.

The signed finite-difference measure construction is proved in full here; no literature-priority claim is attached to that elementary lemma. The project-relative new construction combines actual PSD domination by a genuine moment functional with the moment-equivalent active pair. It preserves every square inequality while changing representability immediately after time zero.

check_controls.py supplies exact finite arithmetic controls of the finite-difference identities, degree-by-degree corrections, summable-tail inequalities, witness value, initial-mixture algebra, and normalized hierarchy algebra. These controls supplement the ordinary all-degree/all-time proof; they do not establish the infinite theorem by sampling. Input hashes and frozen source copies document the inherited premise. Independent review remains required before any integration or acceptance claim.
