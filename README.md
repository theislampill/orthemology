# Orthemology

**Status: research-stage draft (R6); not peer reviewed; fresh-session repository review completed; not external human peer review; not empirically validated. Coined terminology is benchmark-gated, not adopted. See [STATUS.md](STATUS.md).**

Orthemology is a proposed theory of how concrete cases get correctly classified, handled, and audited by rule-governed processes — human, institutional, or automated. It gives first-class, auditable structure to a familiar but usually implicit architecture:

| Term (candidate) | Ordinary-language meaning | Pillar example |
|---|---|---|
| **orthemma** | the concrete situated case, with an identity key and version | this particular pillar, as it now stands |
| **ortheme** | a repeatable, consequence-bearing state-type the case may instantiate | *orthogonal to a declared reference plane within tolerance ε* |
| **metaortheme** | a repeatable higher-order governing standard or configuration | the standard fixing which reference frame, tolerance, instruments, calibration, evidence, and validation count |
| **metaorthemma** | the concrete, case-bound configuration token of that standard | *this* standard bound to *this* plane, tolerance, instrument, and calibration, for this pillar, now |
| **orthing** | the whole rule-governed handling process | identifying the pillar, applying the bound standard, gathering evidence, placing, validating, routing, closing |
| **orthing episode** | one dated, concrete run of that process (may contain several metaorthemmata) | the record of today's check on this pillar |

The final assertion ("this pillar is orthogonal") is a **placement claim** judged for correctness; the ortheme is the state-type itself.

## What to read

- **Current main manuscript:** [`manuscript/orthemma-ortheme-systems-revised-draft.md`](manuscript/orthemma-ortheme-systems-revised-draft.md) — the one current draft (*Orthemma–Ortheme Systems: An Analysis-Relative Architecture for Auditable Classification and Handling*); earlier renderings are superseded.
- **Current formal core:** [`theory/orthemic-core-formalization.md`](theory/orthemic-core-formalization.md), with the derived multi-actor extension in [`theory/orthemic-multi-actor-conflict-note.md`](theory/orthemic-multi-actor-conflict-note.md).
- **Normative registries:** [`docs/verdict-registry.yaml`](docs/verdict-registry.yaml) (verdict semantic IDs + display aliases) and [`docs/notation-registry.yaml`](docs/notation-registry.yaml) (symbol table) — both machine-enforced.
- **Worked case:** [`examples/compaction-stale-steer.md`](examples/compaction-stale-steer.md) (the stale-directive pattern) plus <!-- state:example-json-count -->nine<!-- /state:example-json-count --> machine-readable episode examples under [`examples/`](examples/) validated against [`schemas/`](schemas/).
- **Companion (metaphysical/theological — complete drafts, separate and firewalled):** [`companion/`](companion/README.md).
- **Terminology program (READY TO RUN, NOT RUN):** [`terminology/`](terminology/README.md).
- **Decision records:** [`docs/decisions/`](docs/decisions/) — <!-- state:decision-range -->0001–0019<!-- /state:decision-range -->: 0001–0003 (owner reconciliation R1), 0004–0008 (autonomous closure R2), 0009–0010 (type/token, soundness bearers, orthability senses — R3), 0011–0015 (claim-relative reasoning paths, reference-model semantic contract, source-status normalization, generated project state, latent-state boundary — R4), 0016–0017 (review-state contract, private-evidence boundary — R5), 0018–0019 (experiment-packet readiness/registration, current sourcing state — R6).
- **Generated project state:** [`docs/current-state.yaml`](docs/current-state.yaml) — the canonical machine-readable revision, counts, statuses, and burdens; VERSION/README/STATUS/OPEN-DECISIONS are checked against it in CI.
- **Sourcing:** [`references/orthemology.bib`](references/orthemology.bib) + [`docs/sourcing/`](docs/sourcing/) — per-claim verification statuses.
- **Closure accounting:** [`docs/project-closure/`](docs/project-closure/) — formal audit, counterexample ledger, reviews, burden ledger.
- **Reconciliation history:** [`archive/reconciliation/`](archive/reconciliation/) — exact patches, ledgers, and validation reports (immutable; retain pre-R2 notation by design).
- **Draft PDFs:** [`artifacts/`](artifacts/) — DRAFT-stamped, commit-pinned renderings with source-hash sidecars.

## Two ideas that carry the theory

**Result correctness is not pathway adequacy.** An episode's result can be right while the process that produced it was defective (the stopped-clock validator; the wrongly-calibrated check that happens to agree), and a genuinely reliable, correctly-run process can still miss a rare case. The verdict layer keeps these axes independent: V1 judges the placed result; a **result-free pathway core** (evidential support, configured-procedure truth-conduciveness, evidence currentness, rule/policy/token/execution adequacy, decision-time justification, route safety, closure truthfulness, robustness) judges the process. All four result × pathway combinations are representable, with deterministic fixtures proving it.

**Ground truth is analysis-relative.** Which state-types a case *truly* instantiates is defined relative to a declared, versioned **analysis** `A` (boundary, task, repertoires, loss, tolerance, representation and merger families): `O*(m; A)`. The familiar task-relative notation (`O*_T(m)`) survives only as explicitly scoped shorthand once a single analysis is fixed — it is an abbreviation, not a second ontology. The case itself and its worldly facts are not created by the analysis; only the state-type description is indexed.

## Honesty notes

- **No empirical experiment has validated the framework.** Every designed study is READY TO RUN, NOT RUN; deterministic fixtures and validators check consistency only. The internal records that motivated the design are private and not independently auditable; no public claim rests on them.
- **The coined vocabulary (orthemma/ortheme/metaortheme/metaorthemma/orthing) is candidate terminology**, gated on a designed-but-unrun comparative benchmark; every document can be read with ordinary-language substitutes.
- **The companion theological/metaphysical papers are complete drafts, deliberately separated** from the main manuscript: philosophical conclusions are conditional on labeled premises, creed-internal material is explicitly Atharī-school-labeled, and no engineering evidence supports any metaphysical claim (absolute firewall).
- **Related-work claims are cited with per-claim verification statuses** — current state starts at [`docs/sourcing/CURRENT-SOURCING-LEDGER.md`](docs/sourcing/CURRENT-SOURCING-LEDGER.md) (Decision 0019; R2 ledgers are banners-marked historical baselines); statuses are honest about what was and was not re-fetched.

## Citing

No stable release, DOI, or citation metadata exists (license and identity decisions are owner-only — see [OPEN-DECISIONS.md](OPEN-DECISIONS.md)). Cite by commit per [docs/CITING.md](docs/CITING.md).
