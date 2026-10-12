# Reference geometry: exact deterministic gradient descent classification

11 October 2026 UTC. Bounded mathematical continuation. Ordinary proof and exact symbolic controls, not formal-kernel certification. No protected edits, repository adoption, empirical/noetic identification, external novelty, or programme closure claimed.

## Result

For the transported-reference separable family below, universal same-time natural-gradient commutation through deterministic partitions holds exactly when reciprocal curvature is affine. Equivalently, only that class has an autonomous projected field for every objective, every reference and every deterministic partition on the unrestricted positive simplex. This is stricter than the inherited divergence-contraction condition, which permits every concave reciprocal curvature. The normalized power family contracts for 1<alpha<2 but fails even autonomous deterministic descent.

## 1. Setting and intrinsic mobility

Let phi be C³ on (0,infinity), with phi''>0, and set r=1/phi''. For a fixed positive reference vector mu, not necessarily normalized, define

    f_mu(p)=sum_i mu_i phi(p_i/mu_i),
    h_p(u,v)=sum_i u_i v_i/[mu_i r(p_i/mu_i)],
    w_i=mu_i r(p_i/mu_i), S=sum_i w_i,
    G_w=diag(w)-ww^T/S.

Here p is a strictly positive probability law, and u,v have zero total mass. This is the inverse tangent metric, not the unconstrained inverse Hessian. Indeed G_w g has zero total mass and

    diag(1/w) G_w g = g-1(w^Tg)/S,

whose pairing with any zero-mass v is g^Tv. Thus gradient descent on a pulled-back objective J(p)=Jbar(Kp) is

    pdot=-G_w K^T g, g=dJbar_(Kp).

Covectors are modulo constants; all displayed cometrics annihilate constants, so linear objectives realize all relevant tests. The reference is fixed throughout the flow, not reset to p.

Let K be a deterministic surjective partition matrix, with one 1 per input column and no empty output. Put q=Kp, nu=Kmu and

    W=Kw, V_j=nu_j r(q_j/nu_j).

Since K diag(w) K^T=diag(Kw) and sum W=sum w,

    K G_w K^T=G_W.                                    (1)

Consequently projected fine descent is -G_W g, whereas canonical coarse descent for f_nu is -G_V g.

## 2. Universal classification

The following are equivalent, with quantification over all finite dimensions, positive references and probability states, surjective deterministic partitions, and C² coarse objectives:

(A) Projected fine and canonical coarse vector fields agree in the same time parameter.
(B) Every pulled-back objective admits a projected vector field depending only on q, not the selected positive lift p in its fibre.
(C) r(t)=a t+b on (0,infinity), where a,b>=0 and a+b>0.

It suffices in (A) or (B) to test the 3-to-2 partition merging the first two coordinates and retaining the third, while allowing mu to vary. Requiring mu itself to be a probability law does not weaken the theorem.

### (C) implies (A)

If r(t)=at+b, then w=ap+bmu and W=aq+bnu=V. Equation (1) gives equality. (A) implies (B) immediately.

### (B) implies (A)

For fixed mu, K and q, the fibre has the positive reference-aligned lift

    p*_i=mu_i q_j/nu_j, i in block j.                  (2)

At that lift, all block density ratios agree and W*=V. If projected velocities are independent of the fine lift for every objective, they equal the canonical velocity witnessed at p*. This also proves the fixed-partition equivalence between all-objective autonomous descent and canonical commutation, without changing any parameters.

### (A) implies (C): binary mobility and a probability buffer

For a two-output partition, G_(x,z)=[xz/(x+z)] L, where L=[[1,-1],[-1,1]]. The unmerged singleton has W_2=V_2=z>0. Equality of cometrics thus forces

    W_1 z/(W_1+z)=V_1 z/(V_1+z), hence W_1=V_1,

because the scalar map x -> xz/(x+z) is strictly increasing on x>0.

Fix arbitrary x,y>0 and 0<lambda<1; put X=lambda x+(1-lambda)y. Choose 0<epsilon<min(1,1/X) and set

    mu=(epsilon lambda,epsilon(1-lambda),1-epsilon),
    p=(epsilon lambda x,epsilon(1-lambda)y,1-epsilon X).

Both vectors are positive probability laws. The singleton weight is unchanged and positive. Equality W_1=V_1 reduces to

    lambda r(x)+(1-lambda)r(y)=r(lambda x+(1-lambda)y).

All x,y,lambda are arbitrary. This all-weight Jensen equality makes r affine (continuity is already provided by phi in C³). Positivity on the whole positive half-line forces a>=0 and b>=0, not both zero: a<0 fails at infinity, and b<0 fails near zero. This proves the theorem.

The vector-field assertion yields equality of flows on their common interval of positive existence by local uniqueness: r is C¹ and Jbar is C². No global interior existence or boundary extension is asserted. Same-time equality matters; a scalar speed comparison is weaker.

