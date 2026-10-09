# Full retained-skyline reverse KL has at most a fourth-power information rate

8 October 2026 UTC. New scratch-only sibling. Historical floor remains UNVERIFIED. No predecessor or archive is modified; no protected integration, empirical validation, physical-access claim, kernel assurance, or T20 closure is asserted.

## Result and observation contract

Let n≥1, m=n+1, c=n/m. Under P0 there are n iid product-uniform points (X,Y) in (0,1)². Under P1 there are m iid points with

    F_c(x,y)=1−(1−xy)^c,
    f_c(x,y)=c(1−xy)^(c−2)(1−cxy).

The retained endpoint response is 1{some route has X≤a and Y≤b}. A vector is unchanged during all its queries. Let S be its whole coordinatewise-minimal skyline and K=|S|. The exact ideal endpoint function and S determine each other. They reveal neither labels nor the dominated routes. Write Q0,Q1 for the laws of S. All logarithms below are natural unless a base is specified.

For this fixed-count hard pair,

    0 < D_n := KL(Q0 || Q1) = O((log n)^4/n^4),     n→∞.       (1)

The opposite divergence remains infinite at every n. Equation (1) is an unconditioned reverse-KL bound: the Q1-only event K=m is retained, with its exact mass correction. No exact logarithmic order or leading constant is claimed.

Consequently, for fixed 0<α<1/2, every common adaptive retained-interior testing protocol with fresh independent vectors and unconditional terminal correctness as specified in section 7 satisfies

    E0 N ≥ kl(1−α,α)/D_n = Ω_α(n^4/(log n)^4),                (2)

where N counts every independent retained vector started, including one whose query sequence never finishes. Arbitrarily selected endpoint thresholds, arbitrarily long queries on a retained vector, and interleaving already started vectors do not evade this bound. It also applies to a protocol that receives the whole exact skyline at each start. This is an information envelope, not a claim that exact real-valued skyline readout can be implemented by finitely many physical queries.

The predecessor count test has the fixed-budget upper bound O_α(n^4/log n) in the ideal skyline channel. Thus the worst-case independent-vector cost for the stipulated hard pair has polynomial exponent four, up to logarithmic factors. A possible logarithmic gap remains; no O(n^(4−ε)) worst-case cost is possible for any fixed ε>0 and fixed error tolerance in this channel. The upper bound is not silently transferred to finite-probe or noisy implementations.

## 1. Exact likelihood and the singular mass correction

For an ordered k-point skyline s, let D(s) be its upper dominated region, E(s) its lower undominated complement, U=area(E), D0=1−U, and Dc=∫_D f_c. The exact normalized skyline density from the retained-skyline-likelihood packet is

    g_(N,f),k(s)=(N)_k ∏_i f(x_i,y_i) [∫_D f]^(N−k)

with ordinary Lebesgue measure on 0<x1<⋯<xk<1 and 1>y1>⋯>yk>0, and counting measure over k. There is no extra k! divisor. For A={K≤n}, the common-stratum likelihood is

    L(s)=g1(s)/g0(s)
        =m/(m−k) ∏_i f_c(x_i,y_i) Dc^(m−k)/D0^(n−k).        (3)

Every factor is strictly positive on A. Under Q0, A has probability one. Under Q1 its complement is precisely {K=m}, of mass

    0<p_n:=Q1(K=m)<1/m!.                                   (4)

The predecessor proves (4) by strict TP2 rearrangement; the alternative-only stratum is the entire singular component of Q1 relative to Q0. Therefore

    E0 L = 1−p_n,      KL(Q1 || Q0)=∞.                       (5)

Let φ(v)=−log v+v−1≥0 for v>0. Finiteness of the reverse logarithm is proved in section 5. Exact integration then gives

    D_n=E0[−log L]=E0 φ(L)+p_n.                             (6)

In particular the correction is +p_n, not −p_n or zero. No conditioning on A is used anywhere in the theorem. For comparison only, conditioning Q1 on A would change its likelihood to L/(1−p_n) and its reverse KL to D_n+log(1−p_n); that is a different experiment.

## 2. Dyadic area bounds under both laws

For one latent vector define

    h(a)=min{Y_j:X_j≤a}, with h(a)=1 if this set is empty.

