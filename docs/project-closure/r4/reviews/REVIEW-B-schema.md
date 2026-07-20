# R4 Review B — schema/reference-contract reviewer (adversarial)

> **CANDIDATE REVIEW — REQUIRES INDEPENDENT REVIEW.** Performed as a fresh read-only pass after the corresponding implementation phase, but by the same run that implemented it; it is therefore *not* the independent sign-off the R4 program requires. Model provenance is disputed and unresolved (see `../AUTONOMOUS-R4-STATE.json`).

**Posture: assume the hardened schemas still admit nonsense.**

Baseline: an independent probe found **10 of 11** malformed classes accepted by both layers. Each is now rejected at a declared layer (schema or cross-record semantics); see `../R4-SCHEMA-AND-MUTATION-REPORT.md` for the per-class table and the mutation operator families with their coverage limits.

**Attacks attempted beyond the committed fixtures:** empty constitutive fields; missing disposition-conditional fields; unresolved references; dependency cycles; summary/status contradictions; invalid NA handling; underdeclared analysis; skeletal audit-ready episodes; fake corroboration independence.

**Residual findings (kept, not absorbed):**
1. Conditional structure that JSON Schema cannot express is enforced at the **semantic** layer; this is a declared division of labour, so a consumer validating with a bare JSON-Schema library gets weaker guarantees than CI does. Stated in the report.
2. `tests/invalid/` proves rejection of *enumerated* classes; it is a floor, not a proof of exhaustiveness.
3. Mutation operators are path-aware but still finite and hand-declared; per-family reporting replaces the misleading single-number headline, and the limits are printed.
