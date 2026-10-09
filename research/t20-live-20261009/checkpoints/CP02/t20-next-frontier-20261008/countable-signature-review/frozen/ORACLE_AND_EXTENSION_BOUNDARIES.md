# Observation precision and extensions of the histogram type

These are scoped applications of standard computability, algebra and probability. They explain which earlier identification results survive a change of oracle or coefficient type. No psychological or metaphysical identification is claimed.

## Exact rational input versus certified approximations

An exact numerator/denominator pair is stronger than a Cauchy oracle. Define the latter to return a rational centre y when precision k is requested, with a guarantee |y-q|<=2^(-k). It may return any valid centre, not a prescribed canonical floor or digit expansion.

No algorithm can always halt with the exact finite histogram from this oracle under the prescribed fixed base4 calibration. Run a proposed deterministic halting algorithm on a finite model whose oracle replies with its exact rational probability as the centre each time, retaining the requested nonzero error guarantee. Only finitely many precisions were requested. Add one route at a fresh sufficiently large index. Its success probability is so small that the same finite reply sequence is valid for the different finite model. The algorithm therefore returns the same answer on both.

The argument also allows finitely many adaptively chosen issued profiles: at any profile the extra route either is disabled or changes the no-effect probability by at most its tiny success probability. Choose that probability below every requested error tolerance in the finite transcript. The proof concerns the prescribed fixed calibration. It does not cover arbitrary rate interventions that could turn an unknown port up to survival one, nor a stronger canonical floor oracle.

This is not a contradiction with the polynomial exact-rational decoder. The approximation centre's denominator is not certified to be the true probability's denominator. Nor is a finite non-identification result a statement that increasingly informative observations never help.

## Identification in the limit

Under the external promise of a finite unguarded histogram, enumerate all finite histograms effectively. One enumeration uses increasing denominator weight and its finite integer partitions. At stage n, refine the probability approximation and inspect the first n hypotheses. Retain those consistent with all observed error bounds, and output the least-indexed consistent candidate, if one has been reached.

The true finite hypothesis eventually appears and is always consistent. Every earlier false hypothesis has a different exact probability by finite multiplicative independence, so sufficiently fine approximations eventually exclude it. There are only finitely many earlier indices. Consequently the provisional output stabilises to the true histogram. No finite observed plateau certifies that stabilisation has occurred.

The guarded class also admits limit learning from a fair sequence of finite profiles and precisions. Any two finite guarded histograms use a finite union R of all positive and negative indices. If they agreed on every issued subset of R, finite multiplicative independence would identify all active positive-support aggregates, and the finite guard inverse would identify the complete histograms. Thus some finite profile separates them.

Enumerate finite issued subsets and query each at increasing precision, while enumerating finite guarded hypotheses. Every earlier false hypothesis eventually meets its separating profile at adequate precision and is excluded; the true one remains. This is compatible with the impossibility of a finite complete profile census across unbounded indices.

The code supplies finite-prefix controls for these learning constructions. The learner receives only approximation replies; the test harness separately generates them from a hidden model. Its provisional history is not a finite stopping certificate. Certified error-bound oracles are also not the same as raw empirical frequencies. The finite-model promise remains essential: the infinite mimic can share a finite code's full-profile value.

## A candidate-dependent second-query gap

The finitude audit's lack of a uniform near-equality tolerance needs a qualification. Suppose the full readout q_H is already exact, admits a finite candidate, and fixes its root set R0. In the unguarded independent class, q_R0>=q_H>0. Every inside route has failure factor at most f_max, the factor for the full support R0. Hence

q_H <= q_R0 <= f_max^N,

where N is the number of inside routes. This bounds N by a finite candidate-dependent number. The possible inside supports and counts are therefore finite, and the possible rational values q_R0>=q_H form a finite set containing q_H. There is a positive gap to the next larger value.

A sufficiently narrow certified enclosure for the second response can then establish equality by this discrete gap. The code constructs the gap in small cases and returns a resource-inconclusive status if a supplied enumeration budget is inadequate. It is not a practical uniform bound: the inside-count bound and enumeration can be enormous.

This refinement does not rescue exact identification from approximate first readouts. The finite candidate, its root set and the bound were obtained from an already exact full probability. It also does not remove the unguarded, independence and visibility premises.

## Monoid structure is not arbitrary linear or tensor faithfulness

Finite natural histogram addition maps to multiplication of q, and the weighted denominator grade is additive. The result is an embedding of a free commutative monoid into positive rational multiplication. Finite integer relations are excluded, and finite rational-coefficient relations are also excluded after clearing denominators.

Arbitrary real weights are different. Since f_1,f_2 lie strictly between zero and one,

f_1 = f_2^[log(f_1)/log(f_2)].

The positive real coefficient on the right is not an occurrence count. This is a failure of injectivity after changing to arbitrary real intensities, not a counterexample within the natural-multiplicity theorem. The greedy infinite-tail equality is another failed extension: it allows a convergent infinite real product of integer-multiplicity terms. Finite rational independence does not license either extension.

Linear mixtures of whole inventories also change the experiment. At the base4 calibration, one e=1 route has probability3/4, equal to a mixture of weight3/7 on the empty inventory and4/7 on two such routes. The fixed monomial code is not an injective algebra evaluation on arbitrary mixtures.

A stronger two-port control survives every rate and issued-profile query. Let q_A=1-x, q_B=1-y, q_OR=(1-x)(1-y), and q_AND=1-xy. Then

q_A+q_B=q_OR+q_AND.

A half-and-half mixture of A-only and B-only inventories therefore matches a half-and-half mixture of redundant A/B routes and one AB-only route. At a solo profile, disabled routes have failure probability one and the same identity holds. If the inventory is resampled independently before each trial, the entire endpoint trial law agrees. This is not a model of the full original-agent assumptions; it is an explicit rejected extension to trial-varying latent inventories.

## A concrete second-order repair for that mixture pair

Hold the sampled inventory fixed across two conditionally independent trials. The probability that both trials have no effect is the mixture's second moment of q. For the two mixtures above, right minus left is

xy(1-x)(1-y)>0 when 0<x,y<1.

At x=y=1/2, the values are1/4 and5/16. If the inventory is independently resampled between trials, both values instead reduce to the square of their shared first moment and the distinction disappears.

The degree-two observable therefore separates this particular pair when trial grouping preserves one latent inventory. The retention/observation map is explicit: a single marginal loses the distinction, while the joint no-effect indicator across the grouped pair retains it. This is an actual higher-order observable, not a metaphor or a claim that two moments identify arbitrary mixtures.

Holding an inventory fixed is an added process premise. The pair consists of two trial episodes, not two original producers creating the numerically same external effect independently in one episode. Neither the grouping variable nor a tensor coordinate becomes a created effect or an underived bearer merely by representation.
