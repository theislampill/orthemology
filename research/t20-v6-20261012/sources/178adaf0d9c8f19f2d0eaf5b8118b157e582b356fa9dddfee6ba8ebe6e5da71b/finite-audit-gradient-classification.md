# Finite-audit Fisher descent: exact criterion and sharp cardinality threshold

10 October 2026 UTC. Additive mathematical continuation within active T20. Written universal proofs and exact rational controls; no kernel certification, field-novelty claim, empirical identification, integration, protected edit, or programme closure. The binary gradient packet was a moving draft when inspected and is not imported as verified evidence.

## 1. Result first

Let a strictly positive joint law have a target with r≥2 states and one fixed audit with k≥2 labelled outcomes. Retain every conditional target law p_j and the current target law q=Σ_j w_j p_j, while discarding audit weights w_j whenever they are not reconstructible. Equip the full joint simplex with its categorical Fisher metric. For an ambient C² objective J(p_1,…,p_k,q), take the negative full-source Fisher gradient of its pullback.

There are three exact results.

1. At one signature, projected velocity is independent of the positive weight representative exactly when C(p_j)J_j=0 for each index j whose weight can vary, where C(p)=diag(p)−ppᵀ. Equivalently, this is required at j precisely when some v∈ker Q has v_j≠0, with Q=[p_1 … p_k]. When imposed at every admissible signature, the condition is equivalent to descent of the actual maximal source flow, including matching maximal intervals.
2. If k>r, descent everywhere is equivalent to J on the signature image being a function φ(q) of the current target alone. This is a statement about the restricted objective, not about its arbitrary values outside the image. The corresponding equations and positive target tilts give a regular closed signature flow.
3. The strict inequality is sharp for every 2≤k≤r. The polynomial J=det(QᵀQ) depends genuinely on the conditional laws even at fixed q, yet descends globally. At rank-deficient Q its full differential is zero; those are exactly the nonsingleton fibres. Full-column-rank fibres are singletons. This source flow is complete.

Thus the previously observed three-audit-outcome loss of inquiry-value information for a binary target has a second, different consequence: on the full strictly positive domain, any globally descending full-source Fisher objective is current-target-only. This is not a conclusion about all metrics, all loss definitions, a fixed forward audit channel, or restricted reachable families.

The root supplied the finite-gradient/classification candidate and the Q-Gram sharpness construction. The independent finite-audit worker supplied the audit-row-rescaling proof of actual-flow descent in §5; that is a credited mathematical contribution, not independent corroboration of the proof it supplies. The density construction and sharpness argument were also checked independently during this task. Review status, if any, is carried by a separate review artifact.

## 2. Fixed domain, operations, and inherited ownership

Write Δ_m°={z∈R^m:z_i>0, Σ_i z_i=1}. The source domain is

    X = Δ_k° × (Δ_r°)^k,
    μ_{j,i}=w_j p_{j,i}.

This parametrises every strictly positive k×r joint law bijectively and smoothly. Audit labels and target labels are fixed. The signature and its image are

    F(w,P)=(p_1,…,p_k,q),   q=Qw,   Q=[p_1 … p_k],
    S=F(X) ⊂ A=(Δ_r°)^{k+1}.

At a fixed P, admissible q are precisely the strictly positive-weight mixtures of its columns. They form the relative interior of conv{p_1,…,p_k}, including its lower-dimensional cases. It suffices below to use the defining positive-mixture representation, without relying on that convex-hull characterization.

The posterior-only contract here is rereading one already-fixed D: the empty history returns q; a nonempty history with the same audit label j throughout returns p_j; a history containing two distinct audit labels is impossible. Strictly positive w makes every individual outcome feasible. Thus F exactly captures these conditional answers and feasibility, while audit frequencies are absent. New independent experiments, arbitrary interventions, hidden labels, a fixed forward channel P(D|Θ), and policy values are different contracts.

An ambient C² J means C² on the full product A of open simplex affine spaces. Derivatives can be represented by any smooth Euclidean extension: J_j∈R^r for its p_j slot and h=J_q∈R^r for its q slot. Adding a scalar multiple of the all-ones vector to any derivative changes no intrinsic result. No canonical redundant-coordinate gradient is presumed.

