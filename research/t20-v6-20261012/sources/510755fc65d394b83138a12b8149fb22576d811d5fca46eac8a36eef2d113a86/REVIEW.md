# Independent review: asymptotic Gibbs transport

10 October 2026 UTC. Ordinary mathematical review by a separate participating reviewer. No audit-governor envelope, formal-kernel verification, external peer review, protected integration, or programme closure is claimed.

## Verdict and exact review scope

**Accepted as scoped, without an outstanding correction.** The final source explicitly defines concentration as full mass on the stated Borel set, assigns infinite objective outside the absolute-continuity domain, and handles conditional quantities only almost everywhere. The author adopted the reviewer’s domain-notation clarification before freezing. A direct diff confirmed that this was the only successor change; no hypothesis, identity, or mathematical conclusion changed.

Reviewed source files are in `../asymptotic-gibbs-transport-20261010/`:

- `AUTHOR_MANIFEST.json`: `1e8b0c4553d9f81944ec717ceb33bbbd9a1c6ed7b75f7901ecb30e1a0d7c5f6d`.
- `RESULT.md`: `251d825754c3bcdc7611bf8e133759a87e9b763a1d90d3c3700d64e930b897e5`.
- `check_exact.py`: `6344132a4bfee6b40ffd70d0d0010c1643515f9fe13790ea499c04ca95c90436`.
- `INPUT_BINDING.json`: `c79d35a12221458f75966dda8221404b5e176592aaf6654f512bb344db3bc928`.

The accepted ancestor is `../nonconvex-atomic-limit-classification-20261010/RESULT.md`, SHA-256 `fd5e814ce2766f3283b0472b04e6c00234654ff46df5cbebb324fa1c9668789d`. Its input binding was verified. Its convergence theorem is inherited, rather than independently re-proved or newly credited to this supplement. No ancestor or source file was modified by this reviewer. Source snapshots and the author replay output are in this review directory.

## Measure-theoretic and variational review

### 1. Initial-coordinate objective and arbitrary laws

The inherited theorem supplies Borel maps q and I, with 0≤I<∞ pointwise, and a Borel selected basin S with μ(S)>0. Thus A=∫_S e^(−I)dμ is strictly positive and at most one without any assumption on ∫I dμ. The density of π* is strictly positive on S, so π* is equivalent to the restricted measure μ|S. Every admissible π is therefore absolutely continuous with respect to π*.

For finite J, both KL(π||μ) and ∫I dπ are finite. If f=dπ/dμ, then ∫(f log f)^−dμ≤1/e, since μ is a probability. Hence finite KL makes log f absolutely integrable under π. Adding I and the finite constant log A makes the logarithmic density identity integrable, establishing J(π)=KL(π||π*)−log A without an infinity-minus-infinity operation. Entropy nonnegativity and its equality criterion give the claimed lower bound and uniqueness on the finite domain.

The candidate belongs to that finite domain: ∫I dπ*≤1/(eA), and |log(dπ*/dμ)|≤I+|log A| holds π*-almost surely. Its entropy and transient cost are finite separately. Competitors assigned J=+∞ cannot improve the finite value −log A. This justifies the extended-value minimization, rather than merely a stationarity calculation.

Combining this identity with the accepted ensemble identity is legitimate even when E(0)=∞. No exchange of an unbounded initial energy integral and a limit is performed in the new argument. The ancestor owns the improper-time-integral justification.

### 2. Endpoint measure and null sets

Let λ=q_#(e^(−I)μ). Then λ and ν=q_#μ have the same null sets: a positive μ-almost-everywhere density gives λ(B)>0 whenever ν(B)>0. Consequently r=dλ/dν satisfies 0<r≤1 ν-almost everywhere. This proves positivity even when conditional endpoint means of I are infinite.

Since S=q^(−1)(C), pushing the weighted restriction forward gives q_#(1_S e^(−I)μ)=1_C rν. Thus the claimed endpoint law and A=∫_C r dν are exact for nonatomic laws and many-to-one q alike. Conditional expectation does not require positive mass at individual endpoints. Choosing or changing a representative on a ν-null set has no effect on any absolutely continuous candidate or on ρ*.

The final source explicitly assigns endpoint objective +∞ when ρ is not absolutely continuous with respect to ν or when ρ(C)≠1, and allows any finite nonnegative measurable extension of −log r to the exceptional ν-null set. This prevents an unspecified integral of a ν-a.e.-defined function against a singular candidate. The same entropy proof applies directly, since u e^(−u)≤1/e also controls J_eff under the endpoint optimizer.

The final source explicitly uses π(S)=1 instead of ambiguous support language. Containment of the closed topological support in S would be a stronger and unintended requirement because a selected basin need not be closed. The endpoint constraint similarly reads ρ(C)=1.

### 3. Conditional Jensen and equality

On a regular conditional law μ_y, exp(−u) is strictly convex. For finite m(y)=∫I dμ_y, Jensen gives r(y)≥exp(−m(y)), equivalently J_eff(y)≤m(y), with equality exactly when I is μ_y-almost surely constant. If m(y)=∞, the inequality remains valid while equality is impossible because J_eff(y)<∞ ν-almost everywhere. All fibre claims are understood for ν-almost every endpoint, or for ν restricted to C when discussing only the selected endpoints.

