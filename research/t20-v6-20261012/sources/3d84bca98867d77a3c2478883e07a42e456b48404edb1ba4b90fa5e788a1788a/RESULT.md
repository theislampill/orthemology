# Effective exponential-tilt continuation: interior and endpoint

10 October 2026 UTC. Additive ordinary mathematical research in ACTIVE T20.
No protected edit, canonical integration, field-priority claim, fresh formal-kernel claim, sampling-optimization programme, or T20 closure.

## 1. Outcome and inherited boundary

A supplied computable positive exponential-moment bound makes the full raw-moment record effectively sufficient for every strictly interior normalized tilt on the half-line. The result is uniform in the moment name, exponent and bound, the requested grade, precision, and any computable control parameter u > −a. Arbitrarily large positive u are covered by finitely many certified small steps, rather than by a formal series outside its radius or by an ineffective appeal to analytic continuation.

The endpoint u = −a is different even though its normalizer is finite. A computable original law with a uniformly computable full moment record and the fixed exponential bound 4/3 can have a noncomputable endpoint normalizer and endpoint law. That control's positive-order endpoint moments are infinite. A separate, stronger uniform counterexample has an exactly computable endpoint normalizer and a finite-support endpoint law in every instance, yet no uniform endpoint-mean algorithm exists. Thus the first control is not misapplied to an all-moments-finite endpoint theorem.

The inherited ownership is narrow and explicit:

- `measure-moment-continuation-boundary-20261009/RESULT.md`, §§2 and 6.1, already specifies the raw half-line trait, normalized tilt, original mean output, infinite hierarchy, and ordinary determinacy under some positive exponential moment. Its lognormal negative result applies when this tail hypothesis is absent.
- Its §3 gives the compact exponential series; §6.2 identifies the bounded-coordinate compactification and warns that determination alone is not an effective unbounded-output algorithm.
- `capped-tensor-recovery-20261010/RESULT.md`, §8, has already made bounded-simplex tensor continuation effective by explicit series tails. Its stronger capped indexed-law inverse, and its uncapped indexed-law counterexample, have different input and output representations.
- The present addition supplies an explicit represented-input, noncompact continuation algorithm and the strict-interior/endpoint controls. The probability formulas, positive-series arguments, elementary bounds, and halting-encoding mechanism are classical tools, not new general probability or computability principles.

This packet concerns continuation of the original raw observable x and all its integer powers. It does not replace that output by a bounded proxy, compute an arbitrary indexed hidden observable, or assert a finite exact moment cutoff.

## 2. Representation and mathematical domain

Input is a Borel probability μ on [0,∞), presented through:

1. A uniform full moment name: on input integers r,k ≥ 0, an oracle returns a rational within 2^−k of m_r = ∫x^r dμ. The validity promise includes m_0 = 1. Separate, nonuniform computability of individual moments is not this input.
2. Names of computable real numbers a > 0 and finite M such that

       ∫exp(a x) dμ ≤ M.                                      (1)

   In particular M ≥ 1. A rational upper bound is an allowed special case. Neither an exact value of this integral nor an effective tail modulus at exponent a is supplied.
3. A computable real u with the strict promise u > −a.

All statements are Type-2 uniform relative to these names. Validity, integrability promises, and equality to the endpoint are not decidable tests claimed here. Rational strict lower or upper bounds on already positive computable quantities can be found by refining their names.

Set

    A_r(u) = ∫x^r exp(−u x) dμ,
    Z(u) = A_0(u),
    T_u μ(dx) = exp(−u x) μ(dx)/Z(u).

For u > −a and r ≥ 0,

    x^r exp(−u x) ≤ r! (a+u)^−r exp(a x),                     (2)

with the r = 0 convention. This follows from y^r/r! ≤ exp(y), y = (a+u)x. Thus every A_r(u) is finite, Z(u) is positive, and T_u μ has all polynomial moments. Its original mean output is q(u) = A_1(u)/Z(u); q(0) = m_1 is already part of the input.

At u = −a, (1) still ensures 1 ≤ Z(−a) ≤ M, but it does not ensure A_r(−a) < ∞ for r ≥ 1. Parameters u < −a have no general integrability guarantee. Admitted tilts compose by cancellation whenever the measures involved are defined. No globally defined two-sided group on the original whole law class is asserted.

## 3. Local computation with a geometric remainder

### Lemma E1: a certified small tilt

