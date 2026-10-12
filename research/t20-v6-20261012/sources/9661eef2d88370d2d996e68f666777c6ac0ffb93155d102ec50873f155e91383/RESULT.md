# Determinate moment names compute the law and its damped continuation

10 October 2026 UTC. Additive ordinary mathematical research within ACTIVE T20. No protected edit, canonical integration, new tranche, kernel certification, sampling programme, or closure claim. The parent and this investigator independently reached the compact-fibre route and jointly developed its interpretation; any later independent review is separate. No field-priority claim is made.

## 1. Result and exact input

**Theorem D.** A uniformly named sequence of finite nonnegative integer moments of a probability measure on [0,∞), together with the promise that its Stieltjes moment problem is determinate, uniformly computes that probability in the ordinary weak-measure representation. No positive exponential-moment bound or quantitative determinacy modulus need be supplied. From the same input one uniformly computes

    A_r(t) = ∫ x^r exp(−t x) dμ,   Z(t)=A_0(t),
    T_t μ = exp(−t x)μ/Z(t),       M_r(t)=A_r(t)/Z(t)

for every integer r≥0 and every named real t≥0, including t=0 without deciding whether t is zero. The output includes the weak tilted law and all its raw moments, hence the original raw mean.

A moment name is one oracle returning a rational within 2^(−k) of m_r on input (r,k). Validity includes m_0=1, finiteness of every moment, and existence of a probability with those moments. Determinate means uniqueness among Borel probabilities on this declared half-line, not among all real-line measures. The result is a Type-2 operation relative to these names; computable names give computable outputs. The promises are not tests performed by the algorithm. There is no decision of validity or determinacy, and no guarantee outside the promised class.

This strictly enlarges the inherited positive-exponential-tail domain for nonnegative tilts. It does not replace the stronger ancestor's signed interior continuation u>−a, nor its explicit geometric series budgets. It computes the unbounded trait law, not an ℓ¹ list of hidden indexed weights.

## 2. Effective compactness, made explicit

Put y=x/(1+x), identifying the one-point compactification of the half-line with [0,1]. Let P be the space of probabilities on [0,1], with Wasserstein distance W_1 for the usual bounded metric. Its ideal points are finite rational atomic probabilities on rational points.

Here is a direct effective compactness construction. For integers n,Q≥1, move all mass to the grid {j/n:0≤j≤n}, incurring W_1 error at most 1/n. Round down the first n grid weights to multiples of 1/Q and put the remaining weight at the last point. The total moved mass is less than n/Q, so the second W_1 error is less than n/Q. Enumerating all grid probabilities with denominator Q therefore produces a finite (1/n+n/Q)-net. Choose n,Q effectively to make this bound as small as needed. W_1 between ideal points is computable (on the line it is the integral of the absolute CDF difference, a finite rational sum).

For a finite family of open ideal balls, search finer nets until every net point lies in one of the balls with its certified net radius added to the distance still strictly below the ball radius. This is sound. If the balls really cover P, compactness supplies a positive margin and some net succeeds. Dovetail over finite subfamilies for an enumerated effectively open set. Thus P⊂U is semidecidable. This is upper compactness; it does not decide arbitrary closed-set membership or produce points of every nonempty closed subset.

For N≥1 define the continuous computable clipping map

    c_N(y)=min(y/(1−y),N) for y<1,   c_N(1)=N.

It is (1+N)^2-Lipschitz, and c_N^r is r N^(r−1)(1+N)^2-Lipschitz for r≥1. Consequently λ↦∫c_N^r dλ is uniformly computable on P, directly from W_1 names and these bounds.

## 3. The full moment fibre is effectively closed

There are two equivalent ways to supply the key missing effective information.

### 3.1 Compact envelope and uniform integrability

Compute rational B_r>m_r for r≥1, uniformly in r, using any sufficiently coarse moment approximation plus an error margin. Put

    K_B={λ∈P: ∫c_N^r dλ≤B_r for every r,N≥1}.

Each violated inequality is a computably enumerable open condition. Hence K_B is effectively closed in the effectively compact P and is effectively upper compact. The r=1 bounds give N λ({1})≤B_1 for every N, so λ({1})=0. Monotone convergence then identifies λ with a half-line probability satisfying ∫x^r dλ≤B_r.

