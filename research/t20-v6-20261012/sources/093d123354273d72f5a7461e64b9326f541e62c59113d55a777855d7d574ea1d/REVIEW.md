# Independent review: coercive-SOS energy-controlled polynomial drift

10 October 2026 UTC. Independent ordinary mathematical/source review of the separately frozen broad successor. This report does not modify or replace the previously accepted narrow squared-energy author or review packets. Its verdict concerns the exact full-path hypotheses stated below, not every coercive polynomial drift or a finite moment truncation.

## Verdict and frozen identity

PASS, with no blocking mathematical findings, for `general-coercive-energy-drift-20261010/RESULT.md`, SHA256 `79a467b9cc0ef67817ad02dafe146cf42709b41d1172559d806d883adf31a96e`, and author manifest SHA256 `7389c1ddccb14fc62b7b2480a56547efa88066981eff6c77565156af14fbc530`.

The assumptions are: finite-dimensional real polynomial algebra; coercive SOS H; polynomial b with the actual polynomial certificate S=−b·∇H SOS; normalization and full square positivity at every supplied time; every polynomial coordinate C¹ through zero with continuous right derivative; and every polynomial hierarchy equation on a nontrivial time interval. Initial representability, rank, radial SOS domination, coordinate Carleman bounds and initial tails are not assumptions.

The full frozen report and checker were inspected. The separately recorded execution reproduces the author's 83 controls in a copied workspace and passes 154 independently written finite controls. The author's categories distinguish 39 localization identities, seven beyond-H² controls, 16 inherited regressions and 21 integrity checks. Many independent checks are also explicitly inherited factorial regressions; none is counted as a discovery or a formal proof of the analytic theorem. Author and declared predecessor bindings, including all old narrow author bytes and receipt-bound narrow review bytes, are verified unchanged.

## 1. Abstract energy bound and inherited static existence

Unnormalization A=aL with a=exp(−∫L(H)) gives Gp=b·∇p−Hp and positive mass a. The energy recurrence b_n′=−n A(H^(n−1)S)−b_(n+1), with b_0′=−b_1, is exact. All discarded terms are SOS evaluations: H^n and H^(n−1)S are products of SOS polynomials. This is where the explicit SOS assumptions matter; pointwise energy decrease alone would not suffice before representation. Repeated first-order integration from b_0(0)=1 gives b_n(t)≤n!t^(−n), with no higher-time-derivative or initial-growth premise.

The application of inherited Lemma F is legitimate. Polynomial-functional Cauchy–Schwarz gives A(q²H^(2n))≤sqrt(A(q⁴)A(H^(4n))). The factorial bound and binomial(4n,2n)≤2^(4n) then supply the common width t/2 required by that lemma for every polynomial q. Only its finite front constant depends on q. Zero weighted square moments cause no division. Coercivity makes every energy fibre compact, including empty fibres where the inherited normalized functional construction cannot occur.

The earlier Lemma F is a genuine abstract-functional existence result. Its scalar Hamburger measures, signed polarization, common countable null-set construction, compact algebraic fibres, and Haviland step were inspected. It does not assume a vector measure or a measurable selection of fibre measures. This successor correctly inherits that construction instead of relabelling it as a new theorem. The independent review also checked the cited compact algebraic-set moment statement in the primary revised Chapter 12; its functional hypothesis is square positivity plus annihilation of the ideal, with no real-radical requirement.

After representation, monotone convergence gives ∫exp(σH)dν_t≤(1−σ/t)^(−1) only for σ<t. The same estimate holds for any competing representative because all H-power moments agree and H≥0. Polynomially weighted signed energy pushforwards therefore have exponential tails by actual-measure Cauchy–Schwarz. Equality of all pH^n moments identifies those signed scalar measures, then compact sublevel restrictions agree on all polynomials and hence as measures. This proves joint determinacy without spatial Carleman or exponential-|x| assumptions.

## 2. Continuity and the common weighted energy strip

Every fixed radial moment A_r(R^k) is continuous and bounded on an interior compact time interval, directly from the given polynomial coordinates. The positive continuous mass a is bounded away from zero there. Consequently the represented probabilities are tight, all fixed polynomial tests are uniformly integrable using higher radial moments, and every subsequential time limit has the prescribed full moments. Positive-time determinacy identifies it with the correct representative. This proves weak continuity rather than assuming a choice of continuous representing laws.

For J=[η,B], ε=η/4 leaves the common estimate ∫e^(2εH)dν_r≤2. Thus, for every fixed polynomial P,

    sup_r ∫|P|e^(εH)dν_r ≤ sqrt(2 sup_r A_r(P²)) < ∞.

