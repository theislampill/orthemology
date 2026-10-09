# Full retained-skyline reverse KL: a log-squared upper bound

8 October 2026 UTC. Separate scratch-only strengthening. The log-four packet and all frozen predecessors remain unchanged. Historical floor remains **UNVERIFIED**. This is a written mathematical proof pending its own independent digest-bound review, not protected integration, audit closure, a kernel proof, an empirical experiment, or physical-access certification.

## Result and scope

Let n≥1, m=n+1, c=n/m. In world 0, one retained vector consists of n iid uniform points in the open unit square. In world 1 it consists of m iid points with

    F_c(x,y)=1−(1−xy)^c,
    f_c(x,y)=c(1−xy)^(c−2)(1−cxy).

Let S be the complete coordinatewise-minimal skyline, K its cardinality, E its lower undominated region, U=area(E), and D=1−U. Write Q0,Q1 for the two skyline laws. The ideal endpoint answer at (a,b) is whether some point of S lies in [0,a]×[0,b]. The vector remains unchanged throughout all its queries.

The root-supplied strengthening holds:

    0 < KL(Q0 || Q1) = O((log n)^2/n^4).                    (1)

Consequently, for fixed 0<α<1/2, every common measurable adaptive retained-endpoint protocol on fresh independent vectors, satisfying unconditional terminal correctness in both worlds, obeys

    E0 N = Ω_α(n^4/(log n)^2),                            (2)

where N charges each independent vector from its first observation, including vectors whose query sequences never finish. Exact skyline revelation at each start is also covered. Queries may use arbitrary thresholds, revisit vectors, and interleave them. Full assumptions and the actual-action argument appear in section 8.

This is an upper bound on reverse information and a lower bound on expected started-vector cost. It is **not** a Θ information claim, a matching logarithmic order, a leading constant, a finite forward-KL claim, or an optimal test. The existing count-test upper bound O_α(n^4/log n) in the ideal skyline channel leaves a logarithmic gap. No finite-probe, precision, noise, physical-route, or distribution-free identification claim follows.

The sharper step is entirely under the baseline Q0: a fourth moment of the compensated count and a second moment of a weighted compensation. The auxiliary Poisson process is only a proof device. The actual experiment remains fixed-count.

## 1. Exact finite-Poisson skyline laws and posterior

Let Π_m denote a uniform Poisson point process of intensity m on the unit square, and E_Π its expectation. Include its empty skyline, for which K=0,U=1,D=0. On the ordered nonempty stratum

    0<x1<⋯<xk<1,    1>y1>⋯>yk>0,

the fixed-N uniform skyline density, relative to ordinary ordered-coordinate Lebesgue measure, is

    g_N(s)=(N)_k D^(N−k),       k≤N.

There is no extra k! divisor. The density follows by choosing the ordered skyline labels and requiring every remaining point to lie in D. Mixing with N~Poi(m), and writing N=k+j, gives

    P_Π(N=k+j, S∈ds)/ds
      =e^(−m)m^k(mD)^j/j!,
    q_m(s)=m^k exp(−mU).                                  (3)

The empty mass is e^(−m), also represented by the last expression. Thus, as a regular conditional law,

    N | S = K + Poi(mD).                                  (4)

Conditional on the skyline and the number of hidden points, those points are iid uniform on D. Combining this fact with (4), the entire hidden configuration conditional on S is PPP(m·1_D). This assertion includes the empty case, where D=0 and there are no hidden points.

More generally, for a finite, strictly positive intensity function λ on the square, the same mixture calculation gives

    q_λ(s)=∏_i λ(x_i,y_i) exp(−∫_E λ),                    (5)

with empty mass exp(−∫λ). Normalization in (3) and (5) is inherited from the normalized latent point process, not inferred from numerical integration.

## 2. A bounded skyline density comparison, not arbitrary de-Poissonization

Conditioning Π_m on N=n=m−1 gives exactly Q0. Its conditioning mass is

    p_m=P(Poi(m)=m−1)=P(Poi(m)=m)>0.

Bayes' formula and (4) give the exact Radon–Nikodym derivative of Q0 with respect to the Poisson skyline law:

    r_n(s)=P(Poi(mD)=n−K)/p_m,       K≤n,
    r_n(s)=0,                       K>n.                 (6)

The Poisson pmf is zero at a negative integer, which covers K>n. For the empty skyline D=0,K=0, the numerator is P(Poi(0)=n)=0 because n≥1, so its derivative is also zero.

