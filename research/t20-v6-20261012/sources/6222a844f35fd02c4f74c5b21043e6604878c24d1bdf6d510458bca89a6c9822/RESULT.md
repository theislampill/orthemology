# When a corrective gradient is an observation: exact branch completion and its geometric cost

10 October 2026 UTC. Additive T20 mathematical investigation. Written proofs and executable controls, not kernel verification, empirical validation, an available psychological intervention, repository integration, or research closure.

## 1. Constructive question and inherited boundary

The retained posterior-gradient results establish actual representative-independent Fisher flows and positive target-likelihood tilts. A specified positive likelihood can be a possible observation. Neither statement makes a chosen descending path the guaranteed outcome of a complete experiment about an unchanged target.

This packet supplies the missing complete observation law for a prescribed smooth path, its compensating outcomes, and the sharp probability of following the entire path. The cost is exactly the length of a classical reverse-Funk geometry, whereas the path may have been selected using Fisher geometry. These geometries answer different questions: local correction speed versus probability of obtaining a whole specified observation history.

The inherited `constrained-learning-possibility-20261010/RESULT.md` already owns finite Bayes splitting, posterior martingales, and complete-branch feasibility. The new operation is continuous path completion with a sharp nested-history probability bound. Ordinary point-process filtering and reverse-Funk geometry are classical. This is a source-supported, programme-local transport, with no field-wide originality claim.

## 2. Exact path realisation

Let X take n>=2 fixed values, with strictly positive prior p. Let q:[0,T] -> Delta_n^o be C1, T finite, q(0)=p. Define

    v_i(t) = qdot_i(t)/q_i(t),
    a(t) = max_i v_i(t).

All these functions are continuous and bounded. Since sum_i q_i v_i=0, a>=0, and a=0 precisely when qdot=0. Choose any continuous m>=a and put

    lambda_i(t)=m(t)-v_i(t)>=0,
    beta(t)=exp(-integral_0^t m(s) ds),
    S_i(t)=beta(t)q_i(t)/p_i.

Then S_i(0)=1 and Sdot_i=-lambda_i S_i. Thus S_i lies in (0,1] and is a valid survival function on this horizon. Given X=i, define one observation Y in [0,T] union {infinity} by

    density(Y=t | X=i) = lambda_i(t) S_i(t),
    P(Y=infinity | X=i)=S_i(T).

Integration of -Sdot proves total mass one. Y records the first event time; infinity means no event by T. The target does not change and observation stops after that first event. No construction or nonexplosion theorem for an indefinitely repeating stochastic process is needed.

For the observable event E_t={Y>t}, including infinity, direct Bayes gives

    P(E_t)=sum_i p_i S_i(t)=beta(t),
    P(X=i | E_t)=q_i(t).

Therefore every prescribed positive C1 path is exactly realised along a nested no-event history, at positive probability through each finite horizon. An event has marginal density beta(t)m(t). For almost every t with positive density its posterior is

    r_i(t)=q_i(t)lambda_i(t)/m(t)
          =q_i(t)-qdot_i(t)/m(t).

When m=0, every lambda_i and qdot_i is zero and the event has zero density; no event posterior is required there. It must not be assigned by division by zero.

The complete experiment satisfies the exact barycentre identity

    p = beta(T)q(T) + integral_0^T beta(t)m(t)r(t) dt.       (1)

In (1), the integrand beta m r is defined as the everywhere-defined vector beta q*lambda, equal to zero wherever m=0; no undefined posterior is multiplied by zero. The identity follows componentwise by integrating -(beta q_i)'=beta q_i lambda_i. It explicitly retains the outcomes omitted by a selected descending trajectory. Prespecifying these conditional distributions is a mathematical experiment witness; it does not make a real instrument, source, event clock, calibration or permission available.

## 3. Sharp probability of the complete history

The construction is optimal among all nested observation histories realising q, including histories not presented by regular hazard functions.

**Theorem.** Suppose E_0 is certain, E_t subset E_s for 0<=s<t<=T, P(E_t)>0, and P(X=i | E_t)=q_i(t). Then

    P(E_T) <= exp(-L(q)),
    L(q)=integral_0^T max_i qdot_i(t)/q_i(t) dt.            (2)