## 3. Exact generators and inherited contraction classification

Modulo an arbitrary affine function of t, integrating phi''=1/(at+b) gives

- a=0, b>0: phi(t)=t²/(2b), the weighted quadratic family.
- a>0, b>=0: phi(t)=[(at+b) log(at+b)-(at+b)]/a².

For b=0 this is a positive multiple of t log t modulo affine terms. For a,b>0 it is shifted entropy. All these have affine, hence concave, r and belong to the inherited reference-Bregman contractive class.

For a>0 this shifted-entropy geometry also has a simple affine-blend interpretation. Put M=a+b sum_i mu_i and s_p=(ap+bmu)/M, a probability vector. Direct substitution yields

    h_p=(M/a²) (pullback of the Fisher metric under p -> s_p),
    D_mu^phi(p,q)=(M/a²) KL(s_p || s_q).

When b>0 the image is a restricted subset of the simplex with s_i>b mu_i/M. The reference blend is stipulated geometric data, not acquired evidence. In particular, equality/recovery statements for the blended laws must not be silently promoted to recovery of the original pair p,q without also controlling the reference. The earlier strictly-concave-r pairwise-recovery argument does not apply to affine r.

For normalized power generators with phi_alpha''(t)=t^(alpha-2), r(t)=t^(2-alpha). For 1<alpha<2, r is strictly concave and nonaffine. Their transported Bregman divergences contract under every stochastic K by the inherited theorem, but universal deterministic gradient descent already fails here. The endpoints alpha=1 and alpha=2 satisfy the present theorem. This does not classify arbitrary nonseparable potentials or unadorned simplex geometries.

## 4. Actual same-fibre velocity collisions

Use phi(t)=(4/3)t^(3/2), which has phi''(t)=t^(-1/2) and r(t)=sqrt(t). This differs from the affine-normalized power generator only by an affine term. Let K merge coordinates 1 and 2, retain coordinate 3, and take Jbar(q)=q_1.

