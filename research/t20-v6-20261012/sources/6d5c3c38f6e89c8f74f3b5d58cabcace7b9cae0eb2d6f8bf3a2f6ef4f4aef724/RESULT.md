# Exact objective descent and conditional Fisher geometry on interaction leaves

10 October 2026 UTC. Separate scratch mathematical continuation. Ordinary finite proofs and executable exact controls; no protected-source edit, integration, formal-kernel claim, empirical identification, actual cognitive warrant, or programme closure. The root supplied the individual-objective conjecture, exponential-leaf remedy, and stabilizer-block extension. This worker checked the claims, proved the qualifications, and constructed controls. This is author verification, not independent review.

## 1. Results and their quantifiers

Let a finite product carry all strictly positive probability laws, and retain every interaction moment through a proper order k, where 1 <= k < the number of nontrivial slots. Equip the fine simplex with its evolving Fisher metric. Then:

1. At an interior retained moment z, the projected Fisher gradient of **one specified** smooth moment objective is the same for every positive law in that fibre if and only if the objective differential at z is zero. Consequently a smooth objective has an exact autonomous moment-only projected field on the whole positive simplex if and only if it is constant on the moment domain. This strengthens the inspected all-objectives obstruction by classifying each individual objective on these particular complete proper interaction spaces.
2. There is a positive conditional remedy. Fix a full-support reference r and restrict the state to the finite exponential family p_theta proportional to r exp(theta·phi), where 1 and the components of phi form a basis of the retained observable space. Its moment map is a smooth bijection, with smooth inverse, onto the entire interior moment polytope. The Fisher gradient stays in this family and has the exact autonomous moment equation

       zdot = -C_r(z) grad J(z),
       C_r(z) = Cov_(p_theta(z))(phi).

   The metric is C_r(z)^(-1), the Hessian of the Legendre dual of the log partition function.
3. The reference's log-density class modulo the observable space is an invariant that labels this restriction. Different classes can give different cometrics at the same moment. Across all classes, the pair (moment, log-density class) uniquely reconstructs the full positive law. There is no universal reduction of information from silently discarding the class.

All differential statements are intrinsic to the mass-one affine moment domain. A mass-coordinate derivative is an irrelevant gauge; it is not incorrectly required to vanish. Arbitrary nonlinear decoders or a separately chosen coarse metric cannot remove the first obstruction, which is already disagreement of the actual projected velocity.

## 2. Inheritance and the bounded addition

The inspected local input bytes are bound in INPUT_BINDINGS.json.

- tensor-likelihood-closure-20261010/RESULT.md, §§3-4, already supplies the arbitrary-decoder kernel/multiplier criterion and the constant stabilizing algebra of complete proper finite-product interaction spaces. That algebra theorem is an input here, not rediscovered below. Its §§5-6 carefully distinguish normalized posterior, branch probability, feasibility, and cone contracts.
- tensor-moment-continuation-20261009/RESULT.md, §§2-5, already supplies the Fisher replicator field, covariance moment mobility, exponential-tilt solutions, finite sufficient closure, and continuation equivalence for its control/output interface. Its §7 proves that first moments close for **all** controls on the full positive aggregate simplex exactly when the distinct support vectors are affinely independent. Its explicit discussion after Theorem 2 says that a rich-control converse need not hold for one fixed objective.
- state-dependent-gradient-obstruction-20261009/RESULT.md, §§2-4, already gives the evolving-Fisher same-fibre velocity obstruction, including one linear-objective counterexample and positive deterministic-channel controls. A counterexample for one objective is not yet the classification of all individual objectives proved here.
- noetic-gradient-transport-20261009/RESULT.md, §§2-5, uses a **fixed-reference weighted quadratic** metric. Its pointwise quotient construction and exact descended field remain valid. The present metric is Fisher at the evolving law; fibre-dependent cometrics are a different problem. Its particular-objective support-graph criterion concerns agreement with a separately prescribed canonical channel metric, not the present stabilizer test for existence of any common projected moment field.

The new-to-these-inspected-passages deduction is the fixed-objective stabilizer criterion, its block-mass classification, and its proper-interaction consequence, coupled to an explicit conditional leaf repair with the missing invariant kept visible. The leaf parametrization, convex duality, Fisher metric, and exponential updates are classical; the packet does not claim new information geometry or a project-wide priority search.

