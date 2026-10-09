# Sharp information in the ideal retained skyline

8 October 2026 UTC. New scratch-only prospective candidate after the log-squared lower-bound sibling. All predecessors remain unchanged. Historical floor remains **UNVERIFIED**. This is a written mathematical proof with deterministic controls, pending a fresh independent final-digest-bound attack. It is not accepted integration, a kernel proof, an empirical experiment, physical-access certification, or project closure.

## Result and scope

Let n≥1, m=n+1, and c=n/m. In world 0 a retained vector contains n iid product-uniform points in (0,1)². In world 1 it contains m iid points with distribution and density

    F_c(x,y)=1−(1−xy)^c,
    f_c(x,y)=c(1−xy)^(c−2)(1−cxy).

Let Q0,Q1 denote the laws of the complete coordinatewise-minimal skyline S. Write K=|S|, E for its lower undominated region, U=area(E), and D=1−U. The hypotheses include the stated known pair, fresh independent vectors, and retention without mutation. All logarithms are natural.

The parent-supplied sharp candidates hold:

    KL(Q0 || Q1) ~ (log m)²/(4m⁴),                         (1)

    H²(Q0,Q1) ~ (log m)²/(8m⁴),                          (2)

where the convention is H²(P,Q)=∫(√dP−√dQ)², without a factor 1/2. The entire alternative-only stratum K=m is included in both expressions. The forward divergence KL(Q1||Q0) remains infinite for every n.

For any fixed 0<α<1/2, the ideal experiment that reveals the entire exact skyline of each fresh vector therefore has two-sided-error sample complexity

    Θ_α(m⁴/(log m)²)=Θ_α(n⁴/(log n)²).                   (3)

Here the lower bound applies even to expected baseline started-vector cost E0 N of arbitrary common adaptive protocols with unconditional terminal correctness in both worlds. The matching upper bound is an ordinary fixed-sample likelihood-ratio test of the known pair on exact skyline observations. It consequently also bounds the worst-case expected cost in that ideal channel. No exact optimal testing constant, all-confidence asymptotic, larger-class minimax theorem, finite endpoint-query cost, finite-precision algorithm, noise guarantee, or physical instrument is asserted.

The new step is a sharp fixed-count fourth compensated moment. The auxiliary Poisson process is used only to establish that moment; it does not change the actual fixed-count experiment. Convergence in probability of a likelihood or a conditioning density alone is not used to infer an information integral.

## 1. Precisely inherited ingredients

The consumed result files are byte-bound in SOURCE_BINDINGS.json. Their pending/accepted statuses do not substitute for review of this packet. In particular the log-squared sibling is consumed as a written source, not represented as independently accepted.

The exact common-support likelihood on A0={K≤n} is

    L(s)=m/(m−K) · ∏_(z∈S) f_c(z) · D_c^(m−K)/D^(n−K),
    D_c=∫_D f_c.

The entire singular component of Q1 relative to Q0 is {K=m}, with

    0<p_n:=Q1(K=m)<1/m!,    E0 L=1−p_n.                  (4)

For M=K−mU, M1=∫_E xy dxdy, T=Σ_(x,y∈S)xy, and A=T−mM1, define the global polynomial

    Q=[M²−K]/(2m²)+2A/m.                                (5)

The likelihood-score source proves on {K/m≤1/2,U≤1/2}

    log L=Q+R,       |R|≤40(K/m+U)³.                     (6)

The baseline-moment source gives, with H_n=Σ_(j=1)^n 1/j,

    E0 M²=H_n+O((log m)²/m),
    E0 K=H_n,       Var0 K=H_n−H_n^(2),
    E0 K²=H_n²+H_n−H_n^(2).                             (7)

The log-squared source supplies the following facts, with their specialized proofs from the actual skyline densities:

• Under the uniform Poisson process Π_m of intensity m, including its empty skyline, put Z=mU and M=K−Z. Its skyline density is m^K exp(−Z), and

    EΠ exp[−tM+Z(1−e^(−t)−t)]=1,     t∈R.               (8)

• EΠ M=0, EΠ M²=EΠ Z, and EΠ M⁴=O((log m)²). Every fixed positive integer r satisfies EΠ Z^r=O((1+log m)^r), by the dyadic area bound and Minkowski. More explicitly, ||Z||_(r,Π)≤1+⌈log₂m⌉(r!)^(1/r): every band variable has strict tail at most e^(−t), and independence between bands is unnecessary. These are unconditioned Poisson assertions.

