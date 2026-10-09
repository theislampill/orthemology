# Independent review: full retained-skyline reverse KL and started-vector lower bound

8 October 2026 UTC. New scratch-only written mathematical review. No predecessor, repository, or frozen archive is changed. Historical floor remains **UNVERIFIED**. This is not formal audit closure, protected integration, kernel assurance, empirical validation, or physical-oracle certification.

## Verdict and immutable subject

**PASS for the stated O((log n)^4/n^4) reverse-KL upper bound and its scoped adaptive started-vector lower bound.** No blocking mathematical finding was identified.

Reviewed author result: `../full-skyline-reverse-kl/RESULT.md`.

SHA-256: `4aa4bee754cf89284a327d4322f4d35a93314525da8aaa22e5d028754908e28a`.

The result proves, for the declared fixed-count uniform/Joe pair,

    0 < KL(Q0 || Q1) = O((log n)^4/n^4),
    KL(Q1 || Q0) = infinity,
    E0[N] = Omega_alpha(n^4/(log n)^4)

under the author's common-policy, independent-fresh-vector, unchanged-retained-state and unconditional-terminal-correctness assumptions. The count-test upper comparator yields polynomial exponent four up to logarithmic factors for this hard pair. This review does not infer a sharp logarithmic order, a matching information asymptotic, a leading constant, or a stronger log-squared bound.

The author controls were rerun in this review's separate `author_replay/` directory. Their output is byte-identical to the frozen author's output. Independent controls import no author code and pass all eight groups. Finite numerical controls supplement the proof; the proof, not the controls, establishes the asymptotic and all-protocol conclusions.

## 1. Sources, independence, and support orientation

The exact retained-skyline density, common-support likelihood, singular mass argument, local score expansion and its review, record coupling/count test, and actual-action comparator were inspected. `SOURCE_BINDINGS.json` binds the files inspected. The parent supplied the proposed theorem and proof strategy; independence here means fresh verification and separately written controls, not blind discovery of the strategy. The current reverse-KL author text was first read after an independent derivation of the dyadic moment route, normalization correction, global logarithm bound, and stopping orientation. The independent controls were written without importing or executing author code; author replay was a separate subsequent operation.

On the ordered skyline stratum with k points, the factor `(N)_k`, without an additional k! divisor, agrees with choosing the ordered visible labels. For Q0 there are n uniform routes; for Q1 there are m=n+1 Joe routes with c=n/m. Thus on A={K<=n},

    L = m/(m-k) product_i f_c(x_i,y_i) Dc^(m-k)/D0^(n-k).

Both densities are strictly positive on each common open stratum. The entirety of the Q1-only singular part is K=m, of mass p with 0<p<1/m!, as established by the inherited strict TP2 permutation argument. Consequently Q0 is absolutely continuous with respect to Q1, while Q1 is not absolutely continuous with respect to Q0. Infinite forward KL does not invalidate finite reverse KL.

Crucially, L is the unnormalized common-stratum density, so

    E0 L = 1-p,
    E0[-log L + L - 1] = KL(Q0 || Q1) - p.

The author's **plus p** correction is correct. The conditional alternative Q1(.|A) is a different experiment, with reverse KL `D + log(1-p)`. No silent renormalization occurs. The nonnegative corrected integrand gives strict positivity directly from p>0 once finiteness is established.

## 2. Dyadic geometry and both-world tails

Let h(a) be the lowest Y among points with X<=a, or 1 if none exists. It is nonincreasing, and U is its integral. With J=ceil(log2 n) and a_j=2^(-j-1), the bands [a_j,2a_j] partition [2^(-J),1]. Monotonicity gives

    nU <= 1 + sum_j n a_j h(a_j).

The residual contribution is at most n2^(-J)<=1. The n=1 convention J=0 is correct and gives U<=1.

For T_a=na h(a), the strict tail is zero at t>=na. Below this threshold, T_a>t is exactly the no-point event for [0,a] x [0,t/(na)]. Under either fixed-count world its probability is

    (1-t/n)^n <= exp(-t).

The alternative equality uses cm=n; it does not require independence between coordinate ranks, and it is not a Poisson approximation. The h(a)=1 atom at T_a=na is handled correctly by the split at t=na. Layer cake therefore yields E T_a^4<=24. Minkowski yields the displayed fourth-norm bound for mU without any independence among the bands. A union bound separately gives P(nU>1+Jt)<=J exp(-t). These are valid under both unconditioned laws, including the alternative singular stratum.