## 3. Exact local criterion for one objective

Let X have n states. Let V be a real subspace of R^X containing 1, and let M be a full-row-rank matrix whose rows are a basis of V, with first row 1. Set

    Delta° = {p: p_x>0, sum_x p_x=1},
    Z° = M Delta°,
    A(V) = {f in R^X: f v belongs to V for every v in V}.

Multiplication of functions is pointwise. A(V) is the stabilizing algebra, and A(V) is contained in V because 1 belongs to V. Write J for a C² function on Z°, g for any ambient representative of dJ_z, and f=M^T g. Fisher duality gives

    X_J(p) = -(diag(p)-p p^T) M^T g
           = -diag(p) f + (g·Mp)p.                         (1)

Indeed h_p(u,v)=sum_x u_x v_x/p_x on sum-zero tangents, and pairing (diag(p)-p p^T)M^Tg with a tangent v yields g·Mv. The formula does not depend on the mass gauge.

**Theorem 1 (one-objective, one-fibre criterion).** Fix z in Z°. The vector M X_J(p) is constant over all p in Delta° with Mp=z if and only if f=M^Tg belongs to A(V).

**Proof.** For p,q in that fibre, (1) gives

    M X_J(p) - M X_J(q) = -M diag(f)(p-q).                (2)

Choose one p in the positive fibre. For every h in ker M, the mass of h is zero, and p+epsilon h is positive for sufficiently small |epsilon|. Thus fibre constancy is equivalent to

    ker M subset ker(M diag(f)).                         (3)

By finite-dimensional row/kernel duality, (3) is equivalent to every row of M diag(f) being in row(M). These rows are exactly basis observables multiplied by f. This is fV subset V. Conversely that inclusion makes (2) zero. No continuity or linearity of a prospective decoder was assumed. QED.

If f is constant, full row rank implies that g differs from zero only by the mass-coordinate covector; equivalently dJ_z=0 intrinsically. This is why the mass gauge causes no loophole.

For later use, Z° is the relative interior of the moment polytope M Delta. Here is an elementary justification after deleting the mass coordinate. The remaining evaluation points affinely span R^d. Every strictly positive convex combination is interior: a supporting functional that achieved its maximum at the combination would have to achieve it at every point, contradicting affine spanning. Conversely let b be their uniform barycentre and z any interior point. A short extension y=z+epsilon(z-b) remains in the polytope. Then z is a convex combination with positive coefficient of b and nonnegative coefficients of y, and hence has a strictly positive representing law. In particular every interior fibre used above really has the required perturbation neighbourhood.

## 4. General allowed objectives: stabilizer-block masses

This section applies to arbitrary finite V, not just product moments.

**Lemma 2.** A(V) is exactly the algebra of functions constant on each block of one partition X=B_1 disjoint-union ... disjoint-union B_s.

**Proof.** A(V) is linear, contains 1, and is closed under multiplication: if aV and bV are contained in V, then (ab)V is contained in aV, hence in V. Define x~y when every a in A(V) has a(x)=a(y). Choose one element a of A(V) having different values on different equivalence classes. Such an element exists: in a basis expansion, each unwanted equality defines a proper hyperplane, and finitely many proper hyperplanes do not exhaust a real vector space. Lagrange polynomials in a then give each block indicator 1_(B_j). They belong to A(V), so the full blockconstant algebra is contained in A(V). The reverse inclusion holds by the definition of the blocks. QED.

The block masses w_j=sum_(x in B_j) p_x are functions of z because each block indicator belongs to V. Thus w=Bp=Rz for a fixed matrix R. Their image from positive p is the positive s-block simplex.

**Theorem 3 (global objective classification).** On the convex interior moment domain, the projected field of J descends across every positive moment fibre if and only if

    J(z)=Phi(w(z))                                       (4)

for a C² function Phi on the positive block-mass simplex.

**Proof.** By Theorem 1, descent is equivalent to f(z) belonging to A(V) everywhere. For a moment tangent v=Mh whose block-mass change Bh is zero, we have

    dJ_z(v)=g·Mh=f·h=0,

