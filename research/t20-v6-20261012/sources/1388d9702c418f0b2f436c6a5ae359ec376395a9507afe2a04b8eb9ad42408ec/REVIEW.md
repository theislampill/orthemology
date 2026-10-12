# Focused independent review: audit/flow covariance and discrete transfer

11 October 2026 UTC. Additive review of received `Cross_Front_Theorems.md` §§12–14 and `Dot_Handoff.md`. No edits to received or inherited artifacts, integration, closure, or target-warrant claim. The conclusions are ordinary mathematical review plus exact controls, not formal-kernel verification or a literature-priority survey.

## Result first

- **Accept I and J on their declared domains.** J is a genuine additional universal-audit symmetry classification, not the existing posterior-signature descent classification. Its metric corollary is correct, including n=1, with its connected Cartesian-product position-domain hypothesis retained.
- **Accept the Euler countercontrol:** its two positive, descending paths differ by TV 1/117. It tests audit fidelity, a different invariant from the inherited full-moment Euler square-positivity obstruction.
- **Deduplicate K's constructive numerical formula and joint split repair.** The identical minimum-shift reciprocal step, joint particle transport, covariance descent, shift invariance, and first-order consistency are already in `gradient-discretization-fidelity-20261010/RESULT.md` §§4–6. The useful addition is the audit-commutation theorem and acceptance test.
- **Actual inherited implementation passes the new test.** An exact two-atom control using its `quartic_rational_step`, not a reimplementation, commutes with an origin-labelled positive audit. No existing implementation defect is established.
- No contradiction with fixed-marginal or correlated-target correction: those use constrained full-law geometry, state-dependent entropy scores, and a different preservation contract. A supplied target remains a hypothesis, not a warrant.

## 1. Theorem I: precise acceptance and inheritance

For unchanged labelled maps q_t and factors A_t>0, B_A B_R = B_R B_A = B_(AR), so pushing forward gives the claimed retrospective repair. On the finite origin domain of the packet, all finite positive factors automatically have the needed finite positive normalisers. A general-measure extension must separately require 0<integral AR dmu<infinity; finiteness of integral A and integral R alone does not imply this.

The explicit centred weight solution is correct:

    w_i(t)=w_i(0) exp(integral_0^t c_i(x(s)) ds) / sum_j w_j(0) exp(integral_0^t c_j(x(s)) ds).

Normaliser feedback is permitted because x(s) and the unnormalised per-label factors do not depend on initial weights. The interaction example beta|sum w_i x_i|^2/2 correctly breaks the position condition through xdot_i=-beta sum w_j x_j. The stated initial velocity difference 1/4 and finite Euler position difference 1/16 at h=1/4 are correct.

`joint-atomic-gradient-lift-20261010/RESULT.md` §§2–3 already has exactly xdot_i=-grad F(x_i), wdot_i=-w_i(F_i-E), and explicit unchanged-characteristic exponential factors. It credits `complete-flow-finite-rank-20261010` for the representation. I is an explicit source-revision consequence of that inherited solution, not a new atomic flow or new representation theorem. Its operation-normaliser product identity is also correct; endpoint commutation does not imply equality of the two intermediate normalisers.

## 2. Theorem J: proof audit

On Delta_(n-1)^interior × X, with a C1 vector field and unique local flows, all positive weight audits act in u_i=log(w_i/w_n) as all translations of R^(n-1). Flow commutation implies vector-field equivariance by differentiating at zero. Equivariance implies flow commutation by uniqueness. Translation invariance says both udot and xdot depend only on x. Solving the simplex-tangency equation yields

    xdot=v(x),
    wdot_i=w_i(c_i(x)-sum_j w_j c_j(x)).

Conversely this field is equivariant. c_i have the same C1 regularity in x as the transformed field, up to a common additive gauge. No global completeness is implied. The product with the entire positive simplex is load-bearing: restricted reachable weights, boundary weights, changed labels, or audit-dependent domains are different problems. The packet correctly warns that a lattice-generated audit group need not imply invariance under its real span.

For n=1 the audit is the identity, weight tangent is zero, and every allowed position field v(x) qualifies. Taking c_1=0 recovers the displayed form; no hidden n>=2 requirement remains.

### Standard metric corollary

