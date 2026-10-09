# Independent review: log-squared full-skyline reverse information

8 October 2026 UTC. New, scratch-only written mathematical review. No author, predecessor, archive, or protected repository was modified. Historical floor remains **UNVERIFIED**. This is not audit closure, integration authority, a formal kernel proof, empirical validation, or physical-oracle certification.

## Verdict and immutable subject

**PASS within the stated model and resource contract.** No blocking mathematical finding remains. The subject is `../full-skyline-log-squared/RESULT.md`, SHA-256 **7251887ac088bfc13a93b94e400879e851ebd1ceb1a6337449f9def20cb0c2f7**. This review does not apply automatically to different bytes.

For the stipulated fixed-count uniform/Joe pair, the author proves

    0 < KL(Q0 || Q1) = O(log² n / n⁴),
    KL(Q1 || Q0) = infinity,
    E0 N = Omega_alpha(n⁴ / log² n).

The last statement requires fresh independent vectors, unchanged retained states, a common measurable endpoint policy, and unconditional terminal correctness. N counts each vector from its first observation, including one whose query sequence never finishes. The existing ideal skyline count test has cost O_alpha(n⁴/log n); a logarithmic gap remains. No Theta information assertion, optimal logarithmic rate, leading constant, finite-probe implementation, or physical-route conclusion is certified.

The candidate and its proposed mechanism came from the parent. Independence here means fresh mathematical verification and separately written diagnostic code, not independent discovery of that mechanism. The Poisson posterior, restricted density comparison, compensated-moment derivative, and conditional-variance route were derived before reading the complete author draft. Independent controls import no author code. Author replay is a separate check in this review directory.

## 1. Exact posterior and the restricted density comparison

The ordered k-point skyline density for N uniform points is (N)_k D^(N-k). Choosing the ordered visible labels accounts for the factor (N)_k; there is no additional k! divisor. Poisson mixing gives the joint density of skyline s and total K+j as

    exp(-m) m^k (mD)^j / j!.

Summing j gives q_m(s)=m^k exp(-mU), while division by this skyline density gives N|S=K+Poi(mD). Given the hidden count, the hidden points are iid uniform in D, so their conditional point process is PPP(m 1_D). This is a conditional-density statement and does not require conditioning on a positive-probability exact continuous skyline.

The empty skyline is essential: K=0, U=1, D=0, with PPP probability exp(-m). Its posterior total is zero. Conditioning the Poisson process on N=n=m-1 therefore assigns the empty skyline mass zero. On nonempty strata the fixed-count/Poisson skyline Radon–Nikodym derivative is precisely

    r_n(s) = Poi(mD)(n-K) / Poi(m)(n).

It is zero for K>n. At the empty skyline it is zero because Poi(0)(n)=0 for n>=1, not because n-K is negative. Both cases are now explicit in the author text.

On U<=1/2, v=mD>=m/2>=1. The Poisson mode r=floor(v) obeys r>=1 and r>=v/2. Stirling's lower factorial bound and log u<=u-1 give its mass at most 1/sqrt(pi v). Meanwhile

    Poi(m)(m-1)=Poi(m)(m)
       >= exp(-1/(12m))/sqrt(2 pi m).

Consequently r_n<=2 exp(1/24)<3. This is uniform in n, K, and the skyline within the specified area event. The author correctly transfers only nonnegative skyline functionals restricted to that event. A naive conditioning bound would cost 1/Poi(m)(n), of order sqrt(m), and would not give the claimed rate.

The restriction cannot be dropped: for K=n and D=m^(-2), the ratio is exp(-1/m)/Poi(m)(m-1), which grows like sqrt(2 pi m). Such small dominated areas are available to interior antichains. The independent diagnostics explicitly reject a global constant-three comparison. The proof instead deals separately with the fixed-n complement.

Two small draft wording defects were corrected before binding: the invalid chained phrase r>=v/2>=1 for v<2, and the explanation of the empty-stratum zero. These were not defects in the resulting numerical bound or asymptotic mechanism.

## 2. Area moments and fixed-count exceptional tails

The lower-staircase height h is nonincreasing. The dyadic bands [a,2a], together with a residual interval of width at most 1/b, yield bU<=1+sum ba h(a). This is pathwise, including an empty PPP configuration. Under the Poisson model, the strict tail of ma h(a) is exp(-t) for t<ma and zero at t>=ma. The atom at h(a)=1 causes no problem because the statement uses this split.

Layer cake gives each band variable second moment at most 2. Minkowski, requiring no independence between bands, therefore gives

    E_Pi (mU)^2 <= (1+sqrt(2) ceil(log2 m))².

Under either fixed-count hard-pair law the analogous lower-rectangle void probability is (1-t/n)^n. The alternative equality uses c m=n; it is an exact fixed-count calculation. This proves all positive-integer raw moment bounds used later and the union tail

    P(nU>1+Jt) <= J exp(-t), J=ceil(log2 n).