• For n=m−1 the exact density of the fixed-count skyline law Q0 relative to Π_m is

    r_n(s)=P(Poi(mD)=n−K)/P(Poi(m)=n),                   (9)

where the numerator is zero for a negative index, and it is zero for the empty skyline since n≥1. On {U≤1/2}, r_n≤2e^(1/24)<3. This is a restricted density bound, not a general conditioning assertion.

• There is a superpolynomially small fixed-count tail

    Q0(U>1/2)≤δ_n,
    δ_n≤J exp[−(n/2−1)/J]   for n≥3, J=⌈log₂ n⌉,        (10)

with a harmless cap at 1. Thus m^b δ_n→0 for every fixed b. Also

    E0(A/m)²=O(log m/m⁴).                                (11)

For clarity, (11) comes from the exact weighted Poisson variance

    EΠ A²=m∫_(0,1)² (xy)² e^(−mxy) dxdy
           ≤(2 log m+1/9)/m²,

then (9) on U≤1/2 and (10) on its complement. The random region is not treated as independent of the point process.

The derivations below prove the additional sharp moment, the required uniform integrability, the exact information constants, and the matching ideal-channel order.

## 2. Poisson area concentration, without an unproved conditioning transfer

Set a_m=EΠ Z. A lower rectangle with area xy is empty with probability e^(−mxy). Tonelli and the product substitution yield

    a_m=∫_0^m (log m−log u)e^(−u)du=log m+O(1).           (12)

To justify the O(1) directly, ∫_0^∞|log u|e^(−u)du is finite, and log m times the omitted exponential mass tends to zero. No precise Euler-constant evaluation is needed.

Let N be the number of Poisson points. Conditional on N, K has the ordinary uniform-record law, including K=0 when N=0. Therefore

    VarΠ K=E[H_N−H_N^(2)]+Var(H_N).                       (13)

E H_N=EΠ K=a_m by EΠ M=0. Moreover Var(H_N)=O(1). Here is an explicit tail justification rather than informal substitution of N≈m. On m/2≤N≤2m, the elementary harmonic bounds give |H_N−log m|≤C for an absolute C. On N<m/2 the squared difference is O((1+log m)²), multiplied by an exponentially small Poisson lower tail. On N>2m, H_N≤N and

    E[N² 1{N>2m}]≤e^(−2θm) E[N²e^(θN)]
      =[me^θ+m²e^(2θ)] exp[m(e^θ−1−2θ)]                 (14)

with θ=log 2. Since 2log 2−1>0, (14) tends to zero exponentially up to its polynomial prefactor. The lower tail follows in the same way from E e^(−θN). These bounds also cover N=0, where H_0=0. They prove E(H_N−log m)²=O(1), hence the variance assertion.

It follows that VarΠ K=O(log m). Because Z=K−M, EΠ M=0, and EΠ M²=a_m,

    VarΠ Z≤2 VarΠ K+2 VarΠ M=O(log m).                   (15)

In particular

    EΠ Z²=a_m²+O(log m)~(log m)².                        (16)

This elementary record/compensation route replaces the parent's suggested mixture of the exact fixed-count U² identity. It establishes the same required concentration while handling N=0 and both Poisson tails explicitly.

## 3. The sharp fourth Poisson moment

Differentiating (8) four times at zero gives the exact relation already checked in the log-squared source:

    EΠ M⁴=6EΠ(M²Z)+4EΠ(MZ)−3EΠ Z²+EΠ Z.                (17)

The mixed term has a plus sign; it is not set to zero. With EΠ M⁴=O(log²m), (15), and EΠ M²=a_m, Cauchy–Schwarz gives

    EΠ(M²Z)=a_m EΠ M²+EΠ[M²(Z−a_m)]
            =a_m²+O((log m)^(3/2)),                     (18)

    |EΠ(MZ)|=|EΠ[M(Z−a_m)]|=O(log m).                   (19)

Combining (16)–(19),

    EΠ M⁴=3a_m²+O((log m)^(3/2))~3(log m)².             (20)

This proves the coefficient 3 from a genuine moment identity and a variance bound. It assumes no Gaussian limit and asserts none.

## 4. Sixth moment and the uniform integrability needed for fixed-count transfer

At each finite m, K≤N and 0≤Z≤m. On a compact t-interval, six derivatives of the integrand in (8) are bounded by C_m(1+N⁶)e^(bN) for finite C_m,b. The Poisson exponential moment is finite, so differentiation under expectation is justified through order six.

The sixth derivative at zero is exactly

    M⁶−15M⁴Z−20M³Z+45M²Z²−15M²Z
       +60MZ²−6MZ−15Z³+25Z²−Z.                         (21)