### What is inherited

The three inspected reports are copied and hash-bound in INPUT_BINDINGS.json.

- Audit continuation already owns the fixed-audit posterior signature, its binary injectivity/independence split, and the distinction between posterior answers, event probabilities, and event feasibility. Its finite invariant-observable and paired-tensor methods are not claimed anew.
- Posterior inquiry value already owns the general positive weight fibre {w>0:Qw=q}, the row/kernel criterion for expected quantities, and the three-outcome strictly positive proper-score counterexample. Its mechanism is inherited finite-dimensional fibre factorization, attributed there to H-ICS.
- The binary gradient report was explicitly a draft at capture. It motivates the comparison but is not a verified premise. All finite-dimensional formulas and theorems needed here are derived below. Its broader topology claims are not needed or imported.

Categorical Fisher replicator dynamics, Cauchy–Binet, Vandermonde nonsingularity, and finite-dimensional ODE uniqueness are standard mechanisms. The bounded addition is this exact finite posterior-signature descent criterion, its global k>r classification, its sharp k≤r control, and the accompanying contract boundaries. No exhaustive project or literature priority claim is made.

## 3. Full-source Fisher equations

For tangent perturbations satisfying Σ_j δw_j=0 and Σ_i δp_{j,i}=0, the full categorical Fisher metric is

    g((δw,δP),(ηw,ηP))
      = Σ_j δw_j ηw_j / w_j
        + Σ_j w_j Σ_i δp_{j,i} ηp_{j,i} / p_{j,i}.

Indeed δμ_{j,i}=p_{j,i}δw_j+w_jδp_{j,i}; expansion of Σ δμ ημ/μ has vanishing cross terms. For E=J∘F,

    dE = Σ_j ⟨h,p_j⟩ dw_j + Σ_j ⟨J_j+w_j h,dp_j⟩.

The inverse simplex Fisher operator is C(p)=diag(p)−ppᵀ. Define a_j=C(p_j)J_j. The negative gradient is therefore

    wdot_j = −w_j ⟨h,p_j−q⟩,
    pdot_j = −C(p_j)h − a_j/w_j.                    (1)

The full-source q derivative is

    qdot = −C(q)h − Σ_j a_j.                        (2)

For verification, the matrix total-covariance identity is

    Σ_j w_j C(p_j) + Σ_j w_j(p_j−q)(p_j−q)ᵀ = C(q).

Substitute (1) into d(Σ_j w_jp_j)/dτ to obtain (2). Here τ is evolution time; no audit probability is used as a time parameter.

The source Fisher decrease identity is

    dE/dτ = −Σ_j w_j ⟨h,p_j−q⟩²
             −Σ_j (1/w_j)(J_j+w_jh)ᵀ C(p_j)(J_j+w_jh) ≤ 0.  (3)

This decreases the stipulated numerical objective. It proves neither truth-directedness nor warranted actual belief change.

A useful joint-coordinate form, obtained by differentiating μ_j=w_jp_j, is

    V_{j,i}(μ)=μdot_{j,i}
      = −μ_{j,i}(h_i−⟨q,h⟩) − a_{j,i}.             (4)

All derivatives on the right are evaluated at F(μ). Formula (4) will give actual-flow descent directly; pointwise projectability on a singular quotient is not assumed to imply it automatically.

### Simplex gauge and extension independence

For interior p, C(p) is positive definite on the simplex tangent space and has kernel span{1}. Indeed zᵀC(p)z=Σ_i p_i(z_i−⟨p,z⟩)². Thus C(p)z=0 exactly when z is constant across target states. Every displayed formula is unaffected by adding constants to h or the J_j.

More generally, two ambient objectives that agree on S have equal pullbacks on the entire source X, hence the same intrinsic source gradient and projected field. The assertions concern that pullback, not an arbitrary off-image extension. For k<r, S can have empty ambient interior, so this qualification is substantive. In the k>r theorem, density of full-rank image points also yields the stronger explicit vanishing of the intrinsic p_j derivatives on all S.

