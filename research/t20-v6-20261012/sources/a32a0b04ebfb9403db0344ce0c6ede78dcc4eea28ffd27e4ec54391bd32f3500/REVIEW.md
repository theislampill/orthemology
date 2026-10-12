# Independent review: joint moving-atomic gradient geometry

Status: ACCEPTED as ordinary mathematical evidence, restricted to the final frozen files in `ACCEPTED_BINDINGS.json`. The two-atom supplement and source-interface companion have been read independently. This report supplies ordinary mathematical assessment only, with no integration, kernel-proof, historical-novelty, actual-noetic-validation, or audit-closure authority.

## 1. Scope and independence

The assessed object consists of three participating contributions:

1. `joint-atomic-gradient-lift-20261010`: the joint metric, forced finite-rank lift, finite-moment embedding, and qualified long-time conclusions.
2. `two-atom-moving-moment-chart-20261010`: a root-authored explicit unknown-support two-atom chart and rational quadratic moment dynamics. Root participation is not counted as an additional independent review.
3. `spherical-atomic-source-interface-20261010`: the literature convention check, exact fixed-path action, direct local ambient-speed proof, and global-distance limitation.

I did not edit any author or predecessor file. I independently derived the formulas, challenged the analytic and geometric implications, read the complete author texts, and wrote separate exact controls. Acceptance is restricted to the exact SHA-256 bindings in `ACCEPTED_BINDINGS.json`. Every bound file was reread as needed after final freeze and its digest verified.

## 2. Joint metric, signs, and cometric

For distinct positions and strictly positive weights, the diagonal quadratic form

    G((u,v),(u,v)) = sum(u_i^2/w_i) + sum(w_i |v_i|^2),
    sum(u_i)=0,

is positive definite on the actual tangent space. The simultaneous permutation action is free and proper because the positions are distinct; the quotient is a smooth manifold of dimension r(d+1)-1 and the invariant metric descends without a combinatorial factor.

For E=sum(w_i F(x_i)), direct pairing, including the simplex constraint, gives

    grad E = (w_i(F_i-E), grad F(x_i)).

Thus the negative-gradient signs in both blocks are correct. The position block's factor w_i cancels the w_i in the position differential; no additional w_i belongs in x_i'=-grad F(x_i). The reaction block is centered by E because mass is constrained. A negative or positive constant added to F has no effect on either velocity.

For a polynomial observable f_p, the same calculation gives

    B(p,q) = L(grad p . grad q) + L(pq)-L(p)L(q).

There is no missing transport/reaction cross term in atomic coordinates. There generally are nonzero off-diagonal terms after passing to moments. For example, with weights (1/3,2/3) at (0,2), B(x,x^2)=40/9. Treating the finite moment metric as diagonal or Euclidean would be wrong.

The polynomial form is semidefinite, not an invertible metric on all polynomials modulo constants: B(p,p)=0 exactly when all grad p(x_i)=0 and all p(x_i) have a common value. Nonconstant polynomials can satisfy this. This is the kernel of the map from polynomial tests to cotangent vectors; on the finite image it is precisely the conormal redundancy. The author was asked to state this explicitly; the frozen final text contains and passes that clarification.

The resulting identity E'=-sum(w_i |grad F_i|^2)-Var_w(F_i) is an exact gradient-norm identity, stronger than an isolated formal scalar dissipation calculation.

## 3. Reverse representation and completeness

The new result correctly imports rather than re-proves the accepted predecessor's section 9. I directly rechecked its load-bearing hypotheses and endpoint reasoning: normalized full square positivity, every polynomial coordinate C1, the complete polynomial hierarchy, and a locally uniform bound on the full Hankel rank along the path. Neither initial finite rank nor a bound on one fixed truncated Hankel matrix can replace the last assumption in the general nonlinear theorem.

Autonomous coercive polynomial F supplies both required analytic premises. Its gradient field is locally Lipschitz, each characteristic remains in its compact initial sublevel, and therefore all forward characteristics exist. F is bounded below, so the killing rate has the global lower bound needed to exclude reverse inflow.

The latter is essential to the abstract-to-actual step: after unnormalizing, any atom traced back on a maximal-rank component has mass bounded below. Bounded second moments then bound its position. This excludes entry from infinity and allows continuation through a rank boundary. Forward characteristic completeness handles the other endpoint. Finite positive exponential weights and uniqueness prevent finite-time extinction and collision. The full-rank conclusion follows from the maximal-rank open-and-closed argument, not from assuming the desired rank constancy.

A separately inherited affine-transport/SOS-domination route can remove the path-rank promise for strongly convex quadratic F. Its gradient transport is affine, and a quadratic F with positive-definite Hessian admits F+C-c|x|^2 as an SOS for suitable C and c>0. I read the newly cited predecessor section 4 and checked that specialization. This exception is not extended to arbitrary nonlinear coercive gradients.

