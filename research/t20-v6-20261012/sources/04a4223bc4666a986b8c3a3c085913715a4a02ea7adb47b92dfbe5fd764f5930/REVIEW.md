# Independent review: nonautonomous common-energy reverse lift

10 October 2026 UTC. Independent ordinary mathematical review and finite exact controls. This is a separately bound successor review. Previously accepted autonomous and squared-energy packets remain unchanged.

## Verdict and exact scope

PASS, with no blocking findings, for the frozen `nonautonomous-energy-drift-reverse-lift-20261010/RESULT.md`, SHA256 `5ccaf69ac4c3b5b74471bdea10be494482bfd121c05233a8bc67810bdf0bbf56`. The author manifest SHA256 is `7d5818a87e798dae073455ff499b03e5c0d0796e98e2a655b07376db19d888e4`.

The theorem is on a prescribed finite horizon [0,T]. Its coefficients belong to common finite polynomial bases and are continuous in time. It assumes a fixed coercive SOS H≥1 and constants C,D≥0, κ>0 with the actual SOS certificates CH−b_t·∇H and V_t+D−κH at every time. The supplied path is normalized, positive on every polynomial square, C¹ in every polynomial coordinate through the endpoints, and satisfies every polynomial hierarchy equation. No initial law, rank, radial domination or tail assumption is added.

The whole frozen proof, summary and checker were inspected. The independent replay records 84 author checks and 56 independently written checks, including a continuous-but-nondifferentiable coefficient schedule producing a C¹ moment path that is not C². All frozen author files and the 15 declared original inherited files match their bindings and packaged copies. The exact replay and preservation results are in REPLAY_RESULTS.json and REVIEW_RECEIPT.json. These are finite evidence, not a formal proof of the universal analysis.

## 1. Moving polynomial tests and the clock

The common finite-basis condition is sufficient to make t↦L_t(K_t) continuous, where K_t=V_t+D. Thus a=exp(−∫L(K)) is positive C¹ and A=aL satisfies A′_t(p)=A_t(b_t·∇p−K_tp) for fixed polynomial p. Since K_t=κH+P_t is SOS, its abstract evaluation is nonnegative and a≤1. The pointwise lower bound H≥1 is not incorrectly used to evaluate H−1 in an unrepresented square-positive functional.

For B_n=e^(−Cnt)A_t(H^n), the moving-test differentiation is valid because only its scalar factor varies and H is fixed. The exact derivative is

    B′_n = −n e^(−Cnt)A_t(H^(n−1)Q_t) − e^(−Cnt)A_t(K_tH^n).

Every discarded product is SOS. Consequently B′_n≤−κe^(Ct)B_(n+1), including n=0 by the mass equation. No derivative of b_t, V_t, Q_t, P_t or their SOS decompositions is used. The decomposition of each SOS polynomial need not vary continuously because the argument evaluates the polynomial itself.

The increasing clock θ=κ∫₀ᵗe^(Cr)dr has θ′=κe^(Ct). Applying the inherited repeated-integral argument in this clock gives B_n≤n!θ^(−n), hence A_t(H^n)≤n!r_C(t)^(−n), where r_C=e^(−Ct)θ. The resulting width satisfies r′_C=κ−Cr_C, r_C(0)=0; it equals κ(1−e^(−Ct))/C for C>0 and κt at C=0. The signs, exponential factor and zero-C limit all check independently. The packet derives this exact clock width, without proving or needing an optimality theorem over all possible certificates.

## 2. Static representation and the time-dependent residual

At every positive time the weighted Cauchy–Schwarz estimate supplies the same compact-fibre Lemma F as in the accepted autonomous theorem, with common width r_C(t)/2. Positive-time representation is therefore obtained before any nonpolynomial measure test is used. Exponential-energy summation is asserted only at rates σ<r_C(t); compact-sublevel determinacy then gives a unique joint representing measure without coordinate Carleman bounds.

On an interior interval, every fixed polynomial coordinate has a uniform bound and the positive mass a is bounded away from zero. Tightness, higher-moment uniform integrability and joint determinacy prove weak continuity of the laws. Since r_C is increasing, ε=r_C(η)/4 gives a common rate on [η,B]. Actual-measure Cauchy–Schwarz bounds ∫|p|e^(εH) uniformly for each fixed polynomial. A changing polynomial with bounded coefficients in a common finite basis is controlled by a finite sum of these estimates. This is exactly what is required for b_t·∇p, K_tp, p b_t·∇H and their products with fixed powers of H.