This is a nonincreasing height function and U=∫_0^1 h(x) dx, up to measure-zero boundaries. Set

    J=⌈log₂ n⌉,     a_j=2^(−j−1),     j=0,…,J−1.

The bands [a_j,2a_j] partition [2^(−J),1]. Their heights are at most h(a_j), while the residual interval has area at most 2^(−J)≤1/n. Hence, pathwise,

    nU ≤ 1+Σ_(j=0)^(J−1) T_j,       T_j=n a_j h(a_j).       (7)

For n=1 the sum is empty and the inequality remains true. For a∈(0,1), t≥0 and T_a=na h(a), if t≥na then P(T_a>t)=0. Otherwise b=t/(na)<1 and

    P_i(T_a>t)
      =P_i(no route in [0,a]×[0,b])
      =(1−ab)^n=(1−t/n)^n≤exp(−t),       i=0,1.            (8)

Under P1 the exact equality uses [1−F_c(a,b)]^m=(1−ab)^(cm) and cm=n. This is a fixed-count equality, without Poissonization. The possible atom h(a)=1 does not invalidate the strict-tail formula for b<1; at t≥na the event is impossible.

The layer-cake formula gives E_i T_a^4≤4!=24. Minkowski's inequality applied to (7), which requires no independence among the bands, yields

    ‖mU‖_(4,i) ≤ (m/n)[1+J 24^(1/4)],       i=0,1.         (9)

A union bound also gives, for every t≥0,

    P_i(nU>1+Jt)≤J exp(−t).                               (10)

The formula is valid with J=0 as well. No independence of h(a_j), or of area and count, is assumed.

## 3. Count moments and a simultaneous polynomial-tail window

Let R_m be the ordinary lower-record count of m independent continuous uniform variables. Its record indicators are independent Bernoulli(1/r), r=1,…,m. Under Q0, K has the R_n law and can be coupled below R_m. Under Q1 the verified quantile-record coupling in skyline-count-information gives K≤R_m almost surely on a coupling. In brief, conditional Y given increasing X is stochastically increasing because f_c is TP2. Ordered conditional quantiles Q_j satisfy Q_j(u)≤Q_i(u) for j<i. Consequently a lower record of Y_i=Q_i(V_i) can occur only when the independent uniform V_i is a lower record. This supplies simultaneous indicator domination; it does not assert that the Joe records are independent.

Write H=H_m. For each positive integer r, independence of the uniform record indicators gives

    E(R_m)_r=r! Σ_(i1<⋯<ir) 1/(i1⋯ir)≤H^r.

Since x^4=(x)_4+6(x)_3+7(x)_2+x, under either skyline law,

    E_i K^4 ≤ H^4+6H^3+7H²+H.

Combining this with (9), define

    M_m=(H^4+6H^3+7H²+H)^(1/4)
          +(m/n)[1+J 24^(1/4)]=O(log m).

Then

    E_i(K+mU)^4 ≤ M_m^4=O((log m)^4),       i=0,1.          (11)

For tails, with e₀=exp(1),

    E exp(R_m)=∏_(r=1)^m[1+(e₀−1)/r]≤exp((e₀−1)H).

Markov and the coupling imply P_i(K>e₀H+t)≤exp(−t). Together with (10), put

    t_m=20 log m,
    B_m=e₀H+t_m+(m/n)[1+Jt_m],
    β_m=(J+1)m^(−20),
    G_m={K+mU≤B_m}.

Then, simultaneously under the two unconditioned laws,

    Q_i(G_m^c)≤β_m,       i=0,1.                           (12)

Here B_m=O((log m)²). Eventually B_m/m≤1/2, so G_m lies entirely in A, with K/m≤1/2 and U≤1/2. The alternative-only stratum is not discarded: it is outside this good window and its separate mass occurs in (6).

## 4. Bulk entropy from the verified local score

For a skyline in A put a=k/m and z=a+U. The digest-bound skyline-likelihood-score result, accepted by its independent review, gives whenever a,U≤1/2,

    log L = ((k−mU)²−k)/(2m²)
              +2[Σ_i x_i y_i/m−M1]+R,
    M1=∫_E xy dxdy,       |R|≤40z³.                       (13)

