# Finite geometric-score probes attain the sharp vector order

8 October 2026 UTC. New scratch-only candidate. Historical floor remains **UNVERIFIED**. No prior packet or checkpoint is changed. This is a written mathematical proof with exact deterministic controls, awaiting a fresh independent final-digest-bound review. It is not protected integration, a formal-kernel theorem, an empirical experiment, physical-access certification, or closure.

## Result and qualification

Put m=n+1 and h=H_n. Under the known hypotheses, world 0 has n iid product-uniform routes in (0,1)^2; world 1 has m iid routes with CDF F_c(x,y)=1-(1-xy)^c, c=n/m. Vectors are freshly and independently reset; all queries within a vector concern that unchanged retained vector. The noiseless endpoint oracle returns whether at least one route is coordinatewise at most the queried endpoint.

Let K be the number of distinct coordinatewise-minimal routes, U the area of the lower undominated region, and define

    J=(K-mU)^2-K,                b_n=E0 J.

For this pair,

    E1 J-E0 J ~ h^2/m^2,
    Var0 J ~ 2h^2,              Var1 J ~ 2h^2.                (1)

The previous finite grid extractor already returns enough staircase geometry to approximate J; no extra instrument or hidden route-count observation is required. For fixed rational alpha,eta>0 with alpha+eta<1, the following explicit rational/integer prescription has error at most alpha+eta in each world for all sufficiently large n:

    R = ceil(192m^4/(alpha h^2)),
    L = max(ceil(32m^5/h^2), ceil([m(m-1)R/eta]^(m/n))),
    threshold = b_n+h^2/(4m^2).                              (2)

Every ceiling in (2) is implemented by exact integer arithmetic, as specified below. Extract the grid skyline on each of R fresh vectors, compute its exact rational score J_L, and choose world 1 iff the average score is at least threshold. All R vectors are charged from their first observation. Every run terminates after finitely many endpoint probes.

At fixed error epsilon<1/2, take alpha=eta=epsilon/2, or rational choices summing to at most epsilon. The independent-vector upper bound is O_epsilon(m^4/log^2 m). The sharp predecessor's lower bound applies to this same finite-endpoint class, so the optimal independent-vector order is Theta_epsilon(m^4/log^2 m), including expected baseline started-vector cost and maximum of the two expected costs. This matching statement concerns independent vectors. The present construction has only the following total-query upper bounds:

    expected total endpoint probes: O_epsilon(m^4),
    deterministic worst-case total probes: O_epsilon(m^5/log m).

No total-query optimality is asserted.

**Eventual guarantee only.** The score moment proof establishes the existence of a sufficiently large cutoff n0, but this packet does not compute or certify n0. Formula (2) is a finite, executable prescription for each supplied n>=2; its advertised error guarantee is proved only eventually. It must not be sold as an all-n certified deployment budget. An all-n fallback is the already established finite skyline-count test, at its older vector rate. The n=1 case can use that existing rational count protocol separately. No exact noncomputable skyline observation, affinity evaluation, likelihood-ratio comparison, or unspecified real-number oracle is used in the implemented score test.

## 1. Consumed sharp ingredients and their status

SOURCE_BINDINGS.json binds the exact source bytes. The sharp RESULT.md has SHA-256 52a9c53ca5d1765de2956e685701532529efca9a0292165f8f9e738b43b7a870. A now-present independent PASS receipt binds that digest and its manifest. Its author's older manifest still says review-pending; this packet records the later receipt rather than silently rewriting that history. Currentness of all bound files and the receipt's author/review hashes is checked by the controls. That predecessor review does not review this new test.

We consume these specific claims from the sharp packet, rather than inferring moment convergence from an information rate alone. Write M=K-mU, A=sum_(s in skyline) xy-m integral_E xy, and

    Q=J/(2m^2)+2A/m.

Under world 0,

    E0 J^2 ~ 2h^2,             E0(A/m)^2=O(h/m^4).           (3)

There are events G_m={K+mU<=B_m}, with B_m=O(log^2 m), such that eventually G_m lies in common support, and

    Q0(G_m^c), Q1(G_m^c) <= beta_m,
    beta_m=(ceil(log_2 n)+1)m^(-20),
    sup_Gm |log L| -> 0,
    ||(log L-Q)1_Gm||_(2,Q0) = o(h/m^2),
    ||(log L)1_Gm||_(2,Q0) = O(h/m^2).                    (4)

