# Independent addendum: the strongest inferential transmission issue

2026-10-08 UTC. New sibling addendum; the earlier ASSESSMENT.md is preserved. Time floor **UNVERIFIED**. No integration, protected-state change, or closure.

## Judgment

**The proposed test is faithful and useful as a conditional reconstruction, provided two premises are explicit: the entailment is genuinely logical, and the specified nonfactive evidence exhausts the operative basis relevant to the necessary condition.** It exposes the source-sensitive choice of what the reason for an inferred conclusion is. It does not independently settle that choice or refute knowledge transmission.

The strongest objection is an evidence shift at inference: the subject may infer from the fact P as a reason, rather than merely reusing the experience e or a nonfactive belief that P. This is not a new perceptual episode, and one cannot exclude it merely by stipulating that no additional perception occurred.

## Additional reading

Hawthorne's distinct essay, printed pp. 40–56, including all 24 notes and references, is now inspected continuously. Relevant locations: competent deduction with retained premise knowledge, p. 43; equivalence/distribution, pp. 45–46; nonfactive reasons, pp. 48–49; factive-reason alternative, note 16, p. 55. Dretske accepts the distribution cost in his reply, p. 57.

Source: [Contemporary Debates in Epistemology, chapter 2](https://fitelson.org/epistemology/text_ch2.pdf).

## Exact finite semantics

Let Q and A be independent primitive propositions, and define **P := Q and A**. This ensures P entails Q by logical form, rather than merely because a hand-picked domain happens not to display P with not-Q. At the actual world w0, use the fixed increasing-distance order w0, w1, w2:

    world   Q   A   P=Q∧A   e   bP
    w0      1   1     1     1    1
    w1      1   0     0     0    0
    w2      0   0     0     1    1

bP represents a nonfactive belief that P. Define S(r,T) at w0 as: at the nearest not-T world, r is absent. All counterfactuals here share the same ordering at w0; changing the antecedent changes the selected world without changing the ordering.

- S(e,P) holds, because the nearest not-P world is w1 and e is absent there.
- S(e,Q) fails, because the nearest not-Q world is w2 and e is present there.
- S(bP,Q) also fails, because bP is present at w2.
- A complete nonfactive basis e and bP likewise persists at w2 and fails sensitivity to Q.
- S(P,Q) holds, because P is false at the nearest not-Q world. Indeed, P is false at every not-Q world by its logical form.

These four checks were independently recomputed with a simple finite selector. Neither knowledge nor competence was inferred from the valuations. The finite calculation tests the stated counterfactual structure only.

This is a model of the failure of sensitivity to pass from a proposition to a weaker logical consequence. It is not a countermodel to the validity of deductive entailment. No claim is made that this is a new theorem.

## What yields the incompatibility

In addition to the semantic calculation, assume separately at the actual episode:

1. The subject knows P on the relevant operative basis e.
2. The subject competently deduces Q from P and thereby believes Q, while retaining knowledge of P.
3. The operative basis for Q to which the proposed necessity applies is a nonfactive basis rQ that persists at w2. This can be e, bP, or their conjunction in the displayed case.
4. Knowledge of Q requires S(rQ,Q), for that operative basis.
5. There is no additional operative factive or otherwise conclusive basis that would independently satisfy an existential version of the condition.

Then the model and condition 4 yield not-K(Q). Unrestricted single-premise knowledge transmission together with conditions 1–2 yields K(Q). Thus these commitments cannot all be retained for the same case and interpretation.

Condition 1 is not derived from S(e,P). Condition 2 is not an encoded truth-table label. Actual retention of K(P) is not asserted at w2, where P is false. The hypothesis of knowledge at the actual episode remains a substantive epistemological premise.

Condition 5 is especially important if the retained formal schema is existential: a single nonsensitive contributor cannot exclude another informative operative source. An insufficient reason alongside a sufficient actual basis would not provide the advertised conflict. One must either specify the complete operative basis or justify why this particular rQ is the basis to which the necessity applies.

## Evidence shift: the strongest objection

**Objection.** The argument assumes precisely what the closure defender need not concede. After competent deduction from something known, the premise's factive content P may itself be the subject's reason for Q. Calling the basis merely e or bP underdescribes it. The actual reason need not be the same psychological state-type that could survive P's falsity.

**Consequence.** If rQ = P, then S(rQ,Q) holds. The displayed route to not-K(Q) disappears. If P is included in the complete operative reason conjunction, that conjunction also disappears in every not-Q world. This does not prove K(Q); it only removes this particular necessary-condition failure. Whether P really is the operative reason is not settled by its being true or by the subject's merely possessing knowledge of it.

**Reply available to the conditional reconstruction.** Acknowledge the alternative and identify the disputed premise. The test remains useful because it shows exactly what the nonfactive interpretation and chosen counterfactual semantics commit one to. It cannot adjudicate between factive and nonfactive basing simply by redescribing e as “the real evidence.” A developed account must explain which basis is actually operative and why that individuation is appropriate.

The contrast is therefore between conditional packages. It is not an unacknowledged inconsistency in a view that openly rejects unrestricted transmission and accepts the distribution cost.

## Other limits that matter

- The fixed nearest-world semantics is a transparent reconstruction of one sensitivity gloss. It is not an independently justified metric for every actual case or a complete reconstruction of information theory. A different metric or different reason individuation can change the evaluation.
- A conditional phrased with “unless” is not silently assumed to have every property of this model's explicit counterfactual. The displayed definition, rather than a universal claim about English conditionals, does the work.
- This addresses Hawthorne's strongest single-premise formulation; co-possession of P and an implication without performing an inference would miss the target.
- Actual evidence shift, new defeaters, or loss of premise knowledge must be assessed rather than suppressed. The strongest transmission principle expressly retains premise knowledge.
- The test does not itself distinguish ordinary from allegedly heavyweight conclusions. Nor does it show which real examples instantiate the stipulated ordering.
- The earlier attention example still has its limited role. This inferential test instead grants genuine deduction and studies whether epistemic status transmits under specific assumptions. The two tests must not be merged.

## Recommendation

Retain the test with explicit conditional status and the factive-reason escape. Its main philosophical value is identifying the disputed basis and counterfactual metric after genuine inferential use has been granted. Credit the source debate for the underlying tension; do not present the finite model as an independent cognitive naturalization or an original refutation of Dretske.

## Final exact-file review

Inspected the revised INFERENTIAL_TRANSMISSION_TEST.md, RESULT.md, and PUBLIC_SOURCE_SUMMARIES.md after the two requested repairs. Both strict entailment by definition and the complete-operative-basis/no-additional-conclusive-ground premise are explicit. The attention test is kept distinct from the genuine-inference test. The necessary/sufficient distinction and the factive-reason alternative are preserved. Source attribution to Hawthorne and Dretske's acknowledged distribution cost are sound.

Independently verified the displayed three-world calculation and the additional w3 control at distance 1.5: the latter retains w1 as nearest not-P while selecting w3 as nearest not-Q, so both sensitivity conditions hold. This verifies the schematic modal calculations only, not their real-world epistemological applicability.

**No remaining substantive blocker within this review's scope.** This is scoped approval of the conditional argument and source mapping, not certification of a complete epistemology, the separate fitrah bridge, corpus-wide completeness, or programme closure.

SHA-256 of exact reviewed drafts:

- INFERENTIAL_TRANSMISSION_TEST.md: `9e60b3c227a434093da9f6d1c6dffe624de9ed16abf2dac09d1393311652782c`
- RESULT.md: `4c48b7ec591654c39f9a8bc93c2e15c7e7f8bf67fd3de202d51fec0da07d8972`
- PUBLIC_SOURCE_SUMMARIES.md: `b403d5c798869f9124b40736410d87852022f8c8c94cc71bea9c69ef58404a2a`

The earlier ASSESSMENT.md remains unchanged at SHA-256 `2669ee4d590a46442e94720090a3ab121af779b48b853a16752c1758ed08ce03`.