## 4. Exact pointwise fibre criterion

At a signature s=(P,q), its source fibre is

    W_s={w∈R^k:w_j>0, Qw=q}.

It is nonempty by definition of S. Column stochasticity gives 1ᵀv=0 for v∈ker Q and ensures that Qw=q already enforces Σw_j=1. Fix w⁰∈W_s. Every difference of representatives lies in ker Q, and for every v∈ker Q the weights w⁰±εv stay in W_s for all sufficiently small ε>0.

Consequently the following descriptions of a variable index j are equivalent:

    some two representatives have different w_j;
    some v∈ker Q has v_j≠0;
    rank(Q with column j deleted)=rank(Q).

The last equivalence says exactly that p_j lies in the linear span of the other columns. In full row rank, it reduces to the deletion matrix still having rank r. A rank-deficient matrix need not have every index variable.

### Theorem 1: pointwise criterion

The complete projected velocity (pdot_1,…,pdot_k,qdot) is independent of w∈W_s if and only if

    a_j=C(p_j)J_j=0 for every variable index j.      (5)

Proof. Equation (2) has no w dependence. In (1), h,p_j,a_j are fixed on the fibre; its only possible dependence is a_j/w_j. If w_j takes two distinct values, equality of that entire p_j vector velocity forces a_j=0. Conversely, (5) removes all variable denominators, while each remaining w_j is fixed throughout the fibre. This establishes both directions. ∎

There is no cancellation between different j slots: all conditional laws are retained separately. The equivalence C(p_j)J_j=0 ⇔ the p_j-slot differential vanishes intrinsically uses strict positivity of p_j. Boundary support strata require a separate analysis.

### Partial-variable control

For r=k=3 take

    p_1=p_2=(1/2,1/4,1/4),   p_3=(1/4,1/4,1/2).

Then ker Q=span{(1,−1,0)}. Only w_1,w_2 vary. At this signature the local objective J=p_{3,1} satisfies (5), even though C(p_3)J_3≠0. Thus “every conditional derivative must vanish whenever a fibre is nontrivial” is false pointwise. The global k>r result requires its density argument; it is not that false stronger pointwise claim.

## 5. From the criterion to actual maximal flow, for every k,r

Let J be C². Then V is C¹ on the positive joint simplex, so it has a unique maximal local source flow. Assume (5) at every admissible signature.

Take any equivalent source points μ,ν. Their positive rows have identical conditionals, so

    ν=T_λ μ,   (T_λ z)_{j,i}=λ_j z_{j,i},
    λ_j= w_j(ν)/w_j(μ)>0.

They also have the same target marginal. Define the affine slice, relative to the positive joint simplex,

    K_λ={z: Σ_j(λ_j−1)z_{j,i}=0 for each target i}.

For every z∈K_λ, T_λz is another positive normalized joint law with the same signature: row conditionals are unchanged, the slice equations preserve q, and summing them preserves total mass. Whenever λ_j≠1, its j-th audit weight differs, so (5) gives a_j(F(z))=0.

Apply (4). On K_λ,

    Σ_j(λ_j−1)V_{j,i}(z)
      = −(h_i−⟨q,h⟩)Σ_j(λ_j−1)z_{j,i}
        −Σ_j(λ_j−1)a_{j,i}=0.                       (6)

Thus V is tangent to the affine slice. The same vanishings give

    V(T_λz)=T_λ V(z) on K_λ.                        (7)

Tangency and C¹ source uniqueness make K_λ invariant for every source trajectory starting there. One may see this without a global quotient theorem: restrict V to the embedded affine submanifold K_λ, solve there locally, and use source uniqueness; since K_λ is relatively closed in the source and has no new boundary inside it, this persists throughout the source maximal interval.

Equations (6)–(7) imply T_λΦ_τ(μ)=Φ_τ(ν) on the initial common interval, hence equality of their signatures there. Their maximal intervals coincide. Precisely, T_λ maps K_λ bijectively onto K_(1/λ), which is invariant by the same argument. If one curve extended further, T_λ or its inverse would transfer that extension to the other, remaining positive, normalized, and in the appropriate slice. Uniqueness would contradict its maximality.

