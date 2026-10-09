# Independent final mathematical review

Date: 2026-10-08 UTC.

Status: PASS, scoped to the twelve final author payloads identified by SHA-256 in `REVIEW_RECEIPT.json`. Both theorem files, all-rate and asymptotic additions, controls, source audit, and bindings have been inspected. Later packaging files are outside this exact-byte receipt unless separately checked.

## Independence and inspection scope

This reviewer did not contribute to the author proof or its asymptotic extension. The assigned task was to review the author packet independently, write only in this new sibling, and preserve all author and predecessor bytes. The review directly inspected the complete initial and final `RESULT.md` and `ASYMPTOTIC_DESIGN.md`, plus the complete frozen `RESULT.md` files from `finite-replay-sampling-lower-bound` and `finite-panel-replay-robustness` for ancestry and instrument scope. It subsequently inspected all twelve final author payloads, reran both author entrypoints, and independently checked the resulting outputs against the retained author outputs. It did not re-review all predecessor packets or certify their independent reviews. Initial hashes are retained in `INITIAL_BINDINGS.json`.

The review also opened the CRAN copula package's Sibuya documentation at https://search.r-project.org/CRAN/refmans/copula/html/Sibuya.html on 2026-10-08. The inspected probability-mass formula and Laplace transform support the author's attribution; the proof below does not depend on a borrowed moment assumption. No whole-book, whole-literature, physical, empirical, or novelty-exhaustiveness audit was performed.

## Finding

No blocking mathematical defect was found in the two reviewed theorem files, including the subsequently added global Joe-oriented KL theorem. The all-rate chi-squared bound, finite-prefix adaptive lower bound, both global supremum limits, and stated near-optimality characterization are valid under the declared atomic two-face observation contract and for the exact bytes in the receipt. Their exclusions are necessary and are stated clearly. The imported robust upper test matches the exponent within the enlarged instrument because its original fixed-rate design remains allowed, not because the new optimal hard-pair rate has acquired a broad wrong-count certificate.

## 1. Exact law and support

Write `m=n+1`, `c=n/m`, `x=1-a`, `y=1-b`, and `z=x+y-xy=1-ab`. The per-route probability that both face bits are absent is

    S = x^c + y^c - z^c.

Mutual route independence gives joint absence `S^m`, with margins `A=x^n` and `B=y^n`. Independent coordinate thresholds in the reference give joint absence `AB`. Thus all four cells in equation (4), including the signs of the two off-diagonal perturbations, are correct. Summing reciprocal reference cells yields exactly

    sum(1/P0_cell) = 1/[A(1-A)B(1-B)].

This was also checked symbolically with independent code. The variance/covariance interpretation is only about the two aggregate absence indicators and introduces no additional latent assumption.

There is an independent construction that confirms positivity without needing to quote a threshold density. Given the Sibuya integer `K`, take two independent maxima of `K` independent uniforms. Their joint success at `(a,b)` is `(ab)^K`; after mixing, it is `H_c(ab)`. At interior rates every conditional one-route cell is strictly positive. Aggregating a finite positive number of independent routes consequently preserves positivity of the four aggregate pair cells. This construction has the same command-space threshold law used by the theorem.

For a literal endpoint rate, one bit is deterministic and the other has the same marginal in both worlds. Both divergences are therefore exactly zero. The standard absolute-continuity convention is respected: common zero cells contribute zero, and the interior quotient is not evaluated at a zero denominator. For `x=y` decreasing to zero,

    S / x^c -> 2-2^c,
    Delta / x^n -> (2-2^c)^m,
    chi^2 -> (2-2^c)^(2m).

The strictly positive limit does not contradict equality at the literal boundary. It disproves any argument silently using boundary continuity. The stated convention is correct and essential.

## 2. Central-region bound

The four arguments `xy`, `x`, `y`, and `z` are the corners of an additive rectangle with side lengths `xb` and `ya`. The mixed second difference of `t^c` therefore gives the exact positive integral in equation (6). Since `c-2<0`, replacing its integrand by the value at `xy` gives precisely `c(1-c)ab(xy)^(c-1)`.