The residual D_(u,v) is again order at most one, with finite time-integrated coefficient measures. The product rule

    (b_t·∇−K_t)(pP(H))=(b_t·∇p−K_tp)P(H)+p(b_t·∇H)P′(H)

has no time derivative. Small scalar-energy Fourier frequencies are justified by the uniform weighted exponential bounds. Scalar holomorphic continuation uses those same finite-basis bounds under space/time integration. The finite signed α_p and β_p retain their correct signs and their combined relation, including the β_p(χ′) contribution. No separate vanishing of the two measures is asserted.

The localization χ(H)D_(u,v) is the distributional product, and coercivity of the fixed H gives compact support. Its first-order coefficient bound permits coordinate exponential approximation in C¹ on that compact set, followed by Fourier inversion. Choosing χ=1 near the energy range of a given compact spatial test gives the actual compact-test PDE. Fixed H is essential to this particular argument: it supplies one common scalar variable, its fibres and compact cutoffs. The proof is not extended to unrelated moving coercive energies without common certificates.

Time continuity of the drift and killing coefficients, together with weak continuity on compact test supports, makes the PDE's right integrand continuous. The time-dependent compact-test rule follows after the PDE is proved. This repeats an already accepted analytic mechanism with its genuinely new uniform time bounds checked, rather than claiming that polynomial equations alone identify a PDE.

## 3. Two-time flow and coefficient regularity

For a characteristic, H′≤CH. Gronwall confines a finite-horizon trajectory to a compact energy sublevel depending on its starting point. On that sublevel the continuous-time polynomial vector field has uniform spatial Lipschitz and boundedness estimates. Local existence and continuation therefore reach every prescribed later time. The common basis is important for those uniform local bounds.

All spatial derivatives of the field are continuous in time and locally uniformly bounded, so standard variational equations give smooth dependence on the initial point. Backward uniqueness only along already existing finite trajectories makes the forward map injective. Its nonzero spatial Jacobian gives a diffeomorphism onto the open image; no globally complete backward flow or all-space surjectivity is assumed.

The terminal test U(r,x)=E_(t,r)(x)f(Φ_(t,r)(x)) is C¹ in its starting time even though the coefficients need not be differentiable in time. The two-time cocycle, the compact-uniform expansions Φ_(r+h,r)(x)=x+h b_r(x)+o(h), E_(r+h,r)(x)=1−hK_r(x)+o(h), and local inverse maps give ∂_rU=−b_r·∇U+K_rU. Its needed spatial derivatives and its time derivative are continuous on compact sets. Thus it belongs to the proved time-dependent test class after multiplication by a fixed spatial cutoff.

The cutoff has zero time derivative. Backward-equation cancellation leaves only ν_r(U b_r·∇χ_N). Since K_r≥0, |U|≤||f||∞. Common polynomial degrees and bounded coefficients give a uniform polynomial majorant for b_r, and uniform high moments remove the residual. One can alternatively use the simpler bound N^(−1)||f||∞||∇χ||∞sup_r∫|b_r|dν_r. No global derivative bound on U or compactness of inverse-flow supports is needed.

## 4. Initial law, endpoint estimate and converse

Near zero, continuity of the original radial coordinates gives tightness and higher-moment uniform integrability. One subsequential probability limit has all polynomial moments and represents L₀. The two-time flow-weight tests converge locally uniformly as their start time tends to zero, by continuous dependence of the ODE and weight; boundedness and tightness handle the tails. A single initial law therefore represents the full path.

At positive time the map is injective onto its actual image and the weights are strictly positive. Inverse pushforward and division by the weight recover the initial measure. In the normalized case this initially recovers proportional probabilities, and total mass fixes the factor. Unbounded inverse weights on the image cause no difficulty for equality of known positive measures. Joint positive-time determinacy then gives the stated full-law-fibre classification, finite-time separation, and preservation of finite initial full rank. It does not make initial moment indeterminacy disappear.

The endpoint estimate has the correct reversed Gronwall direction:

    H(Φ_(r,0)(x)) ≥ e^(−C(t−r))H(Φ_(t,0)(x)).