Uniformly on this set, for r≥1,

    0≤∫x^r dλ−∫min(x,N)^r dλ
      ≤∫_{x>N}x^r dλ ≤ B_(r+1)/N.                         (1)

Thus every moment functional is computable and continuous on K_B, uniformly in r. The full equality fibre ∫x^r=m_r is effectively closed relative to K_B. This is why just calling unbounded moments continuous in the weak topology would have been wrong: the next-moment envelope supplies the missing uniform integrability.

### 3.2 An explicit ambient closed-fibre presentation

A useful presentation avoids any reliance on a relative-open-set extension. Define F_m⊂P by all the following continuous closed constraints, for r,N≥1:

    m_r−m_(r+1)/N ≤ ∫c_N(y)^r dλ ≤ m_r.                  (2)

Then F_m is **exactly** the compactified full moment fibre. Every genuine representing law satisfies (2), by (1) with its actual next moment. Conversely, the upper r=1 bounds exclude mass at y=1. For each r, the upper bounds and monotone convergence give ∫x^r≤m_r, while the lower bounds tend to m_r as N→∞. Therefore ∫x^r=m_r. Total mass is already one in P.

All failures of (2) are strict inequalities between computable reals and are semidecidable, uniformly from the moment oracle. Consequently P\F_m is effectively open and F_m is effectively upper compact. In particular, merely knowing the next moment is finite would not justify this step; its supplied numerical name is essential to these effective enclosures.

## 4. Singleton extraction is uniform on the promise

Determinacy and validity say F_m={λ_μ}. Given ε>0, enumerate finite rational atomic probability centers q and semidecide

    P ⊂ B_W1(q,ε) ∪ (P\F_m).                             (3)

This is exactly the assertion F_m⊂B_W1(q,ε). A center sufficiently close to λ_μ exists, so a search eventually succeeds. Every accepted center has the stated error. Every successful computation uses a finite subcover and hence only finitely many constraints, moment grades, precision queries and strict rational margins.

No determinacy modulus was assumed: termination of this search follows from the singleton promise. No finite-dimensional numerical optimization, unspecified dense enumeration inside F_m, or exact real-equality decision is hidden here. Off the promise, a requested search may fail to terminate or may give only a coarse common enclosure. This procedure is not a test that a fibre is a singleton.

To return to the usual weak law on [0,∞), use the bounded ground metric d_b(x,z)=min(1,|x−z|), whose Wasserstein metric metrizes ordinary weak convergence. Let H>m_1 be rational. For an ideal approximation q to λ_μ, output ν=(c_R)_*q, a finite rational atomic half-line law. The coupling which clips x at R and the Lipschitz bound on c_R give

    W_(d_b)(μ,ν) ≤ H/R+(1+R)^2 W_1(λ_μ,q).                (4)

Indeed the clipping error is at most μ((R,∞))≤m_1/R, and the second error is bounded even in ordinary W_1 on the clipped interval. Select R and then the accuracy of q to make both terms small. Atom mass at y=1 in an approximate q causes no problem: c_R sends it to the finite point R. This explicitly verifies the output representation rather than declaring the inverse compactification computable at its singular endpoint. In fact the same construction computes the stronger ordinary W_1 name: with a rational H_2>m_2, the clipping error E|X−min(X,R)| is at most E[X 1_(X>R)]≤H_2/R. Replace H/R by H_2/R in (4), and the whole bound holds for ordinary W_1. This additional observation was supplied by the parent; it still does not compute indexed ℓ¹ masses.

## 5. Uniform damped computation, including the boundary zero

Given a named t≥0, obtain a positive rational U>t. No equality or strict positivity test for t is needed. For R≥1 define

    h_(r,R,t)(y)=c_R(y)^r exp(−t c_R(y)).

For r≥1 its y-Lipschitz constant is at most

    [r R^(r−1)+U R^r](1+R)^2,                             (5)

