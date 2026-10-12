# Positive reciprocal-Taylor correction at arbitrary order

11 October 2026 UTC. Additive ordinary mathematics in active T20. No protected changes, integration, T21, formal-kernel verification, psychological improvement, or closure claim.

## Ownership and consequential increment

The first-order positive rational particle repair is inherited from `gradient-discretization-fidelity-20261010/RESULT.md`, independently reviewed in `gradient-discretization-independent-review-20261010/REVIEW.md`. The audit interpretation is already accepted in `authorial-synthesis-root-review-20261011/ASSESSMENT.md`: rational factors are inherited; exact audit covariance requires invariant potentials and step selection. `audit-tail-positive-repair-20261011/RESULT.md` and its independent review distinguish genuine laws, tail certificates, and effective moment names.

The new external lead is the conversation message private-message:52c58ed4c5c81ae1b365, recorded in `synthesis-successor-check-20261011/evidence.json`. It reports second-order construction and bounded-update determinacy, but supplies no accessible R3 proof/code artifact. Therefore neither result is imported as verified or claimed here as an uncontested discovery. Reciprocal Taylor approximation ([0/m] Padé in the scalar variable), positive tilting and covariance descent are classical mechanisms. The project increment is the explicit arbitrary-order full-law theorem, sharp separation of local and terminal-time assumptions, arbitrary-law endpoint estimate, and its audit/moment boundaries. Targeted predecessors were read; no whole-corpus or historical-priority claim is made.

Parent `positive-high-order-root-20261011/DERIVATION.md` was supplied as collaborative input: it independently proposed the local Taylor bound, normalization mixture argument, finite-moment global estimate and domination determinacy proof. The statements below were derived and checked here; this is author work, not independent review.

The continuous target is normalized exponential tilting with fixed V. When its derivative is defined (in particular with finite initial first loss moment, or at any positive time), it satisfies the centered replicator equation dμ_t/dt=−(V−E_(μ_t)V)μ_t. Finite initial first loss moment suffices for this L1/total-variation derivative. Its classical Fisher–Rao tangent norm squared is Var_(μ_t)(V), so a finite tangent norm at t=0 additionally requires finite variance; at every positive time exponential damping supplies all loss moments. Subject to that geometric qualification, this is the fixed linear-energy Fisher–Rao flow in the unit-rate convention. The method does not purport to integrate an arbitrary Riemannian gradient flow. Scalar positivity on nonnegative arguments is not a general A-stability assertion.

## 1. Full-law definition and all-step structure

Let (X,A,μ) be a probability space, V:X→[0,∞) measurable and finite μ-almost everywhere, m≥1 integer, and h≥0 finite. Put

P_m(z)=sum_{j=0}^m z^j/j!, a_h(x)=1/P_m(hV(x)), Z_h=∫a_h dμ,
T_h μ=a_h μ/Z_h, S_h μ=e^(−hV)μ/B_h, B_h=∫e^(−hV)dμ.

Then 0<a_h≤1 almost everywhere, hence 0<Z_h≤1. Thus T_h is a genuine probability equivalent to μ, including at h=0. There is no finite-support, bounded-loss, finite-energy or moment hypothesis for existence. Allowing V=+∞ needs a separate convention and positive mass on the finite-loss set; otherwise normalization can vanish. We exclude that extension here.

For h>0, a_h is strictly decreasing in V. If ∫Vdμ<∞,

E_(T_h μ)V−E_μV = Cov_μ(V,a_h)/Z_h
= (1/(2Z_h))∫∫(V(x)−V(y))(a_h(x)−a_h(y))dμ(x)dμ(y) ≤0.

The double integral is integrable since a_h≤1. Equality holds exactly when V is μ-almost surely constant. Without a finite initial mean, the new mean is still finite: V/P_m(hV)≤1/h gives E_(T_h μ)V≤1/(hZ_h). Thus the extended-real comparison still holds, although subtracting the two energies is illegitimate. More generally E_(T_h μ)V^k≤k!/(h^k Z_h) for integers 1≤k≤m. These are loss moments, not arbitrary coordinate moments.

For a fixed audit likelihood L≥0 with 0<∫L dμ<∞, define B_L μ=Lμ/∫L dμ. Since a_h>0 and ≤1, the common joint normalizer ∫La_h dμ is finite positive. Multiplication of the same two factors proves exactly

B_L(T_h μ)=T_h(B_L μ).

