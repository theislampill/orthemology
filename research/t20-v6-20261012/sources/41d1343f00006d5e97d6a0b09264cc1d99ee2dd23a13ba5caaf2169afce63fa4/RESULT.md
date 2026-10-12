# Face-stratified completion of a finite exponential leaf

10 October 2026 UTC. Separate scratch mathematical continuation. Ordinary finite proofs and executable exact controls; no protected-source edit, integration, formal-kernel certification, empirical identification, actual cognitive warrant, implementation-failure allegation, or programme closure. The parent supplied the proposed boundary and zero-likelihood questions, the log-expectation necessity route, and the support-sensitive countercontrol. This packet gives proofs, qualifications, and replayable examples. Its verification is author verification, not independent review.

## 1. Result and precise addition

For a finite observable space retaining mass, fix a strictly positive reference r. The closure of its positive exponential leaf is exactly the disjoint union of its finite-parameter exponential families on the **column-saturated faces of the global moment polytope**. Each face has its own minimal affine coordinates. Those coordinates have a positive Fisher metric, including where the old ambient covariance becomes singular. Every feasible mean has a unique relative-entropy completion, positive at every supplied atom on its minimal face.

That completion is selected by r. It need not be the unknown law that produced the mean. A support-changing observation can even leave the mean in the global polytope interior while producing a law outside the old leaf closure.

The exact Bayesian boundary test is as proposed. For nonzero L >= 0 and a finite full-support member p_(r,theta),

    B_L(p_(r,theta)) belongs to closure(E_r)
      iff S=supp L is a saturated facial support of P
          and log L restricted to S belongs to V restricted to S.       (1)

It holds at one finite theta if and only if it holds at every finite theta, and then preserves the entire closed model on every positive branch. Consequently every nonnegative likelihood on a fully retained local scope, including hard zeros, preserves this closed fixed-reference model. The support condition alone is insufficient. Conversely, arbitrary L always gives a positive leaf on the retained support with reference rL; that reference/support is additional model data, not free information discarded by taking a mean.

### Inheritance and nonclaims

The exact direct inputs and portable snapshots are bound in INPUT_BINDINGS.json.

- `leafwise-noetic-geometry-20261010/RESULT.md`, §§6–10, already proves the positive full-support leaf, global-interior mean coordinates, entropy selection, Fisher geometry, and positive-likelihood preservation. These are inherited. Its exclusion of support changes is correct.
- `event-feasibility-descent-20261010/RESULT.md`, §§2–7, already classifies **zero-set** facial supports for all-prior event feasibility and supplies the pairwise global-facet/local-positivity example. Its independent review is included as provenance; it does not review the present extension.
- `hierarchical-marginal-core-20261010/RESULT.md`, §§1–4, already distinguishes all-prior common-core sufficiency from positive local updates on a fixed leaf. The all-zero-inclusive closed-model local corollary here extends that explicitly positive leaf comparison.
- `source-audit-revision-20261010/RESULT.md`, opening, §§2–4 and §8, already separates zero-probability conditioning, model revision, and the failure of inverse-factor recovery after a zero. Generic zero-event noninvertibility is not an addition here.

The bounded addition is the full face-stratified repair of the first packet's deliberately omitted boundary, its same-reference zero-likelihood iff, and the exact distinction between global faces, conditional-support charts, and event-feasibility zero faces. The mathematics of extended finite exponential families and entropy projections is classical; §9 records focused primary/classical attribution. No project-wide or historical novelty claim is made.

## 2. Setting, faces, and minimal coordinates

Let X be a nonempty finite set. Let

    V = span{1, phi_1, ..., phi_d} subset R^X

with the displayed functions linearly independent. Write phi(x) in R^d and

    M = [1; phi],    P = conv{phi(x): x in X}.

P has affine dimension d. For d=0 it is a point and all claims use the zero-dimensional conventions. An equivalent full-row-rank mass-retaining record can be changed to this basis without changing the claims. Supplied columns may repeat or lie inside a face rather than at its vertices.

Fix positive weights r_x. Normalizing r is optional. Put

    A_r(theta) = log sum_x r_x exp(theta·phi(x)),
    p_(r,theta)(x) = r_x exp(theta·phi(x)-A_r(theta)),
    E_r = {p_(r,theta): theta in R^d}.

