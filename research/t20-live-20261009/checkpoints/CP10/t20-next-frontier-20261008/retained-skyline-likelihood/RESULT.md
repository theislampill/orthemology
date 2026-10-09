# Exact retained-skyline likelihood, with singular and common-support information separated

8 October 2026 UTC. New scratch-only sibling; frozen predecessors are unchanged. This is a conditional mathematical observation-channel result. It does not validate physical access, perform an empirical experiment, integrate protected changes, or close T20.

## 1. What the ideal oracle observes

There are N iid threshold pairs Z_j=(X_j,Y_j) in the open unit square, with joint probability law μ absolutely continuous with density f. A retained endpoint query (a,b) returns

    h(a,b)=1{some j has X_j≤a and Y_j≤b}.

The same vector is retained, responses are separately read and nonlatched, and commands do not redraw or mutate the vector. These are the inherited interior-replay assumptions, not consequences of a likelihood calculation.

The observed object is exactly the coordinatewise-minimal/Pareto antichain S of the sample. Each nonminimal point dominates some minimal point, so

    {h=1}=D(S)=union_(z in S) [z_x,1]×[z_y,1].                 (1)

Conversely the minimal points of this upper-closed set recover S. Almost surely there are no ties in either coordinate. Write its k points in the unique order

    0<x_1<...<x_k<1,  1>y_1>...>y_k>0.                       (2)

The full oracle and S are mutually deterministic mathematical readouts. Countably many rational queries suffice to determine the closed set (1) and then its finite minimal antichain: rational hit points are dense in each nondegenerate upper rectangle. This is not a finite procedure for recovering arbitrary real coordinates exactly.

K=|S| is the minimal number of upper rectangles needed to represent this endpoint map. It is not the actual route count N. Arbitrarily many dominated additions leave the whole endpoint map unchanged. Inferences about N from the distribution of S use the extra iid and family assumptions. With boundary atoms or coordinate ties, (2) and the density below must be replaced by an appropriate mixed/tied formulation; none are silently included here.

## 2. Density, reference measure, normalization, and hidden routes

Let Ω_k be the open 2k-dimensional region in (2), equipped with ordinary product Lebesgue measure dx_1 dy_1 ... dx_k dy_k, restricted to Ω_k. Use counting measure over k and this measure within each stratum. For 1≤k≤N the skyline density is

    g_(N,μ),k(s)=(N)_k product_i f(x_i,y_i) μ(D(s))^(N−k),   (3)
    (N)_k=N!/(N−k)!.

It is zero for k>N. There is no additional k! divisor on this x-ordered parameter space.

Proof. Choose, in order, the k distinct sample labels that occupy the ordered skyline positions. There are (N)_k choices. Their density is the product in (3). Every remaining route must be in D(s), and this is sufficient: such a route cannot introduce a new minimum, while points in s are incomparable. Necessity follows by descending a finite chain from any nonminimal sample point to a minimal one. Independence supplies μ(D)^(N−k). These label choices partition the full-probability set of tie-free labeled configurations. Integrating (3), summing over k, therefore gives exactly 1. This is a proof of normalization, not an inference from quadrature.

The same factorization gives the regular conditional latent law. Given a skyline s with positive density and k<N, its ordered k labels are uniform over the (N)_k injections. Given those labels, the remaining labeled routes are independent with law

    μ_s(A)=μ(A∩D(s))/μ(D(s)).                               (4)

Thus the invisible routes are iid draws truncated to the dominated region, not additional observed points or unconstrained iid draws. The conditional assertion is a regular-conditional-density statement; it does not assign positive probability to one exact continuous skyline.

Boundary cases:

- N=1: K=1 and g=f; there are no hidden routes.
- k=N: the factor μ(D)^0 is defined as 1, even if μ(D)=0; the hidden-vector conditional law is the unique law on an empty vector.
- k<N and μ(D)=0: the stratum density is zero there; no truncated law is required at a zero-probability conditioning point.
- N=0, if separately allowed, has one empty skyline with probability 1. It is not part of the n≥1 hard pair.
- For the positive interior densities used below, μ(D)>0 for every s∈Ω_k, so the exceptional zero-mass case does not arise.

For product-uniform routes, ordering the sample by X makes Y an iid continuous sequence. K counts successive lower records. Its probability generating function is

    E[z^K]=z(z+1)...(z+N−1)/N!.                              (5)