Boundedness or strict positivity of L is unnecessary; an unbounded integrable audit and audits deleting support are allowed. The loss, m, h and any baseline must be the same on both paths. If L has infinite integral, B_L μ is not defined even if B_L(T_h μ) exists; no square is asserted. Zero likelihood deletion is not reversible evidence withdrawal without separately retained data.

## 2. Exact local order and its assumptions

Write r_m(z)=1/P_m(z)−e^(−z). Taylor's integral remainder gives for z≥0

0≤e^z−P_m(z)≤e^z z^(m+1)/(m+1)!,
0≤r_m(z)≤z^(m+1)/[(m+1)! P_m(z)]≤z^(m+1)/(m+1)!.

Also r_m(z)/z^(m+1)→1/(m+1)! at zero. If A≥B>0 are integrals of two ordered densities a≥b≥0, the normalized a-law is the mixture (B/A) times the b-law plus (A−B)/A times the normalized remainder law. Consequently TV≤(A−B)/A≤(A−B)/B. TV uses one half the L1 norm.

If E_μ V^(m+1)<∞, these facts yield

TV(T_h μ,S_h μ)≤h^(m+1) E V^(m+1)/[(m+1)!B_h].

This is order-m consistency: one-step local error O(h^(m+1)), for this fixed law and loss. More precisely in L1(μ),

h^(−m−1)[a_h/Z_h−e^(−hV)/B_h]
→[V^(m+1)−E V^(m+1)]/(m+1)!.

To prove it, dominated convergence gives r_m(hV)/h^(m+1)→V^(m+1)/(m+1)! in L1; Z_h,B_h→1; then use a_h/Z_h−b_h/B_h=r_h/Z_h−b_h(Z_h−B_h)/(Z_hB_h). Thus the order is generally exactly m, with the explicit nonzero leading TV coefficient unless V is constant.

Finite support with finite losses, and bounded V on arbitrary laws, satisfy these assumptions automatically. For unbounded V, finite mth moment alone gives only o(h^m) in TV: r_m(z)/z^m is bounded and tends to zero at zero. It need not give O(h^(m+1)). More generally kth finite loss moment gives k right derivatives at zero in L1 for each normalized family, since their kth scalar derivatives are bounded on [0,∞) and dominated by a constant times V^k; through k≤m those derivatives agree. No two-sided neighborhood is asserted for unbounded losses. At h>0 derivative ratios are bounded locally in h (rational weights), so bounded-observable expectations are smooth even without initial loss moments. Unbounded observables need their own integrability.

For a polynomial or other test Q, TV is insufficient. One convenient sufficient condition for local O(h^(m+1)) of expectations is E|Q|<∞ and E[|Q|V^(m+1)]<∞, together with E V^(m+1)<∞. Direct numerator/denominator subtraction proves the bound

|E_T Q−E_S Q|≤h^(m+1)/[(m+1)!Z_h] {E[|Q|V^(m+1)]+(E|Q|/B_h)E V^(m+1)}.

Fixed finite moment summaries do not compute these nonlinear expectations exactly in general.

## 3. Repeated fixed-loss steps: two different global conclusions

The same V and h at every step give T_h^n μ proportional to P_m(hV)^(−n)μ. Normalizers at intermediate steps cancel. It is not an exact semigroup: ordinarily T_h^2≠T_(2h).

If E V^(m+1)<∞, 0≤a^n−b^n≤n(a−b) for a=1/P_m(hV), b=e^(−hV). For nh≤T,

TV(T_h^n μ,S_(nh) μ)≤T h^m E V^(m+1)/[(m+1)!B_T].

This is a uniform mesh-time global order-m bound, including the initial layer, under the stated moment condition. B_T>0 is retained, not treated as a universal constant. The same proof with mixed Q-moments supplies observable bounds. It makes no claim about moving particles, time-dependent potentials, splitting errors or adaptive steps.

A stronger terminal-time theorem needs no loss moments. Put q=m+1. The sharper remainder above gives

a(z)^n−e^(−nz)≤n r_m(z)a(z)^(n−1)≤n z^q/[q!P_m(z)^n]≤n z^q/[q!(1+z)^n].

For n>q, differentiation or weighted algebra gives

sup_(z≥0) z^q/(1+z)^n=(q/n)^q(1−q/n)^(n−q)≤(q/n)^q.

At any fixed t>0 choose h=t/n. Integrating the uniform bound and normalizing gives, for every supplied probability with V finite almost surely,

TV(T_(t/n)^n μ,S_t μ)≤q^q/[q! B_t n^m].

