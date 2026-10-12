# Participating proof notes: determinate moments and continuation

10 October 2026 UTC. Ordinary constructive mathematics; no independent-review or kernel credit.

The author and root independently identified a compact-fibre extraction route. The author's explicit truncated-moment constraints sharpen the root's ambient moment-cap argument. Both preserve the existence and determinacy promise; neither decides that promise.

Let c_N(y)=min(y/(1-y),N), continuously extended by N at y=1. Within probabilities on [0,1], impose for every positive integer r,N:

m_r - m_(r+1)/N <= integral c_N^r <= m_r.

An original law satisfies these because the omitted tail is at most m_(r+1)/N. Conversely the r=1 upper bounds exclude mass at 1, and monotone convergence together with the lower bounds recovers each exact m_r. The constraints are computable continuous closed inequalities with uniformly computable constants. Under promised determinacy their nonempty effectively closed compact fibre is a singleton, enabling computable weak-law extraction by finite-cover search.

For joint nonnegative-time continuation, choose a continuous cutoff chi_N equal to 1 for x<=N and 0 for x>=2N. The compactified integrand chi_N(x) x^r exp(-t x) extends continuously by zero at infinity, jointly computably for t>=0. The truncation error is bounded by m_(r+1)/N, including r=0 using m_1. Thus no test of whether t=0 is needed. The positive normalizer has computable lower bound exp(-t m_1) by Jensen. Division supplies every damped normalized moment. This reasoning must be checked against actual representations and the finite-cover implementation.

Geometric corollary in a specified natural affine coordinate: the initial mean and all derivatives of Fisher variance determine cumulants by V^(k)(0)=(-1)^k kappa_(k+2). Finite cumulant-to-moment recurrences recover uniform moment names. Under the determinacy promise, the preceding algorithm recovers the damped law and hence the future covariance geometry. This is not a claim from uncalibrated intrinsic metric jets alone, nor a convergent Taylor construction, nor an epistemic-warrant inference.

A strict extension beyond exponential tails is the probability density (1/2)exp(-sqrt(x)), x>=0. Its moments are (2r+1)!. The symmetrised square-root law has density |y| exp(-|y|)/2 and admits positive exponential moments below rate 1. Any competing half-line law with these moments induces the same all-order moments after symmetrised square root. The inherited exponential-moment determinacy proof therefore establishes uniqueness, whereas the original x-law has no positive exponential moment. Its Laplace Taylor series has zero radius. Thus a nonanalytic endpoint need not obstruct effective continuation when its moment fibre is determinate.