and its bound is R^r. For r=0, the corresponding constant is U(1+R)^2 and its bound is one. Evaluation and integration of these functions against λ_μ are computable jointly in t and r. The scalar exponential can be evaluated to arbitrary precision on the known compact range. Approximate values of t may first be clipped into [0,U], a computable operation. Their error contributes at most R^(r+1)|Δt|, also for r=0.

For r≥1 the discrepancy from A_r(t) is supported on x>R and is bounded by

    |A_r(t)−∫h_(r,R,t)dλ_μ| ≤ 2m_(r+1)/R.                (6)

Both x^r exp(−tx) and R^r exp(−tR) are bounded by x^r there; integrate and apply the next-moment bound. For r=0 the error is at most m_1/R because both exponentials are in [0,1]. Choose R from a rational upper bound on the relevant moment; use (5) to select the required W_1 accuracy; budget scalar evaluation separately. This is a terminating algorithm at t=0 as well as at positive t. At zero the correct answers are the supplied moments, but branching on that equality is neither used nor needed.

Jensen gives a common positive lower bound on a finite parameter interval:

    Z(t)≥exp(−t m_1)≥exp(−UH)>0,   0≤t≤U.                 (7)

Find a rational D strictly below exp(−UH). Division then computes M_r(t). For example, if z≥D, |a|≤K and approximations to a,z have errors ≤η<D/2, the quotient error is at most 2η/D+2Kη/D². Here K may be any rational upper bound on m_r. The r=0 numerator equals its denominator and M_0=1.

The tilted weak law is computable too. For any bounded d_b-Lipschitz test f, the product f(x)exp(−tx) is bounded computable with an explicit Lipschitz constant from t and the test bounds; integrate against the computed μ and divide by Z(t). Equivalently use clipping as above, with a probability-tail error divided by D, to output finite atomic weak approximations. None of this computes an arbitrary integrable unbounded observable without an effective tail bound.

### Effective continuity and derivatives

For s,t≥0, the mean value estimate on exp(−tx) gives

    |A_r(t)−A_r(s)|≤m_(r+1)|t−s|.                        (8)

On [0,U], normalized moments therefore have a computable Lipschitz bound

    |M_r(t)−M_r(s)|
      ≤[m_(r+1)/D + m_r m_1/D²]|t−s|.                   (9)

Rational upper bounds may replace each moment. Thus the outputs can be presented as computable continuous functions on any supplied compact nonnegative parameter interval, not merely isolated evaluations. Their one-sided derivatives at zero and interior derivatives satisfy A_r^(k)=(-1)^k A_(r+k); quotient differentiation computes every finite derivative of M_r from finitely many such values. This is effective C∞ data in the declared one-sided sense, without analyticity at zero.

For a computable finite piecewise-constant nonnegative control, insert its computable cumulative t=∫g. The same law/mean continuation as the inherited interface is recovered. All statements remain about finite cumulative values.

## 6. A genuine enlargement: determinate with no positive exponential tail

Consider the probability density

    f(x)=(1/2)exp(−sqrt(x)),  x≥0.

Substitution z=sqrt(x) gives density z exp(−z)dz and

    m_r=(2r+1)!,   r≥0.                                  (10)

These moments are uniformly computable. For every a>0, the integral of exp(ax) diverges: after substitution its integrand is z exp(az²−z), which does not tend to zero.

For a direct determinacy proof, let any competing half-line probability have moments (10), and lift it to a symmetric real-line law Y with Y²=X. Its even moments are (2r+1)! and odd moments vanish. For 0<b<1, monotone convergence yields

    E cosh(bY)=Σ_(r≥0)(2r+1)b^(2r)=(1+b²)/(1−b²)².

Since exp(b|Y|)≤2cosh(bY), all competing symmetric lifts have a positive exponential absolute moment and the same moments. Their characteristic functions are analytic in a common strip and agree near zero by their absolutely convergent moment expansions. The identity theorem and characteristic-function uniqueness give equal lifts, and squaring gives equal original laws. This is the classical exponential-determinacy mechanism, applied after a symmetric square-root lift; equivalently this is a Stieltjes-Carleman example.

The Laplace Taylor coefficients at zero have magnitude (2r+1)!/r!. At any nonzero argument their successive term ratio is

    |t|(2r+3)(2r+2)/(r+1),