On U≤1/2, put v=mD≥m/2≥1. A Poisson(v) mass is maximized at floor(v), choosing that mode when v is integral. Then r=floor(v) satisfies r≥1 and r≥v/2. The elementary Stirling lower bound and log u≤u−1 give

    P(Poi(v)=r)
      ≤(2πr)^(−1/2) exp[r−v+r log(v/r)]
      ≤(πv)^(−1/2).

The Stirling upper bound m!≤sqrt(2πm)(m/e)^m exp(1/(12m)) gives

    p_m≥exp(−1/(12m))/sqrt(2πm).

Consequently, for every n≥1,

    r_n(s)≤2 exp(1/24)<3       on {U≤1/2}.                (7)

In particular, for every nonnegative skyline-measurable H,

    E0[H 1{U≤1/2}]≤3 E_Π H.                              (8)

This uniform constant is the reason no square-root sample-size loss appears. The unrestricted elementary estimate E0 H≤E_Π H/p_m would lose a factor of order sqrt(m) and is not used. Equation (8) alone is a restricted comparison; the remaining fixed-count event is handled explicitly below.

## 3. Dyadic area moments and the exceptional fixed-count event

For any point configuration, define h(a)=min{Y_j:X_j≤a}, with h(a)=1 if the set is empty. Then U=∫h. With L=ceil(log2 b), b≥1, and a_j=2^(−j−1), the staircase geometry gives

    bU≤1+Σ_(j=0)^(L−1) b a_j h(a_j).                     (9)

For Π_m take b=m. For 0≤t<ma,

    P_Π(ma h(a)>t)=exp(−t),

and the probability is zero for t≥ma. The endpoint atom when h(a)=1 is respected by this strict-tail formula. Layer cake and Minkowski, without any independence assumption between bands, yield

    E_Π Z^2≤[1+sqrt(2)J_m]^2=:B_m^(2),
    Z=mU,        J_m=ceil(log2 m).                        (10)

For either fixed-count hard-pair world take b=n and J=ceil(log2 n). At 0≤t<na the corresponding void probability is exactly (1−t/n)^n≤e^(−t), including world 1 because cm=n. Hence, for every positive integer r,

    ||mU||_(r,i)≤(m/n)[1+J(r!)^(1/r)],       i=0,1,        (11)
    Q_i(nU>1+Jt)≤J e^(−t),                  t≥0.          (12)

When J=0 the sum is empty and the stated tail event is empty. Define a convenient explicit bound

    δ_n=1,                                      n=1,2,
    δ_n=min{1,J exp[−(n/2−1)/J]},               n≥3.

Then

    Q0(U>1/2)≤δ_n,
    m^r δ_n→0 for every fixed r>0.                         (13)

The last assertion follows from J=O(log n), so the exponential's negative term has order n/log n, which dominates every fixed multiple of log n. This is a proved superpolynomial tail, not an extrapolation of finite diagnostics.

The raw-moment consequences of (11) are also available from the separate probability-prior-art packet's sharper fixed-count exponential tail. That stronger result is not required here: this proof uses the explicit dyadic inequalities, avoiding any dependence on a pending source-review status.

## 4. A fourth moment for the compensated count

Throughout this section the law is Π_m. Define

    M=K−mU=K−Z.

The skyline intensity ratio from (3), at intensities me^(−t) and m, normalizes to one, including the empty stratum:

    E_Π exp[−tK+(1−e^(−t))Z]=1.                          (14)

The equality holds for every real t. At fixed finite m, K≤N with N Poisson and 0≤Z≤m. On a compact t-interval, the first four derivatives are bounded by a constant depending on m times (1+N^4)exp(aN), an integrable variable. Differentiation through the expectation is therefore justified.

The exponent in (14) is

    −tM−Zt²/2+Zt³/6−Zt⁴/24+O(t⁵).

Its first, second, and fourth derivatives give exactly

    E_Π M=0,
    E_Π M²=E_Π Z,
    E_Π M⁴=6E_Π(M²Z)+4E_Π(MZ)−3E_Π Z²+E_Π Z.          (15)

In particular, the mixed term is +4E(MZ), and the Z² term has coefficient −3. Neither term is assumed zero, and K and Z are not assumed independent.

Put F=E_Π M⁴, B=E_Π Z², and b=E_Π Z≤sqrt(B). Cauchy–Schwarz, dropping the nonpositive term in (15), gives

    F≤6sqrt(FB)+4sqrt(bB)+b
     ≤F/2+18B+4B^(3/4)+sqrt(B).

