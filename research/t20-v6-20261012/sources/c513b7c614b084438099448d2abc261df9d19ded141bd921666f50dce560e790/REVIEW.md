# Independent review: audit-aware revision, support and continuation

10 October 2026 UTC. Independent adversarial mathematical and source-interface review. This is a scratch-only review; it confers no protected integration, owner adoption, actual-source assessment, proof-assistant certification or T20 closure.

## Disposition and bound object

**No blocking mathematical or source-interface finding in the final snapshot listed in INPUT_SNAPSHOT.json.** The general arguments were checked directly; exact controls supplement rather than establish their universal quantifiers. The review covers the main audit-revision report and executable controls, the root's zero-audit and triple-interaction notes, and the separate source-to-operation report. No author, predecessor or primary-witness file was modified by this reviewer.

The author corrected concrete reporting, custody and edge-case imprecisions identified during review. An integration notation issue was also corrected. Their disposition is recorded below. The remaining limits are application obligations, not hidden proof claims.

## 1. Exact deletion and its positive replacement

Write p=P(Theta | B=b), J(theta)=P(Y=y,A=a | theta,b), and M(theta)=P(A=a | theta,b). The observed joint history must have positive probability. Its full posterior is N(pJ), whereas audit-aware deletion is N(pM).

The iff criterion is correct. At each coordinate with p(theta)M(theta)>0, equality of the normalized vectors implies J(theta)/M(theta) equals the one positive common normalizing ratio. Conversely this constant ratio makes their normalizations identical. If M=0 then J=0, so no division or further restriction is needed there. This establishes the report's criterion on the support of P(Theta | b,a), not on target states already excluded by the retained history or audit.

Eventwise equality for one y must not be inflated into global conditional independence. Requiring equality for every supported report and background/audit history does give Theta independent of Y conditional on (B,A); report outcomes with zero mass automatically have zero likelihood across that conditional support. The report preserves this distinction. With a full-support prior, the proportionality is a property of the fixed channel and so transfers to any other full-support prior on that same channel. This is not invariance under a changed target or changed observation model.

Bare deletion is a separate condition: J must be constant on the support of p. In particular, audit-aware deletion may be lawful while the audit continues to discriminate. Conversely, a cancellation in the combined J can make bare deletion exact even though the individual factors are informative. One should not demand separate marginal neutrality as a universally necessary condition.

The sequential update N(q_old P(a | Theta,b,y)) and the audit-first update N(P(Theta | b,a) P(y | Theta,b,a)) are both just the two chain-rule factorizations of the same joint law. Neither requires independence. The division-based replacement is valid only on the support on which the old factor is positive and the baseline remains valid. A zero factor can erase prior distinctions: two different priors on two states both map to (1,0) under factor (1,0). No inverse from that posterior alone can recover which prior was used. The report states this limitation and does not resurrect excluded states by conditioning within an unchanged law.

Keeping the old report-conditioned audit factor after first deleting the old report factor is generally wrong. The report's exact exceptional criterion for that procedure is also correct: the old report likelihood must be constant on the support of the resulting N(pK). This is different from the correct audit-aware deletion criterion.

These are model-relative sufficiency and equality claims. Declaring latent source quality, provenance, audit selection or a verifier in the state does not establish that the real event has those semantics.

## 2. The strongest countermodel is generative, not a free likelihood assignment

The construction is a complete finite probability model. Target Theta and source quality are independent fair bits. A good source is 9/10 accurate; a bad source is a fair randomizer. The verifier is 4/5 accurate and its draw is conditionally independent of the source draw given target and quality. The discrepancy flag is the deterministic comparison D=[V differs from Y]. All the reported positive events have positive probability.

I independently enumerated 200 equiprobable causal seeds, using deterministic source/verifier mechanisms rather than importing the author's probability-table code. It gives:

- P(Theta=1 | Y=1)=7/10.
- P(Theta=1 | Y=1,Bad,D=1)=1/5.
- P(Theta=1 | Bad,D=1)=1/2.

Thus the audit-retaining deletion really fails even though both the random-source report and the marginal discrepancy audit are individually neutral after source quality is known. Knowing Y=1 and disagreement reconstructs V=0. The useful information is the report's role in the comparison, not its truthfulness as testimony. Conditional independence before observing D does not imply conditional independence after D is observed.

This goes beyond the predecessor review's explicit neutral report plus target-dependent selector example in one bounded way: even the strongest rival that retains the audit's exact marginal still loses target information. It does not claim to discover selection bias or Bayesian conditioning.

The controls in the report also correctly distinguish a neutral status-only audit, an informative status-only audit, a known adversarial report, a certified false report, and a shared-calibration audit. Shared source quality means distinct reports can be independent conditional on (Theta,quality) while remaining dependent conditional on Theta. Recalibrating all affected factors is therefore substantive, not bookkeeping based on different record IDs. The audit-aware theorem already accommodates that dependence by its choice of B and joint law; it needs no additional independence hypothesis.

## 3. Proper-score accounting is sound and bounded

