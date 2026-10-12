# Conditional normalisation can leave the integrated moment domain

11 October 2026 UTC. Additive root discriminator for §7 of the frozen correction-audit transport application. This instantiates an acknowledged caveat; it does not repair a false theorem or claim a new general Bayes principle.

Let observed Y range over positive integers with ν({n})=2^(-n). Set ε_n=2^(-n), x_n=2^(n/2), and r_n=(1−ε_n)δ_0+ε_nδ_(x_n). The target conditional mean is zero and variance one. The initial integrated relative second moment is

    Σ_n ν_n ε_n x_n² = Σ_n 2^(-n) = 1.

Define the bounded, strictly positive Borel likelihood by L(n,x_n)=1 and L(n,x)=ε_n² at all other x. This is a specified pointwise version, so its values at the atoms are meaningful. The conditional normalizer is Z_n=ε_n+ε_n²−ε_n³. Separate conditional normalisation preserves ν and changes the high-atom mass to

    p_n = 1/(1+ε_n−ε_n²) ≥ 4/5.

The inequality follows from 5/4−(1+ε−ε²)=(ε−1/2)²≥0. Thus the corrected integrated second moment is Σ_n p_n, which diverges, and its first N terms are at least 4N/5. Every individual conditional law still has finite second moment. The failure is specifically integration over the preserved observed marginal.

In contrast, one global joint Bayesian normalisation changes the observed marginal to weights ν_n Z_n/Z. Its normalizer and second moment are

    Z = Σ_n (4^(-n)+8^(-n)−16^(-n)) = 43/105,
    E_global[X²] = (Σ_n 2^(-n))/Z = 105/43.

This global audit is outside the original fixed-ν contract, but within the finite integrated moment domain for the new marginal. It is therefore not interchangeable with separately normalized conditional audits. A uniform lower likelihood bound is a sufficient protective condition for the latter, but this example does not assert its necessity.

## Consequence and limits

Bounded positive likelihoods preserve finite second moment on one fixed probability space after one global normalization. They need not preserve an integrated conditional moment after separate normalizations with arbitrarily small normalizers. The source-correction interface must check its chosen normalization contract and post-audit moment hypothesis.

The counterexample does not say the OU–reaction probability map is undefined. Its one-step law-level definition can extend beyond the finite-moment class. It shows that the inherited finite-moment entrance theorem cannot be invoked through this route without another argument. It makes no claim about the later integrated entropy or convergence of these particular outputs.

No claim is made that an actual epistemic source has this likelihood, or that numerical admissibility establishes the warrant for an audit. This is an exact mathematical discriminator for the interface.

## Verification

check_domain.py executes nine rational/symbolic controls in both normal and optimized Python, with identical output. Four finite partial-sum checks illustrate the analytic bound; the divergence proof is the uniform lower bound above, not finite testing. Two first controls share the same geometric sum but verify different interpretations; counts are not independent evidential witnesses. No Lean/kernel certification or external peer review occurred.
