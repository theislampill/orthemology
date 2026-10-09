# Independent review: sharp ideal-skyline information

8 October 2026 UTC. Scratch-only written mathematical review. No author, predecessor, archive, or protected repository is modified. Historical floor remains **UNVERIFIED**. This review gives no integration authority, physical certification, formal-kernel assurance, or project closure.

## Verdict and immutable subject

**PASS within the declared ideal observation and resource contract**, subject to the final artifact bindings recorded in `REVIEW_RECEIPT.json`. No blocking mathematical finding remains. The reviewed author RESULT.md SHA-256 is **52a9c53ca5d1765de2956e685701532529efca9a0292165f8f9e738b43b7a870**. Its manifest SHA-256 is in that receipt; this review does not automatically apply to later bytes.

For the fixed-count uniform/Joe pair and the Hellinger convention H²(P,Q)=∫(√dP−√dQ)², the reviewed claims are

    KL(Q0 || Q1) ~ log²(m)/(4m⁴),
    H²(Q0,Q1) ~ log²(m)/(8m⁴), m=n+1,
    ideal exact-skyline sample complexity Θ_alpha(n⁴/log² n).

The reverse KL is finite. The forward KL is infinite because the alternative-only stratum K=m has positive mass. The lower bound covers baseline expected started-vector cost E0 N for common adaptive retained-endpoint policies with fresh independent vectors and unconditional terminal correctness. The upper bound is a fixed-sample likelihood-ratio test on full exact skylines of the stipulated known pair. It is not an endpoint-query reconstruction algorithm or a finite-precision implementation theorem.

The parent supplied the sharp conjecture and mechanism. Independence here means a separate mathematical derivation, attack, and diagnostic implementation, rather than independent discovery. The reviewer derived the Poisson fourth coefficient, sixth derivative, variance concentration, normalized density transfer, and information factors before examining the full author draft. The independent script imports neither author nor predecessor diagnostic code. The author replay is separately isolated.

## 1. Dependencies and likelihood convention

The complete skyline density on the ordered k-point antichain is (N)_k ∏ f(z_i) D_f^(N−k). The ordered coordinate measure already fixes the x-order; an extra k! divisor would be erroneous. Under the baseline there are n uniform points and under the alternative there are m=n+1 Joe points with c=n/m. The exact common-support likelihood is therefore

    L = m/(m−K) ∏ f_c(z_i) D_c^(m−K)/D^(n−K).

The only alternative singular stratum is K=m, with 0<p_n<1/m!. Consequently E0 L=1−p_n. The proof preserves this sub-probability likelihood rather than normalizing the common component to one. Its reverse-entropy identity has the correction +p_n, and its squared-Hellinger identity has the same correction +p_n.

The localized expansion inherited from the score packet is applied only where K/m≤1/2 and U≤1/2. The polynomial is

    Q = [(K−mU)²−K]/(2m²) + 2A/m,
    A = Σ_s xy − m∫_E xy,

with |log L−Q|≤40(K/m+U)³ there. The fixed-count second moments and record law are used only under Q0. Neither equality of the one-rectangle void probabilities nor Poisson compensation is used to import an alternative second-moment formula.

The log-squared predecessor provides a specialized, self-contained density calculation and restricted comparison; its substantive calculations were inspected, rather than treating a review label as a substitute for the dependencies. Its fresh completed review is separately bound as context. The sharp result requires its own argument and receives no automatic certification from that predecessor review.

## 2. Auxiliary Poisson law and area variance

Poisson mixing of the uniform skyline density yields

    q_m(s)=m^K exp(−mU),
    N | S = K + Poi(mD).

The empty skyline K=0,U=1,D=0 has mass exp(−m) and total count N=0. It is part of every Poisson normalization used below. Changing the intensity from m to m exp(−t) gives the exact normalized tilt

    E exp[−tM + Z(1−exp(−t)−t)] = 1,
    Z=mU, M=K−Z.

At each fixed m, K≤N and Z≤m. Finite derivatives on compact t-intervals are dominated by a constant depending on m times a polynomial in N times exp(bN). The finite Poisson exponential moments justify differentiation. There is no exchange of an uncontrolled m→∞ limit with a derivative.

In particular EM=0 and EM²=EZ. The void integral gives a_m=EZ=log m+O(1). Conditional on N, K is the independent-uniform record count, including K=0 for N=0. Thus

    Var K = E[H_N−H_N^(2)] + Var(H_N).

The author explicitly bounds Var(H_N)=O(1): on m/2≤N≤2m the distance H_N−log m is bounded, and outside this range elementary Poisson exponential tails dominate its squared growth. The displayed upper-tail calculation at θ=log 2 has exponent m(1−2log 2)<0. The lower-tail argument is likewise exponentially decaying. A hidden substitution N≈m or omission of N=0 is unnecessary. It follows that Var K=O(log m).