Since B^p≤1+B for 0≤p≤1,

    E_Π M⁴≤46(1+B)
           ≤46[1+(1+sqrt(2)J_m)²]=:F_m
           =O((log m)²).                                 (16)

Under Q0, |M|≤m because K≤n<m and 0≤mU≤m. Applying (8) on the good-area event and (13) on its complement proves the fixed-count bound

    E0(K−mU)^4≤3F_m+m^4δ_n=O((log m)²).                  (17)

This is an inequality obtained from the exact restricted density ratio. It does not claim that the Poisson moment equalities in (15) survive conditioning. Indeed the fixed-count mean is E0 M=−1/m, not zero.

## 5. The weighted compensation, verified from its actual skyline density

Let w(x,y)=xy, let M1=∫_E xy dxdy, and set

    A=Σ_(z∈S) w(z)−mM1.

For the Poisson process, use the inhomogeneous finite intensity λ_t(x,y)=m exp(−t w(x,y)). Formula (5) gives its exact skyline likelihood ratio relative to Π_m:

    R_t(S)=exp[−tΣ_S w+m∫_E(1−exp(−tw))],
    E_Π R_t=1.                                           (18)

This holds including the empty skyline. The weight is bounded by one, K≤N, and the total intensity is finite for t near zero. The same Poisson exponential-moment domination as above justifies two derivatives under the expectation. At zero, the first derivative of log R_t is −A and the second is −m∫_E w². Therefore

    E_Π A=0,
    E_Π A²=m E_Π∫_E w².                                 (19)

For an independent check of the precise weighted identity, take T=Σ_(all points) w. Its unconditional mean and variance are m∫w and m∫w². The posterior (4) gives

    E(T|S)=Σ_S w+m∫_D w=m∫w+A,
    Var(T|S)=m∫_D w².

The total-variance formula then gives (19). Thus no unverified weighted-hull extension or independence of a random region and the process is needed.

The lower rectangle below (x,y) is empty with probability exp(−mxy). Tonelli and the product substitution give

    E_Π A²
      =m∫_[0,1]² (xy)²e^(−mxy) dxdy
      =(1/m²)∫_0^m u²(log m−log u)e^(−u)du
      ≤(2 log m+1/9)/m².                                 (20)

For the last inequality, use ∫_0^∞u²e^(−u)du=2; omit the nonpositive −log u term for u≥1; and bound the remaining integral by ∫_0^1u²(−log u)du=1/9.

Under Q0, Σ_S w/m≤K/m≤1 and M1≤1/4, so the loose bound |A/m|≤2 is valid everywhere. Equations (8), (13), and (20) therefore yield

    E0(A/m)²≤3(2 log m+1/9)/m⁴+4δ_n
             =O(log m/m⁴).                              (21)

This is a baseline fixed-count second-moment bound. The exact centering statement E_Π A=0 is not silently transferred to Q0.

## 6. Sharper integrated square of the local log likelihood

On the common strata 1≤K≤n, define the global polynomial score

    Q(S)=[(K−mU)²−K]/(2m²)+2A/m.                         (22)

Under Q0 the skyline count has the ordinary uniform-record law. Its independent Bernoulli(1/r) representation gives E0 K²≤H_n²+H_n. From (22),

    Q²≤(M⁴+K²)/m⁴+8(A/m)².

Consequently (17) and (21) give the explicit bound

    E0 Q²≤V_m/m⁴+33δ_n,
    V_m=3F_m+H_n²+H_n+24(2 log m+1/9)
        =O((log m)²).                                    (23)

The likelihood-score predecessor proves, whenever K/m≤1/2 and U≤1/2,

    log L=Q+R,
    |R|≤40(K/m+U)³,                                     (24)

where L=d(Q1 restricted to {K≤n})/dQ0. This deterministic expansion remains localized; no claim is made about its remainder near U=1.

For the sixth raw moment, the record factorial-moment inequality E(R_m)_r≤H_m^r gives

    E0 K⁶≤P6(H_m),
    P6(h)=h⁶+15h⁵+65h⁴+90h³+31h²+h.

Combining (11) with Minkowski, put

    W_m=P6(H_m)^(1/6)+(m/n)[1+J·720^(1/6)]
        =O(log m).

