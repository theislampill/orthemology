# Participating root proof notes: determinate initial moments versus hierarchy viability

2026-10-10 UTC. Participating research, not independent review. Existing packets remain unchanged.

## Full-atom route

Root and worker independently identified that deleting the entire atom of an N-extremal measure could strengthen the indeterminate-initial counterexample. Worker then identified the simpler Krein zero-atom construction.

For a standard lognormal law mu, choose its nonnegative Krein N-extremal representative eta. Write w=eta({0}). Then 0<w<1. The normalised atom-deleted law rho=(eta-w delta_0)/(1-w) is Hamburger determinate, by the classical full-atom deletion theorem. Its moments are c_0=1 and c_n=exp(n^2/2)/(1-w) for n>=1.

Let B_n(t)=integral x^n exp(-tx) dmu. Put a_0=(B_0-w)/(1-w), a_n=B_n/(1-w) for n>=1, and m_n=a_n/a_0. All coordinates are positive until the unique finite t_star at which B_0(t_star)=w. They satisfy the hierarchy and have initial data c. No positive-time moment representative exists, since adding back w delta_0 to a hypothetical representing positive measure would duplicate all moments of the exponentially damped nonatomic mu, which is moment determinate. The atom at zero then gives a contradiction.

An explicit safe horizon is (1-w)/(2 exp(1/2)), using B_0(t)>=1-t exp(1/2). Any prescribed finite horizon is obtained by positive spatial scaling. Positive scaling preserves determinacy.

This is stronger than failure of an arbitrary ODE uniqueness theorem: the same determinate initial moments also admit their actual positive-law tilt, and that solution is distinct at every positive time. Positivity of individual coordinates does not preserve the full Stieltjes moment cone.

## Computable atom candidate, independently derived

Set q=exp(-1). For H_N=(q^{-(i+j)^2/2}) indexed 0,...,N, the polynomial minimisation with constant coefficient one gives

    w_N = det(H_N) / det(H_N restricted to 1,...,N).

Indeed this is the Schur complement, equivalently the reciprocal of the (0,0) inverse entry. Factor H_ij=q^{-i^2/2}q^{-j^2/2}(q^{-i})^j. The Vandermonde determinant quotient yields

    w_N = product_{j=1}^N (1-q^j).

If the usual N-extremal atom/Christoffel equality is verified in the source, w=lim w_N. The product is positive and computable; its tail lies between 1-q^(N+1)/(1-q) and 1 whenever the lower bound is positive. This would make the entire determinate initial moment name computable. The inherited determinate-recovery result computes the unique positive law, yet the bare coordinatewise-positive hierarchy still has the invalid path above. No contradiction: that earlier result never asserted that arbitrary hierarchy solutions remain realizable.

## Source inspection boundary

Root directly inspected Berg and Christensen, Density questions in the classical theory of moments (1981), Theorem 7, printed pp111-112: complete atom deletion from an indeterminate N-extremal measure gives a determinate measure. URL https://www.numdam.org/article/AIF_1981__31_3_99_0.pdf . Root also inspected Jablonski, Jung and Stochel, arXiv:1110.0249, section2.1, printed p6, equation2.1.6 and following paragraph: the Krein representative is N-extremal, nonnegative, and has zero in its discrete support. URL https://arxiv.org/pdf/1110.0249 . These are targeted contextual inspections, not whole-paper readings or new source discoveries.

## Positive Carleman boundary

Worker independently found a positive uniqueness route via count generating functions. Root checked the divergence transfer: if b_n=c_n^(-1/(2n)) is decreasing and sum b_n diverges, then sum min(b_n,n^(-1/2)) diverges by Cauchy condensation. The condensed terms have the form min(2^k b_(2^k),2^(k/2)); truncation at a diverging cap cannot turn a divergent positive series into a convergent one. This supports the Stirling-transform Carleman estimate, and does not extend general determinacy into Carleman's sufficient condition.

## Later participating checks

The atom/kernel equality is directly present in Berg–Christensen Theorem3 proof, printedp106. The product formula is therefore supported independently of the earlier candidate status. Six finite exact determinant controls are now reproducible in check_determinant.py and its saved output; they supplement the all-N Vandermonde argument and do not verify the cited infinite-dimensional theorems.

The companion diagnostic from the author correctly isolates failure to unshifted Hankel matrices. Shifted matrices remain strictly positive definite. Every fixed finite unshifted matrix starts positive definite and remains so briefly; nevertheless some finite unshifted matrix fails at each positive time. Thus the least detecting degree tends to infinity as time decreases to zero. Root checked the rank-one Schur-complement criterion and all quantifiers directly.