Conversely, equality of projected source trajectories from every equivalent pair even for a common neighborhood of time zero implies equality of their initial derivatives, hence (5). Therefore:

### Theorem 2: global velocity and flow equivalence

For every r,k≥2 and ambient C² J, condition (5) at all s∈S is equivalent to representative-independent projected velocity everywhere and to descent of the actual maximal source flow with matching maximal time intervals.

This is an actual-flow theorem, not a claim that a separately chosen metric on S has this gradient. It does not by itself give continuity of velocity or of a two-sided flow in the ordinary subspace topology of S. If the abstract quotient X/~ is given its quotient topology, the descended maximal flow is continuous: id_R×π is quotient because R is locally compact Hausdorff, its source-flow domain is open and saturated by the matched maximal intervals, and the continuous source flow factors through it. None of this makes the quotient a manifold.

The audit-row-rescaling proof was supplied by the independent finite-audit worker and checked here. Its conclusion is included as a mathematical contribution; the presence of a worker called a reviewer does not independently certify its own added theorem.

## 6. Global rigidity when k>r

The full-domain and ambient-regularity assumptions are load-bearing.

### Lemma 3: dense signatures with every index variable

Suppose k>r. Conditional matrices Q for which every r-column minor is nonzero are dense in the product (Δ_r°)^k. For each such Q, deleting any one column leaves at least r columns and rank r; hence every index is variable.

Proof of existence and density. Choose distinct rational t_j∈(0,1) and a sufficiently small δ>0. Set, for i=1,…,r−1,

    p_i(t)=1/r+δt^i,
    p_r(t)=1/r−δΣ_(i=1)^(r−1)t^i.

Taking 0<δ<1/[r(r−1)] makes every coordinate positive. The column p(t) is an invertible linear transformation of (1,t,…,t^(r−1))ᵀ: its constant vector is (1/r)1 and its other coefficient vectors are δ(e_i−e_r), which are linearly independent. Vandermonde determinants therefore make every r-column minor of the resulting Q* nonzero.

Given any positive Q, let Q_ε=(1−ε)Q+εQ*. Each r-column determinant is a polynomial in ε, nonzero at ε=1; hence it has finitely many zeros. There are finitely many minors. Arbitrarily small positive ε avoid all of their zeros, and positivity holds for 0≤ε≤1. This proves density in conditional-matrix space.

To obtain density in S, do not hold q fixed while making arbitrary column perturbations. Choose one positive representative w of the original signature and set q_ε=Q_εw. Then (Q_ε,q_ε)∈S and converges to (Q,q). This proves the exact needed admissible-signature density. ∎

The full-spark condition is a convenient sufficient dense condition, stronger than necessary. It is not asserted of every Q.

### Theorem 4: exact k>r classification

For k>r and J∈C¹(A), the following are equivalent:

(a) The projected negative source Fisher velocity is independent of every positive weight fibre.

(b) C(p_j)J_j=0 at every s∈S and every j.

(c) There is a C¹ function φ:Δ_r°→R with J(P,q)=φ(q) on S.

If J is C², φ is C², and these conditions are also equivalent to the actual maximal-flow descent of Theorem 2.

Proof. (a)⇒(b): on the dense signatures of Lemma 3, all indices are variable, so Theorem 1 forces every a_j to vanish. Continuity of the a_j extends those vanishings to all S.

(b)⇒(c): define φ(q)=J(q,…,q,q). For any s=(P,q)∈S choose a positive representative w and use the contraction

    p_j(u)=(1−u)p_j+u q,   0≤u≤1.

Every p_j(u) is positive and Σ_jw_jp_j(u)=q. Thus the entire path stays in S at the same fixed q, ending at (q,…,q,q). Its derivative in slot j is q−p_j, a simplex tangent vector. By (b), J_j is constant across target coordinates and therefore annihilates that derivative. The chain rule gives dJ(P(u),q)/du=0. Hence J(P,q)=φ(q). Composition with the diagonal makes φ C¹, or C² if J is C².

