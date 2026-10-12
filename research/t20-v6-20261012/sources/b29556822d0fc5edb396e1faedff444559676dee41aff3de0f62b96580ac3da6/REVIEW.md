# Independent review: nonconvex polynomial-gradient limit classification

10 October 2026 UTC. Ordinary mathematical review, separate from the author and the parent who proposed the extension. This report grants no integration, protected change, formal-kernel verification, philosophical identification, or programme-closure authority.

Verdict: ACCEPTED as ordinary mathematics within the stated forward-law and separately qualified reverse-lift scope. No mathematical blocker remains. This review binds the exact author snapshot c11d417b0aca6273451dd479832ffa3341988d0f6dbe483e6a3f362590c647dc; RESULT.md SHA-256 fd5e814ce2766f3283b0472b04e6c00234654ff46df5cbebb324fa1c9668789d; author manifest SHA-256 2309a439afe5cb6448d8e568560b17bac408718a0a64d24e3ba72df0a716a4cf.

## 1. Scope reviewed

The author studies the actual forward flow of a coercive polynomial F on finite-dimensional Euclidean space, with velocity −∇F and killing factor exp(−∫F). I independently checked both the finite-atomic theorem and §5's extension to any specified initial Borel probability. These are distinct from proving existence of a representing measure for an arbitrary formal hierarchy.

The main conclusions are correct: every particle converges to one critical point; its excess energy above its own limiting critical value is integrable; finite labels have the stated exact winning weights and losing exponential prefactors; and every supplied initial probability has the endpoint-pushforward limit at its least positive-mass critical level. Positive-time finiteness and long-time convergence of all polynomial moments and every finite Wasserstein distance require no initial-moment assumptions here.

## 2. Particle argument

Coercivity yields a global lower bound and compact sublevels. The energy identity traps each local solution in one such set, and local ODE continuation gives global forward existence. Bounded gradient and Hessian on that set make the squared gradient uniformly continuous in time. Its time integral is finite, so it tends to zero. Each cluster point is critical and has the limiting energy.

The local analytic gradient inequality is used only near one cluster point. The first-exit argument correctly traps the eventual trajectory in that neighborhood: the bound on the remaining travel is smaller than its distance to the boundary. It is not assumed in advance that the trajectory eventually remains there. Increasing the gradient exponent to at least 1/2 is legitimate after restricting the energy gap to [0,1].

The integrated inequalities have the correct exponents and signs. For h=F(X)−c and ||∇F||≥κh^θ with θ<1,

    −(h^(2−2θ))' ≥ κ²(2−2θ)h.

This proves the finite excess integral directly. It also covers arbitrarily flat analytic critical points and saddle endpoints, since only the trajectory's nonnegative energy gap is used. The strict bound θ<1 is essential. A nonstationary trajectory cannot reach an equilibrium in finite time by local backward uniqueness along the existing path.

## 3. Finite weights and geometry

The decomposition K_j=c_jt+I_j−R_j(t) yields the exact normalized identity in §3. Every I_j is finite, so every surviving coefficient a_j exp(−I_j) is strictly positive. The minimal occupied critical value exists in the finite list. Losing prefactors and the winner-error bound follow by elementary finite-sum algebra; no uniform exponent, basin computation, or numerical convergence is inferred.

The ensemble identity is correct: D=e^(c*t)Z decreases from 1 to A*, and −(log D)'=E−c*. The finite-atomic metric-length claim also checks out. The transport length is bounded by the sum of particle lengths. In the reaction coordinates 2√w_j, winning-label speeds are bounded by their integrable particle and ensemble gaps, and losing-label speeds by an exponentially decaying square-root mass times a bounded energy difference.

Finite-time injectivity and positive weights preserve the finite rank. A smaller limiting rank results from vanished weights, merged endpoints, or both. This does not give a global identification of a metric completion or establish a smooth metric across all ranks.

## 4. Arbitrary initial probability

### Measurability and selection

The critical-value set is semialgebraic and null by the scalar Sard theorem, hence finite. The critical set itself need not be finite; the proof does not assume it is. A global minimizer ensures a nonempty critical-value set.

Each finite-time flow map is continuous. The endpoint q is their pointwise limit along integer times and is Borel. Then c=F∘q is Borel, and I is the increasing limit of the Borel functions K_n−nc. Finite critical values guarantee an attained least level with positive initial mass. The corresponding integral A* is positive because exp(−I)>0 everywhere on a positive-mass set. Neither uniform boundedness nor integrability of I against the initial law is needed.

Lower critical basins of zero initial mass are explicitly removed from the almost-everywhere comparisons. On the remainder, 0≤g_t≤1, g_t decreases to 1_(B*)exp(−I), and D_t decreases to A*>0. Dominated convergence proves initial-coordinate total variation convergence and physical-space weak convergence. The losing-basin exponential formula follows by dominated convergence of exp(−I_t) on that basin, and its coefficient is positive.

### Polynomial envelope and moments

The sublevel-radius graph proof is valid. The maximum M(s) exists and is monotone. Quantifier elimination gives a finite polynomial sign description of its graph. At each graph point some nonzero defining polynomial must vanish, since otherwise the sign description would hold on an open neighborhood. Their product supplies a nonzero P(s,M(s))=0. This polynomial must have positive degree in its second variable. Outside finitely many zeros of its leading coefficient, Cauchy's root bound bounds M by polynomial coefficient ratios, which have polynomial growth at infinity. Monotonicity handles the remaining bounded interval.

