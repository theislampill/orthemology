# Decision 0035 — Somnic orthing and activation contracts

**Date:** 2026-07-21 · **Authority:** SOL CANDIDATE bounded Task 4 implementation · **Status:** proposed-candidate · **PR:** #12 · **Reopens nothing:** Decisions 0001–0022 remain byte-identical and stand.

<!-- decision-candidate-boundary:start -->
```yaml
schema: orthemology-decision-candidate-boundary-v1
decision: "0035"
status: proposed-candidate
pr: 12
scope: runtime-neutral-somnic-contracts-only
preserves_decisions: ["0001-0022"]
reopens: []
independent_signoff: false
ready_for_merge: false
merged: false
```
<!-- decision-candidate-boundary:end -->

<!-- somnus-claim-status:start -->
```yaml
claim_status_id: somnus-claim-boundaries-v1
empirical_validation: {status: not-established, owner: future empirical study, evidence_basis: no empirical study was run}
performance: {status: not-established, owner: future comparative evaluation, evidence_basis: no matched workflow comparison was run}
learning: {status: not-established, owner: future governed outcome study, evidence_basis: no modification and later-outcome loop was executed}
generalization: {status: not-established, owner: future cross-model and cross-domain study, evidence_basis: fixtures do not establish transfer}
internal_ontology: {status: not-established, owner: future interpretability inquiry, evidence_basis: records do not expose an actor interior state}
terminology_utility: {status: not-established, owner: terminology benchmark, evidence_basis: terminology benchmark was not run}
terminology_adoption: {status: not-established, owner: human terminology review, evidence_basis: no term was adopted}
runtime: {status: not-implemented, owner: external downstream runtime owner, evidence_basis: this repository contains schemas fixtures and offline validation only}
collective_execution: {status: not-implemented, owner: external collective runtime owner, evidence_basis: no network transport council or shared service exists}
```
<!-- somnus-claim-status:end -->

## Decision

> **Waking orths experience.<br>
> Somnus orths the available orthings of experience.<br>
> The frontier tells somnus what is newly at issue; the ledger tells it what the new issue may belong with.**

A waking orthing takes up an occurrence and places, withholds, or revises a placement under the analysis, evidence state, governing configuration, claimant contracts, evaluator versions, and selector versions in force at `t1`. The preserved orthing may later become an orthemma for a different episode. **Meta-orthability** is that later episode's applicability and record-sufficiency gate; **somnic orthing** is the later placement operation over the prior orthing, pathway, residual, governing artifact, or relation. Inapplicability, indeterminacy, and record insufficiency produce explicit non-assessment dispositions.

### Two times and append-only history

The `t1` waking event history is authoritative and append-only. Checkpoints are appended during operation; closure or interruption appends another event; a materialized episode view is derived. A `t2` somnic assessment references the preserved target and a digest of its history. It may supersede an earlier assessment by reference, but it cannot edit the target history, insert later evidence into the `t1` state, or retrospectively change which historical contract version governed. Evidence is separated into observed at `t1`, used at `t1`, indexed but unused at `t1`, and discovered after `t1`.

Session, episode, occurrence, claim attempt, claimant-level orthability assessment, orthing, somnic assessment, and proposal identities remain distinct. A conversational turn is not the primary unit and establishes none of those equalities. Privacy and source-scope limits apply before minimal occurrence capture; activation contracts gate claiming after capture. Inapplicable and indeterminate attempts remain auditable.

### Brownfield ownership

The existing episode schema remains the owner of occurrences, analyses, evidence, candidates, placements, routes, actions, successors, traces, governing configurations, metaorthemmata, and claim/verdict references. The claim ledger remains the claims-and-residual owner. The verdict registry and verdict-record schema remain the result/pathway vocabulary, including evidence, governing-configuration, governing-token, execution, route, and closure axes. Analysis, metaortheme, metaorthemma, handoff, represented-standard/ecology, and corrective-transition records keep their existing roles. The new schemas add only the gaps for activation contracts, append-only events, claimant-level meta-orthability, somnus runs, somnic assessments, and controlled recurrence reports.

### Activation and claimant routing

