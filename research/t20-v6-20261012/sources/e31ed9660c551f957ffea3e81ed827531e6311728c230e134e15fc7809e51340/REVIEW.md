# Independent review: coupled credal inquiry and fixed-model continuation

11 October 2026 UTC. Additive review of the final bytes listed in REVIEW_BINDINGS.json. The reviewer read the mathematical report, inspected the executable controls and named inherited theorem passages, independently derived the principal values, and ran separate exact arithmetic controls. This is ordinary mathematical review and executable evidence, not proof-assistant certification, a calibrated human-warrant judgement, repository integration, or T20 closure.

## Verdict and scope

**The bounded mathematical claims pass, with the explicit policy, uncertainty, information and commitment assumptions retained.** The author incorporated the review clarifications concerning finite terminal menus, private-coin timing, the original pre-audit menu restriction, the fair-skip interpretation under rectangularization, and globally impossible outcome children. Those clarifications are part of the reviewed final result, not qualifications silently added to a different frozen version.

- The original inherited L family has deterministic post-audit minimax loss 11/20 and private-randomized loss 21/40 under its stated branch report/defer menus. Rectangular post-audit minimax is 3/5. Audit cost 1/40 reverses query versus skip when skip means defer at 3/5.
- The separate parent-supplied M family admits both reports everywhere. Its fixed-model audit error is 3/10, rectangular error 1/3. With private randomization available and query cost 9/50, fixed-model planning queries for 12/25 while rectangular planning fairly guesses for 1/2.
- Model-indexed unnormalized policy-value sets give a sufficient finite ex ante repair, followed by root scalarization. This is inherited pointwise law preservation plus classical finite policy enumeration; it is neither a minimum-memory theorem nor a repair of the already correct known-kernel/pathwise controllers.
- The parent’s fixed-Bernoulli repeated-kernel control is correct: endpoint kernels do not suffice to evaluate all repeated-kernel path losses. The entire two-trial path-law convex hull has infinitely many exposed points even though it has a finite-dimensional moment representation.

Exact author/report hashes and replay counts are supplied in the final-binding section below and the machine-readable receipts. No inherited input was edited by this reviewer.

## 1. Exact L calculation, policy class and commitment

The four joint cells are ordered (Theta=1,A=1; Theta=0,A=1; Theta=1,A=0; Theta=0,A=0). The source-owned endpoints are (1,9,9,21)/40 and (9,1,21,9)/40. The independent checker represents each endpoint by forty equally probable explicit outcomes and sums realized losses; it does not import the author’s loss evaluator or optimizer.

The deterministic loss vectors are DD=(3/5,3/5), RD=(27/40,19/40), DR=(3/8,27/40), and RR=(9/20,11/20). The best deterministic maximum is 11/20. For report probabilities x after A=1 and y after A=0, the two affine loss functions satisfy

    (l0+3 l1)/4 = 3/5 - 3x/40 >= 21/40.

The checker verifies the identity by its constant and two linear coefficients, including the absence of a mixed action term. Therefore this bound holds on the whole square, rather than only on sampled rational policies. At (x,y)=(1,2/3), both endpoint losses equal 21/40. An independent convex-hull calculation over deterministic policy vectors attains the same value.

The two branchwise adverse error rates 9/10 and 7/10 come from different endpoints. Pasting them at audit masses 1/4 and 3/4 gives the coherent law (1,9,21,9)/40, outside L, and RR loss 3/4. Conditional minimax instead defers on both branches for 3/5. This is a change in the admissible complete-law family, not a contradiction in probability theory.

Three load-bearing qualifications were checked:

1. **Restricted skip menu.** If arbitrary reports are admitted before the audit, a fair private guess costs 1/2. At the midpoint of L the target is fair and independent of the audit, so unrestricted post-audit classification cannot improve that lower bound. A positive audit cost then defeats inquiry in this particular L example. This does not undermine the separate M witness.
2. **Private coins.** The 21/40 policy is the mixture 2/3 RR plus 1/3 RD, chosen independently of the model and not revealed before model selection. If Nature first sees the sampled complete plan, this mixture costs (2/3)(11/20)+(1/3)(27/40)=71/120. Under that revealed-plan protocol, mixing cannot improve the best deterministic 11/20.
3. **Execution commitment.** The ex ante optimal policy is not conditionally minimax at either branch. Its A=1 action has worst conditional loss 9/10; its A=0 lottery has worst conditional loss 2/3; defer costs 3/5. The set-valued repair evaluates committed history policies and does not erase this preference conflict.