since f is blockconstant. Each fixed-w subset of Z° is convex, so integrating this zero derivative along line segments makes J constant on it. A smooth factor Phi exists concretely: choose one strictly positive normalized law s_j on each B_j, set p(w)=sum_j w_j s_j, and define Phi(w)=J(Mp(w)). This linear section lies in Z°, gives (4), and is C². Conversely (4) has fitness f equal to a linear combination of the block indicators (up to the mass gauge), hence f belongs to A(V). Theorem 1 applies. QED.

The block-mass equation is the usual Fisher/replicator gradient

    wdot_j = -w_j(a_j - sum_l w_l a_l),  a=dPhi_w.

The rest of z also has a closed projected field, because multiplication by each block indicator preserves V. This is the **observable-space stabilizer partition**. It is not asserted to be the decomposition of a moment-image cone: a general observable matrix need not give a permissible diagonal lift of every cone endomorphism.

For a small nontrivial control, let X be a four-state two-bit block B plus one extra state e, with

    V=span{1_X,1_B,x 1_B,y 1_B}.

Its stabilizer is span{1_B,1_e}. The descending objectives are precisely functions of w=p(B). For J=w and retained coordinates (w,u,v),

    (wdot,udot,vdot)=(-w(1-w),-u(1-w),-v(1-w)).

In contrast J=u fails: take w=1/2 and conditional two-bit correlations +1/2 and -1/2, each with zero unary means. Both retained records agree, but vdot is -1/4 and +1/4. The executable controls verify these statements, including the exact stabilizer rank.

## 5. Complete proper product interactions admit only stationary objectives

Let X=product_(i=1)^m X_i, with each finite |X_i|>=2. Decompose each function space into constants plus its uniform-zero-mean contrast space H_i. Let H_S be the tensor product with contrasts on exactly S, and constants elsewhere. Then

    R^X = direct-sum_(S subset [m]) H_S,
    V_k = direct-sum_(|S|<=k) H_S,       1<=k<m.

This V_k is exactly the span of observables depending on at most k distinct slots, hence the content of all marginals of those orders. It is not a generic polynomial-degree truncation or a symmetrization of semantic slots.

The inherited constant-stabilizer theorem says A(V_k)=span{1}. For completeness, its mechanism is short: if fV_k subset V_k, then f belongs to V_k. Choose a nonzero highest-order component f_S with d=|S|>=1. Choose a disjoint set T with |T|=k-d+1 and a nonzero pure contrast h_T. The projection of f h_T on H_(S union T) is exactly f_S tensor h_T and is nonzero. No other component can contribute: outside T its support must equal S, and maximal order then forces that component to be S itself. This contradicts |S union T|=k+1. Thus f is constant. The full inherited proof also addresses finite categorical factors without assuming binary multiplication rules.

**Corollary 4.** For V_k, at every interior moment z the one-objective projected field is fibreconstant exactly when dJ_z=0. An objective has an autonomous projected moment-only field throughout the whole positive simplex exactly when J is constant on its connected interior moment domain, and that field is zero.

This does not say that every pair in a fibre distinguishes every objective, that a chosen single trajectory cannot be described by some smaller state, or that critical points cannot have a well-defined zero field. The quantifier is **all positive lifts of each moment**. At full order k=m the moment map is injective and all objectives descend; at k=0 there is only a mass coordinate and no nonconstant intrinsic moment objective. Those are different, harmless endpoints.

## 6. Fixed-reference exponential leaves and their global mean coordinates

For the rest of the construction, any finite V with basis {1,phi_1,...,phi_d} is allowed. Let phi(x) be its d-vector of nonconstant basis evaluations and set P=conv{phi(x):x in X}, a full-dimensional polytope. Fix r_x>0; its normalization is immaterial. Define

    A_r(theta)=log sum_x r_x exp(theta·phi(x)),
    p_(r,theta)(x)=r_x exp(theta·phi(x)-A_r(theta)),
    E_r={p_(r,theta): theta in R^d}.

**Theorem 5 (finite global mean parametrization).** The map

    theta -> z=E_(p_(r,theta))[phi]=grad A_r(theta)

is a smooth diffeomorphism from R^d onto int P.

