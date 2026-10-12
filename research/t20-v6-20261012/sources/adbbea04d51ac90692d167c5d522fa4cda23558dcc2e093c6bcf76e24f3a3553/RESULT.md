# Initial energy determinacy forces signed-polynomial moment continuation

10 October 2026 UTC. Additive ordinary mathematical research. The parent proposed the proof route and target; a participating subagent checked the route. Independent digest-bound review of this artifact is not claimed. No protected source changes, formal-kernel proof, empirical identification, field-priority claim, or T20 closure.

## 1. Result and the missing signed-control transport

The autonomous SOS restriction can be removed entirely if the initial law has bounded energy values. The proof also gives a materially wider version: determinacy of every polynomial-square-weighted initial energy distribution is enough, and one initial exponential absolute-energy moment ensures that condition. The initial joint support need not be compact. In particular, compact initial laws and finite initial supports admit **every fixed real polynomial energy**, including nonconstant signed linear energies that no scalar shift can make globally nonnegative.

Fix a finite dimension 1 <= d < infinity and a real polynomial h on R^d. Let 0 < T <= infinity. For every t in [0,T), let L_t be a real linear functional on R[x_1,...,x_d]. Assume:

1. L_t(1)=1, and t -> L_t(p) is coordinatewise C1, including continuity and the usual right-sided C1 interpretation at zero.
2. The autonomous hierarchy holds for every real polynomial p:

       L'_t(p) = -L_t(hp) + L_t(h)L_t(p).

3. Full square positivity holds at every time:

       L_t(q^2) >= 0 for every real polynomial q.

4. There is a Borel probability mu with all absolute polynomial moments such that L_0(p)=integral p dmu. For some finite M >= 0,

       |h(x)| <= M for mu-almost every x.

**Bounded-energy theorem.** Necessarily, for every polynomial p and 0 <= t < T,

       A_t(p) = integral p(x) exp(-t h(x)) dmu(x),
       L_t(p) = A_t(p)/Z(t),
       Z(t) = integral exp(-t h(x)) dmu(x) > 0,             (1)

where A is the uniquely fixed unnormalization defined below. Thus all records are represented by the displayed exact tilt. This gives the unique full-square-positive moment path from the given initial record, and it has a unique continuation to all finite forward times within this class.

The theorem does **not** assume a joint representing measure at any positive time. It does **not** assume h is lower bounded on R^d, SOS, shifted SOS, coercive, or bounded on all of R^d. No bound uniform over the unknown functionals L_t is imposed. The only initial growth assumption is bounded h-values under mu, besides the absolute polynomial moments.

**Weighted-energy-determinacy theorem.** In assumption 4, replace bounded |h| by the condition

       h_*(q^2 mu) is Hamburger determinate for every q in R[x].  (D)

This means uniqueness among all finite positive measures on R with that scalar moment record. The same exact formulas (1) are then forced on the whole supplied horizon. In particular, every integral of q^2 exp(-t h) under mu must be finite there. This is a conditional uniqueness and existence-obstruction theorem, **not** a universal global-existence assertion for unbounded energy. Conversely, (1) is an admissible smooth path on any [0,H) where all of these integrals are finite. Section 6 proves both directions precisely.

**Initial exponential-energy sufficient condition.** Condition (D) follows if, for some a>0,

       integral exp(a |h|) dmu < infinity.               (E)

This guarantees a nonzero forward existence interval, at least [0,a/2), while the actual maximal horizon can be larger or infinite. It includes a Gaussian initial law with signed linear h. For standard Gaussian data and h=-x^2 the exact maximal forward horizon is instead t<1/2, and no continuous full-square-positive hierarchy path can pass through t=1/2. Thus the extended theorem has a real horizon boundary.

**Compact-support corollary.** If mu has compact joint support K, the representing probability at each time is unique among all probabilities on R^d and is exactly exp(-t h)mu/Z(t), supported on K. Without a condition determining the joint law, bounded h alone does not guarantee this uniqueness; Section 8 gives a nontrivial signed-energy countercontrol.

**Piecewise-autonomous corollary.** If mu is compactly supported and h_t is any locally finite piecewise-constant-in-time family of real polynomials, a continuous, segmentwise coordinatewise C1, normalized, full-square-positive solution of the corresponding hierarchy is forced to be

       L_t(p) = integral p exp(-H_t) dmu / integral exp(-H_t) dmu,
       H_t(x) = integral_0^t h_s(x) ds.                    (2)