which diverges. Its radius is zero. Theorem D therefore computes a determinate continuation where an origin Taylor summation algorithm fails and no input of the previous positive-exponential theorem exists. This is a concrete distinction between computability under a uniqueness promise and analyticity.

## 7. Calibrated Fisher-jet corollary

In the fixed inherited affine parameter t, set F(t)=log Z(t), q(t)=−F′(t), and V(t)=F″(t)=Var_(T_tμ)(X). Suppose instead the input gives q(0), the uniformly computable full one-sided jet V^(k)(0), and the promise that these arise from a half-line law with all moments finite and determinate. Then these data compute the full moment name and Theorem D applies.

Indeed the cumulants satisfy κ_1=q(0) and κ_n=(-1)^n V^(n−2)(0) for n≥2. Recover moments by the finite Bell recurrence

    m_0=1,
    m_(n+1)=Σ_(j=0)^n binom(n,j) κ_(j+1) m_(n−j).         (11)

Every requested grade requires finitely many named jet entries and computable arithmetic. These are formal derivative identities at zero, justified by finite-order differentiation, not a claim that a cumulant generating function converges there. Once moments are recovered, compute q,V,F and the same-reference Bregman/KL quantities at named nonnegative parameters by the preceding algorithms and their elementary identities.

This answers only the calibrated positive counterpart to the inherited Fisher endpoint obstruction. The natural parameter and its scale, the basepoint, and the mean calibration are essential. An abstract uncalibrated metric jet is not these data. Point masses and zero variance cause no problem for law recovery, but a nonsingular mean-coordinate inverse/Hessian chart would require a nondegeneracy promise and its own domain. No such chart is silently asserted.

## 8. Readout sufficiency without unnecessary law recovery

The same compact fibre gives a narrower conclusion when the task asks only for a particular readout. Suppose F_m is nonempty and a scalar function G is uniformly computable and continuous on it, with the promise that G is constant there. Its common value is computable without a determinacy promise: enumerate rational intervals I of arbitrarily small requested length and semidecide F_m⊂G^(−1)(I). The image is an effectively upper-compact singleton, so one such containment search terminates. This is the classical compact-image/singleton mechanism, applied to the exact numerical fibre; it does not decide constancy or select a hidden law.

For example, each A_r(t), Z(t), or M_r(t) is computable continuously as a function of λ on F_m by the uniform next-moment bounds and positive denominator used in §5, whether or not F_m is a singleton. Thus a promised constant individual readout can be extracted. Whole-law uniqueness is a sufficient premise for any such readout, not a necessary condition for every isolated one.

For the declared *entire positive-time mean continuation*, however, determinacy is exactly the set-theoretic constancy condition. If every representing μ,ν has q_μ(t)=q_ν(t) for all t>0, then (log Z_μ−log Z_ν)′=0. Since both normalizers tend to one at zero, they are equal for all positive t. Laplace uniqueness gives μ=ν. Conversely determinacy makes every readout constant. This necessity is inherited from the earlier Laplace/mean argument; the new application is its combination with the effective compact-fibre construction. Neither promise can be checked merely by testing finitely many parameters. The parent proposed this scope corollary; it is not an independently discovered general selection theorem.

## 9. Sharp limitations and explicit controls