When `a,b<=1/2`, the ratio `ab/(xy)` is at most one. Hence `h<=c/m<=1/m`, and

    (1+h)^m-1 <= mh exp(mh) <= e c ab/(xy).

Multiplying by `(xy)^n` gives the stated bound `Delta<=4e ab AB`. The transformations `u=-n log x`, `v=-n log y`, and inequalities `a<=u/n`, `b<=v/n` then yield equation (8), with the constant `16e^2` and the factors `f(u)f(v)` in the correct locations. The exponential-series bound `exp(u)-1>=u^2/2` gives `f<=2`, so the central uniform constant `64e^2` is valid. Crucially, the sharper product envelope is retained for asymptotics.

## 3. Bounded Sibuya mixture and tails

For `0<c<1`, all coefficients `p_k=(-1)^(k+1) binom(c,k)` are strictly positive. Monotone convergence of their power series at one gives total mass one. The proof uses only `F=1-a^K` and `G=1-b^K`, both in `[0,1]`; all their expectations, products, variances and covariance exist. It never assumes that `K` has a finite first or second moment. In fact `E[K]=infinity` follows from the derivative `c(1-z)^(c-1)` as `z` increases to one, so an argument replacing bounded-transform moments by moments of `K` would fail.

Direct expansion gives

    E F=X, E G=Y, E(FG)=S,
    Var(F)=X[2-(1+a)^c-(1-a)^c].

The chord bound for `(1+a)^c`, the inequality `(1-a)^c>=1-a`, and `2-2^c<=2(1-c)` yield `Var(F)<=2(1-c)Xa`. The analogous bound for `G`, followed by Cauchy-Schwarz, gives equation (10). Using `Delta<=m g S^n` and `m(1-c)=1`, division by the aggregate variances cancels the powers exactly to give

    rho <= 2 sqrt(ab/[(1-A)(1-B)]) (S/sqrt(XY))^n.

Since `1-(1-a)^n>=a`, discarding the leading square-root factor is valid uniformly, including asymmetric approaches to zero. No hidden lower bound on a rate is needed.

For the comparison, put `r=1/c`, `alpha=r/2`, `U=X^2`, and `V=Y^2`. Concavity gives

    U^alpha + V^alpha - (UV)^alpha >= (U+V-UV)^alpha.

Taking the increasing `1/r` power yields the required lower bound on `(X^r+Y^r-X^rY^r)^(1/r)`, and hence the required upper bound on `S`. The direction is correct. Rationalization gives

    [X+Y-sqrt(X^2+Y^2-X^2Y^2)]/sqrt(XY)
      <= (2+XY)/(2+sqrt(2-XY)).

If one rate exceeds one half, `XY<3/4`; using numerator at most `11/4` and denominator at least `3` proves the uniform contraction `11/12`. The resulting `4(11/12)^(2n)` bound covers all interior tail and asymmetric regimes. It is not a compactness assumption disguised as a tail argument.

Finally, `log(12/11)>=1/12` and maximization of `z^4 exp(-z/6)` at `z=24` give `4(24/e)^4<=26244<32768`. The central constant is also smaller. Thus the announced all-rate constant is valid for every integer `n>=1`. The elementary inequality `log t<=t-1` proves the KL upper bound in the advertised orientation.

## 4. Global asymptotics and design

The rectangle substitution in (A1) has the correct factors: `xb/(xy)=b/y` and `ya/(xy)=a/x`. Uniformly on a fixed compact positive `(u,v)` box, `na->u`, `nb->v`, `I_n->1`, and `n^2 m h->uv`. The elementary inequalities

    mh <= (1+h)^m-1 <= exp(mh)-1

make the remainder `O((mh)^2)` uniform. Consequently `n^2 Delta->uv exp(-u-v)`. On such a box all reference cells have a positive common lower bound, proving compact-uniform convergence to `f(u)f(v)`. The Taylor expansion of KL is uniformly justified by the same cell floor and `Delta=O(n^-2)`: summing the four expansions cancels the linear terms, leaves one half of chi-squared, and bounds the cubic remainder by `O(n^-6)` uniformly. Thus scaled KL converges uniformly on the box to `f(u)f(v)/2`.