Its geometric inequalities are x_i y_i≤U and M1≤U². For z≤1/2, the first term in absolute value is at most z²: use |a−U|≤z and k/m²≤a², since k≥1. The second term is at most 2aU+2U²≤2z². Therefore

    |log L|≤3z²+40z³≤23z².                               (14)

The independent review actually proved a smaller remainder constant, but no strengthening is needed here. Eventually 23(B_m/m)²≤1 as well. Thus on G_m, |log L|≤1. For |v|≤1, Taylor's integral remainder gives

    φ(exp(v))=exp(v)−1−v≤(e₀/2)v².

Using (11) and (14), for all sufficiently large m,

    E0[φ(L)1_(G_m)]
      ≤(e₀ 23²/2) E0[(K/m+U)^4]
      ≤(e₀ 23²/2) M_m^4/m^4.                             (15)

The fourth moment, rather than replacing K+mU by the O(log²m) window radius inside the expectation, preserves the O(log⁴m) numerator. There is no claim of global square-integrability of L itself.

## 5. A global logarithm bound, used only for the bad-window entropy

Let the n underlying uniform routes under P0 be (X_r,Y_r), and set

    W=Σ_(r=1)^n[−log(1−X_r)−log(1−Y_r)].

For c≥1/2, the exact route density satisfies

    f_c≥c,
    log⁺f_c(x,y)≤2[−log(1−x)],
    Dc≥cD0.                                               (16)

Indeed 1−cxy≥1−xy implies f_c≥c; omitting the two nonpositive terms log c and log(1−cxy) bounds log⁺f_c by (2−c)[−log(1−xy)], then by 2[−log(1−x)]. Every nonempty skyline contains a point whose upper rectangle has area (1−x_i)(1−y_i), so

    −log D0≤W.

Take absolute values termwise in the logarithm of (3). Because 1≤k≤n, log[m/(m−k)]≤log m and n−k≥0. From (16),

    |log L|
      ≤log m+k(−log c)+2W+(m−k)(−log c−log D0)
                             +(n−k)(−log D0)
      ≤log m+m(−log c)+(2m−1)W
      ≤2m(1+W).                                           (17)

The last inequality uses m(−log c)≤m/(m−1)≤2 and log m+2≤2m. This is a global bound on the entire common support, including the boundary where the local expansion cannot apply.

Under P0, W is the sum of 2n independent Exp(1) variables, so

    E0(1+W)²=4n²+6n+1≤4m²,
    ‖log L‖_(2,0)≤4m².                                   (18)

In particular the reverse logarithm is absolutely integrable for every n. No corresponding unconditioned Q1 logarithm exists on K=m, and none is used.

Since φ(L)≤|log L|+L+1, Cauchy–Schwarz, (5), and (12) give

    0≤E0[φ(L)1_(G_m^c)]
      ≤4m²√β_m+Q1(A∩G_m^c)+Q0(G_m^c)
      ≤4m²√β_m+2β_m
      =O(m^(−8)√log m)=o(m^(−4)).                          (19)

The Q1 tail probability here is essential: E0[L1_(G_m^c)] is the alternative mass on that common-support event. Controlling only the Q0 probability would not justify (19).

## 6. The reverse-KL bound

Combining the exact identity (6), the bulk bound (15), the tail bound (19), and (4), for all sufficiently large m,

    0<D_n
      ≤(e₀ 23²/2) M_m^4/m^4
          +4m²√β_m+2β_m+1/m!.                            (20)

Strict positivity follows already from D_n=E0φ(L)+p_n and p_n>0. The factorial term is o(m^(−4)), while M_m=O(log m). This proves (1). Finiteness for every fixed n follows from (18), so no small-n exceptional divergence is hidden in the asymptotic statement.

The proof does not replace the infinite forward KL by a finite one, does not normalize away the singular event, does not use Monte Carlo evidence, and does not extend a localized Taylor expansion beyond its window. The singular mass and the common-support entropy are handled separately and exactly.

## 7. Arbitrary retained-interior queries and actual-action stopping

Given a complete skyline s, every endpoint answer at (a,b) is the deterministic Borel function

    H_s(a,b)=1{some (x,y)∈s has x≤a and y≤b}.