Let ν be a probability with a uniform full moment name and ∫exp(bx)dν ≤ C, with computable b > 0 and C. If h is computable and |h| < b, then for every r ≥ 0,

    B_r(h) := ∫x^r exp(−h x)dν
            = Σ_(n=0)^∞ (−h)^n m_(r+n)(ν)/n!.                (3)

For any computable c with |h| < c < b, truncation after n = R has error at most

    C r! (b−c)^−r (|h|/c)^(R+1).                            (4)

**Proof.** The absolute integrand series is x^r exp(|h|x), which is integrable by (2) with the positive margin b−|h|. This justifies integration term by term. For x ≥ 0,

    Σ_(n>R) (|h|x)^n/n!
      ≤ (|h|/c)^(R+1) exp(cx),

and x^r exp(cx) ≤ r!(b−c)^−r exp(bx). Integration proves (4). Computable rational upper bounds on the prefactor and on |h|/c strictly below one give a terminating choice of R for any error request. Each finite sum uses finitely many moment queries, with their errors budgeted against finitely many computable coefficients. ∎

The denominator B_0(h) is strictly positive. An explicit lower bound follows from Jensen and m_1(ν) ≤ C/b:

    B_0(h) ≥ exp(−|h| C/b) > 0.                             (5)

Hence division computes every m_r(T_hν) = B_r(h)/B_0(h). Nothing here uses exact comparison of h with zero. If h = 0, the zero tail is interpreted directly; the interior construction below uses a positive rational upper ratio and needs no zero test.

A normalized small step also retains a positive exponential margin. If b+h > 0, then

    ∫exp((b+h)x)d(T_hν) = [∫exp(bx)dν]/B_0(h).               (6)

The following global bounds make repeated steps uniform without iterating enormous ad hoc bounds.

## 4. Uniform finite-step continuation throughout u > −a

### Theorem E2: effective interior continuation

From the input in §2 one can compute Z(u), every A_r(u), and every moment m_r(T_uμ), uniformly in u, r and requested precision. In particular the original raw mean q(u) is computable.

**Proof.** Effectively choose positive rationals d, H and B with

    d < min(a,a+u),      H > M,      B > |u|.

This succeeds using strict promised inequalities and computable min; no test of the sign of u or equality with zero is required. Put

    L = exp(−B H/a),      C = H/L.

For every v on the line segment joining 0 and u, one has v > −a and −v ≤ a. Thus exp(−v x) ≤ exp(a x) for x ≥ 0, giving Z(v) ≤ M < H. Also m_1(μ) ≤ M/a < H/a and Jensen gives

    Z(v) ≥ exp(−v m_1(μ)) ≥ exp(−B H/a) = L.

In particular, with ν_v = T_vμ and b_v = a+v,

    b_v ≥ min(a,a+u) > d,
    ∫exp(b_v x)dν_v = [∫exp(ax)dμ]/Z(v) ≤ C.                (7)

Choose an integer N ≥ 1 with 2B/N < d, and define

    h = u/N,      v_j = jh,      b_j = a+v_j,
    q = 2B/(Nd) < 1,      j = 0,…,N.

There are exactly N steps. All segment points satisfy (7). For each step j < N, |h| < b_j/2; apply E1 with c = b_j/2. Uniformly in j, the grade-r remainder after R terms obeys

    error ≤ C r! (2/d)^r q^(R+1).                           (8)

Here q is a known rational strictly between zero and one. A rational upper bound C_bar > C gives the fully rational search condition

    C_bar r! (2/d)^r q^(R+1) < ε

for any rational target ε > 0. Such an R is found by integer/rational arithmetic.

The local normalizer is exactly

    B_0^(j)(h) = Z(v_(j+1))/Z(v_j) ≥ L/H.                   (9)

A positive rational D < L/H can be computed once for all N divisions. For completeness, the local numerator also satisfies B_r^(j)(h) ≤ C r!(2/d)^r, by applying (2) at the current law with b_j−|h| > d/2. These upper and lower bounds give direct finite error budgets for normalized quotients. For example, if |n−n_hat| ≤ η, |z−z_hat| ≤ η < D/2, z ≥ D, and |n| ≤ K, then

    |n_hat/z_hat − n/z| ≤ 2η/D + 2Kη/D².                    (10)

