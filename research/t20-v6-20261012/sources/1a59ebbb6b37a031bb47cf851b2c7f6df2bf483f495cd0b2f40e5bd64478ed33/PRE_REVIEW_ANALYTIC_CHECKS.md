# Pre-freeze analytical checks

Status: reviewer working notes for the specific entire-fixed-marginal endpoint theorem. These are not an approval of an author artifact and have no integration, release, or closure authority.

## Provenance and independence

The parent supplied the theorem proposal, a direct-method outline, a two-row control, and then a cosine-squared mixture shortcut. Those are participating inputs. The reviewer independently reconstructed the mathematics, checked the primary sources, and wrote the finite-fibre numerical controls in this folder. The author proof will be reviewed after its freeze. Independent checking is not independent origination of the theorem or all of its proof ideas.

## Conditional square-root construction

Let μi(dy,dz)=ν(dy)qi(y,dz), λy=q0(y)+q1(y), and λ=μ0+μ1. A globally Borel RN derivative fi=dμi/dλ gives compatible fibre derivatives for ν-almost every y, after one common null-set adjustment. This avoids assuming separate arbitrary choices of fibre derivatives are jointly measurable. The functions ui=√fi have fibre L² norm 1. Set cy=∫u0u1 dλy, θy=arccos(cy) in [0,π/2]. Kernel integration makes cy and θy measurable.

For θ>0, use ut=[sin((1−t)θ)u0+sin(tθ)u1]/sinθ; use the continuous coefficient limits at θ=0. The fibre norm is 1 and the squared fibre derivative norm is θ². Set qt=ut²λy and r=2ut∂tutλy, with zero transport. For interior times ut is positive λy-almost everywhere, since f0+f1=1 and both coefficients are positive. Define α=2∂tut/ut there. At zero-density endpoints the rate can diverge, but endpoints are dt-null. Thus the action is exactly 4∫θy²dν≤π². These assertions do not assert optimality when transport is allowed.

The path is even Lipschitz in total variation: ∫|ut²−us²|dλy≤2‖ut−us‖L²≤2θy|t−s|, so integration gives ≤π|t−s|. This also gives the endpoint traces without regularity of ν or the endpoint laws.

## Direct method

For action at most C and mass identically 1, total spacetime mass is 1, and the total variations of transport and source are at most √C individually. Extract weak-* limits. The quadratic perspective action is weak-* lower semicontinuous, for example using

E(ρ,j,r)=sup over continuous b,c of [2∫b·dj+2∫c dr−∫(|b|²+c²)dρ].

Finite action forces j,r absolutely continuous with respect to ρ. The fixed spacetime pushforward (t,x)↦(t,πYx) is dt⊗ν and passes to the limit. It fixes the time marginal dt and yields a probability disintegration almost everywhere. For smooth φ, the CE and Cauchy-Schwarz give

|∫φ d(μt−μs)|≤√((t−s)E[s,t]) · supx√(|∇φ|²+φ²).

A countable dense smooth test family reconstructs the narrow-continuous representative, and the integrated CE supplies the prescribed endpoint traces. Continuous marginal tests then hold at all times. Equivalently, extract the curves directly by uniform narrow equicontinuity and pass to their spacetime measures. Compactness here is in the narrow/weak-* topology, not a claim that the constrained metric topology is compact.

## Metric and geodesic

The same test estimate separates unequal endpoints. Time reversal proves symmetry. Concatenate two paths over durations λ and 1−λ: the action is E01/λ+E12/(1−λ). Optimize λ by the square roots of the two actions; handle a zero distance by identity of endpoints. This yields the triangle inequality.

For a minimizer of total energy E=d², partition time into positive lengths ℓi, and denote interval energies Ei and endpoint distances di. Rescaling each restriction gives di≤√(ℓiEi). Then

d≤Σdi≤Σ√(ℓiEi)≤√(Σℓi ΣEi)=d.

Equality in the chain and Cauchy-Schwarz gives Ei=ℓi d² and di=ℓi d. Apply to partitions containing s,t to obtain constant-speed geodesicity. This does not need an unproved optimal time reparametrization result.

## Nested finite tests

At every relaxation stage keep exact probability mass 1 and impose the first N tests from a countable continuous family with uniformly dense linear span in C(Y). These are pathwise-in-time constraints. Nested feasible sets and a common full-marginal competitor give EN increasing and bounded above by E∞≤π². Compactness gives a subsequential limit of minimizers. Every fixed test survives eventually; density and continuity imply the entire marginal. Lower semicontinuity forces E∞≤Elimit≤lim EN≤E∞. Hence EN→E∞ and every cluster path is optimal. There is no rate, finite-N equality claim, full-sequence convergence without uniqueness, strong control-field convergence, time/space-grid consistency theorem, or solver claim.

Exact mass is an explicit hypothesis used for this simple compactness proof. These notes do not claim it is a logically necessary condition for all possible alternative proofs.

## Convex-set shortcut supplied by parent

Let a=cos²(πt/2), b=sin²(πt/2). The mixture μt=aμ0+bμ1 remains in any convex subset K of probability measures containing the endpoints. Taking zero transport and reaction r=a′μ0+b′μ1, pointwise weighted Cauchy-Schwarz gives

|a′f0+b′f1|²/(af0+bf1)≤(a′²/a)f0+(b′²/b)f1.

The right side integrates to π² at interior times. Thus the path has action at most π². Weak closedness of K gives the direct-method closure. Time independence gives restriction/concatenation closure. This establishes the same existence/metric/geodesic mechanism for such K; the sharper conditional-angle upper bound is special additional information for the fixed marginal.

## Independent finite-test leakage example

On Y=R/Z, let ν be uniform, Z a singleton, and fix N. The density

1+ε sin(πt) cos(2π(N+1)y),  0<ε<1,

has mass 1 and keeps every sine/cosine marginal moment of frequencies 1,…,N equal to ν. The source is επ cos(πt) cos(2π(N+1)y), with zero transport, and has finite weighted action because the density is at least 1−ε. Its untested cosine moment at frequency N+1 is ε sin(πt)/2. Endpoints are both ν. This is a feasible, non-optimal control example; it demonstrates why a finite stage is not the entire-marginal constraint. It is not a counterexample to convergence of optimal energies.

## Primary-source context (bounded summary)

[2512.09250v1](https://arxiv.org/html/2512.09250v1), Definition 2, Section 3 and Appendix C.1: the paper uses the half-normalized quadratic action and gives finite-continuous-affine-constraint attainment conditional on finite-action feasibility. It does not by that finite-index statement alone prove the entire-marginal conclusion.

[2402.15860v3](https://arxiv.org/html/2402.15860v3), Theorem 3.4, Lemma 3.8, Theorem 3.9 and Theorem 5.5: constrained attainment, constant energy, metric structure, and a parallelizable-manifold extension already appear in the immediate ancestor. The present check does not assign priority to the general constrained-metric idea or conduct an exhaustive novelty search.
