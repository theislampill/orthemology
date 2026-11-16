# ER-2 — Episode-Reification Incremental-Value Test v2 (packet, NOT a run)

Corrected current packet (Decision 0020; supersedes the historical R6 `ER-1`,
whose original frozen edition remains bound in the canonical experiment
state; [`../episode-reification/`](../episode-reification/) provides its
current reading and reproduction route).
**No run has occurred; no result exists; nothing is externally registered.**
Canonical state: [`STATUS.yaml`](STATUS.yaml) /
[`../experiment-status.yaml`](../experiment-status.yaml).

- Protocol [`PROTOCOL.md`](PROTOCOL.md) · archetypes
  [`E1-E5-SPEC.yaml`](E1-E5-SPEC.yaml) · arm contract
  [`BASELINE-TREATMENT-CONTRACT.md`](BASELINE-TREATMENT-CONTRACT.md) · rubric
  [`SCORING-RUBRIC.md`](SCORING-RUBRIC.md) · decision rules
  [`DECISION-RULES.yaml`](DECISION-RULES.yaml)
- **Public cases:** [`scripts/generate_cases.py`](scripts/generate_cases.py)
  retains 5 archetypes × 4 neutral variants = 20 cases. `public_files()`
  produces the 60 original public forms in memory. To inspect ordinary
  files, run it with `--output-dir "$TEMP_DIR"` for a temporary destination.
  The separate `fixtures/KEYS.json` scoring input remains outside prompt
  assembly; key regeneration requires the explicit `--include-scoring-keys`
  option and is not part of public rendering.
- **Run harness:** [`harness/run_er.py`](harness/run_er.py) — mock/cmd
  adapters, strict parser, one logged format retry, raw retention, payload
  audit; CI uses only the mock adapter
- **Corrected analysis:**
  [`analysis/analyze_er2.py`](analysis/analyze_er2.py) — EQUALITY completion
  scoring, semantic E5/traceability, paired inference, Holm, harm rules,
  mechanical decision execution (non-synthetic only). Public fact IDs come
  from the same seeded generator by default; `--facts-root` optionally
  selects an explicitly supplied rendering directory. Scoring truth stays
  a separate required input
- Smoke tests (produce no result): [`tests/test_smoke.py`](tests/test_smoke.py).
  `--public-only` checks the public facts and exact payload assembly without
  accessing keys, invoking a scorer, or running an adapter
- Original freeze: [`FREEZE-HASH.txt`](FREEZE-HASH.txt). The source revision
  and current consumer successor are bound in
  [`../experiment-status.yaml`](../experiment-status.yaml); the original
  frozen hash, readiness and registration states are unchanged
