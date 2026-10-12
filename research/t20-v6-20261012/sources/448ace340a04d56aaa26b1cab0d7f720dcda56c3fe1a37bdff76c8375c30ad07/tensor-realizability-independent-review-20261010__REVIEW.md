# Independent review: full tensor moment dynamics

10 October 2026 UTC. Ordinary mathematical review of the additive continuation, not formal-kernel certification, empirical evidence, protected integration, or a closure decision.

## 1. Verdict and bound candidate

**PASS for the stated finite-dimensional, full commutative-polynomial interface. No substantive proof gap was found.** The main distinctions are correct:

- Lower-bounded polynomial damping and all-time representability force a fixed initial-law tilt representation, but do not always identify that law uniquely.
- Coercivity identifies the full vector law and gives the initial-moment-fibre/path bijection.
- For quadratic damping, all-time positivity on every polynomial square supplies positive-time moment growth and therefore representability. Neither initial representation nor initial Carleman growth is assumed.
- Polynomial automorphism and certified sum-of-squares extensions have the premises needed for the same conclusion.
- The effective consequence is a conditional negative-square semidecision, not total validity testing or effective measure reconstruction.

The reviewed final candidate is `tensor-realizability-extension-20261010/RESULT.md`, SHA-256:

    449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a

A byte-identical copy is retained in `author-snapshot/RESULT.md`. The final revision differed from the first completely reviewed snapshot only by explicitly recording the subsequently replayed 332-control count. The author checker hash is:

    159f8c8c3994c67a9d1211e0b9211652eca6c4be28f7f6c3d2c13f51696b2a95

This reviewer was given the candidate's proposed route and independently reconstructed its key steps before receiving the stable draft. The reviewer then read the whole draft, coordinated a precise attribution correction, and ran separate controls. This is not a blind or formally mechanized review.

## 2. Analytic exhaustion audit

### Lower bound and the unnormalization

Replacing h by h minus any finite lower bound leaves both the normalized differential equation and normalized tilt unchanged. It is therefore legitimate to use h≥0 everywhere in the argument. The normalizer a(t)=exp(−∫L_v(h)dv) remains strictly positive on every compact time interval; no sign assumption on odd coordinate moments is used.

The identity A'_t(p)=−A_t(hp) is valid for each polynomial. Because multiplication by the fixed polynomial h maps polynomials to polynomials, simultaneous induction over polynomial observables supplies every finite derivative. This is a coordinatewise argument, not an assertion that an infinite-dimensional ODE is locally Lipschitz in some unspecified norm.

### Why the square weights are essential

For every real q, the quantities A_t(q²h^n) are nonnegative under representability. The backwards Taylor remainder is nonnegative as well. In particular,

    A_t(q²h^n) ≤ n! A_0(q²)/t^n.

This is the correct n!, because n counts applications of the damping polynomial h, rather than coordinate degree. For h=|x|² the coordinate degree rises by 2 at each derivative.

The displayed bound controls the derivative of A_t(q²) uniformly in a sufficiently small time neighborhood, for that fixed q. Taylor remainders go to zero there. Polarization then gives analyticity of A_t(p) for an arbitrary signed polynomial p. Treating signed mixed moments as a nonnegative scalar sequence would be invalid; the draft does not do that.

### Selection of one representative and analytic identity

The proof needs a representative at only one positive time s once the full joint cone inequalities are available. The positive exponential series gives integrability of q² exp(bh) for every b<s. This supplies an exponential margin around every strictly positive time u for the integral G_q(u)=∫q² exp((s−u)h)dλ_s.

All derivatives and the summed local Taylor series are justified with such a margin. Polynomial factors in h consume only a smaller part of the margin. The candidate compares the full derivative sequences at s, obtains local identity, and propagates it over the connected interval (0,T) using real analyticity. No measurable family of representing measures, finite-time Bernstein theorem, or unsupported global completely-monotone extension is required.

### Boundary recovery and signed moments

The zero-boundary passage is first made for q², where monotone convergence applies. Continuity at zero gives exactly ∫q² exp(sh)dλ_s=A_0(q²). The q=1 instance gives total mass one, so mass cannot disappear in the inverse tilt.

For the recovered μ, the estimate |p|≤(1+p²)/2 supplies absolute integrability of every polynomial. Polarization recovers all signed mixed moments, including at t=0. This resolves both the mass and signed-observable boundary issues without assuming a representing measure initially.

