# R7E Sol execution TODO

Status date: 2026-07-27

Tracked plan: `docs/superpowers/plans/2026-07-21-r7e-sol-independent-repair.md`

Public AR6 reconciliation:
`docs/project-closure/r7e-sol/AR6_TO_TASKS_10_16_IMPACT_LEDGER.{md,yaml}`

`incoming_work_status: NONE — no third external package exists`

This ledger covers only the tracked R7E Sol execution plan. A completed task
means its exact implementation commit received independent approval. Preparation
artifacts and interrupted external research do not satisfy that gate.

## Current verified baseline

- Protected `main`: `8db1630ab715b0931907c627be97b32399d6f4fc`.
- Exact independently reviewed Task 15 commit:
  `b22d4351f4d3a76bc3f16b41704a470b4abb1aa5`.
- Protected cascade merge commits: PR #13 `e12cfbbf880b52c38f4064bb7ec6e4393705e319`;
  PR #12 `4d09fed5f2d2106fd5ecd9a79b1d13e6b9af32fc`; PR #11
  `f4a4804101202c056a31f3d30f2ef931e1dcca2d`; PR #10
  `2867f3510c343fea8c7fd6c37b8ad38ce5de83a6`; PR #9
  `17f6783d5d5a39a90dee7b10573ef6bc3732ae5e`; PR #8/main
  `8db1630ab715b0931907c627be97b32399d6f4fc`.
- Exact-SHA CI: GREEN throughout the cascade. Protected-main run
  `30320348878` is SUCCESS; the complete run ledger is in
  `R7E-SOL-MERGED-MAIN-VERIFICATION.md`.
- Last independently approved implementation task: Task 15 closure at
  `b22d4351f4d3a76bc3f16b41704a470b4abb1aa5`.
- Task 16 protected integration and fresh-main verification are complete. This
  non-self-referential follow-up record still requires independent review,
  exact-SHA CI, protected merge, and protected-main readback.
- AR6 status: `INTERRUPTED_IN_PROGRESS`. Its 1,329 records are reconciled, but
  no AR6 patch, claim, proof, theorem, source assertion, formal artifact, or
  executable artifact is applied or approved.

## Tasks 1–16

### Task 1 — Establish the durable Sol review control plane

- Status: completed and independently approved at
  `b8f3890d8282a998f413a1e63e4d9998c176c40b`.
- Implementation/review: complete; no remaining Task 1 work.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: none specific to Task 1.
- Next action: preserve as an approved predecessor.

### Task 2 — Generate and validate the complete candidate topology

- Status: completed and independently approved at
  `af90c37f58b70065b2cf96e29d808dfb52f80704`.
- Implementation/review: complete; no remaining Task 2 work.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: none specific to Task 2.
- Next action: preserve the approved topology contract.

### Task 3 — Supersede the R7E provenance and backlog claims

- Status: completed and independently approved at
  `a8c5c3cbc8b2ed3d504e4b4bf08f53e96cc1a3fe`.
- Implementation/review: complete; no remaining Task 3 work.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: none specific to Task 3.
- Next action: preserve the approved provenance boundaries.

### Task 4 — Specify waking/somnic contracts and residual-recurrence v0

- Status: completed and independently approved, including the bounded fifth
  steer, at `aac14b0c46a34b1d1c6ec6e531e724eaa4385bc7`.
- Implementation/review: complete; the retained regression corpus remains the
  controlling evidence.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: none specific to Task 4.
- Next action: do not reopen without an independently reproduced defect.

### Task 5 — Classify R7E as a bounded LLM-mediated orthing witness

- Status: completed and independently approved at
  `167ce32bdc396490d219cdfbbd436babaa59e21a`.
- Implementation/review: complete; future PoO/PoW/PoR placement is not part of
  this task.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: historical episode cardinality and `t1` identities remain bounded
  unknowns, not completion blockers.
- Next action: preserve the approved witness and defer placement work to a
  separately authorized Task 5.x.

### Task 6 — Add the typed DAEE semantic-operator contract

- Status: completed and independently approved at
  `d96e322d699c51387e85536f665d2b205458edee`.
- Implementation/review: complete; no remaining Task 6 work.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: none specific to Task 6.
- Next action: preserve the canonical predicate alias and v2 transition
  contract.

### Task 7 — Repair epistemology and meta-noetic evidence semantics

- Status: completed and independently approved at
  `79e0bac9c3da7b6a6b6f6e783fcd73f9e6df18cd`, with approved CI-repair
  lineage through `78972e3c187357d2137911f9b2258d854d4d73a0`.
