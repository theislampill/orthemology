# R7E Sol Independent Repair and Protected Integration Design

**Date:** 2026-07-21

**Surfaced model:** `gpt-5.6-sol` (Codex task metadata, verified before the first write)

**Repository:** `theislampill/orthemology`

**Review branch:** `review/r7e-sol-independent-repair`

**Exact base:** `candidate/r7e-orthing-supplementation@cbab14747835855d232448f648eefa1d4e36074e`

## Objective

Independently reproduce, adjudicate, and repair every blocking finding against R7E/PR #12 and its cumulative R7 candidate stack; complete publication-grade mathematical-source migration and PDF QA; then, only if every gate passes and no owner-only blocker remains, integrate without history rewriting through PR #12 → #11 → #10 → #9 → #8 → protected `main`, with fresh validation after every step and a final clean-clone verification.

## Current verified topology

The public merged source of truth is protected `main@43fee0f519e2f6984fb143c1e621c83382e71ec7`. The unmerged candidate chain is linear and clean:

1. PR #8: `main` ← `closure/r7-noetic-application-experiment-validity@b0538601913c8234511a1f1131a58eb23a4a0dc4`
2. PR #9: R7 ← `candidate/r7b-deep-noetic-latent-math@86b8bbdddf35ac1e45748279bac05e5a2d4ed85e`
3. PR #10: R7B ← `candidate/r7c-full-math-multitarget-noetic-dynamics@3cce235f0e388ba78a093d43c879a2e73262938b`
4. PR #11: R7C ← `candidate/r7d-final-semantic-math-noetic-integration@e34d2cd56057766f8f656a4ff3486eb34dad607e`
5. PR #12: R7D ← `candidate/r7e-orthing-supplementation@cbab14747835855d232448f648eefa1d4e36074e`

All five PRs were open drafts, mergeable, and green at design time. That state is evidence to refresh, not a timeless fact.

## Approaches considered

### Selected: dedicated cumulative repair branch from R7E

Repair the live cumulative candidate on a new branch based exactly on PR #12's head. Keep review artifacts, semantic contracts, tests, prose, math sources, PDFs, and provenance changes in reviewable commits. Merge the repair branch into PR #12 only after independent whole-branch review, then cascade child-to-parent.

This preserves the exact candidate lineage, keeps every PR identity visible, and avoids editing an Opus candidate branch in place.

### Rejected: repair PR #12 in place

This is mechanically shorter but weakens authorship/provenance separation, makes rollback less legible, and conflicts with the requested dedicated review branch.

### Rejected: restart the repair from `main`

This would be suitable for a new canonical line, but it would require replaying and re-adjudicating 34 cumulative commits before the R7E-specific repair could even be compared. It obscures the supplied audit's actual object: PR #12 and its inherited stack.

## Architecture and phase boundaries

### 1. Reproduction and finding control plane

Create durable Sol review artifacts under `docs/project-closure/r7e-sol/`:

- read-only reproduction with exact environment, topology, Smoke A, and clean-tree evidence;
- finding matrix mapping every audit item to `reproduced`, `refuted`, `partially reproduced`, or `unverified`;
- hunk-by-hunk PR #12 disposition: `keep`, `revise`, `drop`, or `provenance-only`;
- provenance/backlog audit with reconstructibility limits;
- continuously updated state record with next action, checks, commits, and blockers.

Audit claims remain hypotheses until reproduced against live files. Shipped validators prove contract conformance only. The initial Windows console failures are recorded as environment failures: the same validators passed unchanged with Python UTF-8 I/O.

### 2. Candidate state and provenance

Replace the stale handwritten candidate topology with a generated, schema-checked overlay that covers PRs #8–#12. The frozen input record contains exact PR number, branch, base, head, draft/open state, observed CI state, candidate decisions, documents/PDFs, provenance layer, merge order, and observation timestamp. Generation is deterministic and offline; a separately authorized refresh command may query GitHub and rewrite the frozen input.

