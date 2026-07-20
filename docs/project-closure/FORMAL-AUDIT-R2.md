# Formal audit R2 — three passes over the current theory corpus

**Date:** 2026-07-20 · **Auditor:** Claude Fable 5 (R2 autonomous closure) · **Scope:** `theory/orthemic-core-formalization.md`, `manuscript/orthemma-ortheme-systems-revised-draft.md`, `theory/orthemic-multi-actor-conflict-note.md`, `docs/architecture-overview.md`, `docs/glossary.md`, `tests/verdict-fixtures.json`, schemas, `examples/`. **Status:** all listed repairs are implemented in this revision; open items are explicitly dispositioned. Deterministic validation only; nothing here is an empirical claim.

## Pass 1 — type and definition audit

| # | Item | Finding | Disposition |
|---|---|---|---|
| 1 | `Inst_A` domain/codomain | Domain and repertoire were written `M`, `O` with the analysis-dependence implicit | **Repaired**: universal universes `𝓜, 𝓞`; analysis-active `M_A ⊆ 𝓜`, `O_A ⊆ 𝓞`; `Inst_A ⊆ M_A × O_A`; unsubscripted forms licensed scoped shorthand (Decision 0005). An analysis-changing repertoire now visibly changes `O_A` and hence `ver(A)` |
| 2 | Complete vs partial profiles | `Π_A` used without a definition site; `p̂` untyped between complete and partial | **Repaired**: manuscript Definition 10 defines `Π_A`, `Π_A^∂`, exclusivity-marked axes, co-holding components, cross-axis consistency constraints; `p̂ ∈ Π_A^∂`; candidate sets `Ĉ ⊆ Π_A`; candidate-set ≠ one-vague-profile non-conflation rule (Decision 0007) |
| 3 | Observation vs occurrence | Already sound; per-actor `Ω_α` in multi-actor contexts | **Verified, no change** |
| 4 | Metaortheme / meta-policy / metaorthemma / execution | Four layers present (Decision 0002); token identity, binder ≠ executor, validity/expiry/supersession in the token record | **Verified**; supersession semantics for governing *instructions* now worked out in `examples/compaction-stale-steer.md` (Decision 0006) |
| 5 | Claim and burden ledgers | Residual dispositions lacked an explicit exclusivity/precedence rule; "type error" language read as type-theoretic | **Repaired**: Definition 12 states mutual exclusivity by fiat + owner-assigned/transferred precedence rule; Definition 13 qualifies "type error" as a record/schema well-formedness violation |
| 6 | Verdict aggregation | Episode-level V1's aggregation over claims was undefined; a false claim's V2b-T was written "fails/unavailable" | **Repaired**: V1 bullet states claim-wise base + conjunction aggregation (no averaging); F3 row states a false claim's truth-linkage verdict *fails* by factivity, never "unavailable" absent a declared rule |
| 7 | `PROCEDURE_RELIABLE` | `RelSpec_q` already carries reference class, stratum, metric, threshold, protocol, evidence, version/validity; pre-outcome fixing; one-lucky-result exclusion | **Verified, no change** |
| 8 | Robustness | "V1 failure rate over `N(e)`" was undefined for infinite neighborhoods; rebinding under version perturbation unstated | **Repaired**: `PerturbSpec` (varied fields, invariant fields, generator, size/measure, tolerance); robust(e) = finite empirical proportion over an enumerated neighborhood OR probability under a declared measure; metaorthemma rebinding rule (unre-bindable token ⇒ perturbation inadmissible, reportable under V3c) |
| 9 | Applicability | Governance-derived `ReqPath(e)`, four-valued statuses, recorded reasons; `App(e)` retired (Decision 0005) | **Verified/completed**; vacuous adequacy blocked by "not tested is not not-applicable" + F5 |
| 10 | Composite episodes | Edge-direction convention was ambiguous ("supersession edge *to* its predecessor" vs "edges point forward in time") | **Repaired**: one orientation (earlier → later), semantics on labels, in core §5.2 and manuscript §9.2; fusion analyses already required to be explicitly declared |
| 11 | Multi-actor compatibility | `Compat`/`Conflict` compared target sets from different profile spaces informally | **Repaired**: `Compat_m(𝒢_α, 𝒢_β) iff ∃m′ ∈ Reach(m): O*(m′; A_α) ∈ 𝒢_α ∧ O*(m′; A_β) ∈ 𝒢_β`; cooperation = shared analysis + shared set or explicit alignment map `φ`; applied in core §5.3, manuscript §10.5, and the note |
| 12 | Metaortheme state selection | Partition of `S_μ` was silently assumed | **Repaired**: states need not partition unless declared; `select_μ` partial, may return several states or undetermined; undeclared-partition assumption is a V3a defect |
| 13 | Evidence classes | "exactly these three" claimed exhaustiveness | **Repaired**: three *core cross-domain* classes with permitted declared domain-specific subclasses; exhaustiveness labeled a working hypothesis; authorization/warrant remain outside evidence |
| 14 | Route composition | Conflict, priority, hard-constraint dominance, no-route-from-unresolved-factor already present (§5.3) | **Verified, no change** |
| 15 | Analysis relativity | Anti-relativism and version transport were implicit | **Repaired**: §2.6 paragraph — declared public index, objective once fixed; `ver(A)` transport requires a declared transport argument |