The converse is equally valid: every |p|h^n is integrable because μ has all absolute polynomial moments. Dominated convergence at zero uses the one-sided bound |(exp(−uh)−1)/u|≤h. Hence the recovered path extends globally under the lower-bound hypothesis.

## 3. Full-law determinacy and noncoercive ambiguity

### Static coercive lemma

The proof does not assume that coercive h controls the Euclidean norm at a linear or quadratic rate. That would be false for useful polynomial-automorphism examples.

Instead, equality of full polynomial moments first transfers the exponential h moment to a competing positive representative by monotone convergence. Cauchy–Schwarz then bounds |p|exp(rh) for every polynomial p and a sufficiently small positive r. The signed h-pushforward of p times the difference of the two measures has zero moments and an exponential absolute moment. Its Laplace transform therefore vanishes locally and then for all positive arguments.

The signed Laplace uniqueness argument is correct, including total mass: continuity at zero supplies it when only positive transform values were used. Pushing forward by exp(−u) identifies a finite signed measure on [0,1] from all polynomial integrals.

This yields equality of polynomial integrals after restriction to each sublevel {h≤R}. Those sublevels are compact under coercivity, and coordinate polynomials separate their points. Stone–Weierstrass identifies the restricted measures. Exhaustion by sublevels identifies the full vector measures. This is genuinely joint polynomial information; knowing only the scalar h law would not do this.

### Initial law and finite-horizon extension

If two initial laws give the same normalized path, the path fixes their common normalizer by its scalar first-order equation and unit initial value. Positive-time full-moment determinacy then identifies the tilted laws. Inverse tilting identifies the initial laws.

Without coercivity, the candidate correctly replaces a law bijection by the quotient relation

    h_*(pμ)=h_*(pν) for every polynomial p.

Equality of normalized finite-horizon paths fixes the normalizer, hence all weighted transforms on an open time interval. Analyticity propagates equality to every positive time, and signed Laplace uniqueness yields the stated equivalence. Thus global continuation of the moment path is unique even when its underlying law is not. This is not a claim that arbitrary time-indexed choices of representatives themselves form a single law-valued tilt trajectory.

The further correspondence between a path's initial-law lifts and its positive-time moment fibre is valid: every representative at s has exactly the same polynomial-square exponential bounds, so the boundary reconstruction works for any such representative. Normalized inverse tilt and forward tilt are mutually inverse. The distinction between uniqueness of a path and uniqueness of its law is therefore justified.

## 4. Quadratic square positivity and extensions

For h=|x|², every q²h^n is a sum of polynomial squares. Moreover h^n−x_i^(2n) has a multinomial sum-of-squares expansion. Full square positivity consequently gives

    0≤L_t(x_i^(2n))≤n!/[a(t)t^n],  t>0.

Each marginal Carleman term is bounded below by a fixed positive multiple of n^(−1/2). The series diverges. Vanishing even moments are correctly handled by the usual infinite-term convention. The imported multivariate representation theorem therefore applies to every positive-time full sequence. The boundary argument supplies initial representation afterwards.

The theorem is compatible with the inherited determinate-initial counterexample. That example imposes coordinate positivity, not positivity of every polynomial square. It also differs from the earlier scalar sufficient theorem, which starts with valid initial Stieltjes moments satisfying a growth condition. No contradiction or transfer of the wrong Carleman exponent is present.

### Sum-of-squares certificate

If, after a constant shift, h−c|x|² is a sum of squares with c>0, then h and h−cx_i² are sums of squares. Their product factorization gives that h^n−c^n x_i^(2n) is a sum of squares. The factorial bound therefore gives the required coordinate Carleman conditions, and pointwise h≥c|x|² gives coercivity. The draft does not extend this algebraic conclusion to every merely nonnegative or coercive polynomial.

### Polynomial inverse transport

For a polynomial bijection Φ with polynomial inverse Ψ, composition is an automorphism of the entire real polynomial algebra. Thus q↦q∘Φ preserves square positivity and finite-polynomial regularity. Conversely p∘Ψ remains polynomial, ensuring that the returned measure has every original x moment and reproduces every original observable.

This verifies full-vector transport, not just recovery of Φ(x) or h(x). The triangular example has compact sublevels but can grow more slowly than |x| along its curved valley. Ordinary marginal Carleman estimates in the original coordinates are not assumed for this transported case.