Closure means ordinary Euclidean closure in the finite probability simplex; it is also total-variation closure here. For a nonempty face F of P, including F=P, define

    S_F = {x: phi(x) belongs to F}.

This is the **saturated** support: all atoms on F, including duplicate and nonvertex columns. Empty support is never the support of a probability law and is excluded from the union below.

Let D_F=span(F-F) and k_F=dim F. Choose any affine coordinate isomorphism psi_F: aff F -> R^(k_F), and use its evaluation at phi(x) for x in S_F. Then {1, components of psi_F} is a basis of V restricted to S_F: every global affine observable restricts to an affine function on aff F, and every affine function there extends to R^d. Define

    A_(r,F)(eta) = log sum_(x in S_F) r_x exp(eta·psi_F(phi(x))),
    q_(r,F,eta)(x) = 1_(S_F)(x) r_x exp(eta·psi_F(phi(x))-A_(r,F)(eta)),
    E_(r,F) = {q_(r,F,eta): eta in R^(k_F)}.             (2)

The normalization of r restricted to S_F changes A by a constant and changes neither family nor metric. In ambient parameters, coefficients that are constant on F are gauge directions; quotienting them is essential. When k_F=0, (2) is the single law proportional to r on all atoms having that vertex column, not an arbitrary point mass among duplicate atoms.

We use two elementary finite-polytope facts. Every z in P lies in the relative interior of a unique minimal face F(z). Every face is exposed. These facts also follow from any finite halfspace description: intersect the inequalities active at z; their sum exposes the resulting face and all remaining inequalities are strict at z within its affine hull. The inherited event-feasibility proof supplies an independent finite separating-functional proof for a saturated face.

## 3. Closure is exactly the face union

**Theorem 1 (finite facial closure).**

    closure(E_r) = disjoint union_(nonempty faces F of P) E_(r,F).        (3)

In particular, a law p belongs to closure(E_r) exactly when its support is some S_F and

    log(p_x/r_x), x in S_F, belongs to V restricted to S_F.              (4)

### Necessity: limiting log expectations identify the face

Suppose p_n=p_(r,theta_n) -> p, and set S=supp p. Define f_n(x)=log(p_n(x)/r_x). Each f_n belongs to V. On S it converges to the finite function log(p/r). On X\S it tends to -infinity. All its values are uniformly bounded above, since p_n(x)<=1 and min_x r_x>0.

If a law a is supported in S and b has the same retained mean, then

    sum_x a_x f_n(x) = sum_x b_x f_n(x),                 (5)

because f_n is retained and both laws have mass one. The left side has a finite limit. If b has any positive mass outside S, the right side tends to -infinity: at least one positive-weight summand does, and the remaining finitely many summands are bounded above. This contradicts (5). Consequently

    {b in Delta : Mb belongs to M Delta_S} = Delta_S.   (6)

The saturated-face lemma already proved in the event-feasibility input now applies, with S playing the role of the lemma's face index set: conv phi(S) is a face F and S=S_F. This is a geometric use of that lemma, not a claim that the original likelihood has the same zero set.

Finally V restricted to S is a finite-dimensional linear subspace of R^S and hence closed. Since f_n restricted to S converges, log(p/r) restricted to S belongs to it. Rewriting this affine function in the minimal coordinates psi_F and normalizing gives exactly (2). Thus p belongs to E_(r,F). This argument does not assume bounded original parameters or convergence of a chosen parameter subsequence.

### Sufficiency: expose the face and take a normal ray

Let q=q_(r,F,eta). Extend eta·psi_F from aff F to a global affine function c+theta_0·phi. Choose an exposing normal n and h with

    n·phi(x)=h on S_F,     n·phi(x)<h off S_F.

For F=P use n=0. Then

    p_(r,theta_0+t n)(x)
      = r_x exp(theta_0·phi(x)) exp(t(n·phi(x)-h))
        / sum_y r_y exp(theta_0·phi(y)) exp(t(n·phi(y)-h)).              (7)

As t tends to +infinity, terms off S_F vanish and terms on S_F remain. The limit is q. Thus every family in the right side of (3) lies in the closure. Different faces have different saturated supports, making the union disjoint. QED.

This also describes incidence: closure(E_(r,F)) is the union of E_(r,G) for the nonempty faces G of F, equivalently the faces G of P contained in F. Apply the same finite theorem on S_F. It does not produce an ordinary global smooth manifold across changes of dimension.