This avoids the false claim that every coercive polynomial has a quadratic or linear-in-radius lower bound. For example, (a−b²)²+b² is coercive, but along a=b² its energy is b² while its squared radius is b⁴+b². The independent controls verify these expressions.

The crucial moment bound uses terminal rather than initial energy. Along the occupied basins, u_t=F(Φ_t)−c*≥0 is decreasing and g_t≤exp(−t u_t). For every positive lower time t₀, polynomial terminal-energy growth multiplied by exp(−t₀u_t) is bounded uniformly in initial position and t≥t₀. This is an integrable constant under every initial probability. It proves the claimed absolute-moment regularization and dominated convergence without any initial moments.

The Wasserstein step is justified by convergence of absolute p-th moments, or by the supplied explicit coupling. For that coupling both initial-coordinate densities are bounded by g_t/A*. The density difference times |Φ_t|^p has the same constant domination and converges pointwise to zero. The endpoint contribution is compactly supported on the winning critical level. The coupling therefore controls both the common and unmatched parts.

The positive-time ensemble derivative is justified by the uniform bound u exp(−t₀u). Dominated convergence gives D_t→1 as t↓0. Integrating −(log D)' proves the improper ensemble-gap identity even if E(0)=∞. This does not claim finite initial moments or C¹ polynomial coordinates at zero for arbitrary initial laws.

## 5. Countercontrols and continuity boundary

The unequal-well polynomial has critical energies −5/12 and −8/3, with gap 9/4. An initial law carried entirely in the higher well does not create mass in the lower well. Adding any ε>0 at the lower stationary minimum changes the eventual law to its Dirac mass, although the input perturbation tends to zero in total variation and every finite Wasserstein distance. Its exact crossover time is (4/9)log((1−ε)/ε), which diverges as ε↓0. Hence fixed-time continuity and discontinuity of the infinite-time selection map are compatible.

The circle example is a valid non-atomic critical limiting law. The saddle example validates non-minimizing endpoints. The quadratic moving Dirac validates failure of physical-space total variation convergence. None contradicts initial-coordinate total variation convergence, finite-time rank constancy, or finite-time injectivity.

## 6. Source and inheritance checks

I independently opened the author-hosted Absil–Mahony–Andrews paper. Lemma 2.1 supplies the local analytic gradient inequality; Theorem 2.2 and its proof give the finite-length first-exit argument without isolated-critical-point, convexity, or nondegeneracy assumptions. Its discrete Proposition 3.3 is not used. The general particle convergence is classical; the packet derives the integrated-gap and normalized-measure consequences for this setting.

I independently opened Kurdyka's primary article, §1: projection closure, quantifier closure, and one-dimensional finiteness are explicitly available there. I also opened Sard's original article, p.883, which states the scalar critical-value-nullity theorem under finite differentiability satisfied by a polynomial. The algebraic radius-growth argument is proved in the packet rather than attributed to an unstated global rate theorem.

Sources checked:
- Absil, Mahony, Andrews (2005), Lemma 2.1 and Theorem 2.2: https://sites.uclouvain.be/absil/Publi/Convergence_SIOPT/13-60526.pdf
- Kurdyka (1998), §1: https://aif.centre-mersenne.org/item/10.5802/aif.1638.pdf
- Sard (1942), p.883: https://webhomes.maths.ed.ac.uk/~v1ranick/papers/sard.pdf

The copied predecessors support the stated distinctions: the joint-atomic predecessor leaves the general same-energy and particle convergence unasserted; the radial-quartic predecessor already owns its particular infinite-law limit; the general finite-rank reverse theorem retains full path-rank control; the SOS-dissipative theorem separately removes that promise under its certificates; and the discretization result is one-step preservation/consistency, not global iterate convergence. No forward formula is substituted for a missing reverse theorem.

## 7. Evidence scope

The independent script checks exact symbolic identities for the monomial and double-well excess primitives, unequal-well energy gap and reweighting equation/crossover, the circle critical set, and a nonradial coercive valley growth control. These controls supplement the written proofs; they do not enumerate all polynomials, implement a basin solver, or constitute formal-kernel verification.

I read the frozen RESULT.md and the verification/replay notes after the author supplied the manifest, including the final positive-time hierarchy and time-zero regularity paragraph. That paragraph is correct: apply the same envelope to the polynomial generator for positive-time differentiation; when the initial law has all moments, bound the terminal polynomial by a polynomial in its initial energy and use dominated differentiation through zero. No unconditional time-zero regularity is asserted.

All 14 author payload hashes and its snapshot digest were checked before copying into author_snapshot. The copied checker passed 91 checks with the six originals available and 85 portable checks without them. Each fresh JSON report was byte-identical to its corresponding frozen historical author report. The independent symbolic script passed all 10 controls. The author snapshot and all six inspected predecessor files were checked unchanged afterward.

REVIEW_RECEIPT.json records these bindings and results. REVIEW_MANIFEST.json binds this review, the portable checker, the copied author packet, and the reports. check_review.py supplies a fresh portable replay. These receipts establish the executed control and preservation facts; they do not turn ordinary written proofs into formal-kernel proofs.
