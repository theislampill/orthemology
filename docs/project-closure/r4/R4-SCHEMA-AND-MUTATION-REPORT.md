# R4 schema and mutation report

> **CANDIDATE PASS — REQUIRES INDEPENDENT REVIEW.**
>
> **Correction notice (same-day, before merge).** An earlier revision of this file stated that the recursive/path-aware mutation engine and the `tests/invalid/` corpus were *not* completed. **That was wrong.** Both were completed; the work landed while the report was being written and was not re-checked before the report and the session closeout were issued. The false statement is corrected below and recorded in `R4-CORRECTION-LEDGER.md` as **SELF-2**. The lesson is the project's own: a completion claim must be checked against the artifact at the moment of claiming, not from a stale observation.

## Baseline (independent probe, before)

Eleven malformed but theory-relevant records were submitted to the R3 schema layer and cross-record validator. **Ten were accepted by both layers.** One — a verdict record missing statuses for its required verdicts — was accepted at the schema layer but **caught** by cross-record pathway recomputation; the independent audit's phrasing on that sub-case was therefore slightly overstated, recorded as a partial refutation rather than absorbed.

## After (same probe, hardened layer)

**0 of 11 accepted.** Every class is rejected at a declared layer:

| Class | Rejected at |
|---|---|
| P1 analysis with empty task and no D1 components | schema |
| P2 metaortheme: empty ids, duplicate states, no policy relation | schema |
| P3 metaorthemma: empty anchors/binder, no validity semantics | schema |
| P4a/b/c residual `owner-assigned`/`deferred`/`risk-accepted` missing its conditional fields | schema |
| P5 handoff with no payload | schema |
| P6 skeletal record claiming audit-ready | schema |
| P7 verdict record missing required statuses | schema (was: semantic only) |
| P8 `not-applicable` without reason outside `required_path` | schema |
| P9 free-form strings as RelSpec/PerturbSpec | schema |

Schema count: **10** (8 hardened + `reliability-spec` and `perturbation-spec`). All positive examples were migrated to the R4 contract and still validate. Cross-record semantics, negative fixtures, ReqPath derivation, and registry-generated surfaces all run at 0 failures.

## Invalid-record corpus

`tests/invalid/` — **28 fixtures**, each carrying expected-failure metadata (id, why, expected rejection layer, schema, instance). It covers every class reproduced in the read-only baseline audit plus the additional classes the R4 program named: unresolved residual without a queue, transferred without a receiver, claim dependency cycle, plural `of_type`, handoff state-claim missing `valid_for_version`, RelSpec declared after the result, PerturbSpec invariant also varied.

## Recursive/path-aware mutation testing — **completed**

`scripts/validate_recursive_mutations.py` walks every positive example part recursively and applies **18 operator families**. Deterministic; no randomness.

**Totals: 1,247 mutants generated · 1,113 killed at the schema layer · 125 killed at the semantic layer · 9 declared-equivalent · 0 unjustified survivors.**

Families: delete-nested-required · empty-required-string · empty-required-array-or-map · duplicate-unique-member · unknown-reference-id · analysis-version-mismatch · occurrence-version-mismatch · delete-disposition-conditional-field · claim-dependency-cycle · remove-required-verdict-status · contradict-pathway-summary · na-without-reason · plural-metaorthemma-type · empty-metaorthemma-binding · postdate-reliability-declaration · violate-perturbation-invariant · collapse-candidate-set-into-partial-profile (the B1 defect) · collapse-claim-path-into-episode-path (the B2 defect).

### Justified equivalent mutants (9), each with a stated reason

These are **not** survivors in the defect sense; each is a mutation that leaves the record making a different-but-well-formed claim, and each reason is declared in `mutation-spec.json`:

- **Residual redundancy (4 mutants):** a `validated-resolved` residual carrying *both* `evidence_refs` and `verdict_refs` still discharges its contract when one is deleted or emptied — the contract requires one of the two. Deleting **both** *is* killed.
- **Empty residual list (3 mutants):** a ledger that opens no burdens is well-formed. Catching this would require an external source of truth about which burdens actually existed — outside the reference model by construction. This is exactly the limit the whole-state-reread example states in prose: the machine floor can convict a closure claim asserted *over a recorded* unresolved burden, but not a burden nobody recorded.
- **Empty evidence on a `minimal` record (2 mutants):** the contract permits it precisely because a minimal record makes no audit claim; the same mutation on an **audit-ready** record *is* killed at the schema layer.

## Honest coverage limits

The operators are path-aware but finite and hand-declared; they exercise the contract's structure, not its adequacy to the world. The historical figure "208 mutants, 0 survivors" describes only the three earlier top-level operators (`drop-required`, `bad-enum`, `extra-field`) and must not be cited as semantic completeness — the current figure should not be either. What these results support is narrow and specific: **the shipped reference model rejects the malformed-record classes enumerated here, at a declared layer, deterministically.**
