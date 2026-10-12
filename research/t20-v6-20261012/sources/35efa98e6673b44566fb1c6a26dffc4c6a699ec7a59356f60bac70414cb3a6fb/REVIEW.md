# Independent review: infinite initial Fisher–Rao correction-path length

11 October 2026 UTC. Scoped ordinary mathematical review. Verdict: **valid; no countercorrection required**.

## Immutable reviewed bindings and scope

- `infinite-initial-fisher-length-20261011/RESULT.md`, SHA-256 `e8743a543021cd86d205c7b757c038f2acaeb80e0ecc117f1ebf1cef6d6493ec`.
- `positive-high-order-correction-20261011/RESULT.md`, SHA-256 `72dccf1dd0f129899234b6fcaf43db50e2b289c73fbfd8a3e71e88b8d334dcdb`.

Only these two supplied mathematical reports were read. The second was used for its fixed, nonnegative, finite-almost-everywhere loss class, positive-time geometry convention, and arbitrary-initial-law fixed-positive-endpoint theorem. This review independently checks the new counterexample and finite-mean repair; it does not newly re-review the entire approximation theorem, survey the corpus, alter protected sources, or assert formal verification or noetic consequences.

## 1. Initial law, smoothing, and measure differentiability

For n≥1, p_n=1/[2n(n+1)] and p_0=1/2. Telescoping gives sum_{n≥1}p_n=1/2. Every V_n=exp(n²) is finite, V_0=0, and the initial mean is infinite (even its individual positive-index summands do not tend to zero). Thus the law satisfies the supplied arbitrary-law class and fails finite initial energy.

For t≥0 let w_n(t)=p_n exp(−tV_n), B(t)=sum_n w_n(t), and q_n(t)=w_n(t)/B(t). Then 1/2≤B(t)≤1. Dominated convergence yields B(t)→1 and w(t)→p in ℓ¹ at zero; normalization consequently yields q(t)→p in total variation.

On each compact time interval [a,b] with a>0, every k≥0 has sum_n p_n V_n^k exp(−aV_n)<∞: the scalar function v^k exp(−av) is bounded. Local domination with a smaller positive lower endpoint justifies differentiating the ℓ¹-valued weights to every order. Since B is positive, q is C∞ in ℓ¹ on (0,∞). In particular, with m(t)=sum_n q_n(t)V_n,

    q'_n(t)=−(V_n−m(t))q_n(t).

This is a genuine total-variation derivative, not merely coordinatewise differentiation. All positive-time loss moments are finite.

There is no finite total-variation right derivative at zero in this example. Indeed,

    [1−B(t)]/t = sum_n p_n[1−exp(−tV_n)]/t → +∞

by monotone convergence as t decreases to zero (or Fatou for the necessary lower bound). Hence

    [q_0(t)−p_0]/t = p_0[1−B(t)]/[tB(t)] → +∞.

A derivative of a probability curve in total variation would have a finite derivative on the singleton {0}, which is impossible here. The report correctly confines its derivative assertion to positive times.

## 2. Fisher–Rao convention and actual arc length

Under g_q(u,u)=sum_n u_n²/q_n, the positive-time tangent norm is

    ||q'(t)||_FR² = sum_n q_n(t)(V_n−m(t))² = Var_{q(t)}V.

This also gives genuine metric arc length. Set x(t)=(sqrt(q_n(t)))_n in ℓ². On a delayed compact interval x is C¹ (indeed smooth) by exponential domination, and 2||x'(t)||_2=sqrt(Var_{q(t)}V). The square-root embedding into the radius-two Hilbert sphere is the Fisher–Rao isometry. Thus each delayed subarc has length equal to the integral of this speed. The initial curve is continuous also in this embedding because sum_n(sqrt(q_n)−sqrt(p_n))²≤sum_n|q_n−p_n|. Infinite length below is therefore nonrectifiability of a continuous curve, not failure to have an endpoint or an inference from a nonexistent initial tangent.

## 3. Lower bound, coefficient, and disjoint intervals

Finite positive-time second moments justify the nonnegative double-series identity

    Var_q V = (1/2)sum_{i,j}q_i q_j(V_i−V_j)².