**Proof.** Differentiating finite sums gives

    grad A_r(theta)=E_theta[phi],
    Hess A_r(theta)=C_theta=Cov_theta(phi).                (5)

For a nonzero vector a, a^T C_theta a is the variance of a·phi. It is positive: p_theta has full support, and zero variance would make a·phi constant on X, contradicting the basis assumption. Thus the Hessian is positive definite everywhere. In particular A_r is strictly convex and its gradient is injective. For example integrating the positive Hessian along the segment between two distinct parameters gives strictly positive scalar product of their parameter and gradient differences.

Each z(theta) is in int P by the positive-combination argument in §3. Conversely fix z in int P. There is delta>0 with the Euclidean ball of radius delta about z contained in P. For theta nonzero, the support function of P therefore satisfies

    max_x theta·(phi(x)-z) >= delta ||theta||.

With r_min=min_x r_x>0, it follows that

    A_r(theta)-theta·z
      >= log r_min + max_x theta·(phi(x)-z)
      >= log r_min + delta ||theta||.                    (6)

Thus this continuous function is coercive. It attains a minimum on a sufficiently large closed ball; strict convexity makes the minimizer unique, and its first-order condition is grad A_r(theta)=z. This proves surjectivity. Finally the everywhere invertible Hessian and the finite-dimensional inverse-function theorem give a smooth local inverse at every point; uniqueness makes these inverses a global smooth inverse. No unproved general exponential-family surjectivity theorem is being imported. QED.

Write theta_r(z) for the inverse and define the Legendre dual on int P by

    psi_r(z)=theta_r(z)·z-A_r(theta_r(z)).

Differentiation and (5) give

    grad psi_r(z)=theta_r(z),
    Hess psi_r(z)=C_(theta_r(z))^(-1).                    (7)

There is also an exact variational description. For any law p with moment z,

    sum_x p_x log(p_x/r_x)
      = D_KL(p || p_(r,theta_r(z))) + psi_r(z).           (8)

This follows by substituting log(p_theta/r)=theta·phi-A_r; zeros in p are interpreted by 0 log 0=0. Nonnegativity of KL follows from log t<=t-1, with equality only for equal laws. Hence p_(r,theta_r(z)) uniquely minimizes the displayed relative-entropy functional at that moment. If r is uniform this is the familiar maximum-entropy member. That optimization characterization does not establish that an arbitrary actual law in the fibre equals the chosen member.

## 7. Exact Fisher geometry and the invariant carried by each leaf

The derivative of the leaf embedding in a parameter direction a is

    (D_theta p)a = p_x a·(phi(x)-z).

Consequently its induced Fisher metric is a^T C_theta b. Since dz=C_theta dtheta, its metric in mean coordinates is

    h_(r,z)(u,v)=u^T C_r(z)^(-1)v
                =u^T Hess psi_r(z) v.                   (9)

There is a precise relation to pointwise quotient geometry. The moment-fibre tangent is ker M. A leaf tangent has the form p(f-E_p f), with f in V, and its Fisher pairing with h in ker M is sum_x(f_x-E_p f)h_x=0. The dimensions, d and n-d-1, show that these are orthogonal complements in the fine simplex tangent. The leaf tangent is therefore the least-Fisher-energy lift of a prescribed moment velocity; in coordinates the lift is p(phi-z)^T C_r(z)^(-1)u and has energy u^T C_r(z)^(-1)u. These horizontal directions are integrable into the displayed exponential leaves. What fails globally is agreement of that quotient metric between different positive lifts of the same moment, not existence of horizontal lifts at each fine point.

For a C² moment objective J on int P, the negative gradient of J∘z on this leaf therefore has

    thetadot = -grad J(z),
    zdot = -C_r(z) grad J(z),
    pdot_x = -p_x grad J(z)·(phi(x)-z).                 (10)

The last equation is exactly the **full fine Fisher gradient** of J∘E[phi], not a projection chosen after the fact. Its full gradient lies in the leaf tangent space, so restricting the Fisher metric to the leaf changes neither that vector nor its time parameter. Conversely solving either coordinate equation and applying the smooth inverse recovers the same fine solution. Along it,

    dJ/dt = -grad J(z)^T C_r(z) grad J(z) <= 0,

