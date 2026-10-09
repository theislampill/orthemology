# Exact uniform skyline second moments and baseline score localization

8 October 2026 UTC. New scratch-only sibling. The parent supplied the moment candidates; the derivations and exact geometric controls below independently verify them. Historical floor remains UNVERIFIED. No frozen archive or tenth assembly is changed, and there is no protected integration, kernel, empirical, physical-access, or closure claim.

## Result and scope

Let P_1,...,P_n be iid product-uniform points in (0,1)^2. Let S_n be their coordinatewise-minimal skyline, K_n=|S_n|, and

    E_n = {q: no sample point is coordinatewise at most q},
    U_n = area(E_n),
    M_1,n = integral over E_n of xy dx dy,
    T_n = sum over p in S_n of p_x p_y.

Changing the boundaries of E_n does not change its integrals. Set K_0=0, U_0=1, H_0=H_0^(2)=0, and H_j^(r)=sum_(i=1)^j i^(-r). All expectations in this packet are under this uniform baseline; they are not assertions under the Joe alternative.

The proposed identities are correct:

    E U_n = H_(n+1)/(n+1),                              n>=0,       (1)

    E U_n^2 = [H_(n+2)^2-H_(n+2)^(2)
                 +2(H_(n+2)-1)]/[(n+1)(n+2)],          n>=0,       (2)

    E[K_n U_n] = n E U_(n-1)^2
                    -(H_(n+1)-1)/(n+1)
               = [H_(n+1)^2-H_(n+1)^(2)
                    +H_(n+1)-1]/(n+1),                n>=1.       (3)

The final expression in (3) also gives zero at n=0, without invoking U_(-1).

For either a_n=n or a_n=n+1,

    E[(K_n-a_n U_n)^2] = H_n+O(H_n^2/n),                n->infinity,
    K_n-a_n U_n = O_P(sqrt(log n)).                                (4)

In particular the second-moment error tends to zero. With m=n+1, the exact mean is

    E[K_n-mU_n] = -1/m.                                            (5)

For the polynomial leading expression in the active likelihood expansion,

    Q_n = [(K_n-mU_n)^2-K_n]/(2m^2)
            +2[T_n/m-M_1,n],                                     (6)

these identities yield

    E|Q_n| = O(log n/n^2),
    Q_n = O_P(log n/n^2).                                         (7)

Combined with the existing localized likelihood-remainder theorem, this also gives log L_n=O_P(log n/n^2) under the uniform baseline. None of these statements bounds E Q_n^2, likelihood tails, KL, Hellinger, or testing rates; a normal limit or optimality claim does not follow.

## 1. Product integrals and inherited record moments

For a nonnegative integrand b(xy), Tonelli and z=xy give

    integral_[0,1]^2 b(xy) dxdy = integral_0^1 (-log z)b(z) dz.

Write

    A_r = integral_[0,1]^2 (1-xy)^r dxdy = H_(r+1)/(r+1),
    J_r = integral_[0,1]^2 xy(1-xy)^r dxdy
        = (H_(r+2)-1)/[(r+1)(r+2)],                    r>=0.       (8)

The first equality follows by expanding -log(1-t) after substituting t=1-z and telescoping the nonnegative series. The second also follows without differentiating a parameter: J_r=A_r-A_(r+1), followed by H_(r+2)=H_(r+1)+1/(r+2). A fixed query is uncovered with probability (1-xy)^n, so E U_n=A_n, proving (1).

The predecessor count packet proves that sorting independent uniform points by X makes K_N the number of lower records of an iid continuous Y sequence. The successive relative ranks are independent and uniform on {1,...,j}; hence the record indicators are independent Bernoulli(1/j). We consume that established result:

    E K_N = H_N,
    E K_N^2 = H_N^2+H_N-H_N^(2),
    E[K_N(K_N-1)] = H_N^2-H_N^(2).                              (9)

This packet does not claim the record law, (1), or the existing first-moment localization as a new independent contribution. The new increment is the second/cross-moment geometry and its compensated-count/score application.

## 2. The uncovered-area second moment

Take two independent uniform query points p and q, independent of the n sample points, and let R_p=[0,p_x]x[0,p_y]. Conditional on p,q, both queries are uncovered precisely when every sample point avoids R_p union R_q. Thus

    E U_n^2 = integral_(p,q) [1-area(R_p union R_q)]^n dp dq.      (10)

Partition query pairs into the two comparable orientations and the two incomparable orientations; equality boundaries have measure zero.