Here L=dQ1,common/dQ0 is the actual sub-probability common-support likelihood. It is not renormalized. The alternative-only stratum K=m has positive mass and is eventually contained in G_m^c. The sharp proof obtains (3) through a sixth-moment uniform-integrability bound and a restricted fixed-count/Poisson density comparison; it does not transfer an unproved Poisson equality to the fixed-count law. Its both-world tails in (4) are essential below.

For the algebraic global bound, 0<=K<=m and 0<=U<=1 imply |M|<=m and

    |J|<=m^2                                                    (5)

under either world, including the singular stratum. The source also supplies the deliberately loose |Q|<=5 on baseline support. The baseline moment source gives the exact centering in section 3. These are the only moment/likelihood inputs needed for the new mean test. In particular no alternative fourth-moment formula is assumed.

## 2. Deriving the score signal and both variances

On G_m write a=log L. For |a|<=epsilon_m with epsilon_m->0, the elementary exponential remainder gives |exp(a)-1-a|<=C epsilon_m |a|, with a fixed C eventually. Together with (4),

    ||(L-1-Q)1_Gm||_2 = o(h/m^2).                         (6)

Cauchy-Schwarz, (3), and (6) yield

    E0[J(L-1)1_Gm] = E0[JQ1_Gm]+o(h^2/m^2).              (7)

The mixed term is lower order:

    |2E0[JA/m]| <= 2||J||_2 ||A/m||_2
                 =O(h^(3/2)/m^2)=o(h^2/m^2).

Consequently

    E0 JQ = E0 J^2/(2m^2)+2E0[JA/m] ~ h^2/m^2.           (8)

By (5), |Q|<=5, and the baseline tail, replacing E0[JQ1_Gm] by E0 JQ costs at most 5m^2 beta_m=o(h^2/m^2). Exact change of measure on G_m and the two full-law tails give

    E1 J-E0 J
      = E0[J(L-1)1_Gm]+E1[J1_(G_m^c)]-E0[J1_(G_m^c)],
    |E1[J1_(G_m^c)]-E0[J1_(G_m^c)]|<=2m^2 beta_m.        (9)

This includes every alternative singular observation; none is silently discarded. Equations (7)-(9) prove the first part of (1).

Likewise the uniform convergence L->1 on G_m and (3) give

    E1[J^2 1_Gm]=E0[J^2 L1_Gm] ~ 2h^2.

The two omitted second-moment tails are at most m^4 beta_m=o(h^2), by (5). Thus E1 J^2~2h^2 as well. Section 3 gives b_n=O(h^2/m)=o(h), while the just-proved shift is O(h^2/m^2)=o(h). Both squared means are therefore o(h^2); subtraction from the raw moments proves both variance equivalents in (1).

There exists a finite n0 such that for all n>=n0,

    Delta_n:=E1 J-b_n >= h^2/(2m^2),
    Var0 J<=3h^2,                Var1 J<=3h^2.             (10)

The following finite-test proof needs only (10). The derivation above proves existence, not an effective numerical value of n0.

## 3. Exact rational baseline centering

Let a=H_m and g=H_m^(2). The baseline packet's exact compensated second-moment identity gives

    b_n = -2a/m+2/m^2
          -(a^2-g-4)/(m+1)-2(a+1)/(m+1)^2.               (11)

This is rational for each integer n. It obeys |b_n|<=11a^2/m and is generally nonzero. Alternatively one can compute it directly from the three exact baseline moments:

    b_n = E0 K^2-E0 K-2m E0(KU)+m^2 E0 U^2,
    E0 K^2-E0 K = H_n^2-H_n^(2),
    E0(KU) = [H_m^2-H_m^(2)+H_m-1]/m,
    E0 U^2 = [H_(m+1)^2-H_(m+1)^(2)
                +2(H_(m+1)-1)]/[m(m+1)].                (12)

The controls verify agreement using an independent finite-polynomial geometric integral for U^2 and the one-orientation subtraction for KU. A threshold centered at zero is not justified: typically |b_n| is larger than the desired mean separation by order m. Finite-n score centering must not be replaced by its limiting value zero.

## 4. What the finite oracle actually returns

For a finite multiset of N<=m points, put Q_L(x)=ceil(Lx), Q_L(0)=0. Integer-grid queries B(a/L,b/L) exactly test the quantized point set. The existing extractor starts at b=L. While b>=0 it probes B(1,b/L); on a hit, it binary-searches the least first-coordinate index a with a hit and then the least second-coordinate index y with B(a/L,y/L)=1. It records (a,y), sets b=y-1, and repeats. A miss ends the run. Every search has a known-true upper endpoint; the singleton range requires no new query.

