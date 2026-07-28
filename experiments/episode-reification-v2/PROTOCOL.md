# ER-2 — Episode-Reification Incremental-Value Test: Protocol (v2)

**Packet:** `ER-2` (supersedes the historical R6 `ER-1`, whose scoring/leakage defects are recorded in Decision 0020) · **Status:** `STATUS.yaml` / `../experiment-status.yaml` · **No run has occurred; nothing is externally registered.**

## 1. Question and unit

Does an explicit occurrence-anchored episode/verdict record improve pathway-defect discovery, correct remedy selection, completion-decision correctness, and audit traceability over a matched ordinary audit record carrying the same facts? **Unit of inference: the case, paired across arms**; the five archetypes A1–A5 are strata with four neutral surface variants each (20 cases). Repeats are within-case replicates (Decision 0020; deterministic reruns add no independent information).

## 2. Arms, fact source, and information match (audit B8/H1/H2 repair)

`scripts/generate_cases.py` (seed 20260733) renders ONE canonical fact-atom list per case into both arms: baseline chronological log, treatment explicit sectioned/linked record. The treatment adds organization and links only — no diagnostic titles, no defect flags, no interpretation-bearing notes. `fixtures/KEYS.json` holds the hidden scoring truth. `BASELINE-TREATMENT-CONTRACT.md` fixes the match; `tests/test_smoke.py` proves fact-atom parity and label-free payloads.

## 3. Execution

`harness/run_er.py`: mock (offline, deterministic — CI only) and cmd adapters; a provider interface that cannot be instantiated here. Prompts assemble ONLY from the public renderings + frozen probes; the harness never opens KEYS.json. Strict JSON parsing with one logged format retry; failures recorded; raw retained; manifest first.

## 4. Scoring and inference (audit B6/B7/B9 repair)

`SCORING-RUBRIC.md` + `analysis/analyze_er2.py`: completion scored by EQUALITY (`endorse_completion == closure_legitimate` — the ER-1 E1 fix); traceability verifies cited fact IDs exist and intersect the supporting set; E5 requires both neighbor verdicts, mismatch identification, and the correct remedy. Paired case-level arm-swap permutation tests, bootstrap CIs, Holm over the two primaries (defect discovery; completion correctness), E1 false-positive and cost-ratio harm rules, failed-run gate, mechanical decision execution (`DECISION-RULES.yaml`). Synthetic runs adjudicate nothing.