One derivation uses the uniform random relative-rank insertion at each position: these ranks are independent, and the jth position is a new lower record with probability 1/j. Hence P(K=k) is the unsigned first-kind Stirling number divided by N!, P(K=1)=1/N, P(K=N)=1/N!, and E K=H_N. At N=2 the two stratum masses are 1/2 and 1/2; at N=3 they are 1/3,1/2,1/6. These are independent analytic normalization checks for (3).

## 3. Joe specialization and numerically stable dominated mass

The inherited pair has P0: N=n uniform routes, and P1: N=m=n+1 routes with c=n/m and

    F_c(x,y)=1−(1−xy)^c,
    f_c(x,y)=c(1−xy)^(c−2)(1−cxy)>0.                       (6)

Write D_0(s) and D_c(s) for the dominated-region masses under these route laws. Put x_(k+1)=1. Disjoint vertical strips give the exact finite formulas

    D_0=Σ_(i=1)^k (x_(i+1)−x_i)(1−y_i),                    (7)
    D_c=Σ_(i=1)^k [(1−x_i)^c−(1−x_(i+1))^c
                       +(1−x_(i+1)y_i)^c−(1−x_i y_i)^c].  (8)

The four terms in each Joe strip are its CDF rectangle increment. A direct floating-point evaluation can lose accuracy when they nearly cancel. A positive strip representation avoids that cancellation. For a=x_i, b=x_(i+1), y=y_i,

    strip_c(a,b;y)
      =∫_a^b c(1−t)^(c−1)
          [1−y ((1−t)/(1−ty))^(1−c)] dt.                  (9)

The bracket is nonnegative. Its stable evaluation for 0<y<1, t<1 uses

    −expm1(log y+(1−c)[log1p(−t)−log1p(−ty)]).

The substitution v=(1−t)^c removes the endpoint power singularity and gives a bounded integrand:

    strip_c(a,b;y)
      =∫_((1−b)^c)^((1−a)^c)
          [1−y {v^(1/c)/(1−y+y v^(1/c))}^(1−c)] dv.        (10)

For c<1 and y<1 its limiting value at v=0 is 1; throughout the interval it lies in [0,1]. At c=1 use the exact simplification (b−a)(1−y). At y=0 the bracket is 1; at y=1 the whole strip is zero. These endpoint conventions avoid 0^0 ambiguities. If the integration interval is tiny, compute its positive width by a log1p/expm1 power difference and rescale to [0,1]. Formula (10) supplies a stable positive-integrand alternative, not a certified numerical-error guarantee.

Likewise F_c can be computed as −expm1(c log1p(−xy)) and

    log f_c=log c+(c−2)log1p(−xy)+log1p(−cxy).

For 1≤k≤n, the exact likelihood ratio on the common strata is

    L_k(s)=g_1,k(s)/g_0,k(s)
          ={m/(m−k)} product_i f_c(x_i,y_i)
               D_c(s)^(m−k)/D_0(s)^(n−k).                 (11)

For k=m, g_0,m=0 and g_1,m=m! product_i f_c(x_i,y_i). The equality control c=1 with the SAME sample size in both laws gives identical density (3); setting c=1 but leaving different route counts does not.

## 4. Exactly where support separation lives, and how rare it is

Let Q0,Q1 be the two skyline laws, A={K≤n}, B={K=m}, and

    p_n=Q1(B)>0.                                           (12)

All densities are strictly positive on their allowed Ω_k. Consequently B is the entire singular component of Q1 relative to Q0, and Q1 restricted to A and Q0 are mutually absolutely continuous. There is no further singular set hidden within a common stratum. In particular KL(Q1||Q0)=infinity comes entirely from B.

The predecessor's fixed staircase certificate is a subset of B in this m-route world: its incompatible positive hits require at least m minimal routes, not merely m possibly invisible labels. Conversely any strictly interior m-point skyline admits a sufficiently close rational staircase panel with all positive hits and all connector misses. Distinct x and y gaps let one place those finitely many rational sites without crossing a skyline step. Therefore B is, up to null boundary configurations, the countable union of these rational-panel certificate events. One fixed panel can be much rarer than the full-oracle support event B.

Nevertheless even the full event has a factorial upper bound:

    0<p_n<1/m!  for the hard pair n≥1.                       (13)