strictly when dJ is nonzero. This is decrease of the supplied numerical objective, not a truth or warrant test.

Define the log-density class lambda(p)=[log p] in R^X/V. Then

    p,q belong to the same E_r iff log p-log q belongs to V.

Indeed the latter difference is a constant plus a linear combination of phi; normalization gives precisely an exponential tilt. Thus the sets E_r partition Delta°. Equation (10) gives d(log p)/dt in V, so lambda(p) is conserved. In the product decomposition V_k, this fixes the log-linear interaction coefficients of orders above k; it does not assert that the corresponding raw moments or correlations stay fixed.

Every leaf meets each interior moment fibre once by Theorem 5. Therefore

    p -> (E_p[phi], [log p] modulo V)                    (11)

is one-to-one and onto int P times R^X/V. To see onto directly, choose a representative w of the desired quotient class, set r_x=exp(w_x), and invoke Theorem 5. Choose a linear complement of V if coordinates are desired: the parameter-dependent inverse-function theorem, using C_theta>0, also gives smooth reconstruction in these coordinates. The dimensions are d and n-d-1, totaling n-1. The universal augmented state has retained **all** information in the positive law.

Replacing r by another representative of the same leaf translates theta and changes psi by an affine function; C_r(z) and the mean metric do not change. Different leaves need not share C_r(z), as §9 proves exactly. The fixed class must be supplied as model data, or retained as auxiliary state, rather than silently inferred from z.

These claims hold on the common maximal smooth interior existence interval. Arbitrary C² objectives on int P can have unbounded derivatives near its boundary; no unrestricted all-time existence or convergence claim follows. For a linear objective, theta evolves affinely and remains finite at every finite time. More generally a uniform bound on grad J throughout int P prevents finite-time parameter escape and supplies global forward existence by the ordinary local ODE extension argument.

## 8. Finite likelihoods: exact preservation criterion

For a strictly positive likelihood L, Bayes tilting sends p to pL/E_pL. It preserves one fixed leaf E_r (equivalently, preserves it for every starting point) if and only if

    log L belongs to V.                                (12)

Necessity already follows from one p in E_r whose posterior is in E_r: subtract their log densities and add the normalization constant. Sufficiency follows by writing log L=b+a·phi. In that case

    p_(r,theta) -> p_(r,theta+a),
    E_theta L=exp(b+A_r(theta+a)-A_r(theta)),
    z -> grad A_r(theta_r(z)+a).                         (13)

If L represents an actual event likelihood, also require L<=1; an admissible known positive rescaling changes only branch probability, not the posterior or leaf criterion. Equations (13) close exactly given the chosen leaf. They do not contradict the inherited full-simplex no-go: different leaves can supply different posterior moments or probabilities from the same z.

For a single binary coordinate x and |a|<1,

    log(1+a x)=0.5 log(1-a²)+atanh(a)x.

Thus this local likelihood preserves a leaf containing that unary statistic, even with a correlated base. More generally a positive function of at most k slots has its log in complete V_k. But L in V_k is **not** enough: in the two-bit unary space,

    L(x,y)=1+(x+y)/4

is positive and belongs to V_1, while its mixed log coefficient is (1/4)log(3/4), which is nonzero. Starting from the uniform product law, its posterior has odds ratio 3/4, so it leaves the product leaf. Rescaling by 2/3 makes it a valid event likelihood without changing that conclusion.

For arbitrary positive L, a known E_r is sent exactly to E_(rL); the class changes by [log L]. Since the old leaf and z already determine the full p, the one update can still be calculated. What fails when (12) fails is closure in the **same** fixed leaf, not all calculation. These exponential families are generally nonconvex as sets of laws, so conclusions for closed convex restricted prior domains do not automatically transfer. Zero likelihoods can create boundary laws, which lie outside this positive-leaf framework and require a separate support/domain treatment. The Fisher objective flow itself is not automatically a receipt of actual Bayesian evidence.

## 9. Exact two-bit controls: identical means, different geometries

Let x,y in {-1,+1}, V_1=span{1,x,y}, and

    r_rho(x,y)=(1+rho xy)/4,       -1<rho<1.

