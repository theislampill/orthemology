# R4 schema and mutation report

> **CANDIDATE PASS — REQUIRES INDEPENDENT REVIEW.** This report states both what was completed and what was **not**; the incomplete items are named, not glossed.

## Baseline (independent probe, before)

Eleven malformed but theory-relevant records were submitted to the R3 schema layer and cross-record validator. **Ten were accepted by both layers.** One — a verdict record missing statuses for its required verdicts — was accepted at the schema layer but **caught** by cross-record pathway recomputation; the independent audit's phrasing on that sub-case was therefore slightly overstated, and this is recorded as a partial refutation rather than absorbed.

## After (same probe, hardened layer)

**0 of 11 accepted.** Every class is now rejected at a declared layer:

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

Schema count: **10** (8 hardened + `reliability-spec` and `perturbation-spec`). All 8 positive examples were migrated to the R4 contract and still validate. Cross-record semantics, negative fixtures, ReqPath derivation, and registry-generated surfaces all run at 0 failures.

## Mutation testing — **incomplete in this pass**

The R4 program specifies twenty recursive/path-aware operator families and a `tests/invalid/` corpus with expected-failure metadata. **Neither was completed.** What exists is the pre-existing suite:

| Operator family | Scope | Mutants | Survivors |
|---|---|---|---|
| `drop-required` | top-level required fields only | (per run) | 0 |
| `bad-enum` | top-level enum fields only | (per run) | 0 |
| `extra-field` | one undeclared top-level field | (per run) | 0 |

**Coverage limits, stated plainly:** these operators are top-level only. They do **not** exercise nested required fields, empty-string/empty-collection substitution, uniqueness violations, unresolved references, analysis/occurrence version mismatches, disposition-conditional deletions, dependency cycles, missing verdict statuses, summary/status contradictions, NA-without-reason, plural typing, empty bindings, post-dated reliability declarations, perturbation-invariant violations, candidate/partial-profile collapse, or claim/episode path collapse. The historical figure "208 mutants, 0 survivors" is retained **only** as a record of that narrow family and must not be repeated as evidence of semantic completeness.

**What compensates, partially:** the eleven-class probe above, the eleven committed negative fixtures (`tests/schema-negative/`), the ReqPath omission-attack fixture, and the LS-1…LS-7 anti-conflation assertions all target semantic content directly. That is a floor, not the specified engine.

## Residual work (named, with owner)

1. **`scripts/validate_recursive_mutations.py`** — the twenty-family path-aware engine with per-family reporting. *Not written.* Ordinary engineering work; not owner-blocked.
2. **`tests/invalid/`** — the expected-failure corpus with metadata. *Not written*; the eleven probe classes exist only in the ad-hoc probe script and the committed negative fixtures.
3. Per-family mutation scores and justified-equivalent-mutant accounting. *Not produced.*

An independent reviewer should treat R4's schema-contract claim as **supported** and its mutation-coverage claim as **explicitly incomplete**.