### Root-supplied simple reference

    mu=(1,1,2), nu=(2,2),
    p=(1/100,49/100,1/2), p'=(1/4,1/4,1/2),
    Kp=Kp'=(1/2,1/2),
    w(p)=(1/10,7/10,1), w(p')=(1/2,1/2,1).

Thus W(p)=(4/5,1), W(p')=(1,1), and V=(1,1). Their binary mobilities are 4/9 and 1/2. The actual projected velocities at the same coarse state are

    K pdot=(-4/9,4/9), K p'dot=(-1/2,1/2).

There is no autonomous q-only vector field for this single linear objective that covers both fine states. This conclusion is independent of how one might choose a different canonical coarse metric.

### Independent probability-reference control

With exactly the same p,p',K,Jbar, use the normalized reference

    mu=(1/100,1/100,49/50), nu=(1/50,49/50).

Then w(p)=(1/100,7/100,7/10), w(p')=(1/20,1/20,7/10), and V=(1/10,7/10). The projected velocities are

    (-14/195,14/195) and (-7/80,7/80),

respectively. Hence the obstruction does not rely on nonnormalized reference mass. These two-dimensional velocities are collinear, so this fixture establishes failure of same-time autonomy, not failure of every possible trajectory time change. No such stronger assertion is needed.

## 5. A valid restricted-state remedy for every r

For any admissible phi, fix mu and K and restrict to the reference-aligned section (2). At such a state w_i=mu_i r(q_j/nu_j). Writing c=(W^Tg)/(sum W), the fine field satisfies

    pdot_i=-mu_i r(q_j/nu_j)(g_j-c), i in block j,
    qdot_j=-nu_j r(q_j/nu_j)(g_j-c).

Therefore pdot_i=(mu_i/nu_j)qdot_j, proving tangency and invariance of the section for every pulled-back objective. The projected flow is exactly the canonical coarse flow there. This is a conditional restriction with a fixed supplied within-block law, not a repair for arbitrary fine states. An arbitrary fixed section with different block proportions need not be invariant for general r.

Retaining additional state, the actual fine law, or a separately supplied model can also change the question. Pointwise quotient metrics exist at each fine point, but the collision shows they need not define one coarse geometry independent of the lift. None of these mathematical options authenticates an objective, reference, evidence source or actual noetic target.

## 6. Full stochastic comparison inside the contractive class

Here assume additionally that r is concave, exactly the inherited divergence-contractive class. Let K be any nonnegative column-stochastic matrix with no zero row. Define w as before, W=Kw and V_j=(Kmu)_j r((Kp)_j/(Kmu)_j). Rowwise Jensen gives V>=W componentwise. Unlike a deterministic partition, K diag(w) K^T need not be diagonal. The exact decomposition is

    G_V-K G_w K^T = (G_V-G_W)
                         + [diag(Kw)-K diag(w) K^T].   (3)

Both terms are positive semidefinite. For the first, set d=V-W>=0, c_W=(W^Tg)/(sum W), c_V=(V^Tg)/(sum V). Expanding weighted squares gives

    g^T(G_V-G_W)g
       =sum_j d_j(g_j-c_V)^2+(sum W)(c_V-c_W)^2.       (4)

For the second, writing k_i for column i gives

    g^T[diag(Kw)-K diag(w)K^T]g
       =sum_i w_i Var_(k_i)(g).                       (5)

These are pointwise mobility/dissipation identities at a common state, not comparisons of later equal-time trajectories.

For m>=2 outputs, equality of projected and canonical fields for every objective at the specified p,mu,K holds iff K is deterministic and W=V. To prove necessity, equality in the sum of positive semidefinite terms forces both terms zero. If d_j>0, take g=e_j. Since V is strictly positive and m>=2, 0<c_V<1 and the j term in (4) is strictly positive, a contradiction. Thus d=0. Equality of the second matrix forces deterministic columns: its trace is sum_i w_i(1-sum_j K_ji²), a sum of nonnegative terms with strictly positive weights. Sufficiency follows from (3).

If r is strictly concave, W=V for a deterministic K holds exactly when p_i/mu_i is constant on each merged block. Thus for interior powers, the reference-aligned section is exactly the state locus where every objective canonically commutes through a given deterministic partition. If r is affine, V=W for all p and every stochastic K, and (3) reduces to the inherited channel-variance theorem: all-objective commutation holds exactly for deterministic K. For a merely concave r with affine subintervals, retain the precise rowwise Jensen-equality condition rather than incorrectly requiring all densities equal.

For a single objective at the specified state, agreement is equivalent to the sum of the three nonnegative expressions in (4)–(5) being zero, equivalently each being zero. This criterion may hold even when the full matrices differ. For m=1 both tangent fields vanish automatically; one must not conclude V=W from their equality. K then is deterministic, but Jensen may be strict. No classification of a fixed noisy channel for arbitrary nonconcave r is claimed.

## 7. Ancestry, deduplication, attribution and verification

The local depth-two RESULT.md scan for affine reciprocal curvature, shifted entropy and same-fibre velocity found the inherited leafwise report's attribution of the Fisher noisy-channel collision; it found no prior report of this deterministic reciprocal-curvature classification. This is a bounded deduplication check, not a field novelty search.

- reference-bregman-classification-20261011/RESULT.md supplies the transported-reference family, exact concave-r divergence iff, normalized-buffer method, power family and Bauschke–Borwein/Chafai attribution. Its explicit separation of divergence contraction from gradient projectability is preserved.
- noetic-gradient-transport-20261009/RESULT.md §§2–5 and 8 supplies the affine-constrained inverse-Hessian formula, constant-quadratic partition/noise discriminator and pointwise quotient interpretation. Its primary ancestry is Alvarez, Bolte and Brahic, Hessian Riemannian gradient flows in convex programming, §2.2 equations (7)–(10): https://arxiv.org/pdf/1811.10331 . This packet specializes the inherited formula with w_i=mu_i r(p_i/mu_i), rather than claiming new natural-gradient machinery. No additional external source was necessary for this direct derivation; no newly checked primary reading is claimed.
- state-dependent-gradient-obstruction-20261009/RESULT.md §§2–4 supplies the all-objective fibre-constancy criterion and a Fisher collision through a noisy channel, with deterministic Fisher positive control. The present collision is different: a deterministic merge already fails for a contractive nonaffine r.
- leafwise-noetic-geometry-20261010/RESULT.md supplies conditional Fisher exponential-leaf remedies with retained reference-class information. The present section is the explicit reference-aligned partition specialization generalized by direct calculation to all admissible r. The general conditional-model principle is inherited.

The root supplied the affine iff candidate, binary-singleton/Jensen-buffer necessity strategy, the unnormalized-reference fixture, the invariant-section observation and the concave-r stochastic decomposition with its weighted-square identity, and the affine-blend interpretation. This worker independently derived them, strengthened the theorem to universal autonomous descent using the section, and supplied the normalized-reference collision. These are workflow attributions, not priority claims.

verify.py checks the symbolic tangent duality and binary injectivity, the normalized Jensen embedding, affine transport through every one of the 8 three-input binary deterministic partitions (nonempty ones for the two-output test), both radical-to-rational collisions, generator integrations, invariant-section formula, a noisy affine-r variance identity, the general weighted-square gap identity, and the affine-blend Fisher/Bregman identities. Finite controls supplement the all-input proofs. All inherited input bytes and report/control bytes are bound in INPUT_BINDINGS.json and MANIFEST.json. Boundaries remain strict positivity, finite dimensions, fixed supplied references, pulled-back objectives and common interior existence; no rate campaign or protected-source mutation was undertaken.