The author's separate n=1,2 convention delta_n=1 avoids any division by J=0 or negative tail threshold. For n>=3, taking t=(n/2-1)/J proves its stated bound for P0(U>1/2). Since n/log n dominates every multiple of log n, m^r delta_n tends to zero for every fixed r. The superpolynomial statement is analytic; no fitted numerical asymptotic is needed.

## 3. Fourth compensated moment, including differentiation

At Poisson intensities m exp(-t) and m, the exact skyline density ratio is

    exp[-tK+(1-exp(-t))Z], Z=mU.

It normalizes to one for every real t, including on the empty stratum. At fixed finite m, K<=N with N Poisson, and 0<=Z<=m. On a compact t-interval, its first four derivatives are dominated by a constant depending on m times (1+N^4) exp(aN). This has finite expectation. Differentiation at zero is legitimate; no unproved exchange of a varying-m limit and expectation occurs.

Writing M=K-Z, the fourth Taylor coefficient times 24 is

    M^4 - 6 M² Z - 4 M Z + 3 Z² - Z.

Thus E M=0, E M²=E Z, and

    E M^4 = 6 E(M² Z) + 4 E(M Z) - 3 E Z² + E Z.

All signs in the author statement are correct. In particular E(MZ) is not discarded by a false independence or centering claim. With F=E M^4, B=E Z², and b=E Z<=sqrt(B), Cauchy–Schwarz and Young give

    F <= 6 sqrt(FB)+4 sqrt(bB)+b
      <= F/2+18B+4B^(3/4)+sqrt(B).

This implies F<=36B+8B^(3/4)+2sqrt(B)<=46(1+B). With the area second moment this is O(log² m), preserving the compensation that raw fourth moments would lose.

Under the actual fixed-count baseline, |K-mU|<=m. Restricted RN transfer and the exceptional tail therefore yield

    E0(K-mU)^4 <= 3 F_m + m^4 delta_n = O(log² m).

No exact Poisson equality is transferred after conditioning. The fixed-count mean is -1/m, which provides an independent countercheck against such a mistake.

## 4. Weighted compensation and the hidden configuration

For w(x,y)=xy, put A=sum_S w-m integral_E w. The author's inhomogeneous-intensity calculation is self-contained: the skyline density at intensity lambda is product_S lambda times exp(-integral_E lambda). Using lambda_t=m exp(-tw) produces the exact normalized likelihood

    exp[-t sum_S w + m integral_E (1-exp(-tw))].

The bounded weight and finite Poisson exponential moments justify its two derivatives. The first derivative at zero is -A and the second logarithmic derivative is -m integral_E w². Consequently

    E_Pi A=0, E_Pi A²=m E_Pi integral_E w².

The independent conditional-variance derivation checks the same statement without relying on a specialized external theorem. For T=sum_all w,

    E(T|S)=m integral_square w+A,
    Var(T|S)=m integral_D w².

Subtract the expected conditional variance from Var(T)=m integral_square w². This gives exactly the same variance of A. Conditioning a point process on its skyline does not make the skyline independent of the random region; the exact posterior is what justifies this calculation.

The lower-rectangle void probability is exp(-mxy). The product substitution then gives

    E_Pi A² = m^(-2) integral_0^m u²(log m-log u) exp(-u) du
       <= (2 log m+1/9)/m².

The constant 1/9 is integral_0^1 u²(-log u)du. Dropping the nonpositive -log u contribution for u>=1 and bounding exp(-u)<=1 on the remaining piece proves the inequality.

Under Q0, |A/m|<=2 is safely loose (a bound of one would also suffice). The RN comparison and area tail give the author's E0(A/m)² bound with coefficient 4 delta_n. Centering is not transferred. The empty skyline has A=-m/4, and its contribution is necessary to both exact Poisson identities.

## 5. Leading score, remainder and unconditioned entropy

For

    Q = [(K-mU)²-K]/(2m²)+2A/m,

two elementary square inequalities give

    Q² <= [(K-mU)^4+K²]/m^4 + 8(A/m)².

The author's resulting bound E0 Q²<=V_m/m^4+33 delta_n has the correct tail coefficient: one delta_n from the fourth count moment and 32 delta_n from the weighted term. V_m=O(log² m). The ordinary record representation applies to the baseline count and gives E0 K²<=H_n²+H_n.

The inherited local expansion is used only for K/m<=1/2 and U<=1/2. Its remainder is bounded by 40(K/m+U)^3, hence its squared integral is at most 1600 W_m^6/m^6. The sixth-power record polynomial

    h^6+15h^5+65h^4+90h^3+31h²+h

has the correct Stirling-number coefficients. Minkowski again requires no count/area independence. The remainder-square scale log^6 m/m^6 is o(log² m/m^4). The indicator restricting the residual to its valid domain is retained.

The entropy architecture of the earlier log-four result is correctly reused. The same count coupling under the Joe alternative and the fixed-count dyadic tail give both-world bad-window probability beta_m=(J+1)m^(-20). The window radius B_m=O(log² m) eventually satisfies B_m/m<=1/2 and 23(B_m/m)²<=1. On this window |log L|<=1, so phi(exp(a))<=e a²/2 converts the sharper local log-square integral into the desired bulk entropy.

