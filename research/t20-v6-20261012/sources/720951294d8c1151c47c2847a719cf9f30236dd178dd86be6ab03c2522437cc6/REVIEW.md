# Independent mathematical review: capped tensor recovery

Status: PASS for independently checked positive C1–C7, finite-data recovery, cap-free moment continuation, and frozen replay. The reviewer participated in constructing §7.2; its separate independent check is explicitly attributed. No formal-kernel or empirical claim.

## Inherited ownership

Read the finite-support tensor-moment continuation result, including its duplicate-column aggregation, interpolation, graded-product qualification, and declared-control semantic boundary. Read the compact-support moment theorem in measure-moment-continuation-boundary-20261009/RESULT.md §3: compact full-moment determinacy is already proved there and is not a new result here. Read effective-stationary-selection-20261010/RESULT.md E2/E3 and its ℓ1 input contract: effective cap compactness and singleton computation are already proved there. The proposed new bridge is their effective inverse/finite-precision use for indexed law recovery.

## Representation and identification

The support is a known uniformly computable indexed family κ_j in a finite probability simplex. Distinctness is a promise; no real equality decision or effective uniform lower separation is presumed. A complete moment name must give tensor coordinates uniformly in degree, coordinate and requested precision. Merely saying that each individual real coordinate is computable would be insufficient.

Each coordinate coefficient κ_j,a1⋯κ_j,ar lies in [0,1]. Thus each moment coordinate is a computable bounded linear functional on ℓ1 and is 1-Lipschitz. There are finitely many coordinates in each degree; their max norm is computable. A geometrically weighted product metric/residual has an effective tail because each moment component lies in [0,1]. The infinite record belongs to a product, not the inherited algebraic direct sum.

Full moments determine the Borel pushforward measure on the compact closed simplex by polynomial density and finite-measure uniqueness. The indexed law is then identified because μ({κ_j})=p_j for pairwise distinct support. This argument remains valid if support points accumulate at another support point. It does not require effectively isolating that singleton geometrically. If equal support columns are allowed, only the sum of their masses is identified; named source records and token interventions are not silently preserved.

## Effective inverse and finite precision

The nonnegative computable cap and its effective summable-tail modulus provide effective upper compactness of Kc in ℓ1. The total C≥1 guarantees nonemptiness. A consistent complete moment input defines a nonempty zero fibre through a computable nonnegative weighted discrepancy. The fibre is effectively upper compact via Kc⊂U∪{residual>0}; distinct support makes it a singleton. Semideciding containment in rational ℓ1 balls computes that singleton uniformly. Approximation outputs may be rational ideal points outside the exact cap; they name the valid law. No feasibility decision for arbitrary input records is required or obtained.

A stronger uniform finite certificate follows from effective upper compactness of Kc×Kc. For requested positive ε, search finite grade R and rational δ>0 for the cover

Kc² ⊂ {||p−q||1<ε} ∪ {max_{r≤R}||Mr(p)−Mr(q)||∞>δ}.

The right side is effectively open. Product effective compactness follows either from finite product nets or the inherited upper-compact construction. The compact set of pairs at distance at least ε contains no full-moment equality pair. Its open separation cover admits a finite subcover and a positive minimum margin. Therefore some R,δ succeeds. Every accepted certificate gives a strict ℓ1-error bound whenever all listed moment discrepancies are at most δ. This is an effective search with a termination proof, rather than a bare compact-inverse existence claim. It needs no computable dense subset of an arbitrary effectively closed feasible set and does not decide distinctness.

If observed finite coordinates and candidate predictions each differ from the same supplied data by η, their true pairwise discrepancy is at most 2η. Appropriate additional numerical evaluation error must also be budgeted. The certificate by itself does not promise a feasible law for inconsistent/noisy data. No sample-complexity or efficiency estimate follows from the terminating cover search.

## Finite exact cutoff and support accumulation

