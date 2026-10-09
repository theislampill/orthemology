# Independent review: finite geometric-score probes

8 October 2026 UTC. Scratch-only prospective mathematical review. Historical floor remains **UNVERIFIED**. No author, predecessor, protected repository, or archive is changed. This review supplies no integration authority, physical certification, formal-kernel assurance, or closure.

## Verdict and immutable subject

**PASS within the stated eventual, fixed-confidence, noiseless retained-endpoint contract.** No blocking mathematical finding remains. The accepted author RESULT.md SHA-256 is **d7cfa67248e06786e1c4acaae6e61138498ef8e6dc1f14287d7d2664302ee96f**. The author MANIFEST.json SHA-256 is **f7d1033b6f4d269155f1e6dc5950c267414e6d498ab94166aeb55e0cf341b4a3**. This review applies only to those bytes and their bound dependencies.

For m=n+1 and h=H_n, the score J=(K−mU)²−K satisfies

    E1 J−E0 J ~ h²/m²,
    Var0 J ~ 2h²,  Var1 J ~ 2h².

The finite rational-grid implementation then attains independent-vector order Θ_epsilon(n⁴/log² n) at fixed two-sided error epsilon<1/2, including baseline expected started-vector cost and the maximum of both expected costs. The construction has expected total endpoint-query cost O_epsilon(n⁴) and deterministic worst-case total query cost O_epsilon(n⁵/log n). These are query upper bounds, with no query-optimality claim.

**The displayed executable budget is guaranteed only for sufficiently large n, with no effective cutoff certified.** It terminates for each input n≥2 but is not an all-n certified statistical budget. The older count protocol may be used on all n at its older rate; the two theorems do not supply an automatic certified hybrid switching rule without an independently known cutoff. An eventual asymptotic complexity result does not need such a rule, but deployment claims would.

The parent supplied the statistic and proposed constants. Independence here means a separate proof audit, exact integration, algorithm implementation, and diagnostic record, not independent discovery. The independent diagnostic script imports no author or predecessor control code. The author's controls were replayed separately into this review directory.

## 1. Dependency and support audit

The sharp source result has digest 52a9c53ca5d1765de2956e685701532529efca9a0292165f8f9e738b43b7a870. Its later independent PASS receipt binds that same result and author manifest. The older author manifest's pending label is historical; it is not rewritten or mistaken for a new review of the finite test.

The finite proof consumes the sharp source's actual baseline quadratic moment, weighted L² bound, shrinking uniform likelihood window, localized integrated remainder, both-world tail, and started-vector lower bound. It does not infer the score moments solely from the information asymptotics. The relevant formulas and their derivations were inspected directly in the sharp result and written review.

The likelihood is the unnormalized common-support derivative L=dQ1,common/dQ0. It satisfies E0 L=1−p_n, with positive alternative singular mass on K=m. Nothing in this review normalizes that common component to probability one. The common window G_m eventually excludes K=m, and Q_i(G_m^c)≤beta_m in both full laws, with beta_m=(ceil(log_2 n)+1)m^−20. Those are precisely the tail statements needed below.

The global bound |J|≤m² holds in both worlds: 0≤K≤m, 0≤mU≤m imply |K−mU|≤m, and J lies between −m and m². The consumed |Q|≤5 is a loose bound on baseline support. These bounds cover rare high-count and singular observations; no unproved tail moment is substituted for them.

## 2. Log likelihood versus density, and the mean shift

On G_m, write a=log L and let sup|a|≤epsilon_m→0. For all sufficiently large m,

    |exp(a)−1−a| ≤ C epsilon_m |a|.

The source gives ||a 1_G||_2=O(h/m²) and ||(a−Q)1_G||_2=o(h/m²). Hence the genuinely needed density remainder follows:

    ||(L−1−Q)1_G||_2=o(h/m²).

A log-remainder statement alone would not justify integrating J(L−1); the uniform shrinking window is what makes this conversion valid.

The source also establishes E0 J²~2h² and ||A/m||_2=O(sqrt(h)/m²), where Q=J/(2m²)+2A/m. Therefore

    E0 JQ = E0 J²/(2m²)+2E0[JA/m]
           = h²/m²[1+o(1)],

because the mixed term is O(h^(3/2)/m²)=o(h²/m²). Cauchy–Schwarz with the density remainder has error o(h²/m²). Removing the window from E0 JQ costs at most 5m² beta_m, also negligible.

