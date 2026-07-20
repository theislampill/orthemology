# CHANGELOG

## 2026-07-20 — autonomous closure revision (R2)

- **D3 closed** — verdict registry normalization: semantic IDs authoritative, display aliases in conceptual order (V3a→V3e chain), `V2b-P`/`V2b-T`, legacy migration table; registry drives validation ([0004](docs/decisions/0004-verdict-registry-normalization.md), `docs/verdict-registry.yaml`).
- **D4 closed** — symbol-table normalization: one role per symbol; `Γ_E`, `𝒢_{α,A_α}`, `GoalSchema`, `χ`/`L_A*`, `select_μ`, `estatus_e`, `ε_A`, `θ_stop`, `𝒬_e`; `App(e)` retired; machine-enforced ([0005](docs/decisions/0005-symbol-table-normalization.md), `docs/notation-registry.yaml`, `scripts/validate_notation.py`).
- **O3 closed** — stale-steer case note with the directive record and Exists/Authentic/Recovered/Authorized/InForce predicates; fixture F6 ([0006](docs/decisions/0006-compaction-stale-steer-placement.md), `examples/compaction-stale-steer.md`).
- **Π_A defined** — profile space + partial profiles as manuscript Definition 10 ([0007](docs/decisions/0007-profile-space-definition.md)); definitions renumbered.
- **Formal audit R2** — 15 type/definition repairs (incl. typed multi-actor compatibility, well-formed robustness `PerturbSpec`, edge-orientation convention, V1 aggregation, evidence-class subclassing); 16-pattern counterexample ledger; fixtures F6–F7 (`docs/project-closure/FORMAL-AUDIT-R2.md`, `COUNTEREXAMPLE-LEDGER-R2.md`).
- **Manuscript completed** as a publication-clean position-paper draft: retitled (analysis-relative), keywords, conclusion, data/materials availability, cited related work, AURC metric correction, casebook honesty (internal motivation, not validation).
- **Sourcing pass** — `references/orthemology.bib`, `docs/sourcing/SOURCING-LEDGER.md` + `CLAIM-SOURCE-MATRIX.md` with per-claim verification statuses.
- **Companion lane completed as drafts** — school-neutral transcendental paper (Thesis C replaced by C′, [0008](docs/decisions/0008-thesis-c-disposition.md)) and explicitly Atharī creed-internal paper; objections/replies ledger with the researched Hume disposition (OVERSTATED); companion sourcing ledger.
- **Terminology READY TO RUN, NOT RUN** — frozen Pilot 0 packet (arms A/B/C/C′; metaorthemma family; deterministic rubrics; packet hash), Pilot 1 + confirmatory templates.
- **Machine-readable layer** — 8 JSON schemas + 7 validated examples; validators for schemas, notation, claim sources, and cross-document consistency; CI expanded to nine checks.
- **Draft PDFs** — four artifacts with DRAFT status pages, commit/date stamps, and source-hash sidecars (`scripts/build_pdfs.py`; free embeddable fonts only).
- Historical records untouched: archived patches, R1 decision records, the frozen terminology v0 spec, and original provenance headers (moved verbatim to `docs/provenance/document-history.md`).

## 2026-07-19 — initial public state (reconciliation R1)

- Published the current validated corpus: formal core, main manuscript draft, multi-actor note, companion assessment/outline, terminology benchmark designs.
- Implemented, machine-validated, and promoted three owner decisions:
  - **D1** — analysis-relative ground-truth primitive `O*(m; A)` with strictly scoped task-relative shorthand ([decision record](docs/decisions/0001-analysis-relative-ground-truth.md));
  - **M1** — metaorthemma as an episode-local configuration token with verdict V3c ([decision record](docs/decisions/0002-metaorthemma-configuration-token.md));
  - **O2** — result-free pathway adequacy with the V2b^proc/V2b^tok split, governed applicability, four-valued statuses, and fixtures F1–F5 ([decision record](docs/decisions/0003-result-free-pathway-adequacy.md)).
- Added machine-checkable verdict semantics (`tests/verdict-fixtures.json`, `scripts/validate_verdict_semantics.py`; 29 deterministic checks) and repository validation with CI.
- Archived the exact reconciliation patches, ledgers, and validation reports under `archive/reconciliation/`.