Thus fixed-terminal-time global order m survives even for infinite-energy laws. Constants are not uniform over all initial laws or unbounded final times. With fixed h and all grid times starting at zero, n is small in the initial layer; this theorem does not replace the finite-moment uniform mesh estimate. On a delayed interval τ≤nh≤T it gives ≤q^q h^m/[q!B_T τ^m] once n>q. This is a distinct useful arbitrary-law conclusion, not a consequence of local order at h=0.

The endpoint order is generically sharp, even without initial moments. This strengthening was proposed during independent review and then checked by the participating author and parent; its discovery is collaborative, not independent corroboration of its own proof. For q=m+1, log P_m(z)=z−z^q/q!+O(z^(q+1)) near zero. Consequently, at each finite V,

n^m[P_m(tV/n)^(−n)−e^(−tV)]→e^(−tV)(tV)^q/q!.

The uniform scalar majorant already proved bounds the left side by C_m for all n>q, so dominated convergence applies for any probability μ. The same normalization subtraction as in §2 gives convergence in L1(μ) of the normalized signed density error to

(e^(−tV)/B_t) t^q [V^q−E_(S_t μ)V^q]/q!.

Therefore

lim_(n→∞) n^m TV(T_(t/n)^n μ,S_t μ)
= t^q E_(S_t μ)|V^q−E_(S_t μ)V^q|/(2q!).

At t>0 this coefficient is finite and strictly positive exactly when V is not μ-almost surely constant; S_t is equivalent to μ. This proves sharp generic order m rather than merely an upper estimate, while allowing infinite initial energy.

For the algorithm that recomputes every terminal t with exactly n steps t/n, the endpoint bound is uniform over 0≤t≤T after replacing B_t by B_T (t=0 has zero error). This is different from a single fixed-h trajectory with only k steps at its kth grid time.

The terminal estimate also improves observable assumptions. Write C_m=(m+1)^(m+1)/(m+1)!. For any Q with E|Q|<∞, the pointwise density error bound gives

|E_(T_(t/n)^n μ)Q−E_(S_t μ)Q|≤C_m n^(−m)[E|Q|+|E_(S_t μ)Q|]/B_t.

There is no mixed V-moment requirement here. Even some initially nonintegrable observables are covered: let Q=V^s with real s≥0 and t>0, put r=m+1+s, and take integer n>r. Multiplying the density error by V^s=(nz/t)^s and maximizing z^r/(1+z)^n gives

∫V^s[a_(t/n)^n−e^(−tV)]dμ≤r^r/[t^s(m+1)!n^m].

The exact tilted mean M_s(t)=E_(S_t μ)V^s is finite since x^s e^(−tx) is bounded (for s=0 use 1). The normalized expectation error is therefore bounded by

n^(−m)[r^r/(t^s(m+1)!)+C_m M_s(t)]/B_t.

This also proves finiteness of the approximating loss-power expectation at those n. The bound extends to state observables with |Q|≤D(1+V^s), with the corresponding constant. Arbitrary polynomial state observables need not be controlled by V, so no general tensor-observable conclusion follows without such growth or integrability assumptions. These endpoint refinements were proposed by the participating parent and checked algebraically here.

An explicit tensor-relevant corollary is available when the loss actually controls coordinates. After n steps at h>0, every loss moment through degree mn is finite: P_m(hV)^n≥(hV)^(mn)/(m!)^n, and V^k≤1+V^(mn) for 0≤k≤mn. For V=||x||² this makes all absolute state monomials of total degree at most 2mn integrable. The exact positive-time exponential tilt has all polynomial state moments. For any fixed polynomial Q of degree k, |Q|≤D(1+V^ceil(k/2)), so the endpoint observable theorem supplies order m once n is sufficiently large, even from an arbitrary supplied initial law. This is a full-law regularization/approximation statement; it is not an algorithm starting only from missing or divergent initial tensor summaries, or a claim that old tensor values are preserved.

## 4. Countermodels and nontransfers

### Heavy-tail local failure despite m finite moments

Let μ=(1/2)δ_0+(1/2)Pareto(α) on [1,∞), with V(x)=x and m<α<m+1. Then E V^m<∞ and E V^(m+1)=∞. The normalizer difference is

Z_h−B_h=(α/2)h^α ∫_h^∞ r_m(z)z^(−α−1) dz.