The validator must reject omitted PRs, placeholders, duplicate PRs, broken parent links, stale required heads, candidate self-promotion, or a merge/signoff claim lacking evidence.

The R7E swarm claims are not independently reproducible from the repository. Unless complete journals and reports are recovered, counts remain attributed implementing-run observations. The backlog becomes a structured ledger with globally unique immutable IDs, exact loci, full proposal/rejection text available in-repo where rights permit, evidence status, reviewer status, and integration disposition. No extension-stripping workaround is permitted.

### 2A. Bounded R7E LLM-mediated orthing witness

Audit the R7E supplementation pass itself against the formal episode architecture without reopening Decisions 0001–0022. A machine-readable or tabular crosswalk records, only where supported, the orthemmata taken up, declared analysis, LLM executor and subagent roles, governing metaortheme types, case-bound metaorthemmata, evidence/source records, candidate findings or profiles, routing decisions, integrated actions, residual backlog, successor repository state, and the later higher-order audit.

The evidential classification keeps three claims separate:

1. **LLM applicability:** an LLM can act as an executor inside an orthing episode.
2. **LLM-mediated realizability:** an externally scaffolded LLM workflow can instantiate substantial parts of the architecture.
3. **Comparative utility or validity:** Orthemology improves correctness, robustness, efficiency, transfer, or coordination over matched ordinary workflows.

R7E may support the first and provide bounded observational evidence for the second. It cannot establish the third because no matched comparison or empirical terminology study was run. It also cannot establish universal correctness, exact internal ontological representation, cross-model or cross-domain generalization, or full swarm reconstructibility.

Every witness field carries an evidence state such as `repository-verified`, `attachment-observed`, `implementing-run-attributed`, `missing`, or `unresolved`. The classification expressly preserves the missing complete workflow journal, absent per-agent reports and full drafts, duplicate backlog identifiers, incomplete rejection records, unresolved source attachments, and unverifiable swarm statistics. If the supported claim survives, publication prose labels it a constructive behavioral witness or observational case, never empirical validation.

### 2B. Waking orthing, somnic assessment, and agentic-runtime boundary

Preserve the governing distinction: **Waking orths experience. Somnus orths the available orthings of experience.** A waking orthing takes up an occurrence at `t1` under the then-recorded analysis, evidence, governing contracts, evaluator versions, and selector versions. A later somnic operation at `t2` takes the preserved orthing, its pathway, residuals, or relations among orthings as its orthemma. Meta-orthability is the retrospective applicability and record-sufficiency gate. Inapplicability, indeterminacy, or insufficient record yields an explicit non-assessment; it never licenses a fabricated verdict.

Historical orthing events are append-only. A later assessment may supersede an earlier assessment by reference but cannot rewrite, normalize, or hindsight-correct the target `t1` record. Keep `session_id`, `episode_id`, `occurrence_id`, `orthing_id`, `somnus_assessment_id`, and `proposal_id` distinct. Reuse and crosswalk the existing episode, evidence, route, residual, verdict, analysis, metaortheme, and metaorthemma owners before adding fields. Incremental events retain identity, time, executor, capture mode, source revision, and governing versions; a materialized view never replaces event history.

The minimal crosswalkable event vocabulary is `occurrence_apprehended`, `orthability_assessed`, `candidate_set_recorded`, `route_selected`, `placement_committed`, `residual_recorded`, `orthing_closed`, `orthing_abandoned`, `orthing_reopened`, `somnus_assessment_emitted`, and `proposal_emitted`. Capture is incremental and never assumes a clean session close or complete final context.

Evidence records distinguish evidence observed at `t1`, used at `t1`, presented or indexed but unused at `t1`, and discovered after `t1`. Later evidence may support retrospective assessment but cannot be inserted into the historical evidence state. Every reconstructed R7E record declares `live_capture`, `retrospective_reconstruction`, `bootstrap_provenance`, or `unknown`; the R7E case is retrospective reconstruction, never relabeled as live capture.