Each joint law is unique and stays on K. Here locally finite means finitely many switches on every compact time interval contained in the supplied horizon. Degrees and coefficients need no uniform bound across the entire horizon. This corollary covers the inherited finite-channel signed constant and locally finite piecewise-constant controls. It does not claim arbitrary continuous nonautonomous signed-polynomial schedules.

## 2. Unnormalization and scalar weighted energy records

Define

       a(t) = exp(-integral_0^t L_v(h) dv),
       A_t(p) = a(t)L_t(p).

The integrand is continuous on each compact time interval, so a(t)>0, a(0)=1, and A_t(1)=a(t). Product differentiation gives

       A'_t(p) = -A_t(hp).                                (3)

Induction over all polynomials at once bootstraps every coordinate to C-infinity in the interior and yields

       A_t^(n)(p) = (-1)^n A_t(h^n p).                    (4)

Only finitely many polynomial coordinates occur in each differentiation; no norm on the full moment sequence is used. Boundary continuity of every polynomial coordinate remains available. In fact the proof below only needs boundary continuity, interior C1, and the interior hierarchy, although the stated theorem retains the inherited C1 boundary convention.

Fix an arbitrary real polynomial q, without normalizing by its possibly zero square mass. Write

       f(t) = A_t(q^2),
       m_n(t) = A_t(q^2 h^n),
       B_t(r) = A_t(q^2 r(h)),       r in R[z].

Then B_t is a one-variable positive polynomial functional because

       B_t(r^2) = A_t((q r(h))^2) >= 0.                   (5)

In particular f>=0, f^(n)=(-1)^n m_n, and

       f^(2n)(t) = A_t((q h^n)^2) >= 0.                  (6)

This is the replacement for the lower-bounded/SOS argument. No sign for m_(2n+1) is asserted. The auxiliary measure constructed next lives on the scalar energy line and does not presuppose a representing joint law in R^d.

## 3. Symmetric Taylor bounds and interior analyticity

Let t-r,t+r lie in (0,T), with r>0. Taylor-expand f at t in both directions through degree 2N+1. The order-2N+2 integral remainder is nonnegative in both directions by (6). To see the backward sign explicitly, the integral from t to t-r has reversed orientation and its kernel (t-r-v)^(2N+1) is nonpositive, giving a nonnegative product. Adding the two expansions cancels all odd terms and proves

       sum_(k=0)^N r^(2k)m_(2k)(t)/(2k)!
          <= [f(t-r)+f(t+r)]/2.                          (7)

Every term on the left is nonnegative. In particular,

       m_(2n)(t) <= C(t,r)(2n)! r^(-2n),
       C(t,r) = [f(t-r)+f(t+r)]/2.                       (8)

Uniformity is important. Fix a closed interval J strictly inside (0,T), and choose r>0 so J+[-r,r] is still inside (0,T). Let C=max f on that enlarged compact interval. Then (8) holds at every v in J with the same C and r. Polynomial Cauchy-Schwarz for B_v gives

       |m_(2n+1)(v)|^2 <= m_(2n)(v)m_(2n+2)(v),

and hence, since sqrt((2n)!(2n+2)!) <= sqrt(2)(2n+1)!,

       |f^(k)(v)| <= sqrt(2) C k! r^(-k)                (9)

for every k>=0 and v in J. Taylor's remainder is bounded by

       sqrt(2) C (|delta|/r)^(N+1)

whenever the segment from v to v+delta lies in J. It tends to zero for |delta|<r. Therefore f is real analytic throughout (0,T). This conclusion follows from a uniform derivative estimate, rather than from a formal Taylor series or a pointwise bound alone.

## 4. One-dimensional measures and local signed tilt

By the classical Hamburger existence theorem, (5) gives a finite positive Borel measure sigma_t on R with

       integral z^n dsigma_t(z) = m_n(t),       n>=0.      (10)

The only external moment-existence input used here is one-dimensional. A primary author source is Konrad Schmuedgen, *Ten Lectures on the Moment Problem*, Theorem 1.12, printed pp. 14-15, https://arxiv.org/pdf/2008.12698 . Its Corollaries 2.3-2.4, printed p. 19, also give determinacy from the factorial/exponential estimates used here. No multivariate existence theorem is invoked.

