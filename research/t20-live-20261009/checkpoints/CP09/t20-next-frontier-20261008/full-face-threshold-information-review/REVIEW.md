# Independent cold review: full face-threshold information

## Verdict and exact binding

**PASS. No blocking mathematical finding and no requested revision.**

Reviewed author file: `../full-face-threshold-information/RESULT.md`.

SHA-256: `ced60a6b7b98f2b0d181e92f194ca64d201fec2278d61c502e2d13887e803f17`.

The byte-identical snapshot is `reviewed_RESULT.md`. The verdict concerns the mathematical claims and their expressly conditional observation contract in those exact bytes. It does not certify later edits, independently audit the author's numerical implementation, validate a physical instrument, authorize protected integration, or close T20. Author and predecessor files were read-only throughout this review.

The reviewer independently derived the laws, boundary and absolute-continuity argument, divergence conclusions, finite-shell coefficient, and density-envelope constant. A separate scalar-statistic proof of infinite chi-square is given below. Reviewer-owned exact symbolic and finite combinatorial controls supplement the analytic review; author controls were not imported or replayed.

## 1. Laws of the two coordinate minima: PASS

For one alternative route, write its joint CDF as G(a,b)=1-(1-ab)^c. Its margins are H_c. Its interior mixed density is

    G_ab(a,b)=c(1-ab)^(c-2)(1-cab)>0.

Thus the stipulated route law is consistent with a positive continuous-density construction; it is not a separately selected table for each command. The probability that both route thresholds exceed 1-x and 1-y is, by inclusion-exclusion,

    1-H_c(1-x)-H_c(1-y)+H_c((1-x)(1-y))
      =x^c+y^c-(x+y-xy)^c=S(x,y).

The event X=1-min_j A_j<=x means that every A_j is at least 1-x. Independence across routes therefore gives F1=S^m. The product reference gives F0=(xy)^n. Equality conventions do not affect these probabilities because coordinate margins have no atoms. Since mc=n and S(x,1)=x^c, both X and Y have CDF x^n in both worlds.

The face-observation contract is accurate. All coordinate-face comparisons of the same retained vector are measurable functions of its two coordinate minima. Conversely, countably many rational comparisons determine the minima. This is equality of ideal information channels, not a finite-probe algorithm for an arbitrary real number. The observation does not identify individual routes or reveal the latent threshold vector.

## 2. Density, boundaries, and mutual absolute continuity: PASS

The derivatives in the author report are correct. In the open square, z=x+y-xy satisfies z>=x,y and z<=1. Since c<1,

    S_x=c[x^(c-1)-(1-y)z^(c-1)]>0,
    S_y>0,
    S_xy=c z^(c-2)[1-c(1-x)(1-y)]>0.

Consequently the mixed derivative of S^m is the stated strictly positive f1. The chain rule has no negative power of S in the main theorem because m=n+1>=2. The reference density is also strictly positive in the open square.

Importantly, differentiating a CDF alone would not justify discarding a singular residual. Here the additional argument does justify it. On each compact interior rectangle the CDF is smooth, so its rectangular increment equals the integral of f1. Rectangles [epsilon,1-epsilon]^2 increase to the open square as epsilon decreases to zero. Their CDF increments tend to

    F1(1,1)-F1(0,1)-F1(1,0)+F1(0,0)=1.

Because f1 is nonnegative, monotone convergence gives integral over the open square equal to 1. Equivalently, agreement on interior rectangles identifies the measure there, and the exhaustion accounts for all its probability. Continuous Beta margins separately assign zero mass to every edge, including its endpoints. Thus there is neither boundary mass nor an interior singular/diagonal remainder. Density positivity then gives P1 mutually absolutely continuous with P0.

Corner blow-up of a density and failure of likelihood-ratio square integrability are consistent with this conclusion. No pointwise finite density at a boundary is needed.

## 3. Infinite forward chi-square: PASS, with independent corroboration

The exact diagonal CDF is

    F1(r,r)=r^n L_n(r),
    L_n(r)=[2-(2-r)^c]^m,
    L_n(0)=lambda_n=(2-2^c)^m>0,

whereas F0(r,r)=r^(2n). The author's localized Cauchy-Schwarz argument is valid: if L=dP1/dP0 were in L²(P0), then the L² integral over E_r would tend to zero, so P1(E_r)/sqrt(P0(E_r)) would tend to zero. Its actual limit is lambda_n>0. This is a genuine contradiction.

