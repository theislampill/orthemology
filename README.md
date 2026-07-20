# Orthemology

**Status: research-stage draft. Not peer reviewed. No completed empirical validation. Coined terminology is benchmark-gated, not adopted. See [STATUS.md](STATUS.md).**

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

- **Current main manuscript:** [`manuscript/orthemma-ortheme-systems-revised-draft.md`](manuscript/orthemma-ortheme-systems-revised-draft.md) — the one current draft; earlier renderings are superseded.
- **Current formal core:** [`theory/orthemic-core-formalization.md`](theory/orthemic-core-formalization.md), with the derived multi-actor extension in [`theory/orthemic-multi-actor-conflict-note.md`](theory/orthemic-multi-actor-conflict-note.md).
- **Companion (metaphysical/theological, incomplete and separate):** [`companion/`](companion/README.md).
- **Terminology benchmark design (designed, not run):** [`terminology/`](terminology/README.md).
- **Decision records:** [`docs/decisions/`](docs/decisions/) — the three implemented reconciliation decisions.
- **Reconciliation history:** [`archive/reconciliation/`](archive/reconciliation/) — exact patches, ledgers, and validation reports.
- **Machine-checkable semantics:** [`tests/verdict-fixtures.json`](tests/verdict-fixtures.json) + [`scripts/validate_verdict_semantics.py`](scripts/validate_verdict_semantics.py).

## Two ideas that carry the theory

**Result correctness is not pathway adequacy.** An episode's result can be right while the process that produced it was defective (the stopped-clock validator; the wrongly-calibrated check that happens to agree), and a genuinely reliable, correctly-run process can still miss a rare case. The verdict layer keeps these axes independent: V1 judges the placed result; a **result-free pathway core** (evidential support, configured-procedure truth-conduciveness, evidence currentness, rule/policy/token/execution adequacy, decision-time justification, route safety, closure truthfulness, robustness) judges the process. All four result × pathway combinations are representable, with deterministic fixtures proving it.

**Ground truth is analysis-relative.** Which state-types a case *truly* instantiates is defined relative to a declared, versioned **analysis** `A` (boundary, task, repertoires, loss, tolerance, representation and merger families): `O*(m; A)`. The familiar task-relative notation (`O*_T(m)`) survives only as explicitly scoped shorthand once a single analysis is fixed — it is an abbreviation, not a second ontology. The case itself and its worldly facts are not created by the analysis; only the state-type description is indexed.

## Honesty notes

- **No empirical experiment has validated the framework.** All benchmark and fixture material is design only.
- **The coined vocabulary (orthemma/ortheme/metaortheme/metaorthemma/orthing) is candidate terminology**, gated on a designed-but-unrun comparative benchmark; every document can be read with ordinary-language substitutes.
- **The companion theological/metaphysical material is incomplete**, deliberately separated from the main manuscript, and makes no claim that engineering evidence supports metaphysics.
- **The citation apparatus is incomplete**; related-work claims await a sourcing pass.

## Citing

No stable release, DOI, or citation metadata exists yet (license and citation decisions are open — see [OPEN-DECISIONS.md](OPEN-DECISIONS.md)). If you need to reference this work, link to this repository and the commit hash.
