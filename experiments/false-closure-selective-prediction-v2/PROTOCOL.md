# FCSP-2 — False-Closure / Selective-Prediction Benchmark: Protocol (v2)

**Packet:** `FCSP-2` (supersedes the historical R6 `FCSP-1`, whose methods defects are recorded in Decision 0020) · **Status:** `STATUS.yaml` / `../experiment-status.yaml` · **No run has occurred; nothing is externally registered** (a Git freeze is not a preregistration; Decision 0018).

## 1. Question and estimand

Does the manuscript §§5/7 machinery (explicit live-alternative maintenance, evidence scope/currentness checking, identity/version checking, admissible routing, per-burden closure) reduce false closure and improve selective-prediction behaviour over a matched ordinary baseline, at matched information and budget? **Unit of inference: the ITEM, paired across arms**; repeats are within-item technical replicates averaged before inference (temperature-0 reruns add no independent information — DESIGN.yaml). Primary estimands: paired item-level contrasts in false-closure rate and item-level AURC over the frozen 50-item set under the recorded executor configuration. No generalization beyond that population is licensed.

## 2. Arms

Frozen ordinary-language instructions, length-band-matched (±15%), zero coined vocabulary: `baselines/BASELINE-ARM.md` / `treatments/TREATMENT-ARM.md`.

## 3. Items, keys, and isolation (audit B5/G2 repair)

`scripts/generate_items.py` (seed 20260728) emits **PUBLIC-ITEMS.json** (neutral facts only — dates, identities, versions, scope lines, procedure rows, obligation rows; a defect is inferable, never stated) and **KEYS.json** (hidden family labels + scoring truth). The harness (`harness/run_fcsp.py`) assembles prompts ONLY from the public file and the arm instruction — it never opens KEYS.json — and can dump every exact payload for audit. `tests/test_smoke.py` proves payload isolation (no key/label/truth token in any payload), lexical + field-name leakage scans, regeneration equality, and a full mock end-to-end (harness → parser → analysis → report) with no adjudicated outcome. 8 substantive families × 5 items + 10 negative controls = 50 items; families are strata.

## 4. Execution

`harness/run_fcsp.py`: adapters `mock` (deterministic, offline; the ONLY adapter CI uses), `cmd` (user-supplied executor command), and a provider INTERFACE that cannot be instantiated here (no credentials, no live calls — an owner-authorized run act). Strict JSON parsing with ONE logged format retry; failed item-repeats recorded, never dropped; raw outputs retained; the manifest is written before the first call.

## 5. Endpoints, inference, decision

`ENDPOINTS.yaml` — all implemented in `analysis/analyze_fcsp2.py` (audit B2 repair): both primaries with paired arm-swap permutation tests, percentile bootstrap CIs over items, and Holm adjustment; every declared secondary; excess AURC; family and leave-one-family-out sensitivity; failed-run worst-case bounds; mechanical execution of `DECISION-RULES.yaml` for non-synthetic runs. The sensitivity plan is fixed pre-run (`simulation/design_sensitivity.py`, item-level units); **no observed-power rescue exists** (audit B4 repair).