The passage to both global suprema is valid. Both endpoint limits of `f` are zero, and `f` is bounded. Thus the central product envelope forces scaled chi-squared below any prescribed positive tolerance outside a sufficiently large compact box bounded away from zero, including when only one coordinate escapes. The separate tail contraction tends to zero uniformly after multiplication by `n^4`. Nonnegativity and `KL<=chi-squared` provide the same escape envelope for Joe-oriented KL. Compact-uniform convergence then controls the remaining box, separately with the appropriate limit for each divergence. A fixed interior design gives each matching lower limit. This is a genuine tightness/escape argument, not an illicit exchange of supremum with pointwise convergence or a global inference from a local KL expansion alone.

The derivative has the sign of `G(u)=2(1-exp(-u))-u`. Its derivative changes sign once and `G` has precisely one positive root; therefore the scalar maximizer is unique. The supplied numerical characterization is correct:

    u* = 1.5936242600400400923...,
    f(u*)^2 = 0.4193990202224225571...,
    f(u*)^2/2 = 0.2096995101112112785...,
    f(1/3)^2 = 0.0788814953469059027...,
    ratio = 5.3168239063... .

The same escape control places every asymptotically optimal sequence in a fixed compact set eventually. Every convergent subsequence must maximize `f(u)f(v)` (or its positive half) and hence converge to `(u*,u*)`; this proves the stated convergence of the whole sequence. This assertion concerns chi-squared and Joe-oriented KL optimality for this hard pair. No finite-`n` global optimizer, reverse-KL optimum, sharp sequential sample constant, broad wrong-count certificate at the new rate, or improvement factor for the old upper test follows.

## 5. Adaptive policies, stopping, and terminal correctness

The proof correctly treats a replay pair as one atomic observation returning both bits, with both commands chosen before either outcome is seen. A common conditional policy kernel contributes zero relative entropy even when its rates depend on all completed observations and common randomness. Fresh independent endpoint observations have identical conditional laws under both worlds and contribute zero. Equal unconditional fresh laws would not suffice if the latent vector could be retained or selected using earlier data; the author explicitly excludes that case.

At each finite prefix, the conditional KL of a pair is at most the all-rate constant. There is no need for a cell-probability lower bound uniform over all command rates. Interior absolute continuity, common deterministic boundary laws, bounded conditional KL, and the bound on the negative part of `p log(p/q)` provide integrability. Summing the finite-prefix contributions proves equation (14), with expected cost correctly taken under world 1.

For `E_T={stop by T and reject}`, binary data processing applies to each finite prefix. These events increase to actual finite-time rejection. Monotone convergence handles pair cost and lower semicontinuity handles binary KL at any limiting boundary. The unconditional correctness conditions imply `P1(E)>=1-alpha` and `P0(E)<=alpha`. For `alpha<1/2`, monotonicity of binary KL in this separated region gives the stated lower bound. Infinite expected cost is harmless.

The nontermination condition is necessary: mix a valid accurate finite experiment with probability `epsilon` and immediate endless nontermination otherwise. Conditional-on-termination accuracy stays unchanged while unconditional expected informative cost is multiplied by `epsilon`. Thus conditional accuracy alone cannot imply the proposed lower bound. Likewise `alpha>=1/2` admits a no-data fair decision. Neither failure mode is silently allowed.

The independent control script enumerates a randomized three-slot policy whose subsequent pair rates depend on earlier outcomes, with boundary actions and fresh endpoints included. Direct transcript KL agrees with the expected sum of conditional KL values; binary data processing and the cost inequality also hold. This is a finite example validating the bookkeeping, not a numerical proof for arbitrary measurable policies.

## 6. Matching upper theorem and scope

The frozen robust theorem uses `N` fixed-rate replay pairs and `N` fresh diagonal probes with `N>=ceil[200000000(n+1)^4 log(8/alpha)]`. The present Joe world has a fixed finite count, shared coordinate marginal calibration, route independence, fixed threshold laws, and the requisite consistent fresh/replay probabilities, so it belongs to that theorem's alternative class. The old fixed-rate design is available in the enlarged all-rate instrument. Therefore the lower and imported upper orders agree in the fourth power of count; for `0<alpha<=1/4`, their error logarithms have the same order.