A single binary corner indicator would not by itself prove divergence: its chi-square tends to the finite number lambda_n². The localized-integrability step, or accumulation over disjoint shells, is essential and is present.

### Independent scalar-density proof

Let M=max(X,Y). Its distribution functions are precisely the diagonal CDFs:

    G0(r)=r^(2n),
    G1(r)=r^n L_n(r).

For 0<r<1, L_n(r)>=lambda_n and L_n'(r)>0. Both G_i are smooth there, have no endpoint atoms, and have densities

    g0(r)=2n r^(2n-1),
    g1(r)=n r^(n-1)L_n(r)+r^n L_n'(r)
           >=n lambda_n r^(n-1).

Hence

    g1(r)^2/g0(r)>=n lambda_n²/(2r).

Integrating near zero gives infinity. Thus even the coarsening M has infinite forward chi-square, and data processing yields the same conclusion for (X,Y). This independently confirms the critical logarithmic divergence without using the author's localized L² contradiction or numerical density asymptotics.

The proof is about the orientation P1 relative to P0. It makes no reverse-divergence claim.

## 4. Finite dyadic quantizations and limit: PASS

Let h=2^(-n), and abbreviate L_n(r_k)=L_k. Direct subtraction of nested corner probabilities gives the author's p_k and q_k. For a nonterminal shell their quotient reduces to

    q_k²/p_k=(L_k-h L_(k+1))²/(1-h²).

Since L_k>=L_(k+1)>=lambda_n,

    L_k-hL_(k+1)
      =(L_k-L_(k+1))+(1-h)L_(k+1)
      >=(1-h)lambda_n.

This proves the stated lower bound d_n=lambda_n²(1-h)/(1+h) for every shell. The terminal cell contributes L_K²>=lambda_n². Subtracting one proves the all-K linear lower bound, including its harmless potentially negative values at small K.

For fixed n, L_k and L_(k+1) tend to lambda_n, so the individual nonterminal contribution tends to d_n>0. Cesaro averaging of the first K contributions, together with the bounded terminal contribution divided by K, proves

    chi²(P1,K||P0,K)/K -> d_n.

The partitions are nested: refining the terminal cell into the next shell plus a new terminal cell cannot decrease chi-square. This follows from weighted Cauchy-Schwarz and does not require numerical monotonicity checks.

The distinction between transcript and quantization is correctly maintained. The K nested corner indicators can be recovered from 2K coordinate-face bits at commands 1-2^(-k); they identify the K+1 shells. The whole 2K-bit transcript can retain more information. The displayed exact limit is for the shell quantization; data processing supplies a lower bound for the transcript, not equality of their divergences or slopes.

Every fixed finite measurable partition has finite chi-square because absolute continuity removes any baseline-zero cells and only finitely many positive denominators remain. The same reasoning applies to a fixed deterministic finite face word. A finite transcript therefore does not itself have infinite divergence. Its forward KL remains bounded by that of the ideal two-minimum channel.

## 5. Finite forward KL and the constant: PASS

The three derivative estimates are valid on the open square:

    S_x<=c/x, S_y<=c/y, S_xy<=c/(xy).

For the last estimate, the derivative's bracket is at most 1 and xy<=z² implies xy z^(c-2)<=z^c<=1. Since S<=1 and m>=2,

    f1 <= [m(m-1)c²+mc]/(xy).

Substitution of m=n+1 and c=n/(n+1) gives exactly

    m(m-1)c²+mc=n³/(n+1)+n=n²+n/(n+1).

Dividing by f0 gives

    log(f1/f0)<=log(1+1/[n(n+1)])-n log x-n log y.

The right side is nonnegative, and the common margins give E1[-log X]=E1[-log Y]=1/n. It therefore controls the positive part of the log likelihood ratio by an integrable quantity. The negative part satisfies

    integral_{L<1} f0[-L log L] <=1/e,

so no undefined infinity-minus-infinity expression occurs. The author's finite upper bound follows. The laws differ, as their small-corner probabilities demonstrate, so strict positivity of KL also follows. The uniform bound by 2+log(3/2) is correct for every integer n>=1.

Since P0 is the product of the shared margins, this forward KL is also the mutual information of X and Y under P1. Infinite chi-square is thus consistent with finite dependence information here. This observation supplies no sharp n-asymptotic.

## 6. Endpoint controls: PASS