## 4. Every feasible mean has a unique completion, with its full minimal-face support

**Theorem 2 (boundary entropy completion).** For each z in P, let F=F(z). There is exactly one q_r(z) in closure(E_r) with mean z. It belongs to E_(r,F), has support S_F, and uniquely minimizes

    H_r(p) = sum_x p_x log(p_x/r_x)                     (8)

over all laws with E_p[phi]=z, with 0 log 0=0. If r is normalized, (8) is KL divergence to r; otherwise it differs by a constant. The map q_r:P -> closure(E_r) is a homeomorphism inverse to the mean map.

**Proof of existence, positivity, and the variational characterization.** Every law representing z is supported in S_F. Indeed an exposing functional of F has its extremal expectation at z; positive mass outside its extremal set would make that expectation strictly smaller.

There is also a representing law positive at every atom of S_F. Let b be the uniform barycentre of all those columns. Since z lies in relint F, a short extension y=z+epsilon(z-b) remains in F. Then

    z = [epsilon/(1+epsilon)] b + [1/(1+epsilon)] y

has a representation with positive mass at every atom of S_F. If z=b take its uniform representation directly. This includes duplicate columns and k_F=0.

The feasible fibre is nonempty, compact, and convex. H_r is continuous and strictly convex on the finite simplex, so it has a unique minimizer q. Suppose q has a zero coordinate in S_F. Mix it with the strictly positive feasible law a: q(t)=(1-t)q+t a. At every newly positive coordinate the contribution is t a_x log t+O(t); at coordinates where q_x>0 the change is O(t). Thus

    H_r(q(t))-H_r(q) = t log t sum_(x:q_x=0) a_x + O(t) < 0

for sufficiently small t>0. This contradicts minimality. Therefore q is positive on every atom of S_F.

All feasible infinitesimal directions h on S_F satisfy sum h=0 and sum h phi=0. Positivity permits both signs of a small perturbation, so first-order optimality gives

    sum_(x in S_F) h_x [log(q_x/r_x)+1] = 0.

Row/kernel duality, with mass retained, gives log(q/r) in V restricted to S_F. Hence q is in E_(r,F). Theorem 1 puts it in closure(E_r).

For any candidate q in that stratum with mean z, substituting its affine log ratio gives, for every p in the same fibre,

    H_r(p) = D_KL(p || q) + H_r(q).                    (9)

All p are supported in S_F, so this divergence is finite. KL nonnegativity and its equality case make q the unique minimizer. Thus there is exactly one closure member at z. Finally the mean map from compact closure(E_r) to compact P is a continuous bijection onto a Hausdorff space; its inverse is continuous. QED.

This proof treats the entropy selector and its full support directly; it does not assume that the actual unknown law is the selector. The same fibre may contain laws missing some or most of S_F. Duplicate columns further show that even an identifiable mean at a vertex can leave atom weights unknown; the selected weights are the r proportions.

### Finite relative parameters and the extended dual

The inherited positive-leaf theorem applies on S_F after affine redundancies are removed: eta -> E_q[psi_F] is a smooth diffeomorphism onto the relative-face coordinate image of relint F. Coercivity can also be read directly: a ball about the target in these k_F coordinates yields

    A_(r,F)(eta)-eta·z_F >= log min_(S_F) r + delta ||eta||.

Its positive covariance Hessian gives unique finite eta for every z in relint F. An ambient finite theta generally does not exist on a proper face.

Define the global conjugate A_r*(z)=sup_theta[theta·z-A_r(theta)]. For all z in P,

    A_r*(z)=H_r(q_r(z)).                                (10)

The inequality <= follows from H_r(p)=D_KL(p||p_theta)+theta·z-A_r(theta). For the reverse inequality, use the exposing ray (7) for q_r(z). Its limiting dual value is exactly H_r(q_r(z)); the common t h cancels because z lies in F. On a proper face the supremum is not attained at finite theta: equality would require q_r(z)=p_theta, contrary to support. The value in (10) is continuous on P because q_r and finite H_r are continuous. This supplies a continuous entropy potential, not a globally finite smooth inverse Hessian.

## 5. Positive geometry on each face, and the failure of a global inverse

