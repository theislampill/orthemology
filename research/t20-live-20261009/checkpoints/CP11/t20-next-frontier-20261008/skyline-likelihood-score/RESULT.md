# A controlled second-order retained-skyline likelihood expansion

8 October 2026 UTC. New scratch-only sibling after the completed skyline count/mean test. Historical floor remains UNVERIFIED. No protected integration, archive overwrite, physical-access, empirical, rate-optimality, or closure claim is made.

## Result

Retain the exact common-stratum likelihood in ../retained-skyline-likelihood/RESULT.md. Let m=n+1, e=1/m, c=1−e, and let s be an ordered k-point skyline with 1≤k≤n. Write E for its undominated lower staircase, U=area(E), M_j=∫_E (xy)^j dxdy, and t_i=x_i y_i. In particular D0=1−U.

If k/m≤1/2 and U≤1/2, then

    log L(s) = [(k−mU)^2−k]/(2m²)
               + 2[Σ_i t_i/m−M1] + R(s),

    |R(s)| ≤ 24U³+120(k/m)U²+2(k/m)³
            ≤ 40(k/m+U)³.                                  (1)

Thus the root-supplied candidate is correct as a localized, deterministic second-order expansion. In a window k+mU≤B≤m/2 its error is at most 40B³/m³. The leading expression includes geometry beyond count K: the area compensation k−mU and both a visible boundary sum and a lower-staircase moment. This identifies a viable next statistic; it does not establish its variance, its testing information, or superiority to the completed count test.

There is also elementary probabilistic localization under both stated worlds:

    E0 U = E1 U = H_m/m,
    E0 M1 = E1 M1 = (H_(m+1)−1)/[m(m+1)],                 (2)
    P_j(K+mU>B) ≤ 2H_m/B,  j=0,1.                        (3)

Consequently (1) holds on sets of arbitrarily high fixed probability with an O((log m)³/m³) remainder, by choosing B to be a sufficiently large constant times H_m. Taking B=H_m log m yields sets with probability tending to one, at the expense of the larger explicit bound 40(H_m log m)³/m³. These are probability/localization assertions only. They supply no integrated squared-error, likelihood-tail, KL, or Hellinger estimate.

## 1. Geometry and exact algebra

E is coordinatewise lower-closed, up to its irrelevant boundary. For any (x,y) in its closure, the rectangle [0,x]×[0,y] is contained in that closure, so xy≤U. Each skyline point is also in the closure. Therefore t_i≤U and M_j≤U^(j+1). This is why area control suffices; controlling only max_i t_i would not in general control staircase connector corners.

With x_(k+1)=1, all quantities in (1) are exactly determined by the skyline:

    U=x_1+Σ_i (x_(i+1)−x_i)y_i,
    M1=[x_1²+Σ_i (x_(i+1)²−x_i²)y_i²]/4.                 (4)

The Joe density admits the exact factorization

    f_c(x,y)=(1−e) exp(e a(t)) [1+e b(t)],
    a(t)=−log(1−t), b(t)=t/(1−t), t=xy.                  (5)

The exact likelihood therefore has logarithm

    A + Σ_i [e a(t_i)+log(1+e b(t_i))]
      + log D0 + (m−k)log(Dc/D0),
    A=−log(1−ke)+k log(1−e).                             (6)

Here Dc=1−∫_E f_c, and the route density is normalized on the square. This formula follows directly from the exact density, with no asymptotic exchange of integrals.

## 2. Explicit remainder proof

All inequalities below use e≤1/2, U≤1/2, and a0=ke≤1/2. For 0≤t≤1/2,

    a(t)≤2t, b(t)≤2t,
    0≤a(t)+b(t)−2t≤3t²,
    exp(e a(t))≤sqrt(2).

Expansion of the exponential with its elementary nonnegative Taylor bound gives

    |f_c(t)−(1−e+2et)| ≤ 8e t²+4e² t.                   (7)

For detail, exp(ea)(1+eb)−1−e(a+b) is nonnegative and at most

    e² exp(ea)(a²/2+ab) ≤ 9e²t².

Multiply by (1−e), subtract 2et, and use a+b≤4t and 9e²t²≤(9/2)et². The resulting coefficient 7.5 is bounded by 8 in (7).

Integrating (7), let δ satisfy

    Dc−D0=e(U−2M1)−δ,
    |δ|≤8eM2+4e²M1≤8eU³+4e²U².                         (8)

The triangle inequality gives |Dc−D0|≤5eU: use U+2U²≤2U, 8U³≤2U, and 4eU²≤U. Put z=(Dc−D0)/D0. Then |z|≤10eU. Separately the global density bound f_c≥c, integrated on D and on E, gives

    −e≤z≤eU/(1−U)≤e,

so |z|≤1/2. The second bound is important: the looser 10eU alone would not justify the logarithm expansion. Hence

    |(m−k)[log(1+z)−z]|≤m z²≤100eU².                  (9)

