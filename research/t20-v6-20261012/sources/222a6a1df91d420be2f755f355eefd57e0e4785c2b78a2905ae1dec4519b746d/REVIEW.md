# Independent computational review

10 October 2026 UTC. Reviewer: `private-locator:a2a75ddc6fa80f873675`.

**Disposition: PASS within the stated scope and the explicitly trusted mpmath interval-arithmetic boundary. No author correction required.**

This review independently checks the computational follow-on's integral/product bounds, code, exact quadratic algebra, computability argument, and terminating-search proof. It does not claim independent discovery of the supplied polynomial. The author and participating root proposed it; the reviewer independently verified its mathematics and execution. The preceding main theorem and its classical moment-theoretic dependencies are separately reviewed work, not newly established by this computational receipt.

## 1. Bound source bytes

Paths are relative to `private-locator:8f24556a330b05a11a95`.

- `computable-positive-hierarchy-20261010/RESULT.md`
  - SHA-256: `862a4b005351c1f980e1daf2820d8d871fa16835d53029ce27941244d248915f`
- `computable-positive-hierarchy-20261010/certify_degree_one.py`
  - SHA-256: `db299eb62c90782270a7bbf4f1fe012de7b00e7bb3822a7ea052495f4a3e1e1f`
- `computable-positive-hierarchy-20261010/certify_degree_one.log`
  - SHA-256: `9165accacc66176a92dbcd17dd53dbfdcdba8c756acd470a3b10fe1c4a561f89`
- `computable-positive-hierarchy-20261010/explore_candidate.py`
  - SHA-256: `a7729014539d5b20caa10b98f1c75719da438b2ca4b75caeec3165dca4cb87fb`

The author confirmed these final bytes. The source script and log also matched the reviewer's first-run bindings. Inherited inputs are the frozen `determinate-initial-positivity-20261010/RESULT.md` (SHA-256 `cafc520026c66f94442346ff308ed4e202d70e10be8963b8a24ad17bda4e1e0a`) and its `DIAGNOSTIC.md` (SHA-256 `5d0e97c5f4e50ac7981765292b6aa161076a4d0b6af7fbc46aa18e40bd89c2b2`). Full bindings, preservation checks, and final rerun results are in `FINAL_VERIFICATION.json`. All reviewer writes are confined to this separate review directory.

## 2. Analytic bounds and certificate implementation

### Infinite product: pass

For `q = exp(-1)` and `P_n = product_(j=1)^n (1-q^j)`, the tail product lies between `1-sum_(j>n)q^j` and 1. Because `0 < P_n <= 1`, this implies

`P_n - q^(n+1)/(1-q) <= w <= P_n`.

The author's 40-factor code forms the lower endpoint from the outward lower endpoint of `P_40-error`, and the upper endpoint from the outward upper endpoint of `P_40`. This is an enclosing interval; it does not treat a truncated product as exact. The main theorem's identification of this product with the Krein atom is an inherited dependency, not a claim established by the numerical product computation.

### Gaussian tails: pass

Completing the square gives

`exp(rz) phi(z) = exp(r²/2) phi(z-r)`.

For nonnegative t, dropping the damping increases the integrand. The two tails beyond [-M,M] therefore have the bound stated in RESULT.md. The Mills estimate follows by bounding 1 by `v/u` for v >= u > 0 and integrating `v exp(-v²/2)` exactly.

For the fixed polynomial, `(1-c exp(z))² <= 2(1+c² exp(2z))`, with c = 17/50. The code uses shifts 0 and 2, multiplies their two Gaussian tails by the correct factors `2 c_k² exp((2k)²/2)`, and has positive Mills denominators because M = 10 > 2. The tail is nonnegative, so adding `[0, tail_upper]` is valid for both ends of the total integral enclosure.

### Compact rectangles and sign: pass

Every cell is supplied to interval arithmetic as its full closed z-range. The interval exponential, multiplication, square, and division enclose all values of the integrand on that cell, conditional on their stated arithmetic guarantee. Multiplying by the cell width and summing encloses the integral. This is range integration rather than sampled quadrature. Integer inputs and interval divisions enclose the intended rational time and coefficients; no binary Python float is substituted for 1/10 or 17/50. Internal endpoint extraction uses the tested mpmath 1.3.0 representation.

The positive safe margin `1-w-2t exp(1/2)` certifies `t<T_0` and hence D(t)>0 by the analytic lower bound. Subtracting the interval for w encloses the quadratic numerator. Strict interval comparison with zero requires the entire objective interval to be negative, so a successful assertion cannot be based only on a midpoint or lower endpoint.

## 3. Independent executions and exact algebra

The environment used Python 3.12.14, mpmath 1.3.0, and SymPy 1.14.0. Three successful controls were executed independently of the author's saved log:

1. **Unmodified author script:** 50 digits, 4,096 cells on [-10,10], 40 product factors. Exit 0, empty stderr, stdout byte-identical to the frozen author log. The numerator upper endpoint is `-0.032572829660069709...`, which is strictly below -0.0325.
2. **Fine-grid replay:** the reviewer copy changes only precision to 80 digits and cell count to 8,192. Exit 0, empty stderr. Its upper endpoint is `-0.033956476015534169...`.
3. **Separately derived moment/quadratic control:** `check_moment_quadratic.py` independently integrates B_0, B_1, and B_2 with 32,768 cells on [-12,12], 70 digits, and 64 product factors. It uses each moment's individual shifted-Gaussian tail rather than the author's polynomial-square integrand or tail bound. It obtains the outward-rounded enclosure

   `[-0.036840828, -0.033828486]`

   for `B_0 - (17/25)B_1 + (289/2500)B_2 - w`, and independently verifies a positive denominator. Its exact upper endpoint is `-0.033828486900504539...`, also below -0.0325.

The last script separately expands the rational square, checks its coefficient vector `(1,-17/25,289/2500)`, checks the corresponding 2-by-2 Hankel quadratic form, and verifies that the integer vector `(50,-17)` scales the rational-vector numerator by 2,500. These finite algebra checks supplement the elementary identities, rather than serving as a proof-kernel claim.

The independent momentwise method initially used 16,384 cells. It certified negativity, but its upper endpoint `-0.032321734524...` did not meet the reviewer-added stronger -0.0325 target. Diagnostic output identified enclosure width as the limitation. Doubling only the cell count supplied the final passing bound; no author code or theorem was changed. The failed stronger-threshold run, its exact script, and diagnostic replay are retained under names containing `initial_grid`, `initial_failure`, or `diagnose`. They are not counted as successful final controls.

## 4. Uniform computability: pass

The Gaussian tail bound is effective uniformly given integer r: increase M beyond r until its computable upper bound is below the requested error. On a chosen compact z interval, all elementary operations are computable and have a computable modulus. For instance, for `0 <= t <= b`, a coarse bound for the absolute z derivative is

`(r+b exp(M)+M) exp(rM)/sqrt(2 pi)`.

This gives an explicit compact quadrature error bound. Time names can be handled independently using

`|d B_r(t)/dt| <= E[X^(r+1)] = exp((r+1)²/2)`

for all nonnegative t, so their approximation error has a uniform computable bound as well. Approximating time from a nonnegative interval preserves the nonnegative-time tail estimate. These observations fill out the author’s uniform algorithm without assuming a fixed r, a noncomputable quadrature modulus, or a rate inferred from experiments.

The product tail computes w. Its known strict inequality w<1 lets refinement produce a positive rational lower bound for 1-w. The promised safe time domain supplies `D(t) > (1-w)/2`; division is therefore effective. This proves a uniform evaluation algorithm in grade, named safe nonnegative time, and requested precision. It does not implement generic sequence-space integration or recovery of the full Krein support.

## 5. Terminating finite-witness search: pass

This is a proved algorithm, not an executed implementation. The frozen diagnostic supplies existence of a finite negative unshifted Hankel direction at each positive safe time: shifted matrices remain positive, and nonexistence of a representing measure forces an unshifted failure by the Stieltjes existence criterion. These are explicit inherited mathematical dependencies.

For a fixed finite matrix, continuity takes a strictly negative real vector to a strictly negative rational vector; multiplying by a common denominator gives an integer vector. The exact identity `v^T H_N^0 v = Q_t(v)/D(t)` includes the corrected zeroth entry B_0-w and is valid because D(t)>0.

At each search stage there are finitely many vectors, and the uniformly computable moment bounds produce an enclosing interval of the requested width for each one. Thus the stage terminates even for vectors whose true form is zero. Any fixed integer witness is revisited at all sufficiently large stages. A valid enclosing interval whose width tends to zero eventually has a negative upper endpoint for that strictly negative value. This proves soundness and termination for each specified rational `0<t<T_0`. No bound on detecting degree or search time is asserted, and the divergence of the least detecting degree as t approaches zero is consistent with the claim.

## 6. Trust and replay boundaries

The [official mpmath interval documentation](https://mpmath.org/doc/current/contexts.html) describes containment semantics, warns that interval support is experimental, and explains three-valued comparisons. The inspected code uses supported elementary interval operations, but this review does not audit mpmath's implementation or replace its trust assumption with verified-kernel arithmetic. All numerical certification claims remain conditional on mpmath, Python, and the analytic enclosures above. The exploratory quadrature script was inspected for scope only and is not counted as certification evidence.

From the evidence root, the three final successful replay commands are:

    python computable-positive-hierarchy-20261010/certify_degree_one.py
    python computable-positive-hierarchy-review-20261010/certify_degree_one.fine_grid.py
    python computable-positive-hierarchy-review-20261010/check_moment_quadratic.py

Require exit 0 and empty stderr for all three; compare stdout with the corresponding frozen logs. Verify source and script hashes before and after execution. Diagnostic and initial-grid scripts are retained historical checks, not additional required passing commands. No network, generic search campaign, or alteration of earlier packets is required.

**Final scope:** the follow-on establishes uniform coordinate evaluation and a mathematically terminating witness search; it executes one fixed-time witness with independent interval cross-checks. It does not execute the general search, bound its complexity, certify a kernel proof, or revise the frozen main theorem or earlier classifications.