Its expectation is zero. Put F6=EΠ|M|⁶ and ℓ=1+log m. Every term other than M⁶ is a constant multiple of M^i Z^j with 0≤i≤4, j≥1, and i+2j≤6. For i>0, Hölder gives

    EΠ|M|^i Z^j
      ≤F6^(i/6) [EΠ Z^(6j/(6−i))]^((6−i)/6)
      ≤C_(i,j) F6^(i/6) ℓ^j.                            (22)

The raw-moment bound for noninteger exponents follows from any larger integer moment by Lyapunov's inequality. Terms with i=0 are O(ℓ^j), with j≤3. Taking absolute values in (21), dividing by ℓ³, and writing x=F6/ℓ³ therefore gives

    x≤C[1+x^(1/6)+x^(1/3)+x^(1/2)+x^(2/3)].              (23)

Indeed i/2+j≤3 and ℓ≥1. For x≥1 the right side is at most 5C x^(2/3), so x≤(5C)³; x<1 is already bounded. Equivalently each mixed term can be absorbed by Young's inequality. Hence

    EΠ|M|⁶=O((log m)³).                                  (24)

In particular X_m=M⁴/(log m)² is uniformly integrable under its varying Poisson laws, because sup_(m≥2) EΠ X_m^(3/2)<∞. A harmless enlargement of the constant covers bounded m.

## 5. Conditioning density tends to one, and the fourth moment transfers

First, EΠ(K+Z)=2a_m=O(log m), so K+Z=O_P(log m). Also EΠ M²=a_m gives M=O_P(√log m). Thus U=o_P(1), K<m−1 with probability tending to one, and, with

    v=mD=m−Z,       q=n−K=m−1−K,

we have v/m→1, q/m→1 and

    q−v=−M−1=O_P(√log m)=o_P(√m).                       (25)

On these high-probability events, elementary Stirling expansion for the Poisson mass gives

    log P(Poi(v)=q)
      =−(1/2)log(2πq)−(q−v)²/(2v)
          +O(|q−v|³/v²+1/q).                            (26)

One obtains (26) by writing q/v=1+d/v and expanding (1+d/v)log(1+d/v); it is uniform when |d|/v≤1/2. Its error and quadratic term tend to zero in probability by (25). The denominator in (9) is P(Poi(m)=m)=exp[−(1/2)log(2πm)+O(1/m)]. Therefore

    r_n→1 in Π_m-probability.                            (27)

The rare negative-index and empty cases in (9) do not affect this convergence, since the event used above has probability tending to one. This does not assert a global deterministic bound on r_n.

Define r̄_n=r_n 1{U≤1/2}. Then 0≤r̄_n≤3 and r̄_n→1 in probability. Uniform integrability from (24) gives

    EΠ[X_m r̄_n]−EΠ X_m→0.                              (28)

For completeness, truncate X_m at a fixed B. The expectation of its truncated part times |r̄_n−1| tends to zero because this multiplier is bounded and converges in probability to zero. The remaining expectation is bounded by 3EΠ[X_m1{X_m>B}], uniformly small as B→∞. This proves (28), rather than inferring a moment limit from (27) alone.

On the fixed-count complement U>1/2, |M|≤m, so (10) gives

    E0[M⁴1{U>1/2}]/(log m)²≤m⁴δ_n/(log m)²→0.           (29)

The exact change of measure (9), (20), (28), and (29) now prove

    E0 M⁴~3(log m)².                                    (30)

The conditioning transfer is limited to this proved moment statement. Poisson equalities such as EΠ M=0 are not transferred: the fixed-count mean is actually E0 M=−1/m.

## 6. Sharp integrated square of the polynomial score

Let h=H_n. From (7), h~log m, E0 M²=h+o(1), Var0 K=O(log m), and E0 K²=h²+O(log m). By (30) and Cauchy–Schwarz,

    E0(M²K)=h E0 M²+E0[M²(K−h)]
             =h²+O((log m)^(3/2))+o(log m).              (31)

Consequently

    E0(M²−K)²
      =E0 M⁴−2E0(M²K)+E0 K²
      ~2(log m)².                                       (32)

The first summand of Q in (5) thus has squared L² norm asymptotic to (log m)²/(2m⁴). By (11), the second summand has L² norm O(√log m/m²), which is little-o of the first summand's norm. The triangle inequality in L², or an explicit Cauchy–Schwarz cross-term bound, gives

    E0 Q²~(log m)²/(2m⁴).                                (33)

This is a second raw moment, not an assertion of exact centering. In particular the polynomial's nonzero finite-n mean must not be substituted for E0 log L. No computation of that mean is needed here.