On G_m the exact common-support change of measure applies. On its complement one must instead retain the full Q1 expectation, including K=m:

    E1 J−E0 J
      = E0[J(L−1)1_G] + E1[J1_bad] − E0[J1_bad].

The latter two terms together have absolute value at most 2m² beta_m. This proves the claimed positive mean gap and explicitly charges the singular alternative stratum. A baseline tail probability alone would not be sufficient. The independent negative control demonstrates that omitting a singular component can even reverse a mean-gap sign in a finite two-common-atom example.

## 3. Both variances and finite-n centering

Uniformly L→1 on G_m. Consequently

    E1[J²1_G]=E0[J² L1_G]~2h².

Each omitted second-moment tail is at most m⁴ beta_m=o(h²). Thus the alternative raw second moment has the same coefficient 2 as the baseline. An alternative fourth-moment formula or an unproved fixed-count transfer is unnecessary.

The baseline mean b_n is nonzero and is exactly the rational formula stated by the author. It is O(h²/m)=o(h). Adding the established shift leaves E1 J=o(h) as well. Subtracting the squared means from the two raw second moments therefore proves both variance asymptotics.

As an independent centering check, the reviewer integrated the fixed-count skyline density directly, without the author's two-query polynomial formula. On the k-point chamber x_1<...<x_k and y_1>...>y_k, the density is (n)_k D^(n−k), with

    D = 1−x_1−y_k + sum_i x_i y_i − sum_(i<k) x_(i+1)y_i.

Every expanded monomial is integrated by the ordered-simplex identity

    integral_(0<x_1<...<x_k<1) product_i x_i^(a_i)
      = product_(j=1)^k [j+sum_(i≤j)a_i]^(−1),

and its reversed-y analogue. Writing J as a quadratic polynomial in D gives exact normalization, E0 J and E0 J² at n=1,...,6. All six means agree with the author's centering. In particular b_1=−5/9, b_2=−41/48, and b_3=−71/75. The n=1 second raw moment is 94/225, giving variance 221/2025.

Dropping b_n is not justified by b_n→0. Indeed its leading magnitude is order h²/m, a factor of order m larger than the desired signal. The exact diagnostic ratios illustrate this issue; no finite set of ratios proves the general asymptotic or locates n0.

## 4. Finite endpoint extraction and rational geometry

The extractor's input is a binary endpoint oracle on an unchanged vector. It does not read hidden route coordinates or the actual hidden count. At denominator L, its queries are precisely the oracle for points rounded upward by ceil(Lx), with a separate zero bin.

The successive least-x and then least-y searches find an occupied minimal corner. Replacing the upper y bound by the recorded y−1 excludes the dominated remainder and leaves every remaining minimum. Thus all distinct quantized minima are returned in increasing x and decreasing y order. Equality, duplicates, zero/one endpoints, the empty diagnostic set, and zero-coordinate termination are covered. Each binary search maintains a known-true upper endpoint and takes at most ceil(log_2(L+1)) queries. The final miss is charged when it occurs.

For corners (a_i,b_i), the uncovered area is

    U_L = [a_1 L + sum_i (a_(i+1)−a_i)b_i]/L²,
    a_(K_L+1)=L.

This is a staircase area computable from the existing corner list. An empty list gives U_L=1. No additional probes or irrational operations are needed. Both the area and J_L=(K_L−mU_L)²−K_L are rational.

Rounding upward shrinks each upper dominated rectangle. Its lost area is at most the sum of the two coordinate shifts, bounded by 2/L. The union of those losses gives 0≤U_L−U≤2N/L≤2m/L, without any collision condition. The surjection from original minima onto quantized minima gives K_L≤K. If no two labeled points share a bin in either coordinate, all strict coordinate orders are preserved and K_L=K. On that event,

    |J_L−J| ≤ m|U_L−U| |2K−m(U_L+U)| ≤ 4m³/L.

The sign of the score difference is unrestricted. The independent checks include both signs at m=3, even with a collision-free singleton. They also include strict count loss when bins collide. The author provides a stronger negative witness where deleting the collision qualification makes the displayed score bound false.

## 5. Collision probability, budget, and exact decision

For c=n/m, the alternative marginal CDF is 1−(1−t)^c. Concavity of t^c gives a maximum positive-bin mass L^−c. Uniform-bin mass 1/L is no larger. Independence across labeled routes gives a one-coordinate collision probability sum p_j²≤max p_j; no within-route coordinate independence is used. Union over two coordinates, route pairs, and R vectors gives

    P_i(any collision) ≤ R m(m−1)L^−c.

