# Full face-threshold readout has infinite chi-square but finite forward KL

8 October 2026 UTC. New scratch-only successor. Earlier packets are read-only. This is a conditional observation-channel result, not an instrument feasibility claim, empirical validation, protected integration, or T20 closure.

## 1. Exact result and observation contract

Fix an integer n>=1, put m=n+1 and c=n/(n+1). Use exactly the two worlds from arbitrary-face-replay-design:

- P0: n independent route pairs, with independent uniform A and B thresholds within every pair.
- P1: m independent route pairs, each having joint threshold CDF H_c(ab), where H_c(t)=1-(1-t)^c. Within-route dependence is the previously identified Joe construction; its coordinate threshold CDFs are H_c.

A single ideal observation returns the two minimum thresholds T_A and T_B of one retained route-threshold vector. It is equivalent, as a mathematical information channel, to access to every coordinate-face comparison on that vector. The face endpoint at (a,1) reports whether T_A<=a, and (1,b) whether T_B<=b. Rational comparisons already determine the minima. This is not access to each individual route threshold or to route labels, and it is not an assertion that a finite number of probes reveals a real number exactly.

Write X=1-T_A, Y=1-T_B. In these coordinates the laws have CDFs

    F0(x,y)=x^n y^n,
    F1(x,y)=S(x,y)^m,
    S(x,y)=x^c+y^c-(x+y-xy)^c,              0<=x,y<=1.       (1)

Both margins are Beta(n,1): P_i(X<=x)=x^n and P_i(Y<=y)=y^n. For the full two-minimum observation, in the orientation P1 relative to P0,

    chi²(P1||P0)=infinity,                                  (2)
    0<KL(P1||P0)<=2+log(1+1/[n(n+1)])
                   <=2+log(3/2)<2+log 3.                   (3)

Natural logarithms are used. The strict positivity follows because the laws differ, and the absolute continuity and finite upper bound are proved below. No asymptotic order in n of KL is asserted.

For each fixed n there are finite, increasingly resolved retained-face transcripts whose chi-square divergences increase without bound. Section 4 gives an explicit (K+1)-cell quantization, obtainable with at most 2K face probes on the same vector, and proves

    chi²(P1,K||P0,K)/K -> d_n>0,
    d_n=(2-2^c)^(2m) (1-2^(-n))/(1+2^(-n)).                 (4)

Every fixed finite partition has finite divergence. The limit is K->infinity at fixed n, not a joint n/K optimization or a claimed physical precision budget.

## 2. CDF, density, and boundary checks

In one Joe route, the probability that both thresholds exceed 1-x and 1-y is S(x,y), by inclusion-exclusion from H_c. Route independence gives F1=S^m. The corresponding product route tail is xy and gives F0. Thus (1) follows from the inherited fixed-threshold coupling; no separate contextwise tables are being assumed.

Set z=x+y-xy. In the open square,

    S_x=c[x^(c-1)-(1-y)z^(c-1)]>0,
    S_y=c[y^(c-1)-(1-x)z^(c-1)]>0,
    S_xy=c z^(c-2)[1-c(1-x)(1-y)]>0.                       (5)

For example z>=x and c-1<0 give z^(c-1)<=x^(c-1); multiplication by 1-y<1 proves S_x>0. Also 0<S<=min(x^c,y^c)<=1, either from its route-tail interpretation or from the inherited positive route density and event inclusion. Differentiating (1) gives

    f1=m(m-1)S^(m-2)S_x S_y + m S^(m-1)S_xy>0,
    f0=n² x^(n-1)y^(n-1)>0.                               (6)

These formulas are asserted on the open square only. They can diverge near corners; no finite boundary value is required. Since m>=2, the displayed nonnegative powers create no exceptional case at n=1.

The CDF is continuous on the closed square. It is grounded on x=0 or y=0, has total value 1 at (1,1), and has margins x^n,y^n because S(x,1)=x^c and S(1,y)=y^c. These continuous margins give zero probability to every boundary line. On compact interior rectangles, the density integral equals the rectangular CDF increment by the fundamental theorem of calculus. Let such rectangles increase to the whole open square: their increments tend to 1 by continuity and the boundary values. Monotone convergence therefore gives integral f1=1 and accounts for the entire law, with no residual singular component. The same is immediate for f0. In particular P1 and P0 are mutually absolutely continuous and L=f1/f0 is well defined almost everywhere. Absolute continuity does not imply L is square integrable.