Equality is attained by the construction in section 2 with m=a.

**Proof.** Write b(t)=P(E_t). Nestedness implies b(t)q_i(t)<=b(s)q_i(s) for each i. Thus for every partition 0=t_0<...<t_N=T,

    b(T) <= product_j min_i q_i(t_(j-1))/q_i(t_j),
    -log b(T) >= sum_j max_i [log q_i(t_j)-log q_i(t_(j-1))].

Set f_i=log q_i. Uniform continuity of their finitely many derivatives on [0,T] shows that the last sum converges to integral max_i f_i' as the mesh tends to zero: on a subinterval of length h, its difference from h max_i f_i' at the left endpoint is bounded by h times a common modulus of continuity. Summing gives a bound T omega(mesh). This proves (2). The hazard construction with m=a attains exactly exp(-L). QED.

For comparison, the largest probability of obtaining only the endpoint r=q(T) as one designated outcome of any experiment is the inherited splitting bound

    beta_endpoint = min_i p_i/r_i
                  = exp(-max_i integral_0^T v_i(t)dt).     (3)

Necessity follows from beta r_i<=p_i. The residual p-beta r is nonnegative and defines the complementary outcome; if beta=1 then r=p. Equation (2) can be strictly stronger. Equality of (2) and (3) holds iff some one coordinate i maximises v_i(t) at every t. Indeed choose an i attaining max integral v_i; equality requires the continuous nonnegative function a-v_i to have integral zero, hence vanish everywhere. The converse is immediate.

Atoms, singular decreases or an unrecorded failure mechanism do not improve the bound; they are already covered by nestedness. Resetting the meaning of the continuing history, changing the target, or conditioning retrospectively on a nonnested selection is a different contract.

### Exact smooth loop

Take n=2, T=2 and

    q_1(t)=1/2 + (1/4) sin^2(pi t/2),   q_2(t)=1-q_1(t).

The path rises from (1/2,1/2) to (3/4,1/4) and returns. On the rising half, v_1 is maximal, giving cost log(3/2). On the falling half, v_2 is maximal, giving cost log 2. Thus L=log 3 and beta_path=1/3, whereas beta_endpoint=1. This is a smooth posterior-path witness, not an autonomous gradient cycle: a nonconstant gradient trajectory cannot return to its starting point while strictly decreasing its objective.

## 4. Actual geometric identification

On the interior simplex define, for tangent u with sum u_i=0,

    F_q(u)=max_i u_i/q_i,
    D(p,r)=log max_i r_i/p_i.

F is positive on nonzero tangent vectors, positively homogeneous and subadditive; its unit ball is generally not symmetric. It is not an inner-product/Riemannian norm and is not generally smooth at ties. D is nonnegative, zero only for p=r, and satisfies the triangle inequality because max_i s_i/p_i <= (max_i s_i/r_i)(max_i r_i/p_i).

Every C1 path from p to r has integral F_q(qdot)>=D(p,r), by section 3. The straight mixture q(s)=(1-s)p+s r attains equality. Write R_i=r_i/p_i. Its logarithmic speed is

    (R_i-1)/(1+s(R_i-1)).

For fixed s this is strictly increasing in R_i, so a maximal R_i remains the maximiser throughout. Integrating gives log max R_i. Consequently D is exactly the directed length distance induced by F. Monotone reparametrisation leaves this length unchanged: moving more slowly does not improve the exact-history success budget.

These are the classical reverse-Funk metric and its weak/asymmetric Finsler structure on the simplex, with orientation fixed explicitly by the formula above. They are not a new metric invented here. The nontrivial application is that exp(-length) is precisely the optimal probability of a whole prescribed nested Bayesian path. Endpoint-only realisation corresponds to its directed distance; a detour can consume additional probability even when the final posterior is unchanged.

## 5. Fisher descent as a fully specified selected branch

Let phi be C2 on an open neighbourhood of the positive simplex, and restrict to a finite interior portion of its Fisher gradient trajectory. Put h_i=partial_i phi and hbar=sum q_i h_i. The retained negative-Fisher flow is

    qdot_i=-q_i(h_i-hbar).