The returned list consists of all distinct minimal quantized points, ordered by strictly increasing a and strictly decreasing y. Ties, duplicate locations, points at 0 or 1, empty sets, and y=0 termination are covered by the finite-readout proof and the exhaustive controls. Its count is K_L<=K. On the sufficient event C that no two labeled points share a coordinate bin in either coordinate, all pairwise strict coordinate orders are preserved, so K_L=K. The algorithm does not observe or attempt to certify C; C is solely a coupling event in the proof.

If the returned corners are (a_i,b_i), i=1,...,K_L, with a_(K_L+1)=L, then the uncovered area and score are exactly rational:

    U_L = [a_1 L+sum_i(a_(i+1)-a_i)b_i]/L^2,
    J_L = (K_L-m U_L)^2-K_L.                             (13)

For an empty returned set, U_L=1 and K_L=0. The empty case is only an algorithmic boundary control; neither statistical world here has an empty vector. Formula (13) uses the same corners the prior count extractor computed and then discarded. Computing their area requires no additional endpoint probes. The known upper bound m enters (13); the hidden actual route count N does not.

## 5. Quantization error and collision control

Let E and E_L be the original and rounded uncovered sets. Rounding each coordinate upward shrinks each route's upper dominated rectangle, so E is contained in E_L up to boundaries. For a single route whose coordinate shifts are dx,dy in [0,1/L], its upper rectangle loses area at most dx+dy<=2/L. A union bound for area of the set differences therefore proves, deterministically for every finite multiset,

    0<=U_L-U<=2N/L<=2m/L.                                (14)

This assertion does not require C or any distribution. On C the counts also agree, and both K-mU and K-mU_L lie in [-m,m]. Thus

    |J_L-J|
      =m|U_L-U| |2K-m(U+U_L)|
      <=4m^3/L.                                         (15)

With L>=32m^5/h^2,

    |J_L-J|<=e_m:=h^2/(8m^2) on C.                       (16)

This is a pathwise bound on the good coupling event. It is not an assertion that E J_L-E J is bounded by e_m unconditionally, or that conditioning on C leaves the ideal mean and variance unchanged. The test proof below never uses either invalid inference. Score rounding has no fixed sign even though U_L>=U: squaring a compensated quantity can increase or decrease it.

Under world 1 a coordinate has CDF 1-(1-t)^c, c=n/m. Every nonzero bin has mass at most L^(-c); under world 0 its mass is 1/L<=L^(-c). Across independent labeled routes the same-bin probability in one coordinate is the sum of squared bin masses, at most the maximum bin mass. The union bound over both coordinates and route pairs gives

    P_i(C^c)<=m(m-1)L^(-c), i=0,1.

For R vectors let C_all be the event that each vector satisfies C. Then

    P_i(C_all^c)<=R m(m-1)L^(-c)<=eta                     (17)

for the collision resolution in (2). No independence between a route's two coordinates or between C_all and the test statistic is assumed.

## 6. The finite test and its constants

Fix n>=n0 so that (10) holds. Couple the finite extraction with the ideal scores on the same R independent vectors, and write bar J and bar J_L for their averages. By (16), on C_all,

    |bar J_L-bar J|<=e_m.

Write d_m=h^2/(4m^2)=2e_m and t=b_n+d_m. The implemented decision is 1 iff bar J_L>=t; the tie convention is fixed and exact.

In world 0, a wrong decision on C_all forces

    bar J-b_n>=d_m-e_m=e_m.

In world 1, a wrong decision on C_all forces bar J<t+e_m, while (10) gives E1 J>=b_n+4e_m; hence

    E1 J-bar J>=(E1 J)-(t+e_m)>=e_m

with the strict inequality in the first relation only strengthening the event containment. Chebyshev on the unconditioned ideal averages, not on a conditioned law, yields in each world

    P_i(wrong decision)
       <=eta+3h^2/(R e_m^2)
       =eta+192m^4/(R h^2)
       <=eta+alpha.                                     (18)

Thus both errors are controlled, without doubling the stated alpha or dropping a singular event. The per-world variance assumptions alone suffice for the displayed statistical constant.

## 7. Exact finite arithmetic and deterministic algorithm