This contraction also proves the fixed-q signature slice is star-shaped about the all-equal conditionals, despite the possibility that different signatures need different representing weights. It supplies the required global connectedness directly. No assertion that an arbitrarily restricted signature domain is connected is used.

(c)⇒(a): the source pullback is exactly E(w,P)=φ(Qw). Its intrinsic source Fisher gradient is therefore the target-only gradient, independently of how J was extended away from S. The explicit equations in §7 are independent of w after projection. This proves (a). Theorem 2 supplies the C² flow equivalence. ∎

No claim is made that J=φ(q) away from S. In fact there are ambient regions where q lies outside the convex hull of P, and a smooth function supported there is invisible to the pullback. The classification is exactly on the admitted image, or equivalently of source objectives E arising from this signature.

## 7. Positive target tilts and closed current-target dynamics

For E=φ(q), let h(q) be any representative of its intrinsic differential. Equations (1)–(2) reduce to

    wdot_j=−w_j⟨h(q),p_j−q⟩,
    pdot_j=−C(p_j)h(q),
    qdot=−C(q)h(q).                                  (8)

The projected (P,q) equations are C¹ on all A when φ is C². They give a regular closed signature ODE, and not merely a set-theoretic descended vector field.

For any strictly positive vector ℓ∈R^r, define

    Z_p(ℓ)=Σ_i ℓ_i p_i,
    L_ℓ(p)=diag(ℓ)p/Z_p(ℓ).

Multiplying every source cell with target i by ℓ_i and normalizing gives

    μ'_(j,i)=ℓ_i μ_(j,i)/Z_q(ℓ),
    p'_j=L_ℓ(p_j),   q'=L_ℓ(q),
    w'_j=w_j Z_(p_j)(ℓ)/Z_q(ℓ).                     (9)

These are strictly positive normalized laws. The signature update uses only P,q; it preserves the posterior-only equivalence. Composing ℓ and m multiplies them coordinatewise, and 1/ℓ gives the inverse. A common positive scalar factor in ℓ has no effect. Thus these tilts supply a smooth group action on S induced by ambient simplex diffeomorphisms. They also preserve rank Q and the set of variable indices, since Q' is obtained from Q by invertible positive row and column diagonal scalings.

For the gradient trajectory, put

    u_i(τ)=∫_0^τ h_i(q(s)) ds,   ℓ_i(τ)=exp(−u_i(τ)).

Use (9) on the initial joint law. Direct differentiation yields (8). Since q solves the closed C¹ target equation, ℓ is finite and strictly positive on each compact subinterval of the target maximal interval. Formula (9) lifts that entire interval to a source solution. Conversely any source extension projects to a target extension. Therefore the target, source, and admissible signature trajectories have the same maximal interior interval; all representatives have identical signature trajectories.

The ambient signature ODE stays in S as long as its q trajectory stays interior: the positive formula (9) proves this, without presupposing invariance from a set-theoretic quotient argument. Its flow is continuous in the ordinary signature subspace topology on its open maximal domain.

These claims are local/interior unless completeness is separately established. If h can be chosen bounded over Δ_r°, the exponential factors stay finite and nonzero on every bounded time interval, giving complete source and signature flows. More generally bounded coordinate differences of h suffice after changing the scalar gauge. Arbitrary C² φ need not satisfy this. For φ(q)=log q_1,

    qdot_1=−(1−q_1),
    q_1(τ)=1−(1−q_1(0))e^τ,

which reaches zero at the finite positive time log[1/(1−q_1(0))]. No interior extension is claimed beyond it.

The tilt is an expressly defined mathematical operation repertoire whose compatibility was just proved. It does not license arbitrary new evidence channels, actual auditing actions, or empirical interpretation of the chosen objective.

## 8. Sharpness for every k≤r

Let 2≤k≤r and define the polynomial

    J(P,q)=H(P)=det(QᵀQ).                            (10)

By Cauchy–Binet,

    H(P)=Σ_(I⊂{1,…,r}, |I|=k) det(Q_I)².

