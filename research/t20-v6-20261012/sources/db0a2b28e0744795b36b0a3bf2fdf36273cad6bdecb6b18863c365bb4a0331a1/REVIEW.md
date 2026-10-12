# Independent review: valid initial moments versus positive-time realizability

Date: 10 October 2026 UTC.
Reviewer: `private-locator:a2a75ddc6fa80f873675`.
Disposition: **PASS within the stated finite-horizon, indeterminate-initial-data scope. No correction required.**

This is an independent ordinary mathematical review of the existing counterexample, with a fresh execution of its exact algebraic controls. The reviewer did not author or modify the counterexample and did not rely on the root's earlier checking as evidence. This receipt does not alter the author result, the parent classification, or their ownership. It is not a formal-kernel certificate, canonical integration, exhaustive literature review, or extension to determinate initial data.

## 1. Exact inputs and preservation

The following paths are relative to `private-locator:8f24556a330b05a11a95`.

- `initial-validity-counterexample-20261010/RESULT.md`
  - SHA-256: `97362c728875e9bbb808a3272ca1372b1488e9759651cc585af004bdd539a89b`
- `initial-validity-counterexample-20261010/check_controls.py`
  - SHA-256: `1eec67c56a713c85bcd560a8397773ff216aea8d57c39d9228019849db721adc`
- `initial-validity-counterexample-20261010/check_controls.log`
  - SHA-256: `ba3983fb771776607062cc4582292ffc183a05e1b9d79ce10f19927e1b29d09c`
- `realizable-moment-dynamics-20261010/RESULT.md`
  - SHA-256: `c5aeeeed56b5bf5edfa9b87570249f142e3d1be9c06218d8007013c66f5eb688`

All four were hashed before and after the control rerun, with identical results. The parent hash is exactly the frozen hash stated by the author. Only this separate review directory was written. A final preservation check is recorded in `FINAL_VERIFICATION.json`.

## 2. Mathematical checks

### A. Full moment equality and a positive initial representative: pass

For the standard lognormal law, the substitution `y = log x` reduces the r-th moment to the Gaussian integral of `exp(ry)`, giving `exp(r²/2)`. The discrete normalizing sum S is finite, since its tails are Gaussian. Completing the square gives `rk - k²/2 = r²/2 - (k-r)²/2`; translation by an integer r permutes all of Z. Thus the discrete probability eta has exactly the same moments for every nonnegative integer r, including total mass at r = 0. These are full-sequence identities, with no truncation or limiting interchange of signed terms.

Eta has mass `1/S` at 1. The strict condition `epsilon < 1/S` makes `eta - epsilon delta_1` positive, and its mass is `1-epsilon > 0` because S > 1. Division by that mass gives the claimed probability rho_0 with every moment finite. Its moments are exactly `(exp(r²/2)-epsilon)/(1-epsilon)`.

### B. All-grade, all-time strict positivity: pass

For every r >= 0, every x in [1,2], and every 0 <= t < T,

`x^r >= 1` and `exp(-t(x-1)) >= exp(-T)`.

Consequently `B_r(t) >= exp(-t) p exp(-T)` and

`A_r(t) >= exp(-t) (p exp(-T)-epsilon) > 0`.

The same epsilon works simultaneously for all grades and all times in the prescribed interval. Positivity does not depend on numerical quadrature, a finite grade cutoff, or an r-dependent choice. In particular it includes r = 0 and t = 0, so the normalization is everywhere legal.

### C. Boundary smoothness, hierarchy, and unnormalization: pass

Every derivative of the r-th damped moment at nonnegative times is dominated by a higher finite lognormal moment on compact right neighborhoods of zero. At zero the difference quotient can be dominated by `x^(r+1)`. Iteration supplies all continuous right-boundary derivatives, with `B_r' = -B_(r+1)`. The negative atom has the same derivative-chain relation, so `A_r' = -A_(r+1)`.

With the positive denominator A_0, the quotient rule gives the asserted hierarchy, including the r = 0 identity. The initial quotient is the sequence already represented by rho_0. Finally `a_0 = A_0/(1-epsilon)` has value 1 at zero and logarithmic derivative `-m_1`; hence it equals the specified normalized unnormalization. The assertion is coordinatewise smoothness, not a sequence-space differentiability claim.

### D. No representative at every positive time: pass

Fix any s in (0,T). If a probability rho_s on [0,infinity) represented every m_r(s), then