Here is a direct proof rather than an assumed copula property. With t=xy,

    ∂²_xy log f_c=(2−c)/(1−t)^2−c/(1−ct)^2>0,              (14)

because 0<c<1, 2−c>c and 1−t≤1−ct. Integrating (14) over any nondegenerate rectangle gives the strict TP2 inequality. Fix increasing ordered x coordinates and increasing ordered y coordinates. For each of the m! assignments of y ranks to x positions, the joint product density is product_i f_c(x_i,y_(π(i))). Whenever two positions are concordantly paired, reversing that pair strictly decreases this product by TP2. Successive swaps reach the fully reversed permutation, so it has the smallest product, strictly below the average of all m! products. Conditional on these ordered marginal coordinates, assignment probabilities are proportional to these products. All m points are minimal exactly for the fully reversed permutation. Its conditional probability is therefore <1/m!; integration proves (13). Positivity follows by integrating the positive density over any nonempty open antichain region.

This proof also shows the non-strict ≤1/m! bound at c=1, with equality there. It does not assume independence of X and Y ranks under the Joe law.

A strategy that merely waits for B on independent retained vectors has mean 1/p_n>m! under P1, and never terminates under P0. Fixed-budget support-only testing has P1 miss probability (1−p_n)^T after T vectors. This is a bound on that support-only strategy. It is not a lower bound on all skyline tests, because the common-support likelihood (11) also contains information.

For equal priors the exact one-vector optimal error is expressible without conflating these sources:

    error* = (1/2) Σ_(k=1)^n ∫_(Ω_k) min(g_0,k,g_1,k),
    TV(Q1,Q0) = (1/2)[p_n+Σ_(k=1)^n∫|g_1,k−g_0,k|].        (15)

These identities characterize the experiment; they do not evaluate its asymptotic rate.

## 5. Ordinary likelihood information survives removal of the support certificate

Define the normalized common-support alternative

    Q1^A=Q1(·|A),  dQ1^A/dQ0=L/(1−p_n).                   (16)

For each fixed n,

    0<KL(Q1^A||Q0)<infinity,
    0<KL(Q0||Q1^A)<infinity.                               (17)

This is a scoped typical-information statement: conditioning removes the entire singular certificate, while an ordinary finite likelihood distinction remains. It does not assert a typical-set concentration theorem or the size of these divergences as n varies.

Finiteness proof. In the open square, (6) implies

    f_c≥c,
    log^+ f_c≤(2−c)[−log(1−x)],
    D_c≥c D_0.                                             (18)

For the first inequality use 1−cxy≥1−xy and (1−xy)^(c−1)≥1. For the second omit log c and log(1−cxy), both nonpositive, and use 1−xy≥1−x. For any nonempty skyline, D_0 is at least the area (1−x_i)(1−y_i) of one of its rectangles. Thus −log D_0 is bounded by the sum of −log(1−X_j)−log(1−Y_j) over all underlying routes. The Joe margins satisfy E[−log(1−X)]=E[−log(1−Y)]=1/c, and uniform margins have expectation 1.

Taking logs in (11), dropping its nonpositive (m−k)log D_c term, and applying (18) bounds log^+ L by a constant plus finite multiples of these routewise logarithms. Its Q1 expectation on A is finite and remains finite after division by 1−p_n>0. In the reverse direction, −log f_c≤−log c and −log D_c≤−log c−log D_0 give a finite Q0 expectation for log^+(1/L). Normalization in (16) adds only a finite constant. For either probability density ratio R, the negative part of its KL integrand is integrable by −R log R≤1/e on R<1. Hence both KL integrals are finite.

Strictness proof, valid even n=1. On the k=1 stratum write the lone point as (x,y). Then D_0=(1−x)(1−y) and D_c=(1−x)^c+(1−y)^c−(1−xy)^c. As x,y both decrease to zero, (11) tends to (m/n)c=1. In contrast, hold y in a compact subinterval of (0,1) and let ε=1−x decrease to zero. Here f_c tends to a finite strictly positive value,

    D_c=ε^c+O(ε),
    L_1=constant(y) ε^(cn−(n−1))(1+o(1))
       =constant(y) ε^(1/m)(1+o(1)) →0.                   (19)