Then

    E0(K/m+U)⁶≤W_m⁶/m⁶,
    E0[R²1{K/m≤1/2,U≤1/2}]≤1600W_m⁶/m⁶.                (25)

The indicator is essential. In particular, on any event G inside that local domain,

    E0[(log L)²1_G]
      ≤2[V_m/m⁴+33δ_n+1600W_m⁶/m⁶].                     (26)

The residual term O(log⁶m/m⁶) is o(log²m/m⁴); this follows from log⁴m/m²→0. No covariance cancellation beyond the proved estimates is asserted.

## 7. Entropy window, exceptional likelihood tail, and singular mass

This section retains exactly the log-four packet's unconditioned entropy architecture. Its facts are restated to make the strengthened bound auditable.

Under either fixed-count world, K is dominated by the uniform-record count R_m. Under Q0 this follows from its exact record law. Under Q1 it is the predecessor's TP2 conditional-quantile coupling; Joe record indicators are not asserted independent. The uniform-record mgf gives

    Q_i(K>e H_m+t)≤e^(−t),       i=0,1.

With J=ceil(log2 n), define

    t_m=20 log m,
    B_m=e H_m+t_m+(m/n)(1+Jt_m),
    β_m=(J+1)m^(−20),
    G_m={K+mU≤B_m}.

The count bound and (12) prove Q_i(G_m^c)≤β_m under both unconditioned laws. Since B_m=O(log²m), eventually G_m lies in common support and satisfies K/m≤1/2,U≤1/2. The score geometry also gives |log L|≤23(K/m+U)² on K/m+U≤1/2. Hence eventually |log L|≤1 throughout G_m. No forward logarithm is assigned on the alternative-only stratum K=m.

For φ(v)=−log v+v−1 and |a|≤1,

    φ(e^a)=e^a−1−a≤(e/2)a².

Using (26) only on G_m therefore gives

    E0[φ(L)1_Gm]
      ≤e[V_m/m⁴+33δ_n+1600W_m⁶/m⁶].                     (27)

For the bad-window entropy, the exact common-support likelihood is

    L=m/(m−K) ·∏_S f_c ·D_c^(m−K)/D^(n−K),
    D_c=∫_D f_c.

The global inequalities f_c≥c, D_c≥cD and log⁺f_c(x,y)≤2[−log(1−x)] imply

    |log L|≤2m(1+W),
    W=Σ_(r=1)^n[−log(1−X_r)−log(1−Y_r)].

For clarity, −log D≤W because the upper rectangle from any skyline point lies in D; its two margin logs are part of W. Taking absolute values in the exact likelihood then gives the intermediate bound log m+m(−log c)+(2m−1)W, which is at most 2m(1+W). Under Q0, W is a sum of 2n independent Exp(1) variables, so

    E0(1+W)²=4n²+6n+1≤4m²,
    ||log L||_(2,Q0)≤4m².                               (28)

In particular the reverse logarithm is integrable for every n. Since φ(L)≤|log L|+L+1, Cauchy–Schwarz and change of measure on common support give

    E0[φ(L)1_Gmᶜ]
      ≤4m²sqrt(β_m)+Q1({K≤n}∩G_m^c)+Q0(G_m^c)
      ≤4m²sqrt(β_m)+2β_m.                               (29)

Both-world tail control is indispensable for the L term.

The singular component of Q1 relative to Q0 is precisely {K=m}, with mass 0<p_n<1/m!, as proved by the predecessor's strict TP2 permutation argument. Thus E0 L=1−p_n, KL(Q1||Q0)=∞, and the exact unconditioned identity is

    KL(Q0||Q1)=E0 φ(L)+p_n.                              (30)

The sign is plus. No normalization by 1−p_n, conditioning away of a support event, or finite forward-KL substitution occurs. Combining (27)–(30), for all sufficiently large m,

    0<KL(Q0||Q1)
      ≤e[V_m/m⁴+33δ_n+1600W_m⁶/m⁶]
          +4m²sqrt(β_m)+2β_m+1/m!.                       (31)

Here V_m=O(log²m), W_m=O(log m), δ_n is superpolynomially small, the β term is O(m^(−8)sqrt(log m)), and 1/m! is smaller than any inverse power. This proves (1). Strict positivity already follows from (30) and p_n>0; finiteness for every n follows from (28).

## 8. Adaptive started-vector lower bound

