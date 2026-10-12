# Finite polynomial state cannot close unrestricted normalized gradient dynamics

11 October 2026 UTC. Additive ordinary mathematics in active T20. The root proposed the normalized all-laws obstruction and the binomial construction; this worker checked the scope, supplied both complete proofs and executable controls. This is participating author work, not independent review, a formal-kernel proof, field-priority certification, protected integration or programme closure.

## 1. Result and the increment

Fix a nonconstant real polynomial F on R^d, d >= 1. Retain finitely many expectations of polynomials, at least one nonconstant. There is no vector field, even an arbitrary nonlinear or discontinuous one, depending only on that retained vector that reproduces its normalized gradient-and-killing derivative for every finitely supported initial probability law.

The obstruction is stronger than the absence of a finite invariant space for an unnormalized linear generator. It is witnessed by two genuine finite positive laws that have the same retained vector AND the same expected objective, but different derivatives of a retained coordinate. Both laws have actual local weighted characteristic trajectories. The construction also yields different retained outputs at every sufficiently small positive time, so the failure is not merely a formal signed-moment calculation or an ODE uniqueness issue.

This concerns the fixed finite summary z(mu)=(mu(phi_1),...,mu(phi_m)) on the class of ALL finitely supported laws on R^d. It does not prohibit finite coordinates on a supplied rank-restricted or otherwise invariant family of laws. It does not concern arbitrary encoders, nonpolynomial observables, approximation, or states supplied with additional law information or memory.

### Deduplication and ownership

The same-session companion `polynomial-linear-closure-boundary-20261011/NOTE.md` already gives the elementary degree-raising observation below and expressly leaves nonlinear normalized closure open. It was generated from the root's suggestion shortly before this investigation; it is not separately reviewed inherited evidence. That lemma is independently checked here, with no second increment claimed for it.

The current tensor-moment report, section 4, supplies known finite-support interpolation closure. The joint-atomic report, section 4, and two-atom chart supply unknown-support, fixed-rank finite nonlinear closure. The state-dependent-gradient report, section 3, already uses equal-state/different-velocity witnesses. The tensor-likelihood report, sections 3-5, already excludes arbitrary nonlinear decoders for specified finite product-moment passive updates. The leafwise-noetic report, sections 1-5, classifies fixed-objective Fisher descent on proper finite product-interaction summaries. The measure-moment report supplies a different, all-orders indeterminacy obstruction. The ordered-control report, section 3, gives exact finite jets, explicitly without claiming finite state closure. These antecedents are retained, not rediscovered.

No exact theorem with the present quantifiers was found in the bounded current report scan and targeted readings recorded in DEDUP_SCAN.json and SOURCES.md. This is a project-relative extension of the inspected boundary, not an exhaustive absence or historical originality claim. No other report was edited.

## 2. The actual law and the closure contract

Let P=R[x_1,...,x_d] and write mu(p)=integral p dmu. Define

    B_F p = -grad F dot grad p - F p.

For any initial finite probability mu=sum_j w_j delta_(x_j), let X_j(t) solve X_j'=-grad F(X_j), X_j(0)=x_j. Polynomial smoothness gives a common nonzero local interval for the finitely many initial atoms. After shortening the interval, all these paths stay in a common compact set. Put

    a_j(t)=exp(-integral_0^t F(X_j(s)) ds),
    Z(t)=sum_j w_j a_j(t),
    mu_t=sum_j [w_j a_j(t)/Z(t)] delta_(X_j(t)).        (1)

Each a_j and Z is finite and strictly positive. Termwise differentiation of this finite sum proves

    d/dt mu_t(p)=mu_t(B_F p)+mu_t(F) mu_t(p).          (2)

No global completeness, coercivity, moment tail or abstract hierarchy representation is needed for this local result. A common interval is obtained for a pair of finite laws by taking the union of their supports.

Fix phi_1,...,phi_m in P. Universal autonomous closure means a single function

    V: z(P_fin(R^d)) -> R^m

such that z(mu_t)'=V(z(mu_t)) for every finite initial law and every admitted local trajectory (1). In particular it requires equality at t=0. No regularity is assumed for V. A contradiction at this necessary first derivative already disproves the contract.

## 3. The general finite evaluation lemma

**Lemma.** Let X be any set, S a finite-dimensional real vector space of real-valued functions on X containing 1, and g a function not in S. There are finitely supported probability laws mu and nu on X with

    mu(s)=nu(s) for every s in S,     mu(g) != nu(g). (3)

Their combined support can be chosen to have at most dim(S)+1 points.

