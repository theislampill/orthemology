# Independent review of cumulative joint-audit coupling

11 October 2026 UTC. Scratch-only ordinary mathematical review and independent exact controls. No protected changes, source-authentication credit, kernel-proof credit, integration or programme closure.

## Final verdict: PASS with declared scope

The two strictly positive joint-law segments are correct, including their full likelihood-ratio ranges. They share current target interval [1/4,3/4], constant audit probability 1/4 and audit likelihood-ratio interval [1/3,3], while the first audit posterior image is {1/2} and the second [1/10,9/10]. This is a valid failure of sufficiency for those separately retained summaries. It is not a failure of full joint Bayesian or credal conditioning.

Coordinates are (target-and-audit, not-target-and-audit, target-and-no-audit, not-target-and-no-audit). Segment K joins (1,1,1,5)/8 and (1,1,5,1)/8; segment L joins (1,9,9,21)/40 and (9,1,21,9)/40. Both are compact convex sets with strictly positive cells. Writing p for target probability, p ranges through [1/4,3/4]. In K the intersection x is 1/8, the posterior is 1/2, and r=(1-p)/p decreases from 3 to 1/3. In L, x=2p/5-3/40, the posterior is 8p/5-3/10 and

r=(p-1)(16p-3)/(p(16p-13)).

Its derivative is [96(p-1/2)^2+15]/[p^2(16p-13)^2], strictly positive on this entire interval. Its endpoint values are 1/3 and 3. Continuity and strict monotonicity establish the full range, beyond endpoint checking. The independent script checks the polynomial identity exactly and adds 2002 rational segment regressions.

## Finite-polytope positive repair

For a nonnegative linear map M and finitely many probability vertices v_i, let z_i be the total mass of Mv_i. If every z_i=0, every input is impossible on that branch and the conditional image is empty. Otherwise the exact conditional image of conv{v_i}, restricted to positive branch mass, equals conv{Mv_i/z_i : z_i>0}. For an input mixture with weights a_i, its posterior weights are a_i z_i divided by their sum. Conversely, for any desired posterior mixture b_i supported on positive vertices, choose prior weights proportional to b_i/z_i. This proves both containments; zero-event vertices contribute no conditional point and cannot introduce arbitrary laws.

The same proof applies to any finite composition of common nonnegative linear branch maps, provided the relevant realized branch is possible. Normalizing between maps cancels from the final normalization. Model-dependent maps cannot be substituted while retaining a common-state sufficiency claim without retaining their coupling to the model.

## Compact coupled-summary bounds

For nonempty compact C contained in (0,1)×(0,infinity), f(p,r)=pr/(1-p+pr) is strictly increasing in each argument. Let p_min,p_max,r_min,r_max be coordinate extrema. Then min_C f is at least f(p_min,r_min), with equality exactly when (p_min,r_min) belongs to C. Similarly max_C f is at most f(p_max,r_max), with equality exactly when (p_max,r_max) belongs to C. Compactness supplies attainment, and strict monotonicity supplies necessity. Convexity of C is unnecessary. A nonclosed or boundary-inclusive class requires a separately qualified statement, so the stated interior compact hypotheses should remain explicit.

K reaches neither rectangular extremal corner; L reaches both. The rectangular interval [1/10,9/10] is therefore a valid outer envelope for K but an incorrect exact posterior image for K. Exactness depends on coupling, not merely the two ranges.

## Null-boundary compactness control

For v(t)=(t²,t(1-t),0,1-t), t in [0,1], the convex hull is compact in the finite-dimensional probability simplex. In any finite convex mixture with positive audit mass, the posterior is sum_i a_i t_i² / sum_i a_i t_i. This is strictly positive, at most one, and every q in (0,1] is attained by t=q. The t=0 point is audit-null and supplies no posterior. Thus the exact image is (0,1], not its closure [0,1]. Compactness of the original credal set alone does not imply a closed conditional image when branch mass can approach zero. This does not contradict the finite-polytope theorem.

## Ancestry and philosophical scope

Cozman's primary 1997 account explicitly treats vertex updating and interval nonuniqueness as established facts, with Giron and Rios and Walley references. These cannot be claimed as new discoveries here. Independently retrieved source: https://www.cs.cmu.edu/afs/cs/user/fgcozman/www/Research/QuasiBayesian/FiniteConvex/node4.html . The bounded addition is the present same-summary audit-coupling control and its application, with ordinary proof and independent controls; no field-wide novelty search has been performed.

Inspected earlier owners:

- source-audit-revision-semantics-20261010/REPORT.md already distinguishes provenance correction, audit evidence, shared calibration, memory, invalidity and warrant. It requires a real justified audit model and separates accepted-store deletion from full-history revision and human warrant.
- historical-source-revision-20261010/RESULT.md already requires current/history coupling, exhibits separately sufficient one-root summaries that fail under composed revisions, and distinguishes support restoration from positive likelihood division.
- pairwise-corroboration-bound-20261011/RESULT.md already transports missing truth-sensitive interaction into exact partial-identification intervals and rejects inference from unlabelled agreement to sufficient calibration. Parity, missing interaction and generic marginal insufficiency are not newly earned by this packet.
- hase-finite-sidecar-realisation-20261011/RESULT.md and NOVELTY_AND_SCOPE.json already realize finite deterministic correction tables and source-observable labels. They explicitly do not sample general credal sets, provide arbitrary real probabilities, authenticate provenance or implement human warrant. The proposed convex-law record is not thereby an implemented HasE/HasJ sidecar.

Nothing in these numerical laws diagnoses an actual person's epistemic warrant, retracts the retained affirmative source appraisals, assigns a probability to any scripture or establishes a theological defeater. A justified finite vertex law is a positive sufficient mathematical record for its declared operations; the theorem does not determine how to acquire that law or license a historical/source application.

## Final adopted-text review

Read the complete author REPORT.md and replayed its exact verify.py from a separate review-owned directory, leaving author files unchanged. Author replay PASS: 65 normalized laws, 23,130 positive mixtures, 465 null cases, 42 compositions and 202 segment cases; all eight inherited input bindings match. The independently written check.py also passes 2002 segment regressions and 10,100 cases of the adopted full-support boundary.

The final report adopts a stronger null-boundary control than the preliminary curve above: 0≤v≤1/2 and v²≤u≤v/2, with row (u,v−u,(1−v)/2,(1−v)/2). Its parameter set is compact convex; its affine image is compact convex. Every positive-event row is full-support. q=u/v is strictly positive and at most 1/2, while v=q,u=q² realizes every q∈(0,1/2]. The exact conditional image (0,1/2] is correct. This independently verified adopted statement supersedes the preliminary (0,1] fixture as the packet's primary boundary control; neither boundary example is claimed as an independent source discovery.

The final report includes the needed guards: nonempty compact interior coupled C; all-null branch handling; common operator and retained cumulative mass/state pairing; signed quotient coordinates governed by their image cone; no model reselection or robust Bellman claim; no field-wide novelty; no human-warrant or theological revision. Its bounds-versus-attained-set distinction is correct. No required mathematical or scope correction was found in the adopted report.

Final verdict: PASS as bounded ordinary mathematics and exact computational corroboration. This verdict does not assert kernel certification, primary historical authentication, source-calibration acquisition, causal identification, sidecar implementation, repository integration or programme closure. REVIEW_BINDINGS.json identifies the exact adopted files reviewed.