- Implementation/review: complete; source custody and access roles remain
  distinct from claim roles.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: one direct-source custody boundary remains evidence-limited, not a
  completion blocker.
- Next action: preserve the approved source-role boundaries.

### Task 8 — Correct the OSM/CSCG comparison and object firewall

- Status: completed and independently approved at
  `cca756425fa0f23dc9e34c6d0289eea313ab3336`.
- Implementation/review: complete; no remaining Task 8 work.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: none specific to Task 8.
- Next action: preserve the comparison correction and object firewall.

### Task 9 — Repair the argument map, metaphysical bridges, and divine Speech

- Status: completed and independently approved at
  `95da523c1f46fac437928afe9a0351798fe0344c`.
- Implementation/review: complete; the cross-framework positive
  fittingness-to-Wisdom bridge remains explicitly held.
- CI/publication: contained in PR #12 history; not merged to `main`; inherits
  Tasks 15–16 integration gates.
- Blocker: the held bridge is a non-promotion boundary, not a Task 9 defect.
- Next action: preserve the finite approval and explicit held bridge.

### Task 10 — Correct terminology provenance without adopting terminology

- Status: completed and independently approved at
  `72826864abf6fc4ad9d4cf6a29d55a32ed6edd77`.
- Implementation/review: terminal review accepted the source-role,
  historical-attestation, analysis-relative glossary, readiness, benchmark,
  malformed-input, and contrastive-claim boundaries.
- CI/publication: approved local gates passed; the implementation is not yet on
  the PR #12 head, but it is an ancestor of the independently reviewed and green
  review-branch head. No publication is claimed.
- Blocker: none specific to Task 10.
- Next action: preserve Task 10 as the approved predecessor to Task 11.

### Task 11 — Replace the math allowlist with locus-sensitive classification

- Status: completed and independently approved at
  `66e148f024359cce380bac47ea3d2fb1750c760a`.
- Implementation/review: the official post-Task-10 tree was rescanned,
  occurrences were classified by locus and role, and adversarial
  copy/move/delete controls were accepted.
- CI/publication: focused inventory, exact-count, and publication-profile gates
  passed in the approved Task 11 review.
- Blocker: none specific to Task 11.
- Next action: preserve the approved inventory as Task 12 and Task 14 input.

### Task 12 — Migrate all seven publication sources to mathematical markup

- Status: completed and independently approved. The migration closure begins at
  `fd73f652009f182802b10d547618e7e3b29febd7`; subsequent bounded source repairs
  preserve the reviewed tree represented by
  `9dc0094cc6df908fbba1b965bb36d5f3f00979c0`.
- Implementation/review: all seven canonical sources were dispositioned and
  migrated. Table flow, path roots, long mathematics, scripted attachment,
  unique source filenames, and exact source-owned heading repairs were each
  independently reviewed.
- CI/publication: source classification, deterministic generated-source parity,
  mathematical-markup validation, and source/profile validation passed.
- Blocker: none specific to Task 12.
- Next action: preserve the authoritative source commit
  `1703a783d9b25a9cfa93370c4a1a0b568fa497d0` and its reviewed-equivalent tree.

### Task 13 — Repair PDF provenance, candidate status, and artifact generation

- Status: completed and independently approved at
  `61ad3b6f59a72a9b1fca53bd93a7a958e84f6e08`.
- Implementation/review: all six governed PDFs, sidecars, source archives, and
  source manifests bind the authoritative Task 12 source tree and pinned
  offline toolchain. The source-package and heading validators were repaired
  test-first. All 61 final pages were rerendered after stale-page clearing and
  visually inspected.
- CI/publication: double-build byte identity, repository parity, embedded and
  subset font checks, clean offline package builds, ordered 162-heading
  extraction, text structure, link safety, and visual QA pass locally. Exact
  evidence is in `R7E-SOL-ARXIV-COMPATIBILITY.md` and
  `R7E-SOL-PDF-VISUAL-QA.md`.
- Blocker: none specific to Task 13.
- Next action: preserve the approved source packages and PDF parity as Task 14
  and Task 15 inputs.

### Task 14 — Run the complete adversarial and recursive mutation program

- Status: completed and independently approved at
  `5af68cd1e9aa6f16012e4abeeabb3be862b7fc4d`.