At theta=0 both unary means vanish, but

    C_rho(0) = [[1,rho],[rho,1]],
    C_rho(0)^(-1) = [[1,-rho],[-rho,1]]/(1-rho²).

For J(z)=z_1, rho=+1/2 and rho=-1/2 give respective velocities (-1,-1/2) and (-1,+1/2). These are different directions, not merely different speeds. More generally at a mean pair (u,v), write a positive fibre as

    p_c(x,y)=(1+u x+v y+c xy)/4.

Its positivity interval is -1+|u+v| < c < 1-|u-v|, nonempty for every (u,v) in (-1,1)^2. Its cometric is

    C_c(u,v) = [[1-u²,c-uv],[c-uv,1-v²]].

For a covector (a,b), subtracting the projected velocities at c and c' gives

    -(c-c') (b,a).

Thus at **every** interior unary moment, all positive fibre velocities can agree only when a=b=0. This is a complete two-bit control of Corollary 4, not only a zero-mean example.

The leaf invariant is the odds ratio

    OR(p)=p_(++) p_(--)/(p_(+-) p_(-+)),
    OR(r_rho)=((1+rho)/(1-rho))².

Multiplication by exp(theta_1 x+theta_2 y) leaves OR unchanged. The two chosen references have OR 9 and 1/9, respectively. For the preceding linear objective the exact positive trajectory is

    p_t(x,y)=r_rho(x,y) exp(-t x)/cosh(t),
    z(t)=(-tanh(t),-rho tanh(t)).

It has the displayed initial derivatives and remains positive at all finite times.

For rho=0 the reference is uniform and the leaf is exactly the independent product family. Its mean cometric is diag(1-z_1²,1-z_2²), and

    psi_0(z)=sum_(i=1)^2 [(1+z_i)/2 log(1+z_i)
                         +(1-z_i)/2 log(1-z_i)].

Its Hessian is the inverse cometric. An arbitrary base is not thereby made independent. Starting from rho=1/2 and multiplying by (1+x/3)(1+y/4) keeps OR=9 but changes E[xy] from 1/2 to 14/25; the new unary means are (11/25,2/5). Fixed higher-order **log-linear** interaction is therefore distinct from fixed higher-order **moment**, and from independence. For general unary finite-product families a product base yields the product family; a nonproduct base has fixed nonzero higher log-linear terms.

## 10. Classical ancestry, verification, and boundaries

The inspected author-hosted [Wainwright and Jordan, Graphical Models, Exponential Families, and Variational Inference](https://people.eecs.berkeley.edu/~jordan/sail/readings/wainwright-jordan-fnt.pdf), §§3.5-3.6 and Appendix B.3.2, already establishes covariance derivatives, minimal mean parametrization, and convex-dual geometry. In this PDF version the relevant labels are Proposition 2, Proposition 3, Theorem 1, and Proposition 18. The proof here supplies an elementary finite-support coercivity argument rather than importing the source's general-measure hypotheses. The earlier tensor-moment packet already documents the replicator/exponential-tilt ancestry. Only these focused loci were inspected; no field-wide novelty or exhaustive literature search is claimed.

verify.py uses exact SymPy arithmetic. It checks the local fibre identity, stabilizer constraint ranks for binary and mixed categorical interaction spaces, full-order and blockconstant positive controls, the mixed-block objective classification, symbolic two-bit covariance and fibre differences, leaf tangent/Fisher metric identities, exact tilted moments and odds ratios, likelihood preservation and failure, and the product Legendre metric. Finite controls supplement the general ordinary proofs; they do not prove universal statements by enumeration. CONTROL_RESULTS.json and verification.txt record the executed assertions and numerical environment.

The mathematical interpretation is conditional: a specified interaction class can support a faithful autonomous moment geometry, while whole-simplex moment sufficiency fails for every nonstationary objective in a complete proper interaction space. Nothing here identifies an actual cognitive state with a probability law, authenticates an evidence source, chooses the proper objective or reference class, establishes truth or epistemic warrant, authorizes an intervention, proves an efficient reconstruction algorithm, or closes T20. Fisher objective descent, Bayesian leaf preservation, universal posterior sufficiency, and actual warranted learning remain separately typed obligations.