For 0<b<r as in (8), monotone convergence applied to the nonnegative cosh series gives

       integral cosh(bz) dsigma_t
          = sum_(n>=0) b^(2n)m_(2n)(t)/(2n)!
          <= C(t,r)/(1-(b/r)^2).

Since exp(b|z|)<=2 cosh(bz), sigma_t has an exponential absolute moment at every rate b<r. These same estimates apply to any representing measure for (10), since its even moments are the same. Such a record is determinate. For example, the bilateral Laplace transform is analytic on a strip around the imaginary axis; the common moments identify its Taylor series near zero, the analytic identity theorem identifies it on that strip, and uniqueness of Fourier transforms of finite measures identifies the measures. Equivalently, (8) gives the classical Carleman condition.

Take interior u. For v sufficiently close to u, analyticity from (9) and absolute convergence supplied by an exponential moment of sigma_u yield

       f(v) = sum_(n>=0) (-1)^n m_n(u)(v-u)^n/n!
            = integral exp(-(v-u)z) dsigma_u(z).          (11)

There is an exponential margin left after choosing |v-u| sufficiently small. Thus (11) may be differentiated any finite number of times under the integral, giving every moment m_n(v). Consequently exp(-(v-u)z)sigma_u represents B_v, and determinacy proves the local measure identity

       sigma_v = exp(-(v-u)z) sigma_u.                   (12)

For completeness, the neighborhoods can be taken with a uniform positive radius on each compact positive-time interval: enlarge that interval to J, use the common r and C of Section 3, and take increments smaller than r/2, also keeping the connecting segments within J. A finite subdivision then composes (12) from any u>0 to any v>0 in the supplied horizon. Multiplication of the positive density factors gives

       sigma_v = exp(-(v-u)z) sigma_u
       for all u,v in (0,T).                            (13)

Integrability at a distant time is obtained by these finite local transitions. It is not assumed from the initial local exponential radius or from a global bound on h.

There is no exceptional zero-mass problem. If m_0(t)=0, positivity gives |B_t(z^n)|^2<=B_t(1)B_t(z^(2n))=0, so B_t is zero and sigma_t is the zero measure. Every equality above remains valid without division by m_0. Equation (13) then forces all the scalar measures in this q-family to be zero.

## 5. Recovering the boundary scalar measure without losing mass

Fix s in (0,T). For 0<u<=s, (13) says

       sigma_u = exp((s-u)z) sigma_s.                    (14)

Define the a priori possibly infinite measure

       tau_q = exp(sz) sigma_s.

For an even degree 2n, split the integral of z^(2n) in (14) into z>=0 and z<0. As u decreases to zero, the nonnegative integrand on z>=0 increases, so monotone convergence applies. On z<0, its absolute value is at most |z|^(2n), integrable against sigma_s, so dominated convergence applies. Coordinate continuity at zero then gives

       integral z^(2n) dtau_q
          = lim_(u down to 0) m_(2n)(u)
          = A_0(q^2 h^(2n)) < infinity.                 (15)

The n=0 case includes the total mass, so there is no unexplained loss of mass at the boundary. All absolute polynomial moments of tau_q are finite by (15).

For an odd degree, the same limit is justified by domination. On z>=0 use |z|^k exp(sz), integrable against sigma_s by (15) and |z|^k<=1+|z|^(2k). On z<0 use |z|^k, integrable against sigma_s. Thus for every n>=0,

       integral z^n dtau_q = A_0(q^2 h^n)
                           = integral q^2 h^n dmu.       (16)

This step uses neither a joint positive-time measure nor prior compact support of sigma_s. Signed energy is handled by the explicit two-half-line split.

### Null-ideal persistence needs no initial joint law

Sections 2-5 through the first equality in (16) do not actually require any initial representing mu or any initial determinacy. They work for an arbitrary normalized full-square-positive polynomial-functional path with the autonomous hierarchy and boundary continuity.

If L_0(q^2)=0, the recovered positive scalar boundary measure tau_q has total mass A_0(q^2)=0. Thus tau_q=0. Since exp(sz)>0, sigma_s=0, and (13) gives A_t(q^2)=0 for every t>0. Dividing by a(t)>0 proves

       L_0(q^2)=0  implies  L_t(q^2)=0 for every t.       (N)

