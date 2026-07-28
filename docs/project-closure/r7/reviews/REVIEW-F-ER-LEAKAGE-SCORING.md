# R7 Review F — ER leakage and scoring audit

Surfaced model: `claude-opus-4-8`. Posture: attack E1, E5, traceability, labels, fact matching, treatment-only conclusions.

- E1 equality scoring reverted to the R6 or-bug — **DEFEATED** (smoke test unit-tests that refusing legitimate closure scores wrong + false-positive).
- Treatment fixture given a `binding_defect: true` flag — **DEFEATED** (label-free payload scan). Both arms are rendered from one canonical fact list; fact-atom parity is proven; the treatment adds structure/links, never a conclusion.
- E5 requires both neighbor verdicts + mismatch + correct remedy; traceability requires cited fact IDs to exist and intersect the supporting set (both unit-tested). No blocking findings.