For g=(1/alpha) sum dw_i^2/w_i + sum w_i |dx_i|^2 and C2 E, the intrinsic weight equation gives

    d/dt log(w_i/w_n) = -alpha (partial_i E-partial_n E).

Weight-independence of this expression implies E is affine on each entire simplex fibre. Write E=sum_i w_i V_i(x), with C2 coefficient functions (recoverable from finitely many fixed interior evaluations of the affine function). The position velocity is

    xdot_j = -(sum_i w_i grad_(x_j) V_i(x))/w_j.

If independent of w, the identity sum_i w_i grad_(x_j)V_i = -w_j v_j for all positive w implies grad_(x_j)V_i=0 for i!=j and grad_(x_j)V_j=-v_j. This uses an identity on an open simplex, not a boundary regularity assumption. On a connected Cartesian product X_1×...×X_n, each V_i depends only on x_i. Conversely E=sum w_i V_i(x_i)+C gives xdot_i=-grad V_i and c_i=-alpha V_i. All conclusions follow.

For n=1, E(x)=V_1(x)+C is tautologically every C2 energy. The theorem restricts nothing further in that case.

### Position-domain and law-level restrictions

The existing distinct-atom manifold is Delta°×Conf_n(R^d), modulo simultaneous permutations, rather than the corollary's full Cartesian position domain. J's vector-field classification applies to its labelled open Conf domain, but the **global** separable-energy corollary cannot simply be transferred without an extension or connected-fibre argument. Example: on Conf_2(R), E=sign(x_2-x_1) is C-infinity locally constant, has zero gradient and commutes with all audits, but cannot globally equal w_1V_1(x_1)+w_2V_2(x_2)+C. V_1(0) would have to equal both component energy values. The product-domain statement in the received packet is correct; this is a transfer guard, not a counterexample to it.

Likewise arbitrary label-specific V_i and arbitrary r_i require retained labels. A fixed energy must additionally be permutation-invariant to descend to an unlabelled law space; fixed distinct V_i do not generally do so. Origin labels and positions can coincide without becoming the same retained origin. Merging labels that need unequal future audit factors loses that audit contract even when it preserves the current law.

## 3. Exact comparison with posterior-gradient classification

Inspected sources: `posterior-gradient-descent-20261010/RESULT.md`, especially §§4–8, and `finite-audit-gradient-classification-20261010/RESULT.md`, especially §§3–7.

The inherited finite-audit result asks whether the full-source Fisher flow descends through F(w,P)=(P,Qw), identifying different positive w only within Qw=q. Its exact pointwise test is C(p_j)J_j=0 for the indices variable in ker Q. For k>r, its global classification is E=phi(q), allowing nonlinear phi. The binary packet has its own independence-fibre condition and topology/regularity distinctions. Neither is a classification of commutation with every B_r while keeping x fixed and the objective fixed.

This difference is substantive. In the two-coordinate simplex, E(w)=w_0^2 gives F_0=-2w_0^2(1-w_0). At w=(1/2,1/2), r=(1,2), the pushed vector has first coordinate -2/9, while the field at the audited point has first coordinate -4/27. A nonlinear target-only objective can qualify under inherited quotient descent without full positive-audit equivariance. Conversely J allows arbitrary C1 weight-independent position fields and centred fitness fields, without requiring a Fisher gradient. The shared proof mechanisms and tilts are inherited/classical; the universal audit contract and its joint-metric rigidity are distinct in this bounded comparison.

## 4. Discrete invariant and repair: accept, then deduplicate

For w=(1/2,1/2), c=(0,1), h=1/2, r=(1,2), the received Euler computation is exact:

    B_r U_h(w)=(3/13,10/13),
    U_h B_r(w)=(2/9,7/9),
    TV=1/117.

The separate Euler steps decrease E=w_0 and preserve positive normalised weights. Thus source-audit fidelity is genuinely additional to these properties. The inherited raw full-hierarchy Euler obstruction is different: it can lose square positivity at a moving Dirac for every h>0. The present control stays entirely on a valid positive simplex and isolates failed commutation.

K uses A_i=1/[1+h(V_i-min V)], then normalises w_i A_i. For fixed V,h, commutation is exactly B_A B_r=B_r B_A. Positivity, the pairwise covariance sign, common-shift invariance, and first-order expansion are all valid. n=1 and h=0 are harmless identity cases.