Scalar pruning also fails within the same fixture. Keeping only the deterministic policy of smallest scalar worst loss retains RR and discards RD, although their stated mixture improves 11/20 to 21/40. Coordinatewise domination is safe because replacing a dominated vector in any nonnegative same-coordinate composition, including a convex mixture, cannot worsen a component. This does not mean every incomparable vector is indispensable for every smaller objective.

## 2. Unrestricted M witness and full rectangular hull

For M=conv{(4,2,1,3)/10,(3,1,2,4)/10}, write v=(a,b,c,d). Every member has target prior 1/2, b+c=3/10, and a-b=d-c=1/5. If x and y are probabilities of reporting target 1 after A=1 and A=0, respectively, then

    risk_v(x,y) - 3/10 = (1-x)(a-b) + y(d-c) >= 0.

Thus report Theta=A is individually optimal under every model, including against randomized reports. Its common risk is 3/10. This proof is stronger than merely checking the four deterministic rules.

The conditional target probabilities range over q1 in [2/3,3/4] and q0 in [1/4,1/3], while the audit-one mass ranges over [2/5,3/5]. The full rectangular hull allows independent selections of these quantities. The classifier’s error is at most 1/3 in each branch. The balanced pasted law w*=(1/3,1/6,1/6,1/3) attains that error and has the same optimal classifier, establishing exact rectangular audit risk 1/3.

The full rectangular hull need not preserve M’s initial target prior: its range is [5/12,7/12]. Consequently **deterministic** skipping over that hull costs 7/12, not 1/2. The stated menu includes private randomization, and a fair guess costs exactly 1/2 under every law. The balanced w* lower-bounds every skip rule at 1/2 and every paid query rule at 1/3+9/50=77/150. It also rules out improvement from mixing skip and query. Therefore the full randomized rectangular optimum really is 1/2, while the fixed-model optimum is 3/10+9/50=12/25.

Because w* itself preserves the balanced prior and an admissible audit mass, the query-risk gap also persists if the enlarged family is intersected with the balanced-prior constraint. That intersection should not automatically be called rectangular. The report’s unrestricted private-randomized reversal needs no such extra claim.

## 3. Policy-vector repair, null branches and transport

For initial laws in a finite polytope and a common supplied instrument, each fixed lawful finite policy has expected loss linear in the initial joint law. Endpoint evaluation therefore suffices for that policy’s robust loss. Keeping one coordinate per supplied endpoint is a convenient sufficient representation of all compatible branch responses. An alternative exact coupled-profile encoding can do the same job; no literal model ID, transcript, whole law-set representation or full profile is proved necessary merely to preserve one root optimal value.

The set-valued recursion is sound by finite-horizon induction: select one public-history action for all model coordinates, select one common continuation per observed outcome, and sum each model’s own unnormalized costs across outcomes. Never maximize each coordinate or branch independently while constructing a policy. Finite action/outcome alphabets, finite terminal menus, finite horizon and the same lawful information-policy class provide the finiteness and policy correspondence.

Globally impossible outcome children must be omitted or assigned only a zero bookkeeping contribution. They are not reached and do not need lawful terminal decisions. Conversely, a history live under any admissible model cannot be discarded merely because another model gives it zero mass; missing legal completion there remains infeasibility. A separate reviewer control demonstrates that blindly taking a Cartesian product with an empty decision set at an impossible child would falsely remove a valid parent action. The final author convention addresses this distinction.

Convexifying the root deterministic vector set is exact for private random selection of a lawful complete policy under the declared adversary timing. It does not give the policy access to the hidden model coordinate. Likewise, applying the inherited predictive quotient is safe only when all relevant loss rows, outcome masses, information and legal menus are preserved. A finer physical state does not become observable merely because it appears in the model.

The nonlinear escort transport is only an invertible recoding when original probabilities and losses are read through its inverse. It preserves every model’s path values and hence the robust optimization; it does not justify a new probabilistic reading of transformed coordinates or arbitrary convexification of their nonlinear image.

## 4. Repeated uncertain kernels: verified additional boundary

