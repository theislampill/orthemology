# Independent mathematical review: full-law coarse-graining

11 October 2026 UTC. Ordinary independent proof review and separate exact controls. This is not an audit-assess/governor action, protected integration, formal certification, historical-priority determination, or T20 closure. Author files were read and later copied for binding, never edited by this reviewer. Reviewed artifact hashes and replay receipts are recorded separately in REVIEW_BINDINGS.json.

## 1. Findings first

**No blocking mathematical error found in the bound report.** The affirmative commutation theorem, attained full-tangent quotient formula, product-target KL marginal identity, and correlated-Gaussian separator are valid under their stated hypotheses.

Two especially important qualifications were checked rather than inferred:

1. Nonproper observation maps do not ordinarily push arbitrary distributions forward. The report restricts to represented finite-action tangents, proves the bounded-test extension by cutoffs, and makes that extension independent of the representative. This suffices for orthogonal projections.
2. The cost of a displayed pushed field need not equal the minimum norm of its coarse tangent. Equation (6) includes exactly the additional orthogonal residual needed to make its minimum-norm claim correct. The quotient minimum in (15) has a separate attainment proof.

The reviewer flagged the nonproper-testing issue before the first full report inspection; the author already used the range-of-D definition and then expanded its cutoff argument. The reviewer supplied an independent strict residual example during review. These communications are disclosed; this is an iterative independent review, not a claim of blind assessment. Root's marginal-kl-root-check packet is a participating input and is not counted as independent evidence. Its initial incorrect auxiliary dissipation expectation remains preserved and is superseded by the correct value below.

## 2. Tangents and the nonproper-map cutoff argument

For a probability μ, Hμ=L²(μ;R^d)⊕L²_0(μ) is a Hilbert space. For every compact smooth test f, h↦∫(∇f·v+fα)dμ is bounded on Hμ. Consequently ker Dμ is a closed intersection of kernels of continuous linear functionals. A nonempty fibre Dμ^−1{σ} is a closed affine translate of that kernel and has a unique nearest point to zero. No closed-range theorem and no infinite-dimensional manifold theorem is needed for this fixed representable tangent minimum.

To extend zero-tangent testing to a smooth bounded f with bounded gradient, take χ_R with 0≤χ_R≤1, χ_R=1 on B_R, compact support, and |∇χ_R|≤C/R. Then χ_R f→f in L²(μ), while

    ∇(χ_R f)−∇f=(χ_R−1)∇f+f∇χ_R→0 in L²(μ).

The first term converges by dominated convergence, and the second has norm at most C||f||∞/R. Cauchy–Schwarz therefore passes the zero-tangent identity to f. This argument applies to f=φ∘T because φ∈C∞_c and ||DT||≤1 give bounded f and ∇f even when T is nonproper. If two representatives produce the same compact-test distribution, their difference is a zero tangent and thus annihilates every such pullback. This establishes the required representation independence, without claiming an ordinary pushforward operation on all distributions.

The C¹ enlargement is also valid: cut off first, then approximate a compact C¹ function and its first derivatives uniformly by smooth functions. In space-time, use a compact time test multiplied by χ_R(x)φ(Tx). The mass term passes by bounded convergence on the finite time interval; the flux/reaction terms pass by Cauchy–Schwarz using finite integrated action. There is no hidden boundary flux from a nonproper fibre.

The potential pair jμf=(∇f,f−μf) is orthogonal to ker Dμ by exactly this test pairing. It therefore is the minimum representative of Kμf, rather than merely an arbitrary admissible representation. Unbounded potentials need the stated function-and-gradient cutoff convergence; the Gaussian polynomial examples satisfy it. The report does not extend the compact-test iff to every unbounded objective without those hypotheses.

## 3. Contraction, exact gradient commutation, and quotient minima

The pushed fields are conditional expectations of DTv and α. Their exact action deficit is the sum of spatial contraction, conditional velocity variance, and conditional reaction variance. Each term is nonnegative. This establishes action contraction directly and, for distances defined using the same action and path class, contraction after infimizing. It does not by itself establish gradient commutation or an equality of tangent minima.

