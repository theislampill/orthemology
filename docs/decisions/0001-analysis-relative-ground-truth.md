# Decision 0001 — Analysis-relative ground truth (D1)

**Date:** 2026-07-19 · **Decider:** project owner · **Implemented by:** Claude Fable 5 under owner direction · **Status:** implemented and promoted (reconciliation R1).

**Question.** How should the fibre of true orthemes be indexed — task-relative `O*_T(m)`, analysis-relative `O*_A(m)`, both at distinct levels, or one primitive with an abbreviation convention?

**Decision: (d)** — one analysis-relative primitive with a strictly scoped task-relative abbreviation. `Inst_A ⊆ M × O` is the primitive instantiation relation; the true profile is `O*(m; A)`; the declared analysis `A` is explicit and versionable (boundary, task, repertoires, loss, hard constraints, horizon, tolerance, representation family, merger family, governance boundary where relevant). `O*_T(m)` and the other task-subscripted spaces survive only as local scoped shorthand after one analysis with `task(A) = T` is explicitly fixed, and are forbidden wherever more than one analysis is live (audits, multi-actor evaluation, cross-version comparison, execution-vs-review). The occurrence and its worldly facts are analysis-independent; only the state-type description is indexed. Episode records carry the analysis identity and version; result correctness (V1) is judged against `O*(m; A(e))`. No task-to-analysis bridging law exists.

**Why.** The corpus previously carried both `O*_T` and `O*_A` as apparent primitives; every downstream object (V1, candidate families, profile spaces) inherited the ambiguity, and Definition 7's merger gap made task-only indexing ill-defined (two analyses can share a task while differing in tolerance or representation).

**Artifacts:** `archive/reconciliation/D1-COMPLETE-DIFFS.patch`, `D1-GROUND-TRUTH-CHANGE-LEDGER.md`, `D1-VALIDATION-REPORT.md`.