Together with K_r≥κH, integration gives ∫₀ᵗK_r(Φ_(r,0))dr≥r_C(t)H(Φ_(t,0)), proving ∫e^(r_C(t)H)dν_t≤1. It is proved after characteristic identification; the earlier divergent endpoint series is never used.

For the converse, the inherited polynomial sublevel envelope converts H(Φ_(t,0)(x))≤e^(CT)H(x) into a fixed polynomial initial-coordinate bound on [0,T]. Common finite coefficient bases similarly control all generators b_t·∇p−K_tp. Every all-moment initial law therefore permits dominated differentiation, continuously through zero, without differentiating the coefficients. The mass remains strictly positive and normalization restores the original V_t hierarchy.

Continuation is explicitly tied to a prescribed future coefficient family satisfying the local-window assumptions. Nothing in the theorem selects an unspecified future schedule or covers an arbitrary hidden-memory policy.

## 5. Discriminating exact controls

### Moving quadratic transport

For V_t=(x−t)², b_t=−2(x−t), H=1+x², the displayed certificates with C=T², κ=1/2 and D=T²+1/2 are exact. Their scalar remainder T²−t² is nonnegative only on the declared horizon; the independent controls reject a horizonless reuse.

The two-time affine flow, start-time derivative, cocycle, integrated killing and its start-time derivative all check. The latter includes the D shift with the correct sign. Direct backward-test controls for terminal monomials verify the complete two-time cancellation rather than just the forward ODE.

The transported initial two-atom log-weight difference is (1−e^(−2t))/2, whereas fixed-position pure killing gives t+t². These are distinct laws. The earlier pure-killing Theorem V already handled continuously moving quadratics; the new example supplies changing transport, and the author correctly preserves that credit boundary.

For the original unshifted mass, its second derivative contains V²−b·∇V−∂_tV. In the example this equals r⁴+4r²+2r. The specified trajectory has r=−3/8 at t=(log2)/2 and gives −687/4096. The negative-second-derivative claim is correct for that unshifted mass only. An independent control verifies that it does not transfer to the particular D-shifted mass, which is positive at the same state.

### Continuous coefficients really suffice

An additional independent discriminator uses [0,1], H=K=1+x² and b_t(x)=a(t)x with a(t)=|t−1/2|. Set C=κ=1 and D=0. Then P_t=0 and Q_t=1+(1−2a(t))x² are SOS at every time. The coefficient a is continuous but not differentiable at 1/2.

For initial point z, the normalized Dirac path has position z exp(g(t)), where

    g(t)=t/2−t²/2                    for t≤1/2,
    g(t)=t²/2−t/2+1/4               for t≥1/2.

The two formulas and their first derivatives agree at 1/2, but the second derivative of the position jumps by 2z exp(1/8). For z≠0 the moment coordinate L_t(x) is C¹ and not C². Every theorem hypothesis is met. This confirms that a proof demanding higher coefficient or moment time derivatives would impose a real extra assumption; the reviewed proof does not.

## 6. Sources and nonclaims

The review inspected the prior pure-killing Theorem V, the separately accepted autonomous compact-energy localization proof, the static compact-fibre bridge and the polynomial sublevel envelope used in the converse. Their classical representation and semialgebraic ingredients remain explicit inherited dependencies. This successor introduces no new static moment theorem, compact-fibre theorem or coercivity-rate theorem. The needed nonautonomous first-order identities and compact-uniform ODE reasoning are discharged in the proof and controls; no general transport uniqueness theorem is invoked.

The author packet includes exact copies of all source files required by its checker. The review separately compared its 15 declared original source files with those packaged copies before and after isolated replay. No new primary PDF archival claim is made. The accepted autonomous review's source checks remain scoped to those inherited lemmas.

No conclusion is drawn from bare pointwise coercivity of V_t, finite moment truncations, merely pointwise energy inequalities without the stated SOS certificates, arbitrary adaptive control, global time-uniform constants, unspecified future schedules, convergence, or total energy monotonicity under a moving objective. The optional differentiable-objective discussion correctly includes the external-work term. There is no formal-kernel verification, protected integration, mathematical priority finding, empirical/noetic interpretation or T20 closure.
