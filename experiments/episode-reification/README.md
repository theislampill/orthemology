# ER-1 — Episode-Reification Incremental-Value Test (packet, NOT a run)

The frozen, deterministic, preregistration-ready packet for manuscript §13.2.
**No run has occurred; no result exists; nothing here is evidence for any
claim.** Canonical state: [`STATUS.yaml`](STATUS.yaml) and
[`../experiment-status.yaml`](../experiment-status.yaml) (Decision 0018).

- Protocol: [`PROTOCOL.md`](PROTOCOL.md) · case family:
  [`E1-E5-SPEC.yaml`](E1-E5-SPEC.yaml) · arm contract:
  [`BASELINE-TREATMENT-CONTRACT.md`](BASELINE-TREATMENT-CONTRACT.md) ·
  rubric: [`SCORING-RUBRIC.md`](SCORING-RUBRIC.md) · decision rules:
  [`DECISION-RULES.yaml`](DECISION-RULES.yaml)
- Fixtures: [`fixtures/`](fixtures/) — one canonical fact set per case,
  rendered to both arms by the frozen generator
  [`scripts/generate_fixtures.py`](scripts/generate_fixtures.py); all
  synthetic and public.
- Frozen analysis: [`analysis/analyze_er.py`](analysis/analyze_er.py);
  deterministic smoke tests (produce no result):
  [`tests/test_smoke.py`](tests/test_smoke.py).
- Freeze: [`FREEZE-HASH.txt`](FREEZE-HASH.txt). A Git freeze is **not** an
  external preregistration; registry submission is an owner/external act.