**Ownership correction:** this very factor formula and its joint split construction are inherited from `gradient-discretization-fidelity-20261010/RESULT.md` §4 equation (R), with identical covariance descent, shift invariance, actual-segment descent conditions, and first-order calculation in §5. `check_exact.py` already implements it. K adds an audit-fidelity theorem to an existing repair; it does not newly repair a defective existing scheme.

For the corollary's general alpha metric, K as printed has alpha=1 reaction speed. To approximate that general metric in physical step h, replace h by alpha h in the weight factor, while keeping the chosen position step's appropriate speed. This is a units/transfer qualification, not a false printed derivative: K explicitly claims -w_i(V_i-mean V), which is correct.

The positive joint construction only claims positivity, energy nonincrease and covariance. Arbitrary individually decreasing P_i need not approximate xdot_i=-grad V_i; first-order joint consistency additionally requires P_i(x_i)=x_i-h grad V_i(x_i)+O(h^2). No convergence, stiffness or accuracy theorem follows from its structural properties.

A weight-dependent step selection can break commutation even though every chosen step remains positive and descending. Exact control with h(w)=w_0, V=(1,0), w=(1/2,1/2), r=(1,2) gives (1/4,3/4) versus (3/11,8/11). Audit-invariant selection is sufficient; it is not logically necessary in degenerate cases where changed steps induce the same normalised map.

### Actual existing implementation control

Invoked `gradient-discretization-fidelity-20261010/check_exact.py::quartic_rational_step` on w=(1/3,2/3), x=(-1,2), h=1/24, r=(2,1/3). Both orders have positions (-23/24,5/3) and weights (3792295/4971943,1179648/4971943). Its guard h<=1/(6 max|x_i|^2) is unchanged by positive reweighting. The proof applies to every distinct labelled input satisfying that guard and using an audit-invariant h. The implementation merges duplicates; arbitrary hidden-origin audits after such merging require sidecar labels, as I already states.

## 5. Fixed-marginal and correlated-target transfer

Inspected `fixed-marginal-correction-20261011/RESULT.md` §§1–4,6–8 and `correlated-target-marginal-correction-20261011/RESULT.md` §§1–8.

Their full-law constrained gradient is

    mudot=-K_mu(q-phi∘T),    K_nu phi=T_*K_mu q.

For correlated targets, q=log(r/r*), m(y)=-E_mu[grad_y log r*(Z|y)|y], and the multiplier includes -div(nu m)+nu(h-nu h). For the Gaussian family its fixed-marginal mobility M_c(b,s) is independent of target parameters beta,tau, while the target-dependent energy is [s+(b-beta)^2]/(2tau)-1/2+(1/2)log(tau/s). The score and correction remain state-dependent.

These results are not special cases of the finite labelled Cartesian metric corollary: the state, constraint, tangent metric and admissible operations differ. An arbitrary B_R need not preserve the fixed marginal or the Gaussian family. Even an operation that stays inside requires its actual constrained equivariance test. A changed target changes the objective and is outside J's fixed-objective contract. Geometry independent of target parameters is not evidence that flow trajectories are unchanged under target revision. No replay shortcut or failure follows without specifying the audit's action on this full state/context.

The correlated-target positive result also prevents an overbroad gloss that correction must remove dependencies: the same constrained metric can create correlation toward a supplied correlated target. None of positivity, covariance, metric projection, convergence, or source-revision commutation authenticates that target or its dependency structure.

## 6. Execution evidence and stopping boundary

Fresh targeted replay: all 8 tests in `test_audit_covariant_discretisation.py` and all 4 in `test_separable_repair.py` passed with bytecode writing disabled. Inspected `research/contracts.py` functions `replicator`, `audit_tangent`, `rational_weight_step`; formulas match the claims. These finite tests do not prove the converse classification. Independent exact controls and results are in this review folder:

- `independent_controls.py`
- `INDEPENDENT_CONTROLS.json`

They cover actual inherited scheme commutation, n=1, nonlinear fixed-objective noncommutation, adaptive-step failure, and alpha rescaling. No corpus-wide survey, inherited modification, target-warrant inference, production integration, or T20 closure was performed or is justified.