Since Z=K−M and Var M=EM²=a_m,

    Var Z ≤ 2 Var K + 2 Var M = O(log m).

This is sufficient concentration for the sharp fourth moment. It makes no independence assertion between K and Z and proves no central limit theorem.

## 3. Sharp fourth moment and a sixth moment sufficient for transfer

The fourth derivative gives

    EM⁴ = 6E(M²Z) + 4E(MZ) − 3EZ² + EZ.

The signs are correct. In particular the mixed linear term is positive in this rearranged identity. The previously proved EM⁴=O(log² m), together with Var Z=O(log m), yields

    E(M²Z)=a_m²+O(log^(3/2) m),
    E(MZ)=O(log m),
    EZ²=a_m²+O(log m).

Therefore EM⁴=3a_m²+O(log^(3/2) m)~3log² m. The coefficient 3 is derived from exact moments, not from a guessed Gaussian limit.

For the sixth derivative the reviewer independently obtains

    M⁶−15M⁴Z−20M³Z+45M²Z²−15M²Z
       +60MZ²−6MZ−15Z³+25Z²−Z.

Its expectation is zero. All nonleading monomials M^i Z^j have i<6 and i+2j≤6. The dyadic area estimate supplies every fixed raw moment EZ^r=O((1+log m)^r); noninteger orders follow from a larger integer moment. Hölder gives

    E|M|^i Z^j ≤ (E|M|⁶)^(i/6) O((1+log m)^j).

Writing x=E|M|⁶/(1+log m)³ bounds x by a constant times 1+x^(1/6)+x^(1/3)+x^(1/2)+x^(2/3). For x≥1 this forces a uniform finite bound. This verifies E|M|⁶=O(log³ m) without assuming the moment it is meant to prove.

Consequently X_m=M⁴/log² m has uniformly bounded 3/2-moment and is uniformly integrable. This is the exact missing condition that would invalidate a transfer based solely on convergence in probability. The separate diagnostics include a normalized bounded-density counterexample: under a triangular two-atom law, r_m→1 in probability with 0≤r_m≤2 and E r_m=1, yet EX_m=1 and E r_m X_m=2 when X_m is not uniformly integrable. Thus neither normalization nor a bounded density alone can replace the sixth-moment argument.

## 4. Fixed-count conditioning is normalized and localized

Conditioning the Poisson process on N=n=m−1 gives Q0 with exact skyline density

    r_n(s)=Poi(mD)(n−K)/Poi(m)(n).

The numerator is zero for K>n and for the empty skyline, where Poi(0)(n)=0 for n≥1. The normalizer is essential. Poi(m)(m−1)=Poi(m)(m), so its logarithm is −(1/2)log(2πm)+O(1/m). On U≤1/2, the independent Poisson-mode comparison bounds r_n≤2exp(1/24)<3. No global constant bound is asserted.

With v=m−Z and q=m−1−K, one has q−v=−M−1. From the already established moments, q/m→1, v/m→1, and q−v=o_P(√m). The local Stirling formula

    log Poi(v)(q)=−(1/2)log(2πq)−(q−v)²/(2v)
                  +O(|q−v|³/v²+1/q)

is uniform once |q−v|/v≤1/2. This high-probability condition follows from those bounds; no expansion is applied at q=0, negative q, or the empty atom. Dividing by the stated normalizer gives r_n→1 in Poisson probability.

Set r̄_n=r_n 1{U≤1/2}. Then r̄_n is bounded and tends to one in probability. Truncating X_m at a fixed level, followed by uniform integrability, proves E[X_m(r̄_n−1)]→0. This is a valid varying-law expectation argument. On the actual fixed-count complement U>1/2, |M|≤m and its dyadic tail is superpolynomially small, so m⁴P0(U>1/2)/log² m→0. The result is

    E0 M⁴~3log² m.

Only this proved moment statement is transferred. The fixed-count mean is −1/m, which independently demonstrates why the exact Poisson mean-zero identity cannot be copied after conditioning.

## 5. Score-square asymptotic and the localized logarithm

Let h=H_n~log m. The fixed-count second moment is E0 M²=h+o(1), and Var0 K=O(log m). Cauchy–Schwarz with the newly proved fourth moment gives

    E0(M²K)=h²+O(log^(3/2) m)+o(log m).

Together with E0 K²=h²+O(log m), this gives

    E0(M²−K)²~2log² m.

The weighted compensation satisfies ||A/m||_2=O(√log m/m²). Its contribution to Q is little-o of the norm log m/(√2 m²) of the quadratic compensation. This controls the cross term and proves

    E0 Q²~log² m/(2m⁴).

The statement is a raw second moment. Exact centering of Q or log L is neither assumed nor inferred.

