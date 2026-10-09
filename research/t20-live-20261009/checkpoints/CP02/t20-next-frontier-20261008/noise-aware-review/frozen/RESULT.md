# Noise-aware recovery of bounded productive-route histograms

8 October 2026. New sibling after the exact prime-probe and universal CRT stages. Those stages remain unchanged. The full deductions and numerical certificate are in `THEOREMS.md`.

## Result

**With a known valid route-count bound K, a different mask instrument recovers the declared histogram with finite confidence and a sample budget polynomial in K at fixed root count.** It also has a proved finite numerical precision target. This improves the sampling behaviour of the earlier fixed nonzero calibration by changing the instrument as K changes.

Give every selected incidence survival probability p=1/(2K), and suppress other incidences while holding issued roots and absence guards fixed. Every relevant no-effect probability is at least one-half. Logs of these probabilities have a subset-sum form. Möbius inversion, division by known log coefficients and integer rounding recover the enabled positive-support counts. Exact guard and effect-bundle inversions then recover the full histogram.

At r roots, an error tolerance epsilon=p^r/(16·2^r) keeps each exact-log count estimate within one-quarter of its true integer. For L retained probability coordinates and confidence at least 1-delta, a sufficient number of independent trials per actuator setting is

ceil[128·(16K²)^r·log(2L/delta)].

This is a conservative upper bound, not an experimentally optimised sample recommendation. In the full guarded m-effect problem there are G=3^r-2^r issued-profile/mask settings and L=G(2^m-1) coordinates. One paired endpoint observation supplies every effect-query indicator at its setting, so total trials are G times the per-setting budget.

## A matching restricted-family obstruction

The independent reviewer supplied a [separate lower-bound proof](../RESTRICTED_MASK_LOWER_BOUND.md). For K>=2, any fixed-budget protocol using these masks at the prescribed p, even with adaptive mask selection, requires at least (2K)^(2r)/45 total trials for uniform success probability at least two-thirds. Only the full mask distinguishes the explicit hard pair. The pair can also include every root in its common productive baseline when K>=r+1.

The upper and lower results therefore match the exponent of K for this fixed-rate mask family at fixed r and confidence. Constants, dependence on r, confidence dependence and optimal allocation are unresolved. No lower bound is asserted against arbitrary rates, additional observations, narrower classes or expected stopping-time protocols.

This result does not contradict the earlier exponential or unbounded-count obstruction at one fixed nonzero calibration. Choosing p using K prevents that saturation. A correct externally supplied K is part of the stronger instrument's input.

## Numerical certification is explicit

The implementation evaluates logarithms with rational artanh-series intervals and a geometric remainder bound. It chooses a finite series length from a proved error target rather than assuming a fixed iteration cap is enough.

On the statistical good event, the exact empirical inverse is within 1/4 of the true count. The certified interval adds at most 5/64, so the whole interval lies within 21/64 of that integer and strictly inside its unique rounding cell. The negative logarithmic denominator is proved bounded away from zero throughout the interval calculation.

Only exact integers and rational fractions are accepted by the certificate interface; floating inputs are rejected. An independently detected float-input defect was reproduced in a red test and corrected. If an optional arithmetic cap is too small or an empirical panel lies outside the certified region, the routine returns an explicit uncertified outcome.

A rational interval certifies the inversion of the supplied empirical numbers. It does not authenticate the stochastic model, establish the statistical good event, or independently certify the truth of the recovered counts. The probability guarantee remains conditional on the model and sampling assumptions.

## Calibration error and dependence

A bounded calibration corollary permits leakage at nominal zero masks. If each of at most Kr relevant incidences has probability error at most eta and the actual joint law has the stipulated independence, coupling bounds every endpoint-event bias by Kr eta. Allocate sampling tolerance epsilon/2 and require eta<=epsilon/(2Kr); their sum stays within the original epsilon budget. The sufficient sampling coefficient increases fourfold to 512·(16K²)^r.

The code tests both errors together and recovers the original bounded histograms. It also checks a counterexample: perfectly correlated and independent gates can have identical individual probabilities but different endpoint laws. Accurate marginals alone do not warrant the product factorisation. An external bound on total variation of the entire actual joint gate law would supply a separate endpoint-bias bound; the decoder does not infer such a bound from its own readout.

Statistical independence, the ability to control incidences separately, and metaphysical independence from foreign provision remain different claims. The probability floor alone is only a union-bound consequence and does not establish the stronger factorisation needed for logarithmic recovery.

## What the executable checks establish

Eleven author control groups pass. They include 272 extreme-error two-root panels, guarded multi-effect recovery, current coalescent/redundant/priority fixtures under the newly specified instrument, combined sampling/calibration perturbations, certified precision targets, independent high-precision comparisons of log intervals, correlation failure, and explicit rejection of inexact certificate inputs.

The perturbations are deterministic synthetic panels, not empirical trials. No large simulation or physical intervention was performed. The tests check implementation and theorem consequences; the arbitrary finite proof remains in `THEOREMS.md`. The separate reviewer has independent rational-interval and restricted-mask lower-bound checks.

## Source and continuation boundary

The recovered object is still an anonymous histogram within the declared direct-route class. Route tokens, original bearers, intrinsic acts, created effects and complete actual production are not identified with one another. The prior numerical effect convention and alias obligations remain unchanged.

Neither the known bound, attenuation masks, admissible issued profiles, calibrated response law, trial independence nor complete effect catalogue is supplied by the Arabic source argument merely because the mathematics works. A source requirement of complete decisive willing or unchanged productive conditions may prohibit these diagnostics. Even correct class-relative recovery does not establish the source's further bridge from shared actual efficacy to deficient original provision.

The new progress is a conditional, noise-aware identification theorem with an explicit arithmetic implementation, calibration budget and a matching count exponent for its restricted instrument family. The remaining philosophical work concerns the admissibility and warrant of that instrument for the particular causal interpretation, not another unqualified inference from endpoint agreement. No protected integration or T20 closure follows.