When rank Q<k every summand determinant vanishes, so the entire first differential of H is zero. It follows that J_q=0 and J_j=0 at every rank-deficient P. The weight fibre is nonsingleton exactly when ker Q≠0, equivalently rank Q<k. Thus every nonsingleton source fibre is stationary. At rank Q=k every fibre is a singleton. Theorem 1 gives global velocity descent, and Theorem 2 gives actual maximal-flow descent.

There is also a direct completeness check. J_q=0 implies wdot=0. For each fixed strictly positive w, the conditional field is

    pdot_j=−C(p_j)∇_(p_j)H/w_j.

The derivatives of the polynomial H are bounded on the product of closed simplexes. Consequently each d log p_(j,i)/dτ is bounded by a finite constant depending on w. No p_(j,i) reaches zero in finite positive or negative time. The closed product is compact, and the positive field therefore extends for all real times. All rank-deficient source points are equilibria; source uniqueness also prevents a nonstationary trajectory from reaching such a point at a finite interior time.

The objective is not a function of q. Let q be any interior target and choose k affinely independent tangent perturbations v_j with Σ_jv_j=0, possible because k−1≤r−1. For sufficiently small ε>0,

    p_j=q+εv_j,   w_j=1/k

are positive, their average stays q, and the k columns have rank k. To see the last claim, Σ_j a_jp_j=0 implies Σ_j a_j=0 by summing target coordinates, then Σ_j a_jv_j=0; affine independence forces every a_j=0. Hence H>0. At the all-equal p_j=q with the same current target, H=0. This proves genuine conditional dependence at fixed q.

At r=k=2, writing p_1=(1−a,a), p_2=(1−b,b), one obtains det(QᵀQ)=det(Q)²=(b−a)², the binary contrast up to the conventional factor 1/2. For k>r the same determinant is identically zero, so it does not contradict the rigidity theorem. The threshold is exactly k>r for this full-domain classification; generic injectivity when k≤r explains why the condition has room for these objectives.

No general classification for k≤r is asserted beyond Theorems 1–2. Nor is ordinary-signature velocity continuity claimed for the determinant example: binary contrasts already warn that actual source-flow descent can be weaker than that regularity contract.

## 9. Decisive controls and the connection to inquiry value

### Three audit outcomes obstruct a conditional gradient

For r=2,k=3, take

    p_1=(1/4,3/4), p_2=(1/2,1/2), p_3=(3/4,1/4),
    w=(1/4,1/2,1/4),   w'=(1/8,3/4,1/8).

Both signatures have q=(1/2,1/2). Every joint cell is positive. Let J=p_(1,1). Then h=0, J_1=(1,0), and the other conditional derivatives vanish. Here

    a_1=(3/16,−3/16).

Equation (1) gives pdot_1=(−3/4,3/4) at w and (−3/2,3/2) at w'. Meanwhile both have qdot=(−3/16,3/16). Equal current-target velocity does not suffice: the retained future conditional answers have different velocities. The binary contrast between p_1 and p_3 likewise fails to descend in this three-audit setting, because its nonzero conditional derivatives meet variable weights.

For the half-Brier Bayes risk H(p)=(1−||p||²)/2, the same source pair has expected audit gains 1/32 and 1/64. This replays the inherited strictly positive inquiry-value obstruction, rather than claiming a new score example. The shared weight kernel is the common source of the two failures, but their tests differ:

- An expected fixed quantity bᵀw descends iff b annihilates ker Q, equivalently b lies in rowspan Q.
- The projected conditional Fisher speed contains separate reciprocal factors a_j/w_j, so it requires a_j=0 on every variable index.

A conditional-answer quotient therefore does not automatically preserve either expected inquiry policy value or the full-source Fisher dynamics of a conditional-answer loss. These are two stronger, distinct contracts.

### The full-source cometric still forces all audit weights back

For any retained conditional coordinate p_(j,i), its squared full-source Fisher gradient norm is

    n_(j,i)=||grad_g p_(j,i)||²=p_(j,i)(1−p_(j,i))/w_j.  (11)