**Proof.** Set W=S+R g, so dim(W)=dim(S)+1. Evaluations ev_x belong to W*. They span W*: otherwise their span would have a nonzero annihilator w in W, and w(x)=0 for every x in X would make w the zero function, a contradiction. Choose a basis of W* consisting of at most dim(W) evaluations. The functional lambda defined by lambda(s+c g)=c is a finite linear combination sum_j c_j ev_(x_j) of those evaluations. Hence the finite signed measure sigma=sum_j c_j delta_(x_j) annihilates S and has sigma(g)=1. Since 1 is in S, sum_j c_j=0. The positive and negative parts of sigma therefore have the same total mass a>0. Normalize them to mu=sigma_+/a and nu=sigma_-/a. Then (3) holds, with mu(g)-nu(g)=1/a. This constructs genuine probability laws; the signed measure is only an intermediate linear-algebra witness. QED.

If positive weights at every point of one common finite support are desired, choose any strictly positive probability rho on the union of these supports and put mu_theta=(1-theta)mu+theta rho and nu_theta=(1-theta)nu+theta rho for 0<theta<1. They remain equal on S and differ on g by the nonzero factor 1-theta. Thus the obstruction is not forced by a boundary point of that finite simplex.

## 4. The normalized polynomial no-go theorem

**Theorem.** Suppose D=deg(F)>=1 and K=max_i deg(phi_i)>=1, with zero descriptors omitted from this maximum. The universal autonomous closure contract in section 2 fails. The witness laws can be chosen with the same value of mu(F), in addition to the same descriptor.

**Proof.** Choose one retained coordinate p=phi_i with deg(p)=K. For nonzero p, the top homogeneous part of B_F p is -F_D p_K. It is nonzero because the real polynomial ring is an integral domain. The gradient term has degree at most D+K-2 (and vanishes if p is constant), while Fp has degree D+K. Thus

    deg(B_F p)=D+K.                                   (4)

For S=span{1,F,phi_1,...,phi_m}, every element has degree at most max(D,K). Since D,K>=1, D+K>max(D,K), and B_F p is not in S. Apply the finite evaluation lemma with g=B_F p. It gives mu and nu agreeing on F and every phi_i, but differing on B_F p. Formula (2) then gives

    [d/dt mu_t(p)-d/dt nu_t(p)]_(t=0)
      =mu(B_F p)-nu(B_F p) != 0.                     (5)

The normalization terms cancel exactly because BOTH mu(F)=nu(F) and mu(p)=nu(p). Yet z(mu)=z(nu), so no single value V(z(mu)) can equal both derivative vectors. QED.

The evaluation proof gives a combined support bound dim(S)+1 <= m+3. It is a sufficient bound, not a minimality statement. In particular this is not a counterexample against every fixed-rank family: the chosen witnesses need not satisfy such a rank promise.

For comparison, (4) also implies deg(B_F^n p)=deg(p)+nD. The iterates of a nonzero p have distinct degrees and are linearly independent. Consequently P has no nonzero finite-dimensional B_F-invariant subspace. This is the independently checked same-session companion lemma; the passage from it to the normalized arbitrary-vector-field assertion is supplied by (3)-(5), not by assuming nonlinear closure is linear.

**Actual finite-time consequence.** Let h(t)=mu_t(p)-nu_t(p) for the two local trajectories. Then h(0)=0 and h'(0)!=0. Hence h(t)/t tends to a nonzero number as t decreases to zero. There is epsilon>0 such that the retained outputs differ for every 0<t<epsilon. For each such t no deterministic map of the common initial descriptor alone can return both actual retained outputs. No uniqueness theorem for a proposed coarse ODE is being assumed.

## 5. An explicit binomial witness for every F and descriptor

The preceding lemma uses finite evaluation duality. The following separate construction gives a formula that also matches ALL moments below one degree.

Set M=D+K and choose v in R^d with F_D(v)p_K(v)!=0. Such v exists since their product is a nonzero polynomial function. Let

    mu=2^(-(M-1)) sum_(0<=j<=M, j even) binom(M,j) delta_(jv),
    nu=2^(-(M-1)) sum_(0<=j<=M, j odd)  binom(M,j) delta_(jv). (6)

The even and odd binomial sums are both 2^(M-1), by adding and subtracting (1+1)^M and (1-1)^M. All displayed weights are positive; M>=2 and v!=0, so these are probabilities on distinct nodes.

For a one-variable polynomial q, the forward difference Delta q(s)=q(s+1)-q(s) lowers positive degree by one and multiplies the leading coefficient by the previous degree. Induction also gives

    Delta^M q(0)=sum_(j=0)^M (-1)^(M-j) binom(M,j) q(j).

Therefore the even-minus-odd sum annihilates every polynomial q of degree < M, and equals (-1)^M M! a_M when q has degree M and leading coefficient a_M. Restricting any multivariate polynomial r of total degree < M to r(jv) proves

    mu(r)=nu(r) for every deg(r)<M.                   (7)