The arithmetic conditional mean is not interchangeable with the effective cost. In particular, the endpoint prior remains ν, not a distribution already tilted within each fibre. The report uses the correct reference throughout.

### 4. What is preserved

The normalizing constant, pushed-forward optimizer, and variational optimum are preserved. Initial-coordinate relative entropy and average transient cost need not individually equal their endpoint counterparts. The independent controls verify the ordinary entropy chain rule and the fibre-level identity

    KL(tilted conditional law || original conditional law)
       + tilted conditional mean of I = J_eff.

Thus information lost by endpoint merging is not silently treated as recoverable, and “exact transport” is used for the specified Gibbs structure rather than as a claim that q is injective or information-preserving.

## Genuine dynamic counterexample

For F(x)=(x²−1)²/4, the exact particle from 2 is

    X(t)=2/sqrt(4−3 exp(−2t)).

Independent symbolic checks verify its initial condition, gradient-flow equation X'=X(1−X²), and limit 1. The particles −1 and 1 are stationary. The primitive H(x)=(x²−1−log(x²))/8 satisfies H'(x)X'=−F(x), and integrating F along the particle from 2 gives I_2=(3−log 4)/8>0. Hence a=exp(−I_2) lies strictly between zero and one. This verifies the realized dynamical cost rather than merely assuming the source's assigned factor a.

The exact endpoint probability is (1+a)/(2+a); the arithmetic-mean replacement gives 2sqrt(a)/(1+2sqrt(a)). Their positive cross-multiplied difference is (1−sqrt(a))². This is strictly positive for the actual a, not just a formal polynomial identity with an unconstrained parameter. The reported direction of the bias is correct in this example.

A further genuine fourth initial particle at zero has stationary energy 1/4 and is excluded from S. Controls for the resulting four-point initial probability verify the finite-J identity and optimum with the full initial probability as entropy reference, including the support-selection cost.

## Source-compatible infinite-mean stress test

Take the accepted quadratic F(x)=x²/2 and initial points x_n=2sqrt(n log 2), n≥1, with masses μ_n=1/[n(n+1)]. Then μ is a probability, q(x_n)=0, and the exact particle integral is I(x_n)=n log 2. Its unweighted mean cost is infinite:

    Σ μ_n I_n = log 2 · Σ 1/(n+1) = +∞.

Its exponential conditional mean, however, is

    r(0)=Σ 2^(−n)/[n(n+1)] = 1−log 2 ∈(0,1).

The selected mean is finite:

    ∫I dπ* = log 2 · (2log 2−1)/(1−log 2).

The effective endpoint cost is the finite number −log(1−log 2), whereas the arithmetic conditional cost is infinite. All endpoints coincide, so the endpoint relative entropy is zero. The initial entropy plus the selected transient mean nevertheless gives the same finite optimum. This is a genuine coercive-polynomial realization of the report's arbitrary-law and infinite-conditional-mean clauses; it also has infinite initial expected energy. Exact series controls verify the displayed formulas. The universal proof still rests on the written measure argument, not on this example.

## Script audit and executed evidence

The unmodified author checker was replayed from the snapshot, writing its output only within this independent review. It passed.

Its count is accurate as a count of executed assertions:

- One ancestor-hash assertion at line 7.
- Seven symbolic assertions at lines 12, 16, 17, 20, 24, 28, and 29.

There are five distinct algebraic identity families among those seven assertions: lines 17 and 28 repeat the grouped partition-function identity, while lines 16 and 29 repeat the positive endpoint mass through equivalent expressions. The report does not claim seven independent theorem proofs. The source checker alone does not check the actual double-well trajectory, its actual I_2, or the strict parameter range; the independent controls above supply those checks.

`check_independent.py` passed 41 checks: 29 exact mathematical controls, four current-source hashes, four snapshot hashes, one ancestor hash, two replay checks, and one count audit. `INDEPENDENT_CHECKS.json` names each executed check; `AUTHOR_REPLAY.log` records the source replay. These are symbolic/control checks, not a general-purpose proof assistant or a proof of all measure-theoretic statements.

Replay from this workspace:

    python asymptotic-gibbs-transport-independent-review-20261010/check_independent.py

The source's ancestor locator is absolute. `PORTABLE_REPLAY.md` gives an explicit fresh-working-copy relocation recipe that verifies archived original bytes first and leaves them untouched. This limitation concerns replay location, not the mathematical theorem.

## Credit, interpretation, and remaining scope

The source clearly attributes convergence and the arbitrary-law asymptotic identity to the accepted ancestor, and the entropy identity and conditional expectation to standard mathematics. Its contribution is their exact dynamic composition and correct endpoint cost, with a physically realized counterexample to arithmetic cost averaging. It supplies no Bayesian data-generating model, no identification of F with epistemic warrant, no claim of globally minimizing F, no numerical computability theorem for q or I, and no empirical or metaphysical noetic identification. The stated boundaries are adequate.

The review has no authority to integrate protected material or close T20. Its acceptance is confined to the exact source hashes and the conventions stated above.