Start from the supplied full moment name of ν_0 = μ. Equations (3), (8) and (9) compute a full moment name of ν_1; repeat to ν_N = T_uμ. A requested grade/precision at stage j+1 needs only finitely many earlier-grade/precision queries. The recursion has finite depth N, so its expanded oracle computation terminates. It never needs an infinite array to be computed before the next step.

The product of the N computable local normalizers gives Z(u), since Z(0) = 1. Then A_r(u) = Z(u)m_r(ν_N) is computable. This proves all claimed outputs. ∎

### Consequences and limitations

The theorem covers the original nonnegative, finite piecewise-constant controls by evaluating their computable finite cumulative u(t), and also the explicitly enlarged signed interior parameters. A finite control history whose cumulative value remains strictly above −a may be handled at its named interior times. A compact parameter range with a supplied positive distance from −a admits common constants d,B and finite step count. No uniform quantitative bound persists as that distance tends to zero by this argument.

This is a finite-use algorithm for each accuracy, not a complexity estimate or an optimal cutoff. Intermediate moment grades and precision may grow. The direct series about zero need not converge for large positive u; the proof evaluates only certified local series. No existence-only analytic continuation theorem supplies a missing algorithm.

The exponential bound already implies ordinary moment determinacy by the inherited proof. The new algorithm does not need to compute an indexed law first. It computes precisely the tilt normalizer and raw-moment/output family, not every unbounded observable whose expectation happens to exist.

## 5. A finite endpoint normalizer can be noncomputable

### Theorem E3: fixed-input endpoint obstruction

There is a computable probability μ on the nonnegative integers, with uniformly computable all polynomial moments and with computable a > 0 and the fixed bound M = 4/3 in (1), such that Z(−a) is finite and noncomputable. Its normalized endpoint law is noncomputable even in the ordinary weak probability-measure representation.

**Construction.** Fix an effective machine enumeration with undecidable diagonal halting set K. Set w_e = 4^(−e−1), so Σ_e w_e = 1/3, and

    α = Σ_(e∈K) w_e.

This real is noncomputable. After earlier digits have been decided and subtracted, at index e the residual is at least w_e if e ∈ K and at most w_e/3 if e ∉ K. An approximation with error at most w_e/12 and threshold 2w_e/3 decides these alternatives recursively. A computable α would therefore decide K.

Use the computable Cantor bijection

    pair(e,t) = (e+t)(e+t+1)/2+t,      j = 1+pair(e,t).

Whether machine e on input e first halts at exactly stage t is decidable by a finite simulation, including the specified initial configuration at t = 0. Each halting e has exactly one event index j_e. At positive integers define

    p_j = w_e exp(−a j) if j codes that first-halting event,
          0 otherwise;
    P = Σ_(j≥1) p_j,      p_0 = 1−P,
    μ = Σ_(j≥0) p_j δ_j.                                    (11)

The construction can use the fixed a = 1; it is also uniform for any computable a > 0. All p_j with j ≥ 1 are uniformly computable. Since P ≤ 1/3, p_0 ≥ 2/3 and μ is a probability.

**Original-law and moment computation.** Choose a known rational b with 0 < b ≤ a. For r ≥ 0 and any integer J ≥ 0,

    Σ_(j>J) j^r p_j
      ≤ (r!/3)(2/b)^r exp(−b(J+1)/2).                        (12)

Indeed j^r exp(−aj) ≤ r!(2/b)^r exp(−bj/2), and the sum of event weights in any tail is at most 1/3. The bound tends effectively to zero, uniformly in r. Finite simulation computes the terms with j ≤ J. Formula (12) at r = 0 computes P and p_0; at r ≥ 1 it computes m_r, while m_0 = 1. The same tail bound computes the integer-indexed law in ℓ¹, which in particular computes it as a probability measure. All original-input requirements are therefore met.

**Endpoint failure.** At u = −a,

    Z(−a) = p_0 + Σ_(e∈K) w_e = p_0+α ≤ 4/3.                (13)

This is noncomputable because p_0 is computable and α is not. The endpoint law assigns mass p_0/Z(−a) to zero. To avoid assuming that arbitrary singleton masses are computable from a weak measure name, use the explicit bounded computable continuous function

    φ(x) = max(1−2x,0),      x ≥ 0.

On this integer support its integral under T_(−a)μ is exactly p_0/Z(−a). A computable endpoint probability measure would compute that positive integral and hence Z(−a), a contradiction. ∎

### The endpoint-moment restriction is real