For C>1, the seed c/C is strictly inside each positive cap coordinate. Any fixed finite grade has only finitely many scalar moment constraints, including normalization. Choose more positive-cap indices than constraints and a nonzero finitely supported null vector h. Since its coordinate sum is zero, it has both signs. A sufficiently small perturbation ±th of c/C remains strictly positive and below the cap at the chosen indices, with all other entries unchanged. These two laws agree at the selected grades but differ. This proves failure of every fixed exact finite-grade cutoff when infinitely many cap entries are positive. Their higher moments eventually distinguish them by complete-moment determinacy. The argument is compatible with arbitrarily accurate finite certificates: the undetected perturbations can be arbitrarily small.

The C=1 case is a singleton cap and is excluded correctly. Finite positive-cap support has a finite interpolation bound. No absolute memory lower bound for arbitrary encodings is asserted.

Without cap control, a specified accumulation example shows discontinuity: κ0=(0,1), κj=(2^-j,1−2^-j), p^(j)=δj and p=δ0 have every fixed moment difference tending to zero while ||p^(j)−p||1=2. This is an existential obstruction on this support. It does not show failure of pointwise inverse continuity for every possible countable support, and does not change compact moment determinacy. An effective cap excludes the escaping unit masses and restores ℓ1 compactness.

## Independent finite corroboration

controls/independent_checks.py uses exact fractions and passes 2,929 checks: finite-support cap-admissible perturbations on one fixed infinite dyadic support agree in every binary tensor coordinate through the requested degree, differ at the next degree, and preserve normalization; support-accumulation moment differences satisfy the r·2^-j bound; a two-atom control checks the factor between grade-one max error and ℓ1 weight error. These finite executions corroborate examples only. They do not prove the universal effective or noncomputability assertions.

## Finite-data reconstruction and transport checks

A finite family of rational closed moment bands defines F⊂Kc that is effectively upper compact: its complement relative to Kc is enumerably open through strict band violation. Under the promise F≠∅, choosing band widths so that their pairwise discrepancies are within the certificate makes F have small diameter. Searching rational centers for a certified containment F⊂B(q,ε) then returns an ℓ1 approximation to every compatible law. Existence follows by taking a center close to any one member and using the smaller diameter budget. No effective dense enumeration of Kc or F is needed. Empty/inconsistent inputs are outside the recovery promise; no general decision procedure for band consistency follows. Empty-set containment is semidecidable, which should not be confused with decidable consistency.

The original cap need not be invariant under normalized exponential tilts. For ||u||∞≤B and simplex support, e^-B≤exp(−u·κj)≤e^B, and normalization yields tilted weights at most e^(2B)cj. This enlarged cap retains an effective tail when B is a supplied computable bound. Bounded computable observable sequences with a supplied bound are ℓ1-computable functionals; arbitrary unbounded observables are outside that guarantee. None of these numerical facts identifies named sources or licenses their deletion.

## Participating no-tail refinement

The reviewer suggested the following stronger example to the author; its derivation is participating ancestry, not an independent discovery or a separately blind check. The finalized written proof and index conventions have been checked. This is a participating check; a different reviewer independently checked the construction in hidden-mass-independent-review-20261010/REVIEW.md.

Let K be the halting set and α=Σ_(e∈K)4^(-e-1)≤1/3. Use a computable bijection j=1+pair(e,t) from event pairs to positive indices. At index j put pj=4^(-e-1) if program e halts for the first time at exact stage t, and zero otherwise. Each positive-index coordinate is computable by finite simulation. Put p0=1−α, κ0=(0,1), κj=(2^-j,1−2^-j), c0=1, cj=pj for j>0. The cap is coordinate-computable and classically summable with total 1+α, but has no computable summable-tail modulus. The law lies in it and is noncomputable because p0 is noncomputable.

Noncomputability of α follows from base-four digit gaps: once earlier halting digits are known and subtracted, the residual is at most 4^(-e-1)/3 for a zero e-th digit, and at least 4^(-e-1) for a one digit. Approximation to sufficient precision decides that bit; inductively a computable α would decide K. There is no binary-expansion ambiguity.