The comparison does not assert that every same-count model is accepted, that all alternative expected costs have the lower bound, or that the two constants are close. The old upper theorem is imported with its own review requirement. This independent review does not replace that review.

Selecting the second rate after seeing the first outcome changes the action channel. Longer words, retained vectors across replicas, gate-level data and different instruments also change it. No bound for these enlarged channels has been proved here. The text expressly excludes them, along with physical realizability, psychological intervention, calibration availability and universal independence certification.

## 7. Independent controls and retained failures

`independent_controls.py` is original reviewer control code, not an invocation or copy of the author's tests. It uses 150-digit arithmetic, exact rational Sibuya coefficients, and a symbolic cell identity. Its current run reports 43 passed checks and no failed theorem check. The 700-point interior grid includes severe asymmetry, rates on both sides of one half, and rates within `1e-30` of boundaries. Literal endpoints and high-rate interior limits are checked separately. All intermediate comparison and covariance envelopes are checked as well.

The test output intentionally retains invalid numerical methods:

- Naive binary64 subtraction at `n=10^6` gives scaled chi-squared about `3.1096`, versus the high-precision value about `0.4193982`.
- At `n=10^8` it gives about `6.08e14`, versus about `0.4193990`.
- Extending the interior boundary limit continuously would assign about `0.117749` at the `n=1` top corner, whereas the literal pair law has divergence zero.

These are explicit negative controls, not discarded theorem failures. Finite checks do not certify a continuous supremum. Analytic arguments in this review and the author text provide that certificate. `CONTROL_RESULTS.json` preserves the full results and the unsuccessful methods.

## 8. Author control correction and provenance verification

The initial author Sibuya numerical controls compared `approx<=1-hl` and `1-hu<=series_upper`. Those inequalities certify that two rational intervals overlap, which is weaker than showing the algebraic-transform interval is contained in the series-tail interval. The reviewer reported this as a nonblocking control-strength issue; the positive-series theorem itself was already proved correctly.

The author adopted the correction before freeze: 400 exact root bisections and the stronger checks `approx<=1-hu` and `1-hl<=series_upper`. The reviewer inspected the changed code and reran the entire suite successfully. The correction is explicitly retained in the author's exact-control notes and research event record. `AUTHOR_CONTROLS_RERUN.json` preserves the pre-correction run; `AUTHOR_CONTROLS_STRENGTHENED_RERUN.json` preserves the final run. No earlier weak check is being silently represented as a stronger one.

The final author run passed 180 rational/algebraic pair cases, 12 fully contained Sibuya generating-function intervals, 48 literal boundary cases, 12 exact four-cell identities, 1,750 paired high-precision stable evaluations, and the reported local chi-squared/KL displays. Its output matches the final author `CONTROLS_OUTPUT.json` byte for byte. These controls supplement rather than replace the universal analytic proof.

The reviewer inspected and ran `source_binding_check.py`; all 31 declared input/manifest payload hash checks passed. The output matches final `SOURCE_CHECK_OUTPUT.json` byte for byte. This verifies provenance bytes, not independent rereading of every source payload. The two ancestry `RESULT.md` hashes match those recorded before review. The bounded source audit is candid about the full-paper retrieval failures and contribution roles. Its global novelty disclaimer is appropriate.

## Final receipt and exclusions

`REVIEW_RECEIPT.json` binds the twelve author payloads frozen for review, the review artifacts, and the two directly read ancestor theorem files. `verify_review.py` provides a read-only repeatable check of those exact bindings. The review's receipt and later author packaging files cannot be mutually self-hashed; the author may bind this receipt from later packaging without changing any reviewed payload.

PASS does not cover any changed payload, a proof-contributing worker as its own final reviewer, second-rate selection after the first outcome, longer retained words, reverse-KL optimization, a sharp sample constant, physical validation, protected integration, or T20 closure. Those exclusions survive receipt and packaging.