`kappa_s = A_0(s) rho_s + epsilon exp(-s) delta_1`

would be a positive finite measure with the same moments, including its mass, as `lambda_s = exp(-sx) mu`. Lambda_s has a finite positive exponential moment at b = s/2, since its exponential integral is at most 1. Moment determinacy therefore identifies these two positive measures. But their masses at the singleton {1} are respectively at least `epsilon exp(-s) > 0` and zero. This is a contradiction for every such s separately; it is neither an almost-everywhere conclusion nor a statement only at sampled times.

### E. Determinacy argument: pass

The argument is valid for finite positive measures and does not require unit mass. If lambda and kappa share all nonnegative integer moments and lambda has a finite exponential moment of rate b > 0, monotone convergence of the positive exponential series gives kappa the same finite exponential moment. For `|u| < b`, absolute domination by `exp(|u|x)` justifies the moment expansion of both Laplace transforms. Their transforms agree on a positive interval, and each is real analytic on the entire positive half-line, where finite mass and a local strictly positive damping margin justify termwise differentiation. The identity principle extends equality to all positive parameters. Equal zeroth moments supply equal total mass. Pushing forward by `y = exp(-x)`, with zero mass assigned to y = 0, gives equal polynomial integrals on [0,1]; polynomial density and uniqueness of finite Borel measures give equality. Every positivity and domain requirement used here is supplied.

This checks determinacy directly. It does not invoke a representation theorem for functions completely monotone only on a finite time interval.

### F. Indeterminate initial data and precise scope: pass

The interval `0 < theta < 1-epsilon S` is nonempty. In the second representative, the mass at 1 before normalization is `(1-theta)/S-epsilon > 0`; every other atomic mass and the continuous component are nonnegative. Its total mass is `1-epsilon`, and its full moments are unchanged. It is distinct from rho_0 because it has a nonzero absolutely continuous component, whereas rho_0 is discrete. Thus indeterminacy is proved for the actual modified initial sequence, rather than merely inherited without proof from the lognormal sequence.

The conclusion correctly refutes replacing positive-time realizability by unrestricted initial Stieltjes validity, even when all coordinates stay strictly positive. The construction depends on the finite horizon through epsilon. It does not give one globally coordinate-positive path on [0,infinity), and it does not settle whether determinate initial validity plus all-grade positivity suffices. No claim in the parent classification is contradicted: the new path has no positive-time representing measure and therefore lies outside that classification's admissible class.

### G. Scalar-path and attribution checks: pass

A positive probability with the proposed scalar Laplace path on any open positive interval would, by positive-time differentiation, represent all normalized coordinates there. Part D excludes that possibility. The signed measure's negative atom is therefore genuinely hidden only at the initial moment level.

The cited [Arratia–Goldstein–Kochman survey](https://dornsife.usc.edu/sergey-lototsky/wp-content/uploads/sites/211/2023/06/SizeBiasing-Survey.pdf), Section 9, Theorem 9.1 and formula (72), was independently inspected. Taking b = 1 and c = e in its discrete family gives the eta used here. Its attribution supports the author's Chihara–Leipnik naming. This review makes no claim to have inspected Leipnik's original full text or to establish novelty of the hierarchy application.

## 3. Fresh exact-control execution

Executed from the workspace root on 2026-10-10 at 15:58:46–15:58:47 UTC:

`python initial-validity-counterexample-20261010/check_controls.py`

The actual Python executable, exact timestamps, versions, before/after input hashes, and output bindings are in `CONTROL_RECEIPT.json`.

- Python 3.12.14; SymPy 1.14.0.
- Exit code: 0.
- Three exact algebraic assertions passed: the square-completion exponent identity, normalized hierarchy quotient identity, and negative-atom derivative-chain identity.
- Standard error was empty.
- Fresh stdout is stored in `check_controls.rerun.log` and is byte-identical to the author's log.
- Fresh stdout SHA-256: `ba3983fb771776607062cc4582292ffc183a05e1b9d79ce10f19927e1b29d09c`.
- Empty stderr SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The script correctly labels its scope. Its assertions check algebra, not Gaussian summation, measure positivity, universal inequalities, differentiability under the integral, or determinacy. The universal result is supported by the independent proof checks above, not by the script or numerical sampling.

## 4. Final disposition

No blocking mathematical, control, or scope defect was found in the bound author result. The review is complete for the requested claims. No broader campaign, determinate-data theorem, formal certification, or parent-classification revision is included.