The rate is independent of P; the constant need not be. Polynomial coefficients introduced by the drift, energy chain rule, and any fixed number of scalar complex derivatives are therefore permitted. This uses represented measures only. Neither a bound |P|≤Ce^(δH) nor an unproved quantitative coercivity estimate is needed at this stage.

The needed time integrals are measurable. Weak continuity first handles bounded continuous cutoffs; uniform polynomial integrability handles unbounded polynomial coefficients. For the signed measure construction one may apply Riesz to bounded linear functionals on C₀, or integrate the resulting Borel kernels. The uniform total-variation bounds are sufficient in both formulations.

## 3. The new residual-localization proof

The residual D is an order-at-most-one distribution, with finite zero-order coefficient ν_v−ν_u+∫Hν_r dr and finite derivative coefficients −∫b_iν_r dr. Those coefficients are finite because b and H are polynomial and their absolute moments are uniformly bounded. D vanishes on polynomials by the integrated hierarchy, interpreted using these actual finite-moment coefficients.

For pP_N(H), the generator product rule contains two terms:

    G(pP_N(H))=(b·∇p−Hp)P_N(H)+p(b·∇H)P_N′(H).

The second term cannot be omitted. For small scalar frequency, the Taylor sums and their scalar derivatives are dominated by a polynomial coefficient times e^(|z|H). The common weighted energy estimate permits dominated convergence in space and time, proving D(pe^(izH))=0 near the real origin. Complexifying z yields a holomorphic residual in a connected horizontal strip. On each compact substrip every fixed derivative has the same type of domination. The identity theorem applies to the real interval of zeros and reaches every real scalar frequency. No analyticity in the original x-frequencies or global C¹ polynomial density is claimed.

The scalar measures have the correct signs:

    α_p = H_*(pν_v−pν_u) − ∫H_*((b·∇p−Hp)ν_r)dr,
    β_p = −∫H_*(p(b·∇H)ν_r)dr.

Both are finite signed measures with exponential absolute energy tails, by the weighted estimate and total-variation domination under pushforward. Their relation is α_p(e^(iξh))+iξβ_p(e^(iξh))=0. Scalar Fourier inversion for χ∈C_c∞, with its integrable (1+|ξ|)-weighted transform, gives D(pχ(H))=α_p(χ)+β_p(χ′)=0.

It would be wrong to infer that α_p and β_p vanish individually. The independent exact control α=δ₀−δ₁ and β=Lebesgue measure on [0,1] has α(χ)+β(χ′)=0 for every smooth χ despite both being nonzero. The author correctly reasons about their combined order-one scalar distribution. Separate controls reject omission of β and reversal of its sign.

Now T=χ(H)D is the distributional product: T(φ)=D(χ(H)φ). Its coefficient representation includes the χ′(H)∇H contribution. Coercivity makes H^(−1)(suppχ) compact; all surviving coefficient measures are supported there and bounded. Hence T has a C¹ seminorm bound on one compact set. Equation D(pχ(H))=0 says T annihilates every polynomial, with noncompact-polynomial evaluation unambiguously defined by compact support.

Coordinate exponential Taylor polynomials converge together with their first derivatives on that compact set. Applying T therefore gives T(e^(iξ·x))=0 for every ξ. Fourier inversion, now against the compact order-one distribution with O(1+|ξ|) exponential-test growth, gives T=0. This uses exactly the first derivatives required by the residual, and no higher order is concealed. Independent Chebyshev controls show why uniform function approximation alone would be insufficient: T_n(x)/n tends uniformly to zero on [−1,1], while its derivative at 1 equals n.

Finally, for any compact smooth spatial φ, choose χ=1 on a neighborhood of H(suppφ). Then χ(H)φ=φ as smooth functions, including the derivatives. Thus D(φ)=T(φ)=0. This completes a genuine polynomial-to-compact-test PDE proof. Static moment determinacy alone was not substituted for that missing implication.

## 4. Forward flow, spatial cutoff, and initial recovery

Pointwise H′=−S≤0 traps each local characteristic in one compact sublevel. Local polynomial ODE continuation proves forward completeness. Finite-time injectivity uses only backward uniqueness along already existing trajectory segments. The variational determinant is nonzero, so the map is a diffeomorphism onto its open image. Neither all-space surjectivity nor global backward completeness enters.

After the compact-test PDE is established, the time-dependent compact-test rule follows by the usual difference-quotient split. The forward-flow weighted terminal test U is bounded by ||f||∞ because H≥0. A fixed spatial cutoff χ_N has no time derivative. Its product leaves only U b·∇χ_N after backward-equation cancellation; all derivatives of U disappear before removing the cutoff. Uniform polynomial moments control that term. In fact N^(−1)||f||∞||∇χ||∞sup_r∫|b|dν_r already suffices; the author's stronger tail estimate is also correct. This requires neither spatial exponential tails nor compact inverse-flow support.

