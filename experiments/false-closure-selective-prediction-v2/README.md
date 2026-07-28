# FCSP-2 — False-Closure / Selective-Prediction Benchmark v2 (packet, NOT a run)

Corrected current packet (Decision 0020; supersedes the historical R6
`FCSP-1`, preserved byte-frozen at
[`../false-closure-selective-prediction/`](../false-closure-selective-prediction/)).
**No run has occurred; no result exists; nothing is externally registered.**
Canonical state: [`STATUS.yaml`](STATUS.yaml) /
[`../experiment-status.yaml`](../experiment-status.yaml).

- Protocol [`PROTOCOL.md`](PROTOCOL.md) · design [`DESIGN.yaml`](DESIGN.yaml) ·
  endpoints [`ENDPOINTS.yaml`](ENDPOINTS.yaml) · decision rules
  [`DECISION-RULES.yaml`](DECISION-RULES.yaml)
- **Neutral items + hidden keys:** `items/PUBLIC-ITEMS.json` (runner-visible
  facts only) and `items/KEYS.json` (scoring truth; never in a payload), both
  from the seeded generator
  [`scripts/generate_items.py`](scripts/generate_items.py)
- **Run harness:** [`harness/run_fcsp.py`](harness/run_fcsp.py) — mock/cmd
  adapters (provider interface cannot be instantiated here), strict parser,
  one logged format retry, raw retention, payload audit dump; CI uses only
  the mock adapter
- **Complete frozen analysis:**
  [`analysis/analyze_fcsp2.py`](analysis/analyze_fcsp2.py) — every declared
  endpoint, paired permutation + bootstrap CIs + Holm, harm rules, mechanical
  decision execution (non-synthetic runs only)
- Pre-run sensitivity plan:
  [`simulation/design_sensitivity.py`](simulation/design_sensitivity.py)
- Smoke tests (produce no result): [`tests/test_smoke.py`](tests/test_smoke.py)
- Freeze: [`FREEZE-HASH.txt`](FREEZE-HASH.txt)