Every positive integer moment of this endpoint law is infinite. Undecidability of K implies infinitely many halting indices e have first-halting time t_e > 4^(e+1). If only finitely many did, simulation for 4^(e+1) steps plus finitely many hard-coded exceptions would decide K. Along these infinitely many events j_e ≥ t_e and

    w_e j_e > 1,      w_e j_e^r ≥ w_e j_e > 1   (r ≥ 1).

Thus Σ_(e∈K) w_e j_e^r diverges. The normalized endpoint law exists, but it lies outside the inherited all-polynomial-moments-finite class. E3 does not refute a theorem that promises that stronger endpoint admissibility. The next control treats that different promise directly.

## 6. Exact normalization plus finite endpoint moments still lacks a uniform mean algorithm

### Theorem E4: all-moments-finite endpoint uniform obstruction

Even with a computable exact Z(−a) supplied, no uniform operation computes the endpoint mean from the §2 inputs plus the promise that T_(−a)μ has every polynomial moment finite. This remains true for a computably indexed family with a = 1, M = 2, and an endpoint law supported on at most two integers in every instance.

**Proof.** For machine e on input e, if it first halts at stage t put j = t+2 and define

    ν_e = (1−1/j)δ_0 + (1/j)δ_j;

if it never halts define ν_e = δ_0. Define

    D_e = ∫exp(−x)dν_e,
    μ_e(dx) = exp(−x)ν_e(dx)/D_e.

One always has 1/2 ≤ D_e ≤ 1. If a halt at j is known,

    D_e = 1−1/j+exp(−j)/j,
    μ_e({j}) = exp(−j)/(jD_e),
    μ_e({0}) = 1−μ_e({j}).                                  (14)

If no halt has been seen through stage T, any later halt has j ≥ T+3. Its possible change from D_e = 1 is at most 1/(T+3), so D_e is computable uniformly in e. Thus Z_e := 1/D_e is uniformly computable, with 1 ≤ Z_e ≤ 2. In fact |Z_e−1| ≤ 2/(T+3) is a sufficient undecided-halt error bound. The endpoint law ν_e itself is uniformly computable as an ℓ¹ law: its distance to δ_0 in that norm is at most 2/(T+3) if the halt has not yet been seen. This does not reveal whether the tiny positive atom will eventually exist.

The original moments of μ_e are uniformly computable in e and grade. Grade zero is one. For r ≥ 1 a still-undetected halt contributes

    m_r(μ_e) = j^(r−1) exp(−j)/D_e
       ≤ 2(r−1)! 2^(r−1) exp(−(T+3)/2).                    (15)

This follows from y^(r−1)/(r−1)! ≤ exp(y) at y = j/2. Choose T making this bound small, simulate, and return zero if still undecided; if a halt is observed, evaluate (14). This gives one uniform all-moment name for μ_e. Its original law is likewise computable.

The exponential input bound and exact endpoint formula are

    ∫exp(x)dμ_e = 1/D_e = Z_e ≤ 2,
    T_(−1)μ_e = ν_e.                                        (16)

Every ν_e is finitely supported and hence has all moments finite. But

    ∫x dν_e = 1 if e ∈ K, and 0 otherwise.                   (17)

A uniform endpoint-mean algorithm, given the uniformly generated valid moment, exponent, bound and exact-normalizer names, would decide K by accuracy less than 1/3. This is impossible. ∎

This is a uniform-operation obstruction. Each fixed ν_e and each of its moments is individually computable, without a uniform way to choose the needed numerical information from e. E4 does not assert a single finite-support law has a noncomputable moment. Nor does the known endpoint mean upper bound 1 make its actual value computable uniformly.

The two controls have different jobs: E3 gives one computable input with a noncomputable normalizer/law; E4 preserves the stronger finite-moment endpoint promise and supplies normalization, but defeats uniform recovery of the original mean output.

### An endpoint can re-enter the inherited continuation obstruction

There is also a direct bridge to the original scientific obligation of preserving actual continuations. Reuse the inherited lognormal pair ν_+,ν_− from `measure-moment-continuation-boundary-20261009/RESULT.md`, §§4–6: their densities are the standard lognormal density times 1±(1/2)sin(2πlog x). They are distinct, have the common full moment record exp(r²/2), and their later positive-tilt mean responses disagree somewhere in every nonempty positive interval. These are inherited ordinary facts, not a new countermodel or new determinacy theorem.

