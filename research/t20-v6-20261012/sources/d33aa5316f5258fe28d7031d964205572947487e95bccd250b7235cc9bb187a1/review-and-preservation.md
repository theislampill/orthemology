---
title: Review Adjudication and Preservation
date: 6 September 2026
---

## Scope and decision

This assessment accompanies the fifth delivery of *Information, Composition, and Self-Revision: Local Descriptions and Operative Access*. The exact supplied fourth-delivery source and archive are the comparison baseline. The two supplied reviews are advice to adjudicate, not proof of correctness, usefulness, or publication readiness. The research manuscript contains no delivery-version label or discussion of this revision campaign.

The justified change is bounded: clarify the existing workflow's interfaces, candidate-version identity, noninterference assumption, and acceptance boundary; retain the guarded-command citation and add a separately scoped concurrency citation. There is no new theorem, formalism, domain application, or performance claim. The main manuscript remains twelve pages with the same 11-point body type, A4 page, margins, paragraph settings, and mathematical notation.

## Adjudication of the reviews

**Theory freeze and interface scope — accepted, with a correction to the diagnosis.** The predecessor already calls the workflow a specified interface example and permits overlap only when noninterference is established. This was not an absent assumption or an invalid lemma. The revised opening calls the three mechanisms operation interfaces; the scheduling paragraph explicitly names the noninterference assumption and says that interface names do not establish it. The assumed property is that neither job invalidates state or evidence required by the other. Qualification of a concrete implementation is still separate.

**“Version-bound” — accepted as a terminology clarification.** The predecessor's candidates were already immutable and included the material acceptance context, so the intended interpretation was available. The revision identifies them explicitly as candidate versions, rules out reusing a label for changed content or context, and defines version-bound acceptance as comparing receipts with the current candidate identity at the protected boundary. This is not a chronological ordering, a new epoch protocol, or versioning of an entire methodology. Nor does it freeze the whole workflow indefinitely.

**Dijkstra — retained; concurrency support added, not substituted.** The criticism is right that guarded-command syntax alone does not protect against intervening changes. The review itself distinguishes that limitation from Dijkstra's legitimate role: Sections 1–2 support the original sentence about guarded-execution semantics. The predecessor's final paragraph already separately required boundary protection and cited Abadi–Lamport for implementation assumptions. Dijkstra is retained at its original sentence. Herlihy–Wing is added at the sentence about specifying an indivisible concurrent effect. Its definition is a correctness specification, not evidence that this manuscript has implemented or proved a concurrent object.

**The guard's entire input — sharpened after direct examination.** The guard depends on $(q,e_1,e_2,b)$, not just $q$ and $b$. The predecessor's protected-boundary wording can cover all four, but its closing sentence explicitly named only identity and interrupt state. The revision names all four inputs. A coherent read must remain stable through the effect, or the inputs must be jointly revalidated with publication as one atomic operation. Separate atomic field reads do not establish that compound property. This clarifies the implementation obligation without changing the static relation or its proof.

**Effect versus response — made explicit to bound the new citation.** A linearizable operation has an abstract effect within its invocation–response interval. That does not guarantee that its accepted condition remains true until the caller receives the response, much less forever. The manuscript now states that the verdict is scoped to its effect; later material change opens a new acceptance boundary. This preserves and clarifies the predecessor's historical-verdict rule rather than promising permanent readiness.

**Two pieces of reviewer shorthand — not inherited as mathematical claims.** Reviewer 2's shorthand that setting $c=\mathtt{open}$ realises every singleton value omits the value $c=\mathtt{complete}$. The actual manuscript proof already handles that case separately by matching both receipts and clearing the interrupt; it is unchanged. Reviewer 1's proposed identification of unprompted parallel execution with the richer observation map is not generally justified. Dispatch changes execution; the richer map exposes receipt bindings. They can participate in one procedure without being the same operation. Similarly, constancy of an admission predicate is not enough for a positive verdict when its constant value is zero. The manuscript already requires the observed fibre to lie wholly in $h^{-1}(\{1\})$.

**Rankings and “shippable” — not adopted as results.** The reviews supply favourable judgments, not a reader study, an independent proof audit with inspectable records, an exhaustive novelty search, or a venue decision. Their agreement is not treated as independent corroboration. The supportable gain is greater precision of the existing interface and citation boundaries; mathematical strength and application scope are not claimed to have increased.

