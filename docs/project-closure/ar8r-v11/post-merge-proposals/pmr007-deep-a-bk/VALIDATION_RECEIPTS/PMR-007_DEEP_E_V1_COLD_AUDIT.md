# PMR-007 Deep Round E V1 — cold audit

```text
audit epoch: B
candidate: PMR-007-TNAC-1 V1
disposition: REPAIR_REQUIRED
blocking findings: 3
```

## DE-F01 — Candidate-N map hash was incorrect

The source dossier and custody owner recorded
`03c50c0e...` for `A_TO_N_COMPREHENSIVE_INTEGRATION_MAP.yaml`; direct
recomputation gives
`cc1eefd4db0af89f5f948ccfffb0a8f15b8d12468d23c3a4cf5e4eb2f05c34c8`.
A source-custody round cannot be admitted with a false evidence hash.

**Required repair:** correct every occurrence and freeze the repaired owners.

## DE-F02 — source locators were not executable custody checks

V1 labeled source locators but the primary architecture checker did not open the
actual source files, verify their hashes, or verify the expected fragments.

**Required repair:** add an independent source-custody checker binding every
locator to the exact local artifact and preserving the no-Arabic-primary/no-
neutral-migration firewall.

## DE-F03 — N-conditional “best fit” was recorded rather than derived

The checker accepted `A_UNIFIED_PERSONAL` as source-internal best fit because a
field said so.  This is not an auditable comparison.

**Required repair:** define the exact N-track predicate profile and compute the
source-compatibility leader by coverage.  Call it a compatibility result, not an
explanatory or truth result.  It must not create a neutral champion.

## Nonblocking notes

- `TNM-1` is elementary consequence bookkeeping with zero mathematical novelty.
- The architecture dominance relation is a declared partial order, not a
  canonical scalar or exhaustive theory-choice theorem.
- Source compatibility conditional on source truth is not world truth.
- No Arabic-primary verification was performed.
- Candidate N remains provisional and source-specialist review remains open.