For A=m(m−1)R/eta=p/q in lowest terms, the least admissible integer collision grid solves

    L^n q^m ≥ p^m.

This is exactly the ceiling of A^(m/n). Doubling followed by integer binary search terminates; neither floating-point ceiling nor a real-number comparison oracle appears.

Eventually the ideal mean shift is at least h²/(2m²) and both variances at most 3h². Put e=h²/(8m²), choose the threshold b_n+2e, and require L≥32m⁵/h². On the joint collision-free event, the finite and ideal averages differ by at most e. A world-0 error forces the ideal average to exceed its mean by at least e. A world-1 error forces a deviation below its mean by at least e, because the mean is at least b_n+4e. The specified tie rule causes no gap in this argument.

Chebyshev is applied to the **unconditioned independent ideal scores**, not a law conditioned on no collision. Thus in each world

    error ≤ eta + 3h²/(R e²)
          = eta + 192m⁴/(R h²).

The displayed R=ceil(192m⁴/(alpha h²)) makes this at most eta+alpha. There is no extra factor two, and there is no assumption that the mean of J_L differs from the mean of J by at most e without a collision-tail term. Independence of the scores, supplied by fresh independent resets, is required for variance reduction by R; independence from the collision event is unnecessary.

The area-resolution coefficient 32 and the sufficient variance coefficient 192 are arithmetically correct. They are not optimal constants. All runtime comparisons, including the final comparison against R times the rational threshold, are finite exact rational/integer operations. Finite arithmetic is claimed, with no polynomial bit-complexity claim.

## 6. Resource and scope check

For d_L=ceil(log_2(L+1)), the extractor uses at most 1+K_L(1+2d_L) endpoint probes. Since K_L≤K and E_i K≤H_m, its expected cost is at most 1+(1+2d_L)H_m.

At fixed positive alpha and eta, R=Theta(m⁴/h²) and both grid-resolution terms are polynomially bounded in m, so d_L=O(log m). Expected queries per vector are O(log² m), while deterministic per-vector cost is O(m log m). Multiplication by R gives O(m⁴) expected and O(m⁵/log m) worst-case total queries. This argument is not uniform over arbitrarily shrinking error tolerances.

The sharp predecessor's reverse-KL lower bound applies to the same endpoint model because revealing the complete skyline at each first observation dominates all subsequent queries on that retained vector. It charges every started vector and requires unconditional terminal correctness. The finite test uses exactly R starts and always terminates, so it closes the independent-vector order gap under the same known-pair, retention, reset, and accuracy assumptions. It does not prove total-query optimality, noise tolerance, unknown-pair minimax performance, or physical realizability.

No numerical threshold n0 is given by the asymptotic proof. The reference plan can be evaluated for small n, and the diagnostic grids deliberately include such values, but these operations do not certify the claimed error there. The author correctly says so. The all-n older count test remains a separate valid option; a certified switching cutoff is not supplied by combining two assertions.

## 7. Verification evidence and remaining limits

The independent exact controls pass:

- direct ordered-simplex skyline-density normalization and score moments at n=1,...,6;
- 29,381 small-grid multiset extraction, cell-area, score, and actual-query-count cases;
- 71,253 quantization cases across three coarse resolutions, including 886 collision-free cases;
- 15 exact finite-grid uniform laws, checking score bias, expected queries, mean count, and collision probability;
- 18 exact rational parameter/root cases, including grid-root minimality, both threshold margins, and the Chebyshev constant;
- nonzero-centering, both-sign rounding, strict count-loss, missing-singular-term, and insufficient-resolution negative controls.

The 15 finite-grid laws are weighted by exact multinomial probabilities, not sampled. They demonstrate actual coarse-grid bias and expected costs; they do not establish an asymptotic or certify small-n error for the displayed eventual prescription.

The isolated author replay exits successfully. Its JSON output and stdout are byte-identical to the frozen author output files. Its checks include 32 centering cases, 29,381 extraction/cell-area cases, 23,751 quantization cases, 21 exact parameter/root cases, all five stated negative-control categories, and 39 sharp transitive artifact bindings. Separate review verification checks the exact author payload, source bindings, predecessor receipt, and this review's payload hashes.

No mathematical revision to the frozen author proof was required. All assurance remains written mathematical review plus deterministic diagnostics. There is no Monte Carlo evidence, field-wide novelty claim, formal theorem kernel, protected integration, archive rewrite, historical-floor certification, or project closure.
