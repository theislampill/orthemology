# Decision 0034 — R7E Sol independent repair contract

**Date:** 2026-07-21 · **Authority:** SOL CANDIDATE independent-review pass · **Status:** proposed-candidate · **PR:** #12 · **Reopens nothing:** Decisions 0001–0022 remain byte-identical and stand.

<!-- decision-candidate-boundary:start -->
```yaml
schema: orthemology-decision-candidate-boundary-v1
decision: "0034"
status: proposed-candidate
pr: 12
scope: review-state-accounting-only
preserves_decisions: ["0001-0022"]
reopens: []
independent_signoff: false
ready_for_merge: false
merged: false
```
<!-- decision-candidate-boundary:end -->

## Problem

PR #12 contains useful candidate changes, but its inherited candidate overlay
omits PRs #11 and #12, its workflow/backlog claims are not independently
reconstructible from repository evidence, three semantic contradictions pass
the existing validators, and the publication/source lanes remain incomplete.
A green historical suite therefore cannot be treated as independent signoff or
merge readiness.

## Decision

1. Maintain a durable Sol control plane under
   `docs/project-closure/r7e-sol/`: exact read-only reproduction, an
   evidence-backed finding matrix, an R7E hunk disposition, and an autonomous
   state record.
2. Record PR branch/base/head/check/mergeability facts as timestamped
   observations using `head_at_observation`; no tracked file claims to contain
   a timeless current or eventual self-referential branch head.
3. Every independent finding has a stable ID, one of `reproduced`, `refuted`,
   `partially-reproduced`, or `unverified`, evidence, severity, a repair task,
   and terminal status.
4. Every PR #12 changed path receives exactly one disposition: `keep`,
   `revise`, `drop`, or `provenance-only`. Generated PDFs, sidecars, project
   state, and the release manifest do not become independent semantic evidence.
5. The controller-confirmed `gpt-5.6-sol` selection is a pre-write gate. It is
   recorded as controller evidence, not fabricated environment-variable
   evidence.
6. Decision 0034 remains `proposed-candidate` on PR #12. It cannot self-promote,
   issue independent signoff, declare merge readiness, merge a PR, or reopen
   Decisions 0001–0022.

## Non-claims

This decision establishes review-state accounting only. It validates no
empirical, comparative, metaphysical, theological, terminology, swarm, or
publication claim. It does not establish that all blockers are repaired, that
the full mathematical migration is complete, that all PDF pages have final
visual approval, or that any PR is ready to merge.
