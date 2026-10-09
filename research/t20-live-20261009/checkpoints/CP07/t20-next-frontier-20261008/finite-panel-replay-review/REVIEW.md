# Independent adversarial review: finite replay panel

8 October 2026 UTC. Mathematical scratch review only.

**PASS for the stated conditional mathematical certificate.** No incorrect inequality direction, missing positivity condition, unbounded-count gap, or counterexample within the declared model class was found. This is not T20 closure, protected integration, empirical validation, a finite-sample guarantee, or a claim about elapsed research time.

Reviewed `finite-panel-replay/RESULT.md`, `VERIFICATION.md`, and the frozen `dependent-gate-transport/RESULT.md` for scope. The reviewed final `RESULT.md` has SHA256:

    327b6fb25944ac90e7ecd6010a427993b69400fbdc9b79928d731120b6d62243

Also independently checked the subsequently recorded `finite-panel-replay/SHARED_MARGINAL_BOUNDARY.md`, with SHA256:

    3d55f739d398ed1b4b28253cdb5db34ec9b32d46415e14750a612e35f43b4788

**PASS for that separate boundary counterexample as well.**

## 1. Count proof and all signs

- The face reductions are correct: endpoint saturation, mutual route independence, and one common A marginal and one common B marginal imply both marginals at the tested level equal `u=1-(1-t)^(n/m)`. Without common marginals, the faces fix only products.
- Valid tables imply `0<=x_j<=u`, `y_j=1-x_j>=0`, `z_j=1-2u+x_j>=0`, and `y_j+z_j=2p`. The unused constraint `x_j<=u` causes no problem: relaxing constraints can only strengthen an impossibility proof.
- Generalized Holder gives the displayed upper bound on the sum of geometric means. For `m<n`, strict convexity at the two distinct positive arguments `1-t^2` and `(1-t)^2`, whose mean is `1-t`, gives the strictly incompatible lower bound. This includes `m=1`; zero routes already fail either face.
- For `m>n`, `c<=n/(n+1)`, `u<=t<=1/6`, and consequently `2/3<=s=1-2u<=1`. Thus product expansion, division by `s`, and replacement of `w/s` by `w` have their asserted directions. The union/product bound uses valid `x_j` in `[0,1]`.
- `s=p^2-u^2` and `r=p^(2m)` give the exact ratio factorization. Concavity at `h=(1-t)^(-1)` yields `d<=ct/(1-t)`. Integer Bernoulli applies to `d^2` in `[0,1)`, giving `(1-d^2)^m>=1-md^2>=1-A>0`.
- The bound `w>=W=nt^2/(1+nt^2)` follows by taking reciprocals of positive quantities in `(1-t^2)^(-n)>=1+nt^2`. Both lower factors multiplied subsequently are positive.
- The integer separation from `c=1`, rather than an upper bound on `m`, supplies the strict gap. Every inequality applies to every positive integer `m>n`, with no limit exchange or omitted large-count regime.

## 2. Exact gap and n=1

For the uniform version use

    A_* = n^2 / [(n+1)(3n+2)^2],
    W = n / [9(n+1)^2+n].

Then direct common-denominator subtraction gives

    (1-A_*)(1+W)-1
      = n(n^2+7n+4)
        / [(n+1)(9(n+1)^2+n)(3n+2)^2].

This is exactly the displayed `delta_n`; the numerator and denominator are positive. Likewise the displayed sufficient-condition difference has numerator `n^2+7n+4` over `9(n+1)^3`. These cancellations were also independently checked symbolically, without using selected integer cases as proof.

At `n=1`, `t=1/6`, `A_*=1/50`, `W=1/37`, and `delta_1=6/925>0`. No smaller positive count exists, all larger counts are excluded, and the diagonal probability directly determines `x_1=t^2`.

## 3. Equality and remaining dependence

For `m=n`, the two positive target products ensure every `y_j,z_j` is positive. Holder equality for `n>=2` requires identical ratios `y_j/z_j`; the common sums force identical entries. The product then fixes `x_j=t^2`. Along with both marginals `t`, this identifies the full independent Bernoulli table at this single level. It does not establish independence at other levels.

The proposed copula perturbation is valid. The polynomial vanishes at both endpoints, so integrating its strictly positive mixed density gives uniform margins and nonnegative rectangle masses. Since `t<=1/6`, the stated derivative bound and `epsilon=1/100` suffice. The perturbation is nonzero away from its finite zero set but vanishes on the tested row and column. Independent route copies therefore preserve all four observations while violating global product-copula independence. The finite-grid extension follows by the same bounded-derivative argument.

## 4. Shared marginals are genuinely necessary

There is an exact alias if route-specific marginal calibrations are allowed, even when each calibration is an endpoint-preserving homeomorphism and each route uses fixed thresholds. Replace each reference route by two mutually independent routes with the following tables at any `0<t<1`:

    Route I:   A and B marginals t^2; joint success x_I=t^2.
    Route II:  A and B marginals t/(1+t); joint success x_II=0.

Both tables are valid. Their combined face absence is

    (1-t^2)/(1+t)=1-t;

their diagonal absence is `1-t^2`; and their replay absence is

    (1-t^2)(1-t)/(1+t)=(1-t)^2.

Repeating this construction independently `n` times produces `m=2n` with all four exact target probabilities. A full fixed-threshold realization uses the comonotone copula for Route I with marginal map `h_I(a)=a^2`, and the countermonotone copula for Route II with a strictly increasing piecewise-linear marginal map through `(0,0)`, `(t,t/(1+t))`, `(1,1)`. This is outside the theorem precisely because the two route types have different marginal maps.

The recorded boundary addendum instead uses the piecewise-linear `g_(t,w)` for both route types. This is equally valid: its slopes `w/t` and `(1-w)/(1-t)` are strictly positive, its pieces agree at `t`, and its endpoint values are zero and one. Its explicit `U/U` and `V/(1-V)` gate constructions give exactly the stated tables and preserve each realization during replay. Drawing the uniforms independently makes all `2n` route pairs mutually independent. The addendum's scope and non-global qualification are correct.

## 5. Residual claims and semantic boundary

The certificate is operational at known/selectable true reference rate `t`, or existential in latent true-rate coordinates when nominal calibrations are unknown. It supplies neither known nominal commands depending only on `n` nor a finite calibration-discovery algorithm.

The same per-route Bernoulli-pair law must underlie the fresh diagonal measurement and the same-gate replay measurement. This is what justifies using one `x_j` for both `y_j` and `z_j`; preserving an inventory or only preserving marginal laws is insufficient. Mutual independence of the route pairs, rather than pairwise independence alone, is also essential to the products.

The positive gap is conditional on exact equality of the other three probabilities. No noisy-data robustness, physically admissible intervention, all-command independence, minimal panel, unknown-inventory identification outside this model class, or broader closure follows. The author's explicit qualifications appropriately preserve these boundaries.

No author or predecessor file was edited.