- Implementation/review: the authoritative plan inventory contains all 59
  mandatory attacks exactly once and expands them into 77 explicit variants.
  Every variant has a unique mutation ID, a separate valid-control probe, a
  separate invalid-mutation probe, and a machine-readable observation bound to
  its production validator and owner. The 19 Task 14 AR6 inputs are mapped
  exactly once: seven bounded AR2–AR4 negative-evidence records are reproduced
  against exact Task 14 variants, two negative-evidence records without a
  canonical repository owner remain provenance-only, and ten interrupted AR6
  records remain external and provenance-only. The multi-operator attack now
  carries explicit source-independence, warrant, truth, and testimonial-
  transmission promotion mutations through the production entry point.
- CI/publication: 154 separate direct control/mutation processes observe all 77
  variant outcomes; an arbitrary successful command cannot stand in for either
  semantic outcome. The current recursive engine generates 1,813
  mutants across 27 families: 1,546 schema-killed, 248 semantic-killed, and 19
  justified equivalents, with zero unjustified survivors. The canonical report
  is `docs/project-closure/r7e-sol/R7E-SOL-ADVERSARIAL-REPORT.md`.
- Blocker: none specific to Task 14.
- Next action: preserve the approved inventory and exact direct-observation
  bindings as Task 15 and Task 16 evidence.

### Task 15 — Run the exact pinned full suite and clean-clone candidate proof

- Status: completed and independently approved at
  `b22d4351f4d3a76bc3f16b41704a470b4abb1aa5`.
- Implementation/review: the complete `cbab147..ad57371` lineage, source
  boundaries, tests, artifacts, exclusions, PDF container identities, and
  prohibited-terminology boundary were independently reviewed. All 15 original
  findings are terminally resolved without rewriting their original evidence.
- CI/publication: 71/71 re-extracted workflow commands and 8/8 supplemental
  publication commands pass in a new GitHub clone and fresh Python 3.11.9
  lock-only environment. Exact-SHA run `30313374447` is GREEN. Six source
  packages and PDFs pass; two 61-page raster passes are hash-identical; all 61
  pages were visually inspected; generated state and manifest converge; the
  fresh clone is clean.
- Blocker: none specific to Task 15.
- Next action: preserve the exact approved lineage and its immutable CI evidence.

### Task 16 — Perform the authorized protected integration cascade

- Status: completed through protected-main merge and fresh-main verification at
  `8db1630ab715b0931907c627be97b32399d6f4fc`.
- Implementation/review: the authorized PR #13 → #12 → #11 → #10 → #9 → #8
  cascade used ordinary merge commits, preserved ancestry, and reached protected
  `main` without force-push, squash, or rewrite.
- CI/publication: every resulting remote SHA received fresh SUCCESS CI. The
  isolated protected-main clone passed 71/71 workflow commands and 8/8
  supplemental commands; six PDFs total 61 visually inspected pages with
  identical ordered raster hashes and zero defects; 706 manifest entries,
  six source archives with 24 members, 25 source-status claims, and 1,329 AR6
  rows all pass their stated gates.
- Blocker: no remaining semantic, source, proof, PDF, dependency, ancestry, or
  protected-cascade blocker. The non-self-referential verification record
  requires its normal independent-review, exact-SHA CI, protected-merge, and
  protected-readback publication gate.
- Next action: review and merge only the bounded follow-up record commit, then
  verify its containing commit and merge through protected-main Git history.

## AR6 reconciliation boundary

The public YAML contains 1,329 unique package records and preserves zero for:

```text
unclassified_AR6_material_impacts: 0
unmapped_AR6_to_task_dependencies: 0
unresolved_duplicate_patch_relationships: 0
unclassified_interrupted_AR6_claims: 0
```

Every row has a stable neutral artifact ID, package SHA-256, and exact
ignored-custody-record SHA-256. Sensitive historical paths remain only in the
ignored custody ledger. Their public rows use neutral concepts, carry
`IGNORED_PROVENANCE_ONLY`, and explicitly prohibit normative flow.

The pinned 659-file repository snapshot is custody evidence for the package
baseline. Five cumulative research patch layers remain a superseded stack and
must not be applied blindly. Interrupted proof attempts, missing proof audits,
absent solver outcomes, and unfinished candidates remain outside repository
theory unless a later reviewed task accepts a bounded result.

## Protected integration boundary

The reviewed candidate is reachable from protected `main` through the exact
ordinary-merge lineage recorded above. This repository record attests the
earlier merge and fresh-main proof; it does not self-hash or predict its own
containing follow-up commit. That commit and its protected merge remain
verifiable through Git history after protected readback. No tag, release,
external publication, empirical validation, terminology adoption, or approval
of interrupted AR6 work is claimed.