Activation contracts are versioned governing artifacts, not executable skills or keyword triggers. They declare claimant/version, required properties, positive and exclusion indicators, boundary counterexamples, tolerated ambiguity, plural fallbacks plus no-claim, decision and indeterminate policies, fixture suite, effective revision, supersession, and authoring provenance. Indicators are evidence about a boundary, not the boundary itself. The orthability evaluator remains separately identified and versioned. Results are tri-state `applicable`, `inapplicable`, or `indeterminate`, with satisfied, absent, and indeterminate properties separated from observed indicators and exclusions. Accepted contract versions require recorded positive, negative near-boundary, indeterminate, and overlap fixture outcomes. Contract authorship is itself an orthing; the initial artifact may use explicit bootstrap provenance, while later versions require an authoring `orthing_id`.

Somnic meta-orthability distinguishes assessable, inapplicable, indeterminate, and record-insufficient cases using existing verdict/status vocabulary where possible. It keeps historical reasonableness under the `t1` state distinct from the placement a present system would make now; counterfactual replay is deferred. Its frontier contains newly unassessed orthings or prior assessments explicitly reopened by a material delta. Versioned operation, selection rule or watermark, governing versions, material-delta references, and an idempotency key make a repeated unchanged run a no-op or byte-equivalent result.

The only v0 fixture-demonstrated operation is residual recurrence assessment. Controlled fingerprints retain residual type, affected boundary, locus, failure or uncertainty class, normalized object, route stage, raw text, and source orthing IDs. A configurable threshold such as three distinct orthings or episodes is a review trigger, not proof of systemic defect. Reports include dependence, counterexamples or opportunity denominator where supported, suspected locus, confidence, candidate investigation class, and unresolved questions. V0 cannot patch a skill or contract, promote a metaortheme, close a finding, authorize irreversible action, or mutate governance.

Conflicted provisional placement records retain alternatives, selector/version, reason, confidence effect, unresolved status, and a separate authorization rule. Placement does not authorize mutation. The repository may land runtime-neutral schemas, fixtures, validators, a deterministic direct reference operation only under an existing execution owner, the reconstructed R7E case, and outline-only downstream application candidates. It does not create or install skills, private prompts, host configuration, a live ledger emitter, scheduler, daemon, nightly workflow, replay engine, autonomous learner, or self-patching loop. Candidate outlines cover orthability checking, append-only ledgering, separate live residual recording and later recurrence assessment, conflict handling, verdict-aware patch proposals, and a somnus orchestrator, all marked unimplemented and externally owned.

### 3. Semantic operator and DAEE boundary

Retain `c86b3c6673147b8802fe222373a165a37d4d24a8` as both the historical pin and the currently observed public DAEE `main` commit. The independent audit's “new current commit” premise is refuted; its deeper-crosswalk concern remains live because the prior reading of that same commit is incomplete.

Add one typed operator contract for route pressure, event transition, field divergence, field curl, loop break, whole-state reread, and runtime closure. Each entry records input/output type, target field, preconditions, semantic kind, source status, non-claims, correctness relation, and pathway-adequacy relation.

Keep these predicates distinct:

- `AdmissibleCorrectiveTransition`
- `LocallyImprovingTransition`
- `TransitionPathwayAdequate`
- `ClaimRelevantReasoningPathAdequate`
- factive, claim-relative `StrictlySoundReasoning_q`

IR is not ground truth; a field witness is not the world; owner activation is not automatically a metaorthemma; plain route pressure is not a differential gradient; `Delta` is not correctness; runtime closure is not uptake, guidance, or soul access.

### 4. OSM, epistemology, and meta-noetic memetics