Let z_F be the mean in the chosen minimal coordinates and q=q_(r,F,eta). Finite differentiation gives

    C_F(eta)=Cov_q(psi_F)=Hess A_(r,F)(eta).

For a nonzero a, a^T C_F a is the variance of a·psi_F. Since q is positive on all S_F, zero variance would mean this affine observable is constant on F, contradicting the minimal coordinates. Thus C_F is positive definite when k_F>0. The zero-dimensional stratum has the unique metric on its zero tangent space.

For a parameter variation d eta, the law variation is

    d q_x = q_x (psi_F(phi(x))-z_F)·d eta on S_F,
    d q_x = 0 off S_F.

The Fisher metric on this support simplex, sum_(S_F) (d q_x)^2/q_x, pulls back to C_F in eta coordinates and C_F^(-1) in mean coordinates. Equivalently, if psi_(r,F) is the face Legendre potential,

    g_F(u,v)=u^T C_F^(-1) v=u^T Hess psi_(r,F) v.        (11)

For a smooth objective J restricted to relint F, the exact fine Fisher gradient within this support simplex remains in E_(r,F), with

    eta_dot = -grad J(z_F),
    z_F_dot = -C_F(z_F) grad J(z_F),
    q_dot_x = -q_x grad J(z_F)·(psi_F(phi(x))-z_F).      (12)

This is the inherited positive-leaf calculation on the now correctly reduced chart; it is not another whole-simplex descent theorem. Normal covectors in ambient coordinates are gauge directions on the face.

The ambient covariance Cov_q(phi) has image D_F and kernel D_F perpendicular. The variance argument proves this exactly. It is positive on D_F and singular in every lost normal direction. Because q_r(z) is continuous, this ambient covariance extends continuously over all P as a positive-semidefinite field. Its ordinary matrix inverse does not extend as a finite positive-definite metric over proper faces. Stratum-wise inversion or coordinate reduction cannot be silently replaced by one nonsingular ambient inverse.

For example, on the independent two-bit leaf, C=diag(1-z_x²,1-z_y²). At z_x=1, z_y=1/3, the ambient covariance is diag(0,8/9); the relative edge metric is 9/8 in the z_y direction. The interior normal metric coefficient 1/(1-z_x²) diverges. Finite smooth parameter evolution within a stratum preserves its support; a zero-likelihood operation or a limiting process is a separate support change. No rule of automatic smooth crossing, global geodesic continuation, or change-of-support dynamical uniqueness follows from (11)–(12).

## 6. The exact zero-likelihood test and the necessary new model data

Let L>=0 be a nonzero likelihood weight and S={x:L_x>0}. A common positive rescaling changes neither posterior nor criterion; when an actual probability-valued channel outcome is intended, scale L to at most one and include its complementary outcome. Every finite p_(r,theta) has strictly positive event mass alpha_L(theta), so its posterior is well-defined and has support exactly S.

**Theorem 3 (same-reference closure preservation).** The following are equivalent:

1. B_L(p_(r,theta_0)) belongs to closure(E_r) for some finite theta_0.
2. B_L(p_(r,theta)) belongs to closure(E_r) for every finite theta.
3. S=S_F for a nonempty face F of P, and log L restricted to S belongs to V restricted to S.
4. B_L maps every member of closure(E_r) with positive branch mass into closure(E_r).

**Proof.** Theorem 1 forces the saturated face condition for any such posterior. On S,

    log(B_L(p_(r,theta))_x/r_x)
      = theta·phi(x)+log L_x-A_r(theta)-log alpha_L(theta).             (13)

All terms except log L are in V restricted to S. Thus the log-ratio condition in Theorem 1 holds exactly when log L restricted to S belongs to that space, independently of theta. This proves equivalence of 1–3. To obtain 4, take any current stratum E_(r,G). A positive branch has support S_F intersect S_G = S_(F intersect G), the saturated support of a nonempty face. The old log ratio and log L both restrict to retained affine functions on that intersection. Theorem 1 applies. Conversely 4 includes the full-support family and implies 1. QED.

If log L_x=c+b·phi(x) on S_F, the resulting member is the face family with ambient restricted parameter theta+b. In particular it is the limit of p_(r,theta+b+t n_F). Only the restricted values matter; there is no demand for a finite log L off S. Positive L recovers the previously proved whole-support condition and is not a new positive-leaf result. If L=0, the posterior is undefined and is excluded, rather than inserted as an empty-face probability.