Strict positivity and r≥2 make the numerator strictly positive. Thus F together with that norm determines w_j exactly. Preserving the norms for any fixed target coordinate i across k−1 audit labels recovers the remaining weight by normalization, hence recovers every joint cell. In particular an arbitrary record that preserves F and the full-source cometric on all retained observables must be injective on X. No smoothness or special record codomain is needed for that injectivity argument.

This is an explicit generalization of the binary norm reconstruction, not a minimal-probe optimization campaign. Assigning a different reduced metric changes the contract and is not prohibited by (11). Audit frequencies remain unnecessary for the original posterior-answer-only operation repertoire.

## 10. Assumptions that cannot be silently relaxed

- The source contains all strictly positive joint laws, with labelled conditional laws free to vary. On a constrained reachable family, replace ker Q by actual admissible weight differences in the pointwise test; the generic-density argument may fail entirely. On a chosen one-weight section the fibres are all singletons, so equality of projected speeds at that section imposes no fibre comparison. For a concrete invariant restriction, fix k=3,r=2 and w=(1/3,1/3,1/3), and take J=p_(1,1). Then h=0 makes wdot=0 everywhere: the fixed-weight section is invariant and its signature is injective, so its actual flow descends there despite genuine conditional dependence at fixed q. This does not satisfy descent over the unrestricted full-domain fibres. Merely splitting one audit label into constrained duplicate outcomes does not invoke density in the larger unrestricted family and does not change a fixed empirical model. Moreover, the full-source Fisher gradient need not stay inside any such restriction; an induced restricted-model gradient is a different construction. No flow theorem on a noninvariant restriction is inferred.
- Positivity supplies every sufficiently small kernel direction, makes C(p) nondegenerate on simplex tangents, keeps every audit outcome feasible, and validates division by w_j. Zero cells and null audit outcomes require support-sensitive strata and explicit impossible-event handling.
- J is an ambient C¹ function for the classification, and C² for the stated unique C¹ source-flow theory. A discontinuous, merely stratum-wise specified, or otherwise irregular objective is outside this result.
- The condition is global on S. A pointwise or one-signature coincidence of speeds does not imply equality of later trajectories unless the condition continues to hold along the relevant states.
- The metric is the categorical Fisher metric of the full joint law and the loss is J∘F. A product metric that independently weights conditional slots, or an independently stipulated coarse Fisher metric, answers a different question.
- The declared fixed audit is not a family of newly redrawn experiments, and P(D|Θ) is not fixed while varying w. The kernel fibre keeps P(Θ|D) and P(Θ) fixed. If a forward channel or legal operation family is fixed additionally, its actual admissible source family must be checked again.
- Ordinary signature topology, abstract quotient topology, infinitesimal projectability, actual source-flow descent, and existence of a reduced Riemannian metric are distinct. The current-target case has the stronger regular signature ODE, but that does not retroactively establish it for all k≤r controls.
- No actual epistemic warrant, source calibration, psychological implementation, theological conclusion, new authorized action, or field-wide novelty follows from these finite equations.

## 11. Verification boundary

Run `python3 verify.py` from this directory. The portable script uses only Python's standard-library rational arithmetic and checks copied-input integrity. Optionally pass `--original-root PATH` to recheck the two fixed inherited originals. The moving binary draft is reported as a provenance comparison only; a later change is not treated as corruption of the copied snapshot or as a reason to update it silently.

The exact controls compare the Fisher equations against an independently computed categorical-cell gradient; check simplex gauges, the total covariance and energy identities, variable-index/kernel criteria, the partial-variable countercontrol, the three-outcome failure and score gains, target tilt commutation and composition, positive full-spark examples, determinant sharpness and stationary rank loss, row-rescaling tangency/equivariance, and norm reconstruction. The author run with inherited-original checks passed 1,775 assertions across 30 groups; the portable run passes 1,773 across 29 groups. CONTROL_RESULTS.json records the author run and counts. Finite controls corroborate but do not replace the universal density, connectedness, ODE, and maximality proofs above. They are not Lean proofs, independent review, or an empirical experiment.