If p is coordinatewise at most q, the union is R_q. At fixed q, admissible p have area q_x q_y. Therefore this one orientation contributes J_n, and the two comparable orientations contribute 2J_n.

For an incomparable query pair, the event that both queries are uncovered is exactly the event that these two queries are both minimal when appended to the n-point sample. The absence of mutual domination matters here: it is why the same assertion is false on a comparable pair. By exchangeability among the n+2 appended sample labels,

    P(the two specified appended labels are both minimal)
      = E[K_(n+2)(K_(n+2)-1)]/[(n+2)(n+1)].                    (11)

The event on the left already forces incomparability. Consequently (11) is precisely the entire incomparable contribution in (10), with no extra factor of two. Substituting (8) and (9) into (10) proves (2).

As a completely separate integration control, one incomparable orientation can be parameterized by

    p=(tu,s), q=(t,sv),  t,s,u,v in (0,1).

Its Jacobian is ts and its union-rectangle area is ts(u+v-uv). Therefore its contribution is

    I_n = integral_[0,1]^4 ts[1-ts(u+v-uv)]^n dt ds du dv
        = sum_(j=0)^n (-1)^j binom(n,j)/(j+2)^2
             * sum_(r=0)^j (-1)^r binom(j,r)/(r+1)^2.           (12)

The finite polynomial expansion requires no record formula or proposed harmonic second moment. Exact rational evaluation verifies E U_n^2=2(J_n+I_n), as well as 2I_n=(11), at the control values described below.

## 3. The count-area cross moment

Expand K_n into the n indicators that a chosen sample point p is minimal and use Tonelli for the query integral defining U_n. For the joint event

    {p is a sample minimum and q is uncovered},

the n-1 other sample points must avoid R_p union R_q, and p must not be coordinatewise at most q. These conditions are necessary and sufficient. The query q is not itself a sample point, so q being at most p does not disqualify p from being a sample minimum.

Without the restriction p not<=q, the integral over p,q is exactly E U_(n-1)^2. The excluded orientation p<=q contributes J_(n-1). The other comparable orientation remains allowed. Hence

    E[K_n U_n] = n[E U_(n-1)^2-J_(n-1)].                       (13)

Using n J_(n-1)=(H_(n+1)-1)/(n+1) gives the first version of (3). Inserting (2) at n-1 and collecting terms gives the second. This single-orientation subtraction is essential; subtracting both orientations would give an incorrect cross moment.

At n=1, K_1=1 and U_1=1-(1-X_1)(1-Y_1). Direct elementary integration gives

    E U_1=3/4, E U_1^2=1-2/4+1/9=11/18,
    E[K_1 U_1]=3/4,
    E[(K_1-2U_1)^2]=4/9.                                    (14)

At n=0, (2) gives U_0^2=1 exactly.

## 4. Compensated-count localization with the cancellation preserved

Put m=n+1, h=H_m, and g=H_m^(2). By (2), (3), and (9), expanding the square and using H_n=h-1/m gives the following useful exact remainder:

    E[(K_n-mU_n)^2] = H_n + Delta_m,

    Delta_m = -2h/m+2/m^2
                -(h^2-g-4)/(m+1)-2(h+1)/(m+1)^2.              (15)

This identity is obtained from the exact moments before any asymptotic bound is taken. Bounding E K_n^2 and m^2 E U_n^2 separately would lose the cancellation and yield only a log-squared bound.

For m>=2, h>=1 and 0<=g<=h. Termwise bounds in (15) give, for example,

    |Delta_m| <= 11 h^2/m.                                    (16)

Indeed the four absolute terms are at most 2h^2/m, h^2/m, 6h^2/m, and 2h^2/m respectively. Since H_m/H_n->1, (15)-(16) prove the first assertion of (4) for a_n=m. Also H_n=log n+O(1), so H_n^2/n->0.

To obtain the same statement for a_n=n, set C_m=K_n-mU_n. Then K_n-nU_n=C_m+U_n. Formula (2) gives E U_n^2=O(H_n^2/n^2), while (15) gives E C_m^2=O(H_n). Cauchy-Schwarz consequently yields

    |E[(C_m+U_n)^2]-E C_m^2|
      <= 2 sqrt(E C_m^2 E U_n^2)+E U_n^2
       = O(H_n^(3/2)/n+H_n^2/n^2)
       = O(H_n^2/n).                                         (17)

This proves the n version without assuming a covariance sign. The exact means, from (1) and (9), are

    E[K_n-mU_n] = -1/m,
    E[K_n-nU_n] = (H_m-1)/m.                                 (18)