The independent controls check exact rational geometry on 65 deterministic route configurations and exact polynomial-tail fourth moments on 35 (n,a) pairs. They include n=1, powers of two, incomplete dyadic partitions, and the terminal atom. These checks agree with the analytic derivation.

## 3. Count moments, the window, and constants

Under Q0, K has the uniform lower-record law R_n. Under Q1, the inherited conditional-quantile construction provides K<=R_m on a coupling. It does not make Joe record indicators independent. Independence is invoked only for the Bernoulli(1/r) indicators of R_m. Their factorial moments satisfy

    E(R_m)_r <= H_m^r,
    E R_m^4 <= H_m^4+6H_m^3+7H_m^2+H_m.

These identities are independently confirmed by exact Bernoulli convolution for all m=1,...,64. Combined with the area bound, they justify E_i(K+mU)^4<=M_m^4=O(log^4 m). No independence of K and U is needed.

The exact record mgf is at most exp((exp(1)-1)H_m). The author uses the slightly looser threshold exp(1)H_m+t; Markov consequently gives an even smaller tail than exp(-t), so its displayed bound is safe. Together with the dyadic union bound at t=20 log m, this proves under both laws

    P_i(G_m^c) <= beta_m = (J+1)m^(-20).

The two eventual window requirements are genuine and compatible. An explicit sufficient threshold, not needed by the author, is **m>=2^20**. Indeed, writing l=log m,

    B_m <= (40/log 2)l^2 + (exp(1)+60)l + exp(1)+2.

This uses H_m<=1+log m, J<=1+log(m)/log 2, and m/n<=2. The right-hand side divided by m is decreasing for l>=20 log 2: the numerator minus its derivative is positive there. For example, its quadratic coefficient lies between 57 and 58, linear coefficient between 62 and 63, and constant between 4 and 5, so the difference is bounded below by 57l^2-54l-59>0 for l>=13. At m=2^20, l<14 gives a conservative ratio below 12255/1048576<0.012. Hence B_m/m<1/2 and 23(B_m/m)^2<1 for every m at or above that threshold. The independent high-precision diagnostic gives an envelope ratio about 0.0114103 at the threshold, but the coarse inequalities already prove sufficiency.

For these m, G_m lies entirely in common support: K=m would force K+mU>=m>B_m. Thus no finite log likelihood is assigned to the singular stratum.

## 4. Local score to bulk entropy

The predecessor's accepted bound is |R|<=40(a+U)^3 for a=k/m<=1/2, U<=1/2. The author uses this original constant, rather than an unneeded improvement in the predecessor review. Its leading score is

    ((k-mU)^2-k)/(2m^2) + 2(sum_i x_i y_i/m - M1).

With z=a+U, k>=1 implies k/m^2<=a^2. Thus the first term has absolute value at most z^2. The geometric facts x_i y_i<=U and M1<=U^2 bound the second term by 2aU+2U^2<=2z^2. For z<=1/2,

    |log L| <= 3z^2+40z^3 <= 23z^2.

All signs, the -k correction, and constants are preserved. On G_m, the preceding window ensures |log L|<=1. Taylor's integral remainder gives

    exp(v)-1-v <= exp(1)v^2/2,  |v|<=1.

Integrating the fourth-moment bound gives the author's bulk term `(exp(1)*23^2/2) M_m^4/m^4`. Keeping the actual fourth moment inside this integral, rather than bounding it by B_m^4, is essential for the stated log^4 numerator. The author does so. No unbounded likelihood integral is obtained from convergence in probability.

## 5. Global logarithm and bad-window entropy

The global route inequalities f_c>=c, log^+ f_c<=2[-log(1-X)], and Dc>=cD0 are correct. Under Q0, let W be the sum of both negative margin logs over all n latent routes. The bound -log D0<=W follows by using any one skyline point's positive-area upper rectangle, then enlarging to the sum over all routes.

Taking absolute values in the exact likelihood yields the author's pointwise bound

    |log L| <= log m + m(-log c) + (2m-1)W
            <= 2m(1+W).

