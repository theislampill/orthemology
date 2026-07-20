# Architecture overview

One page on how the pieces fit; details in the formal core.

**Objects.** A domain `M` of concrete occurrences (orthemmata, each with identity `κ` and version `v`) and a repertoire `O` of state-types (orthemes). The primitive relation `Inst_A ⊆ M × O` is indexed by a declared, versioned analysis `A`; the true profile is the fibre `O*(m; A)`. Observation is separate from the occurrence (`x = Ω(m)`), and the inferred profile `p̂` is separate from both.

**Governance.** Metaorthemes `μ = ⟨g, S_μ, ε_μ, prov(μ), ver(μ)⟩` govern components (repertoire, individuation, evidence, disclosure, routing, validation, warrant) via meta-policies. Their concrete case-bound instantiations are metaorthemmata `μ̄` (binding map, scope, calibration provenance, binder-with-warrant, validity), collected per episode in `MetaTok(e)`.

**Episodes.** An orthing episode `e = ⟨id; m, κ, v; x, H; α, w, A, T, t; μ⃗, MetaTok, π; C⃗, p̂; r; ε; Q; δ; hand_in, hand_out; a, Succ⟩` is the auditable record: typed evidence, candidate families, placement, route, claim ledger, residual dispositions, handoffs, and labeled successor edges (placements do not transport across versions without lineage argument — "right finding, wrong copy" becomes a statable error).

**Verdicts.** Result: V1 (placement correctness against `O*(m; A(e))`), plus the factive claim-wise annotation V2b^tok. Pathway (result-free core): V2a evidential support; V2b^proc configured-procedure truth-conduciveness; V2c evidence currentness; V3 configuration adequacy; V3a policy adequacy; V3c governing-token adequacy; V3b executor fidelity; V3d decision-time justification; V4a route safety; V5 closure truthfulness; V6 robustness. V4b (near-optimality) is advisory. `ReqPath(e)` is governance-derived; statuses are four-valued; `PathwayAdequate/Defective/Undetermined` follow. Fixtures F1–F5 witness all four result × pathway cells.

**Levels.** Episodes reify into higher-audit occurrences (`ι_n : E^(n) ↪ M^(n+1)`), so yesterday's classification act can be today's audited case; multi-actor settings index everything per actor (`α, β`) under per-actor analyses `A_α`.
