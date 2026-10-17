# Orthemology

Orthemology is a proposed theory of how concrete cases get correctly classified, handled, and audited by rule-governed processes — human, institutional, or automated. It gives first-class, auditable structure to a familiar but usually implicit architecture:

| Term (candidate) | Ordinary-language meaning | Pillar example |
|---|---|---|
| **orthemma** | the concrete situated case, with an identity key and version | this particular pillar, as it now stands |
| **ortheme** | a repeatable, consequence-bearing state-type the case may instantiate | *orthogonal to a declared reference plane within tolerance ε* |
| **metaortheme** | a repeatable higher-order governing standard or configuration | the standard fixing which reference frame, tolerance, instruments, calibration, evidence, and validation count |
| **metaorthemma** | the concrete, case-bound configuration token of that standard | *this* standard bound to *this* plane, tolerance, instrument, and calibration, for this pillar, now |
| **orthing** | the whole rule-governed handling process | identifying the pillar, applying the bound standard, gathering evidence, placing, validating, routing, closing |
| **orthing episode** | one dated, concrete run of that process (may contain several metaorthemmata) | the record of today's check on this pillar |

The final assertion ("this pillar is orthogonal") is a **placement claim** judged for correctness; the ortheme is the state-type itself.

**Status: research-stage draft (R6); not peer reviewed; fresh-session repository review completed; not external human peer review; not empirically validated. Coined terminology is benchmark-gated, not adopted. See [STATUS.md](STATUS.md).**

## Two ideas that carry the theory

**Result correctness is not pathway adequacy.** An episode's result can be right while the process that produced it was defective (the stopped-clock validator; the wrongly-calibrated check that happens to agree), and a genuinely reliable, correctly-run process can still miss a rare case. The verdict layer keeps these axes independent: V1 judges the placed result; a **result-free pathway core** (evidential support, configured-procedure truth-conduciveness, evidence currentness, rule/policy/token/execution adequacy, decision-time justification, route safety, closure truthfulness, robustness) judges the process. All four result × pathway combinations are representable, with deterministic fixtures proving it.

**Ground truth is analysis-relative.** Which state-types a case *truly* instantiates is defined relative to a declared, versioned **analysis** `A` (boundary, task, repertoires, loss, tolerance, representation and merger families): `O*(m; A)`. The familiar task-relative notation (`O*_T(m)`) survives only as explicitly scoped shorthand once a single analysis is fixed — it is an abbreviation, not a second ontology. The case itself and its worldly facts are not created by the analysis; only the state-type description is indexed.

## What to read

Choose a question or work first; the original arguments remain at their existing source owners.

**Research atlas:** [questions, recognition, correction and the twelve avenues](docs/reader/RESEARCH-ATLAS.md).

**Work catalogue:** [manuscripts, mathematical works, sources, components and editions](docs/reader/PAPER-CATALOGUE.md).

**Result index:** [particular statements, assumptions and evidence](docs/reader/RESULT-INDEX.md).

**Current frontiers:** [live questions, conditional bridges and useful continuations](docs/reader/CURRENT-FRONTIERS.md).

**Applications:** [substantive applications and cross-avenue contributions](docs/reader/APPLICATIONS.md).

**Verification guide:** [source ownership, proof scope, runnable checks and maintenance](docs/reader/VERIFICATION-GUIDE.md).