Hence its minimum hazards and optimal path cost are

    lambda_i=h_i-min_j h_j,
    m=hbar-min_j h_j,
    L=integral (hbar-min h)dt.                            (4)

Adding the same scalar to every derivative representative leaves these expressions unchanged. This respects the simplex cotangent gauge. At a stationary full-support point all h_i are equal, every minimum hazard is zero and no signal is needed.

Along the selected branch,

    d phi(q)/dt = -sum_i q_i(h_i-hbar)^2 <=0.

Yet a complete passive observation about unchanged X cannot deterministically send the posterior from p to a different r: taking expectation of the conditional probabilities would give p=r. More generally, if phi is defined and convex on a convex domain containing p and all realised posterior values, the complete posterior law R obeys E phi(R)>=phi(p) whenever these expectations exist. For strictly convex phi and a posterior R that is not almost surely p, the inequality is strict. Random event times independent of X alone are not informative in this sense. The preceding C2 interior assumption does not by itself supply values on event boundary faces; the Jensen claim has this additional domain assumption. Thus all branches cannot be certified as lowering this same convex objective merely because the no-event branch does. This is classical conditional Jensen/Bayes plausibility, now applied to the actual completed gradient experiment.

This does not say that informative observations harm cognition: posterior concentration, proper-score learning and a chosen coherence/correction objective are distinct quantities. Nor does it exclude a deterministic numerical algorithm computing the posterior of evidence already received. Algorithmic iteration time is not additional evidence-acquisition time. An intervention changing X is also outside this fixed-target statement.

### Exact descending-gradient control

For n=2 take phi(q)=(q_1^2+q_2^2)/2 and p=(3/4,1/4). Until q_1 reaches 2/3 the Fisher equation is

    xdot=-x(1-x)(2x-1),
    lambda=(2x-1,0).

The elapsed time is integral_(2/3)^(3/4) 1/[x(1-x)(2x-1)]dx=log(8/3). Only state 1 can generate an event, so every positive-density event posterior is (1,0). The no-event endpoint is (2/3,1/3), with exact optimal probability 3/4; the event outcome has probability 1/4. Therefore

    phi(p)=5/16,
    phi(no event)=5/18 <5/16,
    E phi(posterior)=(3/4)(5/18)+(1/4)(1/2)=1/3 >5/16.

The difference is 1/48. This is a complete source-law control, not just an adverse hypothetical update. In the declared convex feasible set C={q:q_1<=3/4}, the entire gradient path is feasible while every event branch is infeasible. Path feasibility alone therefore cannot discharge the inherited complete-experiment requirement.

## 6. Transport through the retained audit signature

For the retained fully positive joint law of target i and audit label j, write mu_ji=w_j p_ji and q_i=sum_j mu_ji. The target-only Fisher flow already proved in `finite-audit-gradient-classification-20261010` uses a common positive target tilt. Apply the new first-event instrument with state-dependent likelihood S_i(t) or lambda_i(t)S_i(t), independent of audit label conditional on i.

Along survival, the old signature's every conditional p_j and q receives the same positive tilt S; w_j changes by its normalising factor. Conditional on an event at time t, its pre-event conditional rows update by

    p_j -> N(p_j * lambda(t)),    q -> N(q * lambda(t)).

Both updates and the event-time marginal density beta(t)m(t) are determined by the retained initial signature and the selected target objective. Equal retained signatures therefore yield the same event-time law and the same retained posterior answers on every defined event/survival branch, even if the hidden audit frequencies differ. This is an actual stochastic-operation transport for this declared target-only instrument, for the event time and retained posterior answers. It does not determine the joint distribution of the audit label and event time: audit frequencies remain hidden and may differ.

Minimum hazards generally have zeros. A positive-density event can leave the original interior manifold. Since all pre-event p_j are strictly positive and lambda is nonzero, every audit label remains feasible, and all conditional rows acquire the same nonempty target support. The event formula is elementary conditional Bayes on that boundary; the old interior flow theorem is not silently applied there. The observation stops, so no further boundary-gradient evolution is asserted. Choosing m>a, for example m=a+epsilon, keeps each lambda positive but strictly reduces survival probability by exp(-epsilon T). Attainment and strict-positivity are different contracts.