The general resulting flow is unique within the admitted full-positive, locally bounded-full-rank hierarchy class. It is not a theorem about arbitrary infinite-rank hierarchy solutions. Forward characteristic injectivity gives injective finite-law transitions, but backward completeness and surjectivity onto every later law are not implied. The inherited quartic example correctly distinguishes these statements.

Forward completeness of this vector field is not metric or geodesic completeness of its state manifold. Both weight loss and collision are at finite intrinsic path length in the surrounding stratified space. These qualifications are preserved.

## 4. Unknown-support finite-moment geometry

The degree bound 2r-1 is sufficient in any finite spatial dimension.

Injectivity on laws with at most r atoms follows by taking the signed difference, whose support has at most 2r points, choosing a linear form that separates that finite union, and interpolating a cardinal polynomial of degree at most 2r-1 for every support point. This recovers each signed coefficient. There is no known-support assumption hidden in this argument.

For immersion, the frozen tests (x_k-x_ik)e_i(x)^2 have degree at most 2r-1, zero values at all atoms, and a single prescribed first derivative. They first isolate w_i v_ik and hence all velocities. The e_i^2 tests then isolate each weight tangent. Positivity of w_i is used exactly where division by it is required.

An injective immersion alone would not justify the asserted embedded image. The author's additional local inverse closes that gap. The projected r by r Gram matrix uses moments only through degree 2r-2; positivity forces r distinct projected nodes for nearby exact-r laws. Its inverse and moments through degree 2r-1 determine a monic polynomial with simple roots. Root continuation, Vandermonde inversion, and the mixed moments L(x_k ell^a) recover smooth local labels, weights, and spatial coordinates. The latter moments have degree at most r. These formulas work in a moment neighborhood of the fixed point and give an inverse continuous in the subspace topology, so the image really is embedded.

The pushed-forward metric is positive on the image's tangent space. Its redundant ambient matrix has rank r(d+1)-1, and must not be inverted on all ambient coordinates. Higher moments in its entries, and a potential F of degree above the retention bound, are obtained from the reconstructed law. This gives autonomous closure on a constrained, known-rank model; it does not contradict all-laws nonclosure. The two positive rank-two laws sharing degrees zero through two and differing at degree three correctly expose the unknown-support distinction.

## 5. Explicit two-atom supplement

This supplement is correct by an elementary global argument, independent of any predecessor's Lean/kernel status.

For D=b-a^2>0, the recurrence coefficients s=(c-ab)/D and p=(ac-b^2)/D satisfy

    s^2-4p = (c-3ab+2a^3)^2/D^2 + 4D > 0,
    a^2-sa+p = -D < 0.

Therefore the two real roots are distinct and bracket a; the barycentric weight lies strictly between zero and one. The recurrence reconstructs b and c exactly. Conversely every positive distinct two-atom law yields these recurrence coefficients uniquely. Ordering the real roots gives a global smooth inverse. Thus the exact-rank-two moment image is precisely the open set D>0, not merely a local patch.

In (w,x,y) coordinates det G=1 and det J=w(1-w)(x-y)^4. Therefore det B=D^2 Delta^2>0, with Delta=(x-y)^2. This proves that B^-1 is a genuine smooth metric on the three-dimensional image. The quadratic equation is exactly -B times the differential of b/2; its explicit weights and positions remain inside D>0 at every finite time. Its energy derivative is -b-(m4-b^2)/4, so the rate bound follows without any unproved geodesic-convexity assertion.

The Euclidean-boundary caution is important and valid. The realizable triples (0,epsilon,1) approach the impossible triple (0,0,1). Independently, their fourth moment is epsilon^-1+epsilon^2, exposing the missing uniform integrability. No arbitrary continuation to the Euclidean closure is licensed. This does not threaten the smooth inverse at points inside the image or the safeguarded quadratic trajectory.

## 6. Stationarity, nonconvexity, and strong convexity

At positive weights, zero dissipation means every atom is critical and all atom energies coincide. Autonomy and local uniqueness make such a state stationary. Conversely a nonstationary trajectory cannot hit a stationary state at a finite time. The coercive quartic two-dimensional example in the author text is a genuine stationary nonminimum: moving its two atoms by a small common x-displacement lowers the objective while preserving distinctness.

The local-minimum characterization is also correct. Varying one atom with fixed positive mass forces each position to be a local minimum of F; varying two weights forces equal energy values. Conversely, disjoint local-minimum neighborhoods at a common level bound the energy of every nearby mixture below by that level. For r>1 weight variations rule out strictness. At a stationary state, mixed and pure-weight Hessian blocks vanish and the stated weighted positional Hessian remains.

For general coercive polynomial F, compactness bounds the Hessian along every trajectory. The nonnegative integrable function |grad F(X_i)|^2 has bounded derivative and tends to zero. Each particle energy has a limit c_i; the explicit relative-weight formula eliminates every particle with c_i above min_j c_j. This establishes the stated limiting energy and critical-point support of subsequential law limits. It deliberately does not assert convergence of every same-energy weight or of every particle without a further argument.

