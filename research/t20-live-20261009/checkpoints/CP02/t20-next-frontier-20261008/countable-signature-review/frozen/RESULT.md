# Countable input signatures and finite productive inventories

8 October 2026 UTC. It is a new sibling after the frozen finite-signature and noise-aware stages. No earlier stage is changed.

## Main result

**A single fixed computable calibration identifies every finite unguarded route histogram on a countably indexed port alphabet, without a supplied bound on the largest active index.** The calibration is x_i=4^(-2^i). A finite positive support is encoded by e=sum(2^i), giving route-failure factor f_e=1-4^(-e).

Zsigmondy's base4 order theorem makes these factors multiplicatively independent for finite integer histograms. The exact all-issued no-effect probability therefore uniquely identifies the histogram. The rational denominator is4^M with M=sum(e n_e), so the readout itself bounds the finite search. It does not identify the counts without the numerator information.

The first decoder uses numerator prime orders and descending elimination. A subsequent gcd decoder avoids factorisation altogether: it strips old prime support from each4^e-1, retains a certified complete new-prime component, and decodes multiplicities in descending order. It runs in deterministic polynomial bit complexity for an explicitly expanded binary numerator/denominator pair. That is not a polynomial claim in a compressed expression, latent model description, port index, or experimental sampling cost. Details and certificates are in `GCD_DECODER.md`.

## Primary-source verification

The original Zsigmondy1892 scan was inspected at printed p.283. Its specialised order theorem's exceptions do not cover base4; the following paragraph explicitly uses that base. Győry–Smyth2010, Theorem13 p.325 and Lemma6 p.323, provide a modern primary cross-check. The n=1 case is handled directly by prime3. [Original scan](https://zenodo.org/records/2131326/files/article.pdf?download=1), [modern research paper](https://math.colgate.edu/~integers/k27/k27.pdf).

This source check is substantive: the analogous base2 code has a real collision, f_6 f_1=f_2² f_3. The report does not claim that a primitive prime at every exponent is necessary for every other base. The independent review contains a separate arithmetic boundary note; the implemented construction stays with the uniformly justified base4 case.

## What the exact readout does not establish

Allowing infinitely many routes invalidates the finite inference. A computable greedy tail using only factors with e>E, each at multiplicity at most4, has real product exactly f_E. It therefore mimics a single finite route despite infinitely many active supports. Finite prefixes come with explicit error bounds and never equal the target. Prime valuations and denominator grades do not commute with that real limit.

In the unguarded independent class, a second query can supply a positive finitude certificate. Restrict the issued profile to the finite root set decoded from the first exact readout. Equality of the two positive no-effect probabilities excludes all outside routes; only finitely many inside support types remain, and infinitely many independent copies of any one would force probability zero. Thus the actual inventory is finite within that class.

That certificate requires every route to affect the compared absence event. Guards can defeat it by switching which routes are enabled under restriction. Exact equality also cannot be replaced by one fixed tolerance across unbounded indices. With an already exact first readout, however, a candidate-dependent discrete gap can sometimes certify the second equality from a sufficiently precise enclosure. These qualifications and a guarded counterexample are proved in `FINITENESS_AUDIT.md` and `ORACLE_AND_EXTENSION_BOUNDARIES.md`.

## Unknown guards and approximation oracles

No finite issued-profile panel identifies the unrestricted finite guarded inventory on an unknown countable signature. Finitely many profiles assign only finitely many membership patterns to infinitely many indices. Two indices share a pattern, so a route requiring one present and the other absent is disabled throughout the panel. This remains true for infinite issued subsets and arbitrary attenuation rates. A deterministic finite-stopping adaptive algorithm has the same problem along its realised query history.

For the unguarded fixed base4 calibration, exact rational access is stronger than arbitrary valid Cauchy approximations. Any finite reply transcript around a finite model also fits a model with an extra sufficiently rare high-index route. Hence exact finite-stopping identification is unavailable from that approximation oracle alone. Under the finite-model promise, ordinary least-consistent enumeration identifies the histogram in the limit. Guarded histograms likewise admit limit learning by fairly refining finite profiles and precision. Stabilisation has no general knowable stopping time.

The code tests finite prefixes of these constructions; it does not claim that an observed plateau certifies convergence. The approximation result is for the prescribed fixed calibration, while the guarded membership-pattern obstruction survives arbitrary rates. Neither result is an empirical theorem about human inquiry or a metaphysical source count.

## Which algebraic extensions preserve the result

The finite natural histogram map is a multiplicative monoid embedding, with an additive denominator grade. Finite rational-coefficient relations also remain independent after clearing denominators. Arbitrary real intensities do not: f_1=f_2^[log(f_1)/log(f_2)]. The infinite integer-tail construction is a different failure under real-product completion.

Trial-varying mixtures also change the problem. The exact identity

(1-x)+(1-y)=(1-x)(1-y)+(1-xy)

makes two different half-and-half mixtures agree on every one-trial endpoint law across all rate vectors and issued profiles. If one sampled inventory is held fixed across two conditionally independent repeats, their second no-effect moments differ by xy(1-x)(1-y). At x=y=1/2 they are1/4 and5/16. Resampling inventory between repeats removes the distinction again.

This gives an explicit higher-order observation and grouping requirement, not an assertion that two moments identify arbitrary mixtures. The paired trials are separate episodes; they are not two original producers independently creating the numerically same effect in one episode.

## Evidence and remaining boundary

The author suites currently contain15 finite/countable controls,6 gcd-decoder controls and8 oracle/extension controls. They include exact base4 primitive-order checks, unknown high-index recovery, descending zero candidates, a genuine base2 collision, all272 weighted histograms through weight12, factorisation-free recovery of support code256,5,000-fold multiplicity at code1, guarded invisible-route witnesses, greedy-prefix bounds, approximation-compatible alternatives, provisional learners, mixture equality and grouped-repeat separation.

The arbitrary finite and countable claims depend on the written proofs and the correctly scoped classical arithmetic theorem, not on those finite tests alone. The independent reviewer has separate partition, gcd, source and infinite-tail controls. A resource cap is reported as inconclusive, not as an invalid model.

No countably infinite set of necessary originals is established. The known objects are calibrated port indices and stipulated route laws; productive reality, true bearer ownership, complete observed output, independence, trial stability and admission of the interventions remain external obligations. The source's original-efficacy bridge is not supplied by the mathematical code. No protected integration, owner acceptance or T20 closure follows.