For sustained reading, start with the [main exposition](manuscript/orthemma-ortheme-systems-revised-draft.md), then the [formal reference and its two components](docs/reader/PAPER-CATALOGUE.md#formal-reference). The main manuscript is not a summary of every later research collection. The atlas also gives positive source-bound accounts of [recognition and corrective cognition](docs/reader/RESEARCH-ATLAS.md#recognition-sound-cognition-and-correction) and [tensor histories and information geometry](docs/reader/RESEARCH-ATLAS.md#tensor-histories-and-information-geometry); the applications page explains [joint feasibility across avenues](docs/reader/APPLICATIONS.md#joint-feasibility-across-avenues).

**Reader-refactor boundary:** these routes reuse the existing scholarship. Remaining collection dispositions and separate review are tracked in the [implementation record](docs/project-closure/reader-refactor-issue-35/PROGRESS.md); a working link is not a complete-corpus or scientific-acceptance certificate.

## A worked case

A recovered instruction can be genuine, accurately copied and issued by an authorised person, yet no longer govern the present case because it was superseded. The [stale-steer example’s five predicates](examples/compaction-stale-steer.md#3-five-predicates-that-must-not-be-collapsed) distinguish existence, authenticity, recovery, authority and current force. Faithfully following an obsolete instruction can therefore pass execution fidelity while failing the governing-token and evidence-currentness checks. The [actual verdict account and fixture F6](examples/compaction-stale-steer.md#4-how-the-verdict-layer-sees-it) show the distinction; this is an analytic example and deterministic control, not an empirical study.

## Honesty notes
- **No empirical experiment has validated the framework.** The designed public studies stand at their canonical [packet-index](experiments/experiment-status.yaml) states — FCSP-2 and ER-2 `READY_TO_RUN`; FCSP-1 and ER-1 historical `DETERMINISTICALLY_VALIDATED` (superseded); terminology Pilot-0 v2 `READY_FOR_HUMAN_MATCHING_REVIEW`; Pilot 1 and confirmatory templates `DRAFT` — **none of those packets has been run, none externally registered, and no term adopted**. A distinct recovered AR8R record documents an eight-seed internal synthetic T299/T300 pilot with a negative, methodologically bounded result; it is not a public experiment packet or external empirical validation. The deterministic fixtures and validators are **internally conformance-checked over the declared schemas, examples, fixtures, and adversarial operators** — never a mathematical consistency proof. The private source records are not published; the public custody summary supports only its explicit negative disposition.
- **The coined vocabulary (orthemma/ortheme/metaortheme/metaorthemma/orthing) is candidate terminology**, gated on a designed-but-unrun comparative benchmark; every document can be read with ordinary-language substitutes.
- **The companion theological/metaphysical papers are complete drafts, deliberately separated** from the main manuscript: philosophical conclusions are conditional on labeled premises, creed-internal material is explicitly Atharī-school-labeled, and no engineering evidence supports any metaphysical claim (absolute firewall).
- **Related-work claims are cited with per-claim verification statuses** — current state starts at [`docs/sourcing/CURRENT-SOURCING-LEDGER.md`](docs/sourcing/CURRENT-SOURCING-LEDGER.md) (Decision 0019; R2 ledgers are banners-marked historical baselines); statuses are honest about what was and was not re-fetched.
- **Historical candidate overlay and current integration evidence (R7E Sol review, Decisions 0034–0036).** The authoritative [`docs/current-candidate-state.yaml`](docs/current-candidate-state.yaml) and timestamped [`CANDIDATE-TOPOLOGY-INPUT.yaml`](docs/project-closure/r7e-sol/CANDIDATE-TOPOLOGY-INPUT.yaml) preserve the exact pre-integration branch/base/`head_at_observation`/draft/CI/provenance facts observed at `2026-07-21T18:10:22Z`; they are historical candidate-era evidence, not timeless live-head claims. The reviewed lineage subsequently reached protected `main` through ordinary PR #13 → #12 → #11 → #10 → #9 → #8 merges at `8db1630ab715b0931907c627be97b32399d6f4fc`, with exact-SHA CI and fresh-main proof recorded in [`R7E-SOL-MERGED-MAIN-VERIFICATION.md`](docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md). Git integration does not establish empirical validation, external peer review, terminology adoption, publication, or approval of interrupted research.

## Citing

No stable release, DOI, or citation metadata exists (license and identity decisions are owner-only — see [OPEN-DECISIONS.md](OPEN-DECISIONS.md)). Cite by commit per [docs/CITING.md](docs/CITING.md).

## Source owners and repository reference
- **Current main manuscript:** [`manuscript/orthemma-ortheme-systems-revised-draft.md`](manuscript/orthemma-ortheme-systems-revised-draft.md) — the one current draft (*Orthemma–Ortheme Systems: An Analysis-Relative Architecture for Auditable Classification and Handling*); earlier renderings are superseded.
- **Current formal core:** [`theory/orthemic-core-formalization.md`](theory/orthemic-core-formalization.md), with the derived multi-actor extension in [`theory/orthemic-multi-actor-conflict-note.md`](theory/orthemic-multi-actor-conflict-note.md).
- **Normative registries:** [`docs/verdict-registry.yaml`](docs/verdict-registry.yaml) (verdict semantic IDs + display aliases) and [`docs/notation-registry.yaml`](docs/notation-registry.yaml) (symbol table) — both machine-enforced.
- **Worked case:** [`examples/compaction-stale-steer.md`](examples/compaction-stale-steer.md) (the stale-directive pattern) plus <!-- state:example-json-count -->nine<!-- /state:example-json-count --> machine-readable episode examples under [`examples/`](examples/) validated against [`schemas/`](schemas/).
- **Companion (metaphysical/theological — complete drafts, separate and firewalled):** [`companion/`](companion/README.md).
- **Terminology program (Pilot-0 v2 `READY_FOR_HUMAN_MATCHING_REVIEW`; Pilot 1 / confirmatory templates `DRAFT`; NOT RUN, no term adopted):** [`terminology/`](terminology/README.md).
- **Decision records:** [`docs/decisions/`](docs/decisions/) — <!-- state:decision-range -->0001–0040<!-- /state:decision-range -->: 0001–0003 (owner reconciliation R1), 0004–0008 (autonomous closure R2), 0009–0010 (type/token, soundness bearers, orthability senses — R3), 0011–0015 (claim-relative reasoning paths, reference-model semantic contract, source-status normalization, generated project state, latent-state boundary — R4), 0016–0017 (review-state contract, private-evidence boundary — R5), 0018–0019 (experiment-packet readiness/registration, current sourcing state — R6), 0020–0022 (experiment inferential readiness/versioning, daee noetic application, experiment methods gate — R7), 0023–0025 (mathematical typesetting pipeline, dynamic orthing / representation learning, meta-noetic memetics and sound corrective dynamics — R7B), 0026–0028 (candidate and multi-target state — R7C), 0029–0033 (live candidate, representation, ecology, and governed correction — R7D), 0034–0036 (independent repair and Somnic contracts — R7E), 0037 (v5 continuation registry), 0038 (final-sixth scoped successor overlay), 0039 (Seventh–Sixteenth source and evidence successor layer), and 0040 (bounded through-Twentieth archive extension). **Git integration and public custody records do not establish theory adoption, terminology adoption, empirical validation, or natural campaign closure.**
- **Generated project state:** [`docs/current-state.yaml`](docs/current-state.yaml) — the canonical machine-readable revision, counts, statuses, and burdens; VERSION/README/STATUS/OPEN-DECISIONS are checked against it in CI.
- **Sourcing:** [`references/orthemology.bib`](references/orthemology.bib) + [`docs/sourcing/`](docs/sourcing/) — per-claim verification statuses.
- **Closure accounting:** [`docs/project-closure/`](docs/project-closure/) — formal audit, counterexample ledger, reviews, burden ledger.
- **AR8R V11 reconciliation:** [`docs/project-closure/ar8r-v11/`](docs/project-closure/ar8r-v11/README.md) — sanitized evidence dispositions, bounded theorem and synthetic-pilot packets, provenance reconciliation, and active/deferred research-program memory; no private transcript or natural-closure claim.
- **Reconciliation history:** [`archive/reconciliation/`](archive/reconciliation/) — exact patches, ledgers, and validation reports (immutable; retain pre-R2 notation by design).
- **Draft PDFs:** [`artifacts/`](artifacts/) — DRAFT-stamped, commit-pinned renderings with source-hash sidecars.

## Integration history

These retained summaries describe particular source integrations and their original evidence boundaries. They are not live branch, CI or acceptance claims. Use [STATUS.md](STATUS.md) for the status roles, the [frontier guide](docs/reader/CURRENT-FRONTIERS.md) for research continuation, and the linked original collection owners for dated statements. The [pre-refactor entrance](https://github.com/theislampill/orthemology/blob/924493b171ca0bd54df20727c7e47820817affdb/README.md) preserves the earlier arrangement and preparation wording.

**v5 research successors:** the [current guide](docs/architecture/V5-RESEARCH-SUCCESSORS-07-15.md) and [source/review index](docs/provenance/v5-successors/README.md) cover Seventh–Twentieth research in the same v5 programme. [Result status](docs/provenance/v5-successors/RESULT_STATUS.json) keeps written arguments, formal components, finite reference execution and inherited evidence separate. The [final-Sixth layer](docs/architecture/V5-RESEARCH-CONTINUATIONS.md) remains preserved as the accepted predecessor. Candidate identity judgements, foundational warrant, empirical validation and terminology adoption retain their own unresolved scope and review requirements.

The [through-Twentieth extension](experiments/orthemology-v5-successors/groups/t20-successor/README.md) preserves the exact through-Sixteenth base and adds the distinct Seventeenth–Twentieth sources through the existing owners. It contains 262 results and 3,828 source identities, including a separate 212-text-file final reading/report addendum; 37 suite descriptors and 44 native receipts remain unchanged. The new receiving-integration science is NOT_RUN even where original research packets record fresh scoped proof/review execution. The [dated assessment history](docs/provenance/v5-successors/T20_ASSESSMENT_HISTORY.json) preserves earlier judgements separately from the final current appraisal. The original preparation note reported no push, PR or merge and a locally blocked Docker/Poppler PDF rebuild. Those are historical execution observations, not the current checkout’s CI or merge status. Exact-tree qualification and subsequent integration must be checked in their own dated receipts; source custody alone supplies neither.

The [Sixteenth successor](experiments/orthemology-v5-successors/groups/t16-successor/README.md) adds 21 scoped results and 641 source identities. Its supplied core/controller reviews and scientific executions are inherited; no fresh T16 kernel or empirical replay is claimed. The earlier 195 result statements and 44 execution receipts remain unchanged. Final document-review bodies referenced but absent from the supply remain reported, not inspected acceptances.

**v5 source consolidation:** [integration guide](docs/architecture/V5-INTEGRATION-GUIDE.md), [construction provenance](docs/provenance/v5-consolidation/README.md), and [repository-native replay](experiments/orthemology-v5/README.md). Source construction, exact-tree qualification and GitHub landing are separate evidence layers. All six governed PDFs and their source packages now reproduce the reviewed publication source pin recorded in [publication provenance](docs/provenance/v5-consolidation/PUBLICATION_SOURCE_REVIEW.json), including the corrected source text. Integration and artifact reproduction grant no research adoption, novelty, peer-review, release or v6 credit.

## AR8R V11 reconciliation expansion

The current public reconciliation packet is indexed at [`docs/project-closure/ar8r-v11/`](docs/project-closure/ar8r-v11/). Task 7 adds exact-but-deferred Candidate E/G custody, current A–N / M–T–N and transcendental bridge owners, typed proper-function/ontology/TAC matrices, a noncircular formalization queue, and an unresolved Connes-rigidity specification-warrant case. These additions do not adopt the deferred candidates or PMR proposals, repair T354, establish a Lean/kernel proof, select a champion, reach a meniscus, or claim natural closure.

The final separately sealed methodological/control/document successor adds 53 public texts and one integration-only scope record. Exactly one new source-bound result, T20-EMERGENCE-TYPE-CONTROL, describes a chosen unbounded indexed interpretation; all 261 prior result/status records are preserved. Retrospective reading/methodology and packaging receive no new result or native scientific-execution credit. Current document roles and historical predecessors are linked from the Twentieth guide.

The separately dated source-context successor adds 21 selected public records and one receiving-scope record, for 262 results / 3,828 sources. The existing foundational-synthesis and emergence-control owners bind the new reconstruction and application limits, with exact prior statements retained. All statuses, old sources, proof conclusions, 37 suites and 44 receipts remain unchanged. The Twentieth guide links the current reassessment and the preserved report/guide history.
