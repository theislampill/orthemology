# Decision 0036 — Somnic episode identity and intra/inter-somnic relations

**Date:** 2026-07-22 · **Authority:** SOL CANDIDATE bounded Task 4.x follow-up · **Status:** proposed-candidate · **PR:** #12 · **Adds to:** Decision 0035 · **Reopens nothing:** Decisions 0001–0035 stand; Decisions 0001–0022 remain byte-identical.

<!-- decision-candidate-boundary:start -->
```yaml
schema: orthemology-decision-candidate-boundary-v1
decision: "0036"
status: proposed-candidate
pr: 12
scope: runtime-neutral-intra-inter-somnic-contracts-only
preserves_decisions: ["0001-0035"]
reopens: []
independent_signoff: false
ready_for_merge: false
merged: false
```
<!-- decision-candidate-boundary:end -->

## Decision

A Somnus run, somnic episode, and somnic assessment are distinct owners. A run
is an orchestration envelope and may contain zero, one, or several episodes. A
somnic episode is the bounded semantic orthing unit. A somnic assessment is one
placement record owned by exactly one episode. Run completion, episode
disposition, and assessment commitment are independently recorded; none
silently completes another.

Intra-somnic activity stays within one `somnic_episode_id`, even when that
episode has several events, subjects, assessments, or historical comparators.
Inter-somnic activity is an asserted, provenance-bearing relation between two
distinct episode identities. Same-run and same-operator episodes may therefore
be inter-somnic. Different implementation phases do not make activity
inter-somnic when the episode identity is unchanged.

Inter-somnic records keep semantic relation and information path independent.
They preserve asserting, source, and target episodes; source and target
assessment references; run and operator relation; operation/version;
material-delta reference where required; stable relation identity and
idempotency; evidence timing; provenance; confidence; claim status; and
non-inheritance. An episode cannot be inter-somnic with itself.

`compares-with` neither reopens nor mutates its source. `reopens` requires a
new target episode, a material delta, and preserved source state. `reassesses`
requires prior-assessment lineage and bounded depth without automatic
requeueing. Closed assessments remain outside later frontiers absent a
governed trigger. Reopening cycles are rejected. Re-emitting an equivalent
relation is idempotent; a non-equivalent duplicate is rejected.

Cross-operator transclusion preserves source operator, ledger, episode,
assessment, receipt, redaction, and source-status records, then requires a
local meta-orthability result and local disposition. Receipt does not transfer
applicability, closure, confidence, evidence-time, normative authority,
execution authorization, writeback authorization, or adoption. Evidence
received at `t2` never becomes either episode's earlier `t1` evidence.

A collective episode has its own identity. Its internal synthesis is
intra-somnic; its source edges are inter-somnic. Source closure, dissent, and
scope remain preserved. Independent convergence uses a no-communication
information path; direct transclusion cannot claim independence.

## Brownfield ownership

`somnus-run.schema.json` continues to own orchestration. The additive
`somnic-episode.schema.json` owns episode identity, internal activity, and
episode disposition. `somnic-assessment.schema.json` continues to own
placements and now resolves one episode plus explicit lineage/frontier and
relation references. The additive `inter-somnic-relation.schema.json` owns
asserted cross-episode semantic and information-path edges. The Task 4 fixture
bundle and production validator remain the cross-record authority.

## Reconstruction and implementation boundary

R7E history may be represented only as a retrospective reconstructed analogue:
not live capture, not deployed multi-somni telemetry, and not complete episode
lineage. This decision specifies offline schemas, deterministic fixtures, and
validation only. It adds no runtime, scheduler, service, network, automatic
reassessment, automatic writeback, automatic adoption, or automatic mutation.
