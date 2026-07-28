# R7E Sol — Merged-Main Verification Record

**FINAL MERGED-MAIN EVIDENCE (2026-07-27).** This record was authored from
live GitHub facts and a fresh, isolated clone after the authorized R7E Sol
integration cascade reached protected `main`. It attests the earlier,
already-verified main merge `8db1630ab715b0931907c627be97b32399d6f4fc`.

Following the accepted R5/R6 pattern, this file is non-self-referential. Its
containing follow-up commit and merge live in ordinary Git history and are
verified after protected readback; they are never self-hashed or named by a
tracked equality contract.

## Reviewed candidate and protected cascade

The exact independently reviewed candidate was
`b22d4351f4d3a76bc3f16b41704a470b4abb1aa5`. Every integration step used an
ordinary merge commit and preserved both parents:

| Integration step | Resulting merge commit |
|---|---|
| PR #13, review branch into PR #12 head branch | `e12cfbbf880b52c38f4064bb7ec6e4393705e319` |
| PR #12 into PR #11 head branch | `4d09fed5f2d2106fd5ecd9a79b1d13e6b9af32fc` |
| PR #11 into PR #10 head branch | `f4a4804101202c056a31f3d30f2ef931e1dcca2d` |
| PR #10 into PR #9 head branch | `2867f3510c343fea8c7fd6c37b8ad38ce5de83a6` |
| PR #9 into PR #8 head branch | `17f6783d5d5a39a90dee7b10573ef6bc3732ae5e` |
| PR #8 into protected `main` | `8db1630ab715b0931907c627be97b32399d6f4fc` |

Git ancestry in the fresh clone confirms that the reviewed candidate is an
ancestor of every downstream merge and of protected `main`. No force-push,
history rewrite, or squash removed the reviewed lineage.

## Exact-SHA GitHub Actions evidence

All required `validate` runs completed successfully. Paired push and
pull-request runs were required at each intermediate branch boundary; the
final protected-main SHA has its own push run.

| Exact SHA | Successful run IDs |
|---|---|
| `b22d4351f4d3a76bc3f16b41704a470b4abb1aa5` | `30317000439`, `30317471209` |
| `e12cfbbf880b52c38f4064bb7ec6e4393705e319` | `30317917503`, `30317919628` |
| `4d09fed5f2d2106fd5ecd9a79b1d13e6b9af32fc` | `30318432384`, `30318434266` |
| `f4a4804101202c056a31f3d30f2ef931e1dcca2d` | `30318923898`, `30318925662` |
| `2867f3510c343fea8c7fd6c37b8ad38ce5de83a6` | `30319389233`, `30319391979` |
| `17f6783d5d5a39a90dee7b10573ef6bc3732ae5e` | `30319878639`, `30319880488` |
| `8db1630ab715b0931907c627be97b32399d6f4fc` | `30320348878` |

## Fresh protected-main reproduction

The post-merge audit used an isolated GitHub-origin clone with
`HEAD == origin/main == 8db1630ab715b0931907c627be97b32399d6f4fc`.
Its Python 3.11.9 environment was populated only from
`requirements-ci.lock.txt`; `pip check` passed.

| Gate | Result |
|---|---|
| Re-extracted workflow commands | 71/71 passed |
| Supplemental publication commands | 8/8 passed |
| Governed PDFs | six artifacts; 26 + 14 + 8 + 6 + 5 + 2 = 61 pages |
| Raster and visual QA | two complete 150-dpi passes; ordered hashes identical; 61/61 pages inspected; zero defects |
| Tracked tree | 707 paths; clean tracked state; `git fsck` passed |
| Release manifest | 706 non-self entries; every entry rehashed successfully |
| Source packages | six archives; 24 members; archive, member, sidecar, PDF-hash, manifest, and page-count checks passed |
| Source-status registry | 25 classified claims; validation passed |
| Terminology boundary | zero prohibited semantic hits |
| AR6 reconciliation | 1,329/1,329 records; all four closure counters zero |

AR6 remains `INTERRUPTED_IN_PROGRESS` and `NOT_APPLIED_NOT_APPROVED`. Its
reconciled negative evidence and neutral mathematical distinctions retain
their recorded dispositions; no interrupted claim, proof, theorem, source
assertion, formal artifact, executable artifact, or proposed patch is promoted
by this merge verification.

## Scope and remaining gate

This record establishes the protected integration cascade and the fresh-main
technical proof for Tasks 1–16. It does not claim empirical validation,
terminology adoption, external peer review, publication, release, or approval
of interrupted research.

The record's containing follow-up branch must still receive independent review,
exact-SHA CI, an ordinary protected merge, and protected-main readback. That
readback verifies the containing commit and merge through Git history without
placing either identity inside this non-self-referential record.