The author uses the inherited window G_m={K+mU≤B_m} with B_m=O(log² m), and both-world exceptional probability β_m=(⌈log₂n⌉+1)m^(−20). This eventually lies inside the deterministic expansion domain and has sup_G|log L|≤23(B_m/m)²→0. The localized remainder-square is O(log⁶ m/m⁶), negligible relative to log² m/m⁴. Globally |Q|≤5 is a valid loose bound, so its square on G_m^c is also negligible. The L² triangle inequality then proves

    E0[(log L)² 1_G]~log² m/(2m⁴).

There is no assertion of a globally bounded Taylor remainder near U=1. The separate global estimate ||log L||_2≤4m² is used only for exceptional entropy.

## 6. Information constants and the singular component

For φ(v)=−log v+v−1, the shrinking uniform window gives φ(exp(a))=(1/2)a²[1+o(1)]. Hence its bulk expectation is asymptotic to log² m/(4m⁴). Outside that window,

    E0[φ(L)1_bad] ≤ 4m²√β_m + 2β_m
                 = o(log² m/m⁴).

The L term is controlled by E0[L1_bad]=Q1({K≤n}∩bad); the alternative's tail estimate is therefore indispensable and is present. Finally the exact formula KL(Q0||Q1)=E0φ(L)+p_n retains the factorially negligible singular mass. This proves the stated reverse-KL constant 1/4.

Similarly, on common support (√L−1)²=(1/4)(log L)²[1+o(1)] uniformly on G. Its complement is at most 1+L and therefore has expectation at most 2β_m. The exact formula

    H²(Q0,Q1)=E0(√L−1)²+p_n

then gives constant 1/8 under the explicit no-half convention. Thus KL/H²→2. Neither result comes merely from probability convergence or a small local score; the integrated moment, remainder, both-world tail, and support corrections each have an identified role.

## 7. Testing upper and lower bounds have different observation scopes

The affinity is ρ=1−H²/2, so −logρ~log² m/(16m⁴). For R independent full exact skylines, the threshold-one likelihood-ratio test has sum of errors ∫min(dQ0^R,dQ1^R)≤ρ^R. The singular event is assigned to world 1. Choosing R=ceil(log(1/α)/(−logρ)) makes the sum at most α and therefore each error at most α. Its sufficient-budget asymptotic multiplier 16log(1/α) is correct. It is not an exact optimal sample-size constant. Substituting 2α would not alone certify each separate error at most α; the author avoids that mistake.

The likelihood is a Borel function of the exact skyline coordinates and the known n,c. This specifies a legitimate ideal statistical test. No finite endpoint-query recovery, finite-real-arithmetic comparison algorithm, or explicit numeric all-n cutoff is inferred.

For the lower bound, revealing a skyline at the first observation of each fresh vector augments the information. The common policy can still be run while ignoring the addition. Its reveal contributes KL(Q0||Q1) in conditional reverse information, while subsequent retained-endpoint answers add none once that skyline is known. Finite actual-action prefixes therefore have KL at most D_m E0 N_T. Unconditional terminal correctness, binary data processing, monotone convergence and lower semicontinuity give

    E0 N ≥ kl(1−α,α)/D_m.

The expectation is baseline E0; infinite expectation satisfies the inequality. Counting starts covers an infinitely queried vector and interleaving. Accuracy conditional only on termination would not suffice. This lower bound applies to the endpoint channel as well as the full-skyline channel. The matching upper bound is proved only in the latter, so the resulting Θ statement is correctly restricted to ideal exact-skyline independent-vector cost, including either the infimum baseline expected cost or worst-world expected cost.

## 8. Controls and assurance limits

The independent diagnostic script verifies:

- second, fourth and sixth derivative polynomials by the Bell recurrence, separately from the author's exponential-series derivation;
- all sixth-moment Hölder exponents and weighted-degree inequalities;
- direct ordered-simplex integrals of U powers, giving Poisson normalization and second/fourth/sixth identities through intensity degree 6;
- rejection when the Poisson empty atom is removed;
- separate exact one-point fixed-count moments, including E0 M⁴=23/75;
- 24 high-precision normalized density/local-Stirling configurations and rejection of omission of the conditioning denominator;
- a bounded normalized-density counterexample to moment transfer without uniform integrability;
- the entropy, squared-Hellinger and affinity factors, including singular-mass signs;
- six finite independent-product likelihood tests checked against the affinity bound.

The frozen author controls completed with exit status zero, and their script, complete JSON output, and stdout are byte-identical to the frozen author files. The separate currentness verification is recorded in the receipt and verification output. These finite controls are mathematical diagnostics, not Monte Carlo, empirical observations, fitted asymptotics, certified numerical intervals or a formal theorem kernel. The written inequalities and exact probability identities carry the asymptotic claims.

No revision to the author's mathematical proof was required by this review. No field-wide novelty, larger-family minimax theorem, all-confidence limit, exact optimal testing constant, sharp total variation, asymptotic normality, finite-probe or physical claim is certified. All archives and author bytes remain unchanged; the historical floor stays UNVERIFIED.
