# ER-1 — Episode-Reification Incremental-Value Test (packet, NOT a run)

The historical deterministic, preregistration-ready design for manuscript §13.2.
Its original frozen edition and failed-method status remain bound to the
source revision in [`../experiment-status.yaml`](../experiment-status.yaml).
The current generator and smoke reader are an explicitly bound consumer
successor; they preserve the original public case bytes.
**No run has occurred; no result exists; nothing here is evidence for any
claim.** Canonical state: [`STATUS.yaml`](STATUS.yaml) and
[`../experiment-status.yaml`](../experiment-status.yaml) (Decision 0018).

- Protocol: [`PROTOCOL.md`](PROTOCOL.md) · case family:
  [`E1-E5-SPEC.yaml`](E1-E5-SPEC.yaml) · arm contract:
  [`BASELINE-TREATMENT-CONTRACT.md`](BASELINE-TREATMENT-CONTRACT.md) ·
  rubric: [`SCORING-RUBRIC.md`](SCORING-RUBRIC.md) · decision rules:
  [`DECISION-RULES.yaml`](DECISION-RULES.yaml)
- Public cases: [`scripts/generate_fixtures.py`](scripts/generate_fixtures.py)
  retains the five canonical fact sets and their counterexamples.
  `public_files()` renders all 15 original public forms in memory. For
  ordinary files, run the generator with `--output-dir "$TEMP_DIR"`, where
  `TEMP_DIR` names a temporary destination. Tests use these same public
  forms without requiring committed generated copies.
- Original analysis: [`analysis/analyze_er.py`](analysis/analyze_er.py);
  deterministic smoke tests (produce no result):
  [`tests/test_smoke.py`](tests/test_smoke.py). Its `--public-only` mode
  checks generation and fact coverage without scoring or a synthetic run.
- Original freeze: [`FREEZE-HASH.txt`](FREEZE-HASH.txt); current consumer
  bindings are checked separately without changing that hash or the
  historical correction. A Git freeze is **not** an
  external preregistration; registry submission is an owner/external act.
