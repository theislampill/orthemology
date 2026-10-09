# Bounded review: uniform skyline moments

8 October 2026 UTC. Disposition: **PASS for the bound packet's written baseline claims; no required correction found.** This is review evidence for the parent, not project acceptance or closure authority.

Target: `../baseline-skyline-moments/RESULT.md`

SHA-256: `b7bdcfa8b7288d69d569b6ed904c314fe58e4795c92549a6d525c433ad7c139f`

The parent supplied the candidate and the original worker verified it. This cold review re-derives the mathematics and checks the controls, but **does not add another independent source witness or validate either world**. It uses the same declared iid product-uniform model. Historical floor remains **UNVERIFIED**.

## 1. Two-query and added-point derivation

Write A_r=∫(1−xy)^r dxdy=H_(r+1)/(r+1) and J_r=∫xy(1−xy)^r dxdy=A_r−A_(r+1)=(H_(r+2)−1)/[(r+1)(r+2)]. These follow by the product substitution and a nonnegative logarithmic series. A fixed query is uncovered with probability (1−xy)^n, giving E U_n=A_n.

For two independent uniform queries p,q, both are uncovered exactly when all n sample points avoid R_p∪R_q. On p≤q, the union is R_q and integration over p supplies q_x q_y. Each comparable orientation therefore contributes J_n.

On incomparable p,q, being jointly uncovered is equivalent to both added labels being minima in the enlarged sample of n+2 iid points. Exchangeability makes that probability

    E[K_(n+2)(K_(n+2)−1)]/[(n+2)(n+1)].

The event that both added labels are minima already forces incomparability. This probability includes both incomparable orientations; multiplying by two again would be wrong. Lower-record insertion ranks are independent uniforms on {1,...,j}, so E K_N=H_N and E[K_N(K_N−1)]=H_N²−H_N^(2). Consequently

    E U_n² = [H_(n+2)²−H_(n+2)^(2)+2(H_(n+2)−1)]/[(n+1)(n+2)].

For K_n U_n, distinguish a sample label p and a query q. The other n−1 points must avoid R_p∪R_q, and p≤q must be excluded because p itself would cover q. The orientation q≤p is allowed: q is a query, not a competing sample label. Thus, for n≥1,

    E[K_n U_n] = n[E U_(n−1)²−J_(n−1)]
               = [H_(n+1)²−H_(n+1)^(2)+H_(n+1)−1]/(n+1).

This is a fixed-sample-size argument. The added n+2-point sample is an exchangeability device, not Poissonization, and no random sample-size identity has been substituted. The count moments consumed here are inherited record facts, not a new source contribution.

## 2. Boundary checks and compensation

At n=0, U_0=1 and K_0=0; the area-square formula gives 1 and the simplified cross formula gives 0. The expression involving U_(n−1) is not used there. With m=1 the formal polynomial Q_0 is 0; this is only an algebraic extension, not a zero-route instance of the n≥1 likelihood hard pair.

At n=1, U_1=X+Y−XY and K_1=1. Direct sample-coordinate integration gives

    E U_1=3/4, E U_1²=11/18, E[K_1 U_1]=3/4,
    E(K_1−2U_1)²=4/9, E(K_1−U_1)²=1/9.

Set m=n+1, h=H_m, g=H_m^(2), C_m=K_n−mU_n. Substitution of the exact moments, before asymptotic bounds, gives

    E C_m² = H_n+Δ_m,
    Δ_m = −2h/m+2/m²−(h²−g−4)/(m+1)−2(h+1)/(m+1)².

The displayed identity and the exact means E C_m=−1/m and E(K_n−nU_n)=(h−1)/m are correct. The packet's |Δ_m|≤11h²/m bound is valid for m≥2. Therefore E C_m²=H_n+O(H_n²/n), with an additive error tending to zero. The n coefficient follows from K_n−nU_n=C_m+U_n, E U_n²=O(H_n²/n²), and Cauchy–Schwarz. Both variances are H_n+o(1), but neither a normal limit nor a probability lower bound on magnitude follows. There is no lost log-squared term or unsupported covariance-sign assumption.

## 3. The score normalization, L1 bound, and mean

The active score uses **m=n+1** throughout:

    Q_n=(C_m²−K_n)/(2m²)+2(T_n/m−M_1,n).

Direct conditioning gives E T_n=(h−1)/m and E M_1,n=(H_(m+1)−1)/[m(m+1)]. Both quantities are nonnegative, so

    E|Q_n| ≤ [E C_m²+H_n]/(2m²)+2 E T_n/m+2 E M_1,n
            = O(log n/n²).

This proves precisely the asserted L1 and O_P upper bounds. In particular the denominators and coefficient of T_n are not replaced by n.

The exact polynomial mean is

    E Q_n = Δ_m/(2m²)
              +2[(h−1)/(m²(m+1))−1/(m(m+1)²)].

It is not identically zero: independent direct integration at n=1 gives −7/72. For additional asymptotic clarity, g is bounded and the exact expression yields

    E Q_n = −h²/(2m³)+O(h/m³+h²/m⁴)
          ∼ −h²/(2m³).

Thus the packet's O(H_m²/m³) assertion is valid. This asymptotic is only about the polynomial's baseline first moment. It is not E log L, KL, or a testing-information formula.

The inherited deterministic bound |R_n|≤40(K_n/m+U_n)³ is localized. Together with the inherited first-moment localization it gives R_n=O_P((log n)³/n³), and hence log L_n=O_P(log n/n²) under the baseline, whose support is common. It does **not** give an integrated remainder estimate. Nothing here proves E Q_n², a leading score variance, uniform integrability, likelihood-tail control, sharp KL/TV/Hellinger asymptotics, or a new testing rate. Equality of one-query void probabilities between worlds is not used to transfer either new joint moment to the Joe law.

## 4. Verification and scope

- Read the full target proof, controls, generated results and logs, attribution, and the three cited predecessor RESULT files. Their digests match the declared versions; see `CHECK_RESULTS.json`.
- Reran a byte-identical copy of the source controls inside this review sibling. It passed and reproduced the source `CONTROL_RESULTS.json` byte-for-byte. The source packet was not executed in place or rewritten.
- A separately written direct multinomial expansion of (u+v−uv)^j checks the geometric moments exactly for n=0,...,16. It differs from the source control's complementary-product double sum. Wrong orientation factors/subtractions are rejected.
- Symbolic algebra checks the compensation and exact Q-mean identities. Direct two-dimensional sample integration checks n=1, including E Q_1. These are deterministic controls, not empirical data or kernel proofs. The event decomposition and inequalities above carry the general result.
- All ten bound input-file digests remained unchanged after the checks. Only the new `baseline-skyline-moments-review` sibling was written.

No source, archive, tenth assembly, protected integration, GitHub state, lifecycle, or historical-floor certification was changed. No physical observation, independent external source witness, field-wide novelty, or world validation is claimed. Other ongoing score work is not a dependency of this review and was not inspected.