For Hess F >= lambda I > 0, the pointwise Polyak-Lojasiewicz estimate gives

    E' <= -2 lambda (E-F*),

and monotonicity of the gradient gives positional contraction at rate lambda. The finite set of trajectories is compact; a local upper Hessian bound gives integrable F(X_i)-F*. Thus every labeled weight has a strictly positive limiting value. The law nevertheless converges to the unique minimizing Dirac because the positions merge only in the limit. If r>1 the infimum F* is not attained in the distinct-r stratum. Finite-time injectivity, limiting rank collapse, and numerical conditioning are distinct claims and are kept distinct.

## 7. Spherical-action interface and distance limitation

I independently checked the source companion's local calculations. For a specified positive, collision-free C1 atomic curve, arbitrary independent smooth first-order jets force v(x_i)=x_i' and alpha(x_i)=w_i'/w_i in every representing continuity-equation field. Its action is therefore exactly G. The same jets are realizable by a potential with centered reaction values.

The companion's stronger local ambient-speed proof is valid. A test function phi satisfies an action bound involving Q_mu(phi)=mu(|grad phi|^2)+Var_mu(phi). Connecting paths of action O(h^2) stay uniformly O(h)-close on every bounded smooth test. Applying this to phi, phi^2, and |grad phi|^2 makes Q converge uniformly to its endpoint value. A compactly supported smooth function with jets phi(x_i)=u_i/w_i and grad phi(x_i)=v_i simultaneously attains d f_phi(u,v)=G((u,v),(u,v)) and Q_mu(phi)=G((u,v),(u,v)). This yields the lower speed bound; rescaling the original atomic curve yields the upper bound. No global geodesic theorem or full ambient tangent-cone identification is needed.

At rank one the intrinsic distance is the Euclidean base distance. The reaction path cos^2(theta) delta_x+sin^2(theta) delta_y has squared speed 4 and length pi, so ambient action distance is at most pi. For |x-y|>pi, equality with the intrinsic one-atom distance is impossible. Endpoint reaction rates may diverge, but their weighted-square action is integrable. This proves the required global mismatch without invoking any exact ambient distance formula.

I directly inspected [Kondratyev-Vorotnikov v2](https://arxiv.org/html/1809.03430v2), Remark 1.1 and Definition 3.15, and [Laschos-Mielke v2](https://arxiv.org/html/1712.01888v2), its parameter/angular definitions and section 3.5 convention. KV uses unit coefficients for actual transport and reaction rates and states its dynamic definition on the torus. LM's spherical quantity is angular; matching that convention yields the factor two between the unit/unit length and angle. This is not a disagreement in the reaction path's pi length. The density-PDE assumptions of KV do not apply to the linear-potential atomic model.

The optional static Dirac calculation is accepted only as a calculation in LM's static construction. A separately justified domain-specific dynamic/static identification is required before equating that construction to a dynamic action on a new domain. The source author tightened the wording accordingly. Neither the main result nor the elementary global-distance counterexample needs such an extension.

## 8. Evidence, resolved review points, and limits

The independent `check_independent.py` executes 151 exact checks with SymPy 1.14.0. They cover constrained metric inversion; gradient signs and dissipation; full mixed cometric entries; a nonconstant polynomial in the cotangent radical; multivariate Hermite jets at three atoms; unknown-support discrimination; the two-atom discriminant and boundary control; normalized nonlinear hierarchy identities through degree ten; strongly convex quadratic and forward-only quartic controls; and finite reaction/collision lengths. They also verify unchanged predecessor bindings. A copied replay of the root supplement passes its 30 checks without writing to the source directory. The frozen main author checker was separately replayed with 699 portable checks and its report is byte-identical to the frozen portable author report. The author's 708-check report differs by nine optional original-file digest checks, not by nine additional mathematical controls.

These finite symbolic controls supplement the universal proofs. They do not kernel-check the finite-GNS theorem, moment embedding, ODE completeness, compactness arguments, local metric-speed theorem, or source-domain correspondence. No inherited Lean verification is promoted to any new moving-support theorem.

The review raised and resolved two presentation risks before final freeze: the full cometric radical must not be described as constants alone, and a static twice-angle formula must not imply an unproved global dynamic/static identification on all Euclidean space. The local inverse needed for embedding, metric incompleteness, all-laws nonclosure, and asymptotic rank loss were separately verified. No substantive mathematical blocker remains within the stated scope.

The result is conditional mathematics about numerical laws and their geometry. It does not identify an actual noetic or metaphysical bearer, establish the truth or warrant of a target, authenticate observations or tokens, prove empirical correction efficacy, or settle the unbounded/infinite-rank hierarchy problem. This review grants no integration, publication, or programme-closure decision.