For an admissible differentiable strictly convex Bregman score, the proper-score regret identity gives conditional expected loss difference D_F(Q,R). Averaging over histories gives the claimed nonnegative coarsening loss. Since R=E[Q | B,A], the expected linear gradient term vanishes and the loss also equals E[F(Q)-F(R)]. Strict convexity gives equality only when Q=R almost surely. The entropy case is conditional mutual information.

The report explicitly restricts forecasts to the score's admissible domain and requires boundary extensions when used. This matters: finite joint models with zeros do not by themselves make every interior-defined gradient meaningful at the boundary. The quadratic examples are boundary-safe. The report does not silently apply arbitrary Bregman gradients to undefined zero coordinates.

For the selected Bad/disagreement branch, half-Brier regret is (1/5-1/2)^2=9/100. The hybrid policy's conditional regret 9/200 averages only the Bad branches after Y=1, and is not the same quantity as that one branch or the full unconditional coarsening regret. Its positive net gain does not certify exact implementation. Information-minus-implementation-regret is inherited from the warranted-learning report, as the new report acknowledges.

Independent three-state controls tested both quadratic and quartic Bregman losses using direct expected loss, including restricted supports. They corroborate the identities without treating arithmetic enumeration as proof of their general form.

## 4. The null-audit boundary is correct

The root proof fixes a full-support prior p on at least two states and constructs two-column joints (p-epsilon q, epsilon q). For strictly positive q and 0<epsilon<min p/q, both columns are strictly positive. The theta marginal is exactly p, the audit mass is epsilon, and the conditional audit posterior is exactly q. The total absolute change from (p,0) is 2 epsilon, so total variation is exactly epsilon.

The epsilon restriction is nonempty. Also min p/q is at most one by normalization; no hidden problem with audit mass above one occurs. Equality at the bound can make a cell zero, which is why the strict inequality in the positive-model version matters.

The at-least-two-state premise is needed for nonuniqueness: on a singleton target there is only one posterior. The final main report now makes that premise explicit. Different positive q vectors give different conditioned limits while the complete joints tend to the same impossible-audit baseline. Therefore no unique continuous extension of conditioning at this baseline is selected by that baseline alone. The main report extends the same construction to boundary q with nonnegative joints. That extension is valid and explicitly says nonnegative; it is not a claim that a posterior with a zero component is realized by an everywhere-positive joint. Positive q_n converging to a boundary q could supply such a limiting version if needed, but it is unnecessary for the nonuniqueness result.

The theorem does not make a specified positive model ambiguous, prescribe a replacement model, or show an actual source failed. If p excludes a target state, fixing that prior prevents any conditioning from assigning it positive mass. The root note restricts the assertion to positive support. A hypothetical fallibility construction has no automatic defeater force against an exceptionless source premise.

## 5. The tensor/continuation bridge is a real but scoped transport

In the root's known-randomizer submodel, D=V XOR Y. Therefore (-1)^(Theta+Y+D)=(-1)^(Theta+V), whose expectation is 2a-1=rho. More explicitly, the probability of (theta,y,d) is a/4 if theta+y+d is even and (1-a)/4 otherwise, exactly (1+rho(-1)^(theta+y+d))/8.

Let u=(1,1) and s=(1,-1). In the separate target, report and audit vector spaces the law is the typed ordinary tensor

    (u_Theta tensor u_Y tensor u_D + rho s_Theta tensor s_Y tensor s_D)/8.

Contracting any one slot against the all-ones covector annihilates the signed component because its entries sum to zero. Contracting all three slots against the sign covectors returns rho. These are actual linear tensor operations on a specified joint law, not merely renamed workflow steps. The three roles are not silently identified as repeated copies in a symmetric-power state, and tensor order is not tensor rank.

The pairwise marginals are consequently uniform, yet conditioning on Y and D yields the displayed posterior. The deleted prediction is one half and its quadratic regret is rho squared over four. At rho=0 the distinction vanishes, as it must; for rho nonzero the two report histories have the same current target posterior but different posteriors after the same possible future audit value.

This is a valid failure of continuation-safe compression for the expressly enlarged observation repertoire. The fixed accepted-factor store's old quotient concerned named operations on immutable factors; it did not include a new report-dependent audit channel. There is no contradiction. The inherited graded/H-Continuation sources already contain parity-based lower-order blindness and future-safe observation obligations. The new value is their exact instantiation in the audited source/verifier experiment, not a new parity theorem, general tensor theorem, Fisher-gradient result, or universal memory lower bound.

## 6. Source semantics and prior credit

I read both named predecessor results, the provenance review and its explicit selector control, the pinned Deep AX text, the earlier withdrawal report, the new source report, and the governing CP03 clarification. I also checked the new source claims against the retained Arabic bodies for Darʾ items 960, 967, 970 and 1594, the retained recollection passage, and the selected Miftah material on weakening/loss and time-indexed normative change. This is overlapping local source review, not independent witness acquisition or a new edition/scan collation.