OSM means the reported task-specific CA1 **orthogonalized state machine** representation. It is a bounded computational/neuroscientific analogy, not validation of Orthemology or theology. Preserve the object firewall from world/task state through observation, biological response, population representation, CSCG clone, latent posterior, parameter state, representation geometry, inferred profile, and actual profile.

Correct methods precisely: Baum–Welch is expectation-maximization likelihood estimation; Viterbi is decoding/refinement; BPTT computes gradients; Adam is a gradient-based optimizer used with the reported loss. Replace general convergence claims with reported progressive adaptation and representational differentiation.

Source status is explicit: primary-text verified, secondary reconstruction, cross-source synthesis, orthemological extension, computational analogy, and creed-internal inference.

Fiṭrah is modeled only as a qualitative, defeasible, multidimensional normative disposition/proper-function orientation in the school-internal reconstruction. It is not a measurable scalar, one field coordinate, one metaortheme, one algorithm, a discourse-readable soul state, or a guaranteed attractor. “Proper-function warrant” is marked as a modern comparative reconstruction unless separately sourced.

Tawātur is not count, popularity, graph degree, or institutional stability. The warrant record separates source-dependence detection, independence support, and creed-internal warrant, and includes origin, actual source units, copying/common cause, path independence/non-collusion, transmitter quality/competence, circumstantial indicants, coherence, mutation lineage, defeaters, subject-relative conditions, assessor evidence, and conclusion.

Mental analytic representation is typed separately from external existence. Conceivability, universal abstraction, or model representation cannot entail external existence, external possibility, or unseen modality.

Meta-noetic ecology keeps type, represented standard, carrier relation, case-bound metaorthemma, execution, transition, response artifact, later uptake, and slow repertoire/analysis revision separate. One episode cannot silently revise a global standard.

### 5. Terminology, companion, argument map, and divine Speech

The terminology account says the coined forms are **constructed but morphologically grounded**. `orth-` and English `-eme` are established; `-emma` is not presented as an inherited productive English token suffix. Greek `-ma/-mat-` may motivate result/object/instance morphology. Greek `ema` may appear only as deliberately superposed possessive resonance, not as the derivation of `-ma`. Cross-domain usefulness remains a benchmark-gated mnemonic/meta-schema hypothesis, not universal primitives or proven isomorphism.

The dynamic companion and argument map are expanded together. Counts and identifiers are generated from the map. Each rung carries premises, inference type, conclusion, dependencies, source/evidence status, strongest objection, rival exit, scope, and school-neutral versus Atharī-internal status. Empirical learnability does not yield normativity without an explicit, separately defended bridge. Personal attributes cannot be assumed in the premise that purports to establish them.

The Atharī divine-Speech route remains explicit and source-bounded. It distinguishes created human convention; created creaturely speaking, reciting, and writing; created voice, ink, page, and media; Allah's act of speaking; revealed Arabic wording as Allah's Speech; and creaturely hearing/reception. Capacity for disclosure is not actual divine Speech. No OSM or DAEE result supplies this route.

### 6. Mathematical source and PDF publication pipeline

Split `glyph_defect_repaired` from `full_math_source_migrated`. Inventory every publication-facing backtick span as literal code, semantic registry identifier, or mathematics. Migrate mathematical spans through reviewed source transformations, not global replacement.

Cover the main manuscript, formal core, multi-actor note, school-neutral companion, Atharī companion, dynamic companion, and notation gallery. Use typed, collision-free notation; upright semantic operators/IDs; explicit ASCII/accessibility prose; tables and multiline displays that preserve citations and links.

Publication gates require:

- `full_math_source_migrated: true` for every publication paper;
- `expected_notdef: 0`;
- zero unapproved formula-like backticks;
- exact tool/dependency hashes;
- two byte-identical builds;
- extracted-text structure checks;
- rendered page images for every PDF;
- human/model visual inspection of every page, with special attention to formula-heavy pages, overflow, blank pages, glyphs, tables, links, and headings.

### 7. Adversarial review and clean-clone proof