## Preservation argument

The exact edit contract permits five prose replacements within Section 5.4 and one appended bibliography entry. Applying those replacements to the preserved predecessor source reproduces the delivered source exactly. Everything outside that region and the appended entry is therefore byte-identical, including the abstract, information-first structure, physical boundaries, admission argument, and four-question summary table.

The separate comparison checks establish equality of all eight complete numbered statement-and-proof blocks, every displayed mathematical block, all existing labels, and the nineteen inherited bibliography entries. Numbering is checked against the resolved LaTeX labels. The twentieth reference is Herlihy–Wing. The six inherited mathematical checkers also retain their exact bytes.

The inherited 115-obligation map and the twelve additional obligations introduced in the previous delivery are retained with current page locators. These are navigational and author-reviewed semantic records, not mechanically certified atoms or an independently rediscovered denominator. Prior historical judgments remain ancestry; this revision does not re-certify all earlier campaigns. The five changed passages are individually reviewed for preservation: qualified jobs and interrupt handling remain, candidate identity is made explicit, receipt accuracy remains a premise, overlap stays conditional, and acceptance remains protected and effect-scoped. The complete predecessor source and reversible patch are included.

This supports preservation relative to the exact supplied baseline. It does not prove preservation of unstated intentions or universal semantic completeness.

## Targeted evidence

All six inherited mathematical suites were rerun unchanged and passed. Their detailed outputs and exact script hashes are included. Their finite domains and earlier counterexample checks remain as declared; they are not counted as new theory or independent review.

The additional boundary-sensitivity checker exhausts **1,296 ordered pairs** of the workflow's 36 input records. Publishing according to the current joint guard satisfies the boundary relation in each case. Reusing an earlier positive decision admits **68 invalidating transitions**; **16** of those retain candidate identity and interrupt state while changing receipts. Separate witnesses change each of the four guard inputs alone. These results show why naming only two fields would be insufficient without further immutability premises.

A three-state interleaving additionally has no ready state, yet individually atomic reads assemble a ready-looking tuple that never existed. This distinguishes a coherent joint check from per-field read atomicity. A later-interrupt example preserves the old, scoped acceptance record while requiring a new open boundary. A deliberate label-reuse example shows that unchanged tokens cannot certify changed underlying meaning; it violates the immutable-identity premise and is not a counterexample to a theorem.

These are same-author exact checks of abstract records and interleavings. They do not run concurrent threads, verify a lock or compare-and-swap implementation, prove linearizability, establish job noninterference, measure latency, or validate deployed receipt semantics. No new behaviour is credited from the size of the test population.

Document checks separately cover the allowed diff, statement/proof and equation preservation, references, current locators, metadata, page boundaries, and absence of a manuscript-version label. The rendered pages are inspected for layout. The delivery receipt records archive readback, fresh extracted-package rebuilding and testing, and comparison with the published files. The finalised *The Cost of a Decisive Revision* is read-only and checked against its initial byte identity.

The newly authored manuscript-version scan initially misclassified the unchanged IUPAC bibliography phrase “online version 5.0.0” as a manuscript label. The scan was corrected to distinguish manuscript labelling from source-edition data; title metadata and unchanged headers remain checked. Injected manuscript labels still fail. No manuscript text or inherited mathematical checker was changed to obtain this pass. The failed witness and repair rationale are retained in `instrument-notes.json`.

## Sources and limits

Dijkstra's author-manuscript transcription, EWD472, Sections 1–2, was consulted at the University of Texas archive. It explains eligibility of guarded statement lists and the alternative/repetitive constructs. Herlihy and Wing's author-hosted published article was consulted for its abstract and Sections 1.1 and 2.2, particularly printed pages 463–464 and 468–469; pages 463 and 469 were also visually checked. The journal reference is *ACM Transactions on Programming Languages and Systems* 12(3), 463–492 (1990), DOI 10.1145/78969.78972. The source-check file records these exact access scopes, the unsuccessful publisher-page read, and URLs. It does not claim a fresh full read of every inherited reference.

The revision closes the identified ambiguities without enlarging the theory. “Better” here means those specified explanatory and attribution defects are reduced while the prior mathematical content is preserved. Actual readability, general usefulness, historical originality, and publication suitability remain open to readers and independent review; no optimal page count or universal improvement theorem is claimed.
