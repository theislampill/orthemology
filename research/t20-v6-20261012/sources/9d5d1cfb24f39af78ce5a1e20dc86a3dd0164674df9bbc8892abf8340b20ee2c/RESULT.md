# Exact-law correction is not a prior-independent single-sample channel

11 October 2026. Focused application check, using inherited mechanisms and the parent's specified fixture. No protected edit, new sampling campaign, algorithm, or novel mathematical theorem is claimed.

## Conditional result

For the split map Φ=R_a D_h toward π=N(0,1), with h=log 2, a=1/2, there is no fixed Markov kernel K(x,dz) satisfying μK=Φ(μ) for every finite-second-moment input law μ. The claim already fails on {δ_−1, δ_+1, (δ_−1+δ_+1)/2}. This does not contest the inherited injectivity of Φ as a function of exact laws.

Every fixed Markov kernel is affine on input laws: (tμ+(1−t)ν)K=tμK+(1−t)νK. Independent auxiliary randomness is included in this statement. The following fixture violates that necessary condition.

## Exact fixture and proof

Write μ=(δ_−1+δ_+1)/2. The OU stage has A=1/2 and Q=3/4, hence D_hδ_±1=N(±1/2,3/4). Reaction gives

    Φ(δ_±1)=N(±2/7,6/7).

Because reaction acts on the total input density, the true mixture output has density proportional to

    exp(−7z²/12) sqrt(cosh(2z/3)).

The mixture of the two individual outputs instead has density proportional to

    exp(−7z²/12) cosh(z/3).

Their logarithmic second derivatives at zero are −17/18 and −19/18, respectively, a difference of 1/9. Normalizing constants disappear under these derivatives. The densities cannot agree almost everywhere: they are strictly positive and smooth, so equality almost everywhere would imply pointwise equality and equal derivatives. Thus Φ(μ)≠[Φ(δ_−1)+Φ(δ_+1)]/2, contradicting affinity.

The exact arithmetic was executed with SymPy; EXACT_CHECK.txt records the five checked identities. The proof is the affinity argument, not a numerical simulation.

The inherited split report §6 uses a symmetric mixture with means ±1 *after* diffusion. This fixture starts with Diracs at ±1, giving post-diffusion means ±1/2. Its smaller cosh arguments are deliberate. The obstruction is the same inherited mixture-power mechanism, not an independent discovery.

## Injectivity of OU laws does not supply statistical sufficiency

OU itself is a genuine fixed sample channel. Its characteristic-function formula is

    characteristic(D_h μ)(t)=characteristic(μ)(Aᵀt) exp(−tᵀQt/2)

in the centred case. Invertibility of A and nonvanishing of the Gaussian factor give uniqueness of the input law from the entire exact output law. This is algebraic identifiability on the image. It neither gives a stable finite-data procedure nor a Markov inverse.

Indeed, a Markov reverse L for even the two-state experiment {δ_−1,δ_+1} would need

    N(−1/2,3/4)L=δ_−1,     N(+1/2,3/4)L=δ_+1.

Let b(z)=L(z,{+1}), so 0≤b≤1. The first equality forces b=0 almost surely under the first Gaussian; the second forces b=1 almost surely under the second. Both Gaussians have strictly positive Lebesgue densities and are mutually absolutely continuous. These requirements are contradictory. Therefore the noisy observation is not Blackwell-equivalent to the original two-point experiment and is not sufficient to retain all its decision information. Exact law injectivity survives nonetheless.

This is a model-relative sufficiency statement for the explicitly specified two-point family, not a claim that every restricted experiment loses every statistic. With a known prior, a posterior reverse can regenerate its marginal by posterior sampling; that prior-dependent construction is not a single reverse valid for both point-mass parameters, and does not recover the actual original sample with certainty.

## Application consequence

The full Φ is an operation on an available law-state, or on a representation of that law sufficient to perform its density power and normalization. A prior-dependent procedure, or a procedure given the full input law as additional data, is outside the fixed-one-sample obstruction. The inherited Gaussian parameter update remains valid when its needed parameters are supplied. No universal finite representation or single-sample implementation follows from existence, descent, convergence, or injectivity of the exact law operation.

Accordingly, an interface that currently supplies only one incoming draw plus a fixed sample kernel cannot implement this full Φ universally. Such an interface would need additional law information or a separately specified approximation contract. This is a conditional interface obligation, not evidence that any inspected runtime falsely promised the implementation. Full Φ should not be assigned ordinary channel data-processing or Blackwell consequences without first supplying an actual channel contract. Target-relative entropy descent also supplies no new observation, authentication, warrant, or correctness of the target.

## Deduplication and scope

- fibrewise-split-correction-20261011/RESULT.md §§2–6 already owns OU sample implementation, normalized density reaction, Gaussian-law formulas, and the finite-mixture power obstruction; its final paragraph already separates target correction from evidence assimilation.
- information-geometry-transport-20261009/RESULT.md §3, especially the paragraph beginning “Recovery here,” explicitly owns the distinction between full-law injectivity, outcome recovery, statistical sufficiency, stochastic inverse, and isometry. This check applies that existing distinction to OU.
- noetic-gradient-transport-20261009/RESULT.md §§1, 6–8 already separates divergence contraction, prescribed correction transport, and truth/warrant. Those are not new findings here.
- stochastic-exact-inquiry-20261010/RESULT.md §§1–2, 7 owns the fixed hidden-state channel/common-policy contract and finite positive-likelihood zero-error obstruction; it explicitly declined an all-proper-score/Blackwell route as mainly classical restatement. stochastic-inquiry-quotient-transport-20261010/ADDENDUM.md separately distinguishes posterior preservation from complete predictive and stopping contracts. No part of their stopping analysis is extended here.

The scoped reports and decisive sections were inspected; the large concatenated read was truncated, followed by targeted keyword/section inspection. This is not a claim of complete rereading of all inherited reports or an exhaustive corpus absence search. No new external literature was needed: affinity and mutual-absolute-continuity proofs are given in full. The modest present contribution is a precise interface conclusion for this Φ, with the parent's exact ±1 fixture and inherited credit attached.