The same statement extends to an already boundary prior q_(r,F,eta), provided its branch mass is positive: put T={x in S_F:L_x>0}. Its posterior lies in closure(E_r) exactly when T is a saturated support of a face G of F and log L restricted to T belongs to V restricted to T. Faces of F are global faces of P. Again, coordinates that never had prior mass are irrelevant, and the statement concerns all finite relative parameters in that fixed face.

### Constructive local evidence closure, including zeros

**Corollary 4.** On a finite product, suppose V contains every function of a coordinate scope D. Every nonzero nonnegative likelihood L(x)=ell(x_D) preserves closure(E_r) on every positive branch, without enlarging V or changing r. This applies to every retained scope in a downward-closed hierarchical marginal family.

**Proof.** The support indicator b(x)=1_(ell(x_D)>0) belongs to V. Its maximum set on the supplied columns is exactly S, so {z:E_z[b]=1} is a face with saturated support S. Define a D-function equal to log ell at positive values and, for example, zero at its zero values. It belongs to V and restricts to log L on S. Theorem 3 applies. QED.

Any finite sequence of such local updates therefore remains in the closed fixed-reference model whenever each selected branch is positive. Current support is recoverable there as S_(F(z)); support intersections may require new relative-face coordinates even while a global finite theta ceases to exist. Branch mass is already a linear function of the retained record because L belongs to V. The exact posterior record can be computed as

    z' = E_(B_L(q_r(z)))[phi].

This is an exact model-dependent map; it does not assert an efficient reconstruction or local marginal update formula. In particular it does not contradict the all-prior common-core theorem: the known fixed log-density class and membership in closure(E_r) are substantive additional restrictions. If different unknown laws with the same mean are allowed, even a hard unary event can give different retained posteriors. Section 7 and the verifier include such a control.

Preservation is not reachability. It does not say that every face in the closure is attainable by finitely many local hard observations; the inherited pairwise-facet example below separates those claims.

### Arbitrary likelihoods give a new conditional-support leaf

For every nonempty S, define the positive reference r'_x=r_x L_x on S, retain the restricted observables, and remove their affine redundancies. Direct normalization gives

    B_L(p_(r,theta))_x
      = 1_S(x) r'_x exp(theta·phi(x)) / sum_(y in S) r'_y exp(theta·phi(y)).  (14)

Thus all these posteriors lie in a well-defined positive exponential family over S, with moment polytope conv phi(S), whether or not S is facial in P. As theta varies, every member of that restricted family is obtained, because every affine function on aff phi(S) extends to the original ambient space.

- If S is nonfacial, no finite-parameter posterior in (14) belongs to the old closure: all have the forbidden support S.
- If S is facial but log L is not retained on S, (14) is a different reference class on that same face, also disjoint from the old stratum.
- If both tests pass, (14) is exactly the old face stratum.

A new support chart need not be a stratum of the old global P. Its relative interior can lie in the global interior. The pair consisting of the restricted mean and the declared support/reference class determines a member of the chosen conditional leaf. The mean alone can discard both the support and the residual log-density class. Allowing arbitrary reference changes therefore carries additional information and provides no free compression of an arbitrary unknown law. These model choices also do not authenticate a likelihood or confer epistemic warrant.

## 7. Exact controls that separate the possible repairs

### 7.1 Two diagonal events: unchanged means, different laws and metrics

Take X={-1,+1}², phi=(x,y), and uniform r. E_r is the independent product family and P=[-1,1]². From the uniform member, the events x=y and x!=y give

    q_+(x,y)=1_(x=y)/2,      q_-(x,y)=1_(x!=y)/2.

Both have z=(0,0), a global **interior** mean, and respectively E[xy]=+1 and -1. Their supports are opposite pairs of square vertices, neither a face. They cannot be old product-leaf limits: every such limit satisfies the closed polynomial identity

    p_(--) p_(++) = p_(-+) p_(+-),                       (15)

whereas each diagonal law has one side 1/4 and the other 0. Equivalently, a product law with both marginal means zero is uniquely the uniform law. The selected q_r(0,0) is that uniform law and has covariance I; the actual conditioned covariances are

    Cov_(q_+)(x,y)=[[1,1],[1,1]],
    Cov_(q_-)(x,y)=[[1,-1],[-1,1]].                      (16)