## Pass 2 — contradiction and counterexample audit

Every counterexample attempted is recorded with its representability verdict in [`COUNTEREXAMPLE-LEDGER-R2.md`](COUNTEREXAMPLE-LEDGER-R2.md). Summary: 16/16 target patterns representable; 2 required new deterministic fixtures (F6 stale directive; F7 safe-not-best route), 1 required the Pass-1 item-11 repair (different profile spaces with compatible goals), the rest were already witnessed by F1–F5 or by existing definitions. No pattern required a new primitive; no terminology was added to name an already-representable case.

## Pass 3 — mathematical and prose audit

- **Variables defined before use:** verified against the notation registry; the two gaps found (`Π_A` definition site; `Reach(m)` used informally) are closed by Definition 10 and the item-11 repair, which introduces `Reach(m)` explicitly at both use sites.
- **Quantifier scope:** the V3c conjunction, PathwayAdequate/Defective/Undetermined definitions, and Compat/Conflict predicates carry explicit quantifiers; no bare "for all" over an undeclared domain remains in the current corpus.
- **Theorem labeling:** the three inherited results are labeled inherited with no new-theorem claim; the ANDON proposition is labeled a proposition with its (one-line) argument; nothing is labeled "theorem".
- **"Established by construction":** replaced by "consistency shown by construction" in the evidence-tier table; remaining "by construction" instances assert constructive facts (acyclicity of a dated-token graph; definitional exclusions), which is their correct use.
- **No empirical conclusion from deterministic fixtures:** validators print an explicit disclaimer; §13/§15 restate it; checked.
- **Novelty claims bounded:** §8.6/§12 concede facet-by-facet; the residual claim is the union/lifecycle/joint-verdict object; no "no prior system can represent X" claim survives (see also the sourcing pass and Review B).
- **Casebook reliance:** the 33-case casebook and the longitudinal record are now described as internal, not independently auditable, design motivation — not validation (abstract, §1.4, §11.4, §13.4, §15.2).
- **Core/manuscript agreement:** verdict table, core-path membership, fixture list, episode signature, and shorthand convention cross-checked after normalization; `scripts/validate_cross_document_consistency.py` automates the load-bearing agreements.
- **No provisional aliases remain:** enforced by `scripts/validate_notation.py` (0 failures at this revision).

## Acknowledged remaining theoretical limitations

1. The exhaustiveness of the three core evidence classes is a working hypothesis (item 13), deliberately not a theorem.
2. `RequiredBy(·)` (governance derivation of `ReqPath`) is specified by its minimum derivation rules plus governance declaration, not by a closed-form calculus; a full governance calculus is out of scope for this revision.
3. The merger-gap quantity `Δ_A` presupposes a declared loss and representation family and inherits their idealizations; the rate–distortion analogue remains demoted.
4. Composite-episode fusion rules are constrained (declared, well-defined, not last-node) but not uniquely determined; different governance regimes may declare different fusions.
5. Nothing in this audit is empirical validation; the three designed studies (manuscript §13) remain unrun.
