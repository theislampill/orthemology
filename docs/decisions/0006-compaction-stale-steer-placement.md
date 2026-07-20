# Decision 0006 — Compaction / stale-steer example placement (O3)

**Date:** 2026-07-20 · **Decider:** Claude Fable 5 under the owner's standing autonomy mandate (R2 closure) · **Status:** implemented.

**Question.** The theory needed a worked treatment of the "stale steer" pattern: a governing instruction is recovered (e.g., after context compaction or record recovery), is *authentic* — it really was issued — yet is no longer *in force*, and a system that follows it executes faithfully under a defective governing token. Where should this live: inline in the core, inline in the manuscript, or as a dedicated case note?

**Decision.** A dedicated public case note, [`examples/compaction-stale-steer.md`](../../examples/compaction-stale-steer.md), with only concise cross-references from the core and the manuscript. Rationale: the case needs a small formal apparatus of its own (the directive record and the five predicates `Exists`/`Authentic`/`Recovered`/`Authorized`/`InForce`) that would bloat either main text, while the verdict-layer consequences reduce to existing machinery (V2c, V3c, V3d, V5) and therefore need no new primitive.

**Consequences applied:**
- `examples/compaction-stale-steer.md` — the case note (directive record, five predicates, verdict mapping, privacy note);
- deterministic fixture **F6** in `tests/verdict-fixtures.json` (faithful execution + stale token: `EXECUTION_FAITHFUL` pass with `GOV_TOKEN_ADEQUATE` and `EVIDENCE_CURRENT` fail ⇒ `PathwayDefective`) — a combination no prior fixture witnessed;
- one compact paragraph in the manuscript's examples (§11.5) and one cross-reference row in the core's fixture table (§4.2).

**Non-decision.** No new verdict and no new episode component is introduced; the directive record is a domain object (a kind of orthemma whose profile includes governance states), not a seventh formal addition.
