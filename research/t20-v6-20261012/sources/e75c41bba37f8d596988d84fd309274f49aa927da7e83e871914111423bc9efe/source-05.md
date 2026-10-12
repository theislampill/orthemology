# Independent review of the grouped-audit classification

Decision: PASS for the frozen mathematical report and exact controls identified below, within the stated domain and audit contract. No substantive mathematical defect found. This review supplies neither repository closure authority nor an application-specific justification for the audit family.

## Frozen artifact review

The author declared a freeze before inspection. The report and checker were hashed, copied byte-for-byte into a separate sibling replay directory, and read in full. The reviewed bindings are:

- RESULT.md: ff42e395bcb649c267374eb5d6e218bc0fd6e21079104be9a5cd97b77e0d233e
- check_exact.py: e8a1ada4474cd5af57e12a77a6ce38702871b2fa5e007f4368a8432d4c12251a
- INPUT_BINDINGS.json: 9eada5df5e0227de9afa72210dd77e1a09e695d064a58d2f77a9a7fd0b02964b

Author source directory: grouped-source-audit-gradient-20261011. Independent replay directory: grouped-audit-independent-replay. The independent proof and independently written symbolic control below preceded reading the author's frozen proof.

The frozen report's necessity and sufficiency proofs are correct. It explicitly retains the alpha factor, distinguishes ambient differential representatives from intrinsic simplex derivatives, retains C2 regularity via fixed interior evaluations, permits variable within-group metrics, and uses connected product factors correctly. Its statement about coincident maximal intervals is correct and does not claim forward completeness. The exact moving-position path in section 5 differentiates to the displayed equations. The row/column example is correctly limited to action generation and does not claim a multi-partition gradient classification. The inherited-K corollary in section 7 is valid under its stated mass-independent map and step choices, and expressly avoids a new implementation or integrator claim.

The report explicitly acknowledges mass normalization feedback, so its exclusion of cross-group potential dependence is not confused with dynamical independence. Its source guards require an actual group-constant revision contract, allow dependent historical variables, and forbid inferences to empirical independence, warrant, truth-directedness, or a metaphysical common source. No substantive interpretation overreach was found. Optional precision improvement only: state directly that representation labels do not assert real-world mutual exclusivity and normalized w is not automatically an amount of warrant. These points are already imposed in this review and no mathematical conclusion relies on their opposite.

The independent replay of the author's normal run passed 10 control groups / 102 counted checks and fixtures, including all ten current-copy/current-source hash comparisons. The author uses explicit exceptions rather than asserts, so its checks do not vanish under optimization. The independent optimized replay also passed the same 10 groups / 102 counted checks and fixtures under python -O. These finite and symbolic controls supplement the universal proof rather than establishing universal quantifiers by enumeration. Exact binding of the five selected ancestry records is checked; this is not an independent exhaustive ancestry or literature survey.

## Assumptions and result

Let a fixed partition of finitely many labelled indices have K nonempty groups. Positive weights sum to one, m_g is the sum in group g, and r_i=w_i/m_g. Each position domain X_i is a nonempty connected open Euclidean set. The full state domain is the positive weight simplex times the product of the position domains. The metric is

    G = (1/alpha) sum_i dw_i^2/w_i + sum_i w_i ||dx_i||^2, alpha > 0.

For every positive K-tuple a, the stipulated audit multiplies each weight in group g by a_g and renormalizes all weights. It leaves positions and all within-group proportions r unchanged. For E of class C2, the negative-gradient vector field is equivariant under all these audits if and only if

    E = C + sum_g m_g V_g(r_g, x_g)

for C2 functions V_g on the corresponding group state domains. The constant C is redundant and may be absorbed into every V_g. K=1 is vacuous: the audit is the identity and V_1=E is allowed.

## Necessity, without ambiguous ambient simplex derivatives

The change of coordinates w_i=m_g r_i gives

    G = (1/alpha) sum_g dm_g^2/m_g + sum_g m_g h_g,
    h_g = (1/alpha) sum_(i in g) dr_i^2/r_i + sum_(i in g) r_i ||dx_i||^2.

The mixed mass/proportion terms vanish because sum_(i in g) dr_i=0; likewise sum_g dm_g=0. Each h_g is a positive metric on its own internal tangent space and depends only on its own internal state y_g=(r_g,x_g), not on m.

For K>=2 take intrinsic mass coordinates u_g=m_g for g<K, with m_K=1-sum_(g<K)u_g, and mass log-odds q_g=log(m_g/m_K). If p_g is any representative of the intrinsic mass differential d_mE on the simplex, the mass field is

    mdot_g = -alpha m_g (p_g - sum_h m_h p_h),
    qdot_g = -alpha (p_g-p_K) = -alpha partial_(u_g) E.

Replacing p by p+c(1,...,1) changes neither expression. This removes any dependence on an arbitrary extension of E off the simplex.

The audit is translation q_g -> q_g+log(a_g/a_K). Every translation is available. Equivariance therefore makes qdot independent of q at fixed internal state, and hence d_uE independent of u. The positive simplex is connected, so E is affine in the masses:

    E(m,y) = sum_g m_g B_g(y).

The B_g can be recovered by an invertible fixed linear combination of E evaluated at K affinely independent interior mass points. They are therefore C2, even though a proof using mass derivatives alone might initially show only C1 coefficient functions.