### 6.1 General descended audit gradients also admit a common completion

The contributed proof in `../corrective-transport-check-20261010/CONTRIBUTED_SECTION_V2.md` extends the operational result beyond target-only objectives. Under the inherited exact global descent criterion, the joint cell logarithmic velocities are already signature-determined:

    V_(j,i)/mu_(j,i)=-(h_i-q·h)-a_(j,i)/(w_j p_(j,i)).

If a weight w_j varies on the signature fibre, the criterion forces a_j=0. Otherwise w_j is uniquely determined there. Thus all cell velocities, their maximum m, and the minimum cell hazards are common across every equivalent initial lift throughout the shared flow interval. Their integrated conditional survival functions are common too. There is therefore one identical complete first-event kernel for all those lifts, with no hidden selection based on discarded audit frequencies.

After an event, let c_j=sum_i p_(j,i)lambda_(j,i). Label j is feasible iff c_j>0; when feasible its conditional target row is p_j*lambda_j/c_j. The target marginal is q-qdot/m. These quantities are determined by the signature. Entire audit rows can disappear, so the output explicitly includes feasibility flags and leaves impossible conditional rows undefined. No later boundary flow or audit-label frequency recovery is claimed.

The attained probability is optimal for the stipulated full-source trajectory, not a claimed optimum among all alternative lifts of the same signature curve. The supplement gives full proofs and exact conditional-objective boundary controls. This is a collaborating investigator's mathematical contribution, separately subjected to the independent review; it is not counted as an additional independent review by its contributor.

## 7. Source reading, ancestry and credit

- Eden and Brown, *Continuous-Time Filters for State Estimation from Point Process Models of Neural Data*, Statistica Sinica 18 (2008), 1293–1310, [publisher PDF](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A18n44.pdf). Continuous contextual inspection of sections 1–5 and the discussion confirms the classical separation between no-event evolution and event-induced likelihood multiplication. Equations (3.6)–(3.9), (4.1) are relevant. The paper's moving-state neural model, Gaussian approximation and simulation results are not transported as validation of this finite fixed-target construction. The original Snyder book/paper was not directly read; it is an attribution lead through this primary treatment.
- Cormac Walsh, *Gauge-reversing maps on cones, and Hilbert and Thompson isometries*, Geometry & Topology 22 (2018), 55–104, [publisher PDF](https://msp.org/gt/2018/22-1/gt-v22-n1-p02-p.pdf), introduction and sections 2.1–2.4 inspected for the cone-order gauge and orientation. Its reverse-Funk definition gives exactly log max(r_i/p_i) on the positive orthant's probability cross-section. The paper's isometry theorems are not imported.
- Inherited finite splitting/martingale and feasibility results remain credited to `constrained-learning-possibility-20261010`, including its primary literature attribution. The retained posterior-gradient and finite-audit classifications supply actual flows; neither supplied this complete first-event experiment or path-budget result.

Root derived the author construction and geometric mapping. A collaborating investigator independently selected the same first-event route before exchanging details, then supplied the arbitrary-nested-history strengthening and attacked the proof, endpoint comparison, boundary and feasibility claims. Those contributions are credited as mathematical collaboration, not external validation. Universal statements are supported by the displayed written proofs; exact finite/symbolic controls corroborate them without replacing them. No Lean, human-specialist, psychology, actual warrant or divine-source claim follows from this packet.

## 8. Verification contract

Run `python3 verify.py` with Python 3 and SymPy. The author run passed 1,519 exact rational/symbolic assertions covering 100 positive-law pairs, gauge and hazard identities, barycentres, endpoint/partition controls, convex objective and feasibility controls, elapsed time, loop values, and two distinct-weight audit examples. These finite checks do not establish the general partition limit, existence theorem or universal geometric identification; their written proofs carry that scope. The contributed supplement has its own independently authored controls and is credited as collaboration. The independent review receipt is a separate evidence object; author and collaborator checks alone do not constitute that acceptance.