Polynomial Cauchy-Schwarz then gives L_t(qr)=0 for every polynomial r. In particular the initial null ideal I_0={q:L_0(q^2)=0} remains null at every time. It is an ideal: for q in I_0, apply this Cauchy-Schwarz identity at zero with r replaced by q r^2 to obtain L_0((qr)^2)=0.

Thus polynomial algebraic support equations persist whenever a representing law is present. Without further hypotheses this statement does not manufacture a joint law, establish any non-null support inequality, or imply joint determinacy. This is a bounded consequence of the same boundary recovery, not a substitute for the initial conditions in the forcing theorems.

## 6. Initial energy determinacy identifies every square observable

Let nu_q be the finite positive scalar pushforward h_*(q^2 mu). Equation (16) says tau_q and nu_q have the same moments. Under condition (D), this immediately forces equality, including when their common mass is zero. Nothing in Sections 2-5 used boundedness of h under mu.

In the bounded-energy case, nu_q is supported on [-M,M], so (D) follows by an elementary argument that avoids a hidden support assumption on tau_q. Let c=integral q^2 dmu. For R>M and n>=1,

       tau_q({|z|>=R}) <= R^(-2n) integral z^(2n) dtau_q
                       <= c (M/R)^(2n).

Letting n increase forces that mass to zero. A countable exhaustion gives support in [-M,M]. If M=0 the same argument with any R>0 works; if c=0 both measures are zero by their masses. Uniform polynomial approximation on [-M,M] identifies the two finite measures. Hence

       tau_q = h_*(q^2 mu).                              (17)

Combining (13), the definition of tau_q, and (17), for all t>0,

       A_t(q^2) = sigma_t(R)
                = integral exp(-tz) dtau_q(z)
                = integral q(x)^2 exp(-t h(x)) dmu(x).   (18)

The formula already holds at zero. Apply the identity

       p = [(p+1)^2-(p-1)^2]/4

to obtain the same unnormalized formula for every signed polynomial observable p. Each square integral in (18) is finite because it equals the given finite coordinate A_t(q^2). Thus every polynomial observable is absolutely integrable, by |p|<=(1+p^2)/2. Taking p=1 gives a(t)=Z(t); division by this positive number proves (1). This proves the forcing part of the general weighted-energy-determinacy theorem, including the necessary integrability across its entire supplied horizon.

### The converse and the exact forward domain

Suppose for every 0<=t<H and every real polynomial q that

       integral q^2 exp(-t h) dmu < infinity.             (19)

Then all absolute polynomial moments of the finite tilted measure exist. Its mass is strictly positive. Fix an interior t, choose times t_-<t<t_+ inside [0,H), and split by h>=0 or h<0. On a small neighborhood of t,

       |p| |h|^n exp(-v h)
          <= |p| |h|^n [exp(-t_- h)+exp(-t_+ h)].

The right side is integrable by (19), since |p| |h|^n is bounded by a sum of polynomial squares. Dominated differentiation proves every interior derivative of the unnormalized coordinates. At t=0, for 0<=v<=delta<H, the same domination uses the endpoints 0 and delta. The one-sided derivative formulas and their continuity follow as well. Thus (1) is a coordinatewise C-infinity normalized square-positive hierarchy path on [0,H).

Under (D), existence on a specified [0,H) is therefore equivalent to (19), and the path is unique. Equivalently, its maximal open forward horizon is

       T_mu = sup { H>0 : (19) holds for every t in [0,H) },

with supremum zero if the set is empty. The integrability domain is an interval: on h>=0 the forward factor is bounded by one, while on h<0 it increases in t. If T_mu>0, the unique path exists on [0,T_mu). Endpoint inclusion and passage beyond that endpoint require their own integrability and continuity; they are not inferred. If a continuous admissible path passed into a larger open horizon, the forcing theorem would contradict the definition of T_mu.

### Why one exponential energy moment suffices

Assume (E). Since every polynomial moment of mu exists, Cauchy-Schwarz gives

       integral q^2 exp((a/2)|h|) dmu
          <= (integral q^4 dmu)^(1/2)
             (integral exp(a|h|) dmu)^(1/2) < infinity.