Using (8) in the remaining linear term, and expanding 1/(1−U) just enough, yields

    (m−k)z=U+U²−a0 U−2M1+R_D,
    |R_D|≤22U³+6a0 U²+8eU².                           (10)

One can check (10) term by term: the remainder of U/(1−U) after U+U² is ≤2U³; that of −a0U/(1−U) after −a0U is ≤2a0U²; the change in −2(1−a0)M1/(1−U) relative to −2M1 is ≤4U²(a0+U); and the δ term is ≤16U³+8eU². Also

    |log(1−U)+U+U²/2|≤2U³/3.                           (11)

For the visible-point contribution in (6), log(1+v)−v lies in [−v²/2,0] for v≥0. Thus

    |Σ_i[e a(t_i)+log(1+e b(t_i))]−2eΣ_i t_i|
      ≤3ekU²+2e²kU²≤4a0U².                            (12)

Finally the convergent logarithm series, with both arguments at most 1/2, gives

    |A−k(k−1)e²/2|≤(2/3)[a0³+ke³]≤(4/3)a0³.          (13)

Combining (9)–(13), and e≤a0 because k≥1, bounds the total remainder by

    (68/3)U³+118a0U²+(4/3)a0³,

which is bounded by the first displayed bound in (1). The final ≤40(a0+U)³ follows by comparing its nonnegative monomial coefficients. The surviving terms are exactly

    k(k−1)e²/2−keU+U²/2+2eΣ_i t_i−2M1,

which proves (1). Constants were chosen for transparent coverage rather than sharpness.

## 3. Probabilistic localization, and its strict limits

At a fixed endpoint (x,y), membership in E means that no underlying route lies in its lower rectangle. Under P0 this has probability (1−xy)^n. Under P1 it has probability

    [1−F_c(x,y)]^m=(1−xy)^(cm)=(1−xy)^n.

Tonelli therefore gives equality between the two worlds for the expectation of every nonnegative integral ∫_E w(x,y) dxdy. In particular (2) follows from the product-integral identity ∫∫g(xy)=∫_0^1(−log t)g(t)dt. The first integral is H_m/m; the second is (H_(m+1)−1)/[m(m+1)], obtained by differentiating the elementary beta integral or its convergent series.

The completed skyline-count-information packet proves E0 K=H_n≤H_m and E1 K≤H_m. Therefore E_j(K+mU)≤2H_m, and Markov proves (3). For B≤m/2 the event K+mU≤B automatically lies on common support and satisfies both hypotheses of (1). This explicitly avoids assigning a finite likelihood logarithm on the alternative-only stratum K=m.

For each fixed η>0, B=2H_m/η is eventually at most m/2, and the error bound on a set of probability at least 1−η is 40(2H_m/η)³/m³. In this localized sense the remainder has O_P((log m)³/m³) scale under both laws. The weaker Markov information is enough for this assertion; it is not a tail-integrability theorem. In particular no variance order for (K−mU)², no centering claim for the leading statistic, and no logarithmic improvement in testing cost is deduced.

## 4. A genuine obstruction to removing localization

Fix m≥2, take k=1, y=1/2, and x=1−η with η↓0. Then U=1−η/2 tends to one. The exact boundary asymptotic in the retained-skyline-likelihood packet, or direct substitution in (6), gives

    log L=(1/m)log η+O_m(1) → −infinity.

The proposed polynomial leading expression stays bounded: k, U, t and M1 all have finite limits. Hence no globally bounded remainder of the form C(k/m+U)³ can hold over the entire common support for any finite universal C. A small-area restriction or an explicit boundary-sensitive term is necessary. This counterexample does not refute the localized expansion; it shows exactly why localization cannot silently be discarded when computing information integrals.

## 5. Deterministic controls and attribution

controls.py evaluates the exact strip formula and the candidate at 90 decimal digits for deterministic staircase families at m=16 through 16384 and additional fixed-coordinate cases. It checks the stated bound whenever its hypotheses hold, evaluates the boundary family η=10^(−4),10^(−16),10^(−64), and verifies the two first-moment integral identities by independent one-dimensional quadrature. CONTROL_RESULTS.json retains all values. These are synthetic mathematical configurations, not random samples, empirical data, or rigorous interval certificates. The written inequalities carry the general result; finite checks do not prove it.

The root supplied the leading candidate and independently supplied the downset geometry and M1 formula during this work. This packet derives the explicit uniform error constant, the first-moment/Markov localization, and the boundary obstruction from the exact predecessor likelihood. No field-wide novelty is claimed. The result is a written mathematical proof with deterministic executable checks, not a kernel-checked theorem. Independent digest-bound review is still required before acceptance. The bounded operation stops at this viable proved increment, leaving score moments, tail integration, KL/TV/Hellinger asymptotics, and any better test or optimality claim open.
