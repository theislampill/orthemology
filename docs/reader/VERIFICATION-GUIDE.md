# Verification, source inspection and maintenance

> **Reader candidate.** [Scope and review state](../project-closure/reader-refactor-issue-35/PROGRESS.md). Each cited work retains its own scientific standing.

[Atlas](RESEARCH-ATLAS.md) · [Works](PAPER-CATALOGUE.md) · [Results](RESULT-INDEX.md) · [Frontiers](CURRENT-FRONTIERS.md) · [Applications](APPLICATIONS.md) · [Verification](VERIFICATION-GUIDE.md)

## Choose the claim before choosing the check

A claim that a PDF matches its source, a theorem follows from stated assumptions, a finite test passes, and a philosophical interpretation is warranted needs different evidence. The repository preserves those distinctions in its publication, source, result and review owners.

**Source identity and content hashes.** These establish which exact bytes were retained or compared. They do not establish correctness, novelty, source reliability or equivalence between different editions.

**Written mathematical arguments.** Read the actual argument and its assumptions. An ordinary proof is not made less mathematical by lacking Lean formalisation, but its existence is not evidence of fresh kernel checking or empirical applicability.

**Recorded formal compilation.** A receipt concerns the formal declarations and imports checked in its named environment. It does not automatically certify surrounding prose, a proposed application or a metaphysical premise.

**Finite controls.** Observed tests establish behaviour for the cases actually exercised. They are not universal proofs or empirical validation of an unrun study.

**Existing review.** A review establishes what its named reviewer examined and concluded at that time. It is not a fresh independent review of changed prose or of this refactor.

**Owner acceptance and repository merge.** These record the applicable decision or integration event. They do not automatically close research questions, constitute external peer review or validate every component.

The [result/evidence owners][evidence] and [T20 source recovery guide][recovery] supply the scope for concrete results. Do not replace that scope with one badge for an entire page.

## Checking a primary-work claim at its actual level