The source report's main operation choice is faithful to the retained case. A later defective explanation cannot have originated knowledge already present before it; correcting that retrospective attribution is first a provenance/basing correction. It does not establish that an actual earlier observation should be forgotten. The governing clarification allows a defective argument to occasion a separately warranted insight without becoming its adequate warranting basis.

The expected-transmission passage requires genuinely absent expected transmission, not merely failed retrieval. The scoped reporting-veracity passages supply a shared authenticity premise, not autonomous positive likelihood factors for each document. A warranted counterexample must have authenticated attribution and the same interpreted in-domain content before the conjunction is inconsistent. No merely posited random-source model supplies such a counterexample.

The new report preserves the distinctions between evidence, permission, memory, actual basing and source authority. It does not infer a person's knowledge from a posterior or infer loss of knowledge from missing implementation semantics. The source's positive appraisal is neither replaced by generic fallibility nor declared disproved. The CP19 misleading-defeater claim is correctly identified as inherited from its modern source analysis, not freshly attributed to the classical passages.

## 7. Findings and dispositions

1. **Repeated normalized channels, corrected.** The initial controls described 6,400 channels. Their 80 nonzero integer rows normalize to 65 distinct distributions, hence 4,225 unique ordered channels. The final report explicitly calls 6,400 table parameterizations and warns about duplicates. The tests remain valid; the original wording inflated distinct coverage rather than invalidating a theorem.
2. **CP03 byte identity, corrected.** The retained local clarification has 3,893 bytes and Git-framed SHA-1 ac3686bcf1477b721602dacd185e98f6cc8216a5. Removing exactly one final LF yields 3,892 bytes and the recorded pinned Git blob 30d93844fa18bdf487779048b1290036f495772b. The source worker independently verified and disclosed this serialization difference without modifying the witness. It is a bounded custody distinction, not a doctrinal discrepancy.
3. **Target/source-quality symbol collision, corrected.** The standalone triple note originally used T for target, whereas the main model uses T for source quality. The final root note uses Theta for target. Its conditional-on-known-randomizer interpretation remains essential when combining the reports.
4. **Zero-interaction exception, corrected.** The main report's added tensor subsection initially said joint observation changes the posterior and differs from the independent law for every verifier accuracy alpha in (0,1). At alpha=1/2, rho=0 and both claims fail. The formulas and later continuation claim were already correct; the final prose now restricts these two discrimination claims to rho nonzero.
5. **Implementation-scope language, corrected.** The opening description of an unimplemented interface is now explicitly relative to the inspected accepted-evidence store. No exhaustive absence claim about all project implementations is earned.
6. **Singleton target scope, corrected.** The main null-audit setup initially omitted the root note's at-least-two-target-states premise. The joint construction remains valid on one state, but its nonuniqueness conclusion does not. The final main report adds the required scope.
7. **Application scope retained.** No actual source/verifier calibration, authenticated human audit episode, empirical cognition, divine-veracity failure, arbitrary-score boundary theorem, general novelty or programme closure is established. These are explicit unproved bridges and excluded claims, not gaps concealed by passing tests.

## 8. Fresh verification and reproducibility

The reviewer-written independent_controls.py does not import author code. Its exact Fraction controls passed:

- 4,644 positive two-column zero-audit models, including a strict-boundary zero-cell check, impossible-event refusal and an excluded-prior-support guard.
- A separate 200-seed causal realization of the principal selection counterexample.
- 420 three-state joint tensors with retained history, three report outcomes and three audit outcomes: 6,307 positive observation events, 1,214 impossible events excluded, 1,125 restricted-prior-support events, and 4,685 well-defined inverse-factor events.
- 5,014 conditional proper-score identities with quadratic and quartic generators.
- A direct zero-factor noninvertibility witness.

These deterministic finite controls are not empirical sampling and do not establish universal quantifiers. The universal conclusions rest on the proofs reviewed above. Fresh author replays, output comparison, final snapshot hashes and local source-binding verification are recorded in the companion receipts. The final output manifest binds this review, its independent script, and the replay evidence.

## Principal reviewed SHA-256 identities

- source-audit-revision-20261010/RESULT.md: 7b8a82a3ee87d1367a709c9250b2ee8b019ed15794c59015e6382175de46c88e
- source-audit-revision-20261010/verify.py: 445f29a63e680192143879563fa073323f9edfa1fe55966b005789c883d8e593
- source-audit-revision-semantics-20261010/REPORT.md: 1bdaaf26b6d13627d8002b3b8f292d840bf8308479c03acca38d1bd6fdb7f6ce
- source-audit-revision-semantics-20261010/SOURCE_BINDINGS.json: d8f6dcc8ad15f54a868c09dfa09012b35f059f37b75f87232d9f71ecb7f7733a
- audit-aware-correction-root-20261010/ZERO_AUDIT_BOUNDARY.md: c202f660a5458a6fbc5f597b9e1645fc9a0d25361055abdcf8b8dd45d5186016
- audit-aware-correction-root-20261010/TRIPLE_INTERACTION.md: 84b17193706810cbf7d85b62b7dd9fffc1f5d9712816ae4558a9a342af9dc4fc