For n>=2 and rational alpha,eta>0 with alpha+eta<1:

1. Sum the rational harmonic numbers h=H_n, a=H_m, and g=H_m^(2). Compute b_n from (11), R from (2), and L_area=ceil(32m^5/h^2), using exact fractions and integer ceiling division.
2. Put A=m(m-1)R/eta=p/q in lowest positive terms. Find the least positive integer L_collision with

       L_collision^n q^m >= p^m.                          (19)

   Integer doubling supplies a valid upper bound, followed by integer binary search. This is the exact ceiling of A^(m/n), without a floating-point exponent or an undecidable real comparison. Set L=max(L_area,L_collision).
3. Independently reset the retained vector R times. On each vector, run the terminating binary extractor using only rational endpoints of denominator L. Compute J_L by (13), and accumulate the sum as an exact rational.
4. Compare that sum with the rational R[b_n+h^2/(4m^2)]. Choose 1 on equality and 0 otherwise.

These operations halt for every supplied n and rational alpha,eta in the stated domain, assuming each requested oracle response and reset is available. No likelihood, affinity, weighted score correction A, hidden N, exact unrounded coordinate, or infinite computation enters the implemented decision. Arithmetic cost and rational numerator/denominator growth are not endpoint-query counts; finite arithmetic is asserted, not polynomial bit-complexity.

The reference functions in controls.py implement this arithmetic, the grid extraction, area, score, and finite comparison. They do not claim that the unknown eventual cutoff is known. Exhaustive synthetic oracles are diagnostic inputs, not observations from an alleged physical device.

## 8. Resource accounting and what is actually matched

For one vector, with d_L=ceil(log_2(L+1)), the extraction bound is

    T<=1+K_L(1+2d_L)<=1+m(1+2d_L).                       (20)

All existence probes and a possible terminal miss are included. Since K_L<=K and the consumed count bounds are E0 K=H_n and E1 K<=H_m,

    E_i T<=1+(1+2d_L)H_m.                                (21)

For fixed alpha,eta, R=Theta(m^4/h^2) and both resolution terms in (2) are polynomially bounded in m, so log L=O(log m). Equations (20)-(21) give O(log^2 m) expected probes per vector and O(m log m) worst-case probes per vector. Multiplying by R proves the total upper bounds stated above. Rational endpoint indices need O(log m) bits for this fixed-confidence asymptotic, aside from other computation.

The sharp predecessor proves the baseline expected started-vector lower bound

    E0 N_started >= kl(1-epsilon,epsilon)/KL(Q0||Q1)
                 =Omega_epsilon(m^4/log^2 m)

for any common adaptive endpoint policy with independent fresh vectors and unconditional terminal error at most epsilon in both worlds. Full skyline revelation dominates every endpoint answer on a retained vector. The finite test here obeys those premises and uses exactly R started vectors, which closes the independent-vector order gap. It does not assert a sharp numerical sample constant, unknown-pair minimax property, anytime confidence guarantee, endpoint-query lower bound, or optimal expected arithmetic cost.

The physical and epistemic assumptions remain unchanged: this is the stated calibrated pair, noiseless arbitrary rational endpoint access, exact comparisons, fresh independent resets, and unchanged retention. It neither reconstructs all dominated routes nor certifies that a real instrument has this capability. Known n is a parameter of the pair, not a newly observed latent count. Existing eleven-checkpoint assembly and older archives remain untouched.

## 9. Controls, attribution, and remaining boundary

The deterministic control record includes exact baseline-centering comparisons using independent finite-polynomial integrals; exhaustive small-grid extraction/area/score checks; both signs of score rounding; strict count-loss collision examples; exact grid-root minimality; threshold margins and Chebyshev constants; and negative controls for missing centering, treating score rounding as one-sided, insufficient resolution, and dropping the collision qualification. No simulation estimate is used as proof of (1), and no finite collection of n values certifies n0.

The parent supplied the candidate statistic, derivation route, finite-bias scale, threshold, and budget constants. This packet checks their algebra, supplies the explicit change-of-measure treatment of the singular stratum, separates eventwise approximation from unconditional bias, gives exact arithmetic and algorithmic controls, and combines the bounds into the finite-interface vector-order theorem. The sharp moment/information result, baseline moment formulas, and previous grid extraction retain their predecessor attribution. No field-wide novelty is claimed. A fresh independent review of this frozen packet remains necessary before acceptance; no review of this new theorem is implied by predecessor review.