The internal negative-gradient block is

    ydot_h = -(1/m_h) sharp_(h_h) d_(y_h) E.

The audit leaves every y_h and h_h fixed. Equivariance makes this block independent of m. Consequently, for some internal covector A_h(y),

    sum_g m_g d_(y_h) B_g(y) = m_h A_h(y)

for every mass in the open simplex. Comparing the coefficients of these homogeneous linear forms yields d_(y_h)B_g=0 for g!=h. A homogeneous linear form that vanishes on the open affine simplex has every coefficient zero; no extension of E to the boundary is being assumed. Connected product factors then imply B_g depends only on y_g. Simple connectedness is unnecessary. This proves the asserted decomposition.

This proof handles variable within-group metrics: applying their invertible sharp/flat maps is legitimate because their arguments do not change under an audit. A metric depending on other groups or on m would require a different theorem.

## Sufficiency

For E=C+sum_g m_g V_g(y_g),

    ydot_g = -grad_(h_g) V_g,
    qdot_g = -alpha (V_g-V_K).

Both depend only on internal states. Translations in q therefore preserve the entire vector field. Equivalently, in mass coordinates mdot_g=-alpha m_g(V_g-sum_h m_h V_h), whose pushforward under renormalized positive multiplication is the corresponding audited mass field.

## Flow claim and boundaries

C2 energy and the smooth positive-domain metric give a C1 vector field, so local solutions exist uniquely. Vector-field equivariance is equivalent to local-flow commutation. Because each audit is a diffeomorphism of the full stated domain and its inverse is also available, audited initial states have the same maximal existence interval and their maximal solutions correspond under the audit. This does not establish completeness or existence for all nonnegative times. A global semigroup S_t for every t>=0 would need an additional completeness assertion.

The statement concerns strictly positive labelled particles. It does not itself treat zero weights, changing partitions, unlabeled quotient configurations, a sum of overlapping groups, cross-group collision constraints, or a domain failing to be a product. For a smaller mass domain one must specify which audits are actually maps of that domain; the stated full all-a action is automatically available on the full positive simplex.

## Independent exact controls

The script check_grouped_covariance.py constructs the original full weight and position field for

    E = [w1*w2/(w1+w2)] (x1-x2)^2,

then compares it with the exact differential of the audit under (a,a,b), for symbolic positive a,b,alpha. Both three-component residuals simplify identically to zero. Since

    E = m_1 r_1 r_2 (x1-x2)^2

for the partition {1,2}|{3}, this is also directly in the classified family. It is nonlinear in the individual weights and contains a genuine within-group positional interaction.

At weights (1/3,1/3,1/3), positions (0,1,2), alpha=1, the singleton audit (2,1,1) produces audited weights (1/2,1/4,1/4). The actual audited position field is (2/3,-4/3,0); the pushed original position field is (1,-1,0). The actual audited weight field is (1/36,-5/72,1/24); the pushed original weight field is (-1/32,-1/64,3/64). Thus this candidate fails the universal-singleton contract in both blocks, as expected.

## Interpretation guardrails

The partition and group-constant multipliers are stipulated mathematical inputs. A source or provenance label is a representation label, not evidence that the alternatives are mutually exclusive, that observations are independent, or that one shared multiplier correctly models reliability. Normalized weights are probability or optimization weights in the stated model; they are not automatically quantities of epistemic warrant.

“Cross-group interaction excluded” refers to nonseparable energy dependence. The mass dynamics still couple through the common mean sum_h m_h V_h, so the groups are not dynamically independent.

An application as a common-source reliability audit needs an explicit mapping from the actual claims/evidence and proposed audit to these group-constant likelihood multipliers. A common creator or common provenance alone does not supply that mapping or place all claims in one audit group. K=1 then yields a vacuous mathematical audit, not philosophical justification. The theorem establishes a local extension of the specific universal-singleton contract being compared; it carries no global novelty assertion.

No protected repository edits, merge, closure, or philosophical endorsement are made by this review.

## Bounded descent-map corollary, if included by the author

Suppose an internal update sends y to y-tilde while preserving each internal domain and satisfies V_g(y-tilde_g)<=V_g(y_g) for every group. The selected maps and their step-selection rules must be invariant under all group audits; independence from group masses is sufficient. At the second stage let v_g=V_g(y-tilde_g), v_min=min_g v_g, and

    f_g=1/[1+h alpha (v_g-v_min)],
    m'_g=m_g f_g/(sum_j m_j f_j), h>=0.

The finite set of group potential values makes v_min well defined, and every denominator is at least one. The chosen h must also be audit-invariant. The first stage lowers E at fixed masses. The second changes its mass-dependent part by

    sum_g m'_g v_g - sum_g m_g v_g
      = Cov_m(v,f)/(sum_g m_g f_g)
      = [sum_(g<j) m_g m_j (v_g-v_j)(f_g-f_j)]/(sum_g m_g f_g)
      <= 0.

The sign follows because f is decreasing in v. All internal data, f_g, and h are unchanged under audits, so multiplying masses by f and multiplying them by audit factors commute after normalization. Thus the two-stage map is group-audit equivariant and energy nonincreasing. This is an algebraic lift of the given decreasing-potential reweighting construction, not evidence of a new integrator or a numerical-method campaign. No particular internal update, unconditional step size, or global convergence claim follows without additional assumptions.