Hence nu_q has an exponential absolute moment, so it is Hamburger determinate by the classical scalar criterion already used in Section 4. Thus (D) holds for every q. The same estimate proves (19) for 0<=t<a/2, supplying the stated nonzero existence interval. This sufficient interval is not asserted sharp.

### Global continuation under bounded energy

Conversely, bounded |h| under mu gives exp(-Mt)<=Z(t)<=exp(Mt) for t>=0, and |p|exp(-t h) and all their time derivatives are locally dominated by a constant times |p|. Therefore the displayed formula is a normalized square-positive C-infinity solution for every finite t>=0. It agrees with any supplied path on its horizon. This proves existence, uniqueness of the moment path, and unique global forward continuation.

Both forcing theorems are about the initial **record** as well as the chosen representative mu. If another initial law nu has the same polynomial moments, h_*(q^2 nu) has the same moments as h_*(q^2 mu), so (D) identifies those scalar measures. All their tilted square integrals and therefore their exact moment paths and forward moment horizons agree. In the bounded case the q=1 even-moment estimate additionally gives |h|<=M nu-almost surely. None of these facts identifies the joint law nu with mu.

## 7. Compact support, switches, and the inherited finite channel

### Joint-law uniqueness from compact initial support

The law in (1) stays on K. Choose R>=1 with K contained in [-R,R]^d. Any other probability rho having its full moments satisfies

       rho({|x_i|>=R+epsilon})
          <= (R/(R+epsilon))^(2n)

for every coordinate i, epsilon>0 and n>=1. Thus rho is also supported in the bounding box. Polynomials are uniformly dense in continuous functions there and identify rho with the displayed tilt. This establishes uniqueness on all of R^d, rather than only among measures already assumed to stay on K.

### Locally finite switching

Let 0=tau_0<tau_1<... be the switch times, locally finite in [0,T). On [tau_j,tau_(j+1)), the polynomial h_j is fixed. On the first interval the main theorem applies since h_0 is bounded on compact K. At the next switch, moment continuity identifies the initial record for the next segment with the limiting tilted law on K. Its probability and all moments are well defined, and h_1 is bounded on K. Apply the main theorem again with time reset to tau_1. Induction handles every finite number of switches; local finiteness handles every t<T. The successive exponential factors multiply to exp(-H_t), proving (2).

At switch times the hierarchy is interpreted with the appropriate one-sided derivatives; global C1 across a genuine jump of h is unnecessary. The path is continuous, segmentwise C1, and satisfies the integrated equation. No claim about a limit at a switch-accumulation endpoint or an unspecified continuation of the schedule is being made.

### Actual inherited signed-control interface

For the inherited finite stochastic channel, the numerical support consists of the distinct column vectors kappa_j, and h_t(x)=g(t) dot x for arbitrary real piecewise-constant covectors g. This is exactly the allowed class above. Every compact initial finite-channel law therefore forces the unique tilt

       w_j(t) = w_j(0) exp(-U(t) dot kappa_j) / Z(t),
       U(t) = integral_0^t g(s) ds,

from the full hierarchy and full square positivity alone. Future support preservation no longer has to be assumed separately. The tensor record is sum_j w_j(t) kappa_j^(tensor r). The inherited interpolation, closure bounds, duplicate-column aggregation, and control distinguishability results are not reproved or enlarged here. The new implication is that this formally larger full-positive moment-hierarchy class cannot escape the compact initial law's exact support and continuation under those signed controls.

The argument still concerns commutative polynomials and symmetric moments of a fixed finite-dimensional numerical state. It gives no identification of ordered semantic tensors, hidden fine labels within a duplicate-column class, or empirical source validity.

## 8. Discriminating controls and limitations

### 8.1 A genuinely signed finite-channel control

Take the three channel columns

       kappa_0=(0,1),  kappa_1=(1/2,1/2),  kappa_2=(1,0),

with weights (1/2,1/3,1/6). Let g=(1,-1), so h(x,y)=x-y has support values (-1,0,1). For t>=0 the unnormalized atomic weights are

       (exp(t)/2, 1/3, exp(-t)/6).

At t=log(2), the normalizer is 17/12 and the normalized weights are (12/17,4/17,1/17), with coordinate means (3/17,14/17). The expected energy is -11/17.