Activation contracts are versioned governing artifacts, not skills and not keyword triggers. Each accepted version declares required properties, positive and exclusion indicators, counterexamples, ambiguity policy, plural fallbacks plus a no-claim option, effective revision, fixture outcomes, and authorship. The initial artifact may have explicit bootstrap provenance; later versions require a normal authoring orthing. The evaluator is separately identified and versioned and returns `applicable`, `inapplicable`, or `indeterminate`. Required-property findings remain distinct from indicators. One claimant's indeterminacy need not make the episode unresolved when another claimant or an explicitly governed baseline route is applicable.

### Frontier, recurrence, and retrospective loci

A somnus run separates newly unassessed or materially reopened anchors from the eligible historical reference corpus and the comparators actually used. An already-assessed comparator need not be reopened. Closed somnic outputs remain assessable but do not enter the next frontier without a material delta. An unchanged operation/frontier/version/idempotency tuple cannot emit a non-equivalent duplicate.

V0 is limited to controlled residual-fingerprint recurrence. A match is a structural recurrence candidate, not causation, a shared defect, independence, or a remedy. Reports expose episode, session, normalized-input-family, actor, source-family, time-span, and counterexample dimensions and use “distinct episodes” unless a declared independence rule passes. A threshold is a review trigger only. Pattern equivalence, suspected locus, causal diagnosis, and intervention remain separate. The assessment surface preserves metaortheme adequacy, activation-contract adequacy, evaluator accuracy, metaorthemma binding correctness, execution fidelity, evidence adequacy, placement correctness, and closure adequacy.

### Writeback and authorization boundary

Somnus subsumes the practical question of what, if anything, should change in memory, user state, facts, skills, or governing artifacts. It may instead warrant investigation, evidence requests, residual preservation, or no change. Assessment, intervention disposition, proposal, independent authorization, application, and later outcome evaluation remain distinct. Proposal rejection or failed application does not rewrite its supporting assessment; application is not self-validation. `legacy_reflective_proposal` and `somnus_grounded_proposal` remain different provenance modes. The independently queryable chain is `t1` waking orthing, `t2` assessment, `t3` proposal/authorization, `t4` application/successor state, and `t5` outcome evaluation.

### Downstream collective profile

Collective Somnus remains outline-only and downstream. It distinguishes C1 independent type-convergent orthing, C2 federated reference-preserving transclusion followed by local re-orthing, and C3 intentional bounded council coordination. Shared types do not supply transport. A source envelope remains immutable; the recipient appends its source-status, compatibility, local meta-orthability, evidence, disposition, and authorization records. Normative type, actor/time represented standard, case-bound metaorthemma, transclusion packet, and execution are not interchangeable. Receipt is not truth, local applicability, adoption, authorization, execution, or prior local experience.

Multi-operator recurrence is not independence, tawatur, truth, or authorization. Bounded collective closure preserves scope and dissent. A downstream runtime must enforce minimum disclosure, redaction honesty, integrity and version checks, bounded cycles, fail-closed parsing, injection/poisoning/Sybil/common-source defenses, and separate local authorization. An exported artifact is not direct access to an actor's interior state, and NAR or field-witness similarity is not complete semantic identity or recipient uptake.

## Implementation boundary and successor trigger

The repository has no canonical residual-recurrence execution owner: empirical packet harnesses are not a general somnic runtime, and conformance validators are not analyzers. This decision therefore lands schemas, deterministic fixtures, and an offline validator only. A direct reference operation requires a separately approved downstream runtime owner that adopts the schemas and proves deterministic fixture-driven output, idempotency, material-delta reopening, privacy/source handling, and independent authorization.

No replay, counterfactual replay, live ledger emitter, scheduler, daemon, network, shared-memory service, transclusion transport, skill package, private prompt, host configuration, writeback engine, automatic proposal, automatic adoption, automatic execution, automatic patch, promotion, closure, governed learning, or external runtime mutation is implemented. The Hermes/Dreaming comparison remains an externally supplied, source-qualified application outline pending source, license, commit, and test verification; it is described as coarser or more implicit, never as non-reasoning.

## Non-claims

These fixtures show only that the declared records and attacks are internally conformance-checked. They do not demonstrate a deployed Somnus runtime, empirical benefit, long-horizon learning, cross-agent semantic equivalence, independent agent testimony, safe imported execution, population-scale diagnosis, or a civilisational result.