These two laws are computable. Under x = exp(y), integration is against the computable standard-normal density with the bounded computable factor 1±(1/2)sin(2πy). For a bounded computable test of bound K, truncation to [−R,R], R≥1, has tail error at most

    (3K/2) · 2 exp(−R²/2)/(R√(2π)).

On the compact interval, the integrand has effective approximation and uniform-continuity data, so certified quadrature computes its integral. This gives the needed effective measure statement; it is not imported from moment determinacy alone.

Fix a computable a > 0 and put

    D_± = ∫exp(−ax)dν_± > 0,
    μ_± = exp(−ax)ν_±/D_±.

The bounded computable integrands exp(−ax) and x^r exp(−ax), the latter bounded by r!a^−r, compute D_± and all the original μ_± moments uniformly in r by the same Gaussian truncation argument. Positive D_± have computable reciprocals, so one can supply a common rational M > max(1/D_+,1/D_−). Thus both initial laws satisfy the effective input contract, since ∫exp(ax)dμ_± = 1/D_± ≤ M. Their initial full moment records must differ by the inherited positive-exponential determinacy theorem.

At u = −a their normalized laws are ν_± and their full endpoint records coincide. Every endpoint moment is finite and even uniformly computable from exp(r²/2). Nevertheless, for every v > 0 their full later moment records differ: positive tilting makes both laws exponentially integrable and hence moment-determinate, while the tilt remains injective on its image. Their later mean responses have the inherited interval-separation property. Thus replacing the state at this endpoint by its raw moment record alone can lose actual-update congruence, even when computing that record itself causes no difficulty.

This does not defeat E2 or computation from retained initial data. Keeping the distinct initial certified records and the control history computes the later parameter u = v−a > −a directly by E2. It is forgetting that information and retaining only the coincident endpoint moment record that creates the continuation ambiguity. This corollary is a participating root deduction from the inherited pair and the present input boundary, not an independently rediscovered or field-new probability theorem.

## 7. Precisely sufficient additional endpoint information

### 7.1 Exact endpoint normalization computes the weak endpoint law

Under the original input contract, supplying a name of the exact real Z_a := ∫exp(ax)dμ is sufficient to compute T_(−a)μ as an ordinary weak probability measure. Conversely, a name of that endpoint probability measure computes Z_a. This equivalence is about this fixed reweighting operation, not arbitrary total-variation recovery, indexed hidden labels, or unbounded outputs.

Here is a direct construction of the sufficient direction. The interior theorem computes every Z(n), n ≥ 0. Push μ forward by y = exp(−x) and regard the resulting η as a probability on [0,1] with zero mass at zero. Its polynomial moments are

    ∫y^n dη = Z(n),

uniformly computable. From these moments one computes the integral of any computable continuous function on [0,1] with its effective uniform approximation data: approximate it uniformly by a computable rational polynomial, and integrate the finitely many coefficients against the known moments. For example, Bernstein polynomials supply an effective approximation from a supplied modulus of continuity and bound. For a K-Lipschitz function f, their error is at most K/(2√N), because E|Binomial(N,y)/N−y| ≤ 1/(2√N). Rational coefficient approximation adds its own explicit budget.

Consequently the original moment input computes the integral of every computable continuous compactly supported function of x with a supplied or effectively known support bound and effective local approximation data. After replacing x by −log y, such a function extends by zero to a computable continuous function at y = 0, with an effective modulus from that support bound and local data. All compactly supported functions used below have an explicit cutoff support. For the original measure itself, the tail estimate μ((R,∞)) ≤ M exp(−aR) then extends this computation from compactly supported tests to bounded computable Lipschitz tests: multiply by a cutoff equal to one through R and budget at most K M exp(−aR) for a test bounded by K. Thus the original law is computable from the stated moment-only inputs; it has not been silently added as an extra input.

For integers R ≥ 1 take the monotone continuous cutoffs

    χ_R(x) = 1 for x ≤ R,
             R+1−x for R ≤ x ≤ R+1,
             0 for x ≥ R+1.

The numbers s_R = ∫exp(ax)χ_R(x)dμ are computable by the preceding compact-support procedure, increase to Z_a, and obey 0 ≤ s_R ≤ Z_a. Given Z_a as a computable real, search for R with the certified strict inequality Z_a−s_R < ε. Monotone convergence guarantees termination. For a bounded computable continuous test f with supplied bound K and effective local data, compute its cutoff weighted integral and use

    |∫f exp(ax)dμ − ∫f exp(ax)χ_R dμ| ≤ K(Z_a−s_R).          (18)