Keeping S makes each restricted line geometry positive: use psi=x, with y=+x or y=-x, and at zero mean the restricted covariance is 1. Treating (16) as a positive-definite two-dimensional metric or replacing the posterior by q_r(0,0) is a different, unjustified operation. These are mathematical countercontrols, not reports of an implementation doing that.

### 7.2 Facial support alone is insufficient

Take three independent uniform bits, retain (x,y,z), and let

    L(x,y,z)=1_(x=+1) (1+yz/2).

Its support is the full saturated square face x=+1 of the cube. The conditional yz table has probabilities 3/8,1/8,1/8,3/8 in the usual --,-+,+-,++ order, and means zero. Its odds ratio is 9, so log L is not affine in y,z on that face. The old product-face stratum has odds ratio 1. Thus Theorem 3 correctly rejects this posterior despite its facial support. Replacing L by 1_(x=+1) times an exponential affine y,z tilt satisfies both tests.

### 7.3 Saturation includes duplicate and nonvertex columns

Use the six supplied columns

    (0,0), (1,0), (1,0), (2,0), (0,1), (2,1)

and reference weights r=(1,2,3,1,2,4). The bottom edge has saturated support of four atoms, not just its two vertices. At bottom mean (1,0), its selected law is

    q_r=(1,2,3,1,0,0)/7.

The endpoint-only law (1/2,0,0,1/2,0,0) has exactly that mean but is outside the old closure: it omits supplied atoms on the same face. At any old leaf limit, the two duplicate-column probabilities retain ratio 2:3 when positive. A likelihood with different positive values on those duplicates violates the restricted log condition. Even equal duplicate values need not suffice: bottom likelihood (1,2,2,1) is not an exponential affine tilt along the three positions, although it is positive at all four atoms. Likelihood (1,2,2,4), by contrast, is exactly 2^x on that edge and preserves the stratum.

The entropy identity is checked at a nonzero restricted parameter as well: the latter tilt gives q=(1,4,6,4,0,0)/15 with mean (6/5,0). The endpoint law (2/5,0,0,3/5,0,0) has the same mean and obeys (9), with a strictly positive KL gap because it differs from q. If r is normalized by 13, the dual value here is (6/5)log 2-log(15/13).

### 7.4 The inherited global pairwise facet gets a positive five-dimensional chart

Retain phi=(x,y,z,xy,xz,yz) on three bits and put

    a(x,y,z)=(1+xy+xz+yz)/4.

The inherited example has the six-atom facet a=0; its mean under the uniform law there is (0,0,0,-1/3,-1/3,-1/3), with all local pair-table cells positive. It is approached from the uniform-reference leaf by likelihood weights epsilon on the two all-equal atoms and 1 on the six others, as epsilon decreases to zero. Equivalently use the observable exponential tilt exp(-t a) with epsilon=exp(-t).

On this facet, xy+xz+yz=-1. Delete that affine redundancy and take

    psi=(x,y,z,xy,xz).

At the uniform six-atom law the reduced covariance is block diagonal:

    unary block: diagonal 1, off-diagonal -1/3;
    pair block: [[8/9,-4/9],[-4/9,8/9]].                 (17)

Its eigenvalues are 1/3,4/3,4/3,4/9,4/3, all positive. The full six-statistic covariance has rank five and normal kernel spanned by (0,0,0,1,1,1). The six augmented columns are independent, so this particular face family is the entire positive simplex on its six atoms; its five-dimensional metric is fully regular. This is the constructive boundary repair. It retains the true global face rather than replacing it with local marginal positivity.

That face need not be reachable by finitely many pair-local hard observations. Each of the four assignments on every pair occurs among these six atoms. Therefore any pair-local nonnegative factor that stays positive on all six must be positive on every assignment of its pair. Any finite product of such factors stays positive on all eight atoms and cannot have exactly the six-atom support. This reuses the inherited support-projection obstruction; it is not a new local-feasibility theorem.

There is still the normal-ray limit. With normalized pair-local soft factors exp(-t(xy+1)), exp(-t(xz+1)), and exp(-t(yz+1)), their product is exp(-2t) on the six atoms and exp(-6t) on the two all-equal atoms. Its branch probability under uniform r is (6 exp(-2t)+2 exp(-6t))/8, tending to zero, while the normalized posterior tends to the uniform six-atom law. The hard demand that all three pairs anti-align has no supported atom. The limit law is not conditioning on that impossible limiting event. The nonlocal likelihood 1-a, by contrast, reaches the six-atom law directly with positive branch probability 3/4.