All moment coordinates nevertheless have a uniform computable name. Write Mr=κ0^⊗r+Σ_(j≥1)pj(κj^⊗r−κ0^⊗r). The finite prefix is rational and computable. For each degree r≥1, a telescoping product bound gives max-coordinate discrepancy at j at most r·2^-j; hence the tail from N is at most r·2^-N times the remaining probability mass, at most r·2^-N. Grade zero is exactly1. This computes all coordinates uniformly in r and precision. Thus mere coordinate-computable summable caps cannot replace effective cap tails in the general inverse theorem. It is an existential accumulation-support construction, not a theorem that every non-effectively-presented cap or every infinite support defeats computation.

## Primary ancestry check

Independently opened [de Branges, pp.823–824](https://sites.math.rutgers.edu/~zeilberg/purdue22/LdeBstone.pdf): the stated polynomial-density conditions apply to the coordinate algebra. Independently reopened [Galatolo–Hoyrup–Rojas, Theorem2.9 and Remark5](https://members.loria.fr/MHoyrup/computinvmeas.pdf): the compact unique-zero argument is explicitly uniform. These decisive passages, rather than both entire papers or a new literature search, were checked. SOURCE_CHECKS.json binds retained ancestors and the inspected scopes.

A further no-tail qualification is essential: computable nonnegative cap coordinates together with a computable supplied exact total also compute a tail modulus by partial-sum search. The participating counterexample has noncomputable total 1+α. It does not refute recovery with an equivalent computable total-mass input.

## Cap-free moment continuation clarification

The parent's additional corollary was independently checked. Given complete moments of a probability on the simplex and a computable control with ||u||∞≤B, the degree-s tilted numerator is the sum over r≥0 of (-1)^r/r! times M_(s+r) contracted against u in exactly r slots. For each tensor coordinate, the exponential Taylor remainder after r=R is bounded by e^B B^(R+1)/(R+1)!, uniformly in the original law and degree s. This follows from |u·κ|≤B and max-coordinate norm of κ^⊗s≤1. The same series at s=0 computes the denominator, bounded below by e^-B. Effective truncation and division therefore compute the complete updated moment name without any cap.

Each finite contraction is computable; when tensor entries are approximate, a conservative entry-error bound uses the sum of absolute contraction coefficients, at most ||u||1^r, with an additional finite error budget for approximating u. The factorial tail supplies a terminating precision search, not an efficiency estimate. No unjustified termwise sum of a noncompact exponential series is used: the simplex is bounded.

Consequently the participating no-tail example still has computable κ-output and full tensor-moment continuation. The cap strengthens recovery of the indexed law in ℓ1, rather than being necessary for the inherited moment/output interface. This does not give all bounded computable indexed observables without a cap: the index-zero indicator is a bounded computable sequence, but its expectation is the example's noncomputable p0. No named-source or provenance equivalence follows from numerical continuation.

## Final frozen evidence

Author RESULT.md SHA256: 262503e92380ec868f28670b18939d701cd51808aedc65f7fe6f2fa57e0dbf6d.
Author MANIFEST.json SHA256: 40315f75e0136493b8706aefdf7bc17a9844a5a38ba60e5d6dd630f84128aad1.

Fresh snapshot capped-tensor-review-replay-20261010 passes all 1,304 author exact rational checks. All 12 author manifest bindings match original and replay before and after execution. Reviewer-written independent controls pass 2,929 checks. REPLAY_RECEIPT.json records the command, scope, and result; no baseline, protected source or prior frozen review changed.

The final attribution-only delta was inspected, including the separate negative-review reference. The equivalent-total qualification, explicit diagonal input e and first-halt stage convention, strict-error cutoff N=k+ceil(log2 r)+1, and cap-free continuation corollary are present in the frozen source. No remaining blocking mathematical defect was found in the reviewed scope. This does not independently repeat author repository-discovery searches or certify field-wide novelty.