Use the [five principal-work descriptions](PAPER-CATALOGUE.md#core-exposition-and-formal-reference) to locate the source chapter before choosing evidence. A definition in the formal reference is not automatically a theorem about every implementation. The [episode signature](../../theory/orthemic-core-formalization.md#22a-endpoint-plus-bounded-trace) determines what a record contains; the source's governance determines which trace and pathway checks apply. A correct answer does not settle every required check, and a finite adverse control is not an empirical validation of the framework.

For a philosophical or theological statement, first identify its bearer, sense and inferential role. The [orthability step map](../../companion/ARGUMENT-MAP-ORTHABILITY.md) separates the affirmative reductio from additional attribute premises. The [seven Speech bearers](../../companion/orthability-divine-attributes-and-speech-athari.md#21-seven-speech-bearers) prevent transferring a predicate about the reciter's created act to the revealed Word in the manuscript's Atharī account. Existing [source-status records](../../references/source-status.yaml) concern their particular passages and roles; a reader synopsis does not turn partial source access into new authentication. Review the [later authority note](../../companion/orthability-and-the-ground-of-intelligibility.md#later-v11-authority-qualification) with the argument it qualifies.

The [primary curation record](../project-closure/reader-refactor-issue-35/PRIMARY-WORK-COVERAGE.md) states what this refactor actually read. Chapter-link checks establish a navigable route, not that the reader accepted the argument or that a different source's status was inherited.

## Inspecting a selected mathematical result

For the [finite-mediator bound](RESULT-INDEX.md#finite-mediator), read the statement, the complete-mediation assumption and the ordinary proof in the linked paper. A small controller program is not automatically the mediator that the theorem assumes.

For [tensor Theorem G](RESULT-INDEX.md#tensor-moments), distinguish the all-polynomial path assumptions from finite moment truncations, and the law determined by a complete path from the potentially nonunique paths of an initial record. The source's ordinary written theorem is not a Lean proof merely because the repository also contains Lean files.

For [the Fisher corollary](RESULT-INDEX.md#fisher-geometry), check the ambient norm identity in the controlling source as well as the corollary and its existing review. The fixed-fibre dimension result does not assert a globally minimal chart or that every posterior task needs the same information.

## Checking an identity result without merging its evidence scopes

Start with the [Thirteenth/Fourteenth work sequence](PAPER-CATALOGUE.md#identity-representations-and-finite-proof). The Thirteenth papers and the Fourteenth certificate/search paper have ordinary written claims. The [later formal suite][t14-suite] names five target declarations, including full-rule separation, the closed `HasPlus` identity criterion and the separate `HasE` witness/soundness package. The [recorded completion review][t14-review] concerns those declared targets and their controls; it is not fresh execution by this refactor.

A source file containing formal declarations does not make every theorem, computability premise or explanatory paragraph in a linked manuscript kernel-checked. Conversely, the historical written-only label on the earlier manuscript does not erase its later, narrower formal component. Check the exact calculus namespace and target theorem before transferring any evidence label. Do not identify a dated package label with every current public calculus bearing a similar name.

The [certificate/search work][t14-certificates] describes a total mathematical check of supplied finite annotated derivations. Its written undecidability argument explicitly identifies an imported representation premise. No fresh verification of that external premise or executable unrestricted solver is supplied here. The [later restricted checker owner][t15-group-followup] is a different source and problem boundary.

## Verifying a restricted checker claim

Start at [Paper 4](PAPER-CATALOGUE.md#a-complete-restricted-identity-checker) and the [declaration-to-claim map][t15-declarations]. The original restricted Lean checker proves a complete coefficient decision and finite typed-certificate service under the original semantics for its declared grammar. Do not replace that theorem with “finite tests only”. Conversely, do not transfer it to the source's strict Python wire-format interface, explicit grid/witness generator or arbitrary endpoint recognition.

The [reference-interface guide][t15-reference-guide] records three separately scoped executions: canonical decoded-JSON checking, finite generated Python/Lean runtime comparison, and one-variable root-extension checking. It links each source and exact suite record. Replaying a source package must retain its declared dependencies and work layout; a hashed source-store directory is not necessarily a directly runnable standalone project. Successful finite comparisons are not a universal refinement theorem.

The [Python certificate implementation][t15-json-reference] uses standard JSON decoding followed by strict structural checks, including rejection of Boolean values where natural integers are required. That is not a proved duplicate-key-rejecting parser. Lean certificates instead admit harmless redundant/split coefficient representations while requiring genuine coverage of every mask. A user-facing verification claim must say which representation was accepted.

The original whole-domain classifications and collective-observation arguments are written mathematics with the particular checked components recorded by their owners. The latter's exact-real sequential decision rule is not a validated floating-point monitor. A fresh reader check establishes neither full scientific replay nor independent acceptance of this refactor.

## Reading and editing a publication

Start with the [publication profile][profile]. It identifies the substantive sources, generated LaTeX and governed rendering relationships. The formal-reference PDF combines the core and multi-actor note; the notation gallery is a diagnostic reference.

Edit the substantive Markdown owner, not its generated LaTeX or PDF. This refactor does not authorise manuscript revision. The [publication-source review][publication-review] and artifact sidecars identify the existing source pin; do not repin a publication to the navigation commit merely to make it look newer.

The repository's existing full PDF check is:

```sh
python scripts/build_pdfs.py --check
```

It requires the declared publication toolchain and infrastructure; the command's presence here is not a claim that it ran in this authoring environment. It checks governed artifacts, not the differently qualified preserved lineage PDFs. The [lineage note][lineage] explicitly leaves the decisive-revision PDF's exact TeX build relationship unresolved.

For citation identity and commit-specific references, follow [Citing this repository][citing]. A reader page must not invent a DOI, author identity or publication acceptance.

## Inspecting or exporting repaired T20 sources

The [source recovery guide][recovery] documents the maintained resolver:

```sh
python -B scripts/resolve_t20_v6_source.py find tensor-realizability
python -B scripts/resolve_t20_v6_source.py resolve 449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a
```

These find and resolve the exact declared public source. They do not execute its proof or confer new scientific evidence. The guide also documents isolated formal-suite export and its pinned Lean/Mathlib requirements. Follow that actual source-recovery contract, rather than assuming a historical relative command refers to the current checkout.

Held or unavailable identities remain held or unavailable. A public manifest row, transformed locator or archived command is not permission to reconstruct private research or pretend a missing historical execution was observed.

**Recorded reader exercise:** the [current qualification record][qualification] reports the executed five-task exercise, its independent adjudication and exact-candidate limits. The unchanged protocol immediately below retains its preparation-time label; that label is not the current execution status.

## Independent reader comprehension tasks for the final candidate

**Preparation only — NOT_RUN.** These five tasks refine the existing [J01–J07 pilot contracts](../project-closure/reader-refactor-issue-35/PILOT.md) and T01–T18 source/interpretation controls. They add no acceptance stage or terminology requirement and do not constitute C05 review or measured learner uptake.

On the eventual final candidate, a genuinely separate reviewer records the exact SHA/tree, reviewer identity and whether the reader/reviewer is a person or an AI/model session. Give the reader the task prompts below, starting at ordinary README entrances without extra navigation directions from the author. Record the reader's answer before comparison with the existing [source-based answers and adverse readings](../project-closure/reader-refactor-issue-35/PILOT-QUALIFICATION.md#source-based-answers-and-paired-adverse-readings). The right-hand column is for subsequent source adjudication, not an answer supplied in advance.

For each task retain the start page, visited links/anchors, exact target identity, concise answer, supporting source passages, ambiguities and any assistance required. Record route found, explanation supported, qualifications preserved and misleading interpretation rejected separately as yes, no or unobserved. Use the work order's PASS/FAIL/BLOCKED/NOT_RUN dispositions; NOT_APPLICABLE requires its existing reasoned independent acceptance. Preserve the three-document-transition design target and document justified exceptions. Click count alone does not demonstrate understanding.

| Independent-reader prompt | What the reviewer checks against the sources |
|---|---|
| **Trace an intellectual claim to its argument — J01/J04, T01/T09.** Find the finite-mediator claim, identify its originating work, state the assumptions and locate the upper-bound proof and matching construction. | The [finite-mediator route](RESULT-INDEX.md#finite-mediator) reaches substantive non-PDF mathematics. The answer includes the Gaussian law, finite alphabet, complete conditional mediation and fixed-horizon scope. Short controller code is not necessarily the complete mediator; the matching retrospective construction is not a demonstrated forward-causal physical coordinator. |
| **Explain a philosophical distinction and its limits — J05/T16.** Explain basic recognition, sound cognition and correction, including tawātur's role beyond report counting. Identify a premise and a source-supported case that excludes a plausible stronger interpretation. | The [recognition route](RESEARCH-ATLAS.md#recognition-sound-cognition-and-correction) retains proper-function, environment, diversity/non-collusion and relevant source obligations. Basic knowledge without universally prior reflective proof does not imply infallibility or justify diagnosing a present dissenter. A foundational example must retain productive adequacy rather than substitute a generic ban on infinite temporal sequences. |
| **Classify claims and evidence — J02/J03/J06, T04–T08/T15.** Distinguish the composite formal reference and edition relationship; then classify a conditional theorem, finite test, inherited execution receipt, review opinion, historical predecessor and unresolved claim, naming each owner. | Both [formal-reference components](PAPER-CATALOGUE.md#formal-reference) survive; the [decisive/reflexive relationship](PAPER-CATALOGUE.md#decisive-and-reflexive-revision) does not establish an exact build. Theorem G is ordinary conditional mathematics; reader controls are finite tests; the tensor execution record is a dated receipt; the sidecar review has a stated premise. No fresh replay erases earlier positive evidence, and no scoped receipt verifies all surrounding prose. The reader must explicitly identify the predecessor and a still-open claim, not only recite evidence labels. |
| **Follow a question to its frontier — J06, T08/T17.** Reach a tensor or Fisher research question, distinguish a result already supplied from a genuinely remaining claim, and specify the proof, counterexample or application evidence that would advance it. | The [coercive successor](CURRENT-FRONTIERS.md#a-historical-tensor-frontier-has-a-written-successor) addresses a former tensor limitation. The [Fisher frontier](CURRENT-FRONTIERS.md#exact-geometry-versus-weaker-retained-tasks) separates exact ambient-norm preservation on a fixed fibre from posterior-only tasks, a different metric and global varying-rank coordinates. The reader must name the chosen contract and check the final candidate's currentness; none establishes empirical human cognition. |
| **Reject a plausible false interpretation — J07/T18.** Explain the occurrence/missing-outcome joint-feasibility connection, give its counterexample and state its transfer limits. | The [cross-avenue example](APPLICATIONS.md#joint-feasibility-across-avenues) retains complete tuples `(M,M,G)` and `(G,G,G)` without inventing mixed Cartesian tuples or treating an incomplete row as a wildcard. For `{(0,1),(1,0)}`, each coordinate can be zero or one but the sum is always one. The shared operation preserves admissible joint states; it supplies neither Arabic authentication nor evidence of actual empirical dependence. |

The reviewer adjudicates the recorded answers against the actual source passages. The existing [mechanical controls and semantic countercontrol record](../project-closure/reader-refactor-issue-35/PILOT-QUALIFICATION.md#mechanical-controls-and-maintenance-finding) shows that a fabricated universal human-cognition claim could retain valid mechanical routes. These prepared tasks make the independent comprehension obligation testable; they do not discharge it or replace the remaining C05 coverage, preservation, usability and maintenance review.

## Checking reader sources and navigation

<a id="checking-this-reader-pilot"></a>

From the repository root, with the existing locked Python dependencies:

```sh
python -B tests/test_reader_census.py
python -B -O tests/test_reader_census.py
python -B tests/test_reader_pilot.py
python -B -O tests/test_reader_pilot.py
python -B scripts/check_reader_pilot.py
```

These checks compare the crosswalk with the frozen candidate/owner population, bind exact sources, preserve composite and edition relationships, and reject specified omissions and mutations. A reader candidate must disposition every owner group and retain an existing catalogue anchor for every work. Compact support records must still expose actual primary sources and reading forms; anchor existence alone does not prove section-to-work identity. **They do not establish complete work coverage or semantic fidelity.** A misleading explanation with valid source links can still pass mechanical checks; source-based reader review is therefore required.

The optimisation runs above apply to these new validator tests. They are not an instruction to run historical scientific scripts under optimisation: assertion-based controls can lose checks in that mode, as the source recovery guide warns.

The [reader qualification record][qualification] separates actually observed runs, rendered navigation, existing evidence, independent review and the RLGWO acceptance predicates.

## Checking an application contract without overstating it

For the [worked corrective transition](APPLICATIONS.md#a-corrective-step-that-legitimately-ends-in-hold), inspect the original burden accounting, reread and verdict fields together. The result is an admissible transition ending in HOLD, not a hidden claim of closure. The existing commands include:

```sh
python -B scripts/validate_corrective_transition.py
python -B scripts/validate_semantic_operator_contract.py
python -B scripts/validate_noetic_claims.py
python -B scripts/validate_dynamic_orthing.py
python -B scripts/validate_somnic_orthing.py
```

These are repository-local contract/fixture checks, not execution of an external DAEE installation or measurement of cognition. The [application-coverage record][application-coverage] identifies all eleven existing validators actually exercised for this curation increment, the precise reading scopes, and the independent fifty-file denominator. The three runtime profiles' outline status is not changed by a passing schema or fixture.

The reader tests separately require every baseline application file to have a disposition and every principal work to have a direct source route. They reject omitted support files, schema-to-paper promotion and loss of the worked corrective, learning or collective routes. Their coverage proves neither that each interpretation is correct nor that every application elsewhere in the repository is represented. Those remain source-based review and complete-corpus obligations.

## Reanalysis evidence without importing participant records

Start with the [reanalysis guide](../../experiments/orthemology-v5-successors/groups/t15-reanalysis/README.md), [original package instructions](../../experiments/orthemology-v5-successors/source-store/55f26bac8864c6e3279debaf821d1c714abbcff6f22f5364a654823ae6a61b70/README.md) and [checksum list](../../experiments/orthemology-v5-successors/source-store/9ab3df6e096f8158f755ea31408786248d04547d0bd7c38785770d7e9964e41e/SHA256SUMS). The package is preserved in source-store paths, not an already assembled runnable directory at the reader page. Follow the guide's isolated projection and the package's commands; do not treat a command displayed in an archival source as a root-level repository command.

The [input contract](../../experiments/orthemology-v5-successors/source-store/a919102c102ff3d07b447f52490266aca76afa4f84a972e2f3d78b3470f97a7a/INPUTS.json) names two separately obtained official inputs and the selected internal member, worksheet and columns. Those identities are not public participant bodies, and the extra method-context reference is not a third required runtime input. The driver performs local input parsing and aggregate output, not downloading or record-level export. This refactor acquired neither input and did not execute the numerical reanalysis.

The [original provenance](../../experiments/orthemology-v5-successors/source-store/60755eff76d1f0b1cc1fcd56aef8a4b8bf91b17fee744ed20b6c6260e0e8f33e/BINDING.json) records one historical Python environment; the [later environment record](../../experiments/orthemology-v5-successors/groups/t15-reanalysis/ENVIRONMENT.json) identifies the separate integration environment. The source requirement is Python 3.12, not the reader CI's Python 3.11.9. Consult the actual requirements file rather than copying those scientific dependency pins into the reader toolchain.

The [dated execution summary](../../experiments/orthemology-v5-successors/groups/t15-reanalysis/EXECUTION_SUMMARY.json) records original synthetic tests, numerical agreement, aggregate equality and an intended damaged-input exit. An `assertRaises` test that passes is not itself a subprocess failure; the separate corrupted-input command is the recorded exit-2 control. These historical observations remain **FINITE_ONLY**. Byte-identical original and later aggregates establish repeatability at the recorded scope, not a new cohort, proof of an optimiser, participant-mechanism identification or independent review of this refactor.

## Maintaining the reader layer

The work catalogue is the primary editorial home for a work's description and edition presentation. The atlas explains subject relationships; the result index locates claims; frontiers discuss the relevant open question; applications explain a use and its additional assumptions. They should not independently maintain competing status or edition lists.

For a new rendering, update the actual publication/edition owner and the corresponding catalogue route. For a changed statement supporting a synopsis, review that synopsis and its exact source binding. A source change must not silently leave an old interpretation labelled current; an unrelated change need not rewrite every page.

Stage admitted new files before running the existing generation owners:

```sh
python scripts/generate_current_state.py
python scripts/make_manifest.py
python scripts/generate_current_state.py --check
python scripts/validate_current_state.py
python scripts/validate_review_state.py
python scripts/validate_internal_references.py
```

These are selected integration checks, not a substitute for the complete [.github/workflows/validate.yml][ci] contract. Preserve the authored state, existing scientific owners and all required gates. [Decision 0014][decision14] explains the source-digest and convergence rules. A passing pilot or a populated set of headings is not the final refactor.

## Checking the composition and revision lineage

The [catalogue](PAPER-CATALOGUE.md#information-and-composition) supplies commit-pinned TeX line links for the exact source statements. They identify baseline text, not generated Markdown headings. The focused reader tests derive those lines from protected source markers and reject a generic file link or a different valid line in its place. This checks location; it does not certify the argument.

The four-page decisive-revision PDF was read directly for its own description. That is a reading of preserved output, not a clean rebuild, exact-source attribution or new formal verification. The lineage's unverified-build qualification still governs. A PDF and related TeX can make similar statements without their build relationship having been established.

## Original v5 reference versus mapped formal evidence

The [native guide](../../experiments/orthemology-v5/README.md) defines static `--check`, runtime/kernel outcomes and fresh external staging. Its software and formal components have an explicit [original-to-derived amendment](../provenance/v5-consolidation/FORMAL_SOURCE_AMENDMENT.json). Inspect the exact postimage hashes and named target scopes before treating an old missing-build statement or a later successful receipt as applicable to your target.

This refactor's path dispositions account for code, tests, ledgers, prior editions and mathematical notes without running the historical science again. The [coverage record](../project-closure/reader-refactor-issue-35/COLLECTION-COVERAGE.md#original-v5-consolidation) states what was substantively read and what was only role-inspected. A mapped formal audit remains distinct from whole-Python refinement, primary-source authentication and independently accepted mathematics.

## Following the actual controller proof chain

Start from a [named controller work](PAPER-CATALOGUE.md#generated-controllers-observation-laws-and-executable-delivery), then use its contract, the [source map](../provenance/v5-research-continuations/SOURCE_MAP.json), the [result state](../provenance/v5-research-continuations/RESULT_STATUS.json) and the [Sixth-final selection](../provenance/v5-research-continuations/SIXTH_FINAL_OVERLAY.json). One later compiled module over exact qualified predecessors is meaningful evidence, but not a new cold build of the whole closure. A provided replay command is not an executed receipt.

[The final combined source-only replay guide](../../docs/provenance/v5-research-continuations/notes/ed3d671599c4d246dafb7f66bcdc1222d5e43e8667b9f527776e2181d6ff8081.md) distinguishes the runtime, phase and probability roots and requires external output paths. The [common exponential review](../../docs/provenance/v5-research-continuations/notes/a96b3fc7e9c37ccb4ef28fea5d652e2b4229a704b97b8d7531c5595a08cf1ad9.md) states its actual one-module/reused-object boundary. Original scientific checks and immutable source bodies must not be edited to match a simpler reader synopsis. This refactor inspects their interfaces; it does not newly compile the scientific closures.

## Checking a foundational implication without changing its subject

For the [sourcehood/Knowledge family](PAPER-CATALOGUE.md#original-productive-sourcehood-knowledge-and-action-selection), inspect the ordinary argument, exact model specification and original review separately. Preserve the noninferential clarification when reading the creative-Knowledge appendix: logical closure does not describe a source learning from premises. A formal counterinterpretation tests an entailment of its stated predicates; it is not automatically a metaphysically admissible rival.

The [integer budget package](PAPER-CATALOGUE.md#exact-integer-confidence-budgets) also separates exact arithmetic verification from the controller theorem's stochastic applicability. Its record correction is about exact data types, not a new probability law. Follow the existing collection replay owner for supported execution, rather than running a historical archive-relative command as though it described the present checkout.

## Qualifying the philosophical ascent without changing its subject

For the [necessity and attribute family](PAPER-CATALOGUE.md#necessity-objective-correction-and-attribute-ascent), compare the actual argument, its named constituents and its premise map. Ask whether a reader has silently substituted actual independence for existential sufficiency, endpoint supply for complete actual origination, or knowledge of a good for perfect practical orientation. Those substitutions can survive a valid URL and a matching hash; rejecting them requires source-based reading.

The norm-fixing source's semantic retractions also require a real warranted relation to the target and lawful implementation, not just algebra on sets labelled “correct”. Its discrimination appendix gives concrete source/intervention questions. The attribute map's computational checks have their stated finite scope; they are not independent tests of the philosophical truth, primary-text authenticity or actual revelation. Existing scientific judgments remain at their owners, and the current refactor is not authorised to revise them.

## Distinguish exact certificates from source-relative reviews

The [four-corrupt/three-message family](PAPER-CATALOGUE.md#three-messages-and-four-corrupt-roots) separates ordinary arguments from three finite exact certificate trees proving continuous-domain lower bounds. Its author verifier uses assertions; do not treat an optimised run that omits them as replay evidence. Its retained independent verifier and review have their own explicit checking scope. The refactor's normal/optimised tests validate reader behaviour, not those original certificates.

The [complete fixed-codebook theorem](PAPER-CATALOGUE.md#the-complete-fixed-codebook-classification) instead names an external hypergraph theorem and two recorded ordinary reviews, with a required endpoint clarification. Reading those records does not mean the external primary paper was reacquired or reverified in this task. A reviewer should test the shared-random/fixed-codebook and timing distinctions against the actual model, because valid links alone will not detect a summary that silently changes the game.

## Reading mixed proof and execution evidence in the Seventh sequence

Start from the [result-specific guide](../../experiments/orthemology-v5-successors/groups/t07-technical/README.md), then the linked argument and formal declaration. A declared-suite receipt can coexist with **component-only credit for a mixed scientific claim**: running the entire package does not turn its ordinary argument, finite scenarios or external applicability premises into one kernel theorem. Attribution A–C, covering/search, original histories and compiled composition have different theorem scopes.

The guide also separates exact retained raw receipt identities from reviewed public summaries. A public summary can establish its own identity and source contract without revalidating private omitted log bytes. Failed historical attempts remain failures; a later audit-only continuation neither reruns the original producer nor creates additional independent executions. No receipt described there is a fresh scientific replay by this reader refactor.


## Comparing a history theorem with its actual execution contract

For the [Eighth sequence](PAPER-CATALOGUE.md#common-histories-shared-stores-and-actual-batches-the-eighth-sequence), inspect the named trace type and the concrete operations it admits before citing preservation or progress. The same epoch number need not authenticate the same policy; a false return need not be an identity transition; and a forward refinement need not preserve permission in reverse.

The [shared interpreter clarification](../../experiments/orthemology-v5-successors/source-store/ac522e04a17cd99459c265883df2253716cf0ccd0779b1bd748fd0c0a2783f14/EXECUTION_CLARIFICATION.md) separates kernel-checked mathematical definitions from extraction/native evaluation. The separate [shared-root review supplement](../../experiments/orthemology-v5-successors/source-store/8d0d5c3934128136fbd69b70b8a0669fe055e5eb005797e25269a69157361657/PUBLIC_ACCEPTANCE.md) retains failed wrapper attempts and a withdrawn interpreter attribution. Neither source publication nor a new link check upgrades those historical executions.


## Reading Ninth proof, replay and metadata evidence

The [certificate work](PAPER-CATALOGUE.md#finite-common-policy-evidence-without-rerunning-synthesis) has three formal component scopes and a separately ordinary cost argument. Its corrected `d08-g1` descriptor is a **retained-evidence-only** view: the source-owned guide explicitly rejects advertising that descriptor as a runnable `--execute` route. The unchanged original driver/catalogue API is a different source-bound replay route requiring its pinned inputs and a fresh absent output. A correction to membership metadata supplies no additional process or independent evidence.

For the [expression correspondence](PAPER-CATALOGUE.md#expression-stacks-costs-and-the-python-trust-boundary), the completed tail reused previously compiled products and finite observations while performing only its missing stages. Preserve the earlier failed attempts and do not count correlated views as independent runs. For the [initial controller](PAPER-CATALOGUE.md#finite-reconstruction-and-an-actual-initial-state-controller), compiled tuple assertions and formal endpoint statements have different scopes. Inspect both when a claim depends on actual emitted event counts; neither creates a CPython or physical-deployment theorem.

## Matching a typed result to the exact calculus

For the [Eleventh sequence](PAPER-CATALOGUE.md#typed-contexts-substitution-and-source-representation-the-eleventh-works), inspect the actual source grammar and theorem signature before reusing a namespace label. The public P01DF and research raw-index P01DF owners are distinct. P01TC's opaque finite All leaf does not supply P01AC's recursive All rules; HasPlus/HasE are separately named later judgements.

The linked original reviews report source-only rebuilds and exact declaration/axiom checks. Their reported independent acceptance is preserved as **historical research evidence**, not a fresh independent review of this reader refactor. The first substitution adapter failure and corrected retry also remain discoverable through the original collection guide. A support certificate covers the retained typing tree and displayed conversion endpoints, not the recoverable provenance of arbitrary hidden Prop-valued proof intermediates.

[profile]: ../publication-profile.yaml
[lineage]: ../../theory/lineages/h-ics-v5/README.md
[evidence]: ../provenance/v5-successors/EVIDENCE_BINDINGS.json
[recovery]: ../../research/t20-v6-20261012/SOURCE_RECOVERY.md
[publication-review]: ../provenance/v5-consolidation/PUBLICATION_SOURCE_REVIEW.json
[citing]: ../CITING.md
[qualification]: ../project-closure/reader-refactor-issue-35/PILOT-QUALIFICATION.md
[ci]: ../../.github/workflows/validate.yml
[decision14]: ../decisions/0014-generated-project-state-and-whole-state-reread.md

[application-coverage]: ../project-closure/reader-refactor-issue-35/APPLICATION-COVERAGE.md

[t14-suite]: ../../experiments/orthemology-v5-successors/suites/t14-identity.json

[t14-review]: ../../experiments/orthemology-v5-successors/source-store/e9c756ef20f5eb9b5188c3d55c9808fb0462280caa8a6048182ad7b3d55c9cbb/Orthemology_Fourteenth_Completion_Verification_v1_20261005.json

[t14-certificates]: ../../experiments/orthemology-v5-successors/source-store/2c16dbf40f6a945785b51ddc230a0e1f78004fe716a0412492b4345be8c95734/Finite_Certificates_and_Inhabitation_Limits_for_P01AC_and_HasPlus_v1.md

[t15-group-followup]: ../../experiments/orthemology-v5-successors/groups/t15-identity/README.md

[t15-declarations]: ../../experiments/orthemology-v5-successors/source-store/3f6e138825d599075b6f920f0079ccc2ca8b7d6c24c8bba0940af4f62d68de1a/DECLARATION_CLAIM_MAP.md

[t15-reference-guide]: ../../experiments/orthemology-v5-successors/groups/t15-restricted-reference/README.md

[t15-json-reference]: ../../experiments/orthemology-v5-successors/source-store/8f5ba88d07447c8c92d49161f82118f805cae707404b477c81936828103d60ef/certificate_checker.py

## Continuation source identity, theorem scope and replay

For a retained continuation note, the [source map](../provenance/v5-research-continuations/SOURCE_MAP.json) records its origin/member, exact public path and whether it is an exact body, a reading projection or a held identity. The [result owner](../provenance/v5-research-continuations/RESULT_STATUS.json) binds the relevant scientific result to source/review/suite IDs; the [registry](../../experiments/orthemology-v5-continuations/registry.json) resolves those suites. Equal public bytes can have several original aliases without becoming independent evidence.

[The geometric scope note](../../docs/provenance/v5-research-continuations/notes/71156aa5eb3f520e004fd15b3c8eb5a994bbf87c9735c00e0ea9c921f409e10e.md) identifies kernel-checked spines, intrinsic-interior wrappers and ordinary-only block/symmetry/philosophical conclusions. [The causal-restoration guide](../../docs/provenance/v5-research-continuations/notes/b5150cb34c158dfec81cb9a738c02396946dfb2fc8aee0f9abb56b7cecd56347.md) distinguishes finite-sample, causal-locality and generated-process endpoints. Follow the current [isolated export/replay procedure](../../experiments/orthemology-v5-continuations/README.md), not a machine-local command preserved inside an old note. This reader curation does not replay the underlying science or authenticate its external bibliography.

## Match the exact audit or geometry component

For [critical repair](PAPER-CATALOGUE.md#an-exact-obstruction-hidden-by-a-zero-margin), the [CriticalZero receipt](../provenance/v5-research-continuations/checks/db6ccdc793a0-geometry-delta-audit.json) names the polynomial and finite-certificate components; it does not formalise the general C³ localization theorem. The [mixed-rank receipt](../provenance/v5-research-continuations/checks/db6ccdc793a0-mixed-rank-kernel-audit.json) records later MixedRepair/ProductObstruction readbacks, so the earlier note’s pending formal status is not the final word on those components.

For [actual-law audit repair](PAPER-CATALOGUE.md#an-executable-rational-certificate-under-an-actual-source-law), source-level universal refinement of grouped/sequential Lean routines is a positive theorem, not merely finite Python agreement. Conversely, that theorem is not a compiler/host proof or a guarantee that a certificate will be issued. Keep the acquired-prefix clock, independent fresh next draw, abstention and two different probability layers visible when replaying or applying a named result. The current refactor’s source/navigation tests do not replay these scientific suites.


### Receiving new research after the pinned census

The reader check compares the tracked candidate with the approved source commit, not only the files already named in the crosswalk. A new work or checkpoint, or a changed scientific source, requires an explicit finite baseline/disposition update. Do not bypass this by treating it as an ordinary reader edit or adding an original paper to `docs/reader/`. Update the source/edition owner, classify only the new or affected work/support material, and review the affected synopsis; unchanged work descriptions need not be rewritten.

Stage intended public additions before checking; untracked scratch is not part of the published corpus. The exact reader/refactor path allowance keeps explanatory edits out of the scientific census loop, while the original publication, source-preservation and generation gates still apply. A fresh baseline is an identity boundary, not a certificate that new prose has already been reviewed.

## Inspect a prior guarantee at the correct evidence level

For the [concrete sparse example](PAPER-CATALOGUE.md#finite-expected-mistakes-despite-divergent-inverse-moments), inspect the finite-count, divergent-moment and endpoint-support declarations under the same law. For [contamination](PAPER-CATALOGUE.md#the-same-report-policy-before-and-after-contamination), inspect the actual full-word count transport rather than only a prior marginal. For [nonconvexity](PAPER-CATALOGUE.md#two-successful-priors-may-have-no-successful-proper-mixture), distinguish its formal endpoint from the ordinary arbitrary-prior almost-sure lift.

The [rational source](PAPER-CATALOGUE.md#an-executable-rational-witness-with-an-honest-resource-boundary) has separate uncapped core and guarded adapter entry points. Its recorded decimal-parser repair and original independent checks are meaningful evidence, but not a new replay by this catalogue or a proof of the Python interpreter. The explicit source-mode and protected-hash checks continue to preserve all those originals.

## Continuation source and result lookup

For the completed continuation disposition, use the [collection reference](PAPER-CATALOGUE.md#v5-continuation-source-result-and-execution-directory) to identify a work and its original result ID. `collection_dispositions.v5-continuations.result_routes` in the existing crosswalk maps the original registry's exact ID set to work keys; it does not copy claims, scientific statuses or proof receipts. The catalogue then points to the actual note, declaration, recorded review and applicable source owner.

The 676 retained Lean paths are proof/dependency components, not 676 new papers or freshly checked theorems. The 116 suite descriptors are integration adapters, not scholarly works. Historical source-member aliases remain in the original source map even where one public body has several incoming identities. Existing replay helpers and locked environments govern execution; a spaced archive-relative command in an immutable note is not automatically a command for the current checkout.

For the new raw-tape and moment routes, inspect the actual probability-law and tail inputs. For the recursive and indexed-runtime routes, inspect common-policy quantifiers, feasible history guards, literal initial state, acquired-prefix clock and the fuel/output distinction. The reader checks validate bindings and the declared ID population; they do not replace those source-based reviews or rerun the original formal suites.


## Sixteenth volume, proof recovery and independent scope

For a Sixteenth claim, begin at its [constituent work](PAPER-CATALOGUE.md#sixteenth-renewal-certificates-and-supplied-controllers), then the original claim map and source index. The [recovery reference](PAPER-CATALOGUE.md#sixteenth-proof-recovery-and-signed-controller-source-assurance) explains why the 111-module core and the separate 116-module signed/controller closure must not be added as disjoint evidence. It also preserves the different fixture provenance classes, written versus formal results and separate JSON/Python interface.

The [reanalysis entry](PAPER-CATALOGUE.md#sixteenth-social-learning-game-reanalysis) points to its existing exact input and replay contract. No participant input, original PDF or compiler object is republished merely to make a reading route convenient. Replaying this refactor’s reader tests does not replay those mathematical or empirical studies.


## Seventeenth source reading, finite proofs and aggregate software

For a Seventeenth appraisal, read the [report and its explicit disagreements](PAPER-CATALOGUE.md#seventeenth-foundational-research-original-being-perfection-and-warranted-uptake) alongside the [source guide](PAPER-CATALOGUE.md#guide-to-the-six-foundational-sources-and-their-interpretative-relationships). Page-reading metadata, repeated electronic witnesses and source-scope tests do not authenticate all original texts. A reviewer must preserve whose appraisal is affirmative, what its premises are, and which dissent actually survives.

The [mathematical companion](PAPER-CATALOGUE.md#finite-inference-under-assignment-uncertainty) contains ordinary finite proofs, not a newly compiled Lean development. Its earlier substantive text, final authorship/date additions and derived Markdown rendering have a documented relationship; they are not three independent papers.

The [software guide](PAPER-CATALOGUE.md#seventeenth-closed-placement-inquiry-and-exact-supporting-calculations) separates synthetic/aggregate checks from independently pinned manifest verification, original raw-row replay and external DOCX verification. Its public components omit participant data and actual-outcome orchestration. A successful refactor check cannot supply those missing observations or authenticate the external theorem used by the post-inspection certificate. Restore the original indexed package layout before using its own runner; a single source-store file is not that executable directory.


## Eighteenth actual-law proof versus software qualification

Start at the [exact rational endpoint](PAPER-CATALOGUE.md#eighteenth-rational-certificate-to-controller-semantic-endpoint) for the formal statement, then inspect its input binding, lawfulness, measurability and quantification over adversaries. Start at the [implementation account](PAPER-CATALOGUE.md#exact-hidden-change-implementations-and-recovered-composite-qualification) for accepted Python body forms, scoped finite comparisons and recovered-composite replay. A common semantic intention is not a Python/Lean representation theorem; an official cache is not a cold external source build.

For [HasE](PAPER-CATALOGUE.md#eighteenth-hase-transport-and-inhabited-endpoint-countercontrols), keep the exact kernel J theorem, ordinary erased-normal-form argument and separate diagnostic script distinct. For [foundational appraisals](PAPER-CATALOGUE.md#eighteenth-foundational-appraisal-and-the-closed-noncausal-extension), preserve whose position is being described and what a closed extension actually denies. The [source guide](PAPER-CATALOGUE.md#eighteenth-source-and-validation-guide) supplies the inherited reading scope, not a fresh authentication receipt.

## Checking what a source-reading receipt establishes

Use the [Arabic methodology reference](PAPER-CATALOGUE.md#arabic-reading-methodology-and-source-formal-feedback) to distinguish the selected body, the reading act and the claim that depends on it. The [original reading categories](../../experiments/orthemology-v5-successors/source-store/1aedc48f3e7507cb0f14921fcd0905c1f7a89137ed8cabb5450a316903635219/ARABIC_READING_METHOD.md#reading-stages) require actual evidence for a continuous first pass, a local return, a post-completion return or a question-triggered return. A triggered return can overlap the timing categories. A retrospective synthesis has its own value but adds no new primary-reading or proof-replay receipt.

The [reading categories](../../experiments/orthemology-v5-successors/source-store/1aedc48f3e7507cb0f14921fcd0905c1f7a89137ed8cabb5450a316903635219/ARABIC_READING_METHOD.md#reading-stages) retain the actual scope and timing of each receipt:

| Category | What the record must establish |
|---|---|
| AR-S1 | A continuous first pass over the selected received body; extraction and visual reading keep their separate scope. |
| AR-S1R | A local return while the wider first traversal is still under way. |
| AR-S2 | A direct primary return after the selected structure was understood as a whole; a section or volume does not stand for an entire historical work. |
| AR-S3 | An evidenced question or model triggered a primary return. This can overlap AR-S1R or AR-S2; it is not simply the next step. |
| AR-S4 | Synthesis of existing records, with no new primary-reading or proof-replay credit. This supplement has that role. |

This distinction changes how a reader assesses the work. The [selected-body controls](../../experiments/orthemology-v5-successors/source-store/1aedc48f3e7507cb0f14921fcd0905c1f7a89137ed8cabb5450a316903635219/ARABIC_READING_METHOD.md#what-the-completed-studies-actually-show) identify a documented post-completion Darʾ return, distinguish several section/volume returns made during a larger traversal, and withhold a blanket post-completion label where the timing is not established. A later synthesis can improve understanding without becoming another primary reading or an independent witness.

For a claimed source-to-theorem connection, inspect the case's **Return and chronology** and **Still open** sections. [The sign/delegation case](../../experiments/orthemology-v5-successors/source-store/182829543432a0f771f552f74cb3bc2896e5b7e536c0e93bac231b0a3935aef8/CROSS_STREAM_CASES.md#ar-x05-use-signs-and-delegated-acts-at-their-actual-scope) preserves earlier primary returns while leaving its specialised formal transfer unimplemented. [The copied-observation case](../../experiments/orthemology-v5-successors/source-store/182829543432a0f771f552f74cb3bc2896e5b7e536c0e93bac231b0a3935aef8/CROSS_STREAM_CASES.md#ar-x06-repeated-traces-do-not-identify-their-source-or-occurrence) supplies an interpretative link, not an Arabic premise of its statistical result. Relevance, date order and declaration names do not by themselves establish discovery history or fresh execution.

Resolve the supplied aliases through the [finite context/source owner](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json); a custody hash does not supply an omitted body. The [validation summary](../../experiments/orthemology-v5-successors/source-store/3a6e8f9587b050f8093dc48d15cc468b41b3c5a9afbfe5e167ad22707926f274/VALIDATION.json) is an attributed original-author record with an omitted complete check log and no claimed public replay. Keep its recorded scope separate from a new reader-test result. The supplement's retained 14:34 appraisal and the later cooperation reassessment also have different dated owners.

## Checking the six-input Drive-corpus audit

Start with the [Drive methodology reference](PAPER-CATALOGUE.md#six-supplied-drive-inputs-inherited-reading-and-t20-use) and its [original reading/return table](../../experiments/orthemology-v5-successors/source-store/866e0d85f3524013ce7e5e6df1907fe184139259028d6e9b4ded91379893f0fa/DRIVE_CORPUS.md#what-was-actually-read-and-revisited). Match the exact supplied object and one-based PDF coordinates before assessing the source use. The inherited T17 union, selected T18 returns, T20 *Oneness* receipt and separate Arabic witness are different evidence sets. The audit's reconciliation adds no new book reading or independent witness. The [T17 source guide](PAPER-CATALOGUE.md#guide-to-the-six-foundational-sources-and-their-interpretative-relationships) retains its original interpretative responsibility.

The [inherited T17 coverage member](../../experiments/orthemology-v5-successors/source-store/4833ff7cf28db11f9f39972feaf46961fb67d8f7b6e43561f24e68288f932e7b/T17_SIX_SOURCE_COVERAGE.json) attests collective substantive reading of **1,393/1,393 supplied pages**, including the supplied ancillary material, with **190 distinct pages visually inspected**. It is neither one person's six-book claim nor an every-page image check. T18 revisited 188 distinct supplied pages and visually checked 22. Only *Oneness* has a retained fresh T20 exact-English-object receipt: all extracted text and thirteen selected image positions, including blanks and the five diagrams. These returns add no new page to the inherited supplied-page union. Later Arabic reading has its own object and coordinate system; it cannot be counted as another reading of an English translation. The audit itself adds zero primary-reading credit.

Follow the [direct coverage member](../../experiments/orthemology-v5-successors/source-store/4833ff7cf28db11f9f39972feaf46961fb67d8f7b6e43561f24e68288f932e7b/T17_SIX_SOURCE_COVERAGE.json) and [source bindings](../../experiments/orthemology-v5-successors/source-store/4e41aaebbcd30e448cad2b3ac006511c219386e3a0b93d92c416f2ffef04c382/SOURCE_BINDINGS.json). E## identifies an original evidence record; B## identifies an original source-body check. Their original hashes differ in role from the selected public-projection hashes resolved by the [finite context/source owner](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json). The coverage member's own byte hash and its internal coverage-record identifier also refer to different records. No one of these identifiers supplies an omitted original body.

The [verification receipt](../../experiments/orthemology-v5-successors/source-store/3cfc7b197a1c39b4f2c0b67ac3922e8875027b930a59c443fac22a9987e6a1b4/VERIFICATION.json) reports 106/106 original identity/range checks, with no published verifier or public-replay claim. Inspect its scope before treating PASS as evidence: it does not verify bibliographic interpretation, every reading event, empirical claims or philosophical conclusions. At a source-to-result link, check the additional premise and original mathematical owner. The nine mapping areas are not nine newly proved results, and confirmation of an inherited diagram or numerical correction is not another discovery. The receipt's date also leaves the retained 14:34 appraisal and later cooperation reassessment with their separate owners.

## Checking original result credit and receiving execution

Use the [original fifteen-result handoff](PAPER-CATALOGUE.md#the-original-fifteen-result-evidence-and-method-handoff) to follow an achievement through its exact statement, original checks, inherited mechanism and remaining application obligation. The [receiving boundary](../../experiments/orthemology-v5-successors/source-store/d2bf1a9cbfb1e78b79e4ef630fb9c44ba6fb36067557658a6a432e63245fb7c2/METHOD_INTEGRATION_HANDOFF.md#receiving-and-finalisation-boundary) explains why original proof/review PASS and receiving fresh_evidence NOT_RUN can coexist. Reading or indexing a prior receipt does not rerun it. A current documentation CI result also does not supply new native scientific evidence or independent scholarly acceptance.

In the [result ledger](../../experiments/orthemology-v5-successors/source-store/87d09884accfd207240e10d520289cc99947c6a59d1b8ce3adb3b1a8fa880671/RESULT_EVIDENCE_LEDGER.json), inspect `scope`, `provenance`, `fresh_and_inherited`, completed checks and stronger-claim obligations together. An exact declaration signature must be interpreted with its bound source's section variables and typeclass context. The [source bindings](../../experiments/orthemology-v5-successors/source-store/79ad56d83c7585468eebf02286ef86471576e8d16898b96376545b03ac912475/SOURCE_BINDINGS.json) distinguish existing scientific/public aliases from historical original methodology inputs and separately identified projections. Resolve them through the [finite context owner](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json), rather than treating an archive-relative alias as a sibling file or a new result ID.

For example, the [anchored-field handoff](../../experiments/orthemology-v5-successors/source-store/d2bf1a9cbfb1e78b79e4ef630fb9c44ba6fb36067557658a6a432e63245fb7c2/METHOD_INTEGRATION_HANDOFF.md#9-guarded-fixed-source-coverage-and-field-relative-uniqueness) records a general conditional coverage theorem and original independent checking. Coverage does not require CND; guarded uniqueness needs its additional CND/visibility conditions, and an actual application needs qualified classification, conformance, faithful use/role links, an anchor and genuine connectivity. Counting signatures or finite controls cannot discharge those interpretation premises or the separate general Sixth-refinement obligation.

The [original validation](../../experiments/orthemology-v5-successors/source-store/3a4d76f7b6e713bc0e68758cb354e5ed92005fc96357a3d20da5c6b5c5ac67fa/VALIDATION.json) checks source identity, references and signatures, with no fresh scientific execution. Its preserved frozen/canonical synthesis difference and 14:34 appraisal are historical evidence; consult the [present result owner](../provenance/v5-successors/RESULT_STATUS.json) and [later reassessment](PAPER-CATALOGUE.md#cooperation-complete-efficacy-and-the-later-common-source-reassessment) separately. The original fifteen-owner handoff and later result-ledger-v2 have different finite selections. Source authentication and actual normative authority remain independent questions.

## Checking mathematical reading and transfer credit

Start with the [mathematical methodology account](PAPER-CATALOGUE.md#mathematical-reading-local-applications-and-transfer-limits) and its original [coverage and inspection levels](../../experiments/orthemology-v5-successors/source-store/fd16c7ddcbb724e2170b5682414f476cf6e71e7ffb82c49d2ddbcb52d4068cfd/MATH_UTILISATION.md#coverage-and-inspection-levels). In the [utilisation ledger](../../experiments/orthemology-v5-successors/source-store/d0e73b80d86fd9367c434e7711cb1bb40d5e0f61821db03392b5cd2590b61ff5/MATH_UTILISATION.json), inspect the exact component's `inspection_depth`, coexisting `statuses`, `replay_status`, proposed service and required semantic mapping. Seven full and two targeted manuscript body reads coexist with 43 abstract-only priority records; the separately developed local application is not a fifty-third upstream manuscript. Acquiring a PDF or inspecting a family endpoint does not upgrade another manuscript's reading or verification status.

Follow the [local 122 application chain](../../experiments/orthemology-v5-successors/source-store/fd16c7ddcbb724e2170b5682414f476cf6e71e7ffb82c49d2ddbcb52d4068cfd/MATH_UTILISATION.md#family-122-separates-three-manuscripts-from-one-local-application) to the [existing copied-observation work](PAPER-CATALOGUE.md#copied-deletion-traces-and-what-fresh-observations-add) and the [external-transfer assessment](PAPER-CATALOGUE.md#external-theorem-relevance-is-not-a-completed-transfer) for original evidence ownership. Only the local component records replayed/proved status; its later independent PASS supersedes its earlier staging label. All upstream replay fields remain `NOT_RUN`, every direct-upstream-transfer flag is false, and the retrospective ledger adds no replay. The all-`M` fresh-independent formula remains written mathematics with bounded enumeration; cached imports in the recorded finite Lean check were trusted, not rebuilt. These distinctions persist when the reader's navigation tests pass.

Compare the [source bindings](../../experiments/orthemology-v5-successors/source-store/182307031547748730ab7ca741e07edbc64f9d4422258d536b969c5d87e7d651/MATH_SOURCE_BINDINGS.json) with the [retrospective validation](../../experiments/orthemology-v5-successors/source-store/d988a97a3c22e4afb2a36e824e9614ff42e77f0961b29ed5a5eb3d841931d04c/MATH_VALIDATION.json) and [original context selection](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json). The Markdown is an exact selected public body; the three JSON files are derived projections. Original author-output hashes and selected public hashes must not be interchanged, including the explicit 33-module wording correction. Prepared owner aliases, custody-only receipt identities and pinned upstream locators do not assert redistributed bodies or current external availability. The [source-binding boundaries](../../experiments/orthemology-v5-successors/source-store/fd16c7ddcbb724e2170b5682414f476cf6e71e7ffb82c49d2ddbcb52d4068cfd/MATH_UTILISATION.md#boundaries-and-source-binding) retain the deliberately unperformed 713-body scope and unmet target-transfer obligations. Source identity, source reading, formal execution, a faithful target application and philosophical/empirical warrant answer different questions.

## Checking the late result-evidence handoff

Start at the [late documentary subsection of the existing typed-emergence work](PAPER-CATALOGUE.md#late-evidence-handoff-for-the-typed-emergence-control). Compare the [original fifteen-row ledger](../../experiments/orthemology-v5-successors/source-store/87d09884accfd207240e10d520289cc99947c6a59d1b8ce3adb3b1a8fa880671/RESULT_EVIDENCE_LEDGER.json) with the [v2 ledger](../../experiments/orthemology-v5-successors/source-store/6b1e3b7a3ce32842eda6deada3c5bad3ef740215dba77b2f7750d0de51ba333b/RESULT_EVIDENCE_LEDGER_v2.json): the original fifteen result objects are unchanged, and the sole additional row is the already-owned `T20-EMERGENCE-TYPE-CONTROL`. Its successor note is documentary support, not another work, replacement primary edition or owner of those fifteen results. The [original handoff route](PAPER-CATALOGUE.md#the-original-fifteen-result-evidence-and-method-handoff) remains separate.

Read the note's [evidence and receiving boundary](../../experiments/orthemology-v5-successors/source-store/a1c8ae6e7ae4cc8a8e4b1ebe166b2a273a5bd8842c3f56c904b863a346e5ffcd/RESULT_EVIDENCE_SUCCESSOR_NOTE_v2.md#evidence-and-receiving-boundary) before interpreting a status. At capture, fifteen registered T20 owners and one proposed owner make sixteen ledger rows. The proposed row's absent native evidence count is `null`. The [later result map](../../experiments/orthemology-v5-successors/groups/t20-successor/LATE_RESULT_MAP.json) and [present result-status owner](../provenance/v5-successors/RESULT_STATUS.json) separately establish registration and receiving `CANDIDATE`/`NOT_RUN`/count `0`. Original author and reviewer checks remain affirmative within the chosen interpretation, while the documentary assembler and this curation add no scientific execution. Do not repin the present registry to the companion's historical snapshot hash.

In `OTC-X01`, inspect actor, exact span, return versus first-reading status and receipt time. The later Dar volume 10 first reading and retained image/electronic returns do not change the [earlier Arabic audit's scope](PAPER-CATALOGUE.md#arabic-reading-methodology-and-source-formal-feedback), create another historical witness or prove every development step's order. The [source-binding companion](../../experiments/orthemology-v5-successors/source-store/30019626dd1d708c0ce1e77d27311e640354e7fb983badd78d52f7cb1de614e6/SOURCE_BINDINGS_v2.json) distinguishes 23 input bindings from nineteen distinct included paths and two omitted bodies; the related review cannot replace either omitted original input. The [documentary validation](../../experiments/orthemology-v5-successors/source-store/1ffc2e72f4e4ec8b8c1b7cef9e095d11320012c69ec32bf07487511d09e3c11c/VALIDATION_v2.json) and [original context selection](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json) distinguish exact narrative and derived JSON public identities from original hashes. Keep the [later historical application qualification](PAPER-CATALOGUE.md#divine-action-source-audits-and-the-stronger-activity-premise) visible alongside this dated representation-control evidence.

### Checking the mathematical companion and its document QA

Begin with the companion's [source-evidence instructions](../../experiments/orthemology-v5-successors/source-store/40e374a62246636ffdbd424f517094dbaa7a7d00cc177675bed19377598e44fd/MATHEMATICAL_COMPANION.md#finding-the-source-evidence), then use its [catalogue dependency map](PAPER-CATALOGUE.md#the-twentieth-mathematical-companion-and-its-original-result-owners) to reach the original arguments and separately scoped proof/review records. The original result owners retain affirmative evidence even though this explanation performed no new scientific replay. A conditional theorem, a finite interpretation and an actual-world application have different premises and evidence obligations.

Use the [QA record](../../experiments/orthemology-v5-successors/source-store/8e49d169249dae0a00b2afd508e9bc4cfafb76666aa12eac5cc9a3e43bc25d38/MATHEMATICAL_COMPANION_QA.json) for the recorded document checks, the [equation map](../../experiments/orthemology-v5-successors/source-store/4c25dc60be8cb39a8413ffea9f1d3e5bf8a5b33b5e3164c712e8eaae303328e6/MATHEMATICAL_COMPANION_EQUATIONS.json) for equation/code correspondence, and the [derivation record](../../experiments/orthemology-v5-successors/source-store/c7faa0a3263c0ae634c0fb1cf313ce9bc2fe7d66b09e8cd8f9ca079b2485237b/MATHEMATICAL_COMPANION_DERIVATION.json) for selected input identities and notation/heading transformations. QA's `scientific_replay: false`, Word UI `NOT_RUN`, omitted image bodies and historical-draft currentness remain binding limits. A page hash or the owner-only Word document's identity is not a public reading edition. The [context index](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json) distinguishes the exact Markdown from the three derived public JSON bodies; use their public hashes for these retained bytes.

Read the [dated appraisal notice](../../experiments/orthemology-v5-successors/source-store/40e374a62246636ffdbd424f517094dbaa7a7d00cc177675bed19377598e44fd/MATHEMATICAL_COMPANION.md#appraisal-distinction-on-7-october-2026) before treating an old judgement as current. The companion does not supersede later source-informed assessment. The catalogue's scalar-fusion and root-cut examples provide concrete assumption/counterexample tasks: require the original argument, explain the missing premise or failed shortcut, and retain the unresolved claim. Mechanical routes and document QA do not establish reader comprehension or C05 acceptance.

### Checking the final report source readback and document QA

Begin with the [original report's repository/evidence boundary](../../experiments/orthemology-v5-successors/source-store/c8611b26ae09858c157059c1ed83690a586c98da5ac5a6aae8412ede077661cd/REPORT.md#repository-and-evidence-boundary) and [dated research account](PAPER-CATALOGUE.md#the-twentieth-final-report-and-its-dated-research-assessment). Original research execution, receiving native execution, source-correspondence review, document fidelity and owner adoption are separate claims. The report's 261-result/3,539-source baseline precedes the final reading/report addendum; its dated local PDF limitation does not describe every later verified environment. Use the exact candidate's actual checks and current result owners.

The [source-readback scope](../../experiments/orthemology-v5-successors/source-store/ce69a2ea0642ea26272d0d3635af5a880f801e4b82e1859ed9aa8813d14e4871/REPORT_FINAL_SOURCE_READBACK.md#scope-of-acceptance) accepts correspondence of the exact report to inspected records, not independent philosophical endorsement. The [receipt](../../experiments/orthemology-v5-successors/source-store/504d161da15f395acffa4d3f1fef9c97a71142e212abd2b17f94815fe07fccb4/REPORT_FINAL_SOURCE_READBACK.json) preserves 108 unchanged prior bindings, eleven selected-alias inputs and three omitted original bodies, with scientific replay and source changes both false. The author-reported [QA manifest](../../experiments/orthemology-v5-successors/source-store/f9bde6e87cc539dde1205572bd1117428c004489309af5d1ec7c82e7e8ad3bde/REPORT_QA_MANIFEST.json) separately records document content and eleven-page rendering checks. Its image/content-QA/build bodies and owner-only Word edition are unavailable in the public selection; `science_rerun` is false. The original readback receipt and its derived public projection have different hashes and byte counts.

The [original context index](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json) binds the two exact Markdown bodies and two derived JSON bodies. Its later REPORT_v2 and document-QA selections have a [separate successor-edition check](#checking-report-v2-and-shared-successor-source-readback); their source and execution scopes remain distinct from this original four-source route. The [prepared independent-reader tasks](#independent-reader-comprehension-tasks-for-the-final-candidate) provide a separate assessment protocol. For this report, a reviewer can additionally test whether a reader rejects “source-readback PASS endorses the philosophy”, “261/3,539 is the final current total”, or adding the overlapping Safadiyya scan categories into a unique-page count. No such independent assessment is claimed here.

### Checking report v2 and shared successor source readback

Begin with the [expanded report account](PAPER-CATALOGUE.md#the-expanded-report-v2-and-its-separately-owned-additions), [original REPORT.md](../../experiments/orthemology-v5-successors/source-store/c8611b26ae09858c157059c1ed83690a586c98da5ac5a6aae8412ede077661cd/REPORT.md), [REPORT_v2.md](../../experiments/orthemology-v5-successors/source-store/067a2a085e8c4a5ec837c8d17869ade90618b8b5a4d20b562a3e3c32f6e5605e/REPORT_v2.md) and the [original context index](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json). One synthesis has two reading editions. The original report remains its primary source; the expanded text gains no independent result identity. Compare the actual text before consulting a PASS receipt: v2 replaces original line 11, inserts lines 80–93 and 205–240 in v2, and preserves the other 41,018 original bytes. Its entire philosophical-assessment section is unchanged.

The [shared readback narrative](../../experiments/orthemology-v5-successors/source-store/7b49b13c05f553ae1cd48ff630146a1d19281dd9099a7701547894b48a74020a/REPORT_GUIDE_V2_READBACK.md) and [JSON receipt](../../experiments/orthemology-v5-successors/source-store/f08aceaf869f487af3c8859cafc66c86b3653bf48454ca1fc0eda7a62e374350/REPORT_GUIDE_V2_READBACK.json), dated **16:34:51 UTC on 7 October 2026**, accept those source changes and evidence correspondences for document authoring. They record zero retrospective reading/science credit, distinguish eight study groups from counts of individual bodies, and preserve the original fifteen-result objects while separately identifying the proposed late control. They contain twenty source bindings: eighteen included public projections and two omitted historical bodies, REVIEW.md and METHODOLOGY_CORE_SEAL_v1.json. The finalisation receipt is separately identified but also omitted. `proofs_replayed_by_this_reviewer: false` and `scientific_sources_changed_by_this_reviewer: false` govern the readback. The guide identities in that joint record are documentary evidence; complete guide-body curation has its own scope.

| Record | Public identity | Original identity or availability distinction |
|---|---|---|
| REPORT_v2.md | Exact 53,358-byte body, SHA-256 `067a2a085e8c4a5ec837c8d17869ade90618b8b5a4d20b562a3e3c32f6e5605e` | Original and public identities agree; retained draft and final identities also agree in the readback. |
| Shared readback narrative | Exact 3,925-byte body, SHA-256 `7b49b13c05f553ae1cd48ff630146a1d19281dd9099a7701547894b48a74020a` | Source review, not a document-render or scientific-replay receipt. |
| Shared readback JSON | Derived 17,333-byte public body, SHA-256 `f08aceaf869f487af3c8859cafc66c86b3653bf48454ca1fc0eda7a62e374350` | Original 6,967-byte receipt has SHA-256 `4c25f7bea815e6bb09c5c98c942ba7e1132feec1d98b918b476277d887c30d2e`. |
| [Report v2 QA](../../experiments/orthemology-v5-successors/source-store/bd454e0e54267bca72091f721fa77bbe5128ebcacb4e8e051ccbe7ba7298e6da/REPORT_v2_QA_MANIFEST.json) | Derived 10,194-byte public body, SHA-256 `bd454e0e54267bca72091f721fa77bbe5128ebcacb4e8e051ccbe7ba7298e6da` | Original QA record has SHA-256 `79afb007eedb543c412e82561de503c7007f92defc0962cccfc3238d649f3b00`; do not substitute one identity for the other. |

The QA at **16:39:49 UTC** reports 140 authored records, twelve native numbered items, nine exact relative labels/paths and fourteen pages, each 1547 × 2002 pixels, with author-reported original-resolution inspections. All fourteen images are absent here, as are the separate content-QA and build bodies. Its 57,198-byte Word output, SHA-256 `7b10f4433974c08971f892d8ab7781aaae561e9b52b8e5b5c050feff2fc36f2f`, is owner-archive-only. Archive inclusion is not public availability. `source_edits: false` and `science_runs: false` concern the QA stage; they do not deny the earlier edition changes or supply a proof replay. Neither the public projection's attribution nor this reader curation constitutes another render or visual inspection.

**Public evidence bridge.** All nine literal links inside the exact report are relative to its original owner archive. None resolves relative to the retained public report directory. The original index supplies the following exact selected destinations; the reader layer supplies these routes without altering scientific bytes.

| Report's literal destination | Selected public body | What it lets the reader inspect |
|---|---|---|
| `../ontology-type-control/AUDIT.md` | [Typed-control audit](../../experiments/orthemology-v5-successors/source-store/e9e55a70a8a84323d76514f095227067a7b962f6c718daa6e75ce2b4dbf83e05/AUDIT.md) | The original model's intended type distinctions, assumptions and limits. |
| `../ontology-type-control/OriginationTypeControl.lean` | [Original Lean module](../../experiments/orthemology-v5-successors/source-store/e3e5480db5b874448b7f4448ce6bce66e426995afbcb45e31ce61f755e03fdfe/OriginationTypeControl.lean) | The actual declarations; nine author theorems and seven selected readbacks are different counts. |
| `../ontology-type-control/DEFINITION_BINDINGS.json` | [Definition bindings](../../experiments/orthemology-v5-successors/source-store/171f38cd4bb5fc3c44cde69be7c3a04718322db771ec27b3a66d897d829ae7e3/DEFINITION_BINDINGS.json) | Declared interpretation inputs and the scope of represented predicates. |
| `../ontology-type-control/SOURCE_BINDINGS.json` | [Ontology source bindings](../../experiments/orthemology-v5-successors/source-store/fd3f503d6f1dd9ce5b164300154c9b4cc4cd477ed026804ff754338452815bd6/SOURCE_BINDINGS.json) | The separately dated contextual reading and original/public source identities. |
| `../methodology/arabic/ARABIC_READING_METHOD.json` | [Arabic reading method](../../experiments/orthemology-v5-successors/source-store/f7171879244b4660b547bcb75bb3b1c5007c570cc4403050636452744535ff04/ARABIC_READING_METHOD.json) | First reading, returns, reflection and bounded received bodies. |
| `../methodology/arabic/CROSS_STREAM_CASES.json` | [Source/formal cases](../../experiments/orthemology-v5-successors/source-store/a9bbeb51d33e7e60c82a8228582502e6e40aabc559f95b77fdac3e9826d98597/CROSS_STREAM_CASES.json) | Historical source-guided design versus later contextual testing or retrospective alignment. |
| `../methodology/drive/DRIVE_CORPUS.json` | [Supplied Drive corpus audit](../../experiments/orthemology-v5-successors/source-store/6d020b39ac31311ec388678c79dd342ea6b5ee6144e1565e37b16a8d66d11761/DRIVE_CORPUS.json) | Overlap, custody and inherited reading versus Twentieth returns. |
| `../methodology/math/MATH_UTILISATION.json` | [Mathematical utilisation ledger](../../experiments/orthemology-v5-successors/source-store/d0e73b80d86fd9367c434e7711cb1bb40d5e0f61821db03392b5cd2590b61ff5/MATH_UTILISATION.json) | Screening, actual body reading, formal inspection, execution and unperformed transfer. |
| `../methodology/result-ledger/RESULT_EVIDENCE_LEDGER_v2.json` | [Later result-evidence ledger](../../experiments/orthemology-v5-successors/source-store/6b1e3b7a3ce32842eda6deada3c5bad3ef740215dba77b2f7750d0de51ba333b/RESULT_EVIDENCE_LEDGER_v2.json) | Unchanged fifteen-owner baseline plus separately proposed late owner at capture, not automatic native admission. |

Follow the [existing emergence owner](PAPER-CATALOGUE.md#typed-emergence-fresh-acts-created-effects-and-a-stipulated-activity-gap) and [late handoff](PAPER-CATALOGUE.md#late-evidence-handoff-for-the-typed-emergence-control) for original scientific evidence and later qualifications. A source reviewer checking twenty-six bound author/reviewer files did not perform twenty-six new scientific executions. Seven additional review probes are not seven new source-level author theorems. Documentary acceptance does not establish actual necessary-object uniqueness, metaphysical possibility or complete agency semantics. Likewise, the unchanged historical 261/3,539 totals and receiving NOT_RUN fields do not decide a later candidate's current status. Use the [native result-status owner](../provenance/v5-successors/RESULT_STATUS.json) and that candidate's own admission and execution records: the registered emergence control retains receiving CANDIDATE, fresh evidence NOT_RUN and independent evidence count zero.

The existing [independent-reader task protocol](#independent-reader-comprehension-tasks-for-the-final-candidate) is unchanged. Its actual executions and source-based adjudication are recorded in the [current reader qualification][qualification]. Edition, identity and route checks prepare inspectable evidence; reader comprehension requires the separately recorded answers and review.

### Checking the source guide editions and reading boundaries

Begin with the [guide account](PAPER-CATALOGUE.md#the-twentieth-source-guide-and-its-expanded-reading-edition), [original GUIDE.md](../../experiments/orthemology-v5-successors/source-store/7b728e2675cfb232ef160c730babee3f13c844a9b3e09ceabb471d579c975bd4/GUIDE.md), [GUIDE_v2.md](../../experiments/orthemology-v5-successors/source-store/c966158d0c2f2e2dc8007c1de9abbce0587a04cfd918fe1c9284508dbeeff6ee/GUIDE_v2.md) and [original context index](../../experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json). The original guide is one supporting reference with two retained reading forms and no result IDs. Its existing support under the cooperation assessment remains; adding a guide edition does not give the guide original ownership of the studies or their mathematical results.

Compare the actual bytes. Original GUIDE.md has 483 lines and 63,809 bytes. V2 has 499 lines and 68,244 bytes: original line 9's 555-byte paragraph becomes 750 bytes, and new lines 14–29 add 4,240 bytes. All other **63,254 original bytes**, including the complete appraisal, remain identical. The additions explain the methodology/Drive audit and separately dated act/effect control. The guide's 14:34 UTC appraisal on 7 October 2026 is not replaced by the original QA time, 14:49:32, index time, 14:49:59, shared source-review time, 16:34:51, or revised QA time, 16:49:45.

The [shared readback MD](../../experiments/orthemology-v5-successors/source-store/7b49b13c05f553ae1cd48ff630146a1d19281dd9099a7701547894b48a74020a/REPORT_GUIDE_V2_READBACK.md) and [shared JSON](../../experiments/orthemology-v5-successors/source-store/f08aceaf869f487af3c8859cafc66c86b3653bf48454ca1fc0eda7a62e374350/REPORT_GUIDE_V2_READBACK.json) retain their report-support identities. The JSON records zero retrospective methodological reading/science credit, preserved original fifteen-result objects and unchanged 14:34 assessment; `proofs_replayed_by_this_reviewer` and `scientific_sources_changed_by_this_reviewer` are false. It accepts source changes for subsequent document authoring, not DOCX rendering, deployed archive-relative links or native admission. Its reported nine author theorems, seven selected author readbacks, two rejected overclaims, seven reviewer probes and 26 file correspondences are different kinds of evidence.

| Record | Exact selected public identity | Distinction to check |
|---|---|---|
| Original GUIDE.md | 63,809 bytes; `7b728e2675cfb232ef160c730babee3f13c844a9b3e09ceabb471d579c975bd4` | Exact original body; the guide's primary reading form. |
| GUIDE_v2.md | 68,244 bytes; `c966158d0c2f2e2dc8007c1de9abbce0587a04cfd918fe1c9284508dbeeff6ee` | Exact expanded body; reviewed draft/final identities agree. |
| [Guide v2 QA](../../experiments/orthemology-v5-successors/source-store/c86ead4315d1855a717552c0e65aae6c0ffcdccd5852c96cc6416eee2e384be1/GUIDE_v2_QA_MANIFEST.json) | 14,597 bytes; `c86ead4315d1855a717552c0e65aae6c0ffcdccd5852c96cc6416eee2e384be1` | Derived projection of original QA `0539b7be389415fdd9ec0afec8aff7fc18be60ae42785fe5225def98122e827a`, 11,284 bytes. |
| Shared source-readback MD | 3,925 bytes; `7b49b13c05f553ae1cd48ff630146a1d19281dd9099a7701547894b48a74020a` | Exact shared review narrative, reused without a duplicate binding. |
| Shared source-readback JSON | 17,333 bytes; `f08aceaf869f487af3c8859cafc66c86b3653bf48454ca1fc0eda7a62e374350` | Original receipt `4c25f7bea815e6bb09c5c98c942ba7e1132feec1d98b918b476277d887c30d2e` has 6,967 bytes; the QA must identify both correctly. |
| [Current-document map](../../experiments/orthemology-v5-successors/source-store/49e7980551767643cf3edf6748b3e9466bb5383465673a40967a60189973f6c6/CURRENT_DOCUMENTS_v2.json) | 12,039 bytes; `49e7980551767643cf3edf6748b3e9466bb5383465673a40967a60189973f6c6` | Derived role map, original identity `eb0e5766ef250178b9c842b12b44c4052317ff02a42d27649ccca6e82b3385d7`. |

The original [guide QA](../../experiments/orthemology-v5-successors/source-store/12c817b64ee139a28e275f0562c8c1ef2d1aa039f1a0a1115b1462f4b4c00f12/GUIDE_QA_MANIFEST.json) and [three-document map](../../experiments/orthemology-v5-successors/source-store/8366c1a9f89d785084debcf8aa32a6b3c2739a43545a705e6fe8681a8e02f3fa/FINAL_DOCUMENTS.json) are predecessor dependencies. V1 QA reports 247 authored records, four literal relative references and eighteen pages; v2 reports 255, eleven and twenty. Both report twenty external links and 62 Arabic codepoints. V2 retains the historical first-render defect: three section openings stranded headings/locators from their explanation. Its author reports adding `keepNext` to 37 locator paragraphs, changing only `word/document.xml`, then individually reinspecting all twenty pages. These are inherited document-fidelity and visual-inspection claims. The page images, initial build, layout-correction body, content-QA, source-finalisation and preservation bodies are omitted; their hashes do not supply access to those bodies. `source_edited: false` concerns the QA stage, without denying earlier edition changes; `scientific_replay: false` supplies no scientific execution.

The current map selects **research report v2 (14 pages), source/reading guide v2 (20), and unchanged mathematical companion v2 (19)**, totalling 53 historical document pages. It retains v1 report and guide and their QA. The five Word identities across current/historical roles are owner-only, even where metadata calls them an `included_record`; they are not public reading forms. `all_current_document_qa_passed: true` is historically attributed. `qa_renders_selected_for_delivery: false` and `scientific_replay: false` prevent treating the role map as delivered render evidence or replay. Compare the [native result-status owner](../provenance/v5-successors/RESULT_STATUS.json) for later receiving disposition and execution; a document called current does not change those records.

**Reading completion has a source-specific denominator.** In the [original reading index](../../experiments/orthemology-v5-successors/source-store/95f8c77ed7ebd217a5108669ad911ee00a5e92d17c7aab641c8f1f10a7ddf998/READING_INDEX.json), `final_scope_summary` distinguishes thirteen source-work entries, eight completed study groups, 42 principal return points, 48 broader return points, 42 witnesses, 200 original evidence records and 132 records with verified public aliases. None is an interchangeable count of independently read volumes. `pending_studies: []` belongs to that historical selected-study snapshot, not to all C03 work. The public projection selects no new primary source bodies and credits zero new primary reading. The original [validation summary](../../experiments/orthemology-v5-successors/source-store/514a96055a7caad51e2dad0944a4e210fa093601c4902039b41d2f6f82fa175f/READING_INDEX_VALIDATION.json) reports author checks and locator/voice review without replay; it is not this executor's complete rereading of the million-byte index or its 200 evidence records.

The present dependency inspection covers the index's top-level identity/status/purpose, historical predecessor, methodological limits, coordinate conventions, appraisal/history, custody/archive/public-alias rules, final scope summary and thirteen work identity/status records. It does not traverse all witnesses, work-body entries or evidence records. Paragraphs, newline positions, page labels and physical PDF positions remain tied to their own witnesses. A received complete original Sawaʿiq can be historically incomplete, a fully read Shifa transcription can lack a verified print edition, and accounting for Jamiʿ scan positions can exceed directly viewed pages. The guide's textual controls and [prepared specialist questions](../../experiments/orthemology-v5-successors/source-store/5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa/SPECIALIST_REVIEW_QUESTIONS.md) remain evidence for examining an interpretation, without asserting that a specialist has answered them.

**Public evidence bridge.** All eleven relative-link occurrences in the exact guide refer to the owner archive; none resolves literally from its hashed public directory. The reading-index link occurs twice. These ten distinct pairs use the original index's exact selections, preserving source bytes.

| Guide's literal destination | Selected public body | Use and boundary |
|---|---|---|
| `READING_INDEX.json` | [Original reading index](../../experiments/orthemology-v5-successors/source-store/95f8c77ed7ebd217a5108669ad911ee00a5e92d17c7aab641c8f1f10a7ddf998/READING_INDEX.json) | Exact witness/coordinate/receipt lookup; a valid route does not claim whole-index curation. |
| `SPECIALIST_REVIEW_QUESTIONS.md` | [Prepared source and philosophical questions](../../experiments/orthemology-v5-successors/source-store/5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa/SPECIALIST_REVIEW_QUESTIONS.md) | Remaining premise and textual questions; no external specialist-review receipt. |
| `../methodology/arabic/ARABIC_READING_METHOD.json` | [Arabic reading methodology](../../experiments/orthemology-v5-successors/source-store/f7171879244b4660b547bcb75bb3b1c5007c570cc4403050636452744535ff04/ARABIC_READING_METHOD.json) | First pass, local return, completed-body reflection and later targeted return. |
| `../methodology/arabic/CROSS_STREAM_CASES.json` | [Source/formal case ledger](../../experiments/orthemology-v5-successors/source-store/a9bbeb51d33e7e60c82a8228582502e6e40aabc559f95b77fdac3e9826d98597/CROSS_STREAM_CASES.json) | Documented design links versus later contextual testing, retrospective alignment and unimplemented targets. |
| `../methodology/drive/DRIVE_CORPUS.json` | [Supplied Drive corpus ledger](../../experiments/orthemology-v5-successors/source-store/6d020b39ac31311ec388678c79dd342ea6b5ee6144e1565e37b16a8d66d11761/DRIVE_CORPUS.json) | Six object identities, inherited/fresh coverage, overlap and custody limits. |
| `../methodology/math/MATH_UTILISATION.json` | [Mathematical utilisation ledger](../../experiments/orthemology-v5-successors/source-store/d0e73b80d86fd9367c434e7711cb1bb40d5e0f61821db03392b5cd2590b61ff5/MATH_UTILISATION.json) | Screening, substantive reading, formal inspection, replay and transfer are separate. |
| `../methodology/result-ledger/RESULT_EVIDENCE_LEDGER_v2.json` | [Successor result-evidence ledger](../../experiments/orthemology-v5-successors/source-store/6b1e3b7a3ce32842eda6deada3c5bad3ef740215dba77b2f7750d0de51ba333b/RESULT_EVIDENCE_LEDGER_v2.json) | Preserved fifteen-owner baseline and proposed late owner at capture; later admission is separately recorded. |
| `../ontology-type-control/AUDIT.md` | [Typed-emergence audit](../../experiments/orthemology-v5-successors/source-store/e9e55a70a8a84323d76514f095227067a7b962f6c718daa6e75ce2b4dbf83e05/AUDIT.md) | Original interpretation control, stipulated inputs and counterexamples. |
| `../ontology-type-control/SOURCE_BINDINGS.json` | [Late ontology source bindings](../../experiments/orthemology-v5-successors/source-store/fd3f503d6f1dd9ce5b164300154c9b4cc4cd477ed026804ff754338452815bd6/SOURCE_BINDINGS.json) | Separately dated Safadiyya/Darʾ8 and Asbahani returns plus bounded first Darʾ10 reading. |
| `assessments/ROOT_CURRENT_APPRAISAL_20261007_143400.md` | [Dated 14:34 assessment](../../experiments/orthemology-v5-successors/source-store/8b60a62d8956549cdd3a0e22f7101b0bbbc140840e49740cdc248e443f43af27/ROOT_CURRENT_APPRAISAL_20261007_143400.md) | Actual common-source provisional acceptance, universal SourceMode withholding and live comparative defeaters. |

For the originating accounts, use [Arabic methodology](PAPER-CATALOGUE.md#arabic-reading-methodology-and-source-formal-feedback), [Drive corpus](PAPER-CATALOGUE.md#six-supplied-drive-inputs-inherited-reading-and-t20-use), [mathematical utilisation](PAPER-CATALOGUE.md#mathematical-reading-local-applications-and-transfer-limits) and the [original fifteen-result handoff](PAPER-CATALOGUE.md#the-original-fifteen-result-evidence-and-method-handoff). The [late handoff](PAPER-CATALOGUE.md#late-evidence-handoff-for-the-typed-emergence-control), [emergence work](PAPER-CATALOGUE.md#typed-emergence-fresh-acts-created-effects-and-a-stipulated-activity-gap) and [later divine-action source audits](PAPER-CATALOGUE.md#divine-action-source-audits-and-the-stronger-activity-premise) preserve separate original formal credit, contextual reading and application limits. The [cooperation assessment](PAPER-CATALOGUE.md#cooperation-complete-efficacy-and-the-later-common-source-reassessment) and [final report](PAPER-CATALOGUE.md#the-twentieth-final-report-and-its-dated-research-assessment) retain their own dated philosophical scope.

#### Checking the original support records

The four original `part: source-guide` support entries 205–208 belong to the existing guide owner. Check each selected public body against the original context index before using its claims:

| Support | Selected public identity | Original record relationship |
|---|---|---|
| [Specialist questions](../../experiments/orthemology-v5-successors/source-store/5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa/SPECIALIST_REVIEW_QUESTIONS.md) | 11,525 bytes; `5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa` | Exact original body, including its dated assessment. |
| [Index validation summary](../../experiments/orthemology-v5-successors/source-store/514a96055a7caad51e2dad0944a4e210fa093601c4902039b41d2f6f82fa175f/READING_INDEX_VALIDATION.json) | 5,398 bytes; `514a96055a7caad51e2dad0944a4e210fa093601c4902039b41d2f6f82fa175f` | Derived, body-free summary; original validation hash `4f86f26fa49fe61ab3c6449edcf7fe1e690775be033c4915278c0653fe0e56b5`. |
| [Original guide QA](../../experiments/orthemology-v5-successors/source-store/12c817b64ee139a28e275f0562c8c1ef2d1aa039f1a0a1115b1462f4b4c00f12/GUIDE_QA_MANIFEST.json) | 11,460 bytes; `12c817b64ee139a28e275f0562c8c1ef2d1aa039f1a0a1115b1462f4b4c00f12` | Original QA hash `d74edbe7b6e743066a8b6b3c2dbaa17eb88e452da6f84a790b92aa3c6c980149`, with omitted original receipt/image bodies. |
| [Historical document map](../../experiments/orthemology-v5-successors/source-store/8366c1a9f89d785084debcf8aa32a6b3c2739a43545a705e6fe8681a8e02f3fa/FINAL_DOCUMENTS.json) | 2,720 bytes; `8366c1a9f89d785084debcf8aa32a6b3c2739a43545a705e6fe8681a8e02f3fa` | Original delivery binding `6c46d354c086740331eb562649cf0b50c0656edc3dd2631a4ec82c0bdffb9335`; not CURRENT_DOCUMENTS_v2. |

**Check a question against its actual argument.** The [causal nonduplication question](../../experiments/orthemology-v5-successors/source-store/5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa/SPECIALIST_REVIEW_QUESTIONS.md#the-scope-of-causal-nonduplication) returns to [original H02](../../experiments/orthemology-v5-successors/source-store/7b728e2675cfb232ef160c730babee3f13c844a9b3e09ceabb471d579c975bd4/GUIDE.md#h02-ability-to-act-alone-and-actual-whole-production); the [necessary-agreement question](../../experiments/orthemology-v5-successors/source-store/5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa/SPECIALIST_REVIEW_QUESTIONS.md#necessary-agreement-and-productive-conditioning) returns to [original M03](../../experiments/orthemology-v5-successors/source-store/7b728e2675cfb232ef160c730babee3f13c844a9b3e09ceabb471d579c975bd4/GUIDE.md#m03-agreement-and-voluntary-particularisation). The [textual-priorities question](../../experiments/orthemology-v5-successors/source-store/5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa/SPECIALIST_REVIEW_QUESTIONS.md#textual-verification-priorities) returns to [original S05](../../experiments/orthemology-v5-successors/source-store/7b728e2675cfb232ef160c730babee3f13c844a9b3e09ceabb471d579c975bd4/GUIDE.md#s05-textual-controls-that-affect-inference). Swapping these destinations preserves a set of links while losing the source relationship. Standing ability is not actual independent whole production; agreement was not overlooked by Minhaj; corrected wording alone does not establish premise warrant. The [dated-position section](../../experiments/orthemology-v5-successors/source-store/5b6e38a335ae31e2fe3082a36313acec9f62a9ebf78c695b61b20cb291f547fa/SPECIALIST_REVIEW_QUESTIONS.md#dated-current-position-and-comparative-defeaters) returns to the [original guide's final judgement](../../experiments/orthemology-v5-successors/source-store/7b728e2675cfb232ef160c730babee3f13c844a9b3e09ceabb471d579c975bd4/GUIDE.md#relation-to-the-final-judgement). The final appraisal's plain archive locator resolves to the already bridged [14:34 appraisal](../../experiments/orthemology-v5-successors/source-store/8b60a62d8956549cdd3a0e22f7101b0bbbc140840e49740cdc248e443f43af27/ROOT_CURRENT_APPRAISAL_20261007_143400.md). Neither its provisional assessment nor the prepared questions is a receipt of external specialist review.

**Keep reported validation at its actual scope.** The validation summary records 6,359 author checks, 392 final consistency checks and separately scoped supplement counters; it provides no basis for summing them into this executor's test count. Its substantive review names D01–D04, M01–M04, S01–S04, H01–H04 and review questions, with H05 widened through exact return points. It records one definite causal-polarity correction and zero additional primary credit. Thirteen work entries, eight completed ordered study groups, 42 witnesses, 200 evidence records and 132 verified public aliases are different denominators. The complete original log, finite source list, predecessor bodies and two separately hashed historical support bodies are omitted. These reported checks neither replay that log nor close the million-byte index's semantic curation.

**Keep original v1 QA distinct from v2 QA.** V1 binds the original 63,809-byte guide and owner-only Word hash `6487a11eccf51ba547f9665a5fb94e0c1173db457cb711381c2abae7dfb76b53`. Its 247 authored records, four relative-link occurrences, 20 external links, 62 Arabic codepoints and 18 pages retain their historical meaning. The four relative occurrences have three distinct targets, already resolved by the public bridge above. The two historical corrections removed a hyphen only from the SF04 heading and kept SF06's locator with its explanation. They must not acquire v2's 37-locator/three-opening history. V1's exact field is `science_rerun: false`; v2 uses `scientific_replay`. All 18 inspection records omit their image bodies. The earlier curator's recorded hash/XML checks and author's page inspections are not new checks performed here.

**Verify each role's own Word/QA pairing.** The historical map selects [report v1](PAPER-CATALOGUE.md#the-twentieth-final-report-and-its-dated-research-assessment), this guide v1 and the unchanged [mathematical companion v2](PAPER-CATALOGUE.md#the-twentieth-mathematical-companion-and-its-original-result-owners). The separate QA records give 11, 18 and 19 pages; the map records their 48-page aggregate. Every `original_qa_record` has `body_included: false` and a distinct included public QA identity. The later current map explicitly retains the original/public v1 map identities, selects revised report/guide roles and totals 53 pages. Neither a swapped QA pairing nor replacement by the later map preserves the historical assertion. Document QA PASS does not establish scientific correctness, public availability of Word/image bodies, new rendering or current research adoption.

This route allows a reader to compare a claim with its actual study, a conditional result with its assumptions, or an open question with the evidence it needs. Mechanical identity/route controls do not observe that comprehension. The existing [five independent-reader tasks](#independent-reader-comprehension-tasks-for-the-final-candidate) and J01–J07/T01–T18 contracts remain unchanged; the [current qualification record][qualification] identifies actual independent task outcomes and their scope. The original support tail is author-curated. [The source-study appraisals](PAPER-CATALOGUE.md#source-studies-and-historically-distinct-appraisals) now provide the substantive collection routes; remaining support objects have explicit collection ownership under the owner amendment, without claiming every-body reading.

### Reading Twentieth source and evidence records

The [live collection guide](../../research/t20-live-20261009/README.md) preserves the checkpoint sequence and supplement. Within a family, a report's revised form, frozen reviewed copy, implementation companion and receipt can have different evidential roles. A result-bound internal review applies to its stated version; it is not external peer review. Checkpoint membership and matching hashes establish a source route, not an additional discovery.

The [v6 guide](../../research/t20-v6-20261012/README.md) points to the [fifteen contribution records](../../research/t20-v6-20261012/research-v6/synthesis/CROSS_CONTRIBUTIONS.json) and the chapter owners. Those owners distinguish ordinary proof, formal source, historical compiler evidence, finite control and source interpretation. In particular, C09's earlier review is bound to earlier prose: the current finite-history statement must be read at its own current hash. The same precision applies to excluded original bodies and reused sources. A later synthesis may accurately reconcile their recorded results without making the unavailable bodies public or supplying a new complete reading of them.

The reader crosswalk records the scope of the present curation. Complete principal-body reading, targeted argument reading, current-claim inspection and owner/index-grounded support disposition are separate levels. Original scientific owners and their exact source/result indexes retain the finer distinctions; no replay or whole-support-body reading follows merely from a new catalogue link.


## Reading AR8R proof and study evidence

For a mathematical claim, start with the source note's typed setting and conclusion. Then use the collection's correction or status owner to determine which evidence applies to that version. The [OSW-15 source-to-formal guide][c03-ar8r-osw] makes the relevant question precise: does the checked formal proposition represent the intended source claim under justified hypothesis, conclusion and object correspondences?

Two AR8R examples make this distinction useful. [Fable's T299 correction][c03-ar8r-fable-correction] records a scoped Lean formalisation and a counterexample to a stronger interpretation of the historical prose. Its factorisation result does not certify the historical packet end to end. The [V14 synthesis Lean file][c03-ar8r-synthesis-lean] contains complete proofs for attained-image factorisation, the off-range decoder guard, coordinatewise guard recovery and joint refinement. Its [receipt][c03-ar8r-synthesis-receipt] records a standalone check with a declared toolchain and axioms. This reader pass inspected that proof source and receipt without rerunning Lean or establishing a project-wide build.

The [exact proposal index][c03-ar8r-deep-index] and [semantic-reissue owners][c03-ar8r-bw] are different routes to a text. Exact snapshots preserve their bytes and histories; a semantic reissue preserves a declared reconstruction without recovering unavailable original wording. The [six-lane corrections][c03-ar8r-six] retain failed originals, separately repaired Lean files, incomplete central replay and finite-check limitations. A corrected receipt governs the claim it names; it does not validate every note in its folder.

For studies, use the [canonical experiment status][c03-experiment-status]. FCSP-2 and ER-2 are prepared public packets without observed results. Terminology Pilot 0 is feasibility-only, and later stages are drafts. The [historical AR8R synthetic pilot][c03-ar8r-pilot] is a separate completed, negative internal study with support-overlapping, non-case-paired evidence. Mock runs, synthetic power inputs and checks of constructed signatures do not create treatment effects or external empirical validation.

The crosswalk records this curation's actual reading scope. Complete owner indexes give direct note navigation; only specified bodies and proof sources were read in detail. Index-based dispositions are not proof-review credit, and the preserved theorem-origin counts do not measure independent discoveries.

[c03-ar8r-bw]: ../project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-bw-cj-semantic-reissue/README.md
[c03-ar8r-deep-index]: ../project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_RESULT_INDEX.yaml
[c03-ar8r-fable-correction]: ../project-closure/ar8r-v11/fable-research/AR8R-FABLE-R1-CORRECTION-RECEIPT-V1.md
[c03-ar8r-osw]: ../project-closure/ar8r-v11/governance/ORTHEMOLOGICAL-SPECIFICATION-WARRANT-OSW-15.md
[c03-ar8r-pilot]: ../project-closure/ar8r-v11/experiments/t299-t300-negative-synthetic-pilot.md
[c03-ar8r-six]: ../project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/README.md
[c03-ar8r-synthesis-lean]: ../project-closure/ar8r-v11/post-merge-proposals/codex-corpus-synthesis-v14/lean/CodexFibreSynthesis.lean
[c03-ar8r-synthesis-receipt]: ../project-closure/ar8r-v11/post-merge-proposals/codex-corpus-synthesis-v14/lean/LEAN_RECEIPT.json
[c03-experiment-status]: ../../experiments/experiment-status.yaml


## Architecture and scholarly reference routes

Several short reference texts help explain the existing works. They belong with those works and subjects; they add no independent paper or research verdict.

| Reader question | Reference and its contribution |
|---|---|
| What does the formal core record? | The [architecture overview](../architecture-overview.md) connects a concrete occurrence, its observation and an inferred profile to the declared analysis and versioned episode. This makes a correct classification of the wrong version a specific, inspectable error. |
| How do the different kinds of claim relate? | The [six-layer map](../architecture/ORTHEMOLOGY-LAYER-MAP.md) separates formal definitions, application extensions, philosophical arguments, school-labeled theology and empirical designs. Its dated labels describe that map; each work’s source owner supplies its research standing. |
| What does the implemented reference contract establish? | [Decision 0012](../decisions/0012-reference-model-semantic-contract.md) explains nonempty constitutive fields, resolvable references, governance-token bindings and separate claim/episode assessments. The reported controls reject specified malformed records within a bundle. They do not establish store-wide consistency or semantic completeness. |
| Why compare a learning trajectory with its endpoint? | The [latent-variable literature note](../related-work/LATENT-STATE-INFERENCE-AND-ORTHEMOLOGY.md) distinguishes observation, hidden state, representation and profile. Its bounded comparison shows how the same endpoint criterion can leave different pathways unresolved; the cited studies supply a neighboring illustration, with no evidential transfer to Orthemology’s ontology or metaphysics. Read it with [the latent-state application](PAPER-CATALOGUE.md#latent-state-learning-and-governed-updates). |
| What does the historical LLM example support? | The [R7E witness](../project-closure/r7e-sol/R7E-LLM-MEDIATED-ORTHING-WITNESS.md) preserves an affirmative role classification and partially supported bounded realizability account. Missing original journals and identity bindings limit reconstruction; this record does not establish a live Somnus deployment. |

For a scholarly attribution, start at the [current sourcing view](../sourcing/CURRENT-SOURCING-LEDGER.md), which names the actual authority for each claim family. Bibliographic identity, directly checked wording, compilation access and an author’s inference are different claims. A valid record or working link does not establish fresh source authentication.

Some historical records also explain consequential choices. The [R2 related-work review](../project-closure/reviews/REVIEW-B-RELATED-WORK.md) concedes inherited facets while preserving the main paper’s occurrence-centered integration proposal and testable utility hypothesis. The [strict-soundness correction](../decisions/0011-claim-relative-reasoning-path-and-strict-soundness.md) separates claim-relevant reasoning from later routing or closure. [Decision 0007](../decisions/0007-profile-space-definition.md) follows the separately deferred profile-space definition and distinguishes a candidate set from one partial profile. These remain source history and reference support of the existing exposition and formal reference; their dated tests and reviews receive no fresh-execution credit here.
