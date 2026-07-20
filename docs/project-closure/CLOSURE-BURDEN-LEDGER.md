# Closure burden ledger (R2, 2026-07-20)

> **SUPERSEDED IN PART — R3 correction notice (2026-07-20).** Preserved verbatim as history. The R3 read-only audit re-dispositions several rows: #13 (companion type/token language under repair), #14/#23 (source verification is R3 work, not owner-only, until a documented accessibility failure), #15 (one Qurʾānic locus wrong: 20:11 → 20:11–12), #17 (v1 arms not matched as claimed), #19 (schemas accept malformed records; positive-only), #21 ("reproducible build" claim withdrawn — live timestamps, raw-Markdown leakage). The current ledger is `r3/R3-CLOSURE-BURDEN-LEDGER.md` (created at R3 closeout).

Every burden of the non-empirical orthemology lane, with exactly one honest disposition. Dispositions use the project's own residual taxonomy: **validated-resolved** (closed on in-scope, current, sufficient — here: deterministic — evidence), **deferred** (open with a declared trigger), **owner-assigned** (waiting on a decision/resource only the owner can supply), **risk-accepted** (left open under a recorded, accepted limitation). Nothing is transferred; nothing is unresolved-without-a-plan.

| # | Burden | Disposition | Evidence / trigger |
|---|---|---|---|
| 1 | D1/M1/O2 intact through R2 | **validated-resolved** | cross-document validator; decision records 0001–0003 untouched (empty diff vs R1) |
| 2 | D3 verdict registry + migration | **validated-resolved** | Decision 0004; `docs/verdict-registry.yaml` drives 57-check validator |
| 3 | D4 symbol table, machine-validated | **validated-resolved** | Decision 0005; `docs/notation-registry.yaml`; `validate_notation.py` 0 failures |
| 4 | O3 public worked case + formal placement | **validated-resolved** | Decision 0006; `examples/compaction-stale-steer.md`; fixture F6 |
| 5 | Π_A and partial-profile typing | **validated-resolved** | Decision 0007; manuscript Definition 10; core gloss |
| 6 | No undefined current symbols | **validated-resolved** | notation validator + Review A-2 |
| 7 | No undispositioned formal contradiction | **validated-resolved** | FORMAL-AUDIT-R2 (15 items) + Review A; 5 limitations explicitly acknowledged |
| 8 | Well-typed multi-actor compatibility | **validated-resolved** | audit item 11; example `multi-actor-compatibility.json` |
| 9 | Registry/schema/fixture/core/manuscript/overview agreement | **validated-resolved** | `validate_cross_document_consistency.py` 0 failures |
| 10 | Manuscript conclusion + references | **validated-resolved** | §16–§17 + References; 27 rendered entries |
| 11 | Load-bearing related-work claims cited or removed | **validated-resolved** | sourcing ledger 35 rows; Review B; two universals rescoped |
| 12 | Casebook no longer used as public validation | **validated-resolved** | abstract/§1.4/§11.4/§13.4/§15.2/availability statement |
| 13 | School-neutral companion complete draft | **validated-resolved** | `companion/orthability-and-the-ground-of-intelligibility.md` + objections ledger |
| 14 | Atharī companion complete, sourced, school-labeled draft | **validated-resolved** (with recorded source limitation, #23) | `companion/orthability-divine-attributes-and-speech-athari.md` |
| 15 | Arabic/Qurʾān created/uncreated corrections | **validated-resolved** | Atharī paper §1, §3.2, §4.1 (forbidden sentences + corrections) |
| 16 | Speech-capability argument separates reason/revelation | **validated-resolved** | school-neutral §8 boundary; Atharī §8 table |
| 17 | Terminology packet ready to run and clearly unrun | **validated-resolved** | pilot0 freeze hash; readiness report; STATUS wording |
| 18 | No term declared empirically adopted | **validated-resolved** | corpus-wide candidate labels; harm/three-outcome rules frozen |
| 19 | Schemas + examples validate | **validated-resolved** | `validate_schemas.py` 0 failures (8 schemas, 7 examples) |
| 20 | CI checks pass | **validated-resolved** | nine-step workflow green at the closure commit (see closure report for run id) |
| 21 | Draft PDFs / reproducible build | **validated-resolved** | 4 artifacts + sidecars; `build_pdfs.py --check` in CI |
| 22 | Public remote updated and freshly verified | **validated-resolved** | closure report: merge commit, Actions result, fresh-clone validation |
| 23 | Edition-level verification of `[via compilation]` classical loci; Ashʿarī/Māturīdī source for the comparative route | **owner-assigned / deferred** | requires acquiring printed editions; trigger: owner supplies or approves sources; flagged inline in the Atharī paper |
| 24 | Bibliographic re-check of RECORD-CONFIRMED rows | **deferred** | trigger: any external submission (ledger states this) |
| 25 | Legal license | **owner-assigned** | owner-only legal act |
| 26 | Author/citation identity; CITATION.cff; numbered release | **owner-assigned** | owner-only identity facts |
| 27 | Empirical execution (benchmark, fixtures-as-experiment, terminology pilots/confirmatory) | **owner-assigned** | spend + human raters + freeze decision; packets ready |
| 28 | External peer review / preprint / DOI | **owner-assigned** | owner-identity publication acts |
| 29 | Casebook publication (if ever) | **owner-assigned** | rights/privacy call; public corpus does not depend on it |
| 30 | Evidence-class exhaustiveness; RequiredBy calculus; fusion non-uniqueness; Δ_A idealizations | **risk-accepted** | acknowledged theoretical limitations (FORMAL-AUDIT-R2); revisit if practice surfaces a counterexample |

**Counts:** 22 validated-resolved · 1 deferred (#24) · 1 owner-assigned/deferred hybrid (#23) · 6 owner-assigned (#23 partially, #25–29) · 1 risk-accepted (#30).