## 7. Integrated likelihood expansion on a shrinking uniform window

We now restate exactly the global-tail ingredients consumed from the log-four and log-squared sources. Put J=⌈log₂ n⌉, t_m=20log m, and

    B_m=eH_m+t_m+(m/n)(1+Jt_m),
    β_m=(J+1)m^(−20),
    G_m={K+mU≤B_m}.                                      (34)

Under both unconditioned skyline laws, Q_i(G_m^c)≤β_m. This follows from the ordinary-record count domination and the common one-rectangle void tail; the Joe record indicators are not assumed independent. Since B_m=O(log²m), eventually G_m lies in common support, K/m,U≤1/2, and

    sup_(G_m)|log L|≤23(B_m/m)²=:ε_m→0.                  (35)

The sixth raw moments of K+mU are O(log⁶m). Therefore the localized remainder in (6) obeys

    E0[R²1_Gm]=O(log⁶m/m⁶)=o(log²m/m⁴).                 (36)

Only this indicated localization is used. Globally, under Q0, |M|≤m, K≤n<m and |A/m|≤2, hence |Q|≤5. Thus

    E0[Q²1_(G_m^c)]≤25β_m=o(log²m/m⁴).                  (37)

Combining (33), (36), and (37) with the L² triangle inequality on G_m yields

    E0[(log L)²1_Gm]~(log m)²/(2m⁴).                    (38)

The global logarithm bound from the exact likelihood is also retained:

    ||log L||_(2,Q0)≤4m².                               (39)

It follows by bounding |log L|≤2m(1+W), where W is the sum of the 2n independent Exp(1) margin logs of the underlying uniform routes. Equation (39) is used only to control exceptional entropy; it is not a sharp global second-moment claim.

## 8. Reverse entropy and Hellinger constants, including the singular mass

Let φ(v)=−log v+v−1. Since E0 L=1−p_n, the exact reverse-entropy identity is

    KL(Q0||Q1)=E0 φ(L)+p_n.                              (40)

The sign is plus. On G_m, the uniform shrinking bound (35) permits the uniform Taylor equivalence

    φ(e^a)=(1/2)a²[1+o(1)],      |a|≤ε_m,               (41)

where the value at a=0 is understood by continuity. Thus (38) gives

    E0[φ(L)1_Gm]~(log m)²/(4m⁴).                        (42)

On the complement, φ(L)≤|log L|+L+1, (39), and change of measure on common support give the unconditioned bound

    E0[φ(L)1_(G_m^c)]
       ≤4m²√β_m+Q1(A0∩G_m^c)+Q0(G_m^c)
       ≤4m²√β_m+2β_m=o(log²m/m⁴).                       (43)

The Q1 tail is essential for the L term; a Q0 probability bound alone would not suffice. Finally p_n<1/m!=o(log²m/m⁴). Equations (40)–(43) prove (1).

For Hellinger, its definition relative to any common dominating measure gives the exact decomposition

    H²(Q0,Q1)=E0(√L−1)²+p_n.                            (44)

On the singular stratum Q0 has density zero, so its contribution is exactly p_n. On G_m,

    (e^(a/2)−1)²=(1/4)a²[1+o(1)]

uniformly by (35), while (√L−1)²≤1+L everywhere on common support. Hence

    E0[(√L−1)²1_Gm]~(log m)²/(8m⁴),
    E0[(√L−1)²1_(G_m^c)]≤2β_m=o(log²m/m⁴).              (45)

Equations (44)–(45) prove (2). In particular KL(Q0||Q1)/H²(Q0,Q1)→2 with the stated Hellinger convention. The result is not obtained from convergence in probability of Q or log L; the preceding moment, local remainder, both-law tail, and singular-mass controls do the integration work.

## 9. Matching testing order in the ideal exact-skyline channel

Define the affinity

    ρ_m=∫√(dQ0 dQ1)=E0√L=1−H²(Q0,Q1)/2.                (46)

For each fixed n, 0<ρ_m<1. Positivity follows from positive common densities, and strict inequality from distinct normalized laws, already witnessed by p_n>0. For R independent exact skylines, the ordinary likelihood-ratio test of Q0^R against Q1^R, with threshold one, has sum of the two errors

    ∫min(dQ0^R,dQ1^R)≤∫√(dQ0^R dQ1^R)=ρ_m^R.            (47)

An observed K=m is assigned to world 1. Otherwise the test compares the product of the common-support likelihoods to one. Any fixed tie convention has the same sum-of-errors identity. Choosing

    R=⌈log(1/α)/(−log ρ_m)⌉                             (48)