1. **Drop determinacy:** the inherited lognormal Stieltjes pair has exactly the same uniformly computable full moment name and different damped mean germs. No operation from that identical record can return both actual laws or both actual continuations. The compact fibre remains effectively closed, but is not a singleton.
2. **Keep only a finite exact prefix:** for any d≥0, use support {0,…,d+1} and the two probabilities formed from the binomial weights binom(d+1,j)/2^d on the even and odd j, respectively. The finite-difference identity makes their moments through degree d equal; they are distinct and individually determinate because their supports are compact. Their normalized means at t=log 2 are distinct. To see this for every d, put n=d+1 and z=exp(−t)∈(0,1). Their unnormalized generating polynomials are proportional to (1+z)^n±(1−z)^n. With h=((1−z)/(1+z))^n, the difference of their logarithmic z-derivatives is 2h′/(1−h²)<0. Multiplying by z gives the mean difference. The finite controls also check t=log 2 exactly using weights 2^(−j). Thus determinacy does not give a universal finite exact cutoff.
3. **Weak law is not all unbounded integration:** in the inherited endpoint family, a late halt at j gives ν=(1−1/j)δ_0+(1/j)δ_j, otherwise δ_0. This is a uniformly computable weak law, each instance determinate with all moments finite, but its mean is the halting bit. It does not satisfy the present uniform input-moment premise. Supplying the mean here would already supply that missing information.
4. **Negative parameters:** the density in §6 admits no t<0 normalized tilt. Determinacy alone gives no positive-exponential integrability or reverse-control domain. The earlier endpoint obstructions are not repaired by this theorem.
5. **Topology and labels:** the output is a weak law of the trait. On an accumulating known support this need not compute the indexed ℓ¹ allocation or singleton masses. The capped inverse has different information and a stronger output, and is not redundant.
6. **No verification or efficiency:** the extraction is a promised-input search, not a determinacy recognizer, a priori uniform condition number, practical complexity bound, or finite data-acquisition prescription. Its finite margins certify enclosures relative to valid moment names. They do not certify that empirical data meet the mathematical promise.

## 10. Ancestry, transport, and evidence ceiling

Classical primary-source mechanisms checked directly:

- Galatolo–Hoyrup–Rojas, *Dynamics and abstract computability: Computing invariant measures*, author-hosted text: https://members.loria.fr/MHoyrup/computinvmeas.pdf . Proposition 1 and Remark 4 supply uniform upper-compact closed restriction and singleton extraction; Theorem 2.9 and Remark 5 state uniform unique-zero recovery without a supplied isolating ball when uniqueness holds; Proposition 6 and Lemma 2.12 supply the computable measure-space/compactness machinery. We give the needed net, closed-fibre and extraction constructions explicitly above.
- Hoyrup–Rojas, *Computability of probability measures and Martin-Löf randomness over metric spaces*, §4 and its integration characterizations: https://members.loria.fr/MHoyrup/random_metric.pdf . This is the primary computable-measure representation ancestry. Our explicit clipping bounds verify the particular unbounded-to-compact transport needed here.

Project ownership is retained as follows. The half-line state, original mean, Fisher pairing, semigroup, moment hierarchy, lognormal obstruction, and ordinary exponential determinacy come from `measure-moment-continuation-boundary-20261009/RESULT.md`. Effective compact unique-zero recovery already appears in `effective-stationary-selection-20261010/RESULT.md` §4. `capped-tensor-recovery-20261010/RESULT.md` transports it to capped indexed ℓ¹ laws on bounded channel columns. `exponential-tail-effectivity-20261010/RESULT.md` provides explicit noncompact signed interior continuation and endpoint obstructions. `fisher-endpoint-geometry-20261010/RESULT.md` provides the calibrated Fisher-jet negative boundary; the parent proposed the positive jet corollary developed in §7.

The present project-relative addition is the effective full unbounded-moment fibre from its own next-moment tail information, promise-based weak recovery for every determinate half-line input, and uniform nonnegative damping through t=0. The strict-extension example separates this from exponential analyticity. The inspected ancestors do not already contain this theorem; this bounded comparison is not an exhaustive literature or novelty claim.

For the Orthemology transport, the source object is a probability law of the declared nonnegative numerical trait, the retained record is its graded product of all scalar moments, the updates are actual normalized damped tilts, and the output is its original raw mean (or other declared raw moments). On the determinate promised class, the record has a computable inverse into weak laws and computes these actual updates. Determinacy is a mathematical uniqueness premise about that numerical model. It supplies neither source reliability, epistemic entitlement, a norm of warranted belief, hidden fine-state identity, noetic realization, nor metaphysical uniqueness. It does not license identifying an infinite moment product with a finite episode or with the algebraic direct-sum tensor object.

`check_controls.py` passed 13,507 exact checks of finite rational tail/enclosure, compactification, finite-net rounding, quotient-budget, finite-prefix and calibrated cumulant controls, including the copied input hashes. These supplement the ordinary universal proofs, not a universal extraction implementation, proof-kernel certification, or a test of determinacy. Input copies and hashes preserve the inspected ancestry. No protected source is changed.