Division by Z_a ≥ 1 computes the endpoint test integral. In particular this computes the standard bounded-Lipschitz test representation of the probability measure. It is the usual weak measure representation, not a promise of computable integrals for unbounded tests.

Conversely, if ν = T_(−a)μ is supplied as a computable probability measure, then the bounded computable Lipschitz function exp(−ax) has

    ∫exp(−ax)dν = 1/Z_a > 0.

Computing its integral and taking the reciprocal computes Z_a. E3 therefore pinpoints the missing normalization information at the law level. E4 shows why this is not enough for the raw mean or higher moments.

### 7.2 Effective weighted-moment tails compute the endpoint moments

For each r ≥ 0, monotone convergence gives, allowing +∞,

    A_r(−a) = ∫x^r exp(ax)dμ
            = Σ_(n=0)^∞ a^n m_(r+n)(μ)/n!.                 (19)

A sufficient additional input for the uniform full endpoint-moment record is a computable modulus τ(r,k) with

    Σ_(n>τ(r,k)) a^n m_(r+n)(μ)/n! ≤ 2^−k.                 (20)

It supplies finiteness and effective convergence of each nonnegative weighted series. Evaluate its finite partial sum with an independently budgeted numerical error, obtain A_r(−a), and divide by A_0(−a) ≥ 1. If exact Z_a is already supplied, (20) is needed only for the requested positive grades.

This is not an arbitrary strengthening: relative to the original moment names, a uniform name for the finite values A_r(−a) conversely computes such a modulus. Search for a partial sum whose difference from the known total is strictly smaller than the target bound; nonnegative-series convergence guarantees termination. Equivalently, supplied effective spatial tails ∫_(x>R(r,k)) x^r exp(ax)dμ ≤ 2^−k suffice, using continuous cutoffs supported just beyond R and the compact-support computation above.

For only one requested endpoint grade, only the corresponding weighted-integrability information and normalization are required. Another simple sufficient input for every grade is a computable δ > 0 and H with

    ∫exp((a+δ)x)dμ ≤ H.

Then u = −a is strictly interior relative to the stronger exponent a+δ, and E2 applies. Neither classical finiteness of all the endpoint moments nor one upper bound for the endpoint normalizer supplies these effective higher weighted tails; E4 verifies the failure on valid finite-support instances.

## 8. Sources, checks, and claim ceiling

The proofs above are ordinary mathematical proofs. The finite-control script passed 4,560 exact checks of factorial/geometric identities, rational bound selection, quotient error arithmetic, exact finite-model normalized-tilt composition, Cantor coding, and finite versions of the positive-series/halting-weight bounds. A separate composed-oracle control starts with the exact moments r! of Exp(1), the bound a = 5/6, M = 6, and takes two normalized h = 2/3 steps to u = 4/3, beyond the actual origin Taylor radius 1. It computes intermediate moments through recursive approximate moment oracles using rational error budgets, then verifies grades 1 and 2 against 3/7 and 18/49. It supplies a small concrete composition check, not a universal implementation or performance claim. Neither script can decide the halting set, prove an infinite noncomputability statement by examples, or replace the universal series and termination proofs. No formal-kernel claim is made.

The noncompact and capped-tensor ancestor files are copied and hashed in `inputs/` and bound in `SOURCE_LEDGER.json`; their existing result bytes are unchanged. The endpoint controls were developed with a participating mathematical checker; any separate independent review is identified separately rather than relabeling that participation as independent discovery.

For the standard computable-measure representation and bounded integration ancestry, the directly inspected primary source is Mathieu Hoyrup and Cristóbal Rojas, *Computability of probability measures and Martin-Löf randomness over metric spaces*, §4, especially the integration characterizations in §4.3: https://members.loria.fr/MHoyrup/random_metric.pdf . The specific cutoff and moment algorithms needed here are given explicitly above. The ordinary exponential-moment determinacy and compactification ancestry is retained in the cited project ancestor, including its source ledger; no claim of exhaustive literature search or field-level novelty is made.

The result does not close T20, assert source ownership, extend the finite theorem to unspecified outputs or controls, prescribe a sampling budget, or conflate weak computability with an indexed-law inverse. It establishes the effective interior continuation of this exact unbounded moment interface and the exact reasons its endpoint needs additional information.
