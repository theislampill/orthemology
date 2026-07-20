# FCSP-1 — False-Closure / Selective-Prediction Benchmark (packet, NOT a run)

The frozen, deterministic, preregistration-ready packet for manuscript §13.1.
**No run has occurred; no result exists; nothing here is evidence for any
claim.** Canonical machine-readable state: [`STATUS.yaml`](STATUS.yaml) and
[`../experiment-status.yaml`](../experiment-status.yaml) (Decision 0018).

- Protocol: [`PROTOCOL.md`](PROTOCOL.md) · design: [`DESIGN.yaml`](DESIGN.yaml) ·
  endpoints: [`ENDPOINTS.yaml`](ENDPOINTS.yaml) · decision rules:
  [`DECISION-RULES.yaml`](DECISION-RULES.yaml)
- Items: [`items/ITEMS.json`](items/ITEMS.json) — 40 synthetic public scenarios
  from the frozen seeded generator [`scripts/generate_items.py`](scripts/generate_items.py);
  no private-record dependency.
- Arms: [`baselines/BASELINE-ARM.md`](baselines/BASELINE-ARM.md) /
  [`treatments/TREATMENT-ARM.md`](treatments/TREATMENT-ARM.md) — ordinary
  language; coined vocabulary is not a confound.
- Frozen analysis: [`analysis/analyze_fcsp.py`](analysis/analyze_fcsp.py);
  synthetic power simulation (labeled, not pilot evidence):
  [`simulation/power_sim.py`](simulation/power_sim.py).
- Deterministic smoke tests (produce no result):
  [`tests/test_smoke.py`](tests/test_smoke.py).
- Deviations (empty until a run): [`DEVIATION-LEDGER.md`](DEVIATION-LEDGER.md).
- Freeze: [`FREEZE-HASH.txt`](FREEZE-HASH.txt) — any post-freeze edit is a new
  packet version. A Git freeze is **not** an external preregistration;
  registry submission is an owner/external act.