## 8. Support faces and event-feasibility zero faces answer different questions

The inherited event theorem says: for L>=0, the Boolean assertion alpha_L(p)>0 is determined by the retained record for **every** law p exactly when the **zero set** Z=X\supp L is the saturated support of a face, allowing its empty/full endpoints. Theorem 3 here says: from a fixed exponential leaf, the **posterior law remains in that leaf's closure** exactly when the **positive support** S is a saturated face and the positive log values are retained there.

These statements concern complementary index sets, different quantifiers, and different outputs. Neither can be substituted for the other. For the uniform two-bit square, indicator likelihoods make all four combinations explicit:

- A singleton S is facial and gives a closure member, but its three-vertex complement is not facial, so all-prior feasibility does not descend.
- Three vertices S are nonfacial and give no old closure member, but their singleton complement is facial, so feasibility does descend.
- An edge S and its opposite edge are both facial: both contracts hold.
- A diagonal S and the other diagonal are both nonfacial: neither contract holds.

At a finite full-support starting state any nonzero L is feasible anyway. That trivial fact does not establish all-prior feasibility descent. The executable controls enumerate all 15 nonempty square supports and all 80 nonzero likelihood-weight arrays with entries 0,1,2, checking the closure criterion against the independent polynomial identity (15), at both a uniform and a nonuniform product prior. No finite test count replaces the universal proofs.

## 9. Classical attribution, replay, and limits

The finite facial completion is classical extended-exponential-family geometry. [Csiszár and Matúš, Information Projections Revisited (2003)](https://www.researchgate.net/profile/Imre-Csiszar/publication/3084724_Information_projections_revisited/links/5411827f0cf29e4a23296a25/Information-projections-revisited.pdf), §VIII.A, pp. 1484–1485, uses inverse images of faces and explicitly identifies finite extension with Euclidean closure. Theorem 3 and Corollaries 7–8, pp. 1478–1479, supply the unique moment-fibre entropy projection and Pythagorean characterization. The broader variation-closure formula is Theorem 2 of [their Closures of exponential families (2005)](https://arxiv.org/pdf/math/0503653), reprint pp. 10–11; the unrestricted finite specialization gives all facial supports.

The inspected [Wainwright–Jordan source](https://people.eecs.berkeley.edu/~jordan/sail/readings/wainwright-jordan-fnt.pdf), §§3.5–3.6, supports interior coordinates and entropy duality; an exact face-union theorem was not verified there. Version-specific loci, retrieval scope, PDF hashes, and normalization/saturation qualifications are in `sources/PRIMARY_FACE_CLOSURE_NOTES.json`. The direct finite proofs above avoid silently importing general-measure hypotheses. Earlier Barndorff-Nielsen work is identified by the inspected papers but was not independently read here.

`verify.py` uses exact integers/rationals and symbolic identities. It checks input snapshots, exhaustive small square likelihood controls, distinct face/zero-face contracts, both diagonal countercontrols, facial-but-nonaffine failure, duplicate/nonvertex saturation, an exact entropy decomposition, a reduced edge Fisher metric, and the five-dimensional pairwise-facet covariance. The preserved author run passed 35 exact assertion groups, including 80 square likelihood weights at two priors and 144 local-update branch cases across nine selected closed strata of a nonproduct reference. Its exact controls do not certify numerical conditioning, statistical estimation, efficient general polytope reconstruction, or an algorithm for finding a face from approximate data.

`replay.py` verifies all manifest entries before running the controls in a fresh output directory. It compares regenerated control JSON and stdout with the preserved author outputs. The manifest binds this packet's authored files and direct snapshots; no transitive historical verifier replay is claimed. Source attribution is bounded to the inspected loci and does not establish priority beyond those sources.

The repair is conditional on a finite state model, declared retained observables, valid likelihood, and selected reference class. It describes which exact distributions and metrics those choices entail. It neither establishes that an actual cognitive state obeys them nor supplies normative permission, source truth, actual warrant, or a DAEE implementation failure. Crossing support strata, revising a reference class, preserving historical evidence, and verifying warranted use remain separately typed obligations.