Assume a common measurable policy and common world-independent randomization. Each newly observed vector is fresh and independent of all previous vectors and policy randomization, with the stipulated world-specific law; a retained vector never mutates. The observation channel consists only of endpoint answers determined by its skyline. Other latent route labels, gate bits, mutated states, or auxiliary world-dependent signals are excluded.

Augment the actual action history by revealing a vector's entire skyline at its first observation. Simulate the original policy using its original observations, ignoring the added information in its decisions. A new skyline reveal contributes D_n=KL(Q0||Q1) conditional reverse information. Any later endpoint answer from the same vector is deterministic given its skyline and the selected endpoint, and contributes zero. Action choices, randomization and stopping kernels are common in both worlds. Pad the history after termination with a common dummy symbol.

If N_T counts distinct vectors first observed during the first T actual actions, the finite chain rule and data processing give

    KL(history0,T || history1,T)≤D_n E0 N_T.              (32)

The actual-action indexing remains meaningful on a path that queries one retained vector forever. Charging starts, rather than only completed query sequences, prevents an infinite or selectively retained word from evading the cost. Counting allocation/drawing even earlier can only increase N.

Require unconditional terminal correctness:

    P0(finite stop and decision 0)≥1−α,
    P1(finite stop and decision 1)≥1−α,
    0<α<1/2.

Let E_T be the event of stopping and deciding 0 by action T. Binary data processing in (32), then monotone convergence and lower semicontinuity as T→∞, yield

    D_n E0 N≥kl(p,q)≥kl(1−α,α),

where p≥1−α and q≤α are the probabilities of the limiting terminal-0 event. Infinite E0 N satisfies the bound trivially. Correctness only conditional on termination would not suffice. Applying (1) proves (2), with the baseline expectation E0, not E1.

Counting every independently started vector is the headline convention here; no selectively uncharged one-shot exception is needed. Full exact skyline revelation is an information envelope, not a finite algorithm to reconstruct arbitrary real thresholds. The lower bound is conditional on the stated iid family and channel. It does not make a claim about physical access or actual-route architecture.

## 9. Prior art, contribution attribution, and verification limits

The general Poisson compensation machinery is established prior art. Last–Molchanov's [Poisson hulls](https://arxiv.org/html/2212.02150v4) explicitly includes Pareto minima in Example 2.15; Theorem 3.2 gives the conditional interior Poisson law; Theorem 5.1 gives the weighted variance formula. Their [Efron type identities for stopping sets and Poisson hulls](https://arxiv.org/html/2608.06038v1), Theorem 4.7, supplies the joint exponential identity, with Pareto minima again covered by Example 8.4. The latter is an August 2026 preprint. These source results are not claimed as discoveries of this packet. The general exponential identity's earlier antecedent is attributed through that source, without asserting a direct read of the antecedent.

The parent supplied the log-squared candidate, fourth-derivative relation, proposed restricted density transfer, weighted compensation strategy, and entropy reuse. It also supplied the inhomogeneous-tilt verification during the work. This packet verifies those suggestions, supplies explicit inequalities and constants, proves the specialized identities from the actual skyline densities, checks both the tilt and conditional-variance routes, and records deterministic arithmetic controls. This is verification and a bounded synthesis of a supplied candidate, not independent discovery or duplicate fresh-research credit.

The existing local packets own the hard pair, exact skyline likelihood, singular mass, count coupling, local Taylor expansion, log-four entropy argument, and actual-action transport. Their byte hashes are in SOURCE_BINDINGS.json. The probability-prior-art packet owns the targeted source discovery and sharper fixed-count area-MGF corollary; its result is acknowledged but that corollary is not needed in this proof. The general source theorems are attribution/background, since the specialized posterior, exponential and weighted identities are independently proved above. No arbitrary Poisson conditioning theorem or convex-hull-only transfer is imported.

controls.py checks derivative signs symbolically, finite exact coefficients of the Poisson skyline identities by ordered-simplex integration, the empty-stratum contribution, density-ratio algebra and constant, weighted integral bounds, record moment coefficients, and deterministic scale diagnostics. These are mathematical test configurations, not empirical observations or a fitted rate. Numerical quadrature is not a certified interval proof. The written inequalities establish the asymptotic theorem; the scripts do not constitute formal proof checking.

No predecessor is edited or retroactively strengthened. The independent log-four review does not certify this log-squared sibling. This packet requires its own final-digest-bound independent review before acceptance. No field-wide novelty, lower information constant, exact asymptotic, test optimality, protected integration, historical-floor certification, or closure is claimed.