The ordered terms (0,n) and (n,0) together give exactly q_0 q_n V_n². There is no missing or extra factor of two.

For I_n=[1/V_n,2/V_n], the next interval lies strictly below the preceding one since V_{n+1}/V_n=exp(2n+1)>2. On I_n,

    q_0(t)=p_0/B(t)≥p_0,
    q_n(t)=p_n exp(−tV_n)/B(t)≥p_n exp(−2).

Using B≤1 in these lower bounds is correct. Therefore

    integral_{I_n} sqrt(Var_{q(t)}V) dt
       ≥ exp(−1)sqrt(p_0p_n)
       = 1/[2e sqrt(n(n+1))]
       ≥ 1/[2e(n+1)].

For any ε>0, all sufficiently large n have I_n⊂(0,ε]. Summing over any finite collection of these disjoint intervals lower-bounds the length on a delayed compact interval containing them. The lower bounds become arbitrarily large by harmonic divergence. Equivalently, countable additivity for the nonnegative speed integral yields an infinite integral on (0,ε]. Both arguments establish infinite initial arc length. Each fixed [τ,T], 0<τ≤T<∞, still has finite length because its speed is continuous and bounded.

The final root report’s appended path-versus-distance clarification was separately read and checked. For u_n=sqrt(p_n) and v_n=sqrt(q_n(t)), the affinity A=sum_n u_n v_n is positive. The nonnegative great-circle path between these unit vectors has Fisher–Rao length 2 arccos(A)<π, and realizes the intrinsic endpoint distance in the stated convention. Thus the prescribed exponential-tilt orbit has infinite initial length while a different path between its endpoints has finite length. Neither infinite endpoint separation nor impossibility of correction follows.

## 4. Finite initial mean repair

For an arbitrary initial probability and measurable finite nonnegative V, let M(t)=E_{q(t)}V. At t>0 differentiating the first-moment numerator and denominator gives

    M'(t)=−Var_{q(t)}V.

If M(0)=E_pV<∞, monotone convergence of V exp(−tV) as t decreases to zero, together with B(t)→1, gives M(t)→M(0). Integrating on [a,T] and then letting a decrease to zero proves

    integral_0^T Var_{q(t)}V dt = M(0)−M(T)<∞.

Cauchy–Schwarz on (0,T) gives exactly the asserted bound

    L_FR(q|_[0,T])≤sqrt(T[M(0)−M(T)]).

Endpoint continuity and the square-root formulation justify extending the arc-length conclusion to the closed interval. Finite variance at time zero is unnecessary for this repair. All statements retain the report's nonnegative-loss and unit-rate metric convention; a fixed finite lower baseline could be subtracted without changing the normalized exponential flow.

## 5. Optional analytical separation: finite mean is not necessary

This is an additional check, not needed to validate the report. Keep V_0=0 and V_n=exp(n²), but set p_0=1/2 and p_n=1/[2ζ(4)n⁴] for n≥1. The initial mean is still infinite, while sum_{n≥1}sqrt(p_n)<∞.

Put r_n(t)=sqrt(p_n)exp(−tV_n/2), so x=r/||r||_2 and ||r||_2≥sqrt(p_0). On every delayed interval,

    ||x'(t)||_2≤||r'(t)||_2/sqrt(p_0)≤sum_{n≥1}|r'_n(t)|/sqrt(p_0).

Tonelli and direct scalar integration yield

    L_FR≤[2/sqrt(p_0)]sum_{n≥1}sqrt(p_n)[1−exp(−TV_n/2)]
        ≤[2/sqrt(p_0)]sum_{n≥1}sqrt(p_n)<∞.

Thus finite initial mean is strictly a sufficient condition, as the report carefully states. Infinite mean alone would not establish the counterexample's conclusion; the separated-scale harmonic lower bound does that work.

## Conclusion and limits

The root counterexample correctly separates positive-time moment regularization and fixed-positive-endpoint high-order approximation from finite initial Fisher–Rao path length. Its proof, constants, normalization direction, and finite-mean repair all pass. No mathematical alteration is required. No finite numerical experiment was used or claimed to prove divergence. No statement about psychological improvement, empirical validity, effective reconstruction, or audit closure follows.