The coefficient 2m-1 comes from 2+(m-k)+(n-k)=2m+1-2k<=2m-1; it uses k>=1. Also m(-log c)<=m/(m-1)<=2. Under Q0 the 2n margin logs are independent Exp(1), so

    E0(1+W)^2 = 4n^2+6n+1 <= 4m^2,
    ||log L||_(2,Q0) <= 4m^2.

This is valid for every n>=1 and covers the boundary configurations where the local score cannot be used. A separate independent signed derivation gives log L<=log m+mW and -log L<=2+W, corroborating that there is no missing adverse sign or singular Q0 component. No Q1 logarithm on K=m is needed.

On the bad event, phi(L)<=|log L|+L+1. Cauchy-Schwarz handles its logarithm, while the likelihood term is exactly

    E0[L 1_(G_m^c)] = Q1(A intersect G_m^c) <= beta_m.

The second-world tail bound is indispensable here; a Q0 tail bound alone would be insufficient. The resulting bound

    4m^2 sqrt(beta_m) + 2 beta_m
      = O(m^(-8) sqrt(log m)) = o(m^(-4))

is correct. Adding the factorial singular correction gives the author's explicit finite bound (20). This establishes the rate with a genuine integrable-tail argument. It neither removes the singular part nor asserts global square integrability of L.

## 6. Sequential transport and terminal correctness

The complete skyline determines every endpoint comparison, including arbitrary interior thresholds. Revealing it at a vector's first observation can only add information. A rigorous augmented history includes the policy's common random seed or equivalent fresh common randomization as well as every newly revealed skyline. The original policy is simulated using its original observations, so its actual choices do not use the extra skyline data. This makes action-choice kernels common even when vectors are interleaved.

Every newly observed independent vector contributes exactly D=KL(Q0||Q1) in conditional reverse KL. All later endpoint comparisons on that same unchanged vector are deterministic given its previously revealed skyline and contribute zero. Thus the finite actual-action chain rule has cost **E0[N_T]**, as stated. The E1 orientation would be wrong. The independent finite stopped experiment explicitly rejects that wrong orientation.

Indexing by actual actions, charging at the first observation, and dummy padding after termination keep the argument valid even on paths whose within-vector query sequence never ends. No completion assumption for every word is smuggled in. A nonterminating path is not counted as a correct terminal decision. From the unconditional success conditions, the increasing events of accepting Q0 by action T have limiting probabilities p>=1-alpha and q<=alpha. Binary data processing, lower semicontinuity, and monotone convergence then give

    D E0[N] >= kl(p,q) >= kl(1-alpha,alpha).

Infinite E0[N] satisfies this trivially. Correctness conditional only on termination would not imply it.

The optional uncharged one-shot allowance is narrowly limited to distinct independent vectors with identical conditional endpoint laws and no later replay. Any candidate vector that may be retained must be charged from its first observation, preventing selection-based retroactive exemptions. Counting every vector started is the simpler headline convention. The argument would not extend to world-dependent policies, correlated resets, mutable vectors, route labels, gate bits, or other non-skyline information.

For the stipulated two-world problem, a fixed-budget count test provides the inherited O_alpha(n^4/log n) upper bound, while this result gives the matching polynomial exponent from below up to logarithms. It does not prove a corresponding upper bound over arbitrary alternatives or for finite-precision physical instruments.

## 7. Executable controls, receipt, and boundaries

Independent diagnostics passed:

- 65 exact rational dyadic-geometry configurations;
- 35 exact fourth moments from the height-tail polynomial, including the terminal atom;
- 64 exact record distributions, fourth-moment inequalities, and mgf bounds;
- an analytically justified all-m window threshold m>=2^20;
- 87 deterministic exact-likelihood configurations, including large-area boundary sequences;
- 1000 arithmetic checks of the global logarithm second-moment envelope;
- singular-mass correction controls rejecting both the zero and negative correction;
- a stopped reverse-KL identity rejecting E1[N] in place of E0[N].

The author replay separately passed 64 record sizes, 160 height cases, 74 skyline configurations, 33 local-window cases, and 63 stopped terminal words. Its generated result is byte-identical to the bound source output.

`verify_review.py` verifies source digests, author manifest/dependency currentness, review payload digests, replay equality, the independent control result, and the bounded review receipt. This is artifact currentness verification, not formal proof checking. PASS applies only to the exact bound input bytes and to the claims reviewed above. There is no integration authorization, closure authority, historical-floor certification, physical access claim, field-wide novelty claim, or log-squared strengthening.
