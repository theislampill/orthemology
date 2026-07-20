# CHANGELOG

## 2026-07-19 — initial public state (reconciliation R1)

- Published the current validated corpus: formal core, main manuscript draft, multi-actor note, companion assessment/outline, terminology benchmark designs.
- Implemented, machine-validated, and promoted three owner decisions:
  - **D1** — analysis-relative ground-truth primitive `O*(m; A)` with strictly scoped task-relative shorthand ([decision record](docs/decisions/0001-analysis-relative-ground-truth.md));
  - **M1** — metaorthemma as an episode-local configuration token with verdict V3c ([decision record](docs/decisions/0002-metaorthemma-configuration-token.md));
  - **O2** — result-free pathway adequacy with the V2b^proc/V2b^tok split, governed applicability, four-valued statuses, and fixtures F1–F5 ([decision record](docs/decisions/0003-result-free-pathway-adequacy.md)).
- Added machine-checkable verdict semantics (`tests/verdict-fixtures.json`, `scripts/validate_verdict_semantics.py`; 29 deterministic checks) and repository validation with CI.
- Archived the exact reconciliation patches, ledgers, and validation reports under `archive/reconciliation/`.