Let one unknown p in [0,1] be fixed across two conditionally independent Bernoulli trials. The path-law vector is ((1-p)^2,(1-p)p,p(1-p),p^2). Its mismatch probability is 2p(1-p), equal to zero at both endpoint kernels and maximized at 1/2 with value 1/2. A mixture of the two complete endpoint path laws still assigns mismatch zero and is not the same family.

For any p0 in [0,1], the linear functional of the path law

    2p0 E[X1] - E[X1 X2] = p0^2 - (p-p0)^2

has the unique maximizer p=p0. The same holds over the convex hull: a convex combination attains the maximum only if every constituent has p=p0. Every curve point is consequently exposed, so no fixed finite vertex list represents this whole convex hull. Compactness and finite dimension do not imply a polytope.

This does not forbid finite-dimensional (p,p^2) moment coordinates, finite atomic decompositions of individual hull points, or a finite exact solution of a particular loss. It prevents silently transferring the author’s initial-joint-law vertex theorem to a reused unknown-kernel polytope. The mechanism is elementary classical probability and convex geometry, not new tensor theory.

## 5. Inherited ownership and primary-source scope

The reviewer inspected the actual warranted-inquiry Theorem 2: its worst realized path-cost objective explicitly excludes private-randomized worst expected cost. H-Continuation Theorem 2(c) already preserves bounded adaptive policy values and their random mixtures under a supplied instrument. The supplied synthesis D3a–D3b and finite_values code concern preserved joint kernels and known-kernel Bellman values with the stated observation assumptions. None is refuted by this application.

The coupled-credal report already owns L, coupled conditioning, vertex transport and the warning against branchwise model reselection. The audit-continuation and stochastic inquiry addendum already distinguish conditional answers, path probabilities, lawful policy correspondence and stronger stopping objectives. The posterior-inquiry-value report owns the earlier missing-frequency obstruction. The present same-frequency L collision concerns compatibility of adverse models across siblings; the new M witness is separately credited to the parent.

For classical ancestry the reviewer independently accessed the author-hosted [Epstein–Schneider September 2002 manuscript](https://people.bu.edu/lepstein/files-research/rectang50.pdf), reading Definition 3.1 and adjacent explanation on printed pp. 9–10, Theorem 3.2 statement and recursive formula on pp. 12–13, and §4.4 on pp. 19–20. These passages establish the rectangularity, conditional-pasting and preference-enlargement background. No full-proof-appendix or whole-paper reading is claimed. The author’s own source record reports additional selected §4.1 reading and only publisher-abstract access for Iyengar. This reviewer claims no independent Iyengar full-text reading.

## 6. Final binding and replay evidence

Reviewed author RESULT.md SHA-256: 7f0d42d87119221c01358874ddbd007e39c57f9cbd9f8f918d11cfffd15c6946.

Reviewed author verify.py SHA-256: 9be6d46c884c4022c7e44cb5766648ba813d30082311c624392518bb818199f1.

Reviewed root DERIVATION.md SHA-256: 76dc4b67a043e3c8b65a14a2c4ed2c3ed77e8d412b03387ea3b95d3a12383462. All other exact input identities, including inherited source hashes, are in REVIEW_BINDINGS.json.

Fresh read-only replay passed twelve positive runs and required eight deliberately false runs to reject. Normal and optimized outputs match byte-for-byte for each positive script:

- author: 13,676 active checks per mode;
- independent reviewer: 2,537 active checks per mode (2,509 mathematical/control checks plus 28 bound-input checks);
- root L calculation: 944 per mode;
- root unrestricted M calculation: 3,453 per mode;
- root repeated-kernel calculation: 884 per mode;
- root zero-history control: 6 per mode.

All 28 bound inputs were unchanged before and after replay. The author's 669-tree fixture permits terminal decisions only at its fixed horizon; its revised separate small control also checks optional early stopping. Author evidence is replayed author evidence, distinct from the reviewer's independently constructed controls. The author preserved its ten pre-clarification files in reviewed-v1; both that baseline manifest and its final current manifest verified exactly. The verdict binds the corrected current files, not the superseded version.


REPLAY_RECEIPT.json records read-only replays in normal and optimized Python, plus required active rejection of deliberately false checks. The separate reviewer script uses Fraction arithmetic and explicit exceptions, not Python assert. Finite grids corroborate the written identities and proofs; they are not substituted for universal arguments. There is no Lean run, benchmark campaign, model calibration, empirical warrant result, protected source modification or release decision in this review.