Thus L is not constant on the common stratum. The continuous densities make this a genuine positive-measure distinction, not merely a comparison at null points. Since equality in either probability-law KL holds exactly for equal laws, (17) follows. In particular, at n=1 the conditional K itself is identically 1 under both laws, yet the single visible skyline point's coordinates still discriminate them.

The companion count-information analysis owns the separate exact mean gap, variance analysis, and any consequent testing bound. The likelihood result does not infer a rate from (17), from infinite unconditioned KL, or from a first moment alone.

## 6. Exact low-n checks and deterministic quadrature

At n=1, m=2,c=1/2 the two skyline strata have exact probabilities

    Q1(K=1)=3/2−π²/12=0.67753296657588678...,
    Q1(K=2)=π²/12−1/2=0.32246703342411322....                (20)

Derivation: K=1 means one point dominates the other, so its mass is 2∫ f_c D_c. Since continuous margins give E F_X(X)=E F_Y(Y)=1/2, E D_c=E F_c. For c=1/2,

    E F_c=1−(1/4)∫_[0,1]² [1+1/(1−xy)] dxdy
         =3/4−π²/24.

The last integral uses the nonnegative geometric series and Σ_(j≥1)j^−2=π²/6. Alternatively K=2 has mass 2∫f_c[F_Y(y)−F_c(x,y)], giving the complementary expression directly. These calculations verify the ordered factor 2 and normalization without four-dimensional numerical approximation. Conditional on K=1, the skyline density is exactly 2 f_c D_c divided by the first number in (20).

A conditional-hidden-route check is also exact: for uniform N=2 and skyline (1/4,1/3), D=[1/4,1]×[1/3,1] has mass 1/2. The remaining labeled point, after specifying the skyline label, is uniform on D; its probability of lying in [1/2,1]² is (1/4)/(1/2)=1/2. This is a direct instance of (4).

checks.py and CONTROL_RESULTS.json contain deterministic checks only:

- Tensor Gauss–Legendre integration of (3) on k=1 and k=2 strata, with explicit ordered-coordinate transformations and Jacobians, at orders 12,24,48.
- Uniform N=1,2,3 masses agree with their analytic values to floating-point rounding. N=3's k=3 value is provided analytically by (5), not claimed as a computed six-dimensional integral.
- Direct Joe n=1 quadrature converges slowly near the corner singularity. At order 48 it gives 0.6775810270 and 0.3224857329, whose sum is about 1.0000667599, not exactly one. This visible quadrature error is retained rather than hidden or used as proof. The analytic normalization and (20) are authoritative.
- Independent 65-digit one-dimensional product-integral evaluation agrees with (20) to the displayed precision. This numerical agreement is not a rigorous interval error certificate.
- Closed strip formula (8), positive improper integral (9), and bounded transformed integral (10) are compared at deterministic skyline points, including the c=1 control.
- The parent-supplied and independently checked count mean formula is numerically checked as a cross-packet control; the companion count packet owns its proof and use. No random sample, fitted asymptotic, or empirical success rate is reported.

## 7. What this settles and what stays open

Settled for the declared iid retained-threshold model: the observable is a skyline, the proposed density (3) is normalized with the stated ordered measure, invisible routes have conditional law (4), dominated mass has exact/stable strip descriptions, and support-only evidence can be separated exactly from common-support likelihood information. The full-oracle singular event is factorially rare as n grows; the conditioned common-support laws nevertheless differ and have finite mutual KL.

Not settled by this packet: sharp skyline KL/TV/Hellinger asymptotics, optimal testing performance, a practical precision/noise/probe-cost model, finite exact reconstruction of real thresholds, distribution-free actual-count identification, or physical route semantics. A finite-grid approximate reconstruction proposal is a separate frontier and is not used here. Any ideal-oracle sample bound in a companion result must not be silently promoted to a finite-probe or total-probe bound.

Attribution: the parent supplied the candidate skyline density, the three predecessor sources, the oracle guards, and the count-mean candidate. This packet verifies the density/conditional law and derives the stable strip, singular/common-support, factorial rarity, and finite conditional-KL results. The count worker separately owns its count/variance/testing result. The methods are standard order-statistic conditioning, Pareto minima, TP2 rearrangement, and elementary likelihood analysis; no field-wide novelty is claimed. These are written proofs with executable deterministic controls, not newly kernel-checked Lean theorems. Independent review must be bound to the final file hash before acceptance.