Near zero, second moments give tightness, higher moments supply uniform integrability of every polynomial, and a single weakly convergent subsequence yields an all-moment probability representing L₀. Bounded flow-weight tests converge locally uniformly along that subsequence, while tightness controls their tails. One initial law consequently represents the entire path. Positive weights and the inverse map on the actual image make the unnormalized transformation injective; probability masses remove the proportionality ambiguity after normalization. The proof never deduces uniqueness of an initial law from initial moments alone.

The endpoint estimate ∫exp(tH)dν_t≤1 follows after identification from energy decrease along trajectories. It is not the invalid substitution σ=t in the earlier geometric series.

## 5. The arbitrary-polynomial-drift converse

The quantitative sublevel envelope is needed for a converse from every all-moment law. Mere smooth properness would not supply it. The inherited argument was independently inspected: the attained radius-maximizing function M(s) has a semialgebraic graph by quantifier elimination. In a finite quantifier-free description, some nonzero defining polynomial must vanish at each graph point, or the graph would contain a neighborhood. Their product is nonzero and vanishes at (s,M(s)). It must have positive degree in its second variable.

The nonzero leading coefficient is a univariate polynomial and has only finitely many real roots. Beyond them Cauchy's root bound controls M by ratios of polynomial coefficients, hence a polynomial power of 1+s. Monotonicity controls the remaining bounded interval. The proof correctly takes this threshold; a root coefficient need not be nonzero for every s. Thus 1+|y|²≤K(1+H(y))^N for finite K,N, without claiming an optimal or effective exponent.

Along the flow H decreases, so every p(Φ_t) and (Gp)(Φ_t), for polynomial Gp=b·∇p−Hp, has a fixed polynomial bound in the initial coordinates. This is valid for arbitrary polynomial b of the stated class, not only Euclidean gradients. All-moment initial laws allow dominated differentiation, including continuous right derivatives at zero. The resulting positive normalizer yields the exact normalized hierarchy. Together with reverse lifting, this proves the all-law converse, initial-law-fibre classification, unique global continuation of a supplied path and constant rank from finite initial full rank.

## 6. Discriminator and exact scope

The cubic valley H=1+(x−y³)²+y² is coercive and SOS, and its negative Euclidean gradient has SOS energy dissipation. The explicit polynomial radius envelope and SOS identities check. On x=y³, every shifted squared-energy comparison (F+C)²−c|x|² has negative leading coefficient −c at degree six, so no c>0 or finite C rescues the narrow hypothesis. This witnesses a real extension without confusing a static polynomial automorphism with the gradient characteristic map.

The frozen narrow finite-atomic metric and factored-mobility calculations do not depend on the removed radial certificate, so they apply after this broader reverse lift. Factoring M=BᵀB remains a stated hypothesis; degeneracy does not yield a Riemannian inverse metric. General energy-controlled drift may rotate indefinitely and is not asserted to be a gradient or convergent.

The theorem still requires a coercive SOS energy and SOS −b·∇H. It is not a result for every coercive F lacking an SOS shift, arbitrary pointwise energy-decreasing drift, finite square tests, diffusion, finite empirical data, stable numerical inversion, or an infinite-dimensional smooth Riemannian manifold. There is no formal-kernel verification, protected integration, field-priority determination, empirical/noetic identification or T20 closure.

## 7. Source and evidence boundaries

The static Lemma F, compact-sublevel determinacy lemma, narrow flow/cutoff framework, and polynomial sublevel envelope are explicitly inherited. The new mathematical assembly reviewed here is scalar-energy localization of a first-order residual. The review inspected the named local proofs and the exact bound versions; it does not recertify unrelated conclusions of those source packets.

Primary source checks on 10 October 2026 were targeted:

- Schmüdgen, revised Chapter 12, Corollary 12.34(iv), printed p.14: compact algebraic-set representation from a positive functional annihilating the ideal. https://arxiv.org/pdf/2309.10052
- Schmüdgen, The Moment Problem, Theorems 1.12 and 3.8: Haviland and Hamburger existence used inside the inherited lemma. https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf
- Kurdyka 1998, §1, printed pp.771–772: semialgebraic projection and quantifier facts supporting the inherited graph argument. The polynomial root-bound deduction is given directly. https://aif.centre-mersenne.org/item/10.5802/aif.1638.pdf

These primary PDFs were checked through the available web text; this review does not claim newly archived byte copies of those PDFs or new visual PDF verification. Executable replay depends on the exact local files listed in PREDECESSOR_BINDINGS.json. The review's frozen receipt binds its report, independent controls, snapshots and actual execution results. Finite controls supplement the universal written reasoning and do not mechanically certify the analytic or measure-theoretic theorem.
