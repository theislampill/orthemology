# R4 Review A — formal/type reviewer (adversarial)

> **CANDIDATE REVIEW — REQUIRES INDEPENDENT REVIEW.** Performed as a fresh read-only pass after the corresponding implementation phase, but by the same run that implemented it; it is therefore *not* the independent sign-off the R4 program requires. Model provenance is disputed and unresolved (see `../AUTONOMOUS-R4-STATE.json`).

**Posture: assume the formal repairs are wrong.**

| Attack | Result |
|---|---|
| Candidate/profile separation still leaky | `p̂` gloss now types exactly one partial profile; the bounded-set reading is withdrawn in the core and survives only in archived patches. **FIXED** |
| Claim/episode granularity confused | `ReqReason_q ⊆ ReqPath` projection with `ReasoningPathAdequate_q`; `PathwayAdequate(e)` retained separately; both representable in the verdict record. **FIXED** |
| Projection could be gamed post-outcome | Derivation inputs are fixed and recorded (claim dependencies, evidence IDs, governing tokens, governance rules, relevant procedure/execution); a post-hoc projection is a recorded, checkable defect rather than an invisible one. **MITIGATED, not eliminated** — an adversary controlling the record could still author a self-serving projection; this is stated, not hidden. |
| Analysis/actor indexing overstated | Full-index formulation adopted; indices required in the verdict schema. **FIXED** |
| Zero-burden token semantics ambiguous | One rule: material binding or no token. **FIXED** |
| Plural metaorthemma typing | Exactly one `of_type`; many-to-many marked unimplemented. **FIXED** |
| Result/pathway independence broken by the new predicate | Strict soundness remains derived, factive only via truth-linkage; `PathwayAdequate` remains non-factive; four cells intact. **HOLDS** |
| Closure aggregation | Definition-13 floor retained from R3. **HOLDS** |
| Multi-actor profile typing | Unchanged from R3; typed `Compat_m` intact. **HOLDS** |

**Residuals:** the projection-authoring risk above; and the open formal parameters (RequiredBy in general, evidence-class exhaustiveness, fusion non-uniqueness, Δ_A idealizations, many-to-many MetaInst) which remain **stated, not closed**.
