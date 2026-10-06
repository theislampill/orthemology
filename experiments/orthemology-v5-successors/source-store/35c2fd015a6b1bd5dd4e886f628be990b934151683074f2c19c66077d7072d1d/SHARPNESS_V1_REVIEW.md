# Independent focused review: exact-list 21-trial attainment

Verdict: ACCEPT `controller-sharpness-v1` only as an attained worst case for
this one fixed controller order and one fixed actual-root fault world.
The accepted main core and all its protected-service restrictions are unchanged.

## Bound identities and checks

- Extension milestone:
  `tranche8/research/shared-root-progress/milestones/controller-sharpness-v1`
- Extension manifest SHA-256:
  `2ec4b220e069c8a6c7321403c10185670d33bb93faed3362523bfdf42ef157c6`
- Main core manifest SHA-256:
  `fffebbef80cac51557b7bcc7751b135999e5cd6f2dfe2eae816e447b624b403a`
- Extension source SHA-256:
  `6772e1b6852b62b28179e276cd0ab779b810fff0e013d58307b446623c776847`
- Reviewer receipt: `evidence/SHARPNESS_V1_REVIEW_RECEIPT.json`, SHA-256
  `5f2051f02d11fb89837af548e435b5d96093a220f6f5fc9b556243dd1289e248`

The one new module was cold-compiled with verified official Lean 4.19.0,
one job, against the reviewer's already cold-built accepted main core.
No unchanged core proof was unnecessarily replayed. All 12 named extension
theorems and one new reviewer theorem have exactly inventoried standard-only
axiom closures. Source, axiom and reviewer builds were warning-free. Frozen
extension hashes and the main core identity were checked before and after.

## Mathematical result actually reviewed

`worstWorld` fixes the alias class {0,1}, six actual roots, one faulty actual
root (the shared class), lifted bad-label budget 2, and q=r=5. The same world
is used throughout. The bad schedule grants preparation and cancellation but
withholds at the source execution gate throughout. Synchronization replies
may vary arbitrarily under the already accepted completed-slot contract.

Every one of the explicit public list's first 20 paths contains a label of
that one bad actual root. `bad_path_rejected` derives false directly from the
unchanged source attempt gate for arbitrary root-store contents. The actual
first-20 program prefix therefore leaves the full plant unchanged.
`scheduled_take` connects that prefix to the actual full program, and
`last_path_position` verifies that {2,3,4,5,6} is its last support. This does
not rely on an unspecified powerset enumeration order.

`twenty_one_attained` establishes that the prefix has not reached the installed
successor, while all 21 trials reach it on a lawful 259-transition accepted
shared trace. The positive part specializes the independently accepted uniform
source-controller theorem; it does not assume a desired successful trace.

The reviewer added `ReviewerSharpnessControls.lean`. Its
`first_twenty_exact_zero_effect_trace` constructs a lawful 247-transition trace
from initial state through synchronization and the first 20 actual trials.
Accepted shared typed counters then establish zero installations and zero
repairs. Thus an endpoint equality is not hiding earlier effects or a later
reset. The main review's all-world counter control already gives exactly one
installation and zero repairs for the complete run.

## Fixture and scope that must remain visible

This is the compact mathematical fixture with source bytes [65,66,67] (ASCII
ABC), length 3, SHA-256
`b5d4045c3f466fa91fe2cc6abe79232a1a57cdf104f7a26e716e0a1e2789df78`.
The source digest was independently checked against the bound bytes.
The starting draft is ABC plus LF. The result installs the exact criterion,
increments its version 3→4, and retains that original draft. It is not a
finished repair, a retrieved physical repository, or the separate 3013-byte
label-local source fixture.

The source-admission window remains [2,22], and all bounded-slot, authentic
authority, fixed-world and protected-interleaving limitations from
`CORE_V1_REVIEW.md` apply. The count is logical serviced work, not elapsed time.

This is not a lower bound for another path order, another controller, adaptive
protocols, richer observations or randomized search. No opacity or
indistinguishability model is added, and the unchanged native four-path
`runBatch` is not a native 21-path implementation. The word "sharpness" is
accepted only with the explicit fixed-controller/order/world qualification.
