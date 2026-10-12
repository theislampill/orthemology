# Fixed-model inquiry control: independent exact calculation

11 October 2026 UTC. Bounded application of classical nonrectangular uncertainty. No new general decision theory, calibrated human warrant, policy implementation or kernel certification.

## Same source family, altered optimisation contract

Use the inherited L source/audit segment, in order (theta1,A1; theta0,A1; theta1,A0; theta0,A0): vertices (1,9,9,21)/40 and (9,1,21,9)/40. Audit mass is1/4 in both. After A1 the declared menu is report1 or defer; after A0 it is report0 or defer. Wrong report loses1, right report0, defer3/5. This explicitly restricted menu is part of the counterexample, not a claim about every inquiry task.

Let x be probability of reporting after A1 and y after A0. Random choices are model-independent and the adversary selects one model before their outcomes. The two endpoint expected losses are

  l1=3/5+3x/40−9y/40,
  l2=3/5−x/8+3y/40.

Because a fixed policy's loss is linear in this initial JOINT law, the whole L segment has worst loss max(l1,l2). Among four deterministic policies the minimum is11/20, attained by reporting at both branches. Randomised policies attain21/40 at x=1,y=2/3. This is globally optimal over the square: max(l1,l2) >= (l1+3l2)/4 =3/5−3x/40 >=21/40.

Branchwise independent worst-case selection instead uses first endpoint's error9/10 afterA1 and second endpoint's error7/10 afterA0. Reporting at both then receives loss3/4, although no original model gives that expected loss. Local robust choice defers at both, value3/5. With audit cost1/40 and a pre-audit menu restricted to querying or skipping/defer at cost3/5, fixed-model inquiry is preferred (23/40 deterministic,11/20 randomised); independent branch reselection skips (query value5/8).

The pre-audit restriction is substantive. If both report labels with private randomisation are admitted before any audit, fair random guessing has worst error1/2. It defeats the displayed paid-query value11/20, so this particular inquiry-preference reversal does not carry over to that enlarged menu. This review control must accompany the positive restricted-menu result; no philosophical need for the restriction has been established.

This is a difference of admissible uncertainty and decision contract. A theorem intentionally granting an adversary fresh branch choices remains correct. Nor does the fixed-model repair make conditional maxmin preferences dynamically consistent without further assumptions or a commitment mechanism.

## Stronger decision reversal without the restrictive reporting menu

The preceding reviewer control motivates a distinct positive construction. Let the initial joint-law family instead be M=conv{(4,2,1,3)/10,(3,1,2,4)/10}, in the same theta/audit order. Both target reports, with private randomisation, are available before and after inquiry. Every model has target prior1/2. Every model has the same optimal conditional classifier, reportTheta=A, and its expected error is3/10.

To verify optimality including randomised rules, let x,y be probabilities of reporting1 afterA1,A0, respectively, and write v=(a,b,c,d). Then

  risk_v(x,y)−3/10 = (1−x)(a−b)+y(d−c) >=0.

Both coefficients are positive throughout M. Thus the common classifier is individually Bayes-optimal in every model and simultaneously fixed-model minimax, with value3/10. Without querying, every randomised report has error1/2 because the prior is balanced.

Independent conditional worst-case selection takes A1 error1/3 from the first endpoint and A0 error1/3 from the second. Its optimal conditional classification risk is1/3 at both branches. With query cost9/50, fixed-model querying costs12/25 <1/2; branchwise rectangular querying costs77/150 >1/2, so the inquiry decisions reverse under an unrestricted binary-report menu.

The full rectangular hull can enlarge the target-prior range to[5/12,7/12]. Its unrestricted private-randomised skip value is nevertheless1/2 (fair random guessing attains it, and the balanced law supplies the lower bound). A deterministic-only skip would instead cost7/12 in that full hull, so the displayed reversal explicitly uses the stated private-randomisation menu.