For any constant c, h+c takes arbitrarily negative values on R^2, so no constant shift makes it SOS. Moreover the unnormalized square mass of q=1-x grows initially at rate 1/2, so the predecessor's decreasing-square domination is unavailable. The current theorem nevertheless forces the exact law.

The controls also check the same atoms under the genuinely nonlinear signed polynomial h(x,y)=x^3-3y, with values (-3,-11/8,1), and signed switching from g=(1,-1) for time log(2) to -g for time log(3). The net integrated control is g log(2/3), and the final weights are (4/11,4/11,3/11). All calculations are exact.

### 8.2 Bounded energy does not guarantee a unique hidden joint law

Let X take -1 and 1 with equal probabilities, and let Y be independent of X. Let nu_+ and nu_- on (0,infinity) have densities

       f(y)[1 +/- (1/2) sin(2 pi log y)],
       f(y)=exp(-(log y)^2/2)/(y sqrt(2 pi)).

These are distinct positive probabilities with the same moments E[Y^n]=exp(n^2/2). The integer cancellation is

       E[Y^n sin(2 pi log Y)]
          = exp(n^2/2-2 pi^2) sin(2 pi n) = 0.

Take mu_+ and mu_- to be the product laws of (X,Y), and choose h(x,y)=x. Thus |h|=1 under both laws, although h is globally unbounded below. Under the exact tilt the Y-law is unchanged, the normalizer is cosh(t), and

       E_t[X]=-tanh(t),
       E_t[X^a Y^b]=exp(b^2/2) times
          1 if a is even, or -tanh(t) if a is odd.

Their complete mixed-moment paths are identical and evolve nontrivially. Their joint laws remain distinct for every t, because their Y-marginals remain distinct. This is the inherited lognormal ambiguity adapted to the present bounded signed energy, not a newly claimed Stieltjes-class construction. It shows why moment-path uniqueness cannot be reported as general hidden-law uniqueness.

In particular, neither global compact joint support nor future full joint determinacy follows merely from |h| bounded under the initial law. Particular h may impose compactness: for example, a nonconstant univariate polynomial has compact {|h|<=M}. The countercontrol is a genuinely multidimensional hidden-direction example.

### 8.3 Square positivity is indispensable, even for compact delta data

For h(x)=x, put F(0)=0, F(t)=exp(-1/t) for t>0 and b(t)=1-F(t)/2. Define

       A_t(x^n)=(-1)^n b^(n)(t),   L_t(x^n)=A_t(x^n)/b(t).

This normalized coordinatewise smooth path satisfies the signed-linear hierarchy and initially matches delta_0, so its initial energy is bounded by zero. However

       A_t(x^2)=b''(t)=exp(-1/t)(2t-1)/(2t^4)<0
       when 0<t<1/2.

It violates the square test q=x. At t=1/4 the unnormalized value is exactly -64 exp(-4). Thus initial compactness and the hierarchy do not supply the all-time square-positivity premise. This is a signed-linear adaptation of the inherited flat-function countercontrol.

### 8.4 Unbounded Gaussian energies: extension and maximal horizon

Let mu be the standard normal law on R. For h(x)=x, condition (E) holds for every a>0. Completing the square gives Z(t)=exp(t^2/2) and the tilted law N(-t,1). Thus the theorem forces the full moment path globally even though h is unbounded under the initial law. Its moments are

       m_n(t)=sum_(k=0)^(floor(n/2))
          n! (-t)^(n-2k) / [2^k k! (n-2k)!].

For the same initial law with h(x)=-x^2, condition (E) holds for 0<a<1/2, so all the weighted energy distributions are determinate. But the tilted density has Gaussian exponent -(1/2-t)x^2. Consequently

       Z(t)=(1-2t)^(-1/2),
       m_(2n)(t)=(2n-1)!! (1-2t)^(-n),
       m_(2n+1)(t)=0,                 0<=t<1/2.

At t=1/2 the unnormalized density is constant on R and has infinite mass. Also m_2(t) tends to infinity as t increases to 1/2. The forcing theorem and coordinate continuity therefore rule out **any** full-square-positive normalized hierarchy path from these data that includes and passes through t=1/2. Here the exact maximal open forward horizon is T_mu=1/2. This is an actual nonexistence conclusion for the formal positive hierarchy, not merely a failure of one proposed integral formula.