For the *whole objective* E(μ)=Ē(T#μ), its first variation is φ∘T. Pushing its negative-gradient representation gives spatial field −Aμ∇φ and centred reaction −(φ−νφ), where Aμ=E[DT DTᵀ|T]. Since 0≤Aμ≤I, equality of the resulting coarse tangent with the canonical one is equivalent to

    div(ν(Aμ−I)∇φ)=0
    ⇔ ∫∇φᵀ(I−Aμ)∇φ dν=0
    ⇔ (I−Aμ)∇φ=0 ν-almost everywhere.

The middle equivalence uses the admissible test φ and positive semidefiniteness. This removes the possible divergence-free ambiguity. Conditional expectation gives the corresponding fine-point criterion. The argument would not establish that iff for an unrestricted noncontracting map, and the report does not assert it there.

For all compact coarse test potentials, choose functions equal to coordinate y_j on each integer-radius ball. Positivity and a countable cover give I−Aμ=0 almost everywhere. Taking the trace of the conditional expectation then gives I−DT DTᵀ=0 μ-almost everywhere. Thus the all-objectives coisometry criterion is exact. Requiring it at every law recovers the pointwise differential criterion by Dirac laws. This does not imply injectivity or state reconstruction.

The norm-deficit formula (6) is valid: if h* is the fine minimum and k* the coarse minimum, Cμh*−k* lies in the coarse kernel, while k* is orthogonal to that kernel. Pythagoras supplies the fourth nonnegative term. There is no unsupported replacement of a field norm by an infimum.

Under coisometry, Lμ(w,β)=(DTᵀw∘T,β∘T) is an isometric right inverse of Cμ. Lift the already-attained coarse minimum, apply Dμ, and combine its upper cost bound with contraction's lower bound. This proves that the minimum over fine tangent lifts equals the coarse norm and is attained. It does not assert equality for every fine tangent or equality between intrinsic and unrestricted endpoint distances.

The same-fibre mobility-closure criterion is valid as an algebraic statement. Dirac fine laws on a common fibre distinguish every entry of DT DTᵀ using independently specified objective and observable gradients. Fibrewise constancy is sufficient to remove the dependence of Aμ on the hidden conditional law. Positivity, regularity, and well-posedness of a resulting degenerate coarse geometry are rightly left separate.

### Strict test of the fourth loss term

At μ=N(0,[[1,c],[c,1]]), project onto y and take the positive fine potential f=z²/2. Its minimum fine representation is ((0,z),(z²−1)/2), of cost 3/2. Its pushed representation is

    v̄=0,  ᾱ=c²(y²−1)/2,

of cost c⁴/2. That full coarse density tangent has variance velocity c². Its minimum representative is

    v*=c²y/3,  α*=c²(y²−1)/6,

of cost c⁴/6. Their squared residual is c⁴/3. The three original action losses are 1, 0, and (1−c⁴)/2; adding c⁴/3 yields exactly 3/2−c⁴/6. Thus the fourth term can be strictly positive even for orthogonal projection. These identities were checked separately in check_independent.py.

## 4. Actual flow scope and the two different failure mechanisms

Orthogonal projection satisfies coisometry for every μ, with no independence requirement. For a pulled-back nonlinear functional, the report correctly limits flow commutation to the common existence interval and a solution class with coarse uniqueness. Its explicit linear-expectation characteristic formula establishes an affirmative continuing law without appealing to an unstated arbitrary-measure PDE theorem. Bounded C² potentials with bounded first/second derivatives give complete characteristics and bounded positive weights on finite time intervals.

The inherited coercive-polynomial full-law tail theorem does not automatically cover a potential pulled back from fewer coordinates, which need not be coercive in hidden directions. No such hidden-coordinate moment or tail extension is asserted in the reviewed report.

The T(x)=x/2 Gaussian test is a genuine geometry mismatch for a pulled-back objective. Independently, fine m=2,v=4 and F=x²/8 give projected velocity (−5/4,−3/2), whereas the canonical coarse state m=v=1 under y²/2 gives (−2,−3). Their determinant is 3/4, so even a scalar local time change cannot identify their paths.

The product-target KL counterexample is different. The full KL functional is not the pullback of marginal KL: it contains conditional KL. Consequently its failure does not contradict the proved pulled-back-objective theorem.

## 5. Product-target KL identity and positive recovery

With ρ(y,z)=ν(y)r(z|y) and product target πYπZ,

    log(ρ/π)=log(ν/πY)+log(r/πZ),
    E[log(ρ/π)|y]=log(ν/πY)+h(y),

where h(y)=KL(r(·|y)||πZ). The conditional mean of ∇_y log r is zero under the stated differentiation/integrability hypotheses. Therefore the integrated spatial flux is exactly the coarse KL flux; the extra term is solely the centred reaction −ν(h−νh). It vanishes exactly when h is ν-almost everywhere constant. This is an instantaneous criterion; persistence along a trajectory is an additional condition, as the report explicitly states.

For an initial product and a product target, the product of marginal solutions solves the full equation: scores, spatial divergences, and centred reactions split additively. Uniqueness identifies it with the stipulated full solution. The hidden marginal need not already equal its target. This is a valid affirmative restriction and not an inference that initial constancy of conditional KL alone generally remains invariant.

## 6. Independent Gaussian separator verification

For target N(0,I) and Gaussian N(m,Σ), direct full-density calculation gives

    m′=−(I+Σ)m,  Σ′=2I−Σ−Σ².

At Σ₀=[[1,c],[c,1]], 0<|c|<1, the first-coordinate variance derivative is −c². The initial hidden conditional is N(cy,1−c²), with centred conditional divergence c²(y²−1)/2. Its reaction produces exactly the same variance derivative. The marginal initially equals the target; its standalone coarse KL flow is stationary.

Independently solving λ′=(1−λ)(λ+2) gives (λ−1)/(λ+2)=e^(−3t)(λ₀−1)/(λ₀+2). For q=e^(−3t), the covariance has diagonal and off-diagonal entries

    a(t)=1−3c²q(1−q)/(9−c²(1−q)²),
    b(t)=9cq/(9−c²(1−q)²).

The eigenvalues are

    [3+c+2cq]/[3+c−cq],
    [3−c−2cq]/[3−c+cq].

For |c|<1 and 0≤q≤1 all denominators and numerators are positive. Each eigenvalue stays between its positive initial value and 1. The smooth positive Gaussian solution is therefore global forward, and the full-density PDE substitution verifies more than moment consistency. For every finite t>0, 0<q<1 and a(t)<1. As t→∞, a→1 and b→0. The exact all-time separator is valid.

Initially the transport dissipation is 2c²/(1−c²), and the centred reaction dissipation is c². Their sum is c²(3−c²)/(1−c²), so full KL strictly decreases. The initial marginal KL derivative is zero, its second derivative is c⁴/2, and its Taylor coefficient is c⁴/4. These values agree with the corrected root assertion; the earlier root expected value omitted the diagonal contribution and was incorrect.

The marginal divergence is positive at finite positive times, while static KL data processing remains true. Indeed the KL chain rule still bounds marginal KL by full KL. Neither full objective decrease nor that static bound requires the marginal objective to decrease along a full-objective flow.

## 7. Ancestry and inherited-scope checks

The following primary passages were independently opened and inspected:

- Kondratyev–Vorotnikov, [Spherical Hellinger–Kantorovich gradient flows](https://arxiv.org/html/1809.03430v2), Remark 1.1 and the introduction's domain/hypotheses: the centred transport/reaction Onsager formula is classical. Their analytic PDE conclusions carry separate assumptions, not blanket Euclidean arbitrary-measure coverage.
- Liero–Mielke–Savaré, [Optimal Entropy-Transport problems](https://link.springer.com/article/10.1007/s00222-017-0759-8), Lemma 8.22: 1-Lipschitz pushforwards contract HK on separable metric spaces. The report supplies its own direct action proof for the declared centred probability action and keeps scale/domain identification separate.
- Liero–Mielke–Tse–Zhu, [WIAS preprint 3198](https://www.wias-berlin.de/preprint/3198/wias_preprints_3198.pdf), §3.4, Theorem 3.11, equations (3.8a,b), printed page 14: the normalized Gaussian reduced Onsager operator and the mean/covariance equations specialize exactly to the unit/unit formulas here. The author correctly denies fresh priority for Gaussian invariance or this ODE.

The inspected noetic-gradient-transport predecessor already owns its fixed-reference finite-dimensional canonical commutation and quotient results, including the distinction between divergence contraction and dynamic commutation. The present report does not erase that positive geometry or claim its KL separator disproves a whole-objective pullback theorem. Its local contribution claim is bounded to inspected passages and explicit deductions, not an exhaustive novelty claim.

## 8. Evidence and conclusion limits

check_independent.py imports no author/root checker. Its separate receipt contains 29 exact symbolic controls, including full Gaussian density-PDE equality, both initial action channels, all-time covariance and eigenvalue formulas, marginal Taylor coefficients, strict representation/minimum distinction, a noncollinear contraction example, hidden mobility, and a finite exact conditional-variance decomposition.

Fresh replay of the frozen author snapshot passed 70/70 checks, including its copied and original input bindings. Fresh replay of the separately written reviewer checker passed 29/29. All 24 author files were compared before and after, and the snapshot matched byte-for-byte. The reviewer's strict residual example, later incorporated and credited by the author, is a participating contribution and is not counted as an independently originated author claim validated by a second party.

These finite controls supplement the written Hilbert-space, conditional expectation, cutoff, and PDE arguments. They do not certify arbitrary PDE existence, historical novelty, empirical or noetic identification, recovery of discarded information, a globally smooth all-laws manifold, protected integration, or programme closure. The no-blocking finding applies to the hash-bound report with those limits intact.