Thus a common randomized adaptive query policy on one unchanged vector, including every next endpoint and its stopping decisions, can be simulated from s and the policy's common randomization. The statement remains true for endpoints selected from earlier answers and for any finite number of actions. For a lower bound we may reveal s as extra information; no assertion of finite exact recovery is needed.

Consider protocols built from fresh independent latent vectors, retaining each unchanged whenever it is revisited. All newly started vectors have the stated world-specific law independently of previous vectors and the policy randomization. The policy is a common measurable rule in both worlds. It can interleave queries to different retained vectors. Charge each independent vector at its first observation, even if its query sequence never finishes. Counting vectors earlier, when allocated or drawn, can only increase the cost.

Augment the transcript by revealing the whole skyline at that first observation. Continue to simulate the original policy while ignoring the extra information in its decisions. Every new reveal contributes exactly D_n conditional reverse KL. Later queries on that vector are deterministic functions of its already revealed skyline and selected endpoint, so they contribute zero additional conditional information. Action choices, stopping rules, and policy randomization use the same kernels in both worlds. After termination pad by a common dummy symbol.

Let N_T be the number of independent vectors started by the first T actual actions. The chain rule on this augmented finite history gives

    KL(Law0(history_T) || Law1(history_T))
       ≤D_n E0 N_T.                                       (21)

Using actual-action prefixes makes N_T and the history meaningful even on a path that queries one vector forever. A proof indexed only by completed within-vector words would not suffice without extra termination assumptions. Reverse orientation is why the expected cost in (21) is under P0.

If separately allowed, fresh one-shot endpoint-only observations on distinct independent vectors can be left uncharged only when their conditional law is identical in the two worlds and the vectors are never replayed. They then add zero conditional information. Any vector that may subsequently be retained or replayed must instead be covered from its first observation; selective retention cannot leave an informative earlier observation uncharged. Counting every vector, including these one-shot observations, is the simpler sufficient convention.

Require unconditional terminal correctness:

    P0(stop after finitely many actual actions and decide P0)≥1−α,
    P1(stop after finitely many actual actions and decide P1)≥1−α,
    0<α<1/2.                                               (22)

For E_T={stop within T actual actions and decide P0}, binary data processing in (21) gives the lower bound kl(P0(E_T),P1(E_T)). These events increase to the terminal-P0 event. Its probabilities satisfy p≥1−α and q≤α by (22). Monotone convergence of E0 N_T, lower semicontinuity of binary KL, and its monotonicity for p>q imply

    D_n E0 N≥kl(p,q)≥kl(1−α,α).

This proves (2), with infinite expected cost satisfying it trivially. Accuracy only conditional on termination would not imply this conclusion. No almost-sure completion of every query sequence is assumed.

For any procedure required to distinguish all relevant alternatives, this particular pair is an admissible hard case, so its worst-case expected started-vector cost is at least (2). This is a statistical lower bound for the declared iid family and retained observation interface, not distribution-free actual-route-count identification, a practical instrument theorem, or a claim about gate bits, route labels, mutated states, noisy readout, or other channels.

## 8. Verification, attribution, and limits

The parent supplied the reverse-KL candidate, dyadic decomposition, proposed fourth-moment and tail strategy, and the requested actual-action transport scope. This packet verifies all directions and constants, proves the displayed finite bound (20), and supplies the adaptive lower bound. The inherited density, singular support, record coupling, count upper test, and local likelihood expansion remain attributed to their bound source packets; the local score's completed review is additionally bound. No external source is needed for the proof, and no field-wide novelty claim is made.

controls.py contains deterministic checks of the dyadic geometry, exact rational record moments, exact rational height moments, likelihood bounds at fixed skylines, the sign of the singular correction, and a finite stopped-experiment reverse-KL chain-rule example. CONTROL_RESULTS.json and CONTROL_RUN.log retain the outputs. These are arithmetic diagnostics, not empirical samples, a fit to an asymptotic rate, or certified numerical interval proofs. The written inequalities establish the all-n asymptotic result. SOURCE_AUDIT.md and SOURCE_BINDINGS.json record inspection and scope. A fresh independent review must bind the final RESULT.md digest before acceptance.
