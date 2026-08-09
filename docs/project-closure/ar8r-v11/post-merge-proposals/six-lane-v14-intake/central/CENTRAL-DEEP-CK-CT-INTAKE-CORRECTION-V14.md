# Central Deep CK–CT intake correction

The exact 178-file source tree is preserved unchanged. This overlay controls
repository interpretation of that source.

## Execution coverage

The source tree contains 31 JSON result owners and 14 Python checker sources.
Independent output-intercepted replay established:

- `REPRODUCED`: 13 result owners;
- `SOURCE_ABSENT`: 17 result owners;
- `BLOCKED_MISSING_SIDECAR`: the Deep CT distinct-rereview owner, whose source
  requires an omitted frozen-hash sidecar.

The 17 source-absent owners are the CK distinct rereview, CL V1/V2, CM V1/V2,
CN failed V1 plus V1/V2/V3, CO V1/V2, CP distinct plus V1/V2, and CQ distinct
plus V1/V2. The Deep CT distinct-rereview source is present but not replayable
from the sanitized tree. All other source-present result owners were reproduced
at their exact frozen JSON boundary, including the expected negative CK/CT V1
executions.

The supplied CK–CO result index also points to five absent admission-hash
sidecars. The package `ARTIFACT_MANIFEST.json` and `SHA256SUMS` preserve byte
custody, but they do not make those missing sidecars executable dependencies.

## Evidentiary ceiling

The reproduced checkers establish only bounded schema, finite construction,
and model properties. In particular:

- a checker that defines a license as the conjunction of 19 bits does not show
  that any real source/world bridge satisfies those bits;
- hard-coded architecture models do not establish an actual implementation;
- structurally distinct algorithms do not establish independent reviewer or
  model lineage;
- `ADMITTED_POST_MERGE_SCOPED_RESULT` inside the frozen source means central
  thread proposal admission only.

Controlling repository status for CK–CT is therefore:

```text
provenance: POST_MERGE_RESEARCH_PROPOSAL
historical_identity: NONE
repository_scientific_adoption: NONE
owner_adoption: PENDING
external_review: OPEN
general_novelty: 0
Lean_or_kernel_claim: NONE
integrated_champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural_closure: NOT_REACHED
```

The next central operation is actual-map eligibility for Deep CU. If concrete,
target-blind U/I/P implementation maps with common measurable semantics do not
exist, the correct disposition is `BLOCKED_ON_ACTUAL_IMPLEMENTATION_MAP`, not
another synthetic discriminator over inherited profiles.