The last integral tends to a finite strictly positive constant: near zero the integrand is O(z^(m−α)); at infinity r_m≤1 suffices, and positivity is strict. At the atom zero the two normalized masses differ by (Z_h−B_h)/(2Z_hB_h). Therefore TV is bounded below by a positive multiple of h^α, disproving O(h^(m+1)). In particular a uniform O(h^m) mesh-time result can fail for α<m; the same example and argument apply with 0<α<m. The arbitrary-law fixed-terminal-time theorem remains true.

### Centering, auditing and transport

For finite losses a common fixed lower baseline b≤inf V permits replacing V by V−b≥0. This is still order m for the same exponential tilting, since exponentials remove common constants exactly. The rational map itself is not exactly invariant under changing that baseline while holding V fixed. There is a qualified exact gauge convention: if the ambient state space is fixed independently of μ and its audits and the finite value b=inf_(ambient X)V is supplied, then using V−b is exactly invariant under simultaneous additive shifts V→V+c, b→b+c, and retains fixed-audit commutation. Existence of an ambient infimum does not supply an effective procedure for computing it. A supplied baseline convention transforming in this way is enough; no impossibility for all rational implementations is asserted. This external convention differs from recomputing the infimum on the current support. If a baseline is recomputed from audited weights, commutation can fail. Even a support minimum can change after a zero-likelihood audit: use uniform weights on V=(0,1,2), L=(0,1,1), h=1, m=2. Correct then audit with baseline 0 gives surviving ratio 1/P_2(1):1/P_2(2)=2:1; audit then recenter at minimum 1 gives ratio 1:1/P_2(1)=5:2. Both are positive, normalized and descend in their respective frozen losses, but differ. Positive audits preserve support minima, yet weight-dependent baselines or step sizes can still fail. Mean-centering may also make losses negative, destroying unconditional positivity for odd m.

Audit-dependent losses are different correction operators, so multiplication of a fixed factor proves nothing about them. A weight-independent moving-position step may preserve an audit contract on retained labels but is not made order m by an order-m selection substep. A single Dirac undergoing Euler x→(1−h)x for x'=−x is a counterexample: selection has no effect; position local error remains O(h²) even with m>1. Predetermined time-varying scalar potentials still give diagonal multiplicative factors and commute with a fixed audit when both paths use exactly the same sequence; they require a new quadrature/composition argument for any order claim. Coupled or state-dependent loss is not covered. Energy descent alone is not psychological, epistemic or empirical improvement, nor a certificate of source warrant.

### Finite moments, determinacy and tails

For a measure on R^d having all absolute polynomial moments and being moment-determinate, every probability ν≤Cμ is moment-determinate. Indeed if ν' shares all ν moments, then ρ=μ−ν/C+ν'/C is a positive probability sharing all μ moments. Determinacy gives ρ=μ and therefore ν'=ν. Apply this with ν=T_h μ and C=1/Z_h. Bounded likelihood audits preserve this premise; unbounded audits need a separate dominance or determinacy argument. This overlaps the unverified external bounded-update claim; the proof here is available but no novelty is claimed.

For a moment-indeterminate μ, domination alone proves no determinacy; V constant gives T_h μ=μ. Polynomial rational damping does not generally create exponential coordinate tails or all moments. For V=x on the Pareto example, corrected density behaves as x^(−α−m−1), so only polynomial moments of degree k<α+m are finite and every positive exponential moment still diverges. All moments of V are not automatically created by one step. Determinacy is not an effective reconstruction algorithm or a computable moment name.

Nor does determinacy from the entire infinite sequence make a finite summary sufficient. Example m=2,h=1,V=x: μ=(δ_0+δ_2)/2 and ν=δ_1 have equal mass and mean, but corrected means are 1/3 and 1. More generally for any finite degree K, the nonpolynomial continuous function 1/P_m(x) on a compact interval is outside the span of 1,x,...,x^K. Choose K+2 nodes on which its interpolation residual is nonzero; the signed Vandermonde null vector annihilates these moments but not the rational function. Its positive and negative parts have equal nonzero mass and normalize to two compactly supported, hence determinate, probability laws with identical first K moments and different correction normalizers. Thus a finite moment summary cannot in general supply the exact nonlinear update/normalizer. A sufficient special finite-atomic reconstruction contract is a separate premise.

## Evidence and execution scope

`check.py` provides exact rational structural/counterexample controls, symbolic local series controls, rational endpoint-majorant controls and high-precision convergence diagnostics. Finite tests supplement the measure-theoretic proofs, not establish them. `CHECKS.json` records actual execution; optimized execution is separate. No R3 implementation, production floating-point solver, formal kernel or external integration is claimed.