## 3. Infinite chi-square without a density asymptotic

For 0<r<=1 let E_r={(X,Y):X<=r,Y<=r}. Put

    L_n(r)=[2-(2-r)^c]^m,
    lambda_n=L_n(0)=(2-2^c)^m>0.                           (7)

Then the exact corner probabilities are

    P0(E_r)=r^(2n),   P1(E_r)=r^n L_n(r).                   (8)

Hence P1(E_r)/sqrt(P0(E_r))=L_n(r)->lambda_n>0 as r decreases to zero. Suppose chi²(P1||P0)<infinity. Since E0 L=1, this is equivalent to E0 L²<infinity. Cauchy-Schwarz localized to E_r would give

    P1(E_r)/sqrt(P0(E_r))
       <=[integral_(E_r) L² dP0]^(1/2) ->0.               (9)

The last limit is the absolute continuity of the integral of the integrable function L² on shrinking events; equivalently dominated convergence, since E_r decreases to the null point (0,0). This contradicts (8), proving (2). No derivative asymptotic is needed.

This is a direct transport of classical positive tail dependence versus independence. The one-route upper-tail coefficient in uniform marginal coordinates is the classical Joe value 2-2^(1/theta), with theta=1/c. For minima over m independent routes its power gives lambda_n. The Joe family and tail-dependence formula are inherited mathematics, as documented by the [VineCopula authors' tail-dependence reference](https://tnagler.github.io/VineCopula/reference/BiCopPar2TailDep.html), Joe row 6. The local specialization and information-channel boundary are proved here; no field-wide novelty is claimed.

## 4. An explicit finite-resolution witness

Let r_k=2^(-k), E_k=E_(r_k), and for K>=1 partition the square into

    A_k=E_k minus E_(k+1),  0<=k<K,
    A_K=E_K.                                                 (10)

E_0 is the whole square modulo null boundary conventions. Define h=2^(-n). The cell probabilities for k<K are

    p_k=r_k^(2n)(1-h²),
    q_k=r_k^n[L_n(r_k)-h L_n(r_(k+1))],                      (11)

and for the last cell

    p_K=r_K^(2n),   q_K=r_K^n L_n(r_K).                       (12)

All p_k and q_k are strictly positive. The function L_n(r) increases with r and is at least lambda_n. Therefore

    q_k >=r_k^n(1-h)lambda_n,
    q_k²/p_k >=lambda_n² (1-h)/(1+h)=d_n,
    q_K²/p_K=L_n(r_K)²>=lambda_n².                          (13)

Since chi²=Σ q_k²/p_k-1, for every finite K,

    chi²(P1,K||P0,K)>=K d_n+lambda_n²-1.                    (14)

The bound may be negative for small K and then is simply weaker than nonnegativity. It proves unboundedness because d_n>0. More sharply, each shell contribution q_k²/p_k tends to d_n as k->infinity, while the final contribution tends to lambda_n². Cesaro averaging yields (4). These partitions are nested refinements, so their chi-square divergences are nondecreasing by the elementary weighted Cauchy-Schwarz inequality for splitting a cell.

The finite instrument can ask both face comparisons at each a=b=1-r_k, k=1,...,K, retaining the same vector throughout. Both absence bits equal 1 exactly on E_k, up to null equality events. Thus at most 2K probes determine (10), even if the remaining transcript information is discarded. Commands have dyadic denominators up to 2^K. This states one explicit sufficient command/probe budget; it is not a minimal budget, a noisy-actuator guarantee, or a finite method for exact continuous readout. Since the law of this partition is a deterministic function of that finite transcript, the transcript chi-square is at least the quantity in (14).

Every fixed deterministic finite face word has a finite outcome alphabet and finite chi-square here: P1<<P0 implies zero P0 cells also have zero P1 mass, and every nonzero P0 cell in a finite alphabet has a positive denominator. The explicit transcripts above therefore have finite, not infinite, chi-square at each finite K. By data processing their forward KL remains bounded by (3), regardless of K. An infinite chi-square limit does not imply an infinite KL limit.

## 5. A finite forward-KL envelope, including n=1

From (5), since z>=x,y, xy<=z², and 0<z<=1,

    0<S_x<=c/x,  0<S_y<=c/y,
    0<S_xy<=c z^(c-2)<=c/(xy).                             (15)

For the last inequality, xy z^(c-2)<=(z²)z^(c-2)=z^c<=1; also the omitted bracket 1-c(1-x)(1-y) lies in (0,1]. Since S<=1 and m>=2, (6) gives

    f1<=[m(m-1)c²+mc]/(xy)=C_n/(xy),
    C_n=n²+n/(n+1).                                         (16)

Consequently

    log(f1/f0)<=log(C_n/n²)-n log x-n log y.                 (17)

The right side is nonnegative and has finite P1 expectation. The shared Beta(n,1) margins give E1[-log X]=E1[-log Y]=1/n, so the positive part of log(f1/f0) is integrable and its expectation is at most log(C_n/n²)+2. The negative part is also integrable: on L<1,

    integral f1 log(f0/f1)
       =integral_(L<1) f0[-L log L] <=1/e.                  (18)

Thus forward KL is an ordinary finite integral and (17) proves (3). This is a slightly tighter realization of the proposed crude f1<=3n²/(xy) envelope.

At n=1, m=2,c=1/2, the constant is C_1=3/2 and the bound is 2+log(3/2). The corner constant is lambda_1=(2-sqrt(2))²>0, so the infinite-chi-square proof applies without an n>1 assumption. The independent-reference density is then exactly 1. At the separate equality control m=n,c=1, S=xy and F1=F0, so both divergences are zero; the obstruction requires m>n and is not silently applied at c=1.

## 6. What changes, and what does not

1. The frozen all-rate theorem and its adaptive-two-face successor remain correct for their stated interfaces: at most two face probes per independent vector, including a second choice based on the first bit, with charged first probes. Their all-rate bound is 32768/n^4; their sharp nonadaptive chi-square constant is approximately 0.4193990202/n^4.
2. That uniform chi-square bound cannot be extended to unrestricted retained-face words, or to exact two-minimum readout, without an additional word-length/resolution restriction. For each fixed n, (14) eventually exceeds any finite proposed bound.
3. This does not refute the n^4 expected-sample lower bound for the old two-probe experiment. Nor does it prove a better exponent for the stronger experiment: the earlier lower bound used KL, and infinite chi-square alone supplies no lower bound on KL, total variation, power, or achievable testing cost.
4. The constants lambda_n and d_n depend strongly on n. A fixed-n K->infinity statement is not uniform in n. No sample-complexity improvement or recommended testing design is inferred from rare tail shells.
5. The full readout theorem is about coordinate minima, not the full latent vector, latent route identity, arbitrary interior endpoint replay, unknown calibrations, changing threshold states, or a physical device. Finite binary search or noisy readout requires its own precision, retained-state, selectable-rate, and probe-cost analysis.
6. The coarse KL envelope is not a sharp KL asymptotic, an optimal test, or a reverse-KL statement. It deliberately prevents conflating failure of a chi-square upper bound with information divergence in every measure.

## 7. Attribution and verification status

The parent supplied the exact-readout question, shrinking-corner L2 obstruction, and candidate crude KL envelope. The author verified the laws and boundary/absolute-continuity details, tightened the density constant, and derived the explicit nested-shell finite-resolution witness. Classical copula, tail-dependence, Cauchy-Schwarz, absolute-continuity-of-integrals, and divergence facts are inherited.

SOURCE_AUDIT.md distinguishes local reads, targeted external inspection, and unread bibliographic ancestors. CONTROL_RESULTS.json records bounded exact and numerical controls; these are checks of formulas, not empirical sampling or a replacement for the proofs. A separate independent review must be bound to the final RESULT.md hash before acceptance.