Outside the window, the global bound ||log L||_(2,Q0)<=4m² follows from the exact density inequalities and the sum of 2n independent uniform-margin exponential logs. It applies to every n>=1, including near U=1, where a global Taylor remainder would fail. Cauchy–Schwarz controls the logarithm on the bad event. Importantly,

    E0[L 1_bad]=Q1({K<=n} intersect bad),

so the alternative's bad-window bound is needed for the likelihood term. The author uses it. This yields 4m² sqrt(beta_m)+2 beta_m without assuming global square integrability of L.

The common-stratum likelihood has E0 L=1-p_n, where p_n=Q1(K=m) is positive and less than 1/m!. Consequently

    KL(Q0||Q1)=E0[-log L+L-1]+p_n.

The correction is **plus p_n**. No conditional normalization removes the alternative-only skyline stratum. That stratum makes KL(Q1||Q0) infinite while the reverse logarithm remains integrable. Combining the bulk, bad-window and singular contributions gives precisely the author's explicit bound (31), with rate O(log² n/n^4). Strict positivity follows from p_n>0. The finite-n integrability proof, rather than asymptotic big-O notation, covers n=1 and the rest of the small range.

## 6. Sequential information and the started-vector contract

At a vector's first observation, reveal its complete skyline in an augmented transcript, but continue running the original policy using only its original observations. Include common randomization in that augmented history, or equivalently expose its common random kernels. A fresh independent skyline contributes D_n=KL(Q0||Q1) in conditional reverse information. Subsequent endpoint answers on an unchanged retained vector are deterministic given its revealed skyline and selected endpoint; they add zero.

This gives the finite actual-action bound D_n E0 N_T. The expectation is under world 0. It is not E1 N_T. Actual-action prefixes and dummy padding after termination are meaningful even if one vector is queried forever. Interleaving retained vectors does not alter the conditional chain rule. Counting a vector only after its within-vector query word finishes would fail to cover such paths; the author charges its first observation instead.

The events of stopping by action T and choosing world 0 increase to the terminal-world-0 event. Unconditional terminal correctness gives limiting probabilities p>=1-alpha and q<=alpha. Binary data processing, lower semicontinuity, and monotone convergence of E0 N_T yield

    D_n E0 N >= kl(p,q) >= kl(1-alpha,alpha).

Infinite expected cost causes no exception. Correctness conditional only on termination would not suffice. This proves the claimed lower bound for the declared channel; it does not supply physical exact-coordinate access, a finite reconstruction method, or information bounds for labels, mutable states, correlated resets, or other signals.

## 7. Sources, executable checks and verification boundaries

The source bindings identify the complete author result and the inspected predecessor density, record coupling, local score and its review, log-four theorem and its review, baseline moments, and probability-source packets. The exact mathematical dependencies were read in full. The general Last–Molchanov results are attributed as prior art, but no external theorem is needed as an unproved premise in this strengthening: the posterior, scalar intensity identity, and weighted identity all follow from the exact normalized skyline density. This review does not claim a new independent journal-body inspection, recursive verification of a spatial Markov theorem, a fresh exhaustive literature search, or retrospective certification of someone else's reading or research duration.

Independent controls include:

- exact ordered-simplex skyline integrations at fixed counts 0 through 4;
- normalization and coefficients through degree 4 of the scalar and weighted Poisson identities, including the empty atom;
- symbolic second- and fourth-derivative signs;
- 32 exact sixth-moment record distributions;
- 32 high-precision mode/RN cases spanning n=1 through 1,000,000, plus direct density-ratio checks and unsupported strata;
- rejection of a global constant-three RN bound outside the area window;
- six weighted-variance integral diagnostics after the product substitution;
- a finite singular-mass example rejecting zero and negative corrections;
- a finite stopped experiment rejecting E1 starts in place of E0 starts.

These are deterministic mathematical checks. They are not random samples, fitted rates, or interval-certified integrals. The written arguments carry the all-n and all-protocol claims. An initial reviewer-only test contained an incorrectly hand-entered expected value for E(K-2U)^4 at n=1. The exact integration rejected it. Direct integration of (-1+2ab)^4 gives 23/75; the test now derives and checks that value, and all controls pass. The original failed diagnostic log is retained. No author theorem was changed because of that reviewer test error.

The author controls were replayed only in `author_replay/`; their complete result JSON and stdout are byte-identical to the frozen author outputs. The replay passed exact Poisson coefficients through order 5, 156 posterior-ratio configurations, 40 maximum-mass cases, six weighted integrals, 64 exact record distributions, and seven finite scale diagnostics. `verify_review.py` checks input digest currentness, author dependency/manifest bindings, all review payload hashes, replay equality, and the independent control PASS status. This establishes currentness of the reviewed artifacts, not kernel verification of the mathematics. The receipt is restricted to this log-squared theorem and its stated transport scope; it conveys no protected-integration, audit-closure, historical-floor, physical-access, novelty, or optimality authority.