At audit mass1/2, those worst conditionals combine into (1/3,1/6,1/6,1/3). This spliced law preserves the balanced target prior and uses an audit mass within the original family range, yet it lies outside M: its classification error is1/3, whereas every M member has3/10. The query-risk gap therefore also survives intersecting the relaxation with the balanced-prior constraint (that intersection need not be rectangular). The missing information is the joint admissibility of branch responses, not merely the availability of target reports or knowledge of the prior.

This retains the earlier restricted-menu result and its negative control rather than retroactively changing its premises. It is a second mathematical witness to the same failed transport. The declared loss and query cost do not themselves establish a psychological, normative or theological value scale. unrestricted_query_control.py checks the exact affine identity and values; its sampled controls do not replace the written universal nonnegativity proof.

## A further scope control: vertices of transition kernels are not vertices of joint path laws

The linearity argument above concerns a convex set of initial joint laws under a common supplied instrument. It cannot silently be transferred to a convex set of transition/emission kernels reused with one unknown fixed parameter.

Take a fixed Bernoulli parameter p in[0,1], and two trials independent CONDITIONAL ON that p. Single-trial laws form a line segment with endpoints p0,p1. The probability that the trials differ is2p(1−p), maximised at p=1/2 with value1/2; both endpoint models give0. Evaluating only the endpoint kernels therefore misses the worst-case event probability. Mixing the two whole endpoint path laws likewise gives0 for this event and is a different model class.

The full two-trial path-law curve needs the ordinary tensor/moment lift (p,p²). For a fixed p0, the linear path-law observable

  2p0 E[X1]−E[X1 X2] =2p0 p−p²

is uniquely maximised at p=p0. Every point of the path-law curve is consequently exposed in its convex hull; that hull cannot have finitely many extreme points. This does not prevent finite-dimensional representation, finite decompositions of individual points, or finite exact solutions for particular losses. It blocks a fixed finite-vertex representation of this entire continuum of path laws.

These are elementary classical Bernoulli/tensor facts. Their role here is to state the required semantic condition on a proposed finite-model policy-value repair, not to claim new moment theory. Conditional independence of repeated trials does not make the unknown fixed calibration independently reselectable at each trial. A new calibration draw per trial is a different source model.

## Verification and ancestry

check.py executes944 explicit rational checks in both normal and optimised modes. The analytic all-policy bound is the written affine identity above, not the finite grid. Additional kernel controls are separately recorded. No Lean replay is claimed.

Primary publisher search-result abstracts for Epstein and Schneider, Recursive multiple-priors (2003), https://doi.org/10.1016/S0022-0531(03)00097-8 , and Iyengar, Robust Dynamic Programming (2005), https://doi.org/10.1287/moor.1040.0129 , establish the established rectangularity/dynamic-programming ancestry. Root did not read either full proof. The Berkeley2001 version had garbled extracted text, failed screenshot fetching and a403 local fetch; direct ScienceDirect opening also failed403. Those operations confer no full-reading credit. The author worker may independently obtain and record stronger source access.

Existing H-Continuation preserves each policy law; the new coupled-credal report expressly does not claim robust Bellman optimisation. No defect in those inherited statements is inferred. Exact inherited and final author-report hashes should be bound on completion of the independent review.

## Review-driven zero-history control

The independent reviewer identified a real edge case in the proposed recursion: if a child history is impossible under EVERY candidate model, requiring a legal terminal choice there can remove an otherwise feasible policy. Such a child contributes the singleton zero vector, or is omitted from the branch product. If at least one candidate model gives it positive mass, an empty legal continuation set remains a real infeasibility. Componentwise zero mass in only some models does not authorise ignoring the branch for the others.

The six exact zero_branch_control.py checks show that blindly taking a Cartesian product with an empty unreachable child destroys the action, whereas the zero-vector convention preserves it; they also retain the live-child negative control. This is a correction to the new recursion's boundary specification, not an alleged defect in the inherited controller. The author is separately binding the corrected theorem and executable fixture.
