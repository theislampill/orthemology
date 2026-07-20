# ER-2 — Episode-Reification Incremental-Value Test v2 (packet, NOT a run)

Corrected current packet (Decision 0020; supersedes the historical R6 `ER-1`,
preserved byte-frozen at [`../episode-reification/`](../episode-reification/)).
**No run has occurred; no result exists; nothing is externally registered.**
Canonical state: [`STATUS.yaml`](STATUS.yaml) /
[`../experiment-status.yaml`](../experiment-status.yaml).

- Protocol [`PROTOCOL.md`](PROTOCOL.md) · archetypes
  [`E1-E5-SPEC.yaml`](E1-E5-SPEC.yaml) · arm contract
  [`BASELINE-TREATMENT-CONTRACT.md`](BASELINE-TREATMENT-CONTRACT.md) · rubric
  [`SCORING-RUBRIC.md`](SCORING-RUBRIC.md) · decision rules
  [`DECISION-RULES.yaml`](DECISION-RULES.yaml)
- **Fixtures + hidden keys:** `fixtures/<case>/` (baseline log + treatment
  record from one canonical fact list) and `fixtures/KEYS.json` (scoring
  truth; never in a payload) from
  [`scripts/generate_cases.py`](scripts/generate_cases.py) — 5 archetypes × 4
  neutral variants = 20 cases
- **Run harness:** [`harness/run_er.py`](harness/run_er.py) — mock/cmd
  adapters, strict parser, one logged format retry, raw retention, payload
  audit; CI uses only the mock adapter
- **Corrected frozen analysis:**
  [`analysis/analyze_er2.py`](analysis/analyze_er2.py) — EQUALITY completion
  scoring, semantic E5/traceability, paired inference, Holm, harm rules,
  mechanical decision execution (non-synthetic only)
- Smoke tests (produce no result): [`tests/test_smoke.py`](tests/test_smoke.py)
- Freeze: [`FREEZE-HASH.txt`](FREEZE-HASH.txt)