Every implementation task follows test-first red/green/refactor when behavior or validation changes. Required mutations cover stale/omitted candidate topology, candidate self-promotion, literal physical gradient, divergence/curl without a multi-node field, transition-as-correctness, omitted reread, closure-as-uptake, hidden-burden deletion, unauthorized global revision, strict soundness on mere admissibility, tawātur-by-count/popularity, fiṭrah-as-coordinate, mental-to-external entailment, argument-map status contradictions, unsafe created-wording implications, and unapproved formula spans.

Fresh independent agents review each task for specification compliance and quality, then a final Sol reviewer audits the whole branch. Agent reports never replace local diff inspection or fresh tests.

After the full pinned suite passes, clone the repaired branch into a new directory, reinstall only from the exact lock, rerun the complete suite, double-build PDFs, render pages, and verify a clean tree.

### 8. Protected integration

Integration is conditional and serial:

1. review branch → PR #12 branch;
2. PR #12 → PR #11 branch;
3. PR #11 → PR #10 branch;
4. PR #10 → PR #9 branch;
5. PR #9 → PR #8 branch;
6. PR #8 → protected `main`.

Before each merge, refresh model identity, exact heads/bases, mergeability, required checks, and clean local state. Use ordinary merge commits or GitHub's protected merge behavior; never force-push, rewrite, or squash away provenance. Rerun required CI after every integration and stop the line on any red, stale head, unexpected commit, or semantic regression.

After the final merge, fresh-clone `main`, rerun the full pinned suite and PDF build/visual checks, and create a non-self-referential merged verification record through a protected follow-up PR if the final merge SHA could not be known beforehand.

## Non-scope and hard prohibitions

- no empirical experiment, live provider/model call, terminology study, or blind human matching review;
- no terminology adoption;
- no reopening of Decisions 0001–0022 for the R7E witness classification;
- no executable agent skill, `SKILL.md` package, private prompt, machine-local agent configuration, or external skill-registry mutation;
- no scheduled workflow, cron, daemon, live ledger emitter, autonomous nightly somnus process, or self-patching loop;
- no retrospective mutation of a historical orthing or silent insertion of later evidence into its `t1` state;
- no DAEE repository mutation;
- no inference of soul state, guidance, persuasion, or theology from runtime traces;
- no biological-procedure reconstruction;
- no external registration, peer-review claim, preprint, DOI, author identity, license, or other legal/publication status fabrication;
- no force-push, history rewrite, destructive cleanup, or provenance collapse;
- no publication of private transcripts, journals, session identifiers, or rights-sensitive material.

## Stop conditions

Stop before the next write or merge, preserve the exact state, and leave affected PRs unmerged if:

- task metadata no longer reports `gpt-5.6-sol`;
- an audit blocker requires a genuine owner-only decision;
- a required source cannot be verified and weakening/removing the claim would materially change an owner-approved thesis;
- any mandatory semantic attack survives;
- the full math, PDF, clean-tree, pinned-suite, or clean-clone gate is red;
- branch topology, mergeability, or protection differs materially from the verified chain;
- an unexpected external commit makes the planned merge unsafe.

## Done when

Every independent finding and PR #12 hunk has a durable evidence-backed disposition; all blockers are repaired or refuted; the semantic contracts and attacks prevent the known false passes; the scholarship boundaries are explicit; the R7E episode has a provenance-qualified LLM-witness and retrospective somnic-case classification that cannot imply comparative utility or deployed runtime; the repository preserves the two-time append-only rule, versioned activation/evaluator separation, tri-state applicability, deterministic residual-recurrence fixtures, and outline-only downstream ownership; all publication sources are fully math-migrated; every PDF passes byte, text, glyph, and visual checks; the repaired branch passes the exact pinned suite from a clean clone; every authorized integration step passes refreshed CI; protected `main` passes the same clean-clone verification; and the final record states exactly what was verified, what remains owner/external, and what was not claimed.
