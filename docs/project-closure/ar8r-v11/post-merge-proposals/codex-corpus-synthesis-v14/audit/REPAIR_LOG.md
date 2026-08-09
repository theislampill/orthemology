# Codex corpus synthesis V14 repair log

The distinct cold audit returned `REPAIR_REQUIRED`. No blocking finding was
waived.

## AR8R-V14-B01 — theorem-family relation

`REL-02` now classifies AR-T1 and the generic theorem as `SHARED_INVARIANT`.
The prose, candidate records, and verdict distinguish the broader prior-art
fibre theorem from AR-T1's Boolean-target, nonempty-world specialization.
AR8R-T294 remains a strict causal specialization. Novelty and historical
identity remain zero/none.

## AR8R-V14-B02 — fail-closed validation

The validator now pins:

- the repaired candidate-freeze manifest by its own SHA-256;
- its exact fourteen-member set and every frozen member hash;
- all 12 instance IDs and relation classes;
- all 14 theorem-family relation IDs and classes;
- all five candidate IDs and verdicts;
- all eleven countermodel IDs;
- the six residual-hypothesis IDs and statuses;
- exact B1–B4 statuses and zero execution;
- every machine authority surface;
- the T354 blocked and unavailable-TAC/SAC controls;
- semantic source contracts for the seven previously weak citations;
- normalized repository-relative source locators; and
- prose-level promotion patterns.

Mutation tests now require the specific expected issue, not only a generic
`FAIL` result.

## AR8R-V14-B03 — semantic source contracts

CLIM-03 and CLIM-04 now point to the exact Specialist A provenance-root owner;
CLIM-06 and REL-06 point to the observation/co-Büchi owner; REL-05 points to
the language/version custody owner; and REL-10/REL-11 point to the exact Deep
Research ancestry ledger. The validator enforces those mappings.

## AR8R-V14-B04 — nonvacuous review chain

The cold-audit receipt and this repair log are now materialized. The repaired
candidate bytes are frozen separately. A distinct fresh-context rereview must
pass before the final SHA manifest is generated and before the baseline and
mutation tests can be credited.

## Nonblocking findings

The C5 proof label was narrowed to
`ELEVEN_DECLARED_COUNTERMODEL_SKETCHES`. The finite checker retains its
`FINITE_EXHAUSTIVE_REGRESSION_NOT_GENERAL_PROOF` scope. Candidate/public custody
remains explicit until an exact audited head is merged and read back.

## AR8R-V14-RR01 — nonvacuous mutation assertions

The first distinct fresh rereview found five remaining result-only tests whose
mutations also changed frozen or final-manifest bytes. Each now requires the
specific issue emitted by its intended semantic gate: instance identity,
unknown theorem relation, program-status promotion, source-world/nonclaim
promotion, or candidate ancestry/nonclaim deletion. Generic failure from an
unrelated hash mismatch no longer satisfies those tests.

The same rereview noted that C1's metadata omitted `Classical.choice`, although
the Lean receipt already reported it. The dependency list now names classical
choice explicitly. This metadata repair changes no theorem statement, proof,
axiom report, ancestry, novelty, or adoption status.

## AR8R-V14-FR01 — generated release-manifest refresh

The second distinct fresh rereview killed all twenty mutation controls and
qualified the bounded V14 corpus in a disposable completed surface, but
correctly withheld a repository-wide pass because the public release manifest
still carried the pre-diff hashes of six tracked integration files. That
`REPAIR_REQUIRED` receipt is preserved. The release manifest is regenerated
only after the final V14 local receipt and complete synthesis hash manifest are
materialized, then the exact completed tree receives a further whole-branch
rereview.

## AR8R-V14-FR02 — deterministic checker-result bytes

Staging exposed a Windows/Linux custody mismatch: the checker used text-mode
output, so its result file had CRLF bytes in the Windows working tree but an LF
blob under the repository's `eol=lf` policy. The checker now writes encoded
UTF-8 bytes directly with one LF terminator. The regenerated result is
byte-identical to its staged Git blob. Checker source, result, candidate-freeze,
validator pins, and final receipts are refreshed from those deterministic
bytes before the whole-branch rereview.

## AR8R-V14-FR03 — trailing-blank-line diagnostics

The V14-local pass reported five trailing blank lines as nonblocking to the
scientific result. They were nevertheless removed so repository-level
`git diff --check` can remain fail-closed. Candidate hashes, the freeze
manifest, and the final local rereview receipt are refreshed after this
format-only change.