At n=1, c=1/2 and m=2, the reference density is 1, the density-envelope constant is 3/2, and lambda_1=(2-sqrt(2))²>0. All the preceding proofs remain valid. There is no hidden assumption n>1.

The equality control is the separate parameter choice c=1 **and m=n**. Then S=xy and F1=(xy)^n=F0, so both divergences vanish. Simply setting c=1 while retaining m=n+1 would not be an equality control because the margins would change. The author states the correct separate choice and does not make that error. At n=1,m=1 in the equality control the direct CDF calculation suffices; there is no need to apply the main theorem's m>=2 density bound there.

## 7. Interpretation and prohibited overreach: PASS within scope

The report correctly refuses the following implications:

- Infinite chi-square does not prove infinite KL. Finite KL is explicitly proved.
- A fixed-n, K-to-infinity divergence statement does not give a uniform-n information gain, testing exponent, or feasible precision schedule. In particular d_n depends strongly on n. As a corroborating elementary bound, 2-2^c=2(1-exp(-log(2)/(n+1)))<=2 log(2)/(n+1), so d_n is at most [2 log(2)/(n+1)]^(2(n+1)). This reinforces, rather than removes, the nonuniformity warning.
- The old fourth-power expected-sample lower bound concerns fresh vectors with at most two retained-face probes and its explicit charging rule. The present stronger interface does not contradict that theorem. Nor does failure of its chi-square proof strategy decide the full-readout KL asymptotic or achievable cost.
- The 2K-probe construction assumes exact selectable dyadic commands, retained state, and noiseless endpoint observations. It supplies a mathematical sufficient budget, not minimum probe cost, noisy-device performance, finite exact readout, or physical validation.
- No inference about route labels, full latent vectors, arbitrary interior replay, empirical architecture, broad field novelty, protected integration, or T20 closure is authorized.

The statements about the earlier all-rate bound and adaptive successor match their read-only results. Their exact RESULT bytes also match their previous independent-review receipts. This review imports that established predecessor status rather than claiming a complete fresh audit of their lengthy proofs.

## 8. Ancestry and verification evidence

The [VineCopula authors' tail-dependence documentation](https://tnagler.github.io/VineCopula/reference/BiCopPar2TailDep.html) was directly inspected on 8 October 2026: family 6 is Joe and its upper-tail coefficient is 2-2^(1/theta). The linked [author-maintained implementation](https://github.com/tnagler/VineCopula/blob/7829d3b17cf1c214f6d074f248225b4005c087a7/R/BiCopPar2TailDep.R) implements that same coefficient for family 6. Setting theta=1/c gives the claimed one-route coefficient. For m independent routes the joint and marginal upper-tail probabilities are each raised to m, yielding its m-th power. Complementing the minima turns this into the lower-corner coefficient used here.

The documentation points to Joe's 1997 monograph; that monograph was not read in this review. The separate BiCopCDF documentation was inspected only for family identification and supplies no additional theorem proof here. This is targeted primary-package verification, not an exhaustive priority search. The author's limited ancestry/novelty statement is appropriate.

Reviewer-owned `independent_controls.py` produced **19 passing check groups**: 18 exact symbolic identities and exhaustive exact-rational decoding of **284 open rectangular atoms** for K=1,...,8. These test derivative algebra, boundaries, the c=1 control, the density constant including n=1, the independent scalar proof's critical integrand, shell cancellation, the limiting coefficient, the Beta log moment, and finite face-bit decoding. No empirical data, stochastic trials, numerical integration, or author-code replay was used. Analytic inequalities, all-parameter claims, measure arguments and infinite limits are established above, not by a finite control set.

`CONTROL_NOTES.md` preserves two symbolic-harness assumption issues encountered and resolved: positivity of z on the actual domain, and positivity of the formal CDF function. They were simplifier limitations, not counterexamples or theorem changes.

`SOURCE_BINDINGS.json` and `REVIEW_RECEIPT.json` record the exact reviewed bytes and supporting artifact digests. Prospective active analysis was recorded from 19:34:00.767558 to 19:38:20.455603 UTC, totaling 259.688045 seconds. Initial setup/read activity before that start, later report/receipt packaging, verification and reporting are excluded. No wait interval occurred within the recorded active interval.

## Final disposition

PASS for the digest-bound conditional two-minimum theorem and explicit finite-shell witness. No unresolved finding. Any changed RESULT.md requires a renewed binding; this review is not a blanket approval of future text or a grant of integration/closure authority.