The dimension is explicitly finite. Infinitely many grades over a finite coordinate space are not an infinite collection of independent coordinates. The result concerns symmetric moments of a commutative observable algebra, not arbitrary ordered or noncommutative tensors.

## 5. Countercontrols and effective corollary

The noncoercive lognormal product control is valid and nontrivial: the observed first coordinate evolves, while an undamped coordinate retains two distinct laws with identical moments. This defeats universal underlying-law uniqueness without coercivity.

The signed-lognormal control is stronger than a same-energy sphere example. The two laws have identical full initial moments and identical scalar quadratic-energy distributions at every time. Nevertheless their tilted full moment records differ at every positive time by full-law determinacy and injectivity of positive damping. Their means need only disagree somewhere in each open interval; the draft correctly avoids claiming disagreement at every individual time.

The flat-function embedding solves the full quadratic hierarchy from the determinate δ_0 record, but has a negative fourth moment immediately. The exact rational-time certificate checked independently is

    L_(1/4)((x²)²)=−128/(2 exp(4)−1)<0

when ε=1/2. This demonstrates why square positivity cannot be omitted or inferred from initial validity.

The negative-geometric law under h(x)=x supplies the announced finite-time blow-up. Its probabilities sum to one, all initial moments are finite, and its partition function is 1/(2−exp(t)). Thus the universal global damping conclusion cannot simply drop the lower bound.

The semidecision corollary has sufficient effective hypotheses: known rational horizon (or infinity), promised exact quadratic hierarchy and regularity, and uniformly certified coordinate evaluation at rational times. Failure of representability somewhere implies failure of all-time square positivity by the theorem's contrapositive. Continuity in time and in the finitely many coefficients of the witness polynomial produces a rational-time rational-polynomial strict witness. Certified upper error bounds semidecide negativity, and dovetailing finds it.

This gives no witness-degree bound, detection-time bound, total validity decision, or general isolated-multisequence representability algorithm. It does not promise a negative square at a previously specified nonrepresentable time. The final wording retains those distinctions.

## 6. Source check and resolved correction

The two requested inherited results were read first. The full tensor ancestor was then read, followed by the complete candidate. Seven inherited source files are preserved under the candidate's input bindings and were independently compared with their current originals.

The inspected primary external source is [Putinar–Schmüdgen, Multivariate Determinateness](https://arxiv.org/pdf/0810.0840): §6, Theorem 25 and the subsequent Nussbaum attribution, printed p. 24; and §8, Theorem 31/Corollary 32, printed p. 31. The former supplies existence and uniqueness under full positive semidefiniteness and all coordinate Carleman conditions. The latter uses a **strictly determinate** base with determinate or compact fibres. These statements were read in parsed primary PDF text; this reviewer does not claim screenshot or downloaded-PDF hash verification.

The initial draft summarized the latter premise as a determinate base. This reviewer requested the precise strict-determinacy wording. It is corrected in the bound final candidate. The direct exponential-integrability/compact-sublevel proof was valid independently of this attribution correction.

Classical static determinacy inputs are credited. The dynamic application is assessed only relative to the inspected project ancestry, without a comprehensive literature novelty claim.

## 7. Executed evidence and preservation

- Fresh isolated replay of the author's checker: **332 exact checks passed**; `author-replay.log`.
- Independently authored checker: **147 exact checks passed**; `independent-checks.log` and `INDEPENDENT_RESULTS.json`.
- The independent controls include signed three-dimensional hierarchy identities, constant-shift cancellation, joint-square expansions, coordinate comparison, full mixed-observable coordinate inversion, scalarization collisions, exact Gaussian cancellation, and the rational negative-square certificate. Deliberately wrong grade-shift and inverse-tilt-sign alternatives are detected.
- All seven inherited originals match their copied bytes, declared sizes, and SHA-256 digests. In particular, the two principal inherited hashes remain:

    realizable-moment-dynamics-20261010/RESULT.md
    c5aeeeed56b5bf5edfa9b87570249f142e3d1be9c06218d8007013c66f5eb688

    determinate-initial-positivity-20261010/RESULT.md
    cafc520026c66f94442346ff308ed4e202d70e10be8963b8a24ad17bda4e1e0a

The candidate and inherited originals were not edited by this reviewer. The checker was replayed in the separate review snapshot so its generated output did not mutate the author's packet.

The finite controls supplement the universal ordinary proof review. Neither their count nor exact arithmetic certifies an infinite theorem, a formal kernel, an empirical model, actual source truth, noetic realization, or any metaphysical conclusion.