### 8.5 Bounded energy is sufficient but not necessary for a global horizon

The theorem is not a universal global-existence statement for every initial law under signed h. The inherited example h(x)=x with mu({-n})=2^(-n-1), n>=0, has

       Z(t)=1/(2-exp(t)),     E_t[X]=-exp(t)/(2-exp(t)),

only for 0<=t<log(2). It has all polynomial moments and a genuine square-positive tilt on that horizon, but the mean diverges at the endpoint. Its initial h-values are unbounded. The bounded-energy global corollary excludes this case; the more general theorem covers its finite horizon without extending it through its blow-up.

Likewise, the retained lognormal same-initial-moment examples and valid-initial noncompact escape results prohibit replacing the weighted-energy condition by initial representability alone. Bounded energy is one strong sufficient condition, not a necessary one. No conclusion is made that an arbitrary unbounded jointly determinate initial law necessarily satisfies (D).

### 8.6 Complete inputs, not finite surrogates

The proof uses every q-square test and arbitrary energy degree, followed by moment determinacy. A finite list of positive moment matrices is not the premise. A scalar unweighted energy record alone is not the complete q^2-weighted family used to recover all polynomial observables. No finite-cutoff validity test, effective reconstruction algorithm, conditioning bound, or new tensor compression bound is asserted.

## 9. Ancestry and verification status

The retained files listed in INPUT_BINDINGS.json are copied and hashed; they are not edited.

- The compact-initial preservation result owns the time-dependent SOS square-order domination theorem. Its independent review correctly excludes arbitrary signed linear controls. The present result closes that **autonomous and locally finite piecewise-autonomous** missing interface, using energy-line measures instead of monotone square-order domination.
- The tensor realizability extension owns lower-bounded-energy exhaustion from actual joint laws, coercive classification, weighted-square methods, and quadratic square-positivity upgrades. This result neither repeats that general exhaustion theorem nor assumes its joint representation premise. Its distinct trade is initial weighted-energy determinacy (in particular bounded or exponentially integrable energy) in exchange for arbitrary autonomous signed h and only full square positivity at later times.
- The finite-channel tensor continuation result owns the exact signed-control tilt, finite interpolation/closure, and duplicate-column semantics. Here those laws are forced from a larger abstract hierarchy class under the added full-square-positivity promise.
- The classical one-dimensional Hamburger and determinacy results, polynomial Cauchy-Schwarz, Taylor's theorem, measure convergence theorems, and compact polynomial density are standard analysis inputs. Their use here is an ordinary proof, not a claim of mathematical field novelty.

The bilateral Laplace representation mechanism is also classical. Buescu and Paixao, *Positive-definiteness and integral representations for special functions*, https://arxiv.org/html/1801.09537 , Section 3 (Definition 3.4, Theorem 3.5, Corollary 3.6) credits Bernstein and Widder for continuous exponential convexity and bilateral Laplace representation; Section 6 treats exponential weighting, moments, and analyticity. Those statements and attributions were directly inspected. The paper says its main proofs are omitted. Its original Widder reference is *Bull. Amer. Math. Soc.* 40 (1934), 321-326; the publisher access attempt was blocked, so no inspection of that original proof is claimed. Our derivation above is explicit and does not rely on acquiring it. The project-relative content is the passage from the formal positive hierarchy to scalar measures, boundary recovery, and full polynomial-coordinate reconstruction under the stated initial energy condition.

The participating proof-route check is separate from the author artifact and must not be described as independent digest-bound review of this file. A later independent review, if commissioned, should bind the final bytes and replay the controls separately.

check_controls.py runs exact symbolic and rational checks for signed finite-channel and nonlinear hierarchy identities, square positivity as a symbolic weighted sum of atom-value squares, local tilt composition and inversion, zero square mass, compact weighted-energy pushforwards, switching, constant-shift invariance, the symmetric Taylor parity/remainder formula, the odd-moment factorial constant, the bounded-energy hidden-law control, the compact-data flat violation, Gaussian linear forcing and negative-quadratic maximal horizon, the geometric blow-up boundary, and all retained input hashes. These finite controls supplement the universal proof; they do not prove the theorem by sampling.