This includes every descriptor and F, since K,D<M. The leading coefficient of (B_F p)(sv) is -F_D(v)p_K(v). Consequently

    mu(B_F p)-nu(B_F p)
      =(-1)^(M+1) M! F_D(v)p_K(v) / 2^(M-1) != 0.   (8)

Equation (8) is exactly the derivative gap after normalization. The combined support has M+1 points. Unlike the dimension-based construction, it matches every polynomial of degree <=M-1, including many observables not retained in the descriptor. Neither support bound is claimed optimal.

For rational input polynomials a suitable integer v can be found with exact arithmetic by testing the grid {0,...,M}^d: a nonzero polynomial of degree at most M in each coordinate cannot vanish at every point of that grid, by repeated univariate interpolation. This is a finite existence/construction argument, not an efficiency result. Arbitrary real coefficients without effective names and equality tests do not supply a computational algorithm merely by appearing in the theorem.

## 6. A concrete quadratic control with genuine global trajectories

Take d=1, F(x)=x^2/2, and descriptor (mu(x),mu(x^2),mu(x^3)). Here D=2, K=3, M=5 and v=1. Formula (6) gives

    mu=(delta_0+10 delta_2+5 delta_4)/16,
    nu=(5 delta_1+10 delta_3+delta_5)/16.

Both laws have moments

    m_0=1, m_1=5/2, m_2=15/2, m_3=25, m_4=90.

Their fifth moments are 340 and 695/2, respectively. For p=x^3,

    B_F p=-3x^3-x^5/2,
    [mu_t(p)]'_(0)=-605/4,
    [nu_t(p)]'_(0)=-155,
    difference=15/4.

Their expected objective is the same 15/4, so this is not a failure caused by omitting the instantaneous energy alone. The first two descriptor derivatives coincide; the third does not. Each law has rank three, outside the positive rank-two chart that uses these same three raw moments.

For every t>=0, the actual trajectories are given exactly by contracting each initial atom to e^(-t)x and multiplying its initial weight by

    exp[-(1-e^(-2t))x^2/4],

then normalizing. Thus this displayed example is globally forward defined. This stronger existence property belongs to the quadratic control, not to every polynomial F in the theorem.

The script also mixes each law equally with the uniform law on {0,1,2,3,4,5}. The resulting pair has positive weights on the same six-point support, the same descriptor and objective, and derivative gap 15/8.

## 7. Positive boundaries that remain available

1. **Constant cases.** If every descriptor is constant, its derivative is zero. If F is constant, its gradient vanishes and its common scalar weight cancels, so the entire normalized law is stationary. These are excluded cases, not exceptions to the theorem.
2. **Known finite support and fixed rank.** Interpolation on a known finite support and the supplied moving rank-r atomic charts remain valid. Their law domains impose information absent from the all-laws contract. The finite-support size here is allowed to depend on the chosen descriptors; no one fixed universal rank cutoff is promised by this theorem.
3. **Other invariant law families.** For F=x^2/2, a Gaussian initial law N(a_0,v_0), v_0>0, stays Gaussian under the same weighted contraction. With q(t)=(1-e^(-2t))/4, its mean and variance are

       a(t)=e^(-t)a_0/[1+2q(t)v_0],
       v(t)=e^(-2t)v_0/[1+2q(t)v_0].

   Completing the square in the weighted initial density proves this formula, and differentiation gives a'=-a-av and v'=-2v-v^2. Thus (a, second raw moment) closes nonlinearly on this separately justified family. This is a positive scope control, not a new classification of Gaussian flows. Gaussians are not members of the finite-support counterexample class, nor does the family contain all finite laws.
4. **Declared operations and extra state.** The theorem fixes this normalized gradient-and-killing operation and finite polynomial expectations. It does not classify nonpolynomial descriptors, arbitrary encodings, restricted reachable families, augmented states, or history-based prediction. Finite jet accuracy at an increasing degree budget remains available. Approximate closure and error bounds require separate hypotheses.
5. **Interpretation.** No impossibility of finite Riemannian models, finite cognition, noetic restoration, source warrant, or empirical prediction is inferred. The mathematical result identifies a failed universal contract for one explicitly specified numerical law class and operation.

## 8. Evidence and use

Run `python3 verify.py --output-dir private-locator:ff65c22270810eeb9ec1` from this directory. It checks bound input snapshots, exact binomial identities, the explicit pair, normalization cancellation, same-support positive mixing, multivariate direction selection, maximal-degree output, the finite-evaluation construction, constant countercontrols, and the Gaussian formulas. It writes exact machine-readable results in the requested output directory. These finite checks supplement the universal written proofs and do not replace them with enumeration.

SOURCES.md records the bounded primary-literature comparison. No result from that comparison is needed as an unproved premise of sections 2-7. Independent review, preservation, integration, and broader research decisions remain separate.