makes the sum at most α, hence each error at most α. Choosing 2α in place of α would not by itself establish the requested bound for each error, so (48) uses α. Since

    −log ρ_m~(log m)²/(16m⁴),

this particular sufficient fixed budget satisfies

    R~16log(1/α) · m⁴/(log m)².                          (49)

The constant in (49) describes this affinity-based sufficient budget, not the exact optimal sample size. Alternatively, (2) implies 1−ρ_m≥(log m)²/(32m⁴) eventually, so the explicit eventual choice R=⌈32log(1/α)m⁴/(log m)²⌉ proves the order without computing ρ_m numerically. No explicit finite-n cutoff is claimed.

The likelihood is specified by the known n,c and a finite sum/product formula in each skyline's coordinates. For example, with x_(K+1)=1,

    D=Σ_i (x_(i+1)−x_i)(1−y_i),
    D_c=Σ_i[(1−x_i)^c−(1−x_(i+1))^c
                  +(1−x_(i+1)y_i)^c−(1−x_i y_i)^c].

These are Borel measurable functions, and the likelihood-ratio test is a mathematically specified test on the ideal exact observation. This is not a claim that arbitrary real coordinates can be recovered or all exact comparisons decided in a finite number of binary operations or endpoint probes. The known pair and exact skyline-readout assumptions are essential to this upper bound.

For the lower bound, the inherited actual-action argument applies with D_m=KL(Q0||Q1). Reveal the entire skyline at each vector's first observation and simulate the original policy using common world-independent randomization. Each new reveal contributes D_m conditional reverse information; later endpoint answers on that retained vector are deterministic functions of the reveal and contribute none. For every finite actual-action horizon T,

    KL(history0,T || history1,T)≤D_m E0 N_T.

If the protocol satisfies unconditional terminal correctness

    P0(finite stop and decision 0)≥1−α,
    P1(finite stop and decision 1)≥1−α,

binary data processing for the terminal-0 events, followed by monotone convergence and lower semicontinuity, gives

    E0 N≥kl(1−α,α)/D_m
         ~4kl(1−α,α) · m⁴/(log m)²                     (50)

in the sense that the right-hand lower-bound sequence has the displayed asymptotic. Infinite E0 N is allowed and satisfies the inequality. Every fresh vector is charged from its first observation, including one queried forever; no uncharged selective-retention or completion-only convention is introduced. Accuracy conditional only on termination is insufficient.

Equation (50) holds for the endpoint protocols as well as exact-skyline protocols. Equations (48)–(49) provide the upper bound only for exact-skyline protocols. Together they establish (3) for the stated ideal channel, also for the infimum of E0 N or of max(E0 N,E1 N) over two-sided-valid ideal tests. They do not assert matching query complexity for the endpoint-only implementation.

## 10. Attribution, controls, and remaining boundary

The root supplied both sharp constants, the Poisson fourth/sixth-moment route, the need for bounded-density uniform-integrability transfer, the compensated-score reduction, the entropy/Hellinger architecture, and the likelihood-affinity testing consequence. This packet verifies that candidate, supplies the simpler explicit record-based area-variance argument, carries out the sixth derivative and Hölder absorption, proves the transfer carefully, and records deterministic controls. It is not independent discovery credit for the supplied result.

The predecessor packets own the hard pair, skyline likelihood, singular-support analysis, count-record coupling, baseline moments, local expansion, Poisson compensation and weighted variance, and actual-action information argument. General Poisson-hull machinery is credited by the log-squared source to its cited literature; this packet makes no field-wide novelty claim or claim of having newly reviewed those external sources.

controls.py checks the second, fourth, and sixth tilt derivatives; exact low-intensity coefficients of the sixth identity by ordered-simplex skyline integration including the empty skyline; fixed-count low-n moments by a separate direct density integration; exact posterior-ratio algebra and asymptotic test configurations; and the entropy/Hellinger/affinity constants. CONTROL_RESULTS.json and CONTROL_RUN.log retain the checks. These are deterministic arithmetic diagnostics, not Monte Carlo, a fitted rate, empirical observations, rigorous numerical intervals, or formal kernel verification. The written proof, not finite controls, carries the general asymptotics.

The packet remains a candidate until its own final-digest-bound independent attack. No predecessor is edited or retroactively strengthened. The log-squared sibling's review remains a separate operation. No historical-floor certification, protected integration, finite-probe physical realization, asymptotic normality, sharp total variation, exact optimal testing constant, or project closure follows from this result.