Markov applied to either compensated square establishes the O_P assertion in (4). In fact the corresponding variances are also H_n+o(1), because both means tend to zero. This does not identify their limiting distribution or prove a lower bound in probability on their magnitude.

## 5. The polynomial score has an L1 and probability upper bound

A specified point p contributes p_x p_y to T_n if it is minimal. Conditioning on its coordinates gives

    E T_n = n J_(n-1) = (H_m-1)/m,
    E M_1,n = J_n = (H_(m+1)-1)/[m(m+1)].                     (19)

These are nonnegative quantities. Their first moments alone imply T_n/m=O_P(log n/n^2) and M_1,n=O_P(log n/n^2). Together with E[(K_n-mU_n)^2]=O(log n) and E K_n=H_n, the triangle inequality gives directly

    E|Q_n| <= [E(K_n-mU_n)^2+H_n]/(2m^2)
                 +2 E T_n/m+2 E M_1,n
             = O(log n/n^2).                                 (20)

Thus (7) is a valid L1 upper bound as well as a probability bound. It neither states nor implies an L2 bound for Q_n.

There is a further elementary exact first-moment consequence, useful mainly to prevent an incorrect claim of exact centering:

    E Q_n = Delta_m/(2m^2)
               +2[(h-1)/(m^2(m+1))-1/(m(m+1)^2)]
          = O(H_m^2/m^3).                                    (21)

For example E Q_1=-7/72, so the polynomial is not exactly centered. Equation (21) does not evaluate E log L: the existing remainder is only localized, and the displayed polynomial's small mean can be affected by both higher-order terms and exceptional tails.

The active score packet proves, on K_n/m<=1/2 and U_n<=1/2,

    log L_n = Q_n + R_n,
    |R_n| <= 40(K_n/m+U_n)^3.

Its already-established first-moment localization gives R_n=O_P((log n)^3/n^3) under the baseline. One rigorous reading is to define R_n=log L_n-Q_n on the whole common support and use the high-probability localization to prove this O_P assertion; no pointwise bound outside that set is asserted. Since (log n)^3/n^3=o(log n/n^2), combining it with (7) proves the baseline log-likelihood probability bound stated above. Under P0 every skyline is on common support, so this statement does not ignore an alternative-only stratum.

## 6. Verification and retained boundaries

controls.py and CONTROL_RESULTS.json provide reproducible deterministic controls:

- Exact rational polynomial integrations (8) and (12) for every n=0,...,32, independently of the proposed harmonic second/cross-moment formulas.
- Exact count, squared-count, and factorial-count moments by enumerating every permutation for N=1,...,8, independently of the record-indicator calculation.
- Exact checks of (15), (18), (19), and (21), and nonnegativity of both compensated second moments.
- Explicit n=0 and n=1 boundary controls, including (14).
- Deliberately wrong candidates are rejected: omitting the comparable query contribution, and subtracting both comparable orientations from the cross moment.
- Ten independent 70-decimal one-dimensional quadrature comparisons for A_n and J_n at n=0,1,2,5,20; every observed discrepancy is below 10^(-60). This is a numerical agreement report, not an interval-certified error bound.
- Deterministic scaling evaluations through n=10^12, using the algebraically stable remainder (15). They illustrate the proved asymptotic and are not used as its proof.

All controls pass. No candidate mathematical error was found. The analytical partition of query pairs and the exact cross-event characterization carry the general claims; finite calculations are checks.

This is a baseline-only increment. Equality between worlds of the one-query uncovered probability does not imply equality of two-query void probabilities, E U_n^2, or E[K_n U_n]. No Joe-alternative second moment is imported or inferred.

Still open: fourth compensated moments or other adequate uniform-integrability/tail estimates; E Q_n^2 and any exact leading variance; integrated likelihood remainder control; sharp skyline KL/TV/Hellinger asymptotics; any improved valid test; asymptotic normality; finite-probe realization and physical interpretation. In particular (7), (20), and even the exact mean (21) do not establish a testing scale. No field-wide novelty is claimed: the methods are elementary record moments, exchangeability, query-integral geometry, and inequalities.

Attribution: the parent supplied (2), (13), the expected cancellation in (4), and the candidate application to (6). This packet independently verifies those candidates, supplies the simplified cross moment, exact compensated remainder, rational geometric controls, and explicit L1/mean consequences. The inherited count law and the active packet's first-moment/remainder results remain credited to their existing packets. See SOURCE_AUDIT.md for the consumed source digests. Scope ends at this verified scratch increment; it does not certify the entire project or change its historical floor.
